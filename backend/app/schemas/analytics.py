from datetime import date
from typing import Optional, List

from pydantic import BaseModel


class AdmissionOverview(BaseModel):
    nam_tuyen_sinh: int
    total_applicants: int
    admitted_applicants: int
    enrolled_applicants: int
    admission_rate_percent: float
    enrollment_rate_percent: float


class StatsByRegion(BaseModel):
    region: str
    total_applicants: int
    admitted_applicants: int
    enrolled_applicants: int


class StatsByMajor(BaseModel):
    major_name: str
    total_applicants: int
    admitted_applicants: int
    enrolled_applicants: int
    admission_rate_percent: float
    enrollment_rate_percent: float


class StatsByMethod(BaseModel):
    method_name: str
    total_applicants: int
    admitted_applicants: int
    enrolled_applicants: int


class MotivationCounts(BaseModel):
    applicants: int
    admitted: int


class MotivationAnalysis(BaseModel):
    high_motivation: MotivationCounts
    low_motivation: MotivationCounts


class MajorClustering(BaseModel):
    nganh_1: str
    nganh_2: str
    frequency: int


class PreferenceMultivariate(BaseModel):
    motivation_group: str
    enrolled: bool
    applicant_count: int


class VwPhanTichTuyenSinhRead(BaseModel):
    CCCD: str
    HoTen: Optional[str] = None
    GioiTinh: Optional[str] = None
    NgaySinh: Optional[date] = None
    QueQuan: Optional[str] = None
    TenNganh: Optional[str] = None
    KhoiXetTuyen: Optional[str] = None
    TongDiemTHPT: Optional[float] = None
    HSA: Optional[float] = None
    TSA: Optional[float] = None
    IELTS: Optional[float] = None
    SAT: Optional[float] = None
    DXT_THPT: Optional[float] = None
    DXT_HSA: Optional[float] = None
    DXT_TSA: Optional[float] = None
    DXT_SAT: Optional[float] = None
    DXT_IELTS_DGNL: Optional[float] = None
    DXT_IELTS_THPT: Optional[float] = None
    DiemXetTuyen: Optional[float] = None

    class Config:
        orm_mode = True


class AdvancedGenderStats(BaseModel):
    major_name: str
    nam_tuyen_sinh: int
    phuong_thuc: Optional[str] = None
    male_applied: int = 0
    female_applied: int = 0
    other_applied: int = 0
    male_admitted: int = 0
    female_admitted: int = 0
    other_admitted: int = 0
    male_enrolled: int = 0
    female_enrolled: int = 0
    other_enrolled: int = 0


class GeoEnrollmentStats(BaseModel):
    province: str
    nam_tuyen_sinh: int
    phuong_thuc: Optional[str] = None
    major_name: Optional[str] = None
    total_applicants: int = 0
    admitted_applicants: int = 0
    enrolled_applicants: int = 0
    yield_rate: float = 0.0


class ScoreBracket(BaseModel):
    bracket: str
    count: int


class ScoreAnalyticsStats(BaseModel):
    subject_name: str
    major_name: Optional[str] = None
    phuong_thuc: Optional[str] = None
    avg_score: Optional[float] = None
    median_score: Optional[float] = None
    min_score: Optional[float] = None
    max_score: Optional[float] = None
    brackets: List[ScoreBracket]
