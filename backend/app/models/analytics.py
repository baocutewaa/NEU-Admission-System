from sqlalchemy import Column, String, Float, Date, CHAR
from app.models.base import Base


class VwPhanTichTuyenSinh(Base):
    __tablename__ = "vw_phan_tich_tuyensinh"

    CCCD = Column(CHAR(12), primary_key=True)
    TenNganh = Column(String(150), primary_key=True)
    KhoiXetTuyen = Column(String(20), primary_key=True)

    HoTen = Column(String(100), nullable=True)
    GioiTinh = Column(String(10), nullable=True)
    NgaySinh = Column(Date, nullable=True)
    QueQuan = Column(String(100), nullable=True)

    TongDiemTHPT = Column(Float, nullable=True)
    HSA = Column(Float, nullable=True)
    TSA = Column(Float, nullable=True)
    IELTS = Column(Float, nullable=True)
    SAT = Column(Float, nullable=True)

    DXT_THPT = Column(Float, nullable=True)
    DXT_HSA = Column(Float, nullable=True)
    DXT_TSA = Column(Float, nullable=True)
    DXT_SAT = Column(Float, nullable=True)
    DXT_IELTS_DGNL = Column(Float, nullable=True)
    DXT_IELTS_THPT = Column(Float, nullable=True)

    DiemXetTuyen = Column(Float, nullable=True)
