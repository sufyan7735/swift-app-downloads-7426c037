"""Lipower inverter catalogs (catalog-15/16/17): rebuilt RTL from the English originals.
Table + feature icons are mirrored as vectors; English text is replaced by shaped Arabic."""
import sys, os, re; sys.path.insert(0, '/dev-server/tools/catalog-ar')
import engine, pymupdf

engine.LTR_DIRECT = True
SEP = "\u036d"  # glyph the source uses as "/"

GROUP = [("Model", "الموديل"), ("AC Input Data", "بيانات دخل AC"), ("Input", "الدخل"),
         ("AC Output Data", "بيانات خرج AC"), ("Output", "الخرج"), ("Grid-connected operation", "التشغيل المتصل بالشبكة"),
         ("Battery", "البطارية"), ("PV-AC Charger", "شاحن PV-AC"), ("Display", "الشاشة"), ("Interface", "الواجهات"),
         ("Environmental parameters", "المعايير البيئية"), ("Physical parameters", "المعايير الفيزيائية")]
ITEM = [("Input format", "صيغة الدخل"), ("Rated input voltage", "جهد الدخل المقنن"), ("Voltage range fed", "نطاق جهد التغذية للشبكة"),
        ("Frequency range fed", "نطاق تردد التغذية للشبكة"), ("Voltage range", "نطاق الجهد"), ("Frequency range", "نطاق التردد"),
        ("Rated power", "القدرة المقننة"), ("Battery inverter", "إنفرتر البطارية"), ("Photovoltaic inverter", "الإنفرتر الشمسي"),
        ("Photovoltai", "الشمسي"), ("Battery", "البطارية"), ("Output voltage", "جهد الخرج"), ("Output frequency", "تردد الخرج"),
        ("Waveform", "شكل الموجة"), ("Switching time", "زمن التحويل، قابل للضبط"), ("Peak power", "قدرة الذروة"),
        ("Overload capacity", "قدرة التحميل الزائد"), ("Rated output current", "تيار الخرج المقنن"),
        ("Power factor range", "نطاق معامل القدرة"), ("Maximum conversion efficiency", "أقصى كفاءة تحويل DC/AC"),
        ("Rated voltage", "الجهد المقنن"), ("Constant charging voltage", "جهد الشحن الثابت، قابل للضبط"),
        ("Float charging voltage", "جهد الشحن العائم، قابل للضبط"), ("PV charging", "الشحن الشمسي"),
        ("Maximum input power of PV", "أقصى قدرة دخل PV"), ("MPPT input voltage range", "نطاق جهد دخل MPPT"),
        ("Optimal Vmp operating range", "نطاق Vmp التشغيلي الأمثل"), ("Maximum PV input voltage", "أقصى جهد دخل PV"),
        ("Maximum PV input current", "أقصى تيار دخل PV"), ("Maximum PV charging current", "أقصى تيار شحن PV"),
        ("Maximum mains power charging", "أقصى تيار شحن من الشبكة"), ("Maximum charging current", "أقصى تيار شحن"),
        ("LCD interface", "واجهة LCD"), ("RS232", "RS232"), ("Extended slot communication", "منفذ الاتصال الإضافي RS485"),
        ("compatibility BMS", "توافق BMS"), ("Parallel interface", "واجهة التوازي"),
        ("Operating environment temperature", "درجة حرارة بيئة التشغيل"), ("Operating environment humidity", "رطوبة بيئة التشغيل"),
        ("Storage temperature", "درجة حرارة التخزين"), ("Altitude", "الارتفاع"), ("Noise", "الضوضاء"),
        ("Depth × Width × Height", "العمق × العرض × الارتفاع (mm)"), ("Weight (for reference)", "الوزن التقريبي (kg)"),
        ("Standards and Certifications", "المعايير والشهادات")]
