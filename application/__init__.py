import os
import tomllib

from flask import Flask

from .extensions import setup_extensions
from .blueprints import setup_blueprints
from .injects import setup_injects
from . import utils
from .socketio_events import register_socketio_events

CONFIGS = {"basic": "config.toml", "testing": "config.test.toml"}


def create_app(mode="basic"):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["BASEDIR"] = os.path.abspath(os.path.dirname(__file__))

    setup_extensions(app)
    register_socketio_events()

    setup_injects(app)

    setup_blueprints(
        app,
        {
            "vue": ("vue",),
            "character": ("character",),
            "skill": ("skill",),
            "role": ("role",),
            "character_generator": ("character_generator",),
            "bank": ("bank",),
        },
    )

    app.add_url_rule("/map", view_func=utils.map.view)

    return app
