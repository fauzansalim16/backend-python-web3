from ..extensions import db
from datetime import datetime, timezone
from sqlalchemy.orm import relationship

class ProductionDetail(db.Model):
    __tablename__ = 'production_details'
    id = db.Column(db.Integer, primary_key=True)
    production_id = db.Column(db.Integer, db.ForeignKey('productions.id'), nullable=False)
    linked_productions_id = db.Column(db.Integer, db.ForeignKey('productions.id'), nullable=False)
    additional_info = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
