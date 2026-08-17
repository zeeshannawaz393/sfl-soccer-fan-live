# Journey 18 — Content & Social

Official SFL video + live co-watching + club community. Core: CS-01 SFL Watch · CS-02 Party Live · CS-03 Fan Feed. **Theme: DARK for Watch + Party Live (media/immersive, broadcast direction); LIGHT club-colour for the Fan Feed** (matches the light Club Home; spec says "no generic white feed").

## Journey boundaries (no duplication)
Official SFL YouTube + public watch party + club feed = **here**. Fan-hosted Formation Room = J7. Live Coins/Possession = J8. Gifts in live = J10. **Private Fan-to-Fan DM/voice/video = J19.** A **Party Live is a shared public/club content experience — NOT a private group chat.** Gifting shows in a Party only if it's *also* an eligible Fan-hosted live under J10.

## Roles
Guest: view public videos/parties/posts, **no** chat/react/post/watch-progress/reward. Fan: watch-progress, join public+permitted parties, chat/react, post if allowed, report, rewards via J16. Manager: + publish announcements, pin, official club parties, shout-outs, moderate **their club's space only** (never platform-wide power). Party Host: start/end, control synced VOD, pin, mute/remove, assign mods. Creation: any eligible Fan → public Fan Party; Manager → official Club Party; SFL admin → platform party.

## Watch-time is verified, not "screen was open"
Valid watch requires: authenticated Fan, eligible SFL video, **actively playing, app foreground, player visible, regular heartbeats**, no double-device counting, no seek-to-complete. Per heartbeat: `Δvalid = min(ΔserverTime, max(0, ΔvideoPos), heartbeatCap)`; `Progress = min(ΣΔvalid / TargetSeconds, 1)×100`. 20-min target = 1200s → 1080/1200 = 90% (the prototype's 18/20). **Doesn't count:** guest, paused, buffering, background, skipping, two devices, non-SFL, ineligible. Muted **does** count (captions/accessibility). Being present in a Party doesn't count unless the embed is actually playing. **Completion ≤1/day**, fixed app timezone (not device-changeable).

## Co-watch sync (no rebroadcast)
Live → all stay near the live edge; reconnect returns to live position. VOD → Host controls play/pause/seek, participants follow. `Target = HostPos@heartbeat + (ServerNow − heartbeatTime)`; small drift → smooth adjust, large (>~2s config) → seek. **Each client loads the authorized YouTube embed directly — SFL never screen-records or rebroadcasts.** Hosts pick only from authorized SFL content — no pasting arbitrary copyrighted URLs.

## Feed ordering (transparent)
MVP is chronological: `Order = Pinned DESC, Created DESC`. **No unexplained engagement algorithm v1.** Shout-outs are recognition and **don't auto-change Fan Value or issue rewards** unless a configured rule says so.

## Screens built
CS-01 Watch (player + gold task ring + up-next) · CS-01C Task Complete · CS-01U Video Unavailable · CS-02 Party Lobby · CS-02A Create Party · CS-02B Party Live Room (co-watch) · CS-02H Host Moderation · CS-02E Party Ended · CS-03 Fan Feed (light) · CS-03A Create Post · CS-03B Post Detail & Comments · CS-03D Shout-Out · CS-03E Report Content · CS-03Z New-Club Empty Feed.

---
---

# Review — issues

## A — Watch-time integrity is the whole point of CS-01, and it can't trust "screen open"
The daily task pays a reward, so the anti-cheat matters: **playing + foreground + visible + heartbeats + no seek + no double-device**, credited server-side only. Built the tracker to show verified progress with honest states — paused says "resume to continue," buffering doesn't advance, guest says "sign in to earn," and progress "syncs" but doesn't award until the server confirms. Completion is capped at once per day on a fixed timezone. This is a J4/J16 dependency (the reward flows there).

## B — YouTube compliance: official player only, never fake controls over it
Must use the **official YouTube IFrame API** and honour the YouTube API ToS/dev policies. Built the media area so the SFL task tracker sits *beside/below* the player and **never overlays fake controls on it**. This also means SFL can't screen-capture and rebroadcast content in Party Lives — each viewer loads the authorized embed themselves.

## C — Copyright & rights are the platform risk here
Hosts choosing "arbitrary streaming URLs" is a hard no — built Create Party to pick **only from authorized SFL content already in the app**. No user video upload in the feed MVP (moderation/copyright/storage cost) — text+image+SFL-video-link only. Real club/competition footage keeps the licensing flag flagged since day one.

## D — UGC = mandatory moderation stack (Apple/Google policy)
Party chat and the Fan Feed are user-generated, so **report / block / mute / moderation queue / profanity+spam controls / rate limits / sanctions / appeals / audit / guidelines** are required for app-store approval, not optional. Built report flows (CS-03E), host moderation (CS-02H), muted/removed/removed-post states, and chat slow-mode. **Manager moderation authority is scoped to their club** — never platform-wide.

## E — Party Live is not a group chat, and not the Formation Room
Kept CS-02B deliberately lighter than J7's Formation interface (video-first, compact chat, floating reactions) and clearly a **content co-watch**, not private messaging (that's J19) and not a fan-hosted broadcast with Coins/Possession (J7/J8). Gifting only surfaces if the party is *also* an eligible J10 live.

## F — Feed is transparent chronological, shout-outs are recognition-only
Pinned-then-newest, no black-box ranking in v1 — users can trust the order. Shout-outs celebrate without silently moving Fan Value or paying out (the spec's guard against gamified favouritism); any reward is a separate configured rule. Reactions are one-per-Fan, changeable, idempotent.

## G — Guest boundary is consistent
Guests watch public content but can't earn progress, chat, react, or post — every surface shows the honest "create an account to participate" prompt rather than a dead button.

## Theme
**DARK** broadcast Watch + video-first Party Live (gold task ring, club-colour ambient, floating reactions, host identity + viewer count always visible); **LIGHT** club-colour Fan Feed (official announcements, celebratory shout-outs, readable Fan posts — not a white generic feed). Flippable on request.
