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
        assignments: list[models.ResourceAssignment] = db.query(models.ResourceAssignment).filter(
            models.ResourceAssignment.projectId == projectId).all()

        resourceIds: list[int] = []
        for assignment in assignments:
            resourceIds.append(assignment.resourceId)

        dbResources: list[models.Project] = db.query(models.Resource).filter(models.Resource.resourceId.in_(resourceIds)).all()
        resources: list[dict] = []
        for resource in dbResources:
            resources.append(resource.toDict())

        return resources

    @staticmethod
    def findLiveProjects(resourceId: int) -> list[dict]:
        assignments: list[models.ResourceAssignment] = db.query(models.ResourceAssignment).filter(
            models.ResourceAssignment.resourceId == resourceId, models.ResourceAssignment.offBoard is None).all()

        projectIds: list[int] = []
        for assignment in assignments:
            projectIds.append(assignment.projectId)

        dbProjects: list[models.Project] = db.query(models.Project).filter(models.Project.projectId.in_(projectIds)).all()
        projects: list[dict] = []
        for project in dbProjects:
            projects.append(project.toDict())

        return projects

    @staticmethod
    def findByResourceId(resourceId: int) -> list[dict]:
        assignments: list[models.ResourceAssignment] = db.query(models.ResourceAssignment).filter(
            models.ResourceAssignment.resourceId == resourceId).all()

        projectIds: list[int] = []
        for assignment in assignments:
            projectIds.append(assignment.projectId)

        dbProjects: list[models.Project] = db.query(models.Project).filter(
            models.Project.projectId.in_(projectIds)).all()
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
