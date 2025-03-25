from fastapi import APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse, JSONResponse
from PIL import Image
import io
import numpy as np
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr
from utils import reconstruct_image, transform

router = APIRouter()

@router.post("/reconstruct/")
async def reconstruct(file: UploadFile = File(...)):
    """Receives an image, reconstructs it using the model, and returns the result."""
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    
    # Preprocess & Reconstruct
    input_tensor = transform(image)
    reconstructed = reconstruct_image(input_tensor)

    # Save the reconstructed image using matplotlib
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.imshow(reconstructed, cmap="gray")
    ax.axis("off")

    img_io = io.BytesIO()
    plt.savefig(img_io, format="png", bbox_inches="tight", pad_inches=0)
    img_io.seek(0)

    return StreamingResponse(img_io, media_type="image/png")


@router.post("/metrics/")
async def get_metrics(file: UploadFile = File(...)):
    """Returns SSIM & PSNR values separately."""
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    
    # Preprocess & Reconstruct
    input_tensor = transform(image)
    reconstructed = reconstruct_image(input_tensor)

    # Compute SSIM & PSNR
    original = np.array(image.convert("L"))  # Ensure grayscale
    ssim_value = ssim(original, reconstructed, data_range=original.max() - original.min())
    psnr_value = psnr(original, reconstructed, data_range=original.max() - original.min())

    return JSONResponse(content={"ssim": round(ssim_value, 4), "psnr": round(psnr_value, 2)})