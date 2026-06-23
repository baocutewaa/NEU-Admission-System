import { useState, useEffect, useRef } from 'react';

const Navbar = ({ 
    year, setYear, 
    methodFilter, setMethodFilter, 
    majorFilter, setMajorFilter
}) => {
    // Trạng thái quản lý menu nào đang mở: null, 'method', 'major', hoặc 'year'
    const [openMenu, setOpenMenu] = useState(null);
    const navbarRef = useRef(null);

    // Tự động đóng menu khi click ra ngoài vùng bộ lọc
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (navbarRef.current && !navbarRef.current.contains(event.target)) {
                setOpenMenu(null);
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    const toggleMenu = (menuName) => {
        setOpenMenu(openMenu === menuName ? null : menuName);
    };

    return (
        <header className="neu-navbar" ref={navbarRef}>
            {/* Tiêu đề ứng dụng bên trái */}
            <div className="neu-navbar-brand">
                <span className="neu-navbar-title">
                    NEU Admission System
                </span>
            </div>

            {/* Khối các bộ lọc nằm ở giữa Navbar */}
            <div className="neu-filter-container">
                
                {/* 1. Bộ lọc Phương thức */}
                <div className="neu-filter-group">
                    <label className="neu-filter-label">Chương trình đào tạo</label>
                    <div className="neu-select-wrapper-box">
                        <div 
                            className="neu-select-custom"
                            onClick={() => toggleMenu('method')}
                        >
                            {methodFilter || "Tất cả Phương thức"}
                        </div>
                        <span className={`neu-select-arrow-icon ${openMenu === 'method' ? 'rotated' : ''}`}>▼</span>
                        
                        {/* Danh sách xổ xuống được custom hoàn toàn */}
                        {openMenu === 'method' && (
                            <ul className="neu-dropdown-menu">
                                <li 
                                    className="neu-dropdown-item"
                                    onClick={() => { setMethodFilter(""); setOpenMenu(null); }}
                                >
                                    Tất cả Phương thức
                                </li>
                            
                            </ul>
                        )}
                    </div>
                </div>

                {/* 2. Bộ lọc Ngành */}
                <div className="neu-filter-group" style={{ minWidth: '230px' }}>
                    <label className="neu-filter-label">Ngành học</label>
                    <div className="neu-select-wrapper-box">
                        <div 
                            className="neu-select-custom"
                            onClick={() => toggleMenu('major')}
                        >
                            {majorFilter || "Tất cả Ngành"}
                        </div>
                        <span className={`neu-select-arrow-icon ${openMenu === 'major' ? 'rotated' : ''}`}>▼</span>
                        
                        {openMenu === 'major' && (
                            <ul className="neu-dropdown-menu">
                                <li 
                                    className="neu-dropdown-item"
                                    onClick={() => { setMajorFilter(""); setOpenMenu(null); }}
                                >
                                    Tất cả Ngành
                                </li>
                            </ul>
                        )}
                    </div>
                </div>

                {/* 3. Bộ lọc Năm học */}
                <div className="neu-filter-group" style={{ minWidth: '140px' }}>
                    <label className="neu-filter-label">Năm học</label>
                    <div className="neu-select-wrapper-box">
                        <div 
                            className="neu-select-custom"
                            onClick={() => toggleMenu('year')}
                        >
                            Năm {year}
                        </div>
                        <span className={`neu-select-arrow-icon ${openMenu === 'year' ? 'rotated' : ''}`}>▼</span>
                        
                        {openMenu === 'year' && (
                            <ul className="neu-dropdown-menu">
                                {[2024].map((y) => (
                                    <li 
                                        key={y}
                                        className="neu-dropdown-item" 
                                        onClick={() => { 
                                            if (year !== y) {
                                                setYear(y); 
                                                // Tự động reset các bộ lọc phụ khi đổi năm
                                                setMajorFilter(""); 
                                                setMethodFilter("");
                                            }
                                            setOpenMenu(null); 
                                        }}
                                    >
                                        Năm {y}
                                    </li>
                                ))}
                            </ul>
                        )}
                    </div>
                </div>
            </div>

            {/* Vùng bên phải trống */}
            <div style={{ width: '0px' }}></div>
        </header>
    );
};

export default Navbar;