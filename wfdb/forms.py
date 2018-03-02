from flask_wtf import FlaskForm
from wtforms import TextAreaField, PasswordField
from wtforms import validators
from wfdb.models import User


class CommentForm(FlaskForm):
    text = TextAreaField("text", validators=[
        validators.required(),
        validators.length(max=200)
    ])


class FormLogin(FlaskForm):
    username = TextAreaField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])

    def validate(self):
        check_validate = super(FormLogin, self).validate()
        if not check_validate:
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append("Invalid username")
            return False
        if not user.check_password(self.password.data.strip()):
            self.password.errors.append("Invalid password")
            return False
        return True
