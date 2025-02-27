import models
from database import Session
from Resource.resource import Resource

db = Session()

class ResourceService:
    def __init__(self):
        pass

    @staticmethod
    def create(resource: Resource) -> dict:
        dbResource = models.Resource(
            resourceName = resource.resourceName,
            resourceEmail = resource.resourceEmail,
            isDeleted = False
        )
        db.add(dbResource)
        db.commit()
        db.refresh(dbResource)
        return dbResource.toDict()

    @staticmethod
    def findById(resourceId: int) -> dict | None:
        resource: models.Resource = db.query(models.Resource).filter(models.Resource.resourceId == resourceId).first()
        if not resource.isDeleted:
            return resource.toDict()
        return None

    @staticmethod
    def findAll() -> list[dict]:
        resources: list[models.Resource] = db.query(models.Resource).all()
        newResources: list[dict] = []

        for resource in resources:
            if not resource.isDeleted:
                newResources.append(resource.toDict())

        return newResources

    @staticmethod
    def update(resourceId: int, resource: Resource) -> dict | None:
        dbResource: models.Resource = db.query(models.Resource).filter(models.Resource.resourceId == resourceId and models.Resource.isDeleted == False).first()
        if dbResource and not dbResource.isDeleted:
            dbResource.resourceName = resource.resourceName
            dbResource.resourceEmail = resource.resourceEmail
            db.commit()
            db.refresh(dbResource)
            return dbResource.toDict()
        return None

    @staticmethod
    def delete(resourceId: int) -> dict | None:
        dbResource: models.Resource = db.query(models.Resource).filter(models.Resource.resourceId == resourceId).first()
        if dbResource:
            dbResource.isDeleted = True
            db.commit()
            db.refresh(dbResource)
            return dbResource.toDict()
        return None