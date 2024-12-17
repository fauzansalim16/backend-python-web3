from ..models import Farm, User
from ..extensions import db

def seed_farms():
    user = db.session.query(User).first()
    if not user:
        print("No user found in the database.")
        return
    farms = [
        {"farm_name": "kebun sawit sungai pinang", "owner_id": user.id, "location": "0.48474869965423717, 101.39003405954347"}
    ]
    for farm in farms:
        new_farm = Farm(farm_name = farm["farm_name"], owner_id = farm["owner_id"], location = farm ["location"])
        db.session.add(new_farm)

    try:
        db.session.commit()
        print("Farm seeder executed successfully.")
    except Exception as e:
        db.session.rollback() 
        print(f"Error seeding farms: {e}")