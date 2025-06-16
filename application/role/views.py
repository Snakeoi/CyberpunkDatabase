from flask import request, jsonify
from flask.views import MethodView
from application import models
from application.utils import CommonCRUD
from application.utils.decorators import handle_ma_validation_errors
from application.utils.schema_serialization import serialize_schema


class RolePostSchemaView(MethodView):
    decorators = [handle_ma_validation_errors]

    def get(self):
        return jsonify(serialize_schema(models.Role.post_schema()))

class RolePatchSchemaView(MethodView):
    decorators = [handle_ma_validation_errors]

    def get(self):
        return jsonify(serialize_schema(models.Role.patch_schema()))

class CharacterRolePostSchemaView(MethodView):
    decorators = [handle_ma_validation_errors]

    def get(self):
        return jsonify(serialize_schema(models.CharacterRole.post_schema()))

class CharacterRolePatchSchemaView(MethodView):
    decorators = [handle_ma_validation_errors]

    def get(self):
        return jsonify(serialize_schema(models.CharacterRole.patch_schema()))

class RoleIndexView(MethodView):
    decorators = [handle_ma_validation_errors]

    def get(self):
        return CommonCRUD.get_all(
            response_schema=models.Role.get_one_schema(),
            query=models.Role.query
        )

    def post(self):
        return CommonCRUD.post(
            payload_schema=models.Role.post_schema(),
            model=models.Role,
            data=request.json,
            response_schema=models.Role.get_one_schema(),
        )

class RoleDetailView(MethodView):
    decorators = [handle_ma_validation_errors]

    def get(self, ind):
        return CommonCRUD.get_one(
            response_schema=models.Role.get_one_schema(),
            query=models.Role.query.filter_by(id=ind),
        )

    def patch(self, ind):
        return CommonCRUD.patch(
            payload_schema=models.Role.patch_schema(),
            query=models.Role.query.filter_by(id=ind),
            data=request.json,
            response_schema=models.Role.get_one_schema(),
        )

    def delete(self, ind):
        return CommonCRUD.delete(
            query=models.Role.query.filter_by(id=ind),
        )

class CharacterRoleIndexView(MethodView):
    decorators = [handle_ma_validation_errors]

    def get(self, ind):
        return CommonCRUD.get_all(
            response_schema=models.CharacterRole.get_one_schema(),
            query=models.CharacterRole.query.filter_by(character_id=ind)
        )

    def post(self, ind):
        return CommonCRUD.post(
            payload_schema=models.CharacterRole.post_schema(),
            model=models.CharacterRole,
            data=request.json,
            response_schema=models.CharacterRole.get_one_schema(),
        )

class CharacterRoleDetailView(MethodView):
    decorators = [handle_ma_validation_errors]

    def get(self, ind, role_id):
        print(models.CharacterRole.query.filter_by(character_id=ind, id=role_id).all())
        return CommonCRUD.get_one(
            response_schema=models.CharacterRole.get_one_schema(),
            query=models.CharacterRole.query.filter_by(character_id=ind, id=role_id),
        )

    def patch(self, ind, role_id):
        return CommonCRUD.patch(
            payload_schema=models.CharacterRole.patch_schema(),
            query=models.CharacterRole.query.filter_by(character_id=ind, id=role_id),
            data=request.json,
            response_schema=models.CharacterRole.get_one_schema(),
        )

    def delete(self, ind, role_id):
        return CommonCRUD.delete(
            query=models.CharacterRole.query.filter_by(character_id=ind, id=role_id),
        )