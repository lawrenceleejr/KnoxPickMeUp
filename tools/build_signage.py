"""Signage generator — the print pieces that live at participating venues and
around town, all from the same brand system as the cards and coasters.

These are generic branding items — one design for every venue, no per-shop
customization. Builds, into print/signage/ (gitignored), an SVG and a
true-size print-ready PDF for each:
  table-tent      A foldable A-frame table tent (fold at the middle; the top
                  panel prints upside-down so both faces read upright). Sits on
                  bar and cafe tables. 4 x 10 in flat.
  window-sticker  A door/window decal for participating locations — a big
                  mark, the website, and "participating location". 5.6 in round.
  sign-community  A letter-size (8.5 x 11) poster for bulletin boards,
                  break rooms, and community boards.
  sign-bathroom   A letter-size poster written for the captive audience of a
                  restroom stall / above the sink.

All type is converted to outlines (like every other piece of collateral), so
any print shop can run the files as-is.

Usage:
  pip install fonttools brotli uharfbuzz segno cairosvg
  python3 tools/build_signage.py --qr-url https://knoxpickmeup.org/#findus
"""
import argparse, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_collateral import (PAPER, PAPER2, INK, INK2, NIGHT, NIGHT2, ORANGE,
                              ORANGE_INK, GOLD, RULE, SITE, SITE_LABEL, text, svg,
                              mark, mark_w, qr_svg, quiet_pad, write_pdf, tag_url,
                              fraunces, fraunces_it, inter6, inter4)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPI = 100        # signage user units per inch (posters 850x1100 = 8.5x11 in)

STEPS = [
    'Booked a safe ride home? Show your bartender before you leave.',
    'Leave the car — municipal downtown garages are free overnight.',
    'Come back in the morning: a free large coffee, and a free KAT ride to your car.',
]


def qr_card(cx, top_y, size, on_dark=False):
    """A white rounded card with the program QR centered on it."""
    pad = quiet_pad(QR_URL, size)   # mandatory 4-module quiet zone
    box = size + pad * 2
    stroke = RULE if not on_dark else '#ffffff'
    return (f'<rect x="{cx - box / 2:.1f}" y="{top_y:.1f}" width="{box:.1f}" height="{box:.1f}" '
            f'rx="{box * 0.06:.1f}" fill="#ffffff" stroke="{stroke}" stroke-width="1.5"/>'
            + qr_svg(QR_URL, cx - size / 2, top_y + pad, size))


def steps_block(cx, top_y, width, num_size, body_size, gap, num_fill, body_fill):
    """Three numbered how-it-works rows, left-aligned within a centered column."""
    out = []
    indent = num_size * 1.5
    x0 = cx - width / 2
    y = top_y
    for i, s in enumerate(STEPS):
        out.append(text(fraunces, str(i + 1), num_size, x0, y, num_fill)[0])
        # wrap the body to the column width
        for line in wrap(inter4, s, body_size, width - indent):
            out.append(text(inter4, line, body_size, x0 + indent, y, body_fill)[0])
            y += body_size * 1.28
        y += gap
    return ''.join(out), y


def fit(face, s, size, max_w, min_size=10):
    """Largest size <= the requested one at which s fits in max_w."""
    while size > min_size and face.shape(s, size)[1] > max_w:
        size -= 0.5
    return size


def wrap(face, s, size, max_w):
    """Greedy word wrap to max_w (in user units)."""
    words, lines, cur = s.split(' '), [], ''
    for w in words:
        trial = (cur + ' ' + w).strip()
        if face.shape(trial, size)[1] <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


