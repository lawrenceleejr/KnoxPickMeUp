"""Two-sided coaster generator — the night side and the day side of the story.

NIGHT side (faces up under the drink, at the bar): the participating BARS run
around the rim, and the center walks the patron through the decision they're
about to make — leave the car overnight, book a ride home, free coffee when
they come back for it in the morning.

DAY side (the flip): the participating COFFEE SHOPS run around the rim, with
a QR to the program site in the center — where the card gets redeemed.

Venue lists, the QR target, and the center logo are all configurable; with no
flags it builds a sample pair from the demo roster using the brand mark.

Usage:
  pip install fonttools brotli uharfbuzz segno cairosvg
  python3 tools/build_coasters.py \
      --bars "Preservation Pub, Barley's Taproom, Suttree's" \
      --shops "Remedy Coffee, Wild Love Bakehouse, K Brew" \
      --sponsor path/to/sponsor-logo.svg \
      --qr-url https://knoxpickmeup.org/

  --logo REPLACES the center brand mark; --sponsor ADDS a small logo in a
  "printing donated by" slot below the website and leaves the mark in place.

Outputs print/coasters/coaster-night.svg and coaster-day.svg (gitignored —
print artifacts). All type is converted to outlines, like every other piece
of collateral, so any print shop can run the files as-is. Coaster spec is in
PRINTING.md (pulpboard, 3.5-4 in round, flat color).
"""
import argparse, math, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_collateral import (PAPER, INK, INK2, NIGHT, NIGHT2, ORANGE,
                              ORANGE_INK, GOLD, RULE, NIGHT_RULE, SITE, SITE_LABEL,
                              text, arc_text, svg, mark, mark_w, qr_svg, embed_svg,
                              place, sponsor_row, write_pdf, quiet_pad, tag_url,
                              fraunces, fraunces_it, inter6, inter4)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# geometry — 420 units = 4 in round coaster (105 units/in)
W = 420
UPI = 105        # user units per inch, for true-size PDF export
CX = CY = 210
R_EDGE, R_RING, R_INNER, R_NAMES = 204, 192, 158, 175


def qr_panel(cx, top_y, size, qr_url):
    """A white rounded card with the QR on it — reads on either field."""
    pad = quiet_pad(qr_url, size)   # mandatory 4-module quiet zone
    box = size + pad * 2
    return (f'<rect x="{cx - box / 2:.1f}" y="{top_y:.1f}" width="{box}" height="{box}" rx="5" '
            f'fill="#ffffff" stroke="{RULE}" stroke-width="1"/>'
            + qr_svg(qr_url, cx - size / 2, top_y + pad, size))


def logo(cx, top_y, h, logo_path, on_dark):
    """Center logo slot: the supplied SVG if configured, else the brand mark
    in the side's ink (paper silhouette on night, ink on paper)."""
    if logo_path:
        frag, w = embed_svg(logo_path, h)
        return place(frag, cx - w / 2, top_y)
    return mark(cx - mark_w(h) / 2, top_y, h,
                shield=(PAPER if on_dark else INK),
                cup=(NIGHT if on_dark else PAPER))


def chord(y, pad=16):
    """Usable line width inside the inner ring at baseline y."""
    dy = y - CY
    return 2 * math.sqrt(max(R_INNER * R_INNER - dy * dy, 0)) - pad


def fit(face, s, size, max_w, tracking=0.0, min_size=8):
    """Largest size <= the requested one at which s fits in max_w."""
    while size > min_size and face.shape(s, size, letterspacing=tracking)[1] > max_w:
        size -= 0.25
    return size


NAME_TRACK = 0.18  # letterspacing for rim names (em fraction, matches labels)


def _arc_w(face, s, size):
    ws = [face.shape(ch, size)[1] for ch in s]
    return sum(ws) + NAME_TRACK * size * (len(s) - 1)


