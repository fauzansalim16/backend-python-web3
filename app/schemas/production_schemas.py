from ..extensions import ma,fields
from ..models import Production, ProductionDetail

# Schema untuk Transport
class ProductionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Production
        load_instance = True
        include_fk = True 

    # Relasi ke TransportDetail, menyertakan data detail seperti 'id' dan lainnya
    production_details = fields.List(fields.Nested('ProductionDetailSchema'))
    user = fields.Nested('UserSchema', only=['id', 'username']) 
    business = fields.Nested('BusinessSchema', only=['id', 'name', 'type'])  

# Schema untuk TransportDetail
class ProductionDetailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductionDetail
        load_instance = True
        include_fk = True 

