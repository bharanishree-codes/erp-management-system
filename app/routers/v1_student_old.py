from fastapi import APIRouter,Query,Path
from fastapi import Depends,HTTPException

from app.schemas.v1_student import *
from app.models.v1_student import *
from app.models.v1_staff import * 
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.database import get_db
from sqlalchemy import and_

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
from sqlalchemy import text
from sqlalchemy import func, case, and_, literal, cast
from app.dependencies import get_current_user
from sqlalchemy import true

router = APIRouter()


@router.get("/erp/v1/student/personal_info/{stu_KEY}", tags=["Student Management Version 1"])
def get_student_by_key(stu_KEY: int, db: Session = Depends(get_db),
        current_user: str = Depends(get_current_user)):
    student = db.query(StudentPersonalInfo).filter(StudentPersonalInfo.stu_KEY == stu_KEY).first()
    if not student:
        return {"message": "Student not found"}
    return student


# @router.get("/erp/v1/student/personal_info/admission_no/{stu_ID}", tags=["Student Management Version 1"])
# def get_student_by_admission_no(stu_ID: str, db: Session = Depends(get_db),
#                         ):
#     student = db.query(StudentPersonalInfo).filter(StudentPersonalInfo.stu_ID == stu_ID).first()
#     if not student:
#         return {"message": "Student not found"}
#     return student


