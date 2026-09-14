"""Prepara únicamente el sitio público. Nunca incluye documentos, backups o perfiles.
Salida: dist/. Se reconstruye desde una lista explícita de recursos de publicación.
"""
from pathlib import Path
from shutil import copyfile, rmtree
import json
root=Path(__file__).resolve().parent.parent
site=root/'dist'
if site.exists(): rmtree(site)
site.mkdir()
files=['index.html','Plantilla_Maestra_APA7.html','descargas.html','Plantilla_Maestra_APA7_Word.docx','Guia_APA7_Estudio.docx','Plantillas_APA7_Word.zip']
files += ['assets/favicon.svg','assets/favicon.png','assets/enfermera-kawaii.svg','assets/vista-previa.png','assets/vista-editor.png','assets/ejemplo-esquema.png']
models=json.loads((root/'proyecto/catalogo.json').read_text())['models']
files += ['plantillas/Plantilla_'+m['id'].replace('-','_')+'.docx' for m in models]
for name in files:
 src=root/name
 if not src.is_file(): raise SystemExit('Falta recurso público: '+name)
 dest=site/name; dest.parent.mkdir(parents=True,exist_ok=True);copyfile(src,dest)
(site/'.nojekyll').write_text('')
assert len(list((site/'plantillas').glob('*.docx')))==14
assert (site/'index.html').read_bytes()==(site/'Plantilla_Maestra_APA7.html').read_bytes()
print('Sitio preparado en dist/:',len(files)+1,'archivos; sin respaldos ni datos personales.')
