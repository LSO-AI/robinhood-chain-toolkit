"""Pay in USDG on Robinhood Chain (eip155:4663) for any LSO service whose 402 lists Robinhood Chain.
usage: python pay_usdg_robinhood.py "https://equity.lonestaroracle.xyz/equity?ticker=HOOD"
Needs USDG (0x5fc5360D0400a0Fd4f2af552ADD042D716F1d168) on Robinhood Chain in the PRIVATE_KEY wallet."""
import json, sys
from _pay import paid_get, ROBINHOOD_CHAIN

status, data = paid_get(sys.argv[1], network=ROBINHOOD_CHAIN)
print(status)
print(json.dumps(data, indent=2)[:3000])
