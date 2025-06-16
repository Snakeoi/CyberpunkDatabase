from flask import Blueprint
from . import views

role = Blueprint('role', __name__, url_prefix='/api')

role.add_url_rule('/role/', view_func=views.RoleIndexView.as_view('role_index'))
role.add_url_rule('/role/<int:ind>/', view_func=views.RoleDetailView.as_view('role_detail'))
role.add_url_rule('/character/<int:ind>/role/', view_func=views.CharacterRoleIndexView.as_view('character_role_index'))
role.add_url_rule('/character/<int:ind>/role/<int:role_id>/',
                  view_func=views.CharacterRoleDetailView.as_view('character_role_detail'))
role.add_url_rule('/character/role/schema/post',
                  view_func=views.CharacterRolePostSchemaView.as_view('character_role_post'))
role.add_url_rule('/character/role/schema/patch',
                  view_func=views.CharacterRolePatchSchemaView.as_view('character_role_patch'))
role.add_url_rule('/role/schema/post', view_func=views.RolePostSchemaView.as_view('role_post'))
role.add_url_rule('/role/schema/patch', view_func=views.RolePatchSchemaView.as_view('role_patch'))
