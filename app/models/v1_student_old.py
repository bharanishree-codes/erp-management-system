from sqlalchemy import Column, Integer, String, DateTime,Date
from app.database import Base
from sqlalchemy.orm import relationship

class StudentPersonalInfo(Base):
    __tablename__ = "b2e_tbl_id_stu_personal_info"

    stu_KEY = Column(Integer, primary_key=True, index=True)
    stu_ID = Column(String(20), primary_key=True,index=True)
    stu_GENDER = Column(String(10))
    stu_caste = Column(String(50))
    stu_subcaste = Column(String(50))
    stu_bloodgroup = Column(String(5))
    stu_address1 = Column(String(255))
    stu_address2 = Column(String(255))
    stu_state = Column(String(100))
    aadharno = Column(String(20))
    stu_umisidno = Column(String(50))
    stu_state_mis = Column(Integer)
    stu_salutation = Column(String(10))
    stu_emisreasonid = Column(Integer)
    stu_splcatgreasonid = Column(Integer)
    stu_pervillagepanchayat = Column(String(100))
    stu_comtaluk = Column(String(100))
    stu_comvillage = Column(String(100))
    stu_comblock = Column(String(100))
    stu_comvillagepanchayat = Column(String(100))
    stu_bankbranch = Column(String(100))
    stu_bankcity = Column(String(100))
    stu_bankacctype = Column(String(50))
    stu_aadharseedingstatus = Column(String(50))
    stu_aadharremarkmessage = Column(String(255))
    stu_orphancategory = Column(String(50))
    stu_udidno = Column(String(50))
    stu_udidreasonid = Column(Integer)
    stu_postaladdress = Column(String(255))
    stu_country = Column(String(50))
    stu_firstgraduatestatus = Column(String(5))
    stu_firstgraduateno = Column(String(50))
    stu_comcountry = Column(String(50))
    stu_comstate = Column(String(50))
    stu_compostaladdress = Column(String(255))
    stu_comdistrict = Column(String(100))
    stu_comlocationtype = Column(String(50))
    stu_HEIGHT = Column(String(10))  
    stu_WEIGHT = Column(String(10)) 
    stu_locationtype = Column(String(50))
    stu_pertaluk = Column(String(100))
    stu_pervillage = Column(String(100))
    stu_perblock = Column(String(100))
    stu_comzipcode = Column(String(20))
    stu_zipcode = Column(String(20))
    stu_district = Column(String(100))
    stu_religion = Column(String(50))
    stu_birthplace = Column(String(100))
    stu_mothertounge = Column(String(50))
    stu_nationality = Column(String(50))
    ifsc_code = Column(String(20))
    panno = Column(String(20))
    bankaccno = Column(String(30))
    stu_bankaccholname = Column(String(100))
    stu_bankname = Column(String(100))
    languageopted = Column(String(50))
    stu_reference = Column(String(50))
    stu_referralname = Column(String(100))
    stu_name = Column(String)
    stu_mname = Column(String)
    stu_lname = Column(String)
    stu_Class = Column(String)
    stu_DOB = Column(Date)
    stu_GENDER = Column(String)
    stu_others = Column(String)
    remarks = Column(String)
    stu_regno = Column(String)
    statusflag = Column(String)
    stu_mobile = Column(String)
    stu_email = Column(String)
    stu_parentmobile = Column(String)
    stu_parentemail = Column(String)
    stu_specialcatagory = Column(String)
    stu_admissiontype = Column(String)
    stu_admissionquota = Column(Integer)
    stu_House = Column(String)
    stu_Boarding_Point = Column(String)
    stu_Bus_No = Column(Integer)
    stu_encry_url = Column(String)
    stu_excelfilename = Column(String)
    stu_dobsms = Column(String)
    stu_section = Column(String)
    stu_parentname = Column(String)
    stu_address3 = Column(String)
    stu_address4 = Column(String)
    stu_rollno = Column(String)
    stu_classid = Column(String)
    stu_branchid = Column(Integer)
    stu_courseid = Column(Integer)
    stu_year = Column(String)
    stu_admissiondt = Column(DateTime)
    stu_hosflg = Column(String)
    stu_hostelid = Column(Integer)
    stu_busflg = Column(String)
    # imprefid = Column(Integer, primary_key=True, index=True)
    stu_temprollno = Column(String)
    stu_acdyear = Column(String)
    stu_admissionno = Column(String)
    stu_statusflg = Column(Integer)
    stu_longabs = Column(Integer)
    stu_longabsreason = Column(String)
    stu_acadamicyear = Column(Integer)
    stu_apppw = Column(String)
    stu_consper = Column(Integer)
    stu_xper = Column(Integer)
    stu_xiiper = Column(String)
    bankid = Column(Integer)
    fpenrollno = Column(String)
    rfidcardno = Column(String)
    uhfidcardno = Column(String)
    fphostelenrollno = Column(String)
    stuprofileimgpath = Column(String)
    stuprofileimgname = Column(String)
    stu_messflg = Column(Integer)
    franchiseid = Column(Integer)
    processid = Column(String)
    wfstatus = Column(String)
    status = Column(String)
    revision = Column(Integer)
    stu_emisidno = Column(String)
    lastlogin = Column(DateTime)
    stu_statusdate = Column(DateTime)
    stu_statusremarks = Column(String)
    stu_bulkupdate = Column(Integer)
    stu_registerlocation = Column(String)
    stu_admiton = Column(String)
    stu_reference = Column(String)
    stu_source = Column(String)
    deviceid = Column(String)
    fcmtoken = Column(String)
    loginstatus = Column(Integer)


