from fastapi import APIRouter
from fastapi import Depends,HTTPException

from app.schemas.v1_student import *
from app.schemas.v1_payment import *
from app.models.v1_student import *
from app.models.v1_payment import *
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.database import get_db
from sqlalchemy import and_

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
from sqlalchemy import text
from sqlalchemy import func, case, and_
from app.dependencies import get_current_user


router = APIRouter()

@router.get("/erp/v1/student/fees/online/pending",tags=["Student Online Payment Version 1"])
def get_online_payment(stu_key: str, class_id: str, db: Session = Depends(get_db),
                       current_user: str = Depends(get_current_user)):
    query = text("""
    SELECT 
        mandatoryflg,
        feeid,
        onlinefname,
        fee_duedate,
        pendingamt,
        fps_fineperday,
        fps_maxfine,
        actfineamt,
        ROUND(((actfineamt + pendingamt) * fps_minamount / 100),2) fps_minamount,
        (actfineamt + pendingamt) payamt,
        fps_disper,
        ((pendingamt) * fps_disper / 100) AS disamount,
        a.stu_regno,
        a.stu_ID,
        a.stu_name,
        a.stu_mobile,
        a.stu_email,
        (SELECT MAX(docno) FROM hcas.b2e_tbl_col_feeledger) AS docno,
        a.docdate,
        a.doctype,
        a.counterid,
        a.srcid,
        a.srcdtlid,
        a.plusminus,
        a.status,
        a.remarks,
        stu_year,
        stu_acdyear,
        curtype,
        curvalue
    FROM
        (SELECT 
            b.mandatoryflg,
                a.feeid,
                onlinefname,
                DATE_FORMAT(fps_duedate, '%d/%m/%Y') fee_duedate,
                SUM(crdramt) AS pendingamt,
                fps_fineperday,
                fps_maxfine,
                CASE
                    WHEN SUM(crdramt) > 0
                    THEN (
                        CASE
                            WHEN DATEDIFF(NOW(), fps_duedate) * fps_fineperday > fps_maxfine THEN fps_maxfine
                            ELSE CASE
                                WHEN DATEDIFF(NOW(), fps_duedate) * fps_fineperday > 0 THEN DATEDIFF(NOW(), fps_duedate) * fps_fineperday
                                ELSE 0
                            END
                        END
                    )
                    ELSE 0
                END AS actfineamt,
                fps_minamount,
                fps_disper,
                s.stu_regno,
                s.stu_ID,
                s.stu_name,
                s.stu_mobile,
                s.stu_email,
                c.docno,
                c.docdate,
                c.doctype,
                c.counterid,
                c.srcid,
                c.srcdtlid,
                c.plusminus,
                c.status,
                c.remarks,
                '1' AS curtype,
                '1.00' AS curvalue,
                stu_year,
                stu_acdyear
        FROM
            b2e_tbl_col_feeledger
        INNER JOIN b2e_tbl_id_stu_personal_info s ON stu_KEY = studid
        INNER JOIN b2e_tbl_col_feedetail a ON a.feeid = b2e_tbl_col_feeledger.feeid
        INNER JOIN b2e_tbl_col_feepaysettings b ON b.fps_feeid = a.feeid
            AND s.stu_classid = b.fps_classid,
            (SELECT 
                MAX(docno) docno,
                    MAX(docdate) docdate,
                    'Journal' doctype,
                    '20' counterid,
                    MAX(srcid) srcid,
                    MAX(srcdtlid) srcdtlid,
                    'M' plusminus,
                    a.status,
                    s.stu_id,
                    'online payment' remarks
            FROM
                b2e_tbl_col_feeledger a, b2e_tbl_id_stu_personal_info s
            WHERE
                stu_KEY = :stu_key
                    AND stu_classid = :class_id
                    AND s.stu_KEY = a.studid
            GROUP BY a.status , s.stu_id) c
        WHERE
            b2e_tbl_col_feeledger.status = '0'
                AND stu_KEY = :stu_key
                AND stu_classid = :class_id
                AND onlinepay = '1'
                AND c.stu_id = s.stu_id
        GROUP BY mandatoryflg , feeid , onlinefname , fps_duedate , fps_fineperday , fps_maxfine , fps_minamount , fps_disper , curtype , curvalue , stu_year , stu_acdyear , (
            CASE
                WHEN DATEDIFF(NOW(), fps_duedate) * fps_fineperday > fps_maxfine THEN fps_maxfine
                ELSE CASE
                    WHEN DATEDIFF(NOW(), fps_duedate) * fps_fineperday > 0 THEN DATEDIFF(NOW(), fps_duedate) * fps_fineperday
                    ELSE 0
                END
            END
        ) , c.docdate , c.doctype , c.counterid , c.srcid , c.srcdtlid , c.plusminus , c.status , c.remarks) a
    WHERE
        pendingamt > 0
    ORDER BY feeid DESC;
    """)

    result = db.execute(query, {"stu_key": stu_key, "class_id": class_id}).mappings().all()
    return {"paymentlist": [dict(row) for row in result]}



