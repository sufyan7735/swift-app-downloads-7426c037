/**
 * رسومات متجهة واقعية لمجسمات معدات المنظومة الشمسية (إنفرتر، بطاريات، لوحات،
 * مفتاح تحويل، شبكة، أحمال) تُستخدم في وضع «العرض الواقعي» من المخطط الكهربائي.
 * كل الرسوم بالألوان الدلالية نفسها (CSS vars) فتعمل على نمط الورق والنمط الأزرق.
 * التفاصيل مرسومة بمقاييس قريبة من الأجهزة الحقيقية: شاسيه معدني بزعانف تبريد،
 * شاشة LCD، لوحة مفاتيح، ملصق بيانات، مداخل كابلات مع حشوات، وظلال ناعمة.
 */

const C = {
  dc: "var(--sld-dc)",
  ac: "var(--sld-ac)",
  earth: "var(--sld-earth)",
  ink: "var(--sld-ink)",
  frame: "var(--sld-frame)",
  soft: "var(--sld-soft)",
  fill: "var(--sld-fill)",
  band: "var(--sld-band)",
};

const F = "'Segoe UI', 'Tahoma', sans-serif";

export type EquipKind =
  "inverter" | "battery-rack" | "battery-wall" | "board-dc" | "board-ac" | "ats" | "grid" | "loads";

type Box = { x: number; y: number; w: number; h: number; accent: string };

/** تعريفات التدرجات والظلال المشتركة لكل المجسمات الواقعية. */
export function EquipDefs() {
  return (
    <defs>
      <linearGradient id="eqMetal" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stopColor="var(--sld-band)" stopOpacity={1} />
        <stop offset="48%" stopColor="var(--sld-fill)" stopOpacity={0.95} />
        <stop offset="100%" stopColor="var(--sld-band)" stopOpacity={1} />
      </linearGradient>
      <linearGradient id="eqGlass" x1="0" y1="0" x2="0.6" y2="1">
        <stop offset="0%" stopColor="#8fd6ff" stopOpacity={0.55} />
        <stop offset="55%" stopColor="#0e2235" stopOpacity={0.85} />
        <stop offset="100%" stopColor="#06121d" stopOpacity={0.95} />
      </linearGradient>
      <linearGradient id="eqSheen" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%" stopColor="#ffffff" stopOpacity={0.22} />
        <stop offset="35%" stopColor="#ffffff" stopOpacity={0.04} />
        <stop offset="100%" stopColor="#000000" stopOpacity={0.12} />
      </linearGradient>
      <filter id="eqShadow" x="-20%" y="-20%" width="150%" height="150%">
        <feDropShadow dx={1.6} dy={2.6} stdDeviation={2.2} floodOpacity={0.3} />
      </filter>
    </defs>
  );
}

/** زعانف تبريد جانبية كما في شاسيه الإنفرترات المعدنية المصبوبة. */
function Fins({ x, y, h, n, w = 10 }: { x: number; y: number; h: number; n: number; w?: number }) {
  const gap = h / n;
  return (
    <g>
      <rect
        x={x}
        y={y}
        width={w}
        height={h}
        rx={2}
        fill="url(#eqMetal)"
        stroke={C.frame}
        strokeWidth={0.8}
      />
      {Array.from({ length: n }).map((_, i) => (
        <line
          key={i}
          x1={x + 1}
          y1={y + gap * (i + 0.5)}
          x2={x + w - 1}
          y2={y + gap * (i + 0.5)}
          stroke={C.soft}
          strokeWidth={1.2}
          opacity={0.8}
        />
      ))}
    </g>
  );
}

/** فتحات دخول الكابلات مع حشوات (cable glands) أسفل الجهاز. */
function Glands({ x, y, n, gap = 16 }: { x: number; y: number; n: number; gap?: number }) {
  return (
    <g>
      {Array.from({ length: n }).map((_, i) => (
        <g key={i}>
          <rect
            x={x + i * gap}
            y={y}
            width={9}
            height={6}
            rx={1.6}
            fill={C.band}
            stroke={C.frame}
            strokeWidth={0.9}
          />
          <rect
            x={x + i * gap + 2}
            y={y + 5.4}
            width={5}
            height={3}
            rx={1}
            fill={C.soft}
            opacity={0.75}
          />
          <line
            x1={x + i * gap + 4.5}
            y1={y + 8}
            x2={x + i * gap + 4.5}
            y2={y + 13}
            stroke={C.soft}
            strokeWidth={1.1}
          />
        </g>
      ))}
    </g>
  );
}

