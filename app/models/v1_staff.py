from sqlalchemy import Column, Integer, String, DateTime,Date
from app.database import Base
from sqlalchemy.orm import relationship



class TblColTtPeriod(Base):
    __tablename__ = "b2e_tbl_col_ttperiod"

    ttp_id = Column(Integer, primary_key=True)
    ttp_orderby = Column(Integer)
    ttp_dispname = Column(String)
    ttp_starts = Column(DateTime)
    ttp_ends = Column(DateTime)
    ttp_name = Column(String)


class TblColTimeTable(Base):
    __tablename__ = "b2e_tbl_col_timetable"

    tt_key = Column(Integer, primary_key=True)
    tt_period = Column(Integer)      # no ForeignKey
    tt_acdid = Column(Integer)
    tt_dayorder = Column(Integer)
    tt_subkey = Column(String)       # no ForeignKey
    tt_classid = Column(Integer)     # no ForeignKey
    tt_stfkey = Column(String)
    tt_semoryear = Column(Integer)
    tt_stfmapflg = Column(String)

class TblColAcdDays(Base):
    __tablename__ = "b2e_tbl_col_acddays"

    addacdid = Column(Integer, primary_key=True)
    adddoid = Column(Integer)
    addday = Column(String)
    adddate = Column(Date)


class TblColAcdDayOrder(Base):
    __tablename__ = "b2e_tbl_col_acddayorder"

    doid = Column(Integer, primary_key=True)
    doorderno = Column(Integer)
    doname = Column(String)


class TblIdSubject(Base):
    __tablename__ = "b2e_tbl_id_subject"

    Sub_Key = Column(String, primary_key=True)
    SUB_ID = Column(String)
    SUB_NAME = Column(String)
    SUB_SHORTNAME = Column(String)
    SUBTYP_KEY = Column(Integer)
    SUB_UNITNAME = Column(String)
    SUB_POINTS = Column(Integer)



class TblColBatchSchedule(Base):
    __tablename__ = "b2e_tbl_col_batchschedule"

    bsh_id = Column(Integer, primary_key=True)
    bsh_classid = Column(Integer)
    bsh_startdate = Column(Date)
    bsh_enddate = Column(Date)
    bsh_semno = Column(Integer)
    bsh_yearno = Column(Integer)


class TblColStuAtdHdr(Base):
    __tablename__ = "b2e_tbl_col_stuatdhdr"

    attkey = Column(Integer, primary_key=True,index=True)
    atdclassid = Column(Integer)
    atdperiod = Column(Integer)
    atddate = Column(Date)
    atdsem = Column(Integer)
    atdstatus = Column(String)
    franchiseid = Column(Integer)
    processid = Column(Integer)
    wfstatus = Column(String)
    revision = Column(Integer)
    createdby = Column(String)
    createdon = Column(DateTime)


class B2ETblColAcdDayOrderProcess(Base):
    __tablename__ = "b2e_tbl_col_acddayorderprocess"    

    adpid = Column(Integer, primary_key=True)
    adpsemno = Column(String)
    adpstart = Column(Date)
    adpend = Column(Date)
    adpname = Column(String)
    adpacdid = Column(Integer)
    
 
class CatlougeType(Base):
    __tablename__ = "b2e_tbl_id_tb_cataltype" 

    ctyp_key = Column(Integer, primary_key = True)
    ctyp_code = Column(String)
    ctyp_desc = Column(String)
    ctyp_iseditable = Column(Integer)
    ctyp_st_key = Column(Integer) 



class VwDayordPeriodStfSubjClass(Base):  # model name for vw_dayord_period_stf_subj_class
    __tablename__ = "vw_dayord_period_stf_subj_class"

    ttp_orderby = Column(Integer)
    ttp_dispname = Column(String)
    ttp_starts = Column(String)
    ttp_ends = Column(String)
    sub_id = Column(Integer)
    sub_name = Column(String)
    class_name = Column(String)
    class_code = Column(String)
    doorderno = Column(Integer)
    doname = Column(String)
    stf_key = Column(Integer, primary_key = True)
    class_id = Column(Integer)
    ttp_id = Column(Integer)
    sub_key = Column(Integer)
    tt_semoryear = Column(Integer)
    doid = Column(Integer)    