# Journey 14 — Manager Console / Club Management

The club's operational command center — "The Dugout Command Center." A Manager monitors performance, recruits Fans, manages membership, claims rewards, and processes transfer/loan requests. Must feel like a manager's dugout, not a corporate admin panel. **Theme: DARK** (confirmed by user, overriding the light-chrome default for this journey).

## Seven required screens
MC-01 Manager Dashboard · MC-02 Recruit Fans · MC-03 Daily Reward Center · MC-04 Fan List · MC-05 Fan Applications · MC-06 Add Fan by User ID · MC-07 Transfer/Loan Approval Queue. (MC-00 selector + the detail/confirm sheets are supporting.)

## Role & permission rules
A Manager is still a Fan; the role is added on creating/being authorized for a club. Server-side role checks gate every Manager screen. **Invitation ≠ auto-add — the Fan must accept.** Fans are never owned or sold. Loans and permanent transfers require Fan consent. Managers see club-related Fan performance but **not private wallet balances, KYC, email, passwords, or private chats.** Every accept/reject/remove/reward/transfer/loan decision is written to an **audit log**. Multi-club Managers get a **club selector (MC-00)** before the console.

## Commission (three tiers)
Tier 1 = 4% · Tier 2 = 7% · Tier 3 = 11%. `Commission = Qualifying Fan Coin receipts × Rate`. **Recommendation (built to this): Fan receives their full amount; commission is separately platform-funded into the CLUB WALLET — it never silently reduces the Fan's displayed reward.** Undefined & flagged: which receipts qualify, settlement cadence, tier-movement trigger, rounding.

## Monthly club target
Prototype 940/1000 = 94%. **Unit is app-controlled — must NOT be labelled Coins** unless confirmed. Manager must be able to open the card and see exactly which activities contributed (MC-01B). Built the unit as an explicit, named "Club Points" placeholder with a contribution breakdown.

## Daily recruitment target
Prototype 5 Fans/day → 50 Coins, example 3/5 — all backend-controlled. A recruit counts **only** when the Fan is unique, accepts, membership is created, and anti-abuse passes. Link clicks & unfinished applications never count.

## Screens built
MC-00 Club Selector (Manager HQ) · MC-01 Dashboard (wallet/commission/fans/position + monthly target + recruitment snapshot + shortcuts) · MC-01A Commission Detail (tier, next-tier progress, settlement, "Fans' earnings not reduced") · MC-01B Monthly Target Breakdown (contributions + daily chart, named unit) · MC-02 Recruit Fans (daily target, link as match-ticket, QR, 7-day chart, attribution) · MC-02A Recruitment Share Sheet ("apply/accept," never "instantly added") · MC-03 Daily Reward Center (Claimable/Locked/Claimed tabs, "Claim to Club Wallet") · MC-04 Fan List (squad roster, filters, privacy boundary) · MC-04A Fan Performance Detail · MC-04B Remove Fan Confirmation (reason required) · MC-05 Fan Applications (scouting cards, accept/reject + reason sheet) · MC-06 Add Fan by User ID (invitation, consent copy above button, amber pending) · MC-07 Transfer/Loan Approval Queue (origin→Fan→destination, three-step consent tracker, Approve disabled until Fan consent).

---
---

# Review — issues

## A — "Invitation, not acquisition" is the ethical spine, and the UI enforces it
Fans are people, not assets. The whole journey is built so a Manager can *invite* but never *add* — MC-06 shows the consent line directly above the Send button and returns an **amber "Awaiting Fan" clock, not a success check**; MC-07 **disables Approve until Fan consent is received** ("Awaiting Fan Consent"); recruitment copy says "apply/accept," never "opening the link adds you." This is correct and I've kept it visually unambiguous.

## B — Commission funding model is the one big money question (built to the safe default)
Whether commission is **platform-funded (additive)** or **deducted from the Fan** is a product+compliance decision. I built the recommended additive model — Fan keeps 100%, commission lands in the **club wallet** — and MC-01A states "Your Fans' displayed earnings are not reduced." If the client instead wants it deducted from Fans, that changes the Fan-facing reward screens across J3/J4/J8/J10 and needs an explicit call. Also undefined: qualifying receipts, settlement cadence, tier-movement rule, rounding — rendered as server-controlled placeholders, not invented numbers.

## C — The monthly-target unit must be explained, not just metered
A lone 940/1000 meter is not enough (the spec says so). Built MC-01B with a **named unit ("Club Points"), contribution categories, and a daily chart** so the Manager can see how the number was produced. The unit label is a placeholder pending the client's definition — deliberately **not** "Coins."

## D — Privacy boundary is real and load-bearing
Managers see club-relevant performance (Fan Value, live hours, players transferred, active days, level) but **never wallet balances, KYC, email, credentials, or private chats**. Fan List and Fan Detail are built to that line. This matters because the Manager role is powerful — the boundary is what keeps it from becoming surveillance.

## E — Two open policy gaps flagged, not invented
1. **Does Manager removal require Fan consent?** Loans/transfers definitely do; removal is unclear. Built MC-04B as a **reason-required Manager action that notifies the Fan and preserves their account + historical Fan Value**, but the consent rule and what happens to the Fan's seed/club association need the client's answer.
2. **Withdrawals are NOT in the approval queue.** The prototype had a Withdrawals tab; the documented requirement only authorizes **transfer/loan** approvals. Wallet withdrawal stays in J13 (wallet/KYC) unless the client explicitly grants Managers approval authority. Built MC-07 with Transfers/Loans/Completed/Rejected only.

## F — Regulatory carry-over
Manager commission is real money moving on defined rules → sits on the same money-transmission/e-money surface as J13, and the audit-log requirement is exactly the AML scaffolding that surface needs. Real club/competition identity keeps the licensing flag. Design-agnostic; concept stage.

## Theme
**DARK dugout command center** (user override). Club-colour header lighting, scoreboard numerals, Gold = value/rewards, Lime = approval/progress, Amber = pending consent, Coral = rejection/destructive. Fan cards as scouting cards; recruitment link as a digital match ticket; transfers as origin→Fan→destination cards.
