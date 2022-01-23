from marshmallow import Schema, fields, validate


class PaginationSchema(Schema):
    offset = fields.Integer(load_default=0, allow_none=False, validate=validate.Range(min=0))
    limit = fields.Integer(load_default=100, allow_none=False, validate=validate.Range(min=1, max=1000))


class BaseAPIErrorSchema(Schema):
    message = fields.String()


class ValidationErrorSchema(BaseAPIErrorSchema):
    errors = fields.Dict()
