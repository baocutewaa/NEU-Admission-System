// src/utils/format.js

// Biến 14250 thành 14.250
export const formatNumber = (num) => {
    if (!num) return '0';
    return Number(num).toLocaleString('vi-VN');
};

// Cắt ngắn tên ngành nếu quá dài trên giao diện: "Khoa học máy tính" -> "Khoa học..."
export const truncateString = (str, maxLength = 20) => {
    if (!str || str.length <= maxLength) return str;
    return `${str.substring(0, maxLength)}...`;
};