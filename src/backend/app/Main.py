from fastapi import FastAPI, UploadFile, File, HTTPException, status;
from fastapi.middleware.cors import CORSMiddleware;
from fastapi.logger import logger;

from .WhisperService import WhisperService;
from .OpenAIService import OpenAIService;

# ============================================
# components scan
# ============================================
whisper_service = WhisperService()
openai_service = OpenAIService()

# ============================================
# FastAPI
# ============================================
app: FastAPI = FastAPI(title="Autumn", description="Autumn is a speech-to-text service", version="0.0.1")
app.add_middleware(
  CORSMiddleware,
  # allow_origins=["http://localhost:3000"],
  allow_credentials=True,
  allow_origins=["*"],
  allow_methods=["*"],
  allow_headers=["*"],
)
conversation_history = [] # TODO: repalce with actual database

# ============================================
# routes
# ============================================
@app.get("/health")
async def health_check():
  return "healthy"

@app.post("/audio")
async def audio_endpoint(audio: UploadFile = File(...)):
  global conversation_history

  try:
    audio_data: bytes = await audio.read()
    transcript: str = whisper_service.transcribe(audio_data)
    logger.info(f"Transcript: {transcript}")
    
    conversation_history.append({"role": "user", "content": transcript})
    
    return {
      "status": "success",
      "transcript": transcript,
      "message": "Audio processed successfully"
    }
  except Exception as e:
    logger.error(f"Error processing audio: {e}")
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail=f"Error processing audio: {str(e)}"
    )