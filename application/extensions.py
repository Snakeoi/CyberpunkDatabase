"""Initialize any app extensions."""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

def setup_extensions(app):
    app.json.ensure_ascii = False
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

