import { lazy, Suspense, useEffect, useMemo, useState, type ReactNode } from "react";
const PdfPages = lazy(() => import("@/components/pdf-pages"));
import { ArrowRight, Search, BatteryCharging, Check, ChevronDown, Container, Copy, Download, Eye, FileText, Gauge, Info, Layers, Link2, ListChecks, MessageCircle, Play, Share2, Sparkles, Sun, Users, Wrench, X, Zap } from "lucide-react";
import QRCode from "qrcode";
import { createPortal } from "react-dom";
import { CATEGORIES, findProduct, matchCompatibleProducts, productsByCategory, quickSpecs, type Product, type ProductCategory, type ProductFile } from "@/lib/products-data";
import { isVoiceOn, isVoicePlatform, prepareSpeech, silenceNextScreen, speakScreen, speakScreenAfterCurrent, stopSpeaking } from "@/lib/voice-guide";
import ProductVideoPlayer from "@/components/product-video";
import { afterVideoNarration, getProductVideo, videoIntroNarration } from "@/lib/product-video";
import { officialCatalogUrl } from "@/lib/official-catalogs";


// خدمة معلوماتية فقط — لا تحتوي أي زر بيع أو ربط بمسارات عروض الأسعار.
const CAT_TONE: Record<ProductCategory, string> = {
  panels: "bg-brand text-brand-foreground",
  inverters: "bg-skyline text-skyline-foreground",
  batteries: "bg-energy text-energy-foreground",
  storage: "bg-navy text-white",
};
const CAT_BIG_ICON: Record<ProductCategory, ReactNode> = {
  panels: <Sun className="size-10 lg:size-12" />,
  inverters: <Zap className="size-10 lg:size-12" />,
  batteries: <BatteryCharging className="size-10 lg:size-12" />,
  storage: <Container className="size-10 lg:size-12" />,
};

/**
 * نطق الشاشة — على سطح المكتب فقط ومع تفعيل المرشد الصوتي.
 * مع continueAfter يكمل الشرح مباشرة بعد الجملة الجارية (تعليق الفيديو) بلا قطع ولا صمت.
 */
function useScreenVoice(key: string, text: string, continueAfter = false) {
  useEffect(() => {
    if (!text) return;
    if (!isVoicePlatform() || !isVoiceOn()) return;
    if (continueAfter) speakScreenAfterCurrent(key, text);
    else speakScreen(key, text);
    return () => stopSpeaking();
  }, [key, text, continueAfter]);
}

export default function ProductsCatalog({ productId, onOpen, onBack, returnTo }: { productId: string | null; onOpen: (id: string | null) => void; onBack: () => void; returnTo?: { label: string; onReturn: () => void } | null }) {
  const product = productId ? findProduct(productId) : undefined;
  const [category, setCategory] = useState<ProductCategory | "all" | null>(product ? product.category : null);

  if (product) {
    return (
      <ProductDetail
        product={product}
        onOpen={onOpen}
        onBack={returnTo ? returnTo.onReturn : () => { setCategory((c) => (c === "all" ? "all" : product.category)); onOpen(null); }}
        backLabel={returnTo ? returnTo.label : undefined}
      />
    );
  }

  if (category === "all") return <AllProductsView onOpen={onOpen} onBack={() => setCategory(null)} />;
  if (category) {
    return <CategoryView category={category} onOpen={onOpen} onBack={() => setCategory(null)} />;
  }
  return <CategoriesScreen onPick={setCategory} onBack={onBack} />;
}


function BackButton({ onClick, label }: { onClick: () => void; label: string }) {
  // الرجوع لا يعيد نطق الشاشة السابقة؛ يبقى الصوت صامتاً حتى يضغط المستخدم زر إعادة السماع.
  return (
    <button type="button" onClick={() => { silenceNextScreen(); onClick(); }} className="inline-flex items-center gap-1.5 rounded-full border border-border bg-card px-3 py-1.5 text-xs font-bold text-navy shadow-sm transition hover:bg-muted lg:text-sm">
      <ArrowRight className="size-4" /> {label}
    </button>
  );
}

/** صور المعاينة المختارة لكل فئة على بطاقات الأقسام (صور المنتجات الحقيقية). */
const PREVIEW_IDS: Partial<Record<ProductCategory, string[]>> = {
  batteries: ["pylontech-powercube-m1c", "hithium-heroee-maxpower-16", "pylontech-rv12100ch"],
  inverters: ["deye-sun-3-6k-sg04lp1--3-6k-sm2", "solis-s6-eh2p-5-8k--5k", "lipower-2012emh"],
};

