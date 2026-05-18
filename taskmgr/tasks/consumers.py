import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class TaskConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        if user.is_anonymous:
            await self.close(); return
        self.group = f'tasks_{user.id}'
        await self.channel_layer.group_add(self.group, self.channel_name)
        await self.accept()
    async def disconnect(self, code):
        if hasattr(self,'group'):
            await self.channel_layer.group_discard(self.group, self.channel_name)
    async def task_event(self, event):
        await self.send_json({'action':event['action'],'task':event['task']})
