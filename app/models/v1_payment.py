from sqlalchemy import Column, Integer, String, DateTime, Date
from app.database import Base


class FeeDetails(Base):

    __tablename__ = "b2e_tbl_col_feedetail"

    feeid = Column(String,primary_key=True)
    onlinefname = Column(String)
    feename = Column(String)


class FeePaySettings(Base):

    __tablename__ = "b2e_tbl_col_feepaysettings"

    fps_id = Column(Integer,primary_key=True,index=True)
    mandatoryflg = Column(Integer)
    fps_duedate = Column(DateTime)
    fps_fineperday = Column(Integer)
    fps_maxfine = Column(Integer)
    fps_minamount = Column(Integer)
    fps_disper = Column(Integer)


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
    merchant_id = Column(String)
    txn_tranno = Column(String(20))
    txn_pg_type = Column(String(45))




class HcasOnlinePayment(Base):

    __tablename__ = "b2e_tbl_col_api_hcas_onlinepayment"

    apiuid = Column(Integer,primary_key=True)
    admission_no = Column(String)   
    bank_ref_date = Column(DateTime)
    bank_transaction_id = Column(String)
    json_payload = Column(String)
    json_payload_readable = Column(String)
    uuid = Column(String)
    transaction_id = Column(Integer)

class HcasOnlinePaymentLog(Base):

    __tablename__ = "b2e_tbl_col_api_hcas_onlinepayment_log"

    apiluid = Column(Integer,primary_key=True)
    admission_no = Column(String)
    json_payload = Column(String)
    json_payload_readable = Column(String)
    uuid = Column(String)


class UpcomingDue(Base):
    __tablename__ = "vwstuelupcomingdues"  
    sloandid = Column(Integer, primary_key=True)
    sloandstuid = Column(Integer)   
    sloanpid = Column(Integer)      
    sloanfeeid = Column(Integer)    
    sloanautopayledgerid = Column(Integer)  
    sloanno = Column(String)    
    loanpduedate = Column(Date)     
    sloanppayamt = Column(Integer)   
    sloannoinstallment = Column(Integer)   
    sloanpno = Column(Integer, primary_key=True)        
    lfeename = Column(String)         
    lautopayfeename = Column(String)   
    sloanautopaycharges = Column(Integer)   
    sfinededucttype = Column(Integer)    
    totalpayamount = Column(Integer) 
    autopayflg = Column(Integer)            
    duestatus = Column(String)        


class CurrentDue(Base):
    __tablename__ = "vwstuelcurrentdues"  # DB View
    sloandid = Column(Integer, primary_key=True)
    sloandstuid = Column(Integer)
    sloanpid = Column(Integer)
    sloanfeeid = Column(Integer)
    sloanautopayledgerid = Column(Integer)
    sloanno = Column(String)
    loanpduedate = Column(Date)
    sloanppayamt = Column(Integer)
    sloannoinstallment = Column(Integer)
    sloanpno = Column(Integer, primary_key=True)
    lfeename = Column(String)
    lautopayfeename = Column(String)
    sloanautopaycharges = Column(Integer)
    sfinededucttype = Column(String)
    totalpayamount = Column(Integer)
    autopayflg = Column(String)
    duestatus = Column(String)   
    
    
class LoanRepayMent(Base):
    __tablename__ = 'b2e_tbl_col_stu_loanrepayment'

    sloanpid = Column(Integer, primary_key=True)
    sloanpdid = Column(Integer)
    sloanpduedate = Column(Date)
    sloanpactmonth = Column(Integer)
    sloanpactyear = Column(Integer)
    sloanppaymonth = Column(Integer)
    sloanppayyear = Column(Integer)
    sloanppayamt = Column(Integer)
    sloanpautopaydeduct = Column(Integer)
    sloanppaidon = Column(DateTime)
    sloanpdeduct = Column(Integer)
    sloanpremarks = Column(String)
    sloanppaidsts = Column(Integer)
    sloanppaidamount = Column(Integer)
    sloanpno = Column(Integer)
    sloanppayrefno = Column(String(45))
    sloanpremindsts = Column(Integer)




