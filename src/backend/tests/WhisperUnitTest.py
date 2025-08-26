import os, unittest, warnings, sounddevice;

from unittest.case import skip;
from faster_whisper import WhisperModel, available_models;

class UnitTest(unittest.TestCase):
  model: WhisperModel
  audio_dir: str
  models: list[str]

  @classmethod
  def setUpClass(cls):
    warnings.filterwarnings("ignore")
    cls.models    = available_models()
    cls.model     = WhisperModel("large-v3-turbo", device="cpu")
    cls.audio_dir = os.path.join(os.path.dirname(__file__), "audio")
    print(f"Available models: {cls.models}")

  def test_simple_vietnamese(self):
    print(f"Testing simple vietnamese (interview)")
    segments, info = self.model.transcribe(f"{self.audio_dir}/vietnamese.mp3")
    self.assertIsNotNone(segments)
    for segment in segments:
      print(segment.text)

  def test_complex_vietnamese(self):
    print(f"Testing complex vietnamese (transcribe with music in background)")
    segments, info = self.model.transcribe(f"{self.audio_dir}/vietnamese-song.mp3")
    self.assertIsNotNone(segments)
    for segment in segments:
      print(segment.text)

  def test_english(self):
    print(f"Testing english (english conversation)")
    segments, info = self.model.transcribe(f"{self.audio_dir}/english.mp3")
    self.assertIsNotNone(segments)
    for segment in segments:
      print(segment.text)

  @skip("skip")
  def test_mic(self):
    print(f"Testing Mic")
    audio = sounddevice.rec()
    segments, info = self.model.transcribe(audio)
    self.assertIsNotNone(segments)
    for segment in segments:
      print(segment.text)

if (__name__ == "__main__"):
  unittest.main()