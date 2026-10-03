"""catalog-2: Pylontech RV12100CH — rebuilt RTL from the English original."""
import sys; sys.path.insert(0, '/dev-server/tools/catalog-ar')
import engine, os, pymupdf

SRC = '/dev-server/public/catalogs/catalog-2.pdf'
DST = '/dev-server/public/catalogs/official-ar/catalog-2.pdf'
LL, LV = 284, 168   # left table: label right edge, value right edge
RL, RV = 568, 452   # right table
W = 0xffffff


def lab(t, r=LL): return {"ar": t, "r": r, "w": 600}
def val(t, r=LV, **k): return dict({"ar": t, "r": r}, **k)
def hdr(t, r=LL): return {"ar": t, "r": r, "w": 700, "color": W}


p0 = {
    "RV12100CH DATA SHEET·V1.0": {"ar": "نشرة مواصفات RV12100CH · V1.0", "l": 37, "color": W},
    "Voltage:12.8 V | Capacity: 100 Ah | Energy: 1280 Wh": {"ar": "الجهد: 12.8 V | السعة: 100 Ah | الطاقة: 1280 Wh", "l": 34, "w": 400, "dy": 16},
    "Electrical Specification": hdr("المواصفات الكهربائية"),
    "Mechanical Specification": hdr("المواصفات الميكانيكية", RL),
    "Discharge Specification": hdr("مواصفات التفريغ"),
    "Other": hdr("أخرى", RL),
    "Charge Specification": hdr("مواصفات الشحن"),
    "Environment Specification": hdr("المواصفات البيئية"),
    "Dimensions": {"ar": "الأبعاد", "r": RL, "w": 700},
    # left table
    "Nominal Voltage": lab("الجهد الاسمي"), "12.8 VDC": val("12.8 VDC"),
    "Nominal Capacity": lab("السعة الاسمية"), "100 Ah": val("100 Ah"),
    "Internal Resistance": lab("المقاومة الداخلية"), "< 10 mΩ": val("<10 mΩ"),
    "Self Discharge": lab("التفريغ الذاتي"), "≤ 3% per month": val("≤3% شهرياً"),
    "Max. Batteries in Parallel": lab("أقصى عدد بطاريات على التوازي"), "8": val("8"),
    "Design Life": lab("العمر التصميمي"), "≥ 10 years": val("10 سنوات على الأقل"),
    "Short Circuit Current Duration": lab("مدة تيار القصر"), "< 1 kA/100 us": val("<1 kA/100 µs"),
    "Cycle Life": lab("عمر الدورات"), "> 4500 (80% DOD, 0.5 C, 25 °C)": val(">4500 دورة، 80% DOD، 0.5C، 25 °C"),
    "Max. Continuous Discharging Current": lab("أقصى تيار تفريغ مستمر"),
    "Peak Discharging Current": lab("تيار التفريغ الأقصى اللحظي"), "200 A@10 s": val("200 A لمدة 10 s"),
    "Recommended Charging Current": lab("تيار الشحن الموصى به"), "≤50 A": val("≤50 A"),
    "Max. Continuous Charging Current": lab("أقصى تيار شحن مستمر"),
    "Recommended Charging Voltage": lab("جهد الشحن الموصى به"), "14 V ~14.4 V": val("14~14.4 V"),
    "Storage Temperature Range": lab("نطاق حرارة التخزين"),
    "-4 °F ~140 °F (-20 °C ~ 60 °C)": val("من −20 °C إلى 60 °C"),
    "Recommended Storage Temperature": lab("حرارة التخزين الموصى بها"),
    "50 °F ~104 °F (10 °C ~ 40 °C)": val("من 10 °C إلى 40 °C"),
    "Operating Temperature": lab("درجة حرارة التشغيل"),
    "-4 °F ~ 122 °F (-20 °C ~ 50 °C)": val("من −20 °C إلى 50 °C"),
    "*If charging is required when the": val("*عند الحاجة للشحن في حرارة أقل\nمن 0 °C، صِل الشاحن لتفعيل\nغشاء التسخين، وتبدأ البطارية\nالشحن عندما تسخن الخلايا\nإلى أكثر من 0 °C", color=0xff0000, size=6.5, lh=9.3, dy=3),
    "temperature is below 32 °F (0 °C),": None, "please connect the charger to": None,
    "enable the heating film. The battery": None, "starts charging when the cell": None,
    "temperature is heated to above": None, "32 °F (0 °C).": None,
    "Relative Humidity": lab("الرطوبة النسبية"), "5% ~ 95%": val("من 5% إلى 95%"),
    # right table
    "Dimensions(L × W × H)": lab("الأبعاد (الطول × العرض × الارتفاع)", RL),
    "11.81 × 6.3 × 8.27 in": None, "(300 × 160 ×210 mm)": val("300 × 160 × 210 mm", RV, dy=-6.5),
    "Weight": lab("الوزن", RL), "Approx. 26.46 lbs (12 kg)": val("12 kg تقريباً", RV),
    "Terminal Type": lab("نوع الطرف", RL), "M8 × 1.25 × 14 mm": val("M8 × 1.25 × 14 mm", RV),
    "Terminal Torque": lab("عزم ربط الطرف", RL), "8 ± 1 Nm": val("8 ± 1 Nm", RV),
    "Case Material": lab("مادة الغلاف", RL), "Metal": val("معدن", RV),
    "Enclosure Protection": lab("درجة حماية الغلاف", RL), "IP20": val("IP20", RV),
    "Cell Type-chemistry": lab("نوع كيمياء الخلية", RL), "LiFePO4": val("LiFePO4", RV),
    "Cooling": lab("التبريد", RL), "Natural Cooling": val("تبريد طبيعي", RV),
    "Certifications": lab("الشهادات", RL), "UN38.3 MSDS": val("UN38.3، MSDS", RV),
    "Max. Altitude": lab("أقصى ارتفاع تشغيل", RL), "13123 ft (4000 m)": val("4000 m", RV),
    "*Product performance is based on testing in a controlled environment. Your":
        {"ar": "*أداء المنتج مبني على اختبارات في بيئة مضبوطة، وقد تختلف النتائج",
         "r": RL, "color": 0xff0000, "size": 7.6},
    "results may vary due to several external and environmental factors.":
        {"ar": "بحسب عوامل خارجية وبيئية متعددة.", "r": RL, "size": 7.6},
}
# values shared by two rows ("100 A") are matched once by the engine -> handle explicitly
VALS_100A = [((186, 404, 215, 414), "100 A"), ((187, 488, 215, 498), "100 A")]

