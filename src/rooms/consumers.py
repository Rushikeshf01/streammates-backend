import json
from channels.generic.websocket import AsyncWebsocketConsumer

class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_code = self.scope.get('url_route', {}).get(
                'kwargs').get('room_code')
        self.room_group_name = f'chat_{self.room_code}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    

    ''' this method receives a message (that user is wanting to broadcast) from websockets 
    to group and this consumer will send it to the appropriate consumer method to consume 
    the event based on "type" '''
    
    async def receive(self, text_data=None):
        text_data_json = json.loads(text_data)
        print('------------------>>>', text_data_json)
        message = text_data_json["message"]

        await self.channel_layer.group_send(self.room_group_name, text_data_json)

    '''this will receive the message from group, consume it and send it back
    to all connections of the group'''
    
    async def chat_message(self, event):
        message = event["message"]
        print('message received from other connection--------------=====', message, event)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({'type': 'chat_message', 'message': message, 'user': event['user']}))