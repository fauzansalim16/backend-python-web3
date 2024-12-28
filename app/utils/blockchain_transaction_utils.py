from web3 import Web3
import json
from datetime import datetime

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# Contract ABI and address
CONTRACT_ADDRESS = '0x2C2B9C9a4a25e24B174f26114e8926a9f2128FE4' 
CONTRACT_ABI = [
    {
        "inputs": [
            {"internalType": "uint256", "name": "_creatorID", "type": "uint256"},
            {"internalType": "uint256[]", "name": "_broughtIDs", "type": "uint256[]"},
            {"internalType": "string", "name": "_hash", "type": "string"},
            {"internalType": "uint256", "name": "_timestamp", "type": "uint256"}
        ],
        "name": "storeTransaction",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# Initialize the contract
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

def store_transaction(creator_id, brought_ids, hash_data, private_key):
    """
    Store a new transaction in the supply chain contract
    
    Args:
        creator_id (int): ID of the transaction creator
        brought_ids (list): List of vehicle IDs
        hash_data (str): Off-chain data hash
        private_key (str): Private key of the sending account
    """
    # Get the account from private key
    account = w3.eth.account.from_key(private_key)
    
    # Current timestamp in seconds
    timestamp = int(datetime.now().timestamp())
    
    # Build the transaction
    transaction = contract.functions.storeTransaction(
        creator_id,
        brought_ids,
        hash_data,
        timestamp
    ).build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 2000000,  # Adjust gas limit as needed
        'gasPrice': w3.eth.gas_price,
        'chainId': w3.eth.chain_id
    })
    
    # Sign the transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
    
    # Send the transaction
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    
    # Wait for transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    return tx_receipt