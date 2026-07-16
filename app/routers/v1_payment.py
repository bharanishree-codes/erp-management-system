from fastapi import APIRouter
from fastapi import Depends,HTTPException

from app.schemas.v1_student import *
from app.schemas.v1_payment import *
from app.models.v1_student import *
from app.models.v1_payment import *
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.database import get_db
from sqlalchemy import and_, or_
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
from sqlalchemy import text
from sqlalchemy import func, case, and_
from app.dependencies import get_current_user
import json
from num2words import num2words
from datetime import date

router = APIRouter()

@router.get("/erp/v1/student/fees/online/pending",tags=["Student Online Payment Version 1"])
def get_online_payment(stu_key: str, class_id: str, db: Session = Depends(get_db)
                       ):
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

    return {
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

    sequenceno = datetime.utcnow().strftime("%Y%m%d%H%M%S") + str(data.student_key)

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
        updated_at = current_time,
        merchant_id = data.merchant_id,
        txn_tranno = sequenceno,
        txn_pg_type = data.txn_pg_type,
        
        
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
    


@router.get("/erp/v1/student/payment/fees_history", tags=["Student Online Payment Version 1"])
def get_fees_history(student_id: str, db: Session = Depends(get_db)):

    payments = (
        db.query(StudentTransactionHistory)
        .filter(StudentTransactionHistory.studentid == student_id)
        .all()
    )

    if not payments:
        return {"message": "payment not found"}

    fee_online_payment = (
        db.query(FeeOnlinePayment)
        .filter(FeeOnlinePayment.fop_stdrefno == student_id)
        .first()
    )

    fee_api_online_payment = (
        db.query(HcasOnlinePayment)
        .filter(HcasOnlinePayment.admission_no == student_id)
        .first()
    )


    # Safe extraction
    fop_tranno = fee_online_payment.fop_tranno if fee_online_payment else None
    json_payload_readable = (
        fee_api_online_payment.json_payload_readable
        if fee_api_online_payment
        else None
    )

    student = (
        db.query(StudentPersonalInfo)
        .filter(StudentPersonalInfo.stu_ID == student_id)
        .first()
    )
    admission_no = student.stu_admissionno if student else None

    fee_ledger = (
        db.query(FeeLedger)
        .filter(FeeLedger.createdby == student_id)
        .first()
    )

    docno = fee_ledger.docno if fee_ledger else None

    response = []
    for payment in payments:
        response.append({
            "AdmissionNo": admission_no,
            "TransactionDate": payment.updated_at,
            "Amount": payment.amount,
            "Status": payment.status,
            "TransactionID":payment.txn_id,
            "fop_tranno": fop_tranno,
            "docno": docno,
            "fee_details": json_payload_readable
        })

    return response

    
    
    
@router.get("/erp/v1/student/payment/upcoming_student/{student_id}",
            tags=["Student Online Payment Version 1"])
def get_upcoming_dues(student_id: int, db: Session = Depends(get_db)
                   ):

    today = date.today()

    upcoming_student = db.query(CurrentDue).filter(
        CurrentDue.sloandstuid == student_id,
        func.STR_TO_DATE(CurrentDue.loanpduedate, '%d/%m/%Y') > today
    ).all()

    if not upcoming_student:
        return {"message": "Upcoming Student not found"}

    return upcoming_student
    

@router.get("/erp/v1/student/payment/currentdue_student/{student_id}",
            tags=["Student Online Payment Version 1"])
def get_current_dues(student_id: int, db: Session = Depends(get_db)
                  ):

    today = date.today()

    # Join CurrentDue with LoanRepayMent and exclude paid installments
    currentdue_student = db.query(CurrentDue).join(
        LoanRepayMent,
        CurrentDue.sloanpid == LoanRepayMent.sloanpid
    ).filter(
        CurrentDue.sloandstuid == student_id,
        func.STR_TO_DATE(CurrentDue.loanpduedate, '%d/%m/%Y') <= today,
        LoanRepayMent.sloanppaidsts != 2  # Exclude paid installments
    ).all()

    if not currentdue_student:
        return {"message": "CurrentDue Student not found"}

    return currentdue_student



    
    
@router.get("/erp/v1/student/payment/get_feeledger", tags=["Student Online Payment Version 1"])
def get_feeledger(student_key: str, db: Session = Depends(get_db)
                      ):
    # Fetch the most recent record for the student
    student_payment = (
        db.query(FeeOnlinePayment)
        .filter(FeeOnlinePayment.fop_stdkey == student_key)
        .order_by(FeeOnlinePayment.fop_id.desc())   # latest by ID
        .first()
    )

    if not student_payment:
        return {"message": "No fee ledger found for this student key"}

    # Return only the most recent record
    result = {
        "fop_id": student_payment.fop_id,
        "fop_stdrefno": student_payment.fop_stdrefno,
        "fop_tranno": student_payment.fop_tranno
    }

    return {"fee_ledger": result}
    
    
    
def capitalize_each_word(text):
    return ' '.join(word[0].upper() + word[1:] if word else '' for word in text.split())

def check_feerecpay_exists(db, docid: str, feesrpid: int) -> bool:
    """
    Check if records exist in all required tables for the given docid and feesrpid.

    Args:
        db: SQLAlchemy session or connection
        docid (str): The document id (e.g., 'OREC-12515')
        feesrpid (int): The fee receipt payment id (e.g., 12515)

    Returns:
        bool: True if data exists in all 4 tables, otherwise False
    """
    queries = [
        ("b2e_tbl_col_feerecpay", "docid", docid),
        ("b2e_tbl_col_feerecpaypayments", "feesrpid", feesrpid),
        ("b2e_tbl_col_feerecpaydetail", "feesrpid", feesrpid),
        ("b2e_tbl_col_feeledger", "docno", docid),
    ]

    for table, column, value in queries:
        sql = text(f"SELECT 1 FROM {table} WHERE {column} = :value LIMIT 1")
        result = db.execute(sql, {"value": value}).fetchone()
        if not result:  # if no record found in this table
            return False

    return True
    
    
@router.post("/erp/v1/student/payment/feeledger", tags=["Student Online Payment Version 1"])
def feeledger(data: Ledger, db: Session = Depends(get_db)
            ):
    # Fetch FeeOnlinePayment record
    obj = db.query(FeeOnlinePayment).filter(
        FeeOnlinePayment.fop_id == data.id
    ).first()
    if not obj:
        return {"message": f"No record found for id {data.id}"}

    # Fetch FeeOnlinePaymentInput record
    pay_input_obj = db.query(FeeOnlinePaymentInput).filter(
        FeeOnlinePaymentInput.fopt_tranno == obj.fop_tranno
    ).first()
    if not pay_input_obj:
        return {"message": f"No FeeOnlinePaymentInput found for tranno {obj.fop_tranno}"}

    # Fetch HcasOnlinePayment record by UUID
    hcas_sql = db.query(HcasOnlinePayment).filter(
        HcasOnlinePayment.uuid == pay_input_obj.fopt_json
    ).first()
    if not hcas_sql:
        return {"message": f"No uuid found for the json {pay_input_obj.fopt_json}"}

    # ✅ Directly fetch transaction_id from table column
    transaction_id = hcas_sql.transaction_id

     # After decoding json_payload_readable and before creating FeeRecPay
    if transaction_id and str(transaction_id).isdigit():
        loan_pay_tbl = db.query(LoanRepayMent).filter(
            LoanRepayMent.sloanpid == int(transaction_id)
        ).first()

        if loan_pay_tbl:
            # Update loan repayment record
            loan_pay_tbl.sloanppaidamount = loan_pay_tbl.sloanppayamt
            loan_pay_tbl.sloanppaidon = datetime.now()
            loan_pay_tbl.sloanppaidsts = 2
            db.commit()
        else:
            return {
                "message": f"No matching loan repayment found for transaction ID {transaction_id}",
                "transaction_id": transaction_id
            }
    
    # ✅ Decode json_payload_readable safely
    decoded_json = {}
    raw_value = hcas_sql.json_payload_readable.strip()

    if raw_value.startswith("{") and raw_value.endswith("}"):
        # Already JSON
        decoded_json = json.loads(raw_value)
    else:
        # Assume Base64
        decoded_bytes = base64.b64decode(raw_value)
        decoded_string = decoded_bytes.decode("utf-8", errors="ignore").strip()
        if decoded_string.startswith("{") and decoded_string.endswith("}"):
            decoded_json = json.loads(decoded_string)

    student_payment_obj = decoded_json.get('feedetails')

# Validate before using
    if not student_payment_obj:
        return {
            "status": "error",
            "message": "No 'feedetails' found in json_payload_readable",
            "raw_json": decoded_json
        }

    total_amount = 0.0

    for tot_amt in student_payment_obj:
        total_amount += float(tot_amt['feeamt'])

        # print("tot_amt:",total_amount)

    total_amount_value = int(total_amount)
    num_in_words = num2words(total_amount_value)
    num_in_words_capitalized = capitalize_each_word(num_in_words)
    total_amount_in_words = f"INR (Rupees) {num_in_words_capitalized} Only"    
    # doc_id_obj = db.query(FeeCounter).filter(FeeCounter.id == 24).first()

    # if not doc_id_obj:
    #     return {"status": "error", "message": "FeeCounter not found."}

    doc_id_obj = db.query(FeeCounter).filter(FeeCounter.id == 34).with_for_update().first()
    if not doc_id_obj:
        return {"status": "error", "message": "FeeCounter not found."}

    # Increment sequence first to avoid duplicates
    doc_id_obj.seqno += 1
    db.commit()
    db.refresh(doc_id_obj)
    doc_id = f"{doc_id_obj.seqprefix}-{doc_id_obj.seqno}"

    # Check if docid already exists
    existing = db.query(FeeRecPay).filter(FeeRecPay.docid == doc_id).first()
    if existing:
        return {"status": "error", "message": f"docid {doc_id} already exists. Please check FeeCounter."}

                # Fetch current academic year ID
    current_acd_year = db.query(AcademicYear).filter(AcademicYear.currentyear == 1).first()

    if not current_acd_year:
        return {
               "message": f"No active academic year found for the id {current_acd_year}. Please configure the current academic year",
            }
    
    # print("ID:", current_acd_year.acdyearid)

    acd_year_id = current_acd_year.acdyearid

    seq_no = doc_id_obj.seqno
    seq_prefix = doc_id_obj.seqprefix
    doc_id = f"{seq_prefix}-{seq_no}"

    doc_date = obj.fop_date
    student_id = obj.fop_stdkey

    doctype = "receipt"
    status = 0
    currency_type = 1
    currency_value = 1

    billing_year = "BILLING YEAR"

    student_year_obj = db.query(StudentPersonalInfo).filter(StudentPersonalInfo.stu_KEY == student_id).first()
    student_year = student_year_obj.stu_year

    created_by = obj.createdby
    current_time = datetime.now()
    lastmodifyby = None
    lastmodifyon = None
    imprefid = None
    counterid = 34


    existing = db.query(FeeRecPay).filter_by(docid=doc_id).first()
    if existing:
        exists = check_feerecpay_exists(db, docid=doc_id, feesrpid=existing.feerpid)

        if exists:
            for i in range(1):
                print(i)
                doc_id_obj.seqno += 1
                db.add(doc_id_obj)
                db.commit()
                db.refresh(doc_id_obj)
                doc_id = f"{seq_prefix}-{seq_no}"
        else:
            raise HTTPException(status_code=400, detail=f"docid :'{doc_id}' already exists. This field must be unique.")


    save_tbl1 = FeeRecPay(
            docid=doc_id,
            docdate=doc_date,
            studentid=student_id,
            doctype=doctype,
            status=status,
            currencytype=currency_type,
            currrencyvalue=currency_value,
            billingyear=billing_year,
            studentyear=student_year,
            totalamt=total_amount_value,
            amtinwords=total_amount_in_words,
            createdby=created_by,
            createdon=current_time,
            lastmodifyby=lastmodifyby,
            lastmodifyon=lastmodifyon,
            imprefid=imprefid,
            counterid=counterid
        )

    db.add(save_tbl1)
    db.commit()
    db.refresh(save_tbl1)

    tbl1_id = save_tbl1.feerpid

    pay_paments_tbl = FeeRecipePayPayments(
        feesrpid=tbl1_id,
        paymentmode="ONLINE",
        amount=total_amount_value,
        refno=doc_id,
        refdate=doc_date,
        bankname=None,
        status='0'
    )

    db.add(pay_paments_tbl)
    db.commit()
    db.refresh(pay_paments_tbl)

    feetypeid = None

    # Save FeeRecPayDetail records
    saved_detail_ids = []

    for child_rec in student_payment_obj:
        save_tbl2 = FeeRecPayDetail(
            feesrpid=tbl1_id,
            feetypeid=feetypeid,
            feeid=child_rec['feeid'],
            feeamount=child_rec['feeamt'],
            remarks=None,
            status=0,
            imprefid=None,
            acdyear=acd_year_id,
        )
        db.add(save_tbl2)
        db.commit()
        db.refresh(save_tbl2)
        saved_detail_ids.append(save_tbl2.feesrpid)  # store primary key for validation


    for child_rec2 in student_payment_obj:
            crdamt = child_rec2['feeamt']

            cradmant = -1 * float(crdamt)

            ledger = FeeLedger(
                docno=doc_id,
                docdate=doc_date,
                doctype=doctype,
                totalamt=total_amount_value,
                curtype=1,
                curvalue=1,
                acdyear=acd_year_id,
                studid=student_id,
                counterid=34,
                studyear=student_year,
                feeid=child_rec2['feeid'],
                amount=child_rec2['feeamt'],
                remarks=None,
                status=0,
                srcid=0,
                srcdtlid=0,
                plusminus="M",
                crdramt=cradmant,
                createdby=created_by,
                createdon=current_time,
                modifyby=None,
                modifyon=None
            )

            db.add(ledger)
            db.commit()
            db.refresh(ledger)
           
            
    if data.discount:
        # Create FeeVoucher
        voucher = FeeVoucher(
        docid=doc_id,
        docdate=doc_date,
        totalamt=total_amount_value,
        amtinwords=total_amount_in_words,
        posttype="Discount",        
        doctype="rjournal",           
        currencytype=currency_type,
        currencyvalue=currency_value,
        billingyear=billing_year,     # ensure correct format
        mremarks=data.discount,
        status="0",
        createdby=created_by,
        createdon=current_time,
        lastmodifyby=None,
        counterid=counterid,
        imprefid = int(transaction_id) if transaction_id else None              # ✔ reference receipt
    )


        db.add(voucher)
        db.commit()
        db.refresh(voucher)

        voucher_id = voucher.feevid

        # ✅ ONE consolidated discount detail record
        voucher_detail = FeeVoucherDetail(
            feevid=voucher_id,
            feeid=None,  # or a dedicated DISCOUNT_FEE_ID
            amount=total_amount_value,
            remarks=data.discount,
            studid=student_id,
            studyear=student_year,
            status="0",
            acdyear=acd_year_id
        )

        db.add(voucher_detail)
        db.commit() 

   # ✅ Validate all tables after saving
    ledger_records = db.query(FeeLedger).filter(FeeLedger.docno == doc_id).all()
    ledger_saved_ids = [l.feeledgerid for l in ledger_records]  # adjust to your primary key

    if save_tbl1.feerpid and pay_paments_tbl.feesrpid and saved_detail_ids and ledger_saved_ids:
        return {
            "status": "success",
            "message": (
                f"Fee record saved successfully in all tables:\n"
                f"- FeeRecPay: 1 record\n"
                f"- FeeRecipePayPayments: 1 record\n"
                f"- FeeRecPayDetail: {len(saved_detail_ids)} records\n"
                f"- FeeLedger: {len(ledger_saved_ids)} records"
            ),
            "receipt_id": save_tbl1.docid,
            "student_id": student_id,
            "transaction_id": transaction_id,
            "total_amount": total_amount_value,
            "amount_in_words": total_amount_in_words,
            "payment_record_id": pay_paments_tbl.idrcp,
            "detail_record_ids": saved_detail_ids,
            "ledger_record_ids": ledger_saved_ids
        }
    else:
        missing = []
        if not save_tbl1.feerpid:
            missing.append("FeeRecPay")
        if not pay_paments_tbl.feesrpid:
            missing.append("FeeRecipePayPayments")
        if not saved_detail_ids:
            missing.append("FeeRecPayDetail")
        if not ledger_saved_ids:
            missing.append("FeeLedger")

        return {
            "status": "error",
            "message": f"Failed to save records in: {', '.join(missing)}. Please check your input or database constraints.",
            "receipt_id": save_tbl1.docid if save_tbl1.feerpid else None
        }    
        
        
        

@router.get(
    "/erp/v1/student/mcp/payment/{admission_no}",
    tags=["Student Online Payment Version 1"],
    operation_id="mcp_paymentDetails"
)
def get_student_fee_ledger(admission_no: str, db: Session = Depends(get_db)):

    # CASE WHEN credit/debit calculation
    debit_case = case(
        (FeeLedger.crdramt > 0, FeeLedger.crdramt),
        else_=0
    ).label("debit")

    credit_case = case(
        (FeeLedger.crdramt < 0, FeeLedger.crdramt * -1),
        else_=0
    ).label("credit")

    # MAIN QUERY
    rows = (
        db.query(
            FeeLedger.feeledgerid,
            FeeLedger.docno,
            func.date_format(FeeLedger.docdate, "%d/%m/%Y").label("docdate1"),
            FeeLedger.doctype,
            debit_case,
            func.ifnull(StudentPersonalInfo.stu_name, "").label("stu_name"),
            func.ifnull(Currency.cur_name, "").label("cur_name"),
            Currency.cur_id,
            func.ifnull(AcademicYear.acdname, "").label("acdname"),
            func.ifnull(FeeCounter.name, "").label("counter"),
            FeeDetails.feename,
            FeeLedger.studyear,
            credit_case,
            FeeLedger.remarks
        )
        .join(StudentPersonalInfo, StudentPersonalInfo.stu_KEY == FeeLedger.studid)
        .join(FeeDetails, FeeDetails.feeid == FeeLedger.feeid)
        .outerjoin(Currency, Currency.cur_id == FeeLedger.curtype)
        .outerjoin(AcademicYear, AcademicYear.acdyearid == FeeLedger.acdyear)
        .outerjoin(FeeCounter, FeeCounter.id == FeeLedger.counterid)
        .filter(FeeLedger.status == "0")
        .filter(StudentPersonalInfo.stu_admissionno == admission_no)
        .order_by(FeeLedger.docdate)
        .all()
    )

    # CONVERT row objects to dictionary
    result = [
        {
            "feeledgerid": r.feeledgerid,
            "docno": r.docno,
            "docdate1": r.docdate1,
            "doctype": r.doctype,
            "debit": r.debit,
            "stu_name": r.stu_name,
            "cur_name": r.cur_name,
            "cur_id": r.cur_id,
            "acdname": r.acdname,
            "counter": r.counter,
            "feename": r.feename,
            "studyear": r.studyear,
            "credit": r.credit,
            "remarks": r.remarks,
        }
        for r in rows
    ]

    return {"status": "success", "data": result}
       
       
@router.get(
    "/erp/v1/student/discount/status"
)
def check_discount_used(
    student_id: str,
    db: Session = Depends(get_db)
):
    discount_record = db.query(FeeVoucher).filter(
        FeeVoucher.createdby == student_id,
        FeeVoucher.posttype == "Discount"
    ).first()

    if discount_record:
        return {
            "status": "used",
            "student_id": student_id,
            "discount_docid": discount_record.docid,
            "discount_date": discount_record.docdate
        }

    return {
        "status": "un-used",
        "student_id": student_id
    }