/** ملصق بيانات الجهاز (nameplate) بخطوط باركود رمزية. */
function Nameplate({ x, y, w, label }: { x: number; y: number; w: number; label: string }) {
  return (
    <g>
      <rect
        x={x}
        y={y}
        width={w}
        height={11}
        rx={1.4}
        fill={C.fill}
        stroke={C.frame}
        strokeWidth={0.7}
      />
      <text x={x + 3} y={y + 8} fontFamily={F} fontSize={5.6} fontWeight={700} fill={C.soft}>
        {label}
      </text>
      {Array.from({ length: 9 }).map((_, i) => (
        <line
          key={i}
          x1={x + w - 4 - i * 2.4}
          y1={y + 2.4}
          x2={x + w - 4 - i * 2.4}
          y2={y + 8.6}
          stroke={C.soft}
          strokeWidth={i % 3 === 0 ? 1.2 : 0.6}
          opacity={0.8}
        />
      ))}
    </g>
  );
}

/** شاشة LCD بإضاءة خلفية وأسطر قراءات. */
function Lcd({ x, y, w, h, accent }: Box) {
  return (
    <g>
      <rect
        x={x}
        y={y}
        width={w}
        height={h}
        rx={2.6}
        fill={C.band}
        stroke={C.frame}
        strokeWidth={1.1}
      />
      <rect
        x={x + 2}
        y={y + 2}
        width={w - 4}
        height={h - 4}
        rx={1.8}
        fill="url(#eqGlass)"
        stroke={accent}
        strokeWidth={0.9}
      />
      <text x={x + 5} y={y + 10} fontFamily={F} fontSize={6} fontWeight={700} fill={accent}>
        P 12.4 kW
      </text>
      <text x={x + 5} y={y + 18.5} fontFamily={F} fontSize={5.4} fill={C.soft}>
        V 398 / I 31 A
      </text>
      <line
        x1={x + 4}
        y1={y + h - 5}
        x2={x + w - 6}
        y2={y + h - 5}
        stroke={accent}
        strokeWidth={0.8}
        opacity={0.5}
      />
    </g>
  );
}

/** شاسيه الإنفرتر الهجين: زعانف، شاشة، مفاتيح، مؤشرات، عزل DC، مداخل كابلات. */
function Inverter({ x, y, w, h, accent }: Box) {
  const bx = x + 12;
  const bw = w - 24;
  const bh = h - 16;
  return (
    <g filter="url(#eqShadow)">
      {/* الشاسيه */}
      <rect
        x={bx}
        y={y + 3}
        width={bw}
        height={bh}
        rx={7}
        fill="url(#eqMetal)"
        stroke={C.frame}
        strokeWidth={1.6}
      />
      <rect x={bx} y={y + 3} width={bw} height={bh} rx={7} fill="url(#eqSheen)" />
      <Fins x={x + 1} y={y + 10} h={bh - 20} n={9} />
      <Fins x={x + w - 11} y={y + 10} h={bh - 20} n={9} />
      {/* الشاشة ولوحة المفاتيح */}
      <Lcd x={bx + 9} y={y + 11} w={bw * 0.46} h={bh * 0.33} accent={accent} />
      {[0, 1, 2, 3].map((i) => (
        <rect
          key={i}
          x={bx + 10 + i * 11}
          y={y + 11 + bh * 0.33 + 5}
          width={8}
          height={6}
          rx={1.4}
          fill={C.band}
          stroke={C.frame}
          strokeWidth={0.7}
        />
      ))}
      {/* مؤشرات الحالة */}
      {["RUN", "GRID", "ALARM"].map((t, i) => (
        <g key={t}>
          <circle
            cx={bx + bw - 13}
            cy={y + 15 + i * 11}
            r={3.1}
            fill={i === 0 ? C.earth : i === 1 ? accent : C.dc}
            stroke={C.frame}
            strokeWidth={0.7}
          />
          <circle cx={bx + bw - 14} cy={y + 14 + i * 11} r={1} fill="#ffffff" opacity={0.65} />
          <text
            x={bx + bw - 20}
            y={y + 17.4 + i * 11}
            textAnchor="end"
            fontFamily={F}
            fontSize={5.6}
            fill={C.soft}
          >
            {t}
          </text>
        </g>
      ))}
      {/* مفتاح عزل DC الدوار */}
      <circle cx={bx + 16} cy={y + bh - 20} r={8} fill={C.fill} stroke={C.dc} strokeWidth={1.6} />
      <circle cx={bx + 16} cy={y + bh - 20} r={4.6} fill={C.band} stroke={C.dc} strokeWidth={1} />
      <line
        x1={bx + 16}
        y1={y + bh - 20}
        x2={bx + 21.6}
        y2={y + bh - 25.6}
        stroke={C.dc}
        strokeWidth={2}
        strokeLinecap="round"
      />
      <text
        x={bx + 16}
        y={y + bh - 7}
        textAnchor="middle"
        fontFamily={F}
        fontSize={5}
        fontWeight={700}
        fill={C.dc}
      >
        DC SW
      </text>
      <Glands x={bx + 12} y={y + bh + 1} n={Math.max(3, Math.floor(bw / 28))} />
    </g>
  );
}