@router.post("/erp/v1/student/payment/process",tags=["Student Online Payment Version 1"])
def process_online_payment(data: feeOnlinePayment, db: Session = Depends(get_db),
                           current_user: str = Depends(get_current_user)):

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    # Extract request data
    merchant_txn_id = data.merchant_txn_id
    txndt = data.txndt
    txnstatus = data.txnstatus  # SUCCESS or FAILED
    totalamt = data.totalamt
    trackid = data.trackid
    stuid = data.stuid
    studentadminid = data.studentadminid
    # paydetails = data.paydetails
    uniqueid = data.uniqueid  # raw string now

    # Step 1: Find the transaction record
    txn = db.query(StudentTransactionHistory).filter(StudentTransactionHistory.txn_id == merchant_txn_id).first()
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # Step 2: Update transaction history
    txn.response_code = txndt
    txn.status = txnstatus
    txn.amount = totalamt
    txn.txn_ref = trackid
    txn.updated_at = current_time
    txn.created_at = current_time

    db.commit()

    # Step 3: Always insert into FeeOnlinePayment and FeeOnlinePaymentInput
    sequenceno = datetime.utcnow().strftime("%Y%m%d%H%M%S") + str(stuid)
    banktokenid = txn.approval_refno  # approval_refno from history table

    # Insert into FeeOnlinePayment
    fee_payment = FeeOnlinePayment(
        fop_tranno=sequenceno,
        fop_date=datetime.utcnow(),
        fop_banktokenid=banktokenid,
        fop_bankrefno=trackid,
        fop_totalamt=totalamt,
        fop_stdkey=stuid,
        fop_stdrefno=studentadminid,
        fop_status=txnstatus.upper(),  
        createdby=studentadminid,
        createdon=datetime.utcnow(),
    )
    db.add(fee_payment)

    # Insert into FeeOnlinePaymentInput
    fee_input = FeeOnlinePaymentInput(
        fopt_tranno=sequenceno,
        fopt_json=uniqueid,  # raw string
        tcreatedby=studentadminid,
        tcreatedon=datetime.utcnow(),
    )
    db.add(fee_input)
    db.commit()

    return {
        "message": f"Payment {txnstatus.upper()}.",
        "txn_id": merchant_txn_id,
        "status": txnstatus.upper()
    }


@router.post("/erp/v1/student/payment/initiate", tags=["Student Online Payment Version 1"])
def initiate_online_payment(data: hcas_onlinepayment, db:Session = Depends(get_db),
                            current_user: str = Depends(get_current_user)):

    hcas_paymentinsert = HcasOnlinePayment (
        uuid = data.uuid,
        json_payload_readable = data.json_payload_readable,
        json_payload = data.json_payload,
        bank_transaction_id = data.bank_transaction_id,
        bank_ref_date = data.bank_ref_date,
        admission_no = data.admission_no
    )

    db.add(hcas_paymentinsert)
    db.commit()
    db.refresh(hcas_paymentinsert)

    return{
        "message": "data inserted successfully"
    }