class StudentRelationInfo(Base):

    __tablename__ = "b2e_tbl_col_sturelationinfo"

    stp_key = Column(Integer, primary_key=True, index=True)
    stp_stukey = Column(Integer)
    stp_reltype = Column(Integer)
    stp_name = Column(String(100))
    stp_phone = Column(String(100))
    stp_email = Column(String(100))
    stp_occupation = Column(String(100))
    stp_officename = Column(String(100))
    stp_offlocation = Column(String(100))
    stp_higheredu = Column(Integer)
    stp_statusflag = Column(Integer)


class StaffPersonalInfo(Base):

    __tablename__ = "b2e_tbl_id_sf_personal_info"

    stf_key = Column(Integer, primary_key=True, index=True)
    STF_ID = Column(String, primary_key=True, index=True)
    deviceid = Column(String)
    fcmtoken = Column(String)
    lastlogin = Column(DateTime)    
    statusflag = Column(String)
    loginstatus = Column(Integer)
    stf_name = Column(String)


class Catlouge(Base):

    __tablename__ = "b2e_tbl_id_tb_catalogue"

    catlg_key = Column(Integer, primary_key=True, index=True)
    catlg_code = Column(String(100))
    catlg_description =  Column(String(500))
    catlg_st_key =  Column(Integer)
    catlg_ctyp_key = Column(Integer)
    catlg_other = Column(Integer)


class StudentEducationInfo(Base):

    __tablename__ = "b2e_tbl_col_stupreviousedu"    

    spe_key = Column(Integer,primary_key=True,index=True)
    spe_stukey = Column(Integer)
    spe_prevedu = Column(Integer)
    spe_period = Column(String(100))
    spe_subject = Column(String(100))
    spe_specialization = Column(String(100))
    spe_institution = Column(String(100))
    spe_inslocation = Column(String(100))
    spe_board = Column(Integer)
    spe_medium = Column(Integer)
    spe_attemptions = Column(Integer)
    spe_totalmarks = Column(String(100))
    spe_pcmmarks = Column(String(100))
    spe_cutoff = Column(Integer)
    spe_status = Column(Integer)


class StudentCertificates(Base):

    __tablename__ = "b2e_tbl_col_stucertificates"

    stucid = Column(Integer,primary_key=True,index=True)
    stucstukey = Column(Integer)
    stucstustdcid = Column(Integer)
    stucno = Column(String)
    stucstatus = Column(Integer)
    stucdate = Column(DateTime)
    stuceligible = Column(String)    


