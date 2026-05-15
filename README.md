enroll-insight-neu/
├── frontend/                         # React (Vite + TailwindCSS)
│
│
│
├── backend/                          # FastAPI
│   ├── app/
│   │   ├── api/                      # API
│   │   │   ├── v1/
│   │   │   │   ├── endpoints/
│   │   │   │   │   ├── students.py   # API tra cứu hồ sơ, điểm thi thí sinh
│   │   │   │   │   ├── analytics.py  # API trả về data thống kê (tỉ lệ đỗ, vùng miền)
│   │   │   │   │   └── ai_chat.py    # Endpoint xử lý hội thoại AI (RAG & Text-to-SQL)
│   │   │   │   └── api_router.py     # Tập hợp các router con thành một mối
│   │   │   └── deps.py               # Dependency Injection (ví dụ: get_db_session)
│   │   │
│   │   ├── crud/                     # Truy vấn dữ liệu từ database
│   │   │   ├── base.py               # Chứa các hàm CRUD tổng quát (get, create, update, delete)
│   │   │   ├── crud_student.py       # Truy vấn dữ liệu từ bảng thisinh, lien_he, diem_thi
│   │   │   ├── crud_admission.py     # Truy vấn bảng nganh, nguyen_vong, ho_so_nhap_hoc
│   │   │   └── crud_analytics.py     # Các câu lệnh aggregation phức tạp cho Dashboard
│   │   │
│   │   ├── services/                 # Core logic
│   │   │   ├── admission_service.py  # Tính toán điểm quy đổi, logic xét tuyển thông minh
│   │   │   ├── ai_agent.py           # Router điều hướng câu hỏi người dùng (vào RAG hay SQL)
│   │   │   ├── rag_engine/           # Xử lý RAG: Search trong PDF quy chế tuyển sinh
│   │   │   │   ├── vector_store.py   # Kết nối Vector DB (ChromaDB/FAISS)
│   │   │   │   └── retriever.py      # Tìm kiếm ngữ cảnh văn bản phù hợp
│   │   │   └── sql_engine/           # Xử lý Text-to-SQL: Chuyển câu hỏi thành T-SQL
│   │   │       ├── prompt_factory.py # Quản lý system prompts & database schema context
│   │   │       └── sql_executor.py   # Thực thi SQL an toàn (Chế độ Read-only)
│   │   │
│   │   ├── models/                   # SQLAlchemy Models
│   │   │   ├── base.py               # Base class cho tất cả các Model
│   │   │   ├── student.py            # Mapping bảng thisinh, diem_thi, chung_chi
│   │   │   └── admission.py          # Mapping bảng nganh, nguyen_vong, vung_dia_ly
│   │   │
│   │   ├── schemas/                  # Pydantic Models
│   │   │   ├── student_schema.py     # Kiểm tra dữ liệu thí sinh gửi lên/trả về
│   │   │   ├── chat_schema.py        # Định dạng tin nhắn chat của người dùng/AI
│   │   │   └── analytics_schema.py   # Cấu trúc dữ liệu cho các biểu đồ thống kê
│   │   │
│   │   ├── core/                     # Settings
│   │   │   ├── config.py             # Đọc file .env (DB URL, OpenAI/Gemini API Keys)
│   │   │   ├── database.py           # Khởi tạo SQLAlchemy Engine kết nối SQL Server
│   │   │   └── security.py           # Quản lý xác thực JWT
│   │   │
│   │   └── main.py                   # Entry point khởi chạy FastAPI Server
│   │
│   ├── venv/                         # Virtual Environment
│   ├── data_sources/                 # Kho lưu trữ tài liệu PDF/Docx quy chế tuyển sinh
│   ├── .env                          # Biến môi trường quan trọng
│   └── requirements.txt              # Danh sách các thư viện Python cần thiết
│
├── database/                         # Quản lý hạ tầng Dữ liệu
│   ├── migrations/                   # Các bản ghi thay đổi cấu trúc DB (Alembic)
│   └── neu_admission.sql             # Script T-SQL gốc tạo cấu trúc bảng
│
├── .gitignore                        # Cấu hình bỏ qua các file rác, venv, .env khi push Git
└── README.md                         # Tài liệu hướng dẫn cài đặt và mô tả dự án
