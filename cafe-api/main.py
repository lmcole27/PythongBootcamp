from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dic(self):
        # dictionary = {}
        # for column in self.__table__.columns:
        #     dictionary[column.name] =getattr(self, column.name)
        # return dictionary
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")
    
## HTTP GET - Read Record
@app.route("/random", methods=["GET"])
def random_cafe():
    # cafes = db.session.execute(db.select(Cafe)).scalars().all()
    my_cafe = random.choice(db.session.query(Cafe).all())
    return jsonify(my_cafe.to_dic())

@app.route("/add", methods=["GET", "POST"])
def add_cafes():
    print(request.method)
    if request.method == "POST":
        # new_cafe = Cafe()
        new_cafe = request.data
        print(new_cafe)
        #db.session.add(new_cafe)
        return jsonify({"Success":{"Cafe": "Cafe added YO!"}})
    else:
        return jsonify({"Error":{"Unsuccessful": "No cafes added YO!"}})    

@app.route("/all", methods=["GET", "POST"])
def all_cafes():
    cafes = db.session.query(Cafe).all()
    return jsonify([cafe.to_dic() for cafe in cafes])

# @app.route("/search/<location>", methods=["GET"])
# def search_cafes(location):
#     cafes = db.session.query(Cafe).where(Cafe.location==location).all()
#     new_dic = [cafe.to_dic() for cafe in cafes]
#     if new_dic: 
#         return jsonify(new_dic)
#     else:
#         return jsonify({"Error":{"Not found": "No cafes at that location"}})

@app.route("/search", methods = ["GET"])
def search_cafes():
    loc = request.args.get('loc')
    cafes = db.session.query(Cafe).where(Cafe.location==loc).all()
    new_dic = [cafe.to_dic() for cafe in cafes]
    if new_dic: 
        return jsonify(new_dic)
    else:
        return jsonify({"Error":{"Not found": "No cafes at that location"}})



## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
