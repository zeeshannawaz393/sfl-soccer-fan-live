# Journey 11 — Fan Value Activation

Fan Value is a **non-cash performance metric** attached to the Fan. It activates only after the dependency chain completes and the Fan seeds **≥36 Coins** into their club.

## Activation dependency

`Eligible = ClubMember ∧ FirstCoinPurchaseCompleted ∧ CoinBalance ≥ 36 ∧ NotAlreadyActive`

Chain: register (SFL ID) → join club → **complete first Coin purchase** (free/reward Coins may not count) → hold ≥36 Coins → seed 36 → active → accumulates from qualifying results.

## Contradiction correction (from the journey itself)

J2 said "Player & Fan Value are now active"; J11 says active only after the 36-Coin seed. **Correct wording: "Player and Fan Value features are unlocked. Seed 36 Coins to activate your Fan Value."** States: **Locked** (no club/purchase) · **Unlocked** (club + first purchase) · **Ready to activate** (unlocked + balance ≥36) · **Active** (seed done) · **Paused/Transferred**.

## Formula

Win +30 · Draw +10 · Loss **0** (no negative, no floor, no −20 — that's Player Value, not Fan Value). `FVₙ = FV₀ + 30W + 10D`. Recommend seed 36 becomes the opening baseline (Model A) — needs confirmation.

## Fan Value is NOT currency

Never show a coin symbol, $ value, or Withdraw/Convert/Transfer. Display: **"Fan Value 2,140 · +30 after latest win"** in **electric lime / club colour, never currency gold**. Not spendable, not transferable (moves with Fan identity/club), not withdrawable.

## Seed transaction

Coins only (not Gold/Transferred Gold/Player Value/Kit Bag/Fan Value). `S ≥ 36`, `B_new = B − S`. Recommend **fixed S = 36 for v1** to avoid an undefined pay-to-rank mechanism. 36 Coins = $3.60 (purchase equivalent only; Fan Value never becomes cash).

## Screens

FV-00 Value Features Unlocked · FV-01 Explainer (W/D/L cards, "not currency" note) · FV-02 Confirm Seed · FV-03 Activation Processing (atomic) · FV-04 Activation Success · FV-05 Active Dashboard (non-currency hero, value line chart, W/D/L summary) · FV-06 History (result rows + seed row + reference IDs, corrected results show original + replacement) · FV-07 Latest Result Update (win/draw/loss — loss is neutral, not coral) · FV-08 Insufficient Coins · FV-09 Missing Prerequisite (checklist) · FV-10 Already Active (no second debit) · FV-11 Loan/Transfer (value moves with the Fan, not reset/sold).

## Result processing

Idempotency `Count(FanID,FixtureID) ≤ 1`. Only fixtures settled **after** `activated_at` count (no retroactive value → prevents strategic late activation). Postponed/void → no change. Correction (Win→Draw) shows original +30 and corrected +10 (net −20) in history.

## The critical structural gap — what produces W/D/L?

Managers create custom clubs with **no required link to a real football team**, yet Fan Value grows on "the club's real results." This can't be built until a model is chosen: **Model A** link each club to a real team (admin-approved) · Model B internal SFL virtual W/D/L competition · Model C Fan picks a supported team. Recommend **A** (matches "your club's real results") → club-creation needs a **"Supported real-world team"** field + verification.

## Open decisions

Seed→baseline? · larger seeds? · where the 36 Coins go (club/platform/locked/consumed) · seed refundable? · Manager commission on seeds? · **real result source** · retroactive? · max/decay/reset? · FV→Fan Level formula (J12) · % to club rankings · effect on Gold transfer limits · active after leaving club? · new seed per club? · loan result attribution · corrected/abandoned handling · public on profile? · Manager sees history? · club-closed handling · restriction pauses accumulation? · one-time lifetime or per-club?

---
---

# Review — issues (journey unchanged)

## A — J11 reverses the "free activation" we confirmed; I'm building the mandatory seed as specified

This is the resolution of a flag I raised three times (J2 R2, J3 R2, and again here). You'd confirmed *free* activation twice; J11 — the authoritative Fan Value spec, which explicitly rewrites the J2 message — makes the **36-Coin seed mandatory**. That's a clear, deliberate decision, so I'm building it. Two consequences:
- **The J2-21 and J3-10 screens I already built need copy updates** from "Fan Value is active / optional boost" to "unlocked → seed 36 Coins to activate." Minor edits; flagging so the set stays consistent.
- **The regulatory note, one last time (design-agnostic, concept-stage):** paying real-money-derived Coins to activate a progression feature whose value then moves on real match results is the pay-to-activate mechanic I flagged. **But** — importantly — J11 makes Fan Value **non-cashable** (no withdraw/convert/transfer, explicitly not currency). That materially *lowers* its exposure versus Journey 6's Player Value, which *is* tradable/cashable. So Fan Value is the milder of the two surfaces; the seed is the only real-money touchpoint and it's a fixed one-off. Keeping the seed **fixed at 36** (not variable) is important and correct — a variable seed would be a direct pay-to-rank mechanism.

## B — "Fan Value is not currency" is the right call, and I've designed it that way

Lime / club-colour value hero, **no coin icon, no $, no withdraw/convert/transfer** — only the 36-Coin *seed* is gold (because that's the Coin spend). This visual separation is what keeps Fan Value from reading as another wallet, and it's exactly what mitigates the concern in A.

## C — The real blocker for implementation: nothing produces the W/D/L yet

This is the most important flag in the journey and it's **not** design — it's architecture. Fan Value grows on "the club's real results," but clubs are created with no link to a real team. Until a model is chosen it literally cannot be computed. **Recommend Model A** (link each SFL club to a real football team, admin-approved) since it matches the wording — which means:
- The **Create-Club flow (a Manager journey) needs a "Supported real-world team" field** with verification.
- You need a **real-results data feed** (Opta/Sportradar or equivalent) as the oracle.
- Real team names/results/crests carry the same **licensing** question flagged since day one.

Design-agnostic (the screens look the same), but this is the thing that gates a working Fan Value more than any screen.

## D — Consistency (built in)

Seed uses **Coins only**; idempotency (one fixture affects a Fan once); Fan Value **moves with the Fan** on loan/transfer (belongs to the Fan, not sold to the club); **loss = 0** with no floor (distinct from Player Value's −20); **no retroactive** value. Seed→baseline (FV starts at 36) is designed as Model A but flagged for confirmation. **Theme:** light, per standing instruction.

Building the full set. The one decision that actually unblocks a *working* Fan Value is **C** (how W/D/L is produced); A is already decided by J11.

---

# Confirmed: the W/D/L source (resolves flag C)

**Model A is confirmed.** Every fan club **links to a real football team, selected at club creation** — that team's real match results drive both Fan Value and Player Value (Win +30 · Draw +10 · Loss 0, never decreasing). This means:
- The **Create-Club flow (Manager journey) requires a "Supported real-world team" field** with admin verification.
- A **real-results data feed** (Opta/Sportradar-type oracle) is the settlement source.
- Real team names/results/crests carry the **licensing** requirement flagged since day one.