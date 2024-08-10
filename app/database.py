from sqlalchemy import create_engine, TIMESTAMP
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:yoloxdrdz@localhost:3306/fastapi"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    type_annotation_map = {
        datetime: TIMESTAMP(timezone=True)
    }


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
