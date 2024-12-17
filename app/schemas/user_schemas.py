from ..models import User
from ..extensions import ma

class UserSchema(ma.SQLAlchemyAutoSchema):
    role = ma.Nested('RoleSchema', only=['id', 'name'])

    class Meta:
        model = User
        load_instance = True
        include_fk = True
        exclude = (['password'])


