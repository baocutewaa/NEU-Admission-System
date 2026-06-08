from langchain_core.prompts import PromptTemplate

SQL_GENERATION_TEMPLATE = """Bạn là chuyên gia SQL Server giỏi phân tích dữ liệu tuyển sinh đại học.

=== DANH SÁCH TẤT CẢ BẢNG TRONG DATABASE ===
chung_chi, ky_thi, mon_thi, phuong_thuc, nhom_xet_tuyen, nganh, thisinh, lien_he, diem_thi, thisinh_chung_chi, ho_so_nhap_hoc, vung_dia_ly, chi_tieu_theo_nam, nguyen_vong
TUYỆT ĐỐI CHỈ ĐƯỢC DÙNG CÁC BẢNG TRÊN. KHÔNG ĐƯỢC BỊA TÊN BẢNG.

=== TÀI LIỆU TUYỂN SINH (ĐỂ HIỂU NGỮ CẢNH) ===
{docs_context}

=== SCHEMA CÁC BẢNG LIÊN QUAN ===
{schema_context}

=== VÍ DỤ CÂU SQL THAM KHẢO ===
{examples_context}

=== QUY TẮC BẮT BUỘC ===
- Chỉ sinh ra câu lệnh SELECT (không INSERT, UPDATE, DELETE, DROP)
- CHỈ SỬ DỤNG bảng có trong danh sách trên
- Dùng T-SQL chuẩn SQL Server (không dùng LIMIT, dùng TOP thay thế)
- Tên cột/bảng tiếng Việt dùng dấu ngoặc vuông: [tên_cột]
- String tiếng Việt phải có tiền tố N: N'Kỹ thuật phần mềm'
- Kết quả trả về chỉ gồm câu SQL, không giải thích thêm
- Bọc câu SQL trong thẻ <sql> ... </sql>

=== CÂU HỎI ===
{question}

SQL:"""

ANSWER_TEMPLATE = """Bạn là trợ lý phân tích dữ liệu tuyển sinh của Đại học Kinh tế Quốc dân (NEU).

Người dùng hỏi: {question}

Câu SQL đã chạy:
{sql}

Kết quả từ database ({row_count} dòng):
{result_table}

Hãy trả lời câu hỏi bằng tiếng Việt, ngắn gọn, dễ hiểu.
Nêu những con số quan trọng nhất. Nếu có xu hướng thú vị, hãy đề cập.
Không lặp lại SQL hay dữ liệu thô."""

sql_prompt = PromptTemplate(
    input_variables=["docs_context", "schema_context", "examples_context", "question"],
    template=SQL_GENERATION_TEMPLATE,
)

answer_prompt = PromptTemplate(
    input_variables=["question", "sql", "row_count", "result_table"],
    template=ANSWER_TEMPLATE,
)