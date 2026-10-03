# Deye hybrid inverters (3-6K 1P, 14-20K 3P LV, 29.9-50K HV, 60-80K HV) — page 2 (Technical Data)
# rebuilt as an exact RTL mirror of the English original (same method as deye1p.py).
import os, sys, pymupdf
sys.path.insert(0, os.path.dirname(__file__))
import engine, deye1p

ROOT = '/dev-server/public/catalogs'
FAM = [
    ('deye-sun-3-6k-sg04lp1--6k-sm2', ['deye-sun-3-6k-sg04lp1--6k-sm2']),
    ('deye-sun-14-20k-sg05lp3--16k', ['deye-sun-14-20k-sg05lp3--16k', 'deye-sun-14-20k-sg05lp3--20k']),
    ('deye-sun-29-9-50k-sg01hp3--30k', ['deye-sun-29-9-50k-sg01hp3--30k', 'deye-sun-29-9-50k-sg01hp3--50k']),
    ('deye-sun-60-80k-sg02hp3--80k', ['deye-sun-60-80k-sg02hp3--80k']),
]
FOOT = deye1p.FOOT

SEC = dict(deye1p.SEC, **{"AC Output Data": "بيانات خرج AC", "Protection": "الحماية",
                          "Certifications and Standards": "الشهادات والمعايير"})
