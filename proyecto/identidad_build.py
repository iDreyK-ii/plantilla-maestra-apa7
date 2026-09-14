"""Identidad visual autocontenida. No modifica las páginas académicas ni los datos."""
from pathlib import Path
import base64
import json
from bs4 import BeautifulSoup


def asset_uri(root, name, mime):
    return 'data:' + mime + ';base64,' + base64.b64encode((root / 'assets' / name).read_bytes()).decode()


def add_head(s, root):
    for link in s.select('link[rel="icon"],link[rel="apple-touch-icon"]'):
        link.decompose()
    for rel, file, mime in [('icon','favicon.svg','image/svg+xml'),('apple-touch-icon','favicon.png','image/png')]:
        link=s.new_tag('link',rel=rel,href=asset_uri(root,file,mime));link['type']=mime;s.head.append(link)
    for name, content in [('theme-color','#f8dce5'),('description','Escribe tus documentos APA 7 o descarga un Word listo para empezar. Ejemplos, modelos y guías para cualquier estudiante o autor.')]:
        old=s.find('meta',attrs={'name':name})
        if old:old.decompose()
        meta=s.new_tag('meta',attrs={'name':name,'content':content});s.head.append(meta)
    for prop, value in [('og:title','Plantilla Maestra APA 7 · Estudia, escribe y cuida tus ideas'),('og:description','Un espacio académico con 15 plantillas Word, guías paso a paso y descargas directas.'),('og:image','https://idreyk-ii.github.io/plantilla-maestra-apa7/assets/vista-previa.png'),('og:url','https://idreyk-ii.github.io/plantilla-maestra-apa7/'),('og:type','website')]:
        s.head.append(s.new_tag('meta',attrs={'property':prop,'content':value}))


