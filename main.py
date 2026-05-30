from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import Response
import subprocess
import uuid
import os
import shutil

app = FastAPI()

TEMP_DIR = "/tmp/docxpdf"

os.makedirs(TEMP_DIR, exist_ok=True)


@app.get("/")
async def root():
    return {"ok": True}


@app.post("/convert")
async def convert(file: UploadFile = File(...)):

    uid = str(uuid.uuid4())

    input_path = os.path.join(TEMP_DIR, f"{uid}.docx")
    output_path = os.path.join(TEMP_DIR, f"{uid}.pdf")

    try:

        with open(input_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        process = subprocess.run(
            [
                "soffice",
                "--headless",
                "--nologo",
                "--nofirststartwizard",
                "--convert-to",
                "pdf",
                input_path,
                "--outdir",
                TEMP_DIR
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=120
        )

        if process.returncode != 0:
            raise HTTPException(
                status_code=500,
                detail=process.stderr.decode()
            )

        if not os.path.exists(output_path):
            raise HTTPException(
                status_code=500,
                detail="PDF file not created"
            )

        with open(output_path, "rb") as pdf_file:
            pdf_bytes = pdf_file.read()

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": "inline; filename=converted.pdf"
            }
        )

    finally:

        try:
            if os.path.exists(input_path):
                os.remove(input_path)
        except:
            pass

        try:
            if os.path.exists(output_path):
                os.remove(output_path)
        except:
            pass