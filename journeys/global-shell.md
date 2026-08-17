# Global Shell — Cross-Journey App Experience

The operating layer connecting all 19 journeys. Seven screens: G-01 Splash/Router · G-02 Nav Shell & Home · G-03 Notifications · G-04 Chat (=J19) · G-05 Profile/Settings · G-06 KYC · G-07 Support/Disputes. **Theme: LIGHT shell + DARK splash** (user-confirmed) — the shell stays visually *quieter* than Live Rooms/PK/rewards so the big journeys keep their impact.

## Canonical decisions (resolving the doc conflicts)

### Navigation — 5 tabs, no 6th Manager tab
`Home · Market · Stadium (elevated centre) · Games · Wallet`. A 6th "Club" tab would overcrowd. **Manager HQ is a shortcut** (Home header + Profile role card + club screens), never a tab. Floating detached glass pill, centre Stadium crest slightly elevated, labels always visible. Active tab highlighted; re-tapping scrolls to top; each tab keeps its last position for the session. **A Manager role never replaces the Fan experience; Host controls appear only during an active live session.**

### Entry router (G-01) — evaluate state, don't just wait
Order: min supported version → maintenance → validate session → onboarding completion → resolve roles → restore interrupted critical op → resolve deep link → open correct Home. **A deep link never bypasses authorization** — session is validated first, current entity state checked, user routed to the latest valid screen (if already completed, show final status, not an error). **Interrupted critical ops** (pending game result, wallet/escrow/withdrawal processing, live reconnect) open the **recovery state before any conflicting operation.** ~1–2s max, reduced-motion variant, branded error states.

### Additive roles (not "switch")
Profile shows **"Your Roles": Fan (permanent base) · Manager — Red Fury · Host (active only while live).** A user never "switches away" from Fan. Actions: Open Manager HQ / Start a Club / Go Live.

### Level label integrity
Progression measure shown as **"Level Points" (1,240 / 2,000)** — visually distinct from withdrawable wallet Gold, unless the client confirms Club Gold is an actual wallet currency. Wallet values and performance values are always visually separated.

### Guest
No fabricated Fan Value/wallet/rewards. **One persistent "Join SFL" banner + contextual gates** — never repeated disruptive registration modals. Top bar hides Coins/Chat/earnings.

## Notifications (G-03)
**Separate from private chat.** Categories: Club, Transfer/Loan, Prediction, Wallet/Payment, Rewards/Progression, Live/Social, Account/Security. Filters (All/Club/Money/Rewards/Live/Account), grouped Today/Yesterday/Earlier. `Unread = notifications with ReadAt = null`, synced across devices. **"Clear All" archives from view — it never erases payment/security/dispute records.** **Security/payment/withdrawal alerts are never treated as marketing and stay visible even when muted.** Outdated actions open the final detail, never fail silently.

## KYC (G-06) — gates withdrawal only
`CanWithdraw = KYC Approved ∧ Withdrawable ≥ 130 Gold ∧ Account Eligible`. **Not required to browse/join/do non-financial activity.** Intro → personal details → document type → capture (front/back/passport dynamically) → selfie+liveness → review → pending → approved/rejected. **Never just "Verification Failed"** — always the specific reason + which step + whether resubmission is allowed; attempt-limit routes to manual support. **Don't promise "approved in minutes."** Encrypted, short-lived signed doc access, no docs in logs, no public exposure, **no KYC upload via a generic support ticket.**

## Support/Disputes (G-07)
Categories (Account/Club/Payments/Market/Live/Verification/Technical). Transaction disputes **prefill the reference** (purchase/wallet/escrow/transfer/withdrawal/prediction/game-round/loan IDs) when opened from a transaction detail. Ticket statuses: Submitted → Open → Awaiting User → Under Review → Escalated → Resolved/Closed/Rejected/Duplicate. Resolution shows the **exact transaction reference** for any refund/correction, not just "Resolved." Drafts preserved on failure. **No full KYC documents through generic tickets.**

