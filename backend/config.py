import os

FRONTEND_DIR = os.path.abspath("../frontend")
BACKEND_DIR = os.path.abspath(".")
PROJECT_DIR = os.path.abspath("../")

MODEL_PATH = os.path.join(PROJECT_DIR, "NewMedicalImageEncryptionModel.pth")
ENCODED_FEATURES_DIR = os.path.join(PROJECT_DIR, "encoded_features")

os.makedirs(ENCODED_FEATURES_DIR, exist_ok=True)

scripts_dir = os.path.join(FRONTEND_DIR, "scripts")
templates_dir = os.path.join(FRONTEND_DIR, "templates")
