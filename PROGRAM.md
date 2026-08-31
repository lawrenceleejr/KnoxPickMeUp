# Knox Pick-Me-Up — Program Design

**Tagline:** *Ride from last call to first cup.*

A public-private partnership between the City of Knoxville, the Knoxville Police
Department, Knoxville Area Transit (KAT), downtown bars, and downtown coffee
shops. Patrons who drove downtown and choose a safe ride home at the end of the
night — a rideshare, a taxi, or public transit — receive a **Morning Pick-Me-Up
Card**: a card good for a **free large coffee** at a participating downtown shop
(plus a free KAT ride) when they return the next morning to retrieve their car.
It's framed as Knoxville saying *thanks for keeping our roads safe*.

---

## 1. The Problem & The Insight

Impaired driving hurts real people on Knoxville's roads. In the Knoxville
region, crashes involving an impaired driver **seriously injure about 67 people
and kill 27 every year** (Knoxville Regional Transportation Planning
Organization), and **one in three Knox County crash deaths involves an impaired
driver** (Knox County Health Department).

People drive downtown, drink more than planned, and then face a choice: pay for
a ride home *and* a ride back tomorrow (plus the hassle), or just drive. The
parked car is the single biggest reason people talk themselves into driving.

**The insight:** don't fight the car — use it. The car guarantees the patron
returns downtown in the morning. Reward the safe choice at the exact moment it's
made (last call, at the bar) and cash it in at the exact moment it pays off
(the morning trip back for the car). Downtown gets the visitor twice, and one
more impaired driver stays off the road.

**The framing:** the card is a **thank-you**, not a coupon. Knoxville thanks the
patron for the most valuable thing they did all night — getting home without
driving. Warm and non-preachy, it makes the free coffee feel like recognition,
and it sets up patron-side funding ("Pick It Forward," below) where tonight's
crowd stands the coffee for tomorrow's safe riders.

## 2. How It Works (Mechanics)

1. **Patron** drives downtown, parks, and goes out.
2. At the end of the night, patron **takes a safe ride home** instead of driving —
   a booked rideshare/taxi, or a KAT bus.
3. Patron **shows proof of the ride** to a bartender at a participating bar: a
   confirmed rideshare screen or an activated transit ticket.
4. Bartender **writes today's date on and hands over one Morning Pick-Me-Up Card** per ride.
5. While the card is valid, it **doubles as a free KAT pass** — the patron can
   ride any bus free, including the morning trip back downtown to the car.
6. Patron returns in the morning, **claims a free large coffee** at a
   participating shop, and drives home sober.

### Card rules
- Good for **one free large coffee**; no cash value; not for resale; any
  add-ons beyond the large coffee are on the customer.
- **"Hair of the KAT"** — the card doubles as a free KAT pass while valid: show it to board any bus
  free during its validity window. This closes the loop: a free ride back
  downtown to retrieve the car.
