from app.extensions import keys, Cipher, algorithms, modes, padding, default_backend
import os
import secrets
from app.config import Config

def generate_ethereum_key_pair():
    # Generate private key
    private_key_bytes = secrets.token_bytes(32)
    private_key = keys.PrivateKey(private_key_bytes)
    
    # Derive public key
    public_key = private_key.public_key
    
    # Konversi ke format hex
    private_key_hex = private_key.to_hex()
    public_key_hex = public_key.to_hex()
    
    return private_key_hex, public_key_hex

# Key size for AES-256 encryption
aes_key_size = Config.AES_KEY_SIZE
encryption_key = Config.ENCRYPTION_KEY

def encrypt_aes(plain_text):
    #Konversi key ke bytes agar konsisten
    key_bytes = encryption_key.encode() if isinstance(encryption_key, str) else encryption_key
    key_bytes = key_bytes[:aes_key_size]  
    
    iv = os.urandom(16)
    
    try:
        cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # Padding
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(plain_text.encode('utf-8')) + padder.finalize()

        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        return iv + encrypted_data  # Prepend IV
    except Exception as e:
        print(f"Encryption error: {e}")
        raise

def decrypt_aes(encrypted_data):
    #Konversi key ke bytes
    key_bytes = encryption_key.encode() if isinstance(encryption_key, str) else encryption_key
    key_bytes = key_bytes[:aes_key_size]
    
    try:
        iv = encrypted_data[:16]
        encrypted_data = encrypted_data[16:]
        
        cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        decrypted_padded = decryptor.update(encrypted_data) + decryptor.finalize()

        # Remove padding
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()
        
        return decrypted.decode('utf-8')
    except Exception as e:
        print(f"Decryption error: {e}")
        raise