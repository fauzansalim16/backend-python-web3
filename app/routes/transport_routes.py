from flask import Blueprint, jsonify, request
from ..schemas.transport_schemas import TransportSchema
from ..models import Transport
from ..extensions import joinedload

transport_bp = Blueprint('transport_bp', __name__, url_prefix='/api')

@transport_bp.route('/transports', methods=['GET'])
def get_transports():
    transports = Transport.query.options(joinedload(Transport.transport_details)).all()

    transport_schema = TransportSchema(many=True)

    return jsonify(transport_schema.dump(transports)), 200
