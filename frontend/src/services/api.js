import axios from 'axios';

// Đảm bảo FastAPI đang chạy trên port 8000
const API_BASE_URL = 'http://localhost:8000/api/v1/analytics';
const CHAT_API_URL = 'http://localhost:8000/api/v1/chat';
const STUDENT_API_URL = 'http://localhost:8000/api/v1/students';

// Hàm helper để chuẩn hóa bộ lọc, tránh gửi chuỗi "Tất cả..." hoặc Object lên backend
const cleanFilterValue = (value, keyName) => {
    if (!value) return null;
    const actualValue = typeof value === 'object' ? value[keyName] : value;
    if (!actualValue || actualValue.includes('Tất cả') || actualValue === '') {
        return null;
    }
    return actualValue;
};

// ĐÃ CẬP NHẬT: Không gán mặc định = 2024 để bắt buộc Component truyền State năm hiện tại từ UI xuống
export const fetchOverview = async (year) => {
    const response = await axios.get(`${API_BASE_URL}/overview?nam_tuyen_sinh=${year}`);
    return response.data;
};

export const fetchRegions = async (year) => {
    const response = await axios.get(`${API_BASE_URL}/regions?nam_tuyen_sinh=${year}`);
    return response.data;
};

// ==========================================
// ĐÃ SỬA LỖI ĐỒNG BỘ: Dùng Adapter Pattern để map dữ liệu DB sang UI
// ==========================================
export const fetchMajors = async (year) => {
    const response = await axios.get(`${API_BASE_URL}/majors?nam_tuyen_sinh=${year}`);
    return response.data.map(item => ({
        ...item,
        major_id: item.MaNganh || item.major_id,
        major_name: item.TenNganh || item.major_name
    }));
};

export const fetchMethods = async (year) => {
    const response = await axios.get(`${API_BASE_URL}/methods?nam_tuyen_sinh=${year}`);
    return response.data.map(item => ({
        ...item,
        method_id: item.MaPhuongThuc || item.method_id,
        method_name: item.TenPhuongThuc || item.method_name
    }));
};
// ==========================================

export const fetchMotivation = async (year) => {
    const response = await axios.get(`${API_BASE_URL}/motivation?nam_tuyen_sinh=${year}`);
    return response.data;
};

export const fetchClustering = async (year, limit = 10) => {
    const response = await axios.get(`${API_BASE_URL}/clustering?nam_tuyen_sinh=${year}&limit=${limit}`);
    return response.data;
};

export const fetchPreferenceMultivariate = async (year) => {
    const response = await axios.get(`${API_BASE_URL}/preference-multivariate?nam_tuyen_sinh=${year}`);
    return response.data;
};

export const fetchGenderDistribution = async (year, method = null) => {
    let url = `${API_BASE_URL}/gender-distribution?nam_tuyen_sinh=${year}`;
    const cleanMethod = cleanFilterValue(method, 'method_name');
    if (cleanMethod) url += `&phuong_thuc=${encodeURIComponent(cleanMethod)}`;
    
    const response = await axios.get(url);
    return response.data;
};

export const fetchGeographicEnrollment = async (year, method = null, major = null) => {
    let url = `${API_BASE_URL}/geographic-enrollment?nam_tuyen_sinh=${year}`;
    const cleanMethod = cleanFilterValue(method, 'method_name');
    const cleanMajor = cleanFilterValue(major, 'major_name');
    
    if (cleanMethod) url += `&phuong_thuc=${encodeURIComponent(cleanMethod)}`;
    if (cleanMajor) url += `&major_name=${encodeURIComponent(cleanMajor)}`;
    
    const response = await axios.get(url);
    
    // ÁP DỤNG ADAPTER PATTERN: Đảm bảo dữ liệu map chuẩn 100% thuộc tính giao diện cần
    return (response.data || []).map(item => ({
        province: item.province || item.TinhThanh || item.TenTinh || "",
        yield_rate: item.yield_rate ?? item.TiLeNhapHoc ?? item.tile_nhap_hoc ?? 0,
        total_applicants: item.total_applicants ?? item.TongDangKy ?? item.so_luong_dang_ky ?? 0,
        admitted_applicants: item.admitted_applicants ?? item.SoLuongTrungTuyen ?? item.so_luong_trung_tuyen ?? 0,
        enrolled_applicants: item.enrolled_applicants ?? item.SoLuongNhapHoc ?? item.so_luong_nhap_hoc ?? 0
    }));
};

export const fetchScoreAnalytics = async (year, method = null, major = null) => {
    let url = `${API_BASE_URL}/score-analytics?nam_tuyen_sinh=${year}`;
    const cleanMethod = cleanFilterValue(method, 'method_name');
    const cleanMajor = cleanFilterValue(major, 'major_name');
    
    if (cleanMethod) url += `&phuong_thuc=${encodeURIComponent(cleanMethod)}`;
    if (cleanMajor) url += `&major_name=${encodeURIComponent(cleanMajor)}`;
    
    const response = await axios.get(url);
    return response.data;
};

// ==========================================
// CÁC HÀM API KHÁC (ĐÃ CẬP NHẬT BẢO MẬT & ĐỒNG BỘ)
// ==========================================

export const searchStudentApi = async (searchQuery) => {
    try {
        const response = await axios.get(`${STUDENT_API_URL}/search?q=${encodeURIComponent(searchQuery)}`);
        
        // Bọc lót Adapter Pattern ở đây để tránh lỗi trống dữ liệu trên hàng hiển thị
        return response.data.map(item => ({
            ...item,
            cccd: item.CCCD || item.cccd,
            ma_dinh_danh: item.CCCD || item.cccd || item.ma_dinh_danh,
            ho_ten: item.HoTen || item.ho_ten || item.fullName,
            hoTen: item.HoTen || item.ho_ten
        }));
    } catch (error) {
        console.error("Lỗi hệ thống khi tìm kiếm học sinh:", error);
        return [];
    }
};

export const askChatbotApi = async (query) => {
    // ĐÃ SỬA: Đổi từ { message: query } thành { question: query } 
    // để khớp hoàn toàn với Class ChatRequest(BaseModel) ở FastAPI Backend
    const response = await axios.post(`${CHAT_API_URL}/query`, { question: query });
    return response.data;
};