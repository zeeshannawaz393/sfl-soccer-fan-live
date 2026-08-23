# Journey 3 — Buy Coins

## 1. Objective

Let a registered SFL user: purchase 100–100,000 Coins; understand the exact USD value; credit Coins to their own SFL User ID or (optionally) another Fan's; pay via an approved native provider; receive Coins only after server verification; get a receipt and updated balance; continue toward Fan Value activation when eligible. **Guests cannot purchase** — registration/login first.

## 2. Non-negotiable economy rules

**Coin purchase formula:** `100 Coins = $1.00 USD` → `USD Price = Coin Amount ÷ 100`

| Coins | USD |
|---|---|
| 100 | $1 |
| 500 | $5 |
| 1,000 | $10 |
| 5,000 | $50 |
| 10,000 | $100 |
| 20,000 | $200 |
| 50,000 | $500 |
| 100,000 | $1,000 |

All packages have identical per-Coin value → **no "Best Value" label** (only "Popular" is allowed). A real bonus/discount would be required to justify "Best Value".

**Local currency:** USD is canonical. `Local Estimate = USD Price × FX Rate`. Coin quantity never changes with FX. Final charge confirmed by provider.

**Balance:** self → `New = Opening + Purchased`. Other recipient → recipient's balance increases; buyer's balance unchanged.

**Idempotency:** `1 Provider Transaction ID = 1 Coin Credit`. Repeated callbacks never double-credit.

## 3. Visual direction (as specified in this journey)

390×844. Near-black/navy full-screen. Real stadium photography under floodlights, controlled so financial info stays readable. **Metallic gold = Coins/money. Electric lime = selection & primary actions. Coral = payment errors/destructive.** Condensed football-display headings; Manrope body; tabular numerals for all figures. Thin metallic borders, dark glass. No white banking UI, no cartoon coins, no fake finance dashboard. Checkout removes bottom nav; back allowed before payment, never restarts payment after submission; success returns to originating journey.

## 4. Screen inventory

