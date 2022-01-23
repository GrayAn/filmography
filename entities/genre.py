import dataclasses
import typing


@dataclasses.dataclass
class Genre:
    id: typing.Optional[int] = None
    name: typing.Optional[str] = None
