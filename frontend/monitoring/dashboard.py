# frontend/monitoring/dashboard.py
import streamlit as st
import requests
import datetime

st.set_page_config(page_title="Hublet Node Monitor", layout="centered")
st.title("🟢 Hublet - Solana Node Dashboard")

RPC_URL = "https://api.mainnet-beta.solana.com"
payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getEpochInfo"
}

try:
    response = requests.post(RPC_URL, json=payload)
    data = response.json()

    if "result" in data:
        st.success("노드 연결 성공 ✅")
        st.write("⛓ Epoch:", data['result']['epoch'])
        st.write("📈 Slot:", data['result']['absoluteSlot'])
        st.write("🕒 업데이트:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    else:
        st.error("노드 연결 실패")
except Exception as e:
    st.error(f"에러 발생: {e}")