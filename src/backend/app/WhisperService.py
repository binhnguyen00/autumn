import numpy, subprocess;

from fastapi.logger import logger;
from whisper import load_model, available_models, Whisper;

class WhisperService():
  model: Whisper

  def __init__(self):
    logger.info(f"Available models: {available_models()}")
    self.model = load_model("large-v3-turbo")
  
  def transcribe(self, audio: bytes) -> str:
    try:
      audio_data = self.decode_audio_ffmpeg(audio, sr=16000)
      result: dict = self.model.transcribe(audio=audio_data)
      text: str = str(result.get("text", "")).strip()
      if not text:
        raise Exception("Failed to transcribe audio")
      return text
    except Exception as e:
      logger.error(f"Error processing audio: {e}")
      raise

  def transcribe_with_info(self, audio: bytes) -> dict:
    """Return full transcription info including timestamps and confidence"""
    try:
      audio_data = self.decode_audio_ffmpeg(audio, sr=16000)
      result = self.model.transcribe(audio=audio_data, word_timestamps=True)
      return {
        "text"      : str(result.get("text", "")).strip(),
        "language"  : result.get("language"),
        "segments"  : result.get("segments", []),
        "duration"  : len(audio_data) / 16000
      }

    except Exception as e:
      logger.error(f"Detailed transcription failed: {str(e)}")
      raise Exception(f"Failed to transcribe audio: {str(e)}")

  def decode_audio_ffmpeg(self, audio_bytes: bytes, sr: int = 16000) -> numpy.ndarray:
    process = subprocess.Popen(
      ["ffmpeg", "-i", "pipe:0", "-f", "s16le", "-ac", "1", "-ar", str(sr), "pipe:1"],
      stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    out, _ = process.communicate(input=audio_bytes)
    return numpy.frombuffer(out, numpy.int16).astype(numpy.float32) / 32768.0