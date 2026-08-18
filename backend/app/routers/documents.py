from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List, Dict, Any
import io
import pypdf
from pptx import Presentation

router = APIRouter(prefix="/api/v1/documents", tags=["Documents"])

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    file_ext = file.filename.split(".")[-1].lower()
    content = await file.read()
    
    extracted_data = []
    
    try:
        if file_ext == "txt":
            text = content.decode("utf-8", errors="ignore")
            extracted_data.append({
                "page_number": 1,
                "text": text,
                "metadata": {"type": "txt"}
            })
            
        elif file_ext == "pdf":
            pdf_file = io.BytesIO(content)
            reader = pypdf.PdfReader(pdf_file)
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    extracted_data.append({
                        "page_number": i + 1,
                        "text": text,
                        "metadata": {"type": "pdf_page"}
                    })
                    
        elif file_ext == "pptx":
            pptx_file = io.BytesIO(content)
            presentation = Presentation(pptx_file)
            for i, slide in enumerate(presentation.slides):
                text_runs = []
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        text_runs.append(shape.text)
                text = "\n".join(text_runs)
                if text.strip():
                    extracted_data.append({
                        "page_number": i + 1,
                        "text": text,
                        "metadata": {"type": "pptx_slide"}
                    })
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_ext}")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
        
    return {
        "filename": file.filename,
        "document_type": file_ext,
        "total_pages": len(extracted_data),
        "pages": extracted_data
    }
