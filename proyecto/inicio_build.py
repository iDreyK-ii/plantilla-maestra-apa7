"""Inicio en cajones: plantilla general, editor, modelos y ayuda separados."""
from bs4 import BeautifulSoup
from ilustraciones import study_icon

def ordenar_inicio(s,base):
    def frag(html):return BeautifulSoup(html,'html.parser')
    heading=s.select_one('.home-heading')
    heading.select_one('.eyebrow').string='PLANTILLA MAESTRA · APA 7'
    heading.select_one('h1').clear();heading.select_one('h1').append(frag('Tu plantilla APA.<br><em>Lista para empezar.</em>'))
    heading.select_one('p').string='Descarga un Word con formato APA o escribe tu documento aquí. Así de sencillo.'
    stats=heading.select_one('.dashboard-stats').extract()
    hero=s.select_one('.studio-welcome')
    mascot=hero.select_one('.studio-mascot').extract();heading.append(mascot)
    examples=s.select_one('#generalExamples').extract();examples.string='Ver ejemplo en la web';examples['class']=['btn','example-web']
    blank=s.select_one('#generalBlank').extract();blank.string='＋ Nuevo documento';blank['class']=['btn','primary']
    normal=s.select_one('.normal-word-card').extract()
    base_link=normal.select_one('#downloadBaseHome').extract();base_link.string='↓ Descargar plantilla APA (.docx)'
    word_guide=normal.select_one('[onclick="openWordGuide()"]').extract();word_guide.string='Cómo usarla en Word';word_guide['class']=['route-secondary']
    normal.clear();normal.name='section';normal['id']='downloadRoute'
    normal.append(frag('<div><span class="route-kicker">'+study_icon('document')+'01 · LA PLANTILLA PRINCIPAL</span><h2>Plantilla normal APA 7</h2><p>Un Word editable con formato APA y ejemplos de portada, citas, tablas y referencias. Descárgalo y reemplaza los ejemplos por tu contenido.</p><span class="route-note">Para cualquier curso · Sin estructura especializada</span></div><div class="normal-word-actions"></div>'))
    actions=normal.select_one('.normal-word-actions');actions.append(base_link);actions.append(examples);actions.append(word_guide)
    edit=frag('<section id="writeRoute"><div><span class="route-kicker">'+study_icon('pencil')+'02 · EL EDITOR WEB</span><h2>Escribir o editar</h2><p>Empieza en blanco, abre un Word o retoma un documento guardado en este navegador.</p></div><div class="editor-entry-actions"><button id="homeOpenWord" class="btn" onclick="chooseWordFile()">↥ Abrir un Word</button><button id="homeEditSaved" class="btn" onclick="openDocuments()">▤ Mis documentos guardados</button></div><p class="route-note">El Word se abre como copia; no reemplaza tus documentos.</p></section>')
    edit.select_one('.editor-entry-actions').insert(0,blank)
    hero.clear();hero['aria-label']='Opciones principales';routes=s.new_tag('div',attrs={'class':'work-routes'});routes.append(normal);routes.append(edit);hero.append(routes)
    catalog=s.select_one('#wordDownloads');catalog['class']=['word-downloads','home-box']
    catalog.select_one('.downloads-heading .mini-label').string='OTRO TIPO DE TRABAJO'
    catalog.select_one('#wordDownloadsTitle').string='Plantillas específicas'
    catalog.select_one('.downloads-heading p').string='Tesis, ensayos, artículos, informes y más. Elige según tu trabajo y revisa sus indicaciones.'
    catalog.select_one('.downloads-subheading h3').string='Encuentra tu modelo'
    catalog.select_one('.downloads-subheading p').string='Las categorías organizan los 14 modelos. La plantilla normal está en el primer cajón.'
    main=s.select_one('.home-main')
    support=s.new_tag('section',id='homeSupport',attrs={'class':'home-support','aria-label':'Ayuda y herramientas de apoyo'})
    study=s.select_one('.studio-study').extract();study['class']=['studio-study','home-box'];study.select_one('.mini-label').string='APRENDER';study.select_one('h2').string='Ayuda para usar APA';study.select_one('p').string='Ejemplos y 13 lecciones cortas para resolver tus dudas.'
    trust=s.select_one('.trust-home').extract();trust['class']=['trust-home','home-box'];trust.select_one('.mini-label').string='CUIDAR TU TRABAJO';trust.select_one('h2').string='Guardar, planificar y revisar';trust.select_one('p').string='Respalda tus documentos y prepara tu entrega.'
    support.append(study);support.append(trust);catalog.insert_after(support)
    # Accesos adicionales reunidos; no se elimina ninguna herramienta.
    tasks=s.select_one('.task-cards');prev=tasks.find_previous_sibling()
    if prev and 'home-section-title' in prev.get('class',[]):prev.decompose()
    extras=s.new_tag('details',attrs={'class':'home-box extra-tools'});extras.append(frag('<summary>Más herramientas <span>Asistente, revisión y biblioteca de modelos</span></summary>'));tasks.extract();extras.append(tasks)
    library=s.select_one('.models-home').extract();extras.append(library)
    extras.append(frag('<button class="btn" onclick="openGeneralGuide()">¿Qué plantilla necesito?</button>'));support.insert_after(extras)
    recent=s.select_one('#recentDocs');title=recent.find_previous_sibling();box=s.new_tag('section',attrs={'class':'home-box recent-box','aria-label':'Tu actividad local'})
    if title and 'home-section-title' in title.get('class',[]):title.extract();box.append(title)
    recent.extract();box.append(recent);box.append(stats);extras.insert_after(box)
    style=s.new_tag('style',id='inicio-en-cajones');style.string=(base/'inicio.css').read_text();s.head.append(style)
