import bcrypt

def hash_password(password):
    # Gunakan gensalt() dan langsung encode
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')