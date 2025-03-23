from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, StreamingResponse
import torch
import matplotlib.pyplot as plt
import io
import os
from PIL import Image
from torchvision import transforms
from model import MedicalImageEncryptionModel  

app = FastAPI()

# Paths
FRONTEND_DIR = os.path.abspath("../frontend")  
BACKEND_DIR = os.path.abspath(".")
PROJECT_DIR = os.path.abspath("../")
REPO_DIR = os.path.abspath("../../")
MODEL_PATH = os.path.join(REPO_DIR, "NewMedicalImageEncryptionModel.pth")
ENCODED_FEATURES_DIR = os.path.join(PROJECT_DIR, "encoded_features")
os.makedirs(ENCODED_FEATURES_DIR, exist_ok=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load Model
model = MedicalImageEncryptionModel().to(device)
checkpoint = torch.load(MODEL_PATH, map_location=device)
model.load_state_dict(checkpoint["model_state"])
model.eval()

transform = transforms.Compose([transforms.Grayscale(), transforms.ToTensor()])

# Serve homepage with links to encrypt/decrypt
@app.get("/")
async def serve_home():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

# Serve encryption page
@app.get("/encrypt/")
async def serve_encrypt_page():
    return FileResponse(os.path.join(FRONTEND_DIR, "encrypt.html"))

# Serve decryption page
@app.get("/decrypt/")
async def serve_decrypt_page():
    return FileResponse(os.path.join(FRONTEND_DIR, "decrypt.html"))

def encrypt_image(image_tensor):
    with torch.no_grad():
        return model.encoder(image_tensor.unsqueeze(0).to(device)).squeeze(0).cpu()

def save_encoded_features(encoded_tensor, filename):
    save_path = os.path.join(ENCODED_FEATURES_DIR, f"{filename}.pt")
    torch.save(encoded_tensor, save_path)
    return save_path

def plot_images(original, encoded):
    fig, axes = plt.subplots(1, 2, figsize=(8, 4))
    axes[0].imshow(original.squeeze().cpu().numpy(), cmap="gray")
    axes[0].set_title("Original Image")
    axes[0].axis("off")
    axes[1].imshow(encoded.mean(dim=0).cpu().numpy(), cmap="gray")
    axes[1].set_title("Encoded Image")
    axes[1].axis("off")

    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format="png")
    plt.close(fig)
    img_bytes.seek(0)
    return img_bytes

@app.post("/encrypt/")
async def encrypt_image_api(file: UploadFile = File(...)):
    image = Image.open(file.file).convert("L")
    image_tensor = transform(image)
    encoded_tensor = encrypt_image(image_tensor)
    filename = f"encoded_{file.filename.split('.')[0]}"
    save_encoded_features(encoded_tensor, filename)
    img_bytes = plot_images(image_tensor, encoded_tensor)
    return StreamingResponse(img_bytes, media_type="image/png")

def decrypt(encoded_tensor):
    with torch.no_grad():
        return model.decoder(encoded_tensor.unsqueeze(0).to(device)).squeeze(0).cpu()

@app.post("/decrypt/")
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