/** خزانة بطاريات برجية عالية الجهد: وحدات متراصة، BMS، قاطع، قاعدة. */
function BatteryRack({ x, y, w, h, accent }: Box) {
  const bx = x + 14;
  const bw = w - 28;
  const mods = 5;
  const top = y + 4;
  const bmsH = 17;
  const avail = h - 22 - bmsH;
  const mh = avail / mods;
  return (
    <g filter="url(#eqShadow)">
      <rect
        x={bx - 5}
        y={top - 3}
        width={bw + 10}
        height={h - 12}
        rx={4}
        fill="url(#eqMetal)"
        stroke={C.frame}
        strokeWidth={1.6}
      />
      <rect x={bx - 5} y={top - 3} width={bw + 10} height={h - 12} rx={4} fill="url(#eqSheen)" />
      {/* وحدة التحكم */}
      <rect
        x={bx}
        y={top}
        width={bw}
        height={bmsH}
        rx={2}
        fill={C.fill}
        stroke={accent}
        strokeWidth={1.3}
      />
      <text x={bx + 5} y={top + 11} fontFamily={F} fontSize={6.6} fontWeight={700} fill={accent}>
        BMS CONTROL
      </text>
      <circle cx={bx + bw - 9} cy={top + 8.5} r={2.6} fill={C.earth} />
      <circle cx={bx + bw - 17} cy={top + 8.5} r={2.6} fill={C.soft} opacity={0.7} />
      {Array.from({ length: mods }).map((_, i) => {
        const my = top + bmsH + 3 + i * mh;
        const ih = mh - 3;
        return (
          <g key={i}>
            <rect
              x={bx}
              y={my}
              width={bw}
              height={ih}
              rx={2}
              fill={C.fill}
              stroke={C.frame}
              strokeWidth={1}
            />
            <rect x={bx} y={my} width={bw} height={ih} rx={2} fill="url(#eqSheen)" opacity={0.7} />
            {/* مقبض السحب */}
            <rect
              x={bx + 5}
              y={my + ih / 2 - 2}
              width={16}
              height={4}
              rx={2}
              fill={C.band}
              stroke={C.soft}
              strokeWidth={0.7}
            />
            {/* شريط حالة الشحن */}
            {Array.from({ length: 4 }).map((_, k) => (
              <rect
                key={k}
                x={bx + 26 + k * 6}
                y={my + ih / 2 - 2.6}
                width={4}
                height={5.2}
                rx={1}
                fill={k < 3 ? C.earth : C.soft}
                opacity={k < 3 ? 0.9 : 0.35}
              />
            ))}
            <text
              x={bx + bw - 5}
              y={my + ih / 2 + 2.6}
              textAnchor="end"
              fontFamily={F}
              fontSize={5.8}
              fill={C.soft}
            >
              {`MODULE ${i + 1}`}
            </text>
          </g>
        );
      })}
      {/* القاعدة بعجلات */}
      <rect
        x={bx - 5}
        y={y + h - 11}
        width={bw + 10}
        height={5}
        rx={1.4}
        fill={C.soft}
        opacity={0.55}
      />
      <circle cx={bx + 4} cy={y + h - 4} r={3} fill={C.band} stroke={C.frame} strokeWidth={0.8} />
      <circle
        cx={bx + bw - 4}
        cy={y + h - 4}
        r={3}
        fill={C.band}
        stroke={C.frame}
        strokeWidth={0.8}
      />
    </g>
  );
}

