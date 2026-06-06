import axios from 'axios';

// Ensure the FastAPI backend is running on port 8000
const API_BASE_URL = 'http://localhost:8000/api/v1/analytics';

export const fetchOverview = async (year = 2024) => {
    const response = await axios.get(`${API_BASE_URL}/overview?nam_tuyen_sinh=${year}`);
    return response.data;
};

export const fetchRegions = async (year = 2024) => {
    const response = await axios.get(`${API_BASE_URL}/regions?nam_tuyen_sinh=${year}`);
    return response.data;
};

export const fetchMajors = async (year = 2024) => {
    const response = await axios.get(`${API_BASE_URL}/majors?nam_tuyen_sinh=${year}`);
    return response.data;
};

export const fetchMethods = async (year = 2024) => {
    const response = await axios.get(`${API_BASE_URL}/methods?nam_tuyen_sinh=${year}`);
    return response.data;
};

export const fetchMotivation = async (year = 2024) => {
    const response = await axios.get(`${API_BASE_URL}/motivation?nam_tuyen_sinh=${year}`);
    return response.data;
};

export const fetchClustering = async (year = 2024, limit = 10) => {
    const response = await axios.get(`${API_BASE_URL}/clustering?nam_tuyen_sinh=${year}&limit=${limit}`);
    return response.data;
};

export const fetchPreferenceMultivariate = async (year = 2024) => {
    const response = await axios.get(`${API_BASE_URL}/preference-multivariate?nam_tuyen_sinh=${year}`);
    return response.data;
};

export const fetchGenderDistribution = async (year = 2024, method = null) => {
    let url = `${API_BASE_URL}/gender-distribution?nam_tuyen_sinh=${year}`;
    if (method) url += `&phuong_thuc=${encodeURIComponent(method)}`;
    const response = await axios.get(url);
    return response.data;
};

export const fetchGeographicEnrollment = async (year = 2024, method = null, major = null) => {
    let url = `${API_BASE_URL}/geographic-enrollment?nam_tuyen_sinh=${year}`;
    if (method) url += `&phuong_thuc=${encodeURIComponent(method)}`;
    if (major) url += `&major_name=${encodeURIComponent(major)}`;
    const response = await axios.get(url);
    return response.data;
};

export const fetchScoreAnalytics = async (year = 2024, method = null, major = null) => {
    let url = `${API_BASE_URL}/score-analytics?nam_tuyen_sinh=${year}`;
    if (method) url += `&phuong_thuc=${encodeURIComponent(method)}`;
    if (major) url += `&major_name=${encodeURIComponent(major)}`;
    const response = await axios.get(url);
    return response.data;
};
