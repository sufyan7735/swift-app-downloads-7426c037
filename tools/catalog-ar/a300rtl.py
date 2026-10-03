"""Optimus A300-HY Arabic page 2: mirror the English page geometry (RTL) and redraw every text.
Labels become right-anchored at the mirrored left edge; values/grid numbers stay centred in their mirrored cells."""
import sys; sys.path.insert(0, '/dev-server/tools/catalog-ar')
import pymupdf, engine
from engine import norm

EN = '/dev-server/public/catalogs/pylontech-optimus-a300-hy.pdf'
AR = '/dev-server/public/catalogs/official-ar/pylontech-optimus-a300-hy.pdf'
OUT = sys.argv[1] if len(sys.argv) > 1 else '/tmp/cat/a300-ar.pdf'

T = {
    'General Data': 'بيانات عامة',
    'Dimension (W*D*H mm,w/o inverter)': 'الأبعاد (عرض×عمق×ارتفاع mm، بدون إنفرتر)',
    'Weight (tons)': 'الوزن (طن)',
    'Working Temperature Range (℃)': 'نطاق حرارة التشغيل (℃)',
    'Protection Class': 'درجة الحماية',
    'Altitude (m)': 'الارتفاع (m)',
    'Humidity': 'الرطوبة',
    'Fire extinguishing': 'إطفاء الحريق',
    'Cooling System': 'نظام التبريد',
    'Cooling system consumption (kW, Cooling/Heating)': 'استهلاك نظام التبريد (kW، تبريد/تدفئة)',
    'Aux. Power Consumption (kW, continuous/peak, incl. HVAC)': 'استهلاك الطاقة المساعدة (kW، مستمر/ذروة، شامل HVAC)',
    'Max.parallel No.': 'أقصى عدد على التوازي',
    'Anti-corrosion': 'مقاومة التآكل',
    'Certification': 'الشهادات',
    'Battery Data': 'بيانات البطارية',
    'Battery Type': 'نوع البطارية',
    'Nominal Capacity (kWh)': 'السعة الاسمية (kWh)',
    'Continuous Operation C-rate': 'معدل C للتشغيل المستمر',
    'Max.Operation Current (A)': 'أقصى تيار تشغيل (A)',
    'Depth of Discharge': 'عمق التفريغ',
    'Cycle Life': 'عمر الدورات',
    'DC Voltage Range (Vdc)': 'نطاق جهد DC ‏(Vdc)',
    'Nominal operation current (A)': 'تيار التشغيل الاسمي (A)',
    'Round-trip Efficiency@ 0.5C-rate': 'كفاءة الدورة الكاملة عند 0.5C',
    'Hybrid Data On-grid Mode': 'البيانات الهجينة – وضع الربط بالشبكة',
    'Rated AC Power (kW)': 'قدرة AC المقننة (kW)',
    'Rated AC Output Voltage (Vac)': 'جهد خرج AC المقنن (Vac)',
    'Rated AC Output Frequency (Hz)': 'تردد خرج AC المقنن (Hz)',
    'Max AC Current (A)': 'أقصى تيار AC ‏(A)',
    'Overload Capacity': 'قدرة التحميل الزائد',
    'AC PF': 'معامل القدرة AC',
    'CEC Efficiency': 'كفاءة CEC',
    'Isolation Type': 'نوع العزل',
    'Response Time (On-Grid to Off-Grid)': 'زمن الاستجابة (من الشبكة إلى خارجها)',
    'Operation Mode': 'وضع التشغيل',
    'Communication Type': 'نوع الاتصال',
    'Operation Logic': 'منطق التشغيل',
    # values containing words
    'Aerosol': 'إيروسول',
    'Air Cooling': 'تبريد هوائي',
    'Li-ion (LFP)': 'ليثيوم أيون (LFP)',
    '98% (single string)': '98% (سلسلة واحدة)',
    '560~720 (single string)': '560~720 (سلسلة واحدة)',
    '76A (Linear Load)': '76A (حمل خطي)',
    'Non-isolation': 'بدون عزل',
    'Peak Shaving/Energy Shifting/Self-Consumption/Backup': 'تخفيض الذروة / نقل الطاقة / الاستهلاك الذاتي / احتياطي',
    # system configuration
    'System configuration': 'تكوين النظام',
    'Inverter Type': 'نوع الإنفرتر',
    'Inverter QTY': 'عدد الإنفرترات',
    'Cabinet': 'عدد',
    'QTY': 'خزائن',
    'Min.': 'الحد',
    'configuration': 'التكوين',
    'Optional': 'تكوين',
    'Standard': 'تكوين',
    'OPTIM US / A300-HY': 'OPTIM US / A300-HY',
    '*Degration at temperatures below 10℃ or above 40℃': '*ينخفض الأداء عند درجات حرارة أقل من 10℃ أو أعلى من 40℃',
}
# legend second lines differ per entry
LEGEND = {'Min.': ('تكوين', 'الحد الأدنى'), 'Optional': ('تكوين', 'اختياري'), 'Standard': ('تكوين', 'قياسي')}

