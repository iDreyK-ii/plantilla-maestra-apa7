from zipfile import ZipFile
from pathlib import Path
from lxml import etree
import json
checks=[]
def check(name,ok):
 checks.append({'name':name,'ok':bool(ok)})
 print('PASS' if ok else 'FAIL',name)
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
def xml(name):
 with ZipFile(Path('pruebas')/name) as z:
  assert z.testzip() is None
  return etree.fromstring(z.read('word/document.xml'))
plan=xml('ficha-planificacion.docx');paper=xml('confianza-trabajo.docx');review=xml('hoja-revision.docx')
text=lambda x: ' '.join(x.xpath('//w:t/text()',namespaces=ns))
check('Ficha Word conserva anotaciones y conexiones', 'NOTA_PRIVADA_ETICA' in text(plan) and 'Corpus público verificado' in text(plan))
check('Documento Word excluye ficha y checklist privados', 'NOTA_PRIVADA_ETICA' not in text(paper) and 'Confirmaciones del estudiante' not in text(paper))
check('Hoja Word indica límites y confirmaciones manuales', 'No es una certificación APA' in text(review) and 'pendiente o requiere nueva revisión' in text(review))
for name,x in [('Ficha',plan),('Revisión',review)]:
 size=x.find('.//w:pgSz',ns);m=x.find('.//w:pgMar',ns);attr=lambda a,k:a.get('{'+ns['w']+'}'+k)
 check(name+': Carta y márgenes de una pulgada',attr(size,'w')=='12240' and attr(size,'h')=='15840' and all(attr(m,k)=='1440' for k in ['top','bottom','left','right']))
Path('pruebas/confianza-word-resultados.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
assert all(c['ok'] for c in checks)
