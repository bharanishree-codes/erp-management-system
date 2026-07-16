from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from typing import List

# Request Model
# -------------------------------
class FeeRequest(BaseModel):
    stukey: str
    classid: str

# -------------------------------
# Response Model
# -------------------------------
class PaymentItem(BaseModel):
    mandatoryflg: str
    feeid: str
    onlinefname: str
    feeduedate: str
    pendingamt: str
    fps_fineperday: str
    fps_maxfine: str
    actfineamt: str
    fpsminamount: str
    payamt: str
    fps_disper: str
    disamount: str
    stu_regno: str
    stu_ID: str
    stu_name: str
    stu_mobile: str
    stu_email: str
    docno: str
    docdate: str
    doctype: str
    counterid: str
    srcid: str
    srcdtlid: str
    plusminus: str
    status: str
    remarks: str
    stu_year: str
    stu_acdyear: str
    curtype: str
    curvalue: str
    billingyear: str

class PaymentResponse(BaseModel):
    paymentlist: List[PaymentItem]



class feeOnlinePayment(BaseModel):
    merchant_txn_id: str
    txndt: str
    txnstatus: str
    totalamt: int
    trackid: str
    stuid: int
    studentadminid: str
    uniqueid: str

class hcas_onlinepayment(BaseModel):
    uuid : str
    json_payload_readable : str
    json_payload : str
    bank_transaction_id : str
    bank_ref_date : datetime
    admission_no  : str


class hcas_onlinepayment_log(BaseModel):
    uuid: str
    json_payload_readable: str
    json_payload: str
    admission_no: str


class StudentTransactionBase(BaseModel):
    studentid: str
    txn_id: str
    status: str
    amount: int
    txn_ref: str
    approval_refno: str
    response_code: str
    feetype: str
    mode_of_payment: str
    date: str
    studentdetails: str
    merchant_id: str
    txn_tranno: int
    txn_pg_type :str
    student_key: int

class PaymentAwaiting(BaseModel):
    trackid :str
    merchant_txn_id : str
    txndt : str
    txnstatus : str
    feetype : str
    
class FeeHistory(BaseModel):
    student_id: str    
  

class Ledger(BaseModel):
    id: int    
    uuid: str
    discount: Optional[str] = None
    
    
    
class StudentKeyRequest(BaseModel):
    student_key: int         