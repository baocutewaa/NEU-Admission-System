from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.ai_agent import AIAgentService

router = APIRouter()

@router.post("/query", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def ask_admission_bot(payload: ChatRequest):
    """
    Endpoint tiếp nhận câu hỏi tự nhiên về tuyển sinh từ Frontend React,
    chuyển đổi thành lệnh SQL Server nội bộ thông qua RAG Pipeline và trả về đáp án.
    """
    if not payload.question.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Nội dung câu hỏi không được để trống."
        )
        
    try:
        ai_service = AIAgentService()
        result = await ai_service.process_text_to_sql(payload.question)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi hệ thống trong quá trình xử lý Agent: {str(e)}"
        )