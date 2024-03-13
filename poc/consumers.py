import json
from channels.generic.websocket import AsyncWebsocketConsumer


class LogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("log_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        self.channel_layer.group_discard("log_group", self.channel_name)

    async def log_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))