def enhance_identity(s, base):
    root=base.parent
    def frag(html):return BeautifulSoup(html,'html.parser')
    add_head(s,root)
    style=s.new_tag('style',id='identidad-visual');style.string=(base/'identidad.css').read_text()+'\n'+(base/'universal.css').read_text()+'\n'+(base/'kawaii-final.css').read_text()+'\n'+(base/'enfermera.css').read_text();s.head.append(style)
    for mark in s.select('.logo-mark'):
        mark.clear();mark.append(s.new_tag('img',src=asset_uri(root,'favicon.svg','image/svg+xml'),alt='',width='43',height='43'))
    s.select_one('.home-nav .brand small').string='ESTUDIA CON CALMA. ESCRIBE CON PROPÓSITO.'
    h=s.select_one('.home-heading')
    h.select_one('.eyebrow').string='TU ESPACIO ACADÉMICO · HECHO PARA ACOMPAÑARTE'
    h.select_one('h1').clear();h.select_one('h1').append(frag('Tus ideas.<br><em>Una buena presentación.</em>'))
    h.select_one('p').string='De tus apuntes a tu próximo trabajo: aprende, escribe y avanza a tu ritmo.'
    hero=s.select_one('.studio-welcome')
    hero.select_one('.studio-chip').string='APA PARA ESTUDIAR, CREAR Y COMPARTIR'
    hero.select_one('h2').clear();hero.select_one('h2').append(frag('Elige cómo quieres trabajar.'))
    hero.select_one('p').string='Una base clara para cualquier persona que necesite escribir. Tú eliges el tema y dónde continuar.'
    hero.select_one('.studio-hero-actions').replace_with(frag('''<div class="work-routes"><section id="writeRoute"><span class="route-kicker">01 · EN LA WEB</span><h3>Escribe aquí</h3><p>Aprende con ejemplos o empieza con una hoja APA en blanco.</p><button id="generalExamples" class="btn primary" onclick="startGeneralAPA('examples')">Empezar con ejemplos →</button><button id="generalBlank" class="route-secondary" onclick="startGeneralAPA('blank')">Prefiero una hoja en blanco</button></section><section id="downloadRoute"><span class="route-kicker">02 · EN TU EQUIPO</span><h3>Continúa en Word</h3><p>Descarga la APA general explicada o elige un modelo por categoría.</p><a class="btn primary" data-ready-word="base">↓ Descargar APA general</a><button class="route-secondary" onclick="goToWordDownloads()">Explorar los modelos ↓</button></section></div>'''))
    art=hero.select_one('.studio-mascot');art.clear();art.attrs.pop('aria-hidden',None)
    art.append(frag((root/'assets/enfermera-kawaii.svg').read_text()))
    art.append(frag('<span class="care-spark" aria-hidden="true">✦</span><span class="care-spark second" aria-hidden="true">♡</span><span class="care-spark third" aria-hidden="true">✧</span><button type="button" class="motion-toggle" data-motion-toggle="" aria-pressed="false" hidden>Pausar animación</button>'))
    note=s.select_one('.rail-note');note.select_one('b').string='También cuida de ti.';note.select_one('p').string='Una pausa, una idea y un paso más. Tu aprendizaje tiene su propio ritmo.'
    note.insert(0,s.new_tag('img',src=asset_uri(root,'favicon.svg','image/svg+xml'),alt='',width='55',height='55',attrs={'class':'rail-companion','aria-hidden':'true'}))
    from ilustraciones import study_icon
    for kicker,kind in zip(s.select('.route-kicker'),['pencil','document']):kicker.insert(0,frag(study_icon(kind)))
    families=json.loads((base/'ejemplos_apa.json').read_text())['families']
    grid=s.select_one('.home-word-grid')
    for family in families:
        for mid in family['models']:
            link=s.select_one('.home-word-model [data-ready-word="'+mid+'"]')
            card=link.find_parent(class_='home-word-model');card['data-family']=family['id'];card.extract();grid.append(card)
            icon=card.select_one('.model-icon')
            if icon:
                icon.clear();icon['aria-hidden']='true';icon.append(frag(study_icon({'clase':'book','investigacion':'search','publicacion':'document','especialidad':'heart'}[family['id']])))
    buttons='<button type="button" aria-pressed="true" data-home-family="all" onclick="setHomeFamily(\'all\')">Todos <span>14</span></button>'
    for f in families:
        buttons+='<button type="button" aria-pressed="false" data-home-family="'+f['id']+'" onclick="setHomeFamily(\''+f['id']+'\')">'+f['label']+' <span>'+str(len(f['models']))+'</span></button>'
    s.select_one('.studio-model-filter').insert_before(frag('<nav class="model-family-tabs" aria-label="Tipos de trabajo">'+buttons+'</nav>'))
    grid.insert_after(frag('<div id="homeModelEmpty" class="empty-models" role="status" hidden><b>No encontramos un modelo con esos filtros.</b><p>Prueba otro término o vuelve a mostrar todos.</p><button class="btn" onclick="resetHomeFilters()">Mostrar todos los modelos</button></div>'))
    s.select_one('.downloads-subheading h3').string='Modelos para cada tipo de trabajo'
    s.select_one('.downloads-subheading p').string='Filtra por categoría. Cada modelo conserva su estructura, orientaciones y fuentes; no contiene una investigación ya realizada.'
    s.select_one('.normal-word-card h3').string='APA general: el formato, explicado con ejemplos.'
    s.select_one('.normal-word-card p').string='Portada, párrafos, encabezados, citas, tabla, figura y referencias. Sustituye los ejemplos por tu contenido; no es una estructura de tesis.'
    s.select_one('.normal-word-card .mini-label').string='EMPIEZA POR LA BASE · SIN MODELO ESPECIALIZADO'
    s.select_one('.normal-word-actions').append(frag('<button class="btn ghost" onclick="openGeneralGuide()">¿APA general o modelo?</button>'))
    # El nuevo enlace permanece nativo y funciona incluso sin JavaScript.
    normal=s.select_one('#downloadRoute a[data-ready-word="base"]')
    normal['href']=asset_uri(root,'../Plantilla_Maestra_APA7_Word.docx','application/vnd.openxmlformats-officedocument.wordprocessingml.document');normal['download']='Plantilla_Maestra_APA7_Word.docx'
    footer=s.select_one('.home-footer')
    footer.append(frag('<span>Studio APA · '+json.loads((root/'package.json').read_text())['version']+' · Diseño sereno, trabajo riguroso.</span>'))
    from inicio_build import ordenar_inicio
    ordenar_inicio(s,base)


