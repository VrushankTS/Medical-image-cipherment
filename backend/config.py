import os

FRONTEND_DIR = os.path.abspath("../frontend")
BACKEND_DIR = os.path.abspath(".")
PROJECT_DIR = os.path.abspath("../")

MODEL_PATH = os.path.join(PROJECT_DIR, "NewMedicalImageEncryptionModel.pth")
NEW_MODEL_PATH = os.path.join(PROJECT_DIR, "medical_image_encryption.pth")
ENCODED_FEATURES_DIR = os.path.join(PROJECT_DIR, "encoded_features")

os.makedirs(ENCODED_FEATURES_DIR, exist_ok=True)

scripts_dir = os.path.join(FRONTEND_DIR, "scripts")
templates_dir = os.path.join(FRONTEND_DIR, "templates")
images_dir = os.path.join(FRONTEND_DIR, "images")
html_dir = os.path.join(FRONTEND_DIR, "html")
# html_images_dir = os.path.join(html_dir, "images")
# html_js_dir = os.path.join(html_dir, "js")
# html_css_dir = os.path.join(html_dir, "css")