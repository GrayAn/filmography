from flask import Blueprint

from api.base_resource import BaseResource, Request, register_resource
from api.errors import BadRequestError, NotFoundError
from api.schemas import CreateMovieSchema, EditMovieSchema, MovieSchema
from entities import Movie, ObjectDoesNotExistError
import services

movies_api = Blueprint("movies", __name__)


@register_resource(movies_api)
class GetMovieResource(BaseResource):
    """
    Getting a single movie by its id.
    """
    methods = ("GET",)
    rule = "/movies/<int:movie_id>"
    response_schema = MovieSchema()

    def execute(self, req: Request) -> Movie:
        movie = services.movies_service.get_movie(req.url_variables["movie_id"])
        if not movie:
            raise NotFoundError("Movie not found")

        return movie


@register_resource(movies_api)
class CreateMovieResource(BaseResource):
    """
    Creating a new movie.
    """
    methods = ("POST",)
    rule = "/movies"
    request_json_schema = CreateMovieSchema()
    response_schema = MovieSchema()
    response_status = 201

    def execute(self, req: Request) -> Movie:
        movie: Movie = req.json
        try:
            return services.movies_service.create_movie(movie)
        except ObjectDoesNotExistError as e:
            raise BadRequestError(str(e))


@register_resource(movies_api)
class EditMovieResource(BaseResource):
    """
    Updating an existing movie.
    """
    methods = ("PUT",)
    rule = "/movies/<int:movie_id>"
    request_json_schema = EditMovieSchema()
    response_schema = MovieSchema()

    def execute(self, req: Request) -> Movie:
        movie: Movie = req.json
        movie.id = req.url_variables["movie_id"]
        try:
            return services.movies_service.edit_movie(movie)
        except ObjectDoesNotExistError as e:
            raise BadRequestError(str(e))


@register_resource(movies_api)
class DeleteMovieResource(BaseResource):
    """
    Removing a movie.
    """
    methods = ("DELETE",)
    rule = "/movies/<int:movie_id>"
    response_status = 204

    def execute(self, req: Request):
        services.movies_service.delete_movie(req.url_variables["movie_id"])
