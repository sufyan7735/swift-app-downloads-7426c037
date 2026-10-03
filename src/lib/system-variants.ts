/**
 * محرك البدائل الهندسية للمنظومة (Smart System Variants).
 *
 * القاعدة: البديل لا يخترع أي صنف جديد. يأخذ نفس أصناف عرض السعر الرسمي
 * ويعيد ضبط كميات الألواح والبطاريات والمستلزمات التابعة لها فقط، مع الحفاظ
 * على نفس الانفرتر ونفس الأسعار المعتمدة. لذلك يبقى عرض السعر ودراسة الجدوى
 * والمخطط مبنيين على مصدر واحد للحقيقة.
 */

import type { QuoteItem } from "./present";

export type VariantId = "eco" | "rec" | "max";

export type SystemVariant = {
  id: VariantId;
  title: string;
  note: string;
  /** أصناف البديل بعد ضبط الكميات */
  items: QuoteItem[];
  total: number;
  panelQty: number;
  panelWp: number;
  kwp: number;
  batteryQty: number;
  batteryKwh: number;
  /** فرق التكلفة عن الخيار الموصى به */
  delta: number;
};

const PANEL_RE = /(لوح|ألواح|الواح|الوح|solar\s*panel|pv\s*module|bifacial)/i;
const BATTERY_RE = /(بطار|battery|lifepo|ليثيوم)/i;
/** أصناف تتبع عدد الألواح: الهياكل والقواعد وكوابل الـ DC والموصلات */
const PANEL_LINKED_RE = /(هيكل|هياكل|قواعد|قاعدة|حوامل|حامل|structure|استركشر|mc4|موصل)/i;

const PRESETS: { id: VariantId; title: string; note: string; pv: number; bat: number }[] = [
  {
    id: "eco",
    title: "الخيار الاقتصادي",
    note: "أقل تكلفة تأسيسية مع تغطية نهارية كاملة",
    pv: 0.82,
    bat: 0.6,
  },
  {
    id: "rec",
    title: "الموصى به",
    note: "التوازن المعتمد بين التكلفة والاستقلالية",
    pv: 1,
    bat: 1,
  },
  {
    id: "max",
    title: "أقصى استقلالية",
    note: "أكبر تخزين وإنتاج لتغطية الانقطاعات الطويلة",
    pv: 1.3,
    bat: 1.8,
  },
];

function num(value: unknown): number {
  const n = Number(value);
  return Number.isFinite(n) ? n : 0;
}

/** يستخرج قدرة اللوح بالواط من اسم الصنف أو تفاصيله */
function panelWattFrom(item: QuoteItem): number {
  const text = `${item.name} ${(item.details || []).join(" ")}`;
  const match = text.match(/(\d{3,4})\s*(?:w|watt|وات|واط)/i);
  return match ? num(match[1]) : 0;
}

/** يستخرج سعة البطارية بالكيلوواط ساعة من اسم الصنف أو تفاصيله */
function batteryKwhFrom(item: QuoteItem): number {
  const text = `${item.name} ${(item.details || []).join(" ")}`;
  const kwh = text.match(/(\d+(?:[.,]\d+)?)\s*(?:kwh|ك\.?و\.?س|كيلو\s*وات\s*ساعة|كيلو)/i);
  if (kwh) return num(String(kwh[1]).replace(",", "."));
  const ah = text.match(/(\d+(?:\.\d+)?)\s*ah/i);
  const volt = text.match(/(\d+(?:\.\d+)?)\s*(?:v\b|فولت)/i);
  if (ah && volt) return Math.round((num(ah[1]) * num(volt[1])) / 100) / 10;
  return 0;
}

function roundTo(value: number, step: number): number {
  if (step <= 1) return Math.max(1, Math.round(value));
  return Math.max(step, Math.round(value / step) * step);
}

export type VariantSource = {
  items: QuoteItem[];
  /** عدد الألواح في السلسلة، لحفظ تناظر السلاسل عند تغيير العدد */
  perString?: number;
};

