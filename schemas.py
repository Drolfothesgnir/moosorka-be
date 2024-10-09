from marshmallow import Schema, fields


class RecordSchema(Schema):
    id = fields.Int(dump_only=True)
    content = fields.String(required=True, nullable=False)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)  # Added updated_at to the schema
