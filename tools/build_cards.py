"""Batch-generate print-ready Morning Pick-Me-Up cards and pack cover sheets.

Each card gets a unique serial and a unique QR. The QR encodes a URL on the
public site with the serial embedded (?c=KPMU-...#findus):
  - a PATRON who scans it lands on the shop map — the places that redeem it;
  - a SHOP scanning it from the redeem/ scanner has the serial read straight off it.

Each pack of PACK_SIZE cards gets a cover sheet whose QR opens the scanner's
admin pack check-out (redeem/?pack=…), pre-loaded with the pack and its card
range, so whoever hands the pack to a bar just scans it and picks the bar.

Usage:
  pip install fonttools brotli uharfbuzz segno cairosvg
  python3 tools/build_cards.py --year 2026 --start 1 --count 100
Outputs to print/cards/ and print/packs/ (gitignored — print artifacts).
See design/LOGGING.md for the full system.
"""
import argparse, math, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_collateral import (PAPER, INK, INK2, NIGHT, ORANGE, ORANGE_INK, GOLD,
                              RULE, NIGHT_RULE, SITE, text, svg, mark, qr_svg,
                              sponsor_row, write_pdf, fraunces, fraunces_it, inter6, inter4)
from serials import DEMO_KEY, derive_ck_key, serial_letter

# ================= CONFIG =================
PACK_SIZE = 50
UPI = 150        # cards 525x300 = 3.5x2 in; pack sheets 525x700 = 3.5x4.67 in
# ==========================================

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def card_svg(serial):
    url = f'{SITE}?c={serial}#findus'
    b = []
    b.append(f'<rect x="1" y="1" width="523" height="298" rx="14" fill="{PAPER}" stroke="{RULE}" stroke-width="1.5"/>')
    b.append(f'<path d="M15 1.75 H510 a13 13 0 0 1 13.25 13.25 V22 H1.75 V15 A13 13 0 0 1 15 1.75 Z" fill="{ORANGE}"/>')
    b.append(mark(26, 40, 40))
    b.append(text(fraunces, 'Knox Pick-Me-Up', 23, 82, 68, INK)[0])
    b.append(text(inter6, 'MORNING PICK-ME-UP CARD', 9, 499, 64, ORANGE_INK, tracking=0.18, anchor='end')[0])
    b.append(f'<line x1="26" y1="92" x2="499" y2="92" stroke="{RULE}" stroke-width="1"/>')
    b.append(text(fraunces, 'Free large coffee', 36, 26, 148, INK)[0])
    b.append(text(fraunces_it, 'You made the safe call. Your second brew’s on us.', 14.5, 26, 174, INK2)[0])
    rows = [
        [('One large coffee at a participating shop — while supplies last', inter4, INK2)],
        [('Hair of the KAT', inter6, ORANGE_INK),
         (' — your KAT bus fare while this card is valid', inter4, INK2)],
        [('One per ride · Extras are on you · Not for resale · No cash value', inter4, INK2)],
    ]
    for i, segs in enumerate(rows):
        y = 202 + i * 19
        b.append(f'<rect x="26" y="{y-3.5}" width="7" height="1.5" fill="{ORANGE}"/>')
        x = 41
        for seg, face, col in segs:
            pth, w = text(face, seg, 11, x, y, col)
            b.append(pth)
            x += w
    b.append(f'<rect x="397" y="104" width="102" height="102" rx="4" fill="#ffffff" stroke="{RULE}" stroke-width="1"/>')
    b.append(qr_svg(url, 407, 114, 82))
    b.append(text(inter6, 'SCAN FOR PARTICIPATING', 6.8, 499, 222, INK2, tracking=0.16, anchor='end')[0])
    b.append(text(inter6, 'BUSINESSES', 6.8, 499, 233, INK2, tracking=0.16, anchor='end')[0])
    b.append(f'<line x1="26" y1="252" x2="499" y2="252" stroke="{RULE}" stroke-width="1"/>')
    # blank line is where the server writes today's date at hand-out — that
    # date is both the issue date and the start of the one-day validity window
    b.append(text(inter6, 'DATE ISSUED · VALID ONE DAY', 9.5, 26, 274, INK, tracking=0.14)[0])
    b.append(f'<line x1="211" y1="276" x2="345" y2="276" stroke="{INK2}" stroke-width="1"/>')
    b.append(text(inter4, f'Nº {serial}', 9.5, 499, 274, INK2, tracking=0.04, anchor='end')[0])
    return svg(525, 300, ''.join(b),
               f'Knox Pick-Me-Up — Morning Pick-Me-Up Card {serial}')


