from .farm_routes import farm_bp
from .harvest_routes import harvest_bp
from .transport_routes import transport_bp
from .user_routes import user_bp

# Daftar semua blueprint
all_blueprints = [farm_bp, harvest_bp, transport_bp, user_bp]
