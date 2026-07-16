from fastapi import APIRouter,Query,Path
from fastapi import Depends,HTTPException

from app.schemas.v1_student import *
from app.schemas.v1_staff import *
from app.models.v1_student import *
from app.models.v1_staff import *

from sqlalchemy.orm import Session, aliased
from app.database import SessionLocal
from app.database import get_db
from sqlalchemy import and_

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
from sqlalchemy import text
from sqlalchemy import func, case, and_,literal
from app.dependencies import get_current_user
import datetime

router = APIRouter()


@router.post("/erp/v1/staff/todaytimetable", tags=["Staff Management Version 1"])
def get_timetable(data: TimeTable, db: Session = Depends(get_db),
                    current_user: str = Depends(get_current_user)):
    stfkey = data.stfkey           
    stfdate = data.stfdate   
    today = date.today()
    results = (
        db.query(B2ETblColAcdDayOrderProcess.adpsemno)
        .filter(B2ETblColAcdDayOrderProcess.adpstart <= today)
        .filter(B2ETblColAcdDayOrderProcess.adpend >= today)
        .all()
    )
    sem_list = [int(x) for row in results for x in row[0].split(",")]
    

    # Subquery A: All periods

    sub_a = (
        db.query(
            TblColTtPeriod.ttp_orderby.label("ttporderby"),
            TblColTtPeriod.ttp_dispname.label("ttpdispname")
        )
        .group_by(TblColTtPeriod.ttp_orderby, TblColTtPeriod.ttp_dispname)
        .subquery()
    )

    # Subquery B: Timetable with joins
    sub_b = (
        db.query(
            TblColTtPeriod.ttp_orderby,
            TblColTtPeriod.ttp_starts,
            TblColTtPeriod.ttp_ends,
            TblIdSubject.SUB_ID,
            TblIdSubject.SUB_NAME,
            B2EClass.class_name,
            B2EClass.class_code,
            TblColAcdDayOrder.doorderno,
            TblColAcdDayOrder.doname,
            TblColAcdDays.addday,
            TblColTimeTable.tt_stfkey,
            B2EClass.class_id,
            TblColTtPeriod.ttp_id,
            TblIdSubject.Sub_Key,
            TblColTimeTable.tt_semoryear,
            TblColStuAtdHdr.atdstatus
        )
        .join(TblColTtPeriod, TblColTtPeriod.ttp_id == TblColTimeTable.tt_period)
        .join(
            TblColAcdDays,
            (TblColTimeTable.tt_acdid == TblColAcdDays.addacdid) &
            (TblColTimeTable.tt_dayorder == TblColAcdDays.adddoid)
        )
        .join(TblColAcdDayOrder, TblColAcdDays.adddoid == TblColAcdDayOrder.doid)
        .join(TblIdSubject, TblColTimeTable.tt_subkey == TblIdSubject.Sub_Key)
        .join(B2EClass, TblColTimeTable.tt_classid == B2EClass.class_id)
        .filter(
            TblColAcdDays.adddate == stfdate,
            TblColTimeTable.tt_stfkey == stfkey,
            TblColTimeTable.tt_semoryear.in_(sem_list)
        )
        .join(
            TblColBatchSchedule,
            (TblColBatchSchedule.bsh_classid == B2EClass.class_id) &
            (func.date(stfdate) >= TblColBatchSchedule.bsh_startdate) &
            (func.date(stfdate) <= TblColBatchSchedule.bsh_enddate)
        )
        .outerjoin(
            TblColStuAtdHdr,
            (TblColStuAtdHdr.atdclassid == B2EClass.class_id) &
            (TblColTtPeriod.ttp_id == TblColStuAtdHdr.atdperiod) &
            (TblColStuAtdHdr.atddate == stfdate) &
            (TblColStuAtdHdr.atdsem.in_(sem_list))
        )
        .subquery()
    )

    # Final query
    query = (
        db.query(
            sub_a.c.ttporderby,
            sub_a.c.ttpdispname,
            sub_b.c.ttp_starts.label("ttpstarts"),
            sub_b.c.ttp_ends.label("ttpends"),
            sub_b.c.SUB_ID.label("SUBID"),
            sub_b.c.SUB_NAME.label("SUBNAME"),
            sub_b.c.class_name.label("classname"),
            sub_b.c.class_code.label("classcode"),
            sub_b.c.doorderno,
            sub_b.c.doname,
            sub_b.c.addday,
            sub_b.c.tt_stfkey.label("staffkey"),
            sub_b.c.class_id.label("classid"),
            sub_b.c.ttp_id.label("periodid"),
            sub_b.c.Sub_Key.label("subkey"),
            sub_b.c.doorderno.label("dayorder"),
            sub_b.c.tt_semoryear.label("semyear"),
            case(
                (sub_b.c.atdstatus.is_(None), "notdone"),
                else_="done"
            ).label("dispatdstatus")
        )
        .outerjoin(sub_b, sub_a.c.ttporderby == sub_b.c.ttp_orderby)
        .order_by(sub_a.c.ttporderby)
    )

    result = query.all()
    return [dict(row._mapping) for row in result]
    
    
