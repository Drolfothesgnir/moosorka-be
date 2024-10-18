from flask.views import MethodView
from flask import request
from flask_smorest import Blueprint, abort
from schemas import RecordSchema, PaginatedRecordSchema
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

    @blp.arguments(RecordSchema)
    @blp.response(200, RecordSchema)
    def put(self, record_data, record_id):
        record = RecordModel.query.get(record_id)
        if record:
            record.content = record_data["content"]
        else:
            record = RecordModel(id=record_id, **record_data)

        db.session.add(record)
        db.session.commit()

        return record


@blp.route("/record")
class RecordList(MethodView):
    @blp.response(200, PaginatedRecordSchema)
    def get(self):
        # Get pagination parameters
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        sort = request.args.get("sort", "last")

        # Query the records
        query = RecordModel.query

        if sort == "first":
            query = query.order_by(RecordModel.created_at.asc())
        else:
            query = query.order_by(RecordModel.created_at.desc())

        # Use Flask-SQLAlchemy's paginate() method
        paginated_records = query.paginate(page=page, per_page=per_page)

        # Return both the items and the total count
        return {
            "items": paginated_records.items,  # The records for the current page
            "total": paginated_records.total,  # Total number of records
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
