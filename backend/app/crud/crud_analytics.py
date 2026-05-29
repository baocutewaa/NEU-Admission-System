from sqlalchemy.orm import Session
from sqlalchemy import func, case, and_, desc
from app.models.student import ThiSinh
from app.models.admission import NguyenVong, HoSoNhapHoc, Nganh, NhomXetTuyen, PhuongThuc

class CRUDAnalytics:
    
    def get_admission_and_enrollment_rate(self, db: Session, nam_tuyen_sinh: int):
        """
        Calculate Admission Rate and Enrollment Rate for a given year.
        Admission Rate = Admitted / Total Applicants
        Enrollment Rate = Enrolled / Admitted
        """
        # Total distinct applicants
        total_applicants = db.query(func.count(func.distinct(NguyenVong.CCCD)))\
            .filter(NguyenVong.NamTuyenSinh == nam_tuyen_sinh).scalar() or 0
            
        # Admitted applicants
        admitted_applicants = db.query(func.count(func.distinct(NguyenVong.CCCD)))\
            .filter(
                NguyenVong.NamTuyenSinh == nam_tuyen_sinh,
                NguyenVong.TrangThai == u"Trúng tuyển"
            ).scalar() or 0
            
        # Enrolled applicants
        enrolled_applicants = db.query(func.count(func.distinct(HoSoNhapHoc.CCCD)))\
            .filter(HoSoNhapHoc.NamTuyenSinh == nam_tuyen_sinh).scalar() or 0
            
        admission_rate = (admitted_applicants / total_applicants * 100) if total_applicants > 0 else 0
        enrollment_rate = (enrolled_applicants / admitted_applicants * 100) if admitted_applicants > 0 else 0
        
        return {
            "nam_tuyen_sinh": nam_tuyen_sinh,
            "total_applicants": total_applicants,
            "admitted_applicants": admitted_applicants,
            "enrolled_applicants": enrolled_applicants,
            "admission_rate_percent": round(admission_rate, 2),
            "enrollment_rate_percent": round(enrollment_rate, 2)
        }

    def get_stats_by_major(self, db: Session, nam_tuyen_sinh: int):
        """
        Stats by Major (Ngành học)
        """
        # We can group by Nganh.MaNganh and TenNganh
        stats = db.query(
            Nganh.TenNganh,
            func.count(func.distinct(NguyenVong.CCCD)).label('total_applicants'),
            func.count(func.distinct(case((NguyenVong.TrangThai == u"Trúng tuyển", NguyenVong.CCCD), else_=None))).label('admitted_applicants'),
        ).join(NguyenVong, Nganh.MaNganh == NguyenVong.MaNganh)\
         .filter(NguyenVong.NamTuyenSinh == nam_tuyen_sinh)\
         .group_by(Nganh.TenNganh).all()
         
        # For enrolled, we query HoSoNhapHoc
        enrolled_stats = db.query(
            Nganh.TenNganh,
            func.count(func.distinct(HoSoNhapHoc.CCCD)).label('enrolled_applicants')
        ).join(HoSoNhapHoc, Nganh.MaNganh == HoSoNhapHoc.MaNganh)\
         .filter(HoSoNhapHoc.NamTuyenSinh == nam_tuyen_sinh)\
         .group_by(Nganh.TenNganh).all()
         
        enrolled_dict = {row.TenNganh: row.enrolled_applicants for row in enrolled_stats}
        
        result = []
        for row in stats:
            enrolled = enrolled_dict.get(row.TenNganh, 0)
            admission_rate = (row.admitted_applicants / row.total_applicants * 100) if row.total_applicants > 0 else 0
            enrollment_rate = (enrolled / row.admitted_applicants * 100) if row.admitted_applicants > 0 else 0
            result.append({
                "major_name": row.TenNganh,
                "total_applicants": row.total_applicants,
                "admitted_applicants": row.admitted_applicants,
                "enrolled_applicants": enrolled,
                "admission_rate_percent": round(admission_rate, 2),
                "enrollment_rate_percent": round(enrollment_rate, 2)
            })
            
        return result

    def get_stats_by_admission_method(self, db: Session, nam_tuyen_sinh: int):
        """
        Stats by Admission Method (Phương thức xét tuyển)
        """
        stats = db.query(
            PhuongThuc.TenPhuongThuc,
            func.count(func.distinct(NguyenVong.CCCD)).label('total_applicants'),
            func.count(func.distinct(case((NguyenVong.TrangThai == u"Trúng tuyển", NguyenVong.CCCD), else_=None))).label('admitted_applicants')
        ).join(NhomXetTuyen, NhomXetTuyen.MaPT == PhuongThuc.MaPT)\
         .join(NguyenVong, NguyenVong.MaNhom == NhomXetTuyen.MaNhom)\
         .filter(NguyenVong.NamTuyenSinh == nam_tuyen_sinh)\
         .group_by(PhuongThuc.TenPhuongThuc).all()
         
        enrolled_stats = db.query(
            PhuongThuc.TenPhuongThuc,
            func.count(func.distinct(HoSoNhapHoc.CCCD)).label('enrolled_applicants')
        ).join(NhomXetTuyen, NhomXetTuyen.MaPT == PhuongThuc.MaPT)\
         .join(HoSoNhapHoc, HoSoNhapHoc.MaNhom == NhomXetTuyen.MaNhom)\
         .filter(HoSoNhapHoc.NamTuyenSinh == nam_tuyen_sinh)\
         .group_by(PhuongThuc.TenPhuongThuc).all()
         
        enrolled_dict = {row.TenPhuongThuc: row.enrolled_applicants for row in enrolled_stats}
        
        result = []
        for row in stats:
            enrolled = enrolled_dict.get(row.TenPhuongThuc, 0)
            result.append({
                "method_name": row.TenPhuongThuc,
                "total_applicants": row.total_applicants,
                "admitted_applicants": row.admitted_applicants,
                "enrolled_applicants": enrolled
            })
            
        return result

    def get_stats_by_region(self, db: Session, nam_tuyen_sinh: int):
        """
        Stats by Region (Vùng địa lý / Tỉnh thành)
        Uses ThiSinh.HoKhauThuongTru as proxy for region
        """
        stats = db.query(
            ThiSinh.HoKhauThuongTru,
            func.count(func.distinct(NguyenVong.CCCD)).label('total_applicants'),
            func.count(func.distinct(case((NguyenVong.TrangThai == u"Trúng tuyển", NguyenVong.CCCD), else_=None))).label('admitted_applicants')
        ).join(NguyenVong, NguyenVong.CCCD == ThiSinh.CCCD)\
         .filter(NguyenVong.NamTuyenSinh == nam_tuyen_sinh)\
         .group_by(ThiSinh.HoKhauThuongTru).all()
         
        enrolled_stats = db.query(
            ThiSinh.HoKhauThuongTru,
            func.count(func.distinct(HoSoNhapHoc.CCCD)).label('enrolled_applicants')
        ).join(HoSoNhapHoc, HoSoNhapHoc.CCCD == ThiSinh.CCCD)\
         .filter(HoSoNhapHoc.NamTuyenSinh == nam_tuyen_sinh)\
         .group_by(ThiSinh.HoKhauThuongTru).all()
         
        enrolled_dict = {row.HoKhauThuongTru: row.enrolled_applicants for row in enrolled_stats}
        
        result = []
        for row in stats:
            enrolled = enrolled_dict.get(row.HoKhauThuongTru, 0)
            result.append({
                "region": row.HoKhauThuongTru or "Không rõ",
                "total_applicants": row.total_applicants,
                "admitted_applicants": row.admitted_applicants,
                "enrolled_applicants": enrolled
            })
            
        return result

    def get_motivation_analysis(self, db: Session, nam_tuyen_sinh: int):
        """
        Phân loại động lực (Motivation): NV1 - NV3 (Động lực cao) vs NV sau (Dự phòng)
        """
        high_motivation_cond = NguyenVong.ThuTuNguyenVong <= 3
        low_motivation_cond = NguyenVong.ThuTuNguyenVong > 3
        
        stats = db.query(
            func.count(func.distinct(case((high_motivation_cond, NguyenVong.CCCD), else_=None))).label('high_motivation_applicants'),
            func.count(func.distinct(case((low_motivation_cond, NguyenVong.CCCD), else_=None))).label('low_motivation_applicants'),
            func.count(func.distinct(case((and_(high_motivation_cond, NguyenVong.TrangThai == u"Trúng tuyển"), NguyenVong.CCCD), else_=None))).label('high_motivation_admitted'),
            func.count(func.distinct(case((and_(low_motivation_cond, NguyenVong.TrangThai == u"Trúng tuyển"), NguyenVong.CCCD), else_=None))).label('low_motivation_admitted')
        ).filter(NguyenVong.NamTuyenSinh == nam_tuyen_sinh).first()
        
        return {
            "high_motivation": {
                "applicants": stats.high_motivation_applicants,
                "admitted": stats.high_motivation_admitted
            },
            "low_motivation": {
                "applicants": stats.low_motivation_applicants,
                "admitted": stats.low_motivation_admitted
            }
        }

    def get_major_clustering(self, db: Session, nam_tuyen_sinh: int, limit: int = 10):
        """
        Phân nhóm ngành (Major Clustering): Tìm các cặp ngành học thường được đăng ký cùng nhau
        """
        nv1 = db.query(NguyenVong.CCCD, NguyenVong.MaNganh).filter(NguyenVong.NamTuyenSinh == nam_tuyen_sinh).subquery('nv1')
        nv2 = db.query(NguyenVong.CCCD, NguyenVong.MaNganh).filter(NguyenVong.NamTuyenSinh == nam_tuyen_sinh).subquery('nv2')
        
        # Self-join on CCCD but different MaNganh to find pairs
        clustering = db.query(
            nv1.c.MaNganh.label('nganh_1'),
            nv2.c.MaNganh.label('nganh_2'),
            func.count(func.distinct(nv1.c.CCCD)).label('pair_count')
        ).join(nv2, and_(nv1.c.CCCD == nv2.c.CCCD, nv1.c.MaNganh < nv2.c.MaNganh))\
         .group_by(nv1.c.MaNganh, nv2.c.MaNganh)\
         .order_by(desc('pair_count'))\
         .limit(limit).all()
         
        # Map MaNganh to TenNganh
        nganh_dict = {n.MaNganh: n.TenNganh for n in db.query(Nganh).all()}
        
        result = []
        for row in clustering:
            result.append({
                "nganh_1": nganh_dict.get(row.nganh_1, row.nganh_1),
                "nganh_2": nganh_dict.get(row.nganh_2, row.nganh_2),
                "frequency": row.pair_count
            })
            
        return result
        
    def get_multivariate_preference_analysis(self, db: Session, nam_tuyen_sinh: int):
        """
        Kết hợp Đa biến (Preference Analysis): 
        Đánh giá mức độ yêu thích thông qua sự kết hợp của: Thứ tự NV + Hành vi nhập học.
        (Chênh lệch điểm - Score gap bị bỏ qua do chưa có dữ liệu điểm chuẩn)
        """
        # Define high/low motivation
        is_high_nv = NguyenVong.ThuTuNguyenVong <= 3
        is_enrolled = case((HoSoNhapHoc.CCCD != None, True), else_=False)
        
        # We join NguyenVong with HoSoNhapHoc
        stats = db.query(
            case((is_high_nv, "High Motivation (NV1-3)"), else_="Low Motivation (NV>3)").label("motivation_group"),
            is_enrolled.label("enrolled"),
            func.count(func.distinct(NguyenVong.CCCD)).label("count")
        ).outerjoin(HoSoNhapHoc, and_(
            HoSoNhapHoc.CCCD == NguyenVong.CCCD,
            HoSoNhapHoc.MaNganh == NguyenVong.MaNganh,
            HoSoNhapHoc.NamTuyenSinh == NguyenVong.NamTuyenSinh
        )).filter(
            NguyenVong.NamTuyenSinh == nam_tuyen_sinh,
            NguyenVong.TrangThai == u"Trúng tuyển"
        ).group_by(
            "motivation_group", "enrolled"
        ).all()
        
        return [
            {
                "motivation_group": row.motivation_group,
                "enrolled": row.enrolled,
                "applicant_count": row.count
            } for row in stats
        ]

analytics_crud = CRUDAnalytics()
