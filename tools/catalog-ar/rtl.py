"""Re-compose a rebuilt Arabic catalog into a right-to-left layout by moving page regions.
moves: {pno: [((x0,y0,x1,y1), dest_x0), ...]}  -> region copied (not mirrored) to dest_x0 at same y.
All source regions are blanked first, then redrawn at their destinations."""
import pymupdf, sys


def recompose(src, dst, moves):
    s = pymupdf.open(src)
    d = pymupdf.open(src)
    for pno, mv in moves.items():
        page = d[pno]
        for (x0, y0, x1, y1), _ in mv:
            page.draw_rect(pymupdf.Rect(x0, y0, x1, y1), color=None, fill=(1, 1, 1), overlay=True)
        for (x0, y0, x1, y1), dx in mv:
            page.show_pdf_page(pymupdf.Rect(dx, y0, dx + (x1 - x0), y1), s, pno,
                               clip=pymupdf.Rect(x0, y0, x1, y1), overlay=True)
    d.save(dst, garbage=4, deflate=True)


def cols_rev(x0, x1, n, y0, y1, dest_x0):
    """reverse n equal columns spanning [x0,x1]; block placed starting at dest_x0"""
    w = (x1 - x0) / n
    return [((x0 + k * w, y0, x0 + (k + 1) * w, y1), dest_x0 + (n - 1 - k) * w) for k in range(n)]
