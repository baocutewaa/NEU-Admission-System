from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db
from app.crud.crud_analytics import analytics_crud
from app.schemas.analytics import (
    AdmissionOverview,
    StatsByRegion,
    StatsByMajor,
    StatsByMethod,
    MotivationAnalysis,
    MajorClustering,
    PreferenceMultivariate,
)

router = APIRouter()

@router.get("/overview", response_model=AdmissionOverview)
def get_admission_overview(
    nam_tuyen_sinh: int = Query(2024, description="Năm tuyển sinh cần thống kê"),
    db: Session = Depends(get_db)
):
    """
    Lấy thông tin tổng quan (Efficiency & Trend Analytics)
    - Admission Rate (Tỉ lệ đỗ)
    - Enrollment Rate/Yield (Tỉ lệ nhập học)
    """
    return analytics_crud.get_admission_and_enrollment_rate(db, nam_tuyen_sinh=nam_tuyen_sinh)

@router.get("/regions", response_model=List[StatsByRegion])
def get_stats_by_region(
    nam_tuyen_sinh: int = Query(2024, description="Năm tuyển sinh cần thống kê"),
    db: Session = Depends(get_db)
):
    """
    Thống kê theo Vùng địa lý / Tỉnh thành
    """
    return analytics_crud.get_stats_by_region(db, nam_tuyen_sinh=nam_tuyen_sinh)

@router.get("/majors", response_model=List[StatsByMajor])
def get_stats_by_major(
    nam_tuyen_sinh: int = Query(2024, description="Năm tuyển sinh cần thống kê"),
    db: Session = Depends(get_db)
):
    """
    Thống kê theo ngành học (Số lượng đăng ký, tỉ lệ đỗ, tỉ lệ nhập học)
    """
    return analytics_crud.get_stats_by_major(db, nam_tuyen_sinh=nam_tuyen_sinh)

@router.get("/methods", response_model=List[StatsByMethod])
def get_stats_by_method(
    nam_tuyen_sinh: int = Query(2024, description="Năm tuyển sinh cần thống kê"),
    db: Session = Depends(get_db)
):
    """
    Thống kê theo phương thức xét tuyển
    """
    return analytics_crud.get_stats_by_admission_method(db, nam_tuyen_sinh=nam_tuyen_sinh)

@router.get("/motivation", response_model=MotivationAnalysis)
def get_motivation_analysis(
    nam_tuyen_sinh: int = Query(2024, description="Năm tuyển sinh cần thống kê"),
    db: Session = Depends(get_db)
):
    """
    Phân loại động lực (Preference & Behavioral Analysis):
    NV1-3 vs NV>3
    """
    return analytics_crud.get_motivation_analysis(db, nam_tuyen_sinh=nam_tuyen_sinh)

@router.get("/clustering", response_model=List[MajorClustering])
def get_major_clustering(
    nam_tuyen_sinh: int = Query(2024, description="Năm tuyển sinh cần thống kê"),
    limit: int = Query(10, description="Số lượng cặp ngành học"),
    db: Session = Depends(get_db)
):
    """
    Phân nhóm ngành (Major Clustering): Các cặp ngành thường được chọn cùng nhau
    """
    return analytics_crud.get_major_clustering(db, nam_tuyen_sinh=nam_tuyen_sinh, limit=limit)

@router.get("/preference-multivariate", response_model=List[PreferenceMultivariate])
def get_preference_multivariate(
    nam_tuyen_sinh: int = Query(2024, description="Năm tuyển sinh cần thống kê"),
    db: Session = Depends(get_db)
):
    """
    Kết hợp Đa biến (Preference Analysis):
    Thứ tự NV + Hành vi nhập học.
    """
    return analytics_crud.get_multivariate_preference_analysis(db, nam_tuyen_sinh=nam_tuyen_sinh)