VAL = [("None", "لا يوجد"), ("Pure sine wave", "موجة جيبية نقية"),
       ("90-280VAC", "90-280VAC ±3V للوضع العادي، و170-280VAC ±3V لوضع UPS"),
       ("50Hz/ 60Hz(Automatic", "50/60Hz، تكيّف تلقائي"), ("UPS MODE", "وضع UPS: 10 ms، ووضع APL: 20 ms"),
       ("Battery mode", "وضع البطارية: 11s عند حمل 105%~150%، و2s عند 150%~200%\nو400ms عند حمل أكبر من 200%"),
       ("It can display", "يعرض وضع التشغيل والحمل والدخل والخرج وغيرها"), ("Baud rate", "معدل الباود 240"),
       ("Lithium battery BMS", "بطاقة اتصال BMS لبطاريات الليثيوم، بطاقة WIFI، بطاقة تلامس جاف، وغيرها"),
       ("-10~50", "-10~50 °C"), ("-15~60", "-15~60 °C"), ("15~60", "-15~60 °C"),
       ("20%~95%", "من 20% إلى 95% بدون تكاثف"),
       ("The altitude", "لا يتجاوز 1000 متر، وفوقها تُخفَّض القدرة المقننة\nأقصى ارتفاع 4000 متر، راجع IEC 62040"),
       ("Parallel", "توازي وربط بالشبكة")]
SKIP = ("Load;400ms", "meters, the rating", "meters. Refer", "is 4000 meters", "maximum altitude is", "Grid connection", "℃")


def key(t):
    return re.sub(r"\s+", " ", t.replace(SEP, "/")).strip()


def find(t, table):
    for k, v in sorted(table, key=lambda kv: -len(kv[0])):
        if t.startswith(k):
            return v
    return None


def mirror(page, drs, W):
    for d in drs:
        sh = page.new_shape()
        for it in d["items"]:
            op = it[0]
            f = lambda p: pymupdf.Point(W - p.x, p.y)
            if op == "l":
                sh.draw_line(f(it[1]), f(it[2]))
            elif op == "re":
                r = it[1]; sh.draw_rect(pymupdf.Rect(W - r.x1, r.y0, W - r.x0, r.y1))
            elif op == "qu":
                q = it[1]; sh.draw_quad(pymupdf.Quad(f(q.ur), f(q.ul), f(q.lr), f(q.ll)))
            elif op == "c":
                sh.draw_bezier(f(it[1]), f(it[2]), f(it[3]), f(it[4]))
        fill = d.get("fill")
        if fill and sum(fill) < 0.4 and d["rect"].height > 30:
            fill = (0.92, 0.92, 0.92)
        sh.finish(color=d.get("color"), fill=fill, width=d.get("width") or 1,
                  closePath=d.get("closePath", False), even_odd=d.get("even_odd", False),
                  fill_opacity=d.get("fill_opacity") or 1, stroke_opacity=d.get("stroke_opacity") or 1)
        sh.commit()


