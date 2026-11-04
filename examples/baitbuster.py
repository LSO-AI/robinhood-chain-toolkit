"""Pre-buy rug / honeypot check. $0.10 in USDC on Base.  usage: python baitbuster.py 0xTokenAddress

Checks take ~45-120s. The paid call waits up to `wait` seconds; if it isn't done, it returns a job id and
polling /result/<job_id> is free."""
import json, sys, time
import httpx
from _pay import paid_get

addr = sys.argv[1]
status, data = paid_get("https://baitbuster.lonestaroracle.xyz/check", {"address": addr, "wait": 25})
while data.get("status") == "running":
    time.sleep(data.get("poll_after_s", 15))
    data = httpx.get(data["result_url"], timeout=30).json()
print(data.get("verdict"), data.get("symbol"), data.get("chain"))
print(json.dumps(data, indent=2))
