from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import os
from dotenv import load_dotenv

load_dotenv()


'''
On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''
API_KEY = os.environ.get("API_KEY")
API_READ_ACCESS_TOKEN = os.environ.get("API_READ_ACCESS_TOKEN")

HEADER = headers = {
    "accept": "application/json",
    "Authorization": os.environ.get("AUTHORIZATION")
}

search_url = "https://api.themoviedb.org/3/search/movie"   
detail_url = "https://api.themoviedb.org/3/movie/"

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
Bootstrap5(app)


db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movie.db"
# initialize the app with the extension
db.init_app(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title  = db.Column(db.String, unique=True, nullable=False)
    year  = db.Column(db.String, nullable=False)
    description  = db.Column(db.String, nullable=False)
    rating  = db.Column(db.Float)
    ranking = db.Column(db.Integer)
    review = db.Column(db.String)
    img_url = db.Column(db.String, nullable=False)

with app.app_context():
    db.create_all()

# new_movie = Movie(
#     title="Avatar The Way of Water",
#     year=2022,
#     description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
#     rating=7.3,
#     ranking=9,
#     review="I liked the water.",
#     img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
# )
# with app.app_context():
#     db.session.add(new_movie)
#     db.session.commit()


class MyForm(FlaskForm):
    your_rating = StringField('Rating', validators=[DataRequired()])
    your_review = StringField('Review', validators=[DataRequired()])
    submit = SubmitField('Submit')

class addForm(FlaskForm):
    name = StringField('Movie Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route("/")
def home():
    movies = db.session.execute(db.select(Movie).order_by(Movie.ranking)).scalars()
    return render_template("index.html", movies=movies)

@app.route("/add", methods=["GET", "POST"])
def add():
    add_form = addForm()
    if request.method == "POST":
        movie_title = str(request.form["name"])
        return redirect(url_for("select", title=movie_title))
    return render_template("add.html", form=add_form)

@app.route("/select/<title>", methods=["POST", "GET"])
def select(title):
    # if request.method == "GET":
    #     response = requests.get(detail_url, params={"api_key": API_KEY, "movie_id": movie_id})
    #     data = response.json()["results"]
    #     pass
    # else:
    response = requests.get(search_url, params={"api_key": API_KEY, "query": title})
    data = response.json()["results"]
    return render_template("select.html", movies=data)

@app.route("/details/<int:movie_id>", methods=["GET", "POST"])
def details(movie_id):
    if request.method == "GET":
        #response = requests.get(detail_url, params={"api_key": API_KEY, "movie_id": movie_id})
        URL = detail_url + str(movie_id)
        response = requests.get(URL, headers=HEADER)
        data = response.json()

        new_movie = Movie(
            title= data["title"],
            year= data["release_date"][0:4],
            description= data["overview"],
            rating=0,
            ranking=0,
            review="",
            img_url="https://image.tmdb.org/t/p/w500/" + str(data["poster_path"])
            )
    
    with app.app_context():
        db.session.add(new_movie)
        db.session.commit()

    # movie = db.session.execute(db.select(Movie).where(Movie.title==new_movie.title)).scalar()
    # print(new_movie.title, movie.id)
    # return render_template("details.html", data=data)
    return redirect(url_for('edit', id=new_movie.id))

@app.route("/edit/<int:id>", methods=["POST", "GET"])
def edit(id):
    edit_form = MyForm()
    movie_update = db.session.execute(db.select(Movie).where(Movie.id == id)).scalar()
    if request.method == "POST":
        movie_update.rating = request.form["your_rating"]
        movie_update.review = request.form["your_review"]
        db.session.commit()
        return redirect('/')
    return render_template("edit.html", id=id, movie=movie_update, form=edit_form)

@app.route("/delete/<int:id>")
def delete(id):
    movie_delete = db.session.execute(db.select(Movie).where(Movie.id == id)).scalar()
    db.session.delete(movie_delete)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
