from pydantic import BaseModel
from typing import Optional

class Response(BaseModel):
    status: int
    message: str
    count: Optional[int] = None
    data: Optional[dict] | Optional[list] = None
    error: Optional[str] = None