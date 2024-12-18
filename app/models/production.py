from ..extensions import db, ARRAY
from datetime import datetime, timezone
import enum
from sqlalchemy.orm import relationship


# Enum untuk mendefinisikan nilai yang diizinkan
class ProductionType(enum.Enum):
    TRANSPORT = "transport"
    MILL = "mill"
    FARM = "farm"
    REFINERY = "refinery"
    MANUFACTURING = "manufaktur"


class Production(db.Model):
    __tablename__ = 'productions'

    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    linked_productions_id = db.Column(ARRAY(db.Integer), nullable=False) 
    type = db.Column(db.Enum(ProductionType), nullable=False)
    production_location = db.Column(db.String(255), nullable=False)
    production_time = db.Column(db.DateTime, nullable=False)
    additional_info = db.Column(db.String(255), nullable=True)
    quantity = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    hash = db.Column(db.String(255), nullable=False)
    
    #Relationships
    business = db.relationship('Business', backref=db.backref('productions', lazy=True))
    user = db.relationship('User', backref=db.backref('productions', lazy=True))

    production_details = relationship(
        'ProductionDetail', 
        foreign_keys='[ProductionDetail.production_id]',
        backref='productions'
    )
    
    # Jika perlu, tambahkan relationship lain
    linked_production_details = relationship(
        'ProductionDetail', 
        foreign_keys='[ProductionDetail.linked_productions_id]'
    )

