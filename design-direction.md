# Soccer Fan Live — Defined Design Direction: "The Living Stadium"

Soccer Fan Live should feel like a premium digital stadium that is active 24/7 — filled with hosts, fan clubs, rivalries, watch-alongs, conversations, gifts and matchday energy.

It should not feel like:

- A football scores application
- A betting application
- An EA FC clone
- An enterprise club-management dashboard
- Niki Live with football icons pasted on top

The product behaviour can be inspired by Niki Live, but its identity must be unmistakably football.

**Final personality:** Premium + social + tribal + competitive + human + live.

The design must put real people first, football context second, and utilities such as wallets, statistics and management tools third.

---

## 1. Applications I would reference

### Reference matrix

| Application | What SFL should borrow | What SFL should avoid |
|---|---|---|
| Niki Live | Room discovery, Clubs, multi-seat party rooms, gifts, rankings, live events and creator progression | Excessive visual clutter, generic party imagery and too many simultaneous promotional elements |
| TikTok LIVE | Full-screen immersion, prominent Host identity, progressive controls, reactions, multi-guest layouts and bottom-sheet interactions | Making SFL an endless generic vertical-video application |
| Twitch | Following vs discovery, category-based rooms, strong creator identity, schedule awareness and moving viewers between live content | Desktop-style complexity and overly game-streaming-specific terminology |
| BIGO Live | Multi-guest room mechanics, voice rooms, mic queues and live battles | Overloading rooms with badges, currencies, VIP prompts and animations |
| Discord | Persistent communities, permissions, scheduled events, voice rooms, moderators and speaker/audience separation | Complex channel trees that are difficult for casual football fans |
| OneFootball | Match cards, fixture context, live status, team identity and readable match information | Allowing news, scores and statistics to dominate Home |
| EA FC Mobile | Event presentation, high-value player imagery, awards, competition moments and visual ceremony | Applying game-card visuals to every ordinary screen |
| Sorare | Player cards, rarity, ownership, value and squad visualisation | Making the complete app feel like fantasy football or trading |
| Poppo Live | Fast discovery and easy transition from browsing to interacting | Its highly monetised and sometimes visually noisy presentation |

Niki currently connects live streams, party rooms, PK battles, clubs, short videos, Moments, gifts and creator earnings. That connected social model is the strongest structural reference for SFL. *(Source: Niki Live App Store)*

TikTok demonstrates how multi-guest video can remain focused around one primary Host, while allowing guests, moderation, stickers and audience participation. *(Source: TikTok LIVE Multi-Guest)*

Twitch redesigned its mobile experience around a discovery feed because reaching something worth watching quickly is essential for live products. *(Source: Twitch mobile redesign)*

Discord's Stage model — selected speakers with a larger listening audience — is an excellent reference for SFL debates, press-room discussions and club events. *(Source: Discord Stage Channels)*

---

## 2. Product hierarchy

The interface should reflect this order of importance:

1. Live people and rooms
2. Fan clubs and social relationships
3. Matchday activity
4. Host and fan identity
5. Progression and rewards
6. Gifts and economy
7. Football games and player collections
8. Club management and administration

The current prototype treats Market, Wallet, Games, Stadium and Home almost equally. That makes it difficult to understand the app's main purpose.

In the new direction, the purpose becomes clear within three seconds:

> "Find football people, enter a room and participate."

---

## 3. New navigation system

The bottom navigation should be:

| Tab | Purpose |
|---|---|
| Live | Discover Hosts, fan rooms and active conversations |
| Clubs | Access My Club, discover communities and see club activity |
| Go Live | Central elevated action for creating a room |
| Matchday | Fixtures, attached rooms, predictions and reactions |
| Me | Profile, clips, achievements, wallet, rewards and settings |

### Header actions

The header contains:

- SFL logo or page title
- Coin balance
- Messages
- Notifications
- Search or filter depending on context

### Features removed from primary navigation

- Wallet opens from the Coin balance or Profile.
- Market sits under "My Squad" or "Collect."
- Tasks become "Fan Missions" shown contextually.
- Rewards live under Profile and Club.
- Predictions sit inside the relevant fixture.
- Chat remains accessible from the header.
- Manager tools appear inside the managed club.

This makes the navigation social and football-oriented rather than transactional.

---

