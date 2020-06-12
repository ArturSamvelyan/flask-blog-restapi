from flask import Flask

from .config import app_config
from .models import db, bcrypt

from .views.UserView import user_api as user_blueprint
from .views.BlogpostView import blogpost_api as blogpost_blueprint

from flask_cors import CORS

def create_app(env_name):
    app = Flask(__name__)
    cors = CORS(app, response={"/*": {"origins": "*"}})

    app.config.from_object(app_config[env_name])

    bcrypt.init_app(app)
    db.init_app(app)

    app.register_blueprint(user_blueprint, url_prefix='/users')
    app.register_blueprint(blogpost_blueprint, url_prefix='/blogposts')

    @app.route('/', methods=['GET'])
    def index():
        return "It works!"

    return app
