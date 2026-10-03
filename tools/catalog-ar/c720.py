import sys; sys.path.insert(0, "/tmp/cat")
from engine import build, render
H = lambda a, **k: dict(ar=a, w=700, **k)
L = lambda a, **k: dict({"ar": a, "w": 600, "r": 158, **k})
B = lambda a, **k: dict(ar=a, w=400, **k)
p0 = {
 "15": dict(ar="15", w=700),
 "years of product warranty": B("سنة ضمان للمنتج", size=13),
 "30 years of linear warranty": H("30 سنة ضمان أداء خطي للقدرة"),
 "MAX EFFICIENCY": B("أقصى كفاءة", size=13),
 "POWER OUTPUT": B("قدرة الخرج", size=13),
 "* Please refer to Suntech Standard Module Installation Manual for details.": B("* يُرجى الرجوع إلى دليل التركيب القياسي من Suntech للتفاصيل."),
 "*** WEEE only for EU market.": B("*** شعار WEEE لسوق الاتحاد الأوروبي فقط."),
 "** Please refer to Suntech Limited Warranty for details.": B("** يُرجى الرجوع إلى شروط الضمان المحدود من Suntech للتفاصيل."),
 "**** Suntech reserves the right to the final.": B("**** تحتفظ Suntech بحق التفسير النهائي."),
 "HALF-CELL N-Type TOPCon": H("لوح نصف خلية N-Type TOPCon", size=12),
 "Glass-Glass BIFACIAL MODULE": H("ثنائي الوجه زجاج-زجاج", size=12),
 "Higher value for customers": H("قيمة أعلى للعملاء"),
 "effectively reduce system BOS cost, achieve lower LCOE, and": B("يخفض تكلفة مكونات النظام (BOS) بفعالية، ويحقق تكلفة طاقة مستوية (LCOE) أقل،", dy=2.5),
 "improve project profitability": B("ويرفع ربحية المشروع", dy=2.5),
 "Compatible with mainstream trackers": H("متوافق مع أنظمة التتبّع الشائعة"),
 "the module design is highly compatible with power plant tracking systems,": B("تصميم اللوح متوافق بدرجة عالية مع أنظمة التتبّع في محطات الطاقة،", dy=2.5),
 "which offers a cost-effective solution for large power plants": B("مما يوفّر حلاً اقتصادياً للمحطات الكبيرة", dy=2.5),
 "Withstand harsh environments": H("مقاومة البيئات القاسية"),
 "through the high salt spray LID ammonia resistance test, more": B("اجتاز اختبارات رذاذ الملح العالي وLID ومقاومة الأمونيا،", dy=2.5),
 "adaptable to high temperature, strong wind, ice, snow and salt water": B("وأكثر تكيّفاً مع الحرارة المرتفعة والرياح القوية والجليد والثلوج", dy=2.5),
 "corrosion of the climate environment": B("وتآكل المياه المالحة في البيئات المناخية", dy=2.5),
 "Extended wind and snow load tests": H("اختبارات موسّعة لأحمال الرياح والثلوج"),
 "Module certified to withstand extreme wind (2400 Pascal)": B("اللوح معتمد لتحمّل رياح شديدة (2400 Pascal)", dy=2.5),
 "and snow loads (5400 Pascal)": B("وأحمال ثلوج حتى (5400 Pascal)", dy=2.5),
 "Environment Management System": B("نظام الإدارة البيئية"),
 "Occupational Health and Safety": B("الصحة والسلامة المهنية"),
 "Quality Management System": B("نظام إدارة الجودة"),
 "Social Responsibility Standards": B("معايير المسؤولية الاجتماعية"),
 "Guideline for Module Design": B("إرشادات تصميم اللوح"),
 "IEC 60068-2-68 Dust and Sand": B("IEC 60068-2-68  مقاومة الغبار والرمال"),
 "IEC 61730-2 (UL790) Fire Class C": B("IEC 61730-2 (UL790)  فئة الحريق C"),
 "61701 Salt-mist Certification": B("61701  مقاومة رذاذ الملح"),
 "62716 Ammonia Certification": B("62716  مقاومة الأمونيا"),
}
p1 = {
 "Mechanical Characteristics": H("الخصائص الميكانيكية"),
 "Temperature Characteristics": H("الخصائص الحرارية"),
 "Electrical Characteristics": H("الخصائص الكهربائية"),
 "33 pieces per pallet": B("33 لوحاً لكل منصة"),
 "594 pieces per container /40'HC": B("594 لوحاً لكل حاوية 40'HC"),
 "1325×1120×2510 mm per pallet 1264.4 kg per pallet": B("أبعاد المنصة 1325×1120×2510 mm    وزن المنصة 1264.4 kg"),
 "Nominal Module Operating Temperature (NMOT)": L("درجة حرارة التشغيل الاسمية (NMOT)", r=210),
 "Solar Cell": L("الخلية الشمسية"),
 "N-type monocrystalline silicon": B("سيليكون أحادي البلورة N-type"),
 "No. of Cells": L("عدد الخلايا"),
 "Dimensions": L("الأبعاد"),
 "2384 × 1303 × 33 mm (93.9 × 51.3 × 1.3 inches)": B("2384 × 1303 × 33 mm (93.9 × 51.3 × 1.3 بوصة)"),
 "Weight": L("الوزن"),
 "Front \\ Back Glass": L("الزجاج الأمامي / الخلفي"),
 "2.0+2.0 mm (0.079+ 0.079 inches) semi-tempered glass": B("زجاج نصف مقسّى 2.0+2.0 mm (0.079+0.079 بوصة)"),
 "Output Cables": L("كابلات الخرج"),
 "(-) 350 mm and (+) 160 mm in length": B("بطول (-) 350 mm و(+) 160 mm"),
 "or customized length": B("أو بطول حسب الطلب"),
 "Junction Box": L("صندوق التوصيل"),
 "IP68 rated (3 bypass diodes)": B("IP68 (3 ثنائيات تجاوز)"),
 "Operating Module Temperature": L("حرارة تشغيل اللوح"),
 "-40 °C to +85 °C": B("من ‎-40 °C إلى ‎+85 °C"),
 "Maximum System Voltage": L("أقصى جهد للنظام"),
 "Connectors": L("الموصّلات"),
 "Maximum Series Fuse Rating": L("أقصى تصنيف لفيوز السلسلة"),
 "Power Tolerance": L("تفاوت القدرة"),
 "Refer. Bifaciality Factor": L("معامل ثنائية الوجه المرجعي"),
 "For tracker installation*": B("لتركيب أنظمة التتبّع، يُرجى مراجعة Suntech لمعلومات الأحمال الميكانيكية"),
 "Reference to 710W Front": B("بالرجوع إلى الوجه الأمامي 710W"),
 "Rearside Power Gain": L("الكسب من الوجه الخلفي"),
 "Maximum Power at STC (Pmax)": L("القدرة القصوى عند STC (Pmax)"),
 "Optimum Operating Voltage": L("جهد التشغيل الأمثل"),
 "Optimum Operating Current": L("تيار التشغيل الأمثل"),
 "Open Circuit Voltage (Voc/V)": L("جهد الدائرة المفتوحة (Voc/V)"),
 "Short Circuit Current (Isc/A)": L("تيار القصر (Isc/A)"),
 "Packing Configuration": L("إعدادات التعبئة"),
 "Frame": L("الإطار"),
 "Anodized aluminum alloy frame": B("إطار من سبائك الألمنيوم المؤكسد"),
 "Module Type": L("طراز اللوح"),
 "Testing Condition": L("ظروف الاختبار"),
 "Maximum Power (Pmax/W)": L("القدرة القصوى (Pmax/W)"),
}
EX={}
build0=None