/** المستوى الأول: ثلاث بطاقات ضخمة للأقسام. */
function CategoriesScreen({ onPick, onBack }: { onPick: (c: ProductCategory | "all") => void; onBack: () => void }) {
  useScreenVoice(
    "catalog-home",
    "قسم منتجات أكتس. اختر الفئة التي تريد استعراضها: الألواح الشمسية، أو الإنفرترات، أو بطاريات الليثيوم، أو أنظمة التخزين.",
  );
  return (
    <div className="screen-enter w-full space-y-5 pb-4">
      <header className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-[10px] font-black tracking-[0.3em] text-brand" dir="ltr">ACTES PRODUCTS</p>
          <h1 className="mt-1 text-xl font-black text-navy lg:text-3xl">تعرّف على منتجاتنا</h1>
          <p className="mt-0.5 text-xs text-muted-foreground lg:text-sm">اختر الفئة لاستعراض الموديلات ومواصفاتها وملفاتها الرسمية.</p>
        </div>
        <BackButton onClick={onBack} label="الرئيسية" />
      </header>

      <div className="stagger-in grid grid-cols-2 gap-3 md:grid-cols-4">
        {CATEGORIES.map((cat) => {
          const items = productsByCategory(cat.id);
          const brands = Array.from(new Set(items.map((p) => p.brand)));
          const previewIds = PREVIEW_IDS[cat.id];
          const preview = previewIds
            ? previewIds.map((id) => items.find((p) => p.id === id)).filter((p): p is Product => Boolean(p))
            : items.slice(0, 3);
          return (
            <button
              key={cat.id}
              type="button"
              onClick={() => onPick(cat.id)}
              className="group flex flex-col overflow-hidden rounded-2xl border border-border bg-card text-right shadow-sm transition hover:-translate-y-0.5 hover:shadow-xl"
            >
              <span className={`flex items-center justify-between gap-2 px-3 py-3 ${CAT_TONE[cat.id]}`}>
                <span className="text-right">
                  <span className="block text-sm font-black leading-tight lg:text-base">{cat.title}</span>
                </span>
                <span className="shrink-0 opacity-90 transition group-hover:scale-110 [&_svg]:size-7">{CAT_BIG_ICON[cat.id]}</span>
              </span>
              <span className="flex flex-1 flex-col gap-2 p-2.5">
                <span className="grid grid-cols-3 gap-1 text-center">
                  {preview.map((p) => (
                    <span key={p.id} className="overflow-hidden rounded-md border border-border/70 bg-background p-0.5">
                      <img src={p.image} alt={p.name} loading="lazy" className="aspect-square w-full scale-105 object-contain" />
                    </span>
                  ))}
                </span>
                <span className="hidden flex-wrap gap-1.5">
                  {brands.map((b) => (
                    <span key={b} className="rounded-full bg-navy-soft px-2.5 py-0.5 text-[11px] font-bold text-navy" dir="ltr">{b}</span>
                  ))}
                </span>
                <span className="mt-auto flex items-center justify-between gap-1 border-t border-border/70 pt-2">
                  <span className="inline-flex items-center gap-1 text-[11px] font-black text-navy"><Layers className="size-3.5 text-skyline" /> {items.length} موديل</span>
                  <ArrowRight className="size-4 text-brand" />
                </span>
              </span>
            </button>
          );
        })}
        <button
          type="button"
          onClick={() => onPick("all")}
          className="group flex flex-col justify-between gap-4 overflow-hidden rounded-2xl border border-border bg-card p-5 text-right shadow-sm transition hover:-translate-y-0.5 hover:shadow-xl order-first col-span-2 md:col-span-4"
        >
          <span className="flex items-center justify-between">
            <span>
              <span className="block text-2xl font-black text-navy lg:text-3xl">كل المنتجات</span>
              <span className="mt-1 block text-[12px] font-bold text-muted-foreground">ابحث في جميع الموديلات وصفّها حسب الشركة المصنّعة</span>
            </span>
            <Search className="size-10 text-skyline lg:size-12" />
          </span>
          <span className="inline-flex w-fit items-center gap-1 rounded-full bg-brand px-3 py-1.5 text-xs font-bold text-brand-foreground">
            <ArrowRight className="size-3.5" /> استعراض الكل
          </span>
        </button>
      </div>
    </div>
  );
}

/** اسم الشركة المصنّعة الموحّد (يدمج صيغ HiTHIUM المختلفة). */
export function brandOf(p: Product) {
  return /hithium/i.test(p.brand) ? "HiTHIUM" : p.brand;
}

