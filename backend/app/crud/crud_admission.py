from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.admission import Nganh, NguyenVong, HoSoNhapHoc, NhomXetTuyen, PhuongThuc, KyThi, MonThi, ChiTieuTheoNam

class CRUDAdmission:
    def get_majors(self, db: Session, skip: int = 0, limit: int = 100) -> List[Nganh]:
        return db.query(Nganh).offset(skip).limit(limit).all()

    def get_major_by_id(self, db: Session, ma_nganh: str) -> Optional[Nganh]:
        return db.query(Nganh).filter(Nganh.MaNganh == ma_nganh).first()

    def get_aspirations_by_student(self, db: Session, cccd: str, nam_tuyen_sinh: int) -> List[NguyenVong]:
        return db.query(NguyenVong).filter(
            NguyenVong.CCCD == cccd,
            NguyenVong.NamTuyenSinh == nam_tuyen_sinh
        ).order_by(NguyenVong.ThuTuNguyenVong).all()

    def get_admission_methods(self, db: Session) -> List[PhuongThuc]:
        return db.query(PhuongThuc).all()

    def get_enrollment_profile(self, db: Session, cccd: str) -> Optional[HoSoNhapHoc]:
        return db.query(HoSoNhapHoc).filter(HoSoNhapHoc.CCCD == cccd).first()

    def get_quotas_by_year(self, db: Session, nam_tuyen_sinh: int) -> List[ChiTieuTheoNam]:
        return db.query(ChiTieuTheoNam).filter(ChiTieuTheoNam.NamTuyenSinh == nam_tuyen_sinh).all()

admission_crud = CRUDAdmission()
