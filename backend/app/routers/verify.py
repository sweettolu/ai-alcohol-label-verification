from fastapi import APIRouter, UploadFile, File, Form
from io import BytesIO

from app.services.ocr_service import extract_text
from app.services.parser_service import parse_label
from app.services.verification_service import verify_label

router = APIRouter(prefix="/api", tags=["Verification"])


@router.post("/verify")
async def verify(
    file: UploadFile = File(...),
    brand: str = Form(...),
    class_name: str = Form(...),
    alcohol: str = Form(...),
    net_contents: str = Form(...)
):
    contents = await file.read()

    ocr_text = extract_text(BytesIO(contents))
    parsed = parse_label(ocr_text)

    expected = {
        "brand": brand,
        "class": class_name,
        "alcohol": alcohol,
        "net_contents": net_contents
    }

    verification = verify_label(expected, parsed)

    return {
        "filename": file.filename,
        "ocr_text": ocr_text,
        "parsed": parsed,
        "verification": verification
    }