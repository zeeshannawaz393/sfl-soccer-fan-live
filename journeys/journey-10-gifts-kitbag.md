# Journey 10 — Gifts & Kit Bag

The emotional/commercial layer of the live experience. Fans spend Coins on football gifts to Hosts (or PK sides); gifts create stadium reactions, update J8's Coin counter, influence PK Fan Power where applicable, and become collectibles in the recipient's Kit Bag. Canonical: GK-01 Gift Menu · GK-02 Gift Animation States · GK-03 Kit Bag.

## Mechanics

Registered Fan sends; Host receives; Guests can't gift (register + join club first). In PK a gift targets a side. **Coins only** — sending debits the wallet; prices from 1 Coin up (Football = 10, locked; other prototype prices are examples, from server catalogue). `Total = P × Q`, allowed iff `B ≥ Total`, `B_new = B − Total`. On confirm: debit once, live counter += Total, PK side += Total, Fan Power recalcs, animation plays once (×Q). Wallet row: "Gift sent · Golden Boot · −199 · GFT-8841". Display **Coins, not USD** (settlement/commission undefined).

## Catalogue & rarity

Categories: Popular · Match Day · Trophies · Golden Boot · Golden Glove · Fan Support · PK Battle · Referee · Stadium · Club Kit · World Cup · Legends · VIP · Awards (→ J5). Rarity (recommended, configurable): Standard · Rare · Epic · Ultra-Rare · Legend — controls **visuals/animation/sound/chat prominence only**. **Rarity never multiplies Fan Power** — contribution = actual confirmed Coin cost (matches J8).

## Screens

GK-00 Gift Access Gate (guest / no-club / restricted) · GK-01 Gift Menu (recipient/side header, category tabs, 3-col gift grid, balance) · GK-01A Gift Detail + Quantity (hero, qty selector, cost table) · GK-01B Confirm Gift · GK-01C Insufficient Coins (→ Buy Coins, return to same room, re-check) · GK-01D Sending (idempotency key, no repeat) · GK-01E Gift Sent (gift/qty/spent/new balance/ref) · GK-02 Animation States (standard 1–2s edge / rare crossing + club trail / ultra-rare-legend full stadium reaction) · GK-02A Combo & queue (combine identical, queue rares, compact lane for small; actual qty×price, no multiplier) · GK-02B Gift Received (Host: sender/gift/qty/"+199 confirmed support"/thank — never "You earned $X") · GK-03 Kit Bag (collectible grid) · GK-03A Item Detail (source, first collected) · GK-03B Empty · GK-03C Collection History (duplicate sources).

## Critical animation rule

Even the largest animation must never hide: PK timer, side Coin totals, Fan Power, End Live, or safety/report controls.

## Recommended Kit Bag ownership model

Sender pays Coins and **immediately sends** — the gift does **not** enter the sender's bag; the **recipient** collects a non-spendable collectible; duplicates increase the count; Kit Bag items **cannot be re-sent, sold, converted or withdrawn**. Kit Bag = a trophy cabinet, **not another wallet**. (Needs client confirmation.)

## Open decisions

Host settlement (Coins/Gold/credit?) · gift commission · full prices · exact rarity tiers & mapping · max quantities · repeat-send allowed? · which gifts need confirmation · reversed gifts reduce Kit Bag counts? · refunds after delivery? · gifts outside live rooms? · **Fan-to-Fan gifting permitted?** · gift expiry · zero-price promo gifts · do gifts feed Fan Value/club score? · **daily spend limits / responsible-spending controls?** · Hosts disable gift animations/gifting? · Awards-gift unlock via J5 · **club-kit/World-Cup licensing?**

---
---

# Review — issues (journey unchanged)

## A — Kit Bag as a trophy cabinet (not a wallet) is the right call, and it matters for compliance

The recommended model — pay-and-send, recipient collects a **non-spendable, non-resellable, non-withdrawable** collectible, Kit Bag = trophy cabinet — is correct and I've built it that way (no prices, no Sell/Convert/Withdraw/Send-Again anywhere). This isn't just tidy: if Kit Bag items *were* resellable or withdrawable, they'd become **another tradable virtual-asset surface** stacked on top of Journey 6's player market, adding more securities/money-transmission exposure. Keeping the Kit Bag purely commemorative — counts, not currency — is the single most important decision in this journey, and I strongly recommend confirming it as written.

## B — Rarity is visuals only (no Fan Power multiplier) — consistent, designed in

Matches Journey 8's rule: a 199-Coin gift contributes 199 regardless of rarity. Rarity drives animation size/sound/chat prominence, never the score. Built that way.

## C — Fan-to-Host only; Fan-to-Fan gifting is a separate, regulated feature

The doc flags that chat shows a Gift button but the requirement is Fan→Host. **Recommend gifting stays Fan→Host (and Fan→PK-side) only.** Fan-to-Fan gifting is a peer transfer of purchased value — the same money-transmission surface as the Gold P2P transfer flagged back in Journey 3 — and shouldn't be added casually. If it's wanted, it needs the same regulated-feature treatment. Designed Fan→Host/side only.

## D — Daily spend limits & responsible-spending are launch features here, not "if introduced"

Gifting is the app's **primary spend mechanism**, and it stacks on the gambling surfaces (J5 predictions, J6 trading). Per-user daily/velocity spend caps, spend summaries, and responsible-spending prompts are the standard duty-of-care for a Coin-gifting economy and belong at launch — especially since large gifts (999-Coin VIP Box) are one tap away. Flagging as a launch requirement.

## E — Host never sees cash — Coins only

"+199 confirmed support," never "You earned $19.90" (settlement undefined). Followed.

## F — Consistency & other flags

Idempotency (one gift = one debit); combo uses real qty×price (no artificial multiplier); animations are **non-blocking overlays** that never cover the PK timer / side totals / Fan Power / End Live / safety controls. **Licensing:** Club Kit / World Cup / Legends gift categories need real rights or must be original/generic — I've used emoji as stand-ins for the "3D football object" renders (the spec itself notes emoji are placeholders). **Theme:** the gift menu and animations are live-room **overlays over the video** (per the J8/J9 precedent); the **Kit Bag is a light** locker-room collection screen.

No confirmation gate needed to build; A (Kit Bag = collectible, not wallet) is the one decision worth confirming explicitly, since it defines whether the Kit Bag ever becomes an economic surface.