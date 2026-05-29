from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.student import ThiSinh, LienHe, DiemThi, ChungChi, ThiSinhChungChi

class CRUDStudent:
    def get_student_by_cccd(self, db: Session, cccd: str) -> Optional[ThiSinh]:
        return db.query(ThiSinh).filter(ThiSinh.CCCD == cccd).first()

    def get_students(self, db: Session, skip: int = 0, limit: int = 100) -> List[ThiSinh]:
        return db.query(ThiSinh).offset(skip).limit(limit).all()

    def get_student_contact(self, db: Session, cccd: str) -> Optional[LienHe]:
        return db.query(LienHe).filter(LienHe.CCCD == cccd).first()

    def get_student_scores(self, db: Session, cccd: str) -> List[DiemThi]:
        return db.query(DiemThi).filter(DiemThi.CCCD == cccd).all()
        
    def get_student_certificates(self, db: Session, cccd: str) -> List[ThiSinhChungChi]:
        return db.query(ThiSinhChungChi).filter(ThiSinhChungChi.CCCD == cccd).all()

student_crud = CRUDStudent()
