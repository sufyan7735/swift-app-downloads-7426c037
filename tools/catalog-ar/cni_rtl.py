"""Arabic RTL catalogs for HiTHIUM LEGEND 112C / LEGEND 112S and Pylontech OPTIMUS L260-HY.
Spec tables are mirrored about their own centre (label column moves right); product photos, logos and QR codes
stay untouched. Marketing text is translated in place, right-anchored to its original text block.
Usage: python3 cni_rtl.py <src-dir> <out-dir>   (src files: 112c.pdf 112s.pdf l260.pdf)"""
import sys, re; sys.path.insert(0, '/dev-server/tools/catalog-ar')
import pymupdf, engine
engine.LTR_DIRECT = True  # pure-latin runs via insert_text: keeps '-25 ~ 55' in reading order

SRC, OUT = sys.argv[1], sys.argv[2]
R = pymupdf.Rect

T = {
 # ---- shared ----
 'PRODUCT DETAILS': 'تفاصيل المنتج', 'Model': 'الموديل', 'Battery Type': 'نوع البطارية',
 'Battery Cycles': 'عدد دورات البطارية', 'Type of Cooling': 'نوع التبريد', 'Operating Temperature': 'حرارة التشغيل',
 'Storage Temperature': 'حرارة التخزين', 'Allow Relative Humidity': 'الرطوبة النسبية المسموحة',
 'Communication Interface': 'واجهة الاتصال', 'Approval Standards': 'معايير الاعتماد',
 'Product Features': 'مميزات المنتج', 'Contact:': 'للتواصل:', 'Tel:': 'هاتف:',
 'Business Cooperation': 'تعاون تجاري', 'website': 'الموقع',
 '*The above is for reference only, the specification sheet shall prevail.': '*البيانات أعلاه للاسترشاد فقط، ويُعتمد ورق المواصفات الرسمي.',
 '11000 cycles@(25℃, 100%DOD, 0.5P, @70%SOH)': '11000 دورة عند 25°C و 100%DOD و 0.5P و 70%SOH',
 'LiFePO4': 'LiFePO4',
 # ---- 112C ----
 'C&I ESS': 'C&I ESS', 'Safety & Reliability': 'الأمان والموثوقية',
 'High-Efficiency Energy': 'إدارة طاقة', 'Management': 'عالية الكفاءة',
 'Smart Configuration': 'تهيئة ذكية', 'Flexible Installation': 'تركيب مرن',
 'The cabinet is built to withstand harsh environ-': 'الخزانة مصممة لتحمّل البيئات القاسية،',
 'ments, with integrated temperature and smoke': 'مع مراقبة مدمجة للحرارة والدخان',
 'monitoring, along with aerosol fire suppression.': 'ونظام إطفاء حريق بالإيروسول.',
 'Intelligent thermal management algorithm': 'خوارزمية إدارة حرارية ذكية',
 'effectively improves system conversion efficiency.': 'ترفع كفاءة التحويل في النظام بفعالية.',
 'Output voltage levels and control strategies can be': 'يمكن تخصيص مستويات جهد الخرج',
 'customized based on specific requirements.': 'واستراتيجيات التحكم حسب المتطلبات.',
 'Modular DC/AC split design allows for flexible': 'تصميم معياري بفصل DC/AC يتيح',
 'parallel system expansion.': 'توسعة النظام بالتوازي بمرونة.',
 'Compound Mode': 'نمط التجميع', 'Rated Capacity': 'السعة المقننة', 'Rated Charge/': 'معدل الشحن/',
 'Discharge Ratio': 'التفريغ المقنن', 'Rated Energy': 'الطاقة المقننة', 'Rated Voltage': 'الجهد المقنن',
 'Operating Voltage Range': 'نطاق جهد التشغيل', 'Standard Charge': 'تيار الشحن/التفريغ',
 'Discharge Current': 'القياسي', 'Noise': 'الضوضاء', '＜75dB': 'أقل من 75dB', 'Air Cooling': 'تبريد هوائي',
 'Dimensions': 'الأبعاد', 'Battery Weight': 'وزن البطارية', 'Corrosion Resistance Grade': 'درجة مقاومة التآكل',
 'Levels Of Protection': 'درجة الحماية', '0-95% (no condensation)': '0-95% بدون تكثيف', '≥ 93%': '93% أو أكثر',
 '≤ 4000 (decreased above 2000m)': 'حتى 4000m، مع خفض الأداء فوق 2000m', 'DC Side Efficiency': 'كفاءة جانب DC',
 '485, CAN, Ethernet': '485، CAN، Ethernet', '-20℃-60℃': '-20°C ~ 60°C', 'Protection': 'الحماية',
 'Overtemperature/Undertemperature/Overcharge/Overcurrent/Undervoltage': 'حرارة زائدة / حرارة منخفضة / شحن زائد / تيار زائد / جهد منخفض',
 'Fire Protection System': 'نظام الحماية من الحريق', 'aerosol': 'إيروسول',
 'Charging: 0℃-55℃ Discharging: -20℃-55℃': 'الشحن من 0°C إلى 55°C، التفريغ من -20°C إلى 55°C',
 'Allowable Altitude Bbove': 'الارتفاع المسموح', 'Sea Level': 'عن سطح البحر',
 # ---- 112S ----
 'C&I Battery Pack': 'C&I Battery Pack', 'Built for Maximum Flexibility': 'مصمم لأقصى درجات المرونة',
 'Expandable Capacity': 'سعة قابلة للتوسعة',
 'Modular, stackable design allows capacity': 'تصميم معياري قابل للتكديس يتيح توسعة',
 'expansion up to 720kWh, easily adapting to': 'السعة حتى 720kWh، ويتكيّف بسهولة مع',
 'different site sizes and evolving energy demands.': 'أحجام المواقع المختلفة واحتياجات الطاقة المتنامية.',
 'Quick to Install. Easy to Deploy': 'تركيب سريع وتشغيل سهل',
 'Plug-and-play stack architecture enables fast system': 'بنية تكديس Plug-and-play تتيح تركيب النظام',
 'installation in less than 30 minutes, minimizing on-site': 'في أقل من 30 دقيقة، مما يقلل العمل في الموقع',
 'work and reducing deployment time.': 'ويختصر زمن التشغيل.',
 '15+ Years of Daily Cycling': 'أكثر من 15 عاماً من الدورات اليومية',
 'Built with HITHIUM 314Ah LFP cells rated for': 'مبني بخلايا HITHIUM LFP سعة 314Ah مصنّفة',
 '11,000 cycles, designed for long-term daily': 'لـ 11,000 دورة، ومصمم للتشغيل اليومي طويل',
 'operation, helping reduce battery replacements': 'الأمد، مما يقلل استبدال البطاريات',
 'and lifetime energy costs.': 'وتكاليف الطاقة على مدى العمر.',
 'Smart BMS with Intelligent': 'نظام BMS ذكي مع تبريد',
 'An intelligent Smart BMS combined with optimized': 'نظام إدارة بطاريات ذكي مع تحكم محسّن',
 'air-cooling control continuously monitors system': 'بالتبريد الهوائي يراقب حالة النظام باستمرار،',
 'status, enhances thermal stability, and helps ensure': 'ويعزز الاستقرار الحراري، ويساعد على ضمان',
 'safe, reliable operation at the system level.': 'تشغيل آمن وموثوق على مستوى النظام.',
 '-': None,
 'Module Stacking Quantity': 'عدد الوحدات القابلة للتكديس', 'Module Voltage/Capacity': 'جهد/سعة الوحدة',
 'System Operating Voltage': 'جهد تشغيل النظام', 'Maximum Charge/Discharge Current': 'أقصى تيار شحن/تفريغ',
 'System Energy Range': 'نطاق طاقة النظام', 'Standard Charge/Discharge Current': 'تيار الشحن/التفريغ القياسي',
 'Natural Cooling': 'تبريد طبيعي', 'Mounting Method': 'طريقة التركيب', 'Stack-style': 'تكديس رأسي',
 'Levels of Protection': 'درجة الحماية', '10% - 90% (No Condensation)': '10% - 90% بدون تكثيف',
 'Allowable Altitude Above Sea Level': 'الارتفاع المسموح عن سطح البحر', 'UN38.3 IEC62619 CE': 'UN38.3 IEC62619 CE',
 '770*435*1986mm (7 packs)': '770*435*1986mm (7 وحدات)', '770*435*1738mm (6 packs)': '770*435*1738mm (6 وحدات)',
 '770*435*1490mm (5 packs)': '770*435*1490mm (5 وحدات)', '770*435*1242mm (4 packs)': '770*435*1242mm (4 وحدات)',
 'System Size': 'أبعاد النظام',
 'Charging: 0': 'الشحن من 0°C إلى 45°C، التفريغ من -10°C إلى 45°C', '- 45': None, 'Discharging: -10': None,
 '-20': '-20°C ~ 60°C', '- 60': None,
 'Battery Pack': 'وحدة البطارية', 'Combination Mode': 'نمط التجميع', 'Operating Voltage': 'جهد التشغيل',
 'Nominal Voltage': 'الجهد الاسمي', 'Nominal Energy Capacity': 'الطاقة الاسمية', 'Single Module Weight': 'وزن الوحدة المفردة',
 'Nominal Capacity': 'السعة الاسمية', 'Dimensions (Width x Depth x Height )': 'الأبعاد (عرض × عمق × ارتفاع)',
 'Cycle Life': 'عمر الدورات', '≥11000 cycles@25℃±2℃，0.5P，70%SOH': '11000 دورة أو أكثر عند 25°C±2°C و 0.5P و 70%SOH',
 'Relative Humidity': 'الرطوبة النسبية', '10%～90%': '10% ~ 90%', '-20℃~60℃': '-20°C ~ 60°C',
 'Discharge Temperature': 'حرارة التفريغ', 'Charge Temperature': 'حرارة الشحن',
 'Storage Environment Temperature': 'حرارة بيئة التخزين', '0℃~45℃': '0°C ~ 45°C', '-10℃~45℃': '-10°C ~ 45°C',
 'High Voltage Battery Control Box': 'صندوق التحكم عالي الجهد', 'System Voltage': 'جهد النظام',
 'Maximum Operating Current': 'أقصى تيار تشغيل', '0℃～ 45℃': '0°C ~ 45°C', '- 10℃～ 45℃': '-10°C ~ 45°C',
 # ---- L260 ----
 'Hybrid Inverter Integrated': 'إنفرتر هجين مدمج', 'Extraordinary Performance': 'أداء استثنائي',
 'Superior Safety': 'أمان فائق', 'Easy Set-up & Maintenance': 'تركيب وصيانة سهلة',
 'Wide Temp': 'نطاق حرارة', 'Range': 'واسع', 'Back up': 'تحويل احتياطي', 'Switch Seamless': 'سلس',
 'Self-Consumption': 'الاستهلاك الذاتي', 'Peak Shaving': 'تقليم الذروة',
 'General Data': 'بيانات عامة', 'Dimension(W*H*D mm)': 'الأبعاد (عرض×ارتفاع×عمق mm)', 'Weight(T)': 'الوزن (طن)',
 'Working Temperature Range ( ℃)': 'نطاق حرارة التشغيل (°C)', 'Storage Temperature Range ( ℃)': 'نطاق حرارة التخزين (°C)',
 'Ac output voltage (V)': 'جهد خرج AC (V)', 'Frequency(Hz)': 'التردد (Hz)', 'System Efficiency (RTE)': 'كفاءة النظام (RTE)',
 'Normal auxiliary power consumption (kW)': 'استهلاك الطاقة المساعدة الاعتيادي (kW)', 'IP Rating': 'درجة الحماية IP',
 'Altitude(m)': 'الارتفاع (m)', 'Corrosion protection class': 'فئة الحماية من التآكل', 'Humidity': 'الرطوبة',
 'Cooling type': 'نوع التبريد', 'Fire Extinguishing': 'إطفاء الحريق', 'Explosion Relief Panel': 'لوحة تنفيس الانفجار',
 'Water fire protection': 'الحماية المائية من الحريق', 'Authentication level': 'الشهادات', 'Communication': 'الاتصال',
 'Battery Data': 'بيانات البطارية', 'Nominal Capacity (kWh)': 'السعة الاسمية (kWh)', 'DC Voltage Range(V)': 'نطاق جهد DC (V)',
 'Depth of discharge': 'عمق التفريغ', 'Standard Operation DC Current (A)': 'تيار التشغيل القياسي DC (A)',
 'Hybrid Inverter Data': 'بيانات الإنفرتر الهجين', 'Output AC': 'الخرج AC', 'Rated output power（kW）': 'قدرة الخرج المقننة (kW)',
 'Power factor': 'معامل القدرة', 'Max. apparent output power': 'أقصى قدرة خرج ظاهرية', 'Back-up switch time （ms）': 'زمن التحويل الاحتياطي (ms)',
 'THDi': 'THDi', 'Input DC (PV side)': 'المدخل DC (جانب الألواح)', 'Recommended max. PV array size（KW）': 'أقصى حجم موصى به للألواح (kW)',
 'MPPT voltage range（V）': 'نطاق جهد MPPT (V)', 'Max. input current（A）': 'أقصى تيار دخل (A)',
 'MPPT number/Max input strings number': 'عدد MPPT / أقصى عدد سلاسل',
 '< 3T': 'أقل من 3 طن', '-25~55': '-25°C ~ 55°C', '-20~60': '-20°C ~ 60°C', '3P/N/PE, 220 V / 380 V, 230 V / 400 V': '3P/N/PE، 220 V / 380 V، 230 V / 400 V',
 'Liqud cooling, 50% glycol solution': 'تبريد سائل، محلول جلايكول 50%',
 'combustible gas detector+smoke detector+ temperature detector+explosion-proof fan+Aerosol': 'كاشف غازات قابلة للاشتعال + كاشف دخان + كاشف حرارة + مروحة مقاومة للانفجار + إيروسول',
 'Optional': 'اختياري', 'Standard configuration': 'تكوين قياسي',
 'Anti-islanding protection/Over current protection/Short Circuit Protection/DC reverse-polarity protection': 'حماية ضد التشغيل المنعزل / حماية من التيار الزائد / حماية من القصر / حماية من عكس قطبية DC',
 '>0.99(0.8 leading -0.8 lagging)': 'أكبر من 0.99، من 0.8 متقدم إلى 0.8 متأخر',
 '1.2 times of rated power, 100 s; 1.4 times of rated power, 10 s; 1.6 times of rated power, 200 ms': '1.2 ضعف القدرة لمدة 100 s، و 1.4 ضعف لمدة 10 s، و 1.6 ضعف لمدة 200 ms',
 'Basic Parameters': 'المعايير الأساسية', 'Energy (kWh)': 'الطاقة (kWh)', 'Norminal Voltage (V)': 'الجهد الاسمي (V)',
 'Battery Capacity (Ah)': 'سعة البطارية (Ah)', 'Dimension (W*D*H, mm)': 'الأبعاد (عرض×عمق×ارتفاع، mm)', 'Weight (kg)': 'الوزن (kg)',
}