src = pymupdf.open(EN)
sp = src[1]
W = sp.rect.width
lines = engine.lines(sp)
# font weight per line
weights = {}
for b in sp.get_text('dict')['blocks']:
    for l in b.get('lines', []):
        f = l['spans'][0]['font']
        weights[tuple(round(v, 1) for v in l['bbox'])] = 700 if 'Bold' in f else 600 if 'SemiBold' in f else 400

clean = pymupdf.open(EN)
cp = clean[1]
for b in cp.get_text('dict')['blocks']:
    for l in b.get('lines', []):
        cp.add_redact_annot(pymupdf.Rect(l['bbox']))
cp.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)

out = pymupdf.open(AR)  # keep Arabic page 1 untouched
out.delete_page(1)
pg = out.new_page(width=W, height=sp.rect.height)
pg.show_pdf_page(pg.rect, clean, 1)
x = pg.get_contents()[0]
out.update_stream(x, b'q -1 0 0 1 %.4f 0 cm\n' % W + out.xref_stream(x) + b'\nQ\n')

skip_legend2 = set()
for i, L in enumerate(lines):
    t, r = L['t'], L['bbox']
    size = L['size']
    col = '#%06x' % L['color']
    w = weights.get(tuple(round(v, 1) for v in r), 400)
    cy = (r.y0 + r.y1) / 2 + (size * 0.05)
    if t == 'configuration':
        continue
    if t in LEGEND:  # legend: two Arabic lines right-anchored beside the mirrored swatch
        a, b2 = LEGEND[t]
        size = 8
        xr = W - r.x0
        engine.draw_line(pg, xr, cy, a, w, size, col)
        if b2:
            engine.draw_line(pg, xr, cy + 9.5, b2, w, size, col)
        continue
    ar = T.get(t, t).replace('℃', '°C')
    if r.y0 > 640 and r.x0 > 120 and r.x1 < 170 and size < 9:
        size = 7.2
    if t == 'OPTIM US / A300-HY':  # header tag: mirror to the left margin, keep reading order
        lw = engine.line_width(ar, w, size)
        engine.draw_line(pg, W - r.x1 + lw, cy, ar, 700, size, col)
        continue
    label = r.x0 < 80 or t in ('Cabinet', 'QTY', 'Inverter Type')
    if label and t not in ('A300-', 'HY'):
        s = size
        maxw = (W - r.x0) - 290 if r.y1 < 600 and r.x0 < 80 and t not in T.get('', '') else 999
        lw = engine.line_width(ar, w, s)
        if r.y1 < 600 and r.x0 < 80 and size < 9 and lw > 220:
            s = size * 220 / lw
        engine.draw_line(pg, W - r.x0 - (3 if r.x0 < 80 else 0), cy, ar, w, s if t not in ('Cabinet','QTY') else 7, col)
    else:
        s = size
        lw = engine.line_width(ar, w, s)
        if lw > 245:
            s = s * 245 / lw; lw = 245
        cx = W - (r.x0 + r.x1) / 2
        engine.draw_line(pg, cx + lw / 2, cy, ar, w, s, col)

out.save(OUT, garbage=4, deflate=True)
print('saved', OUT)
