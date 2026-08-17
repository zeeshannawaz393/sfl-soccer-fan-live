# Journey 2 — Join a Fan Club

Begins when a registered Fan wants to join an SFL Fan Club; ends when they become an active member and enter Club Home.

Two valid joining routes:

1. Fan applies voluntarily through Club Discovery or a recruitment link.
2. Manager invites a Fan using the Fan's permanent SFL User ID.

A Manager entering a User ID must never add someone immediately — it sends an invitation the Fan must accept.

## Core journey rules

- Guests can browse clubs but must register before applying.
- Every registered account is already a Fan.
- A Fan should have only one active Fan Club membership at a time.
- Applying to a club is voluntary.
- Manager approval completes a Fan-initiated application (the Fan already consented by applying).
- A Manager-initiated invitation requires explicit Fan acceptance.
- Joining through an invitation must not bypass consent.
- Managers cannot see a Fan's phone number or email.
- Club membership, Manager ownership and Host status remain separate role concepts.
- Loans and transfers are handled in Journey 15, not through a normal club-switch button.

## Screen inventory

**J2-01 — No Club / Join Club Entry.** Entry for a registered Fan without a club (from Clubs→My Club, Home widget, Profile, Get Started, or a club-required action). Heading "Find your Fan Club"; benefits (community, Squad Room access, Fan Tasks/rewards, league participation, manager/member comms). Primary: Discover Clubs. Secondary: Enter Recruitment Link. Optional: I have an invitation. States: happy · empty (no recommendations → Browse All / Update Interests) · restricted (under review/suspended → View Account Status) · offline (show cached, disable applying).

**J2-02 — Club Discovery.** Replaces direct club selection at onboarding. Tabs: My Club / Discover / League / Search / Notifications. Sections: Recommended for You (interests, favourite team, language, region, competitions) · Active Now (live rooms, matchday activity) · Open for Applications. Club cards: badge, name, manager, grade, league position, member count, monthly target progress, application status, active-room count, View Club. Card status labels: Applications Open / Closing Soon / Invitation Only / Applications Closed / Club Full / Application Pending / Member. States: empty recommendations · no clubs available (Notify Me / View League Table / Start a Club) · loading (card skeletons) · error (Try Again / Use Recruitment Link).

**J2-03 — Club Search & Filters.** Separate screen (keyboard changes the UI). Search by club name / club ID / manager name — a Fan's personal User ID is NOT searchable here. Filters: applications open, grade, region, language, member range, league position, live now, affiliation/interest. Results carry badge, grade, league position, member count, manager, application status. Recent searches shown before query. States: search empty ("No clubs match…") · no recent searches (show categories, not empty card) · invalid Club ID · offline ("Showing saved results. Connect to refresh").

**J2-04 — Recruitment Link Validation.** Brief resolver when opening a link from outside SFL. "Opening club invitation…" States: valid (auto-continue to Details) · not signed in (show preview, then Create Account / Sign In / Continue as Guest, then RETURN to same club) · expired · revoked · invalid · club deleted/suspended ("currently unavailable" — no internal reasons).

**J2-05 — Club Details / Recruitment Landing** (was jc-01). Hero: cover, badge, name, member/application status, region, established year, manager + verified status. Performance: grade, league position, member count, monthly target progress, recent form, active rooms. Community: description, languages, interests, live schedule, announcement preview, recent activity, member avatars. Application info: open/closed, capacity, manager review required, expected process (not a guaranteed SLA). Consent notice: "Joining is voluntary. Applying asks the Manager to review your request. You can withdraw while it is pending." Actions: Apply to Join / Preview Club Feed / View League Position / Back. States: open · application pending (→ Status/View/Withdraw) · already member (Enter Club) · already invited (Review Invitation) · club full (Notify Me / Similar Clubs) · applications closed (Follow / Others) · invitation-only (Follow) · member of another club (View Current / Leave / Transfer — no immediate switch) · manages another club (blocked, transfer/close first) · account restricted.

