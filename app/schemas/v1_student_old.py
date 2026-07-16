from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from typing import List

class UpdateStudentInfo(BaseModel):
    stu_GENDER: Optional[str] = None
    stu_caste: Optional[str] = None
    stu_subcaste: Optional[str] = None
    stu_bloodgroup: Optional[str] = None
    stu_address1: Optional[str] = None
    stu_address2: Optional[str] = None
    stu_state: Optional[str] = None
    aadharno: Optional[str] = None
    stu_umisidno: Optional[str] = None
    stu_state_mis: Optional[int] = None
    stu_salutation: Optional[str] = None
    stu_emisreasonid: Optional[int] = None
    stu_splcatgreasonid: Optional[int] = None
    stu_pervillagepanchayat: Optional[str] = None
    stu_comtaluk: Optional[str] = None
    stu_comvillage: Optional[str] = None
    stu_comblock: Optional[str] = None
    stu_comvillagepanchayat: Optional[str] = None
    stu_bankbranch: Optional[str] = None
    stu_bankcity: Optional[str] = None
    stu_bankacctype: Optional[str] = None
    stu_aadharseedingstatus: Optional[str] = None
    stu_aadharremarkmessage: Optional[str] = None
    stu_orphancategory: Optional[str] = None
    stu_udidno: Optional[str] = None
    stu_udidreasonid: Optional[int] = None
    stu_postaladdress: Optional[str] = None
    stu_country: Optional[str] = None
    stu_firstgraduatestatus: Optional[str] = None
    stu_firstgraduateno: Optional[str] = None
    stu_comcountry: Optional[str] = None
    stu_comstate: Optional[str] = None
    stu_compostaladdress: Optional[str] = None
    stu_comdistrict: Optional[str] = None
    stu_comlocationtype: Optional[str] = None
    stu_HEIGHT: Optional[str] = None
    stu_WEIGHT: Optional[str] = None
    stu_locationtype: Optional[str] = None
    stu_pertaluk: Optional[str] = None
    stu_pervillage: Optional[str] = None
    stu_perblock: Optional[str] = None
    stu_comzipcode: Optional[str] = None
    stu_zipcode: Optional[str] = None
    stu_district: Optional[str] = None
    stu_religion: Optional[str] = None 
    stu_birthplace: Optional[str] = None
    stu_mothertounge: Optional[str] = None
    stu_nationality: Optional[str] = None
    ifsc_code: Optional[str] = None
    panno: Optional[str] = None
    bankaccno: Optional[str] = None
    stu_bankaccholname: Optional[str] = None
    stu_bankname: Optional[str] = None
    languageopted: Optional[str] = None
    stu_reference: Optional[str] = None
    stu_referralname: Optional[str] = None
    stu_name: Optional[str] = None
    stu_mname: Optional[str] = None
    stu_lname: Optional[str] = None
    stu_Class: Optional[str] = None
    stu_DOB: Optional[date] = None
    stu_others: Optional[str] = None
    remarks: Optional[str] = None
    stu_regno: Optional[str] = None
    statusflag: Optional[str] = None
    stu_mobile: Optional[str] = None
    stu_email: Optional[str] = None
    stu_parentmobile: Optional[str] = None
    stu_parentemail: Optional[str] = None
    stu_specialcatagory: Optional[str] = None
    stu_admissiontype: Optional[str] = None
    stu_admissionquota: Optional[int] = None
    stu_House: Optional[str] = None
    stu_Boarding_Point: Optional[str] = None
    stu_Bus_No: Optional[int] = None
    stu_encry_url: Optional[str] = None
    stu_excelfilename: Optional[str] = None
    stu_dobsms: Optional[str] = None
    stu_section: Optional[str] = None
    stu_parentname: Optional[str] = None
    stu_address3: Optional[str] = None
    stu_address4: Optional[str] = None
    stu_rollno: Optional[str] = None
    stu_classid: Optional[str] = None
    stu_branchid: Optional[int] = None
    stu_courseid: Optional[int] = None
    stu_year: Optional[str] = None
    stu_admissiondt: Optional[datetime] = None
    stu_hosflg: Optional[str] = None
    stu_hostelid: Optional[int] = None
    stu_busflg: Optional[str] = None
    stu_temprollno: Optional[str] = None
    stu_acdyear: Optional[str] = None
    stu_admissionno: Optional[str] = None
    stu_statusflg: Optional[int] = None
    stu_longabs: Optional[int] = None
    stu_longabsreason: Optional[str] = None
    stu_acadamicyear: Optional[int] = None
    stu_apppw: Optional[str] = None
    stu_consper: Optional[int] = None
    stu_xper: Optional[int] = None
    stu_xiiper: Optional[str] = None
    bankid: Optional[int] = None
    fpenrollno: Optional[str] = None
    rfidcardno: Optional[str] = None
    uhfidcardno: Optional[str] = None
    fphostelenrollno: Optional[str] = None
    stuprofileimgpath: Optional[str] = None
    stuprofileimgname: Optional[str] = None
    stu_messflg: Optional[int] = None
    franchiseid: Optional[int] = None
    processid: Optional[str] = None
    wfstatus: Optional[str] = None
    status: Optional[str] = None
    revision: Optional[int] = None
    stu_emisidno: Optional[str] = None
    lastlogin: Optional[datetime] = None
    stu_statusdate: Optional[datetime] = None
    stu_statusremarks: Optional[str] = None
    stu_bulkupdate: Optional[int] = None
    stu_registerlocation: Optional[str] = None
    stu_admiton: Optional[str] = None
    stu_source: Optional[str] = None
    deviceid: Optional[str] = None
    fcmtoken: Optional[str] = None
    loginstatus: Optional[int] = None

    class Config:
        orm_mode = True


