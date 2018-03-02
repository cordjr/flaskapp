from flask_login import LoginManager
from wfdb.models import User

login_manager = LoginManager()
login_manager.login_view = "main.login"


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)
