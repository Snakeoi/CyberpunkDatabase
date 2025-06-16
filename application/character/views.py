from flask import request, jsonify
from flask.views import MethodView
from application import models
from application.utils import CommonCRUD
from application.utils.decorators import handle_ma_validation_errors
from application.utils.schema_serialization import serialize_schema


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
        return CommonCRUD.post(
            payload_schema=models.Character.post_schema(),
            model=models.Character,
            data=request.json,
            response_schema=models.Character.get_one_schema(),
        )

class CharacterDetailView(MethodView):
    decorators = [handle_ma_validation_errors]

    def get(self, ind):
        return CommonCRUD.get_one(
            response_schema=models.Character.get_one_schema(),
            query=models.Character.query.filter_by(id=ind),
        )

    def patch(self, ind):
        return CommonCRUD.patch(
            payload_schema=models.Character.patch_schema(),
            query=models.Character.query.filter_by(id=ind),
            data=request.json,
            response_schema=models.Character.get_one_schema(),
        )

    def delete(self, ind):
        return CommonCRUD.delete(
            query=models.Character.query.filter_by(id=ind),
        )

