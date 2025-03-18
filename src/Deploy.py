from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
PRIVATE_KEY = os.getenv("ANVIL_PRIVATE_KEY")
ACCOUNT = os.getenv("ANVIL_ACCOUNT")
RPC_URL = os.getenv("LOCAL_PROVIDER")
CHAIN_ID = int(os.getenv("CHAIN_ID"))

# Connect to Anvil
w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)

# Load compiled contract
with open("compiled_code.json", "r") as file:
    compiled_sol = json.load(file)

abi = compiled_sol["contracts"]["newContract.sol"]["newContract"]["abi"]
bytecode = compiled_sol["contracts"]["newContract.sol"]["newContract"]["evm"]["bytecode"]["object"]

# Deploy contract
contract = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.get_transaction_count(account.address)

transaction = contract.constructor().build_transaction({
    "from": account.address,
    "gas": 6721975,
    "gasPrice": w3.to_wei("20", "gwei"),
    "nonce": nonce,
    "chainId": CHAIN_ID
})

signed_txn = w3.eth.account.sign_transaction(transaction, PRIVATE_KEY)
txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

contract_address = txn_receipt.contractAddress
print(f"✅ Contract deployed at {contract_address}")

# Save contract address
with open("contract_address.txt", "w") as file:
    file.write(contract_address)
