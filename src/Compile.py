from solcx import compile_standard, install_solc
import json

# Install Solidity compiler
install_solc("0.8.13")

# Load contract
with open("newContract.sol", "r") as file:
    contract_source = file.read()

# Compile contract
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"newContract.sol": {"content": contract_source}},
        "settings": {"outputSelection": {"*": {"*": ["abi", "evm.bytecode"]}}},
    },
    solc_version="0.8.13",
)

# Save compiled contract
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

print("✅ Contract compiled successfully!")