def ring_names(names, face, base_size, fill, dot, max_arc_deg=152):
    """Venue names around the rim: first half across the top arc, the rest
    across the bottom (both reading upright), separated by accent dots.
    Auto-shrinks until each group fits its arc."""
    names = [n.upper() for n in names]
    split = math.ceil(len(names) / 2)
    out = []
    for group, mode in ((names[:split], 'top'), (names[split:], 'bottom')):
        if not group:
            continue
        size = base_size
        while True:
            widths = [_arc_w(face, n, size) for n in group]
            gap = size * 2.4                      # arc px between names
            total = sum(widths) + gap * (len(group) - 1)
            if math.degrees(total / R_NAMES) <= max_arc_deg or size <= 8:
                break
            size -= 0.5
        if math.degrees(total / R_NAMES) > max_arc_deg:
            print(f'WARNING: {len(group)} names do not fit the {mode} arc even at '
                  f'{size}px — consider shorter names or fewer venues per coaster')
        deg = -math.degrees(total / R_NAMES) / 2  # group centered on the arc
        for i, (name, w) in enumerate(zip(group, widths)):
            wdeg = math.degrees(w / R_NAMES)
            out.append(arc_text(face, name, size, CX, CY, R_NAMES, fill,
                                tracking=NAME_TRACK, mode=mode,
                                center_deg=deg + wdeg / 2))
            if i < len(group) - 1:               # dot in the middle of the gap
                mid = math.radians(deg + wdeg + math.degrees(gap / R_NAMES) / 2)
                px = CX + R_NAMES * math.sin(mid)
                py = CY - R_NAMES * math.cos(mid) if mode == 'top' else CY + R_NAMES * math.cos(mid)
                out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="2.4" fill="{dot}"/>')
            deg += wdeg + math.degrees(gap / R_NAMES)
    return ''.join(out)


def night_side(bars, logo_path, qr_url, sponsor=''):
    """The bar side: navy field, bars around the rim, the three steps and a
    QR in the center — for someone already out, deciding about the car."""
    b = []
    b.append(f'<circle cx="{CX}" cy="{CY}" r="{R_EDGE}" fill="{NIGHT}" stroke="{NIGHT2}" stroke-width="1.5"/>')
    b.append(f'<circle cx="{CX}" cy="{CY}" r="{R_RING}" fill="none" stroke="{ORANGE}" stroke-width="2"/>')
    b.append(f'<circle cx="{CX}" cy="{CY}" r="{R_INNER}" fill="none" stroke="{NIGHT_RULE}" stroke-width="1"/>')
    b.append(ring_names(bars, inter6, 13, GOLD, ORANGE))
    b.append(logo(CX, 76, 30, logo_path, on_dark=True))
    hsz = fit(fraunces, 'Drove downtown tonight?', 24, chord(136))
    b.append(text(fraunces, 'Drove downtown tonight?', hsz, CX, 136, PAPER, anchor='middle')[0])
    steps = [
        'Leave the car — municipal garages are free overnight.',
        'Book a ride home. Show your bartender.',
        'Free coffee when you’re back in the morning.',
    ]
    # the whole block fits the tightest of its three rows, numeral included
    indent, ssz = 18, 10.5
    row_w = min(chord(164 + i * 21) for i in range(len(steps)))
    ssz = min(fit(inter4, s, ssz, row_w - indent) for s in steps)
    x0 = CX - (max(inter4.shape(s, ssz)[1] for s in steps) + indent) / 2
    for i, s in enumerate(steps):
        y = 164 + i * 21
        b.append(text(fraunces, str(i + 1), 16, x0, y, ORANGE)[0])
        b.append(text(inter4, s, ssz, x0 + indent, y - 2, PAPER)[0])
    b.append(qr_panel(CX, 216, 60, qr_url))
    b.append(text(inter6, 'SCAN FOR SHOPS, HOURS + THE PROGRAM', 8, CX, 302, GOLD, tracking=0.14, anchor='middle')[0])
    b.append(text(fraunces, SITE_LABEL, 14, CX, 322, PAPER, anchor='middle')[0])
    if sponsor:
        b.append(sponsor_row(CX, 344, sponsor, 'PRINTING DONATED BY', GOLD, h=12))
    return svg(W, W, ''.join(b),
               'Knox Pick-Me-Up coaster, night side — leave the car overnight, '
               'book a ride home, free coffee in the morning; participating bars '
               'around the rim, QR to the program site')


