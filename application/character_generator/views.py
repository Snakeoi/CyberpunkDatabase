from flask.views import MethodView
from flask import request
from flask import jsonify
from application.extensions import db
from application.models import Character
from application.character_generator import utils
from .schemas import CharacterGeneratorSchema
from .utils.skills import SKILLS
from application.models import Skills
from application.models import CharacterSkills
from application.models import Role
from application.models import CharacterRole
from ..utils.decorators import handle_ma_validation_errors

ROLES_MAP = {
    'rocker': 'Rocker',
    'solo': 'Solo',
    'netrunner': 'Netrunner',
    'tech': 'Technik',
    'medic': 'Medyk',
    'media': 'Media',
    'cop': 'Stróż Prawa',
    'corp': 'Korpo',
    'fixer': 'Fixer',
    'nomad': 'Nomada',
}


class CharacterGeneratorView(MethodView):

    decorators = [
        handle_ma_validation_errors
    ]

    def get(self):
        skill_names = set()
        for skill_set in SKILLS.values():
            for skill_name in skill_set:
                skill_names.add(skill_name[0])

        response = []
        for name in skill_names:
            if Skills.query.filter_by(name=name).first() is None:
                response.append(name)

        response = sorted(response)

        return jsonify(response)


    def post(self):
        request_data = request.get_json()
        data = CharacterGeneratorSchema().load(request_data)
        role = data["role"]

        fullname = utils.get_fullname()
        abilities = utils.get_abilities(role)
        armory = utils.get_armory(role)
        cybernetics = utils.get_cybernetics(role)
        inventory = utils.get_inventory(role)
        skills = utils.get_skills(role)
        skills.append(('Język - Angielski', 4))

        notes = ''

        notes += '<h2>Uzbrojenie</h2>'
        notes += '<ul>'
        for item in armory:
            notes += f'<li>{item}</li>'
        notes += '</ul>'

        notes += '<h2>Cybernetyka</h2>'
        notes += '<ul>'
        for item in cybernetics.implants:
            notes += f'<li>{item}</li>'
        notes += '</ul>'

        notes += '<h2>Przedmioty</h2>'
        notes += '<ul>'
        for item in inventory:
            notes += f'<li>{item}</li>'
        notes += '</ul>'

        character = Character(
            name = fullname,
            notes = notes,
            int = abilities['int'],
            ref = abilities['ref'],
            dex = abilities['dex'],
            tech = abilities['tech'],
            cool = abilities['cool'],
            will = abilities['will'],
            luck = abilities['luck'],
            move = abilities['move'],
            body = abilities['body'],
            emp_base = abilities['emp'],
            humanity = (abilities['emp'] * 10) - cybernetics.humanity_loss,
        )

        db.session.add(character)
        db.session.commit()

        character.health = character.health_base()
        db.session.commit()

        for skill in skills:
            skill_name = skill[0]
            skill_value = skill[1]
            character_skill = CharacterSkills(
                character_id = character.id,
                skill_id = Skills.query.filter_by(name=skill_name).first().id,
                level = skill_value
            )
            db.session.add(character_skill)

        db.session.commit()


        role = Role.query.filter_by(name=ROLES_MAP[role]).first()
        character_role = CharacterRole(
            character_id = character.id,
            role_id = role.id,
            level = 4,
        )
        db.session.add(character_role)
        db.session.commit()

        return {
            "character_id": character.id,
        }, 201


