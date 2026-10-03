"""catalog-6: Pylontech PowerCube-M5A-64 (7 pages) — rebuilt RTL from the English original."""
import sys, os, re; sys.path.insert(0, '/dev-server/tools/catalog-ar')
import engine, pymupdf
engine.LTR_DIRECT = True

SRC = '/dev-server/public/catalogs/catalog-6.pdf'
DST = '/dev-server/public/catalogs/official-ar/catalog-6.pdf'
LR, CV = 530, 215

L = [  # (english label prefix, arabic label) — longest first matters
    ("Battery System Capacity (kWh)", "سعة نظام البطاريات (kWh)"),
    ("Battery System Capacity (AH)", "سعة نظام البطاريات (Ah)"),
    ("Battery System Voltage (Vdc)", "جهد نظام البطاريات (Vdc)"),
    ("Battery System Charge Upper-Voltage( V)", "الحد الأعلى لجهد شحن النظام (V)"),
    ("Battery System Nominal Current(A)", "التيار الاسمي للنظام (A)"),
    ("Battery System Continuous Current (A)", "التيار المستمر للنظام (A)"),
    ("Battery System Discharge lower-Voltage( V)", "الحد الأدنى لجهد تفريغ النظام (V)"),
    ("Battery Modules Qty. (Optional )", "عدد وحدات البطارية، اختياري"),
    ("Battery Capacity(kWh)", "سعة وحدة البطارية (kWh)"),
    ("Battery Module", "وحدة البطارية"),
    ("Controller Type", "نوع وحدة التحكم"),
    ("Peak Current (Amps)", "تيار الذروة (A)"),
    ("Operation temp. range", "نطاق حرارة التشغيل"),
    ("Round-trip efficiency", "كفاءة الدورة الكاملة عند 1C"),
    ("Depth of Discharge", "عمق التفريغ"),
    ("Dimension(W*D*H,mm)", "الأبعاد W×D×H (mm)"),
    ("Dimension(W*D*H, mm)", "الأبعاد W×D×H (mm)"),
    ("Dimension (W*D*H, mm)", "الأبعاد W×D×H (mm)"),
    ("Communication", "الاتصال"),
    ("Protection Class", "درجة الحماية"),
    ("Weight(kg)", "الوزن (kg)"), ("Weight (kg)", "الوزن (kg)"),
    ("Operation Temperature", "درجة حرارة التشغيل"),
    ("Storage Temperature", "درجة حرارة التخزين"),
    ("Operation Life", "العمر التشغيلي"),
    ("Humidity", "الرطوبة"), ("Altitude (m)", "الارتفاع (m)"),
    ("Product Certificate for UL", "شهادات المنتج، نسخة UL"),
    ("Product Certificate for CE", "شهادات المنتج، نسخة CE"),
    ("Product Certificate", "شهادات المنتج"),
    ("Nominal Voltage(Vdc)", "الجهد الاسمي (Vdc)"),
    ("Voltage Range(Vdc)", "نطاق الجهد (Vdc)"),
    ("Capacity(kWh)", "السعة (kWh)"),
    ("Nominal Capacity(AH)", "السعة الاسمية (Ah)"),
    ("AC Supply for BMS/FAN", "تغذية AC لنظام BMS والمروحة"),
    ("Operation Current (Max.) (A)", "أقصى تيار تشغيل (A)"),
    ("Related Product", "المنتج المرتبط"),
    ("System Operation Voltage (Vdc)", "جهد تشغيل النظام (Vdc)"),
    ("Self-consumption Power(W)", "الاستهلاك الذاتي (W)"),
]
V = {
    "58~71": "من 58 إلى 71", "0~50℃": "من 0°C إلى 50°C", "-20~50℃": "من -20°C إلى 50°C",
    "460×900×160.5": "460 × 900 × 160.5", "480×858×160": "480 × 858 × 160", "460×858×160": "460 × 858 × 160",
    "RS485(MODBUS RTU)\\CAN\\LAN": "RS485 (Modbus RTU) / CAN / LAN", "RS485(MODBUS RTU)/CAN/LAN": "RS485 (Modbus RTU) / CAN / LAN",
    "100~305VAC/50/60Hz": "100–305 VAC، 50/60 Hz", "0~1500": "من 0 إلى 1500",
    "15+": "أكثر من 15 سنة", "15+Years": "أكثر من 15 سنة", "-20~65": "من -20°C إلى 65°C", "-40~80": "من -40°C إلى 80°C",
    "64× n": "64 × n", "15.68× n": "15.68 × n", "71 × n": "71 × n", "58*n": "58 × n", "10 ~ 40℃": "من 10°C إلى 40°C",
    "10~40℃": "من 10°C إلى 40°C", "（@1C-rate） 96%": "96%", "1~21": "من 1 إلى 21",
    "1050(W)*925(D)*1965(H) (22 slots)": "22 خانة، 1050×925×1965",
    "210+ 115×n (where n = 1~22)": "210 + 115 × n ، حيث n من 1 إلى 22",
    "CANBUS/Modbus RTU/Modbus TCP/IP": "CANBUS / Modbus RTU / Modbus TCP/IP",
    "5 – 95 (without condensing)": "من 5% إلى 95% دون تكاثف", "<4000": "أقل من 4000",
    "＜210A for 5 minutes ＜500A for 30 seconds": "أقل من 210A لمدة 5 دقائق، أقل من 500A لمدة 30 ثانية",
}
SPEC = {  # whole-line specials
    "Basic Parameters": dict(ar="المعايير الأساسية", r=LR, w=700, color=0xffffff),
    "High Voltage Lithium-Ion Phosphate Battery storage system –": dict(ar="نظام تخزين بطاريات ليثيوم حديد فوسفات عالي الجهد", r=LR, w=700),
    "Battery Module: HM5A180F": dict(ar="وحدة البطارية: HM5A180F", r=LR, w=600),
    "Main Controller : S1500M5A180E": dict(ar="وحدة التحكم الرئيسية: S1500M5A180E", r=LR, w=600),
    "PowerCube-M5A-64 System Voltage＜1500V": dict(ar="PowerCube-M5A-64، جهد النظام أقل من 1500V", r=LR, w=700),
    "(External Power Supply Version, NA version) Isolating switch": dict(ar="نسخة التغذية الخارجية، نسخة أمريكا الشمالية، مفتاح عزل", cx=CV, w=400, size=7.5),
    "(External Power Supply Version, EU version) Circuit breaker）": dict(ar="نسخة التغذية الخارجية، النسخة الأوروبية، قاطع دائرة", cx=CV, w=400, size=7.5),
}
N = lambda s: re.sub(r"\s+", " ", s).strip()