def table_page(page):
    W = page.rect.width
    reg = pymupdf.Rect(36, 214, W - 36, 766)
    texts = [l for l in engine.lines(page) if reg.contains(l["bbox"].tl + (0.5, 0.5))]
    drs = [d for d in page.get_drawings() if reg.contains(d["rect"])
           and not pymupdf.Rect(422, 645, 433, 706).contains(d["rect"])
           and not pymupdf.Rect(433, 650, 444, 690).contains(d["rect"])]  # outlined ℃ glyphs
    page.add_redact_annot(reg, fill=False)
    for l in engine.lines(page):  # page header
        if l["t"] in ("Technical Data", "Lipower Inverters"):
            page.add_redact_annot(l["bbox"], fill=False)
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED,
                          text=pymupdf.PDF_REDACT_TEXT_REMOVE)
    mirror(page, drs, W)
    engine.place(page, pymupdf.Rect(0, 27, 0, 44), {"ar": "البيانات الفنية", "r": W - 49, "w": 700}, 13.1, 0x231f20)
    engine.place(page, pymupdf.Rect(0, 27, 0, 37), {"ar": "إنفرترات Lipower", "l": 40, "w": 400}, 8.0, 0x6d6e71)
    for l in texts:
        t, r, sz = key(l["t"]), l["bbox"], l["size"]
        if not t or any(t.startswith(s) for s in SKIP):
            continue
        cx = W - (r.x0 + r.x1) / 2
        if r.x0 < 120:
            s = {"ar": find(t, GROUP) or t, "r": W - r.x0, "w": 700, "size": sz * 1.05}
        elif (r.x0 + r.x1) / 2 < 300 and not t.startswith(("BZ", "2012")):
            s = {"ar": find(t, ITEM) or t, "w": 400, "size": sz * 1.0, "maxw": (r.x1 - r.x0) + 30}
            if r.x0 < 215 and r.x1 < 300 and t.startswith(("Input format", "Rated input", "Voltage range", "Frequency range")) and r.x0 < 205:
                s["r"] = W - r.x0
            else:
                s["cx"] = cx
            if t.startswith(("Battery", "Photovoltai")) and r.x0 > 250:
                s["maxw"] = (r.x1 - r.x0) + 6
        else:
            v = find(t, VAL)
            if v is None:
                v = t.replace("*", " × ").replace("x", " × ") if re.fullmatch(r"\d+[*x]\d+[*x]\d+", t) else t
            if t.startswith("Battery mode") and not any(x["t"].startswith("Load;400ms") for x in texts):
                v = v.replace("\n", "، ")
            s = {"ar": v, "cx": cx, "w": 400, "size": sz * 1.0, "maxw": 250, "center": True, "lh": r.height * 1.55}
        rr = r
        engine.place(page, rr, s, sz, l["color"])


def feature_page(page, header, feats, title=None):
    W = page.rect.width
    reg = pymupdf.Rect(36, 528, W - 30, 726)
    texts = [l for l in engine.lines(page) if reg.contains(l["bbox"].tl + (0.5, 0.5))]
    icons = [d["rect"] for d in page.get_drawings() if reg.contains(d["rect"]) and 18 < d["rect"].width < 36 and abs(d["rect"].width - d["rect"].height) < 2]
    for l in texts:
        page.add_redact_annot(l["bbox"], fill=False)
    hd = [l for l in engine.lines(page) if l["t"] in ("Single Phase Hybrid Inverter", "Product Features")]
    for l in hd:
        page.add_redact_annot(l["bbox"], fill=False)
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,
                          text=pymupdf.PDF_REDACT_TEXT_REMOVE)
    src = pymupdf.open(SRC_DOC)
    pix = src[0].get_pixmap(dpi=36)
    for R in icons:
        R = R + (-8, -8, 8, 8)
        px = pix.pixel(int((R.x1 + 4) * 0.5), int(R.y1 * 0.5))
        page.draw_rect(R, color=None, fill=tuple(c / 255 for c in px[:3]))
    for R in icons:
        R = R + (-8, -8, 8, 8)
        page.show_pdf_page(pymupdf.Rect(W - R.x1, R.y0, W - R.x0, R.y1), src, 0, clip=R)
    for l in hd:
        r = l["bbox"]
        if l["t"].startswith("Single"):
            engine.place(page, r, {"ar": "إنفرتر هجين أحادي الطور", "r": r.x1, "w": 700}, l["size"] * 0.95, l["color"])
        else:
            engine.place(page, r, {"ar": "مزايا المنتج", "r": W - r.x0, "w": 400}, l["size"], l["color"])
    # cluster feature text lines into blocks by column then vertical gap
    cols = {}
    for l in texts:
        cols.setdefault(round(l["bbox"].x0 / 20), []).append(l["bbox"])
    blocks = []
    for c in sorted(cols):
        rs = sorted(cols[c], key=lambda r: r.y0); cur = [rs[0]]
        for r in rs[1:]:
            if r.y0 - cur[-1].y1 > 12:
                blocks.append(cur); cur = [r]
            else:
                cur.append(r)
        blocks.append(cur)
    if len(blocks) == 10 and len(feats) == 11:  # catalog-17: 'Parallel up to 9 units' is outlined vector text
        i = max(k for k, b in enumerate(blocks) if round(b[0].x0) == 280) + 1
        blocks.insert(i, [pymupdf.Rect(279.6, 699.4, 380, 707.9), pymupdf.Rect(279.6, 707.9, 353, 716.4)])
        page.draw_rect(pymupdf.Rect(278, 697, 400, 719), color=None, fill=(1, 1, 1))
    assert len(blocks) == len(feats), [(round(b[0].x0), round(b[0].y0), len(b)) for b in blocks]
    for b, txt in zip(blocks, feats):
        x0 = min(r.x0 for r in b); y0 = min(r.y0 for r in b); y1 = max(r.y1 for r in b)
        sz = b[0].height * 0.78
        n = txt.count("\n") + 1
        rr = pymupdf.Rect(0, y0, 0, y0 + 2 * sz * 0.9 if n == 1 else y0 + sz * 1.35)
        if n == 1:
            rr = pymupdf.Rect(0, y0, 0, y0 + sz * 1.6)
        engine.place(page, rr, {"ar": txt, "r": W - x0, "w": 400, "size": sz * 1.05, "color": 0x3c3c3c}, sz, 0x3c3c3c)


