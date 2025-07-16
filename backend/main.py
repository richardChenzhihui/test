from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from backend.schemas import EditTextRequest, EditTextResponse, ParseRequest, ParseResponse
from backend.word_utils import edit_text, parse_docx_structure
import os

app = FastAPI()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/edit_text", response_model=EditTextResponse)
def edit_text_api(
    file: UploadFile = File(...),
    locate_type: str = Form(...),
    locate_value: str = Form(...),
    op_type: str = Form(...),
    content: str = Form(None)
):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    result = edit_text(file_path, locate_type, locate_value, op_type, content)
    if result["success"]:
        return EditTextResponse(
            success=True,
            download_url=f"/download/{os.path.basename(result['download_url'])}",
            structure=result["structure"]
        )
    else:
        return EditTextResponse(success=False, message=result["message"])

@app.post("/parse", response_model=ParseResponse)
def parse_api(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    structure = parse_docx_structure(file_path)
    return structure

@app.get("/download/{filename}")
def download_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    return FileResponse(file_path, media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document', filename=filename)