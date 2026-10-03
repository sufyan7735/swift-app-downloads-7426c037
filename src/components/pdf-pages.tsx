import { useEffect, useRef, useState } from "react";

/** يرسم صفحات PDF داخل التطبيق (يعمل على متصفحات الجوال التي لا تعرض PDF داخل iframe). */
export default function PdfPages({ url }: { url: string }) {
  const box = useRef<HTMLDivElement>(null);
  const [state, setState] = useState<"loading" | "ok" | "error">("loading");

  useEffect(() => {
    let cancelled = false;
    const el = box.current;
    if (!el) return;
    el.innerHTML = "";
    setState("loading");
    (async () => {
      try {
        const pdfjs = await import("pdfjs-dist");
        const worker = (await import("pdfjs-dist/build/pdf.worker.min.mjs?url")).default;
        pdfjs.GlobalWorkerOptions.workerSrc = worker;
        const doc = await pdfjs.getDocument({ url, disableFontFace: true }).promise;
        const width = el.clientWidth || 360;
        const dpr = Math.min(window.devicePixelRatio || 1, 3);
        for (let i = 1; i <= doc.numPages; i++) {
          if (cancelled) return;
          const page = await doc.getPage(i);
          const base = page.getViewport({ scale: 1 });
          const vp = page.getViewport({ scale: (width / base.width) * dpr });
          const canvas = document.createElement("canvas");
          canvas.width = vp.width;
          canvas.height = vp.height;
          canvas.style.width = "100%";
          canvas.style.height = "auto";
          canvas.className = "mb-2 block rounded bg-card shadow";
          el.appendChild(canvas);
          await page.render({ canvasContext: canvas.getContext("2d")!, viewport: vp }).promise;
          if (i === 1 && !cancelled) setState("ok");
        }
      } catch {
        if (!cancelled) setState("error");
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [url]);

  return (
    <div className="h-full w-full flex-1 overflow-auto bg-muted p-2">
      {state === "loading" && <p className="py-6 text-center text-xs text-muted-foreground">جارٍ تحميل الكتالوج…</p>}
      {state === "error" && <p className="py-6 text-center text-xs text-muted-foreground">تعذّر عرض الملف، استخدم زر «تحميل».</p>}
      <div ref={box} />
    </div>
  );
}
