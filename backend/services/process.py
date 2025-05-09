from typing import Tuple
from services.grobid import extract_xml_from_pdf
from services.parse import extract_text_from_xml_v2, extract_text_from_xml_v1
from services.deepfigures_open import extract_images_from_pdf
from services.predict import predict_gemini
from services.slide_compiler import compile_slide
from fastapi import UploadFile
from datetime import datetime
import os

async def process_file(file: UploadFile) -> Tuple[str, bool]:
    # Get current timestamp
    temp_file_name = "".join(str(datetime.now().timestamp()).split("."))

    # Create tmp directory if it doesn't exist
    if not os.path.exists("tmp"):
        os.makedirs("tmp")
        
    if not os.path.exists(f"tmp/{temp_file_name}"):
        os.makedirs(f"tmp/{temp_file_name}")
        
    # Save the uploaded file to a temporary location
    temp_file_path = f"tmp/{temp_file_name}/paper.pdf"
    with open(temp_file_path, "wb") as temp_file:
        content = await file.read()
        temp_file.write(content)
    
    # # --- Step 1: Extract XML from PDF using GROBID ---
    # xml_data = await extract_xml_from_pdf(temp_file_path)
    
    # # Save the XML data to a file
    # xml_file_path = f"tmp/{temp_file_name}.xml"
    # with open(xml_file_path, "w", encoding="utf-8") as xml_file:
    #     xml_file.write(xml_data)
    
    # # --- Step 2: Parse XML and save in txt file ---
    # txt_file_path = f"tmp/{temp_file_name}.txt"
    # found_section_tag = extract_text_from_xml_v2(xml_file_path, txt_file_path)
    
    # if not found_section_tag:
    #     # If the new method fails, fall back to the old method
    #     extract_text_from_xml_v1(xml_file_path, txt_file_path)
        
    # --- Step 3: Extract images from PDF using DeepFigures ---
    
    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_dir = os.path.join(script_dir, f"../tmp/{temp_file_name}")
    weights_dir = os.path.join(script_dir, "../../weights")
    
    extract_images_from_pdf(file_dir, weights_dir)
    
    # --- Step 4: Generate markdown file ---
    markdown_result_path = f"tmp/{temp_file_name}/slide.md"
    await predict_gemini(temp_file_path, markdown_result_path)
    
    # --- Step : Compile slide ---
    compile_slide_path = f"tmp/{temp_file_name}/slide.pdf"
    compile_success = compile_slide(markdown_result_path, compile_slide_path)
    
    return (temp_file_name, compile_success)
    
    # Remove the temporary file after processing
    # os.remove(temp_file_path)