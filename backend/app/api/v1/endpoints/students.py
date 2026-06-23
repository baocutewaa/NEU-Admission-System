from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.schemas.student import StudentProfileResponse

from app.api.deps import get_db
from app.models.admission import Nganh
from app.models.student import ThiSinh
from app.crud.crud_student import student_crud
from app.crud.crud_admission import admission_crud

router = APIRouter()

# ==========================================
# ENDPOINT: /search
# Hỗ trợ tìm kiếm danh sách thí sinh (Tên hoặc CCCD)
# ==========================================
@router.get("/search")
def search_students(q: str = Query(..., description="Từ khóa tìm kiếm (Tên hoặc CCCD)"), db: Session = Depends(get_db)):
    """
    Tìm kiếm học sinh theo Tên hoặc CCCD.
    Trả về danh sách rút gọn để hiển thị bảng.
    """
    results = db.query(ThiSinh).filter(
        or_(
            ThiSinh.HoTen.ilike(f"%{q}%"),
            ThiSinh.CCCD.ilike(f"%{q}%")
        )
    ).limit(50).all()
    
    formatted_results = []
    for student in results:
        formatted_results.append({
            "cccd": student.CCCD,
            "ma_dinh_danh": student.CCCD,
            "ho_ten": student.HoTen,
            "gioi_tinh": student.GioiTinh
        })
        
    return jsonable_encoder(formatted_results)

# ==========================================
# ENDPOINT: /{cccd}
# Tra cứu hồ sơ chi tiết (File gốc của bạn)
# ==========================================
@router.get("/{cccd}", response_model=StudentProfileResponse)
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

    scores_grouped = {}
    for score in scores:
        exam_scores = scores_grouped.setdefault(score.MaKyThi, [])
        exam_scores.append({
            "MaMon": score.MaMon,
            "Diem": score.Diem,
        })

    majors = db.query(Nganh).all()
    major_name_map = {major.MaNganh: major.TenNganh for major in majors}

    aspirations_compact = []
    for aspiration in aspirations:
        aspirations_compact.append({
            "MaNganh": aspiration.MaNganh,
            "TenNganh": major_name_map.get(aspiration.MaNganh),
            "ThuTuNguyenVong": aspiration.ThuTuNguyenVong,
            "TrangThai": aspiration.TrangThai,
        })
    
    payload = {
        "profile": student,
        "contact": contact,
        "scores": scores_grouped,
        "aspirations": aspirations_compact,
        "enrollment": enrollment,
    }
    return jsonable_encoder(payload)