import { useState } from 'react';
import { searchStudentApi, fetchStudentDetailApi } from '../services/api';

const StudentSearch = () => {
    const [query, setQuery] = useState('');
    const [students, setStudents] = useState([]);
    const [loading, setLoading] = useState(false);
    const [searched, setSearched] = useState(false);
    const [selectedStudent, setSelectedStudent] = useState(null);
    const [studentDetail, setStudentDetail] = useState(null);
    const [loadingDetail, setLoadingDetail] = useState(false);
    const [activeTab, setActiveTab] = useState('profile');

    const handleSearch = async (e) => {
        if (e) e.preventDefault();
        if (!query.trim()) return;

        setLoading(true);
        setSearched(true);
        setSelectedStudent(null);
        setStudentDetail(null);
        try {
            const data = await searchStudentApi(query);
            setStudents(data || []);
        } catch (err) {
            console.error("Lỗi khi tra cứu học sinh:", err);
            setStudents([]);
        } finally {
            setLoading(false);
        }
    };

    const handleViewDetail = async (student) => {
        setSelectedStudent(student);
        setLoadingDetail(true);
        setStudentDetail(null);
        setActiveTab('profile');
        try {
            const detail = await fetchStudentDetailApi(student.cccd);
            setStudentDetail(detail);
        } catch (err) {
            console.error("Lỗi khi tải chi tiết thí sinh:", err);
        } finally {
            setLoadingDetail(false);
        }
    };

    const renderDetailContent = () => {
        if (loadingDetail) {
            return (
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '40px', gap: '12px' }}>
                    <div className="spinner" style={{ width: '32px', height: '32px' }}></div>
                    <span style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Đang tải dữ liệu hồ sơ...</span>
                </div>
            );
        }

        if (!studentDetail) {
            // Fallback display with basic info
            return (
                <div className="student-detail-content-section">
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '20px' }}>
                        <p><strong>Họ tên:</strong><br />{selectedStudent.ho_ten}</p>
                        <p><strong>Mã định danh (CCCD):</strong><br />{selectedStudent.ma_dinh_danh}</p>
                        <p><strong>Giới tính:</strong><br />{selectedStudent.gioi_tinh || 'Chưa rõ'}</p>
                    </div>
                    <div style={{ padding: '16px', background: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: '8px', color: '#64748b', textAlign: 'center' }}>
                        Không lấy được thông tin chi tiết từ máy chủ hoặc đang chờ kết nối.
                    </div>
                </div>
            );
        }

        switch (activeTab) {
            case 'profile':
                return (
                    <div className="student-detail-content-section">
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
                            <p><strong>Họ tên:</strong><br />{studentDetail.profile.HoTen}</p>
                            <p><strong>Mã định danh (CCCD):</strong><br />{studentDetail.profile.CCCD}</p>
                            <p><strong>Giới tính:</strong><br />{studentDetail.profile.GioiTinh || 'Chưa cập nhật'}</p>
                            <p><strong>Ngày sinh:</strong><br />{studentDetail.profile.NgaySinh || 'Chưa cập nhật'}</p>
                            <p><strong>Dân tộc:</strong><br />{studentDetail.profile.DanToc || 'Chưa cập nhật'}</p>
                            <p><strong>Tôn giáo:</strong><br />{studentDetail.profile.TonGiao || 'Chưa cập nhật'}</p>
                            <p><strong>Nơi sinh:</strong><br />{studentDetail.profile.NoiSinh || 'Chưa cập nhật'}</p>
                            <p><strong>Quê quán:</strong><br />{studentDetail.profile.QueQuan || 'Chưa cập nhật'}</p>
                            <p style={{ gridColumn: 'span 2' }}><strong>Hộ khẩu thường trú:</strong><br />{studentDetail.profile.HoKhauThuongTru || 'Chưa cập nhật'}</p>
                        </div>
                        
                        <h3 style={{ marginTop: '24px', marginBottom: '16px', borderBottom: '1px solid var(--border)', paddingBottom: '8px', color: 'var(--primary)' }}>Thông tin liên hệ</h3>
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
                            <p><strong>Số điện thoại:</strong><br />{studentDetail.contact?.SoDienThoai || 'Chưa cập nhật'}</p>
                            <p><strong>Email:</strong><br />{studentDetail.contact?.Email || 'Chưa cập nhật'}</p>
                        </div>
                    </div>
                );
            case 'aspirations':
                return (
                    <div className="student-detail-content-section">
                        <table className="detail-table">
                            <thead>
                                <tr>
                                    <th>Thứ tự NV</th>
                                    <th>Mã Ngành</th>
                                    <th>Tên Ngành</th>
                                    <th>Trạng thái</th>
                                </tr>
                            </thead>
                            <tbody>
                                {studentDetail.aspirations && studentDetail.aspirations.length > 0 ? (
                                    studentDetail.aspirations.map((asp, idx) => (
                                        <tr key={idx}>
                                            <td style={{ fontWeight: 600 }}>NV{asp.ThuTuNguyenVong}</td>
                                            <td>{asp.MaNganh}</td>
                                            <td>{asp.TenNganh || 'Chưa rõ'}</td>
                                            <td>
                                                <span className={`status-badge ${asp.TrangThai === 'Trung tuyen' || asp.TrangThai === 'Trúng tuyển' ? 'status-admitted' : 'status-pending'}`}>
                                                    {asp.TrangThai === 'Trung tuyen' ? 'Trúng tuyển' : asp.TrangThai}
                                                </span>
                                            </td>
                                        </tr>
                                    ))
                                ) : (
                                    <tr>
                                        <td colSpan="4" style={{ textAlign: 'center', color: 'var(--text-muted)' }}>Không đăng ký nguyện vọng nào</td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                );
            case 'scores':
                return (
                    <div className="student-detail-content-section">
                        {Object.keys(studentDetail.scores || {}).length > 0 ? (
                            Object.entries(studentDetail.scores).map(([examName, subjectsList]) => (
                                <div key={examName} style={{ marginBottom: '24px' }}>
                                    <h4 style={{ marginBottom: '12px', color: 'var(--primary)', textTransform: 'uppercase', fontSize: '0.9rem', letterSpacing: '0.5px' }}>
                                        Kỳ thi: {examName}
                                    </h4>
                                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(140px, 1fr))', gap: '12px' }}>
                                        {subjectsList.map((scoreItem, idx) => (
                                            <div key={idx} style={{ background: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: '8px', padding: '12px', textAlign: 'center' }}>
                                                <div style={{ fontSize: '0.8rem', color: '#64748b', fontWeight: 600 }}>{scoreItem.MaMon}</div>
                                                <div style={{ fontSize: '1.35rem', fontWeight: 700, color: '#1e293b', marginTop: '4px' }}>{scoreItem.Diem ?? 'N/A'}</div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            ))
                        ) : (
                            <p style={{ textAlign: 'center', color: 'var(--text-muted)' }}>Chưa có dữ liệu điểm thi</p>
                        )}
                    </div>
                );
            case 'enrollment':
                return (
                    <div className="student-detail-content-section">
                        <div style={{ background: 'rgba(16, 185, 129, 0.06)', border: '1px solid rgba(16, 185, 129, 0.15)', borderRadius: '12px', padding: '20px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
                            <h4 style={{ color: '#047857', fontSize: '1.1rem', fontWeight: 700 }}>Xác nhận nhập học thành công</h4>
                            <p style={{ fontSize: '0.9rem', color: '#334155' }}>Thí sinh đã xác nhận nhập học chính thức vào hệ thống của nhà trường.</p>
                            <hr style={{ border: 0, borderTop: '1px solid rgba(16, 185, 129, 0.15)' }} />
                            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginTop: '8px', fontSize: '0.9rem' }}>
                                <p><strong>Ngành nhập học (Mã):</strong><br />{studentDetail.enrollment.MaNganh}</p>
                                <p><strong>Mã nhóm xét tuyển:</strong><br />{studentDetail.enrollment.MaNhom}</p>
                                <p><strong>Năm tuyển sinh:</strong><br />{studentDetail.enrollment.NamTuyenSinh}</p>
                                <p><strong>Ngày xác nhận:</strong><br />{studentDetail.enrollment.NgayXacNhan || 'Chưa rõ'}</p>
                            </div>
                        </div>
                    </div>
                );
            default:
                return null;
        }
    };

    return (
        <div className="search-page-container fade-in">
            <h2 className="search-title">Tra cứu Học sinh</h2>
            <p className="search-subtitle">
                Tìm kiếm và xem chi tiết hồ sơ xét tuyển của thí sinh.
            </p>

            {/* Thanh tìm kiếm */}
            <form onSubmit={handleSearch} className="glass-panel search-bar-wrapper">
                <div className="search-input-group">
                    <input 
                        type="text" 
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        placeholder="Nhập mã định danh hoặc tên học sinh..." 
                        className="search-input"
                    />
                    <button type="submit" className="search-btn" disabled={loading}>
                        {loading ? 'Đang tìm...' : 'Tìm kiếm'}
                    </button>
                </div>
            </form>

            {/* Khu vực hiển thị kết quả */}
            {loading && <div className="search-empty-state">Đang truy vấn dữ liệu...</div>}

            {!loading && searched && (
                <div className="search-results-layout">
                    
                    {/* BẢNG DANH SÁCH (Chỉ hiển thị khi CHƯA chọn học sinh) */}
                    {!selectedStudent ? (
                        <div className="glass-panel" style={{ width: '100%', overflow: 'hidden' }}>
                            <h3 style={{ padding: '20px 0 0 20px', fontSize: '1.1rem', color: '#1e293b' }}>
                                Kết quả tìm kiếm ({students.length})
                            </h3>
                            {students.length === 0 ? (
                                <p style={{ padding: '20px', color: 'var(--text-muted)' }}>Không tìm thấy thí sinh nào phù hợp.</p>
                            ) : (
                                <div style={{ overflowX: 'auto', padding: '10px 20px 20px 20px' }}>
                                    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                                        <thead>
                                            <tr style={{ textAlign: 'left', borderBottom: '2px solid #e2e8f0', color: '#475569' }}>
                                                <th style={{ padding: '12px', fontSize: '0.9rem' }}>Mã định danh</th>
                                                <th style={{ padding: '12px', fontSize: '0.9rem' }}>Họ và tên</th>
                                                <th style={{ padding: '12px', fontSize: '0.9rem' }}>Hành động</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {students.map((student) => (
                                                <tr key={student.ma_dinh_danh || student.id} style={{ borderBottom: '1px solid #e2e8f0' }}>
                                                    <td style={{ padding: '12px', fontSize: '0.9rem', color: '#0f172a' }}>{student.ma_dinh_danh}</td>
                                                    <td style={{ padding: '12px', fontSize: '0.9rem', color: '#0f172a', fontWeight: 500 }}>{student.ho_ten}</td>
                                                    <td style={{ padding: '12px' }}>
                                                        <button onClick={() => handleViewDetail(student)} className="search-btn" style={{ padding: '6px 12px', fontSize: '0.85rem' }}>
                                                            Chi tiết
                                                        </button>
                                                    </td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            )}
                        </div>
                    ) : (
                        /* KHUNG CHI TIẾT (Chiếm toàn bộ khi ĐÃ chọn học sinh) */
                        <div className="detail-panel">
                            <button className="close-btn" onClick={() => { setSelectedStudent(null); setStudentDetail(null); }}>
                                ✕ Đóng
                            </button>
                            
                            <h2 style={{ marginBottom: '20px', color: '#1e293b', fontSize: '1.35rem', fontWeight: 700 }}>
                                Chi tiết hồ sơ: {selectedStudent.ho_ten}
                            </h2>
                            
                            {/* Thanh chọn Tab */}
                            {studentDetail && (
                                <div className="student-detail-tabs">
                                    <button 
                                        className={`student-detail-tab-btn ${activeTab === 'profile' ? 'active' : ''}`}
                                        onClick={() => setActiveTab('profile')}
                                    >
                                        Thông tin cá nhân
                                    </button>
                                    <button 
                                        className={`student-detail-tab-btn ${activeTab === 'aspirations' ? 'active' : ''}`}
                                        onClick={() => setActiveTab('aspirations')}
                                    >
                                        Nguyện vọng ({studentDetail.aspirations?.length || 0})
                                    </button>
                                    <button 
                                        className={`student-detail-tab-btn ${activeTab === 'scores' ? 'active' : ''}`}
                                        onClick={() => setActiveTab('scores')}
                                    >
                                        Điểm thi THPT
                                    </button>
                                    {studentDetail.enrollment && (
                                        <button 
                                            className={`student-detail-tab-btn ${activeTab === 'enrollment' ? 'active' : ''}`}
                                            onClick={() => setActiveTab('enrollment')}
                                        >
                                            Nhập học
                                        </button>
                                    )}
                                </div>
                            )}

                            {renderDetailContent()}
                        </div>
                    )}
                </div>
            )}

            {!searched && !loading && (
                <div className="search-empty-state">Vui lòng nhập từ khóa để tiến hành tra cứu dữ liệu.</div>
            )}
        </div>
    );
};

export default StudentSearch;