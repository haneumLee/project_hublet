# frontend/monitoring/dashboard.py
import streamlit as st
import requests
import datetime

st.set_page_config(page_title="Hublet Dashboard", layout="centered")
st.title("Hublet - Solana Dashboard")

# ------------------------------
# 노드 상태 체크
# ------------------------------
st.header("Solana 노드 상태 확인")

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
        st.success("노드 연결 성공")
        st.write("Epoch:", data['result']['epoch'])
        st.write("Slot:", data['result']['absoluteSlot'])
        st.write("업데이트:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    else:
        st.error("노드 연결 실패")
except Exception as e:
    st.error(f"에러 발생: {e}")

# ------------------------------
# 지갑 잔액 조회
# ------------------------------
st.header("Solana 지갑 잔액 조회")

wallet_address = st.text_input("지갑 주소를 입력하세요:")

if st.button("잔액 확인"):
    if wallet_address:
        try:
            response = requests.post(
                #"http://backend:5000/wallet/balance",
                "http://backend-devnet:5001/wallet/balance",
                json={"address": wallet_address}
            )
            if response.status_code == 200:
                data = response.json()
                st.success(f"잔액: {data['balance']} SOL")
            else:
                st.error("지갑 조회 실패")
        except Exception as e:
            st.error(f"에러 발생: {e}")
    else:
        st.warning("지갑 주소를 입력해주세요.")

# ------------------------------
# NFT 목록 조회
# ------------------------------
st.header("보유한 NFT 목록")

if wallet_address:
    try:
        nft_response = requests.post(
            #"http://backend:5000/wallet/nfts",
            "http://backend-devnet:5001/wallet/nfts",
            json={"address": wallet_address}
        )

        if nft_response.status_code == 200:
            nft_data = nft_response.json()
            nft_list = nft_data.get("nfts", [])

            if not nft_list:
                st.info("보유한 NFT가 없습니다.")
            else:
                for nft in nft_list:
                    token_address = nft.get("tokenAddress", "Unknown")
                    st.write(f"• NFT Token: `{token_address}`")
        else:
            st.error("NFT 정보를 가져오지 못했습니다.")

    except Exception as e:
        st.error(f"에러 발생: {e}")
else:
    st.warning("지갑 주소를 입력하면 NFT 목록을 조회할 수 있습니다.")

# ------------------------------
# NFT 조회 버튼을 따로 둠
# ------------------------------
if st.button("NFT 조회"):
    if not wallet_address:
        st.warning("지갑 주소를 입력하면 NFT 목록을 조회할 수 있습니다.")
    else:
        try:
            nft_response = requests.post(
                #"http://backend:5000/wallet/nfts",
                "http://backend-devnet:5001/wallet/nfts",
                json={"address": wallet_address}
            )

            if nft_response.status_code == 200:
                nft_data = nft_response.json()
                nft_list = nft_data.get("nfts", [])

                if not nft_list:
                    st.info("보유한 NFT가 없습니다.")
                else:
                    for nft in nft_list:
                        token_address = nft.get("tokenAddress", "Unknown")
                        st.write(f"• NFT Token: `{token_address}`")
            else:
                st.error("NFT 정보를 가져오지 못했습니다.")
        except Exception as e:
            st.error(f"에러 발생: {e}")
