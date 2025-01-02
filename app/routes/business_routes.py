from flask import Blueprint, jsonify, request
from ..models.business import Business, db, ProductionType
from ..schemas import BusinessSchema
from datetime import datetime, timezone

business_bp = Blueprint('business_bp', __name__, url_prefix='/api')

@business_bp.route('/businesses', methods=['GET'])
def get_users():
    businesses = Business.query.all()
    schema = BusinessSchema(many=True)
    return jsonify(schema.dump(businesses))

@business_bp.route('/businesses', methods=['POST'])
def create_business():
    try:
        data = request.get_json()

        # Validate and parse input data
        owner_id = data.get('owner_id')
        name = data.get('name')
        type_value = data.get('type')
        additional_info = data.get('additional_info')
        location = data.get('location')

        if not owner_id or not name or not type_value or not location:
            return jsonify({"error": "owner_id, name, type, and location are required fields."}), 400

        try:
            production_type = ProductionType[type_value.upper()]
        except KeyError:
            return jsonify({"error": "Invalid production type."}), 400

        new_business = Business(
            owner_id=owner_id,
            name=name,
            type=production_type,
            additional_info=additional_info,
            location=location,
            created_at=datetime.now(timezone.utc)
        )

        db.session.add(new_business)
        db.session.commit()

        schema = BusinessSchema()
        return jsonify(schema.dump(new_business)), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