## 4. Visual design philosophy

### A. People first

The largest visual elements should be:

- Real Hosts
- Real fans
- Club members
- Player photography
- Room participants
- Matchday crowds

Balances, charts, icons and labels should never be visually stronger than the people.

Every significant member must have a different real face. We should not reuse the same five stock avatars throughout the application.

### B. Football should provide context, not decoration

We should not place a pitch texture or stadium background behind every screen.

Football identity should appear through:

- Club colours
- Crests
- Kits
- Match attachments
- Fan photography
- Formation-based rooms
- Competition labels
- Stadium sound and motion
- Fan gifts
- Matchday states

This creates authenticity without making every screen resemble a football game menu.

### C. Controlled visual intensity

The interface should have different energy levels.

| Experience | Energy |
|---|---|
| Forms, wallet and settings | Calm, trustworthy |
| Club Home and profile | Social, expressive |
| Live discovery | Media-rich and active |
| Matchday | Competitive and urgent |
| Live room | Immersive |
| Fan Derby or major event | Maximum energy |

The current design uses roughly the same dark card treatment everywhere. The new system should allow emotional escalation.

---

## 5. Colour system

The mobile app should remain dark-first. I would not add a light-mode toggle for the initial version.

### Foundation colours

| Token | Colour | Use |
|---|---|---|
| Arena Black | `#07090D` | Main application background |
| Deep Surface | `#10141C` | Cards and bottom sheets |
| Raised Surface | `#171D27` | Selected and interactive surfaces |
| Primary Text | `#F7F8FA` | Titles and important content |
| Secondary Text | `#A4ADBA` | Supporting information |
| Disabled Text | `#697382` | Inactive content |

### Functional colours

| Token | Colour | Use |
|---|---|---|
| Pitch Volt | `#C9FF3D` | Primary actions and successful participation |
| Live Coral | `#FF3B5F` | Live status only |
| Trophy Gold | `#F3C34F` | Premium gifts, winners and high status |
| Broadcast Cyan | `#42D5FF` | Verified, information and audio activity |
| Warning Amber | `#FFAA3D` | Deadlines and attention states |
| Error Red | `#FF5263` | Errors and destructive actions |

### Club colours

Every club can contribute:

- Primary colour
- Secondary colour
- Accent colour
- Cover imagery
- Crest

Club colours should tint:

- Club page headers
- Room borders
- Matchday fan sides
- Member badges
- Fan Derby halves
- Club-specific gift effects

They must not recolour the entire interface or damage readability.

---

## 6. Typography

The earlier design became difficult to read because too many condensed/game-style treatments were used and several font sizes were too small.

### Recommended family

Use **Manrope Variable** across the interface.

It is:

- Contemporary
- Highly readable
- Strong enough for sport
- Suitable for social products
- Effective for numbers and balances
- Less generic than system-only typography

A separate display treatment can be used only in event artwork, not ordinary interface text.

### Type scale

| Role | Size / line height | Weight |
|---|---|---|
| Hero title | 30 / 36 | 800 |
| Screen title | 24 / 30 | 800 |
| Section heading | 18 / 24 | 750 |
| Card title | 16 / 21 | 700 |
| Body | 15 / 22 | 500 |
| Secondary | 14 / 20 | 500 |
| Metadata | 13 / 18 | 550 |
| Navigation | 12 / 16 | 650 |

Nothing important should be smaller than 12px.

Scores, clocks, rankings and balances should use tabular numerals so values do not visually jump when updated.

---

## 7. Layout system

### Master mobile frame

- Primary design frame: **390 × 844**
- Validate at: 360 × 800
- Large-phone validation: 430 × 932

### Single-column layout

- No clipped tabs
- No horizontal page overflow
- Respect iOS and Android safe areas

### Grid

- 20px outer page padding
- 8px foundational spacing grid
- 12–16px gaps inside groups
- 24–32px between major sections
- Minimum touch target: 44 × 44
- Standard card radius: 18–20px
- Bottom-sheet radius: 24px
- Pills: fully rounded

Horizontal scrolling should only be used for obvious content carousels such as Live avatars or match cards. Important navigation tabs should remain fully visible and clickable.

---

## 8. Live Discovery screen

This becomes the primary Home screen.

### Header

- SFL identity
- For You / Following switch
- Country or language filter
- Coin balance
- Inbox

