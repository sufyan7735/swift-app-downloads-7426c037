import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/downloads")({
  head: () => ({
    meta: [
      { title: "تحميل تطبيق ACTES لويندوز" },
      {
        name: "description",
        content: "تحميل تطبيق ACTES Desktop الخفيف لنظام ويندوز — أقل من 2 ميغابايت.",
      },
      { property: "og:title", content: "تحميل تطبيق ACTES لويندوز" },
      {
        property: "og:description",
        content: "تطبيق سطح مكتب خفيف لويندوز 10 و11 بحجم أقل من 2 ميغابايت.",
      },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary" },
    ],
  }),
  component: DownloadsPage,
});

function DownloadsPage() {
  return (
    <main
      dir="rtl"
      className="min-h-screen bg-background text-foreground flex items-center justify-center p-6"
    >
      <div className="w-full max-w-xl bg-card border border-border rounded-3xl p-8 sm:p-10 shadow-lg">
        <div className="flex items-center gap-4 mb-6">
          <img src="/brand/app-icon.png" alt="ACTES" className="w-16 h-16 rounded-2xl" />
          <div>
            <h1 className="text-2xl font-bold">تطبيق ACTES لويندوز</h1>
            <p className="text-sm text-muted-foreground mt-1">نسخة سطح المكتب — 64 بت</p>
          </div>
        </div>

        <ul className="space-y-2 text-sm text-muted-foreground mb-8">
          <li>• حجم خفيف جداً: 1.6 ميغابايت فقط — لا يحتاج تثبيت.</li>
          <li>• يعمل على ويندوز 10 و11، ويتحدّث تلقائياً بآخر نسخة.</li>
          <li>• الفيديوهات والكتالوجات تُفتح عبر الإنترنت عند الحاجة.</li>
        </ul>

        <a
          href="/downloads/ACTES-windows-x64.zip"
          download
          className="block text-center w-full rounded-xl bg-energy text-primary-foreground font-bold py-4 text-lg hover:opacity-90 transition"
        >
          تحميل التطبيق
        </a>

        <p className="text-xs text-muted-foreground mt-6 text-center">
          فُكّ ضغط الملف ثم شغّل <span className="font-mono">ACTES.exe</span>
        </p>
      </div>
    </main>
  );
}
