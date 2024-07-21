from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory, abort
from django.utils.http import url_has_allowed_host_and_scheme
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

import os
from dotenv import load_dotenv

load_dotenv()

# CREATE APP WITH LOGIN MANAGER
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("APP_SECRET_KEY")

login_manager = LoginManager()
login_manager.init_app(app)


# LOGIN DECORATOR
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy()
db.init_app(app)


# CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
 
    def check_password(self, password):
        return check_password_hash(self.password, password)
    

with app.app_context():
    db.create_all()



# HOME PAGE
@app.route('/')
def home():
    return render_template("index.html")


# USER REGISTRATION PAGE
@app.route('/register', methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        new_user = User()
        new_user.email = request.form.get("email")
        new_user.name = request.form.get("name")
        new_user.password = generate_password_hash(request.form.get("password"), method='pbkdf2', salt_length=8) 
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)    
        return render_template("secrets.html")
    return render_template("register.html")


# LOGIN PAGE - AUTHENTICATE PASSWORD - FLASH MESSAGE
@app.route('/login', methods=['GET', 'POST'])
def login():


    if request.method == "POST":
        u_email = request.form.get("email")
        u_password = request.form.get("password")
        u_user = db.session.execute(db.select(User).where(User.email==u_email)).scalar()

        if u_user:
            if check_password_hash(u_user.password, u_password):
                login_user(u_user)

                next = request.host_url
                if not url_has_allowed_host_and_scheme(next, "localhost:5000"):
                    print(request.args.keys())
                    return abort(400)
                
                return redirect(url_for("secrets"))
            else:
                flash('Login failed. The password is incorrect.')
                return render_template('login.html')
        else:
            flash('Login failed. Email user does not exist. Use the register link to sign up!')
    return render_template('login.html')


# LOGIN PROTECTED PAGE
@app.route('/secrets')
@login_required
def secrets():
    if current_user.is_authenticated:
        print(current_user.name)
    return render_template("secrets.html")


# LOGIN PROTECTED PAGE
@app.route('/download', methods = ["GET", "POST"])
@login_required
def download():
    if request.method == "GET":
        return send_from_directory(directory='static', path="files/cheat_sheet.pdf")
    return render_template("index.html")


# LOGOUT PAGE
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
