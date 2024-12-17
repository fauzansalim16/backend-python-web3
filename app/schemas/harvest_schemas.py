from ..extensions import ma
from ..models.harvest import Harvest

class HarvestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Harvest
        load_instance = True
        include_fk = True  
    #warning! karena dapat menyembabkan N+1
    user = ma.Nested('UserSchema', only=('id', 'username')) 
