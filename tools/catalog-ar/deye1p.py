# Deye SUN-7.6/8/10/12K-SG02LP1 — page 2 (Technical Data) rebuilt as an exact RTL mirror of the English original.
# Table graphics are mirrored horizontally; every text item is re-placed at its mirrored position.
import os, re, sys, pymupdf
sys.path.insert(0, os.path.dirname(__file__))
import engine

EN = '/dev-server/public/catalogs/official/deye-sun-7-6-12k-sg02lp1--8k.pdf'
AR = '/dev-server/public/catalogs/official-ar/deye-sun-7-6-12k-sg02lp1--8k.pdf'
DSTS = [AR, AR.replace('--8k', '--12k')]
FOOT = 762  # footer bar top: kept unmirrored

SEC = {"Battery Input Data": "بيانات دخل البطارية", "PV String Input Data": "بيانات دخل سلاسل الألواح PV",
       "AC Input/Output Data": "بيانات دخل/خرج AC", "Eﬃciency": "الكفاءة", "Efficiency": "الكفاءة",
       "Equipment Protection": "حماية الجهاز", "Interface": "الواجهة", "General Data": "بيانات عامة"}
LAB = {
    "Model": "الموديل",
    "Battery Type": "نوع البطارية", "Battery Voltage Range (V)": "نطاق جهد البطارية (V)",
    "Max. Charging Current (A)": "أقصى تيار شحن (A)", "Max. Discharging Current (A)": "أقصى تيار تفريغ (A)",
    "Charging Strategy for Li-ion Battery": "استراتيجية شحن بطارية الليثيوم", "Number of Battery Input": "عدد مداخل البطارية",
    "Max. PV Access Power (W)": "أقصى قدرة ألواح مسموحة (W)", "Max. PV Input Power (W)": "أقصى قدرة دخل PV (W)",
    "Max. PV Input Voltage (V)": "أقصى جهد دخل PV (V)", "Start-up Voltage (V)": "جهد بدء التشغيل (V)",
    "MPPT Voltage Range (V)": "نطاق جهد MPPT (V)", "Rated PV Input Voltage (V)": "جهد دخل PV المقنن (V)",
    "Max. Operating PV Input Current (A)": "أقصى تيار تشغيل لدخل PV (A)",
    "Max. Input Short-Circuit Current (A)": "أقصى تيار قصر لدخل PV (A)",
    "No. of MPP Trackers/": "عدد متتبعات MPPT", "No. of Strings MPP Tracker": "عدد السلاسل لكل متتبع",
    "Rated AC Input/Output Active Power (W)": "القدرة الفعالة المقننة لدخل/خرج AC (W)",
    "Max. AC Input/Output Apparent Power (VA)": "أقصى قدرة ظاهرية لدخل/خرج AC (VA)",
    "Rated AC Input/Output Current (A)": "التيار المقنن لدخل/خرج AC (A)",
    "Max. AC Input/Output Current (A)": "أقصى تيار لدخل/خرج AC (A)",
    "Max. Continuous AC Passthrough (grid to load) (A)": "أقصى تيار تمرير AC مستمر (من الشبكة للحمل) (A)",
    "Peak Power (off-grid) (W)": "القدرة القصوى اللحظية (خارج الشبكة) (W)",
    "Power Factor Adjustment Range": "نطاق ضبط معامل القدرة",
    "Rated Input/Output Voltage/Range (V)": "جهد/نطاق الدخل والخرج المقنن (V)",
    "Rated Input/Output Grid Frequency/Range(Hz)": "تردد/نطاق شبكة الدخل والخرج (Hz)",
    "Grid Connection Form": "طريقة الربط بالشبكة", "Total Current Harmonic Distortion THDi": "التشوه التوافقي الكلي للتيار THDi",
    "DC Injection Current": "تيار حقن DC", "Max. Efficiency": "الكفاءة القصوى", "Euro Efficiency": "الكفاءة الأوروبية",
    "MPPT Efficiency": "كفاءة MPPT", "Integrated": "حمايات مدمجة", "Surge Protection Level": "مستوى الحماية من التدفق",
    "Communication Interface": "واجهة الاتصال", "Monitor Mode": "وضع المراقبة",
    "Operating Temperature Range (℃)": "نطاق درجة حرارة التشغيل (°C)", "Permissible Ambient Humidity": "الرطوبة المحيطة المسموحة",
    "Permissible Altitude": "الارتفاع المسموح", "Noise (dB)": "الضجيج (dB)", "Ingress Protection(IP) Rating": "درجة الحماية (IP)",
    "Inverter Topology": "طوبولوجيا الإنفرتر", "Over Voltage Category": "فئة الجهد الزائد",
    "Cabinet Size (WxHxD mm)": "أبعاد الهيكل W×H×D (mm)", "Weight (kg)": "الوزن (kg)", "Type of Cooling": "نوع التبريد",
    "Warranty": "الضمان", "Grid Regulation": "معايير الشبكة", "Safety / EMC Standard": "معايير السلامة / EMC",
}
VAL = {
    "Lead-acid or Lithium-ion": "رصاص حمضي أو ليثيوم أيون", "Self-adaption to BMS": "تكيّف ذاتي مع BMS",
    "2 times of rated power, 10s": "ضعف القدرة المقننة لمدة 10s", "0.8 leading to 0.8 lagging": "من 0.8 متقدم إلى 0.8 متأخر",
    "<3% (of nominal power)": "أقل من 3% (من القدرة الاسمية)", "<0.5% In": "أقل من 0.5% In",
    "-40 to +60℃, >45℃ Derating": "-40 ~ +60 °C\nخفض القدرة فوق 45 °C", "<45": "أقل من 45",
    "Non-Isolated": "غير معزول", "Intelligent Air Cooling": "تبريد هوائي ذكي",
    "420×670×233 (Excluding Connectors and Brackets)": "420×670×233 (بدون الموصلات والحوامل)",
    "5 Years/10 Years": "5 سنوات / 10 سنوات",
    "GPRS/WIFI/Bluetooth/4G/LAN(optional)": "GPRS/WIFI/Bluetooth/4G/LAN (اختياري)",
}
PROT = ("حماية من عكس قطبية DC، حماية من زيادة تيار خرج AC، حماية حرارية،\n"
        "حماية من زيادة جهد خرج AC، حماية من قصر دائرة خرج AC، مراقبة مكوّن DC، مفتاح DC،\n"
        "قاطع دائرة خطأ القوس الكهربائي (اختياري)، حماية ضد التشغيل المنعزل،\n"
        "كشف معاوقة العزل، كشف التيار المتبقي")
