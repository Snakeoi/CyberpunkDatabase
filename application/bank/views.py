from flask import request, jsonify
from flask.views import MethodView
from application import models
from application.utils.schema_serialization import serialize_schema
from application.utils import CommonCRUD

class BankAccountEntryPostSchemaView(MethodView):
    def get(self):
        return jsonify(serialize_schema(models.BankAccountEntry.post_schema()))

class BankAccountEntryCharacterIndexView(MethodView):
    def get(self, character_id):
        return CommonCRUD.get_all(
            response_schema=models.BankAccountEntry.get_all_schema(),
            query=models.BankAccountEntry.query.filter_by(character_id=character_id)
            .order_by(models.BankAccountEntry.timestamp.desc()),
        )

class BankAccountEntryIndexView(MethodView):
    def post(self):
        return CommonCRUD.post(
            payload_schema=models.BankAccountEntry.post_schema(),
            model=models.BankAccountEntry,
            data=request.json,
            response_schema=models.BankAccountEntry.get_one_schema(),
        )

class BankAccountEntryDetailView(MethodView):
    def get(self, ind):
        return CommonCRUD.get_one(
            response_schema=models.BankAccountEntry.get_one_schema(),
            query=models.BankAccountEntry.query.filter_by(id=ind),
        )

    def patch(self, ind):
        return CommonCRUD.patch(
            payload_schema=models.BankAccountEntry.patch_schema(),
            query=models.BankAccountEntry.query.filter_by(id=ind),
            data=request.json,
            response_schema=models.BankAccountEntry.get_one_schema(),
        )

    def delete(self, ind):
        return CommonCRUD.delete(
            query=models.BankAccountEntry.query.filter_by(id=ind)
        )

class BankAccountBalanceView(MethodView):
    def get(self, character_id):
        return CommonCRUD.get_one(
            response_schema=models.Character.get_balance_schema(),
            query=models.Character.query.filter_by(id=character_id),
        )