def spec_for(t):
    if t in SPEC: return SPEC[t]
    if t.startswith("PowerCube-M5A-64/zzzV-"): return dict(ar=t, r=LR, w=700)
    if t.startswith("UL1973") or t.startswith("UKCA") or t.startswith("IEC62477") or t.startswith("UN38.3,"):
        return dict(ar=t.replace("，", ", "), cx=CV, w=400, size=t.startswith(("UKCA", "UN38")) and 7.5 or 8)
    if t.startswith("Module "):
        return [dict(ar="الوحدة", r=LR, w=700), dict(ar=t[7:].strip(), cx=CV, w=700)]
    for en, ar in L:
        if N(t).startswith(N(en)):
            v = N(t)[len(N(en)):].strip()
            out = [dict(ar=ar, r=LR, w=600)]
            if v: out.append(dict(ar=V.get(v, v), cx=CV, w=400, maxw=250))
            return out
    return None


doc = pymupdf.open(SRC)
for page in doc:
    todo = []
    for ln in engine.lines(page):
        s = spec_for(ln["t"])
        if s is None:
            if ln["t"] != "Cube the force": print("SKIP", page.number, ln["t"], file=sys.stderr)
            continue
        r = ln["bbox"]
        page.add_redact_annot(pymupdf.Rect(r.x0, r.y0 + 1.2, r.x1 + 2, r.y1 - 1.2), fill=False)
        for x in (s if isinstance(s, list) else [s]):
            todo.append((r, x, ln["size"] * (0.85 if ln["size"] > 13 else 0.9), ln["color"]))
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,
                          text=pymupdf.PDF_REDACT_TEXT_REMOVE)
    for r, s, sz, c in todo:
        engine.place(page, r, s, sz, c)
tmp = '/tmp/cat/c6.pdf'
doc.save(tmp, garbage=4, deflate=True)
d = pymupdf.open(tmp); d.subset_fonts(); d.save(DST + '.tmp', garbage=4, deflate=True); os.replace(DST + '.tmp', DST)
for i in range(len(d)): pymupdf.open(DST)[i].get_pixmap(dpi=80).save(f'/tmp/cat/c6n{i}.png')
print(os.path.getsize(DST))
