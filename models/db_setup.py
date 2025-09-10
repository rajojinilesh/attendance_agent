from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///attendance.db"
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True)
    student = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)