- **J3-01 Guest Registration Gate** — "Create an account to buy Coins"; benefits; Create Account / Sign In / Not now. Stadium-entrance photo, locked gold coin in glass shield, no prices shown. States: normal · registration unavailable · session expired · offline.
- **J3-02 Coin Store** — header (back, "Buy Coins", history icon); balance hero (12,400 Coins, Alex Morgan, User ID 12345); recipient control ("credited to My account · 12345 · Change"); exchange strip "100 Coins = $1.00 USD" + FX note; two-column package grid (coin icon, amount, USD, selected state, optional Popular); sticky CTA "Continue · 5,000 Coins · $50.00". States: default/none selected · loading · catalogue unavailable · offline · region unavailable · provider unavailable · restricted · limit reached · guest gate. **Never create a payment from a cached price without server reconfirm.**
- **J3-03 Select Recipient (bottom sheet)** — tabs My Account / Another User ID; My Account (avatar, name, ID, balance, Use My Account); Another User ID (Recipient User ID field, Find Fan, privacy copy). States: empty · invalid format · searching · found · not found · restricted · network · timeout.
- **J3-04 Recipient Confirmation** — player-card style: avatar, name, User ID, Fan Level, club; 5,000 Coins / $50; warning to confirm correct Fan; Yes / Search Again. No phone/email exposed. Negatives: unavailable · ID changed · suspended · cannot receive · is-own-account (suggest My Account).
- **J3-05 Review Purchase** — package summary (5,000 Coins, $50, formula 5,000÷100); recipient; payment method (Apple/Google/gateway — SFL never shows a raw card form); price detail table (amount, base rate, calc, base price, FX, local estimate, tax/fee, due now); confirmation checkbox; CTA "Pay $50.00 USD" or "Continue to Secure Payment". States: ready · quote refreshing · **price changed (must reconfirm)** · FX refreshed · method unavailable · recipient unavailable · restricted · terms not accepted · server unavailable.
- **J3-06 Native Payment Provider** — SFL creates pending txn + payment request (buyer ID, recipient ID, coins, USD base, local quote, unique ref); native sheet opens; provider returns; SFL verifies receipt server-side. Background shows coins/USD/recipient/ref. Outcomes: authorized · failed · cancelled · pending · unknown (interruption).
- **J3-07 Payment Processing** — "Verifying Your Purchase"; stages Payment received → Receipt verification → Crediting Coins; txn info; "Keep this screen open. Do not repurchase during verification." No Pay button; back disabled / "Continue in Background". **Coins credited only after server verification; poll/receive server update, never rely on client callback.**
- **J3-08 Purchase Successful** — lime verified badge; "5,000 Coins Added"; recipient; previous 12,400 / +5,000 / new 17,400; paid $50; receipt SFL-90312; date; method; Done / View Receipt / Buy More / Return to <origin journey>. For another Fan: "5,000 Coins Sent to Priya" — buyer's own balance not shown increased.
- **J3-09 Receipt Details** — status Paid & Credited; receipt ID; provider txn ID; coins; USD base; FX; final charged; recipient ID; masked method; purchase date; credit date; support link; Download/Share · Report a Problem · Done. No full card/sensitive data.
- **J3-10 Value Activation Callout** — see §6.
- **J3-11 Payment Failed** — "Payment Wasn't Completed / No Coins were added"; safe reason (declined/insufficient/auth failed/method unavailable/provider error); coins/USD/ref; Try Again · Another Method · Return to Store · Support. Coral strip, no blame.
- **J3-12 Purchase Cancelled** — "You were not charged"; package dimmed; Return to Checkout · Back to Store. Neutral grey, no alarm.
- **J3-13 Payment Received, Credit Pending** — "Payment Received / Coin credit still being verified"; coins/USD/ref/last-checked; "Do not repurchase"; Check Status · Continue in Background · Support. Payment stage lime, verify gold-animated, credit grey. If app closed, verification continues server-side + notification.
- **J3-14 Connection Lost** — **before submission:** "payment was not submitted, try again". **after submission:** "we cannot confirm status yet, do not repurchase until checked" → Check Purchase Status. Never auto-assume failure after submission.
- **J3-15 Store/Region Unavailable** — maintenance/provider down/region restricted/account restricted; existing balance stays visible; Try Again · Return · Support. Closed-gate metaphor.
- **J3-16 Duplicate Payment Callback** — one txn credits once; repeat callback → load original receipt, "Purchase Already Completed" (original amount/receipt/credit time/current balance), View Receipt.
- **J3-17 Refund / Reversal** — status refund pending/refunded/reversed; original coins & USD; coins reversed; updated balance; original txn ID; refund ref; reason; View Original Receipt · Support · Done. Coral for reversed, grey pending, lime only on confirmed completion. Recovery-balance policy if coins already spent (confirm with client).

## 5. Purchase state model

`draft` (retry yes) · `recipient_validating` (no payment yet) · `ready` (yes) · `payment_open` (no) · `provider_processing` (no) · `receipt_verifying` (no) · `credited` (not same txn) · `failed` (yes) · `cancelled` (yes) · `credit_pending` (no) · `refunded` (new purchase only) · `reversed` (new purchase only).

## 6. Value activation (J3-10)

`Activation Opportunity = Active Club ∧ Verified Coin Purchase`
`Fan Value Activation = Active Club ∧ Verified Purchase ∧ Available Coins ≥ 36 ∧ Confirmed Seed`

- **A — no club:** "Coins Added. Your Club Comes Next." → Discover Fan Clubs.
- **B — club joined, <36 Coins:** "Build Your Activation Balance / minimum 36-Coin club seed, you have 20." → Buy More Coins.
- **C — eligible:** "Your Value Is Ready to Activate / Seed at least 36 Coins into Red Devils FC." `17,400 − 36 = 17,364 remaining`. → Seed 36 Coins & Activate · Do This Later.
- **D — already active:** no callout; return to origin.

