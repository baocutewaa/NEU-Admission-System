from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any

from app.api.deps import get_db
from app.crud.crud_student import student_crud
from app.crud.crud_admission import admission_crud

router = APIRouter()

@router.get("/{cccd}", response_model=Any)
def get_student_profile(cccd: str, db: Session = Depends(get_db)):
    """
    Tra cứu hồ sơ thí sinh theo CCCD
    """
    student = student_crud.get_student_by_cccd(db, cccd=cccd)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
        
    contact = student_crud.get_student_contact(db, cccd=cccd)
    scores = student_crud.get_student_scores(db, cccd=cccd)
    aspirations = admission_crud.get_aspirations_by_student(db, cccd=cccd, nam_tuyen_sinh=2024) # default year 2024
    enrollment = admission_crud.get_enrollment_profile(db, cccd=cccd)
    
    return {
        "profile": student,
        "contact": contact,
        "scores": scores,
        "aspirations": aspirations,
        "enrollment": enrollment
    }
