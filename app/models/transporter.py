from ..extensions import db
from datetime import datetime, timezone


class Transporter(db.Model):
    __tablename__ = 'transporters'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    location = db.Column(db.String(255),nullable=False)

    user = db.relationship('User', backref=db.backref('transporters', lazy=True))