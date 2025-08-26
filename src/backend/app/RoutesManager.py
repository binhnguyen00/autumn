from typing import Optional;
from fastapi.logger import logger;
from fastapi import APIRouter, UploadFile, File, HTTPException, status;

from .WhisperService import WhisperService;
from .OpenAIService import OpenAIService;
from .MemoryManager import MemoryManager;

class RoutesManager():
  router: APIRouter
  whisper_service: WhisperService
  openai_service: OpenAIService
  memory_manager: MemoryManager

  def __init__(self):
    self.router = APIRouter()
    self.whisper_service = WhisperService()
    self.openai_service = OpenAIService()
    self.memory_manager = MemoryManager()

manager = RoutesManager()

@manager.router.get("/health")
async def health_check():
  return "healthy"

@manager.router.post("/audio")
async def audio_endpoint(audio: UploadFile = File(...)):
  conversation_history = manager.memory_manager.get_conversation_history()

  try:
    audio_data: bytes = await audio.read()
    transcript: str = manager.whisper_service.transcribe(audio_data)
    logger.info(f"Transcript: {transcript}")
    
    conversation_history.append({"role": "user", "content": transcript})
    
    response: Optional[str] = manager.openai_service.chat(transcript, conversation_history)
    if (response):
      conversation_history.append({"role": "assistant", "content": response})
    
    return {
      "status": "success",
      "response": response,
    }
  except Exception as e:
    logger.error(f"Error processing audio: {e}")
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail=f"Error processing audio: {str(e)}"
    )
