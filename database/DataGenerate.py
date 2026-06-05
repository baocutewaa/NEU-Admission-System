import random
from faker import Faker

# Khởi tạo Faker hỗ trợ ngôn ngữ Tiếng Việt
fake = Faker('vi_VN')

# ============================================================
# DỮ LIỆU DANH MỤC CỐ ĐỊNH
# ============================================================

LIST_TINH_THANH = [
    "Hà Nội", "TP. Hồ Chí Minh", "Hải Phòng", "Đà Nẵng", "Cần Thơ", "Hà Giang", "Cao Bằng", "Lai Châu",
    "Lào Cai", "Tuyên Quang", "Lạng Sơn", "Bắc Kạn", "Thái Nguyên", "Yên Bái", "Sơn La", "Phú Thọ",
    "Vĩnh Phúc", "Quảng Ninh", "Bắc Giang", "Bắc Ninh", "Hải Dương", "Hưng Yên", "Thái Bình", "Hà Nam",
    "Nam Định", "Ninh Bình", "Thanh Hóa", "Nghệ An", "Hà Tĩnh", "Quảng Bình", "Quảng Trị", "Thừa Thiên Huế",
    "Quảng Nam", "Quảng Ngãi", "Bình Định", "Phú Yên", "Khánh Hòa", "Ninh Thuận", "Bình Thuận", "Kon Tum",
    "Gia Lai", "Đắk Lắk", "Đắk Nông", "Lâm Đồng", "Bình Phước", "Tây Ninh", "Bình Dương", "Đồng Nai",
    "Bà Rịa - Vũng Tàu", "Long An", "Tiền Giang", "Bến Tre", "Trà Vinh", "Vĩnh Long", "Đồng Tháp",
    "An Giang", "Kiên Giang", "Hậu Giang", "Sóc Trăng", "Bạc Liêu", "Cà Mau"
]

LIST_TINH_MA = [(f"T{index:02d}", ten) for index, ten in enumerate(LIST_TINH_THANH, start=1)]