/** يبني البدائل الثلاثة من أصناف عرض السعر الرسمي. */
export function buildVariants(source: VariantSource): SystemVariant[] | null {
  const items = (source.items || []).filter((i) => i && i.name);
  if (items.length === 0) return null;

  const panelIndex = items.findIndex((i) => PANEL_RE.test(i.name));
  const batteryIndex = items.findIndex((i) => BATTERY_RE.test(i.name));
  if (panelIndex < 0 && batteryIndex < 0) return null;

  const panelItem = panelIndex >= 0 ? items[panelIndex] : null;
  const batteryItem = batteryIndex >= 0 ? items[batteryIndex] : null;
  const panelWp = panelItem ? panelWattFrom(panelItem) : 0;
  const unitKwh = batteryItem ? batteryKwhFrom(batteryItem) : 0;
  const perString = num(source.perString);

  const baseTotal = items.reduce((sum, i) => sum + num(i.total), 0);

  const variants = PRESETS.map((preset) => {
    const panelQty = panelItem
      ? roundTo(num(panelItem.qty) * preset.pv, perString > 1 ? perString : 1)
      : 0;
    const batteryQty = batteryItem ? Math.max(1, Math.round(num(batteryItem.qty) * preset.bat)) : 0;
    const panelRatio = panelItem && num(panelItem.qty) > 0 ? panelQty / num(panelItem.qty) : 1;

    const next = items.map((item, index) => {
      let qty = num(item.qty);
      if (index === panelIndex) qty = panelQty;
      else if (index === batteryIndex) qty = batteryQty;
      else if (PANEL_LINKED_RE.test(item.name)) qty = Math.max(1, Math.round(qty * panelRatio));
      else return item;
      const price = num(item.price) || (num(item.qty) ? num(item.total) / num(item.qty) : 0);
      return { ...item, qty, total: Math.round(price * qty * 100) / 100 };
    });

    const total = next.reduce((sum, i) => sum + num(i.total), 0);
    return {
      id: preset.id,
      title: preset.title,
      note: preset.note,
      items: next,
      total,
      panelQty,
      panelWp,
      kwp: Math.round(((panelQty * panelWp) / 1000) * 100) / 100,
      batteryQty,
      batteryKwh: Math.round(batteryQty * unitKwh * 100) / 100,
      delta: 0,
    } satisfies SystemVariant;
  });

  const recTotal = variants.find((v) => v.id === "rec")?.total ?? baseTotal;
  return variants.map((v) => ({ ...v, delta: Math.round(v.total - recTotal) }));
}

/** يعيد نسخة من معاملات الدراسة بعد اعتماد مواصفات البديل المختار. */
export function applyVariantToStudyParams(
  params: Record<string, unknown> | null,
  variant: SystemVariant | null,
): Record<string, unknown> | null {
  if (!params || !variant || variant.id === "rec") return params;
  const system = { ...((params["system"] as Record<string, unknown>) || {}) };
  if (variant.kwp > 0) {
    system["kwp"] = variant.kwp;
    system["panel_qty"] = variant.panelQty;
  }
  if (variant.batteryQty > 0) {
    system["battery_qty"] = variant.batteryQty;
    system["battery_kwh"] = variant.batteryKwh;
  }
  return { ...params, system, quote_items: variant.items };
}

/** يعيد نسخة من معاملات المخطط بعد اعتماد مواصفات البديل المختار. */
export function applyVariantToSldParams(
  params: Record<string, unknown> | null,
  variant: SystemVariant | null,
): Record<string, unknown> | null {
  if (!params || !variant || variant.id === "rec") return params;
  const next = { ...params };
  if (variant.panelQty > 0) {
    const perStr = num(next["perStr"]);
    next["nPan"] = variant.panelQty;
    if (perStr > 0) next["nStr"] = Math.max(1, Math.ceil(variant.panelQty / perStr));
    if (variant.kwp > 0) next["kWp"] = variant.kwp;
  }
  if (variant.batteryQty > 0) next["nBat"] = variant.batteryQty;
  next["quote_items"] = variant.items;
  return next;
}
