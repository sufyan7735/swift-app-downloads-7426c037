import re
"""Rebuild Arabic UF5000 datasheet (RTL) from the English original.
Fonts: IBM Plex Sans Arabic in /tmp/cat/f (Bold/SemiBold/Regular)."""
import pymupdf

SRC = '/dev-server/public/catalogs/pylontech-uf5000.pdf'
DST = '/dev-server/public/catalogs/official-ar/pylontech-uf5000.pdf'
ARCH = pymupdf.Archive('/tmp/cat/f')
CSS = """
@font-face{font-family:AR;font-weight:400;src:url(IBMPlexSansArabic-Regular.ttf)}
@font-face{font-family:AR;font-weight:600;src:url(IBMPlexSansArabic-SemiBold.ttf)}
@font-face{font-family:AR;font-weight:700;src:url(IBMPlexSansArabic-Bold.ttf)}
*{font-family:AR;margin:0;padding:0;line-height:1.15;color:#22180f}
"""
W = pymupdf.pdfcolor['white']
L, R = 66.2, 532.0          # table edges
VC = L + R - 364.0          # mirrored value-column centre
SPLIT = 330.0               # labels right of this, values left of it
SUBX = L + R - 111.16       # mirrored sub-row line end

src = pymupdf.open(SRC)
clean = pymupdf.open(SRC)
p = clean[0]
for r in [(0, 20, 548, 48), (40, 120, 560, 200), (40, 270, 560, 700)]:
    p.add_redact_annot(pymupdf.Rect(r))
p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)

out = pymupdf.open()
pg = out.new_page(width=p.rect.width, height=p.rect.height)
pg.show_pdf_page(pg.rect, clean, 0)
for r in [(200, 22, 548, 48), (40, 120, 560, 200), (40, 270, 560, 700)]:
    pg.draw_rect(r, color=None, fill=W)
# move feature icons to mirrored positions
for (x0, y0, x1, y1) in [(58, 130, 86, 158), (58, 166, 86, 194), (322, 126, 352, 158), (322, 166, 352, 194)]:
    nx0 = p.rect.width - x1
    pg.show_pdf_page(pymupdf.Rect(nx0, y0, nx0 + (x1 - x0), y1), src, 0, clip=pymupdf.Rect(x0, y0, x1, y1))


def box(rect, text, size, weight=400, align='right'):
    import re
    rtl = bool(re.search('[\u0600-\u06FF]', text))
    if rtl and align in ('right', 'left'): align = 'left' if align == 'right' else 'right'
    html = f'<div dir="{'rtl' if rtl else 'ltr'}" style="font-size:{size}pt;font-weight:{weight};text-align:{align}">{text}</div>'
    pg.insert_htmlbox(pymupdf.Rect(rect), html, css=CSS, archive=ARCH)


FONTS = {w: pymupdf.Font(fontfile=f'/tmp/cat/f/IBMPlexSansArabic-{n}.ttf') for w, n in [(400, 'Regular'), (600, 'SemiBold'), (700, 'Bold')]}


import uharfbuzz as hb
_HB = {}


def hbw(t, w, size):
    if w not in _HB:
        n = {400: 'Regular', 600: 'SemiBold', 700: 'Bold'}[w]
        face = hb.Face(hb.Blob.from_file_path(f'/tmp/cat/f/IBMPlexSansArabic-{n}.ttf'))
        _HB[w] = (hb.Font(face), face.upem)
    font, upem = _HB[w]
    buf = hb.Buffer(); buf.add_str(t); buf.guess_segment_properties(); hb.shape(font, buf, {})
    return sum(p.x_advance for p in buf.glyph_positions) * size / upem


def ltr(t):
    return t


def seq(pieces, y0, size, weight=400, right=None, center=None):
    """pieces in visual right-to-left order; each laid out separately so bidi can't reorder them"""
    f = FONTS[weight]; gap = size * 0.3
    ws = [hbw(t, weight, size) for t in pieces]
    tot = sum(ws) + gap * (len(ws) - 1)
    x = right if right is not None else center + tot / 2
    for t, w in zip(pieces, ws):
        if re.search('[\u0600-\u06FF]', t):
            box((x - w - 6, y0, x + 6, y0 + size * 2), t, size, weight, 'center')
        else:
            n = {400: 'Regular', 600: 'SemiBold', 700: 'Bold'}[weight]
            pg.insert_text((x - w, y0 + size * 1.02), t, fontsize=size, fontname='F' + n,
                           fontfile=f'/tmp/cat/f/IBMPlexSansArabic-{n}.ttf', color=(0.135, 0.094, 0.082))
        x -= w + gap

