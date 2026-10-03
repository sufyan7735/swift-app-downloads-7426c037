"""Suntech STP595S (Ultra V Pro 580-600W) Arabic catalog, page 2: rebuild the four spec tables
with real text on a uniform row grid so labels, values and rules line up exactly.
usage: python3 fix595.py <in.pdf> <out.pdf>   (fonts: IBMPlexSansArabic-*.ttf in /tmp/cat/f)"""
import sys, pymupdf

F = "/tmp/cat/f"
ARCH = pymupdf.Archive(F)
CSS = """
@font-face{font-family:AR;font-weight:400;src:url(IBMPlexSansArabic-Regular.ttf)}
@font-face{font-family:AR;font-weight:600;src:url(IBMPlexSansArabic-SemiBold.ttf)}
@font-face{font-family:AR;font-weight:700;src:url(IBMPlexSansArabic-Bold.ttf)}
*{font-family:AR;margin:0;padding:0;line-height:1.25}
"""
INK, RULE = "#3a3a3a", (0.62, 0.62, 0.62)


sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import engine  # manual bidi: Arabic and LTR runs are shaped and laid out right-to-left separately


def text(page, x0, x1, cy, s, size=7.0, w=400, align="center", lines=1):
    ls = s.split("\n"); lh = size * 1.3
    for i, ln in enumerate(ls):
        y = cy + (i - (len(ls) - 1) / 2) * lh
        lw = engine.line_width(ln, w, size)
        xr = x1 if align == "right" else (x0 + lw if align == "left" else (x0 + x1) / 2 + lw / 2)
        engine.draw_line(page, xr, y, ln, w, size, INK)


def rule(page, x0, x1, y, width=0.5, color=RULE):
    page.draw_line((x0, y), (x1, y), color=color, width=width)


def grid(page, y0, y1, units):
    """row boundaries for rows whose heights are proportional to units"""
    tot = sum(units); h = (y1 - y0) / tot; ys = [y0]
    for u in units: ys.append(ys[-1] + u * h)
    return ys


def wipe(page, x0, y0, x1, y1):
    page.draw_rect(pymupdf.Rect(x0, y0, x1, y1), color=None, fill=(1, 1, 1))


LAB = (452, 574)  # label column (right edge of every table)


def mechanical(page):
    X0, Y0, Y1 = 238, 116.5, 352
    wipe(page, 236, Y0, 578, 354)
    rows = [
        ("الخلية الشمسية", "سيليكون أحادي البلورة N-type بمقاس 182 mm", 1),
        ("عدد الخلايا", "144 (6 × 24)", 1),
        ("الأبعاد", "2278 × 1134 × 30 mm (89.7 × 44.6 × 1.2 inches)", 1),
        ("الوزن", "32.0 kg (70.5 lbs.)", 1),
        ("الزجاج الأمامي / الخلفي", "زجاج نصف مقسّى بسماكة 2.0+2.0 mm", 1),
        ("كابلات الخرج", "طول (-) 350 mm و(+) 160 mm\nأو بطول حسب الطلب", 2),
        ("صندوق التوصيل", "معيار IP68 مع 3 دايودات تجاوز", 1),
        ("درجة حرارة التشغيل", "-40 °C ~ +85 °C", 1),
        ("أقصى جهد للنظام", "1500 V DC (IEC)", 1),
        ("الموصلات", "STP-XC4", 1),
        ("أقصى تيار للمصهر التسلسلي", "25 A", 1),
        ("تفاوت القدرة", "0/+5 W", 1),
        ("معامل ثنائية الوجه", "(80 ± 5)%", 1),
        ("الإطار", "إطار من سبائك الألومنيوم المؤكسد", 1),
        ("مواصفات التعبئة", "عدد 36 لوحاً لكل منصة نقل\nعدد 720 لوحاً لكل حاوية 40'HC\n2310×1120×1255 mm    1202 kg", 3),
    ]
    units = [1 if n == 1 else 0.55 + 0.6 * n for *_, n in rows]
    ys = grid(page, Y0, Y1, units)
    for i, (lab, val, n) in enumerate(rows):
        cy = (ys[i] + ys[i + 1]) / 2
        text(page, *LAB, cy, lab, size=7.5, w=600, align="right")
        text(page, X0 + 4, 444, cy, val, size=7.2, align="right", lines=n)
        if i < len(rows) - 1:
            rule(page, X0, 576, ys[i + 1])
    rule(page, X0, 576, Y1, 0.8, (0.2, 0.2, 0.2))


