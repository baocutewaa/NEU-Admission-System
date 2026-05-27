from sqlalchemy import Column, String, Integer, Float, Date, ForeignKey, CHAR
from sqlalchemy.orm import relationship
from app.models.base import Base

class ThiSinh(Base):
    __tablename__ = "thisinh"
    
    CCCD = Column(CHAR(12), primary_key=True, index=True)
    HoTen = Column(String(100), nullable=False)
    GioiTinh = Column(String(10), nullable=True)
    NgaySinh = Column(Date, nullable=True)
    NoiSinh = Column(String(100), nullable=True)
    QueQuan = Column(String(100), nullable=True)
    HoKhauThuongTru = Column(String(255), nullable=True)
    DanToc = Column(String(50), nullable=True)
    TonGiao = Column(String(50), nullable=True)

    lien_he = relationship("LienHe", back_populates="thi_sinh", uselist=False, cascade="all, delete-orphan")
    diem_thi = relationship("DiemThi", back_populates="thi_sinh", cascade="all, delete-orphan")
    chung_chi_ts = relationship("ThiSinhChungChi", back_populates="thi_sinh", cascade="all, delete-orphan")
    nguyen_vong = relationship("NguyenVong", back_populates="thi_sinh", cascade="all, delete-orphan")
    ho_so_nhap_hoc = relationship("HoSoNhapHoc", back_populates="thi_sinh", cascade="all, delete-orphan")

class LienHe(Base):
    __tablename__ = "lien_he"
    
    CCCD = Column(CHAR(12), ForeignKey("thisinh.CCCD", ondelete="CASCADE"), primary_key=True)
    SoDienThoai = Column(String(15), nullable=True)
    Email = Column(String(100), nullable=True)

    thi_sinh = relationship("ThiSinh", back_populates="lien_he")

class ChungChi(Base):
    __tablename__ = "chung_chi"
    
    MaCC = Column(String(20), primary_key=True)
    TenChungChi = Column(String(150), nullable=True)
    ThangDiem = Column(Integer, nullable=True)

    thi_sinh_cc = relationship("ThiSinhChungChi", back_populates="chung_chi")

class ThiSinhChungChi(Base):
    __tablename__ = "thisinh_chung_chi"
    
    CCCD = Column(CHAR(12), ForeignKey("thisinh.CCCD"), primary_key=True)
    MaCC = Column(String(20), ForeignKey("chung_chi.MaCC"), primary_key=True)
    DiemGoc = Column(Float, nullable=True)
    DiemQuyDoi = Column(Float, nullable=True)

    thi_sinh = relationship("ThiSinh", back_populates="chung_chi_ts")
    chung_chi = relationship("ChungChi", back_populates="thi_sinh_cc")

class DiemThi(Base):
    __tablename__ = "diem_thi"
    
    CCCD = Column(CHAR(12), ForeignKey("thisinh.CCCD"), primary_key=True)
    MaKyThi = Column(String(20), ForeignKey("ky_thi.MaKyThi"), primary_key=True)
    MaMon = Column(String(20), ForeignKey("mon_thi.MaMon"), primary_key=True)
    Diem = Column(Float, nullable=True)

    thi_sinh = relationship("ThiSinh", back_populates="diem_thi")
    ky_thi = relationship("KyThi", back_populates="diem_thi")
    mon_thi = relationship("MonThi", back_populates="diem_thi")
