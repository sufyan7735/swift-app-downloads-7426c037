# Solis S6 hybrid inverters — page 2 (Datasheet) rebuilt as an exact RTL mirror of the English original.
# Page graphics are mirrored horizontally; every text line is re-placed at its mirrored position.
# Usage: python3 solis.py   (rebuilds all four families, both variant files each)
import os, sys, pymupdf
sys.path.insert(0, os.path.dirname(__file__))
import engine

ROOT = '/dev-server/public/catalogs'
FAM = {
    'solis-s6-eh2p-5-8k': ('6k', '8k'),
    'solis-s6-eh3p-12-20k-h': ('12k', '20k'),
    'solis-s6-eh3p-29-9-50k-h': ('30k', '50k'),
    'solis-s6-eh3p-75-125k': ('80k', '125k'),
}

LAB = {
    "DATASHEET": "نشرة المواصفات", "Models": "الطرازات",
    "Input DC (PV side)": "دخل DC (جهة الألواح)", "Battery": "البطارية",
    "Output AC (Grid side)": "خرج AC (جهة الشبكة)", "Input AC (Grid side)": "دخل AC (جهة الشبكة)",
    "Input Generator": "دخل المولد", "Input AC (Generator)": "دخل AC (المولد)",
    "Output AC (Back-up)": "خرج AC (الاحتياطي)", "Efficiency": "الكفاءة", "Protection": "الحماية",
    "Dados gerais": "بيانات عامة", "General Data": "بيانات عامة", "Features": "المميزات",
    "Recommended max. PV array size": "أقصى حجم موصى به لمصفوفة PV",
    "Max. usable PV input power": "أقصى قدرة دخل PV قابلة للاستخدام",
    "Max. input voltage": "أقصى جهد دخل", "Rated voltage": "الجهد المقنن", "Start-up voltage": "جهد بدء التشغيل",
    "MPPT voltage range": "نطاق جهد MPPT", "Max. input current": "أقصى تيار دخل",
    "Max. short circuit current": "أقصى تيار قصر", "MPPT number / Max. input strings number": "عدد MPPT / أقصى عدد سلاسل",
    "THDi": "THDi", "Battery type": "نوع البطارية", "Battery voltage range": "نطاق جهد البطارية",
    "Max. charge / discharge power": "أقصى قدرة شحن / تفريغ", "Max. charge / discharge current": "أقصى تيار شحن / تفريغ",
    "Max. charge / discharge power of each input": "أقصى قدرة شحن / تفريغ لكل مدخل",
    "Max. charge / discharge current of each port": "أقصى تيار شحن / تفريغ لكل منفذ",
    "Number of battery ports": "عدد منافذ البطارية", "Communication": "الاتصال",
    "Rated output power": "قدرة الخرج المقننة", "Rated grid voltage": "جهد الشبكة المقنن",
    "Rated grid frequency": "تردد الشبكة المقنن", "Rated grid output current": "تيار الخرج المقنن للشبكة",
    "Max. output current": "أقصى تيار خرج", "Power factor": "معامل القدرة",
    "Input voltage range": "نطاق جهد الدخل", "Frequency range": "نطاق التردد", "Max. input power": "أقصى قدرة دخل",
    "Rated input current": "تيار الدخل المقنن", "Rated input voltage": "جهد الدخل المقنن",
    "Rated input frequency": "تردد الدخل المقنن", "Max. apparent output power": "أقصى قدرة خرج ظاهرية",
    "Back-up switch time": "زمن التحويل للاحتياطي", "Rated output voltage": "جهد الخرج المقنن",
    "Rated frequency": "التردد المقنن", "Rated output current": "تيار الخرج المقنن",
    "Max. AC passthrough current": "أقصى تيار AC مار", "THDv (@linear load)": "THDv عند حمل خطي",
    "Max. efficiency": "أقصى كفاءة", "EU efficiency": "الكفاءة الأوروبية",
    "BAT charged by PV / AC max. efficiency": "أقصى كفاءة شحن البطارية من PV / AC",
    "BAT charged by PV max. efficiency": "أقصى كفاءة شحن البطارية من PV",
    "BAT discharged to AC max. efficiency": "أقصى كفاءة تفريغ البطارية إلى AC",
    "BAT charged / discharged to AC max. efficiency": "أقصى كفاءة شحن / تفريغ البطارية إلى AC",
    "Surge protection": "الحماية من التدفق المفاجئ", "Ground fault monitoring": "مراقبة أعطال التأريض",
    "Integrated AFCI 2.0": "AFCI 2.0 مدمج", "DC reverse-polarity protection": "حماية DC من عكس القطبية",
    "Anti-islanding protection": "الحماية من التشغيل المنعزل", "Output over current protection": "حماية الخرج من زيادة التيار",
    "Short circuit protection": "الحماية من القصر", "Integrated DC switch": "مفتاح DC مدمج",
    "PV over voltage protection": "حماية PV من زيادة الجهد", "Battery reverse protection": "حماية البطارية من عكس القطبية",
    "Protection class / Over voltage category": "فئة الحماية / فئة الجهد الزائد",
    "Max. allowable phase imbalance (grid & back-up)": "أقصى عدم توازن مسموح بين الأطوار",
    "Max. power per phase (grid & back-up)": "أقصى قدرة لكل طور (الشبكة والاحتياطي)",
    "Dimensions (W × H × D)": "الأبعاد (W × H × D)", "Weight": "الوزن", "Topology": "الطوبولوجيا",
    "Self-consumption (night)": "الاستهلاك الذاتي ليلاً", "Operating ambient temperature range": "نطاق حرارة التشغيل المحيطة",
    "Relative humidity": "الرطوبة النسبية", "Ingress protection": "درجة الحماية",
    "Noise emission (typical)": "مستوى الضجيج النموذجي", "Cooling concept": "طريقة التبريد",
    "Max. operation altitude": "أقصى ارتفاع للتشغيل", "Grid connection standard": "معيار الربط بالشبكة",
    "Grid connection standard ①": "معيار الربط بالشبكة ①", "Safety / EMC standard": "معايير السلامة والتوافق EMC",
    "Safety / EMC standard ①": "معايير السلامة والتوافق EMC ①",
    "DC connection": "توصيل DC", "AC connection": "توصيل AC", "PV connection": "توصيل PV",
    "Battery connection": "توصيل البطارية", "Display": "الشاشة", "Communication interface": "واجهات الاتصال",
    "Preliminary": "مبدئي",
}
VAL = {
    "Li-ion / Lead-acid": "ليثيوم أيون / رصاص حمضي", "Li-ion": "ليثيوم أيون",
    "> 0.99 (0.8 leading - 0.8 lagging)": "> 0.99 (من 0.8 متقدم إلى 0.8 متأخر)",
    "2 times of rated power, 10 s": "ضعف القدرة المقننة لمدة 10 s",
    "1.6 time of rated power, 10 s": "1.6 ضعف القدرة المقننة لمدة 10 s",
    "1.6 times of rated power, 2 s": "1.6 ضعف القدرة المقننة لمدة 2 s",
    "75-100K: 1.6 times of rated power, 10 s; 2 times of rated power, 200 ms;":
        "75-100K: ‏1.6 ضعف القدرة المقننة لمدة 10 s، وضعف القدرة لمدة 200 ms",
    "125K: 1.4 times of rated power, 10 s; 1.6 times of rated power, 200 ms":
        "125K: ‏1.4 ضعف القدرة المقننة لمدة 10 s، و1.6 ضعف لمدة 200 ms",
    "Yes": "نعم", "Optional": "اختياري", "Optional (Brazil: Yes)": "اختياري (البرازيل: نعم)",
    "I / II (PV and BAT), III (MAINS and BACKUP and GEN)": "I / II للألواح والبطارية، III للشبكة والاحتياطي والمولد",
    "Transformerless": "بدون محوّل", "Intelligent fan-cooling": "تبريد ذكي بالمراوح",
    "Intelligent redundant fan-cooling": "تبريد ذكي بمراوح احتياطية",
    "MC4 plug (PV port) / Terminal Block (BAT port)": "قابس MC4 لمنفذ PV / أطراف توصيل لمنفذ البطارية",
    "MC4 connector": "موصل MC4", "MC4 Quick connection plug": "قابس توصيل سريع MC4",
    "Terminal connector": "موصل أطراف", "Terminal Block": "أطراف توصيل", "Terminal block": "أطراف توصيل",
    "OT terminal": "أطراف OT", "7.0\" LCD display & Bluetooth + APP": "شاشة LCD مقاس 7.0 بوصة + Bluetooth + تطبيق",
    "40% rated power": "40% من القدرة المقننة",
    "① Supporting parallel 140A input.": "① يدعم دخلاً متوازياً حتى 140A",
    "① This column only shows the planned certification standards. Please confirm the specific time of obtaining the standards with the local team.":
        "① يعرض هذا العمود معايير الاعتماد المخطط لها فقط، يرجى تأكيد موعد الحصول عليها مع الفريق المحلي.",
}


