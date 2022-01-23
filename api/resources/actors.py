from flask import Blueprint

from api.base_resource import BaseResource, Request, register_resource
from api.schemas import ActorAggregatedPaginatedSchema, PaginationSchema
import services

actors_api = Blueprint("actors", __name__)


@register_resource(actors_api)
class GetActorsAggregatedResource(BaseResource):
    """
    Getting the list of actors aggregated by the years of release
    with the number of their movies in the order of actors' names.
    """
    methods = ("GET",)
    rule = "/actors/aggregated"
    request_query_parameters_schema = PaginationSchema()
    response_schema = ActorAggregatedPaginatedSchema()

    def execute(self, req: Request):
        params = req.query_parameters
        return services.actors_service.get_actors_aggregated(
            offset=params["offset"],
            limit=params["limit"],
        )
