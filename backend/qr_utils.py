import qrcode
import os
import json
import secrets

TOKEN_STORE_FILE = "backend/token_map.json"

def save_token_mapping(token, report_id):
    os.makedirs(os.path.dirname(TOKEN_STORE_FILE), exist_ok=True)

    data = {}
    if os.path.exists(TOKEN_STORE_FILE):
        with open(TOKEN_STORE_FILE, "r") as f:
            data = json.load(f)

    data[token] = report_id

    with open(TOKEN_STORE_FILE, "w") as f:
        json.dump(data, f)

def get_report_id_from_token(token):
    if not os.path.exists(TOKEN_STORE_FILE):
        return None
    with open(TOKEN_STORE_FILE, "r") as f:
        data = json.load(f)
    return data.get(token)

def generate_qr(report_id, hospital, issue_date, qr_dir):
    os.makedirs(qr_dir, exist_ok=True)

    # Generate secure random token
    token = secrets.token_hex(8)

    # Save mapping token -> report_id
    save_token_mapping(token, report_id)

    # QR contains only verification URL
    verify_url = f"http://127.0.0.1:5000/verify?token={token}"

    qr = qrcode.make(verify_url)
    qr_path = os.path.join(qr_dir, f"{report_id}.png")
    qr.save(qr_path)

    return qr_path
