from fastapi import APIRouter, status
from Resource.resource import Resource
from Resource.service import ResourceService
from response import Response

router = APIRouter()

@router.post("/resource", response_model=Response)
def createResource(resource: Resource):
    try:
        createdResource: dict = ResourceService.create(resource)
        createdResource.pop("isDeleted")
        return Response(status=status.HTTP_201_CREATED, message="Resource created successfully", data=createdResource)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST, message="Failed to create resource", error=str(e))

@router.get("/resource/{resourceId}", response_model=Response, status_code=status.HTTP_200_OK)
def getById(resourceId: int):
    resource: dict = ResourceService.findById(resourceId)
    resource.pop("isDeleted")
    if not resource:
        return Response(status=status.HTTP_404_NOT_FOUND, message="Resource not found", error="Invalid resourceId")

    return Response(status=status.HTTP_200_OK, message="Resource fetched successfully", data=resource)

@router.get("/resources", response_model=Response)
def getAll():
    resources = ResourceService.findAll()

    for resource in resources:
        resource.pop("isDeleted")

    return Response(status=status.HTTP_200_OK, message="Resources fetched successfully", data=resources)

@router.put("/resource/{resourceId}", response_model=Response)
def updateResource(resourceId: int, resource: Resource):
    try:
        updatedResource = ResourceService.update(resourceId, resource)
        if not updatedResource:
            return Response(status=status.HTTP_404_NOT_FOUND, message="Resource not found for update", error="Invalid resourceId")

        updatedResource.pop("isDeleted")
        return Response(status=status.HTTP_200_OK, message="Resource updated successfully", data=updatedResource)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST, message="Failed to update resource", error=str(e), data=None)


@router.delete("/resource/{resourceId}", response_model=Response, status_code=status.HTTP_200_OK)
def deleteResource(resourceId: int):
    try:
        deletedResource = ResourceService.delete(resourceId)
        if not deletedResource:
            return Response(status=status.HTTP_404_NOT_FOUND, message="Resource not found for deletion", error="Invalid resourceId")

        return Response(status=status.HTTP_200_OK, message="Resource deleted successfully", data=deletedResource)
    except Exception as e:
        return Response(status=400, message="Failed to delete resource", error=str(e)).model_dump()