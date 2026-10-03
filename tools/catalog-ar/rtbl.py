"""RTL flip of a spec table: label column moves to the right edge, value clusters mirrored per text line.
flip(src, dst, pno, y0, y1, lab=(lx0,lx1), val=(vx0,vx1), extra=[((x0,y0,x1,y1), dest_x0), ...])"""
import pymupdf, numpy as np

Z = 4


def _runs(v, gap):
    out = []; i = 0; n = len(v)
    while i < n:
        if v[i]:
            j = i
            while j < n and v[j]: j += 1
            if out and i - out[-1][1] < gap: out[-1] = (out[-1][0], j)
            else: out.append((i, j))
            i = j
        else: i += 1
    return out


def flip(src, dst, pno, y0, y1, lab, val, extra=(), thr=200, colgap=6.0, doc=None, ralign=False, center=False):
    s = pymupdf.open(src); d = doc or pymupdf.open(src)
    sp = s[pno]; page = d[pno]
    lx0, lx1 = lab; vx0, vx1 = val
    new_l = vx1 - (lx1 - lx0)
    new_v0 = lx0
    pm = sp.get_pixmap(clip=pymupdf.Rect(lx0, y0, vx1, y1), matrix=pymupdf.Matrix(Z, Z))
    rgb = np.frombuffer(pm.samples, np.uint8).reshape(pm.h, pm.w, pm.n)[:, :, :3]
    ink = rgb.mean(2) < thr
    fills, copies = [], []
    for a, b in _runs(ink.any(1), 1):
        ya, yb = y0 + a / Z - 0.3, y0 + b / Z + 0.3
        blk = rgb[a:b].reshape(-1, 3)
        blk = blk[blk.mean(1) > 225]
        if len(blk):
            vals, cnt = np.unique(blk, axis=0, return_counts=True)
            bg = tuple(float(c) / 255 for c in vals[cnt.argmax()])
        else:
            bg = (1, 1, 1)
        fills.append((pymupdf.Rect(lx0, ya, vx1, yb), bg))
        if ralign:
            li = ink[a:b, :int((lx1 - lx0) * Z)].any(0).nonzero()[0]
            if len(li):
                x0 = lx0 + li.min() / Z - 0.6; x1 = lx0 + li.max() / Z + 1.2
                copies.append((pymupdf.Rect(x0, ya, x1, yb), vx1 - 2 - (x1 - x0)))
        else:
            copies.append((pymupdf.Rect(lx0, ya, lx1, yb), new_l))
        vi0 = int((vx0 - lx0) * Z)
        row = ink[a:b, vi0:].any(0)
        whole = _runs(row, int(25 * Z))
        if center and len(whole) == 1:
            x0 = vx0 + whole[0][0] / Z - 0.6; x1 = vx0 + whole[0][1] / Z + 0.6
            copies.append((pymupdf.Rect(x0, ya, x1, yb), new_v0 + ((vx1 - vx0) - (x1 - x0)) / 2))
            continue
        for c0, c1 in _runs(row, int(colgap * Z)):
            x0 = vx0 + c0 / Z - 0.6; x1 = vx0 + c1 / Z + 0.6
            copies.append((pymupdf.Rect(x0, ya, x1, yb), new_v0 + (vx1 - x1)))
    for r, dx in extra:
        fills.insert(0, (pymupdf.Rect(*r), (1, 1, 1)))
        copies.append((pymupdf.Rect(*r), dx))
    for r, c in fills:
        page.draw_rect(r, color=None, fill=c, overlay=True)
    for r, dx in copies:
        page.show_pdf_page(pymupdf.Rect(dx, r.y0, dx + r.width, r.y1), s, pno, clip=r, overlay=True)
    if doc is None:
        d.save(dst, garbage=4, deflate=True)
    return d
