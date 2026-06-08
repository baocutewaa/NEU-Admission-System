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
│   │   │   ├── config.py             # Đọc file .env (DB URL, Ollama config)
│   │   │   ├── database.py           # Khởi tạo SQLAlchemy Engine kết nối SQL Server
│   │   │   └── security.py           # Quản lý xác thực JWT
│   │   │
│   │   └── main.py                   # Entry point khởi chạy FastAPI Server
│   │
│   ├── venv/                         # Virtual Environment
│   ├── data/                         # Kho lưu trữ tài liệu PDF/Docx + ChromaDB
│   │   ├── chroma_db/                # Vector database (tự tạo khi khởi chạy)
│   │   ├── neu_tuyensinh_schema.md   # Schema database chi tiết
│   │   └── Đề án TSĐH năm 2025.pdf  # Đề án tuyển sinh (tài liệu RAG)
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

## 🤖 Cài đặt Ollama (LLM Local)

Hệ thống sử dụng **Ollama** để chạy mô hình ngôn ngữ lớn (LLM) trực tiếp trên máy tính, hoàn toàn **miễn phí** và **không cần API key**.

### 1. Tải và cài đặt Ollama

Truy cập [https://ollama.com/download](https://ollama.com/download) và tải phiên bản phù hợp:

| Hệ điều hành | Cách cài |
|--------------|----------|
| **Windows**  | Tải file `.exe` → chạy và cài đặt |
| **macOS**    | Tải file `.dmg` hoặc `brew install ollama` |
| **Linux**    | `curl -fsSL https://ollama.ai/install.sh \| sh` |

Sau khi cài, kiểm tra:

```bash
ollama --version
```

### 2. Tải model LLM

Hệ thống mặc định sử dụng `qwen2.5:7b` (4.7GB). Chạy lệnh sau để tải:

```bash
ollama pull qwen2.5:7b
```

**Lưu ý về phần cứng:**

| Cấu hình máy              | Model khuyến nghị                   | RAM tối thiểu |
|---------------------------|-------------------------------------|---------------|
| Có GPU NVIDIA (≥6GB VRAM) | `qwen2.5:7b`                        | 8GB           |
| Chỉ có CPU (≥6 cores)     | `qwen2.5:7b` hoặc `qwen2.5:3b`      | 8GB           |
| Máy yếu (≤4 cores)        | `qwen2.5:3b`                        | 4GB           |

Nếu máy yếu, dùng model nhỏ hơn:

```bash
ollama pull qwen2.5:3b
```

### 3. Khởi động Ollama

Ollama thường tự chạy nền sau khi cài. Kiểm tra bằng:

```bash
ollama list
```

Nếu chưa chạy, khởi động thủ công:

```bash
ollama serve
```

Mặc định Ollama chạy tại `http://localhost:11434`.

### 4. Cấu hình trong `.env`

Thêm các biến sau vào file `backend/.env`:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b
EMBED_MODEL=BAAI/bge-m3
```

> **Lưu ý:** `EMBED_MODEL` là model embedding cho RAG (tự động tải lần đầu chạy, ~2.4GB). Không cần cài qua Ollama.

---

## ⚙️ Cấu hình kết nối Database (SQL Server)

Backend đọc cấu hình từ file `backend/.env`. Tạo file này nếu chưa có.

Ví dụ `.env` đầy đủ:

```env
# Database
DB_SERVER=(localdb)\MSSQLLocalDB
DB_NAME=neu_tuyensinh
DB_DRIVER=ODBC Driver 18 for SQL Server
DB_USER=
DB_PASSWORD=

# Ollama LLM
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b
EMBED_MODEL=BAAI/bge-m3
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

### Yêu cầu hệ thống

- Python 3.10+
- Node.js 18+
- SQL Server (LocalDB hoặc full)
- Ollama (đã cài và pull model)
- RAM ≥ 8GB (khuyến nghị 16GB)

### Backend (FastAPI)

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

> Lần đầu khởi chạy sẽ **tự động tải embedding model** (~2.4GB) và **index tài liệu** vào ChromaDB. Quá trình này mất 2-5 phút.

Truy cập API docs: http://127.0.0.1:8000/docs

### Frontend (Vite + React)

```bash
cd frontend
npm install
npm run dev
```

Truy cập giao diện: http://localhost:5173

---

## 🧪 Kiểm tra AI Chatbot

Sau khi khởi chạy backend, mở Swagger UI tại http://127.0.0.1:8000/docs và test endpoint:

```
POST /api/v1/chat/query
```

Body mẫu:

```json
{
  "question": "tìm ra 10 thí sinh có điểm thi môn toán cao nhất"
}
```

Response sẽ trả về `answer` (câu trả lời), `sql` (câu SQL đã chạy), `columns`/`rows` (dữ liệu bảng).