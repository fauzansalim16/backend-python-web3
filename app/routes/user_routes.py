from flask import Blueprint, jsonify, request
from ..models import User, db
from ..schemas import UserSchema
from ..utils.crypto_utils import generate_ethereum_key_pair, encrypt_aes
from ..utils.bcrypt_utils import hash_password
from werkzeug.security import generate_password_hash

user_bp = Blueprint('user_bp', __name__, url_prefix='/api')
@user_bp.route('/users', methods=['GET'])
def get_harvests():
    # Langsung query ke database di dalam route
    users = User.query.all() 
    schema = UserSchema(many=True)
    return jsonify(schema.dump(users))

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
