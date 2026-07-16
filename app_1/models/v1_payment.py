from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base


class FeeDetails(Base):

    __tablename__ = "b2e_tbl_col_feedetail"

    feeid = Column(String,primary_key=True)
    onlinefname = Column(String)


class FeePaySettings(Base):

    __tablename__ = "b2e_tbl_col_feepaysettings"

    fps_id = Column(Integer,primary_key=True,index=True)
    mandatoryflg = Column(Integer)
    fps_duedate = Column(DateTime)
    fps_fineperday = Column(Integer)
    fps_maxfine = Column(Integer)
    fps_minamount = Column(Integer)
    fps_disper = Column(Integer)
    

class Feeledger(Base):

    __tablename__ = "b2e_tbl_col_feeledger" 

    feeledgerid = Column(Integer,primary_key=True)
    crdramt = Column(Integer)
    feeid = Column(Integer)
    status = Column(String)
    docno = Column(String)
    docdate = Column(DateTime)
    doctype = Column(String)
    counterid = Column(Integer)
    srcid = Column(Integer)
    srcdtlid = Column(Integer)
    plusminus = Column(String)
    remarks = Column(String)
    studid = Column(Integer)
    curtype = Column(Integer)
    curvalue = Column(Integer)


class FeeOnlinePayment(Base):

    __tablename__ = "b2e_tbl_col_feeonlinepayment"

    fop_id = Column(Integer,primary_key=True)
    fop_tranno = Column(String)
    fop_date = Column(DateTime)
    fop_banktokenid = Column(String)
    fop_bankrefno = Column(String)
    fop_totalamt = Column(Integer)
    fop_stdkey = Column(Integer)
    fop_stdrefno = Column(String)
    fop_status = Column(String)
    createdby = Column(String)
    createdon = Column(DateTime)


class FeeOnlinePaymentInput(Base):

    __tablename__ = "b2e_tbl_col_feeonlinepaymentinput"    

    fopt_id = Column(Integer,primary_key=True)
    fopt_tranno = Column(String)
    fopt_json = Column(String)
    tcreatedby = Column(String)
    tcreatedon = Column(DateTime)


class StudentTransactionHistory(Base):

    __tablename__ = "hcas_student_transaction_history"


    id = Column(Integer,primary_key=True)
    studentid = Column(String)
    txn_id = Column(String)
    status = Column(String)
    amount = Column(Integer)
    txn_ref = Column(String)
    approval_refno = Column(String)
    response_code = Column(String)
    feetype = Column(String)
    amount = Column(Integer)
    mode_of_payment = Column(String)
    date = Column(String)
    studentdetails = Column(String)
    errorcode = Column(String)
    uniqueid = Column(String)
    updated_at = Column(DateTime)
    created_at = Column(DateTime)



class HcasOnlinePayment(Base):

    __tablename__ = "b2e_tbl_col_api_hcas_onlinepayment"

    apiuid = Column(Integer,primary_key=True)
    admission_no = Column(String)   
    bank_ref_date = Column(DateTime)
    bank_transaction_id = Column(String)
    json_payload = Column(String)
    json_payload_readable = Column(String)
    uuid = Column(String)

class HcasOnlinePaymentLog(Base):

    __tablename__ = "b2e_tbl_col_api_hcas_onlinepayment_log"

    apiluid = Column(Integer,primary_key=True)
    admission_no = Column(String)
    json_payload = Column(String)
    json_payload_readable = Column(String)
    uuid = Column(String)
