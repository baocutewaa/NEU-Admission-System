import os
import glob
import chromadb
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.database import db_chain_connector # Dùng engine kết nối trực tiếp

CHROMA_DIR = os.getenv("CHROMA_PERSIST_DIR", "./data/chroma_db")
COLLECTION_SCHEMA = "neu_schema"
COLLECTION_EXAMPLES = "neu_examples"
COLLECTION_DOCS = "neu_docs"
EMBED_MODEL = os.getenv("EMBED_MODEL", "BAAI/bge-m3")

# --- Cached singletons ---
_embeddings_instance = None
_vector_stores_cache = None

def get_embeddings_service() -> HuggingFaceEmbeddings:
    global _embeddings_instance
    if _embeddings_instance is None:
        print("[VectorStore] Đang load embedding model (chỉ chạy 1 lần)...")
        _embeddings_instance = HuggingFaceEmbeddings(
            model_name=EMBED_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
        print("[VectorStore] Embedding model đã sẵn sàng.")
    return _embeddings_instance

def get_vector_stores():
    """Khởi tạo nhanh kết nối tới các collections trong ChromaDB (cached)."""
    global _vector_stores_cache
    if _vector_stores_cache is not None:
        return _vector_stores_cache

    embeddings = get_embeddings_service()
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    
    schema_store = Chroma(client=client, collection_name=COLLECTION_SCHEMA, embedding_function=embeddings)
    examples_store = Chroma(client=client, collection_name=COLLECTION_EXAMPLES, embedding_function=embeddings)
    docs_store = Chroma(client=client, collection_name=COLLECTION_DOCS, embedding_function=embeddings)
    
    _vector_stores_cache = (schema_store, examples_store, docs_store)
    return _vector_stores_cache

def init_vector_stores(force_reindex: bool = True):
    """Khởi tạo dữ liệu vào ChromaDB. force_reindex=True sẽ xóa và tạo lại toàn bộ."""
    embeddings = get_embeddings_service()
    client = chromadb.PersistentClient(path=CHROMA_DIR)

    if force_reindex:
        print("[VectorStore] Force re-index: xóa toàn bộ collections cũ...")
        for name in [COLLECTION_SCHEMA, COLLECTION_EXAMPLES, COLLECTION_DOCS]:
            try:
                client.delete_collection(name)
                print(f"  Đã xóa collection: {name}")
            except Exception:
                pass

    # Reset cache để tạo lại stores mới
    global _vector_stores_cache
    _vector_stores_cache = None

    schema_store, examples_store, docs_store = get_vector_stores()
    
    # 1. Build schema index
    if schema_store._collection.count() == 0:
        print("Đang tạo schema index cho RAG...")
        tables = db_chain_connector.get_usable_table_names()
        docs = []
        for t in tables:
            try:
                table_info = db_chain_connector.get_table_info([t])
                docs.append(Document(page_content=table_info, metadata={"table": t}))
            except Exception as e:
                print(f"Lỗi khi lấy thông tin bảng {t}: {e}")
        
        if docs:
            schema_store.add_documents(docs)
            print(f"Đã thêm thông tin của {len(docs)} bảng vào vector store.")
    else:
        print("Schema index đã tồn tại. Bỏ qua khởi tạo lại.")

    # 2. Build examples index
    if examples_store._collection.count() == 0:
        print("Đang tạo examples index cho RAG...")
        default_examples = [
            {
                "question": "Có bao nhiêu thí sinh nhập học?",
                "sql": "SELECT COUNT(*) FROM ho_so_nhap_hoc;"
            },
            {
                "question": "Cho tôi biết chỉ tiêu của ngành 7340101 (Quản trị kinh doanh)?",
                "sql": "SELECT ChiTieuDieuChinh FROM chi_tieu_theo_nam WHERE MaNganh = '7340101';"
            },
            {
                "question": "Thông tin liên hệ của thí sinh có cccd là 012345678901?",
                "sql": "SELECT SoDienThoai, Email FROM lien_he WHERE CCCD = '012345678901';"
            },
            {
                "question": "Liệt kê danh sách các thí sinh nữ nộp chứng chỉ IELTS với điểm IELTS trên 7.0?",
                "sql": "SELECT thisinh.HoTen, thisinh_chung_chi.DiemGoc FROM thisinh JOIN thisinh_chung_chi ON thisinh.CCCD = thisinh_chung_chi.CCCD WHERE thisinh.GioiTinh = N'Nữ' AND thisinh_chung_chi.MaCC = 'IELTS' AND thisinh_chung_chi.DiemGoc > 7.0;"
            },
            {
                "question": "Em muốn biết danh sách 5 chứng chỉ phổ biến nhất mà các bạn nộp?",
                "sql": "SELECT TOP 5 chung_chi.TenChungChi, COUNT(*) AS SoLuong FROM thisinh_chung_chi JOIN chung_chi ON thisinh_chung_chi.MaCC = chung_chi.MaCC GROUP BY chung_chi.TenChungChi ORDER BY SoLuong DESC;"
            },
            {
                "question": "Có bao nhiêu thí sinh đăng ký xét tuyển năm 2025?",
                "sql": "SELECT COUNT(DISTINCT CCCD) AS SoThiSinh FROM nguyen_vong WHERE NamTuyenSinh = 2025;"
            },
            {
                "question": "Danh sách ngành có nhiều nguyện vọng đăng ký nhất?",
                "sql": "SELECT TOP 10 nganh.TenNganh, COUNT(*) AS SoNguyenVong FROM nguyen_vong JOIN nganh ON nguyen_vong.MaNganh = nganh.MaNganh GROUP BY nganh.TenNganh ORDER BY SoNguyenVong DESC;"
            },
            {
                "question": "Tỉ lệ trúng tuyển của từng ngành năm 2025?",
                "sql": "SELECT n.TenNganh, COUNT(CASE WHEN nv.TrangThai = N'Trung tuyen' THEN 1 END) * 100.0 / COUNT(*) AS TiLeTrungTuyen FROM nguyen_vong nv JOIN nganh n ON nv.MaNganh = n.MaNganh WHERE nv.NamTuyenSinh = 2025 GROUP BY n.TenNganh ORDER BY TiLeTrungTuyen DESC;"
            },
            {
                "question": "Năm 2024 NEU tuyển sinh bao nhiêu ngành, gồm các ngành gì?",
                "sql": "SELECT COUNT(*) AS SoNganh FROM chi_tieu_theo_nam WHERE NamTuyenSinh = 2024; SELECT n.MaNganh, n.TenNganh FROM chi_tieu_theo_nam ct JOIN nganh n ON ct.MaNganh = n.MaNganh WHERE ct.NamTuyenSinh = 2024;"
            },
            {
                "question": "Có bao nhiêu thí sinh trúng tuyển năm 2025?",
                "sql": "SELECT COUNT(DISTINCT CCCD) AS SoTrungTuyen FROM nguyen_vong WHERE NamTuyenSinh = 2025 AND TrangThai = N'Trung tuyen';"
            },
            {
                "question": "Thí sinh nào có điểm thi THPT cao nhất?",
                "sql": "SELECT TOP 1 ts.HoTen, SUM(dt.Diem) AS TongDiem FROM diem_thi dt JOIN thisinh ts ON dt.CCCD = ts.CCCD WHERE dt.MaKyThi = 'THPT2025' GROUP BY ts.HoTen ORDER BY TongDiem DESC;"
            },
            {
                "question": "Số lượng thí sinh nhập học theo từng phương thức?",
                "sql": "SELECT pt.TenPhuongThuc, COUNT(*) AS SoLuong FROM ho_so_nhap_hoc hs JOIN nhom_xet_tuyen nxt ON hs.MaNhom = nxt.MaNhom JOIN phuong_thuc pt ON nxt.MaPT = pt.MaPT GROUP BY pt.TenPhuongThuc;"
            },
            {
                "question": "Chỉ tiêu và số nhập học thực tế của các ngành năm 2025?",
                "sql": "SELECT n.TenNganh, ct.ChiTieuDieuChinh, COUNT(hs.CCCD) AS SoNhapHoc FROM chi_tieu_theo_nam ct JOIN nganh n ON ct.MaNganh = n.MaNganh LEFT JOIN ho_so_nhap_hoc hs ON ct.MaNganh = hs.MaNganh AND hs.NamTuyenSinh = ct.NamTuyenSinh WHERE ct.NamTuyenSinh = 2025 GROUP BY n.TenNganh, ct.ChiTieuDieuChinh;"
            },
            {
                "question": "Thí sinh từ tỉnh nào đăng ký nhiều nhất?",
                "sql": "SELECT TOP 10 vdl.TenTinh, COUNT(DISTINCT nv.CCCD) AS SoThiSinh FROM nguyen_vong nv JOIN thisinh ts ON nv.CCCD = ts.CCCD JOIN vung_dia_ly vdl ON ts.HoKhauThuongTru LIKE '%' + vdl.TenTinh + '%' GROUP BY vdl.TenTinh ORDER BY SoThiSinh DESC;"
            },
            {
                "question": "Điểm trung bình thi THPT của thí sinh trúng tuyển ngành Quản trị kinh doanh?",
                "sql": "SELECT AVG(dt.Diem) AS DiemTB FROM diem_thi dt JOIN nguyen_vong nv ON dt.CCCD = nv.CCCD WHERE nv.MaNganh = '7340101' AND nv.TrangThai = N'Trung tuyen' AND dt.MaKyThi = 'THPT2025';"
            }
        ]
        
        ex_docs = []
        for ex in default_examples:
            ex_docs.append(Document(
                page_content=ex["question"],
                metadata={"sql": ex["sql"]}
            ))
            
        if ex_docs:
            examples_store.add_documents(ex_docs)
            print(f"Đã thêm {len(ex_docs)} ví dụ SQL vào vector store.")
    else:
        print("Examples index đã tồn tại. Bỏ qua khởi tạo lại.")

    # 3. Build docs index
    if docs_store._collection.count() == 0:
        print("Đang tạo docs index cho RAG từ thư mục data...")
        data_dir = os.path.join(os.path.dirname(__file__), "../../../data")
        pdf_files = glob.glob(os.path.join(data_dir, "*.pdf"))
        md_files = glob.glob(os.path.join(data_dir, "*.md"))
        
        all_docs = []
        
        for pdf_file in pdf_files:
            try:
                loader = PyPDFLoader(pdf_file)
                all_docs.extend(loader.load())
            except Exception as e:
                print(f"Lỗi đọc {pdf_file}: {e}")
                
        for md_file in md_files:
            try:
                loader = TextLoader(md_file, encoding="utf-8")
                all_docs.extend(loader.load())
            except Exception as e:
                print(f"Lỗi đọc {md_file}: {e}")

        if all_docs:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            split_docs = text_splitter.split_documents(all_docs)
            docs_store.add_documents(split_docs)
            print(f"Đã thêm {len(split_docs)} đoạn dữ liệu tài liệu vào vector store.")
    else:
        print("Docs index đã tồn tại. Bỏ qua khởi tạo lại.")