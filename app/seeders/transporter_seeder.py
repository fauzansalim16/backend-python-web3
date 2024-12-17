from ..models import Transporter, User
from ..extensions import db

def seed_transporters():
    user = db.session.query(User).first()
    if not user:
        print("No user found in the database.")
        return
    transporters = [
        {"owner_id": user.id, "company_name": "pt truk sejahtera","location": "0.48474869965423717, 101.39003405954347"}
    ]
    for transporter in transporters:
        new_transporter = Transporter(company_name = transporter["company_name"], owner_id = transporter["owner_id"], location = transporter["location"])
        db.session.add(new_transporter)

    try:
        db.session.commit()
        print("Transporter seeder executed successfully.")
    except Exception as e:
        db.session.rollback() 
        print(f"Error seeding transporters: {e}")