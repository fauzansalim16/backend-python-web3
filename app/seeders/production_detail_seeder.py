from ..models import Production, ProductionDetail
from ..extensions import db


def seed_production_details():
    # Cari produksi yang ada di database
    production = db.session.query(Production).first()  # Ambil produksi dengan ID tertentu

    if not production:
        print("No production found with the specified ID in the database.")
        return

    # Buat satu detail produksi secara eksplisit tanpa loop
    new_detail = ProductionDetail(
        production_id=production.id,
        linked_productions_id=production.id,
        additional_info="Detail added",
    )

    db.session.add(new_detail)

    try:
        db.session.commit()
        print("ProductionDetail seeder executed successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding production details: {e}")
