# Journey 6 — Player Transfer Market

Fans buy and sell virtual player assets linked to real footballers. Prices move on real match results; purchases use Coins; every transfer is escrow-protected. Separate from Journey 15 (which transfers/loans actual Fan *memberships* between clubs).

## Mechanics

**Access:** Guests browse only. Registered Fans transact (Managers/Hosts via Fan role). Must have **joined a club** to transact. **Player Value activates** after joining a club + completing first Coin purchase; missing prereq → Join Club or Buy Coins gate.

**Player Value ≠ wallet balance** (must be crystal clear): "420 Player Value" is the app-set *sale price*, not 420 spendable Coins; can't be withdrawn/converted directly; Coins enter the wallet only on a completed sale. UI label: "Current market value · 420 Coins" + tooltip "Player Value is the app-set sale price. It is not part of your wallet balance."

**Value movement:** Win +30 · Draw +10 · Loss 0. `V_new = V_current + Δ`. A "locked variant" loss −20 with a floor `V_new = max(Floor, V_current − 20)` exists but **activation trigger + floor are undefined → server-configured, don't invent.**

**Escrow:** buyer balance B, price P → spendable `B − P`, escrow holds `P`. On completion: player moves seller→buyer squad, escrowed Coins release to seller, purchase price becomes buyer's acquisition baseline. On failure: refund P. **No fee/commission defined → none shown until confirmed.**

**P/L:** Unrealized `= Current App Value − Acquisition Price` (not earned by value rising). Realized `= Completed Sale Price − Acquisition Price` (only on completed sale). Squad value `= Σ current app value of owned players`.

## Screens

PL-00 Market Access Gate (guest / no club / no first purchase / offline) · PL-01 Player Market (card grid, filters, value + movement) · PL-01A Search & Filters (sheet) · PL-01B Empty/No-results/Error · PL-02 Player Detail (value + history chart with W/D/L markers, rules strip, fixtures, seller, escrow explainer, Buy via Escrow) · PL-02A Price Changed (reconfirm) · PL-03 Buy via Escrow (price/balance/after-hold/held + escrow copy) · PL-03A Insufficient Coins (→ Buy Coins, return to listing) · PL-04 Escrow in Progress (stepper: funds held → ownership transferring → coins released → complete; txn ID; dispute) · PL-04A Failed & Refunded · PL-05 Purchase Complete (new value baseline) · PL-06 My Players (squad: owned, squad value, Unrealized P/L, listings, pending; tabs All/Available/Listed/Pending) · PL-07 List for Sale (acquisition vs current app value, list at app value) · PL-08 Listing Live · PL-09 Sale in Progress (seller, buyer funded escrow) · PL-10 Player Sold (Realized P/L, Coins credited).

## Negative/system states

Listing sold while viewing (block checkout) · price change before confirm (reconfirm) · double-tap Confirm (one escrow only) · balance change during checkout (recalc) · another buyer starts escrow (reserve for first valid) · transfer fails (restore + refund) · escrow delayed (keep visible + support) · own listing (Manage, not Buy) · disconnect after confirm (recover via txn ID) · app closes (resume PL-04 via deep link) · dispute (freeze release) · result updates mid-checkout (respect server-approved price) · feed fails (preserve ownership, value temporarily unavailable).

## Open product decisions (server-configurable until confirmed)

Inventory model (rec: one unique instance per listing) · value scope (rec: one global app value per real footballer, per-Fan acquisition baseline) · loss-penalty trigger + floor · market/seller fee · listing expiry · squad limit · same-club transaction rules · postponed/abandoned-match value rule · task counting (count *completed* transfers, not listings) · escrow settlement time.

**Original docs also make Market a primary bottom tab (Home/Stadium/Market/Games/Wallet).**

---
---

# Review — issues (journey unchanged)

## A — This is the app's deepest regulatory surface, and it deliberately re-adds the mechanic we removed from Fan Value

Player Value **moves on real match Win/Draw/Loss**, you buy players with real-money-derived Coins, and you sell them for Coins that convert to Gold and withdraw to cash. That is, precisely: **buy an asset → its value tracks real-world sporting events → sell for a currency that cashes out.** This is the Sorare model, and Sorare is simultaneously fighting the UK Gambling Commission (gambling) *and* facing financial-instrument/securities questions over the same mechanic. Stacked on Journey 5's prediction-for-prize loop, this is the heaviest compliance item in SFL — securities *and* gambling exposure at once.

