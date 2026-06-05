from datetime import date
from typing import Dict, List, Optional

from pydantic import BaseModel

from app.schemas.admission import HoSoNhapHocRead


class ThiSinhRead(BaseModel):
    CCCD: str
    HoTen: str
    GioiTinh: Optional[str] = None
    NgaySinh: Optional[date] = None
    NoiSinh: Optional[str] = None
    QueQuan: Optional[str] = None
    HoKhauThuongTru: Optional[str] = None
    DanToc: Optional[str] = None
    TonGiao: Optional[str] = None

    class Config:
        orm_mode = True


class LienHeRead(BaseModel):
    CCCD: str
    SoDienThoai: Optional[str] = None
    Email: Optional[str] = None

    class Config:
        orm_mode = True


class DiemThiRead(BaseModel):
    CCCD: str
    MaKyThi: str
    MaMon: str
    Diem: Optional[float] = None

    class Config:
        orm_mode = True


class DiemThiItem(BaseModel):
    MaMon: str
    Diem: Optional[float] = None


class ThiSinhChungChiRead(BaseModel):
    CCCD: str
    MaCC: str
    DiemGoc: Optional[float] = None
    DiemQuyDoi: Optional[float] = None

    class Config:
        orm_mode = True


class NguyenVongCompact(BaseModel):
    MaNganh: str
    TenNganh: Optional[str] = None
    ThuTuNguyenVong: int
    TrangThai: str


class StudentProfileResponse(BaseModel):
    profile: ThiSinhRead
    contact: Optional[LienHeRead] = None
    scores: Dict[str, List[DiemThiItem]]
    aspirations: List[NguyenVongCompact]
    enrollment: Optional[HoSoNhapHocRead] = None
