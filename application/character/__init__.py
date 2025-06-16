from flask import Blueprint
from . import views

character = Blueprint('character', __name__, url_prefix='/api')

character.add_url_rule('/character/schema/post', view_func=views.CharacterPostSchemaView.as_view('post_schema'))
character.add_url_rule('/character/schema/patch', view_func=views.CharacterPatchSchemaView.as_view('put_schema'))
character.add_url_rule('/character/', view_func=views.CharactersIndexView.as_view('character_index'))
character.add_url_rule('/character/<int:ind>/', view_func=views.CharacterDetailView.as_view('character_detail'))
