import datetime

from flask import render_template, Blueprint
from flask_login import login_required

from wfdb.models import Post, db, Comment, User





blog_blueprint = Blueprint('blog',
                           __name__,
                           template_folder="../templates/blog",
                           url_prefix='/blog'
                           )


@blog_blueprint.route("/")
@login_required
def blog():
    posts = Post.query.order_by(Post.publish_date.desc()).all()

    return render_template("blog.html", posts=posts)


@blog_blueprint.route("/<int:post_id>", methods=["GET", "POST"])
@login_required
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
        form.text.data = ""

    return render_template("blog/post.html", post=post, form=form)
