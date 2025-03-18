from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
PRIVATE_KEY = os.getenv("ANVIL_PRIVATE_KEY")
RPC_URL = os.getenv("LOCAL_PROVIDER")

# Connect to Anvil
w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)

# Load contract ABI & Address
with open("compiled_code.json", "r") as file:
    compiled_sol = json.load(file)

with open("contract_address.txt", "r") as file:
    contract_address = file.read().strip()

abi = compiled_sol["contracts"]["newContract.sol"]["newContract"]["abi"]
contract = w3.eth.contract(address=contract_address, abi=abi)

# View initial StudentId
student_id = contract.functions.viewMyId().call()
print(f"Initial StudentID: {student_id}")

# Update StudentId to 5341
nonce = w3.eth.get_transaction_count(account.address)
update_txn = contract.functions.updateID(5341).build_transaction({
    "from": account.address,
    "gas": 2000000,
    "gasPrice": w3.to_wei("20", "gwei"),
    "nonce": nonce,
    "chainId": 31337
})

signed_update_txn = w3.eth.account.sign_transaction(update_txn, PRIVATE_KEY)
update_txn_hash = w3.eth.send_raw_transaction(signed_update_txn.raw_transaction)
w3.eth.wait_for_transaction_receipt(update_txn_hash)

# View updated StudentId
updated_value = contract.functions.viewMyId().call()
print(f"Updated value is {updated_value}")
