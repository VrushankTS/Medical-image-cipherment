from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse
import torch
import io
from torchvision import transforms
from utils import decrypt
from evals import device
from PIL import Image
import numpy as np

router = APIRouter()

@router.post("/decrypt/")
async def decrypt_image_api(file: UploadFile = File(...)):
    encoded_tensor = torch.load(file.file, map_location=device)
    if len(encoded_tensor.shape) == 2:
        encoded_tensor = encoded_tensor.unsqueeze(0)
    reconstructed_tensor = decrypt(encoded_tensor)
    reconstructed_image = transforms.ToPILImage()(reconstructed_tensor)

    img_bytes = io.BytesIO()
    reconstructed_image.save(img_bytes, format="PNG")
    img_bytes.seek(0)
    return StreamingResponse(img_bytes, media_type="image/png")


