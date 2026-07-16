from fastapi import APIRouter,Query,Path
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


@router.get("/erp/v1/student/personal_info/{stu_KEY}", tags=["Student Management Version 1"])
def get_student_by_key(stu_KEY: int, db: Session = Depends(get_db),
        current_user: str = Depends(get_current_user)):
    student = db.query(StudentPersonalInfo).filter(StudentPersonalInfo.stu_KEY == stu_KEY).first()
    if not student:
        return {"message": "Student not found"}
    return student


@router.get("/erp/v1/student/personal_info/admission_no/{stu_ID}", tags=["Student Management Version 1"])
def get_student_by_admission_no(stu_ID: str, db: Session = Depends(get_db),
        current_user: str = Depends(get_current_user)):
    student = db.query(StudentPersonalInfo).filter(StudentPersonalInfo.stu_ID == stu_ID).first()
    if not student:
        return {"message": "Student not found"}
    return student

@router.get("/erp/v1/student/relation_info/{stp_stukey}", tags=["Student Management Version 1"])
def get_student_info_by_student_key(stp_stukey: int, db: Session = Depends(get_db),
        current_user: str = Depends(get_current_user)):
    student = db.query(StudentRelationInfo).filter(StudentRelationInfo.stp_stukey == stp_stukey).all()
    if not student:
        return {"message": "Student not found"}
    return student

@router.get("/erp/v1/student/catalogue/all", tags=["Student Management Version 1"])
def get_all_catalogue_items(db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)):
    catlouge = db.query(Catlouge).all()
    return catlouge

@router.get("/erp/v1/student/education_details/{spe_stukey}", tags=["Student Management Version 1"])
def get_student_details_by_student_key(spe_stukey: int, db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)):
    student = db.query(StudentEducationInfo).filter(StudentEducationInfo.spe_stukey == spe_stukey).all()
    if not student:
        return {"message": "Student not found"}
    return student


@router.get("/erp/v1/student/student_certificates/{stucstukey}", tags=["Student Management Version 1"])
def get_student_by_student_key(stucstukey: int, db: Session = Depends(get_db),
     current_user: str = Depends(get_current_user)):
    student = db.query(StudentCertificates).filter(StudentCertificates.stucstukey == stucstukey).all()
    if not student:
        return {"message": "Student not found"}
    return student


@router.put("/erp/v1/student/personal/update/{stp_stukey}", tags=["Student Management Version 1"])
def update_student_personal_info(stu_KEY:int,request:UpdateStudentInfo, db:Session = Depends(get_db),
        current_user: str = Depends(get_current_user)):
    obj=db.query(StudentPersonalInfo).filter(StudentPersonalInfo.stu_KEY == stu_KEY).first()

    if not obj:
        raise HTTPException(status_code=404, detail="Student Not Found")
    
    Update_student_info = request.dict(exclude_unset=True)

    for key,value in Update_student_info.items():
        setattr(obj,key,value)

    db.commit()
    db.refresh(obj)

    return{
        "message":"Record Updated Successfully"
    }



@router.post("/erp/v1/student/education", tags=["Student Management Version 1"])
def register_student_education(data: CreateStudentEducationInfo, db: Session = Depends(get_db),
        current_user: str = Depends(get_current_user)):
    try:
        new_edu = StudentEducationInfo(**data.dict(exclude_unset=True))
        db.add(new_edu)
        db.commit()
        db.refresh(new_edu)
        return {
            "message": "Student Created Successfully",
            "spe_key": new_edu.spe_key
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Insertion failed: {str(e)}")


@router.delete("/erp/v1/student/education/delete/{spe_key}", tags=["Student Management Version 1"])
def delete_student_education(spe_key:int, db: Session = Depends(get_db),
        current_user: str = Depends(get_current_user)):
    obj = db.query(StudentEducationInfo).filter(StudentEducationInfo.spe_key == spe_key).first()

    db.delete(obj)
    db.commit()
    
    return {
        "message": "Student Deleted Successfully"
    }



@router.put("/erp/v1/student/relationship/update/{stu_KEY}", tags=["Student Management Version 1"])
def update_student_relation_info(stp_stukey:int,request:UpdateStudentRelationInfo, db:Session = Depends(get_db),
    current_user: str = Depends(get_current_user)):
    obj = db.query(StudentRelationInfo).filter(StudentRelationInfo.stp_stukey == stp_stukey).first()

    if not obj:
        raise HTTPException(status_code=404, detail="Student Not Found")
    
    Update_student_data = request.dict(exclude_unset=True)

    for key,value in Update_student_data.items():
        setattr(obj,key,value)

    db.commit()
    db.refresh(obj)

    return {
        "message": "Record Updated Successfully"
    }

# @router.get("/erp/v1/student/certificates", tags=["Student Management Version 1"])
# def fetch_all_student_certificates(db: Session = Depends(get_db)):
#     obj = db.query(StudentCertificateInfo).all()
#     return obj

@router.get("/erp/v1/student/certificates", tags=["Student Management Version 1"])
def fetch_all_student_certificates(db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return db.query(StudentCertificateInfo).all()


@router.get("/erp/v1/student/admission_types", tags=["Student Management Version 1"])
def fetch_all_admission_type(db:Session = Depends(get_db),
     current_user: str = Depends(get_current_user)                         
):
    obj = db.query(StudentNature).all()
    return obj

@router.get("/erp/v1/student/admission_quotas", tags=["Student Management Version 1"])
def fetch_all_admission_quotas(db:Session = Depends(get_db),
        current_user: str = Depends(get_current_user) ):
    obj = db.query(StudentQuota).all()
    return obj


@router.get("/erp/v1/student/program_details/{stu_key}", response_model=List[StudentProgramDetails])
def get_student_program_details_by_student_key(stu_key: int, db: Session = Depends(get_db),
     current_user: str = Depends(get_current_user) ):
    sql = text ("""
        SELECT 
            a.stu_programid, 
            b.programgroup, 
            b.pmbasicid, 
            a.stu_name, 
            a.stu_key
        FROM b2e_tbl_id_stu_personal_info a
        INNER JOIN b2e_tbl_col_pmbasic b ON b.pmbasicid = a.stu_programid
        WHERE a.stu_key = :stu_key
    """)

    result = db.execute(sql, {"stu_key": stu_key})
    rows = result.fetchall()

    if not rows:
        raise HTTPException(status_code=404, detail="Student not found")

    return [dict(row._mapping) for row in rows]



@router.get("/erp/v1/student/type_filter/{stu_KEY}/{stu_classid}", response_model=list[StudentResponse])
def get_students_by_type(
    stu_KEY: str = Path(...),
    stu_classid: int = Path(...),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    results = (
        db.query(
            StudentPersonalInfo.stu_classid,
            StudentPersonalInfo.stu_rollno,
            StudentPersonalInfo.stu_name,
            StudentPersonalInfo.stu_Class,
            B2EClass.class_id,
            B2EClass.smfranchiseid
        )
        .join(B2EClass, StudentPersonalInfo.stu_classid == B2EClass.class_id)
        .filter(
            StudentPersonalInfo.stu_KEY == stu_KEY,
            StudentPersonalInfo.stu_classid == stu_classid
        )
        .all()
    )
    return results


