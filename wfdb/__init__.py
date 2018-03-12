from flask import Flask, redirect, url_for

from wfdb.models import db
from wfdb.controlers.blog import blog_blueprint
from wfdb.controlers.main import main_blueprint
from wfdb.extensions import login_manager


def create_app(config_obj: str) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_obj)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(blog_blueprint)

    db.init_app(app)
    return app


def index():
    return redirect(url_for("main.home"))


if __name__ == "__main__":
    app = create_app('wfdb.config.DevConfig')
    app.add_url_rule('/', 'index', index)
    login_manager.init_app(app)
    app.run()