def day_side(shops, logo_path, qr_url, sponsor=''):
    """The morning side: paper field, coffee shops around the rim, and a QR to
    the program site in the center."""
    b = []
    b.append(f'<circle cx="{CX}" cy="{CY}" r="{R_EDGE}" fill="{PAPER}" stroke="{RULE}" stroke-width="1.5"/>')
    b.append(f'<circle cx="{CX}" cy="{CY}" r="{R_RING}" fill="none" stroke="{ORANGE_INK}" stroke-width="2"/>')
    b.append(f'<circle cx="{CX}" cy="{CY}" r="{R_INNER}" fill="none" stroke="{GOLD}" stroke-width="1"/>')
    b.append(ring_names(shops, inter6, 13, INK, ORANGE))
    b.append(logo(CX, 88, 30, logo_path, on_dark=False))
    hsz = fit(fraunces, 'Back for your car?', 26, chord(156))
    b.append(text(fraunces, 'Back for your car?', hsz, CX, 156, INK, anchor='middle')[0])
    sub = 'That card is a free large coffee — and your KAT fare.'
    b.append(text(fraunces_it, sub, fit(fraunces_it, sub, 12.5, chord(180)), CX, 180, ORANGE_INK, anchor='middle')[0])
    b.append(qr_panel(CX, 198, 76, qr_url))
    b.append(text(inter6, 'SCAN FOR SHOPS, HOURS + THE PROGRAM', 8, CX, 308, INK2, tracking=0.14, anchor='middle')[0])
    b.append(text(fraunces, SITE_LABEL, 14, CX, 330, INK, anchor='middle')[0])
    if sponsor:
        b.append(sponsor_row(CX, 349, sponsor, 'PRINTING DONATED BY', INK2, h=12))
    return svg(W, W, ''.join(b),
               'Knox Pick-Me-Up coaster, day side — free large coffee with your card; '
               'participating coffee shops around the rim, QR to the program site')


def split_list(s):
    return [v.strip() for v in s.split(',') if v.strip()]


def main():
    ap = argparse.ArgumentParser(description='Build the two-sided Knox Pick-Me-Up coaster.')
    ap.add_argument('--bars', default='Preservation Pub, Barley’s Taproom, Suttree’s, '
                                      'Peter Kern Library, Boyd’s Jig & Reel',
                    help='comma-separated bars for the night-side rim')
    ap.add_argument('--shops', default='Remedy Coffee, Wild Love Bakehouse, K Brew, Honeybee Coffee',
                    help='comma-separated coffee shops for the day-side rim')
    ap.add_argument('--logo', default='',
                    help='path to an SVG to use as the center logo on both sides '
                         '(default: the brand mark, in each side’s ink) — REPLACES the mark')
    ap.add_argument('--sponsor', default='',
                    help='path to a sponsor logo SVG — rides in a small "printing '
                         'donated by" slot below the website (mark stays; does NOT '
                         'replace it, unlike --logo)')
    ap.add_argument('--qr-url', default=f'{SITE}#findus',
                    help='URL both QRs encode (both sides carry a QR and the '
                         'website)')
    ap.add_argument('--src', default='coaster',
                    help='channel tag added to the QR URL as ?src=… for Cloudflare '
                         'attribution (empty to disable). See design/ANALYTICS.md')
    ap.add_argument('--out', default=os.path.join(REPO, 'print', 'coasters'),
                    help='output directory')
    args = ap.parse_args()
    for flag, val in (('--logo', args.logo), ('--sponsor', args.sponsor)):
        if val and not os.path.isfile(val):
            ap.error(f'{flag} file not found: {val}')

    qr = tag_url(args.qr_url or f'{SITE}#findus', args.src)   # both sides carry the QR
    os.makedirs(args.out, exist_ok=True)
    # 420 units = 4 in round  ->  105 user-units per inch
    for name, svg_str in (('coaster-night', night_side(split_list(args.bars), args.logo, qr, args.sponsor)),
                          ('coaster-day', day_side(split_list(args.shops), args.logo, qr, args.sponsor))):
        svg_f = os.path.join(args.out, name + '.svg')
        open(svg_f, 'w').write(svg_str)
        write_pdf(svg_str, os.path.join(args.out, name + '.pdf'), UPI)
        print(f'{name:14s} -> {svg_f}  (+ .pdf)')
    print('Print as a 4 in round, 2-sided pulpboard coaster — see PRINTING.md.')


if __name__ == '__main__':
    main()
