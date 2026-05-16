class ErrorCode:
    DB_CONNECTION_FAILED = "DatabaseConnectionFailedErrorCode"
    INTERNAL_SERVER_ERROR = "InternalServerErrorCode"
    CHAT_PROCESSING_FAILED = "ChatProcessingFailedErrorCode"
    AGENT_INVOKE_FAILED = "AgentInvokeFailedErrorCode"
    MENU_ITEM_NOT_FOUND = "MenuItemNotFoundErrorCode"
    ORDER_NOT_FOUND = "OrderNotFoundErrorCode"
    INSUFFICIENT_STOCK = "InsufficientStockErrorCode"
    INVALID_REQUEST = "InvalidRequestErrorCode"


ErrorCodeStatus = {
    ErrorCode.DB_CONNECTION_FAILED: "BB_DB_001",
    ErrorCode.INTERNAL_SERVER_ERROR: "BB_SYS_001",
    ErrorCode.CHAT_PROCESSING_FAILED: "BB_CHAT_001",
    ErrorCode.AGENT_INVOKE_FAILED: "BB_AGENT_001",
    ErrorCode.MENU_ITEM_NOT_FOUND: "BB_MENU_001",
    ErrorCode.ORDER_NOT_FOUND: "BB_ORD_001",
    ErrorCode.INSUFFICIENT_STOCK: "BB_ORD_002",
    ErrorCode.INVALID_REQUEST: "BB_REQ_001",
}