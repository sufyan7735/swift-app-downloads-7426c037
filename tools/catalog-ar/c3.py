"""catalog-3: Pylontech 12V Smart series — the English original has outlined (vector) text,
so English glyphs are removed with line-art redaction (only paths fully inside each box) and
Arabic is placed RTL with the shared engine."""
import sys; sys.path.insert(0, '/dev-server/tools/catalog-ar')
import engine, os, pymupdf
from pymupdf import Rect

SRC = '/dev-server/public/catalogs/catalog-3.pdf'
DST = '/dev-server/public/catalogs/official-ar/catalog-3.pdf'
TEAL, GREY, LAB, WHITE = 0x14b4b4, 0x5b5c5d, 0x4a4a4a, 0xffffff

doc = pymupdf.open(SRC)
jobs = {0: [], 1: []}   # (redact_rect or None, place_rect, spec)


def add(p, red, spec=None, at=None):
    jobs[p].append((Rect(red), Rect(at or red), spec))


# ---------------- page 0 ----------------
add(0, (15, 352, 200, 446), {"ar": "سلسلة 12V", "r": 196, "w": 700, "size": 19, "color": WHITE}, (0, 364, 10, 382))
jobs[0].append((None, Rect(0, 392, 10, 406), {"ar": "بطاريات ليثيوم حديد\nفوسفات ذكية", "r": 196, "w": 400, "size": 14, "color": WHITE, "lh": 20}))
tiles = [  # (x_text_left, right_edge, head_y, desc_y0, desc_y1, head, desc)
    (58, 152, 569, 580, 606, "50%", "أخف وزناً من بطاريات الرصاص\nالحمضية بنفس السعة"),
    (169, 268, 569, 577, 607, "30%", "كثافة طاقة أعلى من بطاريات\nLiFePO4 بنفس السعة"),
    (58, 152, 639, 649, 678, "4000\u200e+\u200e", "أكثر من 4,000 دورة حياة\nلتحقيق أعلى عائد استثمار"),
    (169, 268, 639, 649, 680, "تطبيق ذكي", "وحدة Bluetooth مدمجة تتيح\nالمراقبة اللحظية عبر\nالأجهزة المحمولة"),
    (58, 152, 703, 715, 752, "4S4P", "حتى 16 بطارية بتوصيل 4S4P\nلبناء نظام بطاريات بطاقة\nقصوى 40.96 kWh"),
    (169, 268, 703, 715, 752, "تسخين ذاتي", "غشاء التسخين الداخلي يتيح\nشحن البطارية في البرد القارس"),
]
for xl, xr, hy, d0, d1, h, ds in tiles:
    add(0, (xl - 2, hy - 9, xl + 94, hy + 13 if hy == 703 else hy + 7), {"ar": h, "r": xr, "w": 600, "size": 13, "color": TEAL}, (0, hy - 6, 1, hy + 6))
    add(0, (xl, d0 - 7 if hy == 703 else d0, xr + 2, d1), {"ar": ds, "r": xr, "w": 400, "size": 6.3, "color": GREY, "lh": 8.6}, (0, d0 + 1, 1, d0 + 9))
add(0, (330, 572, 440, 597), {"ar": "التطبيقات", "r": 562, "w": 700, "size": 15, "color": TEAL})
add(0, (330, 608, 566, 668), {"ar": "صُممت RV12200 لتحل محل بطاريات الرصاص الحمضية ذات الدورة\nالعميقة، وهي مثالية للمركبات الترفيهية RV والقوارب والشاحنات\nوالكبائن وغيرها من تطبيقات الدورة العميقة خارج الشبكة.",
                             "r": 562, "w": 400, "size": 8, "color": 0x575859, "lh": 11.8}, (0, 613, 1, 625))

# ---------------- page 1 ----------------
P = 13.84
LT, RT = (51, 294), (312, 555)       # table x-extents
LLR, LVR, RLR, RVR = 288, 178, 549, 446


def band(x0, x1, cy, h=5.2): return (x0 + 2, cy - h, x1 - 2, cy + h)


def hdr(t, tbl, cy, r=None):
    add(1, band(*tbl, cy, 5.6), {"ar": t, "r": r or tbl[1] - 6, "w": 700, "size": 8.5, "color": WHITE})


def rows(tbl, lr, vr, y0, items):
    for k, (l, v) in enumerate(items):
        cy = y0 + k * P
        add(1, band(*tbl, cy), {"ar": l, "r": lr, "w": 600, "size": 7, "color": LAB})
        if v:
            jobs[1].append((None, Rect(0, cy - 4, 1, cy + 4), {"ar": v, "r": vr, "w": 400, "size": 7, "color": LAB}))


