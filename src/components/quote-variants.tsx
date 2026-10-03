import { useMemo, useState } from "react";
import {
  BatteryCharging,
  Check,
  Columns3,
  Scale,
  Sun,
  TrendingDown,
  TrendingUp,
} from "lucide-react";
import { buildPvsystStudy } from "@/lib/pvsyst-engine";
import { buildEconomics, DEFAULT_TARIFF_USD } from "@/lib/pvsyst-economics";
import {
  applyVariantToStudyParams,
  type SystemVariant,
  type VariantId,
} from "@/lib/system-variants";
import type { View } from "@/lib/present";

const nf = (n: number, d = 0) =>
  n.toLocaleString("en-US", { minimumFractionDigits: d, maximumFractionDigits: d });

type Props = {
  variants: SystemVariant[];
  active: VariantId;
  onPick: (id: VariantId) => void;
  study: View["study"];
};

type Metrics = { annual: number | null; saving: number | null; payback: number | null };

const TONE: Record<VariantId, { chip: string; ring: string; icon: typeof TrendingDown }> = {
  eco: {
    chip: "bg-skyline text-skyline-foreground",
    ring: "border-skyline/60 bg-skyline/5",
    icon: TrendingDown,
  },
  rec: {
    chip: "bg-energy text-energy-foreground",
    ring: "border-energy bg-energy/10",
    icon: Check,
  },
  max: {
    chip: "bg-brand text-brand-foreground",
    ring: "border-brand/60 bg-brand/5",
    icon: TrendingUp,
  },
};

