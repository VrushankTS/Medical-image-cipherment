import torch
import matplotlib.pyplot as plt
import io
import os
import numpy as np
from torchvision import transforms
from config import ENCODED_FEATURES_DIR
from evals import model, new_model, device

transform = transforms.Compose([transforms.Grayscale(), transforms.ToTensor()])

def encrypt_image(image_tensor):
    with torch.no_grad():
        return model.encoder(image_tensor.unsqueeze(0).to(device)).squeeze(0).cpu()

def decrypt(encoded_tensor):
    with torch.no_grad():
        return model.decoder(encoded_tensor.unsqueeze(0).to(device)).squeeze(0).cpu()

def save_encoded_features(encoded_tensor, filename):
    save_path = os.path.join(ENCODED_FEATURES_DIR, f"{filename}.pt")
    torch.save(encoded_tensor, save_path)
    return save_path

def plot_encoded_image(encoded):
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.imshow(encoded.mean(dim=0).cpu().numpy(), cmap="gray")
    ax.axis("off")

    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format="png", bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    img_bytes.seek(0)
    return img_bytes


def reconstruct_image(image_tensor):
    """Reconstructs the image using the model."""
    with torch.no_grad():
        reconstructed, _, _, _, _ = new_model(image_tensor)
    reconstructed = reconstructed.squeeze().cpu().numpy()
    return (reconstructed * 255).astype(np.uint8)