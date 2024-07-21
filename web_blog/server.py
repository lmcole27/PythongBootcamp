from sre_parse import SubPattern
from flask import Flask, render_template
import random
from datetime import datetime
import requests
import json
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def hello():
    random_number=random.randint(0, 10)
    current_year =  datetime.now().year
    response_gender = requests.get("https://api.genderize.io?name=linda")
    response_gender.raise_for_status()
    gender_data = response_gender.json()
    est_gender = gender_data["gender"]
    response_age = requests.get("https://api.agify.io?name=linda")
    response_age.raise_for_status()
    age_data = response_age.json()
    est_age = age_data["age"]
    return render_template("index.html", num=random_number, year=current_year, guess_gender=est_gender, guess_age=est_age)

@app.route("/guess/<name>")
def a(name):
    response_gender2 = requests.get(f"https://api.genderize.io?name={name}")
    gender_data2 = response_gender2.json()
    est_gender2 = gender_data2["gender"]
    response_age2 = requests.get(f"https://api.agify.io?name={name}")
    age_data2 = response_age2.json()
    est_age2 = age_data2["age"]
    s_name = (str(name)).title()
    return render_template("name.html", guess_gender2=est_gender2, guess_age2=est_age2, name_var=name, s_name=s_name)
    
@app.route("/blog")
def blog():
    response_blog = requests.get("https://api.npoint.io/c790b4d5cab58020d391")
    blog_data = response_blog.json()
    return render_template("blog.html", posts = blog_data)

if __name__ == "__main__":
    app.run(debug=True)