WARR2 = "تعتمد مدة الضمان على موقع التركيب النهائي للإنفرتر، للمزيد يرجى الرجوع إلى سياسة الضمان"


def spans(page):
    out = []
    for b in page.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            t = engine.norm(''.join(s['text'] for s in l['spans']))
            if t:
                out.append(dict(t=t, r=pymupdf.Rect(l['bbox']), size=l['spans'][0]['size'], color=l['spans'][0]['color']))
    return out


def rebuild():
    src = pymupdf.open(EN)
    sp = spans(src[1])
    W, H = src[1].rect.width, src[1].rect.height
    # strip all text above the footer, keep graphics
    for s in sp:
        if s['r'].y1 < FOOT:
            src[1].add_redact_annot(s['r'], fill=False)
    src[1].apply_redactions(images=0, graphics=0, text=0)

    out = pymupdf.open()
    p = out.new_page(width=W, height=H)
    p.show_pdf_page(p.rect, src, 1)                       # will be mirrored
    p.show_pdf_page(pymupdf.Rect(0, FOOT, W, H), src, 1, clip=pymupdf.Rect(0, FOOT, W, H))  # footer, unmirrored
    x = p.get_contents()[0]
    c = out.xref_stream(x).decode()
    c = c.replace("q ", "q -1 0 0 1 %.4f 0 cm " % W, 1)
    out.update_stream(x, c.encode())
    p = out[0]

    seen = set()
    done_prot = done_warr = False
    for s in sp:
        t, r = s['t'], s['r']
        key = (t, round(r.x0), round(r.y0))
        if r.y1 >= FOOT or key in seen:
            continue
        seen.add(key)
        col, sz = s['color'], s['size']
        mcx = W - (r.x0 + r.x1) / 2
        if t == "Technical Data":
            engine.place(p, r, {"ar": "البيانات الفنية", "r": W - 49, "w": 700}, 14, col); continue
        if t.startswith("www."):
            engine.place(p, r, {"ar": t, "l": W - r.x1, "w": 400}, sz, col); continue
        if r.x0 < 60:  # label column
            if t in SEC:
                engine.place(p, r, {"ar": SEC[t], "r": W - 49, "w": 700}, sz, col)
            else:
                engine.place(p, r, {"ar": LAB.get(t, t), "r": W - 49, "w": 600 if t == "Model" else 400, "maxw": 150}, sz, col)
            continue
        if 490 < r.y0 < 524:  # integrated protections (4 lines)
            if not done_prot:
                engine.place(p, pymupdf.Rect(0, 490, 0, 498), {"ar": PROT, "cx": W - 373.5, "center": True, "maxw": 330, "lh": 8.4}, 7.2, col)
                done_prot = True
            continue
        if t.startswith("-40 to"):
            a, b = "-40 ~ +60 °C", "، خفض القدرة فوق 45 °C"
            wa, wb = engine.width(a, 400, sz), engine.line_width(b, 400, sz)
            xr = mcx + (wa + wb + 2) / 2
            rr = pymupdf.Rect(0, 586, 0, 595)
            engine.LTR_DIRECT = True; engine.put(p, xr, 590.5, a, True, 400, sz, "#%06x" % col); engine.LTR_DIRECT = False
            engine.place(p, rr, {"ar": b, "r": xr - wa - 2}, sz, col); continue
        if t.startswith("the Warranty"):
            engine.place(p, r, {"ar": WARR2, "cx": W - 373.5, "maxw": 340}, sz, col); continue
        engine.place(p, r, {"ar": VAL.get(t, t), "cx": mcx, "center": True, "lh": 9, "w": 600 if col == 0xffffff else 400, "maxw": 300}, sz, col)
    return out


if __name__ == "__main__":
    pg = rebuild()
    for dst in DSTS:
        d = pymupdf.open('/tmp/dy/ar-orig.pdf')
        d.delete_page(1)
        d.insert_pdf(pg)
        d.subset_fonts()
        d.save(dst + '.tmp', garbage=4, deflate=True); d.close(); os.replace(dst + '.tmp', dst)
    print(os.path.getsize(DSTS[0]))
