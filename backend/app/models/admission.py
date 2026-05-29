from sqlalchemy import Column, String, Integer, Float, Date, ForeignKey, CHAR
from sqlalchemy.orm import relationship
from app.models.base import Base

class KyThi(Base):
    __tablename__ = "ky_thi"
    
    MaKyThi = Column(String(20), primary_key=True)
    TenKyThi = Column(String(150), nullable=True)

    diem_thi = relationship("DiemThi", back_populates="ky_thi")

class MonThi(Base):
    __tablename__ = "mon_thi"
    
    MaMon = Column(String(20), primary_key=True)
    TenMon = Column(String(100), nullable=True)
    NhomMon = Column(String(50), nullable=True)

    diem_thi = relationship("DiemThi", back_populates="mon_thi")

class PhuongThuc(Base):
    __tablename__ = "phuong_thuc"
    
    MaPT = Column(String(20), primary_key=True)
    TenPhuongThuc = Column(String(150), nullable=True)

    nhom_xet_tuyen = relationship("NhomXetTuyen", back_populates="phuong_thuc")

class NhomXetTuyen(Base):
    __tablename__ = "nhom_xet_tuyen"
    
    MaNhom = Column(String(20), primary_key=True)
    MaPT = Column(String(20), ForeignKey("phuong_thuc.MaPT"), nullable=False)
    TenNhom = Column(String(150), nullable=True)
    MoTa = Column(String(255), nullable=True)

    phuong_thuc = relationship("PhuongThuc", back_populates="nhom_xet_tuyen")
    nguyen_vong = relationship("NguyenVong", back_populates="nhom_xet_tuyen")
    ho_so_nhap_hoc = relationship("HoSoNhapHoc", back_populates="nhom_xet_tuyen")

class Nganh(Base):
    __tablename__ = "nganh"
    
    MaNganh = Column(String(20), primary_key=True)
    TenNganh = Column(String(150), nullable=True)
    ChiTieu = Column(Integer, nullable=True)

    chi_tieu_nam = relationship("ChiTieuTheoNam", back_populates="nganh")
    nguyen_vong = relationship("NguyenVong", back_populates="nganh")
    ho_so_nhap_hoc = relationship("HoSoNhapHoc", back_populates="nganh")

class HoSoNhapHoc(Base):
    __tablename__ = "ho_so_nhap_hoc"
    
    CCCD = Column(CHAR(12), ForeignKey("thisinh.CCCD"), primary_key=True)
    MaNganh = Column(String(20), ForeignKey("nganh.MaNganh"), primary_key=True)
    MaNhom = Column(String(20), ForeignKey("nhom_xet_tuyen.MaNhom"), nullable=False)
    NamTuyenSinh = Column(Integer, nullable=True)
    NgayXacNhan = Column(Date, nullable=True)

    thi_sinh = relationship("ThiSinh", back_populates="ho_so_nhap_hoc")
    nganh = relationship("Nganh", back_populates="ho_so_nhap_hoc")
    nhom_xet_tuyen = relationship("NhomXetTuyen", back_populates="ho_so_nhap_hoc")

class VungDiaLy(Base):
    __tablename__ = "vung_dia_ly"
    
    MaTinh = Column(String(10), primary_key=True)
    TenTinh = Column(String(100), nullable=False)
    DiaBanVung = Column(Integer, nullable=False) # TinyInt corresponds to Integer in most setups

class ChiTieuTheoNam(Base):
    __tablename__ = "chi_tieu_theo_nam"
    
    MaNganh = Column(String(20), ForeignKey("nganh.MaNganh"), primary_key=True)
    NamTuyenSinh = Column(Integer, primary_key=True)
    ChiTieuKeHoach = Column(Integer, nullable=True)
    ChiTieuDieuChinh = Column(Integer, nullable=True)
    GhiChu = Column(String(255), nullable=True)

    nganh = relationship("Nganh", back_populates="chi_tieu_nam")

class NguyenVong(Base):
    __tablename__ = "nguyen_vong"
    
    MaNguyenVong = Column(Integer, primary_key=True, autoincrement=True)
    CCCD = Column(CHAR(12), ForeignKey("thisinh.CCCD"), nullable=False)
    MaNganh = Column(String(20), ForeignKey("nganh.MaNganh"), nullable=False)
    MaNhom = Column(String(20), ForeignKey("nhom_xet_tuyen.MaNhom"), nullable=False)
    NamTuyenSinh = Column(Integer, nullable=False)
    ThuTuNguyenVong = Column(Integer, nullable=False)
    TrangThai = Column(String(30), nullable=False, default=u"Chưa xác định")

    thi_sinh = relationship("ThiSinh", back_populates="nguyen_vong")
    nganh = relationship("Nganh", back_populates="nguyen_vong")
    nhom_xet_tuyen = relationship("NhomXetTuyen", back_populates="nguyen_vong")
