from fastapi import APIRouter, status
from Assignment.service import AssignmentService
from response import Response

router = APIRouter()

@router.post("/assignment/{projectId}/{resourceId}", response_model=Response)
def createAssignment(projectId: int, resourceId: int):
    try:
        if AssignmentService.findRecord(projectId, resourceId):
            return Response(status=status.HTTP_400_BAD_REQUEST, message="Resource already associate with project", error="Resource already associate with project")

        createdAssignment: dict = AssignmentService.create(projectId, resourceId)
        return Response(status=status.HTTP_201_CREATED, message="Assignment successful", data=createdAssignment, count=1)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST, message="Failed to create assignment", error=str(e))

@router.get("/assignments/resource/{resourceId}", response_model=Response)
def getResourceAssignment(resourceId: int):
    try:
        assignments: list[dict] = AssignmentService.findByResourceId(resourceId)
        return Response(status=status.HTTP_200_OK, message="Resources fetched successfully", data=assignments, count=len(assignments))
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST, message="Failed to get assignment", error=str(e))

@router.get("/assignments/live/{resourceId}", response_model=Response)
def getLiveAssignments(resourceId: int):
    try:
        assignments: list[dict] = AssignmentService.findLiveProjects(resourceId)
        return Response(status=status.HTTP_200_OK, message="Resources fetched successfully", data=assignments,count=len(assignments))
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST, message="Failed to get assignment", error=str(e))

@router.get("/assignments/project/{projectId}", response_model=Response)
def getProjectAssignment(projectId: int):
    try:
        assignments: list[dict] = AssignmentService.findByProjectId(projectId)
        return Response(status=status.HTTP_200_OK, message="Resources fetched successfully", data=assignments, count=len(assignments))
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST, message="Failed to get assignment", error=str(e))

@router.post("/offboard/{projectId}/{resourceId}", response_model=Response)
def offboard(projectId: int, resourceId: int):
    try:
        AssignmentService.makeOffBoard(projectId, resourceId)
        return Response(status=status.HTTP_200_OK, message="offboard  successful", data=None)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST, message="Failed to create assignment", error=str(e))

@router.get("/bench")
def getBenchResource():
    try:
        benchedResources: list[dict] = AssignmentService.findBenchResource()
        return Response(status=status.HTTP_200_OK, message="Fetched successful", data=benchedResources, count=len(benchedResources))
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST, message="Failed to create assignment", error=str(e))
