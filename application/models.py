import math
from enum import StrEnum
from sqlalchemy.orm import validates
from marshmallow import validate

from .extensions import db
from .extensions import ma

class AbilitiesEnum(StrEnum):
    int = 'int'
    ref = 'ref'
    dex = 'dex'
    tech = 'tech'
    cool = 'cool'
    will = 'will'
    luck = 'luck'
    move = 'move'
    body = 'body'
    emp = 'emp'

class Character(db.Model):
    __tablename__ = "character"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text, nullable=True)

    int = db.Column(db.Integer, nullable=False)
    ref = db.Column(db.Integer, nullable=False)
    dex = db.Column(db.Integer, nullable=False)
    tech = db.Column(db.Integer, nullable=False)
    cool = db.Column(db.Integer, nullable=False)
    will = db.Column(db.Integer, nullable=False)
    luck = db.Column(db.Integer, nullable=False)
    move = db.Column(db.Integer, nullable=False)
    body = db.Column(db.Integer, nullable=False)

    emp_base = db.Column(db.Integer, nullable=False)

    def humanity_base(self):
        return self.emp_base * 10

    humanity = db.Column(db.Integer, nullable=False)

    def emp_debuff(self):
        return self.emp_base - int(self.humanity / 10)

    def emp(self):
        return self.emp_base - self.emp_debuff()

    def health_base(self):
        return 10 + 5 * (math.ceil((self.will + self.body) / 2))

    health = db.Column(db.Integer, nullable=False, default=0)

    def serious_wounds(self):
        return math.ceil(self.health_base() / 2)

    def survivability(self):
        return self.body

    def character_roles_names(self):
        return ", ".join(
            [role.role.name for role in self.character_roles]
        )

    def get_balance(self):
        return sum(entry.amount for entry in self.bank_account_entries)

    def get_health_status(self):
        if self.health > 0:
            return f"{self.health}/{self.health_base()}"
        else:
            return "†"

    character_roles = db.relationship(
        'CharacterRole',
        back_populates='character',
        overlaps="role,character",
        cascade="all, delete-orphan",
    )
    character_skills = db.relationship(
        'CharacterSkills',
        back_populates='character',
        overlaps="skills,character",
        cascade="all, delete-orphan"
    )
    bank_account_entries = db.relationship(
        'BankAccountEntry',
        back_populates='character',
        overlaps="bank_account_entries,character",
        cascade="all, delete-orphan"
    )

    @classmethod
    def post_schema(cls) -> ma.SQLAlchemySchema:
        class CharacterPostSchema(ma.SQLAlchemySchema):
            class Meta:
                model = cls
                include_fk = True
                include_relationships = True

            name = ma.auto_field(required=True)
            notes = ma.auto_field(required=True)
            int = ma.auto_field(required=True)
            ref = ma.auto_field(required=True)
            dex = ma.auto_field(required=True)
            tech = ma.auto_field(required=True)
            cool = ma.auto_field(required=True)
            will = ma.auto_field(required=True)
            luck = ma.auto_field(required=True)
            move = ma.auto_field(required=True)
            body = ma.auto_field(required=True)
            humanity = ma.auto_field(required=True)
            emp_base = ma.auto_field(required=True)

        return CharacterPostSchema()

    @classmethod
    def patch_schema(cls) -> ma.SQLAlchemySchema:
        class CharacterPatchSchema(ma.SQLAlchemySchema):
            class Meta:
                model = cls
                include_fk = True
                include_relationships = True

            name = ma.auto_field()
            notes = ma.auto_field()
            int = ma.auto_field()
            ref = ma.auto_field()
            dex = ma.auto_field()
            tech = ma.auto_field()
            cool = ma.auto_field()
            will = ma.auto_field()
            luck = ma.auto_field()
            move = ma.auto_field()
            body = ma.auto_field()
            humanity = ma.auto_field()
            emp_base = ma.auto_field()
            health = ma.auto_field()

        return CharacterPatchSchema()

    @classmethod
    def get_one_schema(cls) -> ma.SQLAlchemySchema:
        class CharacterGetOneSchema(ma.SQLAlchemySchema):
            class Meta:
                model = cls
                load_instance = True
                include_fk = True
                include_relationships = True

            def get_humanity_base(self, obj):
                return cls.humanity_base(obj)

            def get_emp_debuff(self, obj):
                return cls.emp_debuff(obj)

            def get_emp(self, obj):
                return cls.emp(obj)

            def get_health_base(self, obj):
                return cls.health_base(obj)

            def get_serious_wounds(self, obj):
                return cls.serious_wounds(obj)

            def get_survivability(self, obj):
                return cls.survivability(obj)

            id = ma.auto_field()
            name = ma.auto_field()
            notes = ma.auto_field()
            int = ma.auto_field()
            ref = ma.auto_field()
            dex = ma.auto_field()
            tech = ma.auto_field()
            cool = ma.auto_field()
            will = ma.auto_field()
            luck = ma.auto_field()
            move = ma.auto_field()
            body = ma.auto_field()
            emp_base = ma.auto_field()
            humanity_base = ma.Method('get_humanity_base')
            humanity = ma.auto_field()
            emp_debuff = ma.Method('get_emp_debuff')
            emp = ma.Method('get_emp')
            health_base = ma.Method('get_health_base')
            serious_wounds = ma.Method('get_serious_wounds')
            survivability = ma.Method('get_survivability')
            health = ma.auto_field(required=True)

            character_roles = ma.Nested(CharacterRole.get_all_schema(), many=True)
            character_skills = ma.Nested(CharacterSkills.get_all_schema(), many=True)

        return CharacterGetOneSchema()

    @classmethod
    def get_all_schema(cls) -> ma.SQLAlchemySchema:
        class CharacterGetAllSchema(ma.SQLAlchemySchema):
            class Meta:
                model = cls
                load_instance = True
                include_fk = True
                include_relationships = True

            def get_character_roles_names(self, obj):
                return cls.character_roles_names(obj)

            def get_health_status(self, obj):
                return cls.get_health_status(obj)

            id = ma.auto_field()
            name = ma.auto_field()
            health_status = ma.Method('get_health_status')
            roles_list = ma.Method('get_character_roles_names')

        return CharacterGetAllSchema()

    @classmethod
    def get_balance_schema(cls) -> ma.SQLAlchemySchema:
        class CharacterBalanceSchema(ma.SQLAlchemySchema):
            class Meta:
                model = cls
                load_instance = True
                include_fk = True
                include_relationships = True

            def get_balance(self, obj):
                return obj.get_balance()

            id = ma.auto_field()
            balance = ma.Method('get_balance')

        return CharacterBalanceSchema()

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    special_ability = db.Column(db.String(50), nullable=False)

    character_roles = db.relationship(
        'CharacterRole',
        back_populates='role',
        overlaps="character,roles",
        cascade="all, delete-orphan"
    )

    @classmethod
    def get_one_schema(cls) -> ma.SQLAlchemySchema:
        class CharacterGetOneSchema(ma.SQLAlchemySchema):
            class Meta:
                model = cls
                load_instance = True
                include_fk = True
                include_relationships = True

            id = ma.auto_field()
            name = ma.auto_field()
            special_ability = ma.auto_field()

        return CharacterGetOneSchema()

    @classmethod
    def get_all_schema(cls) -> ma.SQLAlchemyAutoSchema:
        class CharacterGetAllSchema(ma.SQLAlchemyAutoSchema):
            class Meta:
                model = cls
                load_instance = True
                include_fk = True
                include_relationships = True

            id = ma.auto_field()
            name = ma.auto_field()
            special_ability = ma.auto_field()

        return CharacterGetAllSchema()

    @classmethod
    def post_schema(cls) -> ma.SQLAlchemySchema:
        class CharacterPostSchema(ma.SQLAlchemySchema):
            class Meta:
                model = cls
                include_fk = True
                include_relationships = True

            name = ma.auto_field(required=True)
            special_ability = ma.auto_field(required=True)

        return CharacterPostSchema()

    @classmethod
    def patch_schema(cls) -> ma.SQLAlchemySchema:
        class CharacterPatchSchema(ma.SQLAlchemySchema):
            class Meta:
                model = cls
                include_fk = True
                include_relationships = True

            name = ma.auto_field()
            special_ability = ma.auto_field()

        return CharacterPatchSchema()

