# Robinhood Chain toolkit (LoneStarOracle)

Pay-per-call data and safety checks for agents and apps on **Robinhood Chain**, sold over [x402](https://x402.org). No signup, no API key: an agent calls the endpoint, gets an HTTP 402 with the price, pays in stablecoins, and gets the data.

Built and operated by [LoneStarOracle](https://lonestaroracle.xyz) (Texas). Full machine-readable catalog of 70+ endpoints: [`lonestaroracle.xyz/openapi.json`](https://lonestaroracle.xyz/openapi.json).

## What's here

| Service | Endpoint | Price | What it answers |
|---|---|---|---|
| **TokenGap** | `GET https://gap.lonestaroracle.xyz/gap?ticker=TSLA` | $0.05 | Is the tokenized stock trading at a premium or discount to the real share? Per venue (Robinhood Chain stock tokens, Solana xStocks), with liquidity, $1k/$10k price impact, best buy/sell venue. Signals `IN_LINE` / `PREMIUM` / `DISCOUNT` / `STALE` / `THIN` |
| **TokenGap** | `GET https://gap.lonestaroracle.xyz/gaps` | $0.10 | Every supported stock token ranked by gap |
| **BaitBuster** | `GET https://baitbuster.lonestaroracle.xyz/check?address=0x...` | $0.10 | Pre-buy rug / honeypot check for a Robinhood Chain, Base or Solana token: contract powers, who can pull the liquidity, copycat names, known rug launchers, bait pools, real cash you could exit with |
| **BaitBuster** | `GET https://baitbuster.lonestaroracle.xyz/record` | free | Published track record of the warnings (graded 24h after each call) |

TokenGap tickers: AAPL BMNR COIN DIS GDX HOOD JPM MCD MSTR NVDA PYPL QQQ SKHY SPY TSLA UBER V. A missing or unknown ticker returns a free `400` with the list, so you never pay for a bad request.

## Paying in USDG on Robinhood Chain

12 LoneStarOracle services also accept **USDG on Robinhood Chain** (`eip155:4663`, USDG `0x5fc5360D0400a0Fd4f2af552ADD042D716F1d168`), settled through the standard x402 v2 flow via the [Primer](https://x402.primer.systems) facilitator: EquityScope, MacroPulse, OptionsFlow, TechAnalysis, AnalystEdge, CapitolFlow, EarningsCalendar, InsiderFlow, PortfolioRisk, RWARisk, SmartMoney, StablePulse. Their 402 response lists the Robinhood Chain option next to Base and Solana; your client picks the network it holds funds on.

TokenGap and BaitBuster currently take USDC on Base or Solana.

## Quick start

```bash
pip install -r requirements.txt

# 1. See what an endpoint costs and which networks it accepts (no wallet, no payment)
python examples/discover.py https://gap.lonestaroracle.xyz/gap?ticker=TSLA

# 2. Pay and call (needs a wallet with USDC on Base)
export PRIVATE_KEY=0x...        # a throwaway wallet with a few dollars, never your main wallet
python examples/tokengap.py TSLA
python examples/baitbuster.py 0xTokenAddress

# 3. Pay in USDG on Robinhood Chain
python examples/pay_usdg_robinhood.py "https://equity.lonestaroracle.xyz/equity?ticker=HOOD"
```

## How x402 works here

1. Call the endpoint with no payment. You get `402 Payment Required` with a `payment-required` header (base64 JSON) listing each accepted network, asset, amount and pay-to address.
2. Your x402 client signs a payment for one of them (gasless for the payer on EVM: an EIP-3009 authorization).
3. Retry with the payment header. The facilitator settles on-chain and you get the data.

Any standard x402 v2 client works (Python `x402`, TypeScript `@x402/fetch`). Legacy v1 clients (`x402-fetch` 1.x) are supported too.

## Notes

- Stock tokens are not offered to US persons. These services provide **data about** them; they don't trade, custody or sell them.
- BaitBuster measures warnings. It does not tell you what to buy, and it can't predict a liquidity pull that hasn't happened yet.
- Status: [status.lonestaroracle.xyz](https://status.lonestaroracle.xyz) · Contact: jay@lonestaroracle.xyz · X: [@LSO_AI](https://x.com/LSO_AI)

MIT licensed.
