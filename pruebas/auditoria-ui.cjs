const {chromium}=require('playwright');const {default:AxeBuilder}=require('@axe-core/playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:1440,height:1040}});const p=await ctx.newPage();let errors=[];p.on('pageerror',e=>errors.push(e.message));p.on('console',m=>{if(m.type()==='error')console.log('CONSOLE',m.text().slice(0,160))});let reports=[];
await p.goto('http://localhost:3000');
async function audit(name){const a=await new AxeBuilder({page:p}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();reports.push({name,violations:a.violations});console.log(name,a.violations.map(v=>[v.id,v.impact,v.nodes.map(n=>n.target)]));}
await audit('Inicio');await p.screenshot({path:'pruebas/inicio.png',fullPage:true});
await p.evaluate(()=>openNewDocWizard());await audit('Asistente');await p.evaluate(()=>closeModal('wizardModal'));
await p.evaluate(()=>loadDoc({id:uid(),name:'Mi trabajo académico',html:'<h1>Introducción</h1><p class="apa-normal">La investigación parte de una pregunta. Escribe aquí tus ideas y utiliza los estilos APA para darles una estructura clara.</p><h2>Propósito del trabajo</h2><p class="apa-normal">El editor te acompaña con herramientas de formato, citas y referencias. Cada paso se conserva en tu dispositivo.</p>',refs:[]}));
await audit('Editor');await p.screenshot({path:'pruebas/editor.png'});
await p.evaluate(()=>exportMenu());await audit('Exportación Word');await p.screenshot({path:'pruebas/word-menu.png'});await p.evaluate(()=>closeModal('dialogModal'));
await p.evaluate(()=>openReferenceManager());await audit('Referencias');await p.evaluate(()=>closeModal('refModal'));
await p.evaluate(()=>openGuide());await audit('Guía');await p.evaluate(()=>closeModal('guideModal'));
await p.setViewportSize({width:390,height:844});await p.evaluate(()=>showHome());await audit('Inicio móvil');await p.screenshot({path:'pruebas/inicio-movil.png',fullPage:true});
fs.writeFileSync('pruebas/accesibilidad.json',JSON.stringify({reports,errors},null,2));await b.close();if(reports.some(r=>r.violations.length)||errors.length)process.exitCode=1})();
