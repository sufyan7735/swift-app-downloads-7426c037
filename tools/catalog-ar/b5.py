import sys; sys.path.insert(0, '/dev-server/tools/catalog-ar')
import pymupdf
from rtbl import flip
S = '/dev-server/public/catalogs/official-ar/'
D = ((46, 192), (192, 555))
jobs = [(f, 36, 764) + D for f in ['deye-sun-14-20k-sg05lp3--16k', 'deye-sun-14-20k-sg05lp3--20k',
        'deye-sun-29-9-50k-sg01hp3--30k', 'deye-sun-29-9-50k-sg01hp3--50k',
        'deye-sun-60-80k-sg02hp3--80k', 'deye-sun-7-6-12k-sg02lp1--12k']]
jobs=[(f,58,740,l,v) if '29-9-50k' in f else (f,y0,y1,l,v) for f,y0,y1,l,v in jobs]
jobs.append(('solis-s6-eh3p-75-125k--125k', 72, 770, (43, 190), (190, 553)))
N = int(sys.argv[1])
for f, y0, y1, l, v in jobs[N:N + 1]:
    flip(S + f + '.pdf', '/tmp/cat/' + f + '-r.pdf', 1, y0, y1, l, v, ralign=True, center=True)
    pymupdf.open('/tmp/cat/' + f + '-r.pdf')[1].get_pixmap(dpi=80).save('/tmp/cat/' + f + '-r-2.png')
