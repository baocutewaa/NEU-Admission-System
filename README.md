# 🎓 NEU Admission System - Hệ thống Phân tích & Hỗ trợ Tuyển sinh Đại học Kinh tế Quốc dân

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React%2019-61DAFB?style=flat-square&logo=react)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Build-Vite%206-646CFF?style=flat-square&logo=vite)](https://vitejs.dev/)
[![SQL Server](https://img.shields.io/badge/Database-SQL%20Server-CC292B?style=flat-square&logo=microsoftsqlserver)](https://www.microsoft.com/sql-server)
[![Ollama](https://img.shields.io/badge/LLM-Ollama%20%28Qwen2.5%29-000000?style=flat-square&logo=ollama)](https://ollama.com/)
[![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-FF6F00?style=flat-square)](https://www.trychroma.com/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python)](https://www.python.org/)

Hệ thống Phân tích Đa chiều & Hỗ trợ Tuyển sinh dành cho **Trường Đại học Kinh tế Quốc dân (NEU)**. Dự án kết hợp giữa Dashboard thống kê trực quan tương tác và Trợ lý AI thông minh tích hợp công nghệ **Text-to-SQL** & **RAG (Retrieval-Augmented Generation)** chạy hoàn toàn cục bộ (Local LLM), đảm bảo tính bảo mật và chính xác cao trong truy vấn dữ liệu tuyển sinh.

---

## 📖 Công nghệ trong Dự án

- 🤖 **Trợ lý AI Text-to-SQL + RAG**: Cho phép người dùng đặt câu hỏi bằng tiếng Việt tự nhiên (VD: *"Liệt kê 10 thí sinh có điểm toán cao nhất trúng tuyển ngành QTKD năm 2024"*), tự động chuyển thành câu lệnh T-SQL chuẩn xác và trả về bảng dữ liệu + câu trả lời chi tiết.
- 🔄 **Cơ chế Self-Correction & Security**: Tự động phát hiện và sửa lỗi cú pháp SQL Server, bảo vệ dữ liệu bằng cơ chế Read-Only Query Executor (ngăn chặn thao tác xóa/sửa dữ liệu).
- 📊 **Dashboard Thống kê Trực quan**: Biểu đồ phân bố địa lý (Geo Heatmap), Boxplot phân bố điểm thi, tỉ lệ giới tính, thống kê nguyện vọng & tỉ lệ nhập học (Yield Rate).
- 🔍 **Tra cứu Hồ sơ Thí sinh**: Tìm kiếm toàn bộ lịch sử điểm thi, chứng chỉ quốc tế (IELTS, TOEFL,...), danh sách nguyện vọng và kết quả nhập học theo CCCD.


### 🧠 Luồng xử lý AI Chatbot (Agent Flow):
1. **Tiếp nhận câu hỏi**: Người dùng gửi câu hỏi tiếng Việt từ Frontend.
2. **Context Retrieval (RAG)**: Truy vấn thông tin cấu trúc bảng (Schema Index), các câu ví dụ mẫu (Examples Index) và tài liệu quy chế tuyển sinh (Docs Index) từ ChromaDB bằng model embedding `BAAI/bge-m3`.
3. **Sinh truy vấn SQL (Text-to-SQL)**: Ollama (Qwen2.5) nhận prompt kèm ngữ cảnh và tạo ra câu lệnh SQL Server (T-SQL).
4. **Thực thi an toàn (Safe Execution)**: `sql_executor` kiểm tra tính hợp lệ (chỉ chấp nhận lệnh `SELECT`/`WITH`), thực thi trên SQL Server và kiểm tra lỗi. Nếu phát hiện lỗi, kích hoạt vòng lặp **Self-Correction**.
5. **Tổng hợp đáp án**: LLM nhận kết quả trả về từ database và biên soạn câu trả lời ngôn ngữ tự nhiên thân thiện kèm dữ liệu bảng.

---

## 📁 Cấu trúc Thư mục Dự án

```text
NEU-Admission-System/
├── frontend/                         # Giao diện người dùng (React 19 + Vite)
│   ├── src/
│   │   ├── components/               # Biểu đồ ECharts (GeoHeatmap, ScoreBoxplot, GenderAnalytics)
│   │   ├── services/                 # API client kết nối Backend (Axios)
│   │   ├── App.jsx                   # Component giao diện chính (Tabs, Navigation)
│   │   └── index.css                 # Style hệ thống & Design Tokens
│   ├── package.json                  # Dependencies Frontend
│   └── vite.config.js                # Cấu hình Vite
├── frontend/                         # React (Vite + TailwindCSS)
│   ├── node_modules/
│   ├── public/
│   │   └── vietnam.json
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   │   ├── charts/
│   │   │   │   ├── GenderAnalyticsChart.jsx
│   │   │   │   ├── GeoHeatmapChart.jsx
│   │   │   │   └── ScoreBoxplotChart.jsx
│   │   │   └── common/
│   │   │       ├── Navbar.jsx
│   │   │       └── Sidebar.jsx
│   │   ├── pages/
│   │   │   ├── ChatBot.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   └── StudentSearch.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── styles/
│   │   │   ├── App.css
│   │   │   └── index.css
│   │   ├── utils/
│   │   │   ├── chartHelpers.js
│   │   │   ├── format.js
│   │   │   └── storage.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── .gitignore
│   ├── eslint.config.js
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   ├── README.md
│   └── vite.config.js
│
│
├── backend/                          # FastAPI Server & AI Services
│   ├── app/
│   │   ├── api/                      # API Endpoints (v1)
│   │   │   ├── v1/
│   │   │   │   ├── endpoints/
│   │   │   │   │   ├── analytics.py   # API Thống kê & Phân tích tuyển sinh
│   │   │   │   │   ├── students.py    # API Tra cứu hồ sơ thí sinh
│   │   │   │   │   └── ai_chat.py     # API Trợ lý AI Chatbot
│   │   │   │   └── api_router.py      # Gom nhóm các router API
│   │   │   └── deps.py               # Dependency Injection (Database Session)
│   │   │
│   │   ├── crud/                     # Tầng xử lý truy vấn DB (CRUD & Aggregations)
│   │   ├── services/                 # Core Business & AI Logic
│   │   │   ├── ai_agent.py           # Orchestrator chính của AI Agent
│   │   │   ├── rag_engine/           # Vector Store (ChromaDB) & Retriever
│   │   │   │   ├── vector_store.py   # Khởi tạo & lưu vết embeddings
│   │   │   │   └── retriever.py      # Tìm kiếm ngữ cảnh phù hợp
│   │   │   └── sql_engine/           # Text-to-SQL Engine
│   │   │       ├── prompt_factory.py # Quản lý System Prompts & Context
│   │   │       └── sql_executor.py   # Thực thi SQL an toàn (Read-Only)
│   │   │
│   │   ├── models/                   # SQLAlchemy Models (ThiSinh, Nganh, NguyenVong,...)
│   │   ├── schemas/                  # Pydantic Schemas (Request/Response Models)
│   │   ├── core/                     # Configuration & Kết nối Database
│   │   └── main.py                   # Entrypoint khởi chạy FastAPI App
│   │
│   ├── data/                         # Lưu trữ ChromaDB & Tài liệu Tuyển sinh PDF/MD
│   │   ├── chroma_db/                # Chứa Vector DB đã index
│   │   └── Đề án TSĐH năm 2025.pdf  # Tài liệu quy chế tuyển sinh cho RAG
│   ├── .env                          # Biến môi trường
│   └── requirements.txt              # Thư viện Python phụ thuộc
│
├── database/                         # Hạ tầng Dữ liệu (SQL Server)
│   ├── neu_admission.sql             # Script tạo cấu trúc Bảng (Schema DDL)
│   ├── vw_phan_tich_tuyensinh.sql    # Script tạo các SQL View thống kê
│   ├── DataGenerate.py               # Script sinh dữ liệu giả lập (Mock data)
│   └── DuLieuTuyenSinh_SQLServer.sql # File Insert dữ liệu mẫu sẵn có
│
└── README.md                         # Tài liệu hướng dẫn dự án
```

---

## 🤖 Khởi chạy LLM Local với Ollama

Hệ thống sử dụng **Ollama** để vận hành Mô hình Ngôn ngữ Lớn (LLM) nội bộ, hoàn toàn **bảo mật, miễn phí** và **không cần API Key ngoài**.

### 1. Cài đặt Ollama
Tải và cài đặt Ollama từ [https://ollama.com/download](https://ollama.com/download):
- **Windows**: Chạy file `.exe` cài đặt trực tiếp.
- **macOS**: Tải `.dmg` hoặc chạy `brew install ollama`.
- **Linux**: `curl -fsSL https://ollama.ai/install.sh | sh`

Kiểm tra phiên bản sau khi cài:
```bash
ollama --version
```

### 2. Tải Mô hình LLM (Qwen2.5)
Mặc định hệ thống sử dụng model `qwen2.5:7b` (dung lượng ~4.7GB):
```bash
ollama pull qwen2.5:7b
```

#### 💡 Khuyến nghị cấu hình phần cứng:

| Cấu hình Phần cứng          | Mô hình Khuyến nghị | RAM / VRAM Tối thiểu | Ghi chú & Hiệu năng                            |
| :-------------------------- | :------------------ | :------------------- | :--------------------------------------------- |
| **GPU NVIDIA** (≥ 6GB VRAM) | `qwen2.5:7b`        | 8GB RAM + 6GB VRAM   | ⚡ Khuyên dùng: Phản hồi nhanh nhất (~1–3s)     |
| **CPU Đa nhân** (≥ 6 Cores) | `qwen2.5:7b`        | 16GB RAM             | 🔄 Chạy chế độ CPU với 10 threads (~4–8s)      |
| **Máy yếu / Laptop VP**     | `qwen2.5:3b`        | 8GB RAM              | 🍃 Model nhẹ, đáp ứng tốt phần cứng phổ thông  |

Nếu sử dụng máy cấu hình khiêm tốn, bạn có thể tải model nhỏ hơn:
```bash
ollama pull qwen2.5:3b
```
*(Nếu đổi model, nhớ cập nhật biến `OLLAMA_MODEL=qwen2.5:3b` trong file `backend/.env`)*.

---

## ⚙️ Cấu hình Database & Biến Môi trường

### 1. Chuẩn bị Database SQL Server
1. Mở SQL Server Management Studio (SSMS) hoặc VS Code Database Extension.
2. Tạo database mới tên: `neu_tuyensinh`.
3. Chạy script tạo bảng từ file: `database/neu_admission.sql`.
4. Chạy script tạo view thống kê: `database/vw_phan_tich_tuyensinh.sql`.
5. Nạp dữ liệu mẫu: Chạy file `database/DuLieuTuyenSinh_SQLServer.sql` (hoặc chạy `python database/DataGenerate.py` để tự sinh thêm dữ liệu mới).

### 2. Cấu hình File `backend/.env`
Tạo file `backend/.env` với nội dung cấu hình sau:

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

Thêm các biến sau vào file `backend/.env.example`:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b
EMBED_MODEL=BAAI/bge-m3
```

> **Lưu ý:** `EMBED_MODEL` là model embedding cho RAG (tự động tải lần đầu chạy, ~2.4GB). Không cần cài qua Ollama.

---

## ⚙️ Cấu hình kết nối Database (SQL Server)

Backend đọc cấu hình từ file `backend/.env.example`. Tạo file này nếu chưa có.

Ví dụ `.env` đầy đủ:

```env
# Database Settings (SQL Server)
DB_SERVER=(localdb)\MSSQLLocalDB
DB_NAME=neu_tuyensinh
DB_DRIVER=ODBC Driver 18 for SQL Server
DB_USER=
DB_PASSWORD=

# Ollama LLM Settings
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b

# Embedding Model Settings (Dùng cho RAG)
EMBED_MODEL=BAAI/bge-m3
CHROMA_PERSIST_DIR=./data/chroma_db
```

> **📌 Lưu ý về Database Auth:**
> - Nếu sử dụng **Windows Authentication**, hãy để trống `DB_USER` và `DB_PASSWORD`.
> - Nếu sử dụng **SQL Server Authentication**, nhập tài khoản SQL vào `DB_USER` và `DB_PASSWORD`.
> - Hãy đảm bảo máy tính đã cài đặt **ODBC Driver 18 for SQL Server** (hoặc tùy chỉnh `DB_DRIVER` tương ứng với bản ODBC Driver trên máy).

---

## ▶️ Hướng dẫn Khởi chạy Dự án

### Yêu cầu Tiền đề (Prerequisites)
- **Python**: `3.10` trở lên
- **Node.js**: `18.x` hoặc `20.x` trở lên
- **Database**: SQL Server (LocalDB, Express, hoặc Enterprise)
- **Ollama**: Đã khởi chạy dịch vụ Ollama (`ollama serve`) và pull model.

---

### Bước 1: Khởi chạy Backend (FastAPI)

1. Di chuyển vào thư mục `backend`:
   ```bash
   cd backend
   ```

2. Tạo và kích hoạt môi trường ảo Python:
   - **Windows (PowerShell/CMD)**:
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - **Linux / macOS**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. Cài đặt các thư viện phụ thuộc:
   ```bash
   pip install -r requirements.txt
   ```

4. Khởi chạy ứng dụng FastAPI Server:
   ```bash
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

   > ⚡ **Lưu ý trong lần chạy đầu tiên**: Backend sẽ tự động tải HuggingFace Embedding Model (`BAAI/bge-m3` ~2.4GB) và tiến hành index tài liệu Đề án tuyển sinh cùng cấu trúc DB vào ChromaDB. Quá trình này diễn ra khoảng 1 - 3 phút.

5. Kiểm tra API Documentation (Swagger UI):
   Open browser: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### Bước 2: Khởi chạy Frontend (React + Vite)

1. Mở cửa sổ Terminal mới và di chuyển vào thư mục `frontend`:
   ```bash
   cd frontend
   ```

2. Cài đặt Node modules:
   ```bash
   npm install
   ```

3. Khởi chạy Vite Dev Server:
   ```bash
   npm run dev
   ```

4. Truy cập Giao diện Web:
   Mở trình duyệt truy cập: [http://localhost:5173](http://localhost:5173)

---

## 📡 Danh sách API Endpoints Chính

### 1. Trợ lý AI Chatbot (`/api/v1/chat`)

| Phương thức | API Endpoint         | Mô tả Chức năng                                                                          |
| :---------: | :------------------- | :--------------------------------------------------------------------------------------- |
|   `POST`    | `/api/v1/chat/query` | Tiếp nhận câu hỏi tiếng Việt tự nhiên, chuyển đổi T-SQL, thực thi và trả kết quả chi tiết |

### 2. Thống kê & Phân tích (`/api/v1/analytics`)

| Phương thức | API Endpoint                               | Mô tả Chức năng                                                           |
| :---------: | :----------------------------------------- | :------------------------------------------------------------------------ |
|    `GET`    | `/api/v1/analytics/overview`               | Lấy chỉ số tổng quan tuyển sinh (Tỉ lệ đỗ, Yield Rate nhập học)           |
|    `GET`    | `/api/v1/analytics/regions`                | Thống kê số lượng thí sinh đăng ký theo Tỉnh / Thành                      |
|    `GET`    | `/api/v1/analytics/majors`                 | Thống kê theo Ngành học (Số NV, chỉ tiêu, số lượng trúng tuyển & nhập học) |
|    `GET`    | `/api/v1/analytics/methods`                | Thống kê phân bố thí sinh theo Phương thức xét tuyển                      |
|    `GET`    | `/api/v1/analytics/score-analytics`        | Phân tích phân bố điểm thi THPT & điểm chuẩn các ngành                    |
|    `GET`    | `/api/v1/analytics/geographic-enrollment` | Dữ liệu bản đồ nhiệt (Heatmap) tỉ lệ nhập học theo địa phương             |
|    `GET`    | `/api/v1/analytics/gender-distribution`    | Phân tích cơ cấu giới tính Nam/Nữ theo ngành & phương thức                |

### 3. Tra cứu Hồ sơ Thí sinh (`/api/v1/students`)

| Phương thức | API Endpoint             | Mô tả Chức năng                                                                        |
| :---------: | :----------------------- | :------------------------------------------------------------------------------------- |
|    `GET`    | `/api/v1/students/{cccd}` | Tra cứu hồ sơ chi tiết thí sinh (Thông tin cá nhân, điểm thi, chứng chỉ, nguyện vọng) |

---

## 🛡️ An toàn & Bảo mật Hệ thống

- **Chống SQL Injection**: SQL Executor áp dụng cơ chế phân tích cú pháp nghiêm ngặt, từ chối mọi câu lệnh có chứa từ khóa làm thay đổi cấu trúc/dữ liệu (`INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `EXEC`,...).
- **Xử lý ngoại lệ (Self-Correction)**: Khi câu SQL do LLM sinh ra gặp lỗi cú pháp trên SQL Server, AI Agent sẽ tự gửi lại thông tin lỗi kèm cấu trúc bảng để LLM sửa chữa câu SQL tự động.
- **Offline & Private**: Toàn bộ luồng xử lý RAG và LLM chạy 100% Local qua Ollama & ChromaDB, không tải bất kỳ dữ liệu nhạy cảm nào của trường hay thí sinh lên đám mây.

---

## 🤝 Đóng góp & Phát triển (Contributing)

Mọi đóng góp nhằm nâng cao tính năng hoặc tối ưu hiệu năng đều được hoan nghênh:
1. Fork dự án.
2. Tạo nhánh tính năng mới (`git checkout -b feature/AmazingFeature`).
3. Commit các thay đổi (`git commit -m 'Add some AmazingFeature'`).
4. Push lên nhánh (`git push origin feature/AmazingFeature`).
5. Mở một Pull Request.

---

## 📄 Giấy phép (License)

Dự án được phát triển phục vụ mục đích nghiên cứu, học tập và ứng dụng thực tế trong công tác quản lý tuyển sinh tại Đại học Kinh tế Quốc dân (NEU).