from pydantic import BaseModel
from typing import  Optional
from datetime import datetime

class Assignment(BaseModel):
    recordId: Optional[int] = None
    projectId: int
    resourceId: int
    onBoard: Optional[datetime] = None
    offBoard: Optional[datetime] = None
