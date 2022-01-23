import dataclasses
import typing

from .cast import Actor
from .genre import Genre


@dataclasses.dataclass
class Movie:
    title: str
    year: int
    id: typing.Optional[int] = None
    actors: typing.List[Actor] = dataclasses.field(default_factory=list)
    genres: typing.List[Genre] = dataclasses.field(default_factory=list)
