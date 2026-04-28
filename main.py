import io
import re
import mammoth
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="DOCX to Markdown Converter")


def docx_to_markdown(file_bytes: bytes) -> str:
    result = mammoth.convert_to_markdown(io.BytesIO(file_bytes))
    return result.value


@app.post("/api/convert")
async def convert(file: UploadFile = File(...)):
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Only .docx files are supported")
    content = await file.read()
    try:
        markdown = docx_to_markdown(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")
    word_count = len(re.findall(r"\w+", markdown))
    return JSONResponse({"markdown": markdown, "word_count": word_count, "filename": file.filename})


@app.get("/", response_class=HTMLResponse)
async def index():
    with open("index.html", "r") as f:
        return f.read()
