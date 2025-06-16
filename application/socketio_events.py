from flask_socketio import join_room
from .extensions import socketio


def register_socketio_events():
    @socketio.on('join_character')
    def on_join_character(data):
        character_id = data.get('character_id')
        if character_id:
            join_room(f'character_{character_id}')

