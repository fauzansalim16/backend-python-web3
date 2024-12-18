from app.extensions import db
from app.seeders import (
    seed_roles, 
    seed_users, 
)
from app.seeders.business_seeder import seed_businesses
from app.seeders.production_seeder import seed_productions
from app.seeders.production_detail_seeder import seed_production_details

# Mapping seeder names to functions, with the correct order
SEEDERS = {
    "role_seeder": seed_roles,             
    "user_seeder": seed_users,             
    "business_seeder": seed_businesses,
    "production_seeder": seed_productions,
    "production_detail_seeder": seed_production_details,

}

def run_specific_seeder(seeder_name):
    """
    Fungsi ini menjalankan seeder tertentu berdasarkan nama seeder.
    """
    from app.__init__ import create_app
    app = create_app()
    
    seeder = SEEDERS.get(seeder_name)
    if not seeder:
        print(f"Seeder '{seeder_name}' not found!")
        return

    with app.app_context():
        seeder()
        print(f"Seeder '{seeder_name}' executed successfully!")

def run_all_seeders():
    """
    Fungsi ini menjalankan semua seeders dalam urutan yang benar.
    """
    from app.__init__ import create_app
    app = create_app()

    with app.app_context():
        db.drop_all()  
        db.create_all() 

        print("Starting to run all seeders...")

        # Menjalankan seeders sesuai urutan yang benar
        for seeder_name in SEEDERS:
            run_specific_seeder(seeder_name)
        
        print("All seeders executed successfully!")
