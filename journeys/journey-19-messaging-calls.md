# Journey 19 — Messaging, Voice & Video Calls

Private Fan communication, club group chat, one-to-one calling. Foundation: Chat Inbox · Chat Thread · Voice/Video Call. **Theme: DARK "Team Communication Tunnel"** (stadium-dark inbox, full-screen blurred-portrait calls).

## Journey boundaries
Private Fan↔Fan / Manager↔Fan DM, club group chat, 1:1 voice/video = **here.** Live-room public chat = J7/J8. Party Live chat = J18. Fan Feed comments = J18. **Gold transfer = J13. Sending gifts = J10 (via the chat Gift action).** Hard rule: **a private message can NEVER transfer Coins/Gold — money moves only through Wallet or Gift journeys.**

## Contact permissions (anti-spam/harassment)
- **Directly allowed:** Fan ↔ members of their active club; Manager → Fans in their managed club; anyone with an existing accepted conversation; a Fan replying to a legit Manager club message.
- **Request required:** different-club Fan first contact, found-by-User-ID, discovered-in-live-room, former member with no existing convo.
- **Blocked:** guests, blocked/suspended users, users who disabled requests, **Manager contacting a Fan outside their managed club without permission.**
- **Calls are stricter:** 1:1 only (MVP), **existing accepted conversation required**, recipient must explicitly answer, **Manager status does NOT bypass call privacy**, no call button inside a pending request. No club group calls in scope.

## Messaging integrity
Types (MVP): **text, gift, system** only (no images/voice notes assumed). Delivery: `Sending → Sent → Delivered → Read → Failed` — **never show "Delivered" just because the sender had internet.** Server-authoritative sequence (`Seq(M1)<Seq(M2)`) keeps order on reconnect. Offline send = local queue + **idempotency ID** retried → server accepts once (**no duplicates**). System messages are visually distinct and **uneditable**.

## Money stays out of chat
The Gift button opens **J10** (recipient locked to the chat participant, Coins deducted via J10), and produces a gift **system message** ("Priya sent you a Golden Boot"). **No chat action ever says "Send Cash / Send Gold / Pay User / Transfer Coins."** Gold transfer keeps its J13 User-ID + limits + confirmation.

## Calling lifecycle
`Initiated → Ringing → Connecting → Active → Ended` (+ Declined / Busy / No Answer / Cancelled / Unavailable / Permission Denied / Connection Failed / Blocked). **State comes from the signaling service, never a fake timer.** Duration = `Now − ConnectedTime` — **starts on connect, not while ringing.** Recipient's **camera never transmits before they accept**; voice→video upgrade needs the other side to accept. A **Manager cannot force a Fan to answer** or auto-start a call.

## Screens built
MSG-01 Inbox · MSG-02 New Message/Search · MSG-03 Message Requests · MSG-04 One-to-One Thread (delivery states + gift card + system msg) · MSG-04B Blocked/Failed · MSG-05 Club Group Chat (system events, Manager pin) · MSG-06 Send Gift in Chat · CALL-01 Outgoing · CALL-02 Incoming (video) · CALL-P Camera/Mic Permission · CALL-03 Active Voice · CALL-04 Active Video · CALL-05 Ended/Missed/Failed · CALL-06 History · MSG-08 Settings.

---
---

# Review — issues

## A — Contact permissions are the anti-harassment spine
Unrestricted messaging/calling would be a spam-and-harassment engine. Built the tiered model: club members direct, everyone else via **message request**, calls stricter still (accepted conversation required, no call button on a pending request). Crucially, **Manager power does not bypass this** — a Manager can't cold-message a Fan outside their club or force a call. This is the single most important safety decision in the journey.

## B — Money never moves through chat (the hard rule, enforced in UI)
The Gift button routes to **J10**, not the wallet — Coins deducted there, a gift *system message* posted here, and **no "pay/send cash/transfer" language anywhere**. Gold transfer stays in J13 with its User-ID + level limits + confirmation. This keeps the regulated money surface (J13) as the only path for value, which matters for the money-transmission posture flagged since J3.

## C — Honest delivery + call states (no fake "Delivered", no fake "Ringing")
Delivery shows Sent only when the server accepts and Delivered only when the recipient's account actually received it — never "Delivered" just because the sender was online. Calls take state from **signaling**, the timer starts **on connect not on ring**, and Outgoing never shows "Ringing" if the recipient was never reached. Small honesty details, but they're what stop the app from lying about reachability.

## D — Camera/consent privacy on calls
The recipient's **camera doesn't transmit until they accept**, voice→video upgrades need explicit acceptance, permission screens always offer an escape ("Use Voice Instead", "Open Settings") and **never trap the user**. No recording by default — and the design makes **no E2E-encryption claim** (that would need a real, independently-reviewed architecture, per the spec).

## E — Idempotent, ordered, offline-safe messaging
Server-authoritative sequence + client idempotency ID means reconnects don't reorder or duplicate messages, and offline sends queue and resolve once. Built the Sending/Failed/retry states so a flaky connection is visible and recoverable, not silently lost.

## F — Club chat, loan access, and club-scoped moderation
Fans get club chat on join, lose it on leave/removal/transfer. **On loan:** destination club chat = full access, origin = read-only/none during the loan (my recommendation; client to confirm), restored on return. System messages ("Alex joined", "Priya is now on loan at Blue Wolves") are distinct and uneditable. Manager moderation (pin/mute/slow-mode/remove) applies **only to their managed club** — never platform-wide.

## G — Blocking is silent and un-bypassable; reporting is evidence-scoped
Blocking stops DMs/calls/requests/gifts and can't be routed around via another entry point, and it **never alerts the blocked user**. Reports carry message ID + surrounding context + participant IDs + conversation ID; **call reports carry metadata, not recorded content.** This is the UGC-safety surface Apple/Google require.

## H — Privacy settings default to safe
"Who can message/call me" defaults so **unknown users can't immediately video-call** someone. Users can't disable essential safety/transaction system messages. Read receipts and online status are user-controlled.

## Theme
**DARK "Team Communication Tunnel"** — club-colour gradient sent bubbles, neutral received bubbles, gold gift event cards, distinct system messages, full-screen blurred-portrait call backgrounds with glass controls and a red end-call. Native to SFL, not a generic messenger clone.
