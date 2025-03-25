from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse
from PIL import Image
from utils import encrypt_image, save_encoded_features, plot_encoded_image, transform

router = APIRouter()

@router.post("/encrypt/")
async def encrypt_image_api(file: UploadFile = File(...)):
    image = Image.open(file.file).convert("L")
    image_tensor = transform(image)
    encoded_tensor = encrypt_image(image_tensor)
    filename = f"encoded_{file.filename.split('.')[0]}"
    save_encoded_features(encoded_tensor, filename)
    img_bytes = plot_encoded_image(encoded_tensor)
    return StreamingResponse(img_bytes, media_type="image/png")
