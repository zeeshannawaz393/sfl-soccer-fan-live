# Journey 12 — Progression, Levels & League Tables

Four distinct systems: personal **Fan Level** (1–20), monthly **Fan Club League**, real **Tournament tables**, and **Club Grade**. Canonical: PR-01 Fan Level · PR-02 Fan Club League · PR-03 Tournament Group Tables · PR-04 Club Grade.

## Metric distinctions (never conflate)

| Metric | What it is |
|---|---|
| Fan Value | Personal fan-performance metric (J11), non-cash |
| Fan Level | Personal progression 1–20 |
| Eligible Club Gold earned | **Lifetime cumulative** progression input (a ledger, not a balance) |
| Wallet Gold (Earned) | Current spendable/transferable Gold |
| Transferred Gold | Gold received from another user — hold or withdraw only |
| Club Monthly Score | Monthly combined eligible Fan contributions |
| Highest Spend | Separate club ranking on qualifying spend |
| Club Grade | Club status A / B / C |
| Tournament Points | Real football standings (3W+D) |

Fan Value ≠ Gold. League Points ≠ Coins. Tournament Points ≠ SFL reward points.

## Fan Level

Levels 1–20. Progress from **cumulative eligible Club Gold earned**. Higher levels = larger Gold-transfer limits; L20 unlimited. Known limits: L1 65 · L2 130 · L3 390 · L4 520 · **L5–19 undefined (don't interpolate)** · L20 unlimited. `CurrentLevel = max{L : C ≥ T_L}`, `ProgressToNext = C / T_{L+1} × 100` (prototype 1,240/2,000 = 62%, limit 520). Full threshold table missing.

**Critical: Club Gold earned is a lifetime ledger, not the wallet balance.** Earn 100 → spend 60 → Wallet Gold 40, but cumulative earned stays 100. **Levels must never drop because Gold was spent.** (Confirm the client doesn't intend one shared balance.)

## Gold-transfer limit

Allowed iff `A ≤ EarnedGold ∧ A ≤ L(F) ∧ Source = EarnedGold`. Transferred Gold can't be a source. Per-transaction vs per-period undefined (prototype = per-transaction).

## Approved activity (server-configured, no hard-coded amounts)

Include: daily/weekly tasks, club rewards, approved live, PK, recruitment, prediction participation, monthly rewards. **Exclude:** purchased Coins, converted Gold, received/Transferred Gold, refunds, duplicates, fraud, admin/test. Each event: FanID · ClubID-at-time · source · eligible Gold · approval · timestamp · ref.

## Screens

PR-00 Hub · PR-01 Fan Level Dashboard (Level badge, progress, transfer limit, Fan Value shown **separately, no Gold/Coin icon**) · PR-01A How to Earn · PR-01B Level Roadmap (1–20 ladder) · PR-01C Level Up · PR-01D Activity History · PR-02 Fan Club League (Rank/Club/Points/Fans/Live/Value/Grade, your-club pinned, prize cut-lines, podium, countdown) · PR-02A Club Contribution Breakdown · PR-02B My Contribution · PR-02C **Highest-Spending Clubs (separate, explicitly labelled — never "Best Clubs")** · PR-02D Monthly Close/Reset · PR-03 Tournament Group Table (P/W/D/L/GF/GA/GD/Pts, qualified/eliminated cut-lines) · PR-03A Group Fixtures · PR-04 Club Grade (metallic badge, monthly target, rank) · PR-04A Grade Rules · PR-04B Prize Eligibility.

## Monthly reset

Score resets monthly; **Fan Level does NOT reset**; Fan Value does not reset; previous month stays viewable; rewards → J16. Contributions **stay with the club where the activity occurred** when a Fan changes clubs (no retroactive move).

---
---

# Review — issues (journey unchanged)

## A — The Fan Value vs Fan Level conflict is resolved (correctly)

J11 said "Fan Value drives Fan Level"; J12 says "Level comes from Club Gold earned." The doc's own recommendation is the right one and I've built to it: **Fan Level = cumulative eligible Club Gold earned; Fan Value stays a separate fan metric** (it may feed the *Club League* via a defined weight, but does **not** convert directly into Level). So the two never merge — which is exactly why I showed them as distinct metrics on J4's My Stats and J11's dashboard. Resolved.

## B — "Club Gold earned" is a lifetime ledger, not the wallet — this is the important one

Progression must be driven by **lifetime eligible Gold earned**, which **never decreases when the Fan spends Gold**. If Level were tied to the current Wallet Gold balance, a Fan would *lose levels by spending* — almost certainly not intended. This means the wallet model has a **progression ledger** sitting alongside the spendable balances. I've designed the Level dashboard against the lifetime-earned figure, with the current Wallet Gold shown separately. **Please confirm** these are two different numbers (they should be).

## C — Highest Spend is kept separate from the main league — the right ethical call

Keeping "Highest-Spending Clubs" as its own explicitly-labelled leaderboard (never merged into the main "Best Clubs" table) matters: it stops the app from presenting **spending as the definition of fan performance**, which — stacked on the gambling/trading surfaces — would be a bad pay-to-win signal. Built as a distinct, clearly-titled tab in a gold/black treatment, separate from the contribution league.

## D — No invented weights or thresholds

L5–19 transfer limits, the full 1–20 threshold table, the League scoring weights (1 live hour = ? pts), Grade thresholds, and the monthly-target *unit* are all undefined. I've rendered these as **server-calculated placeholders** rather than inventing formulas, and the Grade screen **names its target unit explicitly** (the doc flags that "940/1,000" has no defined unit).

## E — The Gold-transfer limit is the money-transmission surface, and it's well-structured

Level-gated transfer limits + "Transferred Gold can't be re-sent" is effectively an **anti-money-laundering / responsible-transfer design** (trust rises with level; received value can't be passed through a chain). That's good — but it confirms **peer Gold transfer is a real money-transmission feature** (flagged since J3), so the limits, KYC and the withdrawal path need the same legal review before launch. Also confirm whether the limit is per-transaction or per-period.

## F — Tournament tables + Club Grade need real data + licensing

Real competition standings (World Cup / AFCON / UEFA) require a **licensed data feed** with **competition-specific tie-breaks** (don't assume they're identical across bodies), and real team/competition names/crests carry the licensing question flagged since day one. Same for the club→real-team results that drive Fan/Player Value.

## The complete economy/metric map (now fully specified — reference for the Wallet journey J13)

- **Coins** — bought with USD; spent on gifts/predictions/players/seeds.
- **Earned Gold** — current spendable Gold from tasks/rewards; transferable up to the level limit; withdrawable per rules.
- **Transferred Gold** — received from another Fan; hold or withdraw only, never re-sent.
- **Coins ↔ Gold** — 13:10 conversion (J3).
- **Lifetime eligible Club Gold earned** — progression ledger; drives Fan Level; never decreases.
- **Fan Value** — separate non-cash fan metric; may weight the Club League, not Level.
- **Club Monthly Score / Grade / Tournament Points** — club-competition and real-football metrics, distinct from all currency.

Theme: **light**. No confirmation gate to build; **B** (lifetime ledger vs wallet balance) is the one thing worth an explicit yes.