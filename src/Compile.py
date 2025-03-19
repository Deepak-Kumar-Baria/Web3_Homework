from solcx import compile_standard
import json

SOLIDITY_PRAGMA = "0.8.13"

def Compile_Solidity(contract: str) -> str:

    with open(contract,"r") as file:
        contract_file = file.read()

    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {contract: {"content": contract_file}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi",  "evm.bytecode"]
                    }
                }
            },

        },
        solc_version = SOLIDITY_PRAGMA
    )

    return compiled_sol

if __name__ == "__main__":
    compiled_sol = Compile_Solidity("./newContract.sol")
    with open('./Compiled/newContract.json','w') as file:
        json.dump(compiled_sol, file)