/** بطارية جدارية: شاسيه أنيق مع شريط SOC وقاطع مدمج وملصق بيانات. */
function BatteryWall({ x, y, w, h, accent }: Box) {
  const bx = x + 10;
  const bw = w - 20;
  const bh = h - 16;
  return (
    <g filter="url(#eqShadow)">
      <rect
        x={bx}
        y={y + 4}
        width={bw}
        height={bh}
        rx={9}
        fill="url(#eqMetal)"
        stroke={C.frame}
        strokeWidth={1.6}
      />
      <rect x={bx} y={y + 4} width={bw} height={bh} rx={9} fill="url(#eqSheen)" />
      {/* شريط الشحن */}
      <rect
        x={bx + 9}
        y={y + 12}
        width={bw - 18}
        height={11}
        rx={5.5}
        fill={C.fill}
        stroke={C.frame}
        strokeWidth={1}
      />
      {Array.from({ length: 5 }).map((_, i) => (
        <rect
          key={i}
          x={bx + 12 + i * ((bw - 24) / 5)}
          y={y + 14.6}
          width={(bw - 30) / 5}
          height={5.8}
          rx={1.4}
          fill={i < 4 ? C.earth : C.soft}
          opacity={i < 4 ? 0.92 : 0.3}
        />
      ))}
      <text x={bx + 9} y={y + 33} fontFamily={F} fontSize={6} fontWeight={700} fill={C.soft}>
        SOC 82%
      </text>
      {/* قاطع البطارية */}
      <rect
        x={bx + bw - 34}
        y={y + 26}
        width={25}
        height={15}
        rx={2.4}
        fill={C.fill}
        stroke={accent}
        strokeWidth={1.2}
      />
      <line
        x1={bx + bw - 28}
        y1={y + 38}
        x2={bx + bw - 15}
        y2={y + 29}
        stroke={accent}
        strokeWidth={1.6}
        strokeLinecap="round"
      />
      <circle cx={bx + bw - 28} cy={y + 38} r={1.5} fill={accent} />
      <Nameplate x={bx + 9} y={y + bh - 16} w={Math.max(40, bw * 0.5)} label="LFP BATTERY" />
      <Glands x={bx + 14} y={y + bh + 2} n={2} />
    </g>
  );
}

/** لوحة توزيع IP65 بنافذة شفافة تُظهر سكة DIN والقواطع والمشبك الأرضي. */
function Board({ x, y, w, h, accent, dc }: Box & { dc: boolean }) {
  const bx = x + 8;
  const bw = w - 16;
  const bh = h - 14;
  const rails = Math.max(2, Math.min(3, Math.floor(bh / 28)));
  const perRail = Math.max(3, Math.floor(bw / 17));
  return (
    <g filter="url(#eqShadow)">
      <rect
        x={bx}
        y={y + 4}
        width={bw}
        height={bh}
        rx={5}
        fill="url(#eqMetal)"
        stroke={C.frame}
        strokeWidth={1.6}
      />
      {/* النافذة الشفافة */}
      <rect
        x={bx + 5}
        y={y + 10}
        width={bw - 10}
        height={bh - 20}
        rx={3}
        fill={C.fill}
        stroke={accent}
        strokeWidth={1.2}
      />
      <rect
        x={bx + 5}
        y={y + 10}
        width={bw - 10}
        height={bh - 20}
        rx={3}
        fill="url(#eqSheen)"
        opacity={0.6}
      />
      {Array.from({ length: rails }).map((_, r) => {
        const ry = y + 16 + r * ((bh - 26) / rails);
        return (
          <g key={r}>
            {/* سكة DIN */}
            <rect
              x={bx + 8}
              y={ry + 14}
              width={bw - 16}
              height={3}
              rx={1}
              fill={C.soft}
              opacity={0.65}
            />
            {Array.from({ length: perRail }).map((_, i) => (
              <g key={i}>
                <rect
                  x={bx + 9 + i * 14}
                  y={ry}
                  width={10}
                  height={15}
                  rx={1.4}
                  fill={C.band}
                  stroke={C.frame}
                  strokeWidth={0.8}
                />
                <rect
                  x={bx + 11 + i * 14}
                  y={ry + 2.4}
                  width={6}
                  height={4}
                  rx={1}
                  fill={dc ? C.dc : accent}
                  opacity={0.85}
                />
                <line
                  x1={bx + 14 + i * 14}
                  y1={ry + 8}
                  x2={bx + 14 + i * 14}
                  y2={ry + 12.6}
                  stroke={dc ? C.dc : accent}
                  strokeWidth={1.6}
                />
              </g>
            ))}
          </g>
        );
      })}
      {/* مشبك التأريض */}
      <rect
        x={bx + 8}
        y={y + bh - 14}
        width={bw - 16}
        height={5}
        rx={1.2}
        fill={C.earth}
        opacity={0.35}
      />
      <text
        x={bx + 10}
        y={y + bh - 10.2}
        fontFamily={F}
        fontSize={5}
        fontWeight={700}
        fill={C.earth}
      >
        PE / N BAR
      </text>
      <circle cx={bx + bw - 6} cy={y + 4 + bh / 2} r={2} fill={C.soft} />
      <Glands x={bx + 10} y={y + 4 + bh - 2} n={Math.max(2, Math.floor(bw / 30))} />
    </g>
  );
}

