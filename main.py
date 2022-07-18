from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = r"sqlite:///file_location\books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


if database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
    pass
else:
    print("hello")
    db.create_all()


@app.route('/')
def home():
    if database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
        pass
    else:
        db.create_all()
    all_books = Book.query.all()
    return render_template("index.html", books=all_books)


@app.route("/add")
def add_list():
    return render_template("add.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    if database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
        pass
    else:
        db.create_all()

    book = request.form["book_name"]
    author = request.form["author"]
    rating = request.form["rating"]
    library_book = Book.query.all()

    if len(library_book) == 0:
        new_book = Book(title=book, author=author, rating=rating)
        db.session.add(new_book)
        db.session.commit()
    book_present = Book.query.filter_by(title=book).first()
    if book_present:
        pass
    else:
        new_book = Book(title=book, author=author, rating=rating)
        db.session.add(new_book)
        db.session.commit()

    return home()


@app.route("/edit", methods=["GET", "POST"])
def edit_rating():
    if request.method == "POST":
        book_id = request.form['id']
        book_rating_to_update = Book.query.get(book_id)
        book_rating_to_update.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))

    book_id = request.args['id']
    book_rating_to_update = Book.query.get(book_id)
    return render_template("rating_edit_page.html", value=book_rating_to_update)


@app.route("/delete")
def delete_rating():
    book_id = request.args['id']
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
