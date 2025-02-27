from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base

class Resource(Base):
    __tablename__: str = 'Resource'
    resourceId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    resourceName = Column(String, nullable=False)
    resourceEmail = Column(String, nullable=False, unique=True)
    isDeleted = Column(Boolean, nullable=False)

    def toDict(self):
        return {
            "resourceId": self.resourceId,
            "resourceName": self.resourceName,
            "resourceEmail": self.resourceEmail,
            "isDeleted": self.isDeleted
        }

class Project(Base):
    __tablename__: str = 'Project'
    projectId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    projectName = Column(String, nullable=False)
    projectManager = Column(Integer, ForeignKey('Resource.resourceId'), nullable=False)
    projectStatus = Column(String, nullable=False)
    startDate = Column(DateTime, nullable=False, default=func.now())
    endDate = Column(DateTime, nullable=True)
    softDeadline = Column(DateTime, nullable=False)
    hardDeadline = Column(DateTime, nullable=False)
    projectDescription = Column(String, nullable=False)

    def toDict(self):
        return {
            "projectId": self.projectId,
            "projectName": self.projectName,
            "projectManager": self.projectManager,
            "projectStatus": self.projectStatus,
            "startDate": self.startDate,
            "endDate": self.endDate,
            "softDeadline": self.softDeadline,
            "hardDeadline": self.hardDeadline,
            "projectDescription": self.projectDescription
        }

class ResourceAssignment(Base):
    __tablename__: str = 'Resource_assignment'
    recordId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    projectId = Column(Integer, ForeignKey('Project.projectId'), nullable=False)
    resourceId = Column(Integer, ForeignKey('Resource.resourceId'), nullable=False)
    onBoard = Column(DateTime, nullable=False, default=func.now())
    offBoard = Column(DateTime, nullable=True)

    def toDict(self):
        return {
            "recordId": self.recordId,
            "projectId": self.projectId,
            "resourceId": self.resourceId,
            "onBoard": self.onBoard,
            "offBoard": self.offBoard
        }