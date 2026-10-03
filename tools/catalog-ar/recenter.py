"""Re-center merged (single-cluster) value rows inside the value region of an already flipped table.
usage: recenter.py file.pdf pno y0 y1 vx0 vx1 [--dry]"""
import sys, pymupdf, numpy as np
from rtbl import _runs
Z = 4
f, pno, y0, y1, vx0, vx1 = sys.argv[1], int(sys.argv[2]), *map(float, sys.argv[3:7])
dry = '--dry' in sys.argv
s = pymupdf.open(f); d = pymupdf.open(f); sp = s[pno]; page = d[pno]
pm = sp.get_pixmap(clip=pymupdf.Rect(vx0, y0, vx1, y1), matrix=pymupdf.Matrix(Z, Z))
rgb = np.frombuffer(pm.samples, np.uint8).reshape(pm.h, pm.w, pm.n)[:, :, :3]
ink = rgb.mean(2) < 200
mid = (vx0 + vx1) / 2; n = 0
for a, b in _runs(ink.any(1), 1):
    cl = _runs(ink[a:b].any(0), int(12 * Z))
    if len(cl) != 1: continue
    x0 = vx0 + cl[0][0] / Z - 0.6; x1 = vx0 + cl[0][1] / Z + 0.6
    nx = mid - (x1 - x0) / 2
    if abs(nx - x0) < 2: continue
    ya, yb = y0 + a / Z - 0.3, y0 + b / Z + 0.3
    blk = rgb[a:b].reshape(-1, 3); blk = blk[blk.mean(1) > 225]
    vals, cnt = np.unique(blk, axis=0, return_counts=True)
    bg = tuple(float(c) / 255 for c in vals[cnt.argmax()])
    n += 1
    if dry: print(round(ya), round(x0), '->', round(nx)); continue
    r = pymupdf.Rect(x0, ya, x1, yb)
    page.draw_rect(r, color=None, fill=bg, overlay=True)
    page.show_pdf_page(pymupdf.Rect(nx, ya, nx + r.width, yb), s, pno, clip=r, overlay=True)
print('rows', n)
if not dry: d.save(f + '.tmp', garbage=4, deflate=True)
