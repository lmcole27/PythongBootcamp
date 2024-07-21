from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
db.init_app(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


with app.app_context():
    db.create_all()

all_books = []

@app.route('/')
def home():
    result = db.session.execute(db.select(Book).order_by(Book.title))
    all_books = result.scalars().all()
    for book in all_books:
        print(f"main.py {book.title}")
    return render_template('index.html', books=all_books)


@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        new_book = Book(title=request.form["title"], 
                        author=request.form["author"], 
                        rating=request.form["rating"])
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route("/edit/<int:index>", methods=["POST", "GET"])
def edit(index):
    with app.app_context():
        book_to_update = db.session.execute(db.select(Book).where(Book.id == index)).scalar()
        if request.method == "POST":
            book_to_update.rating = request.form["new_rating"]
            db.session.commit()
            return redirect(url_for('home')) 
    return render_template('edit.html', book=book_to_update)

@app.route("/delete/<int:index>")
def delete(index):
    with app.app_context():
        book_to_delete = db.session.execute(db.select(Book).where(Book.id == index)).scalar()
        db.session.delete(book_to_delete)
        db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)

