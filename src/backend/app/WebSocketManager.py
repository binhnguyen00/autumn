import json;

from fastapi import WebSocket;
from fastapi.logger import logger;

class WebSocketManager():
    def __init__(self):
      self.active_connections: list[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
      await websocket.accept()
      self.active_connections.append(websocket)
      logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")
  
    def disconnect(self, websocket: WebSocket):
      if (websocket in self.active_connections):
        self.active_connections.remove(websocket)
      logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")
    
    async def send_message(self, websocket: WebSocket, message: dict):
      try:
        await websocket.send_text(json.dumps(message))
      except Exception as e:
        logger.error(f"Error sending WebSocket message: {e}")