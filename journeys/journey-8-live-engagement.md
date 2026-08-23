# Journey 8 — Live Engagement: Coins & Possession

Not a destination — the real-time engagement engine embedded inside J7 (Formation Live Rooms), J9 (PK Battles) and J10 (Gifting). Two canonical components: **LE-01 Coins Counter** and **LE-02 Possession bar**. Production values come **only from server-confirmed Coin events** — the prototype's random counter/possession animation is visual-prototype-only.

## Critical distinction

- **Coins** = absolute integer ("4,820 Coins sent") — total of successful qualifying Coin-backed support events this session. Metallic gold.
- **Possession** = relative % ("Blues 61% — 39% Reds") — each side's share of qualifying support. Club/team colours. **Never manually editable; the app calculates it.** Never presented as a Coin/wallet/cash balance.

## Formulas

- Coins: `Total = Σ Gᵢ`. Gift contribution `= UnitPrice × Quantity` (199×2 = 398). Counter 4,820 + 398 = 5,218.
- Viewer wallet: `New = B − G`, accepted only if `B ≥ G`. On debit failure: no animation, no counter increase, no possession change, balance unchanged.
- Possession: `A/(A+B)×100`; `B = 100 − A`. Display: round A, derive B = 100 − A (always sums to 100). No rarity multipliers — a 199-Coin gift contributes 199, full stop.

## Qualifying support

Count: successfully purchased+sent gifts, direct Coin support (if added), PK gifts assigned to a side, watchalong gifts assigned Home/Away — quantity × actual Coin price. Exclude: failed/pending/refunded/duplicate/free/test/fraud-blocked/unsuccessful-debit.

## Two-sided vs single-Host (key correction)

Possession only appears where there are **two valid support targets**:
- **PK Battle:** Host A vs Host B — viewer picks a side.
- **Match Watchalong:** linked fixture → Home = Side A, Away = Side B.
- **Single-Host Fan Party:** show the **absolute Coins counter only; hide possession** (no legitimate second side). The prototype's fake "North 62% — 38% South" with random 20–80 swing must not ship.

## Components / states

LE-00 Explanation (first entry) · LE-01 Regular Coins counter (zero/active/+gift/large/syncing/final) · LE-01A PK side counters · LE-01B Gift-confirmed event (confirm → animate → counter → side total → possession) · LE-01C Coins detail sheet · LE-02A Possession initial (50/50 "no support yet" — avoids ÷0) · LE-02 Live possession bar (neutral/A-leads/B-leads/tie/100-0/swing/syncing/final; **not** clamped to 20–80) · LE-02B Swing event (config thresholds change animation, never the result) · LE-02C Possession detail (shows the division) · LE-03 Reconnect/sync (freeze official values, no simulated movement, restore server snapshot) · LE-04 Final summary (Full Time totals; PK final possession — winner decided in J9).

## Server-authoritative flow

Event: id, session id, sender, receiver side, gift id, unit price, qty, total, status, timestamp, sequence. Status `Created → Confirmed → Counted`; failure `Created → Failed`; refund `Confirmed → Reversed`. Only Confirmed & non-reversed count. **Idempotency: `Count(EventID) = 1`** — duplicate WebSocket messages or repeated taps never double-count.

## Currency labelling

`100 Coins = $1` but the live counter **never** shows USD/earnings/cash/withdrawable — Host settlement & commission are undefined, and Coins-sent ≠ Host earnings. Label is always **"Coins sent."**

## Open decisions

Regular-room side definition · hide possession when single-Host (rec: yes) · qualifying = actual price, no multipliers (confirm) · Host settlement (Coins/Gold/%?) · live-gift commission · refund effect on live possession · possession time window (rec: session/PK round) · zero state (rec: 50/50 + "no support") · rounding (rec: round A, derive B) · top-fan visibility · linked fixture for watchalong · direct Coin send control · fraud/correction · finalization delay · Host task credit.

---
---

# Review — issues (journey unchanged)

## A — "Possession" directly contradicts the approved design direction; renamed to "Fan Power"

The design direction (§9 and §20) is explicit: **the gift-support metric must be called "Fan Power" / "Support Score", NOT "Possession"** — because possession has a real football meaning (ball-possession %) and it's misleading to represent gift *spending* as possession. §20's avoid-list literally reads "Calling gift-based support 'Possession'." We already built it as **"FAN POWER"** in the dark Fan Derby template and the light Journey 5 derby.

Journey 8 is titled and written entirely around "Possession." That's a head-on conflict with a locked direction. **I've designed these components using "Fan Power"** (with the same math), and flag it so you can override: if you specifically want the word "Possession" despite §20, say so and I'll swap the label — the mechanic is identical either way. My strong recommendation is to keep **Fan Power** for consistency with everything already built.

## B — The single-Host possession fix is correct; designed exactly that way

The doc's core correction — possession/Fan Power appears **only** with two valid support targets (PK, or a watchalong's Home/Away), and a single-Host room shows the **absolute Coins counter only** — is right, and it kills the prototype's fake random North/South bar. I've built two variants: a single-Host room with **just** the gold Coins capsule (no Fan Power bar), and a two-sided room with side counters + the Fan Power bar. This also implies J7's Go Live setup should later capture room type + optional linked fixture + Side A/B (noted as a recommended addition, not locked).

## C — Server-authoritative, no random motion, idempotency — followed in the design

Every value shown is a *confirmed* state, not a simulated one; the gift-confirmed sequence updates counter → side total → Fan Power **after** confirmation; the reconnect state **freezes** the last confirmed values rather than inventing movement; and the "one EventID = one count" rule is reflected (a single gift = a single +199). No decorative/random possession swing anywhere.

## D — Never "earnings/USD/cash" — followed

The counter is labelled **"Coins sent"** everywhere; no USD conversion, no "earnings," per the undefined-settlement rule.

## E — Theme / surface note

These components are **overlays on the live video** — physically, a Coins counter and a Fan Power bar sit over the broadcast (the Host's camera), not on a white page. So I've rendered them as premium glass overlays over a photographic live background — which is exactly the look of the reference images you liked (video + gold/club-colour overlays). The **explainer and the detail sheets are light** bottom sheets (utility surfaces). This keeps the app chrome light per your standing instruction while treating the live-video surface as what it is. If you want even the video-overlay chrome reworked, say so — but a live counter can't live on a flat white background.

No confirmation gate needed to build; A is the one decision for you (keep "Fan Power," or force "Possession").