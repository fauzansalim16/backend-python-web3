from flask import Blueprint, jsonify, request
from ..models import Harvest, db
from ..utils.hash_record_utils import generate_record_hash
from ..utils.send_to_node import create_transaksi
from ..schemas.harvest_schemas import HarvestSchema

harvest_bp = Blueprint('harvest_bp', __name__, url_prefix='/api')

@harvest_bp.route('/harvests', methods=['GET'])
def get_harvests():
    # Langsung query ke database di dalam route
    harvests = Harvest.query.all()  # Mengambil semua data harvest
    schema = HarvestSchema(many=True)
    return jsonify(schema.dump(harvests))

@harvest_bp.route('/harvests', methods=['POST'])
#@jwt_required()
def create_harvest():
    try:
        data = request.get_json()
        
        if not all(key in data for key in ['farm_id', 'quantity', 'harvest_date']):
            return jsonify({"msg": "Missing required fields"}), 400
        
        # current_user = get_jwt_identity()
        # user_id = current_user['id']  
        
        # Buat entri harvest baru
        record_data = {
            "farm_id": data['farm_id'],
            "user_id": 1, #ambil dari jwt 
            "quantity": data['quantity'],
            "harvest_date": data['harvest_date']
        }
        record_hash = generate_record_hash(record_data)

        new_harvest = Harvest(
            farm_id = data['farm_id'],
            user_id = 1, #ambil dari jwt
            quantity = data['quantity'],
            harvest_date = data['harvest_date'],
            hash = record_hash
        )
        
        db.session.add(new_harvest)
        db.session.commit()
        
        # mengirim transaksi ke node
        # create_transaksi(new_harvest.id, new_harvest.hash, new_harvest.user_id)
        schema = HarvestSchema()
        return jsonify(schema.dump(new_harvest)), 201

    except Exception as e:
        return jsonify({"msg": "An error occurred", "error": str(e)}), 500
