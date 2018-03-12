from flask_wtf import FlaskForm
from wtforms import TextAreaField, PasswordField, StringField
from wtforms import validators

from wfdb.models import User


class CommentForm(FlaskForm):
    text = TextAreaField("text", validators=[
        validators.required(),
        validators.length(max=200)
    ])


class FormLogin(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired(), validators.Length(max=255)])
    password = PasswordField('Password', validators=[validators.DataRequired(), validators.Length(min=8)])

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

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired(),
                                                     validators.Length(max=255)])
    password = PasswordField('Password', validators=[validators.DataRequired(),
                                                     validators.Length(min=8)])
    confirm = PasswordField('Confirm', validators=[validators.DataRequired(),
                                                     validators.equal_to('password')])

    def validate(self):
        check_validate = super(FormLogin, self).validate()
        if not check_validate:
            return False

        user = User.query.filter_by(username=self.username.data).first()

        if user:
            self.username.errors.append('User with that name already exists')
            return False
        return True





