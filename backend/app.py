from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from config import templates_dir, scripts_dir, images_dir
from routes.home import router as home_router
from routes.encrypt import router as encrypt_router
from routes.decrypt import router as decrypt_router
from routes.reconstruct import router as reconstruct_router

app = FastAPI()

# Mount static directories
app.mount("/templates", StaticFiles(directory=templates_dir), name="templates")
app.mount("/scripts", StaticFiles(directory=scripts_dir), name="scripts")
app.mount("/images", StaticFiles(directory=images_dir), name="images")

# Include routers
app.include_router(home_router)
app.include_router(encrypt_router)
app.include_router(decrypt_router)
app.include_router(reconstruct_router)
