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
                NguyenVong.TrangThai.ilike(u"Trung tuyen")
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
            func.count(func.distinct(case((NguyenVong.TrangThai.ilike(u"Trung tuyen"), NguyenVong.CCCD), else_=None))).label('admitted_applicants'),
        ).join(NguyenVong, Nganh.MaNganh == NguyenVong.MaNganh)\
         .filter(NguyenVong.NamTuyenSinh == nam_tuyen_sinh)\
         .group_by(Nganh.TenNganh).all()
         
        # For enrolled, we query HoSoNhapHoc
        enrolled_stats = db.query(
        Nganh.TenNganh,
        func.count(func.distinct(HoSoNhapHoc.CCCD)).label('enrolled_applicants')
    ).join(HoSoNhapHoc, and_(
        Nganh.MaNganh == HoSoNhapHoc.MaNganh, 
        HoSoNhapHoc.NamTuyenSinh == nam_tuyen_sinh # Phải lọc kèm năm
    ))\
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
            func.count(func.distinct(case((NguyenVong.TrangThai.ilike(u"Trung tuyen"), NguyenVong.CCCD), else_=None))).label('admitted_applicants')
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
            func.count(func.distinct(case((NguyenVong.TrangThai.ilike(u"Trung tuyen"), NguyenVong.CCCD), else_=None))).label('admitted_applicants')
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
            func.count(func.distinct(case((and_(high_motivation_cond, NguyenVong.TrangThai.ilike(u"Trung tuyen")), NguyenVong.CCCD), else_=None))).label('high_motivation_admitted'),
            func.count(func.distinct(case((and_(low_motivation_cond, NguyenVong.TrangThai.ilike(u"Trung tuyen")), NguyenVong.CCCD), else_=None))).label('low_motivation_admitted')
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
        Sửa triệt để lỗi SQL Server bằng giải pháp Subquery nhằm loại bỏ tham số ẩn (?) trong GROUP BY.
        """
        from sqlalchemy import and_, case, func

        is_high_nv = NguyenVong.ThuTuNguyenVong <= 3
        motivation_expr = case((is_high_nv, "High Motivation (NV1-3)"), else_="Low Motivation (NV>3)")
        enrolled_expr = case((HoSoNhapHoc.CCCD != None, True), else_=False)
        
        # Bước 1: Đưa toàn bộ logic biểu thức phức tạp vào Subquery để định hình cột rõ ràng
        subquery = db.query(
            NguyenVong.CCCD.label("applicant_cccd"),
            motivation_expr.label("motivation_group"),
            enrolled_expr.label("enrolled")
        ).outerjoin(HoSoNhapHoc, and_(
            HoSoNhapHoc.CCCD == NguyenVong.CCCD,
            HoSoNhapHoc.MaNganh == NguyenVong.MaNganh,
            HoSoNhapHoc.NamTuyenSinh == NguyenVong.NamTuyenSinh
        )).filter(
            NguyenVong.NamTuyenSinh == nam_tuyen_sinh,
            NguyenVong.TrangThai.ilike(u"Trung tuyen")
        ).subquery()
        
        # Bước 2: Truy vấn từ subquery, lúc này group_by chỉ là các cột thông thường nên SQL Server chạy mượt mà
        stats = db.query(
            subquery.c.motivation_group,
            subquery.c.enrolled,
            func.count(func.distinct(subquery.c.applicant_cccd)).label("count")
        ).group_by(
            subquery.c.motivation_group,
            subquery.c.enrolled
        ).all()
        
        return [
            {
                "motivation_group": row.motivation_group,
                "enrolled": row.enrolled,
                "applicant_count": row.count
            } for row in stats
        ]

    def get_advanced_gender_distribution(self, db: Session, nam_tuyen_sinh: int, phuong_thuc: str = None):
        """
        Advanced Gender Distribution with optional method filtering.
        """
        query = db.query(
            Nganh.TenNganh,
            ThiSinh.GioiTinh,
            func.count(func.distinct(NguyenVong.CCCD)).label('applied'),
            func.count(func.distinct(case((NguyenVong.TrangThai.ilike(u"Trung tuyen"), NguyenVong.CCCD), else_=None))).label('admitted'),
        ).join(NguyenVong, Nganh.MaNganh == NguyenVong.MaNganh)\
         .join(ThiSinh, ThiSinh.CCCD == NguyenVong.CCCD)\
         .join(NhomXetTuyen, NhomXetTuyen.MaNhom == NguyenVong.MaNhom)\
         .join(PhuongThuc, PhuongThuc.MaPT == NhomXetTuyen.MaPT)\
         .filter(NguyenVong.NamTuyenSinh == nam_tuyen_sinh)
         
        if phuong_thuc:
            query = query.filter(PhuongThuc.TenPhuongThuc == phuong_thuc)
            
        stats = query.group_by(Nganh.TenNganh, ThiSinh.GioiTinh).all()
        
        enrolled_query = db.query(
            Nganh.TenNganh,
            ThiSinh.GioiTinh,
            func.count(func.distinct(HoSoNhapHoc.CCCD)).label('enrolled')
        ).join(HoSoNhapHoc, Nganh.MaNganh == HoSoNhapHoc.MaNganh)\
         .join(ThiSinh, ThiSinh.CCCD == HoSoNhapHoc.CCCD)\
         .join(NhomXetTuyen, NhomXetTuyen.MaNhom == HoSoNhapHoc.MaNhom)\
         .join(PhuongThuc, PhuongThuc.MaPT == NhomXetTuyen.MaPT)\
         .filter(HoSoNhapHoc.NamTuyenSinh == nam_tuyen_sinh)
         
        if phuong_thuc:
            enrolled_query = enrolled_query.filter(PhuongThuc.TenPhuongThuc == phuong_thuc)
            
        enrolled_stats = enrolled_query.group_by(Nganh.TenNganh, ThiSinh.GioiTinh).all()
        
        results_dict = {}
        for row in stats:
            major = row.TenNganh
            gender = row.GioiTinh or "Khác"
            if gender not in ["Nam", "Nữ"]: gender = "Khác"
            
            if major not in results_dict:
                results_dict[major] = {
                    "major_name": major,
                    "nam_tuyen_sinh": nam_tuyen_sinh,
                    "phuong_thuc": phuong_thuc,
                    "male_applied": 0, "female_applied": 0, "other_applied": 0,
                    "male_admitted": 0, "female_admitted": 0, "other_admitted": 0,
                    "male_enrolled": 0, "female_enrolled": 0, "other_enrolled": 0,
                }
            
            if gender == "Nam":
                results_dict[major]["male_applied"] = row.applied
                results_dict[major]["male_admitted"] = row.admitted
            elif gender == "Nữ":
                results_dict[major]["female_applied"] = row.applied
                results_dict[major]["female_admitted"] = row.admitted
            else:
                results_dict[major]["other_applied"] = row.applied
                results_dict[major]["other_admitted"] = row.admitted
                
        for row in enrolled_stats:
            major = row.TenNganh
            gender = row.GioiTinh or "Khác"
            if gender not in ["Nam", "Nữ"]: gender = "Khác"
            if major in results_dict:
                if gender == "Nam": results_dict[major]["male_enrolled"] = row.enrolled
                elif gender == "Nữ": results_dict[major]["female_enrolled"] = row.enrolled
                else: results_dict[major]["other_enrolled"] = row.enrolled

        return list(results_dict.values())

    def get_geographic_enrollment_stats(self, db: Session, nam_tuyen_sinh: int, phuong_thuc: str = None, major_name: str = None):
        """
        Geographic Heatmap data.
        """
        query = db.query(
            ThiSinh.HoKhauThuongTru.label("province"),
            func.count(func.distinct(NguyenVong.CCCD)).label('applied'),
            func.count(func.distinct(case((NguyenVong.TrangThai.ilike(u"Trung tuyen"), NguyenVong.CCCD), else_=None))).label('admitted'),
        ).join(NguyenVong, ThiSinh.CCCD == NguyenVong.CCCD)\
         .join(Nganh, Nganh.MaNganh == NguyenVong.MaNganh)\
         .join(NhomXetTuyen, NhomXetTuyen.MaNhom == NguyenVong.MaNhom)\
         .join(PhuongThuc, PhuongThuc.MaPT == NhomXetTuyen.MaPT)\
         .filter(NguyenVong.NamTuyenSinh == nam_tuyen_sinh)
         
        if phuong_thuc:
            query = query.filter(PhuongThuc.TenPhuongThuc == phuong_thuc)
        if major_name:
            query = query.filter(Nganh.TenNganh == major_name)
            
        stats = query.group_by(ThiSinh.HoKhauThuongTru).all()
        
        enrolled_query = db.query(
            ThiSinh.HoKhauThuongTru.label("province"),
            func.count(func.distinct(HoSoNhapHoc.CCCD)).label('enrolled')
        ).join(HoSoNhapHoc, ThiSinh.CCCD == HoSoNhapHoc.CCCD)\
         .join(Nganh, Nganh.MaNganh == HoSoNhapHoc.MaNganh)\
         .join(NhomXetTuyen, NhomXetTuyen.MaNhom == HoSoNhapHoc.MaNhom)\
         .join(PhuongThuc, PhuongThuc.MaPT == NhomXetTuyen.MaPT)\
         .filter(HoSoNhapHoc.NamTuyenSinh == nam_tuyen_sinh)
         
        if phuong_thuc:
            enrolled_query = enrolled_query.filter(PhuongThuc.TenPhuongThuc == phuong_thuc)
        if major_name:
            enrolled_query = enrolled_query.filter(Nganh.TenNganh == major_name)
            
        enrolled_stats = enrolled_query.group_by(ThiSinh.HoKhauThuongTru).all()
        enrolled_dict = {row.province: row.enrolled for row in enrolled_stats}
        
        results = []
        for row in stats:
            province = row.province or "Không rõ"
            enrolled = enrolled_dict.get(row.province, 0)
            yield_rate = (enrolled / row.admitted * 100) if row.admitted > 0 else 0
            results.append({
                "province": province,
                "nam_tuyen_sinh": nam_tuyen_sinh,
                "phuong_thuc": phuong_thuc,
                "major_name": major_name,
                "total_applicants": row.applied,
                "admitted_applicants": row.admitted,
                "enrolled_applicants": enrolled,
                "yield_rate": round(yield_rate, 2)
            })
            
        return results

    def get_score_analytics(self, db: Session, nam_tuyen_sinh: int, phuong_thuc: str = None, major_name: str = None):
        """
        Score Distribution Analytics.
        """
        from app.models.student import DiemThi
        from app.models.admission import MonThi
        import statistics

        query = db.query(
            MonThi.TenMon,
            DiemThi.Diem
        ).join(DiemThi, MonThi.MaMon == DiemThi.MaMon)\
         .join(NguyenVong, NguyenVong.CCCD == DiemThi.CCCD)\
         .join(Nganh, Nganh.MaNganh == NguyenVong.MaNganh)\
         .join(NhomXetTuyen, NhomXetTuyen.MaNhom == NguyenVong.MaNhom)\
         .join(PhuongThuc, PhuongThuc.MaPT == NhomXetTuyen.MaPT)\
         .filter(NguyenVong.NamTuyenSinh == nam_tuyen_sinh, DiemThi.Diem != None)

        if phuong_thuc:
            query = query.filter(PhuongThuc.TenPhuongThuc == phuong_thuc)
        if major_name:
            query = query.filter(Nganh.TenNganh == major_name)
            
        raw_data = query.all()
        
        subject_scores = {}
        for row in raw_data:
            subj = row.TenMon
            if subj not in subject_scores:
                subject_scores[subj] = []
            subject_scores[subj].append(row.Diem)
            
        results = []
        for subj, scores in subject_scores.items():
            if not scores: continue
            
            avg_s = sum(scores) / len(scores)
            med_s = statistics.median(scores)
            min_s = min(scores)
            max_s = max(scores)
            
            brackets = { "<5": 0, "5-7": 0, "7-8": 0, "8-9": 0, "9-10": 0 }
            for s in scores:
                if s < 5: brackets["<5"] += 1
                elif s < 7: brackets["5-7"] += 1
                elif s < 8: brackets["7-8"] += 1
                elif s < 9: brackets["8-9"] += 1
                else: brackets["9-10"] += 1
                
            results.append({
                "subject_name": subj,
                "major_name": major_name,
                "phuong_thuc": phuong_thuc,
                "avg_score": round(avg_s, 2),
                "median_score": round(med_s, 2),
                "min_score": round(min_s, 2),
                "max_score": round(max_s, 2),
                "brackets": [{"bracket": k, "count": v} for k, v in brackets.items()]
            })
            
        return results

analytics_crud = CRUDAnalytics()
