chani_auto_publisher.py

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
import requests
import base64
import os

app = FastAPI(title="CHANI Auto Publisher")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_OWNER = os.getenv("GITHUB_OWNER", "Rufio244")

class PublishRequest(BaseModel):
repo_name: str
files: Dict[str, str]

def headers():
return {
"Authorization": f"Bearer {GITHUB_TOKEN}",
"Accept": "application/vnd.github+json",
"X-GitHub-Api-Version": "2022-11-28"
}

def repo_exists(repo_name):
r = requests.get(
f"https://api.github.com/repos/{GITHUB_OWNER}/{repo_name}",
headers=headers()
)
return r.status_code == 200

def create_repo(repo_name):
return requests.post(
"https://api.github.com/user/repos",
headers=headers(),
json={
"name": repo_name,
"private": False,
"auto_init": True
}
)

def get_sha(repo_name, filename):
r = requests.get(
f"https://api.github.com/repos/{GITHUB_OWNER}/{repo_name}/contents/{filename}",
headers=headers()
)

if r.status_code == 200:
    return r.json()["sha"]

return None

def upload_file(repo_name, filename, content):

encoded = base64.b64encode(
    content.encode("utf-8")
).decode()

payload = {
    "message": f"CHANI update {filename}",
    "content": encoded
}

sha = get_sha(repo_name, filename)

if sha:
    payload["sha"] = sha

return requests.put(
    f"https://api.github.com/repos/{GITHUB_OWNER}/{repo_name}/contents/{filename}",
    headers=headers(),
    json=payload
)

@app.post("/publish")
def publish(data: PublishRequest):

if not GITHUB_TOKEN:
    return {
        "error": "Missing GITHUB_TOKEN"
    }

if not repo_exists(data.repo_name):
    create = create_repo(data.repo_name)

    if create.status_code not in [201]:
        return {
            "error": create.json()
        }

results = []

for filename, content in data.files.items():

    response = upload_file(
        data.repo_name,
        filename,
        content
    )

    results.append({
        "file": filename,
        "status": response.status_code
    })

return {
    "success": True,
    "repository": f"https://github.com/{GITHUB_OWNER}/{data.repo_name}",
    "files": results
}

@app.get("/")
def health():
return {
"system": "CHANI",
"status": "online"
}
