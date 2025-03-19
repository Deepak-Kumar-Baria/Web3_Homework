from web3 import Web3
from Deploy import deploy_contract
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Contract file and contract details
contract_file = "./newContract.sol"
contract_name = 'newContract'

# Load environment variables
account = os.getenv("ANVIL_ACCOUNT")
private_key = os.getenv("ANVIL_PRIVATE_KEY")
provider = os.getenv("LOCAL_PROVIDER")
chain_id = 31337

# Connect to the provider (local node, e.g., Ganache)
connection = Web3(Web3.HTTPProvider(provider))

# Deploy the contract
contract_address, abi = deploy_contract(contract_file, contract_name, account, private_key, provider, chain_id)
print(f"Contract deployed at {contract_address}")

# Interact with the deployed contract
simple_storage = connection.eth.contract(address=contract_address, abi=abi)

# Get the nonce for the transaction
nonce = connection.eth.get_transaction_count(account)

# Build the transaction to update the stored value
print("Creating Transactions")
transaction = simple_storage.functions.updateID(5341).build_transaction(
    {
        "chainId": chain_id,
        "gasPrice": connection.eth.gas_price,
        "from": account,
        "nonce": nonce
    }
)

# Sign the transaction
signed_txn = connection.eth.account.sign_transaction(transaction, private_key=private_key)

# Send the transaction
print("Updating stored Value")
tx_hash = connection.eth.send_raw_transaction(signed_txn.raw_transaction)  # Fix here

# Wait for the transaction receipt to confirm that it was mined
tx_receipt = connection.eth.wait_for_transaction_receipt(tx_hash)
print("Updated successfully")

# Call the view function to get the updated value
updated_value = simple_storage.functions.viewMyId().call()
print(f"Updated value is {updated_value}")
