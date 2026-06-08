from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from langchain_community.utilities import SQLDatabase
from app.core.config import settings
from app.models.base import Base

# 1. Khởi tạo SQLAlchemy engine hiện tại của bạn
# Khuyến khích bật pool_pre_ping=True để tự động hồi sinh kết nối nếu SQL Server ngắt kết nối tạm thời
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True
)

# 2. Khởi tạo SessionLocal class hiện tại của bạn
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. TÍCH HỢP THÊM: Tạo connector cho RAG Text-to-SQL
# LangChain sẽ dùng chung engine này để quét schema và thực thi các câu lệnh SELECT an toàn
db_chain_connector = SQLDatabase(engine)

# 4. Dependency để lấy DB session cho các endpoint CRUD hiện tại
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()