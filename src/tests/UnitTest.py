import os;
import json;
import unittest;

from whisper import Whisper, load_model;

class UnitTest(unittest.TestCase):
  model: Whisper
  audio_dir: str

  @classmethod
  def setUpClass(cls):
    cls.model     = load_model(name="large")
    cls.audio_dir = os.path.join(os.path.dirname(__file__), "audio")

  def test_simple_vietnamese(self):
    result: dict = self.model.transcribe(f"{self.audio_dir}/vietnamese-song.mp3")
    print(json.dumps(result.get("text"), indent=2, ensure_ascii=False))
    self.assertTrue(result.get("text", False))

  def test_complex_vietnamese(self):
    result: dict = self.model.transcribe(f"{self.audio_dir}/vietnamese.mp3")
    print(json.dumps(result.get("text"), indent=2, ensure_ascii=False))
    self.assertTrue(result.get("text", False))

  def test_english(self):
    result: dict = self.model.transcribe(f"{self.audio_dir}/english.mp3")
    print(json.dumps(result.get("text"), indent=2, ensure_ascii=False))
    self.assertTrue(result.get("text", False))

if (__name__ == "__main__"):
  unittest.main()