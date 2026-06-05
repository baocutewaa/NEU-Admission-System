CREATE OR ALTER VIEW dbo.vw_phan_tich_tuyensinh AS
SELECT
    ts.CCCD,
    ts.HoTen,
    ts.GioiTinh,
    ts.NgaySinh,
    ts.QueQuan,
    n.TenNganh,
    nh.MaNhom                                           AS KhoiXetTuyen,
    d_thpt.TongDiemTHPT,
    d_other.HSA,
    d_other.TSA,
    cc.IELTS,
    cc.SAT,

    d_thpt.TongDiemTHPT                                 AS DXT_THPT,

    CASE WHEN d_other.HSA >= 85
         THEN CAST(d_other.HSA AS FLOAT) * 30.0 / 150.0
    END                                                 AS DXT_HSA,

    CASE WHEN d_other.TSA >= 60
         THEN CAST(d_other.TSA AS FLOAT) * 30.0 / 100.0
    END                                                 AS DXT_TSA,

    CASE WHEN cc.SAT >= 1200
         THEN CAST(cc.SAT AS FLOAT) * 30.0 / 1600.0
    END                                                 AS DXT_SAT,

    CASE
        WHEN cc.DiemIELTSQuyDoi IS NOT NULL
             AND (d_other.HSA >= 85 OR d_other.TSA >= 60)
        THEN cc.DiemIELTSQuyDoi
             + (COALESCE(CAST(d_other.HSA AS FLOAT) * 30.0 / 150.0,
                         CAST(d_other.TSA AS FLOAT) * 30.0 / 100.0) * 2.0) / 3.0
    END                                                 AS DXT_IELTS_DGNL,

    CASE
        WHEN cc.DiemIELTSQuyDoi IS NOT NULL
             AND ISNULL(d_thpt.TongDiemTHPT, 0) > 0
        THEN cc.DiemIELTSQuyDoi + d_thpt.TongDiemTHPT
    END                                                 AS DXT_IELTS_THPT,

    (
        SELECT MAX(v)
        FROM (VALUES
            (ISNULL(d_thpt.TongDiemTHPT, 0)),
            (ISNULL(CASE WHEN d_other.HSA >= 85
                         THEN CAST(d_other.HSA AS FLOAT) * 30.0 / 150.0 END, 0)),
            (ISNULL(CASE WHEN d_other.TSA >= 60
                         THEN CAST(d_other.TSA AS FLOAT) * 30.0 / 100.0 END, 0)),
            (ISNULL(CASE WHEN cc.SAT >= 1200
                         THEN CAST(cc.SAT AS FLOAT) * 30.0 / 1600.0 END, 0)),
            (ISNULL(CASE
                        WHEN cc.DiemIELTSQuyDoi IS NOT NULL
                             AND (d_other.HSA >= 85 OR d_other.TSA >= 60)
                        THEN cc.DiemIELTSQuyDoi
                             + (COALESCE(CAST(d_other.HSA AS FLOAT) * 30.0 / 150.0,
                                         CAST(d_other.TSA AS FLOAT) * 30.0 / 100.0) * 2.0) / 3.0
                    END, 0)),
            (ISNULL(CASE
                        WHEN cc.DiemIELTSQuyDoi IS NOT NULL
                             AND ISNULL(d_thpt.TongDiemTHPT, 0) > 0
                        THEN cc.DiemIELTSQuyDoi + d_thpt.TongDiemTHPT
                    END, 0))
        ) AS T(v)
    )                                                   AS DiemXetTuyen

FROM dbo.thisinh ts

LEFT JOIN dbo.ho_so_nhap_hoc   hs  ON ts.CCCD    = hs.CCCD
LEFT JOIN dbo.nhom_xet_tuyen   nh  ON hs.MaNhom  = nh.MaNhom
LEFT JOIN dbo.nganh            n   ON hs.MaNganh = n.MaNganh

