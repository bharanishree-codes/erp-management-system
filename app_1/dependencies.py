from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.utils.auth import decode_token
from app.database import get_db
from app.models.v1_student import StudentPersonalInfo, StaffPersonalInfo

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/erp/v1/generate-token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_key = decode_token(token)
    
    student = db.query(StudentPersonalInfo).filter(StudentPersonalInfo.stu_ID == user_key).first()
    staff = db.query(StaffPersonalInfo).filter(StaffPersonalInfo.STF_ID == user_key).first()

    if not student and not staff:
        raise HTTPException(status_code=401, detail="Invalid user in token")

    return user_key