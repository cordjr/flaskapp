import datetime

from flask import Flask, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import TextAreaField
from wtforms import validators
from logging.config import dictConfig


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = "86b03e6b-02a4-501f-bc27-5021c38d87a5"
db = SQLAlchemy(app)

tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)


class CommentForm(Form):
    text = TextAreaField("text", validators=[
        validators.required(),
        validators.length(max=200)
    ])


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    posts = db.relationship('Post', backref='user', lazy='dynamic')

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
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    tags = db.relationship('Tag', secondary=tags,
                           backref=db.backref('posts', lazy='dynamic'),
                           lazy='dynamic')


class Tag(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())


class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    text = db.Column(db.Text())
    date = db.Column(db.DateTime())
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user = db.relationship(User)


blog_blueprint = Blueprint('blog',
                           __name__,
                           template_folder="templates/blog",
                           url_prefix='/blog'
                           )
main_blueprint = Blueprint('main',
                           __name__,
                           template_folder="templates/main",
                           url_prefix='/main'
                           )


@main_blueprint.route("/")
def home():
    latest_movies = Movie.query.order_by(
        Movie.release_date.desc()
    ).limit(5).all()

    return render_template("main/index.html", latest_movies=latest_movies)


@main_blueprint.route("/actor/<int:actor_id>")
def actor(actor_id):
    actor = Actor.query.get_or_404(actor_id)

    return render_template("main/actor.html", actor=actor)


@main_blueprint.route("/movie/<int:movie_id>")
def movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    return render_template("main/movie.html", movie=movie)


@blog_blueprint.route("/")
def blog():
    posts = Post.query.order_by(Post.publish_date.desc()).all()

    return render_template("blog/blog.html", posts=posts)


@blog_blueprint.route("/<int:post_id>", methods=["GET", "POST"])
def post(post_id):
    post = Post.query.get_or_404(post_id)

    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment()
        comment.text = form.text.data
        comment.date = datetime.datetime.now()
        comment.post = post
        comment.user = User.query.get(1)

        db.session.add(comment)
        db.session.commit()

    return render_template("blog/post.html", post=post, form=form)


# def configure_log():
#     dictConfig({
#         'version': 1,
#         'formatters': {'default': {
#             'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
#         }},
#         'handlers': {'wsgi': {
#             'class': 'logging.StreamHandler',
#             'stream': 'ext://flask.logging.wsgi_errors_stream',
#             'formatter': 'default'
#         }},
#         'root': {
#             'level': 'INFO',
#             'handlers': ['wsgi']
#         }
#     })


if __name__ == "__main__":

    app.register_blueprint(main_blueprint)
    app.register_blueprint(blog_blueprint)

    app.run(debug=True)