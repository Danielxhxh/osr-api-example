# API examples OSR

## Installation and Setup

### Virtual Environment
If you don't want to use a Python virtual environment, you can skip this step.
```bash
python3 -m venv env
source env/bin/activate
 ```

### Environment Variables
Modify the `.env` adding your GitLab private token. (User Settings > Access tokens > Personal Access tokens) 

### Install dependencies
 ```bash
pip install -r requirements.txt
 ```

## Run the Application
 ```bash
uvicorn main:app --reload --port 3000
 ```

--- 

## APIs examples
### Create a new repository
`POST /project/create`
 ```bash
{
    "project_name": "Sandbox-1",
    "namespace_id": 97430675, //ID of the subgroup you want to create the repository in.
    "description": "A repository about..." // Optional field
}
 ```

### Commit
`POST /repositories/{repository_id}/commit`
 ```bash
 {
    "branch": "main",
    "commit_message": "A commit",
    "actions": [
        {
            "action": "create",
            "file_path": "TestAPI.txt",
            "content": "This is a new file."
        },
        {
            "action": "update",
            "file_path": "Cool.pdf",
            "content": "A.  Tab.\r\n\r\nNew line after an empty line.\r\nAnother new line."
        }
    ]
}
```
Note: Other examples at [website](https://docs.gitlab.com/ee/api/commits.html).