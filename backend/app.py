# backend/app.py
from flask import Flask, jsonify, request
import requests 

# Flask 기반 API 서버 컨테이너 구성
app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "message": "Hublet API is alive"}), 200

# Solana 지갑 잔액 조회 API
# 사용자가 POST로 지갑 주소(address)를 보내면,
# Solana 메인넷 RPC를 통해 해당 지갑의 SOL 잔액을 조회하여 응답합니다.

@app.route("/wallet/balance", methods=["POST"])
def wallet_balance():
    # 요청에서 JSON 데이터 파싱
    data = request.get_json()
    address = data.get("address")

    # 지갑 주소가 없을 경우 에러 반환
    if not address:
        return jsonify({"error": "Missing wallet address"}), 400

    # Solana RPC에 보낼 페이로드 구성
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBalance",
        "params": [address]
    }

    try:
        # Solana 메인넷에 HTTP POST 요청
        res = requests.post("https://api.mainnet-beta.solana.com", json=payload)
        res_json = res.json()

        # 응답에서 lamports 값 추출 → SOL 단위로 변환 (1 SOL = 10^9 lamports)
        lamports = res_json["result"]["value"]
        sol = lamports / 1e9

        # 주소와 잔액을 JSON 형태로 반환
        return jsonify({"address": address, "balance": sol}), 200

    except Exception as e:
        # 오류 발생 시 에러 메시지 반환
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # 반드시 host="0.0.0.0"