# ============================================================ letter posters
def poster(eyebrow, headline, sub, foot):
    """Letter-size portrait poster (850 x 1100 = 8.5 x 11 in at 100 u/in)."""
    W, H, cx = 850, 1100, 425
    b = [f'<rect width="{W}" height="{H}" fill="{PAPER}"/>',
         f'<rect x="24" y="24" width="{W-48}" height="{H-48}" fill="none" stroke="{RULE}" stroke-width="2"/>',
         f'<rect x="24" y="24" width="{W-48}" height="10" fill="{ORANGE}"/>']
    b.append(mark(cx - mark_w(120) / 2, 66, 120))
    b.append(text(fraunces, 'Knox Pick-Me-Up', 40, cx, 250, INK, anchor='middle')[0])
    b.append(text(inter6, eyebrow, 13, cx, 284, ORANGE_INK, tracking=0.18, anchor='middle')[0])
    # headline (may be two lines, split on a literal newline) — each line fit
    # to the inner width so a longer message can't run off the sheet
    TEXTW = W - 120
    hy = 352
    for line in headline.split('\n'):
        b.append(text(fraunces, line, fit(fraunces, line, 52, TEXTW), cx, hy, INK, anchor='middle')[0])
        hy += 58
    b.append(text(fraunces_it, sub, fit(fraunces_it, sub, 22, TEXTW), cx, hy + 4, ORANGE_INK, anchor='middle')[0])
    steps_svg, steps_end = steps_block(cx, hy + 56, 560, 28, 18, 12, ORANGE, INK2)
    b.append(steps_svg)
    # QR + website, positioned from where the steps actually ended (they wrap,
    # so the end moves) with a guaranteed gap; guard the footer below it
    qsz = 180
    qy = steps_end + 20
    b.append(qr_card(cx, qy, qsz))
    label_y = qy + qsz + 2 * quiet_pad(QR_URL, qsz) + 30
    b.append(text(inter6, 'SCAN — FREE COFFEE FOR A SAFE RIDE HOME', 13, cx, label_y, INK2, tracking=0.14, anchor='middle')[0])
    b.append(text(fraunces, SITE_LABEL, 28, cx, label_y + 34, INK, anchor='middle')[0])
    assert label_y + 34 < H - 70, 'poster copy overflows the footer — shorten a step'
    b.append(text(inter6, foot, 10.5, cx, H - 58, INK2, tracking=0.12, anchor='middle')[0])
    return svg(W, H, ''.join(b), f'Knox Pick-Me-Up poster — {headline.replace(chr(10), " ")}')


# ============================================================ window sticker
def window_sticker():
    """A door/window decal (560 ≈ 5.5 in round) built to read from across the
    street: a big, dominant mark, then a large wordmark and 'participating
    location' beneath — high contrast, one simple circle."""
    S, cx = 560, 280
    b = [f'<circle cx="{cx}" cy="{cx}" r="272" fill="{PAPER}" stroke="{NIGHT}" stroke-width="7"/>',
         f'<circle cx="{cx}" cy="{cx}" r="250" fill="none" stroke="{GOLD}" stroke-width="2"/>']
    # the logo — the hero, sized to read at a distance but nudged down off the
    # ring so the composition breathes inside the disc
    b.append(mark(cx - mark_w(272) / 2, 86, 272))
    b.append(text(fraunces, 'Knox Pick-Me-Up', 43, cx, 430, INK, anchor='middle')[0])
    b.append(text(inter6, 'PARTICIPATING LOCATION', 15.5, cx, 464, ORANGE_INK, tracking=0.22, anchor='middle')[0])
    b.append(text(fraunces_it, SITE_LABEL, 21, cx, 496, INK2, anchor='middle')[0])
    return svg(S, S, ''.join(b),
               'Knox Pick-Me-Up window sticker — participating location, knoxpickmeup.org')