def card_back_svg(sponsor=''):
    """Static back — identical on every card, so printers run it as one plate.
    The night side of the story: navy field, the mark, and how it works. An
    optional `sponsor` SVG rides in a small slot above the footer rule; the
    program mark is never displaced."""
    b = []
    b.append(f'<rect x="1" y="1" width="523" height="298" rx="14" fill="{NIGHT}" stroke="{NIGHT}" stroke-width="1.5"/>')
    b.append(f'<path d="M15 298.25 H510 a13 13 0 0 0 13.25 -13.25 V278 H1.75 v7 A13 13 0 0 0 15 298.25 Z" fill="{ORANGE}"/>')
    # header: mark + wordmark + tagline
    b.append(mark(26, 34, 44, shield=PAPER, cup=NIGHT))
    b.append(text(fraunces, 'Knox Pick-Me-Up', 24, 86, 58, PAPER)[0])
    b.append(text(fraunces_it, 'Ride from last call to first cup.', 14.5, 86, 80, GOLD)[0])
    b.append(f'<line x1="26" y1="100" x2="499" y2="100" stroke="{NIGHT_RULE}" stroke-width="1"/>')
    # how it works — three numbered lines
    steps = [
        ('1', 'Booked a safe ride home? Show your bartender before you leave.'),
        ('2', 'Sleep easy — most municipal garages & lots are free evenings & weekends.'),
        ('3', 'Ride KAT back free on this card — coffee’s on us.'),
    ]
    for i, (num, line) in enumerate(steps):
        y = 132 + i * 34
        b.append(text(fraunces, num, 22, 26, y, ORANGE)[0])
        b.append(text(inter4, line, 11.5, 48, y - 3, PAPER)[0])
    # optional sponsor slot: a small logo on a white chip, centered in the gap
    # above the footer rule — mark and steps untouched
    if sponsor:
        b.append(sponsor_row(262.5, 216, sponsor, 'PRINTING DONATED BY', GOLD, h=14))
    b.append(f'<line x1="26" y1="232" x2="499" y2="232" stroke="{NIGHT_RULE}" stroke-width="1"/>')
    # footer: partnership + website
    b.append(text(inter6, 'A ROAD-SAFETY PARTNERSHIP · CITY OF KNOXVILLE · KPD · KAT', 7.5, 26, 254, GOLD, tracking=0.14)[0])
    b.append(text(inter4, 'knoxpickmeup.org · hello@knoxpickmeup.org — shops, details, and the fine print', 9.5, 26, 270, '#b9b3a4')[0])
    return svg(525, 300, ''.join(b),
               'Knox Pick-Me-Up card back — how it works, partnership line, and website')


def pack_serial(year, pack_no):
    # Pack serials carry a leading "P" (KPMU-YYYY-P####) so a pack can never be
    # mistaken for a card (KPMU-YYYY-########X) anywhere in the data or by eye.
    return f'KPMU-{year}-P{pack_no:04d}'