### Live-following row

Circular real avatars with animated Live borders:

- Hosts the user follows
- Friends currently live
- Club members live
- Recommended Hosts

Names should be visible beneath avatars rather than represented only by badges.

### Matchday spotlight

One large live card when an important match or event is active.

Example:

> **Manchester Derby Watch-Along**
> United Fans Live vs City Central
> 2.8K watching · 7 friends inside

This card uses:

- Real Host imagery
- Both club crests
- Live score or countdown
- Room type
- Strong Join button

### Live room grid

Large two-column cards with approximately 70% media and 30% information.

Each card shows:

- Real Host or group
- Room title
- Club or league
- Viewer count
- Language/country
- Live badge
- Room format

Room filters:

- For You
- Following
- Matchday
- Fan Rooms
- Debates
- New Hosts

The cards should feel alive. Where technically appropriate, a muted preview can begin after the user pauses on a card.

---

## 9. Room design system

We should not design a completely different interface for every room. One reusable live-room shell should support four room templates.

### Template 1: Solo Live

Best for:

- Fan commentary
- Transfer discussions
- Match reactions
- Football news
- Creator shows

Layout:

- Full-screen Host video
- Host identity at top
- Chat overlay in lower third
- Follow and viewer count
- Gift, comment, share and guest controls
- Optional fixture attachment

### Template 2: Squad Room

Niki and BIGO demonstrate the appeal of multi-seat rooms. BIGO currently supports a Host with up to 11 additional friends, which maps naturally to football's 11-player concept. *(Source: BIGO Live Google Play)*

SFL structure:

- One prominent Host/Captain
- Eleven participant seats
- Club-themed pitch
- Audience remains unlimited
- Request-seat queue
- Mute, lock and moderation states
- Position labels optional

The Host should remain visually larger than the other 11 members.

Participant avatars should be large enough to recognise. Names can appear on selection rather than forcing 11 names permanently onto the pitch.

### Template 3: Watch-Along

Attached to an official fixture:

- Host video or audio
- Match score and clock
- Key event notifications
- Team lineups
- Polls
- Predictions
- Fan split
- Chat
- Goal reactions
- Club-room recommendations

OneFootball should influence match-information clarity, but not the complete visual language. It provides detailed live scores and team-focused content; SFL's differentiation is that every match leads into live people and communities. *(Source: OneFootball)*

### Template 4: Fan Derby

This replaces generic "PK Battle."

Layout:

- Two Hosts in a vertical or horizontal split
- Club colour on each side
- Large central timer
- Support Points
- Top fans
- Gift-combination events
- Momentum animation
- Round result and winner ceremony

The metric should be called **Fan Power** or **Support Score**, not Possession. Football possession has a real match meaning and should not be represented by gift spending.

"Penalty Shootout" remains the name of the actual football mini-game.

---

## 10. Live-room interaction layers

A live room should use three clear layers.

### Content layer

- Video
- Audio seats
- Fan Derby
- Match data
- Host and guests

### Social layer

- Chat
- Join notifications
- New followers
- Gift announcements
- Reactions
- Polls
- Moderator messages

### Action layer

- Comment
- Request mic/seat
- Share
- Fan games
- Gifts

User profiles, gift menus, match details, seat requests and reporting should open in bottom sheets. They should not navigate the user away from the room.

TikTok's approach of keeping interactive controls over the live content is the right reference, while Discord provides the stronger speaker/audience and moderation model. *(Sources: TikTok LIVE, Discord Stages)*

---

## 11. Fan Club design

A club is not simply a table of members. It is a persistent social home.

### Club header

- Real fan cover image
- Crest
- Club name
- Level or league
- Member count
- Members currently online
- Join/Joined state
- More actions

### Club navigation

Use four visible tabs: **Home · Rooms · Feed · Members**

Do not hide tabs beyond the edge of the screen.

### Club Home

- Live now
- Next scheduled event
- Club announcement
- Members online
- Weekly club mission
- Recent Fan Feed posts
- Club ranking
- Top contributors

### Club Rooms

- Active voice rooms
- Match watch-alongs
- Upcoming scheduled rooms
- Club debates
- Past clips

### Club Feed

- Photos
- Reaction videos
- Polls
- Matchday posts
- Announcements
- Creator clips

