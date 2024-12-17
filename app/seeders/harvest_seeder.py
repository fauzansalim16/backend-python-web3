from ..models import Harvest, Farm, User
from ..extensions import db
from ..utils.hash_record_utils import generate_record_hash
from datetime import datetime, timezone

# Seeder untuk Harvest
def seed_harvests():
    farm = db.session.query(Farm).first()
    user = db.session.query(User).first()
    if not farm:
        print("No farm found in the database.")
        return
    if not user:
        print("No user found in the database.")
        return
    
    # Data harvests
    harvests = [
        {"farm_id": farm.id, "user_id": user.id, "quantity": 100, "harvest_date": '2024-11-15 21:28'},
        {"farm_id": farm.id, "user_id": user.id, "quantity": 100, "harvest_date": '2024-10-15 21:28'},
        {"farm_id": farm.id, "user_id": user.id, "quantity": 100, "harvest_date": '2024-12-15 21:28'}

    ]

    # Tambahkan data harvest ke database
    for harvest in harvests:
        # Buat hash dari record
        record_data = {
            "farm_id": harvest["farm_id"],
            "user_id": harvest["user_id"],
            "quantity": harvest["quantity"],
            "harvest_date": harvest["harvest_date"],
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        record_hash = generate_record_hash(record_data)

        # Buat instance Harvest
        new_harvest = Harvest(
            farm_id=harvest["farm_id"],
            user_id=harvest["user_id"],
            quantity=harvest["quantity"],
            harvest_date=harvest["harvest_date"],
            hash=record_hash
        )
        db.session.add(new_harvest)

    # Commit perubahan ke database
    try:
        db.session.commit()
        print("Harvest seeder executed successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding harvests: {e}")
