from flask import request, jsonify
from flask.views import MethodView
from application import models
from application.utils import CommonCRUD
from application.utils.decorators import handle_ma_validation_errors
from application.utils.schema_serialization import serialize_schema
from application.extensions import socketio


class CharacterPostSchemaView(MethodView):
    decorators = [handle_ma_validation_errors]

    def get(self):
        return jsonify(serialize_schema(models.Character.post_schema()))

class CharacterPatchSchemaView(MethodView):
    decorators = [handle_ma_validation_errors]

    def get(self):
        return jsonify(serialize_schema(models.Character.patch_schema()))

class CharactersIndexView(MethodView):
    decorators = [handle_ma_validation_errors]

    def get(self):
        return CommonCRUD.get_all(
            response_schema=models.Character.get_all_schema(),
            query=models.Character.query
        )

    def post(self):
        response, status = CommonCRUD.post(
            payload_schema=models.Character.post_schema(),
            model=models.Character,
            data=request.json,
            response_schema=models.Character.get_one_schema(),
        )
        if status == 201:
            data = response.get_json()
            socketio.emit(
                "character_update",
                data,
                room=f"character_{data['id']}",
            )
        return response, status

class CharacterDetailView(MethodView):
    decorators = [handle_ma_validation_errors]

    def get(self, ind):
        return CommonCRUD.get_one(
            response_schema=models.Character.get_one_schema(),
            query=models.Character.query.filter_by(id=ind),
        )

    def patch(self, ind):
        print(request.json.get('humanity'))
        response = CommonCRUD.patch(
            payload_schema=models.Character.patch_schema(),
            query=models.Character.query.filter_by(id=ind),
            data=request.json,
            response_schema=models.Character.get_one_schema(),
        )
        socketio.emit(
            "character_update",
            models.Character.get_one_schema().dump(
                models.Character.query.get(ind)
            ),
            room=f"character_{ind}",
        )
        return response

    def delete(self, ind):
        return CommonCRUD.delete(
            query=models.Character.query.filter_by(id=ind),
        )

