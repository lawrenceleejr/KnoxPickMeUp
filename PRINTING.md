# Knox Pick-Me-Up — Printing Guide

Everything needed to take this repo's artwork to a print shop: what to
order, exact specs to quote, how to generate the files, and what to check
before a run. The physical kit is the program — the cards are the
redeemable item, the packs are the fraud control, the coasters are the ad.

> **Ordering for the pilot?** [RFQ-PILOT.md](RFQ-PILOT.md) is the full
> 6-month, 6-venue order — quantities, specs, and a copy-paste quote-form
> request — sized so the resulting quote is the city budget's printing line.

---

## 1. What gets printed

| Piece | Artwork | Quantity logic |
|---|---|---|
| **Card books** (the main event) | `tools/build_cards.py` → `print/cards/` (unique front per card + one static back) | 50 cards/book; 20 books per 1,000 cards |
| **Pack cover sheets** | same script → `print/packs/` (one per book, with pack serial + check-out QR) | 1 per book |
| **Register QRs** (one per coffee shop) | generate per shop, see §5 | 1–2 per shop, laminated |
| **Coasters** (two-sided) | `tools/build_coasters.py` → `print/coasters/` (night side: bars + the three steps; day side: shops; **both sides carry a QR**) · single-sided spot design: [`assets/coaster.svg`](assets/coaster.svg) | thousands — bars burn through them; they're the advertising |
| **Signage** (table tents, window sticker, posters) | `tools/build_signage.py` → `print/signage/` | per venue / community boards |
| **Staff sheets** (barista one-pager, bar onboarding) | `tools/build_staff.py` → `print/staff/` (letter-size) | one laminated behind each bar |
| **Sponsor one-sheet** | `tools/build_sponsor.py` → `print/sponsor/` (letter-size) | outreach leave-behind |
| **Stickers** (laptop / promo) | `tools/build_stickers.py` → `print/stickers/` (a big die-cut mark, and a bold wordmark lockup: name + tagline + website) | giveaways — laptops, water bottles, notebooks |

Optionally, a **sponsor logo** rides in a small "printing donated by" slot on
the card back (`build_cards.py --sponsor logo.svg`) and both coaster sides
(`build_coasters.py --sponsor logo.svg`) — the program mark stays; the sponsor
logo shares the piece, it never replaces it. (`--logo` on the coaster is the
separate *center* slot that **does** replace the mark.)

## 2. The card books — what to ask a printer for

In printer language this is a **raffle-ticket book with variable data**:
perforated tear-off cards, sequential serials, bound in books — one of the
most commoditized products in printing. The only "special" ask is that the
variable data includes a **unique QR per card** (called *variable-data
printing*, VDP), which any digital-press shop can do.

**Copy-paste RFQ:**

> Tear-off card books, 50 cards per book plus a printed cover (artwork
> supplied). Card size 3.5″ × 2″ (quote with and without a 0.75″ bound
> stub). Stock: **14pt uncoated cover** — cards must accept a ballpoint
> pen, so no gloss or UV coating. Ink 4/4: **front carries
> variable data** (unique QR + serial per card, sequential across books;
> print-ready files supplied, one file per card), **back is static** (one
> file, same on every card). Micro-perforation between stub and card (or
> above the binding edge if no stub). Bound by padding or staple at the
> top edge with a chipboard backer; per-book cover sheet supplied.
> Quantity: 1,000 cards / 20 books — please also quote 2,500 and 5,000.

Why each line matters:
- **Uncoated stock** is non-negotiable: at hand-out the bartender **writes
  today's date** on the card's DATE ISSUED line in ballpoint — that's the
  validity control — and glossy or UV-coated stock resists pen ink.
- **Front variable / back static** is what keeps two-sided cheap — VDP is
  priced per variable *side*, and our back
  (`print/cards/card-back.svg`) is deliberately identical on every card.
- **The stub option** is the raffle-book upgrade worth asking about: a
  small bound stub repeats the serial and stays in the book when the card
  is torn out, giving every bar an automatic paper log of what it issued.
  If a printer quotes it cheaply, take it (and ask for the stub artwork —
  the generator can be extended to produce it).
