import { useState } from 'react';
import { searchStudentApi } from '../services/api';

const StudentSearch = () => {
    const [query, setQuery] = useState('');
    const [students, setStudents] = useState([]);
    const [loading, setLoading] = useState(false);
    const [searched, setSearched] = useState(false);
    const [selectedStudent, setSelectedStudent] = useState(null);

    const handleSearch = async (e) => {
        if (e) e.preventDefault();
        if (!query.trim()) return;

        setLoading(true);
        setSearched(true);
        setSelectedStudent(null);
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
                        <div className="glass-panel" style={{ width: '100%' }}>
                            <h3 style={{ padding: '10px 0 0 20px' }}>Kết quả tìm kiếm ({students.length})</h3>
                            {students.length === 0 ? (
                                <p style={{ marginTop: '10px' }}>Không tìm thấy thí sinh nào phù hợp.</p>
                            ) : (
                                <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '10px' }}>
                                    <thead>
                                        <tr style={{ textAlign: 'left', borderBottom: '1px solid #334155' }}>
                                            <th style={{ padding: '12px' }}>Mã định danh</th>
                                            <th style={{ padding: '12px' }}>Họ và tên</th>
                                            <th style={{ padding: '12px' }}>Hành động</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {students.map((student) => (
                                            <tr key={student.ma_dinh_danh || student.id} style={{ borderBottom: '1px solid #1e293b' }}>
                                                <td style={{ padding: '12px' }}>{student.ma_dinh_danh}</td>
                                                <td style={{ padding: '12px' }}>{student.ho_ten}</td>
                                                <td style={{ padding: '12px' }}>
                                                    <button onClick={() => setSelectedStudent(student)} className="search-btn" style={{ padding: '6px 12px' }}>
                                                        Chi tiết
                                                    </button>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            )}
                        </div>
                    ) : (
                        /* KHUNG CHI TIẾT (Chiếm toàn bộ khi ĐÃ chọn học sinh) */
                        <div className="detail-panel">
                            <button className="close-btn" onClick={() => setSelectedStudent(null)}>
                                ✕ Đóng
                            </button>
                            
                            <h2 style={{ marginBottom: '20px', color: '#1e293b' }}>Chi tiết hồ sơ</h2>
                            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '25px' }}>
                                <p><strong>Họ tên:</strong><br />{selectedStudent.ho_ten}</p>
                                <p><strong>Mã định danh:</strong><br />{selectedStudent.ma_dinh_danh}</p>
                                <p><strong>Giới tính:</strong><br />{selectedStudent.gioi_tinh}</p>
                                <p><strong>Phương thức:</strong><br />{selectedStudent.phuong_thuc}</p>
                                <p><strong>Ngành:</strong><br />{selectedStudent.major_name || selectedStudent.nganh_trung_tuyen}</p>
                                <p><strong>Điểm xét tuyển:</strong><br />{selectedStudent.diem_xet_tuyen}</p>
                                <p><strong>Trạng thái:</strong><br />
                                    <span style={{ color: selectedStudent.trang_thai === 'Trúng tuyển' ? '#10b981' : '#f59e0b' }}>
                                        {selectedStudent.trang_thai}
                                    </span>
                                </p>
                            </div>
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