p1.update({
 "(Vmp/V)": L("(Vmp/V)", w=400), "(Imp/A)": L("(Imp/A)", w=400), 
 "2384 × 1303 × 33 mm (93.9 × 51.3 × 1.3 inches)": B("2384 × 1303 × 33 mm  /  93.9 × 51.3 × 1.3 بوصة"),
 "2.0+2.0 mm (0.079+ 0.079 inches) semi-tempered glass": B("زجاج نصف مقسّى 2.0+2.0 mm  /  0.079+0.079 بوصة"),
 "(-) 350 mm and (+) 160 mm in length": B("بطول 350 mm للسالب و160 mm للموجب"),
 "Maximum Series Fuse Rating": L("أقصى فيوز للسلسلة"),
 "Nominal Module Operating Temperature (NMOT)": L("درجة حرارة التشغيل الاسمية (NMOT)", r=160),
 "Graphs*": H("المنحنيات   تيار-جهد وقدرة-جهد (710W)", size=12),
 "STC: lrradiance*": B("STC: إشعاع 1000 W/m²، حرارة اللوح 25 °C، AM=1.5؛  NMOT: إشعاع 800 W/m²، حرارة محيطة 20 °C، AM=1.5، سرعة رياح 1 m/s؛  تفاوت القياس ضمن ±3%"),
 "IP68 rated (3 bypass diodes)": B("IP68 مع 3 ثنائيات تجاوز"),
 "-40 °C to +85 °C": B("من −40 °C إلى +85 °C"),
})
p0.update({
 "IEC 60068-2-68 Dust and Sand": B("IEC 60068-2-68   الغبار والرمال"),
 "IEC 61730-2 (UL790) Fire Class C": B("IEC 61730-2 (UL790)   فئة الحريق C"),
 "61701 Salt-mist Certification": dict(ar="61701   رذاذ الملح", l=479),
 "62716 Ammonia Certification": dict(ar="62716   الأمونيا", l=479),
 "HALF-CELL N-Type TOPCon": H("لوح نصف خلية N-Type TOPCon", size=12),
})
W = lambda a, **k: dict({"ar": a, "white": True, "color": 0x585858, "size": 7, **k})
ex = {1: [
 ((43,499,116,508), W("كفاءة اللوح (%)", w=600, r=158)),
 ((43,648,116,657), W("كفاءة اللوح (%)", w=600, r=158)),
 ((43,700,160,709), W("معامل حرارة Pmax", w=600, r=160)),
 ((43,713,160,722), W("معامل حرارة Voc", w=600, r=160)),
 ((43,725,160,735), W("معامل حرارة Isc", w=600, r=160)),
 ((39,535,213,551), W("الكسب الإضافي من الوجه الخلفي", w=700, size=12, color=0x231f20, l=40)),
 ((38,740,578,759), W("تتوفر معلومات التركيب والتشغيل في دليل التركيب. جميع القيم الواردة في هذه النشرة قابلة للتغيير دون إشعار مسبق، وقد تختلف المواصفات قليلاً.\nجميع المواصفات مطابقة للمعيار EN 50380. اختلاف ألوان الألواح عن الصور أو تغيّر لونها دون التأثير على أدائها لا يُعدّ انحرافاً عن المواصفات.", size=5, r=576, dy=-3, lh=7)),
], 0: [
 ((298,721,540,734), W("تدهور السنة الأولى 1%          التدهور السنوي 0.40%", size=7.5, r=538)),
]}
p1["Reference to 710W Front"] = B("بالرجوع إلى الوجه الأمامي 710W", l=217)
from engine import dump
R0 = 562
for k in list(p0):
    if any(k.startswith(x) for x in ("Higher value","Compatible","Withstand","Extended","effectively","improve","the module","which offers","through","adaptable","corrosion","Module certified","and snow")):
        v = p0[k]; v["r"] = R0
p0["15"] = None
p0["years of product warranty"] = dict(ar="15 سنة ضمان للمنتج", w=700, size=16, r=298, color=0x231f20)
p0["30 years of linear warranty"] = H("30 سنة ضمان أداء خطي للقدرة", r=298)
for k in ("61701 Salt-mist Certification","62716 Ammonia Certification","IEC 60068-2-68 Dust and Sand","IEC 61730-2 (UL790) Fire Class C"):
    p0.pop(k, None)
ex[0] += [((463,529,592,569), W("", w=400))]
for i,(a) in enumerate(["مقاومة رذاذ الملح  IEC 61701","مقاومة الأمونيا  IEC 62716","الغبار والرمال  IEC 60068-2-68","فئة الحريق C  IEC 61730-2 (UL790)"]):
    y=[536,545,555,563][i]
    ex[0].append(((560,y-4,561,y+4), dict(ar=a, r=588, size=7, color=0x585858, white=True, bg=(1,1,1))))
build("/dev-server/public/catalogs/official/suntech-stp720s-d66-nsh.pdf", "/tmp/cat/s720.pdf", {0: p0, 1: p1}, ex)
render("/tmp/cat/s720.pdf", "/tmp/cat/s720")
