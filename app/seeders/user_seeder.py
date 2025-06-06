from ..models import User
from ..extensions import db
from werkzeug.security import generate_password_hash
from ..utils.crypto_utils import encrypt_aes

def seed_users():
    users = [
        {"username": "owner_test_1", "role_id": 1,"password": "password", "public_key":"0xc02251ee9b46423918b86a66e941a57e677cba44ad6c477dd171bb942cd158aab8607b2478504c5bc0554bdba80c39f55f6bdda556d0aaeeba4bcdbdba12e3d11","private_key":"c87509a1c067bbde78beb793e6fa76530b6382a4c0241e5e4a9ec0a0f44dc0d3"}
    ]

    for user in users:
        new_user = User(username = user["username"], role_id = user["role_id"], password=generate_password_hash(user["password"]), public_key = user["public_key"], private_key = encrypt_aes(user["private_key"]))
        db.session.add(new_user)

    try:
        db.session.commit()
        print("User seeder executed successfully.")
    except Exception as e:
        db.session.rollback() 
        print(f"Error seeding users: {e}")