class StudentCertificateInfo(Base):

    __tablename__ = "b2e_tbl_col_stustdcertificate"

    stustdcid = Column(Integer,primary_key=True,index=True)
    stustdcname = Column(String)
    stustdorderid = Column(Integer)
    stustdcstatus = Column(String)


class StudentNature(Base):

    __tablename__ = "b2e_tbl_id_stu_nature"

    stustatusflag =  Column(Integer,primary_key=True,index=True) 
    stnstautsname = Column(String)
    stuactivestatus = Column(String)


class StudentQuota(Base):

    __tablename__ = "b2e_tbl_col_admissionquota"    

    quota_id =  Column(Integer,primary_key=True,index=True) 
    quota_name = Column(String)
    quota_per = Column(Integer)
    status = Column(String)    


class UserDevice(Base):

    __tablename__ = "b2e_tbl_userdevices"

    ludid = Column(Integer,primary_key=True,index=True)
    luserid = Column(String)
    ldeviceid = Column(String)
    ldevicename = Column(String)
    lstatus = Column(String)
    createdby = Column(String)
    createdon = Column(DateTime)
    lfcmtokenid = Column(String)
    lremarks = Column(String)
    llastlogin = Column(DateTime)
    lupdatedon = Column(String)
    lnotification_enabled = Column(Integer)


class ActIDUser(Base):

    __tablename__ = "act_id_user"

    ID_ = Column(String,primary_key=True,index=True)
    PWD_ = Column(String)


class PMBasic(Base):
    __tablename__ = "b2e_tbl_col_pmbasic"

    pmbasicid = Column(Integer, primary_key=True, index=True)
    programgroup = Column(String)

class B2EClass(Base):
    __tablename__ = "b2e_tbl_id_class"   

    stu_classid = Column(Integer)
    class_id = Column(Integer, primary_key=True, index=True)
    smfranchiseid = Column(Integer)
    class_name = Column(String)
    class_code = Column(String)
    cbid = Column(Integer)           # missing field for join
    classacdid = Column(String)


class TimeTableStud(Base):
    __tablename__ = "b2e_tbl_col_timetablestud"

    st_key = Column(Integer, primary_key=True, index=True)
    st_tt_key = Column(Integer)
    st_stu_key = Column(Integer)


class AcademicYear(Base):
     __tablename__ = "b2e_tbl_col_acdyear"

     acdyearid = Column(Integer, primary_key=True, index=True)
     acdname = Column(String)
     acdstartdate = Column(DateTime)
     acdenddate = Column(DateTime)
     currentyear = Column(Integer)
     status = Column(String)
     acdfinstart = Column(DateTime)
     acdfinend = Column(DateTime)
     currentfinyear = Column(Integer)
     admissionstartdate = Column(DateTime)
     admissionenddate = Column(DateTime)
     
     
class BookHdr(Base):
    __tablename__ = "b2e_tbl_id_tb_lbookhdr"
    lcat_key = Column(Integer, primary_key=True, index=True)
    lcat_auth_key = Column(String)
    lcat_booktitle = Column(String)
    lcat_scat_key = Column(Integer)
    lcat_isbn = Column(String)
    lcat_issn = Column(String)
    lcat_callno = Column(String)
    lcat_edition = Column(String)
    lcat_seriesno = Column(String)
    lcat_cat_key = Column(Integer)
    lcat_pub_key = Column(Integer)
    lcat_booktype = Column(String)


class BookDet(Base):
    __tablename__ = "b2e_tbl_id_tb_lbookdet"
    lcad_key = Column(Integer, primary_key=True, index=True)
    lcad_lcat_key = Column(Integer)
    lcad_accessno = Column(String)
    lcad_rack = Column(String)
    lcad_row = Column(String)
    lcad_position = Column(String)


class Department(Base):
    __tablename__ = "b2e_tbl_department"
    depid = Column(Integer, primary_key=True, index=True)
    department = Column(String)


class Publisher(Base):
    __tablename__ = "b2e_tbl_id_tb_lpublisher"
    pub_key = Column(Integer, primary_key=True, index=True)
    pub_name = Column(String)


