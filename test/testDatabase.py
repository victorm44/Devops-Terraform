import unittest
import requests
from database import create_tables, create_movie_table, close_connection, insert_movie, get_all_movies, Movie
from main import app

class YourAppTest(unittest.TestCase):

    def setUp(self):
        create_tables()
        create_movie_table()

        # Agregar registros de prueba
        for i in range(1, 10):
            movie_data = {
                "title": f"Movie {i}",
                "overview": f"Overview for Movie {i}",
                "year": 2020 + i,
                "rating": 7.5 + i * 0.1,
                "category": "Action"
            }
            insert_movie(Movie(**movie_data))

    def tearDown(self):
        close_connection()

    def test_get_all_movies(self):
        response = requests.get('http://localhost:8000/movies')
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 100)  # Verificar que haya al menos 100 registros

    def test_get_movie_by_id(self):
        response = requests.get('http://localhost:8000/movies/1')
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['id'], 1)

    # Agrega más pruebas según tus necesidades

if __name__ == '__main__':
    unittest.main()
