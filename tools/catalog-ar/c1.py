# catalog-1: Pylontech RV12314 (12.8V 314Ah) — Arabic RTL rebuild from the English original
import os, sys, pymupdf
sys.path.insert(0, os.path.dirname(__file__))
import engine

SRC = '/dev-server/public/catalogs/catalog-1.pdf'
DST = '/dev-server/public/catalogs/official-ar/catalog-1.pdf'

HL = [  # (title, body)
    ("عمر دورات طويل", "عمر يصل إلى أكثر من 6000 دورة\nلتحقيق أعلى عائد على الاستثمار."),
    ("تسخين ذاتي", "غشاء تسخين مدمج يتيح شحن البطارية\nفي البيئات شديدة البرودة."),
    ("وزن خفيف", "بطاريات فوسفات الحديد الليثيوم أخف بنسبة 60%\nمن بطاريات الرصاص الحمضية، ما يسهّل\nالتركيب والنقل."),
    ("حماية متعددة", "تدعم الحماية من OC/OV/OT/UV/UT/SC،\nويوفّر نظام إدارة البطارية BMS\nحماية وإدارة شاملتين."),
    ("حماية احتياطية نشطة", "مرحّل إضافي يفصل الدخل/الخرج\nلضمان السلامة عند حدوث عطل في البطارية."),
]
LAB = {
    "Electrical Parameters": "المعايير الكهربائية", "Environmental Parameters": "المعايير البيئية",
    "Other": "أخرى", "Mechanical Parameters": "المعايير الميكانيكية",
    "Nominal Voltage": "الجهد الاسمي", "Nominal Capacity": "السعة الاسمية",
    "Maximum Series and Parallel Capability": "أقصى قدرة توصيل على التوالي والتوازي",
    "Cycle Life": "عمر الدورات", "Maximum Sustained Discharge Current": "أقصى تيار تفريغ مستمر",
    "Peak Discharge Current": "تيار التفريغ الأقصى اللحظي", "Maximum Sustained Charge Current": "أقصى تيار شحن مستمر",
    "Recommended Charge Current": "تيار الشحن الموصى به", "Recommended Charge Voltage": "جهد الشحن الموصى به",
    "Recommended Storage Temperature": "درجة حرارة التخزين الموصى بها", "Working Temperature": "درجة حرارة التشغيل",
    "Altitude": "الارتفاع", "Relative Humidity": "الرطوبة النسبية", "Switch": "مفتاح تشغيل",
    "Certifications": "الشهادات", "Heating Film": "غشاء التسخين", "Dimension（L*W*H）": "الأبعاد (الطول × العرض × الارتفاع)",
    "Weight": "الوزن", "Terminal Type": "نوع الأطراف", "Terminal Torque": "عزم ربط الأطراف",
    "Case Material": "مادة الغلاف", "Production Rating": "درجة الحماية", "Battery Type": "نوع البطارية",
}
VAL = {
    "4S or 8P": "4S أو 8P", "10-35℃": "من 10°C إلى 35°C", "-20-50℃": "من −20°C إلى +50°C",
    "＜4000m": "أقل من 4000 m", "5%-95%（No Condensation)": "من 5% إلى 95% بدون تكاثف", "Yes": "نعم",
    "340*280*235": "340 × 280 × 235 mm", "≈31.5kg": "حوالي 31.5 kg", "Metal": "معدن",
}


def spans(page):
    out = []
    for b in page.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            t = ''.join(s['text'] for s in l['spans']).strip()
            if t:
                out.append(dict(t=t, r=pymupdf.Rect(l['bbox']), size=l['spans'][0]['size'], color=l['spans'][0]['color']))
    return out


def redact(page, items):
    for it in items:
        page.add_redact_annot(it['r'], fill=False)
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,
                          text=pymupdf.PDF_REDACT_TEXT_REMOVE)


def page0(p):
    sp = [s for s in spans(p) if s['r'].x0 > 360]
    head = next(s for s in sp if s['t'] == "Product Highlights")
    titles = [s for s in sp if s['size'] > 13 and s['size'] < 15]
    body = [s for s in sp if s['size'] < 10]
    redact(p, sp)
    R = 550
    engine.place(p, head['r'], {"ar": "أبرز مزايا المنتج", "r": R, "w": 700}, head['size'], head['color'])
    for (ti, bo), t in zip(HL, sorted(titles, key=lambda s: s['r'].y0)):
        engine.place(p, t['r'], {"ar": ti, "r": R, "w": 700}, t['size'], t['color'])
        bs = [b for b in body if t['r'].y1 - 2 < b['r'].y0 < t['r'].y1 + 60]
        y = t['r'].y1 + 1
        for line in bo.split("\n"):
            engine.place(p, pymupdf.Rect(0, y, 0, y + 12), {"ar": line, "r": R, "w": 400}, 8.6, bs[0]['color'] if bs else 0x333333)
            y += 12.6


def page1(p):
    W = p.rect.width
    sp = [s for s in spans(p) if s['size'] > 5]
    redact(p, [s for s in spans(p)])
    for s in sp:
        t, r = s['t'], s['r']
        if r.x0 < 60:
            heading = s['size'] > 13
            engine.place(p, r, {"ar": LAB.get(t, t), "r": W - 53, "w": 700 if heading else 600}, s['size'] * (1.05 if heading else 0.98), s['color'])
        else:
            cx = W - (r.x0 + r.x1) / 2
            engine.place(p, r, {"ar": VAL.get(t, t), "cx": cx, "w": 400, "maxw": 260}, s['size'] * 0.98, s['color'])


if __name__ == "__main__":
    doc = pymupdf.open(SRC)
    page0(doc[0]); page1(doc[1])
    doc.subset_fonts(); doc.save(DST + '.tmp', garbage=4, deflate=True); os.replace(DST + '.tmp', DST)
    engine.render(DST, '/tmp/cat/a1', 90); print(os.path.getsize(DST))
