import requests
import json
import time

def check_blockchain():
    url = "http://127.0.0.1:5000/blockchain-alerts"
    try:
        print("🔍 Connecting to Blockchain Node (via App Server API)...")
        time.sleep(1)
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            if not data:
                print("\n[BLOCKCHAIN LEDGER]")
                print("The blockchain is currently empty. No alerts have been minted yet.")
                return

            print("\n" + "="*50)
            print(" 🔗 DECENTRALIZED LEDGER (SECURE BLOCKCHAIN DATA) 🔗")
            print("="*50)
            
            for block in data:
                print(f"\n[ BLOCK #{block['block_id']} ]")
                print(f"  ├─ Security   : {block['security']}")
                print(f"  ├─ Timestamp  : {block['timestamp']}")
                print(f"  ├─ Status     : {block['status']}")
                print(f"  └─ Image Link : /{block['image_path']}")
            print("\n" + "="*50)
            
        else:
            print(f"Error checking blockchain: Server returned code {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect! Is your `python app.py` server running in the background?")
        
if __name__ == "__main__":
    check_blockchain()
