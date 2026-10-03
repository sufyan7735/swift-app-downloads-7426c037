"""catalog-5: Pylontech Fidus Battery Plus — rebuilt RTL from the English original."""
import sys; sys.path.insert(0, '/dev-server/tools/catalog-ar')
import engine, os, pymupdf

SRC = '/dev-server/public/catalogs/catalog-5.pdf'
DST = '/dev-server/public/catalogs/official-ar/catalog-5.pdf'
LR = 537            # label right edge (mirror of x=75)
C1, C2, CM = 311, 175, 243   # FB-L-16, FB-L-16-Pro, merged value centres (mirrored)
def lab(t): return {"ar": t, "r": LR, "w": 600}

p0 = {
    "Superior Safetyand Reliability": {"ar": "أمان وموثوقية فائقة", "r": 299, "w": 700, "size": 15},
    "Multi-layer protection design, built-in fire": {"ar": "تصميم حماية متعدد الطبقات مع وحدة", "r": 299, "w": 400, "dy": 3},
    "suppression module": {"ar": "إخماد حريق مدمجة", "r": 299, "w": 400, "dy": 3},
    "Designed for Extreme Conditions": {"ar": "مصممة للظروف القاسية", "r": 588, "w": 700, "size": 15},
    "Available in extreme cold region, against water jet, fully": {"ar": "تعمل في المناطق شديدة البرودة، ومقاومة لنفث الماء،", "r": 588, "w": 400, "dy": 3},
    "dustproofed, smoke & salty air resistant.": {"ar": "ومحكمة ضد الغبار، ومقاومة للدخان والهواء المالح.", "r": 588, "w": 400, "dy": 3},
    "Flexible Installation": {"ar": "تركيب مرن", "r": 226, "w": 700, "size": 15},
    "Wall-mounted or ﬂoor-standing.": {"ar": "تثبيت على الجدار أو على الأرض.", "r": 226, "w": 400, "dy": 3},
    "Smart Monitoring": {"ar": "مراقبة ذكية", "r": 477, "w": 700, "size": 15},
    "APP & LED display": {"ar": "تطبيق جوال وشاشة LED", "r": 477, "w": 400, "dy": 3},
}
labels = {
    "Model": {"ar": "الطراز", "r": LR, "w": 700, "size": 15},
    "Nominal Voltage (Vdc)": "الجهد الاسمي (Vdc)", "Nominal Capacity (Wh)": "السعة الاسمية (Wh)",
    "Usable Capacity (Wh)*": "السعة القابلة للاستخدام (Wh)*", "Depth of Discharge (%)*": "عمق التفريغ (%)*",
    "Dimensions (mm)": "الأبعاد (mm)", "Weight (Kg)": "الوزن (kg)", "Discharge Voltage (Vdc)": "جهد التفريغ (Vdc)",
    "Charge Voltage (Vdc)": "جهد الشحن (Vdc)",
    "Maximum Continuous Charge/Discharge Current (A)": "أقصى تيار شحن/تفريغ مستمر (A)",
    "Peak Charge/Discharge Current (A)": "تيار الشحن/التفريغ الأقصى اللحظي (A)", "Communication": "الاتصال",
    "Configuration (maximum quantity in one battery group)*": "التهيئة: أقصى عدد في مجموعة البطاريات الواحدة*",
    "Configuration (maximum strings)**": "التهيئة: أقصى عدد من السلاسل**",
    "Storage Temperature (°C)": "درجة حرارة التخزين (°C)", "Cooling Type": "نوع التبريد",
    "Protective Class": "فئة الحماية", "IP Rating of Enclosure": "درجة حماية الغلاف",
    "Anti-corrosion": "مقاومة التآكل", "Humidity(%, RH, No Condensation)": "الرطوبة %RH، بدون تكاثف",
    "Altitude(m)": "الارتفاع (m)", "Certifications": "الشهادات",
    "Design Life (year) (25°C /77℉)": "العمر التصميمي بالسنوات عند 25°C", "Cycle Life (25°C /77℉) ù*": "عمر الدورات**** عند 25°C",
    "Interaction": "التفاعل", "Fire extinguishing": "إطفاء الحريق",
    "Working": "درجة حرارة التشغيل", "Temperature": "(°C) ***", "(°C ) ***": None,
    "charging:": {"ar": "الشحن:", "r": 477, "w": 400}, "discharging:": {"ar": "التفريغ:", "r": 477, "w": 400},
}
p1 = {k: (lab(v) if isinstance(v, str) else v) for k, v in labels.items()}
p1["Working"] = {"ar": "درجة حرارة\nالتشغيل °C***", "r": LR, "w": 600, "lh": 8.6, "dy": 4.5, "size": 7.2}
p1["Temperature"] = None
vals = {"51.2": None, "16076": None, "100": None, "435(W)*240(D)*900(H)": "435 (W) × 240 (D) × 900 (H)", "130kg": "130 kg",
        "40 ~ 56.8": "40~56.8", "56 ~ 56.8": "56~56.8", "200/200": None, "300A@15s": "300 A لمدة 15 s", "CAN，RS485": "CAN, RS485",
        "20": None, "6": None, "-20 ~ 60": "من −20°C إلى 60°C", "Natural": "طبيعي", "I": None, "IP65": None, "C5-M": None,
        "5 ~ 95": "من 5% إلى 95%", "≤4000": None, "IEC62619、 IEC63056、UN38.3、 EMC/CE": "IEC62619, IEC63056, UN38.3, EMC/CE",
        "15": None, "8000": None, "Display screen、Bluetooth and WIFI": "شاشة عرض، Bluetooth وWiFi", "Aerosol (Optional)": "إيروسول، اختياري"}
