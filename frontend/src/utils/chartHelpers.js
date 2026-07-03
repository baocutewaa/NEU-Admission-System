
/**
 * Đảo ngược mảng để khớp thứ tự hiển thị trục Y của ECharts (từ dưới lên)
 */
export const reverseDataArray = (arr, key) => {
    if (!arr) return [];
    return arr.map(item => item[key]).reverse();
};

/**
 * Lấy số lượng thí sinh theo dải điểm (bracket) của một môn học
 */
export const getCountByBracket = (brackets, bracketKey) => {
    if (!brackets) return 0;
    const target = brackets.find(b => b.bracket === bracketKey);
    return target ? target.count : 0;
};
