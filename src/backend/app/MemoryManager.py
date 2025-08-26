from openai.types.chat import ChatCompletionMessageParam;

class MemoryManager():
  conversation_history: list[ChatCompletionMessageParam]

  def __init__(self):
    self.conversation_history = []

  def get_conversation_history(self) -> list[ChatCompletionMessageParam]:
    return self.conversation_history