from fastapi import APIRouter, UploadFile, File

router = APIRouter(
    prefix="/api",
    tags=["Verification"]
)

@router.post("/verify")
async def verify_label(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "status": "Image received successfully"
    }