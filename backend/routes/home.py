from fastapi import APIRouter
from fastapi.responses import FileResponse
from config import *
import os

router = APIRouter()

@router.get("/")
async def serve_home():
    return FileResponse(os.path.join(html_dir, "index.html"))

@router.get("/encrypt/")
async def serve_encrypt_page():
    return FileResponse(os.path.join(templates_dir, "encrypt.html"))

@router.get("/decrypt/")
async def serve_decrypt_page():
    return FileResponse(os.path.join(templates_dir, "decrypt.html"))

@router.get("/reconstruct/")
async def serve_reconstruct_page():
    return FileResponse(os.path.join(templates_dir, "reconstruct.html"))

@router.get("/about/")
async def serve_about_page():
    return FileResponse(os.path.join(html_dir, "about.html"))

@router.get("/services/")
async def serve_about_page():
    return FileResponse(os.path.join(html_dir, "services.html"))