@router.post("/erp/v1/staff/studentlist", tags=["Staff Management Version 1"])
def get_students(data: AttendanceRequest, db: Session = Depends(get_db),
                      current_user: str = Depends(get_current_user)):
    # Subquery for timetable students
    subq = (
        db.query(TimeTableStud.st_stu_key)
        .join(TblColTimeTable, TblColTimeTable.tt_key == TimeTableStud.st_tt_key)
        .filter(
            TblColTimeTable.tt_period == data.periodid,
            TblColTimeTable.tt_classid == data.classid,
            TblColTimeTable.tt_semoryear.in_([int(x) for x in data.semyear.split(",")]),
            TblColTimeTable.tt_subkey == data.subid,
            TblColTimeTable.tt_dayorder == data.dayorder,
            TblColTimeTable.tt_acdid == data.acdid
        )
        .subquery()
    )

    # Current Academic Year subquery
    current_year_subq = (
        db.query(AcademicYear.acdyearid)
        .filter(AcademicYear.currentyear == 1)
        .scalar_subquery()
    )

    # Main Query – fetch only needed columns
    results = (
        db.query(
            StudentPersonalInfo.stu_KEY,
            StudentPersonalInfo.stu_rollno,
            StudentPersonalInfo.stu_name
        )
        .join(subq, subq.c.st_stu_key == StudentPersonalInfo.stu_KEY)
        .filter(
            StudentPersonalInfo.stu_statusflg.in_([0, 1]),
            StudentPersonalInfo.stu_longabs == 0,
            StudentPersonalInfo.stu_acadamicyear == current_year_subq,
        )
        .order_by(StudentPersonalInfo.stu_rollno, StudentPersonalInfo.stu_ID)
        .all()
    )

    # Convert to JSON-friendly list of dicts
    response = [
        {
            "Student_Key": r.stu_KEY,
            "RollNo": r.stu_rollno,
            "Name": r.stu_name
        }
        for r in results
    ]
    return response



@router.post("/erp/v1/staff/attendance/dropdown")
def get_attendance(payload: Attendance_dropdown, db: Session = Depends(get_db),
                      current_user: str = Depends(get_current_user)):
    stf_key = payload.stf_key
    adddate = payload.adddate

    subquery = (
        db.query(TblColBatchSchedule.bsh_semno)
        .filter(
            and_(
                adddate >= TblColBatchSchedule.bsh_startdate,
                adddate <= TblColBatchSchedule.bsh_enddate,
            )
        )
        .distinct()
        .subquery()
    )

    query = (
        db.query(
            func.distinct(func.trim(B2EClass.class_name)).label("class_name"),
            TblColTtPeriod.ttp_name,
            TblColTtPeriod.ttp_id,
            B2EClass.class_id,
            TblColAcdDayOrder.doname,
            TblColAcdDayOrder.doid,
            TblColTimeTable.tt_semoryear,
            TblIdSubject.Sub_Key,
        )
        .join(TblColAcdDayOrder, TblColTimeTable.tt_dayorder == TblColAcdDayOrder.doid)
        .join(StaffPersonalInfo, TblColTimeTable.tt_stfkey == StaffPersonalInfo.stf_key)
        .join(B2EClass, TblColTimeTable.tt_classid == B2EClass.class_id)
        .join(TblIdSubject, TblColTimeTable.tt_subkey == TblIdSubject.Sub_Key)
        .join(TblColTtPeriod, TblColTimeTable.tt_period == TblColTtPeriod.ttp_id)
        .join(TblColAcdDays, TblColAcdDayOrder.doid == TblColAcdDays.adddoid)
        .filter(
            TblColTimeTable.tt_acdid == 25,
            StaffPersonalInfo.stf_key == stf_key,
            StaffPersonalInfo.statusflag == 0,
            TblColAcdDays.adddate == adddate,
            TblColTimeTable.tt_semoryear.in_(subquery),
        )
        .order_by(TblColTtPeriod.ttp_name)
    )

    result = query.all()
    return {"data": [dict(row._mapping) for row in result]}

