from ..models import User
from ..extensions import db
from werkzeug.security import generate_password_hash
from ..utils.crypto_utils import encrypt_aes

def seed_users():
    users = [
        {"username": "test1", "role_id": 1,"password": "password", "public_key":"gg","private_key":"c87509a1c067bbde78beb793e6fa76530b6382a4c0241e5e4a9ec0a0f44dc0d3"}
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