Fan Value result formula (shown only after activation explained): Win +30 · Draw +10 · Loss 0.

## 7. Conversion rules (executed in Journey 13, referenced here)

- Coins→Gold: `Gold = ⌊Coins × 10/130⌋` (130 Coins → 10 Gold)
- Gold→Coins: `Coins = ⌊Gold × 100/13⌋` (13 Gold → 100 Coins)
- Disclosed commission: `30/130 = 23.08%` on Coins→Gold. Shown before confirmation.
- Gold withdrawal reference: `≈ USD = Gold/13` → 130 Gold ≈ $10.

**Three distinct rates the UI must never conflate:** Buy Coins 100:$1 · Coins→Gold 130:10 · Withdraw 13 Gold ≈ $1. (Retuned so $1 of coins still yields the same gold as the old 13:10 when 10 Coins = $1.)

## 8. Notifications, analytics, accessibility

Buyer/recipient/pending/refund notifications (sender identity per privacy settings). Analytics events per the list; **never** include phone/email/full payment data. A11y: 44×44 targets; 14–16px body; tabular numerals; gold contrast on dark; selection not colour-only (checkmark); reduced-motion; every status = icon+colour+text; screen-reader announces coins/USD/recipient/state; warn before exiting unresolved payment.

---
---

# Review — issues found (journey above unchanged)

## Two things that contradict decisions we already locked

**R1 — The currency is a TWO-currency system, and my earlier "Gold everywhere" normalization was wrong.** In Journey 1 (v2) I recorded "currency is Gold everywhere; all 'Coins' copy replaced," and I applied that to Journey 2. Journey 3 reveals the real economy: **Coins and Gold are two different currencies with distinct roles.**
- **Coins** — the hard top-up currency, bought with USD (100 Coins = $1). This is what J3 is entirely about.
- **Gold** — obtained by converting Coins (13 Coins → 10 Gold, §7), used for gifting/support and eligible for withdrawal (13 Gold ≈ $1).

So the correct model is: **you buy Coins; you convert Coins to Gold; you spend/transfer/withdraw Gold.** My J1/J2 correction over-collapsed this. The fix: Coins label applies to purchase, top-up balance, and the store; Gold applies to gifts, peer transfers, and cash-out. Journey 3 is the source of truth for the economy — I'll re-open the J1/J2 "Gold everywhere" note and split it. **This changes currency labels on already-built screens** (the gift tray priced "🪙 Gold" should be Coins if gifts are bought directly, or Gold if gifts are paid from converted Gold — needs one clear rule, see R3).

**R2 — J3-10 re-couples Fan Value to a mandatory paid seed, reversing the decoupling you confirmed in Journey 2.** On Journey 2 you said "go with recommend," which set: *Fan Value activates on club membership alone — no mandatory purchase; value driven by participation, not results.* But J3-10's activation formula is `Active Club ∧ Verified Purchase ∧ Available Coins ≥ 36 ∧ Confirmed Seed` — i.e. you **must buy Coins and seed 36 of them** to activate. That's exactly the pay-to-activate gate we removed, and it re-opens the regulatory concern (paying real money to unlock a progression system). **Pick one:**
- (a) Honour J2: Fan Value activates free on membership; the 36-Coin seed becomes an **optional** "starting stake / boost," never a gate. *(My recommendation — keeps the decoupling and the cleaner regulatory posture.)*
- (b) Override J2: activation requires the paid seed — then accept the pay-to-activate posture and get it legal-reviewed per market.

(Minor: J3-10 says "Red Devils FC"; the club elsewhere is "Red District FC.")

## Two external constraints that reshape the economy

