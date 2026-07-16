from fastapi import APIRouter
from fastapi import Depends,HTTPException

from app.schemas.v1_student import *
from app.models.v1_student import *
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.database import get_db
from sqlalchemy import and_

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
from sqlalchemy import text
from sqlalchemy import func, case, and_
from app.dependencies import get_current_user




router = APIRouter()


SECRET_KEY = "MZysriwB2EpRrgsi"  
BLOCK_SIZE = 16

def encrypt_password(plain_password: str) -> str:
    cipher = AES.new(SECRET_KEY.encode('utf-8'), AES.MODE_ECB)
    padded = pad(plain_password.encode('utf-8'), BLOCK_SIZE)
    encrypted = cipher.encrypt(padded)
    return base64.urlsafe_b64encode(encrypted).decode('utf-8')



@router.post("/erp/v1/rbac/login", tags=["Student and Staff RBAC Login Version 1"])
def login(request: LoginRequest, db: Session = Depends(get_db),
                      current_user: str = Depends(get_current_user),
                      ):
                      
    """
    [View API Details](https://studio.hcaschennai.edu.in/mark_down/psm013002/)
    """
    
    user_role = None
    user_found = False
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Encrypt password
    encrypted_input_password = encrypt_password(request.password)

    # -------- Staff Login --------
    staff_user = db.query(StaffPersonalInfo).filter(
        StaffPersonalInfo.STF_ID == request.userid
    ).first()

    if staff_user:
        # Validate password
        staff_pwd_row = db.query(ActIDUser.PWD_).filter(
            ActIDUser.ID_ == request.userid
        ).first()

        if not staff_pwd_row or staff_pwd_row[0] != encrypted_input_password:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        user_role = "staff"
        user_found = True

        if request.device_validation.lower() == "yes":
            if staff_user.deviceid != request.deviceid or staff_user.fcmtoken != request.fcmtoken:
                staff_user.deviceid = request.deviceid
                staff_user.fcmtoken = request.fcmtoken

        staff_user.lastlogin = request.lastlogin
        db.commit()

    # -------- Student Login --------
    if not user_found:
        student_user = db.query(StudentPersonalInfo).filter(
            StudentPersonalInfo.stu_ID == request.userid
        ).first()

        if student_user:
            if student_user.stu_apppw != encrypted_input_password:
                raise HTTPException(status_code=401, detail="Invalid username or password")

            user_role = "student"
            user_found = True

            if request.device_validation.lower() == "yes":
                if student_user.deviceid != request.deviceid or student_user.fcmtoken != request.fcmtoken:
                    student_user.deviceid = request.deviceid
                    student_user.fcmtoken = request.fcmtoken

            student_user.lastlogin = request.lastlogin
            db.commit()

    if not user_found:
        raise HTTPException(status_code=404, detail="User ID not found")

    # -------- Device Validation Logic --------
    if request.device_validation.lower() == "yes":
        existing_device = db.query(UserDevice).filter(
            and_(
                UserDevice.luserid == request.userid,
                UserDevice.ldeviceid == request.deviceid,
                UserDevice.lfcmtokenid == request.fcmtoken
            )
        ).first()


        if existing_device:
        # Update status and last login time
            existing_device.lstatus = True
            existing_device.lupdatedon = current_time
            existing_device.llastlogin = request.lastlogin
            existing_device.lremarks = "Device validated and status updated"
            existing_device.ldevicename = request.device_name 
            existing_device.lnotification_enabled = 1 

        else:
        # Insert new record
            new_device = UserDevice(
                luserid=request.userid,
                ldeviceid=request.deviceid,
                lfcmtokenid=request.fcmtoken,
                createdby=request.userid,
                createdon=current_time,
                llastlogin=request.lastlogin,
                lupdatedon=current_time,
                lremarks="Device validated and added successfully",
                lstatus=True,
                ldevicename=request.device_name,
                lnotification_enabled=1
            )
            db.add(new_device)
        db.commit()


    elif request.device_validation.lower() == "no":
        existing_empty_device = db.query(UserDevice).filter(
            and_(
                UserDevice.luserid == request.userid,
                UserDevice.ldeviceid == "",
                UserDevice.lfcmtokenid == ""
            )
        ).first()      


        if existing_empty_device:
        # Update device name and timestamp even if record exists
            existing_empty_device.ldevicename = request.device_name
            existing_empty_device.lupdatedon = current_time
            existing_empty_device.llastlogin = request.lastlogin
            existing_empty_device.lremarks = "Device validation denied"
            existing_empty_device.lnotification_enabled = 0

        else:
        # Insert new record with empty deviceid and fcmtoken
            new_device = UserDevice(
                luserid=request.userid,
                ldeviceid="",
                lfcmtokenid="",
                createdby=request.userid,
                createdon=current_time,
                llastlogin=request.lastlogin,
                lupdatedon=current_time,
                lremarks="Device validation denied by user",
                lstatus=False,
                ldevicename=request.device_name,
                lnotification_enabled=0
            )
            db.add(new_device)

        db.commit()    

    # -------- Return Response --------
    response_data = {
        "userid": request.userid,
        "password_encrypted": encrypted_input_password,
        "user_type": request.user_type,
        "deviceid": request.deviceid if request.device_validation.lower() == "yes" else "",
        "fcmtoken": request.fcmtoken if request.device_validation.lower() == "yes" else "",
        "lastlogin": request.lastlogin,
        "device_validation": request.device_validation
    }

    return {
        "status": "success",
        "message": "Login successful",
        "data": response_data
    }
    
    
@router.post("/erp/v1/rbac/logout", tags=["Student and Staff RBAC Login Version 1"])
def logout(request: UpdateLogout, db: Session = Depends(get_db),
            current_user: str = Depends(get_current_user)):
    # Fetch actual object, not query
    staff = db.query(StaffPersonalInfo).filter(
        StaffPersonalInfo.stf_key == request.stf_key
    ).first()

    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")

    staff.loginstatus = 1  
    db.commit()
    db.refresh(staff)

    return {
        "message": "Logout successfully",
        "stf_key": staff.stf_key,
        "login_status": staff.loginstatus
    }