/** شريط تبديل البدائل الهندسية ولوحة المقارنة المباشرة داخل عرض السعر الرسمي. */
export default function QuoteVariants({ variants, active, onPick, study }: Props) {
  const [open, setOpen] = useState(false);

  const metrics = useMemo(() => {
    const out: Record<string, Metrics> = {};
    for (const variant of variants) {
      let annual: number | null = null;
      if (study?.params) {
        const params = applyVariantToStudyParams(study.params, variant);
        const result = buildPvsystStudy(params, {
          city: study.city,
          customer: study.customer,
          reference: study.number,
          monthlyConsumption: study.monthlyConsumption,
        });
        annual = result?.annualEnergy ?? null;
      }
      if (annual === null && variant.kwp > 0) annual = Math.round(variant.kwp * 1700);
      const eco =
        annual && variant.total > 0
          ? buildEconomics({
              annualEnergy: annual,
              kwp: variant.kwp || null,
              capex: variant.total,
              tariff: DEFAULT_TARIFF_USD,
              dieselPrice: 1.1,
            })
          : null;
      out[variant.id] = {
        annual,
        saving: eco ? Math.round(eco.annualSaving) : null,
        payback: eco?.paybackYears ?? null,
      };
    }
    return out;
  }, [variants, study]);

  return (
    <section className="mb-4 rounded-xl border border-border bg-soft p-3 sm:p-4">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h3 className="inline-flex items-center gap-2 text-sm font-black text-navy">
          <span className="grid size-7 place-items-center rounded-lg bg-brand/10 text-brand [&_svg]:size-4">
            <Scale />
          </span>
          بدائل المنظومة
        </h3>
        <button
          type="button"
          onClick={() => setOpen((v) => !v)}
          className="inline-flex items-center gap-1.5 rounded-full border border-border bg-card px-3 py-1.5 text-[11px] font-bold text-navy transition hover:border-brand hover:text-brand"
        >
          <Columns3 className="size-3.5" />
          {open ? "إخفاء المقارنة" : "مقارنة البدائل جنباً إلى جنب"}
        </button>
      </div>

      <div className="mt-3 grid gap-2 sm:grid-cols-3">
        {variants.map((variant) => {
          const tone = TONE[variant.id];
          const Icon = tone.icon;
          const on = variant.id === active;
          const m = metrics[variant.id];
          return (
            <button
              key={variant.id}
              type="button"
              onClick={() => onPick(variant.id)}
              className={`flex h-full flex-col gap-1.5 rounded-xl border-2 p-3 text-right transition hover:-translate-y-0.5 hover:shadow-md ${on ? tone.ring + " shadow-md" : "border-border bg-card"}`}
            >
              <span className="flex items-center gap-2">
                <span
                  className={`grid size-7 shrink-0 place-items-center rounded-lg [&_svg]:size-3.5 ${tone.chip}`}
                >
                  <Icon />
                </span>
                <strong className="text-[13px] font-black leading-5">{variant.title}</strong>
                {variant.id === "rec" && (
                  <span className="rounded-full bg-energy/15 px-2 py-0.5 text-[9px] font-black text-energy">
                    معتمد
                  </span>
                )}
              </span>
              <span className="text-[10px] font-semibold leading-4 text-muted-foreground">
                {variant.note}
              </span>
              <span className="mt-auto flex flex-wrap items-center gap-x-3 gap-y-1 pt-1 text-[10px] font-bold text-navy">
                <span className="inline-flex items-center gap-1">
                  <Sun className="size-3 text-amber-500" /> {nf(variant.kwp, 1)} kWp
                </span>
                {variant.batteryKwh > 0 && (
                  <span className="inline-flex items-center gap-1">
                    <BatteryCharging className="size-3 text-emerald-600" />{" "}
                    {nf(variant.batteryKwh, 1)} kWh
                  </span>
                )}
              </span>
              <span className="flex items-baseline justify-between pt-1">
                <span className="text-sm font-black text-brand">${nf(variant.total)}</span>
                {variant.delta !== 0 && (
                  <span
                    className={`text-[10px] font-black ${variant.delta > 0 ? "text-brand" : "text-energy"}`}
                  >
                    {variant.delta > 0 ? "+" : "−"}${nf(Math.abs(variant.delta))}
                  </span>
                )}
              </span>
              {m?.payback && (
                <span className="text-[10px] font-semibold text-muted-foreground">
                  استرداد ≈ {nf(m.payback, 1)} سنة
                </span>
              )}
            </button>
          );
        })}
      </div>

      {open && (
        <div className="mt-3 overflow-x-auto rounded-lg border border-border bg-card">
          <table className="w-full min-w-[560px] border-collapse text-right text-[11px]">
            <thead>
              <tr className="bg-muted/60">
                <th className="border-b border-border p-2 text-right font-black">المقارنة</th>
                {variants.map((v) => (
                  <th key={v.id} className="border-b border-border p-2 text-center font-black">
                    {v.title}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {[
                {
                  label: "عدد الألواح",
                  pick: (v: SystemVariant) => (v.panelQty ? `${nf(v.panelQty)} لوح` : "—"),
                },
                {
                  label: "قدرة الألواح",
                  pick: (v: SystemVariant) => (v.kwp ? `${nf(v.kwp, 1)} kWp` : "—"),
                },
                {
                  label: "سعة التخزين",
                  pick: (v: SystemVariant) =>
                    v.batteryKwh ? `${nf(v.batteryKwh, 1)} kWh` : "بدون بطاريات",
                },
                {
                  label: "الإنتاج السنوي",
                  pick: (v: SystemVariant) => {
                    const a = metrics[v.id]?.annual;
                    return a ? `${nf(a)} kWh` : "—";
                  },
                },
                { label: "تكلفة المنظومة", pick: (v: SystemVariant) => `$${nf(v.total)}` },
                {
                  label: "فارق الاستثمار",
                  pick: (v: SystemVariant) =>
                    v.delta === 0
                      ? "المرجع"
                      : `${v.delta > 0 ? "+" : "−"}$${nf(Math.abs(v.delta))}`,
                },
                {
                  label: "الوفر السنوي",
                  pick: (v: SystemVariant) => {
                    const s = metrics[v.id]?.saving;
                    return s ? `$${nf(s)}` : "—";
                  },
                },
                {
                  label: "فترة الاسترداد",
                  pick: (v: SystemVariant) => {
                    const p = metrics[v.id]?.payback;
                    return p ? `${nf(p, 1)} سنة` : "—";
                  },
                },
              ].map((row) => (
                <tr key={row.label} className="odd:bg-muted/20">
                  <td className="border-b border-border p-2 font-bold text-muted-foreground">
                    {row.label}
                  </td>
                  {variants.map((v) => (
                    <td
                      key={v.id}
                      className={`border-b border-border p-2 text-center font-black ${v.id === active ? "text-brand" : "text-navy"}`}
                    >
                      {row.pick(v)}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