LIST_NGANH = [
    # I. Các ngành/chương trình mới mở và tuyển sinh năm 2025
    ('7340408', 'Quan hệ lao động', 60),
    ('7380109', 'Luật thương mại quốc tế', 60),

    # II. Các ngành/chương trình mới mở và tuyển sinh từ năm 2024
    ('EP15', 'Khoa học dữ liệu', 120),
    ('EP16', 'Trí tuệ nhân tạo', 120),
    ('EP17', 'Kỹ thuật phần mềm', 60),
    ('EP18', 'Quản trị giải trí và sự kiện', 60),
    ('7480104', 'Hệ thống thông tin', 60),
    ('7480202', 'An toàn thông tin', 60),

    # III. Các chương trình học bằng tiếng Việt
    ('7510605', 'Logistics và Quản lý chuỗi cung ứng', 110),
    ('7340120', 'Kinh doanh quốc tế', 120),
    ('7310106', 'Kinh tế quốc tế', 120),
    ('7340122', 'Thương mại điện tử', 60),
    ('7340121', 'Kinh doanh thương mại', 290),
    ('7340115', 'Marketing', 300),
    ('7340302', 'Kiểm toán', 170),
    ('7340301', 'Kế toán', 290),
    ('7340201', 'Tài chính - Ngân hàng', 500),
    ('7340204', 'Bảo hiểm', 160),
    ('7340404', 'Quản trị nhân lực', 120),
    ('7340101', 'Quản trị kinh doanh', 760),
    ('7810201', 'Quản trị khách sạn', 160),
    ('7810103', 'Quản trị dịch vụ du lịch và lữ hành', 190),
    ('7310101_1', 'Kinh tế học', 150),
    ('7310101_2', 'Kinh tế và quản lý đô thị', 120),
    ('7310101_3', 'Kinh tế và quản lý nguồn nhân lực', 70),
    ('7310105', 'Kinh tế phát triển', 220),
    ('7310108', 'Toán kinh tế', 160),
    ('7310107', 'Thống kê kinh tế', 120),
    ('7340405', 'Hệ thống thông tin quản lý', 120),
    ('7480201', 'Công nghệ thông tin', 120),
    ('7480101', 'Khoa học máy tính', 60),
    ('7380107', 'Luật kinh tế', 190),
    ('7380101', 'Luật', 60),
    ('7340401', 'Khoa học quản lý', 120),
    ('7340403', 'Quản lý công', 140),
    ('7850101', 'Quản lý tài nguyên và môi trường', 70),
    ('7850103', 'Quản lý đất đai', 60),
    ('7340116', 'Bất động sản', 130),
    ('7850102', 'Kinh tế tài nguyên thiên nhiên', 110),
    ('7620115', 'Kinh tế nông nghiệp', 80),
    ('7620114', 'Kinh doanh nông nghiệp', 85),
    ('7310104', 'Kinh tế đầu tư', 180),
    ('7340409', 'Quản lý dự án', 60),
    ('7320108', 'Quan hệ công chúng', 60),
    ('7220201', 'Ngôn ngữ Anh', 140),

    # IV. Các chương trình đào tạo bằng tiếng Anh
    ('EBBA', 'Quản trị kinh doanh (E-BBA)', 160),
    ('EPMP', 'Quản lý công và Chính sách (E-PMP)', 120),
    ('EP01', 'Khởi nghiệp và phát triển kinh doanh (BBAE)', 120),
    ('EP02', 'Định phí Bảo hiểm & Quản trị rủi ro (Actuary)', 110),
    ('EP03', 'Phân tích dữ liệu kinh tế (Economic Data Analytics)', 120),
    ('EP04', 'Kế toán tích hợp chứng chỉ quốc tế', 60),
    ('EP05', 'Kinh doanh số (E-BDB)', 60),
    ('EP06', 'Phân tích kinh doanh (BA)', 60),
    ('EP07', 'Quản trị điều hành thông minh (E-SOM)', 60),
    ('EP08', 'Quản trị chất lượng và Đổi mới (E-MQI)', 60),
    ('EP09', 'Công nghệ tài chính (BFT)', 120),
    ('EP10', 'Tài chính và Đầu tư (BFI)', 120),
    ('EP11', 'Quản trị khách sạn quốc tế (IHME)', 60),
    ('EP12', 'Kiểm toán tích hợp chứng chỉ quốc tế', 60),
    ('EP13', 'Kinh tế học tài chính (FE)', 120),
    ('EP14', 'Logistics và Quản lý chuỗi cung ứng tích hợp chứng chỉ quốc tế (LSIC)', 120),

    # V. Các chương trình định hướng ứng dụng POHE
    ('POHE1', 'POHE - Quản trị khách sạn', 60),
    ('POHE2', 'POHE - Quản trị lữ hành', 60),
    ('POHE3', 'POHE - Truyền thông Marketing', 60),
    ('POHE4', 'POHE - Luật kinh doanh', 60),
    ('POHE5', 'POHE - Quản trị kinh doanh thương mại', 60),
    ('POHE6', 'POHE - Quản lý thị trường', 60),
    ('POHE7', 'POHE - Thẩm định giá', 60),

    # VI. Các chương trình tiên tiến
    ('TT1_KT', 'Tiên tiến - Kế toán', 60),
    ('TT1_KHTC', 'Tiên tiến - Kế hoạch tài chính', 60),
    ('TT1_QTKD', 'Tiên tiến - Quản trị kinh doanh', 60),
    ('TT2_TC', 'Tiên tiến - Tài chính', 60),
    ('TT2_KXQT', 'Tiên tiến - Kinh doanh quốc tế', 60),

    # VII. Các chương trình chất lượng cao
    ('CLC1_KTPT', 'Chất lượng cao - Kinh tế phát triển', 60),
    ('CLC1_NH', 'Chất lượng cao - Ngân hàng', 60),
    ('CLC1_CNTT', 'Chất lượng cao - Công nghệ thông tin và chuyển đổi số', 60),
    ('CLC1_BH', 'Chất lượng cao - Bảo hiểm tích hợp chứng chỉ ANZIIF', 60),
    ('CLC2_KTDT', 'Chất lượng cao - Kinh tế Đầu tư', 60),
    ('CLC2_QTNL', 'Chất lượng cao - Quản trị nhân lực', 60),
    ('CLC2_QTKD', 'Chất lượng cao - Quản trị kinh doanh', 60),
    ('CLC2_QHCC', 'Chất lượng cao - Quan hệ công chúng', 60),
    ('CLC3_TCDN', 'Chất lượng cao - Tài chính doanh nghiệp', 60),
    ('CLC3_DM', 'Chất lượng cao - Digital Marketing', 60),
    ('CLC3_QTM', 'Chất lượng cao - Quản trị Marketing', 60),
    ('CLC3_QTKDQT', 'Chất lượng cao - Quản trị Kinh doanh quốc tế', 60),
    ('CLC3_KTQT', 'Chất lượng cao - Kinh tế quốc tế', 60),
    ('CLC3_LOG', 'Chất lượng cao - Logistics và quản lý chuỗi cung ứng', 60),
    ('CLC3_TMDT', 'Chất lượng cao - Thương mại điện tử', 60),
    ('CLC3_KT', 'Chất lượng cao - Kiểm toán tích hợp chứng chỉ ACCA', 60)
]

