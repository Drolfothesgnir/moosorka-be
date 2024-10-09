from flask.views import MethodView
from flask import request
from flask_smorest import Blueprint, abort
from schemas import RecordSchema
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
    @blp.response(200, RecordSchema(many=True))
    def get(self):
        skip = request.args.get("skip")
        limit = request.args.get("limit")
        query = RecordModel.query

        if skip:
            query = query.offset(int(skip))
        if limit:
            query = query.limit(int(limit))

        return query.all()

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
