from solcx import compile_standard, install_solc
import pprint, json, os
from web3 import Web3
# import os
# os.chdir(os.path.dirname(__file__))
# print(os.getcwd())
# import pathlib
# print(pathlib.Path.cwd())

pp = pprint.PrettyPrinter(indent=4)

# print("solcx.get_installable_solc_versions() ", solcx.get_installable_solc_versions())
fname = "Z:\\workspace3\\PySolidityTutorial\\src\\web3_py_simple_storage\\SimpleStorage.sol"

# simple_storage_file = open(fname, 'r').read()
with open(fname) as file: simple_storage_file = file.read()
# print(simple_storage_file)

# Compile Our Solidity
# install_solc("0.6.0")
install_solc("0.8.0")

# Solidity source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.0",
)


# pp.pprint(compiled_sol)

with open("compiled_code.json", 'w') as file: json.dump(compiled_sol, file)


#get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

#get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

#connect to Ganache
# GanacheChainID = 1337
# GanacheSvr = "http://127.0.0.1:7545" #ui
# ganachepubkey = "0xcdd72CB697c62b492297FF2b8DF19Aa843172C3e"
#
# # GanacheCLI = "http://127.0.0.1:8545"
# # ganacheCLIpubkey  = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
#
# w3 = Web3(Web3.HTTPProvider(GanacheSvr))
# chain_id = GanacheChainID
# myaddress = ganachepubkey
# myprivkey = os.environ['ganacheprivkey']

RinkebyChainID = 4
Rinkebypubkey: str = "0x4175B7Aa527ba2584CC339A485e8486e49E2814C"
InfuraRinkeby = "https://rinkeby.infura.io/v3/af52ad401335491db49ec4a96f4ca667"
w3 = Web3(Web3.HTTPProvider(InfuraRinkeby))
chain_id = RinkebyChainID
myaddress = Rinkebypubkey
myprivkey = os.environ['Rinkebyprivkey']


SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

nonce = int(w3.eth.getTransactionCount(myaddress))
print("\nnonce / getTransactionCount:",nonce)

#1.Build txn
#2.Sign txn
#3.Send txn
txn = {"chainId":chain_id, "from":myaddress, "nonce":nonce}
transaction = SimpleStorage.constructor().buildTransaction(txn)
# print("\ntransaction:")
# pp.pprint(transaction)

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=myprivkey)
print("Deploying contract...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Contract deployed to {tx_receipt.contractAddress}")

# Working w/ the contract, you always need its address & ABI
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# call() -> Simulate make the call & getting a retval w/ no state change. "Calling is just a simulation."
# transact() -> Actually make a state change on block chain.

print(f"initial value of the store fn:\t: {simple_storage.functions.retrieve().call()}")
print(f'{simple_storage.functions.store(15).call() = }')
print(f"{simple_storage.functions.retrieve().call() = }")

txn = {"chainId":chain_id, "from":myaddress, "nonce":(nonce:=nonce+1)}

print(f"{nonce = }")

store_txn = simple_storage.functions.store(15).buildTransaction(txn)
signed_store_txn = w3.eth.account.sign_transaction(store_txn, private_key=myprivkey)
tx_hash = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
print("Waiting for transaction to finish...")
#good practice to wait for block confirmations
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"{simple_storage.functions.retrieve().call() = }")




print(f"\n\ninitial value of the store fn:\t: {simple_storage.functions.retrieve().call()}")
print(f'{simple_storage.functions.store(99).call() = }')
print(f"{simple_storage.functions.retrieve().call() = }")

