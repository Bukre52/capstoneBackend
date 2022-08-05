from pydoc import describe
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os



app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

CORS(app)
# this is a db table
class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String, nullable=False)

    def __init__(self, name, price, description, img_url):
        self.name = name
        self.price = price
        self.description = description
        self.img_url = img_url

# the schema changes data from visible data to computer data like 010101
class MovieSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "price", "description", "img_url")

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

@app.route("/add-movie", methods=["POST"])
def add_movie():
    name = request.json.get("name")
    description = request.json.get("description")
    price = request.json.get("price")
    img_url = request.json.get("img_url")

    new_record = Movies(name, price, description, img_url)
    db.session.add(new_record)
    db.session.commit()

    return jsonify(movie_schema.dump(new_record))


@app.route("/movies", methods=["GET"])
def get_all_movies():
    all_movies = Movies.query.all()
    return jsonify(movies_schema.dump(all_movies))


@app.route("/movie/<id>", methods=["DELETE","GET","PUT"])
def movie_id(id):
    movie = Movies.query.get(id)
    if request.method == "DELETE":
        db.session.delete(movie)
        db.session.commit()
    
        return books_schemas.jsonify(movie)
    elif request.method == "PUT":
        name = request.json['name']
        price = request.json['price']
        description = request.json['description']
        img_url = request.json['img_url']

        movie.name = name
        movie.price = price
        movie.description = description
        movie.img_url = img_url

        db.session.commit()
        return movie_schema.jsonify(movie)
    elif request.method == "GET":
        return movie_schema.jsonify(movie)

if __name__ == "__main__":
    app.run(debug=True)