for k, v in vals.items():
    p1[k] = {"ar": v or k, "cx": CM, "w": 400}
p1["FB-L-16"] = {"ar": "FB-L-16", "cx": C1, "w": 600}
p1["FB-L-16-Pro"] = {"ar": "FB-L-16-Pro", "cx": C2, "w": 600}
p1["0~55"] = {"ar": "من 0°C إلى 55°C", "cx": C1, "w": 400}
p1["-20~60"] = {"ar": "من −20°C إلى 60°C", "cx": C1, "w": 400}
p1["-20 ~ 55"] = {"ar": "من −20°C إلى 55°C", "cx": C2, "w": 400}
fn = {"w": 400, "r": LR, "size": 6.8}
p1["*Battery supports*"] = dict(fn, ar="*تدعم البطارية عمق تفريغ 100%؛ السعة المقننة عند 25°C وتفريغ 0.2C. الحد الأدنى الافتراضي لـ SOC هو 5% وقابل للضبط.", dy=2)
p1["** For multi-group*"] = dict(fn, ar="**في الأنظمة متعددة المجموعات يلزم LV-HUB-V2 للتوصيل على التوازي ويعمل كوحدة رئيسية. أقصى 19 بطارية لكل مجموعة.", dy=1)
p1["*** BMS limits*"] = dict(fn, ar="***يحدّ BMS تيار الشحن/التفريغ في الحرارة القصوى. بين −20°C و0°C يعمل التسخين للسماح بالشحن فوق 0°C.", dy=1.5)
p1["**** Specs based*"] = dict(fn, ar="****المواصفات مبنية على 25°C وشحن/تفريغ 0.2C ونطاق SOC من 5% إلى 95%.", dy=1)

tmp = '/tmp/cat/c5.pdf'
engine.build(SRC, tmp, {0: p0, 1: p1})
d = pymupdf.open(tmp); d.subset_fonts(); d.save(DST + '.tmp', garbage=4, deflate=True); os.replace(DST + '.tmp', DST)
engine.render(DST, '/tmp/cat/c5n', 110); print(os.path.getsize(DST))
