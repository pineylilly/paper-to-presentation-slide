import requests

async def extract_xml_from_pdf(file_path: str) -> str:
    # Send POST request to GROBID service with the PDF file
    response = requests.post(
        'http://localhost:8070/api/processFulltextDocument', 
        files=(
            ('input', open(file_path, 'rb')),
            ('consolidateHeader', '1'),
        )
    )
    
    return response.text