class BookIssue(Base):
    __tablename__ = "b2e_tbl_id_tb_lbookissue"
    bis_id = Column(Integer, primary_key=True, index=True)
    bis_lcad_key = Column(Integer)
    bis_duedate = Column(Date)
    bis_returndate = Column(Date)     

class SchoolSettings(Base):
    __tablename__ = "b2e_tbl_id_school_settings"

    schsettings_id = Column(Integer, primary_key=True, index=True)         
    
    
class ExamScheduleHdr(Base):
    __tablename__ = "b2e_tbl_id_exam_schedule_hdr"
    iExamSchKey = Column(Integer, primary_key=True, index=True)
    iclass_ID = Column(Integer)
    sSemester = Column(Integer)
    iExam_ID = Column(Integer)
    nTotal = Column(Integer)
    dCreatedOn = Column(DateTime)
    sCreatedBy = Column(String)
    dPublishingDate = Column(DateTime)
    esh_acdyear = Column(Integer)
    esh_semtype = Column(String)
    iStatus = Column(Integer)
    esh_mrg = Column(Integer)
    esh_retake = Column(Integer)
    esh_docno = Column(String)

class ExamScheduleDtl(Base):
    __tablename__ = "b2e_tbl_id_exam_schedule_dtl"
    iExamDtlKey = Column(Integer, primary_key=True, index=True)
    iExamSchKey = Column(Integer)
    sSub_ID = Column(Integer)
    staff_key = Column(Integer)
    iSplitKey = Column(Integer)
    dSchDate = Column(DateTime)
    sSchTime = Column(DateTime)
    iDuration = Column(Integer)
    nPass_Mark = Column(Integer)
    nMax_Mark = Column(Integer)
    sStatus = Column(String)
    finalsubmit = Column(Integer)


class ExamResult(Base):

    __tablename__ = "b2e_tbl_id_tb_examresult"

    er_key = Column(Integer, primary_key=True, index=True)
    er_passfail = Column(String)
    er_attendance = Column(String)
    er_marks = Column(Integer)
    er_examSchDtlKey = Column(Integer)
    er_stuid = Column(Integer)


class Notification(Base):

    __tablename__ = "b2e_tbl_id_notification"    

    notify_id = Column(Integer,primary_key=True, index=True)
    notify_stdid = Column(Integer)
    notify_msg = Column(String)
    notify_postedon = Column(DateTime)
    notifyattach = Column(String)
    notifyattachfile = Column(String)
    notify_type = Column(String)
    wfstatus = Column(String)
    status = Column(String)
    


class AppSettings(Base):
    __tablename__ = "b2e_tbl_appsettings"

    appid = Column(Integer, primary_key=True, index=True)
    appserver = Column(String)    


class PersonalNotification(Base):
    __tablename__ = "b2e_tbl_col_departmentchartnotifi"

    depchnid = Column(Integer,primary_key=True, index=True)
    deptid = Column(Integer)
    content = Column(String)
    imagepath = Column(String)
    usertype = Column(String)
    createdby = Column(String)
    createdon = Column(DateTime)


class CourseBranch(Base):
    __tablename__ = "b2e_tbl_col_coursebranch"

    cbid = Column(Integer,primary_key=True,index=True)
    cdeptid = Column(Integer)
    branchname = Column(String)
    branchcode = Column(String)

 #==============================================================================


class B2EDepartment(Base):
    __tablename__ = "b2e_tbl_col_departments"  

    bcatid = Column(Integer,primary_key=True,index=True)  
    bcatname = Column(String)



class B2EStudent_detail(Base):
    __tablename__ = "b2e_tbl_col_stuatddtl"

    atd_id = Column(Integer, primary_key=True, index=True)
    atd_attkey = Column(Integer)  
    atd_stdid = Column(Integer)   
    atd_status = Column(String) 


class B2EStudent_schedule(Base):
    __tablename__ = "vw_student_schedule"

    id = Column(Integer, primary_key=True, autoincrement=True)
    class_id = Column(Integer)
    class_name = Column(String)
    acdyearid = Column(Integer)
    adddate = Column(DateTime)

















    