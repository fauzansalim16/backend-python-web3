from flask import json
# from app.models import User
# from app import create_app
# from app.utils.crypto_utils import decrypt_aes

# # Fungsi untuk mengonversi string hex ke bytes
# def hex_to_bytes(hex_str):
#     # Menghilangkan prefix '\x' dan mengonversi ke bytes
#     hex_str = hex_str.replace("\\x", "")
#     return bytes.fromhex(hex_str)

# def get_user_by_id(user_id):
#     # Inisialisasi aplikasi Flask
#     app = create_app()

#     # Membuat konteks aplikasi
#     with app.app_context():
#         # Query user berdasarkan ID
#         user = User.query.get(user_id)
#         if not user:
#             return jsonify({"error": "User not found"}), 404

#         # Mengonversi private_key dari hex string ke bytes
#         private_key_hex = user.private_key  # Asumsi data private_key ada dalam format hex

#         # Mengonversi hex ke bytes
#         encrypted_private_key = hex_to_bytes(private_key_hex)

#         # Dekripsi private_key
#         decrypted_private_key = decrypt_aes(encrypted_private_key)
        
#         # Return decrypted private_key
#         return decrypted_private_key

# if __name__ == "__main__":
#     result = get_user_by_id(7)
#     print(result)

from web3 import Web3
from typing import Dict, Any, Optional

class BlockchainQuery:
    def __init__(self, node_url: str, contract_address: str):
        self.w3 = Web3(Web3.HTTPProvider(node_url))
        self.contract_address = contract_address
        
        # ABI untuk fungsi yang kita butuhkan
        self.contract_abi = [
            {
                "inputs": [
                    {
                        "internalType": "string",
                        "name": "_hash",
                        "type": "string"
                    }
                ],
                "name": "getTransactionByHash",
                "outputs": [
                    {
                        "components": [
                            {
                                "internalType": "uint256",
                                "name": "creatorID",
                                "type": "uint256"
                            },
                            {
                                "internalType": "uint256[]",
                                "name": "broughtIDs",
                                "type": "uint256[]"
                            },
                            {
                                "internalType": "string",
                                "name": "hash",
                                "type": "string"
                            },
                            {
                                "internalType": "uint256",
                                "name": "timestamp",
                                "type": "uint256"
                            }
                        ],
                        "internalType": "struct SupplyChain.Transaction",
                        "name": "",
                        "type": "tuple"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            }
        ]
        
        # Inisialisasi kontrak
        self.contract = self.w3.eth.contract(
            address=self.contract_address, 
            abi=self.contract_abi
        )

    def get_transaction_by_offchain_hash(self, hash_data: str) -> Dict[str, Any]:
        """
        Mengambil data transaksi dari blockchain berdasarkan hash off-chain
        
        Args:
            hash_data (str): Hash data off-chain
            
        Returns:
            Dict dengan data transaksi
        """
        try:
            # Panggil fungsi smart contract
            result = self.contract.functions.getTransactionByHash(hash_data).call()
            
            # Format hasil ke dictionary
            return {
                'creator_id': result[0],
                'brought_ids': result[1],
                'hash': result[2],
                'timestamp': result[3]
            }
        except Exception as e:
            raise Exception(f"Error getting transaction by hash: {str(e)}")

    def get_transaction_by_tx_hash(self, tx_hash: str) -> Optional[Dict[str, Any]]:
        """
        Mengambil data transaksi dari blockchain berdasarkan transaction hash
        
        Args:
            tx_hash (str): Transaction hash dari blockchain
            
        Returns:
            Dict dengan data transaksi dan receipt
        """
        try:
            # Hapus prefix '0x' jika ada
            if tx_hash.startswith('0x'):
                tx_hash = tx_hash[2:]
            
            # Convert ke bytes
            tx_hash_bytes = bytes.fromhex(tx_hash)
            
            # Dapatkan transaction receipt
            tx_receipt = self.w3.eth.get_transaction_receipt(tx_hash_bytes)
            
            # Dapatkan transaction detail
            tx_detail = self.w3.eth.get_transaction(tx_hash_bytes)
            
            # Decode input data menggunakan ABI
            func_obj, func_params = self.contract.decode_function_input(tx_detail['input'])
            
            return {
                'transaction': {
                    'creator_id': func_params['_creatorID'],
                    'brought_ids': func_params['_broughtIDs'],
                    'hash': func_params['_hash'],
                    'timestamp': func_params['_timestamp']
                },
                'receipt': {
                    'block_number': tx_receipt['blockNumber'],
                    'block_hash': tx_receipt['blockHash'].hex(),
                    'transaction_hash': tx_receipt['transactionHash'].hex(),
                    'gas_used': tx_receipt['gasUsed'],
                    'status': 'Success' if tx_receipt['status'] == 1 else 'Failed'
                }
            }
        except Exception as e:
            raise Exception(f"Error getting transaction by tx hash: {str(e)}")

# Contoh penggunaan
if __name__ == "__main__":
    # Inisialisasi dengan URL node dan alamat kontrak
    blockchain_query = BlockchainQuery(
        node_url='http://your-node-url:port',
        contract_address='YOUR_CONTRACT_ADDRESS'
    )
    
    try:
        # Contoh mengambil data berdasarkan hash off-chain
        offchain_hash = "e5b292c3e2efd9203b9b57c7904f98fad784d027dd618d7d9f90a370c968e13c8"
        result1 = blockchain_query.get_transaction_by_offchain_hash(offchain_hash)
        print("\nData dari hash off-chain:")
        print(json.dumps(result1, indent=2))
        
        # Contoh mengambil data berdasarkan transaction hash
        tx_hash = "0x123abc..." # Ganti dengan transaction hash yang valid
        result2 = blockchain_query.get_transaction_by_tx_hash(tx_hash)
        print("\nData dari transaction hash:")
        print(json.dumps(result2, indent=2))
        
    except Exception as e:
        print(f"Error: {str(e)}")