## Universal patterns
- **Permissions requested at first relevant use**, never all at onboarding (notifications/camera/mic/photos/bluetooth), each with SFL explanation → OS prompt → denied → permanently-denied/Open-Settings, continue-without where possible.
- **Connectivity:** offline banner (financial + live actions disabled, cached data visible) → reconnecting (auto-retry, drafts preserved) → synced. Stale data shows "Last updated HH:MM" + Refresh; wallet/game/approval state never shown as current when unverifiable.
- **Loading:** content-shaped **skeletons** for sections; full-screen only for routing, KYC submit, payment, wallet settlement, game-result recovery, transfer processing.
- **Errors:** general (Retry + reference ID), unauthorized, session expired (preserve deep link/draft), content removed, **action-already-completed (show the completed state, not a failure)**, concurrent change ("another Manager already processed this"), rate limited.
- **Success pattern:** what happened + amount/object + destination + new status + timestamp + **reference ID for financial/critical actions** + primary/secondary action. **Never rely on a green checkmark alone.**

## Screens built
G-01 Splash/Router (dark) · G-01X Router States (dark: update/maintenance/recovery) · G-02 Fan Home (light + nav pill) · G-02M Manager Home · G-02G Guest Home · G-03 Notifications · G-05 Profile/My Stats · G-05B Settings · G-05C Security & Devices · G-05E Delete Account · G-06A KYC Intro · G-06D Document Capture · G-06H KYC Approved · G-06I KYC Rejected · G-07A Support Hub · G-07D Ticket Detail · G-UNI Universal States (offline/skeleton/error/success).

---
---

# Review — key decisions & flags

## A — 5-tab nav with Manager HQ as a shortcut (resolves the 6th-tab conflict)
The docs disagreed (6th Club tab vs HQ shortcut vs 5 positions). Built **5 tabs + HQ shortcut** — a 6th tab overcrowds a 390px bar and a Manager role shouldn't reshape the whole app. Manager HQ appears in the Home header, Profile role card, and club screens.

## B — Additive roles everywhere (never "switch")
The prototype's "Switch anytime" contradicts the additive model used since J1. Profile shows **"Your Roles"** with Fan as the permanent base — you *add* Manager/Host, you never leave Fan. Consistent with J14/J19.

## C — Level Points ≠ wallet Gold
Labelled the progression bar **"Level Points"** so lifetime progression can't be confused with spendable/withdrawable Gold (the J12/J13 distinction). Wallet and performance numbers are visually separated on Profile.

## D — Router integrity: deep links never bypass auth, interrupted ops recover first
The router validates session before honouring any deep link and opens recovery states (pending withdrawal, game result, transfer processing) before letting a conflicting action start. This protects the money surfaces (J13) and the atomic operations (J15/J17) from being double-driven.

## E — Notifications: archive-not-erase, security always visible, separate from chat
Money/security/dispute notifications can't be muted away or wiped from the record; "Clear" archives the view only. Kept fully separate from J19 private chat.

## F — KYC gates withdrawal only + honest failure states
KYC isn't required to browse or join — only to withdraw. Every rejection names the reason/step (never bare "Failed"), and the privacy promises are conditioned on the real provider (no "approved in minutes", no docs in logs, no generic-ticket uploads). This is the AML/age surface tied to J13.

## G — Support prefills transaction references; resolution shows the real txn
Disputes opened from a transaction carry its reference automatically, and resolutions show the exact refund/correction transaction ID — not a vague "Resolved." Draft preservation on failure.

## H — Universal honesty: no fake-current data, success needs a reference
Offline disables financial/live actions and stale data is labelled "Last updated…"; success screens always carry a reference ID for financial/critical actions rather than a lone checkmark. This is the app-wide version of the honesty bar applied per-journey.

## Theme
**LIGHT shell** (Home/Profile/Settings/Notifications/Support/KYC) — quieter than the immersive journeys, club colour for club-scoped screens, gold=value, lime=progress, blue=info/nav, amber=pending, coral=failure. **DARK splash** — stadium tunnel, crest through floodlights, ~1–2s.
