from flask import Blueprint
from . import views

character_generator = Blueprint('character_generator', __name__, url_prefix='/api/character/generate')

character_generator.add_url_rule('/', view_func=views.CharacterGeneratorView.as_view('character_generator'))