import os
from web3 import Web3, EthereumTesterProvider
import solcx

def setup_blockchain():
    """
    Initializes a local, in-memory blockchain using eth-tester.
    Compiles the AlertStorage.sol contract and deploys it!
    """
    print("[blockchain] Starting in-memory blockchain setup...")
    
    # 1. Connect to our fake local blockchain (eth-tester)
    w3 = Web3(EthereumTesterProvider())
    if not w3.is_connected():
        print("[blockchain] Failed to connect to local test chain.")
        return None, None, None

    # The test chain gives us a few fake accounts loaded with fake money.
    # We will use the first account to "deploy" our contract.
    owner_account = w3.eth.accounts[0]
    print(f"[blockchain] Connected! Using account: {owner_account}")

    # 2. Compile the Solidity Smart Contract
    # Solcx needs a specific version of the Solidity compiler installed in Python.
    # We install exactly version 0.8.0 as requested in our .sol file.
    try:
        solcx.install_solc('0.8.0')
    except Exception as e:
        print(f"[blockchain] Solc version setup error (ignoring if already installed): {e}")

    contract_path = os.path.join(os.path.dirname(__file__), "contracts", "AlertStorage.sol")
    print(f"[blockchain] Compiling contract at: {contract_path}")
    
    with open(contract_path, 'r') as file:
        contract_source = file.read()

    # Compile the source code using solcx
    compiled_sol = solcx.compile_source(
        contract_source,
        output_values=['abi', 'bin'],
        solc_version='0.8.0'
    )

    # Our contract is named "AlertStorage" in the source code.
    contract_id, contract_interface = compiled_sol.popitem()
    bytecode = contract_interface['bin']
    abi = contract_interface['abi']

    print("[blockchain] Contract compiled successfully!")

    # 3. Deploy the Smart Contract to the blockchain
    # This creates the actual "table" on the local network.
    AlertStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
    
    # Build a transaction to deploy the contract
    tx_hash = AlertStorage.constructor().transact({'from': owner_account, 'gas': 3000000})
    
    # Wait for the network to agree the contract has been created (mined)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    contract_address = tx_receipt.contractAddress

    print(f"[blockchain] Contract DEPLOYED at address: {contract_address}")

    # Return the connected web3 instance, the active account, and the deploy contract wrapper
    deployed_contract = w3.eth.contract(address=contract_address, abi=abi)
    
    return w3, owner_account, deployed_contract
