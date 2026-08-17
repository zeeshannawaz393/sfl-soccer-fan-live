# Journey 17 — Mini-Games

Short football-themed games where Fans spend to play and can receive Coins/gifts. Core: MG-01 Games Hub · MG-02 Penalty Shootout · MG-03 Spin the Wheel · MG-04 Result/Payout (+ MG-05 History). **Theme: DARK "Football Arcade"** (immersive game surface; explicit night-stadium direction) — flippable on request.

## ⚠️ The compliance headline — the cash-out loop
SFL already lets users **buy Coins with money → spend on chance games → win Coins → convert to Gold → withdraw to cash.** That money-in → chance → money-out loop can be **real-money gaming / gambling** depending on jurisdiction, and Apple/Google both police purchased-currency chance prizes with real-world value hard. **The cash-out relationship MUST be resolved with jurisdiction-specific legal + app-store review before release.**

**Built to the safer recommendation (Option A — Bonus Coins):** prizes are credited as a **separate, non-withdrawable Bonus Coins** balance (usable for gifts/games/in-app, never convertible/withdrawable/transferable) + Kit Bag gifts. This **breaks the money-out leg** — real money can enter (entry cost) but chance winnings can't leave. Also surfaced the free-daily-ticket entry (Option B) so play needn't always cost real Coins. This is a design choice that de-risks launch; the pure Coin-in/Coin-out variant remains a legal decision.

## Prototype economics are broken (kept as visual only)
Prototype penalty = 333% RTP (+23 Coins/shot expected); prototype wheel = 244% Coin RTP. The platform would haemorrhage currency. **These are examples only.** Built the UI against a **balanced example table (79% RTP)** — Saved 45% / Standard goal 40% (+10) / Great 12% (+20) / Top-corner 3% (+50) — and disclose odds on a rules screen. Real values are backend-config after legal sign-off.

## The outcome is server-decided, never the animation
`ExpectedPayout = Σ Pᵢ·Vᵢ`, `RTP = ExpectedPayout / EntryCost × 100`, `Margin = EntryCost − ExpectedPayout` (gifts get an internal value). Flow: **validate → reserve/deduct entry once → server commits + records outcome → app animates TOWARD the committed result → settle → return new balance.** Client `Math.random()` is never used. The wheel/ball animates to the already-decided result — never lands on one segment and awards another.

## Gross ≠ net (shown on every result)
`NewBalance = Previous − EntryCost + Prize`. Every result separates **Entry cost / Gross prize / Net change** — "Won 20" and "Net +10" are not the same and the UI never conflates them. Losses are calm and factual; **no fake near-miss** ("Almost won 50!") ever.

## Screens built
MG-01 Games Hub (Coins + Bonus Coins + free ticket, session summary) · MG-01R Rules & Odds disclosure · MG-01X Insufficient Coins · MG-02 Penalty aim (server-committed) · MG-02G Goal result · MG-02S Saved (calm) · MG-03 Wheel + prize table · MG-03A Spinning · MG-04C Coin/Bonus result · MG-04G Gift result (→ Kit Bag) · MG-REC Interrupted-round recovery · MG-PEND Payout pending · MG-REF Entry refunded · MG-LIM Daily limit / restricted region · MG-05 History.

---
---

# Review — issues

## A — The gambling / cash-out loop is the single biggest release risk in the whole app
This is where money-in meets chance meets (potentially) money-out. It needs **jurisdiction-specific legal review + explicit Apple/Google approval** before launch — non-negotiable, and bigger than any visual decision. I've de-risked the *design* by building **Option A (Bonus Coins)**: entry can cost real Coins, but **winnings land in a non-withdrawable Bonus bucket**, cutting the cash-out leg. If the client insists on Coin-in → Coin-out → withdraw, that's a deliberate legal exposure they must own, and the RTP/limits/age-gating all tighten accordingly.

## B — Prototype RTP > 100% would bankrupt the economy; fixed to a disclosed, balanced table
333% and 244% RTP are unshippable. Built to a **79%-RTP example** with the full odds table shown on the rules screen (MG-01R), because if segments look equal, users assume equal odds — so equal-size segments carry equal probability (or the difference is disclosed). Actual numbers are backend config post-legal.

## C — Outcome is server-authoritative; the animation only visualises it
The most important integrity rule: **the server commits the result before any animation**, the app animates toward it, and repeated taps return the same round (idempotency) — never a second charge. Built the round-status model (Reserved → Committed → Settling → Completed) into the recovery screens so an interrupted shot resolves from the committed outcome or refunds — a Fan is never charged for a round they can't see resolve.

## D — Gross vs net honesty, and calm losses
Every result card shows **entry cost, gross prize, and net change** as separate lines, and a zero-prize outcome is never dressed as a reward. Loss states are muted and factual — **no near-miss theatre**, no auto-"Spin Again", no fake countdowns or false scarcity. This is the "arcade, not casino" bar and the responsible-play line.

## E — Bonus Coins vs Coins is a real wallet-model addition
Introducing a non-withdrawable Bonus bucket touches J13 (wallet) and J16 (rewards): it must be **visually and functionally distinct** from spendable Coins and from Transferred Gold, and can be spent on gifts/games but never converted or withdrawn. Built it as a distinct cyan "B" chip. Confirm the client wants this bucket (it's the safest path) — if not, the whole cash-out question reopens.

## F — Responsible-play + privacy controls are built in, not bolted on
Daily play limit, session spend/net summary, easy exit, no auto-repeat, age/region checks, self-exclusion hooks. And a firm privacy line from the spec: **Managers must NOT see or control an individual Fan's game spending** — this stays out of the Manager Console (J14). Restricted-region shows an honest "unavailable here," never a fake technical error.

## G — Gifts create inventory, not wallet credit
A gift outcome writes a **Kit Bag inventory transaction** (J10), not a Coin credit — kept those paths separate so the wallet ledger stays clean.

## Theme
**DARK "Football Arcade"** — night stadium, real goalmouth/keeper imagery, floodlights, game-specific colour identities (penalty green, wheel purple/blue), cost always visible before play, currency never hidden by effects, football celebrations not casino imagery. Flippable on request.