### Club Members

- Manager
- Moderators
- Hosts
- Members
- New members
- Online state
- Search and filters

This borrows Discord's persistent community model, but presents it through a simpler mobile structure rather than a complex channel tree.

---

## 12. Fan versus Manager experience

The distinction must be clear without creating two visually unrelated applications.

### Fan view

The Fan sees:

- Club activity
- Rooms
- Events
- Feed
- Members
- Missions
- Rankings
- Chat
- Join/leave actions

### Manager view

A Manager sees the same Club Home, plus a visible **Manage** action.

The Manage action opens **Club Studio**:

- Applications
- Member roles
- Moderator assignments
- Scheduled rooms
- Announcements
- Club missions
- Reports and safety
- Performance
- Rewards or treasury
- Club settings

The Manager workspace should be calmer and more operational:

- Solid surfaces
- Fewer background photographs
- Clear lists
- Explicit status chips
- Search and filters
- Confirmation for sensitive actions

The fan-facing club remains emotional and social; the manager-facing workspace becomes efficient and trustworthy.

---

## 13. Matchday design

Matchday is how we stop SFL from becoming a generic live application.

### Matchday Home

- Date selector
- Live fixtures
- Upcoming fixtures
- Following clubs
- Rooms attached to each match
- Friends watching
- Predictions awaiting action
- Post-match rooms

### Fixture card

Each card includes:

- Team crests
- Team names
- Score or kickoff
- Competition
- Match status
- Number of live SFL rooms
- Friends or club members inside

Primary action: **Join Matchday** — not simply "View Match."

### Match detail

Four visible tabs:

- **Live** — score, time and key match events
- **Rooms** — official, popular, club and language-specific watch-alongs
- **Match** — lineups, statistics and table context
- **Fans** — polls, predictions, posts and fan sentiment

This is where OneFootball's information hierarchy and SFL's live social model meet.

---

## 14. Profile and social identity

The Profile should make someone feel like a football personality, not a wallet account.

### Profile header

- Large real avatar
- Cover image
- Display name and User ID
- Country/language
- Favourite team
- Club membership
- Follow and Message
- Fan level
- Followers/following

### Profile content

Tabs: **Moments · Clips · Achievements**

Additional content:

- Host level
- Club role
- Matchday streak
- Fan badges
- Gift collection
- Favourite players
- Rooms hosted
- Derby record

Wallet, settings, KYC and support remain in the account menu rather than filling the public profile.

---

## 15. Player cards and Market

EA FC and Sorare should influence this module only.

Sorare succeeds by combining real player photography, card ownership, lineups and real-world performance. *(Source: Sorare)*

EA FC Mobile demonstrates how club identity, famous players and event artwork can make special moments feel valuable. *(Source: EA SPORTS FC Mobile)*

### SFL player-card treatment

- Real licensed player photograph
- Club and country
- Position
- Current value
- Form
- Rarity
- Ownership status
- Next fixture
- Trend

Cards can have premium frames, but ordinary fan profiles, settings and club members should not be turned into game cards.

Player collection should live under: **Me → My Squad**

The Market should be accessible from My Squad and selected Matchday surfaces — not from the central navigation.

---

## 16. Gifts and effects

Human images must remain real. Gifts and live effects can use premium 3D or cinematic animation rather than cartoon illustrations.

### Gift families

- Scarf
- Flag
- Match ball
- Golden boot
- Trophy
- Captain's armband
- Stadium lights
- Drum
- Chant wave
- Goal explosion
- Tifo
- Team bus
- Legendary stadium
- World trophy

### Visual levels

| Tier | Behaviour |
|---|---|
| Common | Small animated object near chat |
| Rare | Short overlay around Host |
| Epic | Room-wide club-colour effect |
| Legendary | Full-screen stadium sequence |
| Derby Combo | Repeated support animation with counter |

Gift effects must not permanently cover the Host, match score or moderation controls.

---

## 17. Motion direction

Motion should make the product feel active without becoming exhausting.

### Persistent subtle motion

- Live-avatar pulse
- Audio-speaking ring
- Match clock
- Viewer-count transitions
- Room preview
- Fan Power movement

### Event motion

- Goal pulse
- New participant entering a seat
- Gift combination
- Derby lead change
- Promotion or level-up
- Winner celebration

