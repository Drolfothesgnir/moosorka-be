from db import db
from datetime import datetime, timezone


class RecordModel(db.Model):
    __tablename__ = "records"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))
    pinned = db.Column(db.Boolean, default=False)
