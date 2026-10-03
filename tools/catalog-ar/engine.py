"""Rebuild Arabic catalog from English original: redact mapped English lines, insert shaped Arabic.
Bidi is done manually: each line is split into Arabic and LTR runs, laid out right-to-left."""
import pymupdf, sys, json, re
import uharfbuzz as hb

F = "/tmp/cat/f/IBMPlexSansArabic-"
FILES = {700: F + "Bold.ttf", 600: F + "SemiBold.ttf", 400: F + "Regular.ttf"}
HBF = {}
LTR_DIRECT = False
for w, p in FILES.items():
    blob = hb.Blob.from_file_path(p); face = hb.Face(blob); font = hb.Font(face)
    HBF[w] = (font, face.upem)
ARCH = pymupdf.Archive("/tmp/cat/f")
CSS = """
@font-face{font-family:AR;font-weight:400;src:url(IBMPlexSansArabic-Regular.ttf)}
@font-face{font-family:AR;font-weight:600;src:url(IBMPlexSansArabic-SemiBold.ttf)}
@font-face{font-family:AR;font-weight:700;src:url(IBMPlexSansArabic-Bold.ttf)}
*{font-family:AR;margin:0;padding:0;line-height:1.2}
"""
TOP_K = 0.72  # box top = vertical-center - TOP_K*size  (calibrated)


def width(text, w, size):
    font, upem = HBF[w]
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(font, buf, {})
    return sum(p.x_advance for p in buf.glyph_positions) * size / upem


AR = re.compile(r"[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]")


def runs(line):
    """split into runs of (text, is_ltr) in logical order; whitespace becomes separators"""
    toks = re.findall(r"\S+|\s+", line)
    out = []
    for t in toks:
        if t.isspace():
            out.append((" ", None)); continue
        if AR.search(t):
            # a token mixing Arabic + latin (e.g. "وLID" or "(LCOE)،") -> split
            parts = re.findall(r"[\u0600-\u06FF،؛]+|[^\u0600-\u06FF،؛]+", t)
            for p in parts:
                out.append((p, "n" if not re.search(r"[A-Za-z0-9]", p) and not AR.search(p) else (not AR.search(p) and p not in "،؛")))
        elif not re.search(r"[A-Za-z0-9]", t):
            out.append((t, "n"))
        else:
            out.append((t, True))
    # resolve neutral punctuation tokens: LTR only if both strong neighbours are LTR
    res = []
    for i, (t, d) in enumerate(out):
        if d == "n":
            prev = next((x[1] for x in reversed(out[:i]) if x[1] in (True, False)), None)
            nxt = next((x[1] for x in out[i + 1:] if x[1] in (True, False)), None)
            d = True if (prev is True and nxt is True) else False
        res.append((t, d))
    out = res
    # merge consecutive same-direction tokens (spaces join LTR only if both sides LTR)
    merged = []
    for i, (t, d) in enumerate(out):
        if d is None:
            prev = merged[-1][1] if merged else None
            nxt = next((x[1] for x in out[i + 1:] if x[1] is not None), None)
            if prev is True and nxt is True:
                merged[-1] = (merged[-1][0] + " ", True)
            elif prev is False and nxt is False:
                merged[-1] = (merged[-1][0] + " ", False)
            else:
                merged.append((" ", None))
            continue
        if merged and merged[-1][1] == d:
            merged[-1] = (merged[-1][0] + t, d)
        else:
            merged.append((t, d))
    return merged


def put(page, x_right, cy, text, d, w, size, col):
    tw = width(text, w, size)
    top = cy - TOP_K * size
    box = pymupdf.Rect(x_right - tw - 1.0, top, x_right + 8, top + size * 2.2)
    dirn = "ltr" if d else "rtl"
    al = "left" if d else "right"
    if d:
        box = pymupdf.Rect(x_right - tw - 1.0, top, x_right + 8, top + size * 2.2)
    html = '<div dir="%s" style="white-space:nowrap;text-align:%s;font-size:%.2fpt;font-weight:%d;color:%s">%s</div>' % (
        dirn, al, size, w, col, text.replace("&", "&amp;").replace("<", "&lt;"))
    if d and LTR_DIRECT:
        c = tuple(int(col[i:i + 2], 16) / 255 for i in (1, 3, 5))
        page.insert_text((x_right - tw, cy + size * 0.36), text, fontsize=size, fontname="plx%d" % w, fontfile=FILES[w], color=c)
        return tw
    rc = page.insert_htmlbox(box, html, css=CSS, archive=ARCH)
    if rc[0] < 0:
        print("NOFIT run", text, file=sys.stderr)
    return tw