@router.get("/erp/v1/student/personal_info/admission_no/{stu_ID}", tags=["Student Management Version 1"])
def get_student_by_admission_no(
    stu_ID: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    # Join StudentPersonalInfo with CourseBranch
    result = (
        db.query(StudentPersonalInfo, CourseBranch)
        .outerjoin(CourseBranch, StudentPersonalInfo.stu_branchid == CourseBranch.cbid)
        .filter(StudentPersonalInfo.stu_ID == stu_ID)
        .first()
    )

    if not result:
        return {"message": "Student not found"}

    student_info, branch_info = result

    return {
        "student": student_info.__dict__,
        "branch": {
            "cdeptid": branch_info.cdeptid if branch_info else None,
            "branchcode": branch_info.branchcode if branch_info else None
        }
    }

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



@router.post("/erp/v1/opac/list_books", tags=["Student Management Version 1"])
def get_opac_books(payload: OpacRequest, db: Session = Depends(get_db),
                        current_user: str = Depends(get_current_user)):

    # subquery to get due date
    subquery = (
        db.query(
            BookIssue.bis_lcad_key,
            func.ifnull(func.date_format(BookIssue.bis_duedate, "%d/%m/%Y"), "null").label("duedate")
        )
        .filter(BookIssue.bis_returndate == "0000-00-00")
        .subquery()
    )

    # main query
    rows = (
        db.query(
            BookHdr.lcat_key.label("key"),
            func.ifnull(Publisher.pub_name, "-").label("pubname"),
            BookHdr.lcat_booktitle.label("booktitle"),
            func.ifnull(subquery.c.duedate, "null").label("duedate"),
            BookHdr.lcat_auth_key.label("authkey"),
            BookHdr.lcat_isbn.label("isbn"),
            BookHdr.lcat_issn.label("issn"),
            BookHdr.lcat_callno.label("callno"),
            BookHdr.lcat_edition.label("edition"),
            BookHdr.lcat_seriesno.label("seriesno"),
            BookDet.lcad_accessno.label("accessno"),
            BookDet.lcad_rack.label("rack"),
            BookDet.lcad_row.label("row"),
            BookDet.lcad_position.label("position"),
            Department.department.label("department"),
            case(
                (BookHdr.lcat_scat_key == 1, "Text"),
                (BookHdr.lcat_scat_key == 2, "Reference")
            ).label("lcat_scat_key"),
        )
        .join(BookDet, BookDet.lcad_lcat_key == BookHdr.lcat_key)
        .join(Department, Department.depid == BookHdr.lcat_cat_key)
        .outerjoin(Publisher, Publisher.pub_key == BookHdr.lcat_pub_key)
        .outerjoin(subquery, subquery.c.bis_lcad_key == BookDet.lcad_key)
        .filter(
            BookHdr.lcat_booktype == "bkd",
            func.lower(BookHdr.lcat_booktitle) == payload.title.lower(),
            func.lower(BookHdr.lcat_auth_key) == payload.author.lower(),
        )
        .all()
    )

    # format response
    opaclist = []
    for row in rows:
        data = dict(row._mapping)
        opaclist.append({
            "key": str(data["key"]),
            "pubname": data["pubname"],
            "booktitle": data["booktitle"],
            "duedate": data["duedate"],
            "authkey": data["authkey"],
            "isbn": data["isbn"],
            "issn": data["issn"],
            "callno": data["callno"],
            "edition": data["edition"],
            "seriesno": data["seriesno"],
            "accessno": data["accessno"],
            "rack": data["rack"],
            "row": data["row"],
            "position": data["position"]
        })

    return {"opaclist": opaclist}



@router.post("/erp/v1/student/exam_schedule/{class_id}", tags=["Student Management Version 1"])
def get_exam_schedule(class_id: int, db: Session = Depends(get_db),
       current_user: str = Depends(get_current_user)               ):
    sem_type = case(
        (func.mod(ExamScheduleHdr.sSemester, 2) == 1, "Odd Semester"),
        else_="Even Semester"
    )

    query = (
        db.query(
            Catlouge.catlg_description.label("ename"),#
            TblIdSubject.SUB_NAME.label("subname"),#
            func.date_format(ExamScheduleDtl.dSchDate, "%d/%m/%Y").label("edate"),#
            func.date_format(ExamScheduleDtl.sSchTime, "%h:%i %p").label("etime"),#
            ExamScheduleHdr.sSemester,#
            AcademicYear.acdname,#
            sem_type.label("semtype")
        )
        .join(ExamScheduleDtl, ExamScheduleDtl.iExamSchKey == ExamScheduleHdr.iExamSchKey)
        .join(Catlouge, Catlouge.catlg_key == ExamScheduleHdr.iExam_ID)
        .join(CatlougeType, CatlougeType.ctyp_key == Catlouge.catlg_ctyp_key)
        .join(B2EClass, B2EClass.class_id == ExamScheduleHdr.iclass_ID)
        .join(AcademicYear, AcademicYear.acdyearid == ExamScheduleHdr.esh_acdyear)
        .join(TblIdSubject, TblIdSubject.Sub_Key == ExamScheduleDtl.sSub_ID)
        .filter(ExamScheduleHdr.dPublishingDate == None)
        .filter(B2EClass.class_id == class_id)
        .order_by(ExamScheduleHdr.dCreatedOn.desc())
    )
     
    results = query.all()
    return [dict(row._mapping) for row in results]


@router.post("/erp/v1/student/exam_result/{student_key}", tags=["Student Management Version 1"])
def get_exam_result(student_key: int, db: Session = Depends(get_db),
                    current_user: str = Depends(get_current_user)):
    query = (
        db.query(
            ExamScheduleHdr.iExamSchKey,
            B2EClass.class_name,
            StudentPersonalInfo.stu_name,
            Catlouge.catlg_code.label("ecode"),
            Catlouge.catlg_description.label("ename"),
            TblIdSubject.SUB_ID.label("subcode"),
            TblIdSubject.SUB_NAME.label("subname"),
            func.date_format(ExamScheduleDtl.dSchDate, "%d/%m/%Y").label("edate"),
            func.date_format(ExamScheduleDtl.sSchTime, "%h:%i %p").label("etime"),
            ExamScheduleDtl.nPass_Mark.label("minmarks"),
            ExamScheduleDtl.nMax_Mark.label("maxmarks"),
            ExamScheduleDtl.iDuration.label("eduration"),
            ExamScheduleHdr.sSemester,
            AcademicYear.acdname,
            case(
                (func.mod(ExamScheduleHdr.sSemester, 2) == 1, "Odd Semester"),
                else_="Even Semester"
            ).label("sem"),
            case(
                (ExamResult.er_passfail == "P", "PASS"),
                else_="FAIL"
            ).label("passfail"),
            case(
                (ExamResult.er_attendance == "A", "ABSENT"),
                else_=""
            ).label("attendance"),
            ExamResult.er_marks,
            StudentPersonalInfo.stu_rollno,
            StudentPersonalInfo.stu_KEY,
        )
        .join(ExamScheduleDtl, ExamScheduleDtl.iExamSchKey == ExamScheduleHdr.iExamSchKey)
        .join(Catlouge, Catlouge.catlg_key == ExamScheduleHdr.iExam_ID)
        .join(CatlougeType, CatlougeType.ctyp_key == Catlouge.catlg_ctyp_key)
        .join(B2EClass, B2EClass.class_id == ExamScheduleHdr.iclass_ID)
        .join(AcademicYear, AcademicYear.acdyearid == ExamScheduleHdr.esh_acdyear)
        .join(TblIdSubject, TblIdSubject.Sub_Key == ExamScheduleDtl.sSub_ID)
        .join(ExamResult, ExamResult.er_examSchDtlKey == ExamScheduleDtl.iExamDtlKey)
        .join(StudentPersonalInfo, StudentPersonalInfo.stu_KEY == ExamResult.er_stuid)
        .filter(
            ExamScheduleHdr.dPublishingDate.isnot(None),
            StudentPersonalInfo.stu_KEY == student_key
        )
        .order_by(ExamScheduleHdr.dCreatedOn.desc())
    )

    results = query.all()
    return [dict(row._mapping) for row in results]




# @router.post("/erp/v1/student/timetable", tags=["Student Management Version 1"])
# def get_timetable(payload: student_timetable, db: Session = Depends(get_db)):
#     # Subquery for grouped ttperiod
#     ttperiod_subq = (
#         db.query(
#             TblColTtPeriod.ttp_orderby.label("ttporderby"),
#             TblColTtPeriod.ttp_dispname.label("ttpdispname")
#         )
#         .group_by(
#             TblColTtPeriod.ttp_orderby,
#             TblColTtPeriod.ttp_dispname
#         )
#         .subquery()
#     )

#     # Subquery for timetable joins
#     timetable_subq = (
#         db.query(
#             TblColTimeTable.tt_period,
#             TblColTtPeriod.ttp_orderby,
#             func.coalesce(TblColTtPeriod.ttp_starts, "").label("ttpstarts"),
#             func.coalesce(TblColTtPeriod.ttp_ends, "").label("ttpends"),
#             func.coalesce(TblIdSubject.SUB_NAME, "").label("subject"),
#             func.coalesce(StaffPersonalInfo.stf_name, "").label("stfname")
#         )
#         .join(TblColTtPeriod, TblColTtPeriod.ttp_id == TblColTimeTable.tt_period)
#         .join(
#             TblColAcdDays,
#             (TblColTimeTable.tt_acdid == TblColAcdDays.addacdid)
#             & (TblColTimeTable.tt_dayorder == TblColAcdDays.adddoid)
#         )
#         .join(TblColAcdDayOrder, TblColAcdDayOrder.doid == TblColAcdDays.adddoid)
#         .join(TblIdSubject, TblIdSubject.Sub_Key == TblColTimeTable.tt_subkey)
#         .join(B2EClass, B2EClass.class_id == TblColTimeTable.tt_classid)
#         .join(StaffPersonalInfo, StaffPersonalInfo.stf_key == TblColTimeTable.tt_stfkey)
#         .filter(
#             TblColAcdDays.adddate == payload.studate,
#             B2EClass.class_id == payload.classid,
#             TblColTimeTable.tt_semoryear.in_(["1"])
#         )
#         .subquery()
#     )

#     # Subquery to get today's dayorder
#     today_dayorder_subq = (
#         db.query(func.ifnull(TblColAcdDays.adddoid, 0))
#         .join(AcademicYear, AcademicYear.acdyearid == TblColAcdDays.addacdid)
#         .filter(
#             func.date(TblColAcdDays.adddate) == date.today(),
#             AcademicYear.currentyear == 1
#         )
#         .scalar_subquery()
#     )

#     # Final query
#     query_results = (
#         db.query(
#             ttperiod_subq.c.ttpdispname,
#             func.coalesce(timetable_subq.c.ttpstarts, "").label("ttpstarts"),
#             func.coalesce(timetable_subq.c.ttpends, "").label("ttpends"),
#             func.coalesce(timetable_subq.c.stfname, "").label("stfname"),
#             func.coalesce(timetable_subq.c.subject, "").label("subject"),
#             today_dayorder_subq.label("doname")
#         )
#         .outerjoin(
#             timetable_subq,
#             ttperiod_subq.c.ttporderby == timetable_subq.c.ttp_orderby
#         )
#         .order_by(ttperiod_subq.c.ttporderby)
#         .all()
#     )

#     # Return only desired fields
#     results = [
#         {
#             "ttpdispname": row.ttpdispname,
#             "ttpstarts": row.ttpstarts,
#             "ttpends": row.ttpends,
#             "stfname": row.stfname,
#             "subject": row.subject,
#             "doname": row.doname
#         }
#         for row in query_results
#     ]                   
#     return results


@router.post("/erp/v1/student/timetable", tags=["Student Management Version 1"])
def get_timetable(payload: student_timetable, db: Session = Depends(get_db),
                    current_user: str = Depends(get_current_user)):

    # Step 1: Get today's adpsemno from dayorderprocess
    target_date = date.today()
    dayorder = (
        db.query(
            B2ETblColAcdDayOrderProcess.adpsemno
        )
        .filter(
            B2ETblColAcdDayOrderProcess.adpstart <= target_date,
            B2ETblColAcdDayOrderProcess.adpend >= target_date
        )
        .first()
    )

    if not dayorder:
        return {"message": "No dayorder found for today"}

    semnos = dayorder.adpsemno.split(",")  # "1,3,5" -> ["1","3","5"]

    # Step 2: Subquery for grouped ttperiod
    ttperiod_subq = (
        db.query(
            TblColTtPeriod.ttp_orderby.label("ttporderby"),
            TblColTtPeriod.ttp_dispname.label("ttpdispname")
        )
        .group_by(
            TblColTtPeriod.ttp_orderby,
            TblColTtPeriod.ttp_dispname
        )
        .subquery()
    )

    # Step 3: Subquery for timetable joins
    timetable_subq = (
        db.query(
            TblColTimeTable.tt_period,
            TblColTtPeriod.ttp_orderby,
            func.coalesce(TblColTtPeriod.ttp_starts, "").label("ttpstarts"),
            func.coalesce(TblColTtPeriod.ttp_ends, "").label("ttpends"),
            func.coalesce(TblIdSubject.SUB_NAME, "").label("subject"),
            func.coalesce(StaffPersonalInfo.stf_name, "").label("stfname")
        )
        .join(TblColTtPeriod, TblColTtPeriod.ttp_id == TblColTimeTable.tt_period)
        .join(
            TblColAcdDays,
            (TblColTimeTable.tt_acdid == TblColAcdDays.addacdid)
            & (TblColTimeTable.tt_dayorder == TblColAcdDays.adddoid)
        )
        .join(TblColAcdDayOrder, TblColAcdDayOrder.doid == TblColAcdDays.adddoid)
        .join(TblIdSubject, TblIdSubject.Sub_Key == TblColTimeTable.tt_subkey)
        .join(B2EClass, B2EClass.class_id == TblColTimeTable.tt_classid)
        .join(StaffPersonalInfo, StaffPersonalInfo.stf_key == TblColTimeTable.tt_stfkey)
        .filter(
            TblColAcdDays.adddate == payload.studate,
            B2EClass.class_id == payload.classid,
            TblColTimeTable.tt_semoryear.in_(semnos)   # <-- dynamic sem numbers
        )
        .subquery()
    )

    # Step 4: Subquery to get today's dayorder
    today_dayorder_subq = (
        db.query(func.ifnull(TblColAcdDays.adddoid, 0))
        .join(AcademicYear, AcademicYear.acdyearid == TblColAcdDays.addacdid)
        .filter(
            func.date(TblColAcdDays.adddate) == date.today(),
            AcademicYear.currentyear == 1
        )
        .scalar_subquery()
    )

    # Step 5: Final query
    query_results = (
        db.query(
            ttperiod_subq.c.ttpdispname,
            func.coalesce(timetable_subq.c.ttpstarts, "").label("ttpstarts"),
            func.coalesce(timetable_subq.c.ttpends, "").label("ttpends"),
            func.coalesce(timetable_subq.c.stfname, "").label("stfname"),
            func.coalesce(timetable_subq.c.subject, "").label("subject"),
            today_dayorder_subq.label("doname")
        )
        .outerjoin(
            timetable_subq,
            ttperiod_subq.c.ttporderby == timetable_subq.c.ttp_orderby
        )
        .order_by(ttperiod_subq.c.ttporderby)
        .all()
    )

    results = [
        {
            "ttpdispname": row.ttpdispname,
            "ttpstarts": row.ttpstarts,
            "ttpends": row.ttpends,
            "stfname": row.stfname,
            "subject": row.subject,
            "doname": row.doname
        }
        for row in query_results
    ]

    return results


@router.get("/erp/v1/student/generalnotification", tags=["Student Management Version 1"])
def get_generalnotification(db: Session = Depends(get_db),
                   current_user: str = Depends(get_current_user)):
    results = (
        db.query(
            Notification.notify_msg,
            func.date_format(Notification.notify_postedon, '%d/%m/%Y').label("notify_posted"),
            func.ifnull(Notification.notifyattach, '').label("notifyattach"),
            Notification.notifyattachfile,
            AppSettings.appserver
        )
        .select_from(Notification)
        .join(AppSettings, literal(True), isouter=True)
        .filter(
            Notification.notify_type == "G",
            Notification.wfstatus == "0",
            Notification.status == "0"
        )
        .order_by(Notification.notify_postedon.desc())
        .all()
    )

    # Convert Row objects to dict
    return [
        {
            "notify_msg": row.notify_msg,
            "notify_posted": row.notify_posted,
            "notifyattach": row.notifyattach,
            "notifyattachfile": row.notifyattachfile,
            "appserver": row.appserver,
        }
        for row in results
    ]


@router.get("/erp/v1/student/departmentnotification", tags=["Student Management Version 1"])
def get_departmentnotification(department_id: int, db: Session = Depends(get_db),
                   current_user: str = Depends(get_current_user)):
    department_notification = (
        db.query(
            PersonalNotification.content,
            PersonalNotification.imagepath,
            PersonalNotification.usertype,
            PersonalNotification.createdby,
            PersonalNotification.createdon
        ).filter(PersonalNotification.deptid == department_id )
        .order_by(PersonalNotification.depchnid.desc())
        .all()
    )

    return [
        {
            "content":row.content,
            "imagepath":row.imagepath,
            "usertype":row.usertype,
            "createdby":row.createdby,
            "createdon":row.createdon
        }
        for row in department_notification
    ]


@router.get("/erp/v1/student/personalnotifications/{stu_key}", tags=["Student Management Version 1"])
def get_notifications(stu_key: int, db: Session = Depends(get_db),
                        current_user: str = Depends(get_current_user)):
    notifications = (
        db.query(
            Notification.notify_msg,
            func.date_format(Notification.notify_postedon, "%d/%m/%Y").label("notify_posted"),
            func.ifnull(Notification.notifyattach, "").label("notifyattach"),
            Notification.notifyattachfile,
            AppSettings.appserver,
        )
        .select_from(Notification)
        .join(StudentPersonalInfo, StudentPersonalInfo.stu_KEY == Notification.notify_stdid)
        .join(AppSettings, true())  # CROSS JOIN
        .filter(
            StudentPersonalInfo.stu_KEY == stu_key,
            Notification.notify_type.in_(["S", "T"]),
            Notification.wfstatus == "0",
            Notification.status == "0",
        )
        .order_by(Notification.notify_postedon.desc())
        .all()
    )

    # Convert SQLAlchemy Row objects into dicts
    return [dict(row._mapping) for row in notifications]



# @router.get("/dayorderprocess")
# def get_dayorderprocess(db: Session = Depends(get_db)):
#     # Dynamically get today’s date in YYYY-MM-DD format
#     target_date = date.today()

#     results = (
#         db.query(
#             B2ETblColAcdDayOrderProcess.adpsemno,
#             B2ETblColAcdDayOrderProcess.adpname
#         )
#         .filter(
#             B2ETblColAcdDayOrderProcess.adpstart <= target_date,
#             B2ETblColAcdDayOrderProcess.adpend >= target_date
#         )
#         .all()
#     )

#     return [dict(r._mapping) for r in results]  # Convert Row objects to dicts



# Map Roman → Number (1 to 5 only)

ROMAN_MAP = {
    "I": 1,
    "II": 2,
    "III": 3,
    "IV": 4,
    "V": 5
}

@router.post("/erp/v1/student/batchschedule", response_model=list[BatchScheduleResponse],
              tags=["Student Management Version 1"])
def get_batchschedule(payload: BatchScheduleRequest, db: Session = Depends(get_db),
                      ):

    target_date = date.today()

    # Step 1: Get adpsemno dynamically
    dayorder = (
        db.query(B2ETblColAcdDayOrderProcess.adpsemno,
                 B2ETblColAcdDayOrderProcess.adpname)
        .filter(
            B2ETblColAcdDayOrderProcess.adpstart <= target_date,
            B2ETblColAcdDayOrderProcess.adpend >= target_date
        )
        .first()
    )
    if not dayorder:
        return []
    

    semnos = [int(s.strip()) for s in dayorder.adpsemno.split(",")]
    adpname = dayorder.adpname

    # Step 2: Build dynamic classacdid list → [payload.classacdid, -1, -2]
    classacdid_list = [str(payload.classacdid - i) for i in range(3)]

    # Step 3: Fetch student year (Roman → Number)
    student = (
        db.query(StudentPersonalInfo.stu_year)
        .filter(StudentPersonalInfo.stu_KEY == payload.stu_key)   # assume stu_key is part of payload
        .first()
    )
    if not student:
        return []

    yearno = ROMAN_MAP.get(student.stu_year.upper(), student.stu_year)

    # Step 4: Query with dynamic payload values
    results = (
        db.query(TblColBatchSchedule.bsh_startdate)
        .join(B2EClass, B2EClass.class_id == TblColBatchSchedule.bsh_classid)
        .join(CourseBranch, CourseBranch.cbid == B2EClass.cbid)
        .join(B2EDepartment, B2EDepartment.bcatid == CourseBranch.cdeptid)
        .filter(
            CourseBranch.cdeptid == payload.cdeptid,
            B2EClass.cbid == payload.cbid,
            TblColBatchSchedule.bsh_semno.in_(semnos),
            B2EClass.classacdid.in_(classacdid_list),
            func.substr(func.cast(TblColBatchSchedule.bsh_startdate, String), 1, 2) != "00",
            TblColBatchSchedule.bsh_yearno == yearno,   # ✅ now using converted value
            B2EClass.class_id == payload.class_id,
        )
        .all()
    )

    return [
    BatchScheduleResponse(
        bsh_startdate=r.bsh_startdate,
        adpname=adpname   
    )
    for r in results
]




@router.post("/erp/v1/student/hourly_attendance", tags=["Student Management Version 1"])
def get_hourly_attendance(payload: AttendanceRequest, db: Session = Depends(get_db),
                           ):

    class_id = payload.class_id
    stu_key = payload.stu_key
    start_date = payload.start_date
    end_date = payload.end_date
    acdname = payload.acdname

    # ----------------------
    # Subquery: total hours from vw_student_schedule
    # ----------------------
    schedule_subq = (
        db.query(
            func.count().label("total_count"),
            B2EStudent_schedule.class_id,
            B2EStudent_schedule.class_name,
            B2EStudent_schedule.acdyearid
        )
        .filter(
            B2EStudent_schedule.adddate.between(start_date, end_date),
            B2EStudent_schedule.class_id == class_id
        )
        .group_by(
            B2EStudent_schedule.class_name,
            B2EStudent_schedule.class_id,
            B2EStudent_schedule.acdyearid
        )
        .subquery()
    )

    # ----------------------
    # Subquery: academic year filter
    # ----------------------
    acdyear_subq = (
        db.query(AcademicYear.acdyearid)
        .filter(AcademicYear.acdname == acdname)
        .subquery()
    )

    # ----------------------
    # Inner query (per student)
    # ----------------------
    inner_q = (
        db.query(
            B2EClass.class_id.label("class_id"),
            B2EClass.class_name.label("class_name"),
            CourseBranch.branchname.label("branchname"),
            B2EDepartment.bcatname.label("bcatname"),
            StudentPersonalInfo.stu_rollno.label("stu_rollno"),
            StudentPersonalInfo.stu_name.label("stu_name"),
            schedule_subq.c.total_count.label("tothrs"),
            func.sum(case((B2EStudent_detail.atd_status == "P", 1), else_=0)).label("attn"),
            func.sum(case((B2EStudent_detail.atd_status == "A", 1), else_=0)).label("absnt")
        )
        .select_from(TblColStuAtdHdr)
        .join(B2EStudent_detail, TblColStuAtdHdr.attkey == B2EStudent_detail.atd_attkey)
        .join(StudentPersonalInfo, B2EStudent_detail.atd_stdid == StudentPersonalInfo.stu_KEY)
        .join(B2EClass, StudentPersonalInfo.stu_classid == B2EClass.class_id)
        .join(CourseBranch, B2EClass.cbid == CourseBranch.cbid)
        .outerjoin(B2EDepartment, CourseBranch.cdeptid == B2EDepartment.bcatid)
        .join(schedule_subq, schedule_subq.c.class_id == B2EClass.class_id)
        .filter(
            B2EClass.class_id == class_id,
            StudentPersonalInfo.stu_longabs.in_([0]),
            TblColStuAtdHdr.atddate.between(start_date, end_date),
            StudentPersonalInfo.stu_KEY == stu_key,
            schedule_subq.c.acdyearid.in_(acdyear_subq)
        )
        .group_by(
            B2EClass.class_id,
            B2EClass.class_name,
            CourseBranch.branchname,
            B2EDepartment.bcatname,
            StudentPersonalInfo.stu_rollno,
            StudentPersonalInfo.stu_name,
            schedule_subq.c.total_count
        )
        .subquery()
    )

    # ----------------------
    # Outer query (final result with percentage)
    # ----------------------
    final_q = (
        db.query(
            inner_q.c.class_id,
            inner_q.c.class_name,
            inner_q.c.branchname,
            inner_q.c.bcatname,
            inner_q.c.stu_rollno,
            inner_q.c.stu_name,
            inner_q.c.tothrs,
            func.sum(inner_q.c.attn).label("attn"),
            func.sum(inner_q.c.absnt).label("absnt"),
            func.round(
                (func.sum(inner_q.c.attn) / cast(inner_q.c.tothrs, Integer)) * 100,
                0
            ).label("percent")
        )
        .select_from(inner_q)
        .group_by(
            inner_q.c.class_id,
            inner_q.c.class_name,
            inner_q.c.branchname,
            inner_q.c.bcatname,
            inner_q.c.stu_rollno,
            inner_q.c.stu_name,
            inner_q.c.tothrs
        )
        .order_by(
            func.round((func.sum(inner_q.c.attn) / cast(inner_q.c.tothrs, Integer)) * 100, 0).desc()
        )
    )

    results = final_q.all()

    return [dict(r._mapping) for r in results]
