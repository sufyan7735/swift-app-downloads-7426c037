// الكتالوجات الرسمية الأصلية للمصنّع (بدون أي هوية لأكتس) — بدون تظليل.
// النسخة العربية مترجمة هندسياً بنفس تصميم ملف المصنّع مع إبقاء الرموز الفنية بالإنجليزية.
import type { Product } from "./products-data";

// أسماء ملفات الكتالوجات العربية الموجودة فعلياً في /catalogs/official-ar/
const AR_FILES = [
  "catalog-1", "catalog-11", "catalog-13", "catalog-15", "catalog-16", "catalog-17", "catalog-2", "catalog-3",
  "catalog-4", "catalog-5", "catalog-6", "catalog-7",
  "deye-sun-14-20k-sg05lp3--16k", "deye-sun-14-20k-sg05lp3--20k",
  "deye-sun-29-9-50k-sg01hp3--30k", "deye-sun-29-9-50k-sg01hp3--50k",
  "deye-sun-3-6k-sg04lp1--6k-sm2", "deye-sun-60-80k-sg02hp3--80k",
  "deye-sun-7-6-12k-sg02lp1--12k", "deye-sun-7-6-12k-sg02lp1--8k",
  "hithium-heroee-legend-112c", "hithium-heroee-legend-112s", "hithium-heroee-neopower-4-g2", "pylontech-optimus-a300-hy", "pylontech-optimus-l260-hy", "pylontech-uf5000",
  "solis-s6-eh2p-5-8k--6k", "solis-s6-eh2p-5-8k--8k",
  "solis-s6-eh3p-12-20k-h--12k", "solis-s6-eh3p-12-20k-h--20k",
  "solis-s6-eh3p-29-9-50k-h--30k", "solis-s6-eh3p-29-9-50k-h--50k",
  "solis-s6-eh3p-75-125k--125k", "solis-s6-eh3p-75-125k--80k",
  "suntech-stp595s-c72-nsh", "suntech-stp720s-d66-nsh",
];
const AR_SET = new Set(AR_FILES);
const arUrl = (name: string) => `/catalogs/official-ar/${name}.pdf`;

export function officialCatalogUrl(product: Product, lang: "en" | "ar"): string | null {
  const src = product.files.find((f) => f.kind === "Datasheet" || f.kind === "Catalog")?.url;
  if (!src) return null;
  if (lang === "en") return src;

  // 1) معرّف المنتج/الموديل نفسه  2) معرّف السلسلة  3) أول موديل من نفس السلسلة  4) اسم الملف القديم
  const base: string = product.baseId ?? product.id.split("--")[0] ?? product.id;
  for (const name of [product.id, base]) if (AR_SET.has(name)) return arUrl(name);
  const sibling = AR_FILES.find((n) => n.startsWith(`${base}--`));
  if (sibling) return arUrl(sibling);
  const legacy = (src.split("/").pop() ?? "").replace(/\.pdf$/i, "");
  if (AR_SET.has(legacy)) return arUrl(legacy);
  return null;
}
