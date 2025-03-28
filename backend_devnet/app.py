# backend_devnet/app.py
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "message": "Hublet Devnet API is alive"}), 200

@app.route("/wallet/balance", methods=["POST"])
def wallet_balance():
    data = request.get_json()
    address = data.get("address")
    if not address:
        return jsonify({"error": "Missing wallet address"}), 400

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBalance",
        "params": [address]
    }

    try:
        res = requests.post("https://api.devnet.solana.com", json=payload)
        res_json = res.json()
        lamports = res_json["result"]["value"]
        sol = lamports / 1e9
        return jsonify({"address": address, "balance": sol}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/wallet/nfts", methods=["POST"])
def wallet_nfts():
    data = request.get_json()
    address = data.get("address")
    if not address:
        return jsonify({"error": "Missing wallet address"}), 400

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTokenAccountsByOwner",
        "params": [
            address,
            {"programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"},
            {"encoding": "jsonParsed"}
        ]
    }

    try:
        res = requests.post("https://api.devnet.solana.com", json=payload)
        result = res.json().get("result", {})
        accounts = result.get("value", [])

        nfts = []
        for acc in accounts:
            amount = acc["account"]["data"]["parsed"]["info"]["tokenAmount"]
            if amount["amount"] == "1" and amount["decimals"] == 0:
                nft_info = {
                    "mint": acc["account"]["data"]["parsed"]["info"]["mint"],
                    "owner": acc["account"]["data"]["parsed"]["info"]["owner"]
                }
                nfts.append(nft_info)

        return jsonify({"address": address, "nfts": nfts}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)