import dataclasses
import typing

from flask import request, Response
from flask.scaffold import Scaffold
from flask.views import View
from marshmallow import ValidationError

from api.errors import BaseAPIError, BadRequestError
from api.schemas import BaseAPIErrorSchema, ValidationErrorSchema


@dataclasses.dataclass(frozen=True)
class Request:
    # URL variables
    # For request GET /users/10 to the endpoint "/users/<int:user_id>"
    # url_variables will be {"user_id": 10}
    url_variables: typing.Dict[str, typing.Any]
    # Query parameters
    # If BaseResource.request_query_parameters_schema is defined
    # query parameters are loaded with this schema
    # otherwise this attribute is None.
    query_parameters: typing.Any
    # JSON data
    # If BaseResource.request_json_schema is defined
    # request data is loaded with this schema as JSON
    # otherwise this attribute is None.
    json: typing.Any


class BaseResource(View):
    """
    Base class for views. Example of usage:

        class PaginationSchema(Schema):
            offset = fields.Integer(default=0, validate=validate.Range(min=0))
            limit = fields.Integer(default=100, validate=validate.Range(min=1, max=1000))

        class UserSchema(Schema):
            id = fields.Integer()
            name = fields.String()

        class GetUserResource(BaseResource):
            rule = "/users"
            methods = ("GET",)
            request_query_parameters_schema = PaginationSchema()
            response_schema = UserSchema(many=True)

            def execute(req: Request):
                params = req.query_parameters
                users = users_service.get_users(offset=params["offset"], limit=params["limit"])
                return users

    Request GET /users?offset=0&limit=2 may return something like this:
    """
    rule: str = None
    methods: typing.Iterable[str] = None
    request_query_parameters_schema = None
    request_json_schema = None
    response_schema = None
    response_status = 200

    def __init__(self):
        if not self.rule:
            raise NotImplementedError("'rule' attribute is not defined")

        if not self.methods:
            raise NotImplementedError("'methods' attribute is not defined")

    def execute(self, req: Request):
        """
        Actual resource implementation.
        Must be overridden in a subclass.
        """
        raise NotImplementedError()

    def dispatch_request(self, **kwargs) -> Response:
        # Request query parameters and JSON body are retrieved if they are required.
        # If they do not correspond the request schemas a Bad Request error is raised
        # with the validation details.
        try:
            req = Request(
                url_variables=kwargs,
                query_parameters=self._get_query_parameters(),
                json=self._get_request_json(),
            )
        except BadRequestError as e:
            return validation_error_to_response(e)

        # Actual business logic execution.
        # If any API errors are raised in the subclassed view
        # they are caught and turned into HTTP errors.
        try:
            response = self.execute(req)
        except BaseAPIError as e:
            return error_to_response(e)

        if self.response_schema:
            response = self.response_schema.dumps(response)

        return Response(
            response=response,
            status=self.response_status,
        )

    def _get_query_parameters(self):
        """
        Request query parameters are retrieved
        if the corresponding schema is defined.
        They are validated with the given schema.
        """
        if self.request_query_parameters_schema:

            try:
                data = self.request_query_parameters_schema.load(request.args)
            except ValidationError as e:
                raise BadRequestError(
                    message="This request has invalid query parameters structure",
                    errors=e.normalized_messages(),
                )

            return data

    def _get_request_json(self):
        """
        JSON body is retrieved
        if the corresponding schema is defined.
        It is validated with the given schema.
        """
        if self.request_json_schema:

            if request.json is None:
                raise BadRequestError("JSON body is required for this request")

            try:
                data = self.request_json_schema.load(request.json)
            except ValidationError as e:
                raise BadRequestError(
                    message="This request has invalid JSON body structure",
                    errors=e.normalized_messages(),
                )

            return data


def register_resource(app: Scaffold):
    """
    This decorator is used to add the subclasses
    of BaseResource to the application.
    """
    def decorator(resource):
        app.add_url_rule(rule=resource.rule, view_func=resource.as_view(resource.__name__))
    return decorator


def error_to_response(error: BaseAPIError) -> Response:
    """
    Making a HTTP error response of an error.
    """
    schema = BaseAPIErrorSchema()
    return Response(
        response=schema.dumps(error),
        status=error.status,
    )


def validation_error_to_response(error: BadRequestError) -> Response:
    """
    Making a HTTP Bad Request response of a validation error.
    """
    schema = ValidationErrorSchema()
    return Response(
        response=schema.dumps(error),
        status=error.status,
    )
