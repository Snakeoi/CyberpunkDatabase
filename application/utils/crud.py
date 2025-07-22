from typing import Any

from flask import jsonify, abort
from marshmallow.exceptions import ValidationError

from application.extensions import db
from application.extensions import ma


class CommonCRUD:
    @classmethod
    def parse_shema_messages(cls, e: ValidationError) -> dict[str, list[str]]:
        """Parse validation error messages from Marshmallow."""
        return {'errors': [message for messages_set in e.messages.values() for message in messages_set]}

    @classmethod
    def get_all(cls, response_schema: "ma.Schema", query: "db.Query"):
        return jsonify(response_schema.dump(query.all(), many=True))

    @classmethod
    def get_one(cls, response_schema: "ma.Schema", query: "db.Query"):
        instance = query.one_or_none()
        if instance is None:
            abort(404)
        return jsonify(response_schema.dump(instance))

    @classmethod
    def post(cls, payload_schema: "ma.Schema", model: "db.Model",
             data: dict[str:Any], response_schema: "ma.Schema"=None):
        if response_schema is None:
            response_schema = payload_schema

        try:
            instance = model(**payload_schema.load(data))
        except ValidationError as e:
            return cls.parse_shema_messages(e), 400

        db.session.add(instance)
        db.session.commit()

        return jsonify(response_schema.dump(instance)), 201

    @classmethod
    def put(cls, payload_schema: "ma.Schema", query: "db.Query",
            data: dict[str:Any], response_schema: "ma.Schema"=None):
        if response_schema is None:
            response_schema = payload_schema
        instance = query.one_or_none()
        if instance is None:
            abort(404)
        try:
            data = payload_schema.load(data)
        except ValidationError as e:
            return cls.parse_shema_messages(e), 400
        for key in data.keys():
            setattr(instance, key, data[key])
        db.session.commit()
        return jsonify(response_schema.dump(instance))

    @classmethod
    def patch(cls, payload_schema: "ma.Schema", query: "db.Query",
              data: dict[str:Any], response_schema: "ma.Schema"=None):
        return cls.put(payload_schema, query, data, response_schema)

    @classmethod
    def delete(cls, query: "db.Query"):
        instances = query.all()
        if len(instances) == 0:
            abort(404)
        for instance in instances:
            db.session.delete(instance)
        db.session.commit()
        return jsonify(), 204
