from flask import Flask, request, jsonify
from flask_cors import CORS
import os 
from json import JSONEncoder
from database import Genre, Movie, create_tables, insert_genre, get_all_genres, create_movie_table, insert_movie, get_all_movies, delete_movie_by_id, update_movie, close_connection

os.environ["DB_HOST"] = "aws_db_instance.dbmovies.address"

app = Flask(__name__)
CORS(app)

create_tables()
create_movie_table()

@app.route('/')
def message():
    return '<h1>Victor</h1>'

class MovieEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Movie):
            return obj.dict()
        return JSONEncoder.default(self, obj)


@app.route('/genres', methods=['POST'])
def create_genre():
    data = request.json
    new_genre = Genre(**data)
    insert_genre(new_genre)

    serialized_genre = {
        "name": new_genre.name,
        "description": new_genre.description
    }

    return jsonify(serialized_genre)

@app.route('/genres', methods=['GET'])
def get_genres():
    genres = get_all_genres()
    serialized_genres = []
    for genre in genres:
        serialized_genre = {
            "id": genre.id,
            "name": genre.name,
            "description": genre.description
        }
        serialized_genres.append(serialized_genre)

    return jsonify(serialized_genres)

@app.route('/movies/<int:id>', methods=['GET'])
def get_movie(id):
    movies = get_all_movies()
    for movie in movies:
        if movie.id == id:
            serialized_movie = {
                "id": movie.id,
                "title": movie.title,
                "overview": movie.overview,
                "year": movie.year,
                "rating": movie.rating,
                "category": movie.category
            }
            return jsonify(serialized_movie)
    return jsonify({"message": "Movie not found"})

@app.route('/movies/', methods=['GET'])
def get_movies():
    movies = get_all_movies()
    serialized_movies = []
    for movie in movies:
        serialized_movie = {
            "id": movie.id,
            "title": movie.title,
            "overview": movie.overview,
            "year": movie.year,
            "rating": movie.rating,
            "category": movie.category
        }
        serialized_movies.append(serialized_movie)

    return jsonify(serialized_movies)

@app.route('/movies', methods=['POST'])
def create_movie():
    data = request.json
    new_id = max(movie.id for movie in get_all_movies()) + 1 if get_all_movies() else 1
    data['id'] = new_id
    movie = Movie(**data)
    insert_movie(movie)

    serialized_movie = {
        "id": movie.id,
        "title": movie.title,
        "overview": movie.overview,
        "year": movie.year,
        "rating": movie.rating,
        "category": movie.category
    }

    return jsonify(serialized_movie)

@app.route('/movies/<int:id>', methods=['PUT'])
def update_movie_endpoint(id):
    data = request.json
    movies = get_all_movies()
    existing_movie = next((m for m in movies if m.id == id), None)

    if existing_movie is None:
        return jsonify({"message": "Movie not found"})

    updated_movie = Movie(id=existing_movie.id, **data)
    updated = update_movie(updated_movie)

    if updated:
        serialized_updated_movie = {
            "id": updated.id,
            "title": updated.title,
            "overview": updated.overview,
            "year": updated.year,
            "rating": updated.rating,
            "category": updated.category
        }
        return jsonify(serialized_updated_movie)

    return jsonify({"message": "Update failed"})


@app.route('/movies/<int:id>', methods=['DELETE'])
def delete_movie(id):
    movies = get_all_movies()
    deleted_movie = next((movie for movie in movies if movie.id == id), None)

    if deleted_movie:
        delete_movie_by_id(id)
        return jsonify({"message": "Movie deleted successfully"})

    return jsonify({"message": "Movie not found"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)