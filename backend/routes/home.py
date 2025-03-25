from fastapi import APIRouter
from fastapi.responses import FileResponse
from config import templates_dir
import os

router = APIRouter()

@router.get("/")
async def serve_home():
    return FileResponse(os.path.join(templates_dir, "index.html"))

@router.get("/encrypt/")
async def serve_encrypt_page():
    return FileResponse(os.path.join(templates_dir, "encrypt.html"))

@router.get("/decrypt/")
async def serve_decrypt_page():
    return FileResponse(os.path.join(templates_dir, "decrypt.html"))
