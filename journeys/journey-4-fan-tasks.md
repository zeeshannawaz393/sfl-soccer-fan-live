# Journey 4 — Fan Tasks & Duties

Turns normal SFL participation into a structured daily/weekly retention loop: Fan sees today's duties → understands the exact qualification rule → opens the relevant journey → server verifies the qualifying action → progress updates → all required tasks complete → completion reward becomes claimable → Coins or earned Gold credited → My Stats / Fan Level / club contribution update.

## Original documented scope

FT-01 Tasks Hub (Daily/Weekly) · FT-02 Task Detail · FT-03 Daily Completion Reward Claim · FT-04 My Stats. These four require additional states/overlays to cover the journey fully.

## Values NOT locked (must be server-configured)

- Number of daily/weekly tasks (spec example 3/6; old prototype 3/5).
- Reward amounts (prototype shows 40 Gold — mockup only, not a business rule).
- Reward currency (Coins or Gold).
- Reset time and qualifying thresholds.
- Recruited-Fan "eligible" definition (verified/age/non-fraud) — configured centrally, not by UI.
- Claim grace period.

## Roles (additive)

Fan / Manager / Host: full access (Manager & Host are additive Fan roles). Guest: no participation, registration gate. Suspended/restricted: per restriction rules. Club membership doesn't block all tasks, but club-specific tasks lock until joined.

## Task status model

`Locked` · `Available` · `In Progress` · `Verifying` · `Complete` · `Claimable` · `Claimed` · `Expired` · `Unavailable` · `Restricted`.

**Formulas:**
- Task progress: `min(Current/Target, 1) × 100` (e.g. 18/20 min = 90%).
- Daily progress: `Completed Required / Total Required × 100` (e.g. 3/6 = 50%). Optional tasks don't block the reward unless marked Required.
- Reward claimable: `All Required Complete ∧ Not Previously Claimed ∧ Within Claim Window`.
- Coin reward → Coin balance. Gold reward → **earned Gold** (not Transferred Gold).

## Task catalogue

Recruit eligible Fans · Buy 2 players · Sell/release 2 players · Watch SFL YouTube (~20 min/day) · Go Live · Participate in PK · Make predictions · Submit votes (MOTM/WOTM) · Maintain active days · Daily challenge · Weekly challenge. Each has a photographic football identity (broadcast thumbnail for Watch, player card for Market, live crowd for Go Live, scoreboard for Predictions, split-screen for PK, streak flame for active days).

## Screen journey