# per file: page -> list of (region, value_mode) mirrored about region centre. value_mode 'left' = values left-aligned
CFG = {
 '112c': {1: [(R(18, 15, 578, 732), 'left')]},
 '112s': {1: [(R(18, 15, 578, 812), 'left')], 2: [(R(18, 345, 578, 812), 'left')], 3: [(R(18, 468, 578, 715), 'left')]},
 'l260': {1: [(R(64, 98, 544, 668), 'center'), (R(253.6, 683.5, 539.3, 792), 'center')]},
}
FOOT = '*البيانات أعلاه للاسترشاد فقط، ويُعتمد ورق المواصفات الرسمي.'
# text drawn as vector outlines in the source: (rect to erase, arabic or None, size, colour, weight)
VEC = {'112s': {
 1: [(R(257, 573, 409, 585), 'حتى 4000m، مع خفض الأداء فوق 2000m', 10, '#333333', 400),
     (R(26, 786, 272, 798), FOOT, 8, '#9a9a9a', 400), (R(309, 361, 474, 371), None, 0, '', 0), (R(271, 391, 312, 401), None, 0, '', 0)],
 2: [(R(26, 787, 272, 798), FOOT, 8, '#9a9a9a', 400)],
 3: [(R(26, 693, 272, 703), FOOT, 8, '#9a9a9a', 400), (R(30, 743, 101, 758), 'للتواصل:', 13, '#000000', 600),
     (R(30, 771, 59, 787), 'هاتف:', 13, '#000000', 600), (R(418, 816, 505, 826), 'تعاون تجاري', 6.5, '#000000', 400),
     (R(528, 815, 559, 824), 'الموقع', 6.5, '#000000', 400)]}}