def enhance_downloads(s,root):
    add_head(s,root)
    style=s.new_tag('style');style.string='''body{background:#fcf8f9;color:#294d46}main{max-width:1120px}h1,h2{color:#294f46}a{background:#246b66;color:#fff;border-radius:11px}a:hover{background:#19564f}a:focus-visible{outline:3px solid #974a69;outline-offset:3px}.base{background:linear-gradient(110deg,#e7f5ef,#fff0f4);border:1px solid #bfdace}.tag{color:#5c7163}.note{background:#fff3e2;color:#70562f}article{border-color:#d6e4d8;border-radius:18px;box-shadow:0 4px 15px #304b3408}.plain{color:#32664f}.download-intro{display:flex;align-items:center;gap:32px}.download-intro>div{flex:1}.download-intro img{width:280px;height:auto;border-radius:25px;mix-blend-mode:multiply}.download-brand{display:flex;align-items:center;gap:12px;font-weight:700;color:#365849;font-size:13px;margin-bottom:25px}.download-brand img{width:40px;height:40px}.base a{margin:4px 3px 4px 0}footer{color:#526e59}@media(max-width:650px){.download-intro{display:block}.download-intro img{width:210px;display:block;margin:8px auto}.download-intro h1{font-size:31px}.base a{display:block;text-align:center}}''';s.head.append(style)
    main=s.select_one('main');brand=s.new_tag('div',attrs={'class':'download-brand'});brand.append(s.new_tag('img',src=asset_uri(root,'favicon.svg','image/svg+xml'),alt='',width='40',height='40'));brand.append('PLANTILLA MAESTRA APA 7 · TU BIBLIOTECA WORD');main.insert(0,brand)
    intro=s.new_tag('section',attrs={'class':'download-intro'});text=s.new_tag('div')
    for node in [s.select_one('main > .tag'),s.select_one('h1'),s.select_one('.lead')]:
        if node:node.extract();text.append(node)
    intro.append(text);intro.append(BeautifulSoup((root/'assets/enfermera-kawaii.svg').read_text(),'html.parser'));brand.insert_after(intro)
    button=s.new_tag('button',type='button',attrs={'class':'motion-toggle','data-motion-toggle':'','aria-pressed':'false','hidden':''});button.string='Pausar animación';text.append(button)
    visual=s.new_tag('style');visual.string=(root/'proyecto/kawaii-final.css').read_text()+'\n'+(root/'proyecto/enfermera.css').read_text();s.head.append(visual)
    motion=s.new_tag('script');motion.string=(root/'proyecto/movimiento.js').read_text();s.body.append(motion)

    # Familias visibles incluso sin JavaScript en la página independiente.
    families=json.loads((root/'proyecto/ejemplos_apa.json').read_text())['families']
    old_grid=s.select_one('.grid')
    if old_grid:
        groups=s.new_tag('div',id='modelos-por-categoria')
        nav=s.new_tag('nav',attrs={'class':'download-category-nav','aria-label':'Categorías de plantillas'})
        for f in families:
            a=s.new_tag('a',href='#categoria-'+f['id'],attrs={'class':'plain'});a.string=f['label'];nav.append(a)
            section=s.new_tag('section',id='categoria-'+f['id']);h=s.new_tag('h2');h.string=f['label'];section.append(h);grid=s.new_tag('div',attrs={'class':'grid'})
            for mid in f['models']:
                link=s.select_one('a[data-static-file="plantillas/Plantilla_'+mid.replace('-','_')+'.docx"]')
                if link:
                    card=link.find_parent('article');card.extract();grid.append(card)
            section.append(grid);groups.append(section)
        old_grid.insert_before(nav);old_grid.replace_with(groups)
        extra=s.new_tag('style');extra.string='.download-category-nav{display:flex;flex-wrap:wrap;gap:10px 22px;margin:22px 0}#modelos-por-categoria>section{scroll-margin-top:24px;margin-bottom:30px}';s.head.append(extra)
    s.select_one('.base h2').string='APA general, con ejemplos para empezar'
    s.select_one('.base p').string='Una base sin estructura especializada: portada, párrafos, niveles de encabezado, citas, tabla, figura y referencias. Los ejemplos son didácticos; sustitúyelos antes de entregar.'
