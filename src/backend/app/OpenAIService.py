import os, json, openai;

from typing import Iterable, Optional;
from openai.types.chat import ChatCompletion, ChatCompletionMessageParam, ChatCompletionToolUnionParam;
from openai.types.chat.chat_completion_message import ChatCompletionMessage;

from .WeatherService import WeatherService;

class OpenAIService():
  client: openai.OpenAI
  weather_service: WeatherService

  def __init__(self):
    self.model = "gpt-4.1-nano"
    self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    self.weather_service = WeatherService()

  def chat(
    self, 
    prompt: str, 
    conversation_history: list[ChatCompletionMessageParam], 
    system_rule: Optional[str] = None
  ) -> Optional[str]:
    tools: Iterable[ChatCompletionToolUnionParam] = self.available_tools()
    all_messages: list[ChatCompletionMessageParam] = []
    system_message: ChatCompletionMessageParam = {
      "role": "system",
      "content": system_rule or "You are a helpful assistant."
    }
    has_system_message: bool = any(msg.get("role") == "system" for msg in conversation_history)
    if (system_rule and not has_system_message):
      all_messages.append(system_message)
      all_messages.extend(conversation_history)
      all_messages.append({"role": "user", "content": prompt})
    elif (not has_system_message):
      all_messages.append(system_message)
      all_messages.extend(conversation_history)
      all_messages.append({"role": "user", "content": prompt})
    else:
      all_messages.extend(conversation_history)
      all_messages.append({"role": "user", "content": prompt})

    response: ChatCompletion = self.client.chat.completions.create(
      model=self.model,
      messages=all_messages,
      tools=tools,
      tool_choice="auto",
      temperature=0.1
    )
    message: ChatCompletionMessage = response.choices[0].message

    if (message.tool_calls):
      tool_messages = [] # multiple tools call
      
      for tool_call in message.tool_calls:
        if (tool_call.type == "function"):
          function_name: str = tool_call.function.name
          function_args: dict = json.loads(tool_call.function.arguments)

        # TODO: Consider moving this logic to a separate service
        if (function_name == "get_current_weather"):
          result: dict = self.weather_service.get_current_weather(location=function_args.get("location", ""))
          tool_messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result)
          })

      if (tool_messages):
        assistant_message: ChatCompletionMessageParam = {
          "role": "assistant",
          "content": message.content,
          "tool_calls": [
            {
              "id": tool_call.id,
              "type": tool_call.type,
              "function": {
                "name": tool_call.function.name,
                "arguments": tool_call.function.arguments
              }
            } for tool_call in message.tool_calls if (tool_call.type == "function")
          ]
        }
        
        follow_up: ChatCompletion = self.client.chat.completions.create(
          model=self.model,
          messages=[
            *all_messages,
            assistant_message,
            *tool_messages
          ]
        )
        return follow_up.choices[0].message.content

    return message.content

  def available_tools(self) -> Iterable[ChatCompletionToolUnionParam]:
    return [
      {
        "type": "function",
        "function": {
          "name": "get_current_weather",
          "description": "Get the current weather for a specific location. Only call this function if the user has explicitly provided a location. If no location is provided, ask the user for their location first.",
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