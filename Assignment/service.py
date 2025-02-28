import datetime
import models
from database import Session

db = Session()

class AssignmentService:
    def __init__(self):
        pass

    @staticmethod
    def create(projectId: int, resourceId: int) -> dict:
        dbAssignment: models.ResourceAssignment = models.ResourceAssignment(
            projectId = projectId,
            resourceId = resourceId,
        )
        db.add(dbAssignment)
        db.commit()
        db.refresh(dbAssignment)
        return dbAssignment.toDict()

    @staticmethod
    def findRecord(projectId: int, resourceId: int) -> bool:
        assignment: models.ResourceAssignment = db.query(models.ResourceAssignment).filter(
            models.ResourceAssignment.projectId == projectId, models.ResourceAssignment.resourceId == resourceId).first()
        if assignment:
            return True
        return False

    @staticmethod
    def findByProjectId(projectId: int) -> list[dict]:
        dbResources: list[models.Resource] = db.query(models.Resource).join(models.ResourceAssignment, models.Resource.resourceId == models.ResourceAssignment.resourceId).filter(models.ResourceAssignment.projectId == projectId, models.ResourceAssignment.offBoard.is_(None)).all()

        resources: list[dict] = []
        for resource in dbResources:
            resources.append(resource.toDict())

        return resources

    @staticmethod
    def findLiveProjects(resourceId: int) -> list[dict]:
        dbProjects: list[models.Project] = db.query(models.Project).join(models.ResourceAssignment, models.Project.projectId == models.ResourceAssignment.projectId).filter(models.ResourceAssignment.resourceId == resourceId, models.ResourceAssignment.offBoard.is_(None)).all()

        projects: list[dict] = []
        for project in dbProjects:
            projects.append(project.toDict())

        return projects

    @staticmethod
    def findByResourceId(resourceId: int) -> list[dict]:
        dbProjects: list[models.Project] = db.query(models.Project).join(models.ResourceAssignment, models.Project.projectId == models.ResourceAssignment.projectId).filter(models.ResourceAssignment.resourceId == resourceId).all()

        projects: list[dict] = []
        for project in dbProjects:
            projects.append(project.toDict())

        return projects

    @staticmethod
    def makeOffBoard(projectId: int, resourceId: int):
        assignment: models.ResourceAssignment = db.query(models.ResourceAssignment).filter(
            models.ResourceAssignment.projectId == projectId, models.ResourceAssignment.resourceId == resourceId).first()
        if assignment:
            assignment.offBoard = datetime.datetime.now()
            db.commit()
            db.refresh(assignment)

    @staticmethod
    def findBenchResource() -> list[dict]:
        subquery = (
            db.query(models.ResourceAssignment.resourceId)
            .filter(models.ResourceAssignment.offBoard.is_(None))
            .subquery()
        )

        benchResources = (
            db.query(models.Resource)
            .filter(models.Resource.resourceId.notin_(subquery))
            .all()
        )

        resources: list[dict] = []
        for resource in benchResources:
            resources.append(resource.toDict())

        return resources