# FILE: app/models/harvest.py
from ..extensions import db
from datetime import datetime, timezone

class Harvest(db.Model):
    __tablename__ = 'harvests'
    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    harvest_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    hash = db.Column(db.String(255), nullable=False)
    """
    backref('harvests') adalah nama object yang akan digunakan saat pemanggilan nanti
    contoh user = User.query.get(1)
    user_harvests = user.harvests
    """
    farm = db.relationship('Farm', backref=db.backref('harvests', lazy=True))
    user = db.relationship('User', backref=db.backref('harvests', lazy=True))
