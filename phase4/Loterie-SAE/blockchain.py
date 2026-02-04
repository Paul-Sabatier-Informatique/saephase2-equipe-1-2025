import sys
import os
from web3 import Web3
from solcx import compile_source, set_solc_version

# Solidity
set_solc_version("0.8.0")

# Connexion Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
w3.eth.default_account = w3.eth.accounts[0]

# Chemin du dossier du script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Lecture du contrat
with open(os.path.join(BASE_DIR, "loterie.sol"), "r") as f:
    source_code = f.read()

compiled_sol = compile_source(source_code, output_values=["abi", "bin"])
_, contract_interface = compiled_sol.popitem()

abi = contract_interface["abi"]
bytecode = contract_interface["bin"]

# ---------------- ACTIONS ----------------

def deploy():
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = contract.constructor(w3.to_wei(1, "ether")).transact()
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(receipt.contractAddress)

def participer(adresse):
    contract = w3.eth.contract(address=adresse, abi=abi)
    tx = contract.functions.participer().transact({
        "value": w3.to_wei(1, "ether")
    })
    w3.eth.wait_for_transaction_receipt(tx)
    print("Participation OK")

# ---------------- MAIN ----------------

if len(sys.argv) < 2:
    print("Aucune action fournie")
    sys.exit(1)

action = sys.argv[1]

if action == "deploy":
    deploy()

elif action == "participer":
    if len(sys.argv) < 3:
        print("Adresse du contrat manquante")
    else:
        participer(sys.argv[2])
