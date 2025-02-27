from fastapi import FastAPI
from database import engine
from Project.controller import router as projectRouter
from Resource.controller import router as resourceRouter
from Assignment.controller import router as assignmentRouter

import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(resourceRouter)
app.include_router(projectRouter)
app.include_router(assignmentRouter)

@app.get("/")
def read_root():
    return {"Hello": "World"}