import { useState, useEffect } from 'react';
import Navbar from './components/common/Navbar';
import Sidebar from './components/common/Sidebar';
import Dashboard from './pages/Dashboard';
import ChatBot from './pages/ChatBot';          
import StudentSearch from './pages/StudentSearch'; 
import { fetchMethods, fetchMajors } from './services/api';
import { getLocalData, setLocalData } from './utils/storage';

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard');
  
  // Rút gọn việc đọc khởi tạo an toàn từ LocalStorage bằng utils/storage
  const [year, setYear] = useState(() => getLocalData('selected_year', 2024));
  
  const [methodFilter, setMethodFilter] = useState('');
  const [majorFilter, setMajorFilter] = useState('');
  const [filterOptions, setFilterOptions] = useState({ methods: [], majors: [] });

  useEffect(() => {
    // Tự động đồng bộ hóa ghi data an toàn vào LocalStorage bằng utils/storage
    setLocalData('selected_year', year);

    const loadFilterData = async () => {
      try {
        const [methodsRes, majorsRes] = await Promise.all([
          fetchMethods(year),
          fetchMajors(year)
        ]);

        const sanitizeData = (res, keyName) => {
          if (!res || !Array.isArray(res)) return [];
          return res.map(item => {
            if (typeof item === 'string') return { [keyName]: item };
            return item;
          });
        };

        setFilterOptions({
          methods: sanitizeData(methodsRes, 'method_name'),
          majors: sanitizeData(majorsRes, 'major_name')
        });
      } catch (err) {
        console.error("Không thể lấy danh mục bộ lọc cho Navbar:", err);
      }
    };
    loadFilterData();
  }, [year]);

  const renderPageContent = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard year={year} methodFilter={methodFilter} majorFilter={majorFilter} />;
      case 'chatbot':
        return <ChatBot />;
      case 'search':
        return <StudentSearch />;
      default:
        return <Dashboard year={year} methodFilter={methodFilter} majorFilter={majorFilter} />;
    }
  };

  return (
    <div className="app-container">
      <Navbar 
        currentPage={currentPage}
        year={year} setYear={setYear}
        methodFilter={methodFilter} setMethodFilter={setMethodFilter}
        majorFilter={majorFilter} setMajorFilter={setMajorFilter}
        methodsData={filterOptions.methods}
        majorsData={filterOptions.majors}
      />

      <div style={{ display: 'flex', flex: 1, position: 'relative' }}>
        <Sidebar currentPage={currentPage} setCurrentPage={setCurrentPage} />
        <main className="main-content">
          {renderPageContent()}
        </main>
      </div>
    </div>
  );
}

export default App;