Worth naming clearly: back in Journey 2 you accepted my recommendation to **decouple Fan Value from match outcomes** specifically to avoid this. Journey 6 is a *different* system (a tradable asset, not a personal progression signal), so it's not a contradiction — but it re-introduces the exact result-linked-value mechanic we kept out of Fan Value, in the one place where it carries the most weight. That's a deliberate product choice; I'm flagging it so it's a conscious one. Design-agnostic (screens look the same regardless of how it's classified), so I've built it as concept — but it needs a combined **gambling + securities** legal opinion per market before any real launch, and likely geofencing + 18+ + the responsible-play scaffolding from J5.

**One thing in the design actually helps the posture:** listing price is the **app-set value, not free-entry** (the Fan can't name an arbitrary price). That makes it read more like a controlled game economy than a peer-to-peer securities exchange, and it blocks wash-trading/manipulation. Keep that — it's a good decision both for fairness and for the regulatory framing.

## B — Navigation conflict: original docs want Market as a primary bottom tab; our approved direction demoted it

The original docs list Market as a primary tab (Home/Stadium/Market/Games/Wallet). But the approved design direction (§2 hierarchy, §3 nav) deliberately put "football games and player collections" **7th of 8 priorities** and moved Market *out* of primary nav ("Market sits under My Squad / Collect"), specifically so the app leads with people and clubs, not a trading floor. Leading the bottom nav with Market contradicts the "people first, utilities third" thesis — and, given flag A, leading with the trading floor is also the wrong regulatory optics.

**Recommendation: honour the design direction — Market is reachable (via Me → My Squad, and Matchday surfaces) but not a primary bottom tab.** This is a genuine docs-vs-direction disagreement, so it's your call; I've designed Market as a destination, not a nav tab.

## C — Licensed player photography is required (stand-ins used)

This journey needs real footballer likenesses on the cards. Those are licensed rights (Sorare and EA pay heavily for them) — the same licensing gap I flagged in the very first review. I've used football-fan photography as stand-ins so the layout is real; the shipping product needs actual licensed player imagery, or the "players" become fictional/original characters.

## Consistency (all good)

Coins-only for buy/sell (correct, feeds the same wallet); escrow + idempotency + txn-ID recovery are as rigorous as J3/J5; **Unrealized vs Realized P/L** is labelled honestly (profit only on completed sale), matching J5's net-not-profit discipline; the "Player Value ≠ wallet" distinction is handled with an explicit tooltip. **Theme:** J6 spec asks dark navy; built **light** per standing instruction, with photographic player cards as the premium treatment.

No confirmation gate needed to build (nothing contradicts a locked decision). Built light; A/B/C recorded, B is the one real decision for you (Market as primary tab or not).

---

# Confirmed model (v2)

- **Player Value never decreases.** Same formula as Fan Value: Win +30 · Draw +10 · Loss 0. The J6 "−20 loss / floor variant" is **removed** — value only rises or holds. (Screens showing a ▼−20 chip / "Unreal. −20" need updating.)
- **Every fan club links to a real football team**, chosen at club creation (Model A from J11). A player's value tracks **that real footballer's real team's match results**.
- **Transfers are internal-only** — buying/selling players happens between Fans inside SFL, with **no link to real-world transfers**. The player is a real-footballer-backed asset whose *value* follows real results, but *ownership* moves only within the app.
- Combined with app-set listing prices (not free-entry), this is a **controlled internal game economy** on real-result-backed assets — the only real-world hook is the match-result value feed.
- **Consequence to note:** because value only goes up or holds, player prices are **monotonic** (they inflate over time; a held player never loses nominal value). This also *lowers* the speculation/loss framing versus a normal market — there's no downside from results — but the buy/sell escrow is still a real-money-adjacent flow needing the licensing/legal review flagged in §A.
- **Confirmed: 18 = a per-Fan squad floor** — every Fan must hold **≥18 players** in My Squad. Two consequences to resolve:
  - **Reaching 18 from zero is expensive if bought** (18 × ~app price ≈ thousands of Coins ≈ hundreds of USD) — recommend each Fan is **granted/drafted a starter squad** (naturally, the ~18 players of their linked real team) rather than buying up from empty, or onboarding stalls. *(Needs confirmation.)*
  - **Can't sell below 18.** The J4 task is a *paired* "buy 2 **and** sell 2," so it works as buy-then-sell around the floor; but a Fan sitting exactly at 18 must buy before selling. My Squad needs a **squad-count / "minimum 18" indicator** and the list/sell flow must **block the sale that would drop below 18** ("buy a player first").
- **Confirmed — starter squad:** joining a fan club is **not** empty — the Fan's squad is **seeded with the linked real team's players** (~18), so they start at the floor and trade from there. No buy-up-from-zero.
- **Confirmed — sell-floor guard:** My Squad shows a "minimum 18" indicator; the list/sell flow **blocks any sale that would drop below 18** ("buy a player first"). The J4 "buy 2 & sell 2" task works as paired buy-then-sell around the floor.
- **J6 screen updates (applied):** removed the ▼−20 / "Unreal. −20" states (value never decreases — falling/biggest-drop filters removed too); squad summary reflects the 18-player floor; a starter-squad note ("seeded from your club's team") on My Squad.