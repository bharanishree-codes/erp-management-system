from fastapi import APIRouter
from app.schemas.v1_media import *
from app.models.v1_media import *
from fastapi import FastAPI, UploadFile, File, Form, Query, Depends,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import os
import shutil
from app.database import get_db
from sqlalchemy import and_
from app.dependencies import get_current_user


from app.database import SessionLocal

router = APIRouter()

@router.get("/erp/v1/student/files/{sfstu_id}")
def get_uploaded_files_for_student(sfstu_id:int,db: Session = Depends(get_db),
     current_user: str = Depends(get_current_user)):
    student = db.query(StudentFile).filter(StudentFile.sfstu_id == sfstu_id).all()
    if not student:
        return {"message": "Student not found"}
    return student


UPLOAD_ROOT = "D:/HCAS/DATA/Excel/STUDENT/"


@router.post("/erp/v1/student/files/upload/")
async def process_student_file_upload(
    sfstu_id: int = Form(...),
    filetitle: str = Form(...),
    uploadby: str = Form(...),
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_user)
):
    try:
        # Print incoming form data
        # print("sfstu_id:", sfstu_id)
        # print("filetitle:", filetitle)
        # print("uploadby:", uploadby)
        # print("filename:", file.filename)
        # print("content_type:", file.content_type)

        # Create student-specific folder
        folder_path = os.path.join(UPLOAD_ROOT, str(sfstu_id))
        os.makedirs(folder_path, exist_ok=True)

        # Full file path
        file_path = os.path.join(folder_path, file.filename)

        # Save the uploaded file to disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Database insert
        db: Session = SessionLocal()
        new_file = StudentFile(
            sfstu_id=sfstu_id,
            filetitle=filetitle,
            filename=file.filename,
            filepath=folder_path,
            viewattach="",
            uploadby=uploadby,
            uploadon=datetime.now()
        )
        db.add(new_file)
        db.commit()
        db.close()

        return {"message": "File uploaded successfully"}

    except Exception as e:
        print("Error occurred:", e)
        return JSONResponse(content={"error": "Something went wrong"}, status_code=500)


@router.delete("/erp/v1/student/files/{sfid}/delete")
def delete_uploaded_file(sfid:int, db:Session = Depends(get_db),
               current_user: str = Depends(get_current_user)):

    obj = db.query(StudentFile).filter(StudentFile.sfid == sfid).first()

    db.delete(obj)
    db.commit()

    return {
        "message":"File Deleted Successfully"
    }
    