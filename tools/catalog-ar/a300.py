"""Optimus A300-HY page 2: RTL flip of the spec table, navy section bands handled separately."""
import sys; sys.path.insert(0, '/dev-server/tools/catalog-ar')
import pymupdf, numpy as np
from rtbl import flip, _runs
S = '/dev-server/public/catalogs/official-ar/pylontech-optimus-a300-hy.pdf'
OUT = '/tmp/cat/a300-r.pdf'
L, M, R = 75, 300, 541
NAVY = (0.1389, 0.1684, 0.3090)
bands = [(65.3, 79.0), (269.6, 283.2), (405.2, 418.8), (541.7, 555.3)]
segs = [(79.4, 241.5), (283.5, 404.9), (419.1, 541.4), (555.6, 602)]
d = None
for y0, y1 in segs:
    d = flip(S, OUT, 1, y0, y1, (L, M), (M, R), doc=d, ralign=True, center=True)
s = pymupdf.open(S); page = d[1]; Z = 4
for y0, y1 in bands:
    pm = s[1].get_pixmap(clip=pymupdf.Rect(L + 1.5, y0 + 1.5, R - 1.5, y1 - 1.5), matrix=pymupdf.Matrix(Z, Z))
    rgb = np.frombuffer(pm.samples, np.uint8).reshape(pm.h, pm.w, pm.n)[:, :, :3]
    lite = rgb.mean(2) > 150
    cols = lite.any(0)
    runs = _runs(cols, int(12 * Z))
    page.draw_rect(pymupdf.Rect(40, y0 - 0.3, L - 0.3, y1 + 0.3), color=None, fill=(0.953, 0.953, 0.953), overlay=True)
    page.draw_rect(pymupdf.Rect(L, y0, R, y1), color=None, fill=NAVY, overlay=True)
    for c0, c1 in runs:
        x0 = L + 1.5 + c0 / Z - 0.6; x1 = L + 1.5 + c1 / Z + 0.6
        r = pymupdf.Rect(max(x0, L + 1), y0, min(x1, R - 0.5), y1)
        if x0 < M:   # label -> flush right
            nx = R - 4 - r.width
        else:        # value -> centred in left value column
            nx = L + ((R - M) - r.width) / 2
        page.show_pdf_page(pymupdf.Rect(nx, y0, nx + r.width, y1), s, 1, clip=r, overlay=True)
# certificates row: long value spills into the label column
cy0, cy1 = 241.6, 269.4
_px = s[1].get_pixmap(clip=pymupdf.Rect(520, cy0 + 2, 530, cy0 + 4)).pixel(2, 1)
page.draw_rect(pymupdf.Rect(L + 0.3, cy0, R - 0.3, cy1), color=None, fill=tuple(c / 255 for c in _px[:3]), overlay=True)
lab = pymupdf.Rect(80, cy0 + 1, 178, cy1 - 1); val = pymupdf.Rect(269, cy0, 540, cy1)
page.show_pdf_page(pymupdf.Rect(R - 4 - lab.width, cy0, R - 4, cy1), s, 1, clip=lab, overlay=True)
page.show_pdf_page(pymupdf.Rect(L + 1, cy0, L + 1 + val.width, cy1), s, 1, clip=val, overlay=True)
d.save(OUT, garbage=4, deflate=True)
pymupdf.open(OUT)[1].get_pixmap(dpi=80).save('/tmp/cat/a300.png')
