import sys; sys.path.insert(0,'/dev-server/tools/catalog-ar')
from rtbl import flip
S='/dev-server/public/catalogs/official-ar/'
jobs=[('solis-s6-eh3p-75-125k--80k',72,770,(43,190),(190,553)),
('deye-sun-3-6k-sg04lp1--6k-sm2',36,764,(46,192),(192,555)),
('deye-sun-7-6-12k-sg02lp1--8k',36,764,(46,192),(192,555))]
for f,y0,y1,l,v in jobs:
  flip(S+f+'.pdf','/tmp/cat/'+f+'-r.pdf',1,y0,y1,l,v,ralign=True)
