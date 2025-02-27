from pydantic import BaseModel
from typing import Optional

class Resource(BaseModel):
    resourceId: Optional[int] = None
    resourceName: str
    resourceEmail: str
    isDeleted: Optional[bool] = False

