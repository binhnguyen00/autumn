import numpy;

from whisper import load_model, available_models, Whisper;

class WhisperService():
  model: Whisper

  def __init__(self):
    self.model = load_model("large-v3-turbo")
  
  def transcribe(self, audio: bytes) -> str:
    ndarray: numpy.ndarray = numpy.frombuffer(audio, dtype=numpy.int16)
    result: dict = self.model.transcribe(audio=ndarray)
    if (not result.get("text", False)):
      raise Exception("Failed to transcribe audio")
    return result.get("text") # type: ignore