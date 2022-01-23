import typing

from sqlalchemy.orm import Session

from database.connection import get_session
from database.repositories import ActorsRepo, GenresRepo
from database import models
import entities


class MoviesRepo:
    def get_movie(self, movie_id: int) -> typing.Optional[entities.Movie]:
        """
        Movie object is retrieved from the database
        with the related Actor and Genre objects.
        """
        with get_session() as session:

            movie_model = session.query(models.Movie).filter(models.Movie.id == movie_id).first()
            if not movie_model:
                return

            # Database model is converted to the entity
            # to unbound it from the database connection.
            return self._model_to_entity(movie_model)

    def create_movie(self, movie: entities.Movie) -> entities.Movie:
        """
        New Movie object is saved to the database.
        Related Actor and Genre objects may contain only their ids.
        Return the inserted object id.
        """
        # Checking that actors and genres are actually exist
        # because SQLite doesn't check for foreign constraints
        self._check_for_actor_existence(movie.actors)
        self._check_for_genre_existence(movie.genres)

        with get_session() as session:

            session.begin()
            movie_model = models.Movie()
            movie_model.title = movie.title
            movie_model.year = movie.year
            session.add(movie_model)
            # Need to save the movie here to get its id
            session.commit()

            session.begin()
            self._create_actor_relations(movie_id=movie_model.id, actors=movie.actors, session=session)
            self._create_genre_relations(movie_id=movie_model.id, genres=movie.genres, session=session)
            session.commit()

            return self._model_to_entity(movie_model)

    def edit_movie(self, movie: entities.Movie) -> typing.Optional[entities.Movie]:
        """
        A Movie object is updated in the database.
        Old relations with Actor and Genre objects are removed
        and new ones are created.
        """
        # Checking that actors and genres are actually exist
        # because SQLite doesn't check for foreign constraints
        self._check_for_actor_existence(movie.actors)
        self._check_for_genre_existence(movie.genres)

        with get_session() as session:

            movie_model = session.query(models.Movie).filter(models.Movie.id == movie.id).first()
            if not movie_model:
                return

            session.begin()
            movie_model.title = movie.title
            movie_model.year = movie.year
            self._delete_actor_relations(movie_id=movie.id, session=session)
            self._delete_genre_relations(movie_id=movie.id, session=session)
            self._create_actor_relations(movie_id=movie.id, actors=movie.actors, session=session)
            self._create_genre_relations(movie_id=movie.id, genres=movie.genres, session=session)
            session.commit()

            return self._model_to_entity(movie_model)

    def delete_movie(self, movie_id: int):
        """
        A Movie object is removed from the database
        identified by its id.
        Relations with Actor and Genre objects are removed as well.
        """
        with get_session() as session:

            session.begin()
            self._delete_actor_relations(movie_id=movie_id, session=session)
            self._delete_genre_relations(movie_id=movie_id, session=session)
            session.query(models.Movie).filter(models.Movie.id == movie_id).delete()
            session.commit()

    def _model_to_entity(self, model: models.Movie) -> entities.Movie:
        return entities.Movie(
            id=model.id,
            title=model.title,
            year=model.year,
            actors=[
                entities.Actor(
                    id=actor_model.id,
                    name=actor_model.name,
                ) for actor_model in model.actors
            ],
            genres=[
                entities.Genre(
                    id=genre_model.id,
                    name=genre_model.name,
                ) for genre_model in model.genres
            ],
        )

    def _check_for_actor_existence(self, actors: typing.List[entities.Actor]):
        actors_repo = ActorsRepo()
        found_actors = actors_repo.get_actors([actor.id for actor in actors])
        if len(found_actors) < len(actors):
            raise entities.ObjectDoesNotExistError("Some actors don't exist")

    def _check_for_genre_existence(self, genres: typing.List[entities.Genre]):
        genres_repo = GenresRepo()
        found_genres = genres_repo.get_genres([genre.id for genre in genres])
        if len(found_genres) < len(genres):
            raise entities.ObjectDoesNotExistError("Some genres don't exist")

    def _create_actor_relations(self, movie_id: int, actors: typing.List[entities.Actor], session: Session):
        for actor in actors:
            actor_movie_model = models.ActorMovie()
            actor_movie_model.actor_id = actor.id
            actor_movie_model.movie_id = movie_id
            session.add(actor_movie_model)

    def _create_genre_relations(self, movie_id: int, genres: typing.List[entities.Genre], session: Session):
        for genre in genres:
            genre_movie_model = models.GenreMovie()
            genre_movie_model.genre_id = genre.id
            genre_movie_model.movie_id = movie_id
            session.add(genre_movie_model)

    def _delete_actor_relations(self, movie_id: int, session: Session):
        session.query(models.ActorMovie).filter(models.ActorMovie.movie_id == movie_id).delete()

    def _delete_genre_relations(self, movie_id: int, session: Session):
        session.query(models.GenreMovie).filter(models.GenreMovie.movie_id == movie_id).delete()
