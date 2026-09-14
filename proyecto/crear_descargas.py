from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import json,base64,html
ROOT=Path(__file__).resolve().parent.parent
cat=json.loads((ROOT/'proyecto/catalogo.json').read_text())
with ZipFile(ROOT/'Plantillas_APA7_Word.zip','w',ZIP_DEFLATED) as z:
 z.write(ROOT/'Plantilla_Maestra_APA7_Word.docx','Plantilla_Maestra_APA7_Word.docx')
 z.write(ROOT/'Guia_APA7_Estudio.docx','Guia_APA7_Estudio.docx')
 for p in sorted((ROOT/'plantillas').glob('*.docx')):z.write(p,'plantillas/'+p.name)
 z.writestr('LEEME.txt','16 documentos Word: 15 plantillas APA 7 y una guia de estudio.\nFormato base: Carta, margenes 2,54 cm, Times New Roman 12, doble espacio y sangrias reales.\nReemplaza los corchetes y retira la ficha didactica antes de entregar. Los modelos institucionales son adaptaciones estructurales, no formularios oficiales aprobados. Consulta las advertencias y fuentes dentro de cada archivo.\n')
(ROOT/'proyecto/paquete-word.js').write_text('const WORD_PACK_BASE64='+json.dumps(base64.b64encode((ROOT/'Plantillas_APA7_Word.zip').read_bytes()).decode())+';\n')
esc=html.escape
cards=''
for m in sorted(cat['models'],key=lambda m:(m['historical'],m['category']!='UPeU')):
 file='plantillas/Plantilla_'+m['id'].replace('-','_')+'.docx'
 cards+=f'<article><p class="tag">{esc(m["org"])}</p><h2>{esc(m["label"])}</h2><p>{esc(m["summary"])}</p><p class="note">{esc(m["warnings"][0])}</p><a href="{file}" download>Descargar Word (.docx)</a></article>'
page='''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Descargas Word — Plantilla Maestra APA 7</title><style>*{box-sizing:border-box}body{margin:0;background:#fbf8ff;color:#3d3247;font:16px/1.65 system-ui,sans-serif}main{max-width:1120px;margin:40px auto;padding:0 22px}h1{line-height:1.2;font-size:36px}h2{font-size:22px}a{display:inline-block;background:#73508f;color:white;text-decoration:none;padding:12px 18px;border-radius:12px;font-weight:650}a:focus{outline:3px solid #304c28;outline-offset:3px}.lead{font-size:18px}.base{background:#f0e7f9;border:1px solid #c6b0d8;border-radius:22px;padding:28px;margin:24px 0}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}article{background:white;border:1px solid #ded0e8;padding:24px;border-radius:18px;min-width:0}.tag,.note{font-size:13px}.tag{color:#634176;font-weight:bold}.note{background:#fcf4e5;padding:12px;border-radius:8px}.plain{background:transparent;color:#624177;text-decoration:underline;padding:0;margin:14px 0}footer{margin:32px 0;font-size:14px}@media(max-width:600px){.grid{grid-template-columns:1fr}h1{font-size:28px}.base{padding:20px}a{white-space:normal}}</style></head><body><main><p class="tag">PLANTILLA MAESTRA APA 7 · ARCHIVOS LISTOS</p><h1>Descarga tus plantillas Word</h1><p class="lead">La plantilla normal y los 14 modelos, cada uno en su propio archivo .docx. No necesitas crear un documento ni activar JavaScript.</p><section class="base"><h2>Plantilla APA normal — la plantilla maestra</h2><p>Portada, estilos, encabezados 1–5, párrafos, referencias y número de página. Carta · márgenes 2,54 cm · Times New Roman 12 · doble espacio.</p><a href="Plantilla_Maestra_APA7_Word.docx" download>↓ Descargar plantilla normal (.docx)</a> <a href="Plantillas_APA7_Word.zip" download>↓ Todos los Word (.zip)</a><p><a href="Guia_APA7_Estudio.docx" download>↓ Descargar guía práctica APA 7 (.docx)</a></p></section><h2>14 modelos por tipo de trabajo</h2><p>Son adaptaciones educativas con fuentes. Confirma los requisitos de tu programa o revista antes de entregar.</p><div class="grid">'''+cards+'''</div><footer><p>Reemplaza las indicaciones entre corchetes y retira la ficha didáctica. La estructura institucional puede requerir ajustes de papel, portada o presentación.</p><p>Esta página acompaña al proyecto completo: si trabajas sin servidor, extrae primero todo el ZIP. Para la aplicación HTML autónoma, utiliza sus descargas incorporadas. El visor incrustado puede bloquear descargas: abre la página en una pestaña normal.</p><a class="plain" href="Plantilla_Maestra_APA7.html">Abrir el editor y las guías →</a></footer></main></body></html>'''
from bs4 import BeautifulSoup
soup=BeautifulSoup(page,'html.parser')
for a in soup.select('a[download]'):
 path=ROOT/a['href'];mime='application/zip' if path.suffix=='.zip' else 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
 a['download']=path.name;a['data-static-file']=str(path.relative_to(ROOT));a['href']='data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode()
soup.select('footer p')[1].string='Los archivos están incorporados en esta página. Puedes descargar este HTML y usarlo solo, sin internet, sin JavaScript y sin extraer archivos vecinos. Abre el HTML en un navegador normal, no dentro de un visor limitado.'
from identidad_build import enhance_downloads
enhance_downloads(soup,ROOT)
(ROOT/'descargas.html').write_text(str(soup))
print('15 plantillas, guía y ZIP disponibles en la página de descargas sin JavaScript')
