from google import genai
from google.genai import types as genai_types
from services.system_instruction import get_system_instruction
from dotenv import load_dotenv
import os

load_dotenv()

model = "gemini-2.5-pro-preview-03-25"

async def predict_gemini(pdf_file_path: str, markdown_result_path: str) -> str:
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        raise ValueError("API key not found. Please set the GOOGLE_API_KEY environment variable.")
    
    client = genai.Client(api_key=api_key)
    
    pdf = open(pdf_file_path, "rb").read()
    
    print("Generating content...")
    
    first_response = client.models.generate_content(
        model=model,
        contents=[
            genai_types.Part.from_bytes(
                data=pdf,
                mime_type="application/pdf"
            ),
            "Please create sli.dev markdown file for this pdf plase concern what output will look like to and sure in content in not too heavy just main point no need to include any reference in it think like i am author of this paper want to create slide from my paper."
        ],
        config=genai_types.GenerateContentConfig(
            temperature=0,  # Adjust the temperature for creativity (0.0-1.0)
            system_instruction=get_system_instruction(),  # System instruction for the model
        ),
    )
    
    first_markdown = first_response.text.strip("```markdown\n")
    with open(markdown_result_path, "w", encoding="utf-8") as file:
        file.write(first_markdown)
    
    print("Markdown file generated successfully.")
    