class FeeCounter(Base):
    __tablename__ = 'b2e_tbl_col_feecounter'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    seqtype = Column(String(255))
    seqprefix = Column(String(255))
    seqno = Column(String(255))
    status = Column(String(255))
    seqauto = Column(String(255)) 



class FeeRecPay(Base):
    __tablename__ = 'b2e_tbl_col_feerecpay'

    feerpid = Column(Integer, primary_key=True, index=True)
    docid = Column(String(255))
    docdate = Column(DateTime)
    studentid = Column(String(255))
    doctype = Column(String(255))
    status = Column(String(255))
    currencytype = Column(String(255))
    currrencyvalue = Column(String(255))
    billingyear = Column(String(255))
    studentyear = Column(String(255))
    totalamt = Column(String(255))
    amtinwords = Column(String(255))
    createdby = Column(String(255))
    createdon = Column(DateTime)
    lastmodifyby = Column(String(255))
    lastmodifyon = Column(String(255))
    imprefid = Column(String(255))
    counterid = Column(String(255)) 





class FeeRecipePayPayments(Base):
    __tablename__ = 'b2e_tbl_col_feerecpaypayments'

    idrcp = Column(Integer, primary_key=True, index=True)
    feesrpid = Column(Integer)
    paymentmode = Column(String(255))
    amount = Column(Integer)
    refno = Column(String(255))
    refdate = Column(DateTime)
    bankname = Column(String(255))
    status = Column(String(255))  




class FeeRecPayDetail(Base):
    __tablename__ = 'b2e_tbl_col_feerecpaydetail'

    feesrpdetailid = Column(Integer, primary_key=True, index=True)
    feesrpid = Column(Integer)
    feetypeid = Column(Integer)
    feeid = Column(Integer)
    feeamount = Column(Integer)
    remarks = Column(String(255))
    status = Column(String(255))
    imprefid = Column(String(255))
    acdyear = Column(Integer)


class FeeLedger(Base):
    __tablename__ = 'b2e_tbl_col_feeledger'

    feeledgerid = Column(Integer, primary_key=True, index=True)
    docno = Column(String(255))
    docdate = Column(DateTime)
    doctype = Column(String(255))
    totalamt = Column(Integer)
    curtype = Column(Integer)
    curvalue = Column(Integer)
    acdyear = Column(Integer)
    counterid = Column(Integer)
    studid = Column(Integer)
    studyear = Column(String(255))
    feeid = Column(Integer)
    amount = Column(Integer)
    remarks = Column(String(255))
    srcid = Column(Integer)
    srcdtlid = Column(Integer)
    plusminus = Column(String(255))
    crdramt = Column(Integer)
    status = Column(String(255))
    createdby = Column(String(255))
    createdon = Column(DateTime)
    modifyby = Column(String(255))
    modifyon = Column(String(255))    
    
    
class Currency(Base):
    __tablename__ = 'b2e_tbl_currency'

    cur_id = Column(Integer, primary_key=True, index=True)
    cur_name = Column(String)
    cur_code = Column(String)
    cur_subname = Column(String)
    cur_decimal = Column(Integer)
    cur_status = Column(Integer)
        
        
class FeeVoucher(Base):
    __tablename__ = 'b2e_tbl_col_feevoucher'

    feevid = Column(Integer, primary_key=True, index=True)
    docid = Column(String)
    docdate = Column(DateTime)
    totalamt = Column(Integer)
    amtinwords = Column(String)
    posttype = Column(String)
    doctype = Column(String)
    currencytype = Column(Integer)
    currencyvalue = Column(Integer)
    billingyear = Column(String)
    mremarks = Column(String)
    status = Column(String)
    createdby = Column(String)
    createdon = Column(DateTime)
    lastmodifyby = Column(String)
    counterid = Column(Integer)
    imprefid = Column(String)

class FeeVoucherDetail(Base):
    __tablename__ = 'b2e_tbl_col_feevoucherdtl'

    feevdtlid = Column(Integer, primary_key=True, index=True)
    feevid = Column(Integer)
    studid= Column(Integer)
    studyear = Column(String)
    feeid = Column(Integer)
    amount = Column(Integer)
    remarks = Column(String(255))
    status = Column(String(255))
    acdyear = Column(Integer)        