FL, FR = 288, 568  # feature text right edges (icons stay left of text)


def ft(t, r): return {"ar": t, "r": r, "w": 700, "size": 8.5}
def fd(t, r, **k): return dict({"ar": t, "r": r}, **k)


p1 = {
    "RV12100CH DATA SHEET·V1.0": {"ar": "نشرة مواصفات RV12100CH · V1.0", "l": 37, "color": W},
    "Charge at different rates at 77 °F (25 °C)": hdr("الشحن بمعدلات مختلفة عند 25 °C", 288),
    "Discharge at different rates at 113 °C (45 °C)": hdr("التفريغ بمعدلات مختلفة عند 45 °C", 568),
    "Discharge at different rates at -4 °F (-20 °C)": hdr("التفريغ بمعدلات مختلفة عند −20 °C", 288),
    "Discharge at different rates at 77 °F (25 °C)": hdr("التفريغ بمعدلات مختلفة عند 25 °C", 568),
    "Key Features": hdr("المزايا الرئيسية", 568),
    "MORE CAPACITY": ft("سعة أكبر", FL),
    "100% of usable energy allows the battery to fully discharge.": fd("طاقة قابلة للاستخدام بنسبة 100% تتيح تفريغ البطارية بالكامل.", FL, dy=1.5),
    "LONG CYCLE LIFE": ft("عمر دورات طويل", FR),
    "More than 4500 cycles at a depth of discharge of 80%.": fd("أكثر من 4500 دورة بعمق تفريغ 80%", FR, dy=1.5),
    "LIGHT WEIGHT": ft("وزن خفيف", FL),
    "50% lighter than lead-acid batteries of the same capacity.": fd("أخف بنسبة 50% من بطاريات الرصاص الحمضية بنفس السعة.", FL, dy=1.5),
    "REAL-TIME MONITORING": ft("مراقبة لحظية", FR),
    "The running indicator, alarm indicator and SoC indicators allow you to": fd("مؤشرات التشغيل والإنذار وحالة الشحن SoC تتيح لك\nمراقبة حالة البطارية لحظياً.", FR, lh=9, dy=1.5),
    "monitor battery status in real time.": None,
    "ENERGY EXPANSION": ft("توسعة الطاقة", FL),
    "Up to 8 batteries in parallel connection, building a 12 V 800 Ah battery": fd("حتى 8 بطاريات على التوازي لبناء نظام 12 V بسعة 800 Ah\nوبطاقة قصوى 10.24 kWh", FL, lh=8.5, dy=1.5),
    "system with a max. energy output of 10.24 kWh.": None,
    "LOW-TEMPERATURE HEATING": ft("تسخين في الحرارة المنخفضة", FR),
    "The heating film allows the battery to work in extreme cold.": fd("غشاء التسخين يتيح للبطارية العمل في البرد الشديد.", FR, dy=1.5),
    "LOW SELF-DISCHARGE LOSS": ft("تفريغ ذاتي منخفض", FL),
    "Supports to be stored for over 12 months if it has been disconnected": fd("يمكن تخزينها أكثر من 12 شهراً عند فصلها\nعن الأجهزة الأخرى.", FL, lh=8.5, dy=1.5),
    "from other devices.": None,
    "INTELLIGENT BMS": ft("نظام BMS ذكي", FR),
    "The built-in BMS manages charging and discharging status, helps in": fd("نظام BMS المدمج يدير الشحن والتفريغ، ويوازن الخلايا،\nويوفر حمايات متعددة.", FR, lh=8.5, dy=1.5),
    "balancing the individual cells, and provides multiple protections.": None,
    "Tel: +86-21-51317699 | E-mail: service@pylontech.com.cn | Web: en.pylontech.com.cn":
        {"ar": "الهاتف: +86-21-51317699 | البريد: service@pylontech.com.cn | الموقع: en.pylontech.com.cn", "r": 568},
    "5/F, No.71- 72, Lane 887, Zu Chongzhi Road, China (Shanghai) Pilot Free Trade Zone":
        {"ar": "الطابق 5، رقم 71-72، الممر 887، طريق Zu Chongzhi، منطقة التجارة الحرة التجريبية، شنغهاي، الصين", "r": 568},
}

p0["100 A"] = val("100 A")
engine.build(SRC, DST, {0: p0, 1: p1})

d = pymupdf.open(DST)
_s = pymupdf.open(SRC)
d[0].show_pdf_page(pymupdf.Rect(30, 110, 200, 150), _s, 0, clip=pymupdf.Rect(30, 110, 200, 150))
d.subset_fonts(); d.save(DST + '.tmp', garbage=4, deflate=True)
os.replace(DST + '.tmp', DST)
engine.render(DST, '/tmp/cat/c2n', 110)
print(os.path.getsize(DST))
