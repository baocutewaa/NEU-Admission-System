-- ============================================================
--  NEU TUYỂN SINH -- CẤU TRÚC DATABASE
--  T-SQL (SQL Server / SSMS)
--  Giữ nguyên cấu trúc cũ + bổ sung bảng mới theo đề án
-- ============================================================

USE master;
GO

IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'neu_tuyensinh')
    CREATE DATABASE neu_tuyensinh
        COLLATE Vietnamese_CI_AS;
GO

USE neu_tuyensinh;
GO

-- ============================================================
--  PHẦN 1: CẤU TRÚC CŨ (chuyển sang T-SQL)
-- ============================================================

-- ------------------------------------------------------------
-- 1.1  chung_chi
-- ------------------------------------------------------------
IF OBJECT_ID('chung_chi', 'U') IS NULL
CREATE TABLE chung_chi (
    MaCC        VARCHAR(20)   NOT NULL,
    TenChungChi NVARCHAR(150) NULL,
    ThangDiem   INT           NULL,
    CONSTRAINT PK_chung_chi PRIMARY KEY (MaCC)
);
GO

-- ------------------------------------------------------------
-- 1.2  ky_thi
-- ------------------------------------------------------------
IF OBJECT_ID('ky_thi', 'U') IS NULL
CREATE TABLE ky_thi (
    MaKyThi  VARCHAR(20)   NOT NULL,
    TenKyThi NVARCHAR(150) NULL,
    CONSTRAINT PK_ky_thi PRIMARY KEY (MaKyThi)
);
GO

-- ------------------------------------------------------------
-- 1.3  mon_thi
-- ------------------------------------------------------------
IF OBJECT_ID('mon_thi', 'U') IS NULL
CREATE TABLE mon_thi (
    MaMon   VARCHAR(20)   NOT NULL,
    TenMon  NVARCHAR(100) NULL,
    NhomMon NVARCHAR(50)  NULL,
    CONSTRAINT PK_mon_thi PRIMARY KEY (MaMon)
);
GO

-- ------------------------------------------------------------
-- 1.4  phuong_thuc
-- ------------------------------------------------------------
IF OBJECT_ID('phuong_thuc', 'U') IS NULL
CREATE TABLE phuong_thuc (
    MaPT          VARCHAR(20)   NOT NULL,
    TenPhuongThuc NVARCHAR(150) NULL,
    CONSTRAINT PK_phuong_thuc PRIMARY KEY (MaPT)
);
GO

-- ------------------------------------------------------------
-- 1.5  nhom_xet_tuyen
-- ------------------------------------------------------------
IF OBJECT_ID('nhom_xet_tuyen', 'U') IS NULL
CREATE TABLE nhom_xet_tuyen (
    MaNhom  VARCHAR(20)   NOT NULL,
    MaPT    VARCHAR(20)   NOT NULL,
    TenNhom NVARCHAR(150) NULL,
    MoTa    NVARCHAR(255) NULL,
    CONSTRAINT PK_nhom_xet_tuyen PRIMARY KEY (MaNhom),
    CONSTRAINT FK_nhomxettuyen_phuongthuc
        FOREIGN KEY (MaPT) REFERENCES phuong_thuc (MaPT)
);
GO

-- ------------------------------------------------------------
-- 1.6  nganh
-- ------------------------------------------------------------
IF OBJECT_ID('nganh', 'U') IS NULL
CREATE TABLE nganh (
    MaNganh  VARCHAR(20)   NOT NULL,
    TenNganh NVARCHAR(150) NULL,
    ChiTieu  INT           NULL,
    CONSTRAINT PK_nganh PRIMARY KEY (MaNganh)
);
GO

-- ------------------------------------------------------------
-- 1.7  thisinh
-- ------------------------------------------------------------
IF OBJECT_ID('thisinh', 'U') IS NULL
CREATE TABLE thisinh (
    CCCD            CHAR(12)      NOT NULL,
    HoTen           NVARCHAR(100) NOT NULL,
    GioiTinh        NVARCHAR(10)  NULL,
    NgaySinh        DATE          NULL,
    NoiSinh         NVARCHAR(100) NULL,
    QueQuan         NVARCHAR(100) NULL,
    HoKhauThuongTru NVARCHAR(255) NULL,
    DanToc          NVARCHAR(50)  NULL,
    TonGiao         NVARCHAR(50)  NULL,
    CONSTRAINT PK_thisinh PRIMARY KEY (CCCD)
);
GO

