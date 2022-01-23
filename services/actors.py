from database.repositories import ActorsRepo
from entities import ActorsAggregatedPaginated


class ActorsService:
    def __init__(self):
        self.actors_repo = ActorsRepo()

    def get_actors_aggregated(self, offset: int, limit: int) -> ActorsAggregatedPaginated:
        return self.actors_repo.get_actors_aggregated(offset=offset, limit=limit)
