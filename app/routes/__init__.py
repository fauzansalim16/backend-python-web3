from .production_routes import production_bp
from .user_routes import user_bp
from .business_routes import business_bp

# Daftar semua blueprint
all_blueprints = [production_bp, user_bp, business_bp]
