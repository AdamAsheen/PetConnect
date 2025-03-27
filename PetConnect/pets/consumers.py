import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

# Make sure we bring these in, so we can query the database
from django.contrib.auth.models import User
from pets.models import ChatRoom, Message

class ChatConsumer(WebsocketConsumer):
    """
    Handles websocket connections and receives messages from the client.
    """

    def connect(self):
        try:
            self.room_name = self.scope['url_route']['kwargs']['room_name']

            print(f"DEBUG: Trying to connect to room: {self.room_name}") 
            # Try to get the ChatRoom with primary key == room_name
            chat = ChatRoom.objects.get(chat_name=self.room_name)

            # Group name to use for Channels
            self.room_group_name = f"chat_{chat.id}"

            # Join the room group
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            self.accept()

        except ChatRoom.DoesNotExist as e:
            print(e)
            # If the room does not exist, we won't accept the connection
            self.close()

    def disconnect(self, close_code):
        # Leave the room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def new_message(self, data):
        """
        Create and save a new Message in the database, matching
        the fields of our 'Message' model.
        """
        chat_room_id = data["refChat"]   # e.g. "1"
        user_id = data["author"]         # e.g. "1"
        content = data["message"]        # The text typed by user

        # Fetch the ChatRoom, and the User
        chat_room = ChatRoom.objects.get(id=chat_room_id)
        user = User.objects.get(id=user_id)

        # Create and save the new Message
        msg = Message(
            chat_room=chat_room,
            sender=user,
            content=content
        )
        msg.save()

    def receive(self, text_data):
        """
        Called when the client sends a message via WebSocket.
        """
        data_json = json.loads(text_data)
        print("===Received===")
        print(data_json)

        # Save the message to the database
        self.new_message(data_json)

        # Then broadcast it to everyone in the same room
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',  # name of the method to call
                'message': data_json["message"]
            }
        )

    def chat_message(self, event):
        """
        Called when we get a 'chat_message' event from the group.
        """
        message = event['message']
        # Send it back to the browser via WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))