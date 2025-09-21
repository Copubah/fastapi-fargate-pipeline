from fastapi import FastAPI
import os

app = FastAPI(title="FastAPI CI/CD Demo", version="1.0.0")


@app.get("/")
def read_root():
    return {
        "message": "Hello from FastAPI!",
        "environment": os.getenv("ENVIRONMENT", "dev"),
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}