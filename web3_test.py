from web3 import Web3
from decimal import Decimal, getcontext
import time

# 設▒~Z Decimal ▒~Z~D精度
getcontext().prec = 40

INFURA_URL = "https://mainnet.infura.io/v3/4bb56e71ab134308ae0482a142a4205f"
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

# ETH/USDC 0.3% pool address
POOL_ADDRESS = Web3.to_checksum_address("0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8")

# slot0 ABI
SLOT0_ABI = [
    {
        "inputs": [],
        "name": "slot0",
        "outputs": [
            {"internalType": "uint160", "name": "sqrtPriceX96", "type": "uint160"},
            {"internalType": "int24", "name": "tick", "type": "int24"},
            {"internalType": "uint16", "name": "observationIndex", "type": "uint16"},
            {"internalType": "uint16", "name": "observationCardinality", "type": "uint16"},
            {"internalType": "uint16", "name": "observationCardinalityNext", "type": "uint16"},
            {"internalType": "uint8", "name": "feeProtocol", "type": "uint8"},
            {"internalType": "bool", "name": "unlocked", "type": "bool"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

pool_contract = w3.eth.contract(address=POOL_ADDRESS, abi=SLOT0_ABI)

def get_eth_usdc_price():
    slot0 = pool_contract.functions.slot0().call()
    sqrt_price_x96 = slot0[0]

    print(f"[Debug] sqrtPriceX96: {sqrt_price_x96}")

    sqrt_price = Decimal(sqrt_price_x96) / Decimal(2 ** 96)
    print(f"[Debug] sqrt_price = sqrtPriceX96 / 2^96 = {sqrt_price}")

    price = sqrt_price ** 2
    print(f"[Debug] price = sqrt_price^2 = {price}")

    # ETH/USDC: token0 = USDC (6 decimals), token1 = ETH (18 decimals)
    adjusted_price = price * Decimal("1e-12")
    print(f"[Debug] adjusted_price = price * 1e-12 = {adjusted_price}")
    eth_usdc_price = Decimal("1") / adjusted_price
    print(f"▒~\~E 1 ETH ▒~I~H {eth_usdc_price:.2f} USDC")
    return eth_usdc_price

while True:
    try:
        price = get_eth_usdc_price()
        print(f"\n▒~\~E ETH/USDC 實▒~Z~[▒~C▒▒| ▒▒~Z▒~D {price:.2f} USDC\n")
    except Exception as e:
        print("▒~]~L ▒~Y▒▒~T~_▒~L▒誤▒~Z", e)
    time.sleep(5)