def spans(page):
    out = []
    for b in page.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            t = engine.norm(''.join(s['text'] for s in l['spans']))
            if t:
                s0 = l['spans'][0]
                out.append(dict(t=t, r=pymupdf.Rect(l['bbox']), size=s0['size'], color=s0['color'], bold='Semibold' in s0['font']))
    return out


def rebuild(en):
    src = pymupdf.open(en)
    sp = spans(src[1])
    W, H = src[1].rect.width, src[1].rect.height
    for s in sp:
        src[1].add_redact_annot(s['r'], fill=False)
    src[1].apply_redactions(images=0, graphics=0, text=0)
    out = pymupdf.open()
    p = out.new_page(width=W, height=H)
    p.show_pdf_page(p.rect, src, 1)
    x = p.get_contents()[0]
    c = out.xref_stream(x).decode()
    c = c.replace("q ", "q -1 0 0 1 %.4f 0 cm " % W, 1)
    out.update_stream(x, c.encode())
    p = out[0]
    miss = []
    for s in sp:
        t, r, sz, col = s['t'], s['r'], s['size'], s['color']
        w = 600 if s['bold'] else 400
        if t == "DATASHEET":
            engine.place(p, r, {"ar": LAB[t], "r": W - r.x0, "w": 700}, sz, col); continue
        if t.startswith("①"):
            engine.place(p, r, {"ar": VAL.get(t, t), "r": W - r.x0, "maxw": W - 2 * r.x0}, sz, col); continue
        if r.x0 < 150 and t in LAB:
            engine.place(p, r, {"ar": LAB[t], "r": W - r.x0, "w": w, "maxw": 150}, sz, col); continue
        if r.x0 < 60:
            miss.append(t)
        if t == "Preliminary":
            continue  # rotated watermark: dropped (would read mirrored)
        v = VAL.get(t, t)
        if not engine.AR.search(v) and "①" not in v:  # pure Latin/numeric value: draw as one LTR run so "< 10 ms" keeps its order
            fs = sz
            tw = engine.width(v, w, fs)
            if tw > 380: fs *= 380 / tw; tw = 380
            engine.LTR_DIRECT = True
            engine.put(p, W - (r.x0 + r.x1) / 2 + tw / 2, (r.y0 + r.y1) / 2, v, True, w, fs, "#%06x" % col)
            engine.LTR_DIRECT = False
            continue
        engine.place(p, r, {"ar": VAL.get(t, t), "cx": W - (r.x0 + r.x1) / 2, "center": True, "w": w, "maxw": 380}, sz, col)
    if miss:
        print("UNTRANSLATED LABELS:", miss, file=sys.stderr)
    return out


if __name__ == "__main__":
    for fam, (a, b) in FAM.items():
        pg = rebuild(f'{ROOT}/official/{fam}--{a}.pdf')
        for v in (a, b):
            dst = f'{ROOT}/official-ar/{fam}--{v}.pdf'
            d = pymupdf.open(dst)
            d.delete_page(1)
            d.insert_pdf(pg)
            d.subset_fonts()
            d.save(dst + '.tmp', garbage=4, deflate=True); d.close(); os.replace(dst + '.tmp', dst)
        print(fam, os.path.getsize(dst))
