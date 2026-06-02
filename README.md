## 📁 Project Structure

```text
NEU-Admission-System/
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
├── .gitignore                        
└── README.md                         

---

## ⚙️ Cấu hình kết nối Database (SQL Server)

Backend đọc cấu hình từ file `backend/.env`. Tạo file này nếu chưa có.

Ví dụ `.env`:

```env
DB_SERVER=(localdb)\MSSQLLocalDB
DB_NAME=neu_tuyensinh
DB_DRIVER=ODBC Driver 18 for SQL Server
DB_USER=
DB_PASSWORD=
```

Ghi chú:
- Nếu dùng Windows Authentication (Trusted Connection), để trống `DB_USER` và `DB_PASSWORD`.
- Nếu dùng SQL Login, điền `DB_USER` và `DB_PASSWORD`.
- Cần cài `ODBC Driver 18 for SQL Server` (hoặc đổi `DB_DRIVER` đúng với driver đã cài).

### Khởi tạo database

1. Tạo database `neu_tuyensinh` trên SQL Server.
2. Chạy script tạo bảng: `database/neu_admission.sql`.
3. Chạy script tạo view: `database/vw_phan_tich_tuyensinh.sql`.
4. (Tuỳ chọn) Chạy file `database/DataGenerate.py` để tạo script dữ liệu mẫu.
5. (Tuỳ chọn) Chạy script dữ liệu mẫu: `DuLieuTuyenSinh_SQLServer.sql`.
6. (Tuỳ chọn) Tạo view phân tích: `database/vw_phan_tich_tuyensinh.sql`.

---

## ▶️ Khởi chạy project

### Backend (FastAPI)

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Truy cập API docs: http://127.0.0.1:8000/docs

### Frontend (Vite + React)

```bash
cd frontend
npm install
npm run dev
```

Truy cập giao diện: http://localhost:5173