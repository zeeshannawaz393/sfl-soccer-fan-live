# Journey 7 — Go Live: Formation Rooms

The foundational live-room journey. Journeys 8 (Coins + Fan Power) and 9 (PK) embed inside it. A Host goes live and opens a football-formation room where Fans take numbered **position seats** (GK, CB, CM, LW, ST…) as audio participants.

> Note: built from the five-screen structure supplied in-thread (GL-01–GL-05). The fuller original spec (expanded setup, permissions, Host/viewer variants, seat management, negative states, ending, live summary) did not reach this working context — states below are extended sensibly and should be reconciled against the full spec if it differs.

## Screens

**GL-01 — Go Live Setup.** Stream title + cover; camera/microphone permission (requested at Go Live, per J1 timing); **11-seat or 13-seat** mode (13 adds two substitute seats); host eligibility (registered Fan + club, per the additive-role rule); Go Live CTA. States: eligible · permission missing · restricted · offline.

**GL-02 — Formation Picker.** Choose **4-3-3 / 4-4-2 / 3-5-2 / 3-4-3 / 5-3-2**; interactive pitch preview; 13-seat mode adds 2 subs to the chosen shape. States: selected · 13-seat variant.

**GL-03 — Formation Live Room.** Main Host video; eleven position seats occupied by Fan avatars (GK/CB/CM/LW/ST…); live chat; **Coins counter from J8** (single-Host → Coins only, no Fan Power — the J8 correction); gift + PK-Battle entry points. Host & viewer variants.

**GL-04 — Host Seat Management.** Open/close positions; move Fans between positions; mute or remove Fans; end the live session.

**GL-05 — Fan Join-Position Flow.** Tap an open position → confirm the position → grant microphone permission → join as an audio participant. Handle **position-taken** and **formation-full** states.

## Consistency notes

- **Single-Host formation room shows the Coins counter only** — no Fan Power bar (J8 rule: Fan Power needs two valid support targets). If the room becomes a PK (J9) or a watchalong (Home/Away), the two-sided Fan Power bar appears.
- **Go Live is available to any Fan** (Host is an additive Fan role, per J1) — no separate "host role" gate; camera/mic are requested here, contextually.
- Gifts use **Coins**; the counter is labelled "Coins sent," never earnings/USD (J8).
- Live-room surface renders over the Host video / on a photographic pitch (media surface); setup & picker are light utility.

## Extended states (for a complete flow)

Position taken while joining · formation full · seat vacated (Fan leaves) · Host mutes/removes a seat · Host reassigns a position · mic permission denied · reconnecting · Host ends live → **Live Summary** (duration, peak viewers, Coins sent, gifts, new followers, top fan) · session ended remotely.