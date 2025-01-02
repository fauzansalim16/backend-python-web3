# FILE: app/schemas/product_schema.py
from ..extensions import ma
from ..models.business import Business

class BusinessSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Business
        load_instance = True
        include_fk = True  
    # Atur field apa yang ingin disertakan, seperti 'id' dan 'name'
    user = ma.Nested('UserSchema', only=['id', 'username'])  
