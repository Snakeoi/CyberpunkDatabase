from flask import Blueprint
from . import views

skill = Blueprint('skill', __name__, url_prefix='/api')

skill.add_url_rule('/skill/', view_func=views.SkillIndexView.as_view('skill_index'))
skill.add_url_rule('/skill/<int:ind>/', view_func=views.SkillDetailView.as_view('skill_detail'))
skill.add_url_rule('/character/<int:ind>/skill/',
                   view_func=views.CharacterSkillIndexView.as_view('character_skill_index'))
skill.add_url_rule('/character/<int:ind>/skill/<int:skill_id>/',
                   view_func=views.CharacterSkillDetailView.as_view('character_skill_detail'))
skill.add_url_rule('/character/skill/schema/post',
                   view_func=views.CharacterSkillPostSchemaView.as_view('character_skill_post'))
skill.add_url_rule('/character/skill/schema/patch',
                   view_func=views.CharacterSkillPatchSchemaView.as_view('character_skill_patch'))
skill.add_url_rule('/skill/schema/post', view_func=views.SkillPostSchemaView.as_view('skill_post'))
skill.add_url_rule('/skill/schema/patch', view_func=views.SkillPatchSchemaView.as_view('skill_patch'))