CENTERED = {'Wide Temp', 'Range', 'Back up', 'Switch Seamless', 'Self-Consumption', 'Peak Shaving'}
NAMES = {'112c': 'hithium-heroee-legend-112c', '112s': 'hithium-heroee-legend-112s', 'l260': 'pylontech-optimus-l260-hy'}


def draw(pg, xr, cy, ar, w, size, col):
    if not engine.AR.search(ar):
        engine.put(pg, xr, cy, ar, True, w, size, col)
    else:
        engine.draw_line(pg, xr, cy, ar, w, size, col)


def fix(s):
    return s.replace('℃', '°C').replace('（', '(').replace('）', ')').replace('＜', '<')


def weight(f):
    return 700 if ('Bold' in f or 'Black' in f or 'Heavy' in f) else 600 if ('Semi' in f or 'Medium' in f) else 400


def text_lines(page):
    out = []
    for b in page.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            sp = l['spans']; t = engine.norm(''.join(s['text'] for s in sp))
            if t:
                out.append(dict(t=t, bbox=R(l['bbox']), size=sp[0]['size'], color=sp[0]['color'], w=weight(sp[0]['font'])))
    return out


def mirrored_region(clean, pno, r):
    """one-page doc holding region r of clean[pno], mirrored about r's vertical centre line"""
    p = clean[pno]
    d = pymupdf.open(); q = d.new_page(width=p.rect.width, height=p.rect.height)
    q.show_pdf_page(r, clean, pno, clip=r)
    x = q.get_contents()[0]
    d.update_stream(x, b'q -1 0 0 1 %.4f 0 cm\n' % (r.x0 + r.x1) + d.xref_stream(x) + b'\nQ\n')
    return d


