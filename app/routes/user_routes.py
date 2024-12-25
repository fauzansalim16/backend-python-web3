from flask import Blueprint, jsonify, request
from ..models import User, db
from ..schemas import UserSchema
from ..utils.crypto_utils import generate_ethereum_key_pair, encrypt_aes
from ..utils.bcrypt_utils import hash_password
from ..extensions import jwt_required, get_jwt_identity
from werkzeug.exceptions import NotFound

user_bp = Blueprint('user_bp', __name__, url_prefix='/api')

@user_bp.route('/users/authorize', methods=['GET'])
@jwt_required()
def get_authorize_endpoint():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@user_bp.route('/users', methods=['GET'])
def get_users():
    # Langsung query ke database di dalam route
    users = User.query.all() 
    schema = UserSchema(many=True)
    return jsonify(schema.dump(users))

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    # Cari user berdasarkan ID
    user = User.query.get(user_id)
    
    if user is None:
        return jsonify({"message": "User not found"}), 404
    
    schema = UserSchema()
    return jsonify(schema.dump(user)), 200

#Todo hanya user dengan role = Owner yang bisa mengakses api ini 
@user_bp.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()

        if not all(key in data for key in ['username', 'password', 'role_id']):
            return jsonify({"msg": "Missing required fields"}), 400

        # Generate RSA keys
        private_key, public_key = generate_ethereum_key_pair()

        encrypted_private_key = encrypt_aes(private_key)

        # Create new user
        new_user = User(
            username=data['username'],
            password=hash_password(data['password']),
            role_id=data['role_id'],
            public_key=public_key,
            private_key=encrypted_private_key,  # Simpan byte langsung
        )

        db.session.add(new_user)
        db.session.commit()

        schema = UserSchema()
        return jsonify(schema.dump(new_user)), 201

    except Exception as e:
        return jsonify({"msg": "An error occurred", "error": str(e)}), 500

#Todo hanya user dengan role = Owner yang bisa mengakses api ini 
@user_bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    
    if not user:
        raise NotFound(f"User with id {id} not found.")
    
    # Hapus user dari database
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({"message": f"User with id {id} has been deleted."}), 200