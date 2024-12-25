# utils/send_to_node.py

from web3 import Web3
from typing import Dict, Any, Optional

class BlockchainQuery:
    def __init__(self, node_url: str, contract_address: str):
        self.w3 = Web3(Web3.HTTPProvider(node_url))
        self.contract_address = contract_address
        
        self.contract_abi = [
            {
                "inputs": [{"internalType": "string", "name": "_hash", "type": "string"}],
                "name": "getTransactionByHash",
                "outputs": [{
                    "components": [
                        {"internalType": "uint256", "name": "creatorID", "type": "uint256"},
                        {"internalType": "uint256[]", "name": "broughtIDs", "type": "uint256[]"},
                        {"internalType": "string", "name": "hash", "type": "string"},
                        {"internalType": "uint256", "name": "timestamp", "type": "uint256"}
                    ],
                    "internalType": "struct SupplyChain.Transaction",
                    "name": "",
                    "type": "tuple"
                }],
                "stateMutability": "view",
                "type": "function"
            }
        ]
        
        self.contract = self.w3.eth.contract(
            address=self.contract_address, 
            abi=self.contract_abi
        )

    def get_transaction_by_offchain_hash(self, hash_data: str) -> Dict[str, Any]:
        try:
            result = self.contract.functions.getTransactionByHash(hash_data).call()
            return {
                'creator_id': result[0],
                'brought_ids': result[1],
                'hash': result[2],
                'timestamp': result[3]
            }
        except Exception as e:
            raise Exception(f"Error getting transaction by hash: {str(e)}")

    def get_transaction_by_tx_hash(self, tx_hash: str) -> Optional[Dict[str, Any]]:
        try:
            if tx_hash.startswith('0x'):
                tx_hash = tx_hash[2:]
            
            tx_hash_bytes = bytes.fromhex(tx_hash)
            tx_receipt = self.w3.eth.get_transaction_receipt(tx_hash_bytes)
            tx_detail = self.w3.eth.get_transaction(tx_hash_bytes)
            
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