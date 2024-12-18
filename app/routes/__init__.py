from .production_routes import production_bp
from .user_routes import user_bp

# Daftar semua blueprint
all_blueprints = [production_bp, user_bp]