/** خزانة مفتاح التحويل التلقائي بين الشبكة والمولد. */
function Ats({ x, y, w, h, accent }: Box) {
  const bx = x + 10;
  const bw = w - 20;
  const bh = h - 16;
  return (
    <g filter="url(#eqShadow)">
      <rect
        x={bx}
        y={y + 4}
        width={bw}
        height={bh}
        rx={5}
        fill="url(#eqMetal)"
        stroke={C.frame}
        strokeWidth={1.6}
      />
      <rect x={bx} y={y + 4} width={bw} height={bh} rx={5} fill="url(#eqSheen)" />
      {/* مؤشرات المصدر */}
      <circle cx={bx + 17} cy={y + 18} r={3.6} fill={C.earth} />
      <text x={bx + 25} y={y + 20.6} fontFamily={F} fontSize={6} fontWeight={700} fill={C.soft}>
        GRID
      </text>
      <circle cx={bx + 17} cy={y + 31} r={3.6} fill={C.soft} opacity={0.6} />
      <text x={bx + 25} y={y + 33.6} fontFamily={F} fontSize={6} fill={C.soft}>
        GEN
      </text>
      {/* ذراع التحويل */}
      <rect
        x={bx + bw - 38}
        y={y + 13}
        width={30}
        height={24}
        rx={2.6}
        fill={C.fill}
        stroke={accent}
        strokeWidth={1.3}
      />
      <line
        x1={bx + bw - 31}
        y1={y + 33}
        x2={bx + bw - 15}
        y2={y + 17}
        stroke={accent}
        strokeWidth={2}
        strokeLinecap="round"
      />
      <circle cx={bx + bw - 31} cy={y + 33} r={1.8} fill={accent} />
      <circle cx={bx + bw - 15} cy={y + 17} r={1.8} fill={accent} />
      <Nameplate x={bx + 12} y={y + bh - 14} w={Math.max(40, bw * 0.5)} label="ATS 4P" />
      <Glands x={bx + 12} y={y + 4 + bh - 2} n={3} />
    </g>
  );
}

/** برج نقل الشبكة العامة مع عوازل وأسلاك. */
function Grid({ x, y, w, h, accent }: Box) {
  const cx = x + w / 2;
  const top = y + 4;
  const base = y + h - 10;
  const halfTop = 8;
  const halfBase = 19;
  return (
    <g>
      <g stroke={accent} strokeWidth={1.6} fill="none">
        <line x1={cx - halfTop} y1={top} x2={cx - halfBase} y2={base} />
        <line x1={cx + halfTop} y1={top} x2={cx + halfBase} y2={base} />
        <line x1={cx - 14} y1={top + 11} x2={cx + 14} y2={top + 11} />
        <line x1={cx - 17} y1={top + 23} x2={cx + 17} y2={top + 23} />
        <line x1={cx - 12} y1={top + 11} x2={cx + 12} y2={top + 23} />
        <line x1={cx + 12} y1={top + 11} x2={cx - 12} y2={top + 23} />
        <line x1={cx - 22} y1={top + 4} x2={cx + 22} y2={top + 4} />
        {/* أسلاك متهدّلة */}
        <path d={`M ${cx - 22} ${top + 5} q -16 9 -30 4`} strokeWidth={1.1} />
        <path d={`M ${cx + 22} ${top + 5} q 16 9 30 4`} strokeWidth={1.1} />
      </g>
      <circle cx={cx - 20} cy={top + 4} r={2.4} fill={accent} />
      <circle cx={cx + 20} cy={top + 4} r={2.4} fill={accent} />
      <rect
        x={cx - halfBase - 4}
        y={base}
        width={halfBase * 2 + 8}
        height={5}
        rx={1.4}
        fill={C.soft}
        opacity={0.5}
      />
    </g>
  );
}

