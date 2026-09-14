/* APA general y categorías de uso. No se sustituyen modelos ni documentos existentes. */
const MODEL_FAMILIES=Object.fromEntries(GENERAL_APA_DATA.families.map(f=>[f.id,f.models]));
let homeFamily='all';
function setHomeFamily(family){if(family!=='all'&&!Object.hasOwn(MODEL_FAMILIES,family))return;homeFamily=family;document.querySelectorAll('[data-home-family]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.homeFamily===family)));filterHomeModels()}
function resetHomeFilters(){homeFamily='all';$('homeModelSearch').value='';$('homeModelCategory').value='Todas';setHomeFamily('all')}
function generalExamplesHTML(){
 const data=GENERAL_APA_DATA;
 const prompts=' data-template-prompt="true"';
 const blocks=data.blocks.map(b=>{
  if(b.kind==='heading')return (b.pagebreak?'<div class="page-break" contenteditable="false" aria-label="Salto de página"></div>':'')+'<h'+b.level+'>'+esc(b.text)+'</h'+b.level+'>';
  if(b.kind==='runin')return '<h'+b.level+prompts+'><span class="runin">'+esc(b.text)+'</span>'+esc(b.body)+'</h'+b.level+'>';
  if(b.kind==='instruction')return '<p class="apa-noindent"'+prompts+'>[Guía: '+esc(b.text)+']</p>';
  if(b.kind==='paragraph')return '<p class="apa-normal"'+prompts+'>'+esc(b.text)+'</p>';
  if(b.kind==='quote')return '<blockquote'+prompts+'>'+esc(b.text)+'</blockquote>';
  if(b.kind==='reference')return '<p class="reference"'+prompts+'>'+esc(b.before)+'<em>'+esc(b.italic)+'</em>'+esc(b.after)+'</p>';
  if(b.kind==='table')return '<div class="table-wrap" id="'+uid()+'"'+prompts+'><div class="table-label">'+esc(b.number)+'</div><div class="table-title">'+esc(b.title)+'</div><table><thead><tr>'+b.headers.map(x=>'<th scope="col">'+esc(x)+'</th>').join('')+'</tr></thead><tbody>'+b.rows.map(row=>'<tr>'+row.map(x=>'<td>'+esc(x)+'</td>').join('')+'</tr>').join('')+'</tbody></table><div class="table-note">'+esc(b.note)+'</div></div>';
  if(b.kind==='figure')return '<div class="figure-wrap" id="'+uid()+'"'+prompts+'><div class="figure-label">'+esc(b.number)+'</div><div class="figure-title">'+esc(b.title)+'</div><img src="'+data.figureData+'" alt="'+esc(b.alt)+'"><div class="figure-note">'+esc(b.note)+'</div></div>';
  return '';
 }).join('');
 const cover={Title:'[Título del trabajo académico]',Author:'[Nombre del estudiante o autor]',Institution:'[Institución, si corresponde]',School:'[Facultad o programa, si se solicita]',Course:'[Asignatura, si corresponde]',Professor:'[Docente, si corresponde]',Date:'[Fecha de entrega]'};
 return {cover,html:coverHTML(cover)+'<p class="apa-title">'+esc(cover.Title)+'</p><p class="apa-noindent"'+prompts+'>['+esc(data.notice)+']</p>'+blocks};
}
function startGeneralAPA(mode='examples'){
 if(!['examples','blank'].includes(mode))return;
 if(currentId&&!saveState()&&!confirm('No se pudo guardar el documento actual. Conserva una copia antes de continuar. ¿Crear otro de todos modos?'))return;
 const content=mode==='examples'?generalExamplesHTML():{html:'<p class="apa-normal"><br></p>',cover:{}};
 loadDoc({id:uid(),name:mode==='examples'?'APA general · ejemplos para aprender':'Mi documento APA',html:content.html,refs:[],config:{type:'APA general',institutionRules:'',generalMode:mode},cover:content.cover,progress:[]});
 saveState();toast(mode==='examples'?'Ejemplos listos. Sustitúyelos por tu contenido antes de entregar.':'Hoja APA lista. Escribe tu contenido o añade una portada.');
}
function openGeneralGuide(){dialog('Una base APA, a tu manera','<p>El documento general sirve para aprender el formato sin adoptar una estructura de tesis, artículo o informe.</p><ul><li><b>Con ejemplos:</b> portada, introducción, niveles de encabezado, citas, tabla, figura y referencias. Las instrucciones están marcadas para sustituirlas.</li><li><b>Hoja en blanco:</b> papel Carta, márgenes, tipografía, interlineado y numeración ya preparados; tú decides la estructura.</li><li><b>Modelo específico:</b> consulta la categoría que corresponde a tu tarea y conserva sus advertencias institucionales.</li></ul><p class="notice">Los ejemplos no son resultados reales ni un trabajo listo para entregar. APA no obliga a utilizar todas las secciones.</p>','<button class="btn" onclick="closeModal(\'dialogModal\')">Entendido</button>')}