/** المستوى الثاني: أقسام الشركات المصنّعة، ثم موديلات الشركة المختارة. */
function CategoryView({ category, onOpen, onBack }: { category: ProductCategory; onOpen: (id: string) => void; onBack: () => void }) {
  const cat = CATEGORIES.find((c) => c.id === category)!;
  const items = useMemo(() => productsByCategory(category), [category]);
  const brands = useMemo(() => Array.from(new Set(items.map(brandOf))), [items]);
  const [brand, setBrand] = useState<string | null>(brands.length === 1 ? brands[0] ?? null : null);
  const shown = brand ? items.filter((p) => brandOf(p) === brand) : [];
  useScreenVoice(
    `catalog-cat-${category}-${brand ?? "brands"}`,
    brand ? `${cat.title} من ${brand}. يتوفر ${shown.length} موديل.` : `${cat.title}. اختر الشركة المصنّعة لعرض موديلاتها.`,
  );
  const goBack = brand && brands.length > 1 ? () => setBrand(null) : onBack;
  return (
    <div className="screen-enter w-full space-y-4 pb-4">
      <BackButton onClick={goBack} label={brand && brands.length > 1 ? cat.title : "الفئات"} />
      <header className={`flex items-center gap-3 rounded-2xl px-4 py-4 shadow-sm ${CAT_TONE[category]}`}>
        <span className="shrink-0 opacity-90">{CAT_BIG_ICON[category]}</span>
        <div>
          <h1 className="text-xl font-black lg:text-2xl">{cat.title}{brand ? <span dir="ltr"> — {brand}</span> : null}</h1>
          <p className="text-[12px] font-bold opacity-85">{brand ? `${shown.length} موديل` : `${brands.length} شركات مصنّعة — ${items.length} موديل`}</p>
        </div>
      </header>
      {brand ? (
        <div className="stagger-in grid grid-cols-2 gap-2.5 sm:grid-cols-3 lg:gap-3 xl:grid-cols-4">
          {shown.map((p) => <ProductCard key={p.id} product={p} onOpen={() => onOpen(p.id)} />)}
        </div>
      ) : (
        <div className="stagger-in grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {brands.map((b) => {
            const list = items.filter((p) => brandOf(p) === b);
            return (
              <button key={b} type="button" onClick={() => setBrand(b)} className="group flex flex-col overflow-hidden rounded-2xl border border-border bg-card text-right shadow-sm transition hover:-translate-y-0.5 hover:shadow-lg">
                <span className="grid grid-cols-3 gap-1.5 bg-background p-2">
                  {list.slice(0, 3).map((p) => (
                    <img key={p.id} src={p.image} alt={p.name} loading="lazy" className="aspect-square w-full object-contain" />
                  ))}
                </span>
                <span className="flex items-center justify-between border-t border-border/70 px-4 py-3">
                  <span className="text-lg font-black text-navy" dir="ltr">{b}</span>
                  <span className="inline-flex items-center gap-1 rounded-full bg-brand px-3 py-1 text-xs font-bold text-brand-foreground">
                    {list.length} موديل <ArrowRight className="size-3.5 rotate-180" />
                  </span>
                </span>
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
}

/** بطاقة «كل المنتجات»: بحث + أزرار الشركات المصنّعة. */
function AllProductsView({ onOpen, onBack }: { onOpen: (id: string) => void; onBack: () => void }) {
  const all = useMemo(() => CATEGORIES.flatMap((c) => productsByCategory(c.id)), []);
  const brands = useMemo(() => Array.from(new Set(all.map(brandOf))), [all]);
  const [brand, setBrand] = useState<string | null>(null);
  const [q, setQ] = useState("");
  useScreenVoice("catalog-all", "كل المنتجات. ابحث باسم المنتج أو الموديل، أو اختر الشركة المصنّعة.");
  const terms = q.trim().toLowerCase().split(/\s+/).filter(Boolean);
  const shown = all.filter((p) => {
    if (brand && brandOf(p) !== brand) return false;
    const hay = `${p.name} ${p.model} ${p.brand} ${p.power}`.toLowerCase();
    return terms.every((t) => hay.includes(t));
  });
  const chip = (active: boolean) =>
    `rounded-full border px-3 py-1 text-[11px] font-bold transition lg:text-xs ${active ? "border-navy bg-navy text-white" : "border-border bg-card text-navy hover:bg-muted"}`;
  return (
    <div className="screen-enter w-full space-y-4 pb-4">
      <BackButton onClick={onBack} label="الفئات" />
      <header className="rounded-2xl bg-navy px-4 py-4 text-white shadow-sm">
        <h1 className="text-xl font-black lg:text-2xl">كل المنتجات</h1>
        <p className="text-[12px] font-bold opacity-85">{shown.length} من {all.length} موديل</p>
      </header>
      <div className="relative">
        <Search className="pointer-events-none absolute right-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="ابحث بالاسم أو الموديل أو القدرة…"
          className="w-full rounded-full border border-border bg-card py-2.5 pl-4 pr-9 text-sm text-foreground shadow-sm outline-none focus:border-navy"
        />
      </div>
      <div className="flex flex-wrap gap-1.5" dir="ltr">
        <button type="button" onClick={() => setBrand(null)} className={chip(brand === null)}>All</button>
        {brands.map((b) => (
          <button key={b} type="button" onClick={() => setBrand(b)} className={chip(brand === b)}>{b}</button>
        ))}
      </div>
      {shown.length ? (
        <div className="grid grid-cols-2 gap-2.5 sm:grid-cols-3 lg:gap-3 xl:grid-cols-4">
          {shown.map((p) => <ProductCard key={p.id} product={p} onOpen={() => onOpen(p.id)} />)}
        </div>
      ) : (
        <p className="py-10 text-center text-sm text-muted-foreground">لا توجد نتائج مطابقة.</p>
      )}
    </div>
  );
}

function brandLabel(b: string) {
  if (/hithium|heroee/i.test(b)) return "HiTHIUM";
  return b;
}

// شعارات المصنّعين مستخرجة من الكتالوجات الرسمية في public/catalogs.
const MAKER_LOGOS: Record<string, string> = {
  Deye: "/brand/makers/deye.png",
  Solis: "/brand/makers/solis.png",
  "Li-Power": "/brand/makers/lipower.png",
  Pylontech: "/brand/makers/pylontech.png",
  HiTHIUM: "/brand/makers/hithium.png",
  Suntech: "/brand/makers/suntech.png",
};

function makerLogo(b: string) {
  const l = brandLabel(b);
  const k = Object.keys(MAKER_LOGOS).find((n) => n.toLowerCase().replace(/[^a-z]/g, "") === l.toLowerCase().replace(/[^a-z]/g, ""));
  return k ? MAKER_LOGOS[k] : undefined;
}

function BrandBadge({ brand, large = false }: { brand: string; large?: boolean }) {
  const logo = makerLogo(brand);
  return (
    <span dir="ltr" className={`pointer-events-none flex w-full items-center justify-between gap-2 border-b border-border/70 bg-card ${large ? "h-14 px-3" : "h-8 px-2"}`}>
      <span className={`flex items-center font-black tracking-wide text-navy ${large ? "text-base" : "text-[11px]"}`}>
        {logo ? <img src={logo} alt={brandLabel(brand)} className={large ? "h-7 w-auto max-w-36" : "h-4 w-auto max-w-20"} /> : brandLabel(brand)}
      </span>
      <img src="/brand/actes-logo-full.png" alt="ACTES" className={large ? "h-10 w-auto" : "h-5 w-auto"} />
    </span>
  );
}

function ProductCard({ product, onOpen }: { product: Product; onOpen: () => void }) {
  // نبدأ تحضير الشرح الصوتي قبل فتح المنتج، حتى ينطلق مع الفيديو بلا انتظار.
  const warm = () => {
    const v = getProductVideo(product.id);
    if (v) prepareSpeech(videoIntroNarration(product, v), true);
  };
  return (
    <article
      onPointerEnter={warm}
      onTouchStart={warm}
      className="group flex flex-col overflow-hidden rounded-xl border border-border bg-card text-right shadow-sm transition hover:shadow-md"
    >
      <BrandBadge brand={product.brand} />
      <button type="button" onClick={() => { warm(); onOpen(); }} aria-label={product.name} className="relative block aspect-[4/5] w-full overflow-hidden bg-background">
        <img src={product.image} alt={product.name} loading="lazy" decoding="async" width={800} height={1000} className="size-full scale-105 object-contain p-1 transition duration-500 group-hover:scale-110" />
      </button>

      <div className="flex flex-1 flex-col gap-0.5 border-t border-border/70 px-2.5 pb-2.5 pt-2">
        <span className="text-[9px] font-bold text-skyline lg:text-[10px]">{product.brand}</span>
        <h3 className="line-clamp-2 text-[10.5px] font-bold leading-tight text-navy lg:text-[12px]">{product.name}</h3>
        <p className="line-clamp-1 text-[9px] text-muted-foreground lg:text-[10px]" dir="ltr">{product.model}</p>
        <span className="mt-0.5 inline-flex w-fit items-center gap-1 rounded-full bg-navy-soft px-2 py-0.5 text-[11px] font-black text-navy lg:text-xs" dir="ltr">
          <Zap className="size-3" />{product.power}
        </span>
        <button type="button" onClick={() => { warm(); onOpen(); }} className="mt-auto inline-flex w-full items-center justify-center gap-1 rounded-full bg-brand px-2 py-1.5 text-[11px] font-bold text-brand-foreground shadow-sm transition hover:opacity-90 lg:text-xs">
          <ArrowRight className="size-3.5" /> عرض المنتج
        </button>
      </div>
    </article>
  );
}

function Section({ icon, title, children, defaultOpen = false }: { icon: ReactNode; title: string; children: ReactNode; defaultOpen?: boolean }) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div className="overflow-hidden rounded-xl border border-border bg-card shadow-sm">
      <button type="button" onClick={() => setOpen((v) => !v)} aria-expanded={open} className="flex w-full items-center gap-2.5 px-3.5 py-3 text-right transition hover:bg-muted/60">
        <span className="grid size-8 place-items-center rounded-full bg-navy-soft text-navy [&_svg]:size-4">{icon}</span>
        <span className="flex-1 text-sm font-black text-navy lg:text-[15px]">{title}</span>
        <ChevronDown className={`size-4 text-muted-foreground transition ${open ? "rotate-180" : ""}`} />
      </button>
      {open && <div className="border-t border-border/70 px-3.5 py-3 text-sm leading-7 text-foreground">{children}</div>}
    </div>
  );
}

function Bullets({ items }: { items: string[] }) {
  return (
    <ul className="space-y-1.5">
      {items.map((t) => (
        <li key={t} className="flex gap-2"><span className="mt-2.5 size-1.5 shrink-0 rounded-full bg-energy" /><span>{t}</span></li>
      ))}
    </ul>
  );
}

/** روابط الملفات مجمّعة حسب نوع الوثيقة الرسمية. */
const FILE_GROUPS: { kind: ProductFile["kind"]; title: string }[] = [
  { kind: "User Manual", title: "دليل الاستخدام (User Manual)" },
  { kind: "Installation Manual", title: "دليل التركيب (Installation Manual)" },
  { kind: "Certificate", title: "الشهادات (Certificates)" },
];

function productUrl(id: string) {
  if (typeof window === "undefined") return "";
  return `${window.location.origin}/?product=${encodeURIComponent(id)}`;
}

function specSummaryText(product: Product) {
  const lines = quickSpecs(product, 6).map(([k, v]) => `• ${k}: ${v}`);
  return [`${product.name} — ${product.brand}`, `الموديل: ${product.model}`, `القدرة: ${product.power}`, "", ...lines, "", productUrl(product.id)].join("\n");
}

/** اسم ملف نظيف للتنزيل من رابط الملف. */
function fileNameOf(file: ProductFile) {
  const base = (file.url.split("?")[0] ?? "").split("/").pop() || "document.pdf";
  return /\.pdf$/i.test(base) ? base : `${base}.pdf`;
}

/** تنزيل الملف عبر جلب محتواه أولاً — يعمل داخل تطبيق الويندوز وفي المتصفح. */
async function downloadFile(file: ProductFile) {
  try {
    const res = await fetch(file.url);
    if (!res.ok) throw new Error("fetch failed");
    const blob = await res.blob();
    const href = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = href;
    a.download = fileNameOf(file);
    a.rel = "noopener";
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(href), 10000);
  } catch {
    const a = document.createElement("a");
    a.href = file.url;
    a.download = fileNameOf(file);
    document.body.appendChild(a);
    a.click();
    a.remove();
  }
}

/** نافذة عرض ملف PDF داخل التطبيق. */
function PdfViewer({ file, onClose }: { file: ProductFile; onClose: () => void }) {
  if (typeof document === "undefined") return null;
  return createPortal(
    <div className="fixed inset-0 z-[100] flex flex-col bg-navy/80 p-2 backdrop-blur-sm sm:p-4" role="dialog" aria-modal="true">
      <div className="mx-auto flex h-full w-full max-w-4xl flex-col overflow-hidden rounded-2xl border border-border bg-card shadow-2xl">
        <div className="flex items-center gap-2 border-b border-border px-3 py-2">
          <FileText className="size-4 shrink-0 text-brand" />
          <span className="flex-1 truncate text-xs font-black text-navy lg:text-sm">{file.label}</span>
          <button type="button" onClick={() => downloadFile(file)} className="rounded-full bg-navy-soft px-3 py-1 text-[11px] font-bold text-navy transition hover:opacity-90">تحميل</button>
          <button type="button" onClick={onClose} aria-label="إغلاق" className="grid size-7 place-items-center rounded-full bg-muted text-navy transition hover:bg-border"><X className="size-4" /></button>
        </div>
        <Suspense fallback={<div className="flex-1 bg-muted" />}><PdfPages url={file.url} /></Suspense>
      </div>
    </div>,
    document.body,
  );
}

/** نافذة المشاركة: واتساب، مشاركة الجهاز، نسخ الملخص، ورمز QR. */
function ShareSheet({ product, onClose }: { product: Product; onClose: () => void }) {
  const [qr, setQr] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);
  const url = productUrl(product.id);
  const summary = specSummaryText(product);

  useEffect(() => {
    let alive = true;
    QRCode.toDataURL(url, { margin: 1, width: 420, color: { dark: "#0b2239", light: "#ffffff" } })
      .then((d) => { if (alive) setQr(d); })
      .catch(() => { if (alive) setQr(null); });
    return () => { alive = false; };
  }, [url]);

  const share = async () => {
    try {
      if (navigator.share) await navigator.share({ title: product.name, text: summary, url });
      else window.open(`https://wa.me/?text=${encodeURIComponent(summary)}`, "_blank", "noopener");
    } catch { /* المستخدم ألغى المشاركة */ }
  };
  const copy = async () => {
    try { await navigator.clipboard.writeText(summary); setCopied(true); setTimeout(() => setCopied(false), 1800); } catch { /* ignore */ }
  };

  return (
    <div className="fixed inset-0 z-[70] grid place-items-center bg-navy/80 p-3 backdrop-blur-sm" role="dialog" aria-modal="true">
      <div className="w-full max-w-sm overflow-hidden rounded-2xl border border-border bg-card shadow-2xl">
        <div className="flex items-center gap-2 border-b border-border px-3.5 py-2.5">
          <Share2 className="size-4 text-brand" />
          <span className="flex-1 text-sm font-black text-navy">مشاركة المنتج</span>
          <button type="button" onClick={onClose} aria-label="إغلاق" className="grid size-7 place-items-center rounded-full bg-muted text-navy transition hover:bg-border"><X className="size-4" /></button>
        </div>
        <div className="space-y-3 p-4">
          <div className="grid place-items-center rounded-xl border border-border bg-white p-3">
            {qr ? <img src={qr} alt="رمز QR لصفحة المنتج" className="size-40 object-contain" /> : <span className="grid size-40 place-items-center text-xs text-muted-foreground">جارٍ توليد الرمز…</span>}
          </div>
          <p className="text-center text-[11px] leading-5 text-muted-foreground">امسح الرمز بالجوال لفتح مواصفات {product.model} وملفاته الرسمية مباشرة.</p>
          <div className="grid gap-2">
            <button type="button" onClick={share} className="inline-flex items-center justify-center gap-1.5 rounded-full bg-brand px-3 py-2 text-xs font-bold text-brand-foreground transition hover:opacity-90"><Share2 className="size-4" /> مشاركة الملخص الفني</button>
            <a href={`https://wa.me/?text=${encodeURIComponent(summary)}`} target="_blank" rel="noopener noreferrer" className="inline-flex items-center justify-center gap-1.5 rounded-full bg-skyline px-3 py-2 text-xs font-bold text-skyline-foreground transition hover:opacity-90"><MessageCircle className="size-4" /> إرسال عبر واتساب</a>
            <button type="button" onClick={copy} className="inline-flex items-center justify-center gap-1.5 rounded-full bg-navy-soft px-3 py-2 text-xs font-bold text-navy transition hover:opacity-90">
              {copied ? <><Check className="size-4" /> تم النسخ</> : <><Copy className="size-4" /> نسخ ملخص المواصفات</>}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

function ProductDetail({ product, onOpen, onBack, backLabel }: { product: Product; onOpen: (id: string) => void; onBack: () => void; backLabel?: string | undefined }) {
  // فيديو تعريفي حقيقي داخل معرض ACTES يبدأ أولاً (إن توفر لهذا الموديل)، ثم تظهر تفاصيل المنتج.
  const videoKey = product.baseId ?? product.id;
  const video = useMemo(() => getProductVideo(videoKey), [videoKey]);
  const [reelDone, setReelDone] = useState(!video);
  useEffect(() => { setReelDone(!getProductVideo(videoKey)); }, [videoKey]);

  // بعد الفيديو: جملة أو جملتان عن الفائدة العملية ولمن يناسب المنتج،
  // بلا تكرار الاسم أو الموديل أو القدرة أو المواصفات التي نطقها الفيديو.
  const afterVideoText = useMemo(() => {
    if (video) return afterVideoNarration(product);
    return `${product.name}. ${afterVideoNarration(product).split(".")[0]}.`;
  }, [product, video]);

  useScreenVoice(`catalog-product-${product.id}`, reelDone ? afterVideoText : "", !!video);
  const [viewFile, setViewFile] = useState<ProductFile | null>(null);
  const [shareOpen, setShareOpen] = useState(false);
  const summaryRows = useMemo(() => quickSpecs(product, 6), [product]);
  const linked = useMemo(
    () => (product.compatible ? matchCompatibleProducts(product, [...product.compatible.items, product.compatible.source].join(" ")) : []),
    [product],
  );

  if (!reelDone && video) {
    return (
      <div className="screen-enter w-full space-y-4 pb-4">

        <div className="flex flex-wrap items-center justify-between gap-2">
          <BackButton onClick={onBack} label={backLabel ?? CATEGORIES.find((c) => c.id === product.category)?.title ?? "منتجاتنا"} />

          <span className="text-[11px] font-black text-skyline">{product.brand}</span>
        </div>
        <ProductVideoPlayer
          key={product.id}
          video={video}
          title={`${product.name} — ${product.model}`}
          narration={videoIntroNarration(product, video)}
          onFinish={() => setReelDone(true)}
        />
      </div>
    );
  }


  return (
    <div className="screen-enter w-full space-y-4 pb-4">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <BackButton onClick={onBack} label={backLabel ?? CATEGORIES.find((c) => c.id === product.category)?.title ?? "منتجاتنا"} />
        <div className="flex items-center gap-2">
          {video ? (
            <button type="button" onClick={() => setReelDone(false)} className="inline-flex items-center gap-1.5 rounded-full border border-border bg-card px-3 py-1.5 text-xs font-bold text-navy shadow-sm transition hover:bg-muted">
              <Play className="size-3.5" /> الفيديو التعريفي
            </button>
          ) : null}
          <button type="button" onClick={() => setShareOpen(true)} className="inline-flex items-center gap-1.5 rounded-full bg-navy px-3 py-1.5 text-xs font-bold text-skyline-foreground shadow-sm transition hover:opacity-90">
            <Share2 className="size-3.5" /> مشاركة / رمز QR
          </button>
        </div>
      </div>



      <section className="grid gap-4 rounded-2xl border border-border bg-card p-3 shadow-sm md:grid-cols-[minmax(0,3fr)_minmax(0,3fr)] lg:p-5">
        <div className="relative overflow-hidden rounded-xl border border-border/70 bg-background">
          <BrandBadge brand={product.brand} large />
          <div className="overflow-hidden">
          <img src={product.image} alt={product.name} width={1200} height={1200} className="aspect-square w-full object-contain p-1.5" />
          </div>
        </div>
        <div className="flex flex-col gap-3">
          <div>
            <span className="text-[11px] font-bold text-skyline">{product.brand}</span>
            <h1 className="mt-0.5 text-base font-bold leading-snug text-navy lg:text-xl">{product.name}</h1>
            <p className="mt-1 text-[11px] text-muted-foreground" dir="ltr">{product.model}</p>
          </div>
          <div className="w-fit rounded-xl bg-navy px-4 py-2 text-skyline-foreground shadow-sm">
            <span className="block text-[11px] font-bold opacity-80">القدرة</span>
            <span className="block text-2xl font-black lg:text-3xl" dir="ltr">{product.power}</span>
          </div>
          <dl className="grid grid-cols-2 gap-2 text-xs">
            <div className="rounded-lg bg-muted px-3 py-2"><dt className="text-muted-foreground">العلامة التجارية</dt><dd className="font-black text-navy">{product.brand}</dd></div>
            <div className="rounded-lg bg-muted px-3 py-2"><dt className="text-muted-foreground">الفئة</dt><dd className="font-black text-navy">{CATEGORIES.find((c) => c.id === product.category)?.title}</dd></div>
          </dl>
          <p className="text-sm leading-7 text-foreground">{product.description}</p>
        </div>
      </section>

      {summaryRows.length > 0 && (
        <section className="rounded-2xl border border-border bg-card p-4 shadow-sm">
          <h2 className="mb-2.5 flex items-center gap-2 text-base font-black text-navy"><Gauge className="size-5 text-brand" /> الملخص الفني السريع</h2>
          <div className="grid grid-cols-2 gap-2 lg:grid-cols-3">
            {summaryRows.map(([k, v]) => (
              <div key={k} className="rounded-xl border border-border/70 bg-muted/50 px-3 py-2">
                <span className="block text-[10px] font-bold text-muted-foreground">{k}</span>
                <span className="mt-0.5 block text-[12px] font-black leading-snug text-navy">{v}</span>
              </div>
            ))}
          </div>
        </section>
      )}

      <section className="rounded-2xl border border-border bg-card p-4 shadow-sm">
        <h2 className="mb-2 flex items-center gap-2 text-base font-black text-navy"><Info className="size-5 text-skyline" /> عن المنتج</h2>
        <p className="text-sm leading-7 text-foreground">{product.about}</p>
      </section>

      <div className="space-y-2.5">
        <Section icon={<Sparkles />} title="أهم المميزات"><Bullets items={product.features} /></Section>
        <Section icon={<ListChecks />} title="الاستخدامات"><Bullets items={product.uses} /></Section>
        <Section icon={<Users />} title="لمن يناسب هذا المنتج؟"><p>{product.suitableFor}</p></Section>
        <Section icon={<Wrench />} title="المواصفات الفنية"><SpecsView product={product} /></Section>
        {product.compatible && product.compatible.items.length > 0 && (
          <Section icon={<Link2 />} title="المنتجات المتوافقة">
            <div className="flex flex-wrap gap-1.5">
              {product.compatible.items.map((c) => <span key={c} className="rounded-full bg-navy-soft px-2.5 py-1 text-xs font-bold text-navy">{c}</span>)}
            </div>
            {linked.length > 0 && (
              <div className="mt-3">
                <p className="mb-1.5 text-xs font-black text-navy">متوفر في كتالوج ACTES — اضغط للانتقال:</p>
                <div className="grid gap-2 sm:grid-cols-2">
                  {linked.map((lp) => (
                    <button key={lp.id} type="button" onClick={() => onOpen(lp.id)} className="flex items-center gap-2 rounded-xl border border-border bg-card p-2 text-right transition hover:-translate-y-0.5 hover:shadow-md">
                      <img src={lp.image} alt="" loading="lazy" className="size-12 shrink-0 rounded-lg border border-border/70 object-contain p-0.5" />
                      <span className="min-w-0 flex-1">
                        <span className="block text-[10px] font-bold text-skyline">{lp.brand}</span>
                        <span className="block truncate text-[12px] font-black text-navy">{lp.name}</span>
                        <span className="block truncate text-[10px] text-muted-foreground" dir="ltr">{lp.model} — {lp.power}</span>
                      </span>
                      <ArrowRight className="size-4 shrink-0 text-brand" />
                    </button>
                  ))}
                </div>
              </div>
            )}
            <p className="mt-2 text-xs text-muted-foreground">المصدر: {product.compatible.source}</p>
          </Section>
        )}
        <Section icon={<FileText />} title="الكتالوجات والملفات" defaultOpen>
          {(() => {
            const en = officialCatalogUrl(product, "en");
            const ar = officialCatalogUrl(product, "ar");
            if (!en) return <p className="text-xs text-muted-foreground">لا يتوفر كتالوج رسمي لهذا المنتج حالياً.</p>;
            const row = (url: string, label: string, dir: "ltr" | "rtl", open: string, dl: string) => (
              <div dir={dir} className="flex flex-wrap items-center justify-between gap-2 rounded-lg border border-border px-3 py-2">
                <span className="flex items-center gap-2 text-sm font-bold text-navy"><FileText className="size-4 text-brand" /> {label} <span className="text-xs font-normal text-muted-foreground">(PDF)</span></span>
                <span className="flex gap-1.5">
                  <button type="button" onClick={() => setViewFile({ kind: "Datasheet", label, url })} className="inline-flex items-center gap-1 rounded-full bg-skyline px-3 py-1 text-xs font-bold text-skyline-foreground transition hover:opacity-90"><Eye className="size-3.5" /> {open}</button>
                  <button type="button" onClick={() => downloadFile({ kind: "Datasheet", label, url })} className="inline-flex items-center gap-1 rounded-full bg-navy-soft px-3 py-1 text-xs font-bold text-navy transition hover:opacity-90"><Download className="size-3.5" /> {dl}</button>
                </span>
              </div>
            );
            return (
              <div className="space-y-2">
                {row(en, "Official Datasheet (EN)", "ltr", "Open", "Download")}
                {ar && row(ar, "الكتالوج الرسمي (عربي)", "rtl", "فتح", "تحميل")}
              </div>
            );
          })()}
          {product.certificates && (
            <div className="mt-3 rounded-lg bg-muted px-3 py-2 text-xs leading-6">
              <span className="font-black text-navy">الشهادات والمعايير المذكورة في الكتالوج: </span>{product.certificates}
            </div>
          )}
          {FILE_GROUPS.filter((g) => g.kind !== "Datasheet" && g.kind !== "Catalog" && product.files.every((f) => f.kind !== g.kind)).length > 0 && (
            <p className="mt-2 text-xs text-muted-foreground">أدلة الاستخدام والتركيب والشهادات غير متوفرة حالياً ضمن الملفات الرسمية المرفقة، وسيتم إضافتها فور توفرها من الشركة المصنعة.</p>
          )}
        </Section>
      </div>

      {viewFile && <PdfViewer file={viewFile} onClose={() => setViewFile(null)} />}
      {shareOpen && <ShareSheet product={product} onClose={() => setShareOpen(false)} />}
    </div>
  );
}


function SpecsView({ product }: { product: Product }) {
  return (
    <div className="space-y-4">
      {product.modelTable && (
        <div>
          <h3 className="mb-1.5 text-sm font-black text-navy">مقارنة موديلات السلسلة</h3>
          <div className="overflow-x-auto rounded-lg border border-border">
            <table className="w-full min-w-max text-xs">
              <thead className="bg-navy text-skyline-foreground">
                <tr>
                  <th className="px-2.5 py-2 text-right font-bold">البند</th>
                  {product.modelTable.models.map((m) => <th key={m} className="px-2.5 py-2 text-center font-bold" dir="ltr">{m}</th>)}
                </tr>
              </thead>
              <tbody>
                {product.modelTable.rows.map((r, i) => (
                  <tr key={r.label} className={i % 2 ? "bg-muted/60" : ""}>
                    <td className="px-2.5 py-1.5 font-bold text-navy">{r.label}</td>
                    {r.values.map((v, j) => <td key={j} className="px-2.5 py-1.5 text-center" dir="ltr">{v}</td>)}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
      {product.specs.map((g) => (
        <div key={g.title}>
          <h3 className="mb-1.5 text-sm font-black text-navy">{g.title}</h3>
          <dl className="divide-y divide-border overflow-hidden rounded-lg border border-border">
            {g.rows.map(([k, v]) => (
              <div key={k} className="grid grid-cols-[minmax(0,2fr)_minmax(0,3fr)] gap-2 px-2.5 py-1.5 text-xs odd:bg-muted/50">
                <dt className="font-bold text-navy">{k}</dt>
                <dd className="text-foreground">{v}</dd>
              </div>
            ))}
          </dl>
        </div>
      ))}
    </div>
  );
}
