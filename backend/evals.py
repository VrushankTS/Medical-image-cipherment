import torch
from model import MedicalImageEncryptionModel
from config import MODEL_PATH

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = MedicalImageEncryptionModel().to(device)
checkpoint = torch.load(MODEL_PATH, map_location=device)
model.load_state_dict(checkpoint["model_state"])
model.eval()
