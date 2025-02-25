from fastapi import FastAPI,  HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from gitlab import GitlabCreateError, GitlabGetError
from pydantic import BaseModel
from gitlab_client import get_gitlab_client
from typing import Optional, List, Any
import uvicorn
import base64

gl = get_gitlab_client()

class NewProject(BaseModel):
    project_name: str
    namespace_id: int
    description: Optional[str] = ""

    
class NewCommit(BaseModel):
    branch: str
    commit_message: str
    actions: List[Any]

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)



@app.get("/repositories/{repository_id}/files")
async def get_project_files(repository_id: int):
    try:
        project = gl.projects.get(repository_id)
        default_branch = project.default_branch
        items = project.repository_tree(ref=default_branch, path="", recursive=True, per_page=100)
        return JSONResponse(content=items, status_code=200)

    except GitlabGetError as e:
        status_code = getattr(e, "response_code", 500)
        message = "Access forbidden: insufficient permissions" if status_code == 403 else "Project not found" if status_code == 404 else "An error occurred while retrieving the project"
        return JSONResponse(content={"status": "error", "message": message}, status_code=status_code)



@app.get("/repositories/{repository_id}/files/{file_id}")
async def get_file_content(repository_id: int, file_id: str):
    try:
        project = gl.projects.get(repository_id)
        file_info = project.repository_blob(file_id)

        content = base64.b64decode(file_info['content']).decode('utf-8')
        size = file_info['size']

        return JSONResponse(content={"content": content, "size": size}, status_code=200)

    except GitlabGetError as e:
        status_code = getattr(e, "response_code", 500)
        message = "Access forbidden: insufficient permissions" if status_code == 403 else "Project not found" if status_code == 404 else "An error occurred while retrieving the file"
        return JSONResponse(content={"status": "error", "message": message}, status_code=status_code)



@app.post("/project/create")
async def create_project(data: NewProject):
    try:
        project = gl.projects.create({
            "name": data.project_name, # Name of the project
            "namespace_id": data.namespace_id, # ID of the group
            "description": data.description # Optional field
        })
        return JSONResponse(content=project.attributes, status_code=200)
    
    except GitlabCreateError as e:
        status_code = getattr(e, "response_code", 500)
        message = "Access forbidden: insufficient permissions" if status_code == 403 else "Project creation failed"
        return JSONResponse(content={"status": "error", "message": message}, status_code=status_code)


@app.post("/repositories/{repository_id}/commit")
async def commit(repository_id: int, data: NewCommit):
    try:
        print(repository_id)
        # Get the GitLab client instance
        gl = get_gitlab_client()

        # Attempt to retrieve the project
        project = gl.projects.get(repository_id)

        # Prepare commit data
        commit_data = {
            "branch": data.branch,
            "commit_message": data.commit_message,
            "actions": data.actions
        }

        # Create the commit
        project.commits.create(commit_data)

        return JSONResponse(content={"status": "success", "message": "Commit created successfully."}, status_code=200)

    except GitlabGetError as e:
        status_code = getattr(e, "response_code", 500)
        detail = "Project not found" if status_code == 404 else "Access forbidden: insufficient permissions"
        raise HTTPException(status_code=status_code, detail=detail)

    except GitlabCreateError as e:
        status_code = getattr(e, "response_code", 500)
        message = "Access forbidden: insufficient permissions" if status_code == 403 else "Commit creation failed"
        return JSONResponse(content={"status": "error", "message": message}, status_code=status_code)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