LAB = dict(deye1p.LAB, **{
    "Charging Strategy for Li-Ion Battery": "استراتيجية شحن بطارية الليثيوم",
    "Max. DC Input Power (W)": "أقصى قدرة دخل DC ‏(W)", "Max. DC Input Voltage (V)": "أقصى جهد دخل DC ‏(V)",
    "MPPT Range (V)": "نطاق MPPT ‏(V)", "Rated DC Input Voltage (V)": "جهد دخل DC المقنن (V)",
    "Full Load DC Voltage Range (V)": "نطاق جهد DC عند الحمل الكامل (V)", "PV Input Current (A)": "تيار دخل PV ‏(A)",
    "Max. PV I (A)": "أقصى تيار قصر لدخل PV ‏(A)",
    "No.of MPP Trackers": "عدد متتبعات MPPT", "No.of Strings per MPP Tracker": "عدد السلاسل لكل متتبع",
    "Rated AC Output Active Power (W)": "القدرة الفعالة المقننة لخرج AC ‏(W)",
    "Max AC Output Active Power (W)": "أقصى قدرة فعالة لخرج AC ‏(W)",
    "AC Output Rated Current (A)": "التيار المقنن لخرج AC ‏(A)", "Max. AC Output Rated Current (A)": "أقصى تيار لخرج AC ‏(A)",
    "Max. Three-phase Unbalanced Output Current (A)": "أقصى تيار خرج غير متوازن ثلاثي الطور (A)",
    "Max. Continuous AC Passthrough (A)": "أقصى تيار تمرير AC مستمر (A)", "Peak Power (Off Grid)": "القدرة القصوى (خارج الشبكة)",
    "Generator Input/Smart Load": "دخل المولد / الحمل الذكي", "/AC Couple Current (A)": "/ تيار الربط AC ‏(A)",
    "Output Frequency and Voltage": "تردد وجهد الخرج", "Grid Type": "نوع الشبكة",
    "Total Harmonic Distortion (THD)": "التشوه التوافقي الكلي (THD)", "DC Current Injection": "حقن تيار DC",
    "Safety EMC / Standard": "معايير السلامة / EMC", "Cooling": "التبريد", "Communication with BMS": "الاتصال مع BMS",
    "Protection Degree": "درجة الحماية", "Installation Style": "طريقة التركيب",
    "*Note: The function of Multiple units work in parallel mode will be avaiable in Q1 2023":
        "*ملاحظة: ميزة تشغيل عدة وحدات على التوازي متاحة اعتباراً من الربع الأول 2023",
})
VAL = dict(deye1p.VAL, **{
    "Lithium-ion": "ليثيوم أيون", "Three Phase": "ثلاثي الطور", "Smart Cooling": "تبريد ذكي",
    "Natural Cooling": "تبريد طبيعي", "5 Years (10 Years Optional)": "5 سنوات (10 سنوات اختياري)",
    "1.5 time of rated power, 10 S": "1.5 ضعف القدرة المقننة لمدة 10 s",
    "1.5 times of rated power, 10s": "1.5 ضعف القدرة المقننة لمدة 10s",
    "-40-60℃, >45℃ Derating": "-40 ~ +60 °C، خفض القدرة فوق 45 °C",
    "376×470×241.5 (Excluding Connectors and Brackets)": "376×470×241.5 (بدون الموصلات والحوامل)",
    "456×750×268.5 (Excluding Connectors and Brackets)": "456×750×268.5 (بدون الموصلات والحوامل)",
    "527×894×294 (Excluding Connectors and Brackets)": "527×894×294 (بدون الموصلات والحوامل)",
    "606×927×314 (Excluding Connectors and Brackets)": "606×927×314 (بدون الموصلات والحوامل)",
    "Power Network Monitoring, Island Protection Monitoring, Earth Fault Detection, DC Input Switch,":
        "مراقبة الشبكة، مراقبة الحماية من التشغيل المنعزل، كشف أعطال التأريض، مفتاح دخل DC،",
    "Power Network Monitoring, Island Protection Monitoring, Earth Fault Detection, DC Input Switch":
        "مراقبة الشبكة، مراقبة الحماية من التشغيل المنعزل، كشف أعطال التأريض، مفتاح دخل DC",
    "DC Terminal Insulation Impedance Monitoring, Residual Current (RCD) Detection, Surge protection level":
        "مراقبة معاوقة عزل أطراف DC، كشف التيار المتبقي (RCD)، مستوى الحماية من التدفق",
    "DC Terminal Insulation Impedance Monitoring, DC Component Monitoring, Ground Fault Current Monitoring":
        "مراقبة معاوقة عزل أطراف DC، مراقبة مكوّن DC، مراقبة تيار أعطال التأريض",
    "Overvoltage Load Drop Protection, Residual Current (RCD) Detection, Surge protection level":
        "حماية فصل الحمل عند زيادة الجهد، كشف التيار المتبقي (RCD)، مستوى الحماية من التدفق",
    "Insulation Resistor Detection, Residual Current Monitoring Unit, Output Over Current Protection,":
        "كشف مقاومة العزل، وحدة مراقبة التيار المتبقي، حماية الخرج من زيادة التيار،",
    "DC Polarity Reverse Connection Protection, AC Output Overcurrent Protection, Thermal Protection,":
        "حماية من عكس قطبية DC، حماية من زيادة تيار خرج AC، حماية حرارية،",
    "AC Output Overvoltage Protection, AC Output Short Circuit Protection, DC Component Monitoring,":
        "حماية من زيادة جهد خرج AC، حماية من قصر خرج AC، مراقبة مكوّن DC،",
    "Overvoltage Load Drop Protection, Ground Fault Current Monitoring, Arc Fault Circuit Interrupter (optional),":
        "حماية فصل الحمل عند زيادة الجهد، مراقبة تيار أعطال التأريض، قاطع خطأ القوس (اختياري)،",
    "DC Polarity Reverse Connection Protection, AC Output Overcurrent Protection":
        "حماية من عكس قطبية DC، حماية من زيادة تيار خرج AC",
    "AC Output Overvoltage Protection, AC Output Short Circuit Protection, Thermal Protection":
        "حماية من زيادة جهد خرج AC، حماية من قصر خرج AC، حماية حرارية",
    "Anti-islanding Protection, PV String Input Reverse Polarity Protection,":
        "حماية ضد التشغيل المنعزل، حماية سلاسل PV من عكس القطبية،",
    "the Warranty Period Depends the Final Installation Site of Inverter, More Info Please Refer to Warranty Policy": deye1p.WARR2,
    "Wall-mounted": "تثبيت على الحائط",
    "Output Shorted Protection, Surge Protection": "حماية الخرج من القصر، الحماية من التدفق",
})


