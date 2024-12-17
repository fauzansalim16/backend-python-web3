from app.extensions import db
from app.seeders import (
    seed_roles, 
    seed_users, 
    seed_farms, 
    seed_harvests, 
    seed_transporters, 
    seed_transports, 
    seed_transport_details
)

# Mapping seeder names to functions, with the correct order
SEEDERS = {
    "role_seeder": seed_roles,             
    "user_seeder": seed_users,             
    "farm_seeder": seed_farms,             
    "harvest_seeder": seed_harvests,       
    "transporter_seeder": seed_transporters,
    "transport_seeder": seed_transports,
    "transport_detail_seeder": seed_transport_details
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
