"""catalog-4: HeroEE MaxPower 16 — rebuilt RTL from the English original."""
import sys; sys.path.insert(0, '/dev-server/tools/catalog-ar')
import engine

SRC = '/dev-server/public/catalogs/catalog-4.pdf'
DST = '/dev-server/public/catalogs/official-ar/catalog-4.pdf'
LR, VR = 561, 338  # label column right edge, value column right edge (mirrored)


def lab(t): return {"ar": t, "r": LR, "w": 600}
def val(t): return {"ar": t, "r": VR}


FR = 285  # features right edge
p0 = {
    "Product Features": {"ar": "مزايا المنتج", "r": FR, "w": 700},
    "·Flexible Expansion": {"ar": "· توسعة مرنة", "r": FR, "w": 700},
    "·Easy Maintenance": {"ar": "· صيانة سهلة", "r": FR, "w": 700},
    "·High Performance": {"ar": "· أداء عالٍ", "r": FR, "w": 700},
    "·All-Round Safety": {"ar": "· أمان شامل", "r": FR, "w": 700},
    "·HeroEE Cells Powered by HiTHIUM": {"ar": "· خلايا HeroEE مدعومة من HiTHIUM", "r": FR, "w": 700},
    "Ranked Top 3 in Global Energy Storage Battery": {"ar": "ضمن أفضل 3 مصنّعين عالمياً في شحنات", "r": FR, "w": 700},
    "Shipments in 2024": {"ar": "بطاريات تخزين الطاقة لعام 2024", "r": FR, "w": 700},
    "Solar": {"ar": "ألواح شمسية", "anchor": "center"},
    "Gird": {"ar": "الشبكة", "anchor": "center"},
    "PV input": {"ar": "دخل PV", "anchor": "center"},
    "Inverter": {"ar": "العاكس", "anchor": "center"},
    "AC Input": {"ar": "دخل AC", "anchor": "center"},
    "AC Output": {"ar": "خرج AC", "anchor": "center"},
    "Back-up load": {"ar": "الأحمال الاحتياطية", "anchor": "center"},
    "Lithium Battery": {"ar": "بطارية ليثيوم", "anchor": "center"},
}
L = {
    "Model": {"ar": "الطراز", "r": LR, "w": 600, "color": 0xffffff},
    "Battery Type": "نوع البطارية", "Battery Capacity": "سعة البطارية", "Cell Capacity": "سعة الخلية",
    "Battery Cell Lifespan": "عمر خلايا البطارية", "Rated Voltage": "الجهد المقنن",
    "Charge Voltage Range": "نطاق جهد الشحن", "Discharge Voltage Range": "نطاق جهد التفريغ",
    "Recommend Charge/Discharge Current": "تيار الشحن/التفريغ الموصى به",
    "Maximum Charge/Discharge Current": "أقصى تيار شحن/تفريغ", "DOD": "عمق التفريغ (DOD)",
    "Charge Mode": "نمط الشحن", "Built-in Communication Ports": "منافذ الاتصال المدمجة",
    "Built-in Screen": "الشاشة المدمجة", "Scalable": "قابلية التوسعة",
    "Ingress Protection Level": "درجة الحماية", "Protection": "الحمايات",
    "Operating Temperature": "درجة حرارة التشغيل", "Storage Temperature": "درجة حرارة التخزين",
    "Humidity": "الرطوبة", "Net Weight/Dimensions": "الوزن الصافي / الأبعاد", "Certification": "الشهادات",
}
p1 = {k: (v if isinstance(v, dict) else lab(v)) for k, v in L.items()}
p1.update({
    "PRODUCT DETAILS": {"ar": "تفاصيل المنتج", "r": 570, "w": 700},
    "HeroEE MaxPower 16": {"ar": "HeroEE MaxPower 16", "l": 30, "color": 0xffffff},
    "LiFePO4": val("LiFePO4"), "16076.8Wh": val("16076.8Wh"), "314Ah": val("314Ah"),
    "51.2[VDC]": val("51.2 VDC"),
    "11000 cycles@(25℃，100%DOD，0.5P,@70%SOH)": val("11000 دورة عند 25 °C، 100% DOD، 0.5P، 70% SOH"),
    "43.2~58.4[VDC]": val("43.2~58.4 VDC"), "100A": val("100A"), "200A": val("200A"), "90%": val("90%"),
    "CC-CV": val("CC-CV"), "CAN/RS485/RS232": val("CAN/RS485/RS232"),
    "LCD Touchscreen": val("شاشة LCD تعمل باللمس"),
    "Up to 16 batteries in parallel,256KWh": val("حتى 16 بطارية على التوازي، 256 kWh"),
    "IP30": val("IP30"),
    "Overtemperature/Undertemperature/Overcharge/": dict(val("ارتفاع/انخفاض الحرارة، الشحن الزائد،\nالتيار الزائد، القصر، انخفاض الجهد"), size=9.5, lh=11, dy=2),
    "Overcurrent/Short Circuit/Undervoltage": None,
    "Charging：0℃~40℃ Discharging：-20℃~40℃": dict(val("الشحن: من 0 °C إلى 40 °C، التفريغ: من −20 °C إلى 40 °C"), size=10),
    "-20℃~60℃": val("من −20 °C إلى 60 °C"),
    "10%~90%": val("من 10% إلى 90%"),
    "110kg / L520*W240*H781.2mm": val("110kg / L520*W240*H781.2mm"),
    "CE，CB，UN38.3，IEC 62619": val("CE، CB، UN38.3، IEC 62619"),
    "Contact:": {"ar": "للتواصل:", "r": 395, "w": 600},
    "Tel:": {"ar": "الهاتف:", "r": 395, "w": 600},
    "https://www.hero-ee.com": {"ar": "https://www.hero-ee.com", "r": 395},
    "*The above is for reference only, the specification sheet shall prevail.":
        {"ar": "*المعلومات أعلاه للاسترشاد فقط، ويُعتمد بما ورد في ورقة المواصفات.", "r": 570},
    "Business Cooperation": {"ar": "التعاون التجاري", "anchor": "center"},
    "website": {"ar": "الموقع", "anchor": "center"},
})
engine.build(SRC, DST, {0: p0, 1: p1}, {0: [((28, 197, 205, 211), {"ar": "نظام تخزين طاقة منزلي", "l": 28, "w": 600, "size": 20, "color": 0xffffff})]})
import pymupdf
d = pymupdf.open(DST)
_s = pymupdf.open(SRC)
for clip in [(20, 85, 390, 190), (35, 238, 180, 290)]:  # restore title + badge removed by overlapping redactions
    d[0].show_pdf_page(pymupdf.Rect(clip), _s, 0, clip=pymupdf.Rect(clip))
d.subset_fonts(); d.save(DST + '.tmp', garbage=4, deflate=True)
import os; os.replace(DST + '.tmp', DST)
engine.render(DST, '/tmp/cat/c4n', 70)
print(os.path.getsize(DST))
