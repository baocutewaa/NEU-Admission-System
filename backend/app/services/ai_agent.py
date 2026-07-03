import re
import os
import time
import asyncio
from langchain_ollama import OllamaLLM
from app.services.rag_engine.vector_store import get_vector_stores
from app.services.rag_engine.retriever import retrieve_rag_context
from app.services.sql_engine.prompt_factory import sql_prompt, answer_prompt
from app.services.sql_engine.sql_executor import execute_query_safe

class AIAgentService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        print("[AIAgent] Khởi tạo LLM và Vector Stores (chỉ chạy 1 lần)...")
        self.llm = OllamaLLM(
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            model=os.getenv("OLLAMA_MODEL", "qwen2.5:3b"),
            temperature=0.1,
            num_predict=512,   # Giới hạn output token → giảm thời gian inference
            num_thread=10,     # Tận dụng 10/12 logical processors
        )
        self.schema_store, self.examples_store, self.docs_store = get_vector_stores()
        print("[AIAgent] Khởi tạo hoàn tất.")

    def _extract_sql(self, llm_output: str) -> str:
        # 1. Thử match các pattern có đóng tag/block
        for pattern in [r"<sql>(.*?)</sql>", r"```sql\s*(.*?)```", r"```(.*?)```"]:
            match = re.search(pattern, llm_output, re.DOTALL | re.IGNORECASE)
            if match:
                return self._clean_sql(match.group(1).strip())
        
        # 2. Thử match <sql> không có closing tag (model nhỏ hay quên đóng tag)
        match = re.search(r"<sql>\s*(.*)", llm_output, re.DOTALL | re.IGNORECASE)
        if match:
            return self._clean_sql(match.group(1).strip())

        # 3. Fallback: tìm SELECT/WITH trong output
        upper = llm_output.upper()
        for keyword in ("SELECT", "WITH"):
            idx = upper.find(keyword)
            if idx != -1:
                return self._clean_sql(llm_output[idx:].strip())
        return self._clean_sql(llm_output.strip())

    def _clean_sql(self, sql: str) -> str:
        """Loại bỏ các artifact markdown/XML còn sót trong SQL."""
        # Xóa các closing tags/blocks còn sót
        sql = re.sub(r"</sql>", "", sql, flags=re.IGNORECASE).strip()
        sql = re.sub(r"<sql>", "", sql, flags=re.IGNORECASE).strip()
        sql = re.sub(r"```\w*", "", sql).strip()
        sql = re.sub(r"```", "", sql).strip()
        # Xóa backtick đơn ở đầu/cuối
        sql = sql.strip("`").strip()
        # Luôn tìm và cắt về đúng vị trí SELECT/WITH (bỏ mọi rác ở đầu)
        upper = sql.upper()
        for keyword in ("SELECT", "WITH"):
            idx = upper.find(keyword)
            if idx != -1:
                return sql[idx:].strip()
        return sql

    def _format_result_table(self, query_result: dict, max_rows: int = 15) -> str:
        if "error" in query_result:
            return f"Lỗi hệ thống: {query_result['error']}"
        cols = query_result.get("columns", [])
        rows = query_result.get("rows", [])
        if not rows:
            return "(Không tìm thấy dữ liệu phù hợp trong hệ thống)"
        
        lines = [" | ".join(str(c) for c in cols), "-+-".join("-" * max(len(str(c)), 8) for c in cols)]
        for row in rows[:max_rows]:
            lines.append(" | ".join(str(v) if v is not None else "NULL" for v in row))
        return "\n".join(lines)

    async def process_text_to_sql(self, question: str) -> dict:
        total_start = time.perf_counter()

        # 1. Tìm ngữ cảnh bảng & ví dụ gần nhất (blocking → chạy trong thread)
        t0 = time.perf_counter()
        context = await asyncio.to_thread(
            retrieve_rag_context, question, self.schema_store, self.examples_store, self.docs_store
        )
        print(f"[Timing] RAG retrieval: {time.perf_counter() - t0:.2f}s")

        # 2. Sinh câu lệnh SQL (blocking LLM call → chạy trong thread)
        sql_input = sql_prompt.format(
            schema_context=context["schema"],
            examples_context=context["examples"],
            docs_context=context["docs"],
            question=question
        )
        t0 = time.perf_counter()
        raw_sql = await asyncio.to_thread(self.llm.invoke, sql_input)
        print(f"[Timing] LLM sinh SQL: {time.perf_counter() - t0:.2f}s")
        print(f"[Debug] Raw LLM output: {raw_sql[:500]}")
        generated_sql = self._extract_sql(raw_sql)
        print(f"[Debug] Extracted SQL: {generated_sql[:300]}")

        # 3. Thực thi an toàn
        t0 = time.perf_counter()
        query_result = await asyncio.to_thread(execute_query_safe, generated_sql)
        print(f"[Timing] SQL execution: {time.perf_counter() - t0:.2f}s")

        # Self-correction (Tự sửa lỗi nếu SQL Server báo lỗi cú pháp)
        if "error" in query_result:
            fix_prompt = (
                f"Câu hỏi gốc: {question}\n\n"
                f"Câu SQL sau bị lỗi trên SQL Server:\n{generated_sql}\n\n"
                f"Lỗi: {query_result['error']}\n\n"
                f"=== CẤU TRÚC BẢNG (kiểm tra kỹ tên cột) ===\n{context['schema']}\n\n"
                f"=== QUY TẮC ===\n"
                f"- Kiểm tra tên cột có đúng với bảng không (VD: ChiTieu thuộc bảng nganh, ChiTieuDieuChinh thuộc chi_tieu_theo_nam)\n"
                f"- Chỉ dùng bảng: chung_chi, ky_thi, mon_thi, phuong_thuc, nhom_xet_tuyen, nganh, thisinh, lien_he, diem_thi, thisinh_chung_chi, ho_so_nhap_hoc, vung_dia_ly, chi_tieu_theo_nam, nguyen_vong\n"
                f"- Trả về câu SQL sửa lại bọc trong thẻ <sql>...</sql>"
            )
            t0 = time.perf_counter()
            raw_sql = await asyncio.to_thread(self.llm.invoke, fix_prompt)
            print(f"[Timing] LLM self-correction: {time.perf_counter() - t0:.2f}s")
            generated_sql = self._extract_sql(raw_sql)
            query_result = await asyncio.to_thread(execute_query_safe, generated_sql)

        # 4. Trả lời ngôn ngữ tự nhiên
        result_table = self._format_result_table(query_result)
        if "error" not in query_result:
            answer_input = answer_prompt.format(
                question=question,
                sql=generated_sql,
                row_count=query_result.get("row_count", 0),
                result_table=result_table
            )
            t0 = time.perf_counter()
            answer = await asyncio.to_thread(self.llm.invoke, answer_input)
            print(f"[Timing] LLM trả lời NL: {time.perf_counter() - t0:.2f}s")
        else:
            answer = f"Tôi xin lỗi, hệ thống không thể tự động thực thi truy vấn này. Lỗi: {query_result['error']}"

        print(f"[Timing] === TỔNG THỜI GIAN: {time.perf_counter() - total_start:.2f}s ===")

        return {
            "question": question,
            "sql": generated_sql,
            "answer": answer,
            "row_count": query_result.get("row_count", 0),
            "tables_used": context["schema_tables"],
            "columns": query_result.get("columns"),
            "rows": query_result.get("rows"),
        }

