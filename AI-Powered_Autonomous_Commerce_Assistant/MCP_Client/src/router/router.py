from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.models.model import MemoryRequest, ChatResponse
from src.service.coffee_service import ChatService
from src.utils.exceptions.custom_app_exception import AppBaseException
from src.utils.exceptions.error_codes import ErrorCode, ErrorCodeStatus
from src.repository.error_repository import ErrorRepository

error=ErrorRepository()

router = APIRouter(prefix="/api/v1", tags=["Chat"])

@router.post("/chat")
async def chat(request: MemoryRequest):
    try:
        service = ChatService()
        message=request.message.strip()
        if message:
            reply = await service.process_chat(message,request.thread_id)
            return JSONResponse(
                content=ChatResponse(reply=reply).model_dump(),
                status_code=200
            )
        else:
            raise AppBaseException(
                error_code=ErrorCodeStatus.get(ErrorCode.CHAT_PROCESSING_FAILED, "BB_CHAT_001"),
                message=f"User query can't be empty",
                status_code=500,
            )
    except AppBaseException:
        raise
    except Exception as e:
        error.error(
                file_name="router",
                function_name="chat",
                message=str(e)
            )
        return JSONResponse(
            content={"error_code": "BB_SYS_001", "message": str(e)},
            status_code=500
        )