**R3 — Real-money withdrawal + peer transfers = money-transmission / e-money regulation, and it collides with app-store rules.** Two hard constraints stack here:
- **Apple/Google mandate their in-app purchase (StoreKit / Play Billing) for consumable digital currency like Coins, taking ~30%.** An "approved payment gateway" is not permitted for digital-coin top-ups on iOS/Android. That 30% cut is almost certainly *why* the convert/withdraw rates are so punitive — but it must be designed in: you sell $1 of Coins, the platform nets ~$0.70 before your own margin.
- **A currency you buy with real money, send to other users, and cash out is regulated as stored value / money transmission** (e-money licence, KYC/AML, geofencing) in most markets — a bigger surface than the Fan Value gambling flag. Worse, **Apple prohibits using IAP to buy anything cash-redeemable** — so the Coins (IAP) → Gold (withdrawable) bridge may itself violate store policy. The two-currency split looks like an attempt to thread this needle; whether it actually complies needs a real payments/legal review before this is built, not after. Flagging as **foundational**, not cosmetic.

**R4 — Purchase & velocity limits should be required, not "if introduced."** With $1,000 packages, per-user daily/monthly spend caps, velocity checks, and cooling-off are AML/responsible-spending requirements in regulated markets, not optional polish. Recommend the "maximum purchase limit reached" state is a launch feature.

## Smaller notes

- **R5 — The $50 default anchors high.** Pre-selecting 5,000 Coins ($50) and labelling it "Popular" anchors spend upward. A user-friendlier default is a $5–$10 tier; high-anchor is a deliberate monetization choice — just make it conscious.
- **R6 — Round-trip loss is severe.** $1 → 100 Coins → convert → Gold → withdraw. Convert is still 13 Coins → 10 Gold (not retuned here); the cash-out screens (Journey 13) must show the live round-trip honestly so it doesn't read as a bait-and-switch.
- **R7 — Theme:** this journey's own spec calls for **dark cinematic** (near-black, gold-on-black, "no white banking interface"). That's your explicit instruction for J3, so I'll build it dark — consistent with "financial/immersive surfaces are dark, app chrome is light." Confirming this is intended and not a conflict with the light direction.

## Recommendations (say "go with recommend" to unblock the build)

1. **Currency:** two currencies — **Coins** (buy/top-up/store) and **Gold** (gift/transfer/withdraw via conversion). Re-split the J1/J2 "Gold everywhere" note. *(R1)*
2. **Fan Value:** stays **free on membership** (honour J2); 36-Coin seed becomes an **optional boost**, not a gate. *(R2)*
3. **Payments:** design for **native IAP (StoreKit/Play Billing), ~30% cut**; treat withdrawal/P2P as a **regulated, legal-review-gated** feature, likely post-MVP. *(R3)*
4. **Limits:** spend/velocity caps are **launch features**. *(R4)*
5. **Default package:** pre-select a **mid-low tier** (e.g. 100 Coins / $10) as "Popular". *(R5)*
6. **Theme:** build J3 **dark cinematic** per its own spec. *(R7)*

The 17 screens themselves (store, recipient, review, processing, success, receipt, all the negative/pending/duplicate/refund states) are well-specified and ready to design as soon as R1/R2/R7 are confirmed — those three set the currency labels, the activation copy, and the theme, which appear on nearly every screen.

---

# Confirmed (v2) — recommendations accepted, one override

- **R1 accepted:** two currencies — **Coins** (bought with USD, top-up/store) vs **Gold** (gift/transfer/withdraw via 13:10 conversion). The J1/J2 "Gold everywhere" note is superseded by this split.
- **R2 accepted:** Fan Value **activates free on club membership**; the 36-Coin seed is an **optional boost**, never a gate. J3-10 copy reframed from "activate" to "boost."
- **R3/R4/R5 accepted:** native IAP posture; spend/velocity limits are launch features; default-select a mid-low package as "Popular."
- **R7 OVERRIDDEN by user:** build Journey 3 in the **light** system (not the dark spec in §3). Keep it premium/branded — gold for Coin values, green for selection/primary, coral for errors — not a sterile white bank.
