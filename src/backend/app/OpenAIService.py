import os, json, openai;

from typing import Iterable, Optional;
from openai.types.chat import ChatCompletion, ChatCompletionMessageParam, ChatCompletionToolUnionParam;
from openai.types.chat.chat_completion_message import ChatCompletionMessage;

from .WeatherService import WeatherService;

class OpenAIService():
  client: openai.OpenAI
  model: str
  weather_service: WeatherService

  def __init__(self):
    self.model = "gpt-4.1-nano"
    self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if (not self.client.api_key):
      raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")

    self.weather_service = WeatherService()

  def chat(self, prompt: str, conversation_history: list[ChatCompletionMessageParam]) -> Optional[str]:
    tools: Iterable[ChatCompletionToolUnionParam] = self.available_tools()
    messages = conversation_history + [{"role": "user", "content": prompt}]

    response: ChatCompletion = self.client.chat.completions.create(
      model=self.model,
      messages=messages,
      tools=tools,
      function_call="auto"
    )
    message: ChatCompletionMessage = response.choices[0].message

    if (message.function_call):
      function_name: str = message.function_call.name
      function_args: dict = json.loads(message.function_call.arguments)

      if (function_name == "get_current_weather"):
        """ get weather result and send back to the model """
        result: dict = self.weather_service.get_current_weather(location=function_args.get("location", ""))
        
        follow_up: ChatCompletion = self.client.chat.completions.create(
          model=self.model,
          messages=messages + [
            {"role": "user", "content": prompt},
            {
              "role": "assistant", 
              "content": None,
              "function_call": {
                "name": function_name,
                "arguments": message.function_call.arguments
              }
            },
            {
              "role": "function",
              "name": function_name,
              "content": json.dumps(result)
            }
          ],
        )
        return follow_up.choices[0].message.content

    return message.content

  def available_tools(self) -> Iterable[ChatCompletionToolUnionParam]:
    return [
      {
        "type": "function",
        "function": {
          "name": "get_current_weather",
          "description": "Get the current weather for a given location",
          "parameters": {
            "type": "object",
            "properties": {
              "location": {
                "type": "string",
                "description": "The city and country, e.g., 'Hanoi, Vietnam'"
              }
            },
            "required": ["location"]
          }
        }
      }
    ]