-- ------------------------------------------------------------
-- 1.8  lien_he
-- ------------------------------------------------------------
IF OBJECT_ID('lien_he', 'U') IS NULL
CREATE TABLE lien_he (
    CCCD        CHAR(12)     NOT NULL,
    SoDienThoai VARCHAR(15)  NULL,
    Email       VARCHAR(100) NULL,
    CONSTRAINT PK_lien_he PRIMARY KEY (CCCD),
    CONSTRAINT FK_lienhe_thisinh
        FOREIGN KEY (CCCD) REFERENCES thisinh (CCCD)
        ON DELETE CASCADE
);
GO

-- ------------------------------------------------------------
-- 1.9  diem_thi
-- ------------------------------------------------------------
IF OBJECT_ID('diem_thi', 'U') IS NULL
CREATE TABLE diem_thi (
    CCCD    CHAR(12)    NOT NULL,
    MaKyThi VARCHAR(20) NOT NULL,
    MaMon   VARCHAR(20) NOT NULL,
    Diem    FLOAT       NULL,
    CONSTRAINT PK_diem_thi PRIMARY KEY (CCCD, MaKyThi, MaMon),
    CONSTRAINT FK_diemthi_thisinh FOREIGN KEY (CCCD)    REFERENCES thisinh (CCCD),
    CONSTRAINT FK_diemthi_kythi   FOREIGN KEY (MaKyThi) REFERENCES ky_thi  (MaKyThi),
    CONSTRAINT FK_diemthi_monthi  FOREIGN KEY (MaMon)   REFERENCES mon_thi  (MaMon)
);
GO

-- ------------------------------------------------------------
-- 1.10  thisinh_chung_chi
-- ------------------------------------------------------------
IF OBJECT_ID('thisinh_chung_chi', 'U') IS NULL
CREATE TABLE thisinh_chung_chi (
    CCCD       CHAR(12)    NOT NULL,
    MaCC       VARCHAR(20) NOT NULL,
    DiemGoc    FLOAT       NULL,
    DiemQuyDoi FLOAT       NULL,
    CONSTRAINT PK_thisinh_chungchi PRIMARY KEY (CCCD, MaCC),
    CONSTRAINT FK_tscc_thisinh  FOREIGN KEY (CCCD) REFERENCES thisinh   (CCCD),
    CONSTRAINT FK_tscc_chungchi FOREIGN KEY (MaCC) REFERENCES chung_chi (MaCC)
);
GO

-- ------------------------------------------------------------
-- 1.11  ho_so_nhap_hoc
-- ------------------------------------------------------------
IF OBJECT_ID('ho_so_nhap_hoc', 'U') IS NULL
CREATE TABLE ho_so_nhap_hoc (
    CCCD         CHAR(12)    NOT NULL,
    MaNganh      VARCHAR(20) NOT NULL,
    MaNhom       VARCHAR(20) NOT NULL,
    NamTuyenSinh INT         NULL,
    NgayXacNhan  DATE        NULL,
    CONSTRAINT PK_ho_so_nhap_hoc PRIMARY KEY (CCCD, MaNganh),
    CONSTRAINT FK_hsnhaphoc_thisinh       FOREIGN KEY (CCCD)    REFERENCES thisinh        (CCCD),
    CONSTRAINT FK_hsnhaphoc_nganh         FOREIGN KEY (MaNganh) REFERENCES nganh          (MaNganh),
    CONSTRAINT FK_hsnhaphoc_nhomxettuyen  FOREIGN KEY (MaNhom)  REFERENCES nhom_xet_tuyen (MaNhom)
);
GO


-- ============================================================
--  PHẦN 2: BẢNG MỚI THEO ĐỀ ÁN TUYỂN SINH
-- ============================================================

