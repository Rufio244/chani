from github import Github
from config import *


class ChaniGitHub:

    def __init__(self):
        self.github = Github(GITHUB_TOKEN)
        self.user = self.github.get_user(GITHUB_USERNAME)


    def create_repo(self, name):

        repos = [r.name for r in self.user.get_repos()]

        if name in repos:
            return "Repo already exists"

        repo = self.user.create_repo(
            name,
            private=False,
            description="Created by Chani AI System"
        )

        return repo.html_url


    def upload_file(self, repo_name, path, content):

        repo = self.user.get_repo(repo_name)

        try:
            old = repo.get_contents(path)

            repo.update_file(
                path,
                "Chani Auto Update",
                content,
                old.sha
            )

        except:

            repo.create_file(
                path,
                "Chani Initial Upload",
                content
            )


        return "Uploaded"


    def push_system(self, files):

        self.create_repo(DEFAULT_REPO)

        for file in files:

            self.upload_file(
                DEFAULT_REPO,
                file["path"],
                file["content"]
            )


        return "Chani System Synced"