jobs[0].append((Rect(52, 698, 160, 754), Rect(0, 0, 1, 1), None))
add(1, (50, 60, 175, 80), {"ar": "المواصفات", "r": 555, "w": 700, "size": 16, "color": TEAL})
hdr("المواصفات الكهربائية", LT, 99)
rows(LT, LLR, LVR, 114.6, [
    ("الجهد الاسمي", "12.8 VDC"), ("السعة الاسمية", "200 Ah"), ("المقاومة", "<10 mΩ"), ("الكفاءة", "99%"),
    ("التفريغ الذاتي", "≤3% شهرياً"), ("أقصى عدد بطاريات توازي/توالي", "4S4P"), ("عمر الدورات", "أكثر من 4000 دورة"),
    ("أقصى تيار تفريغ مستمر", "100 A"), ("تيار التفريغ الأقصى اللحظي", "200 A لمدة 5 s"),
    ("أقصى تيار شحن مستمر", "100 A"), ("جهد الشحن الموصى به", "14~14.6 V")])
hdr("المواصفات البيئية", LT, 276)
rows(LT, LLR, LVR, 291.8, [
    ("درجة حرارة التفريغ", "من −20 °C إلى 60 °C"), ("درجة حرارة الشحن", "من 0 °C إلى 55 °C"),
    ("درجة حرارة التخزين", "من −40 °C إلى 60 °C"), ("درجة حرارة التشغيل", "من −20 °C إلى 50 °C"),
    ("الرطوبة النسبية", "من 5% إلى 95%")])
hdr("أخرى", LT, 368.8)
rows(LT, LLR, LVR, 384.3, [
    ("الشهادات", "UL1973, FCC, CE, UKCA, Bluetooth SIG"), ("الاتصال", "BLE 5.0"), ("أقصى ارتفاع تشغيل", "4000 m"),
    ("غشاء التسخين", "مدعوم"), ("تطبيق الجوال", "Pylontech Auto")])
hdr("المواصفات الميكانيكية", RT, 99)
rows(RT, RLR, RVR, 114.6, [
    ("الأبعاد (الطول × العرض × الارتفاع)", "459 × 190 × 215 mm"), ("الوزن", "20.9 kg تقريباً"),
    ("نوع الطرف", "M8 × 1.25 × 14 mm"), ("عزم ربط الطرف", "9 ± 1 Nm"), ("مادة الغلاف", "PC"),
    ("درجة الحماية", "IP65"), ("نوع كيمياء الخلية", "LiFePO4")])
add(1, (318, 221, 385, 237), {"ar": "الأبعاد", "r": 549, "w": 700, "size": 10, "color": TEAL})
add(1, (496, 410, 540, 419), {"ar": "الوحدة: inch (mm)", "r": 540, "w": 400, "size": 5.5, "color": GREY})
hdr("الشحن بمعدلات مختلفة عند 25 °C", LT, 463.6)
hdr("التفريغ بمعدلات مختلفة عند 25 °C", RT, 463.6)
hdr("التفريغ بمعدلات مختلفة عند −20 °C", LT, 603.2)
hdr("التفريغ بمعدلات مختلفة عند 50 °C", RT, 603.2)
add(1, (51, 731, 420, 752), {"ar": "*أداء المنتج مبني على اختبارات في بيئة مضبوطة، وقد تختلف النتائج\nبحسب عوامل خارجية وبيئية متعددة.",
                            "r": 420, "w": 400, "size": 7, "color": GREY, "lh": 9.6}, (0, 733, 1, 741))
add(1, (55, 766, 187, 797), {"ar": "شركة Pylon Technologies المحدودة\nالطابق 5، رقم 71-72، الممر 887، طريق Zu Chongzhi\nمنطقة التجارة الحرة التجريبية، شنغهاي، الصين",
                            "r": 182, "w": 400, "size": 5, "color": GREY, "lh": 7.2}, (0, 771, 1, 777))

for pno, items in jobs.items():
    page = doc[pno]
    reds = [r for r, _, _ in items if r is not None]
    for red in reds:
        if any(o is not red and o.contains(red) for o in reds):
            continue  # nested boxes break covered-line-art removal
        page.add_redact_annot(red, fill=False)  # one box per pass: batched passes leave some glyphs behind
        page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                              graphics=pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED,
                              text=pymupdf.PDF_REDACT_TEXT_REMOVE)
    for _, at, spec in items:
        if spec:
            engine.place(page, at, spec, spec.get("size", 7), spec.get("color", GREY))

doc[1].draw_rect(Rect(313,173.2,360,176.4),color=None,fill=(237/255,242/255,244/255)); doc[1].draw_rect(Rect(313,176.4,360,178.8),color=None,fill=(1,1,1));
doc.subset_fonts(); doc.save(DST + '.tmp', garbage=4, deflate=True)
os.replace(DST + '.tmp', DST)
engine.render(DST, '/tmp/cat/c3n', 110)
print(os.path.getsize(DST))
