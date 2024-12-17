# FILE: app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from sqlalchemy.orm import joinedload
from marshmallow import fields
from sqlalchemy.dialects.postgresql import ARRAY

# Impor cryptography yang diperlukan
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from eth_keys import keys

# Initialize extensions
jwt = JWTManager()
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

__all__ = ['jwt', 'jwt_required', 'get_jwt_identity', 'joinedload', 'fields', 'ARRAY', 'rsa', 'serialization', 'Cipher', 'algorithms', 'modes', 'padding', 'default_backend', 'keys']

