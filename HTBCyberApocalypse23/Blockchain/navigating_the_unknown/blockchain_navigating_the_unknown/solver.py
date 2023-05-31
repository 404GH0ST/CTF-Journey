from web3 import Web3

w3 = Web3(Web3.HTTPProvider('http://104.248.169.175:31137'))

latest = w3.eth.get_block('latest')
print(latest)

# Initialize the address calling the functions/signing transactions
caller = "0x76031BE10862fe0C5B06EAe7e734d51577dF0691" # Address
private_key = "0xcbfe6f40d855b6927a78c95e5b79c5879b1c883d31a26a98a6441fc0db5001a2"  # To sign the transaction
contract_address = "0xB65e50A36eaB45c181e67EDA36BaC49Ab08719b8" # Target Contract

# Initialize address nonce
nonce = w3.eth.get_transaction_count(caller)

# Initialize contract ABI and address
abi = [{
  "inputs": [],
  "stateMutability": "nonpayable",
  "type": "constructor"
}, {
  "inputs": [],
  "name":
  "TARGET",
  "outputs": [{
    "internalType": "contract Unknown",
    "name": "",
    "type": "address"
  }],
  "stateMutability":
  "view",
  "type":
  "function"
}, {
  "inputs": [],
  "name": "isSolved",
  "outputs": [{
    "internalType": "bool",
    "name": "",
    "type": "bool"
  }],
  "stateMutability": "view",
  "type": "function"
}, {
  "inputs": [{
    "internalType": "uint256",
    "name": "version",
    "type": "uint256"
  }],
  "name":
  "updateSensors",
  "outputs": [],
  "stateMutability":
  "nonpayable",
  "type":
  "function"
}, {
  "inputs": [],
  "name": "updated",
  "outputs": [{
    "internalType": "bool",
    "name": "",
    "type": "bool"
  }],
  "stateMutability": "view",
  "type": "function"
}]

# Create smart contract instance
contract = w3.eth.contract(address=contract_address, abi=abi)

# initialize the chain id, we need it to build the transaction for replay protection
Chain_id = w3.eth.chain_id

# Call your function
call_function = contract.functions.updateSensors(10).build_transaction({
  "chainId":
  Chain_id,
  "from":
  caller,
  "nonce":
  nonce
})

# Sign transaction
signed_tx = w3.eth.account.sign_transaction(call_function,
                                            private_key=private_key)

# Send transaction
send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

# Wait for transaction receipt
tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)
print(tx_receipt)  # Optional