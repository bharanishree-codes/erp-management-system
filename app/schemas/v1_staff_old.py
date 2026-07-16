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