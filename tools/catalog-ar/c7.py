"""catalog-7: Pylontech PowerCube-M1C — rebuilt RTL from the English original."""
import sys; sys.path.insert(0, '/dev-server/tools/catalog-ar')
import engine, os, pymupdf

SRC = '/dev-server/public/catalogs/catalog-7.pdf'
DST = '/dev-server/public/catalogs/official-ar/catalog-7.pdf'
LR, CV, W = 532, 243, 0xffffff
L = {
    "Basic Parameters": {"ar": "المعايير الأساسية", "r": LR, "w": 700, "color": W},
    "Module": {"ar": "الوحدة", "r": LR, "w": 700, "size": 15},
    "Related Product": "المنتج المرتبط", "System Operation Voltage (Vdc)": "جهد تشغيل النظام (Vdc)",
    "Operation Current (Max.)(A)": "أقصى تيار تشغيل (A)", "Self-consumption Power-Relay Off (W)": "الاستهلاك الذاتي، المرحّل مفصول (W)",
    "Self-consumption Power-Relay On (W)": "الاستهلاك الذاتي، المرحّل موصول (W)", "Dimension(W*D*H, mm)": "الأبعاد W×D×H (mm)",
    "Dimension (W*D*H,mm)": "الأبعاد W×D×H (mm)", "Dimension (W*D*H, mm)": "الأبعاد W×D×H (mm)",
    "Communication": "الاتصال", "Protection Class": "درجة الحماية", "Weight(kg)": "الوزن (kg)", "Weight (kg)": "الوزن (kg)",
    "Operation Life": "العمر التشغيلي", "Operatior Life": "العمر التشغيلي", "Operation Temperature": "درجة حرارة التشغيل",
    "Storage Temperature": "درجة حرارة التخزين", "Capacity (kwh)": "السعة (kWh)", "Nominal Voltage (Vdc)": "الجهد الاسمي (Vdc)",
    "Nominal Capacity (AH)": "السعة الاسمية (Ah)", "Voltage Range (Vdc)": "نطاق الجهد (Vdc)", "Depth of Discharge": "عمق التفريغ",
    "Product Certificate": "شهادات المنتج", "Battery System Capacity (kwh)": "سعة نظام البطاريات (kWh)",
    "Battery System Voltage (Vdc)": "جهد نظام البطاريات (Vdc)", "Battery System Capacity (AH)": "سعة نظام البطاريات (Ah)",
    "Battery Module": "وحدة البطارية", "Battery Module Capacity (kWh)": "سعة وحدة البطارية (kWh)",
    "Battery Modules Qty. (Optional)": "عدد وحدات البطارية، اختياري",
    "Battery System Charge Upper-Voltage (Vdc)": "الحد الأعلى لجهد شحن النظام (Vdc)",
    "Max. /Continuous Operation Current (A)": "أقصى تيار تشغيل/المستمر (A)",
    "Battery System Discharge lower-Voltage (Vdc)": "الحد الأدنى لجهد تفريغ النظام (Vdc)",
    "Efficiency": "الكفاءة", "Humidity": "الرطوبة", "Altitude (m)": "الارتفاع (m)", "Cycle Life": "عمر الدورات",
}
V = {"0~1000": None, "148": None, "6": None, "15": None, "330*628*150.5": "330 × 628 × 150.5",
     "CAN /LANCAN/Ethernet/Modbus TCP/IP/Modbus RTU": "CAN / LAN CAN / Ethernet / Modbus TCP/IP / Modbus RTU",
     "IP20": None, "13": None, "15+": "أكثر من 15 سنة", "-20~65": "من −20°C إلى 65°C", "-40~80": "من −40°C إلى 80°C",
     "PowerCube-M1C": None, "4.74": None, "32": None, "27~36": None, "95%": None, "RS485/CAN": None, "47": None,
     "10+ years": "أكثر من 10 سنوات", "0~50°C": "من 0°C إلى 50°C", "-20~60°C": "من −20°C إلى 60°C",
     "UN38.3/UL9540A/IEC62619/EC63056/UL1973/UL9540A/VDE2510-50VCE/UN38.3": "UN38.3 / UL9540A / IEC62619 / IEC63056 / UL1973 / VDE2510-50 / CE",
     "4.74*n": "4.74 × n", "32*n": "32 × n", "H32148-C": None, "1~23": None, "36*n": "36 × n", "148/74": None, "27*n": "27 × n",
     "815*659*2130": "815 × 659 × 2130", "CAN/Ethernet/Modbus TCP/IP/Modbus RTU": "CAN / Ethernet / Modbus TCP/IP / Modbus RTU",
     "120kg+47*n": "120 kg + 47 kg × n", "10+Years": "أكثر من 10 سنوات", "10~40°C": "من 10°C إلى 40°C",
     "-20-60°C": "من −20°C إلى 60°C", "5%~95%": "من 5% إلى 95%", "<4000": None,
     "IEC62619/EC63056/UL1973/UL9540A/VDE2510-50VCE/UN38.3": "IEC62619 / IEC63056 / UL1973 / UL9540A / VDE2510-50 / CE / UN38.3",
     "7000": None}


def mk(extra):
    m = {k: ({"ar": v, "r": LR, "w": 600} if isinstance(v, str) else v) for k, v in L.items()}
    for k, v in V.items():
        m[k] = {"ar": v or k, "cx": CV, "w": 400}
    m.update(extra); return m


p0 = mk({"Powercube M1C": {"ar": "Powercube M1C", "r": 539, "w": 700, "size": 23},
         "High Voltage Lithium lon Phosphate": {"ar": "نظام تخزين بطاريات ليثيوم", "r": 539, "w": 600, "size": 13.5},
         "Battery storage system": {"ar": "حديد فوسفات عالي الجهد", "r": 539, "w": 600, "size": 13.5},
         "H32148-C": {"ar": "H32148-C", "cx": 369, "w": 600, "size": 10},
         "SC1000-200J-C": {"ar": "SC1000-200J-C", "cx": 368, "w": 600, "size": 10}})
p0["PowerCube-M1C"] = {"ar": "PowerCube-M1C", "cx": CV, "w": 400}
p1 = mk({"Powercube M1C": {"ar": "Powercube M1C", "r": 539, "w": 700, "size": 23},
         "PowerCube-M1C": {"ar": "PowerCube-M1C", "cx": 370, "w": 600, "size": 10}})
tmp = '/tmp/cat/c7.pdf'
engine.build(SRC, tmp, {0: p0, 1: p1})
d = pymupdf.open(tmp); d.subset_fonts(); d.save(DST + '.tmp', garbage=4, deflate=True); os.replace(DST + '.tmp', DST)
engine.render(DST, '/tmp/cat/c7n', 110); print(os.path.getsize(DST))
