from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from typing import List


class TimeTable(BaseModel):
    stfkey:int
    stfdate:date    
    
class AttendanceRequest(BaseModel):
    classid: str
    strdate: str
    periodid: str
    staffkey: str
    semyear: str
    dayorder: str
    subid: str 
    acdid: str         


class LoadPeriod(BaseModel):
    addeate: str        # "2025-09-19"
    tt_period: str      # "14"
    tt_classid: str     # "394"
    stf_key: str        # "457"
    tt_subkey: str      # "1933"
    semoryear: str      # "5"    


class ChildAttendance(BaseModel):
    atd_reason: Optional[int]
    atd_status: Optional[str]
    atd_subjectkey: Optional[int]
    atd_staffkey: Optional[int]
    atd_stdid: Optional[int]

class StudentAttendance(BaseModel):
    atdclassid: int
    atdsem: int
    atddate: date
    atdperiod: int
    atdstatus: str
    franchiseid: int
    processid: int
    wfstatus: str
    revision: int
    createdby: str
    createdon: datetime
    child_data: Optional[List[ChildAttendance]] = []

class AttendancePayload(BaseModel):
    data: StudentAttendance