class CreateStudentEducationInfo(BaseModel):
    spe_stukey: int
    spe_prevedu: Optional[int] = None
    spe_period: Optional[str] = None
    spe_subject: Optional[str] = None
    spe_specialization: Optional[str] = None
    spe_institution: Optional[str] = None
    spe_inslocation: Optional[str] = None
    spe_board: Optional[int] = None
    spe_medium: Optional[int] = None
    spe_attemptions: Optional[int] = None
    spe_totalmarks: Optional[str] = None
    spe_pcmmarks: Optional[str] = None
    spe_cutoff: Optional[int] = None
    spe_status: Optional[int] = None


class UpdateStudentRelationInfo(BaseModel):
    stp_reltype : Optional[int] = None
    stp_name : Optional[str] = None
    stp_phone : Optional[str] = None
    stp_email : Optional[str] = None
    stp_occupation : Optional[str] = None
    stp_officename : Optional[str] = None
    stp_offlocation : Optional[str] = None
    stp_higheredu : Optional[int] = None
    stp_statusflag : Optional[int] = None


class LoginRequest(BaseModel):
    userid: str
    password: str
    deviceid: str
    fcmtoken: str
    lastlogin: datetime
    device_name: str
    device_validation: str
    user_type: str

class StudentProgramDetails(BaseModel):
    stu_programid: int
    programgroup: str
    pmbasicid: int
    stu_name: str
    stu_key: int

class StudentResponse(BaseModel):
    stu_classid: int
    stu_rollno: str
    stu_name: str
    stu_Class: str
    class_id: int
    smfranchiseid: Optional[int]

    class Config:
        orm_mode = True


class UpdateLogout(BaseModel):
    stf_key: int    
    
    
class OpacRequest(BaseModel):
    title: str
    author: str  

class student_timetable(BaseModel):
    classid: str
    studate: str  

class personalnotification(BaseModel):
    department_id: int


class BatchScheduleRequest(BaseModel):
    cdeptid: int
    cbid: int
    classacdid: int
    class_id: int
    stu_key: int

# Output model (response)
class BatchScheduleResponse(BaseModel):
    bsh_startdate: date   # or str if you want string format
    adpname: str


class AttendanceRequest(BaseModel):
    class_id: int
    stu_key: int
    start_date: str  # or date if you want auto-parse
    end_date: str
    acdname: str

