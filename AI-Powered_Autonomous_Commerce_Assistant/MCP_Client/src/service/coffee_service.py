from src.agent.agent import run_agent
import re
from langchain_core.messages import AIMessage
from src.utils.exceptions.custom_app_exception import AppBaseException
from src.utils.exceptions.error_codes import ErrorCode, ErrorCodeStatus
from src.repository.error_repository import ErrorRepository

error=ErrorRepository()

class ChatService:
    async def process_chat(self, message: str,thread_id:str) -> list:
        try:
            result = await run_agent(message,thread_id)
            messages = result.get("messages", [])
            if not messages:
                error.error(
                    file_name="coffee_service",
                    function_name="process_chat",
                    message="Agent returned no messages."
                )
                raise AppBaseException(
                    error_code=ErrorCodeStatus.get(ErrorCode.CHAT_PROCESSING_FAILED, "BB_CHAT_001"),
                    message="Agent returned no messages.",
                    status_code=500,
                )
            structured_data = result.get("structured_response")
            json_response = structured_data.model_dump()
            print(json_response)
 
            return (messages[-2].tool_calls[0]['args'])
                
        except AppBaseException:
            raise
        except Exception as exc:
            error.error(
                    file_name="coffee_service",
                    function_name="process_chat",
                    message=f"Chat processing failed: {str(exc)}"
                )
            raise AppBaseException(
                error_code=ErrorCodeStatus.get(ErrorCode.CHAT_PROCESSING_FAILED, "BB_CHAT_001"),
                message=f"Chat processing failed: {str(exc)}",
                status_code=500,
            )
        