**J2-06 — Review Application.** Full screen or large sheet. Club summary, Fan avatar/name/SFL ID, current membership "No Active Club", receiving Manager. Privacy note: "The Manager will see your public profile, SFL User ID, Fan Level and relevant activity — not your phone number, email or wallet credentials." Optional "Why do you want to join?" (optional unless client wants questions). Checkbox "I understand the Manager will review my application." Actions: Submit / Cancel. Validation: consent unchecked · note too long · already submitted elsewhere · club closed/full while reviewing · network. Backend uses an idempotency key against double submission.

**J2-07 — Application Submitted** (was jc-02). Success illustration, "Application sent", club badge/name, timestamp, "Pending Manager Review". No 24/48h promise unless SLA enforced. Actions: View Application / Browse Live Rooms / Discover Others / Withdraw. Notification-failure copy: "Your application was submitted. Notification delivery could not be enabled; check Applications for updates."

**J2-08 — My Application Status.** Persistent tracker: club summary, reference, timestamp, status timeline (Submitted → Manager review → Decision), optional note, notification preference, manager profile link. States: pending (Withdraw; Message Manager only if pre-membership messaging allowed) · under review · approved (auto-route to Membership Confirmed) · rejected (→ Not Approved) · withdrawn (Apply Again if open) · auto-closed (explain outcome, not a "rejection") · loading/error ("Showing your last known application status").

**J2-09 — Withdraw Application Confirmation.** Sheet, not a destination. "Withdraw your application to Red District FC?" Explains manager can no longer approve, can reapply, no membership affected. Keep Application / Withdraw. Failure: already approved (membership started) · already rejected · network (keep state).

**J2-10 — Application Approved / Membership Confirmed.** "Welcome to Red District FC", role: Fan, manager, effective date, unlocked access (Club Home, Squad Room, Tasks, Feed, Rewards, chat). Actions: Enter Club / View Today's Tasks / Set Club Notifications. Good moment for the contextual notification prompt (in-app explanation before OS prompt). Partial-failure: "You joined the club successfully. Notification settings could not be saved." — do not roll back membership.

