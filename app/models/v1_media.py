from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base

class StudentFile(Base):
    __tablename__ = "b2e_tbl_col_stufiles"

    sfid = Column(Integer, primary_key=True, index=True)
    sfstu_id = Column(Integer)
    filetitle = Column(String(255))
    filename = Column(String(255))
    filepath = Column(String(255))
    viewattach = Column(String(255))
    uploadby = Column(String(255))
    uploadon = Column(DateTime)