-- Tổng điểm THPT
LEFT JOIN (
    SELECT
        dt.CCCD,
        SUM(CASE
            -- A00: Toán + Vật Lý + Hóa Học 
            WHEN nh2.MaNhom = 'A00' AND mt.TenMon IN (N'Toán', N'Vật Lý', N'Hóa Học')         THEN dt.Diem
            -- A01: Toán + Vật Lý + Tiếng Anh
            WHEN nh2.MaNhom = 'A01' AND mt.TenMon IN (N'Toán', N'Vật Lý', N'Tiếng Anh')       THEN dt.Diem
            -- B00: Toán + Hóa Học + Sinh Học
            WHEN nh2.MaNhom = 'B00' AND mt.TenMon IN (N'Toán', N'Hóa Học', N'Sinh Học')       THEN dt.Diem
            -- C00: Ngữ Văn + Lịch Sử + Địa Lý
            WHEN nh2.MaNhom = 'C00' AND mt.TenMon IN (N'Ngữ Văn', N'Lịch Sử', N'Địa Lý')     THEN dt.Diem
            -- D01: Toán + Ngữ Văn + Tiếng Anh
            WHEN nh2.MaNhom = 'D01' AND mt.TenMon IN (N'Toán', N'Ngữ Văn', N'Tiếng Anh')     THEN dt.Diem
            -- D07: Toán + Hóa Học + Tiếng Anh
            WHEN nh2.MaNhom = 'D07' AND mt.TenMon IN (N'Toán', N'Hóa Học', N'Tiếng Anh')     THEN dt.Diem
            -- HSA: dùng môn "Khoa học"
            WHEN nh2.MaNhom = 'HSA' AND mt.NhomMon = 'HSA'                                    THEN dt.Diem
            ELSE 0
        END) AS TongDiemTHPT
    FROM      dbo.diem_thi        dt
    JOIN      dbo.ky_thi          kt  ON dt.MaKyThi = kt.MaKyThi
    JOIN      dbo.mon_thi         mt  ON dt.MaMon   = mt.MaMon
    JOIN      dbo.ho_so_nhap_hoc  hs2 ON dt.CCCD    = hs2.CCCD
    JOIN      dbo.nhom_xet_tuyen  nh2 ON hs2.MaNhom = nh2.MaNhom
    WHERE     kt.TenKyThi LIKE N'%THPT%'
    GROUP BY  dt.CCCD
) d_thpt ON ts.CCCD = d_thpt.CCCD

-- HSA / TSA
LEFT JOIN (
    SELECT
        dt.CCCD,
        SUM(CASE WHEN kt.TenKyThi LIKE N'%năng lực%' THEN dt.Diem ELSE 0 END) AS HSA,
        SUM(CASE WHEN kt.TenKyThi LIKE N'%tư duy%'   THEN dt.Diem ELSE 0 END) AS TSA
    FROM  dbo.diem_thi dt
    JOIN  dbo.ky_thi   kt ON dt.MaKyThi = kt.MaKyThi
    GROUP BY dt.CCCD
) d_other ON ts.CCCD = d_other.CCCD

-- Chứng chỉ
LEFT JOIN (
    SELECT
        tc.CCCD,
        MAX(CASE WHEN cc.MaCC = 'IELTS' THEN tc.DiemGoc    END) AS IELTS,
        MAX(CASE WHEN cc.MaCC = 'SAT'   THEN tc.DiemGoc    END) AS SAT,
        MAX(CASE WHEN cc.MaCC = 'IELTS' THEN tc.DiemQuyDoi END) AS DiemIELTSQuyDoi
    FROM  dbo.thisinh_chung_chi tc
    JOIN  dbo.chung_chi         cc ON tc.MaCC = cc.MaCC
    GROUP BY tc.CCCD
) cc ON ts.CCCD = cc.CCCD;
GO


select * from vw_phan_tich_tuyensinh