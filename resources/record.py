from flask.views import MethodView
from flask import request
from flask_smorest import Blueprint, abort
from schemas import RecordSchema, PaginatedRecordSchema, RecordUpdateSchema
from models import RecordModel
from db import db
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("records", __name__, description="Operations on records")


@blp.route("/record/<string:record_id>")
class Record(MethodView):
    @blp.response(200, RecordSchema)
    def get(self, record_id):
        record = RecordModel.query.get_or_404(record_id)
        return record

    def delete(self, record_id):
        record = RecordModel.query.get_or_404(record_id)
        db.session.delete(record)
        db.session.commit()

        return {"message": "Record deleted."}

    @blp.arguments(RecordUpdateSchema)
    @blp.response(200, RecordSchema)
    def put(self, record_data, record_id):
        record = RecordModel.query.get_or_404(record_id)

        # Update only the fields present in the request
        if "content" in record_data:
            record.content = record_data["content"]
        if "pinned" in record_data:
            record.pinned = record_data["pinned"]

        db.session.add(record)
        db.session.commit()

        return record


@blp.route("/record")
class RecordList(MethodView):
    @blp.response(200, PaginatedRecordSchema)
    def get(self):
        # Get pagination and sorting parameters
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        sort = request.args.get("sort", "last")
        pinned = request.args.get(
            "pinned", type=str
        )  # Treat pinned as a string initially
        substring = request.args.get("s", type=str)

        # Start with base query
        query = RecordModel.query

        # Handle `pinned` filter (convert 'true'/'false' string to boolean)
        if pinned is not None:
            pinned_value = (
                pinned.lower() == "true"
            )  # Converts 'true' to True, 'false' to False
            query = query.filter_by(pinned=pinned_value)

        # Handle substring search in the content
        if substring:
            query = query.filter(RecordModel.content.ilike(f"%{substring}%"))

        # Handle sorting
        if sort == "first":
            query = query.order_by(RecordModel.created_at.asc())
        else:
            query = query.order_by(RecordModel.created_at.desc())

        # Paginate the results
        paginated_records = query.paginate(page=page, per_page=per_page)

        # Return the paginated results
        return {
            "items": paginated_records.items,
            "total": paginated_records.total,
            "has_next": paginated_records.has_next,
        }

    @blp.arguments(RecordSchema)
    @blp.response(201, RecordSchema)
    def post(self, record_data):
        record = RecordModel(**record_data)
        try:
            db.session.add(record)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while creating a record.")

        return record


@blp.route("/record/dump")
class RecordDump(MethodView):
    @blp.response(200, RecordSchema(many=True))
    def get(self):
        return RecordModel.query.order_by(RecordModel.created_at.asc())
