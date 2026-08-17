# Journey 1 — Onboarding, Registration and Sign-in

## Core role rule

Users must not choose Fan or Manager during registration.

- Everyone who registers becomes a Fan.
- A Fan becomes a Manager after creating a club.
- A Fan becomes a Host only while running a live session.
- A Guest has no account and can only browse.
- A registered Fan without a club can still explore the app.

---

## New account flow

### 1. Splash and Entry Router

**Purpose:** Determine where the user should be sent.

Content: SFL logo · subtle stadium-light or live-signal animation · loading indicator.

Behind-the-scenes checks:

- Is the user already signed in?
- Is onboarding complete?
- What was the last completed onboarding step?
- Is the app version supported?
- Is the device online?
- Is the account suspended or restricted?

Routing:

- No session → Welcome
- Incomplete registration → Resume the incomplete step
- Completed session → Live Discovery
- Guest session → Limited Live Discovery

States: Loading · Offline with `Try Again` · Maintenance · Mandatory app update with store link · Session expired.

### 2. Welcome

**Purpose:** Present the product and three entry paths.

Content: cinematic football-fan hero · SFL logo · headline such as *"Your club. Your stage. Game on."* · short proposition: *"Join fan communities, watch live reactions, take a position and experience matchday together."*

Actions: `Create Account` · `Sign In` · `Explore as Guest`

Guest explanation: *Browse live rooms and clubs. Create an account to join rooms, participate, predict, send gifts or start a club.*

This screen must not ask whether the user is a Fan or Manager.

### 3. Create Account — Phone Number

**Purpose:** Begin identity verification.

Content: country selector · country code · phone-number field · explanation (*"We'll send a verification code to this number"*) · Terms and Privacy links · minimum-age notice · existing-user link (*"Already have an account? Sign in"*).

Primary action: `Continue`

Validation and states: invalid phone number · unsupported country · number already registered → offer `Sign In` · too many verification attempts · unable to send code · network error.

The phone number should never be publicly displayed to other members.

### 4. OTP Verification

**Purpose:** Confirm ownership of the phone number.

Content: six-digit OTP input · masked phone number · `Edit Number` · resend countdown · note that the code may be detected automatically.

Actions: `Verify` · `Resend Code` · `Change Number`

States: sending · code sent · wrong code · expired code · resend available · too many failed attempts · temporarily locked.

Successful result: continue to the age gate.

### 5. Age and Eligibility

**Purpose:** Enforce the platform's minimum-age policy.

Content: date-of-birth selector · explanation (*"Your date of birth is used to confirm eligibility and will not appear publicly"*) · Terms/age-policy link.

Primary action: `Continue`

States: valid and eligible · invalid date · future date · under the required age · date could not be verified.

Underage result: a dedicated blocked state explains that the user cannot create an account, without accusing them of fraud. The minimum age should be configurable by country rather than hard-coded into the interface.

### 6. Create Password — Conditional Screen

The current prototype registers users through OTP but later expects them to sign in with a password without ever asking the user to create one. If password sign-in is retained, this screen is required.

Content: create password · confirm password · show/hide · strength indicator · requirements (minimum length, upper/lowercase, number, special character if required).

Primary action: `Create Password`

Alternatively, SFL can use phone OTP for every sign-in and remove passwords and password-recovery screens entirely.

Recommendation from the journey: allow returning users to use either their password or a phone verification code.

### 7. Profile Setup

**Purpose:** Create the user's public social identity.

Content: profile photo · display name · unique username · optional bio · optional favourite real-world team · country or fan region if relevant.

Required: display name, unique username. Optional: photo, bio, favourite team.

Actions: `Continue` · `Skip Photo`

Validation: username already taken · unsupported characters · inappropriate name · image upload failure · image size/type error.

Camera and photo permissions are requested only after the user taps `Add Photo`.

### 8. Football Interests — Optional

Replaces/redefines the current `Pick Your Club` onboarding screen. The existing prototype lets users select an SFL Fan Club directly, but the Club Journey requires membership by application or accepted manager invitation — those rules conflict.

**Recommended purpose:** personalize discovery without making the user a club member.

Content: "What do you follow?" — favourite teams, leagues, competitions, national teams; content preferences (match reactions, transfer talk, club discussions, predictions, live debates).

Actions: `Continue` · `Skip for Now`

This selection only personalizes Live Discovery and Matchday. It does not join the user to an SFL Fan Club. For a shorter MVP onboarding this can merge into Profile Setup.

