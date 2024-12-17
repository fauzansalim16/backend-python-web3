from ..extensions import db
from datetime import datetime, timezone

class TransportDetail(db.Model):
    __tablename__ = 'transport_details'
    id = db.Column(db.Integer, primary_key=True)
    transport_id = db.Column(db.Integer, db.ForeignKey('transports.id'), nullable=False)
    harvest_id = db.Column(db.Integer, db.ForeignKey('harvests.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Relationships
    harvest = db.relationship('Harvest', backref=db.backref('transport_details', lazy=True))
