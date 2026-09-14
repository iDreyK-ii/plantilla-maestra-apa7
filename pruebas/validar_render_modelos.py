"""Comprobación adicional tras convertir las 14 plantillas con LibreOffice."""
from pathlib import Path
import json
import pymupdf
ROOT=Path(__file__).resolve().parent.parent
catalog=json.loads((ROOT/'proyecto/catalogo.json').read_text())
checks=[]
for m in catalog['models']:
 name='Plantilla_'+m['id'].replace('-','_')
 file=ROOT/'pruebas/modelos-render'/(name+'.pdf')
 try:
  d=pymupdf.open(file);blank=[];outside=[]
  for i,p in enumerate(d):
   if len(p.get_text().strip())<8:blank.append(i+1)
   if abs(p.rect.width-612)>1 or abs(p.rect.height-792)>1:outside.append(i+1)
   for w in p.get_text('words'):
    if w[0]<-1 or w[2]>613 or w[1]<-1 or w[3]>793:outside.append(i+1)
  checks.append(dict(file=file.name,pages=len(d),blankPages=blank,outsidePaper=sorted(set(outside)),ok=not blank and not outside))
  if m['id'] in ['upeu-perfil','upeu-articulo']:
   page=2 if m['id']=='upeu-perfil' else 0;d[page].get_pixmap(matrix=pymupdf.Matrix(1.25,1.25)).save(str(ROOT/'pruebas'/(name+'-vista.png')))
 except Exception as e:checks.append(dict(file=file.name,ok=False,error=str(e)))
(ROOT/'pruebas/modelos-render-resultados.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
for r in checks:print('PASS' if r['ok'] else 'FAIL',r['file'],r.get('pages',''),r.get('error',''))
if not all(r['ok'] for r in checks):raise SystemExit(1)
