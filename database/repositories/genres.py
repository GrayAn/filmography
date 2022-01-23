import typing

from database.connection import get_session
from database import models
import entities


class GenresRepo:
    def get_genres(self, genres_ids: typing.List[int]) -> typing.List[entities.Genre]:
        with get_session() as session:

            genre_models = session.query(models.Genre).filter(models.Genre.id.in_(genres_ids)).all()
            return [
                entities.Genre(
                    id=genre_model.id,
                    name=genre_model.name,
                ) for genre_model in genre_models
            ]
