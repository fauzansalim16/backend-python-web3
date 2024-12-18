from ..models import Business, User, Production
from datetime import datetime, timezone
from ..extensions import db


def seed_productions():
    # Cari user dan bisnis yang sesuai
    user = db.session.query(User).first()
    business = db.session.query(Business).first()

    if not user:
        print("No user found in the database.")
        return

    if not business:
        print("No business found with the name 'tukul'.")
        return

    # Buat produksi spesifik tanpa loop
    new_production = Production(
        business_id=business.id,
        user_id=user.id,
        linked_productions_id=[1],
        type="FARM",
        production_location="jakarta",
        production_time=datetime.now(timezone.utc),
        additional_info="Some info",
        hash="some-hash-value",
    )

    new_production2 = Production(
        business_id=business.id,
        user_id=user.id,
        linked_productions_id=[1],
        type="FARM",
        production_location="bandung",
        production_time=datetime.now(timezone.utc),
        additional_info="Additional info for production 2",
        hash="some-hash-value-2",
    )

    db.session.add(new_production)
    db.session.add(new_production2)

    try:
        db.session.commit()
        print("Production seeder executed successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding productions: {e}")
