"""Show what an x402 endpoint costs and which networks it accepts. Free: no wallet, no payment."""
import base64, json, sys
import httpx

USDC_DECIMALS = 6

url = sys.argv[1] if len(sys.argv) > 1 else "https://gap.lonestaroracle.xyz/gap?ticker=TSLA"
r = httpx.get(url, timeout=30)
if r.status_code != 402:
    print(r.status_code, r.text[:500])
    sys.exit()
header = r.headers.get("payment-required")
if header:
    req = json.loads(base64.b64decode(header))
else:   # legacy v1 servers put the requirements in the body
    req = r.json()
print("x402 version", req.get("x402Version"))
for a in req["accepts"]:
    amount = a.get("amount") or a.get("maxAmountRequired")
    print(f"  {a['network']:45} {int(amount) / 10**USDC_DECIMALS:>7.3f}  asset {a['asset']}  pay to {a['payTo']}")
