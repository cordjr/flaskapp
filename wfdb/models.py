from flask_sqlalchemy import SQLAlchemy
from flask_login.mixins import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash,

db = SQLAlchemy()

tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), unique=True)
    _password = db.Column(db.String(), name="password")
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    active = db.Column(db.Boolean)

    @property
    def is_active(self):
        return self.acttive

    def get_id(self):
        return self.id

    @property
    def password(self):
        return self._password

    @password.setter
    def set_password(self, value):
        self._password = generate_password_hash(value)

    def check_password(self, value):
        return check_password_hash(self._password, value)

    def __repr__(self):
        return f"<User({self.username})"


class Actor(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    birthday = db.Column(db.Date())
    deathday = db.Column(db.Date())
    hometown = db.Column(db.String())
    bio = db.Column(db.Text())
    picture = db.Column(db.String())
    roles = db.relationship("MovieRole", backref="actor")
    directorships = db.relationship('Movie', backref='director', lazy='dynamic')

    def __repr__(self):
        return f"<Actor({self.first_name} {self.last_name}"


class Movie(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String)
    release_date = db.Column(db.Date)
    director_id = db.Column(db.Integer, db.ForeignKey('actor.id'))
    summary = db.Column(db.Text)


class MovieRole(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    role_name = db.Column(db.String())
    movie = db.relationship('Movie', backref='cast')


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    text = db.Column(db.Text)
    publish_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    tags = db.relationship('Tag', secondary=tags,
                           backref=db.backref('posts', lazy='dynamic'),
                           lazy='dynamic')


class Tag(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())


class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.Text)
    date = db.Column(db.DateTime)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)
