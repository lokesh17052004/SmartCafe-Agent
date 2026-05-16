from pydantic import BaseModel,Field
from typing import Optional
class ChatRequest(BaseModel):
    message:str

class ChatResponse(BaseModel):
    reply:dict

class OrderDetails(BaseModel):
    """
    Use this model when then user needs the details about the particular order
    """
    order_code :str = Field("Fill this field once the order is placed")
    status:str = Field("Fill this field when the order is placed")
    total_price:float = Field("Fill this field when the order is placed")
    reply:str 

class OtherResponse(BaseModel):
    reply:str = Field("Fill the reply field if the user prompt is related to bean and brew")

class MenuItem(BaseModel):
  
    item_name:str
    price:float

class MemoryRequest(BaseModel):
    message:str
    thread_id:str

class MenuDetails(BaseModel):
    items:list[MenuItem]

class OffContext(BaseModel):
    response:str = Field("Fill the response field if the user prompt is out of context")