/* Solo preferencia decorativa: nunca lee ni modifica documentos académicos. */
(()=>{
 const key='pma7-decorative-motion',root=document.documentElement,media=matchMedia('(prefers-reduced-motion: reduce)');
 let paused=false;try{paused=localStorage.getItem(key)==='paused'}catch(e){}
 function apply(){const reduced=media.matches;root.dataset.decorativeMotion=(paused||reduced)?'paused':'running';document.querySelectorAll('[data-motion-toggle]').forEach(b=>{b.hidden=false;b.disabled=reduced;b.setAttribute('aria-pressed',String(paused||reduced));b.textContent=reduced?'Movimiento reducido':paused?'Activar animación':'Pausar animación';b.setAttribute('aria-label',b.textContent);b.title=reduced?'Se respeta la preferencia de accesibilidad de tu dispositivo.':'Solo cambia el movimiento decorativo.'})}
 document.querySelectorAll('[data-motion-toggle]').forEach(b=>b.addEventListener('click',()=>{paused=!paused;try{localStorage.setItem(key,paused?'paused':'running')}catch(e){}apply()}));
 media.addEventListener('change',apply);window.addEventListener('storage',e=>{if(e.key===key){paused=e.newValue==='paused';apply()}});apply();
})();
