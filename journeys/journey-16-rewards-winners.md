# Journey 16 — Rewards & Monthly Winners

Collects rewards earned across SFL (J4 tasks, J5 predictions, J12 league, J14 recruitment/targets) and announces monthly winning clubs & Fans. Core: RW-01 Rewards Hub · RW-02 Monthly Winners. **Theme: hybrid — LIGHT for the Rewards Hub + claim flows (app chrome); DARK "Trophy Night" for RW-02 Monthly Winners (immersive celebration).**

## Reward categories
- **Individual Fan** — correct prediction, daily/weekly tasks, voting outcome, personal campaign.
- **Club performance** — grade reached, league climb, recruitment target, monthly target, winning position. **Destination must be explicit: Manager personal wallet vs club wallet vs divided among Fans — never ambiguous.**
- **Monthly competition** — top clubs, highest-spending clubs, winner announcements, your club's position + prize. (Individual "Top Spender" = recognition only; no defined individual prize.)

## The J5↔J16 conflict — RESOLVED (single claimable ledger)
J5 said prediction rewards auto-credit on resolve; J16/prototype say manually claimable. **Can't be both.** Chosen rule: **one central reward ledger** — `Pending → Verified → Claimable → Claimed → Wallet Credited`. Prediction result reads "You won 20 Coins — ready to claim," Fan claims in RW-01. Gives one consistent mechanism + lets fraud checks finish before wallet credit. (If client prefers auto-credit: drop Claim, show "Credited.")

## Calculation rules
- **Personal:** `Credit = configured amount`, into the exact currency bucket. **Coins never silently become Gold, Gold never silently becomes Coins.** Transferred Gold is never a reward destination.
- **Club monthly score:** `Score = Σ eligible Fan contribution` — weights/caps/fraud-exclusions/tie-breaks are **backend config**, not invented; explained in "How rankings work."
- **Highest spend:** separate from league score; `= Σ qualifying Coin spend by eligible Fans`. Which spend qualifies (live/PK gifts, predictions, votes, players, mini-games) is client-defined. **Buying Coins ≠ spending until used.**
- **Shared club prize (MVP):** equal split — `Base = ⌊Prize / EligibleFans⌋`, remainder distributed one-at-a-time to highest eligible contributors deterministically. 5,000 / 100 = 50 each. Eligibility criteria (joined before cut-off, member at close, min activity, not fraud-blocked, didn't leave early) visible **before** month ends.

## Screens built
RW-01 Rewards Hub (light) · RW-01A Reward Detail — Prediction · RW-01A-C Reward Detail — Club (explicit destination) · RW-01B Claim Confirmation · RW-01C Claim Success · RW-01D Locked/In-Progress · RW-01E Claim Failed/Under-Review · RW-01F Reward History · RW-02C Provisional Rankings (dark) · RW-02D Results Under Review (dark) · RW-02 Final Podium (dark Trophy Night) · RW-02A Your Club Result (dark) · RW-02B Prize Distribution Breakdown · RW-02E Top Spender Recognition.

---
---

# Review — issues

## A — The J5 auto-credit vs J16 claim contradiction is the headline, and it's resolved
The same reward cannot both auto-credit (J5) and be manually claimed (J16). Built the **single claimable ledger** (`Pending→Verified→Claimable→Claimed→Credited`) so predictions, tasks, and club rewards all flow through one mechanism, and fraud/verification finishes **before** money hits the wallet. The prediction result now says "ready to claim," not "credited." This is a real behaviour change to J5's copy — flagged there. If the client wants auto-credit instead, it's a one-line switch (drop Claim, show "Credited").

## B — Currency integrity: Coins stay Coins, Gold stays Gold
Every reward card names its **destination bucket** and its **currency**, and the two never silently convert. Transferred Gold is never a reward destination (it's the received-from-a-Fan bucket, J13). This keeps the wallet model (J13) honest end-to-end.

## C — Club-reward destination must be decided before claim (built as explicit)
"Red Fury reached Grade A → 100 Gold" is meaningless until it says **whose** wallet. Built RW-01A-Club so the destination (Club Wallet vs personal Gold) is shown above the Claim button and can't be ambiguous — the spec's own non-negotiable.

## D — League Ranking and Highest-Spending are separate, never one podium
Kept them as **distinct tabs** in RW-02 with their own scoring explanation — mixing "best club" with "biggest spender" into one podium would present spending as merit (the same pay-to-win risk flagged in J12). Whether a club can win both prizes or only the higher one is a client decision (noted).

## E — Provisional ≠ final; celebration only after verified success
RW-02C shows a countdown and "results subject to verification" and **declares no winner**; RW-02D is the under-review hold with **no claim buttons**. The podium and confetti appear only in RW-02 (Final). This matches the spec's "celebrate after verified success, not before" and protects against announcing a winner that fraud review later changes.

## F — No "spend to recover rank" pressure; Top Spender is recognition, privacy-guarded
The non-winning club state avoids any "spend more to climb" nudge and points to "How rankings work" + next competition date. Top Spender (RW-02E) is labelled **recognition only** (no individual prize is defined) and I used a **contribution tier / rank rather than a precise personal spend total** as the safer public display — exact amounts are a privacy choice.

## G — Nothing disappears silently; corrections are ledger entries
Expired/revoked/under-review/corrected all have explicit, calm, factual states with a reason + reference ID — a user never just sees a reward vanish. Corrections write a visible ledger entry; wallet transactions are never silently edited (J13 invariant).

## H — Undefined values rendered as config, not invented
Score weights, per-Fan caps, qualifying-spend list, tie-breaks, expiry policy, and exact prize amounts are all **backend-configured placeholders** with a "How rankings work" surface — no invented business rules. Prototype amounts (20 Coins, 40 Gold, 5,000 prize) shown as examples.

## Regulatory note
No new money-in/out here (rewards credit existing wallet buckets), so this journey is lower-risk than J13 — but the reward ledger inherits the same audit/idempotency discipline (atomic, idempotent claim; no double-credit on repeated taps). Real club identity keeps the licensing flag. Concept stage.

## Theme
Hybrid per the standing rule: **LIGHT** Rewards Hub + claim flow; **DARK "Trophy Night"** Monthly Winners (podium, club-colour glow, gold/silver/bronze, real stadium celebration) — the immersive-celebration exception, flippable on request.