-- ------------------------------------------------------------
-- 2.1  vung_dia_ly
--      Danh mục tỉnh + địa bàn vùng ưu tiên (1, 2, 3, 4)
--      theo phân loại của Bộ GD&ĐT
--      → Thống kê tỉ lệ đỗ / nhập học theo vùng
-- ------------------------------------------------------------
IF OBJECT_ID('vung_dia_ly', 'U') IS NULL
CREATE TABLE vung_dia_ly (
    MaTinh    VARCHAR(10)   NOT NULL,
    TenTinh   NVARCHAR(100) NOT NULL,
    DiaBanVung TINYINT      NOT NULL,   -- 1 | 2 | 3 | 4 (ưu tiên khu vực)
    CONSTRAINT PK_vung_dia_ly  PRIMARY KEY (MaTinh),
    CONSTRAINT CK_diabanvung   CHECK (DiaBanVung BETWEEN 1 AND 4)
);
GO

-- ------------------------------------------------------------
-- 2.2  chi_tieu_theo_nam
--      Chỉ tiêu tuyển sinh từng ngành theo từng năm
--      → Theo dõi điều chỉnh chỉ tiêu theo cụm 5 năm
-- ------------------------------------------------------------
IF OBJECT_ID('chi_tieu_theo_nam', 'U') IS NULL
CREATE TABLE chi_tieu_theo_nam (
    MaNganh          VARCHAR(20)   NOT NULL,
    NamTuyenSinh     INT           NOT NULL,
    ChiTieuKeHoach   INT           NULL,    -- chỉ tiêu đặt ra đầu năm
    ChiTieuDieuChinh INT           NULL,    -- sau điều chỉnh (nếu có)
    GhiChu           NVARCHAR(255) NULL,
    CONSTRAINT PK_chitieu_theonam PRIMARY KEY (MaNganh, NamTuyenSinh),
    CONSTRAINT FK_chitieu_nganh FOREIGN KEY (MaNganh) REFERENCES nganh (MaNganh)
);
GO

-- ------------------------------------------------------------
-- 2.3  nguyen_vong
--      Toàn bộ nguyện vọng thí sinh đăng ký (kể cả không trúng)
--      → Tính Admission Rate, Enrollment Rate
--      → Phân tích thứ tự NV → mức độ yêu thích ngành
-- ------------------------------------------------------------
IF OBJECT_ID('nguyen_vong', 'U') IS NULL
CREATE TABLE nguyen_vong (
    MaNguyenVong    INT IDENTITY(1,1) NOT NULL,
    CCCD            CHAR(12)     NOT NULL,
    MaNganh         VARCHAR(20)  NOT NULL,
    MaNhom          VARCHAR(20)  NOT NULL,
    NamTuyenSinh    INT          NOT NULL,
    ThuTuNguyenVong TINYINT      NOT NULL,   -- 1 = NV ưu tiên nhất
    TrangThai       NVARCHAR(30) NOT NULL    -- 'Trung tuyen' | 'Khong trung tuyen' | 'Rut ho so'
        CONSTRAINT DF_nv_trangthai DEFAULT N'Chua xac dinh',
    CONSTRAINT PK_nguyen_vong PRIMARY KEY (MaNguyenVong),
    CONSTRAINT UQ_nguyen_vong UNIQUE (CCCD, MaNganh, NamTuyenSinh),
    CONSTRAINT FK_nv_thisinh  FOREIGN KEY (CCCD)    REFERENCES thisinh        (CCCD),
    CONSTRAINT FK_nv_nganh    FOREIGN KEY (MaNganh) REFERENCES nganh          (MaNganh),
    CONSTRAINT FK_nv_nhom     FOREIGN KEY (MaNhom)  REFERENCES nhom_xet_tuyen (MaNhom),
    CONSTRAINT CK_nv_thutu    CHECK (ThuTuNguyenVong BETWEEN 1 AND 30)
);
GO

CREATE NONCLUSTERED INDEX IX_nv_nganh_nam
    ON nguyen_vong (MaNganh, NamTuyenSinh)
    INCLUDE (TrangThai, ThuTuNguyenVong);
GO


PRINT N'=== Tạo cấu trúc database thành công! ===';
PRINT N'--- Bảng cũ (giữ nguyên): chung_chi, ky_thi, mon_thi, phuong_thuc,';
PRINT N'    nhom_xet_tuyen, nganh, thisinh, lien_he, diem_thi, thisinh_chung_chi, ho_so_nhap_hoc';
PRINT N'--- Bảng mới: vung_dia_ly, chi_tieu_theo_nam, nguyen_vong';
GO