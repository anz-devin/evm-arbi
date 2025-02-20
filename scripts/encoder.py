import os
from web3 import Web3
from eth_account import Account
from uniswap_universal_router_decoder import FunctionRecipient, RouterCodec
from dotenv import load_dotenv

load_dotenv()
RPC_BSC = os.getenv("RPC_BSC")
w3 = Web3(Web3.HTTPProvider(RPC_BSC))
acc = Account.from_key(os.getenv("PRIVATE_KEY"))
print("Current account: ", acc.address)

USER = "0x1b47a6F76a21fDee8BeCA56040A698f87aBc1511"
ROUTER = "0x1A0A18AC4BECDDbd6389559687d1A73d8927E416"
PERMIT2 = "0x31c2F6fcFf4F8759b3Bd5Bf0e1084A055615c768"
tokens = {
    "BNBXBT": "0xA18BBdCd86e4178d10eCd9316667cfE4C4AA8717",
    "USDT": "0x55d398326f99059fF775485246999027B3197955",
    "WBNB": "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",
}
DEADLINE = 1800000000

codec = RouterCodec(w3, RPC_BSC)
amount, expiration, nonce = codec.fetch_permit2_allowance(
    USER, tokens['USDT'], ROUTER, PERMIT2,
)

data, signable_message = codec.create_permit2_signable_message(
    tokens['BNBXBT'],
    int(10e18), 
    DEADLINE,
    nonce,
    ROUTER,
    DEADLINE,
    56,
    PERMIT2,
)
signed_message = acc.sign_message(signable_message)

encoded_data = codec.encode.chain() \
    .permit2_permit(
        data, signed_message,
    ) \
    .v3_swap_exact_in(
        FunctionRecipient.SENDER,
        int(10e18),
        0,
        [
            tokens['BNBXBT'],
            2500,
            tokens['WBNB'],
            10000,
            tokens['BNBXBT'],
        ],
    ) \
    .build(DEADLINE)

# Need to approve to `PERMIT2` first
print("Encoded data: ", encoded_data)
