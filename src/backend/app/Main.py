from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File, HTTPException, status;
from fastapi.middleware.cors import CORSMiddleware;
from fastapi.logger import logger;

from .WhisperService import WhisperService;
from .WebSocketManager import WebSocketManager;

# ============================================
# services
# ============================================
whisper_service   = WhisperService()
websocket_manager = WebSocketManager()

# ============================================
# FastAPI
# ============================================
app: FastAPI = FastAPI(title="Autumn", description="Autumn is a speech-to-text service", version="0.0.1")
app.add_middleware(
  CORSMiddleware,
  # allow_origins=["http://localhost:3000"],
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# ============================================
# routes
# ============================================
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
  await websocket_manager.connect(websocket)
  try:
    while True:
      audio_data = await websocket.receive_bytes()
      await process_audio_pipeline(websocket, audio_data)

  except WebSocketDisconnect:
    websocket_manager.disconnect(websocket)

async def process_audio_pipeline(websocket: WebSocket, audio_data: bytes):
  """Main processing pipeline for audio to commerce response"""
  try:
    await websocket_manager.send_message(websocket, {
      "type": "status", 
      "message": "Transcribing audio..."
    })
    transcript = whisper_service.transcribe(audio_data)
    await websocket_manager.send_message(websocket, {
      "type": "transcript", 
      "text": transcript
    })

    # TODO: implement openai api function call

    await websocket_manager.send_message(websocket, {
      "type": "response",
      "data": None
    })
  except Exception as e:
    logger.error(f"Error in processing pipeline: {e}")
    await websocket_manager.send_message(websocket, {
      "type": "error",
      "message": str(e)
    })

@app.get("/health")
async def health_check():
  return "healthy"

@app.post("/api/audio")
async def audio_endpoint(audio: UploadFile = File(...)):
  try:
    audio_data: bytes = await audio.read()
    transcript: str = whisper_service.transcribe(audio_data)
    logger.info(f"Transcript: {transcript}")
    
    # TODO: Process the transcript with OpenAI API if needed
    
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