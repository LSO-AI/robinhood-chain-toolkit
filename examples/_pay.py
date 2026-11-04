"""Shared helper: call an x402 endpoint and pay with an EVM wallet on one network."""
import asyncio, os
from eth_account import Account
from x402.client import x402Client
from x402.http.clients.httpx import x402HttpxClient
from x402.mechanisms.evm.exact.register import register_exact_evm_client
from x402.mechanisms.evm.signers import EthAccountSigner

BASE = "eip155:8453"
ROBINHOOD_CHAIN = "eip155:4663"


def paid_get(url, params=None, network=BASE):
    key = os.environ.get("PRIVATE_KEY")
    if not key:
        raise SystemExit("set PRIVATE_KEY (a throwaway wallet holding a few dollars of USDC/USDG)")

    async def _go():
        signer = EthAccountSigner(Account.from_key(key))
        # Register only the network you hold funds on, so the client never signs a payment it can't cover
        client = register_exact_evm_client(x402Client(), signer, networks=network)
        async with x402HttpxClient(client) as http:
            r = await http.get(url, params=params or {}, timeout=60)
            return r.status_code, r.json()

    return asyncio.run(_go())
