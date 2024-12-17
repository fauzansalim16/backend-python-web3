from ..models import TransportDetail, Transport, Harvest
from ..extensions import db

def seed_transport_details():
    transport = db.session.query(Transport).first()
    harvests = db.session.query(Harvest.id).limit(3).all()
    if not transport:
        print("No farm found in the database.")
        return
    
    if len(harvests) < 3:
        print("Not enough harvests available.")
        return

    transportDetails = [
        {"transport_id": transport.id, "harvest_id": harvests[0][0]},
        {"transport_id": transport.id, "harvest_id": harvests[1][0]},
        {"transport_id": transport.id, "harvest_id": harvests[2][0]}
    ]
    for transportDetail in transportDetails:
        new_transportDetail = TransportDetail(transport_id = transportDetail["transport_id"], harvest_id = transportDetail["harvest_id"])
        db.session.add(new_transportDetail)

    try:
        db.session.commit()
        print("TransportDetail seeder executed successfully.")
    except Exception as e:
        db.session.rollback() 
        print(f"Error seeding transportDetails: {e}")