def line_width(line, w, size):
    tot = 0
    for t, d in runs(line):
        tot += size * 0.27 if d is None else width(t.rstrip(), w, size)
    return tot


def draw_line(page, x_right, cy, line, w, size, col):
    x = x_right
    for t, d in runs(line):
        if d is None:
            x -= size * 0.27; continue
        t2 = t.rstrip()
        x -= put(page, x, cy, t2, d, w, size, col)


def norm(s):
    return re.sub(r"\s+", " ", s.replace("ﬁ", "fi").replace("ﬀ", "ff").replace("‘", "'")).strip()


def lines(page):
    out = []
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            sp = l["spans"]
            t = norm("".join(s["text"] for s in sp))
            if t:
                out.append(dict(t=t, bbox=pymupdf.Rect(l["bbox"]), size=sp[0]["size"], color=sp[0]["color"]))
    return out


def place(page, r, s, size0, col0):
    w = s.get("w", 400)
    size = s.get("size", size0)
    col = "#%06x" % s.get("color", col0)
    ls = s["ar"].split("\n")
    lw = max(line_width(x, w, size) for x in ls)
    if "maxw" in s and lw > s["maxw"]:
        size *= s["maxw"] / lw; lw = s["maxw"]
    if "cx" in s:
        xr = s["cx"] + lw / 2
    elif "r" in s:
        xr = s["r"]
    elif "l" in s:
        xr = s["l"] + lw
    else:
        a = s.get("anchor", "left")
        xr = r.x0 + max(lw, r.width) if a == "left" else ((r.x0 + r.x1) / 2 + lw / 2 if a == "center" else r.x1)
    cy = (r.y0 + r.y1) / 2 + s.get("dy", 0)
    lh = s.get("lh", size * 1.35)
    for i, ln in enumerate(ls):
        lwi = line_width(ln, w, size)
        if s.get("center"):
            x = xr - (lw - lwi) / 2
        else:
            x = xr
        draw_line(page, x, cy + i * lh, ln, w, size, col)


def build(src, dst, pages, extra=None):
    """pages: {pno: {english_text: spec}}; extra: {pno: [(rect, spec_or_None)]} manual redactions/placements"""
    doc = pymupdf.open(src)
    extra = extra or {}
    for pno in sorted(set(pages) | set(extra)):
        mapping = pages.get(pno, {})
        page = doc[pno]
        todo, used = [], set()
        for ln in lines(page):
            key = ln["t"] if ln["t"] in mapping else next((k for k in mapping if k.endswith("*") and ln["t"].startswith(k[:-1])), None)
            if key is None:
                continue
            spec = mapping[key]
            used.add(key)
            if spec is None:
                spec = {"ar": ""}
            if isinstance(spec, str):
                spec = {"ar": spec}
            r = ln["bbox"]
            page.add_redact_annot(pymupdf.Rect(r.x0, r.y0 + 1.2, r.x1, r.y1 - 1.2), fill=False)
            if spec.get("ar"):
                todo.append((r, spec, ln["size"], ln["color"]))
        for k in mapping:
            if k not in used:
                print("UNMATCHED", pno, k, file=sys.stderr)
        for rect, spec in extra.get(pno, []):
            rect = pymupdf.Rect(rect)
            if spec and spec.get("white"):
                todo.append((rect, dict(spec, _white=True), spec.get("size", 7), spec.get("color", 0x585858)))
                continue
            page.add_redact_annot(rect, fill=False)
            if spec:
                todo.append((rect, spec, spec.get("size", 7), spec.get("color", 0x585858)))
        page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,
                              text=pymupdf.PDF_REDACT_TEXT_REMOVE)
        for r, s, sz, c in todo:
            if s.get("_white"):
                page.draw_rect(r, color=None, fill=s.get("bg", (1, 1, 1)))
                if not s.get("ar"):
                    continue
            place(page, r, s, sz, c)
    doc.save(dst, garbage=4, deflate=True)


def dump(path, pno):
    d = pymupdf.open(path)
    for ln in lines(d[pno]):
        r = ln["bbox"]
        print([round(r.x0), round(r.y0), round(r.x1), round(r.y1)], round(ln["size"], 1), hex(ln["color"]), ln["t"][:100])


def render(path, out, dpi=110):
    d = pymupdf.open(path)
    for i, p in enumerate(d):
        p.get_pixmap(dpi=dpi).save(f"{out}-{i}.png")
