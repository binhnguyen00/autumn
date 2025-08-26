import numpy, subprocess, pathlib, os;

from fastapi.logger import logger;
from faster_whisper import WhisperModel, available_models;
from faster_whisper.transcribe import Segment, TranscriptionInfo;

class WhisperService():
  model: WhisperModel

  def __init__(self):
    logger.info(f"Available models: {available_models()}")
    try:
      logger.info("Loading model...")
      model_dir: str = os.getenv("WHISPER_MODEL_DIR", "")
      if (not model_dir): 
        raise Exception("WHISPER_MODEL_DIR is not set")
      snapshots = pathlib.Path(model_dir)
      hash: str = ""
      for item in snapshots.iterdir():
        hash = item.name
        break

      self.model: WhisperModel = WhisperModel(f"{model_dir}/{hash}", device="cpu")
      logger.info("Model loaded successfully")
    except Exception as e:
      logger.error(f"Failed to load model: {e}")
      raise

  def transcribe(self, audio: bytes) -> str:
    try:
      audio_data = self.decode_audio_ffmpeg(audio, sr=16000)
      segments, info = self.model.transcribe(audio=audio_data, language="vi")
      segments_list: list[Segment] = list(segments)
      if (not segments_list):
        return ""
      return segments_list[0].text
    except Exception as e:
      logger.error(f"Error processing audio: {e}")
      raise

  def decode_audio_ffmpeg(self, audio_bytes: bytes, sr: int = 16000) -> numpy.ndarray:
    process = subprocess.Popen(
      ["ffmpeg", "-i", "pipe:0", "-f", "s16le", "-ac", "1", "-ar", str(sr), "pipe:1"],
      stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    out, _ = process.communicate(input=audio_bytes)
    return numpy.frombuffer(out, numpy.int16).astype(numpy.float32) / 32768.0