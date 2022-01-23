from marshmallow import Schema, fields, post_load

from entities import Actor, Genre, Movie
from .actors import ActorSchema
from .genres import GenreSchema


class MovieSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    year = fields.Integer()
    actors = fields.Nested(ActorSchema, many=True)
    genres = fields.Nested(GenreSchema, many=True)


class CreateMovieSchema(Schema):
    title = fields.String(required=True, allow_none=False)
    year = fields.Integer(required=True, allow_none=False)
    actor_ids = fields.List(fields.Integer, required=False, allow_none=False, default=[])
    genre_ids = fields.List(fields.Integer, required=False, allow_none=False, default=[])

    @post_load
    def create_entity(self, data, **kwargs) -> Movie:
        return Movie(
            title=data["title"],
            year=data["year"],
            actors=[
                Actor(id=actor_id) for actor_id in data["actor_ids"]
            ],
            genres=[
                Genre(id=genre_id) for genre_id in data["genre_ids"]
            ],
        )


class EditMovieSchema(CreateMovieSchema):
    pass
