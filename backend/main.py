from fastapi import FastAPI
from pydantic import BaseModel
from geopy.distance import geodesic
from models.db_setup import Attendance, SessionLocal

app = FastAPI()

# Replace with your campus coordinates
CAMPUS_COORDS = (12.9716, 77.5946)

class AttendanceIn(BaseModel):
    student: str
    latitude: float
    longitude: float

@app.post("/mark_attendance/")
def mark_attendance(data: AttendanceIn):
    distance = geodesic((data.latitude, data.longitude), CAMPUS_COORDS).meters
    if distance > 100:
        return {"status": "failed", "reason": "Out of range"}
    session = SessionLocal()
    record = Attendance(student=data.student, latitude=data.latitude, longitude=data.longitude)
    session.add(record)
    session.commit()
    return {"status": "success", "distance_m": distance}
