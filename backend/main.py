# run by calling
# (dev) uvicorn main:app --reload
# (prod) uvicorn main:app

from typing import Annotated
from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from services.process import process_file

app = FastAPI()

current_process_count = 0
max_process_count = 5

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/process")
async def process(file: UploadFile):
    if (file.content_type != "application/pdf"):
        return {"error": "File type not supported"}
    
    global current_process_count
    if current_process_count >= max_process_count:
        raise HTTPException(status_code=400, detail="There are too many processes running. Please try again later.")
    
    current_process_count += 1
    try:
        process_id, compile_success = await process_file(file)
        current_process_count -= 1
        return {
            "filename": file.filename,
            "is_compile_success": compile_success,
            "id": process_id
        }
    except Exception as e:
        current_process_count -= 1
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the file: {str(e)}")
    
    
@app.get("/process/{process_id}/markdown")
async def get_markdown(process_id: str):
    try:
        # Get the markdown file from the process ID
        with open(f"tmp/{process_id}/slide.md", "r") as f:
            markdown_text = f.read()
        return { "data": markdown_text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"File not found: {str(e)}")

@app.get("/process/{process_id}/slide")
async def get_slide(process_id: str):
    try:
        # return response as file
        return FileResponse(f"tmp/{process_id}/slide.pdf", media_type='application/pdf')
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"File not found: {str(e)}")