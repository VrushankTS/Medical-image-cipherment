import torch
from model import MedicalImageEncryptionModel
from new_model import NewMedicalImageEncryptionModel
from config import MODEL_PATH, NEW_MODEL_PATH

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = MedicalImageEncryptionModel().to(device)
checkpoint = torch.load(MODEL_PATH, map_location=device)
model.load_state_dict(checkpoint["model_state"])
model.eval()

new_model = NewMedicalImageEncryptionModel().to(device)
checkpoint = torch.load(NEW_MODEL_PATH, map_location=device)
new_model.load_state_dict(checkpoint)
new_model.eval()