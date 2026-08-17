# Journey 15 — Fan Transfer & Loan

Moves a Fan between clubs, permanently or on loan. Connects MC-04 Fan List, MC-07 Approval Queue, G-03 Notifications. **Theme: LIGHT** (user-confirmed).

## The non-negotiable gate
`CanProcess = Cf ∧ Ao ∧ Ad ∧ E` — **Fan consent AND origin-Manager approval AND destination-Manager approval AND live eligibility.** Any false → move never completes. A Fan is a **member, never an asset.** No price tag, no "buy/sell/own/asset" language anywhere.

## Two move types
- **Permanent transfer** — Fan leaves current club, joins destination; active club changes; no auto-return. **Fan Value + Level + User ID + wallet + history all preserved.** Past participation stays historical; future eligible activity → new club.
- **Temporary loan** — Fan temporarily represents another club; defines origin/destination/start/end(or season)/return club/rules/early-return. **Auto-returns to origin at loan end.** Fan Value never reset at start or end; pre-loan activity stays with origin, loan activity → destination, post-return activity → origin. League results never retro-recalculated.

## No financial formula (deliberate)
No transfer/loan fee, no Coin/Gold payment, no commission, no club-to-club payment. This is a **membership reassignment, not a sale.** Do **not** reuse the J6 Player Transfer Market formula — that's for football players, not human Fans. If the client later adds money, it needs a separate escrow/settlement design.

## Two initiation routes
- **Route A — Manager-proposed:** Manager picks Fan → destination → Loan/Transfer → terms → sends offer (this records the initiating club's approval of *those exact terms*). Fan accepts/declines → other Manager approves → eligibility re-check → process → confirm all.
- **Route B — Fan-requested (ML-00):** Fan requests move → picks type + destination → submits with initial consent → both Managers review. If terms unchanged → process. If any term changes → **Fan must consent again.**

## Consent is version-locked
`ValidConsent = AcceptedTermsVersion == CurrentTermsVersion`. `TermsChanged ⇒ Consent Required Again`. A Manager can't change duration/destination after the Fan accepted and keep the old consent. Managers can never approve on the Fan's behalf. Only one active move per Fan. Rejection reasons mandatory for Managers; decline reason optional for the Fan.

## Screens built (light "Transfer Window")
ML-00 Request a Move (Fan route) · ML-01 Create Offer (Manager) · ML-01A Review & Send · ML-02 Fan Consent (loan) · ML-02P Fan Consent (permanent, "membership will end") · ML-02A Accept Confirmation (understanding checkbox) · ML-02D Decline Sheet · MC-07D Manager Approval Detail (light) · ML-03 Processing Tracker (match-event timeline) · ML-03A Permanent Transfer Complete (destination colour takeover) · ML-03B Loan Activated · ML-03C Loan Ending/Return · plus negative states (Terms Changed, Offer Expired, Fan Declined).

## Atomic processing
End/suspend origin membership · create destination membership · apply loan/permanent status · preserve User ID + Fan Value + Level · update active club · update both Fan Lists · update club-journey eligibility · notify · audit — **all together, or full rollback.** Fan never appears in both active rosters (unless the model explicitly supports parent+loan). "Accepted" ≠ "Moved" — no celebration until processing completes.

---
---

# Review — issues

## A — Consent is the spine, and the design makes it the visual focus (not a checkbox)
The whole journey exists to prove a Fan is a member, not merchandise. Built ML-02 as a full consent checkpoint: large Fan portrait between both crests, plain-language explanation, the **protection notice** ("You are a member, never owned or sold. You can decline."), a lime Accept and an **equally visible Decline**, plus "Ask Manager a Question" (opens chat without accepting). No celebration until processing completes — "Accepted" and "Moved" are visually different states.

## B — Version-locked consent is the anti-manipulation control, and it's built
`AcceptedTermsVersion == CurrentTermsVersion` is what stops a Manager quietly changing the loan duration or destination after the Fan agreed. Built the **Terms Changed** state that invalidates prior consent and forces a fresh Accept, with old-vs-new terms shown side by side. This is the single most important integrity rule in the journey.

## C — "Membership reassignment, not a sale" is enforced visually
No price tags, no market value, no cart, no bid, no "buy/sell/own/asset" wording. Completion is a **club-colour stadium takeover**, not a receipt. I deliberately did **not** reuse the J6 player-market treatment — that's for football players; this is a person. If the client introduces fees later, flagged that it needs its own escrow/settlement design (and a fresh consent surface).

## D — Loan return needs a real date, not the word "season"
"One season" cannot drive an automatic return — the system needs a configured season-end date. Built ML-03B/03C against an explicit **return date** with a live countdown and the 7-day / 1-day / on-return reminders. The auto-return preserves Fan Value and re-attributes future activity to the origin club without recalculating past league results.

## E — Route ambiguity resolved with two clear initiation paths
The docs contradict (ML-01 = Manager-proposed; MC-07 = Fan-initiated). Built **both**: ML-00 for the Fan route (records initial Fan consent up front) and ML-01 for the Manager route (sending records the initiating club's approval, so they don't re-approve unchanged terms). Both converge on the same approval + eligibility + atomic-processing pipeline.

## F — Atomicity & the "two active clubs" trap
Processing must be atomic with rollback — a mid-failure must never leave a Fan clubless. Built ML-03 as a multi-party match-event timeline where processing is a single committed step, and the Fan is never shown active in both rosters. Failure state says plainly "your club membership has not changed" + reference ID.

## G — Regulatory carry-over (light)
No money moves here, so this journey itself is low-risk — but it touches the same audit-log discipline as J13/J14 (terms version, consent timestamp, both decisions, rollback info per request). Real club identity keeps the licensing flag. Design-agnostic; concept stage.

## Theme
**LIGHT** Transfer Window — origin → Fan → destination composition, amber clock for loans, movement arrow for permanent, consent as a major checkpoint, destination-club colour takeover only after completion.
