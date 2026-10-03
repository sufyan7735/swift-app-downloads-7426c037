"""Mirror page-1 feature layouts of Arabic catalogs to RTL.

Inside each configured band, icon-like elements are mirrored about the band
centre and every Arabic text block is moved so its right edge lands where the
English text started (mirrored). Elements are moved as vector clips of the
original page, so fonts/glyphs are untouched. Backgrounds are refilled with
the colour sampled around each element (bands must sit on flat colour).

usage: python3 p1mirror.py <name> [...]   (names = keys of CFG)
"""
import sys, re, shutil
import pymupdf as fitz
import numpy as np

AR = re.compile(r"[\u0600-\u06FF\uFB50-\uFDFF\uFE70-\uFEFF]")
C = "/dev-server/public/catalogs"

# name -> (english source, [bands]) ; band = (x0,y0,x1,y1[, mode])
# mode "text": only text blocks move (icons stay); "all" (default)
DEYE_B = [(300, 545, 580, 760)]
CFG = {
    "deye-sun-7-6-12k-sg02lp1--8k": ("catalog-13", DEYE_B),
    "deye-sun-7-6-12k-sg02lp1--12k": ("catalog-13", DEYE_B),
    "deye-sun-3-6k-sg04lp1--6k-sm2": ("catalog-14", DEYE_B),
    "deye-sun-14-20k-sg05lp3--16k": ("catalog-11", DEYE_B),
    "deye-sun-14-20k-sg05lp3--20k": ("catalog-11", DEYE_B),
    "deye-sun-29-9-50k-sg01hp3--30k": ("catalog-12", DEYE_B),
    "deye-sun-29-9-50k-sg01hp3--50k": ("catalog-12", DEYE_B),
    "deye-sun-60-80k-sg02hp3--80k": ("catalog-10", DEYE_B),
}


def bg_color(arr, sc, r):
    x0, y0, x1, y1 = [int(v * sc) for v in r]
    h, w, _ = arr.shape
    pad = 3
    ring = []
    for (a, b, c, d) in [(x0 - pad, y0 - pad, x1 + pad, y0), (x0 - pad, y1, x1 + pad, y1 + pad),
                         (x0 - pad, y0, x0, y1), (x1, y0, x1 + pad, y1)]:
        a, b, c, d = max(a, 0), max(b, 0), min(c, w), min(d, h)
        if c > a and d > b:
            ring.append(arr[b:d, a:c].reshape(-1, 3))
    px = np.concatenate(ring)
    return tuple(np.median(px, axis=0) / 255.0)


def elements(page, band, arr, sc):
    X0, Y0, X1, Y1 = band[:4]
    B = fitz.Rect(X0, Y0, X1, Y1)
    texts = []
    for b in page.get_text("dict")["blocks"]:
        if b["type"] != 0:
            continue
        r = fitz.Rect(b["bbox"])
        if not B.contains(r):
            continue
        s = "".join(sp["text"] for l in b["lines"] for sp in l["spans"])
        if AR.search(s):
            texts.append(r)
    # icon pixels: non-bg pixels in band not covered by arabic text
    x0, y0, x1, y1 = [int(v * sc) for v in (X0, Y0, X1, Y1)]
    sub = arr[y0:y1, x0:x1].astype(int)
    bg = np.median(sub.reshape(-1, 3), axis=0)
    mask = (np.abs(sub - bg).sum(axis=2) > 40)
    for r in texts:
        a, b, c, d = int(r.x0 * sc) - x0 - 2, int(r.y0 * sc) - y0 - 2, int(r.x1 * sc) - x0 + 2, int(r.y1 * sc) - y0 + 2
        mask[max(b, 0):d, max(a, 0):c] = False
    from scipy import ndimage
    lab, n = ndimage.label(ndimage.binary_dilation(mask, iterations=4))
    icons = []
    for sl in ndimage.find_objects(lab):
        if sl is None:
            continue
        ys, xs = sl
        r = fitz.Rect((xs.start + x0) / sc, (ys.start + y0) / sc, (xs.stop + x0) / sc, (ys.stop + y0) / sc)
        if r.width < 3 or r.height < 3:
            continue
        icons.append(r)
    return texts, icons


def en_anchor(en_page, r, band):
    best = None
    for b in en_page.get_text("dict")["blocks"]:
        if b["type"] != 0:
            continue
        for l in b["lines"]:
            lr = fitz.Rect(l["bbox"])
            if not fitz.Rect(band[:4]).contains(lr):
                continue
            if lr.y1 < r.y0 - 2 or lr.y0 > r.y1 + 2:
                continue
            if lr.x1 < r.x0 - 30 or lr.x0 > r.x1 + 30:
                continue
            best = lr.x0 if best is None else min(best, lr.x0)
    return best


def run(name):
    en_name, bands = CFG[name]
    path = f"{C}/official-ar/{name}.pdf"
    src = fitz.open(path)
    doc = fitz.open(path)
    en = fitz.open(f"{C}/{en_name}.pdf")[0]
    page = doc[0]
    sc = 3
    pix = src[0].get_pixmap(matrix=fitz.Matrix(sc, sc), alpha=False)
    arr = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, 3)
    moves = []
    for band in bands:
        mode = band[4] if len(band) > 4 else "all"
        c2 = band[0] + band[2]
        texts, icons = elements(src[0], band, arr, sc)
        if mode == "all":
            for r in icons:
                moves.append((r, fitz.Rect(c2 - r.x1, r.y0, c2 - r.x0, r.y1)))
        for r in texts:
            a = en_anchor(en, r, band)
            right = c2 - (a if a is not None else r.x0)
            moves.append((r, fitz.Rect(right - r.width, r.y0, right, r.y1)))
    for old, _ in moves:
        o = old + (-0.8, -0.8, 0.8, 0.8)
        page.draw_rect(o, color=None, fill=bg_color(arr, sc, o), overlay=True)
    for old, new in moves:
        page.show_pdf_page(new, src, 0, clip=old, overlay=True)
    tmp = path + ".tmp"
    doc.save(tmp, garbage=3, deflate=True)
    doc.close(); src.close()
    shutil.move(tmp, path)
    print(name, "moved", len(moves))


if __name__ == "__main__":
    for n in sys.argv[1:]:
        run(n)
