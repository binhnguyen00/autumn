from whisper import load_model, available_models, Whisper;

class WhisperService():
  model: Whisper

  def __init__(self):
    self.model = load_model("large-v3-turbo")
  
  def transcribe(self, audio: bytes) -> str:
    pass