from application.extensions import ma
from marshmallow import validates, ValidationError


class CharacterGeneratorSchema(ma.SQLAlchemyAutoSchema):
    role = ma.String(required=True)

    @validates("role")
    def validate_role(self, value, data_key):
        allowed_roles = [
            "rocker",
            "solo",
            "netrunner",
            "tech",
            "medic",
            "media",
            "cop",
            "corp",
            "fixer",
            "nomad",
        ]
        if value not in allowed_roles:
            raise ValidationError(f"Unavailable role")