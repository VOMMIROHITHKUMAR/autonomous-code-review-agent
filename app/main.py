from fastapi import FastAPI

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