**J2-11 — Application Not Approved.** Respectful: badge, "Application not approved", date, manager reason if any, neutral note "Clubs manage their own capacity and criteria. This does not restrict your SFL account." Actions: Discover Others / Similar Clubs / Reapply if allowed / Contact Support (abuse/policy only). States: no reason ("The Manager did not provide a reason" — don't invent) · reapplication unavailable (Applications Closed + cooldown date + Follow) · club full ("reached capacity before your application was processed" — not a rejection).

**J2-12 — Club Invitation Notification.** In Notifications Center, deep-links to Details. Badge, "Red District FC invited you to join", manager, time, status (New/Expiring/Accepted/Declined/Revoked/Expired). Privacy: "Jay Malik used your SFL User ID to send this invitation." — don't imply phone access. Empty: "You don't have any club invitations." → Discover Clubs.

**J2-13 — Invitation Details / Accept or Decline** (was jc-03). Club info (badge, cover, name, grade, position, members, monthly target, manager, description, language/region, active rooms). Invitation info (sender, received, expiry, optional message, SFL ID used). Consent: "You will only become a member if you choose Accept." Actions: Accept / Decline / View Full Profile. States: active · already member (Enter Club) · member of another club (disable accept; Leave or Transfer first) · pending application elsewhere (accept only after confirm: "Accepting will withdraw your pending application to Blueview United") · expired · revoked · club full after invite (recommend: valid invitation reserves a place until expiry) · club suspended/deleted.

**J2-14 — Decline Invitation Confirmation.** "Decline Red District FC's invitation?" Optional reason (Already in another club / Not interested / Joined another / Prefer not to say), shared with manager only if disclosed. Keep / Decline. Result: marked Declined; Fan can still apply later unless policy prevents.

**J2-15 — Invitation Accepted / Membership Confirmed.** Reuses Approved screen with copy "Invitation accepted. You're now a member of Red District FC." Actions: Enter Club / Meet the Squad / View First Tasks. Race conditions (expired/revoked/unavailable/joined elsewhere/place lost): show exact reason, never a false success.

**J2-16 — Club Home — Member View** (was jc-04; matches existing Club Home design). Hero: cover, badge, name, member status, grade, league position, member count, manager + chat action. Monthly performance: target, current points, completion %, position, reward qualification. Primary: Enter Squad Room. Quick actions: Tasks / Live / Rewards / League Table / Club Chat / Member Directory. Feed: announcements, member posts, live alerts, task reminders, reward announcements, matchday discussion. Member actions: Chat Manager / Notification settings / Report / Leave Club. States: empty feed (don't leave blank) · no live rooms (show next scheduled) · no rewards (View Progress) · no daily tasks (show reset time) · target not configured · manager unavailable (keep functional; "Manager contact temporarily unavailable") · offline (cached; disable posts/chat/membership changes) · membership ended remotely (route to Membership Ended, don't leave a broken Home).

**J2-17 — Membership Ended.** Variants: left voluntarily / removed by manager / transfer completed / loan ended / club closed / club suspended. Content: previous club, effective date, reason where appropriate, what remains on account. Actions: Discover Clubs / View Transfer Status / Contact Support / View Wallet. No confidential moderation info.

**J2-18 — Leave Club Review.** Full screen (leaving affects many features). Shows membership duration, contribution, unclaimed rewards, active tasks, pending transfer/loan, Fan Value state. Consequence summary (recommended rules): wallet balances remain · owned players remain · Fan Level & history remain · Tasks/Squad Room access end · new club-point contributions stop · Fan Value freezes until requirement met again · pending loan/transfer resolved first · unclaimed rewards handling defined. Actions: Stay / Continue Leaving / Chat Manager. Blocked when: active loan/transfer processing · unsettled critical transaction · sole Manager · account review. Sole Manager must transfer/appoint/close via Manager journey, not the Fan leave flow.

**J2-19 — Confirm Leave Club.** "Leave Red District FC?" Checkbox "I understand I will lose access to this club's Squad Room, Tasks, Feed and member rewards." Optional reason. Actions: Leave Club (destructive) / Cancel. Fresh OTP not normally required (backend may require reauth on suspicious activity). Failure: already ended · transfer began elsewhere · data changed · network · server error. Never show success unless backend confirms.

**J2-20 — Left Club / No Club State.** "You left Red District FC", effective date, retained-asset summary, Fan Value status, reward/transfer notice. Actions: Discover / Explore Rooms / View Profile. Cooldown not defined — recommend none unless abuse appears; if added, show clearly.

**J2-21 — Fan Value & Player Value Callout** (was jc-05). Activates when: (1) Fan joined a club AND (2) completed first Coin purchase. Both done: "Fan Value and Player Value are now active." — W/D/L outcomes affect value; values are not wallet balances; Fan Value cannot be withdrawn directly. Actions: Activate Starting Value / Learn How Value Works. Partial states: joined but no purchase (Buy First Coins) · purchased but no club (Join a Club) · processing · error ("membership and Coins are safe").

**J2-22 — Guest Must Register.** Trigger: guest taps Apply / Accept / Enter Squad Room / Tasks / Chat. Club preview stays visible. "Create an SFL account to apply to Red District FC." Actions: Create Account / Sign In / Keep Browsing. Critical: after auth, RETURN to the same club and intended action — not a generic home.

## Cross-journey (belong to Journey 14, Manager Console)

Pending Applications · Application Review · Accept/Reject · Add Fan by User ID · Send Invitation · Invitation status · Fan List.

## State model

**Membership:** `none` · `application_pending` · `invitation_pending` · `active` · `transfer_pending` · `ended`
**Application:** `draft` · `submitted` · `under_review` · `approved` · `rejected` · `withdrawn` · `auto_closed`
**Invitation:** `pending` · `accepted` · `declined` · `expired` · `revoked` · `unavailable`

## Decisions requiring confirmation (journey recommendations)

1. One active membership per Fan — Recommended.
2. Pending applications — one at a time for MVP.
3. Invitation expiry — 7 days, configurable.
4. Invitation reserves capacity — yes, until expiry.
5. Club capacity — from platform config.
6. Rejection reason — optional for Manager, visible to Fan.
7. Reapplication cooldown — none initially.
8. Club-switch cooldown — none unless abuse.
9. Unclaimed rewards after leaving — remain claimable for a limited period.
10. Fan Value after leaving — freeze, not delete.
11. Managers joining other clubs — block while actively managing.
12. Pre-membership Manager chat — disabled until application/invitation exists.

---
---

# Review — issues found (journey above unchanged)

## The one that matters: Fan Value is a regulatory landmine (J2-21)

**Fan Value activates only after a real-money Coin purchase, and its worth then rises and falls with real match Win/Draw/Loss outcomes.** That specific combination — pay real money → hold an asset → asset value moves on the outcome of a real sporting event — is the textbook definition regulators use for gambling/financial-speculation products. Sorare is fighting exactly this fight with the UK Gambling Commission over the same mechanic, and Sorare at least never gated activation behind a mandatory purchase. Three things compound the risk:

- **Mandatory purchase to unlock progression** reads as a paywall on a core system and, combined with outcome-linked value, is close to "pay to play a game of chance."
- **"Player prices" that move** turns members into tradable assets whose price you can speculate on — the design direction's §20 explicitly says *don't* treat fans as tradable footballers; J2-21 does exactly that for the value layer.
- **"Cannot be withdrawn directly"** is the standard fig leaf, but if value ever converts to anything of worth (rewards, status, resale), regulators look through it.

I know the standing instruction is "cross that bridge when we get there" — but this isn't a visual-polish bridge, it's load-bearing on the data model and the monetization. My recommendation: **decouple activation from the purchase** (activate Fan Value on club membership alone), and **decouple value from match outcomes** (drive it off participation — attendance, contribution, streaks — not W/D/L). You keep the progression hook and the football texture without the gambling surface. If the client insists on outcome-linked, purchasable value, it needs a legal opinion per target market *before* it's designed, not after. Flagging as **BLOCKER-level for J2-21 only** — the other 21 screens are unaffected and can proceed.

## Consistency flags (quick to fix)

- **F1 — Coins vs Gold.** Journey 1 (confirmed v2) locked the currency name as **Gold**; J2-21 says "Coin purchase / Buy First Coins" throughout. Normalize to Gold everywhere.
- **F2 — Weekly vs Monthly club target.** Design direction §11/§32 defines a **weekly** club mission (the thing fans see on Club Home and owners set in Club Studio). J2-02/J2-16 introduce a **monthly target** with "monthly reward qualification." Pick one cadence, or define both explicitly (e.g., weekly missions + a monthly league target) so the Club Home doesn't show two competing progress systems.
- **F3 — Grade vs Level.** Journey uses "Club grade"; §11 uses "Level or league." One term.
- **F4 — "I have an invitation" (J2-01) vs push invitations (J2-12).** J2-12 says invitations arrive in the Notification Center via SFL ID. So what does the J2-01 "I have an invitation" button do — enter an invite *code*? If invitations are ID-targeted and pushed, there's no code to enter. Either add an invite-code mechanism or drop that entry point and route people to Notifications.

## Product recommendations (take or leave)

- **R1 — Reconsider "one pending application at a time" (decision 2).** It's the safe MVP choice, but it throttles the top of your funnel: a Fan applies to one club, waits days for a manager who may never respond (you explicitly refuse to promise an SLA), and churns. Recommend **allow multiple simultaneous applications, but only one acceptance** — the first approval the Fan accepts auto-withdraws the rest. Keeps the "one membership" rule intact while letting Fans hedge against slow managers.
- **R2 — Auto-close stale applications.** With no manager SLA, applications can sit in `submitted` forever. Add a Fan-visible expiry ("applications expire after 14 days if not reviewed") so `auto_closed` isn't a mystery state.
- **R3 — Invitation capacity reservation (decision 4 = yes) can be gamed.** A manager could fire invitations at many Fans to hold seats hostage. Cap concurrent outstanding invitations per club, or only reserve on the Fan's *first open* of the invitation, not on send.
- **R4 — Pre-membership Manager chat: agree it's disabled (decision 12),** but J2-08 still lists "Message Manager" as a pending-state action. Remove it from J2-08 to match, or the two contradict.
- **R5 — Leaving and the club's Weekly Mission (§32).** When a Fan leaves mid-mission, their contribution to the club's collective progress bar needs a defined rule (retain vs. subtract). J2-18 covers the Fan's assets but not the club's shared state. Recommend: contributions already made stay counted; the member just stops adding.

## What's genuinely strong (so it's on record)

The consent architecture (application = consent, invitation = requires acceptance, ID-based invite never auto-adds), the "return to the same club after auth" rule (reinforces Journey 1's A3 deep-link flag), the idempotency key, the separation of Manager operations into Journey 14, and the three state-model tables are all correct and implementation-ready. J2-16 also fully specs the Club Home member view — it supersedes the thinner design-direction §11 sketch and is what the Club Home screen (backlog task #1) should be built from.

## Decision recommendations (on your list of 12)

Agree as written on 1, 3, 5, 6, 7, 8, 9, 10, 11. Change 2 (→ multiple applications, single acceptance, per R1). Confirm 4 with a cap (per R3). Confirm 12 and fix the J2-08 contradiction (per R4). Plus the currency-name and target-cadence normalizations (F1, F2) and the J2-21 decoupling above.

---
---

# Confirmed model (v2) — all recommendations accepted

**J2-21 Fan Value — decoupled (removes the gambling surface):**
- Fan Value activates on **club membership alone** — no mandatory Gold purchase gate.
- Value is driven by **participation** (attendance, contribution, streaks, tasks completed), **not** by match Win/Draw/Loss outcomes.
- Members are never priced or traded as assets; "player prices that move on results" is dropped.
- Fan Value is a status/progression signal, not a wallet balance, and is not withdrawable.
- On leaving a club, Fan Value **freezes** (not deleted) until membership resumes.

**Currency (F1):** the currency is **Gold** everywhere. All "Coins" copy is replaced.

**Club target cadence (F2):** one progress model on Club Home to avoid competing bars —
- **Weekly Club Mission** (§32) is the prominent, owner-set collective progress bar.
- **Monthly** frame is expressed only as **League position / points** (standings), not a second progress bar.

**Terminology (F3):** the club's own tier is **Club Level**; the competition it plays in is its **League**. "Grade" is retired.

**Invitation entry (F4):** invitations arrive two ways only — **ID-targeted push** (Notifications → J2-13) and **recruitment links** (J2-04). The ambiguous "I have an invitation" code button is **dropped**; J2-01 keeps Discover Clubs + Enter Recruitment Link.

**Applications (R1, R2):** a Fan may hold **multiple simultaneous applications**; accepting one (or an invitation) **auto-withdraws the rest**. The one-active-membership rule is unchanged. Applications **auto-expire after 14 days** if a manager never reviews them (Fan-visible), surfacing as `auto_closed` with a clear reason.

**Invitations (R3):** an active invitation reserves a place **until expiry (7 days)**, but concurrent outstanding invitations per club are **capped** to prevent seat-hoarding.

**J2-08 fix (R4):** "Message Manager" is **removed** from the pending application state (pre-membership manager chat stays disabled per decision 12).

**Leaving mid-mission (R5):** contributions already made to the club's Weekly Mission **stay counted**; the departing member simply stops adding new progress.

**Club-switch / reapplication cooldowns:** **none** (decisions 7, 8) unless abuse appears.
**Unclaimed rewards after leaving:** remain claimable for a **limited period** (decision 9).
