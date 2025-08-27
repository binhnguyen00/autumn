import numpy, subprocess;

from typing import Literal;
from fastapi.logger import logger;
from faster_whisper import WhisperModel, available_models;
from faster_whisper.transcribe import Segment, TranscriptionInfo;
from huggingface_hub import snapshot_download;

class WhisperService():
  model: WhisperModel

  def __init__(self):
    logger.info(f"Available models: {available_models()}")
    try:
      path = snapshot_download("mobiuslabsgmbh/faster-whisper-large-v3-turbo")
      self.model = WhisperModel(path, device="cpu")
    except Exception as e:
      logger.error(f"Failed to load model: {e}")
      raise

  def transcribe(self, audio: bytes, language: Literal["vi", "en"] = "vi") -> str:
    try:
      audio_data = self.decode_audio_ffmpeg(audio, sr=16000)
      segments, info = self.model.transcribe(audio=audio_data, language=language)
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