main.py

from fastapi import FastAPI
from pydantic import BaseModel
import requests
import base64
import os

app = FastAPI(title="Chani Auto Publisher")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_OWNER = os.getenv("GITHUB_OWNER")

class PublishRequest(BaseModel):
repo_name: str
files: dict

def github_headers():
return {
"Authorization": f"Bearer {GITHUB_TOKEN}",
"Accept": "application/vnd.github+json"
}

@app.post("/publish")
def publish(req: PublishRequest):

repo_url = f"https://api.github.com/repos/{GITHUB_OWNER}/{req.repo_name}"

check = requests.get(repo_url, headers=github_headers())

if check.status_code == 404:
    create_repo = requests.post(
        "https://api.github.com/user/repos",
        headers=github_headers(),
        json={
            "name": req.repo_name,
            "private": False
        }
    )

    if create_repo.status_code not in [201]:
        return {
            "error": create_repo.json()
        }

for filename, content in req.files.items():

    encoded = base64.b64encode(
        content.encode("utf-8")
    ).decode()

    requests.put(
        f"https://api.github.com/repos/{GITHUB_OWNER}/{req.repo_name}/contents/{filename}",
        headers=github_headers(),
        json={
            "message": f"update {filename}",
            "content": encoded
        }
    )

return {
    "status": "published",
    "repo": f"https://github.com/{GITHUB_OWNER}/{req.repo_name}"
}
