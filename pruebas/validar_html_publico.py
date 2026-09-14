from pathlib import Path
from docx import Document
import html5lib, re, json
src=Path('Plantilla_Maestra_APA7.html').read_text()
p=html5lib.HTMLParser(strict=False);p.parse(src)
assert not p.errors, p.errors
assert src.count('</html>')==1 and src.count('</body>')==1
assert not re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]',src)
for file in ['Plantilla_Maestra_APA7_Word.docx','pruebas/publicacion-word.docx','pruebas/trabajo-exportado.docx']:
    d=Document(file);txt='\n'.join(p.text for p in d.paragraphs)
    assert not re.search(r'function\s+\w+|onclick\s*=|<[/!]?(?:html|script|button)|Abrir impresión|Tus documentos permanecen en este dispositivo',txt),file
    print('PASS DOCX sin código ni controles:',file)
print('PASS HTML5: cero errores de análisis, cierres correctos y sin caracteres de control')
Path('pruebas/html-publico.json').write_text(json.dumps({'html5_parse_errors':p.errors,'docx_checked':3,'status':'passed'},indent=2))
