from ..models import Business, User
from ..extensions import db


def seed_businesses():
    user = db.session.query(User).first()
    if not user:
        print("No user found in the database.")
        return

    # Tambahkan bisnis secara eksplisit tanpa loop
    business1 = db.session.query(Business).filter_by(name="PT Sawit Jaya").first()
    if not business1:
        business1 = Business(
            name="PT Sawit Jaya",
            owner_id=user.id,
            type="TRANSPORT",
            location="Jakarta",
        )
        db.session.add(business1)

    business2 = db.session.query(Business).filter_by(name="Mills CPO X").first()
    if not business2:
        business2 = Business(
            name="Mills CPO X",
            owner_id=user.id,
            type="MILL",
            location="Riau",
        )
        db.session.add(business2)

    business3 = db.session.query(Business).filter_by(name="Farm A").first()
    if not business3:
        business3 = Business(
            name="Farm A",
            owner_id=user.id,
            type="FARM",
            location="Lampung",
        )
        db.session.add(business3)

    try:
        db.session.commit()
        print("Business seeder executed successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding businesses: {e}")
