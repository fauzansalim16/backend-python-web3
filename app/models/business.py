from ..extensions import db
from datetime import datetime, timezone
import enum

class ProductionType(enum.Enum):
    TRANSPORT = "transport"
    MILL = "mill"
    FARM = "farm"
    REFINERY = "refinery"
    MANUFACTURING = "manufaktur"

class Business(db.Model):
    __tablename__ = 'businesses'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Enum(ProductionType), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    additional_info = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(255),nullable=False)

    user = db.relationship('User', backref=db.backref('businesses', lazy=True))