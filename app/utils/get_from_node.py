from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from typing import Dict, Any, Optional

class BlockchainQuery:
    def __init__(self, node_url: str, contract_address: str):
        self.w3 = Web3(Web3.HTTPProvider(node_url))
        # Add PoA middleware
        self.w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
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

    def get_transaction_details(self, tx_hash: str) -> Dict[str, Any]:
        try:
            tx = self.w3.eth.get_transaction(tx_hash)
            return {
                'from_address': tx['from'],
                'to_address': tx['to'],
                'block_hash': tx['blockHash'].hex(),
                'block_number': tx['blockNumber'],
                'transaction_hash': tx_hash
            }
        except Exception as e:
            raise Exception(f"Error getting transaction details: {str(e)}")

    def get_block_details(self, block_hash: str) -> Dict[str, Any]:
        try:
            block = self.w3.eth.get_block(block_hash)
            return {
                'block_hash': block_hash,
                'timestamp': block['timestamp'],
                'miner': block['miner'],
                'number': block['number']
            }
        except Exception as e:
            raise Exception(f"Error getting block details: {str(e)}")

    def get_transaction_by_offchain_hash(self, hash_data: str, tx_hash: Optional[str] = None) -> Dict[str, Any]:
        try:
            result = self.contract.functions.getTransactionByHash(hash_data).call()
            response = {
                'creator_id': result[0],
                'brought_ids': result[1],
                'hash': result[2],
                'timestamp': result[3],
            }
            
            if tx_hash:
                tx_details = self.get_transaction_details(tx_hash)
                block_details = self.get_block_details(tx_details['block_hash'])
                
                response.update({
                    'transaction_creator': tx_details['from_address'],
                    'block_creator': block_details['miner'],
                    'block_number': tx_details['block_number'],
                    'block_hash': tx_details['block_hash'],
                    'transaction_hash': tx_hash
                })
                
            return response
            
        except Exception as e:
            raise Exception(f"Error getting transaction by hash: {str(e)}")