# ============================================================ table tent
def tent_panel():
    """One face of the table tent, drawn in a 400 x 500 local box."""
    W, H, cx = 400, 500, 200
    b = [f'<rect width="{W}" height="{H}" fill="{PAPER}"/>',
         f'<rect y="0" width="{W}" height="8" fill="{ORANGE}"/>']
    b.append(mark(cx - mark_w(80) / 2, 40, 80))
    b.append(text(fraunces, 'Drove here tonight?', 27, cx, 190, INK, anchor='middle')[0])
    b.append(text(fraunces_it, 'Get home safe — coffee’s on us tomorrow.', 14, cx, 216, ORANGE_INK, anchor='middle')[0])
    b.append(qr_card(cx, 244, 128))
    b.append(text(inter6, 'SCAN FOR HOW IT WORKS', 11, cx, 420, INK2, tracking=0.16, anchor='middle')[0])
    b.append(text(fraunces, SITE_LABEL, 20, cx, 452, INK, anchor='middle')[0])
    return ''.join(b)


def table_tent():
    """Foldable A-frame tent, 400 x 1000 (4 x 10 in). Fold at the middle; the
    top panel is rotated 180° so it reads upright once the sheet is folded
    over and stood up."""
    W, H = 400, 1000
    panel = tent_panel()
    b = [f'<rect width="{W}" height="{H}" fill="{PAPER}"/>',
         # bottom panel, upright
         f'<g transform="translate(0,500)">{panel}</g>',
         # top panel, rotated 180° about the sheet's upper-half center
         f'<g transform="translate({W},500) rotate(180)">{panel}</g>',
         # fold guide — a hairline dash across the crease and a small paper
         # label sitting ON the orange band, so nothing knocks a hole in the art
         f'<line x1="0" y1="500" x2="{W}" y2="500" stroke="{NIGHT}" stroke-width="0.75" stroke-dasharray="6 5" opacity="0.5"/>',
         text(inter6, 'FOLD', 7, W / 2, 503.5, PAPER, tracking=0.3, anchor='middle')[0]]
    return svg(W, H, ''.join(b),
               'Knox Pick-Me-Up table tent — foldable A-frame for bar and cafe tables')


def main():
    ap = argparse.ArgumentParser(description='Build Knox Pick-Me-Up signage (tents, stickers, posters).')
    ap.add_argument('--qr-url', default=f'{SITE}#findus',
                    help='URL every QR on the signage encodes')
    ap.add_argument('--src', default='sign',
                    help='channel tag added to the QR URL as ?src=… for Cloudflare '
                         'attribution (empty to disable). See design/ANALYTICS.md')
    ap.add_argument('--out', default=os.path.join(REPO, 'print', 'signage'),
                    help='output directory')
    args = ap.parse_args()

    global QR_URL
    QR_URL = tag_url(args.qr_url or f'{SITE}#findus', args.src)
    os.makedirs(args.out, exist_ok=True)

    pieces = {
        'table-tent.svg': table_tent(),
        'window-sticker.svg': window_sticker(),
        'sign-community.svg': poster(
            'A ROAD-SAFETY PROGRAM FOR DOWNTOWN KNOXVILLE',
            'Ride home tonight.\nCoffee’s on us tomorrow.',
            'A thank-you for keeping our roads safe.',
            'CITY OF KNOXVILLE · KPD · KAT · DOWNTOWN BARS & COFFEE SHOPS'),
        'sign-bathroom.svg': poster(
            'BEFORE YOU HEAD OUT',
            'Not driving home?\nGood call.',
            'Show your bartender your ride — get a free-coffee card.',
            'CITY OF KNOXVILLE · KPD · KAT · DOWNTOWN BARS & COFFEE SHOPS'),
    }
    for name, body in pieces.items():
        svg_f = os.path.join(args.out, name)
        open(svg_f, 'w').write(body)
        write_pdf(body, svg_f[:-4] + '.pdf', UPI)   # true-size print-ready PDF
        print(f'{name:22s} -> {svg_f}  (+ .pdf)')
    print('Print: tent on card stock (fold at the middle); sticker as a window '
          'cling; posters at 8.5 x 11. Print-ready PDFs sit beside each SVG; '
          'all type is outlined and every piece is generic (no per-shop info).')


if __name__ == '__main__':
    main()