def pack_svg(year, pack_no, first, last, size=PACK_SIZE):
    pk = pack_serial(year, pack_no)
    b = []
    b.append(f'<rect width="525" height="700" fill="{PAPER}" stroke="{RULE}" stroke-width="1.5"/>')
    b.append(f'<rect width="525" height="16" fill="{ORANGE}"/>')
    b.append(mark(40, 52, 56))
    b.append(text(fraunces, 'Knox Pick-Me-Up', 30, 118, 92, INK)[0])
    b.append(text(inter6, f'CARD PACK · {size} CARDS', 11, 40, 142, ORANGE_INK, tracking=0.16)[0])
    b.append(f'<line x1="40" y1="162" x2="485" y2="162" stroke="{RULE}" stroke-width="1"/>')
    b.append(text(inter6, 'PACK SERIAL', 9, 40, 190, INK2, tracking=0.18)[0])
    b.append(text(fraunces, pk, 26, 40, 222, INK)[0])
    b.append(text(inter6, 'CARD SERIALS', 9, 40, 254, INK2, tracking=0.18)[0])
    b.append(text(fraunces, f'{first}', 20, 40, 282, INK)[0])
    b.append(text(fraunces, f'through  {last}', 20, 40, 310, INK)[0])
    b.append(f'<line x1="40" y1="336" x2="485" y2="336" stroke="{RULE}" stroke-width="1"/>')
    # The QR opens the scanner's admin check-out (redeem/?pack=…) pre-loaded
    # with this pack and its card range; the volunteer just picks the bar and
    # submits. The same QR is what the in-app admin scanner reads.
    checkout_url = f'{SITE}redeem/?pack={pk}&first={first}&last={last}'
    b.append(text(inter6, 'CHECKING THIS PACK OUT TO A BAR?', 11, 40, 366, INK, tracking=0.14)[0])
    b.append(qr_svg(checkout_url, 40, 382, 160))
    b.append(text(inter4, 'Scan it: pick the bar, submit. Ten seconds.', 12, 222, 414, INK2)[0])
    b.append(text(inter4, 'Ties every card in this pack to that bar for the', 12, 222, 434, INK2)[0])
    b.append(text(inter4, 'monthly numbers — no other paperwork.', 12, 222, 454, INK2)[0])
    b.append(f'<line x1="40" y1="560" x2="485" y2="560" stroke="{RULE}" stroke-width="1"/>')
    b.append(text(inter6, 'BAR', 9, 40, 592, INK2, tracking=0.18)[0])
    b.append(f'<line x1="80" y1="592" x2="300" y2="592" stroke="{INK2}" stroke-width="1"/>')
    b.append(text(inter6, 'DATE', 9, 330, 592, INK2, tracking=0.18)[0])
    b.append(f'<line x1="378" y1="592" x2="485" y2="592" stroke="{INK2}" stroke-width="1"/>')
    b.append(text(inter4, 'Backup for the QR: write it down and text a photo to the program.', 10.5, 40, 630, INK2)[0])
    return svg(525, 700, ''.join(b),
               f'Knox Pick-Me-Up card pack {pk}, card serials {first} to {last}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--year', type=int, default=2026)
    ap.add_argument('--start', type=int, default=1, help='first serial number')
    ap.add_argument('--count', type=int, default=PACK_SIZE, help='how many cards')
    ap.add_argument('--key', default=os.environ.get('KPMU_PROGRAM_KEY', ''),
                    help='the ONE program secret — MUST match PROGRAM_KEY in the '
                         'Apps Script (or set env KPMU_PROGRAM_KEY)')
    ap.add_argument('--out', default=os.path.join(REPO, 'print'),
                    help='output directory (cards/ and packs/ are created inside)')
    ap.add_argument('--force', action='store_true',
                    help='allow a --start that is not the first card of a pack '
                         '(pack cover sheets will be off-boundary — rarely what you want)')
    ap.add_argument('--sponsor', default='',
                    help='optional path to a sponsor logo SVG — rides in a small '
                         '"printing donated by" slot on the card back (mark stays)')
    args = ap.parse_args()
    if args.sponsor and not os.path.isfile(args.sponsor):
        ap.error(f'--sponsor file not found: {args.sponsor}')

    if args.start < 1 or args.count < 1:
        ap.error('--start and --count must both be >= 1')
    # a run should begin on a pack boundary, or pack cover sheets silently
    # overlap/overwrite a previous run's ranges
    if (args.start - 1) % PACK_SIZE != 0 and not args.force:
        ap.error(f'--start {args.start} is not the first card of a pack (packs are '
                 f'{PACK_SIZE} cards, so start must be 1, {PACK_SIZE + 1}, '
                 f'{2 * PACK_SIZE + 1}, …). Pass --force to override.')

    key = args.key or DEMO_KEY
    if key == DEMO_KEY:
        print('WARNING: using the public demo key — fine for samples, '
              'NEVER for a real print run. Pass --key or set KPMU_PROGRAM_KEY.')
    ck = derive_ck_key(key)

    cards_dir = os.path.join(args.out, 'cards')
    packs_dir = os.path.join(args.out, 'packs')
    os.makedirs(cards_dir, exist_ok=True)
    os.makedirs(packs_dir, exist_ok=True)

    serials = [f'KPMU-{args.year}-{n:08d}' for n in range(args.start, args.start + args.count)]
    serials = [b + serial_letter(b, ck) for b in serials]
    def emit(path, svg_str):
        open(path, 'w').write(svg_str)
        write_pdf(svg_str, path[:-4] + '.pdf', UPI)   # true-size print-ready PDF

    for s in serials:
        emit(os.path.join(cards_dir, f'card-{s}.svg'), card_svg(s))
    emit(os.path.join(cards_dir, 'card-back.svg'), card_back_svg(args.sponsor))

    for i in range(0, len(serials), PACK_SIZE):
        chunk = serials[i:i + PACK_SIZE]
        pack_no = (args.start + i - 1) // PACK_SIZE + 1
        emit(os.path.join(packs_dir, f'pack-{pack_serial(args.year, pack_no)}.svg'),
             pack_svg(args.year, pack_no, chunk[0], chunk[-1], size=len(chunk)))

    print(f'{len(serials)} cards -> {cards_dir}  (SVG + print-ready PDF each)')
    print(f'{math.ceil(len(serials)/PACK_SIZE)} pack sheets -> {packs_dir}')
    print('PDFs are true-size with outlined type — hand them straight to any print shop.')


if __name__ == '__main__':
    main()
