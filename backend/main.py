from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests
from typing import List, Dict, Any
import os
from dotenv import load_dotenv
import logging
import json
from datetime import datetime

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

# Configuration CORS plus permissive pour le développement
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# URLs des APIs
SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com"
COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd"

class WalletRequest(BaseModel):
    wallets: List[str]

def get_sol_price():
    try:
        response = requests.get(COINGECKO_URL)
        if response.status_code == 200:
            data = response.json()
            return data['solana']['usd']
        return None
    except Exception as e:
        logger.error(f"Error fetching SOL price: {str(e)}")
        return None

async def get_wallet_transactions(wallet: str, limit: int = 10) -> List[Dict[str, Any]]:
    try:
        rpc_payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getConfirmedSignaturesForAddress2",
            "params": [wallet, {"limit": limit}]
        }
        response = requests.post(SOLANA_RPC_URL, json=rpc_payload)
        if response.status_code == 200:
            data = response.json()
            if 'result' in data:
                return data['result']
        return []
    except Exception as e:
        logger.error(f"Error fetching transactions: {str(e)}")
        return []

async def get_transaction_details(signature: str) -> Dict[str, Any]:
    try:
        rpc_payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTransaction",
            "params": [signature, {"encoding": "json", "maxSupportedTransactionVersion": 0}]
        }
        response = requests.post(SOLANA_RPC_URL, json=rpc_payload)
        if response.status_code == 200:
            return response.json()
        return {}
    except Exception as e:
        logger.error(f"Error fetching transaction details: {str(e)}")
        return {}

async def get_token_accounts(wallet: str) -> List[Dict[str, Any]]:
    try:
        rpc_payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTokenAccountsByOwner",
            "params": [
                wallet,
                {
                    "programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
                    "encoding": "jsonParsed"
                }
            ]
        }
        logger.info(f"Sending token accounts request for wallet {wallet}")
        response = requests.post(SOLANA_RPC_URL, json=rpc_payload)
        logger.info(f"Token accounts raw response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if 'result' in data and 'value' in data['result']:
                return data['result']['value']
        return []
    except Exception as e:
        logger.error(f"Error fetching token accounts: {str(e)}")
        return []

async def get_stake_accounts(wallet: str) -> List[Dict[str, Any]]:
    try:
        rpc_payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getStakeAccounts",
            "params": [wallet]
        }
        response = requests.post(SOLANA_RPC_URL, json=rpc_payload)
        if response.status_code == 200:
            data = response.json()
            if 'result' in data:
                return data['result']
        return []
    except Exception as e:
        logger.error(f"Error fetching stake accounts: {str(e)}")
        return []

@app.get("/")
async def root():
    return {"message": "Solana Wallet Dashboard API"}

@app.post("/analyze")
async def analyze_wallets(request: Request):
    try:
        # Get current SOL price
        sol_price = get_sol_price()
        logger.info(f"Current SOL price: ${sol_price}")

        # Parse request body
        try:
            data = await request.json()
            logger.info(f"Parsed request data: {data}")
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            return JSONResponse(
                status_code=400,
                content={"detail": f"Invalid JSON: {str(e)}"}
            )

        if not isinstance(data, dict) or 'wallets' not in data:
            return JSONResponse(
                status_code=400,
                content={"detail": "Request must include 'wallets' field"}
            )

        wallet_data = []
        for wallet in data['wallets']:
            if not isinstance(wallet, str):
                continue

            logger.info(f"Analyzing wallet: {wallet}")
            try:
                # Get SOL balance
                rpc_payload = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "getBalance",
                    "params": [wallet]
                }
                
                response = requests.post(SOLANA_RPC_URL, json=rpc_payload)
                balance = 0
                if response.status_code == 200:
                    data = response.json()
                    if 'result' in data and 'value' in data['result']:
                        balance = float(data['result']['value']) / 1e9

                # Get additional wallet information
                transactions = await get_wallet_transactions(wallet)
                token_accounts = await get_token_accounts(wallet)
                stake_accounts = await get_stake_accounts(wallet)

                # Count NFTs (heuristic: token accounts with decimals 0 and uiAmount 1)
                nft_count = 0
                for token_account in token_accounts:
                    if (
                        token_account.get('account', {}).get('data', {}).get('parsed', {}).get('info', {}).get('tokenAmount', {}).get('decimals') == 0 and
                        token_account.get('account', {}).get('data', {}).get('parsed', {}).get('info', {}).get('tokenAmount', {}).get('uiAmount') == 1
                    ):
                        nft_count += 1

                # Calculate total staked amount
                total_staked = sum(
                    float(account.get('account', {}).get('lamports', 0)) / 1e9
                    for account in stake_accounts
                )

                wallet_data.append({
                    "address": wallet,
                    "balance": balance,
                    "usd_value": balance * sol_price if sol_price else None,
                    "total_staked": total_staked,
                    "staked_usd_value": total_staked * sol_price if sol_price else None,
                    "transaction_count": len(transactions),
                    "token_count": len(token_accounts),
                    "nft_count": nft_count,
                    "last_transaction": transactions[0] if transactions else None,
                    "tokens": token_accounts,
                    "stake_accounts": stake_accounts
                })

            except Exception as e:
                logger.error(f"Error processing wallet {wallet}: {str(e)}")
                wallet_data.append({
                    "address": wallet,
                    "error": str(e)
                })

        # Sort by total value (balance + staked)
        wallet_data.sort(
            key=lambda x: (x.get('balance', 0) + x.get('total_staked', 0)) * (sol_price or 0),
            reverse=True
        )

        return wallet_data

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": str(e)}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