/** مبنى الأحمال / نقطة الاستهلاك بنوافذ مضاءة. */
function Loads({ x, y, w, h, accent }: Box) {
  const bw = Math.min(74, w - 18);
  const bx = x + w / 2 - bw / 2;
  const top = y + 10;
  const bh = h - 22;
  return (
    <g filter="url(#eqShadow)">
      <rect
        x={bx}
        y={top}
        width={bw}
        height={bh}
        rx={2}
        fill="url(#eqMetal)"
        stroke={accent}
        strokeWidth={1.6}
      />
      <path
        d={`M ${bx - 8} ${top} L ${bx + bw / 2} ${top - 14} L ${bx + bw + 8} ${top} Z`}
        fill={C.band}
        stroke={accent}
        strokeWidth={1.5}
      />
      {[0, 1].map((r) =>
        [0, 1, 2].map((c) => (
          <rect
            key={`${r}-${c}`}
            x={bx + 8 + c * ((bw - 16) / 3)}
            y={top + 8 + r * (bh / 2.3)}
            width={(bw - 24) / 3}
            height={10}
            rx={1}
            fill={C.earth}
            opacity={0.45}
            stroke={C.soft}
            strokeWidth={0.7}
          />
        )),
      )}
      <rect
        x={bx + bw / 2 - 7}
        y={top + bh - 14}
        width={14}
        height={14}
        rx={1}
        fill={C.fill}
        stroke={C.soft}
        strokeWidth={0.8}
      />
    </g>
  );
}

/** لوح شمسي واقعي بخلايا نصف مقطوعة وقضبان تجميع وإطار ألومنيوم. */
export function PvRealSymbol({ x, y, w, h }: { x: number; y: number; w: number; h: number }) {
  const cols = 6;
  const rows = 4;
  const cw = (w - 4) / cols;
  const ch = (h - 4) / rows;
  return (
    <g>
      <rect
        x={x}
        y={y}
        width={w}
        height={h}
        rx={2}
        fill={C.band}
        stroke={C.frame}
        strokeWidth={1.4}
      />
      <rect
        x={x + 1.6}
        y={y + 1.6}
        width={w - 3.2}
        height={h - 3.2}
        fill="url(#eqGlass)"
        opacity={0.9}
      />
      {Array.from({ length: rows }).map((_, r) =>
        Array.from({ length: cols }).map((_, c) => (
          <g key={`${r}-${c}`}>
            <rect
              x={x + 2 + c * cw}
              y={y + 2 + r * ch}
              width={cw - 0.9}
              height={ch - 0.9}
              fill={C.fill}
              stroke={C.soft}
              strokeWidth={0.4}
              opacity={0.55}
            />
            <line
              x1={x + 2 + c * cw + cw / 2}
              y1={y + 2 + r * ch}
              x2={x + 2 + c * cw + cw / 2}
              y2={y + 1 + (r + 1) * ch}
              stroke={C.soft}
              strokeWidth={0.35}
            />
          </g>
        )),
      )}
      {/* قضيب التجميع الأوسط (half-cut) */}
      <line
        x1={x + 1}
        y1={y + h / 2}
        x2={x + w - 1}
        y2={y + h / 2}
        stroke={C.frame}
        strokeWidth={1}
      />
      <rect x={x} y={y} width={w} height={h} rx={2} fill="url(#eqSheen)" opacity={0.5} />
    </g>
  );
}

/** يرسم مجسم المعدة الواقعي داخل مساحة الصندوق. */
export function EquipArt({
  kind,
  x,
  y,
  w,
  h,
  accent,
}: {
  kind: EquipKind;
  x: number;
  y: number;
  w: number;
  h: number;
  accent: string;
}) {
  const box = { x, y, w, h, accent };
  switch (kind) {
    case "inverter":
      return <Inverter {...box} />;
    case "battery-rack":
      return <BatteryRack {...box} />;
    case "battery-wall":
      return <BatteryWall {...box} />;
    case "board-dc":
      return <Board {...box} dc />;
    case "board-ac":
      return <Board {...box} dc={false} />;
    case "ats":
      return <Ats {...box} />;
    case "grid":
      return <Grid {...box} />;
    case "loads":
      return <Loads {...box} />;
    default:
      return null;
  }
}
