import os
from dotenv import load_dotenv
from github import Github

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN is not set in .env")

github = Github(GITHUB_TOKEN)


def get_repository():
    return github.get_repo("VOMMIROHITHKUMAR/autonomous-code-review-agent")