"""Tokenized stock vs the real share. $0.05 in USDC on Base.  usage: python tokengap.py TSLA"""
import json, sys
from _pay import paid_get

ticker = sys.argv[1] if len(sys.argv) > 1 else "TSLA"
status, data = paid_get("https://gap.lonestaroracle.xyz/gap", {"ticker": ticker})
print(status)
print(json.dumps(data, indent=2))