@router.post("/erp/v1/student/payment/log", tags=["Student Online Payment Version 1"])
def initiate_online_payment_log(data:hcas_onlinepayment_log, db:Session = Depends(get_db),
                                current_user: str = Depends(get_current_user)):
    OnlinepaymentLog = HcasOnlinePaymentLog(
        uuid = data.uuid,
        json_payload_readable = data.json_payload_readable,
        json_payload = data.json_payload,
        admission_no=data.admission_no
    )

    db.add(OnlinepaymentLog)
    db.commit()
    db.refresh(OnlinepaymentLog)

    return {
        "data inserted successfully"
    }


@router.post("/erp/v1/student/payment/transaction/history", tags=["Student Online Payment Version 1"])
def student_transaction_history(data:StudentTransactionBase, db:Session = Depends(get_db),
                                current_user: str = Depends(get_current_user)):

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    student_history = StudentTransactionHistory(
        studentid = data.studentid,
        txn_id = data.txn_id,
        status = data.status,
        amount = data.amount,
        txn_ref = data.txn_ref,
        approval_refno = data.approval_refno,
        response_code = data.response_code,
        feetype = data.feetype,
        mode_of_payment = data.mode_of_payment,
        date = data.date,
        studentdetails = data.studentdetails,
        created_at = current_time,
        updated_at = current_time
        
    )
    db.add(student_history)
    db.commit()
    db.refresh(student_history)

    return {
       "Record Inserted Successfully"
    }



@router.post("/erp/v1/student/payment/transaction/update", tags=["Student Online Payment Version 1"])
def update_online_payment_status(data: feeOnlinePayment, db: Session = Depends(get_db),
                                 current_user: str = Depends(get_current_user)):
    # Extract request data
    merchant_txn_id = data.merchant_txn_id
    txndt = data.txndt
    txnstatus = data.txnstatus.upper()  # Normalize to uppercase
    totalamt = data.totalamt
    trackid = data.trackid
    stuid = data.stuid
    studentadminid = data.studentadminid
    uniqueid = data.uniqueid

    # Step 1: Find the transaction record
    txn = db.query(StudentTransactionHistory).filter(
        StudentTransactionHistory.txn_id == merchant_txn_id
    ).first()

    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # Step 2: Update transaction history
    txn.response_code = txndt
    txn.status = txnstatus
    txn.amount = totalamt
    txn.txn_ref = trackid
    db.commit()

    # Step 3: Skip inserts if status is AWAITED
    if txnstatus == "AWAITED":
        return {
            "message": "Transaction is in AWAITED state. Only history updated.",
            "txn_id": merchant_txn_id,
            "status": txnstatus,
        }

    # Step 4: Insert into FeeOnlinePayment and FeeOnlinePaymentInput
    sequenceno = datetime.utcnow().strftime("%Y%m%d%H%M%S") + str(stuid)
    banktokenid = txn.approval_refno

    # Insert into FeeOnlinePayment
    fee_payment = FeeOnlinePayment(
        fop_tranno=sequenceno,
        fop_date=datetime.utcnow(),
        fop_banktokenid=banktokenid,
        fop_bankrefno=trackid,
        fop_totalamt=totalamt,
        fop_stdkey=stuid,
        fop_stdrefno=studentadminid,
        fop_status=txnstatus,
        createdby=studentadminid,
        createdon=datetime.utcnow(),
    )
    db.add(fee_payment)

    # Insert into FeeOnlinePaymentInput
    fee_input = FeeOnlinePaymentInput(
        fopt_tranno=sequenceno,
        fopt_json=uniqueid,
        tcreatedby=studentadminid,
        tcreatedon=datetime.utcnow(),
    )
    db.add(fee_input)

    db.commit()

    return {
        "message": f"Payment {txnstatus} processed. Records inserted.",
        "txn_id": merchant_txn_id,
        "status": txnstatus,
    }