from marshmallow import Schema, fields, validate

class BookQuerySchema(Schema):
    page = fields.Integer(missing=1, validate=validate.Range(min=1))
    size = fields.Integer(missing=10, validate=validate.Range(min=1, max=100))
    min_price = fields.Float(validate=validate.Range(min=0), allow_none=True)
    max_price = fields.Float(validate=validate.Range(min=0), allow_none=True)
    release_after = fields.Date(allow_none=True)
    category = fields.String(allow_none=True)
    author = fields.String(allow_none=True)