# header (teal square kept on the right)
box((250, 26, 545, 46), '<b>بطارية جهد منخفض</b> / تُركَّب في خزانة (رف)', 10, 400)
# features (right column icon at ~509-537, left column at ~243-273)
box((300, 135, 503, 160), 'مرنة للاستخدام المختلط', 15, 700)
seq(['متوافقة مع خزائن', '19 inch'], 171, 15, 700, right=503)
box((40, 135, 238, 160), 'قابلة للتوسعة بحرية', 15, 700)
box((40, 171, 238, 196), 'فعالية فائقة من حيث التكلفة', 15, 700)
# table head
box((SPLIT, 272, R, 298), 'الوحدة', 15, 400)
box((VC - 80, 278, VC + 80, 298), ltr('UF5000'), 9, 600, 'center')

C = lambda a, b: ['من', a + ' °C', 'إلى', b + ' °C']
rows = [
    ('الجهد الاسمي (VDC)', ltr('51.2')),
    ('سعة وحدة البطارية (kWh)', ltr('5.12')),
    ('السعة القابلة للاستخدام (kWh)', ltr('4.864')),
    (['الأبعاد', '(W*D*H mm)'], ltr('442*452.6*161')),
    ('الوزن (kg)', ltr('42')),
    ('عمق التفريغ', ltr('95%')),
    None, None, None,
    ('منفذ الاتصال', ltr('RS485/CAN')),
    ('درجة الحماية', ltr('IP20')),
    ('عدد الوحدات في السلسلة الواحدة (pcs)', ltr('20')),
    ('درجة حرارة التشغيل – الشحن', C('−10', '+55')),
    ('درجة حرارة التشغيل – التفريغ', C('−10', '+55')),
    ('درجة حرارة التخزين', C('−20', '+60')),
    ('الرطوبة النسبية (RH)', ['من', '5%', 'إلى', '95%', 'بدون تكثّف']),
    ('تيار القصر / مدته (A)', ltr('&lt;2000/1ms')),
    ('الارتفاع عن سطح البحر (m)', ltr('≤4000')),
    (['العمر التصميمي عند', '25 °C'], '15 سنة'),
    (['عمر الدورات عند', '25 °C'], ltr('&gt;6,000')),
    ('الشهادات', ltr('IEC62619/UN38.3/RoHS/Reach/WEEE/MSDS')),
]
top, h = 305.86, 17.97
col = (0.135, 0.094, 0.082)
pg.draw_line((L, top), (R, top), color=col, width=0.5)
for i, row in enumerate(rows):
    y0, y1 = top + i * h, top + (i + 1) * h
    full = row is not None or i == 8
    pg.draw_line((L if full else L, y1), (R if full else SUBX, y1), color=col, width=0.5)
    if row:
        lab, val = row
        if isinstance(lab, list): seq(lab, y0 + 3.5, 7.5, 600, right=R - 2)
        else: box((SPLIT - 10, y0 + 3.5, R, y1), lab, 7.5, 600)
        if isinstance(val, list): seq(val, y0 + 3.5, 7.5, 400, center=VC)
        else: box((L, y0 + 3.5, 2 * VC - L, y1), val, 7.5, 400, 'center')
# merged charge/discharge rows 6-8
m0 = top + 6 * h
box((SUBX + 2, m0 + 14, R, m0 + 3 * h), 'تيار الشحن /<br>التفريغ (A)', 7.5, 600)
for k, (lab, val) in enumerate([('(اعتيادي)', '100'), ('(أقصى)', '100'), ('(ذروة)', '121~200@15sec')]):
    y0 = m0 + k * h
    box((SUBX - 90, y0 + 3.5, SUBX - 6, y0 + h), lab, 7.5, 400)
    box((L, y0 + 3.5, 2 * VC - L, y0 + h), ltr(val), 7.5, 400, 'center')

out.subset_fonts()
out.save(DST, garbage=3, deflate=True)
out[0].get_pixmap(dpi=110).save('/tmp/cat/uf-new.png')
print('ok')
