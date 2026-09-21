from fastapi import FastAPI

from app.pull_request import get_changed_files
from app.review_engine import review_code
from app.github_client import post_pr_comment


app = FastAPI(
    title="Autonomous Code Review Agent",
    description="AI-powered GitHub Pull Request Code Review Agent",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Autonomous Code Review Agent is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/review/{pr_number}")
def review_pull_request(pr_number: int):
    changed_files = get_changed_files(pr_number)

    review = review_code(changed_files)

    post_pr_comment(pr_number, review)

    return {
        "status": "review completed",
        "pr_number": pr_number,
        "review": review
    }