def ltr(p, cx, cy, v, w, sz, col, mx=330):
    tw = engine.width(v, w, sz)
    if tw > mx: sz *= mx / tw; tw = mx
    engine.LTR_DIRECT = True
    engine.put(p, cx + tw / 2, cy, v, True, w, sz, "#%06x" % col)
    engine.LTR_DIRECT = False


def rebuild(en):
    src = pymupdf.open(en)
    sp = deye1p.spans(src[1])
    W, H = src[1].rect.width, src[1].rect.height
    for s in sp:
        if s['r'].y1 < FOOT:
            src[1].add_redact_annot(s['r'], fill=False)
    src[1].apply_redactions(images=0, graphics=0, text=0)
    out = pymupdf.open()
    p = out.new_page(width=W, height=H)
    p.show_pdf_page(p.rect, src, 1)
    p.show_pdf_page(pymupdf.Rect(0, FOOT, W, H), src, 1, clip=pymupdf.Rect(0, FOOT, W, H))
    x = p.get_contents()[0]
    c = out.xref_stream(x).decode()
    out.update_stream(x, c.replace("q ", "q -1 0 0 1 %.4f 0 cm " % W, 1).encode())
    p = out[0]
    seen, miss = set(), []
    for s in sp:
        t, r, col, sz = s['t'], s['r'], s['color'], s['size']
        key = (t, round(r.x0), round(r.y0))
        if r.y1 >= FOOT or key in seen:
            continue
        seen.add(key)
        mcx, cy = W - (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2
        if t == "Technical Data":
            engine.place(p, r, {"ar": "البيانات الفنية", "r": W - 49, "w": 700}, 14, col); continue
        if t.startswith("www."):
            engine.place(p, r, {"ar": t, "l": W - r.x1, "w": 400}, sz, col); continue
        if t == "SC" and r.x0 < 100:
            continue  # subscript of "Max. PV I(SC)", folded into the Arabic label
        if r.x0 < 60:
            if t in SEC:
                engine.place(p, r, {"ar": SEC[t], "r": W - 49, "w": 700}, sz, col)
            elif t.startswith("*Note"):
                engine.place(p, r, {"ar": LAB[t], "r": W - 49}, sz, col)
            else:
                if t not in LAB: miss.append(t)
                engine.place(p, r, {"ar": LAB.get(t, t), "r": W - 49, "w": 600 if t == "Model" else 400, "maxw": 150}, sz, col)
            continue
        v = VAL.get(t, t)
        w = 600 if col == 0xffffff else 400
        if v.startswith("-40 ~ +60 °C"):
            a, b = "-40 ~ +60 °C", v[len("-40 ~ +60 °C"):].replace("\n", "، ")
            wa, wb = engine.width(a, 400, sz), engine.line_width(b, 400, sz)
            xr = mcx + (wa + wb + 2) / 2
            engine.LTR_DIRECT = True; engine.put(p, xr, cy, a, True, 400, sz, "#%06x" % col); engine.LTR_DIRECT = False
            engine.place(p, r, {"ar": b, "r": xr - wa - 2}, sz, col); continue
        if not engine.AR.search(v):
            ltr(p, mcx, cy, v, w, sz, col, 66 if col == 0xffffff and v.startswith(('SUN', '-')) else 330); continue
        engine.place(p, r, {"ar": v, "cx": mcx, "center": True, "w": w, "maxw": 340}, sz, col)
    if miss:
        print("UNTRANSLATED:", miss, file=sys.stderr)
    return out


if __name__ == "__main__":
    for en, dsts in FAM:
        pg = rebuild(f'{ROOT}/official/{en}.pdf')
        for n in dsts:
            dst = f'{ROOT}/official-ar/{n}.pdf'
            d = pymupdf.open(dst)
            d.delete_page(1)
            d.insert_pdf(pg)
            d.subset_fonts()
            d.save(dst + '.tmp', garbage=4, deflate=True); d.close(); os.replace(dst + '.tmp', dst)
            print(n, os.path.getsize(dst))
