# movie_database.py
from typing import List, Dict
import json

class MovieDatabase:
    """Classe para gerenciar o banco de dados de filmes"""
    
    def __init__(self, file_path: str = "movies.json"):
        self.file_path = file_path
        self.movies = self._load_movies()
    
    def _load_movies(self) -> List[Dict]:
        """Carrega a base de dados de filmes do arquivo JSON"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return []
    
    def get_movies_by_genre(self, genre: str) -> List[Dict]:
        """Retorna filmes filtrados por gênero"""
        return [movie for movie in self.movies if genre.lower() in 
                [g.lower() for g in movie.get('genres', [])]]
    
    def get_movies_by_rating(self, min_rating: float) -> List[Dict]:
        """Retorna filmes com avaliação acima do valor especificado"""
        return [movie for movie in self.movies if movie.get('rating', 0) >= min_rating]
