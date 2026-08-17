# Journey 9 — PK Battle

Live Host-vs-Host support competition (Niki-style battle, football rivalry). **Not** the penalty mini-game (that's J17). Two Hosts in split-screen; Fans gift either side; highest qualifying support at full time wins. Uses the J8 engine (Coins counters + Fan Power bar).

## Canonical screens

PK-01 Matchmaking/Invite · PK-02 Countdown/Start · PK-03 PK Battle Live · PK-04 Winner/Result. Plus the full set of entry/matchmaking/challenge/result states below.

## Mechanics

A Host challenges another (random or invite-by-SFL-ID); opponent accepts/declines; split-screen live; each side shows actual Coins; **Fan Power** calculated from qualifying support; viewers gift either side; final screen shows winner, final Coins, Fan Power, rewards, rematch, exit. Default 3:00, **server-configurable**.

## Roles

Host: start random / invite by ID / accept-decline / compete / receive side support / rematch / exit. Fan: watch, chat, gift Side A/B, share, report, follow either. Guest: watch + see Coins/Fan Power/result only — gifting/chat gated ("Join SFL to support your side"). Entry from an existing live room (Host taps Start PK, viewers transition) **or** from Stadium (eligible Fan → temp Host after eligibility + camera/mic checks).

## Winning formula

A, B = confirmed qualifying Coins per side. Fan Power `A/(A+B)×100`. **Winner from exact Coin totals, not rounded %:** `A>B`→A, `B>A`→B, `A=B`→Draw. If 501 vs 499 rounds to 50/50, still "Blues win by 2 Coins" — show exact margin, and one decimal for very close battles. `A=0,B=0` → "Draw · no qualifying support" (50/50 is only neutral visual).

## Timing (server-authoritative)

`starts_at`, `ends_at`, gift `server_received_at`, finalization ts. Qualifies iff `serverReceivedAt < endsAt`. At zero: gift buttons lock, Finalizing, server processes accepted events, totals lock, Fan Power computed, winner declared. Late events never change the result. One server clock drives every device's countdown.

## Screens

PK-00 Entry/Eligibility (registered · club · camera · mic · host-allowed · no active PK · network) · PK-01 Matchmaking method (Quick Match / Challenge by ID / Browse Live Hosts) · PK-01A Random Search (radar) · PK-01B Invite by ID (lookup → opponent card; validation states incl. can't-invite-self, not-a-host, invitations-disabled, rate-limit) · PK-01C Incoming Challenge (accept/decline, expiry) · PK-01D Challenge Sent (waiting; decline shown without reasoning) · PK-01E Opponent Found / Matchup (VS, rules card) · PK-02 Ready Check · PK-02A Countdown (3·2·1; disconnect before start → no start) · PK-03 Live Battle (split video, side Coins, Fan Power bar, central server timer, side-specific gift, chat, lead-change messages) · PK-03A Choose Side & Gift (sheet retains target; "Full time — gift not sent" if battle ends while open) · PK-03B Lead Change (flash; no extra Coins from animation) · PK-03C Final 10s (buttons active until server deadline, totals never hidden) · PK-03D Finalizing (server-side, not client values) · PK-04A Winner · PK-04B Loser (same verified table) · PK-04C Draw · PK-04D Rematch (new Battle ID, reset Coins/Fan Power/timer, preserve history).

## Cancellation/disconnect

Decline → back to matchmaking · expire → allow re-invite · leave before start → cancel no result · disconnect in countdown → pause/cancel · brief disconnect in battle → reconnecting + grace · voluntary exit → forfeit · server fail → technical cancel · both disconnect → cancel/review · viewer disconnect → rejoin snapshot · gift accepted before disconnect counts, unconfirmed doesn't · result delayed → stay Finalizing.

## Rewards/task (configurable)

Reward amount/currency/who/auto-vs-claim/commission all **undefined → configurable, never hard-code**. PK task (J4) completes only when battle actually starts, meets min duration, reaches verified result, not cancelled for abuse. Opening matchmaking/accepting invite ≠ task complete.

## Open decisions

3-min duration final? · Fan-start-from-Stadium? · both already live? · random-match compatibility · invite lifetime · reconnect grace · voluntary-exit=loss? · gifts if technically cancelled · tie allowed / sudden-death · winner/loser rewards · audience merge model · formation-seat Fans audible during PK · Host can block PK invites · repeat-battle rate-limit · PK-gift commission · PK history saved · **spectator betting/prediction on winner: none defined, must NOT be added** · moderation auto-terminate.

---
---

# Review — issues (journey unchanged)

## A — "Possession" → "Fan Power" (same as J8, applied)

J9 uses "Possession" throughout; I've kept it as **Fan Power** for consistency with §20 and everything already built. Same flag as J8 — one string to swap if you want "Possession"; identical math.

## B — Winner from exact Coins, not rounded % — a genuinely good correctness call, designed in

The doc's insistence that the winner is decided by **exact Coin totals** (501 vs 499 = "Blues win by 2 Coins" even if the bar rounds to 50/50) is exactly right and avoids a "the bar says tie but someone won" trust break. The result screens show **exact gold Coin totals prominently and the winning margin**, with Fan Power % as secondary — not the other way round.

## C — Draw allowed, no forced sudden-death — the right ethical call, designed in

Recommending a **draw** rather than forcing Fans to spend more Coins to break a tie is anti-dark-pattern and correct — I built a proper Draw result. If the client later insists on a winner, a *disclosed* sudden-death rule can be added, but the default should never be "keep spending until someone wins."

## D — No spectator betting on the PK winner — correctly excluded, kept out

The doc explicitly says spectators can't bet/predict the winner and "it should not be added." Good — that keeps PK from becoming *another* gambling surface on top of J5/J6. I have not added any winner-prediction mechanic.

## E — Consistency

Server-authoritative timer + Finalizing (client never declares the result); gifts use **Coins**; rewards kept configurable (no hard-coded amount); entry-as-temp-Host matches J1's "Host is an additive Fan role" and the contextual camera/mic permission timing. **Surface:** the live battle, countdown, matchup and result are cinematic **video** surfaces (overlays on the Host cameras, per the J8 precedent you accepted); the eligibility, matchmaking-method and invite-by-ID setup screens are **light** utility. A live PK can't render on a flat white page — but the pre-live setup does.

No confirmation gate needed; A is the one label decision (Fan Power vs Possession).