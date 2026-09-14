"""Publicación única: fuentes, Word preparados, documentación y pruebas actuales."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,hashlib
ROOT=Path(__file__).resolve().parent.parent
main=ROOT/'Plantilla_Maestra_APA7.html'
assert main.read_bytes()==(ROOT/'index.html').read_bytes(), 'El alias del servidor no corresponde a la entrega actual'
assert not list(ROOT.glob('Plantilla_Maestra_APA7_Web_v3*.html'))
assert not list(ROOT.glob('Plantilla_Maestra_APA7_v3*_Proyecto.zip'))
files=[ROOT/x for x in ['Plantilla_Maestra_APA7.html','index.html','Plantilla_Maestra_APA7_Word.docx','LEEME_APA7.md','FUENTES_Y_MODELOS_APA7.md','REVISION_APA7.md','package.json','package-lock.json','requirements.txt','descargas.html','Plantillas_APA7_Word.zip','Guia_APA7_Estudio.docx','README.md','PUBLICAR_GITHUB.md','requirements-build.txt','.gitignore','.gitattributes']]
files+=list((ROOT/'plantillas').glob('*.docx'))
files+=list((ROOT/'.github/workflows').glob('*.yml'))
files+=[p for p in (ROOT/'proyecto').iterdir() if p.is_file() and p.suffix in ['.js','.py','.json','.css','.txt','.md','.html']]
files+=[p for p in (ROOT/'pruebas').iterdir() if p.is_file() and (p.suffix in ['.cjs','.py'] or p.name in ['resultados.json','avanzadas.json','word-resultados.json','word-estructura.json','publicacion-resultados.json','accesibilidad.json','html-publico.json','modelos-resultados.json','modelos-word-resultados.json','modelos-render-resultados.json','limpieza.json','descargas-resultados.json','descargas-word-resultados.json','descargas-inicio.png','descargas-movil.png','github-resultados.json','diseno-resultados.json','general-resultados.json','general-word-resultados.json','office-resultados.json','descargas-marcos-resultados.json','error-selector-reproducido.json','descarga-corregida-movil.png','descarga-corregida-marco.png','confianza-resultados.json','confianza-word-resultados.json','confianza-plan.png','confianza-entrega.png','confianza-proteccion.png','confianza-movil.png','studio-resultados.json','multinavegador-resultados.json','studio-inicio.png','studio-editor.png','studio-aprender.png','studio-movil.png','figura.png','inicio.png','editor.png','biblioteca-modelos.png','biblioteca-movil.png','Plantilla_upeu_perfil-vista.png','Plantilla_upeu_articulo-vista.png'])]
files.append(ROOT/'investigacion/enlaces-upeu.json')
files += [ROOT/'assets'/name for name in ['favicon.svg','favicon.png','estudiantes-kawaii.webp','vista-previa.png','vista-editor.png','ejemplo-esquema.png']]
files=sorted(set(files));assert all(p.exists() for p in files)
manifest={'edition':json.loads((ROOT/'package.json').read_text())['version'],'catalog':'2026-09-13.1','files':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
manifest_path=ROOT/'pruebas/entrega-manifiesto.json';manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
version=json.loads((ROOT/'package.json').read_text())['version']
output=ROOT/('Word_APA_GitHub_'+version.replace('.','_')+'.zip')
with ZipFile(output,'w',ZIP_DEFLATED,compresslevel=9) as z:
 for p in files+[manifest_path]:z.write(p,p.relative_to(ROOT))
with ZipFile(output) as z:
 assert z.testzip() is None
 assert z.read('Plantilla_Maestra_APA7.html')==main.read_bytes()
 assert len([n for n in z.namelist() if n.startswith('plantillas/') and n.endswith('.docx')])==14
print(output.name,output.stat().st_size,'bytes;',len(files)+1,'archivos; integridad ZIP correcta')
