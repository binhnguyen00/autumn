class WeatherService():

  def get_current_weather(self, location: str) -> dict:
    """ mock """
    return {
      "location": location,
      "temperature": "24°C",
      "condition": "Sunny"
    }