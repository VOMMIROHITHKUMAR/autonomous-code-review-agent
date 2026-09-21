import hashlib
import hmac
import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request

from app.pull_request import get_changed_files
from app.review_engine import review_code
from app.github_client import post_pr_comment


load_dotenv()

GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")


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


@app.post("/webhook/github")
async def github_webhook(request: Request):
    # Read the raw request body
    body = await request.body()

    # Get GitHub's signature
    signature = request.headers.get("X-Hub-Signature-256")

    if not GITHUB_WEBHOOK_SECRET:
        return {
            "status": "error",
            "reason": "GITHUB_WEBHOOK_SECRET is not configured"
        }

    if not signature:
        return {
            "status": "unauthorized",
            "reason": "Missing GitHub webhook signature"
        }

    # Calculate the expected GitHub signature
    expected_signature = "sha256=" + hmac.new(
        GITHUB_WEBHOOK_SECRET.encode("utf-8"),
        body,
        hashlib.sha256
    ).hexdigest()

    # Compare signatures securely
    if not hmac.compare_digest(signature, expected_signature):
        return {
            "status": "unauthorized",
            "reason": "Invalid GitHub webhook signature"
        }

    # Convert the verified JSON body into a Python dictionary
    payload = await request.json()

    action = payload.get("action")

    if action not in ["opened", "synchronize", "reopened"]:
        return {
            "status": "ignored",
            "reason": f"Unsupported action: {action}"
        }

    pull_request = payload.get("pull_request")

    if not pull_request:
        return {
            "status": "ignored",
            "reason": "No pull request data"
        }

    pr_number = pull_request.get("number")

    changed_files = get_changed_files(pr_number)

    review = review_code(changed_files)

    post_pr_comment(pr_number, review)

    return {
        "status": "review completed",
        "pr_number": pr_number,
        "action": action,
        "review": review
    }