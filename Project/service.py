from sqlalchemy import func

import models
from database import Session
from Project.project import Project

db = Session()

class ProjectService:
    def __init__(self):
        pass

    @staticmethod
    def create(project: Project) -> dict:
        dbProject: models.Project = models.Project(
            projectName = project.projectName,
            projectManager = project.projectManager,
            projectStatus = project.projectStatus,
            projectDescription = project.projectDescription,
            softDeadline = project.softDeadline,
            hardDeadline = project.hardDeadline
        )
        db.add(dbProject)
        db.commit()
        db.refresh(dbProject)
        return  dbProject.toDict()

    @staticmethod
    def findById(projectId: int) -> dict | None:
        project: models.Project = db.query(models.Project).filter(models.Project.projectId == projectId).first()
        if project:
            return project.toDict()
        return None

    @staticmethod
    def findAll() -> list[dict]:
        projects: list[models.Project] = db.query(models.Project).all()
        newProjects: list[dict] = []

        for project in projects:
            newProjects.append(project.toDict())

        return newProjects

    @staticmethod
    def update(projectId: int, project: Project) -> dict | None:
        dbProject: models.Project = db.query(models.Project).filter(models.Project.projectId == projectId).first()
        if dbProject:
            dbProject.projectName = project.projectName
            dbProject.projectManager = project.projectManager
            dbProject.projectStatus = project.projectStatus
            dbProject.endDate = project.endDate
            dbProject.softDeadline = project.softDeadline
            dbProject.projectDescription = project.projectDescription
            db.commit()
            db.refresh(dbProject)
            return dbProject.toDict()
        return None

    @staticmethod
    def endProject(projectId: int):
        project: models.Project = db.query(models.Project).filter(models.Project.projectId == projectId).first()
        if project:
            project.endDate = func.now()
            db.commit()

        db.query(models.ResourceAssignment).filter(models.ResourceAssignment.projectId == projectId, models.ResourceAssignment.offBoard.is_(None)).update({"offBoard": func.now()})
        db.commit()
