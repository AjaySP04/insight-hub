from pydantic import BaseModel

class ChatInput(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    response: str