- **Sequential across books** — give the printer the serial order and let
  them collate so book 1 is serials 1–50, book 2 is 51–100, etc. The pack
  cover sheets are generated to match exactly that split.

**Ballpark:** short-run digital VDP books land around **$0.08–0.20 per
card**, so a 1,000-card pilot is roughly **$100–250** — one sponsor
conversation. There's a natural sponsor: a local print shop, credited on
the card backs ("printing donated by ___").

## 3. Who to send it to

- **A local Knoxville commercial printer** — best option, and on-theme as
  a program sponsor. Franchise shops (Minuteman Press, Allegra, etc.)
  handle perforated VDP books routinely. Ask for *"perforated tear-off
  books with variable data."*
- **Online, VDP-capable:** Smartpress (accepts supplied variable-data
  files, does custom perforation and padding); raffle-ticket specialists
  (TicketPrinting.com, Admit One) if they'll take per-card QR art.
- **Coasters:** any custom-coaster house (pulpboard, 4″ round, two-sided
  4/4 — the artwork is flat color). The night side floods navy, so ask for
  a printed sample to check show-through on the board weight.
- **Avoid** pure-template services (Vistaprint-style): generally no
  per-card QR + perforation + books.

## 4. Generating the print files

Every generator writes a **true-size, print-ready PDF** next to each SVG (type
outlined, correct physical dimensions) — hand the PDFs straight to a shop.

```sh
pip install fonttools brotli uharfbuzz segno cairosvg
python3 tools/build_cards.py --year 2026 --start 1 --count 1000 \
    --key 'THE-PROGRAM-KEY'   # same PROGRAM_KEY as in the Apps Script
```

The `--key` (or env `KPMU_PROGRAM_KEY`) is the system's one secret; each
serial's checksum letter derives from it and **must match `PROGRAM_KEY` in
the Apps Script** or every card will scan as invalid. Without it the script
uses a public demo key and prints a loud warning — fine for samples, never
for a real run.

That writes to `print/` (gitignored), each as an SVG **and** a `.pdf`:
- `print/cards/card-KPMU-2026-00000001Q.svg` … — one file per card (front)
- `print/cards/card-back.svg` — the static back, once
- `print/packs/pack-KPMU-2026-P0001.svg` … — one cover sheet per 50

The two-sided coaster is its own generator — venue rosters, the day-side QR
target, and the center logo are flags (defaults build a demo pair with the
brand mark):

```sh
python3 tools/build_coasters.py \
    --bars "Preservation Pub, Barley's Taproom, …" \
    --shops "Remedy Coffee, Wild Love Bakehouse, …" \
    --qr-url https://knoxpickmeup.org/#findus \
    --logo path/to/logo.svg            # both optional — QR defaults to the shop map, logo to the brand mark
# -> print/coasters/coaster-night.svg + coaster-day.svg
```

Rerun it when the roster changes — the rim names auto-shrink to fit, and the
night/day pair is regenerated in one shot. **Both sides** carry a QR to the
program site and the website, so the coaster works face-up either way. The QR is
tagged `?src=coaster` by default so Cloudflare Web Analytics can tell coaster
scans from other channels (`--src` overrides it, `--src ''` disables) — see
[`design/ANALYTICS.md`](design/ANALYTICS.md).

**Venue & community signage** is a third generator — table tents for bar and
cafe tables, a window/door sticker for participating locations, and
letter-size posters for community boards and restrooms:

```sh
python3 tools/build_signage.py --qr-url https://knoxpickmeup.org/#findus
# each writes .svg + .pdf into print/signage/:
#   table-tent       4x10in foldable A-frame (fold at the middle)
#   window-sticker   5.6in round participating-location decal
#   sign-community    8.5x11 poster (bulletin boards)
#   sign-bathroom     8.5x11 poster (restroom / above the sink)
```

Like the coaster, the signage QR is tagged `?src=sign` for channel attribution
(`--src` overrides, `--src ''` disables) — see
[`design/ANALYTICS.md`](design/ANALYTICS.md).

**Staff sheets** are a fourth generator — the letter-size references that go
behind the bar, not in front of patrons:

