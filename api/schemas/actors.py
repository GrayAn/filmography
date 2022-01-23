from marshmallow import Schema, fields


class ActorSchema(Schema):
    id = fields.Integer()
    name = fields.String()


class ActorAggregatedSchema(Schema):
    name = fields.String()
    year = fields.Integer()
    number = fields.Integer()


class ActorAggregatedPaginatedSchema(Schema):
    actors = fields.Nested(ActorAggregatedSchema, many=True)
    total = fields.Integer()
    limit = fields.Integer()
    offset = fields.Integer()
