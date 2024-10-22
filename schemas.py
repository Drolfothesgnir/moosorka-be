from marshmallow import Schema, fields


class RecordSchema(Schema):
    id = fields.Int(dump_only=True)
    content = fields.String(required=True, nullable=False)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)  # Added updated_at to the schema
    pinned = fields.Boolean(required=False)


class PaginatedRecordSchema(Schema):
    items = fields.List(fields.Nested(RecordSchema))  # List of records
    total = fields.Int()  # Total number of records
    has_next = fields.Bool()


class RecordUpdateSchema(Schema):
    content = fields.String(required=False)
    pinned = fields.Boolean(required=False)