### Motion rules

- Ordinary transitions: 180–240ms
- Bottom sheets: 280ms
- Large celebration: 1.5–3 seconds
- Respect reduced-motion preferences
- No continuous background animation on operational screens

---

## 18. Imagery direction

The visual system must use real, varied imagery.

### Required imagery

- Distinct real faces for every recurring Host/member
- Football fans of different regions and ages
- Real football environments
- Matchday streets and stadium exteriors
- Fans wearing team colours
- Hosts recording from realistic personal spaces
- Real player photography where legally licensed

### Image treatment

- Edge-to-edge photography on discovery and live surfaces
- Dark gradient behind text
- Faces kept inside safe crop zones
- Club-colour light treatment
- Background scrim of approximately 30–45%
- No repeated generic stadium image
- No cartoon people
- No fake illustrated profile portraits

Forms, wallet and administration screens should use solid surfaces rather than forcing photography behind fields.

---

## 19. Components to standardise

- Live room card
- Host avatar with status ring
- Member avatar with role badge
- Fixture card
- Club card
- Match event row
- Live header
- Chat message
- Gift event
- Viewer/fan stack
- Fan Power bar
- Audio seat
- Video guest tile
- Join-seat bottom sheet
- User mini-profile sheet
- Gift sheet
- Confirmation sheet
- Manager list row
- Status badge
- Empty/loading/error states

The current project created many isolated screens. The redesign should create a smaller number of powerful templates with clear states.

---

## 20. What we should deliberately avoid

- Generic blue stadium backgrounds everywhere
- White full-page backgrounds
- Tiny typography
- Condensed fonts for ordinary UI
- Repeated faces
- Horizontal tab cut-offs
- Manager controls visible to Fans
- Wallet and Coin prompts on every screen
- Treating fans as tradable footballers
- Calling gift-based support "Possession"
- Too many competing badges
- Glass effects behind forms and dense information
- Football pitch patterns on unrelated screens
- Constant high-energy animation
- Game cards used for ordinary people
- Scores and news becoming more prominent than live rooms

---

## 21. First design batch

Before redesigning the complete application, I would create these eight high-fidelity screens:

1. Live Discovery — For You
2. Live Discovery — Matchday state
3. Solo Live room
4. Squad Room with Host + 11 seats
5. Watch-Along attached to a fixture
6. Fan Derby
7. Fan-facing Club Home
8. Manager Club Studio

These screens will answer the most important questions:

- Does SFL feel alive?
- Is it visibly football-specific?
- Are real people the focus?
- Is the interface premium without becoming empty?
- Can Fan and Manager experiences coexist?
- Does the app resemble Niki functionally without copying it visually?

Once this direction is approved, onboarding, Matchday details, profiles, chat, gifts, player cards and wallet can inherit the same design language.

**The final direction:** Niki/BIGO live mechanics + TikTok/Twitch discovery + Discord community structure + OneFootball match context + controlled EA FC/Sorare progression visuals — all unified as one premium football social platform.

---
---

# Additions (sections 22–30)

The following sections extend the direction above. Nothing earlier is changed; these fill areas the original document does not yet cover.

---

## 22. Onboarding and first run

The three-second purpose test ("find football people, enter a room and participate") is won or lost in the first session, so onboarding must feed the For You feed before the user ever sees it.

Maximum three steps, all skippable except the first:

1. **Pick your team** — searchable grid of clubs with crests and colours. This choice tints the user's experience from the very first screen: their club's colours appear on their profile, their Matchday tab prioritises their fixtures, and their Live feed boosts rooms from their club community.
2. **Follow people** — a curated row of recommended Hosts and popular fan clubs for the chosen team and language. Target at least three follows so the Following feed and live-avatar row are never empty on day one.
3. **Matchday alerts** — one clear toggle: "Tell me when my club plays and when my people go live." Framed as a fan benefit, not a permissions dialog.

Rules:

- No wallet, coins, KYC or purchases anywhere in onboarding.
- First landing after onboarding is Live Discovery with at least one personalised element already visible (followed Host live, club room active, or the user's next fixture).
- Onboarding uses the same imagery standards as the rest of the app: real fans, not illustrations.

---

## 23. Scheduled rooms and event states

Twitch's schedule awareness and Discord's scheduled events are referenced in section 1 but need a concrete surface. Live products die between live moments; scheduling is how SFL stays alive at 3pm on a Tuesday.

### Scheduled room card

A variant of the live room card with:

- Host or club identity
- Room title and template type
- Countdown or start time
- Attached fixture if relevant
- **Remind me** action
- Number of fans already waiting

### Lifecycle states

Every room moves through one visual lifecycle:

> Scheduled → Starting soon (15 min) → Live → Ended → Clip recap

- "Starting soon" upgrades the card treatment (warmer border, pulsing countdown) without using the Live Coral badge — coral remains live-only per section 5.
- "Ended" cards convert into clip recaps rather than disappearing, so club pages never look abandoned.
- Scheduled rooms appear in Club Home ("next scheduled event"), Matchday (pre-match rooms), and the Host's profile.

---

## 24. Sound and haptic identity

Section 4 mentions "stadium sound and motion" — this defines it. Sound is a major differentiator for a stadium feeling, and no reference app owns it well.

### Sound palette

- **Ambient crowd bed** — a very low, optional stadium murmur inside Watch-Along and Fan Derby rooms only. Never on discovery, forms or operational screens.
- **Goal moment** — a short crowd-roar swell layered under the goal-pulse animation.
- **Gift sounds** — tiered to match section 16: common gifts are near-silent, rare gifts a short chant sting, legendary gifts a full stadium sequence.
- **Derby lead change** — a rising crowd note on the side taking the lead.
- **Seat join** — a subtle whistle-adjacent tick when someone takes a seat in a Squad Room.

### Haptics

- Light tap on goal events and derby lead changes.
- Success haptic on level-up, mission completion and winning ceremonies.
- No haptics for chat, viewer counts or routine navigation.

### Rules

- One global sound toggle plus a per-room mute; default follows the device silent switch.
- Sounds never overlap the Host's audio at competing volume — ambience ducks under speech.

---

## 25. Host experience

The document designs the viewer side thoroughly; the Host side needs equal definition because Hosts are the supply that makes discovery work.

### Pre-live setup (bottom sheet from Go Live)

- Room title
- Template choice: Solo Live, Squad Room, Watch-Along, Fan Derby
- Club tag and language
- Fixture attachment (auto-suggested on matchdays)
- Cover frame selection from camera
- Optional schedule-for-later instead of going live now

### During live: Host dashboard

A Host-only collapsible panel showing viewers, new followers, gift totals for this session, the seat-request queue, and quick moderation actions. Calm and glanceable — the Host is performing, not reading analytics.

### Post-live summary

One ceremony-light screen: session duration, peak viewers, new followers, gifts earned, and suggested clips to publish to the Club Feed or their profile. This is where progression (Host level movement) is shown — an earned-reward moment, matching the energy system in section 4C.

---

## 26. Clips, Moments and content creation

Clips appear throughout the document (profiles, club feeds, recaps) but need a creation loop.

- **Clip button** inside every live room — captures the last 30 seconds; viewers and Hosts can both clip.
- **Auto-highlights** — goal moments in Watch-Alongs and winner ceremonies in Derbies are automatically offered to the Host as clips after the room ends.
- Clips are 15–60 second vertical videos that flow into three places: the creator's profile (Clips tab), the relevant Club Feed, and the fixture's Fans tab.
- **Moments composer** — a simple post creator for the Club Feed and profile: photo, short video, poll, or matchday check-in. One composer reused everywhere, opened as a bottom sheet.
- Clips always carry a "watch the Host live / follow" pathway — content exists to route people back into live rooms, keeping the section 2 hierarchy intact.

---

## 27. Notifications and quiet-day energy

### Notification tiers (matched to the section 4C energy system)

| Tier | Examples | Behaviour |
|---|---|---|
| Urgent | Your club kicks off in 15 min; derby against your rival club starting | Immediate push, rich fixture imagery |
| Standard | A followed Host went live; your seat request was accepted; club event starting | Immediate push, standard |
| Digest | Club feed activity, new followers, mission progress, rankings movement | Bundled once or twice daily |

Coin promotions and market activity never use the Urgent tier.

### Quiet-day states

Every high-energy surface needs a defined "no match today" state so the app never looks dead:

- **Matchday tab, no live fixtures:** upcoming fixtures with prediction deadlines, last match's post-match rooms and clips, and scheduled watch-alongs — never a blank list.
- **Live Discovery, low supply:** the grid backfills with scheduled rooms, top clips from the last 24 hours, and club activity, clearly separated from truly-live content so the Live badge never lies.
- **Club Home, nothing live:** next scheduled event and the weekly mission take the hero position.

---

## 28. Progression and badge grammar

Levels and badges appear across profiles, chat, clubs and rooms. Without one grammar they will collide into the "too many competing badges" failure listed in section 20.

One visual grammar, where shape communicates category before colour communicates rank:

| Category | Shape language | Where it appears |
|---|---|---|
| Fan level | Rounded shield | Profile, chat, mini-profile sheet |
| Host level | Star/beam mark | Room header, profile, discovery cards |
| Club role | Armband-inspired chip | Club members list, club chat |
| Event/seasonal | Trophy/medal forms | Profile achievements, ceremonies |

Rules:

- Maximum **two** badges beside any chat message: fan level + one other.
- Full badge collections live on the profile Achievements tab, not inline.
- Levels use numbered tiers with Trophy Gold reserved for the top band only, keeping gold scarce per section 5.

---

## 29. Refinements layered onto existing systems

Small additive rules that strengthen sections already defined, changing nothing:

- **Same-colour derby rule (extends §5):** when both clubs in a Fan Derby or fan split share a similar primary colour, the away/challenger side automatically uses its secondary colour, and each half carries its crest watermark so sides stay unmistakable.
- **Club-tint contrast rule (extends §5):** text on club-tinted surfaces always uses the neutral text tokens; club colours tint borders, glows and backgrounds only, never the text itself.
- **Gold vs amber separation (extends §5):** Trophy Gold and Warning Amber are close at small sizes; warnings therefore always pair the colour with a clock/alert icon, and Trophy Gold never appears with an icon of urgency.
- **Ambient motion budget (extends §17):** at most two persistent ambient animations in any viewport at once (e.g., live-avatar pulses count as one system). Event motion is exempt.
- **Tiered card previews (extends §8):** muted in-card previews activate on Wi-Fi/unmetered connections and in the following row first; the general grid can fall back to animated stills. The feed must feel alive even where autoplay is off.
- **Tabular numerals (extends §6):** confirm the chosen Manrope build exposes tabular figures before locking the numeric system; if unavailable, pair a numeric companion face for scores, clocks and balances only.
- **Header density at 390px (extends §8):** if the Discovery header cannot hold identity + For You/Following + filter + coins + inbox comfortably, the country/language filter moves into the room-filter row; the For You/Following switch always stays in the header.

---

## 30. Second design batch

After the first eight screens are approved, the next batch should extend the language in this order:

1. Onboarding trio (team pick, follow people, alerts)
2. Matchday Home + Match detail (Live/Rooms/Match/Fans tabs)
3. Profile (own and public views)
4. Scheduled room card states (scheduled → starting soon → ended → clip recap)
5. Gift sheet and gift-tier effects
6. Host pre-live setup and post-live summary
7. Moments composer and Club Feed
8. Quiet-day states for Matchday, Discovery and Club Home
9. My Squad and player-card Market
10. Wallet and account (calm-energy proof of section 4C)

This batch proves the system can flex from maximum energy (batch one) down to calm and trustworthy — the full emotional range in section 4C.

---

## 31. Light theme addendum (approved deviation)

Sections 5 and 20 define the product as dark-first with no light mode and list white full-page backgrounds as something to avoid. A light-mode concept in the Niki/BIGO visual language was explicitly requested and explored on 14 Aug 2026, so this addendum records it as an approved alternate direction rather than a silent contradiction.

### Light palette

| Token | Colour | Use |
|---|---|---|
| Day Surface | `#F4F6FB` | Application background |
| Card White | `#FFFFFF` | Cards and sheets |
| Line | `#ECEEF5` | Hairline borders |
| Ink | `#14161C` | Primary text |
| Ink Soft | `#707786` | Secondary text |
| Pitch Green | `#0FB753 → #7CD843` | Primary actions, active states, Go Live |
| Live Gradient | `#FF416C → #FF7A3B` | Live status and gift button only |
| Coin Gold | `#FFB300 → #FFD54F` | Coins, VIP, winners, Captain |
| Club Red / Club Sky | `#E4362B` / `#5FA8DE` | Derby sides and club identity |

### Rules carried over unchanged

- All §2 hierarchy, §3 navigation, §6 type scale (nothing important below 12px, tabular numerals), §7 grid, §9 room structures (Host + 11 seats), §16 gift families and §18 real-imagery rules apply identically in light mode.
- "Fan Power" naming, Live-only usage of the live colour, and the no-betting-framing rule apply identically.
- Whether the shipped product is dark-first (§5), light-first (this addendum), or theme-switchable is an open product decision — the two concept sets exist to make that comparison.

---

## 32. Missions system — Fan Missions and Club Owner Tasks

Section 3 removes Tasks from primary navigation and renames them "Fan Missions shown contextually." This section defines that system for both roles. The two sides are deliberately different in tone: fan missions are playful and progression-driven; owner tasks are operational first, gamified second.

### Principles

- Missions reward **participation**, never spending alone. Purchase-linked missions are capped at one per cadence and never the featured mission.
- No gambling framing anywhere: predictions can be a mission ("make your prediction before kickoff"), but rewards come from participating, not from predicting correctly with coins at stake.
- Missions are surfaced **contextually** (Matchday tab, Club Home, Profile, post-match) — never as popups over a live room, and never as a nav tab.
- All progress numerals use tabular figures; mission text obeys the §6 type floor.

### A. Fan Missions

Four cadences:

**Daily** (reset 24h, 3 active at a time)
- Watch any live room for 10 minutes
- Send 5 chat messages
- Visit your club's Home
- React to a live moment (goal, derby lead change)
- Send any gift (capped: the only spend-linked daily)

**Weekly**
- Join 2 watch-alongs
- Take a seat in a Squad Room
- Make predictions on 3 fixtures
- Post once in your Club Feed
- Support your side in a Fan Derby
- Follow 2 new Hosts

**Matchday specials** (active only on your club's matchday — the §4C "competitive and urgent" energy)
- Join a match room before kickoff
- Predict before kickoff
- Stay through the full 90
- Post a post-match reaction

**Streaks and seasonal**
- Matchday streak (already on the §14 profile)
- Season-long fan journey (attend N of your club's fixtures) feeding the §28 badge grammar

**Rewards:** Fan XP (fan level), small coin drops, §28 badges, and cosmetic flair (chat name colour, profile frame, club-tinted entrance effect). Big-ticket rewards are cosmetic and social, not financial.

**Surfacing:** a "Fan Missions" card on Matchday Home (§13), a club-specific mission row on Club Home (§11), full list under Profile → Rewards (§3). A quiet checklist is reachable from a room's overflow menu, never an overlay.

### B. Club Owner / Manager Tasks

Two distinct kinds, both living in Club Studio (§12):

**1. Duties — the Manager Inbox (operational, not gamified)**

A counted to-do list at the top of Club Studio:

- Membership applications awaiting review
- Reports awaiting action (always first when present — safety beats growth)
- Scheduled rooms with no assigned moderator
- Announcement drafts unpublished
- Empty event calendar for the coming week (warning state)
- Expiring roles or inactive moderators

Presented as list rows with counts and status chips in the calm §12 visual treatment. Clearing duties earns no rewards — it is the job.

**2. Club Growth Missions (weekly, gamified, collective)**

The owner activates one featured mission per week — this becomes the "Weekly club mission" fans see on Club Home (§11). Fan contributions roll up into a single collective progress bar.

Examples:

- Run 3 club rooms this week
- Host a watch-along for every club fixture
- Get 25 members active in a week
- Welcome every new member within 24h (greeter role)
- Win a Fan Derby as a club
- 15 Club Feed posts from 10 different members

**Rewards:** club XP (club level/league, §11), treasury coins (§12), and club-wide unlocks — a custom club gift, a tifo celebration effect, a ranking boost, member entrance flair. Rewards land on the club, not the owner personally, so owners are incentivised to grow the community rather than farm it.

### C. How the two sides connect

The owner picks the mission; the fans complete it; the club levels up; every member sees the shared reward. This loop is the retention engine that §2's hierarchy implies: it gives owners a reason to program content, fans a reason to return on non-matchdays (§27), and clubs a shared identity beyond chat.
