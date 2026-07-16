from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import base64

from app.database import get_db
from app.schemas.v1_auth import UserKeyInput, SecretKeyInput
from app.utils.auth import create_access_token
from app.models.v1_student import StudentPersonalInfo, StaffPersonalInfo

router = APIRouter()

@router.post("/erp/v1/generate-secret-key")
def generate_secret_key(data: UserKeyInput, db: Session = Depends(get_db)):
    user_key = data.user_key
    user_type = data.user_type
    
    provided_password = data.secrete_key
    provided_user_url = data.user_url

    expected_password = "b2e_meritplus_2025"
    expected_user_url = "http://fastapi.hcaschennai.edu.in/"

    if provided_password!= expected_password:
        raise HTTPException(status_code=401, detail="Invalid password")
    if provided_user_url!= expected_user_url:
        raise HTTPException(status_code=401,detail="Ivalid url")
    
    if user_type == "student":
    # Check if user is a student
        student = db.query(StudentPersonalInfo).filter(StudentPersonalInfo.stu_ID == user_key).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        print("stu_statusflg value:", student.stu_statusflg)
        if student.stu_statusflg in [0, 1]:  # Only 0 and 1 are active
            secret_key = base64.b64encode(user_key.encode()).decode()
            return {"secret_key": secret_key}
        else:
            raise HTTPException(status_code=403, detail="Student is inactive")

    elif user_type == "staff":
    # Check if user is a staff
        staff = db.query(StaffPersonalInfo).filter(StaffPersonalInfo.STF_ID == user_key).first()
        if not staff:
            raise HTTPException(status_code=404, detail="Staff not found")
        if staff.statusflag == "0": # Only 0 is active
            secret_key = base64.b64encode(user_key.encode()).decode()
            return {"secret_key": secret_key}
        else:
            raise HTTPException(status_code=403, detail="Staff is inactive")
    else:    
        # If not found in either
        raise HTTPException(status_code=404, detail="User not found")



@router.post("/erp/v1/generate-token")
def generate_token(data: SecretKeyInput, db: Session = Depends(get_db)):
    secret_key = data.secret_key

    if not secret_key.isascii():
        raise HTTPException(status_code=400, detail="Invalid secret key format")

    decoded_bytes = base64.b64decode(secret_key.encode())
    user_key = decoded_bytes.decode()

    student = db.query(StudentPersonalInfo).filter(StudentPersonalInfo.stu_ID == user_key).first()
    staff = db.query(StaffPersonalInfo).filter(StaffPersonalInfo.STF_ID == user_key).first()

    if not student and not staff:
        raise HTTPException(status_code=404, detail="User not found")

    token = create_access_token(user_key)

    return {
        "access_token": token,
        "token_type": "bearer"
    }