from database.repositories import MoviesRepo
from entities import Movie


class MoviesService:
    def __init__(self):
        self.movies_repo = MoviesRepo()

    def get_movie(self, movie_id: int) -> Movie:
        return self.movies_repo.get_movie(movie_id)

    def create_movie(self, movie: Movie) -> Movie:
        return self.movies_repo.create_movie(movie)

    def edit_movie(self, movie: Movie) -> Movie:
        return self.movies_repo.edit_movie(movie)

    def delete_movie(self, movie_id: int):
        self.movies_repo.delete_movie(movie_id)
