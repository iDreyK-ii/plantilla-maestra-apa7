/* Exportación OOXML real en el navegador. docx se empaqueta localmente: no CDN, red ni servidor. */
import {Document,Packer,Paragraph,TextRun,Header,PageNumber,Table,TableRow,TableCell,WidthType,BorderStyle,ImageRun,ExternalHyperlink,TableOfContents,StyleLevel,AlignmentType,LevelFormat} from 'docx';
const TNR='Times New Roman';
const map={'apa-normal':'APANormal','apa-noindent':'APANoIndent','apa-title':'APATitle','apa-subtitle':'APASubtitle','apa-subtitle1':'APASubtitle1','apa-subtitle2':'APASubtitle2',reference:'APAReference'};
const definitions=[
 ['APANormal','APA Párrafo',{indent:{firstLine:720}}],
 ['APANoIndent','APA Sin sangría',{indent:{firstLine:0}}],
 ['APATitle','APA Título',{alignment:AlignmentType.CENTER,indent:{firstLine:0}},{bold:true}],
 ['APASubtitle','APA Subtítulo',{alignment:AlignmentType.CENTER,indent:{firstLine:0}}],
 ['APASubtitle1','APA Subtítulo 1',{indent:{firstLine:0}},{bold:true}],
 ['APASubtitle2','APA Subtítulo 2',{indent:{firstLine:0}},{bold:true,italics:true}],
 ...Array.from({length:5},(_,i)=>['APAHeading'+(i+1),'APA Nivel '+(i+1),{alignment:i===0?AlignmentType.CENTER:AlignmentType.LEFT,indent:{firstLine:i>2?720:0},outlineLevel:i,keepNext:true},{bold:i<3,italics:i===2}]),
 ['APAReference','APA Referencia',{indent:{left:720,hanging:720}}],
 ['APAQuote','APA Cita larga',{indent:{left:720,firstLine:0}}],
 ['APACover','APA Portada',{alignment:AlignmentType.CENTER,indent:{firstLine:0}}],
 ['APANumber','APA Número de elemento',{indent:{firstLine:0},keepNext:true},{bold:true}],
 ['APACaption','APA Título de elemento',{indent:{firstLine:0},keepNext:true},{italics:true}],
 ['APANote','APA Nota de elemento',{indent:{firstLine:0}}],
];
const none={style:BorderStyle.NONE,size:0,color:'auto'},line={style:BorderStyle.SINGLE,size:8,color:'000000'};
export async function buildDOCX(html,title='Documento académico'){
 const root=document.createElement('div');root.innerHTML=html;
 const media=new Map(),warnings=[];
 for(const img of root.querySelectorAll('img')){
  try{if(!/^data:image\/(png|jpeg|gif|webp);base64,/i.test(img.src))throw Error('Imagen no incorporada');const im=new Image();im.src=img.src;await im.decode();const scale=Math.min(1,1600/im.naturalWidth,1600/im.naturalHeight);const canvas=document.createElement('canvas');canvas.width=Math.max(1,Math.round(im.naturalWidth*scale));canvas.height=Math.max(1,Math.round(im.naturalHeight*scale));canvas.getContext('2d').drawImage(im,0,0,canvas.width,canvas.height);const png=canvas.toDataURL('image/png');const bytes=Uint8Array.from(atob(png.split(',')[1]),c=>c.charCodeAt(0));const ratio=Math.min(1,624/canvas.width,600/canvas.height);media.set(img,{bytes,width:Math.round(canvas.width*ratio),height:Math.round(canvas.height*ratio)});}catch(e){warnings.push('No se pudo exportar una imagen: '+(img.alt||'sin descripción'));}
 }
 const numbering=[];let listCounter=0,pendingBreak=false;
 function runs(node,format={}){
  if(node.nodeType===3)return node.textContent?[new TextRun({text:node.textContent,...format})]:[];
  if(node.nodeType!==1)return [];
  const tag=node.tagName;
  if(node.matches('.selection-marker,.page-number,.no-print,script,style'))return [];
  if(tag==='BR')return [new TextRun({break:1,...format})];
  if(tag==='IMG'){const m=media.get(node);return m?[new ImageRun({data:m.bytes,type:'png',transformation:{width:m.width,height:m.height},altText:{title:node.alt||'Figura',description:node.alt||'Figura académica',name:'Figura'}})]:[new TextRun({text:'[Imagen pendiente: '+(node.alt||'revisar fuente')+']',...format})];}
  const f={...format};if(['B','STRONG'].includes(tag)||node.classList.contains('runin'))f.bold=true;
  if(['I','EM'].includes(tag))f.italics=true;if(tag==='U')f.underline={};if(tag==='S')f.strike=true;if(tag==='SUP')f.superScript=true;if(tag==='SUB')f.subScript=true;
  const cs=node.style;if(cs.fontWeight)f.bold=/bold|[6-9]00/.test(cs.fontWeight);if(cs.fontStyle)f.italics=cs.fontStyle==='italic';
  if(node.classList.contains('runin')&&node.closest('h5'))f.italics=true;
  const children=[...node.childNodes].flatMap(n=>runs(n,f));
  if(tag==='A'&&/^https?:\/\//i.test(node.getAttribute('href')||''))return [new ExternalHyperlink({children,link:node.getAttribute('href')})];
  return children;
 }
 function paragraph(node,style='APANormal',extra={}){
  const options={style,children:[...node.childNodes].flatMap(n=>runs(n)),...extra};
  const alignment={left:AlignmentType.LEFT,right:AlignmentType.RIGHT,center:AlignmentType.CENTER,justify:AlignmentType.JUSTIFIED};
  if(alignment[node.style?.textAlign])options.alignment=alignment[node.style.textAlign];
  if(pendingBreak){options.pageBreakBefore=true;pendingBreak=false;}
  if(node.matches?.('h4,h5'))options.children=[...node.childNodes].flatMap(n=>runs(n,{bold:false,italics:false}));
  return new Paragraph(options);
 }
 function table(node){
  if(!node.rows?.length)return [];
  const cols=Math.max(1,...[...node.rows].map(r=>[...r.cells].reduce((a,c)=>a+Math.max(1,c.colSpan),0)));
  const compactTable=node.rows.length<=6&&node.textContent.length<800;
  const rows=[...node.rows].map((row,i)=>new TableRow({tableHeader:row.parentElement.tagName==='THEAD'||(i===0&&!!row.querySelector('th')),cantSplit:true,children:[...row.cells].map(cell=>new TableCell({width:{size:9360*cell.colSpan/cols,type:WidthType.DXA},columnSpan:cell.colSpan>1?cell.colSpan:undefined,rowSpan:cell.rowSpan>1?cell.rowSpan:undefined,margins:{top:60,bottom:60,left:90,right:90},borders:{top:i===0?line:none,left:none,right:none,bottom:cell.tagName==='TH'||i===node.rows.length-1?line:none},children:[paragraph(cell,'APANoIndent',{keepNext:compactTable&&i<node.rows.length-1,children:[...cell.childNodes].flatMap(n=>runs(n,cell.tagName==='TH'?{bold:true}:{})),spacing:{line:360,before:0,after:0}})]}))}));
  const result=[];if(pendingBreak){result.push(new Paragraph({pageBreakBefore:true,spacing:{line:20,before:0,after:0}}));pendingBreak=false;}
  result.push(new Table({width:{size:9360,type:WidthType.DXA},columnWidths:Array(cols).fill(Math.floor(9360/cols)),borders:{top:line,bottom:line,left:none,right:none,insideHorizontal:none,insideVertical:none},rows}));return result;
 }
 function list(node,level=0,ref=null){
  if(!ref){ref='list'+(++listCounter);numbering.push({reference:ref,levels:Array.from({length:9},(_,i)=>({level:i,format:node.tagName==='OL'?LevelFormat.DECIMAL:LevelFormat.BULLET,text:node.tagName==='OL'?'%'+(i+1)+'.':'•',alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:720*(i+1),hanging:360}},run:{font:TNR,size:24}}}))});}
  const out=[];for(const li of [...node.children].filter(n=>n.tagName==='LI')){
   const clone=li.cloneNode(true);clone.querySelectorAll('ul,ol').forEach(n=>n.remove());out.push(paragraph(clone,'APANoIndent',{numbering:{reference:ref,level:Math.min(level,8)}}));
   for(const sub of [...li.children].filter(n=>n.matches('ul,ol')))out.push(...list(sub,level+1,sub.tagName===node.tagName?ref:null));
  }return out;
 }
 function blocks(node){
  if(node.nodeType===3)return node.textContent.trim()?[new Paragraph({style:'APANormal',children:runs(node)})]:[];
  if(node.nodeType!==1)return [];
  if(node.matches('.page-number,.selection-marker,.no-print,script,style'))return [];
  if(node.matches('.cover')){const out=[];[...node.children].forEach((n,i)=>out.push(paragraph(n,i===0?'APATitle':'APACover',i===0?{spacing:{before:1920,after:480,line:480}}:{})));pendingBreak=true;return out;}
  if(node.matches('.page-break')){pendingBreak=true;return [];}
  if(node.matches('.toc')){const out=[];if(pendingBreak){out.push(new Paragraph({pageBreakBefore:true}));pendingBreak=false;}out.push(new Paragraph({style:'APATitle',text:'Índice'}),new TableOfContents('Índice',{hyperlink:true,useAppliedParagraphOutlineLevel:true,stylesWithLevels:Array.from({length:5},(_,i)=>new StyleLevel('APA Nivel '+(i+1),i+1)),beginDirty:true}));warnings.push('Actualiza el índice en Word con clic derecho → Actualizar campo / toda la tabla. Word recalcula sus propias páginas.');return out;}
  if(node.matches('table'))return table(node);
  if(node.matches('ul,ol'))return list(node);
  if(node.matches('.table-wrap,.figure-wrap')){const out=[];for(const child of node.children){if(child.matches('.table-label,.figure-label'))out.push(paragraph(child,'APANumber'));else if(child.matches('.table-title,.figure-title'))out.push(paragraph(child,'APACaption'));else if(child.matches('.table-note,.figure-note')){if(child.textContent.trim())out.push(paragraph(child,'APANote'));}else if(child.matches('.figure-placeholder'))out.push(paragraph(child,'APANoIndent'));else out.push(...blocks(child));}return out;}
  if(node.matches('img'))return [new Paragraph({style:'APANoIndent',alignment:AlignmentType.CENTER,children:runs(node)})];
  if(node.matches('h1,h2,h3,h4,h5'))return [paragraph(node,'APAHeading'+node.tagName.slice(1),(node.dataset.sectionKey==='referencias'||/^referencias$/i.test(node.textContent.trim()))?{pageBreakBefore:true}:{})];
  if(node.matches('blockquote'))return [paragraph(node,'APAQuote')];
  if(node.matches('p')||Object.keys(map).some(k=>node.classList.contains(k)))return [paragraph(node,Object.keys(map).map(k=>node.classList.contains(k)?map[k]:null).find(Boolean)||'APANormal')];
  if([...node.children].some(n=>n.matches('p,div,h1,h2,h3,h4,h5,table,ul,ol,blockquote,figure,img')))return [...node.childNodes].flatMap(blocks);
  return [paragraph(node,'APANormal')];
 }
 const children=[...root.childNodes].flatMap(blocks);
 if(pendingBreak)children.push(new Paragraph({pageBreakBefore:true}));
 const doc=new Document({creator:'Plantilla Maestra APA 7',title,description:'Trabajo editable exportado desde la Plantilla Maestra APA 7. Revisar requisitos institucionales.',features:{updateFields:true},styles:{default:{document:{run:{font:TNR,size:24,language:{value:'es-PE'}},paragraph:{spacing:{line:480,before:0,after:0},indent:{firstLine:720},alignment:AlignmentType.LEFT,widowControl:true}}},paragraphStyles:definitions.map(([id,name,paragraph,run={}])=>({id,name,basedOn:'Normal',next:'APANormal',quickFormat:true,run:{font:TNR,size:24,...run},paragraph:{spacing:{line:480,before:0,after:0},widowControl:true,alignment:AlignmentType.LEFT,...paragraph}}))},numbering:{config:numbering},sections:[{properties:{page:{size:{width:12240,height:15840},margin:{top:1440,bottom:1440,left:1440,right:1440,header:720,footer:720}}},headers:{default:new Header({children:[new Paragraph({alignment:AlignmentType.RIGHT,indent:{firstLine:0},spacing:{before:0,after:0,line:240},children:[new TextRun({font:TNR,size:24,children:[PageNumber.CURRENT]})]})]})},children:children.length?children:[new Paragraph({style:'APANormal'})]}]});
 return {blob:await Packer.toBlob(doc),warnings};
}
