import sys; sys.path.insert(0,"/tmp/cat")
import pymupdf, numpy as np
from rtl import recompose, cols_rev
S="s595.pdf"; src=pymupdf.open(S)[1]; E=575
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
    m=[]
    for b in out:
        if m and b[0]-m[-1][1]<6: m[-1]=(m[-1][0],b[1])
        else: m.append(b)
    res=[]
    for s,e in m:
        cols=np.where(a[s:e].any(0))[0]; inkR=x0+(cols.max()+1)/z
        res.append(((x0,y0+s/z-0.6,x1,y0+e/z+0.6), right-(inkR-x0)))
    return res
p1=[((37,93,160,117),E-123),((370,108,590,372),30),((37,117,162,350),E-125),
((37,352,225,367),E-188),((37,372,150,396.3),E-113),((37,396.3,162,512),E-125),
((37,525,205,558),E-168),((205,533,385,558),E-168-182),((375,528,590,726),30),((37,558,162,662),E-125),
((37,660,145,684),E-108),((37,684,162,736),E-125)]
p1+=bands(162,112,370,350,E-130)+bands(162,684,370,736,E-130)
p1+=cols_rev(162,572,5,396.3,408,37)+cols_rev(162,572,10,408,497,37)+cols_rev(162,572,5,497,509,37)
p1+=cols_rev(170,356,3,553,662,E-130-186)
p0=[((36,525,255,625),E-219),((280,528,605,600),20),((60,655,240,715),E-180),((285,628,580,742),30)]
recompose(S,"s595r.pdf",{0:p0,1:p1})
d=pymupdf.open("s595r.pdf")
for i,p in enumerate(d): p.get_pixmap(dpi=110).save(f"r595-{i}.png")
