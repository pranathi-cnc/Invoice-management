
# main.py
import hashlib
import os
from fastapi import Depends

from security import get_current_user

from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pocketbase import PocketBase
from pocketbase.client import FileUpload 
from auth import router as auth_router
from invoice_ai.processor import process_invoice

app = FastAPI(title="FastAPI PocketBase Local Uploader")
app.include_router(auth_router)

# Cleaned CORS configuration to allow local browser HTML components
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to your running PocketBase database engine
pb = PocketBase('http://127.0.0.1:8090')

ALLOWED_MIME_TYPES = [
    "application/pdf",
    "image/png",
    "image/jpeg",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
]

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type."
        )

    try:
        # Read uploaded file
        file_bytes = await file.read()

        # Generate SHA256 hash
        file_hash = hashlib.sha256(file_bytes).hexdigest()

        records = pb.collection("docs").get_full_list()

        existing_name = None
        existing_hash = None

        # Check filename and hash
        for record in records:

            if hasattr(record, "file_name") and record.file_name == file.filename:
                existing_name = record

            if hasattr(record, "hash_id") and record.hash_id == file_hash:
                existing_hash = record

        # =====================================================
        # Same filename + Same content
        # =====================================================
        if existing_name and existing_hash:
            raise HTTPException(
                status_code=409,
                detail="This file has already been uploaded."
            )

        # =====================================================
        # Same filename + Different content
        # =====================================================
        if existing_name:
            raise HTTPException(
                status_code=409,
                detail="A file with this name already exists. Please rename your file."
            )

        # =====================================================
        # Different filename + Same content
        # =====================================================
        if existing_hash:
            raise HTTPException(
                status_code=409,
                detail=f"A file with the same content already exists as '{existing_hash.file_name}'. Please use the existing file."
            )
        
        # Save file locally for OCR

        local_file_path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        with open(local_file_path, "wb") as f:
            f.write(file_bytes)

        # =====================================================
        # Upload new file
        # =====================================================

        print(file.filename)
        print(file.content_type)
        pocketbase_file = FileUpload(
            (
                file.filename,
                file_bytes,
                file.content_type
            )
        )

        new_record = pb.collection("docs").create({
            "file": pocketbase_file,
            "file_name": file.filename,
            "file_size": len(file_bytes),
            "file_type": file.filename.split(".")[-1].lower(),
            "hash_id": file_hash
        })

        # Process invoice using OCR + Gemini

        invoice_data = process_invoice(
            file_bytes,
            file.filename
        )

        file_url = (
            f"http://127.0.0.1:8090/api/files/docs/"
            f"{new_record.id}/{new_record.file}"
        )

        return {
    "status": "success",
    "message": "File uploaded successfully.",
    "file_url": file_url,
    "invoice_data": invoice_data
}

    except HTTPException:
        raise

    except Exception as e:
        print("UPLOAD ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
           
  



# --- ENDPOINT 2: FETCH STORED GALLERY LIST ---
@app.get("/files")
async def list_files():
    try:
        # Fetch data rows from PocketBase ordered by creation date
        records = pb.collection("docs").get_full_list()
        
        file_list = []
        for record in records:
            # PocketBase paths use: /api/files/{collection_name}/{record_id}/{filename}
            url = f"http://127.0.0.1:8090/api/files/docs/{record.id}/{record.file}"
            file_list.append({
                "id": record.id,
                "filename": record.file_name,      # Original filename
                "file_size": record.file_size,
                "file_type": record.file_type.upper(),
                "uploaded_at": record.created,
                "url": url
            })
        return file_list
        
    except Exception as e:
        print(f"CRITICAL GALLERY FETCH ERROR: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to query database files: {str(e)}"
        )