- **FT-00 Guest Gate** — "Join SFL to Complete Fan Tasks"; benefits; Create Account / Sign In / Keep Exploring. Locked mission card, gold reward preview behind lock, no fake progress.
- **FT-01 Tasks Hub: Daily** — title "Fan Tasks / Today's Duties"; Daily/Weekly tabs; hero **progress ring** (3/6, 50%); reward preview ({amount} Coins/Gold); reset countdown; CTA (Continue / Claim / Claimed). Task rows: icon/thumbnail, title, one-line requirement, current/target, progress bar, reward chip, deadline, Required/Optional marker, status, deep-link action. States: none started · partial · all complete · claimable · claimed · reset approaching · offline cached · verification pending · no tasks configured · club tasks locked · restricted.
- **FT-02 Tasks Hub: Weekly** — tab state, more campaign-oriented: weekly progress (4/8), week range, reset (2d 06h), weekly reward preview, milestone strip (25/50/75/100%), weekly tasks. Club crest/colour wash where a task contributes to the club. Trophy treatment at 100%. States: week started · in progress · milestone reached · all complete · claimable · claimed · expired · unclaimed expired · none configured.
- **FT-03 Task Detail** — back, task type, status pill; hero varies by type (real thumbnail); requirement section (what to do, exact qualifying rule, what doesn't count, start/end, count, daily/weekly); reward section (amount, Coins/earned Gold, contributes to daily/weekly/Fan Level/club points); progress (current/target/%/last update/verification); primary CTA (Watch Now / Open Market / Predict / Vote / Go Live / Enter PK / Invite / Continue); secondary (How Progress Is Counted / Set Reminder / Report Missing Progress).
- **FT-04 Locked Task Detail** — state of Detail. Reasons: no club (→ Discover Clubs) · no Coins (→ Buy Coins) · Fan Value inactive (→ Review Activation) · live eligibility (→ View Requirements) · player prerequisite (→ Open Market). Prerequisite as a short stepper; lime only on the resolving action.
- **FT-05 Task Progress Verification** — "Checking Your Progress"; task, action detected, time, verification ref; "activity recorded, progress updates after verification"; Check Again / Continue with Others / Report. VAR-style. States: pending · verified · rejected (non-qualifying) · duplicate · delayed · network. Don't show task incomplete while verification pending.
- **FT-06 Individual Task Completed** — "Task Complete", title, 100%, reward/contribution, updated daily progress (4/6), remaining (2 left); Continue Tasks / View Progress. Compact celebration, auto-return to Hub. If not separately claimable: "This task now counts toward your daily completion reward."
- **FT-07 All Daily Tasks Complete** — trigger `Completed Required = Total Required`. "Daily Duties Complete"; ring 6/6; reward; completed summary; Claim Reward / View Completed. Full stadium, celebrating fans, match-win presentation.
- **FT-08 Confirm Reward Claim (sheet)** — "Claim Daily Reward"; amount+currency; destination (Coin Balance / Earned Gold); current+new balance (e.g. 860 + 40 = 900 Gold); period; claim ref; Claim 40 Gold / Not Now. No ambiguity between Gold and Transferred Gold.
- **FT-09 Reward Claim Processing** — "Crediting Your Reward"; stages (completion verified → claim registered → wallet credit); amount, reward ID; "don't claim again". Rule `1 Reward Instance ID = 1 Wallet Credit`. No second Claim button; Continue in Background.
- **FT-10 Reward Claimed** — "Reward Claimed", +amount Coins/Gold; previous/credited/new balance; updated Fan Level & club contribution; claim ref; Done / View Wallet / View My Stats. If Gold, label **Earned Gold**.
- **FT-11 My Stats** — (fulfils FT-04) real avatar, name, User ID, club+crest, Fan Level, Fan Value, level bar. Metrics: active days · live-stream hours · tasks completed · predictions · club points · Fan Level · Fan Value · players transferred. Player-career-card presentation, club-colour wash, FIFA-attribute styling. Actions: task history · reward history · Wallet · Fan Level · Fan Value · share public stats. States: new/no stats · no club · Fan Value inactive · partial unavailable · offline · private.

## Empty/error/exceptional

No active tasks · tasks reset ("A New Task Day Has Started") · unclaimed reward expired (claim window — grace period client-configured) · progress not updating (still syncing) · reward claim failed (completion recorded, retry without repeating tasks) · already claimed (load original claim, not an error) · offline (cached, last-updated, network actions disabled, no claim attempted) · account restriction (show restricted activities without hiding earned claimable rewards).

## Navigation deep-links

Buy Coins → J3 · Join club → J2 · Recruit → referral flow · Buy/sell players → J6 · Watch YouTube → J18 · Go Live → J7 · PK → J9 · Predictions/votes → J5 · Rewards history → J16 · Wallet → J13 · Fan Value → J11 · Fan Level → J12. Destination journeys return the Fan to the task or update it automatically.

---
---

# Review — notes (journey above unchanged)

Journey 4 is internally consistent and reuses prior primitives cleanly (guest gate, server-verify-before-credit, idempotency `1 Reward Instance ID = 1 credit`, deep-link-and-return). A few things to align with what we've already locked:

**R1 — Currency wording is now correct here and confirms the two-currency model.** Journey 4 correctly separates **Coins** and **Gold**, and crucially adds a third distinction: task rewards go to **earned Gold**, kept separate from **Transferred Gold** (peer-received) — so Gold itself has sub-buckets. This validates the R1 fix from Journey 3 (Coins vs Gold are distinct) and refines it: the wallet has at least Coins, Earned Gold, and Transferred Gold. The design must never blur these (FT-08 explicitly warns about it). Carry this into the Wallet journey (J13).

**R2 — "Watch SFL YouTube ~20 min/day" and referral tasks carry policy weight.** Rewarding watch-time on an external platform (YouTube) with in-app currency, and rewarding recruitment with currency, are both incentivized-action patterns that (a) YouTube's own terms restrict (paying for views/watch-time violates YouTube policy), and (b) referral-for-currency can trip promotion/lottery rules in some markets. Flagging as a compliance check, not a design blocker — the *screens* are fine; the *mechanic* needs review. Recommend the "eligible referral" definition (already noted as server-side) explicitly excludes paying purely for a signup.

**R3 — Reward currency is server-configured, so every reward surface must render both Coins and Gold gracefully.** The spec is right to keep amount/currency dynamic. Design implication: the reward chip, claim sheet, and success screen all need a Coins variant and a Gold variant (gold coin glyph vs gold bar/ingot), and the claim destination label must switch between "Coin Balance" and "Earned Gold." I'll build both variants.

**R4 — Fan Value on My Stats stays consistent with the J2/J3 decoupling.** FT-11 shows Fan Value as a metric — fine. FT-04's "Fan Value inactive → Review Activation" lock should point to the *free* membership activation (not a paid gate), per the confirmed model.

**R5 — Theme:** Journey 4's spec asks for dark cinematic. Per standing instruction, I'll build it **light**, keeping the football-photographic task identities (broadcast thumbnail, player card, scoreboard, etc.) as the liveliness — imagery does the cinematic work inside the light frame. Progress ring as hero, gold for rewards, green for completion/actions, coral for expiry/LIVE.

## Confirmed build set

Given nothing here contradicts a locked decision (unlike J3), no confirmation gate needed. Building light, with both Coins and Gold reward variants shown, progress-ring hero, photographic task rows, and the full state coverage (guest gate, daily hub, weekly hub, task detail, locked detail, verification, task-complete, all-complete, claim sheet, claim processing, claimed, My Stats, plus key empty/error states).