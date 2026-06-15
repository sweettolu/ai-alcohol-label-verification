from fastapi import FastAPI
from app.routers.verify import router as verify_router

app = FastAPI(
    title="AI Alcohol Label Verification API",
    version="1.0.0"
)

app.include_router(verify_router)


@app.get("/")
def root():
    return {
        "message": "AI Alcohol Label Verification API is running!"
    }