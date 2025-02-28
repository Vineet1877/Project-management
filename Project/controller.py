from fastapi import APIRouter, status
from Project.project import Project
from Project.service import ProjectService
from Assignment.service import AssignmentService
from response import Response

router = APIRouter()

@router.post("/project", response_model=Response)
def createProject(project: Project):
    try:
        createdProject: dict = ProjectService.create(project)
        AssignmentService.create(createdProject.get("projectId"),project.projectManager)
        return Response(status=status.HTTP_201_CREATED, message="Project created successfully", data=createdProject)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST, message="Failed to create project", error=str(e))

@router.get("/project/{projectId}", response_model=Response)
def getById(projectId: int):
    project: dict = ProjectService.findById(projectId)
    if not project:
        return Response(status=status.HTTP_404_NOT_FOUND, message="Project not found", error="Invalid projectId")

    return Response(status=status.HTTP_200_OK, message="Project fetched successfully", data=project)

@router.get("/projects", response_model=Response)
def getAll():
    projects = ProjectService.findAll()
    return Response(status=status.HTTP_200_OK, message="Resources fetched successfully", data=projects)

@router.put("/project/{projectId}", response_model=Response)
def updateProject(projectId: int, project: Project):
    try:
        updatedProject = ProjectService.update(projectId, project)
        if not updatedProject:
            return Response(status=status.HTTP_404_NOT_FOUND, message="Project not found for update", error="Invalid projectId")

        return Response(status=status.HTTP_200_OK, message="Resource updated successfully", data=updatedProject)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST, message="Failed to update resource", error=str(e), data=None)

@router.post("/endProject/{projectId}")
def endProject(projectId: int):
    ProjectService.endProject(projectId)
    return Response(status=status.HTTP_200_OK, message="Project ended")