class CharacterRole(db.Model):
    __tablename__ = "character_roles"
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    level = db.Column(db.Integer, nullable=False)

    character = db.relationship('Character', back_populates='character_roles', overlaps="roles,character")
    role = db.relationship('Role', back_populates='character_roles', overlaps="character,roles")

    @classmethod
    def get_all_schema(cls) -> ma.SQLAlchemySchema:
        class CharacterGetAllSchema(ma.SQLAlchemySchema):
            class Meta:
                model = cls
                load_instance = True
                include_fk = True
                include_relationships = True

            id = ma.auto_field()
            level = ma.auto_field()
            role = ma.Nested(Role.get_one_schema())

        return CharacterGetAllSchema()

    @classmethod
    def get_one_schema(cls) -> ma.SQLAlchemySchema:
        class CharacterGetAllSchema(ma.SQLAlchemySchema):
            class Meta:
                model = cls
                load_instance = True
                include_fk = True
                include_relationships = True

            id = ma.auto_field()
            level = ma.auto_field()
            role = ma.Nested(Role.get_one_schema())

        return CharacterGetAllSchema()

    @classmethod
    def post_schema(cls) -> ma.SQLAlchemySchema:
        class CharacterPostSchema(ma.SQLAlchemySchema):
            class Meta:
                model = cls
                include_fk = True
                include_relationships = True

            character_id = ma.auto_field(required=True)
            role_id = ma.auto_field(required=True)
            level = ma.auto_field(required=True)

        return CharacterPostSchema()

    @classmethod
    def patch_schema(cls) -> ma.SQLAlchemySchema:
        class CharacterPatchSchema(ma.SQLAlchemySchema):
            class Meta:
                model = cls
                include_fk = True
                include_relationships = True

            level = ma.auto_field()

        return CharacterPatchSchema()

