from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

# Import your forms from the forms.py
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm

from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy import ForeignKey
import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("APP_SECRET_KEY")

# TODO: Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

ckeditor = CKEditor(app)
Bootstrap5(app)


# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy()
db.init_app(app)


# Commenter Image
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)

# CONFIGURE TABLES

# TODO: Create a User table for all your registered users. 
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(250))
    name = db.Column(db.String(250), unique=True)

    posts = relationship("BlogPost", back_populates="author")
    comments = relationship("Comment", back_populates="comment_author")
    
    def check_password(self, password):
        return check_password_hash(self.password, password)


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    author_id = mapped_column(ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")

    post_comments = relationship("Comment", back_populates="parent_post")

    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.Text, nullable=True)


class Comment(db.Model):
    __tablename__ = "comments" 
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)

    author_id = mapped_column(ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comments")
    
    post_id = mapped_column(ForeignKey("blog_posts.id"))
    parent_post = relationship("BlogPost", back_populates="post_comments")

with app.app_context():
    db.create_all()


# LOGIN DECORATOR
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

# ADMIN ONLY DECORATOR
def admin_only(function):
    @wraps(function)
    def wrapper_function(*args, **kwargs):
        if current_user.is_authenticated and int(current_user.id) == 1:
            return function(*args, **kwargs)
        else:
            return abort(403)      
    return wrapper_function    


# # TODO: Use Werkzeug to hash the user's password when creating a new user.
@app.route('/register', methods=["GET", "POST"])
def register():
    r_form = RegisterForm()
    if r_form.validate_on_submit():
        u_email=r_form.email.data
        if db.session.execute(db.select(User).where(User.email==u_email)).scalar():
            flash('Registration failed. This user already exists. Please login.')
            return redirect(url_for("login"))
        new_user = User(
        name=r_form.name.data,
        email=r_form.email.data,
        password = generate_password_hash(r_form.password.data, method='pbkdf2', salt_length=8) 
        )

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("get_all_posts"))

    return render_template("register.html", form=r_form)


# TODO: Retrieve a user from the database based on their email. 
@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u_email = form.email.data
        u_password = form.password.data
        u_user = db.session.execute(db.select(User).where(User.email==u_email)).scalar()

        if u_user:
            if check_password_hash(u_user.password, u_password):
                login_user(u_user)
                
                return redirect(url_for("get_all_posts"))
            else:
                flash('Login failed. The password is incorrect.')
                return render_template('login.html', form=form)
        else:
            flash('Login failed. Email user does not exist. Use the register link to sign up!')
    
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route('/')
def get_all_posts():
    posts = db.session.execute(db.select(BlogPost)).scalars().all()
    return render_template("index.html", all_posts=posts)


# TODO: Allow logged-in users to comment on posts
#@login_required
@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    # all_comments = db.session.execute(db.select(Comment).where(Comment.post_id==post_id)).scalars().all()
    # print("all_comments")
    # print("all_comments[0]")
    c_form = CommentForm() 
    if c_form.validate_on_submit():

        if current_user.is_authenticated:
            new_comment = Comment(
                text = c_form.comment_text.data,
                author_id=current_user.id,
                post_id=requested_post.id
            )
            db.session.add(new_comment)
            db.session.commit()
        else:
            flash('Login required to comment on a Post.')
            return redirect(url_for("login"))

    return render_template("post.html", post=requested_post, form=c_form)


# TODO: Use a decorator so only an admin user can create a new post
@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():          
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


# TODO: Use a decorator so only an admin user can edit a post
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)


# TODO: Use a decorator so only an admin user can delete a post
@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5002)