for key, name in NAMES.items():
    src = pymupdf.open(f'{SRC}/{key}.pdf')
    clean = pymupdf.open(f'{SRC}/{key}.pdf')
    regions_all = CFG[key]
    infos = []
    for pno, sp in enumerate(src):
        regs = regions_all.get(pno, [])
        L = text_lines(sp)
        infos.append(L)
        cp = clean[pno]
        for l in L:
            inreg = any(r.contains(l['bbox']) for r, _ in regs)
            tr = T.get(l['t'], l['t'])
            if inreg or tr != l['t']:
                if key == '112s' and pno in (2, 3) and l['size'] > 20:
                    continue  # big white-page title overlaps the model line: whited out at draw time instead
                bb = l['bbox']; c = (bb.y0 + bb.y1) / 2; k = l['size'] * 0.42
                cp.add_redact_annot(R(bb.x0, max(bb.y0, c - k), bb.x1, min(bb.y1, c + k)))
        cp.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)
        for vr, *_ in VEC.get(key, {}).get(pno, []):
            cp.add_redact_annot(vr)
        if VEC.get(key, {}).get(pno):
            cp.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED, text=pymupdf.PDF_REDACT_TEXT_NONE)
    clean = pymupdf.open('pdf', clean.tobytes())

    out = pymupdf.open()
    for pno, sp in enumerate(src):
        W, H = sp.rect.width, sp.rect.height
        pg = out.new_page(width=W, height=H)
        pg.show_pdf_page(pg.rect, clean, pno)
        regs = regions_all.get(pno, [])
        for r, _ in regs:
            pg.draw_rect(r, color=None, fill=(1, 1, 1), overlay=True)
            m = mirrored_region(clean, pno, r)
            pg.show_pdf_page(pg.rect, m, 0)
        L = infos[pno]
        for vr, ar, size, col, w in VEC.get(key, {}).get(pno, []):
            if not ar:
                continue
            cy = (vr.y0 + vr.y1) / 2 + size * 0.05
            reg = next((r for r, _ in regs if r.contains(vr)), None)
            draw(pg, (reg.x0 + reg.x1 - vr.x0) if reg else vr.x1, cy, ar, w, size, col)
        for l in L:
            t, b = l['t'], l['bbox']
            tr = T.get(t, t)
            reg = next(((r, mode) for r, mode in regs if r.contains(b)), None)
            if tr is None:
                continue
            if reg is None and tr == t:
                continue  # untouched original text (model names, numbers)
            if key == '112s' and pno in (2, 3) and l['size'] > 20:
                pg.draw_rect(R(b.x0, (b.y0 + b.y1) / 2 - l['size'] * 0.45, b.x1, (b.y0 + b.y1) / 2 + l['size'] * 0.8), color=None, fill=(1, 1, 1))
            ar = fix(tr); size = l['size']; col = '#%06x' % l['color']; w = l['w']
            cy = (b.y0 + b.y1) / 2 + size * 0.05
            lw = engine.line_width(ar, w, size) if engine.AR.search(ar) else engine.width(ar, w, size)
            if reg:
                r, mode = reg
                C = r.x0 + r.x1
                mid = (r.x0 + r.x1) / 2
                is_label = b.x0 < mid - 40 and (mode == 'left' or b.x0 < r.x0 + 30)
                if mode == 'center' and not is_label:
                    maxw = (r.x1 - r.x0) * 0.62 if r.width > 400 else r.width * 0.45
                    if lw > maxw:
                        size *= maxw / lw; lw = maxw
                    cx = C - (b.x0 + b.x1) / 2
                    draw(pg, cx + lw / 2, cy, ar, w, size, col)
                else:
                    draw(pg, C - b.x0, cy, ar, w, size, col)
            else:
                if t in CENTERED:
                    draw(pg, (b.x0 + b.x1) / 2 + lw / 2, cy, ar, w, size, col)
                    continue
                grp = [o['bbox'].x1 for o in L if abs(o['bbox'].x0 - b.x0) < 5 and abs(o['bbox'].y0 - b.y0) < 45]
                draw(pg, max(grp + [b.x1]), cy, ar, w, size, col)
    dst = f'{OUT}/{name}.pdf'
    out.save(dst, garbage=4, deflate=True)
    print('saved', dst)
