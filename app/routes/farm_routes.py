from flask import Blueprint, jsonify, request
from ..models import Farm, db
from ..schemas import FarmSchema
from ..extensions import jwt_required, get_jwt_identity

farm_bp = Blueprint('farm_bp', __name__, url_prefix='/api')

@farm_bp.route('/farms/authorize', methods=['GET'])
@jwt_required()
def get_authorize_endpoint():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@farm_bp.route('/farms', methods=['GET'])
def get_farms():
    # Fetch all farms directly in the route
    farms = Farm.query.all()  # Directly querying the database without the service function
    schema = FarmSchema(many=True)
    return jsonify(schema.dump(farms))

@farm_bp.route('/farms', methods=['POST'])
def create_farm():
    data = request.json
    # Directly handling farm creation in the route
    new_farm = Farm(
        farm_name=data['farm_name'],
        owner_id=data['owner_id'],
        location=data['location']
    )
    db.session.add(new_farm)
    db.session.commit()
    schema = FarmSchema()
    return jsonify(schema.dump(new_farm)), 201
