from web3 import Web3
from solcx import compile_source, install_solc
import json

install_solc("0.8.0")

# Connexion à Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

account = w3.eth.accounts[0]
w3.eth.default_account = account

# Compilation du contrat
with open("loterie.sol", "r") as file:
    source_code = file.read()

compiled_sol = compile_source(
    source_code,
    output_values=["abi", "bin"]
)

contract_id, contract_interface = compiled_sol.popitem()
abi = contract_interface["abi"]
bytecode = contract_interface["bin"]

def deploy_loterie():
    mise = w3.to_wei(1, "ether")
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)

    tx_hash = contract.constructor(mise).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print("Loterie déployée à l'adresse :", tx_receipt.contractAddress)

def afficher_solde(adresse):
    contract = w3.eth.contract(address=adresse, abi=abi)
    solde = contract.functions.getBalance().call()
    print("Solde :", w3.from_wei(solde, "ether"), "ETH")

def participer(adresse):
    contract = w3.eth.contract(address=adresse, abi=abi)
    tx = contract.functions.participer().transact({
        "value": w3.to_wei(1, "ether")
    })
    w3.eth.wait_for_transaction_receipt(tx)
    print("Participation réussie")

def choisir_gagnant(adresse):
    contract = w3.eth.contract(address=adresse, abi=abi)
    tx = contract.functions.choisirGagnant().transact()
    w3.eth.wait_for_transaction_receipt(tx)
    print("Gagnant sélectionné")

while True:
    print("\n--- MENU LOTERIE ---")
    print("1. Lancer une loterie")
    print("2. Afficher le solde")
    print("3. Participer")
    print("4. Sélectionner le vainqueur")
    print("5. Quitter")

    choix = input("Votre choix : ")

    if choix == "1":
        deploy_loterie()

    elif choix == "2":
        addr = input("Adresse du contrat : ")
        afficher_solde(addr)

    elif choix == "3":
        addr = input("Adresse du contrat : ")
        participer(addr)

    elif choix == "4":
        addr = input("Adresse du contrat : ")
        choisir_gagnant(addr)

    elif choix == "5":
        break
