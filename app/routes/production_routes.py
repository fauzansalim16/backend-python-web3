from flask import Blueprint, jsonify, request, json
from ..schemas.production_schemas import ProductionSchema
from ..models import Production, User, db
from ..utils.hash_record_utils import generate_record_hash
from ..utils.crypto_utils import decrypt_aes, hex_to_bytes
from ..utils.get_from_node import BlockchainQuery
from ..extensions import joinedload
from app.utils.blockchain_transaction_utils import store_transaction
from app.config import Config

production_bp = Blueprint('transport_bp', __name__, url_prefix='/api')

blockchain_query = BlockchainQuery(
    node_url='http://127.0.0.1:8545',  
    contract_address='0x2C2B9C9a4a25e24B174f26114e8926a9f2128FE4'
)

@production_bp.route('/productions/offchain/<hash_data>', methods=['GET'])
def get_blockchain_transaction_by_hash(hash_data):
    try:
        result = blockchain_query.get_transaction_by_offchain_hash(hash_data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@production_bp.route('/productions/test', methods=['POST'])
def get_blockchain_transaction_by_hashes():
    """
    API Endpoint untuk mendapatkan informasi transaksi dari hash data off-chain dan hash transaksi blockchain.
    """
    try:
        # Ambil input dari body request
        request_data = request.get_json()
        hash_data = request_data.get('hash_data')
        tx_hash = request_data.get('tx_hash')

        # Validasi input
        if not hash_data or not tx_hash:
            raise ValueError("Both 'hash_data' and 'tx_hash' are required.")

        # Panggil fungsi dari BlockchainQuery
        result = blockchain_query.get_transaction_by_offchain_and_blockchain_hashes(hash_data, tx_hash)
        return jsonify(result), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': f"Error retrieving transaction details: {str(e)}"}), 500


@production_bp.route('/productions', methods=['GET'])
def get_productions():
    productions = Production.query.options(
        joinedload(Production.production_details),
        joinedload(Production.user),  # Memuat relasi users
        joinedload(Production.business)  # Memuat relasi businesses
    ).all()
  
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
            "user_id": 12, #ambil dari jwt 
            "type": data['type'],
            "quantity": data['quantity'],
            "production_location": data['production_location'],
            "additional_info": additional_info, 
            "production_time": data['production_time']
        }
        record_hash = generate_record_hash(record_data)

        new_productions = Production(
            business_id = data['business_id'],
            user_id = 12, #ambil dari jwt
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
        
        # user = User.query.filter_by(id=new_productions.user_id).first()
        # decrypt_private_key = decrypt_aes(Config.PRIVATE_KEY)

        user = User.query.filter_by(id=new_productions.user_id).first()

        encrypted_private_key = hex_to_bytes(user.private_key)
        decrypt_private_key = decrypt_aes(encrypted_private_key)

        # mengirim transaksi ke node
        tx_receipt = store_transaction(new_productions.id, new_productions.linked_productions_id, new_productions.hash, decrypt_private_key)
        
        blockchain_data = {
            'transaction_hash': tx_receipt['transactionHash'].hex(),
            'block_number': tx_receipt['blockNumber'],
            'block_hash': tx_receipt['blockHash'].hex()
        }

        # Update additional_info di database
        new_productions.additional_info = json.dumps(blockchain_data)  # Konversi ke string JSON
        db.session.commit()

        # Menyiapkan data response
        response_data = {
            'production': ProductionSchema().dump(new_productions),
            'blockchain_receipt': {
                'transaction_hash': tx_receipt['transactionHash'].hex(),
                'block_number': tx_receipt['blockNumber'],
                'block_hash': tx_receipt['blockHash'].hex(),
                'gas_used': tx_receipt['gasUsed'],
                'status': 'Success' if tx_receipt['status'] == 1 else 'Failed'
            }
        }

        return jsonify(response_data), 201
    except Exception as e:
        return jsonify({"msg": "An error occurred", "error": str(e)}), 500