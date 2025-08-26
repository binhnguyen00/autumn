from fastapi import FastAPI;
from fastapi.logger import logger;
from fastapi.middleware.cors import CORSMiddleware;

from .RoutesManager import manager;

# ============================================
# application
# ============================================
logger.info("Loading FastAPI...")
app: FastAPI = FastAPI(title="Autumn", description="Autumn is a speech-to-text service", version="0.0.1")
app.add_middleware(
  CORSMiddleware,
  # allow_origins=["http://localhost:3000"],
  allow_credentials=True,
  allow_origins=["*"],
  allow_methods=["*"],
  allow_headers=["*"],
)
logger.info("FastAPI loaded successfully")

# ============================================
# register routes
# ============================================
app.include_router(manager.router)