def seconds_to_time(value):
    if value is None:
        return ""
    # If it's already timedelta, convert to HH:MM:SS
    if isinstance(value, datetime.timedelta):
        total_seconds = int(value.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    # If it's integer in seconds
    elif isinstance(value, (int, float)):
        return str(datetime.timedelta(seconds=int(value)))
    # If it's already a string, just return it
    return str(value)


@router.post("/erp/v1/staff/attendance_status")
def get_attendance_status(payload: LoadPeriod, db: Session = Depends(get_db),
                           current_user: str = Depends(get_current_user)):

    hdr = aliased(TblColStuAtdHdr)
    dtl = aliased(B2EStudent_detail)
    timetable = aliased(TblColTimeTable)

    # Subquery for attendance details
    subq = (
        db.query(
            hdr.atdclassid,
            hdr.atdstatus,
            hdr.atddate,
            hdr.atdperiod,
            dtl.atd_subjectkey
        )
        .join(dtl, hdr.attkey == dtl.atd_attkey)
        .filter(
            hdr.atddate == payload.addeate,
            hdr.atdperiod == payload.tt_period,
            hdr.atdclassid == payload.tt_classid,
            dtl.atd_staffkey.in_(
                db.query(timetable.tt_stfkey)
                .filter(
                    timetable.tt_classid == payload.tt_classid,
                    timetable.tt_period == payload.tt_period,
                    timetable.tt_subkey == payload.tt_subkey,
                    timetable.tt_stfmapflg.in_([0, 1])
                )
            )
        )
        .subquery()
    )

    # Main query
    query = (
        db.query(
            VwDayordPeriodStfSubjClass.ttp_orderby.label("ttporderby"),
            VwDayordPeriodStfSubjClass.ttp_dispname.label("ttpdispname"),
            VwDayordPeriodStfSubjClass.ttp_starts,
            VwDayordPeriodStfSubjClass.ttp_ends,
            VwDayordPeriodStfSubjClass.sub_id,
            VwDayordPeriodStfSubjClass.sub_name,
            VwDayordPeriodStfSubjClass.class_name,
            VwDayordPeriodStfSubjClass.class_code,
            VwDayordPeriodStfSubjClass.doorderno,
            VwDayordPeriodStfSubjClass.doname,
            TblColAcdDays.addday,
            VwDayordPeriodStfSubjClass.stf_key,
            VwDayordPeriodStfSubjClass.class_id,
            VwDayordPeriodStfSubjClass.ttp_id,
            VwDayordPeriodStfSubjClass.sub_key,
            VwDayordPeriodStfSubjClass.tt_semoryear,
            subq.c.atdstatus,
        )
        .join(TblColAcdDays, VwDayordPeriodStfSubjClass.doid == TblColAcdDays.adddoid)
        .outerjoin(
            subq,
            (subq.c.atdclassid == VwDayordPeriodStfSubjClass.class_id) &
            (subq.c.atdperiod == VwDayordPeriodStfSubjClass.ttp_id) &
            (TblColAcdDays.adddate == subq.c.atddate) &
            (VwDayordPeriodStfSubjClass.sub_key == subq.c.atd_subjectkey)
        )
        .filter(
            TblColAcdDays.addacdid.in_(
                db.query(TblColAcdDays.addacdid).filter(TblColAcdDays.adddate == payload.addeate)
            ),
            TblColAcdDays.adddate == payload.addeate,
            VwDayordPeriodStfSubjClass.ttp_id == payload.tt_period,
            VwDayordPeriodStfSubjClass.class_id == payload.tt_classid,
            VwDayordPeriodStfSubjClass.stf_key == payload.stf_key,
            VwDayordPeriodStfSubjClass.tt_semoryear == payload.semoryear
        )
    )

    rows = query.all()

    # Case logic for "done" / "notdone"
    response = []
    for row in rows:
        row_dict = row._asdict()
        response.append({
            "ttporderby": row_dict.get("ttporderby"),
            "ttpdispname": row_dict.get("ttpdispname"),
            "ttpstarts": seconds_to_time(row_dict.get("ttp_starts")),
            "ttpends": seconds_to_time(row_dict.get("ttp_ends")),
            "SUBID": row_dict.get("sub_id"),
            "SUBNAME": row_dict.get("sub_name"),
            "classname": row_dict.get("class_name"),
            "classcode": row_dict.get("class_code"),
            "doorderno": row_dict.get("doorderno"),
            "doname": row_dict.get("doname"),
            "addday": row_dict.get("addday"),
            "staffkey": row_dict.get("stf_key"),
            "classid": row_dict.get("class_id"),
            "periodid": row_dict.get("ttp_id"),
            "subkey": row_dict.get("sub_key"),
            "dayorder": row_dict.get("doorderno"),   # if this is correct mapping
            "semyear": row_dict.get("tt_semoryear"),
            "dispatdstatus": "done" if row_dict.get("atdstatus") else "notdone"
        })


    return response




@router.post("/erp/v1/staff/attendance_post")
def student_attendance_insert(
    payload: AttendancePayload,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    data = payload.data

    # Check for duplicate
    existing_record = db.query(TblColStuAtdHdr).filter(
        and_(
            TblColStuAtdHdr.atdclassid == data.atdclassid,
            TblColStuAtdHdr.createdby == data.createdby,
            TblColStuAtdHdr.atddate == data.atddate,
            TblColStuAtdHdr.atdperiod == data.atdperiod
        )
    ).first()

    if existing_record:
        raise HTTPException (
            status_code=400,
            detail="Duplicate record found. Entry already exists with the same atdclassid, createdby, and atddate/period."
        )

    # Insert parent record
    new_parent = TblColStuAtdHdr(
        atdclassid=data.atdclassid,
        atdsem=data.atdsem,
        atddate=data.atddate,
        atdperiod=data.atdperiod,
        atdstatus=data.atdstatus,
        franchiseid=data.franchiseid,
        processid=data.processid,
        wfstatus=data.wfstatus,
        revision=data.revision,
        createdby=data.createdby,
        createdon=data.createdon
    )
    db.add(new_parent)
    db.commit()
    db.refresh(new_parent)
    parent_id = new_parent.attkey

    # Insert child records
    child_records = [
        B2EStudent_detail(
            atd_attkey=parent_id,
            atd_reason=child.atd_reason,
            atd_status=child.atd_status,
            atd_subjectkey=child.atd_subjectkey,
            atd_staffkey=child.atd_staffkey,
            atd_stdid=child.atd_stdid
        )
        for child in data.child_data
    ]

    if child_records:
        db.add_all(child_records)
        db.commit()

    return {
        "message": "Data Inserted Successfully",
        "parent_id": parent_id,
        "child_count": len(child_records)
    }
    
    
    

@router.get("/erp/v1/staff/attandance/studentlist/{class_id}")
def get_students(class_id: str, db: Session = Depends(get_db),
                   current_user: str = Depends(get_current_user)):
    # Subquery for current academic year
    subquery = (
        db.query(AcademicYear.acdyearid)
        .filter(AcademicYear.currentyear == 1)
        .subquery()
    )

    # Main query
    query = (
        db.query(
            StudentPersonalInfo.stu_KEY,
            StudentPersonalInfo.stu_ID,
            StudentPersonalInfo.stu_name,
            func.ifnull(StudentPersonalInfo.stu_parentmobile, "").label("stuparentmobile"),
            literal("0").label("atdstatus"),
            literal("0").label("atd_id"),
            literal("0").label("atdsmsnotify"),
            literal("0").label("atdemailnotify"),
            literal("").label("atdreason"),
            literal("").label("attkey"),
            StudentPersonalInfo.stu_rollno,
            StudentPersonalInfo.stu_admissionno,
        )
        .filter(StudentPersonalInfo.stu_classid == class_id)   # <-- parameter
        .filter(StudentPersonalInfo.stu_statusflg.in_([0, 1]))
        .filter(StudentPersonalInfo.stu_acadamicyear == subquery.as_scalar())
        .order_by(StudentPersonalInfo.stu_rollno)
    )

    result = query.all()

    # Convert Row objects -> dicts
    students = [
        {
            "stu_KEY": r.stu_KEY,
            "stu_ID": r.stu_ID,
            "stu_name": r.stu_name,
            "stuparentmobile": r.stuparentmobile,
            "atdstatus": r.atdstatus,
            "atd_id": r.atd_id,
            "atdsmsnotify": r.atdsmsnotify,
            "atdemailnotify": r.atdemailnotify,
            "atdreason": r.atdreason,
            "attkey": r.attkey,
            "stu_rollno": r.stu_rollno,
            "stu_admissionno": r.stu_admissionno,
        }
        for r in result
    ]

    return {"students": students}    