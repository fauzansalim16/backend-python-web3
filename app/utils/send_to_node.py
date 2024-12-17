from app.models import User 
from app.utils.crypto_utils import decrypt_aes
from web3 import Web3
from eth_account import Account
from flask import jsonify

# Inisialisasi koneksi Web3
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))  # Ganti node sesuai konfigurasi kamu

def send_to_blockchain(id_transaction, hash_value, private_key):
    """
    Mengirim data sederhana ke blockchain menggunakan Web3.py.
    """
    try:
        # Format data menjadi string JSON sederhana
        transaction_data = {
            "id_transaction": id_transaction,
            "hash": hash_value
        }
        
        # Encode data menjadi hex
        encoded_data = web3.to_hex(text=str(transaction_data))
        
        # Dapatkan nonce untuk transaksi
        sender_account = Account.from_key(private_key)
        nonce = web3.eth.get_transaction_count(sender_account.address)

        # Buat transaksi
        transaction = {
            'to': '0x0000000000000000000000000000000000000000',  # Address tujuan (contoh: alamat kosong)
            'value': 0,
            'gas': 21000,
            'gasPrice': web3.to_wei('1', 'gwei'),
            'nonce': nonce,
            'data': encoded_data,
            'chainId': 1337  # Chain ID (ganti sesuai jaringan kamu)
        }

        # Tanda tangani transaksi
        signed_tx = Account.sign_transaction(transaction, private_key)
        
        # Kirim transaksi ke node blockchain
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return web3.to_hex(tx_hash)  # Mengembalikan hash transaksi
    except Exception as e:
        raise Exception(f"Failed to send transaction: {str(e)}")


def create_transaksi(transaction_id, hash_value, user_id):
    try:
        # Ambil user dari database
        user = User.query.get(user_id)
        if not user or not user.private_key:
            return jsonify({"msg": "Private key not found for the given user"}), 404
        
        # Dekripsi private key user
        private_key = decrypt_aes(user.private_key)
        
        # Kirim data ke blockchain
        tx_hash = send_to_blockchain(transaction_id, hash_value, private_key)

        return jsonify({
            "msg": "Transaction sent successfully",
            "transaction_id": transaction_id,
            "hash": hash_value,
            "blockchain_tx_hash": tx_hash
        }), 200
    except Exception as e:
        return jsonify({"msg": "An error occurred", "error": str(e)}), 500

