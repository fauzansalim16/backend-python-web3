from ..models import Role
from ..extensions import db

def seed_roles():
    roles = [
        {"id": 1, "name": "Owner"},
        {"id": 2, "name": "Transporter"},
        {"id": 3, "name": "Farmer"},
        {"id": 4, "name": "Miller"},
        {"id": 5, "name": "Refiner"},
    ]
    for role in roles:
        new_role = Role(name=role["name"])
        db.session.add(new_role)

    try:
        db.session.commit()
        print("Role seeder executed successfully.")
    except Exception as e:
        db.session.rollback() 
        print(f"Error seeding roles: {e}")