def electrical(page):
    X0, X1, Y0, Y1 = 37, 448, 395.5, 508
    wipe(page, 34, Y0, 578, Y1 + 1.5)
    models = ["STP580S-C72/Nsh+", "STP585S-C72/Nsh+", "STP590S-C72/Nsh+", "STP595S-C72/Nsh+", "STP600S-C72/Nsh+"]
    data = [
        ("القدرة القصوى (Pmax/W)", ["443.0", "580", "446.7", "585", "450.5", "590", "454.3", "595", "458.1", "600"]),
        ("جهد التشغيل الأمثل (Vmp/V)", ["40.4", "42.68", "40.5", "42.79", "40.6", "42.91", "40.7", "43.02", "40.8", "43.13"]),
        ("تيار التشغيل الأمثل (Imp/A)", ["10.98", "13.59", "11.04", "13.67", "11.10", "13.75", "11.16", "13.83", "11.2", "13.91"]),
        ("جهد الدائرة المفتوحة (Voc/V)", ["48.9", "51.42", "49", "51.55", "49.1", "51.68", "49.3", "51.81", "49.4", "51.94"]),
        ("تيار القصر (Isc/A)", ["11.54", "14.32", "11.61", "14.4", "11.67", "14.48", "11.74", "14.56", "11.80", "14.64"]),
    ]
    eff = ["22.5", "22.6", "22.8", "23.0", "23.2"]
    ys = grid(page, Y0, Y1, [1] * 8)
    cw = (X1 - X0) / 10
    cy = lambda i: (ys[i] + ys[i + 1]) / 2
    labels = ["طراز اللوح", "ظروف الاختبار"] + [d[0] for d in data] + ["كفاءة اللوح (%)"]
    for i, l in enumerate(labels):
        text(page, *LAB, cy(i), l, size=7.5, w=600, align="right")
    for k, m in enumerate(models):
        text(page, X0 + 2 * k * cw, X0 + 2 * (k + 1) * cw, cy(0), m, size=7, w=600)
        text(page, X0 + 2 * k * cw, X0 + (2 * k + 1) * cw, cy(1), "NMOT", size=7)
        text(page, X0 + (2 * k + 1) * cw, X0 + 2 * (k + 1) * cw, cy(1), "STC", size=7)
        text(page, X0 + 2 * k * cw, X0 + 2 * (k + 1) * cw, cy(7), eff[k], size=7)
    for r, (_, vals) in enumerate(data):
        for c, v in enumerate(vals):
            text(page, X0 + c * cw, X0 + (c + 1) * cw, cy(r + 2), v, size=7)
    for i in range(1, 8):
        rule(page, X0, 576, ys[i])
    rule(page, X0, 576, Y0, 0.8, (0.2, 0.2, 0.2))


def bifacial(page):
    X0, X1, Y0, Y1 = 258, 448, 556, 659
    wipe(page, 254, Y0, 578, Y1 + 1.5)
    hdr = ["25%", "15%", "5%"]
    data = [
        ("القدرة القصوى Pmax عند STC", ["750.0", "690.0", "630.0"]),
        ("جهد التشغيل الأمثل (Vmp/V)", ["43.2", "43.1", "43.1"]),
        ("تيار التشغيل الأمثل (Imp/A)", ["17.39", "16.00", "14.61"]),
        ("جهد الدائرة المفتوحة (Voc/V)", ["52.0", "51.9", "51.9"]),
        ("تيار القصر (Isc/A)", ["18.30", "16.84", "15.37"]),
        ("كفاءة اللوح (%)", ["29.0", "26.7", "24.4"]),
    ]
    ys = grid(page, Y0, Y1, [1] * 7)
    cw = (X1 - X0) / 3
    cy = lambda i: (ys[i] + ys[i + 1]) / 2
    text(page, *LAB, cy(0), "الكسب من الوجه الخلفي", size=7.5, w=600, align="right")
    for c, h in enumerate(hdr):
        text(page, X0 + c * cw, X0 + (c + 1) * cw, cy(0), h, size=7, w=600)
    for r, (l, vals) in enumerate(data):
        text(page, *LAB, cy(r + 1), l, size=7.5, w=600, align="right")
        for c, v in enumerate(vals):
            text(page, X0 + c * cw, X0 + (c + 1) * cw, cy(r + 1), v, size=7)
    for i in range(1, 8):
        rule(page, X0, 576, ys[i])


def thermal(page):
    X0, Y0, Y1 = 243, 687, 738
    wipe(page, 240, Y0, 578, Y1 + 0.5)
    rows = [
        ("درجة حرارة التشغيل الاسمية (NMOT)", "42 ± 2 °C"),
        ("المعامل الحراري للقدرة (Pmax)", "-0.29%/°C"),
        ("المعامل الحراري للجهد (Voc)", "-0.25%/°C"),
        ("المعامل الحراري للتيار (Isc)", "+0.046%/°C"),
    ]
    ys = grid(page, Y0, Y1, [1] * 4)
    for i, (l, v) in enumerate(rows):
        cy = (ys[i] + ys[i + 1]) / 2
        text(page, 430, LAB[1], cy, l, size=7.5, w=600, align="right")
        text(page, X0 + 4, 444, cy, v, size=7.2, align="right")
        rule(page, X0, 576, ys[i + 1])


if __name__ == "__main__":
    doc = pymupdf.open(sys.argv[1]); p = doc[1]
    mechanical(p); electrical(p); bifacial(p); thermal(p)
    doc.save(sys.argv[2], garbage=4, deflate=True)
