import pandas as pd
from sqlalchemy import text
from app.core.database import engine

def execute_query_safe(sql: str, max_rows: int = 100) -> dict:
    """Thực thi câu lệnh SQL sử dụng Connection Pool của SQLAlchemy một cách an toàn."""
    sql_clean = sql.strip().rstrip(";")
    
    if not sql_clean:
        return {"error": "Câu lệnh SQL trống."}

    # Safety Guardrail: Chỉ cho phép đọc dữ liệu
    first_word = sql_clean.split()[0].upper()
    if first_word not in ("SELECT", "WITH"):
        return {"error": "Hành vi bị từ chối: Hệ thống chỉ cho phép thực thi câu lệnh đọc dữ liệu (SELECT/WITH).", "sql": sql_clean}

    try:
        # Sử dụng connection từ Pool để tối ưu hiệu năng
        with engine.connect() as conn:
            df = pd.read_sql_query(text(sql_clean), conn)
            
        row_count = len(df)
        truncated = False
        if row_count > max_rows:
            df = df.head(max_rows)
            truncated = True

        return {
            "columns": list(df.columns),
            "rows": df.values.tolist(),
            "row_count": row_count,
            "truncated": truncated,
            "sql": sql_clean,
        }
    except Exception as e:
        return {"error": str(e), "sql": sql_clean}