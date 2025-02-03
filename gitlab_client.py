import json
from gitlab import Gitlab
from dotenv import load_dotenv
import os

load_dotenv()  

# Access the private token
gitlab_url = os.getenv("GITLAB_URL")
admin_private_token = os.getenv("GITLAB_PRIVATE_TOKEN")

gl = None

def get_gitlab_client():
    global gl
    if gl is None:
        # Initialize the GitLab client only on first use
        gl = Gitlab(url=gitlab_url, private_token=admin_private_token)
        gl.auth()
    return gl