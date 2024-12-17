from ..models import Transport, Transporter, User, Harvest
from ..extensions import db

def seed_transports():
    transporter = db.session.query(Transporter).first()
    user = db.session.query(User).first()
    harvests = db.session.query(Harvest.id).limit(3).all()

    if not transporter:
        print("No transporter found in the database.")
        return
    if not user:
        print("No user found in the database.")
        return
    if not harvests:
        print("No harvests found in the database.")
        return
    
    # Extracting the harvest IDs from the result tuple (harvests are returned as tuples)
    harvest_ids = [harvest[0] for harvest in harvests]

    transports = [
        {
            "transporter_id": transporter.id,
            "user_id": user.id,
            "vehicle_id": 12313,
            "harvests_id": harvest_ids,  # Assigning the array of harvest ids
            "pickup_location": "0.48474869965423717, 101.39003405954347",
            "delivery_location": "0.48474869965423717, 101.39003405954347",
            "pickup_time": '2024-12-15 21:28',
            "delivery_time": '2024-11-15 21:28'
        }
    ]
    
    for transport in transports:
        new_transport = Transport(
            transporter_id=transport["transporter_id"], 
            user_id=transport["user_id"], 
            vehicle_id=transport["vehicle_id"],
            harvests_id=transport["harvests_id"],  # Properly setting harvests_id
            pickup_location=transport["pickup_location"], 
            delivery_location=transport["delivery_location"],
            pickup_time=transport["pickup_time"],
            delivery_time=transport["delivery_time"]
        )
        db.session.add(new_transport)

    try:
        db.session.commit()
        print("Transport seeder executed successfully.")
    except Exception as e:
        db.session.rollback() 
        print(f"Error seeding transports: {e}")
