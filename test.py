import traceback

try:
    from blockchain_utils import setup_blockchain
    setup_blockchain()
except Exception as e:
    with open("err.txt", "w") as f:
        traceback.print_exc(file=f)
    print("Error saved to err.txt")
