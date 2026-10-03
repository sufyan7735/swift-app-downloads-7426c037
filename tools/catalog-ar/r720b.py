import sys; sys.path.insert(0,"/tmp/cat")
import pymupdf, numpy as np
exec(open("r720.py").read().split("recompose(")[0])
src=pymupdf.open("s720.pdf")[1]
def bands(x0,y0,x1,y1,right):
    z=4; pm=src.get_pixmap(clip=pymupdf.Rect(x0,y0,x1,y1),matrix=pymupdf.Matrix(z,z),colorspace=pymupdf.csGRAY)
    a=np.frombuffer(pm.samples,np.uint8).reshape(pm.h,pm.w)<200
    rows=a.any(1); out=[]; i=0
    while i<len(rows):
        if rows[i]:
            j=i
            while j<len(rows) and rows[j]: j+=1
            out.append((i,j)); i=j
        else: i+=1
    # merge bands with gaps < 3px
    m=[]
    for b in out:
        if m and b[0]-m[-1][1]<6: m[-1]=(m[-1][0],b[1])
        else: m.append(b)
    res=[]
    for s,e in m:
        cols=np.where(a[s:e].any(0))[0]; inkR=x0+(cols.max()+1)/z
        ya=y0+s/z-0.6; yb=y0+e/z+0.6
        res.append(((x0,ya,x1,yb), right-(inkR-x0)))
    return res
# replace values block moves with per-row right-aligned moves
p1=[m for m in p1 if m[0] not in [(162,116,370,352),(162,683,366,740)]]
p1=[m for m in p1 if not (393<=m[0][1]<=393 and m[0][0]>=162)]
p1+=bands(162,116,370,352,E-130)+bands(162,683,366,740,E-130)
p1+=cols_rev(162,580,5,393,408,37)+cols_rev(162,580,10,408,510,37)
recompose("/tmp/cat/s720.pdf","/tmp/cat/s720r.pdf",{0:p0,1:p1})
render("/tmp/cat/s720r.pdf","/tmp/cat/r720",dpi=130)
