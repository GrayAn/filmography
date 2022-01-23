from marshmallow import Schema, fields


class GenreSchema(Schema):
    id = fields.Integer()
    name = fields.String()