F15 = ["شاشة لمس ملونة\nبعرض واضح للمعايير", "قدرة خرج أعلى للإنفرتر\nفي وضع الطاقة الشمسية",
       "خرجان AC رئيسي ومساعد\nبقدرة خرج كافية", "مؤشر إضاءة RGB\nبتصميم عصري",
       "استغلال أعلى للطاقة الشمسية\nبتكامل الألواح مع الشبكة", "ترشيح EMI ومقاومة\nعالية للتداخل", "تصميم خارجي أبيض مطفأ"]
FBZ = ["إعادة تشغيل تلقائية لبطارية الليثيوم\nوشحن أنسب لبطاريات الليثيوم",
       "وضع تغذية ذكي يوزّع الحمل\nبين الألواح والشبكة والبطارية",
       "جهد شحن الشبكة والألواح قابل للضبط\nليطابق متطلبات البطاريات المختلفة",
       "هيكل نحيف وتركيب سهل\nونقل مريح",
       "حماية من عكس توصيل البطارية\nبمصهر لأمان أعلى",
       "PFC، كفاءة عالية، استهلاك أقل\nوحماية للبيئة وتوفير في التكلفة",
       "يعمل دون بطارية\nلتقليل تكلفة النظام",
       "تشغيل متوازٍ حتى 9 وحدات\nلتغذية أحمال أكبر",
       "دقة عالية لجهد الخرج ±5%\nلحماية أجهزتك",
       "خيار اتصال WIFI خارجي\nللمراقبة في أي وقت",
       "دعم BMS لبطاريات الليثيوم"]

FBZ4 = [f for f in FBZ if not f.startswith("تشغيل متوازٍ")]  # BZ4024 original lists 10 features
JOBS = {15: F15, 16: FBZ, 17: FBZ4}
if __name__ == "__main__":
    for n in [int(a) for a in sys.argv[1:]] or JOBS:
        src = f'/dev-server/public/catalogs/catalog-{n}.pdf'; dst = f'/dev-server/public/catalogs/official-ar/catalog-{n}.pdf'
        global SRC_DOC; SRC_DOC = src
        doc = pymupdf.open(src)
        feature_page(doc[0], None, JOBS[n]); table_page(doc[1])
        doc.subset_fonts(); doc.save(dst + '.tmp', garbage=4, deflate=True); os.replace(dst + '.tmp', dst)
        engine.render(dst, f'/tmp/cat/lp{n}', 110); print(n, os.path.getsize(dst))
