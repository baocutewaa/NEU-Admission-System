// src/utils/storage.js
export const getLocalData = (key, defaultValue = null) => {
    try {
        const item = window.localStorage.getItem(key);
        return item ? JSON.parse(item) : defaultValue;
    } catch {
        return defaultValue;
    }
};

export const setLocalData = (key, value) => {
    try {
        window.localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
        console.error("Lỗi ghi localStorage", error);
    }
};