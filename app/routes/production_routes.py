from flask import Blueprint, jsonify, request
from ..schemas.production_schemas import ProductionSchema
from ..models import Production, db
from ..utils.hash_record_utils import generate_record_hash
from ..extensions import joinedload

production_bp = Blueprint('transport_bp', __name__, url_prefix='/api')

@production_bp.route('/productions', methods=['GET'])
def get_productions():
    productions = Production.query.options(joinedload(Production.production_details)).all()

    production_schema = ProductionSchema(many=True)

    return jsonify(production_schema.dump(productions)), 200

@production_bp.route('/productions/<int:production_id>', methods=['GET'])
def get_production_details(production_id):
    # Gunakan joinedload untuk memastikan detail dimuat
    production = Production.query.options(
        joinedload(Production.production_details)
    ).get_or_404(production_id)
    
    production_schema = ProductionSchema()
    return jsonify(production_schema.dump(production)), 200

@production_bp.route('/productions', methods=['POST'])
#@jwt_required()
def create_production():
    try:
        data = request.get_json()
        
        if not all(key in data for key in ['business_id', 'linked_productions_id', 'type','quantity', 'production_location','production_time']):
            return jsonify({"msg": "Missing required fields"}), 400
        
        additional_info = data.get('additional_info', None)

        # current_user = get_jwt_identity()
        # user_id = current_user['id']  
        
        # Buat entri harvest baru
        record_data = {
            "business_id": data['business_id'],
            "linked_productions_id": data['linked_productions_id'],
            "user_id": 1, #ambil dari jwt 
            "type": data['type'],
            "quantity": data['quantity'],
            "production_location": data['production_location'],
            "additional_info": additional_info, 
            "production_time": data['production_time']
        }
        record_hash = generate_record_hash(record_data)

        new_productions = Production(
            business_id = data['business_id'],
            user_id = 1, #ambil dari jwt
            linked_productions_id = data['linked_productions_id'],
            quantity = data['quantity'],
            type = data['type'],
            production_location = data['production_location'],
            additional_info=additional_info, 
            production_time = data['production_time'],
            hash = record_hash
        )
        
        db.session.add(new_productions)
        db.session.commit()
        
        # mengirim transaksi ke node
        # create_transaksi(new_harvest.id, new_harvest.hash, new_harvest.user_id)
        schema = ProductionSchema()
        return jsonify(schema.dump(new_productions)), 201

    except Exception as e:
        return jsonify({"msg": "An error occurred", "error": str(e)}), 500