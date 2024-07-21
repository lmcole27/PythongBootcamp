from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, func
from sqlalchemy.exc import SQLAlchemyError
#import random
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

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=True)
    img_url: Mapped[str] = mapped_column(String(500), nullable=True)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=True)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=True)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=True)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=True)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=True)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dic(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

all_cafe_data = {}

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random", methods=["POST", "GET"])
def get_random_cafe():
    random_cafe = db.session.execute(db.select(Cafe).order_by(func.random()).limit(1)).scalar()
    return random_cafe.to_dic() 

#OPTION 2
    # random_cafe = random.choice(db.session.query(Cafe).all())    
    # return jsonify(Cafe={
    #     "id": random_cafe.id,
    #     "name": random_cafe.name,
    #     "map_url": random_cafe.map_url,
    #     "img_url": random_cafe.img_url,
    #     "location": random_cafe.location,
    #     "seats": random_cafe.seats,
    #     "has_toilet": random_cafe.has_toilet,
    #     "has_wifi": random_cafe.has_wifi,
    #     "has_sockets": random_cafe.has_sockets,
    #     "can_take_calls": random_cafe.can_take_calls,
    #     "coffee_price": random_cafe.coffee_price,
    # })

#OPTION 3
    # random_cafe = random.choice(db.session.query(Cafe).all())    
    # return jsonify(random_cafe.to_dic())


@app.route("/all")
def get_all_cafes():
    cafes = db.session.execute(db.select(Cafe)).scalars().all()
    return {cafe.id : cafe.to_dic() for cafe in cafes}, 200

#OPTION 2
    # cafes = db.session.execute(db.select(Cafe)).all()
    # all_cafe_data = {cafes[i][0].id : cafes[i][0].to_dic() for i in range(len(cafes))}
    # return all_cafe_data

#OPTION 3
    # for i in range(len(cafes)):
    #     cafe_data = cafes[i][0].to_dic()
    #     all_cafe_data.update({cafes[i][0].id : cafe_data)
    # return all_cafe_data

    # def to_dic(self):
    #     return {column.name: getattr(self, column.name) for column in self.__table__.columns}

@app.route("/search", methods=["POST"])
def search():
    loc = request.args.get('loc')
    loc_cafes = db.session.execute(db.select(Cafe).where(Cafe.location==loc)).scalars().fetchall()
    if loc_cafes:
        return {cafe.id : cafe.to_dic() for cafe in loc_cafes}
    #OR 
    # return jsonify(cafe.id : cafe.to_dic() for cafe in loc_cafes)
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}), 404
    
    
# HTTP POST - Create Record
@app.route("/add2", methods=["POST"])
def add_cafe():
    newCafe = Cafe(
        name = request.args.get('name'),
        location = request.args.get('location'),
        map_url = request.args.get('map_url'), 
        img_url = request.args.get('img_url'),
        seats = request.args.get('seats'),         
        coffee_price = request.args.get('coffee_price')
        #has_toilet = bool(request.args.get('has_toilet'))       
         )

    if request.args.get('has_toilet') == "True":
        newCafe.has_toilet = True
    elif request.args.get('has_toilet') == "False":
        newCafe.has_toilet = False
    
    if request.args.get('has_wifi') == "True":
        newCafe.has_wifi = True
    elif request.args.get('has_wifi') == "False":
        newCafe.has_wifi = False

    if request.args.get('has_sockets') == "True":
        newCafe.has_sockets = True
    elif request.args.get('has_sockets') == "False":
        newCafe.has_sockets = False

    if request.args.get('can_take_calls') == "True":
        newCafe.can_take_calls = True
    elif request.args.get('can_take_calls') == "False":
        newCafe.can_take_calls = False

    db.session.add(newCafe)
    db.session.commit()
    return jsonify(response={"Success": "Successfully added the new cafe."}), 200


# HTTP SEARCH - Search Record
@app.route("/idsearch", methods=["POST"])
def idsearch():
    name = request.args.get('name')
    try:
        found_cafe = db.session.execute(db.select(Cafe).where(Cafe.name==name)).scalars().one()
    except SQLAlchemyError:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}), 404
    else:
        return jsonify(response={"id" : found_cafe.id}), 200
        # OR
        # return jsonify(response = {found_cafe.id : found_cafe.to_dic()}), 200
        
    
# HTTP PUT/PATCH - Update Record
@app.route("/update", methods=["GET", "POST", "PATCH"])
def update():
    cafe_id = request.args.get('cafe_id', default = 1, type = int)
    try:
        update_cafe = db.session.execute(db.select(Cafe).where(Cafe.id==cafe_id)).scalars().one()
    except SQLAlchemyError:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe with that id."}), 404
    else:
        update_cafe.coffee_price = request.args.get('new_price')
        db.session.add(update_cafe)
        db.session.commit()
        return jsonify(response={"Success": "Successfully updated the cafe."}), 200


#OPTION 2
## HTTP PUT/PATCH - Update Record
@app.route("/update2/<int:id>", methods=["GET", "POST", "PATCH"])
def update2(id):
    update_cafe = db.one_or_404(db.select(Cafe).filter_by(id=id), 
        description=f"Sorry we do not have a cafe with id = {id}.")
    if update_cafe:     
        update_cafe.coffee_price = request.args.get('new_price')
        db.session.add(update_cafe)
        db.session.commit()
        return jsonify(response={"Success": "Successfully updated the cafe."}), 200


# HTTP DELETE - Delete Record
@app.route("/delete/", methods=["DELETE"])
def delete():
    if request.args.get('API_Key') == 'secret':
        try:
            cafe_id = request.args.get('cafe_id')
            del_cafe = db.session.execute(db.select(Cafe).where(Cafe.id==cafe_id)).scalars().one()
        except SQLAlchemyError:
            return jsonify(error={"Not Found": "Sorry, we don't have a cafe with that id."}), 404
        else:     
            db.session.delete(del_cafe)
            db.session.commit()
            return jsonify(response={"Success": "Successfully deleted the cafe."}), 200
    else:
        return jsonify(error={"Access Denied": "Sorry, we don't have access to delete a cafe."}), 404

if __name__ == '__main__':
    app.run(debug=True)
