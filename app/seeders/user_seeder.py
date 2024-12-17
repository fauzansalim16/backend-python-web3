from ..models import User
from ..extensions import db
from werkzeug.security import generate_password_hash

def seed_users():
    users = [
        {"username": "owner1", "role_id": 1,"password": "password123", "public_key":"gg","private_key":"gg"},
        {"username": "transporter1", "role_id": 2,"password": "password123","public_key":"gg","private_key":"gg"},
        {"username": "farmer1", "role_id": 3,"password": "password123","public_key":"gg","private_key":"gg"},
        {"username": "miller1", "role_id": 4,"password": "password123","public_key":"gg","private_key":"gg"},
        {"username": "refiner1", "role_id": 5,"password": "password123","public_key":"gg","private_key":"gg"},
    ]

    for user in users:
        new_user = User(username = user["username"], role_id = user["role_id"], password=generate_password_hash(user["password"]), public_key = user["public_key"], private_key = user["private_key"])
        db.session.add(new_user)

    try:
        db.session.commit()
        print("User seeder executed successfully.")
    except Exception as e:
        db.session.rollback() 
        print(f"Error seeding users: {e}")