### 9. SFL User ID Reveal

**Purpose:** Explain the permanent ID used for financial and club actions.

Content: celebration message (*"You're in!"*) · large SFL User ID · copy button · share button · explanation of uses (managers can invite you to a club; fans can transfer Gold to you; support can locate your account; the ID can identify transactions).

**Important recommendation:** the current requirement generates the ID from the first two and last three phone digits (`12XXXXXXXX345 → 12345`). This must change because a five-digit value is not globally unique, different users can collide, it exposes part of the phone number, it eases account enumeration, and a phone-number change would create identity problems.

Use a server-generated permanent ID instead (e.g. `SFL-847291`, `R7K-42M`, or a unique 8–10 digit number). The social username and the transactional SFL ID remain separate.

### 10. Choose How to Start

**Purpose:** Route the registered Fan toward their first meaningful action.

Headline: *How do you want to start?* Supporting copy: *Everyone starts as a Fan. You can join a club, create your own, or explore first.*

- **Option A — Join a Club:** discover fan clubs · apply voluntarily · enter club communities · complete duties and earn rewards. Route: Club Discovery → Club Details → Apply to Join.
- **Option B — Start a Club:** create a club · choose identity and colours · become its Manager · recruit and manage Fans. Route: Create Club Journey.
- **Option C — Explore for Now:** browse live rooms · follow Matchday · discover clubs · complete membership later. Route: Live Discovery as a registered Fan without a club.

The Option C user is not a Guest — they have an account and the base Fan role without a club.

---

## Returning-user flow

### 11. Sign In

Content: phone number or email · password · show/hide · `Forgot Password?` · `Sign In` · optional `Send me a login code` · Apple/Google sign-in only if fully implemented · link *"New to SFL? Create an account"*.

States: incorrect credentials · account not found · temporarily locked · suspended · onboarding incomplete · network error.

Routing after sign-in: onboarding incomplete → resume last step · Fan without club → Live Discovery with `Join a Club` prompts · club member → personalized app · Manager → app with Club Studio access · suspended/restricted → account-status screen.

On mobile, "Remember me" is unnecessary — a secure session remains active by default.

---

## Password-recovery flow (only if password login remains)

### 12. Forgot Password

Phone number or email · recovery-process explanation · `Send Verification Code`. States: account not found · code delivery failed · too many requests.

### 13. Recovery Verification

Six-digit code · masked phone/email · resend countdown · change recovery method. States: wrong code · expired code · too many attempts.

### 14. Create New Password

New password · confirm · strength and requirements · `Update Password`. Completion: password updated · other sessions optionally signed out · return to Sign In or enter the app automatically.

---

## Exception and blocked states

### 15. Account Access Block

The current project combines duplicate accounts, fraud signals and underage users into one screen. These should be separate variants:

- **Number Already Registered** — account exists · `Sign In` · `Recover Account`
- **Underage** — age ineligibility · no route into the app · privacy/support link
- **Security Review** — registration could not complete · reference number · `Contact Support` · never expose fraud-detection details
- **Suspended Account** — reason category where legally appropriate · appeal/support option · sign-out action

---

## Decisions to confirm (from the journey)

1. Authentication method: OTP-only, password-based, or both?
2. User ID generation: replace the phone-derived five-digit ID with a server-generated permanent ID.
3. Club selection during onboarding: remove direct SFL club selection; membership happens via the application/invitation journey.
4. Registered "Explore" users remain Fans without a club — not Guests.
5. Social sign-in: only show Apple and Google if both creation and sign-in are fully supported.
6. Permissions: notifications, camera and microphone requested contextually, not during onboarding.

---
---

# Review — issues found and additions (on top of the journey, nothing above changed)

## A. Flow-level issues

**A1. Age gate ordering.** DOB is collected *after* OTP (step 5 after step 4), which means the platform has already collected and verified a minor's phone number before discovering they are ineligible — a data-protection problem (GDPR/child-data) and wasted SMS spend. Move the age gate before the OTP send: either ahead of the phone screen or as a DOB field on it. On underage, nothing has been stored except a transient form value.

**A2. Ten steps is a heavy funnel.** Recommended compressions, none of which lose a requirement: merge Football Interests into Profile Setup (already allowed for MVP); make the SFL ID Reveal a dismissible celebration sheet on top of "Choose How to Start" rather than its own step; skip Create Password entirely at registration (see D1). Target: Welcome → Phone+DOB → OTP → Profile (with interests) → Choose How to Start, with the ID sheet overlaid. Five steps.

