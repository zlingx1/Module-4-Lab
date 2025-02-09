from flask import Flask
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(200))

    def __repr__(self):
        return f"{self.name} - {self.description}"

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/books')
def get_books():
    out = []
    books = Book.query.all()

    for book in books:
        data = {'name':book.name, 'description':book.description}
        out.append(data)

    return {"books": out }

@app.route('/books/<id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return {"name":book.name, "description":book.description}

@app.route('books/', methods=["POST"])
def add_book():
    book = Book(name=request.json['name'], description=request.json['description'])

    db.session.add(book)
    db.session.commit()

    return {"id":book.id}

@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)

    if book is None:
        return { "status" : "error 404" }

    db.session.delete(book)
    db.session.commit()

    return { "status" :  "" }