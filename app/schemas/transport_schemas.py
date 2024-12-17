from ..extensions import ma,fields
from ..models import Transport, TransportDetail

# Schema untuk Transport
class TransportSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Transport
        load_instance = True
        include_fk = True  # Menyertakan foreign key dalam hasil

    # Relasi ke TransportDetail, menyertakan data detail seperti 'id' dan lainnya
    transport_details = fields.List(fields.Nested('TransportDetailSchema', only=['id']))

# Schema untuk TransportDetail
class TransportDetailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TransportDetail
        load_instance = True