LIST_PHUONG_THUC = [
    ('PT1', 'Xét tuyển thẳng'),
    ('PT2', 'Thi tốt nghiệp THPT'),
    ('PT3', 'Xét tuyển kết hợp')
]

LIST_NHOM = [
    ('A00', 'Toán, Lý, Hóa', 'PT2'),
    ('A01', 'Toán, Lý, Anh', 'PT2'),
    ('B00', 'Toán, Hóa, Sinh', 'PT2'),
    ('C00', 'Văn, Sử, Địa', 'PT2'),
    ('D01', 'Toán, Văn, Anh', 'PT2'),
    ('D07', 'Toán, Hóa, Anh', 'PT2'),
    ('SAT', 'Xét tuyển chứng chỉ SAT', 'PT3'),
    ('IELTS', 'Xét tuyển chứng chỉ Tiếng Anh + Điểm thi', 'PT3'),
    ('HSA', 'Đánh giá năng lực ĐHQGHN', 'PT3'), 
    ('TSA', 'Đánh giá tư duy Bách Khoa', 'PT3')  
]

LIST_MON_THI = [
    # Môn THPT
    ('TOAN', 'Toán', 'KHTN'), ('VAN', 'Ngữ Văn', 'XH'), ('ANH', 'Tiếng Anh', 'NN'),
    ('LY', 'Vật Lý', 'KHTN'), ('HOA', 'Hóa Học', 'KHTN'), ('SINH', 'Sinh Học', 'KHTN'),
    ('SU', 'Lịch Sử', 'XH'), ('DIA', 'Địa Lý', 'XH'), ('GDCD', 'Giáo dục công dân', 'XH'),
    # Môn thành phần HSA
    ('HSA_DL', 'Tư duy định lượng', 'HSA'),
    ('HSA_DT', 'Tư duy định tính', 'HSA'),
    ('HSA_KH', 'Khoa học', 'HSA'),
    # Môn thành phần TSA
    ('TSA_TOAN', 'Tư duy Toán học', 'TSA'),
    ('TSA_DOC', 'Tư duy Đọc hiểu', 'TSA'),
    ('TSA_KH', 'Tư duy Khoa học/GQVĐ', 'TSA')
]

LIST_CHUNG_CHI = [
    ('SAT', 'Scholastic Assessment Test', 1600),
    ('IELTS', 'International English Language Testing System', 9.0),
    ('TOEIC', 'Test of English for International Communication', 990)
]

LIST_KY_THI = [
    ('TN2024', 'Kỳ thi Tốt nghiệp THPT 2024'),
    ('HSA2024', 'Đánh giá năng lực ĐHQGHN 2024'),
    ('TSA2024', 'Đánh giá tư duy ĐHBK Hà Nội 2024')
]

# ============================================================
# HÀM BỔ TRỢ & SINH DỮ LIỆU T-SQL
# ============================================================

def escape_str(val):
    """Hàm xử lý chuỗi an toàn cho SQL Server (thay thế đơn nháy thành đôi nháy)"""
    if val is None:
        return ""
    return str(val).replace("'", "''")