**A3. Deep links must survive the funnel.** The Entry Router routes to generic destinations, but the most common growth entry is a shared room/club/match link. The router must carry the intended destination through registration or guest browsing and land the user there afterwards. Without this, every shared link converts into a cold Discovery landing.

**A4. Email appears at sign-in but is never captured.** Screens 11–13 offer "phone number or email," but registration collects no email. Either drop email from sign-in/recovery, or add an optional "recovery email" prompt after onboarding (recommended — see A5).

**A5. Phone-number recycling is the real recovery risk.** With OTP-first auth, a user who loses their number (carriers recycle numbers aggressively in many markets) loses the account — and worse, the number's new owner can OTP into it. Mitigations: optional recovery email prompted post-onboarding (not during), re-verification prompts for dormant accounts, and support recovery via SFL ID + evidence.

**A6. SMS as a single point of failure.** OTP-only auth makes SMS deliverability a hard dependency; in several target markets SMS delivery is slow or filtered. Plan a fallback OTP channel (WhatsApp OTP or email once captured) behind the same six-digit UI.

**A7. Guest scope needs one precise decision** (added as Decision 7): can a Guest *watch* a live room, or only browse listings? Recommendation: guests can watch public rooms with chat, seats, gifts and follows locked behind a registration prompt — watching is the conversion hook, and a browse-only guest mode converts far worse. Rate-limit guest watch time per day if cost or abuse is a concern.

