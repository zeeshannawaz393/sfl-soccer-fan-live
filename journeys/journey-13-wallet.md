# Journey 13 — Wallet, Convert, Transfer & Withdraw

Controls every wallet balance and money-adjacent action. Preserves three separate balances and prevents Transferred Gold from recirculating. Canonical: WA-01 Wallet Home · WA-02 Convert · WA-03 Transfer · WA-04 Withdraw · WA-05 History. KYC becomes mandatory inside Withdrawal.

## Three buckets

| Bucket | Spend | Convert | Transfer | Withdraw |
|---|---|---|---|---|
| **Coins** (bought 100=$1) | Yes | Yes | No direct Fan transfer | No |
| **Gold / Earned** (rewards, converted) | via flows | Yes | Yes (level-limited) | Yes |
| **Transferred Gold** (received) | No | No | No | Yes |

Transferred Gold can only be **held or withdrawn** — never re-sent or converted. This stops the same balance circulating between accounts.

## Conversion (retuned for 100 Coins = $1)

The old `13 Coins → 10 Gold` was calibrated when **10 Coins = $1**. Coins are now **100 = $1** (store packs 10×, same USD). Gold withdraw is unchanged: **13 Gold = $1**.

To keep the **same USD round-trip** ($1 of coins still yields the same gold / withdraw value), only the coin side of convert is 10×:

- **Coins → Gold:** `130 Coins → 10 Gold` (`Gold = ⌊Coins × 10/130⌋`). Platform share `30/130 = 23.08%`.
- **Gold → Coins:** `13 Gold → 100 Coins` (`Coins = ⌊Gold × 100/13⌋`) — same USD as the old `13 Gold → 10 Coins`.
- Example: 130 Coins ($1.30) → 10 Gold; converting 10 Gold back → 76 Coins. **Recommend inputs in multiples of 130.**
- **Must disclose: converting back does NOT restore the original balance.**

Do not 10× Gold amounts or gameplay coin costs. Withdraw stays `USD = Gold / 13` (130 Gold ≈ $10).

## Withdrawal value

`130 Gold ≈ $10` → `USD = Gold / 13`. Gross `= Gold/13`; Net `= Gross − fee` (fee undefined). Min withdrawal 130 Gold. Withdrawable = Earned Gold + Transferred Gold.

## Screens

WA-00 Access Gate · WA-01 Wallet Home (3 bucket cards + rules + KYC status + level/limit) · WA-01A Bucket Rules · WA-02 Convert Coins→Gold · WA-02A Gold→Coins · WA-02B Confirm (commission + round-trip warning) · WA-02C Processing (atomic) · WA-02D Success · WA-02E Error · WA-03 Recipient by SFL User ID · WA-03A Transfer Amount (level limit; Transferred Gold shown unavailable) · WA-03B Confirm (recipient gets **Transferred Gold**) · WA-03C Processing (atomic) · WA-03D Success · WA-03E Over-Level-Limit · WA-03F Transferred-Gold Block · **KYC-01–06** (intro, ID document, selfie/liveness, pending, approved, rejected) · WA-04 Eligibility · WA-04A Amount + USD + method · WA-04B Select Gold Source (Earned / Transferred / combined) · WA-04C Confirm (gross/fee/net) · WA-04D Processing · WA-04E Success · WA-04F Failed (state whether Gold restored) · WA-05 History (all buckets + filters) · WA-05A Detail (rate, share, buckets, refs).

## Ledger invariants

Server-authoritative; idempotency key per op; atomic linked debit/credit; no negative balance; failed conversions restore source; Transferred Gold never becomes another user's Transferred Gold via a second transfer; client balances never authoritative; pending withdrawals can't be double-spent; corrections are auditable reversals, never deletions.

## Open decisions

Non-multiple rounding · min/max conversion · converted-Gold transfer-eligible? · level limit per txn/day/week/month · L5–19 limits · transfer fee · transfer reversible? · withdrawal methods/fees/time · 130 min before or after fees · local-currency FX + provider · withdrawal source choice · KYC provider/countries/documents/expiry · daily/monthly withdrawal limits · step-up auth · fraud limits · tax/reporting · Host gift settlement balance · does converted Gold count as "earned Gold" (for progression?) · dispute rules · manager/club wallet structure.

---
---

# Review — issues (journey unchanged)

## A — This is the money-transmission / e-money product; it's the app's foundational compliance surface

Real money in (Coins bought with USD) → convert to Gold → **transfer Gold to other users** → **withdraw Gold to cash**. That is the complete regulated flow: buying stored value, peer-to-peer transfer, and cash-out. In virtually every market it requires an **e-money / money-transmitter licence (or a licensed payments partner)**, **KYC/AML** (which this journey correctly builds in — KYC gates withdrawal), **transaction monitoring**, **geofencing**, and **tax/reporting**. This is the single biggest "cross the bridge later" item in SFL, alongside the J5/J6 gambling surfaces — and unlike those, it's not optional flavour; the withdraw button *is* the regulated act. Design-agnostic (the screens are identical regardless of how it's licensed), so I've built it as concept — but nothing here should go live without a payments/e-money legal structure in place. The good news: the journey already includes the right AML scaffolding (KYC-gated withdrawal, per-op idempotency, auditable reversals, the anti-recirculation Transferred-Gold bucket).

## B — The conversion is lossy, and the design's job is to be honest about it (done)

The convert rate still charges **23.08%** on Coins→Gold. After the 100 Coins = $1 change, the displayed math is **130 Coins → 10 Gold** (and **13 Gold → 100 Coins** the other way) so $1 in still ≈ $0.54 out via withdraw. The old 13:10 unit pair would have leaked ~10× cash-out. Round trip: 130 Coins → 10 Gold → **76 Coins**. The UI must stay honest: commission on every conversion, **"converting back won't restore your balance"**, multiples of 130.

## C — KYC-gated withdrawal + document privacy — correct AML design (built)

Withdrawal is blocked until KYC is Approved; ID document + selfie/liveness via a compliant provider; documents never shown in public profiles or manager screens. Built the KYC intro/document/selfie/pending/approved/rejected states. The **withdrawal source selector** (Earned vs Transferred Gold) is a good addition — it stops silently draining Earned Gold a Fan meant to transfer later.

## D — Three-bucket integrity is the whole point, and it's consistent

Coins / Earned Gold / **Transferred Gold** are visually distinct and each card states its own rules; Transferred Gold can be **held or withdrawn only** (the anti-money-laundering core — received value can't be passed down a chain); transfers are **level-gated** (J12) and can't source from Transferred Gold. All consistent with the J12 metric map.

## E — Secure, not casino — the visual bar

Exact tabular balances, disclosed math, verified-User-ID transfers, visible KYC status, and a transaction reference on every financial result. Built to feel like a bank, not a slot machine. **Theme:** light.

One open item worth an explicit answer (affects progression): **does converted Gold count as "earned Gold" for Fan Level?** Per J12, Level is driven by *approved-activity* Gold and explicitly **excludes converted Gold** — so converted Gold should be spendable/transferable/withdrawable but **not** feed the progression ledger. Confirm.

No confirmation gate to build. Built light; A is the foundational compliance flag (known), and the one small confirm is whether converted Gold counts toward Level (recommend: no).