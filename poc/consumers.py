import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class LogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        while True:
            await self.send(json.dumps({'message': 'Hello'}))
            await asyncio.sleep(1)

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.send(text_data=json.dumps({'message': message}))
