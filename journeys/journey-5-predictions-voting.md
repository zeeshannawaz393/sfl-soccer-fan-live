# Journey 5 — Predictions & Voting

## Purpose

Let eligible Fans spend Coins on: exact-score match predictions, MOTM/WOTM selections, and league/tournament award voting. Every paid entry shows: type, cost, closing time, possible reward, winning slots, one-vs-multiple-entry rule, server-recorded timestamp. A platform oracle resolves the event, determines winners, updates Wallet + Notifications.

## Locked requirements

**Exact-score prediction:** cost **13 Coins**; correct-result reward **20 Coins**; closes **15 min before kickoff**; **one entry per Fan per match**; exact score required; timestamped; charged on submission; winning-slot info shown; oracle-resolved.

**MOTM/WOTM:** **13 Coins** per vote; locks 15 min before match; candidate list; reward/eligibility note; timestamp.

**Awards:** categories — Best Player, Best Goalkeeper, Best Young Player, Best Goal, Player of the Month, Top Scorer, Player of the Tournament, +competition-specific. Each card shows candidates, 13-Coin cost, deadline, reward, winning slots.

## Calculations

- Close: `Kickoff − 15 min` (server clock, not phone).
- Accept: `Server Time < Close ∧ Balance ≥ 13 ∧ No Existing Entry`.
- Balance after entry: `Opening − 13`.
- Correct: `Predicted Home = Actual Home ∧ Predicted Away = Actual Away`.
- Winner (limited slots): `Correct ∧ Rank ≤ Winning Slots` (rank by verified server submission time — earliest wins).
- Reward: 20 Coins if winner else 0. Net for a winner: `20 − 13 = +7`. **UI must show cost (13) and reward (20) separately — never "20 Coins profit."**

## Screens

PV-00 Guest/Eligibility Gate · PV-01 Predict & Vote Hub (Predict/Vote/Awards tabs; filters; fixture + voting cards showing type/teams/kickoff/cost/reward/slots/status/user-entry) · PV-02 Exact-Score Prediction (score selector + info panel + server countdown) · PV-03 Confirm Prediction (sheet: score, cost, before/after balance, reward, one-entry note, Pay 13 Coins) · PV-04 Prediction Submitted/My Pick (debit + timestamp + ref, Awaiting Match) · PV-05 MOTM/WOTM Selection (candidate list, FIFA-card portraits) · PV-06 Confirm Pick (sheet) · PV-07 Pick Submitted · PV-08 Awards Hub (trophy/glove/boot silhouettes) · PV-09 Award Candidates (Best Goal = playable clips) · PV-10 Insufficient/Locked/Already-entered states · PV-11 Match Live/Awaiting Resolution (oracle timeline, no early celebration) · PV-12 Result & Winners (win / not-correct / correct-outside-slots) · PV-13 Reward Credit Status (`1 Winning Entry ID = 1 Reward Credit`).

## Void/refund

Postponed before close: update times, notify, keep entry if identity unchanged. Postponed after close: void + refund 13 + reopen. Cancelled/abandoned: void, refund 13, wallet txn, notify. `Balance After Void = Current + 13`. Client-approval needed.

## Wallet & accessibility

Entry debit −13 / reward credit +20 / void refund +13, all on **Coins** (never Gold/Transferred Gold). A11y: labelled score steppers; score not colour-only; cost/reward readable pre-confirm; exact close time in countdown; locked status has text; candidate name/team/position labels; goal-clip captions; tabular numerals; 44×44; reduced-motion.

---
---

# Review — issues (journey unchanged)

## A — This is where the app becomes, mechanically, a gambling product

Pay 13 Coins → predict a real match outcome → win 20 Coins if correct. Combined with the confirmed economy (Coins bought with real money in J3, convertible to Gold, Gold withdrawable to cash), the full loop is: **real money in → stake on a sporting event → win → convert → cash out.** That is the definition regulators use for football-pools / prize-competition / fixed-odds products, and it carries licensing regimes (UK Gambling Commission and equivalents), mandatory age-verification, and responsible-gambling obligations in most markets. The "limited winning slots + earliest-timestamp priority + 13-in/20-out" structure reads like an attempt to frame it as a skill-based prize competition rather than a bet — but exact-score prediction is largely chance, so that defence is weak and jurisdiction-specific.

This is **the single biggest compliance item in the entire product** — larger than J3's money-transmission and J2's Fan Value. It's also **design-agnostic**: the screens look the same whether it ships licensed, geofenced, or reframed as free-to-enter. So I'll design it as concept per your standing "cross that bridge later," but flag clearly that the *mechanic* is licence-gated and needs a gambling-law opinion per market before any real launch. If it must ship unlicensed, the usual escape is **free entry** (no Coin cost) with prizes — which removes the "stake" and changes these screens' cost chips, not their layout.

## B–D — Agreeing with the doc's own recommendations (applied in the design)

- **B — Rename MOTM/WOTM "vote" → "Pick."** A vote that locks *before* kickoff is a prediction, not a vote. I've built it as "Who will be Player of the Match?" per the doc's own recommendation. (Real voting would need a post-match deadline.)
- **C — One paid entry per category/event.** Clearer and fairer than pay-to-vote-repeatedly, and it keeps a sporting vote from becoming a spending contest. Designed as one-per-category. (If multi-vote is intended, the UI must say "each additional vote costs 13 Coins" explicitly.)
- **D — "Correct but outside winning slots" must be foreshadowed at entry, not sprung at the result.** A Fan who predicts correctly and gets 0 (because they were 124th for 100 slots) will feel cheated if it's a surprise. The entry and confirm screens now show winning-slot count prominently, and PV-12 explains the rank neutrally. Cleaner alternative: drop the slot cap so every correct entry wins — recommend this unless payout cost forces a cap.

## E — Responsible-gambling scaffolding is missing

If classified as gambling/prize-competition, launch needs: per-user spend/velocity limits, self-exclusion / cool-off, verified 18+ (the J1 age gate helps but "16+" may be too low for a gambling product — likely 18+), and "play responsibly" messaging + helpline links in regulated markets. None appear in the journey. Flagging as a launch requirement contingent on classification.

## F — Net-not-profit honesty (built in)

The design shows entry cost (−13) and reward (+20) as separate lines and the net as +7 — never "20 Coins profit," per the doc's own warning.

## Consistency & theme

- **Currency:** correct — Coins only, explicitly not Gold. Consistent with the J3/J4 un-collapsed model.
- **Theme:** J5's spec asks for dark cinematic; per your standing instruction I built it **light**, keeping the photographic match/stadium imagery and team-colour splits as the "broadcast" liveliness inside the light frame.

No confirmation gate needed to build (nothing contradicts a locked decision; the gambling flag is the same standing "later" item). Built light with B/C/D/F applied and A/E recorded.