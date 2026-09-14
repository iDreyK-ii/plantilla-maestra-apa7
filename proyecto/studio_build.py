from pathlib import Path
import json,base64
from bs4 import BeautifulSoup

def enhance(s,base):
 def frag(html):return BeautifulSoup(html,'html.parser')
 s.title.string='Plantilla Maestra APA 7 · Tu estudio académico'
 home=s.select_one('#home');home['class']=['home','studio-home']
 nav=s.select_one('.home-nav');nav.select_one('.brand small').string='TU ESTUDIO ACADÉMICO'
 tiny=nav.select_one('.field-row > .small')
 if tiny:tiny.decompose()
 nav.select_one('.field-row').insert(0,frag('<span id="runtimeBadge" class="runtime-badge">Word directo disponible · iniciando editor</span>'))
 rail=frag('''<aside class="studio-rail" aria-label="Navegación del escritorio"><div class="rail-label">TU ESPACIO</div><button class="rail-link selected" onclick="studioHome()"><span>▦</span> Mi escritorio</button><button class="rail-link" onclick="openDocuments()"><span>▤</span> Mis documentos</button><button class="rail-link" onclick="goToWordDownloads()"><span>↓</span> Plantillas Word</button><button class="rail-link" onclick="chooseWordFile()"><span>↥</span> Abrir un Word</button><div class="rail-label">APRENDE Y AVANZA</div><button class="rail-link" onclick="openGuide()"><span>✦</span> Aprender APA 7</button><button class="rail-link" onclick="openStartPath()"><span>↗</span> Mi primera entrega</button><button class="rail-link" onclick="openDownloadHelp()"><span>?</span> Ayuda de descarga</button><div class="rail-note"><span class="tiny-spark">✧</span><b>Un paso a la vez.</b><p>Las ideas son tuyas.<br>El orden lo ponemos juntos.</p><span class="offline-chip">● Local y sin cuenta</span></div></aside>''')
 nav.insert_after(rail)
 heading=s.select_one('.home-heading');heading.clear();heading.append(frag('''<div><div class="eyebrow">MENOS FORMATO. MÁS IDEAS. ✦</div><h1>Tu próximo gran trabajo<br>empieza <em>aquí.</em></h1><p>Escribe con claridad, aprende a tu ritmo y llévate un Word con base APA 7.</p></div><div class="dashboard-stats"><div><b id="studioDocs">0</b><span>documentos locales</span></div><div><b>15</b><span>plantillas APA 7</span></div><div><b id="studioLessons">0/13</b><span>prácticas completadas</span></div></div>'''))
 oldhero=s.select_one('.welcome-panel');art=s.select_one('.welcome-art svg');art.extract()
 hero=frag('''<section class="studio-welcome"><div><span class="studio-chip">TU NUEVO LUGAR PARA ESCRIBIR</span><h2>Una página en blanco.<br>Un montón de posibilidades.</h2><p>De tu primera idea a la entrega: un editor académico,<br>modelos con fuentes y una guía que sí se entiende.</p><div class="studio-hero-actions"><button class="btn primary" onclick="openNewDocWizard()">＋ Nuevo documento APA</button><button class="btn" onclick="chooseWordFile()">↥ Abrir mi Word</button><a class="btn" data-ready-word="base">↓ Plantilla normal</a><button class="btn ghost" onclick="openStartPath()">¿Por dónde empiezo? →</button></div></div><div class="studio-mascot" aria-hidden="true"></div></section>''');hero.select_one('.studio-mascot').append(art)
 heading.insert_after(hero);oldhero.decompose()
 # La plantilla normal queda a continuación del bloque de bienvenida, no escondida en un asistente.
 normal=s.select_one('.normal-word-card .mini-label');normal.string='LISTA PARA ABRIR · LA PLANTILLA NORMAL'
 s.select_one('.normal-word-card h3').string='Tu base APA 7, sin empezar de cero.'
 for i,card in enumerate(s.select('.home-word-model')):
  id=card.select_one('[data-ready-word]')['data-ready-word'];m=next(m for m in json.loads((base/'catalogo.json').read_text())['models'] if m['id']==id)
  card['data-category']=m['category'];card['data-tone']=str(i%4)
  card.insert(0,frag('<div class="model-icon" aria-hidden="true">'+['✦','▤','✎','◇'][i%4]+'</div>'))
  badge=s.new_tag('span',attrs={'class':'apa-badge'});badge.string='APA 7 · .docx';card.insert(1,badge)
 filt=frag('''<div class="studio-model-filter"><div class="field"><label for="homeModelSearch">Encuentra tu próximo trabajo</label><input id="homeModelSearch" placeholder="Buscar tesis, ensayo, informe…" oninput="filterHomeModels()"></div><div class="field"><label for="homeModelCategory">Procedencia</label><select id="homeModelCategory" onchange="filterHomeModels()"><option>Todas</option><option>UPeU</option><option>General</option><option>Revista</option></select></div><span id="homeModelCount" role="status">14 modelos disponibles</span></div>''')
 s.select_one('.home-word-grid').insert_before(filt)
 # Foco en el documento, sin sustituir ninguna herramienta original.
 bar=s.select_one('.toolbar');bar.extract();wrap=s.new_tag('div',attrs={'class':'studio-command-area'});tabs=frag('<nav class="ribbon-tabs" aria-label="Seleccionar herramientas">'+''.join(f'<button class="ribbon-tab" aria-pressed="{"true" if t=="Todas" else "false"}" data-ribbon-tab="{t}" onclick="setRibbon(\'{t}\')">{t}</button>' for t in ['Todas','Inicio','Insertar','Referencias','Revisar','Vista'])+'</nav>');wrap.append(tabs);wrap.append(bar);s.select_one('.topbar').insert_after(wrap)
 for i,g in enumerate(bar.select('.group')):g['data-ribbon']=['Inicio','Inicio','Inicio','Inicio','Insertar Referencias','Inicio','Inicio Insertar'][min(i,6)]
 bar.append(frag('''<div class="group" data-ribbon="Revisar"><button class="tool" onclick="openFind()">Buscar / reemplazar</button><button class="tool" onclick="runChecker()">Revisar formato</button></div><div class="group" data-ribbon="Vista"><button id="focusToggle" class="tool" aria-pressed="false" onclick="toggleFocusMode()">Concentración</button><button class="tool" onclick="openWritingGoal()">Meta de escritura</button></div>'''))
 s.select_one('#documentsModal .field-row').append(frag('<button class="btn" onclick="chooseWordFile()">Abrir Word (.docx)</button>'))
 s.select_one('#documentsModal .small').string='Admite Word (.docx), Copia APA (.json) y HTML. El Word se abre como copia nueva, con revisión de formato; no reemplaza tus documentos guardados.'
 s.find(id='openFile')['accept']='.json,.html,.htm,.docx'
 s.body.append(frag('<input id="wordOpenFile" type="file" accept=".docx" hidden onchange="importWordFile(this.files[0])">'))
 s.select_one('.top-actions').insert(0,frag('<button class="btn ghost" onclick="chooseWordFile()">Abrir Word</button>'))
 # Mejora silenciosa: todos los enlaces iniciales son nativos y llevan el archivo completo.
 files={'base':base.parent/'Plantilla_Maestra_APA7_Word.docx','pack':base.parent/'Plantillas_APA7_Word.zip','guide':base.parent/'Guia_APA7_Estudio.docx'}
 for m in json.loads((base/'catalogo.json').read_text())['models']:files[m['id']]=base.parent/'plantillas'/('Plantilla_'+m['id'].replace('-','_')+'.docx')
 basebtn=s.find(id='downloadBaseHome');basebtn.name='a';basebtn.attrs.pop('onclick',None);basebtn['data-ready-word']='base'
 for button in s.select('[onclick="downloadWordPack()"]'):
  button.name='a';button.attrs.pop('onclick',None);button['data-ready-word']='pack'
 study=frag('<section class="studio-study"><div><span class="mini-label">APRENDE ALGO. ESCRIBE MEJOR.</span><h2>APA, explicado sin enredos.</h2><p>13 módulos cortos, ejemplos, pasos concretos y ejercicios con respuesta.</p></div><div><button class="btn primary" onclick="openGuide()">Empezar a aprender →</button> <a class="btn" data-ready-word="guide">↓ Guía de estudio Word</a></div></section>')
 s.select_one('#wordDownloads').insert_after(study)
 for a in s.select('a[data-ready-word]'):
  path=files[a['data-ready-word']];mime='application/zip' if path.suffix=='.zip' else 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
  a['href']='data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode();a['download']=path.name
 nojs=s.select_one('.noscript-note');nojs.clear();nojs.append('El editor necesita JavaScript, pero las plantillas sí se pueden descargar desde sus enlaces directos, incluso sin conexión. Activa JavaScript para escribir o abrir un DOCX aquí.')

 # Protección y orientación: accesos visibles, fuera de la hoja académica.
 s.select_one('.studio-rail .rail-note').insert_before(frag('<div class="rail-label">TRABAJA CON CONFIANZA</div><button class="rail-link" onclick="openProtection()"><span>◇</span> Protección y respaldo</button><button class="rail-link" onclick="openResearchPlan()"><span>↗</span> Planifica tu trabajo</button><button class="rail-link" onclick="openDeliveryCenter()"><span>✓</span> Antes de entregar</button>'))
 s.select_one('.sidebar .quick').append(frag('<button class="btn" onclick="openResearchPlan()">Ficha de planificación</button><button class="btn" onclick="openDeliveryCenter()">Antes de entregar</button><button class="btn" onclick="openProtection()">Protección y respaldo</button>'))
 s.select_one('.toolbar').append(frag('<div class="group" data-ribbon="Revisar"><button class="tool" onclick="openResearchPlan()">Planificar</button><button class="tool" onclick="openDeliveryCenter()">Antes de entregar</button><button class="tool" onclick="openProtection()">Protección</button></div>'))
 s.select_one('#documentsModal .field-row').append(frag('<button class="btn" onclick="openProtection()">Respaldo e historial</button>'))
 s.select_one('.studio-study').insert_after(frag('<section class="trust-home"><div><span class="mini-label">TU TRABAJO, MEJOR PROTEGIDO</span><h2>Avanza con un plan. Conserva tu progreso.</h2><p>Planifica tu investigación, recupera puntos anteriores y revisa qué falta antes de entregar. Sin porcentajes de aprobación inventados.</p></div><div><button class="btn primary" onclick="openProtection()">Protección y respaldo</button><button class="btn" onclick="openResearchPlan()">Planificar mi trabajo</button><button class="btn" onclick="openDeliveryCenter()">Revisión de entrega</button></div></section>'))
 s.body.append(frag('<input type="file" id="workspaceBackupInput" accept=".json" hidden onchange="prepareWorkspaceImport(this.files[0])">'))
