# Knox Pick-Me-Up

*Ride from last call to first cup.*

**🌐 Live site: <https://knoxpickmeup.org/>**

A proposed public-private road-safety partnership for downtown Knoxville:
patrons who drove downtown and take a safe ride home at the end of the night —
a rideshare, taxi, or public transit — show proof of the ride to their
bartender and receive a **Morning Pick-Me-Up Card**, good for a **free large coffee**
at a participating downtown shop when they return the next morning to pick up
their car. While valid (one day), the card also doubles as a free KAT transit
pass — including the ride back downtown to the car.

Partners: City of Knoxville · Knoxville Police Department · Knoxville Area
Transit (KAT) · downtown bars · downtown coffee shops.

## The pages

Three pages, one static site — each aimed at a different audience:

| Page | Audience | What it does |
|---|---|---|
| [`index.html`](https://knoxpickmeup.org/) | **Public** — patrons, partners, press | The program site: how it works, why it matters, the card, an OpenStreetMap map of participating shops/bars and the free municipal garages, partner pitch, FAQ. Every card’s QR lands patrons here, on the shop map (the places that redeem it). Linked everywhere. |
| [`/redeem/`](https://knoxpickmeup.org/redeem/) | **Business** — coffee-shop baristas | The card scanner. Opened from the shop's register QR (`?shop=slug`, with a dropdown fallback), it scans a card's QR with the phone camera, shows live detection feedback, and logs the redemption — with duplicate/voided-card rejection, offline queueing, manual entry, and a stop button. Runs in labeled demo mode until the backend is configured. |
| [`/dashboard/`](https://knoxpickmeup.org/dashboard/) | **Admin** — you, and anyone you hand the link | Live program numbers from the Sheet: issued/redeemed/rate tiles, integrity counters, redemptions over time, to-shop and from-bar rankings, the bar→shop flow matrix, latest activity. Unlinked and unindexed but freely shareable — it exposes venue names, timestamps, and counts only, never patron data or serials. |

Also business-facing but not a page: each **card pack's cover sheet** carries
a QR that opens the scanner's admin pack check-out (pre-loaded with the pack
and its card range — pick the bar and submit).

## Contents

- **[`index.html`](index.html) · [`redeem/`](redeem/index.html) ·
  [`dashboard/`](dashboard/index.html)** — the three pages above; self-contained
  static files, no build step. Libraries are vendored in
  [`assets/vendor/`](assets/vendor) (Leaflet for the map, jsQR for the
  scanner), so the only thing fetched from a third party at view time is the
  map's basemap tiles — OpenStreetMap data in CARTO's minimal rendering,
  retina where the screen supports it — and only once a visitor scrolls to
  the map.
- **[`PROGRAM.md`](PROGRAM.md)** — full program design: mechanics, card spec,
  fraud controls, branding guide, partner engagement playbook, pilot budget,
  metrics, timeline, and risk register.
- **[`design/LOGGING.md`](design/LOGGING.md)** — the card-tracking system:
  QR scan-to-log redemptions (`redeem/index.html`), pack check-out, Google Sheets
  backend, Looker Studio dashboards — no servers, $0, volunteer-proof.
- **[`PRINTING.md`](PRINTING.md)** — the printing guide: card-book specs and
  a copy-paste RFQ, vendor guidance, file generation, register QRs, and the
  pre-flight checklist for every print run.
- **[`BRAND.md`](BRAND.md)** — the visual identity guide: logo suite, the
  signature mark, color palette, typography, favicon, layout language, and usage.
- **[`assets/`](assets)** — brand assets as scalable SVG (print- and web-ready;
  all type converted to outlines, no font dependencies):
  - [`logo.svg`](assets/logo.svg) — primary lockup (light backgrounds)
  - [`logo-dark.svg`](assets/logo-dark.svg) — lockup for dark backgrounds
  - [`mark.svg`](assets/mark.svg) — the signature mark (a coffee cup in a rounded badge)
  - [`logo-mark.svg`](assets/logo-mark.svg) — the mark sealed in a badge (emblem)
  - [`favicon.svg`](assets/favicon.svg) — app icon / favicon
  - [`palette.svg`](assets/palette.svg) — color swatch sheet
  - [`card.svg`](assets/card.svg) — a **reference render** of the Morning Pick-Me-Up Card (business-card size), signed with the public demo key. Real cards come from `tools/build_cards.py` with the program key — don't print this file.
  - [`coaster.svg`](assets/coaster.svg) — a one-sided brand **swatch** of the coaster. The two-sided print coaster comes from `tools/build_coasters.py`.

## How the data flows

One Google Sheet is the entire database. Who writes what:

| Data | Written by | Human involved? |
|---|---|---|
| `Redemptions` (each coffee handed over) | the **Apps Script web app**, when a barista scans a card on [`/redeem/`](https://knoxpickmeup.org/redeem/) | barista points a phone camera; no typing |
| `Packs` (which bar got which serials) | the **scanner's admin pack check-out**, opened by the QR on each pack's cover sheet | deliverer picks the bar and scans the pack |
| `Venues`, `Packs.voided` (kill switch) | **you, by hand** | rarely |

Nothing else ever writes to the Sheet. Full architecture, the Apps Script
code, and failure-mode analysis: [`design/LOGGING.md`](design/LOGGING.md).

## Set up the program (one afternoon)

Everything below is free and requires no server. Steps 1–3 happen in Google,
4–5 in this repo, 6–8 back in Google/GitHub.

1. **Create the program Google account** (e.g. `knoxpickmeup@gmail.com`) so
   nothing is tied to one volunteer. Do all Google steps signed in as it.
2. **Create the Sheet** with three tabs and header rows:
   - `Redemptions`: `timestamp | serial | shop | status | bar | pack serial`
   - `Packs`: `timestamp | pack serial | first | last | bar | voided`
   - `Venues`: `slug | name | type | joined | deactivated | monthly cap`
     (the last column is the optional shop redemption cap the dashboard tracks against)
   Share it with **no one** (partners get the dashboard, not the sheet), and
   right-click the `Redemptions` tab → *Protect sheet* → only you.
3. **Paste the Apps Script** from [`design/LOGGING.md`](design/LOGGING.md)
   into the Sheet (Extensions → Apps Script). Set `PROGRAM_KEY` to one long
   random string — **the only secret in the whole system** (backups, card
   checksums, and register QRs all derive from it); save it somewhere safe.
   Deploy → New deployment → Web app, *Execute as: me*,
   *Access: anyone*. Copy the `/exec` URL. Run `nightlySnapshot` once to
   authorize it, then add a daily time-driven trigger for it (Triggers → Add).
   While you're there, add a weekly time-driven trigger for `weeklyDigest`
   (Monday morning) so the coordinator gets the week-in-review email.
4. **Configure this repo** (marked `CONFIG` blocks at the top of each file):
   - [`redeem/index.html`](redeem/index.html): `SCRIPT_URL` = the `/exec` URL; fill the
     `SHOPS` map (slug → display name), and optionally seed the `BARS` roster
     used by the admin pack check-out.
   - [`dashboard/index.html`](dashboard/index.html): the same `SCRIPT_URL`.
   Commit and merge to `main` — Pages redeploys automatically.
5. **Print things** — follow [`PRINTING.md`](PRINTING.md): generate the
   card books and pack cover sheets with `tools/build_cards.py`, make one
   register QR per coffee shop, and use the RFQ + pre-flight checklist
   there when ordering.
6. **Dashboards** — the built-in one is live immediately at
   [`/dashboard/`](https://knoxpickmeup.org/dashboard/) (unlinked and unindexed; share the URL
   freely). Optionally build a Looker Studio view on the Sheet for partners
   who want to slice data themselves.
7. **Turn on backups** — repo Settings → Secrets and variables → Actions →
   add `BACKUP_URL` (the `/exec` URL) and `PROGRAM_KEY` (the same one
   secret). Run the *Nightly data backup* workflow once by hand
   (Actions tab → Run workflow) and confirm a commit touching
   `data/backup/*.csv` appears.
8. **Dry-run** with one friendly bar and one shop before the pilot: open the
   scanner's admin mode, check a pack out to the bar, scan a card at a
   register, and watch it land on the dashboard.

## Backups — "what if someone breaks the sheet?"

Four independent layers, detailed in
[`design/LOGGING.md`](design/LOGGING.md#h-backups--disaster-recovery):

1. **Sheet version history** (built into Google) — one-click restore for bad
   edits; covers 95% of accidents.
2. **Nightly Drive snapshots** — the Apps Script copies the whole file into
   a "KPU Backups" folder daily, keeping 30 dated copies.
3. **Nightly off-Google backup** — a GitHub Action pulls every tab and
   commits CSVs to [`data/backup/`](data/backup) in this repo; **git history
   is the archive**, so any past day is recoverable even if the entire
   Google account is lost. If the backup breaks, the Action fails and
   GitHub emails you — that's the whole monitoring system.
4. **Paper** — pack cover sheets carry a hand-written bar/date line, and
   every card is dated by hand.

Losing the whole Google account costs under an hour: rebuild the Sheet from
the repo's CSVs, re-paste the script, update `SCRIPT_URL` in two files.

## Publishing the site

Every push to `main` republishes <https://knoxpickmeup.org/> automatically, via
the *Deploy site* workflow ([`.github/workflows/deploy-pages.yml`](.github/workflows/deploy-pages.yml)).
There is still no build step — the workflow uploads the repo as-is; its one job
is to inject the `CARTO_TILE_URL` secret into the map so the CARTO API key never
lands in git. Unset the secret and the site falls back to CARTO's keyless public
basemap, so local checkouts and forks work unchanged.

This requires **Settings → Pages → Source = GitHub Actions**; the setup, and
which credentials here are public-by-design versus genuinely secret, are in
[`design/ANALYTICS.md`](design/ANALYTICS.md#keys--secrets--whats-public-by-design).
