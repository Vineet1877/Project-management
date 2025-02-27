from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Project(BaseModel):
    projectId: Optional[int] = None
    projectName: str
    projectManager: int
    projectStatus: str
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None
    softDeadline: datetime
    hardDeadline: datetime
    projectDescription: str
