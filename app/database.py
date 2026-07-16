from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

FILE_DATABASE_URL = "mysql+mysqlconnector://hcas:hcas@127.0.0.1:4407/hcas"

engine = create_engine(FILE_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()