```sh
python3 tools/build_staff.py
# writes .svg + .pdf into print/staff/:
#   barista-one-pager   the six scan outcomes + what to do, manual entry, offline
#   bar-onboarding      what a bar agrees to, handing out a card, packs, contact
```

Laminate `barista-one-pager` and keep it by the register; the wording of the
scan outcomes is copied from the scanner, so reprint it if the scanner's
banners change.

```sh
python3 tools/build_stickers.py
# writes .svg + .pdf into print/stickers/:
#   sticker-mark       just the mark, ~4in tall (the pin tip stays visible)
#   sticker-wordmark   bold, left-aligned name + tagline + website (die-cut to type)
```

Order them as **die-cut (or kiss-cut) vinyl** from any sticker house. The
artwork sits on a transparent ground with **no border** — the shop cuts to the
outline and adds the white die-cut border and bleed. Cheapest way to put the
brand (and the website) in people's hands.

These are **generic branding items** — one design for every venue, no
per-shop customization. (The only per-shop artifact is the register QR in
§5.) Every piece carries a QR and the website. **In the browser:** the
*Build print materials* GitHub Action (Actions tab → Run workflow) runs the
coaster, signage, and staff-sheet generators together and hands back a
downloadable zip of PDFs — no terminal.

The PDFs are vector with **all type converted to outlines** (no font
substitution at the shop) and at exact physical size.

**Bleed:** artwork is at exact trim size. Edge-bleed pieces — the round
coaster and sticker, the card's orange band and navy back, the tent's top
bar — run color to the trim edge, so a shop will ask for **1/8″ bleed**.
Ask for their template/specs first, then extend the relevant generator to
their bleed + crop-mark spec before the final run (the layouts are
parametric — a small change, not a redesign).

Each pack cover sheet's QR opens the scanner's admin pack check-out
(`redeem/?pack=…`), pre-loaded with the pack and its card range — whoever
delivers the pack picks the bar and submits (see
[`design/LOGGING.md`](design/LOGGING.md)). No form or extra config to set.

## 5. Register QRs (one per coffee shop)

Each shop's counter QR opens the scanner pre-set to that shop:

```sh
CK=$(python3 tools/ckkey.py 'THE-PROGRAM-KEY')   # derived serial-check key
python3 -c "import segno; segno.make(
  'https://knoxpickmeup.org/redeem/?shop=SLUG&k=$CK',
  error='q').save('register-SLUG.png', scale=12, border=2)"
```

The `&k=` value is the **derived** check key — safe on printed paper (it
can't unlock backups or reveal the program key) — and it's what lets the
scanner verify each scanned serial's checksum instantly, even offline.
Use the slugs from the `SHOPS` map in [`redeem/index.html`](redeem/index.html). Print
at ~3″, mount on card stock, laminate. Error level `q` keeps them
scannable when the lamination glares or the corner gets coffee on it.

## 6. Pre-flight checklist (every run)

1. **Serial continuity** — `--start` must be the next unused number
   (check the highest serial in the `Packs` tab or `data/backup/packs.csv`;
   never reprint a live range).
2. **Program key** — `--key` matches the Apps Script's `PROGRAM_KEY`
   (no demo-key warning in the script output), register QRs carry the
   matching `&k=` from `tools/ckkey.py`, and the proof card scans as
   valid, not "serial doesn't check out".
3. **Pack check-out proof** — scan a pack cover sheet's QR: it should open
   the admin check-out with the pack pre-loaded, ready to assign to a bar.
4. **Proof one card end to end**: print `card-…0001` on a desk printer,
   scan its QR with a phone — it must open the public site — then scan it
   from `redeem/?shop=demo-cafe` and see the serial extracted.
5. **Pen test** on the shop's actual stock sample: write a date in ballpoint,
   smudge check after 10 seconds.
6. **QR size sanity**: the card QR prints at about 0.55″ — fine for
   phone cameras, but don't let a shop shrink the card below 3.5″ × 2″.
7. Order **books = cards ÷ 50**, and physically match pack cover sheets
   to books by serial range when they arrive.

---

*Specs live here; the logging system the QRs feed is in
[`design/LOGGING.md`](design/LOGGING.md); brand rules are in
[`BRAND.md`](BRAND.md).*
