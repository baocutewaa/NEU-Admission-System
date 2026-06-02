from datetime import date
from typing import Optional

from pydantic import BaseModel


class KyThiRead(BaseModel):
    MaKyThi: str
    TenKyThi: Optional[str] = None

    class Config:
        orm_mode = True


class MonThiRead(BaseModel):
    MaMon: str
    TenMon: Optional[str] = None
    NhomMon: Optional[str] = None

    class Config:
        orm_mode = True


class PhuongThucRead(BaseModel):
    MaPT: str
    TenPhuongThuc: Optional[str] = None

    class Config:
        orm_mode = True


class NhomXetTuyenRead(BaseModel):
    MaNhom: str
    MaPT: str
    TenNhom: Optional[str] = None
    MoTa: Optional[str] = None

    class Config:
        orm_mode = True


class NganhRead(BaseModel):
    MaNganh: str
    TenNganh: Optional[str] = None
    ChiTieu: Optional[int] = None

    class Config:
        orm_mode = True


class HoSoNhapHocRead(BaseModel):
    CCCD: str
    MaNganh: str
    MaNhom: str
    NamTuyenSinh: Optional[int] = None
    NgayXacNhan: Optional[date] = None

    class Config:
        orm_mode = True


class VungDiaLyRead(BaseModel):
    MaTinh: str
    TenTinh: str
    DiaBanVung: int

    class Config:
        orm_mode = True


class ChiTieuTheoNamRead(BaseModel):
    MaNganh: str
    NamTuyenSinh: int
    ChiTieuKeHoach: Optional[int] = None
    ChiTieuDieuChinh: Optional[int] = None
    GhiChu: Optional[str] = None

    class Config:
        orm_mode = True


class NguyenVongRead(BaseModel):
    MaNguyenVong: int
    CCCD: str
    MaNganh: str
    MaNhom: str
    NamTuyenSinh: int
    ThuTuNguyenVong: int
    TrangThai: str

    class Config:
        orm_mode = True
