from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer


class BoardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'draw',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            'draw',
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        await self.channel_layer.group_send(
            'draw',
            {
                'type': 'chat_message',
                'data': text_data,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        data = event['data']

        # Send message to WebSocket
        await self.send(text_data=data)
