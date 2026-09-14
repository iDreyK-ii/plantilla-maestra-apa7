"""Verificación opcional con LibreOffice real, sin cargar documentos a servicios.
Ejecutar después de test:general. Requiere LibreOffice Writer y PyMuPDF.
Los PDF/perfiles viven en una carpeta temporal y no se entregan.
No equivale a una prueba manual en Microsoft Word.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
from docx import Document
import pymupdf, subprocess, json, re, shutil, hashlib
ROOT=Path(__file__).resolve().parent.parent
engine=shutil.which('libreoffice') or shutil.which('soffice')
if not engine:raise SystemExit('Instala LibreOffice Writer para ejecutar esta comprobación adicional.')
files=[ROOT/'Plantilla_Maestra_APA7_Word.docx',*sorted((ROOT/'plantillas').glob('*.docx')),ROOT/'Guia_APA7_Estudio.docx',ROOT/'pruebas/apa-general-exportada.docx']
assert len(files)==17 and all(p.exists() for p in files),'Ejecuta test:general primero.'
version=subprocess.check_output([engine,'--version'],text=True).strip()
font=subprocess.check_output(['fc-match','Times New Roman'],text=True).strip() if shutil.which('fc-match') else 'No disponible'
checks=[]
def normalized(t):return re.sub(r'\W','',t.casefold())
with TemporaryDirectory(prefix='apa7-office-') as tmp:
    folder=Path(tmp);profile=(folder/'profile').as_uri();dest=folder/'pdf';dest.mkdir()
    process=subprocess.run([engine,'-env:UserInstallation='+profile,'--headless','--convert-to','pdf','--outdir',str(dest),*[str(p) for p in files]],text=True,capture_output=True,timeout=180)
    for f in files:
        result={'name':str(f.relative_to(ROOT)),'ok':False,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}
        try:
            assert process.returncode==0,process.stderr
            pdf=pymupdf.open(dest/(f.stem+'.pdf'));assert 0<len(pdf)<100
            text='\n'.join(p.get_text() for p in pdf);assert len(text)>100
            for p in pdf:
                assert abs(p.rect.width-612)<1 and abs(p.rect.height-792)<1,'Tamaño distinto de Carta'
                assert len(normalized(p.get_text()))>8,'Página vacía o solo numerada'
                for block in p.get_text('dict')['blocks']:
                    for line in block.get('lines',[]):
                        for span in line['spans']:
                            x0,y0,x1,y1=span['bbox'];assert x0>=-1 and y0>=-1 and x1<=613 and y1<=793,'Texto fuera de página'
            doc=Document(f);last=next(p.text for p in reversed(doc.paragraphs) if p.text.strip())
            assert normalized(last)[-60:] in normalized(text),'Final del contenido no localizado en PDF'
            if f.name in ['Plantilla_Maestra_APA7_Word.docx','apa-general-exportada.docx']:
                assert sum(len(p.get_images()) for p in pdf)>0,'Figura ausente'
                assert any(all(normalized(w) in normalized(p.get_text()) for w in ['Tabla 1','Actividad','Lectura','Redacción']) for p in pdf),'Tabla breve dividida'
            result.update(ok=True,pages=len(pdf),pdf_sha256=hashlib.sha256((dest/(f.stem+'.pdf')).read_bytes()).hexdigest());pdf.close()
        except Exception as e:result['error']=str(e)
        checks.append(result);print('PASS' if result['ok'] else 'FAIL',result['name'],result.get('error',''))
report={'engine':version,'font_resolution':font,'scope':'Apertura y renderizado real; Carta, texto dentro de página, contenido final, tabla breve e imagen. No certifica Microsoft Word ni contenido académico.','checks':checks}
(ROOT/'pruebas/office-resultados.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
if not all(c['ok'] for c in checks):raise SystemExit(1)
