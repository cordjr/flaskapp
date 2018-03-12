from flask import render_template, Blueprint, flash, request, url_for, redirect
from flask_login import login_user, login_required

from wfdb.forms import FormLogin, RegisterForm
from wfdb.models import Actor, Movie, User, db

main_blueprint = Blueprint('main',
                           __name__,
                           template_folder="../templates/main",
                           url_prefix='/main'
                           )


@main_blueprint.route("/")
@login_required
def home():
    latest_movies = Movie.query.order_by(
        Movie.release_date.desc()
    ).limit(5).all()

    return render_template("index.html", latest_movies=latest_movies)


@main_blueprint.route("/actor/<int:actor_id>")
@login_required
def actor(actor_id):
    actor = Actor.query.get_or_404(actor_id)

    return render_template("actor.html", actor=actor)


@main_blueprint.route("/movie/<int:movie_id>")
@login_required
def movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    return render_template("movie.html", movie=movie)


@main_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = FormLogin()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data)
        login_user(user)
        flash("Logged with success!!", "success")
        return render_template(request.args.get("next") or url_for(".home"))

    return render_template("login.html", form=form)


@main_blueprint.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.password = form.username.data

        db.session.add(user)
        db.session.commit()
        flash("User has been created please login!!", category="")
        return redirect(url_for(".login"))
    return render_template("register.html", form=form)