**A8. "Start a Club" straight out of registration invites spam clubs.** Keep Option B visible (it signals the product's ambition) but gate creation lightly: completed profile required, plus either a small coin cost, a minimum fan level, or a pending-review state before the club is publicly listable. The Create Club Journey should define which.

**A9. Username friction.** Auto-suggest a unique username from the display name (editable) instead of making users invent one against a taken-name wall. Also reserve confusable variants (case, diacritics) to prevent impersonation, and note that inappropriate-name checks are async — the UI needs a "name under review" state, not only an inline rejection.

**A10. Missing consents and settings.** Not in the journey but required somewhere in this flow: explicit Terms acceptance mechanics (checkbox vs. implied — jurisdiction-dependent), analytics/tracking consent where required (GDPR/ATT), language selection (default from device, editable — the Discovery header's country/language filter needs a source of truth), and an account-deletion path (app-store requirement; can live in Settings but must exist at launch).

## B. Consistency with the design direction

**B1. "Gold" vs "Coins."** The ID Reveal says "Fans can transfer Gold to you"; every designed surface so far says Coins. Pick one currency name and use it everywhere. Note separately: peer-to-peer transfer of purchased currency has regulatory weight (money-transmission rules in some markets) — worth a deliberate product decision, not a side effect of the ID screen copy.

**B2. Journey 1 supersedes design-direction §22.** The §22 onboarding trio (team pick → follow hosts → alerts) is absorbed as follows: "pick your team" → Football Interests (step 8); "follow hosts/clubs" → recommend adding *follow* actions inside Football Interests or first-run Discovery, since following is lightweight and needs no application — this preserves the cold-start personalization §22 existed for while respecting the membership-by-application rule; "matchday alerts" → contextual notification prompt at the first follow or first fixture interaction (consistent with Decision 6).

**B3. Role rule matches §12 and §32.** Fan → Manager via club creation aligns with the Fan/Manager design split and the owner-tasks system. The Host rule ("Host only while running a live session") also implies Go Live is available to every Fan — the §25 pre-live sheet should not check for any "host role."

## C. Recommendations on the decisions

1. **Auth: OTP-first.** No password at registration. Sign-in is OTP by default; an optional password can be created later in Settings for users who want it, and either credential works at sign-in (matching the journey's own recommendation). This removes screens 6 and 12–14 from the critical path — they become Settings/recovery variants. Add a non-SMS OTP fallback (A6).
2. **User ID: server-generated, 8-digit numeric**, never phone-derived. Digits-only is easiest to say aloud and type across languages/keyboards; display with the `SFL-` prefix as decoration, store the number. Confirmed: username (social) and SFL ID (transactional) stay separate.
3. **Club selection: remove direct join from onboarding.** Interests personalize; *follows* are allowed (lightweight, no approval); *membership* only via application/invitation.
4. **Explore users are Fans without a club** — agreed. Give them "join a club" nudges through Fan Missions (§32) rather than interstitials.
5. **Social sign-in: hide until fully implemented** for both creation and sign-in — and when added, define phone/Apple/Google account-linking and dedupe rules first.
6. **Permissions: contextual** — notifications at first follow or first matchday-alert opt-in; camera at `Add Photo` and Go Live; microphone at first seat request.
7. **(Added) Guest scope:** guests can watch public rooms; all participation locked behind registration (A7).

---
---

# Confirmed model (v2) — supersedes the open decisions above

## Authentication model

SFL will support both:

1. **Email and password**
   - Primary returning-user sign-in method
   - Email must be verified
   - Password recovery available
2. **Phone and OTP**
   - Phone verification during registration
   - Alternative `Sign in with OTP`
   - Used for password recovery and security verification

OTP is **not** required after every email/password login. OTP is required for:

- Registration
- Phone-based sign-in
- Password recovery
- New or suspicious devices
- Sensitive account changes

## Revised registration flow

1. Splash and session check
2. Welcome
3. Enter phone number
4. Verify phone OTP
5. Age and eligibility check
6. Enter email and create password
7. Verify email
8. Profile setup
9. SFL User ID reveal
10. Choose how to start
11. Join a Club, Start a Club or Explore as a registered Fan

The separate Club Selection screen is removed from onboarding. Optional football interests can be included inside Profile Setup.

## Revised sign-in screen

Two methods on one screen:

**Email and Password:** email · password · show/hide · forgot password · sign in · Apple/Google can be added later if implemented properly.

**Phone OTP:** country code · phone number · send OTP · OTP verification · continue into the app.

## User ID

The client-required permanent SFL User ID is retained. Used for:

- Manager club invitations
- Gold transfers
- Account identification
- Support and transaction references

The database also maintains an invisible internal UUID so every account remains technically unique.

## Manager adding a Fan (consent-safe flow)

1. Manager enters the Fan's User ID.
2. SFL shows the Fan's avatar, display name and basic profile.
3. Manager confirms the correct person.
4. Manager sends a club invitation.
5. Fan receives a notification.
6. Fan accepts or declines.
7. Only after acceptance is the Fan added to the club.

"Add Fan by User ID" does not bypass consent.

## Permission timing

Permissions requested only when relevant:

- **Photos:** when adding an avatar or live-room cover
- **Camera:** when taking a profile photo or starting video
- **Microphone:** when going live, joining a panel or taking a position
- **Notifications:** after onboarding, club joining or the first meaningful action
- **Contacts:** only if contact-based invitations are later added

The app explains the benefit immediately before showing the operating-system permission prompt.

---

## Remaining flags after v2 confirmation

**F1 — The visible SFL ID must itself be unique; the internal UUID does not make it safe.** The UUID guarantees technical account uniqueness, but every workflow the visible ID is used for — Gold transfers, manager invitations, support lookup — operates on the *visible* ID. If two accounts can share a visible ID (which is implied by needing the UUID for uniqueness, and is guaranteed if the ID stays phone-derived five-digit), then "enter the Fan's User ID" cannot resolve to one person: an invitation or Gold transfer can target the wrong account, and the confirm-avatar step only helps when the manager knows the face. Requirement to carry into implementation: the visible SFL ID must be globally unique at assignment (server-generated, e.g. 8-digit numeric with `SFL-` display prefix), and the UUID stays internal. If the client insists on the phone-derived format, collisions must be prevented by suffixing/reissuing — but this weakens the privacy and enumeration fixes and should be pushed back on.

**F2 — Age gate remains after OTP (step 5 after step 4).** Under this ordering an underage user's phone number is collected and verified before they are blocked. If deliberate, add automatic purge of the phone record on the underage outcome; the cleaner fix is still DOB before the OTP send.

**F3 — Email verification as a blocking step (step 7) will cost registrations.** Recommendation: send the verification email at step 6 but let registration continue immediately; show a "verify your email" banner until done, and require verified email only for password recovery and sensitive account changes. Since phone is already verified at this point, account integrity does not depend on blocking here.

**F4 — Currency name is confirmed as Gold** (used consistently in the v2 model). All designed surfaces that say "Coins" (light Discovery header, gift tray prices, missions rewards) must be updated to Gold in the next design pass.

**F5 — Step 6 password entry should include the same strength/requirement states** defined in the original screen 6, and the two-method sign-in screen needs a clear default (recommend: email tab default, `Sign in with OTP` as the secondary tab or link, matching "primary returning-user method").