def generate_sql(num_students=3000):
    sql_statements = []
    
    # 1. Cấu hình ban đầu cho SQL Server
    sql_statements.append("USE neu_tuyensinh;")
    sql_statements.append("GO\n")
    sql_statements.append("SET NOCOUNT ON;")
    sql_statements.append("GO\n")
    
    sql_statements.append("-- ==========================================================")
    sql_statements.append("-- CHÈN DỮ LIỆU DANH MỤC CỐ ĐỊNH")
    sql_statements.append("-- ==========================================================")
    sql_statements.append("BEGIN TRANSACTION;")
    
    for pt in LIST_PHUONG_THUC:
        sql_statements.append(f"INSERT INTO phuong_thuc (MaPT, TenPhuongThuc) VALUES ('{pt[0]}', N'{escape_str(pt[1])}');")
        
    for ng in LIST_NGANH:
        sql_statements.append(f"INSERT INTO nganh (MaNganh, TenNganh, ChiTieu) VALUES ('{ng[0]}', N'{escape_str(ng[1])}', {ng[2]});")
        
    for ma_tinh, ten_tinh in LIST_TINH_MA:
        sql_statements.append(
            f"INSERT INTO vung_dia_ly (MaTinh, TenTinh, DiaBanVung) VALUES ('{ma_tinh}', N'{escape_str(ten_tinh)}', {random.randint(1, 4)});"
        )
        
    for ng in LIST_NGANH:
        chi_tieu_ke_hoach = ng[2]
        chi_tieu_dieu_chinh = max(0, int(round(chi_tieu_ke_hoach * random.uniform(0.9, 1.1))))
        sql_statements.append(
            "INSERT INTO chi_tieu_theo_nam (MaNganh, NamTuyenSinh, ChiTieuKeHoach, ChiTieuDieuChinh, GhiChu) "
            f"VALUES ('{ng[0]}', 2024, {chi_tieu_ke_hoach}, {chi_tieu_dieu_chinh}, N'Kế hoạch tuyển sinh năm 2024');"
        )
        
    for nhom in LIST_NHOM:
        sql_statements.append(
            "INSERT INTO nhom_xet_tuyen (MaNhom, MaPT, TenNhom, MoTa) "
            f"VALUES ('{nhom[0]}', '{nhom[2]}', N'{escape_str(nhom[1])}', NULL);"
        )
        
    for mon in LIST_MON_THI:
        sql_statements.append(f"INSERT INTO mon_thi (MaMon, TenMon, NhomMon) VALUES ('{mon[0]}', N'{escape_str(mon[1])}', N'{escape_str(mon[2])}');")
        
    for cc in LIST_CHUNG_CHI:
        sql_statements.append(f"INSERT INTO chung_chi (MaCC, TenChungChi, ThangDiem) VALUES ('{cc[0]}', N'{escape_str(cc[1])}', {cc[2]});")
        
    for kt in LIST_KY_THI:
        sql_statements.append(f"INSERT INTO ky_thi (MaKyThi, TenKyThi) VALUES ('{kt[0]}', N'{escape_str(kt[1])}');")

    sql_statements.append("COMMIT TRANSACTION;")
    sql_statements.append("GO\n")

    # 2. Sinh dữ liệu động cho Thí sinh theo Batch Transaction
    sql_statements.append(f"-- ==========================================================")
    sql_statements.append(f"-- BẮT ĐẦU SINH DỮ LIỆU {num_students} THÍ SINH (CHIA THEO BATCH TRANSACTION)")
    sql_statements.append(f"-- ==========================================================")
    
    batch_size = 500  # Cứ 500 thí sinh gom vào 1 Transaction để tăng tốc tối đa cho SQL Server
    
    for i in range(num_students):
        if i % batch_size == 0:
            sql_statements.append("BEGIN TRANSACTION;")
            
        # A. THÍ SINH
        cccd = f"0{random.randint(10000000000, 99999999999)}"  # Đảm bảo đủ 12 số kiểu CHAR(12)
        ho_ten = fake.name()
        gioi_tinh = random.choice(['Nam', 'Nữ'])
        ngay_sinh = fake.date_of_birth(minimum_age=16, maximum_age=21).strftime('%Y-%m-%d')
        noi_sinh = random.choice(LIST_TINH_THANH)
        que_quan = random.choice(LIST_TINH_THANH)
        ho_khau = fake.address().replace("\n", ", ")
        
        sql_statements.append(
            "INSERT INTO thisinh (CCCD, HoTen, GioiTinh, NgaySinh, NoiSinh, QueQuan, HoKhauThuongTru, DanToc, TonGiao) "
            f"VALUES ('{cccd}', N'{escape_str(ho_ten)}', N'{gioi_tinh}', '{ngay_sinh}', N'{escape_str(noi_sinh)}', N'{escape_str(que_quan)}', N'{escape_str(ho_khau)}', N'Kinh', N'Không');"
        )
        sql_statements.append(f"INSERT INTO lien_he (CCCD, SoDienThoai, Email) VALUES ('{cccd}', '09{random.randint(10000000, 99999999)}', 'user{i}@gmail.com');")
        
        # B. ĐIỂM THI THPT (Bắt buộc Toán, Văn, Anh)
        toan = round(random.uniform(5.0, 10.0), 2)
        van = round(random.uniform(5.0, 9.5), 2)
        anh = round(random.uniform(4.0, 10.0), 2)
        
        sql_statements.append(f"INSERT INTO diem_thi (CCCD, MaKyThi, MaMon, Diem) VALUES ('{cccd}', 'TN2024', 'TOAN', {toan});")
        sql_statements.append(f"INSERT INTO diem_thi (CCCD, MaKyThi, MaMon, Diem) VALUES ('{cccd}', 'TN2024', 'VAN', {van});")
        sql_statements.append(f"INSERT INTO diem_thi (CCCD, MaKyThi, MaMon, Diem) VALUES ('{cccd}', 'TN2024', 'ANH', {anh});")

        is_khtn = random.choice([True, False])
        if is_khtn:
            sql_statements.append(f"INSERT INTO diem_thi (CCCD, MaKyThi, MaMon, Diem) VALUES ('{cccd}', 'TN2024', 'LY', {round(random.uniform(5,10),2)});")
            sql_statements.append(f"INSERT INTO diem_thi (CCCD, MaKyThi, MaMon, Diem) VALUES ('{cccd}', 'TN2024', 'HOA', {round(random.uniform(5,10),2)});")
            sql_statements.append(f"INSERT INTO diem_thi (CCCD, MaKyThi, MaMon, Diem) VALUES ('{cccd}', 'TN2024', 'SINH', {round(random.uniform(5,10),2)});")
            valid_groups = ['A00', 'A01', 'B00', 'D01', 'D07']
        else:
            sql_statements.append(f"INSERT INTO diem_thi (CCCD, MaKyThi, MaMon, Diem) VALUES ('{cccd}', 'TN2024', 'SU', {round(random.uniform(5,10),2)});")
            sql_statements.append(f"INSERT INTO diem_thi (CCCD, MaKyThi, MaMon, Diem) VALUES ('{cccd}', 'TN2024', 'DIA', {round(random.uniform(5,10),2)});")
            sql_statements.append(f"INSERT INTO diem_thi (CCCD, MaKyThi, MaMon, Diem) VALUES ('{cccd}', 'TN2024', 'GDCD', {round(random.uniform(6,10),2)});")
            valid_groups = ['C00', 'D01']

        nhom_xet_tuyen = random.choice(valid_groups)
        
        # C. ĐIỂM THI HSA (ĐHQGHN)
        has_hsa = random.random() < 0.3
        hsa_score_total = 0
        if has_hsa:
            dinh_luong = random.randint(30, 50)
            dinh_tinh = random.randint(30, 50)
            khoa_hoc = random.randint(30, 50)
            hsa_score_total = dinh_luong + dinh_tinh + khoa_hoc
            
            sql_statements.append(f"INSERT INTO diem_thi (CCCD, MaKyThi, MaMon, Diem) VALUES ('{cccd}', 'HSA2024', 'HSA_DL', {dinh_luong});")
            sql_statements.append(f"INSERT INTO diem_thi (CCCD, MaKyThi, MaMon, Diem) VALUES ('{cccd}', 'HSA2024', 'HSA_DT', {dinh_tinh});")
            sql_statements.append(f"INSERT INTO diem_thi (CCCD, MaKyThi, MaMon, Diem) VALUES ('{cccd}', 'HSA2024', 'HSA_KH', {khoa_hoc});")

        # D. ĐIỂM THI TSA (Bách Khoa)
        has_tsa = random.random() < 0.2
        tsa_score_total = 0
        if has_tsa:
            tsa_toan = round(random.uniform(20, 40), 2)
            tsa_doc = round(random.uniform(10, 20), 2)
            tsa_kh = round(random.uniform(20, 40), 2)
            tsa_score_total = tsa_toan + tsa_doc + tsa_kh
            
            sql_statements.append(f"INSERT INTO diem_thi (CCCD, MaKyThi, MaMon, Diem) VALUES ('{cccd}', 'TSA2024', 'TSA_TOAN', {tsa_toan});")
            sql_statements.append(f"INSERT INTO diem_thi (CCCD, MaKyThi, MaMon, Diem) VALUES ('{cccd}', 'TSA2024', 'TSA_DOC', {tsa_doc});")
            sql_statements.append(f"INSERT INTO diem_thi (CCCD, MaKyThi, MaMon, Diem) VALUES ('{cccd}', 'TSA2024', 'TSA_KH', {tsa_kh});")

        # E. CHỨNG CHỈ QUỐC TẾ
        has_cert = random.random() < 0.3
        cert_group = None
        if has_cert:
            cert_type = random.choice(['IELTS', 'SAT'])
            if cert_type == 'IELTS':
                diem_goc = random.choice([6.0, 6.5, 7.0, 7.5, 8.0])
                diem_quy_doi = 10.0 if diem_goc >= 7.5 else (9.5 if diem_goc == 7.0 else (9.0 if diem_goc == 6.5 else 8.5))
                sql_statements.append(f"INSERT INTO thisinh_chung_chi (CCCD, MaCC, DiemGoc, DiemQuyDoi) VALUES ('{cccd}', 'IELTS', {diem_goc}, {diem_quy_doi});")
                cert_group = 'IELTS'
            else:
                diem_goc = random.randint(1200, 1550)
                diem_quy_doi = round(diem_goc * 30 / 1600, 2)
                sql_statements.append(f"INSERT INTO thisinh_chung_chi (CCCD, MaCC, DiemGoc, DiemQuyDoi) VALUES ('{cccd}', 'SAT', {diem_goc}, {diem_quy_doi});")
                cert_group = 'SAT'

        # F. XÁC ĐỊNH PHƯƠNG THỨC TRÚNG TUYỂN ƯU TIÊN
        if has_cert and random.random() > 0.3: 
            nhom_xet_tuyen = cert_group
        elif has_hsa and hsa_score_total > 85:
            nhom_xet_tuyen = 'HSA'
        elif has_tsa and tsa_score_total > 60:
            nhom_xet_tuyen = 'TSA'

        nganh_trung_tuyen = random.choice(LIST_NGANH)

        # G. NGUYỆN VỌNG (Đảm bảo tính duy nhất của cặp CCCD, MaNganh, NamTuyenSinh theo UQ_nguyen_vong)
        so_nv = random.randint(3, 6)
        danh_sach_nganh = [nganh_trung_tuyen]
        while len(danh_sach_nganh) < so_nv:
            nganh_moi = random.choice(LIST_NGANH)
            if nganh_moi[0] not in [n[0] for n in danh_sach_nganh]:
                danh_sach_nganh.append(nganh_moi)
        random.shuffle(danh_sach_nganh)

        for thu_tu, nganh_nv in enumerate(danh_sach_nganh, start=1):
            if nganh_nv[0] == nganh_trung_tuyen[0]:
                trang_thai = 'Trung tuyen'
            else:
                trang_thai = random.choices(['Khong trung tuyen', 'Rut ho so'], weights=[0.9, 0.1])[0]

            sql_statements.append(
                "INSERT INTO nguyen_vong (CCCD, MaNganh, MaNhom, NamTuyenSinh, ThuTuNguyenVong, TrangThai) "
                f"VALUES ('{cccd}', '{nganh_nv[0]}', '{nhom_xet_tuyen}', 2024, {thu_tu}, N'{trang_thai}');"
            )
        
        # H. HỒ SƠ NHẬP HỌC
        sql_statements.append(
            "INSERT INTO ho_so_nhap_hoc (CCCD, MaNganh, MaNhom, NamTuyenSinh, NgayXacNhan) "
            f"VALUES ('{cccd}', '{nganh_trung_tuyen[0]}', '{nhom_xet_tuyen}', 2024, '2024-08-{random.randint(20, 30)}');"
        )
        
        # Đóng transaction của Batch hiện tại
        if (i + 1) % batch_size == 0 or (i + 1) == num_students:
            sql_statements.append("COMMIT TRANSACTION;")
            sql_statements.append("GO\n")

    return "\n".join(sql_statements)

if __name__ == "__main__":
    try:
        # Số lượng thí sinh cần sinh dữ liệu (Bạn có thể điều chỉnh tham số này)
        TOTAL_STUDENTS = 3000
        
        print("Đang tạo kịch bản sinh dữ liệu T-SQL...")
        sql_script = generate_sql(TOTAL_STUDENTS)
        
        # Ghi ra file nén định dạng UTF-8 có BOM để SSMS nhận diện tiếng Việt chính xác nhất
        output_file = "DuLieuTuyenSinh_SQLServer.sql"
        with open(output_file, "w", encoding="utf-8-sig") as f:
            f.write(sql_script)
            
        print(f"--> Đã tạo thành công file: '{output_file}' tương thích hoàn toàn SQL Server!")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")