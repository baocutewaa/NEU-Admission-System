from app.models.base import Base
from app.models.student import ThiSinh, LienHe, DiemThi, ChungChi, ThiSinhChungChi
from app.models.admission import (
    KyThi, MonThi, PhuongThuc, NhomXetTuyen, Nganh,
    HoSoNhapHoc, VungDiaLy, ChiTieuTheoNam, NguyenVong
)

# Export all models so that Alembic/SQLAlchemy can easily find them in one place
__all__ = [
    "Base",
    "ThiSinh", "LienHe", "DiemThi", "ChungChi", "ThiSinhChungChi",
    "KyThi", "MonThi", "PhuongThuc", "NhomXetTuyen", "Nganh",
    "HoSoNhapHoc", "VungDiaLy", "ChiTieuTheoNam", "NguyenVong"
]