- **One card per ride** — the ride is the ticket. Accepted proof: a confirmed
  rideshare/taxi, or an activated KAT ticket. A group sharing one Uber gets one
  card (the booker's). Two rides, two cards. Cards are handed out **while
  supplies last** — a bar out for the night says so, no confrontation needed.
- **Designated-driver exception, bartender's call:** a sober designated driver
  taking everyone else home hasn't shown a "ride," but is the exact behavior
  the program exists to reward — a bartender may hand them a card as a
  thanks, entirely at their discretion. Not a patron entitlement; a tool for
  staff to use when they see the safe choice being made.
- Valid **one day** from issue — the card reads "date issued · valid one day,"
  with a blank line the server fills in at hand-out. That written date is both
  the record of issue and the start of the validity window (covers the
  morning-after trip; prevents hoarding).
- Serialized (`KPMU-YYYY-########` plus a one-letter keyed checksum, e.g.
  `…00004217T`, so serials can't be invented by counting). Packs of 50 carry
  their own serial with a leading P (`KPMU-YYYY-P####`); the pack check-out
  record ties every card serial to its issuing bar, and each redemption is
  stored with that bar attached — so no per-card bar mark is needed.

### Fraud & abuse controls
- **Serialization:** every card has a unique number; books of 50 are checked
  out to bars, so issuance is traceable per venue per week.
- **One-per-ride rule** is self-limiting: a card requires a distinct booked
  ride shown at the bar, dated by hand at the moment of proof.
- **Two-touch validation:** bar dates it at issue, coffee shop log at redemption.
  Redemptions are logged by scanning the card's QR at the register and packs
  are checked out to bars by scanning the pack sheet — a zero-maintenance,
  $0 system built on the static site plus Google Sheets, with live
  dashboards; full architecture and setup runbook in
  [design/LOGGING.md](design/LOGGING.md). Mismatched or duplicate serials
  are flagged automatically.
- **Pack kill switch:** a lost, stolen, or misprinted pack is voided with one
  cell in the tracking sheet — every card in it immediately fails to scan at
  every register, and attempted uses are logged with where they turned up.
- **Short expiry** kills secondary-market and stockpiling value.
- **Low stakes by design:** the worst case of a gamed card is one free coffee.
  Controls are proportionate — the program must stay a 10-second interaction at
  the bar, or bartenders won't do it on a busy Saturday.
- **Bartender discretion is a feature:** staff already judge sobriety and IDs;
  they can decline a card without confrontation ("we're out tonight").

### Overnight parking
Leaving the car overnight has to feel free and safe, or the program falls apart.
Fortunately Knoxville already provides this: **downtown's public parking —
municipal garages and surface lots alike — is free after 6 pm on weeknights
and all weekend.** The program doesn't need to negotiate a parking policy — it
just needs to *advertise* the free-parking reality loudly (on coasters, cards,
and signage) so patrons stop treating "but my car" as a reason to drive.
Coordinate messaging with the City so posted hours and any move-out times are
stated accurately (a couple of sites price Saturday daytime or special events
differently); recruit private lot operators as sponsors where a public facility
isn't nearby.

## 3. Branding

| Element | Spec |
|---|---|
| Name | **Knox Pick-Me-Up** — the morning coffee is the literal pick-me-up; getting home safe is the figurative one |
| Tagline | *Ride from last call to first cup.* |
| Core frame | The card is a **thank-you for keeping our roads safe** — recognition, not a coupon |
| Story arc | Last call → Ride home → Morning → Coffee |
| Palette | Warm paper `#faf5eb`, espresso ink `#241a10`, night navy `#101a30`, sunrise orange `#ff8200` (a nod to Knoxville's favorite color) used sparingly as the single accent — see [BRAND.md](BRAND.md) |
| Design | Editorial and typographic — generous whitespace, hairline rules, a serif display face (Fraunces), and one accent color; no gradients, shadows, emoji, or clip-art |
| Voice | Warm, wry, zero lecture. Never "don't drink and drive"; always "good call — coffee's on us." Promise "a free large coffee," and don't oversell it. |
| Physical kit | Coasters ("Booked your ride? Show your bartender."), restroom mirror clings, table tents, window decals ("Pick-Me-Up Partner"), and books of Morning Pick-Me-Up Cards |

Two distinct pieces of print: **coasters** are the advertising medium — they sit
under the drink at exactly the decision moment, and bars go through thousands
anyway, so the program replaces a cost with free branded stock. The **Morning
Pick-Me-Up Card** is the redeemable item — a simple, wallet-sized card (not a coaster),
easy to date, carry home, and hand to a barista.

## 4. Monetization & Sustainability

The funding model is deliberately open — it will be locked with partners as
they come on board. The design constraint is fixed: **the perk is always free to
the patron who took the safe ride.** Candidate revenue streams, roughly in order
of long-run sustainability:

### A. Merchant-funded ("coupon economics") — the self-sustaining core
Coffee shops provide the free large coffee as their own customer-acquisition
cost, the way they'd fund any promotion — not a program payout. The math that
makes it rational: the card brings in a late-night crowd they rarely see in the
morning, a large coffee is a small pour against a morning ticket that usually
runs higher, and a good first visit creates a regular. Shops can cap monthly
redemptions while the model proves out.
*Pro:* zero external money needed; scales automatically with participation.
*Con:* asks the smallest businesses to carry the direct cost; needs early
ticket-size data to keep shops convinced.

### B. Pick It Forward (patron round-up) — the thank-you loop
**Status: parked for the pilot.** It's kept here as a funding *option* to
switch on later; it is deliberately absent from the public site and all
collateral for now, so don't treat it as a live pillar until the program
decides to turn it on.

An optional $1 line on bar tabs: tonight's patrons stand the coffee for
tomorrow's safe riders. This is the purest expression of the brand — the
community literally thanking people for getting home safe — and even modest
uptake at busy venues funds a large share of the coffees.
*Pro:* on-brand, visible, feels like Knoxville looking after Knoxville.
*Con:* revenue varies with uptake; needs simple POS handling and transparent
accounting (publish the pot monthly).

### C. Sponsorship tiers — the accelerant
Annual "presented by" packages for organizations whose interests align with
safer roads: rideshare companies (the program drives bookings), auto insurers,
hospital/trauma systems, parking operators, downtown property owners. Sponsor
logos ride on coasters and cards already in every bar downtown — unusually good
placement per dollar. The placement is built: `build_cards.py --sponsor` and
`build_coasters.py --sponsor` drop a logo into a "printing donated by" slot
without touching the program mark, and `tools/build_sponsor.py` prints the
outreach one-sheet (what it funds, where the logo rides, the logo spec).
*Pro:* covers fixed costs (printing, coordinator) that per-coffee models don't.
*Con:* renewal risk; keep alcohol brands off patron-facing materials.

### D. Bar partner dues — optional, later
A modest monthly membership once the program has proven foot-traffic and
goodwill value. Not recommended for the pilot: bars joining free is what makes
the network dense enough to matter.

### E. Grants & city seed — launch only
One-time money (highway-safety grants, downtown-vitality funds, community
foundations) for the pilot's fixed costs. Treated strictly as seed, never as
the operating model. Live applications — the DKA Quality of Life grant and
the THSO highway-safety cycle — are tracked in [FUNDING.md](FUNDING.md).

**Recommended architecture:** A as the base (the coffee costs the program
nothing in cash — the shop absorbs it as CAC), B as the community flywheel and
story, C to cover fixed costs, E to get off the ground. D held in reserve. KAT
rides come in as KAT's in-kind contribution (see Section 5). Under this
structure the marginal cost of one more safe ride home is approximately zero to
the program — which is what makes it durable.

### Pilot fixed costs (6 months, illustrative)

| Item | Estimate |
|---|---|
| Printing: coasters, cards, signage | $4,000 |
| Part-time coordinator (reconciliation, restock, partner care) | $9,000 |
| Launch marketing & press event | $3,000 |
| Contingency | $2,000 |
| **Total fixed** | **~$18,000** |

The coffee itself is carried by participating shops (Model A) and backstopped by
Pick It Forward / sponsorship (B/C) if a shop needs it; KAT rides are KAT's
in-kind contribution. So the program's cash budget is essentially the fixed
costs above, not a per-perk payout.

## 5. Partner Value & Engagement Playbook

### Downtown bars — *the distribution network*
**Pitch:** "Free coasters and signage, a safer close to your night, reduced
dram-shop-adjacent risk, and your name on a city-backed road-safety program.
The ask is a 10-second date-and-hand at last call."
- Cost to join: $0 at pilot. Program supplies all materials and card books.
- Engagement: start with 5–8 anchor venues in the Old City and Market Square
  whose owners talk to each other; early-partner billing (logo on cards, press)
  creates FOMO for the second wave.
- Staff onboarding: one laminated reference behind the bar; 5-minute pre-shift
  brief; small monthly staff perk (e.g., coffee for the crew) to keep buy-in.
- Pick It Forward: venues that opt in add the $1 round-up line and get
  "Community" billing.

### Coffee shops — *the redemption network*
**Pitch:** "Morning traffic from the late-night crowd — customers you don't
currently get — plus your logo in every bar downtown. You control your exposure
with a monthly cap while we prove the ticket math together."
- Redemption workflow: take the card, log the serial, done. Monthly data shared
  back (redemptions, average ticket uplift) so the value is visible.
- Recruit shops within a short walk of major garages first (Gay Street, Market
  Square, Old City).
- Coffee shops help pick the funding architecture (Section 4) — real
  co-ownership, not a terms sheet.

### City of Knoxville — *credibility & promotion*
**Pitch:** "A positive-incentive complement to enforcement. One prevented
impaired-driving crash costs the city far more than this program's entire pilot.
The asks are mostly promotion, not an open-ended budget line."
- Asks: co-promote the already-free evening/weekend municipal garage and lot parking,
  inclusion in city communications, optional one-time seed for launch costs.
- Offer: full transparency — quarterly issuance/redemption data by venue.

### Knoxville Police Department — *credibility & reach*
**Pitch:** "You get a carrot to pair with the stick. Every card is a documented
decision to not drive home impaired — one less risk on the road."
- Asks: public endorsement, program mention at high-risk moments (football
  Saturdays, New Year's, holiday weekends), no enforcement role inside bars.
- KPD is a *supporter*, not an operator — the program must never feel like
  surveillance or a sobriety checkpoint. Cards are anonymous; no personal data
  is ever collected.

### Knoxville Area Transit (KAT) — *"Hair of the KAT": an accepted ride & a free-ride partner*
**Pitch:** "Riders already taking the bus home safely should qualify for the
perk too — and a valid Pick-Me-Up Card should let anyone ride KAT free while it lasts,
including the morning trip back to the car. It puts KAT in front of the exact
crowd that needs a late ride, wins first-time riders, and drives off-peak
ridership."
- Asks: (1) recognize an activated KAT ticket as valid ride proof; (2) accept a
  valid Pick-Me-Up Card as free fare during its one-day window; help communicate
  late-night and weekend routes/hours to patrons and bar staff.
- Structure: the free rides are KAT's in-kind contribution to a shared
  road-safety goal — new riders and goodwill in exchange, not a program payout.
  Sponsorship can support KAT's marketing of the program if useful.
- Cost control for KAT: the card is valid one day only, so exposure is naturally
  capped; boardings can be tallied (driver count or farebox code) for clean,
  anonymous ridership data.
- Longer term: coordinate service/marketing around the highest-risk nights so
  a bus home is a genuinely easy option, not just an eligible one.
- Note: there is no longer a free downtown trolley, so the free-ride benefit is
  what the program provides — it does not lean on a pre-existing free service.

### Outreach sequence
Ready-to-send first-contact emails for the partners below live in
[OUTREACH.md](OUTREACH.md).
1. **City + KPD first** (credibility unlocks everything else) — one-pager + this site.
2. **3 anchor coffee shops** (redemption must exist before issuance; they
   co-design the funding model).
3. **5–8 anchor bars** for the pilot footprint.
4. **KAT** to confirm transit tickets as accepted proof, agree the
   free-ride-for-cardholders benefit, and align late-night service messaging.
5. **Sponsors** once the partner map makes the placement value concrete.
6. **Press launch** with city/KPD, tied to a high-risk weekend.
7. **Second wave** recruitment using pilot data.

## 6. Metrics & Success Criteria

- **Primary:** cards issued and redeemed (by venue, by night of week).
- **Road safety:** late-night impaired-driving crashes / arrests / single-vehicle
  incidents in the downtown zone (with KPD, acknowledging small-sample noise in a
  pilot) — the outcome the program exists to move.
- **Economic:** average redemption ticket size vs. the cost of a large coffee
  (the number that proves Model A); repeat-customer reports from coffee shops;
  Pick It Forward uptake; overnight garage stays on program nights.
- **Qualitative:** bartender friction reports, patron surveys via QR on the card.
- **Pilot success gates:** ≥60% of anchor bars actively issuing by month 2;
  ≥50% redemption rate; average redemption ticket comfortably above the coffee's
  cost; zero material fraud incidents; partner renewal intent.

## 7. Timeline

| Phase | Window | Milestones |
|---|---|---|
| Design & city buy-in | Months 0–2 | City/KPD MOU, free-parking co-promotion agreement |
| Partner recruitment | Months 2–3 | 3 coffee shops + 6 bars + KAT signed; funding architecture locked with partners; materials printed |
| Pilot launch | Month 4 | Press event on a high-visibility weekend |
| Pilot run | Months 4–9 | Monthly reconciliation, mid-pilot tune-up |
| Evaluate & scale | Month 10+ | Public report, second-wave recruitment, sponsor expansion |

## 8. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Bartenders skip it on busy nights | 10-second workflow, staff perks, coasters do the marketing passively |
| Patron fears a ticket or tow for leaving the car | Lead with the fact that municipal garages and lots are free evenings/weekends; confirm hours with the City; print them on signage; program contact on the card |
| Perception of promoting drinking | Framing is strictly "safe ride home / safer roads"; KPD/city endorsement; no alcohol-brand sponsors on patron-facing materials |
| Fraud (fake ride screens, duplicates) | One-free-coffee cap, one-per-ride rule, serials, expiry, bartender discretion; accept small leakage as marketing cost |
| Redemption load concentrates on a few coffee shops | Per-shop monthly caps at pilot; recruit shops near every major garage; publish redemption spread |
| Coffee shops lose faith in the coupon math | Share ticket-uplift data monthly; Pick It Forward / sponsor funds can backstop the coffee cost if Model A underperforms |
| Program conflated with enforcement | KPD as endorser only; cards anonymous — no data on individuals is ever collected |

## 9. Program Philosophy & References

**The objection we expect:** *"You're rewarding people for a night of drinking
— with public money, no less."* It's a fair thing to raise, and the honest
answer is a **harm-reduction** one. People are going to go out and drink
downtown whether or not this program exists. Given that, the only question that
changes outcomes is: *when they've had too much, how do we make the safe choice
the easy one?* Pick-Me-Up doesn't subsidize the drinking — the perk is
explicitly tied to **not driving**, it's claimed the *next morning*, and it's
capped at a coffee. It buys down the single largest friction that pushes people
to drive impaired (the parked car). The public-interest math is
straightforward: alcohol-impaired crashes impose enormous public costs, so even
a modest reduction easily outweighs the cost of coffee and bus fare.

This is not a new or fringe idea — there's a substantial literature on
harm reduction, alternative-transportation programs, and the behavioral design
of incentives. The evidence is genuinely **mixed**, and we take that seriously:
the responsible reading is that a reward like this should be **one component of
a broader effort** (enforcement, education, transit, responsible-service
training) and should be **evaluated**, not sold as a silver bullet. The
references below are the ones to read first — both the supportive and the
skeptical.

### The harm-reduction frame ("meet people where they are")
- **What Is Harm Reduction?** — Johns Hopkins Bloomberg School of Public Health
  (2022). Plain-language primer on the philosophy.
  <https://publichealth.jhu.edu/2022/what-is-harm-reduction>
- **Harm Reduction as an Alcohol-Prevention Strategy** — *Alcohol Research:
  Current Reviews* (NIAAA), 2018.
  <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6876518/>
- **Harm reduction approaches to alcohol use: health promotion, prevention, and
  treatment** — *Addictive Behaviors* (2002). Foundational framing of pragmatic,
  non-abstinence approaches. <https://www.sciencedirect.com/science/article/abs/pii/S0306460302002940>

### Do "safe ride" / alternative-transportation programs actually work?
- **The effectiveness of alternative transportation programs in reducing
  impaired driving: a literature review and synthesis** — *Journal of Safety
  Research* (2020). Reviews ~125 studies; well-implemented programs *can* reduce
  impaired driving, and identifies the design attributes that predict success
  (low cost, high awareness, convenience, rides to *and* from venues, multiple
  sponsors, year-round availability). <https://pubmed.ncbi.nlm.nih.gov/33334469/>
- **Safe Ride Programs: Alternatives to Impaired Driving** — Traffic Injury
  Research Foundation (TIRF) literature review. Practitioner-oriented synthesis.
  <https://tirf.ca/projects/safe-ride-programs-alternatives-impaired-driving/>
- **Alternative Transportation** — NHTSA, *Countermeasures That Work*. The
  standard U.S. reference rating what's proven vs. promising.
  <https://www.nhtsa.gov/book/countermeasures-that-work/alcohol-impaired-driving/countermeasures/other-strategies-behavior-change/alternative>

### The skeptical / cost-effectiveness view (read these too)
- **Efficacy and cost-effectiveness of subsidized ridesharing as a drunk-driving
  intervention in Columbus, OH** — *Accident Analysis & Prevention* (2020).
  Found crash reductions but modest, expensive savings — and a self-reported
  *increase* in drinking that partly offset the benefit. A direct caution about
  the "rewarding drinking" risk, and why the perk must be small and safe-ride-
  tied. <https://pubmed.ncbi.nlm.nih.gov/32866769/>
- **Effectiveness of designated driver programs for reducing alcohol-impaired
  driving: a systematic review** — *American Journal of Preventive Medicine*
  (2005). The Community Preventive Services Task Force found **insufficient
  evidence** that designated-driver *promotion* alone works.
  <https://pubmed.ncbi.nlm.nih.gov/15894161/>
- **Alcohol-Impaired Driving: Multicomponent Interventions with Community
  Mobilization** — The Community Guide (CPSTF **recommends**, strong evidence).
  Why Pick-Me-Up should sit inside a multi-part strategy, not stand alone.
  <https://www.thecommunityguide.org/findings/motor-vehicle-injury-alcohol-impaired-driving-multicomponent-interventions-community.html>

### Behavioral design (why reward at the decision moment)
- **Nudge: Improving Decisions About Health, Wealth, and Happiness** — Thaler &
  Sunstein (2008). The case for removing friction and rewarding the desired
  choice at the exact moment it's made — the design principle behind dating
  the card at last call.

### The scale of the problem (why public money is justified)
- **The Economic and Societal Impact of Motor Vehicle Crashes, 2019** — NHTSA
  (Report DOT HS 813 403): alcohol-impaired crashes cost an estimated **$58
  billion** in economic costs and **$296 billion** in comprehensive (quality-of-
  life-inclusive) societal harm in 2019 alone.
  <https://crashstats.nhtsa.dot.gov/Api/Public/ViewPublication/813403.pdf>
- **Impaired Driving Facts** — CDC. Ongoing toll and cost figures for
  alcohol-impaired driving. <https://www.cdc.gov/impaired-driving/facts/index.html>

*How to use these:* lead partner and city conversations with the harm-reduction
frame and the cost-of-the-problem figures; be upfront that the direct evidence
for reward programs is mixed; commit to the design attributes the successful
programs share (Section 5) and to publishing an honest evaluation (Section 6).

---

*Data sources: Knoxville Regional Transportation Planning Organization (annual
injuries and fatalities in area impaired-driving crashes); Knox County Health
Department (share of deadly crashes involving an impaired driver).*

*Contact: hello@knoxpickmeup.org · Knoxville, TN*