class Skills(db.Model):
    __tablename__ = "skills"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    inherit = db.Column(db.String(50), nullable=False)
    cost_multiplier = db.Column(db.Integer, nullable=False)

    character_skills = db.relationship(
        'CharacterSkills',
        back_populates='skill',
        overlaps="character",
        cascade="all, delete-orphan"
    )

    @validates('inherit')
    def validate_inherit(self, key, value):
        if value not in AbilitiesEnum.__members__.values():
            raise ValueError(f"{value} is not a valid ability.")
        return value

    @classmethod
    def get_all_schema(cls) -> ma.SQLAlchemyAutoSchema:
        class SkillsGetAllSchema(ma.SQLAlchemyAutoSchema):
            class Meta:
                model = cls
                load_instance = True
                include_fk = True
                include_relationships = True

        return SkillsGetAllSchema()

    @classmethod
    def get_one_schema(cls) -> ma.SQLAlchemySchema:
        class SkillsGetAllSchema(ma.SQLAlchemySchema):
            class Meta:
                model = cls
                load_instance = True
                include_fk = True
                include_relationships = True

            id = ma.auto_field()
            name = ma.auto_field()
            inherit = ma.auto_field()
            cost_multiplier = ma.auto_field()

        return SkillsGetAllSchema()

    @classmethod
    def post_schema(cls) -> ma.SQLAlchemySchema:
        class SkillsPostSchema(ma.SQLAlchemySchema):
            class Meta:
                model = cls
                include_fk = True
                include_relationships = True

            name = ma.auto_field(required=True)
            inherit = ma.auto_field(required=True)
            cost_multiplier = ma.auto_field(required=True)

        return SkillsPostSchema()

    @classmethod
    def patch_schema(cls) -> ma.SQLAlchemySchema:
        class SkillsPatchSchema(ma.SQLAlchemySchema):
            class Meta:
                model = cls
                include_fk = True
                include_relationships = True

            name = ma.auto_field()
            inherit = ma.auto_field()
            cost_multiplier = ma.auto_field()

        return SkillsPatchSchema()

