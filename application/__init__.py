import os
import tomllib

from flask import Flask

from .extensions import setup_extensions
from .blueprints import setup_blueprints
from .injects import setup_injects
from . import utils
from .socketio_events import register_socketio_events
from .middleware import update_user_last_seen

CONFIGS = {"basic": "config.toml", "testing": "config.test.toml"}


def create_app(mode="basic"):
    app = Flask(__name__)

    app.config.from_file(f"../configs/{CONFIGS[mode]}", load=tomllib.load, text=False)

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["BASEDIR"] = os.path.abspath(os.path.dirname(__file__))

    setup_extensions(app)
    register_socketio_events()

    setup_injects(app)

    @app.before_request
    def after_request():
        update_user_last_seen()

    setup_blueprints(
        app,
        {
            "vue": ("vue",),
            "user": ("user_auth", "user_api"),
            "character": ("character",),
            "skill": ("skill",),
            "role": ("role",),
            "character_generator": ("character_generator",),
            "bank": ("bank",),
            "docs": ("docs",),
        },
    )

    app.add_url_rule("/map", view_func=utils.map.view)

    return app
