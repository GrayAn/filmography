import typing

from sqlalchemy import func

from database.connection import get_session
from database import models
import entities


class ActorsRepo:
    def get_actors(self, actor_ids: typing.List[int]) -> typing.List[entities.Actor]:
        with get_session() as session:

            actor_models = session.query(models.Actor).filter(models.Actor.id.in_(actor_ids)).all()
            return [
                entities.Actor(
                    id=actor_model.id,
                    name=actor_model.name,
                ) for actor_model in actor_models
            ]

    def get_actors_aggregated(self, offset: int, limit: int) -> entities.ActorsAggregatedPaginated:
        """
        Getting the list of actors aggregated
        by their name and years of their movies
        The number of their movies is included in results.
        The results are ordered by actors' names and movies' year
        in the ascending order.

        This request may be time consuming on large tables of data.
        In this case creation of a new table should be considered
        which will include actor id, movie year and number of movies
        though it will require filling this table on changing data
        in actor, movie and actor_movie tables.
        """
        with get_session() as session:

            query = session.query(models.Actor, models.Movie.year, func.count(models.Actor.id)). \
                join(models.ActorMovie, models.Actor.id == models.ActorMovie.actor_id). \
                join(models.Movie, models.Movie.id == models.ActorMovie.movie_id). \
                group_by(models.Actor, models.Movie.year). \
                order_by(models.Actor.name). \
                order_by(models.Movie.year)
            total = query.count()

            items = query.offset(offset).limit(limit).all()

            return entities.ActorsAggregatedPaginated(
                actors=[
                    entities.ActorAggregated(
                        name=item[0].name,
                        year=item[1],
                        number=item[2],
                    ) for item in items
                ],
                total=total,
                limit=limit,
                offset=offset,
            )