class CharacterSkills(db.Model):
    __tablename__ = "character_skills"
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), nullable=False)
    level = db.Column(db.Integer, nullable=False)

    character = db.relationship('Character', back_populates='character_skills', overlaps="skills,character")
    skill = db.relationship('Skills', back_populates='character_skills', overlaps="character,skills")

    def ability_level(self):
        attr =  getattr(self.character, self.skill.inherit)
        if type(attr) == int:
            return attr
        else:
            return attr()

    def base(self):

        return self.level + self.ability_level()

    @classmethod
    def get_all_schema(cls) -> ma.SQLAlchemyAutoSchema:
        class CharacterSkillsGetAllSchema(ma.SQLAlchemySchema):
            class Meta:
                model = cls
                load_instance = True
                include_fk = True
                include_relationships = True

            def get_ability_level(self, obj):
                return cls.ability_level(obj)

            def get_base(self, obj):
                return cls.base(obj)

            id = ma.auto_field()
            skill = ma.Nested(Skills.get_one_schema())
            level = ma.auto_field()
            ability_level = ma.Method('get_ability_level')
            base = ma.Method('get_base')


        return CharacterSkillsGetAllSchema()

    @classmethod
    def get_one_schema(cls) -> ma.SQLAlchemyAutoSchema:
        class CharacterSkillsGetAllSchema(ma.SQLAlchemySchema):
            class Meta:
                model = cls
                load_instance = True
                include_fk = True
                include_relationships = True

            def get_ability_level(self, obj):
                return cls.ability_level(obj)

            def get_base(self, obj):
                return cls.base(obj)

            id = ma.auto_field()
            skill = ma.Nested(Skills.get_one_schema())
            level = ma.auto_field()
            ability_level = ma.Method('get_ability_level')
            base = ma.Method('get_base')

        return CharacterSkillsGetAllSchema()

    @classmethod
    def post_schema(cls) -> ma.SQLAlchemySchema:
        class CharacterSkillsPostSchema(ma.SQLAlchemySchema):
            class Meta:
                model = cls
                include_fk = True
                include_relationships = True

            character_id = ma.auto_field(required=True)
            skill_id = ma.auto_field(required=True)
            level = ma.auto_field(required=True)

        return CharacterSkillsPostSchema()

    @classmethod
    def patch_schema(cls) -> ma.SQLAlchemySchema:
        class CharacterSkillsPatchSchema(ma.SQLAlchemySchema):
            class Meta:
                model = cls
                include_fk = True
                include_relationships = True

            level = ma.auto_field()

        return CharacterSkillsPatchSchema()

class BankAccountEntry(db.Model):
    __tablename__ = "bank_account_entries"
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=True)

    character = db.relationship('Character', back_populates='bank_account_entries', overlaps="bank_account_entries,character")

    @classmethod
    def get_all_schema(cls) -> ma.SQLAlchemySchema:
        class BankAccountEntryGetAllSchema(ma.SQLAlchemySchema):
            class Meta:
                model = cls
                load_instance = True
                include_fk = True
                include_relationships = True

            id = ma.auto_field()
            timestamp = ma.auto_field()
            amount = ma.auto_field()
            description = ma.auto_field()

        return BankAccountEntryGetAllSchema()

    @classmethod
    def get_one_schema(cls) -> ma.SQLAlchemySchema:
        class BankAccountEntryGetOneSchema(ma.SQLAlchemySchema):
            class Meta:
                model = cls
                load_instance = True
                include_fk = True
                include_relationships = True

            id = ma.auto_field()
            timestamp = ma.auto_field()
            amount = ma.auto_field()
            description = ma.auto_field()

        return BankAccountEntryGetOneSchema()

    @classmethod
    def post_schema(cls) -> ma.SQLAlchemySchema:
        class BankAccountEntryPostSchema(ma.SQLAlchemySchema):
            class Meta:
                model = cls
                include_fk = True
                include_relationships = True

            character_id = ma.auto_field(required=True)
            amount = ma.auto_field(required=True, validate=[
                validate.Range(min=-10000000000, max=10000000000),
                validate.NoneOf([0], error="Kwota nie może być zerem.")
            ])
            description = ma.auto_field()

        return BankAccountEntryPostSchema()

    @classmethod
    def patch_schema(cls) -> ma.SQLAlchemySchema:
        class BankAccountEntryPatchSchema(ma.SQLAlchemySchema):
            class Meta:
                model = cls
                include_fk = True
                include_relationships = True

            amount = ma.auto_field()
            description = ma.auto_field()

        return BankAccountEntryPatchSchema()