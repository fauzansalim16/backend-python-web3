from ..extensions import db, ARRAY
from datetime import datetime, timezone

class Transport(db.Model):
    __tablename__ = 'transports'
    id = db.Column(db.Integer, primary_key=True)
    transporter_id = db.Column(db.Integer, db.ForeignKey('transporters.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, nullable=False)
    harvests_id = db.Column(ARRAY(db.Integer), nullable=False) 
    pickup_location = db.Column(db.String(255), nullable=False)
    delivery_location = db.Column(db.String(255), nullable=False)
    pickup_time = db.Column(db.DateTime, nullable=False)
    delivery_time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    hash = db.Column(db.String(255), nullable=True)
    
    # Relationships
    transporter = db.relationship('Transporter', backref=db.backref('transports', lazy=True))
    user = db.relationship('User', backref=db.backref('transports', lazy=True))
    transport_details = db.relationship('TransportDetail', backref='transport', lazy=True)


