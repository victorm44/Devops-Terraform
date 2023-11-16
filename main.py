#main.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os 
from database import Genre, Movie, create_tables, insert_genre, get_all_genres, create_movie_table, insert_movie, get_all_movies, update_movie, close_connection

os.environ["DB_HOST"] = "aws_db_instance.dbmovies.address"

app = Flask(__name__)
CORS(app)

create_tables()
create_movie_table()

@app.route('/')
def message():
    return '<h1>Victor</h1>'

@app.route('/genres', methods=['GET'])
def get_genres():
    genres = get_all_genres()
    return jsonify(genres)

@app.route('/genres', methods=['POST'])
def create_genre():
    data = request.json
    genre = Genre(**data)
    insert_genre(genre)
    return jsonify(genre)

@app.route('/movies', methods=['GET'])
def get_movies():
    movies = get_all_movies()
    return jsonify(movies)

@app.route('/movies/<int:id>', methods=['GET'])
def get_movie(id):
    movies = get_all_movies()
    for movie in movies:
        if movie.id == id:
            return jsonify(movie)
    return jsonify({"message": "Movie not found"})

@app.route('/movies/', methods=['GET'])
def get_movies_by_category():
    category = request.args.get('category')
    year = request.args.get('year')
    movies = get_all_movies()
    filtered_movies = [movie for movie in movies if movie.category == category]
    return jsonify(filtered_movies)

@app.route('/movies', methods=['POST'])
def create_movie():
    data = request.json
    new_id = max(movie.id for movie in get_all_movies()) + 1 if get_all_movies() else 1
    data['id'] = new_id
    movie = Movie(**data)
    insert_movie(movie)
    return jsonify(movie)

@app.route('/movies/<int:id>', methods=['PUT'])
def update_movie_endpoint(id):
    data = request.json
    existing_movie = None
    movies = get_all_movies()

    for m in movies:
        if m.id == id:
            existing_movie = m
            break

    if existing_movie is None:
        return jsonify({"message": "Movie not found"})

    updated_movie = Movie(id=existing_movie.id, **data)
    updated = update_movie(updated_movie)

    if updated:
        return jsonify(updated)
    return jsonify({"message": "Update failed"})

@app.route('/movies/<int:id>', methods=['DELETE'])
def delete_movie(id):
    movies = get_all_movies()
    for movie in movies:
        if movie.id == id:
            deleted_movie = movie
            return jsonify(deleted_movie)
    return jsonify({"message": "Movie not found"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
