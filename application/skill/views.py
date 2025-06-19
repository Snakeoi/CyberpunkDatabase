from flask import request, jsonify
from flask.views import MethodView
from application import models
from application.utils import CommonCRUD
from application.utils.decorators import handle_ma_validation_errors
from application.utils.schema_serialization import serialize_schema
from application.extensions import socketio


class SkillPostSchemaView(MethodView):
    decorators = [handle_ma_validation_errors]

    def get(self):
        return jsonify(serialize_schema(models.Skills.post_schema()))

class SkillPatchSchemaView(MethodView):
    decorators = [handle_ma_validation_errors]

    def get(self):
        return jsonify(serialize_schema(models.Skills.patch_schema()))

class CharacterSkillPostSchemaView(MethodView):
    decorators = [handle_ma_validation_errors]

    def get(self):
        return jsonify(serialize_schema(models.CharacterSkills.post_schema()))

class CharacterSkillPatchSchemaView(MethodView):
    decorators = [handle_ma_validation_errors]

    def get(self):
        return jsonify(serialize_schema(models.CharacterSkills.patch_schema()))

class SkillIndexView(MethodView):
    decorators = [handle_ma_validation_errors]

    def get(self):
        return CommonCRUD.get_all(
            response_schema=models.Skills.get_one_schema(),
            query=models.Skills.query
        )

    def post(self):
        return CommonCRUD.post(
            payload_schema=models.Skills.post_schema(),
            model=models.Skills,
            data=request.json,
            response_schema=models.Skills.get_one_schema(),
        )

class SkillDetailView(MethodView):
    decorators = [handle_ma_validation_errors]

    def get(self, ind):
        return CommonCRUD.get_one(
            response_schema=models.Skills.get_one_schema(),
            query=models.Skills.query.filter_by(id=ind),
        )

    def patch(self, ind):
        return CommonCRUD.patch(
            payload_schema=models.Skills.patch_schema(),
            query=models.Skills.query.filter_by(id=ind),
            data=request.json,
            response_schema=models.Skills.get_one_schema(),
        )

    def delete(self, ind):
        return CommonCRUD.delete(
            query=models.Skills.query.filter_by(id=ind),
        )

class CharacterSkillIndexView(MethodView):
    decorators = [handle_ma_validation_errors]

    def get(self, ind):
        return CommonCRUD.get_all(
            response_schema=models.CharacterSkills.get_one_schema(),
            query=models.CharacterSkills.query.filter_by(character_id=ind),
        )

    def post(self, ind):
        response, status = CommonCRUD.post(
            payload_schema=models.CharacterSkills.post_schema(),
            model=models.CharacterSkills,
            data=request.json,
            response_schema=models.CharacterSkills.get_one_schema(),
        )
        if status == 201:
            socketio.emit(
                "character_update",
                models.Character.get_one_schema().dump(
                    models.Character.query.get(ind)
                ),
                room=f"character_{ind}",
            )
        return response, status

class CharacterSkillDetailView(MethodView):
    decorators = [handle_ma_validation_errors]

    def get(self, ind, skill_id):
        return CommonCRUD.get_one(
            response_schema=models.CharacterSkills.get_one_schema(),
            query=models.CharacterSkills.query.filter_by(character_id=ind, id=skill_id),
        )

    def patch(self, ind, skill_id):
        response = CommonCRUD.patch(
            payload_schema=models.CharacterSkills.patch_schema(),
            query=models.CharacterSkills.query.filter_by(character_id=ind, id=skill_id),
            data=request.json,
            response_schema=models.CharacterSkills.get_one_schema(),
        )
        socketio.emit(
            "character_update",
            models.Character.get_one_schema().dump(
                models.Character.query.get(ind)
            ),
            room=f"character_{ind}",
        )
        return response

    def delete(self, ind, skill_id):
        response, status = CommonCRUD.delete(
            query=models.CharacterSkills.query.filter_by(character_id=ind, id=skill_id),
        )
        if status == 204:
            socketio.emit(
                "character_update",
                models.Character.get_one_schema().dump(
                    models.Character.query.get(ind)
                ),
                room=f"character_{ind}",
            )
        return response, status
