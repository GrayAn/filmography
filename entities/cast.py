import dataclasses
import typing


@dataclasses.dataclass
class Actor:
    id: typing.Optional[int] = None
    name: typing.Optional[str] = None


@dataclasses.dataclass
class ActorAggregated:
    name: str
    year: int
    number: int


@dataclasses.dataclass
class ActorsAggregatedPaginated:
    actors: typing.List[ActorAggregated]
    total: int
    limit: int
    offset: int
