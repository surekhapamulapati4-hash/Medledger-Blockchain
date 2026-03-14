from web3 import Web3
import json
import os
from dotenv import load_dotenv

# =========================================================
# LOAD ENV VARIABLES
# =========================================================

load_dotenv()

INFURA_URL = os.getenv("INFURA_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

if not INFURA_URL or not PRIVATE_KEY or not WALLET_ADDRESS or not CONTRACT_ADDRESS:
    raise Exception("❌ Missing blockchain environment variables")

# =========================================================
# CONNECT TO SEPOLIA BLOCKCHAIN
# =========================================================

w3 = Web3(Web3.HTTPProvider(INFURA_URL))

if not w3.is_connected():
    raise Exception("❌ Failed to connect to Sepolia via Infura")

print("✅ Connected to Sepolia Blockchain")

# =========================================================
# LOAD CONTRACT ABI
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
abi_path = os.path.join(BASE_DIR, "abi.json")

if not os.path.exists(abi_path):
    raise Exception("❌ abi.json file not found")

with open(abi_path, "r") as f:
    abi = json.load(f)

# =========================================================
# CREATE CONTRACT OBJECT
# =========================================================

contract = w3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS),
    abi=abi
)

# =========================================================
# STORE HASH ON BLOCKCHAIN (FIXED FOR RENDER)
# =========================================================
def store_hash(report_id, report_hash):

    try:

        report_id = str(report_id)
        report_hash = str(report_hash)

        wallet = Web3.to_checksum_address(WALLET_ADDRESS)

        nonce = w3.eth.get_transaction_count(wallet)

        transaction = contract.functions.addReport(
            report_id,
            report_hash
        ).build_transaction({
            "chainId": 11155111,
            "from": wallet,
            "nonce": nonce,
            "gas": 300000,
            "gasPrice": w3.to_wei("20", "gwei")
        })

        signed_tx = w3.eth.account.sign_transaction(transaction, PRIVATE_KEY)

        raw_tx = getattr(signed_tx, "rawTransaction", None) or getattr(signed_tx, "raw_transaction")

        tx_hash = w3.eth.send_raw_transaction(raw_tx)

        print("✅ Transaction sent:", w3.to_hex(tx_hash))

        # DO NOT WAIT FOR RECEIPT
        return w3.to_hex(tx_hash)

    except Exception as e:

        print("❌ Blockchain store error:", str(e))
        return None


# =========================================================
# GET HASH FROM BLOCKCHAIN
# =========================================================

def get_hash(report_id):

    try:

        report_id = str(report_id)

        result = contract.functions.getReport(report_id).call()

        blockchain_hash = result[0]

        if not blockchain_hash or blockchain_hash == "":
            return None

        return blockchain_hash

    except Exception as e:

        print("❌ Blockchain fetch error:", str(e))
        return None
