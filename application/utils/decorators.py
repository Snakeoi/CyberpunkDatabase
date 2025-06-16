from functools import wraps

from flask import jsonify
from marshmallow import ValidationError


def handle_ma_validation_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as err:
            errors = []
            for field, messages in err.messages.items():
                for message in messages:
                    errors.append(f"{field}: {message}")
            return jsonify({"errors": errors}), 400

    return wrapper
