(() => {
  'use strict';
  const $=s=>document.querySelector(s), all=s=>[...document.querySelectorAll(s)];
  const el=(tag,text,cls)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=text;if(cls)n.className=cls;return n;};
  const STORAGE='high-contrast-annotations-v1';
  let notes=[];try{const stored=JSON.parse(localStorage.getItem(STORAGE)||'[]');if(Array.isArray(stored))notes=stored.filter(validNote).slice(-100);}catch{}
  let target=null,busy=false,choosing=false,available=false,unavailable='Start .venv/bin/python tools/proof_explorer/serve.py to enable annotations.',moving=null;
  const pending=new Map(), mounted=new Map();
  let mathQueue=Promise.resolve();
  function typesetAnnotations(nodes=all('.paper-annotation')){
    if(!window.MathJax?.typesetPromise)return;
    mathQueue=mathQueue.then(()=>window.MathJax.startup.promise).then(()=>{
      const connected=nodes.filter(n=>n.isConnected);return connected.length?window.MathJax.typesetPromise(connected):undefined;
    }).then(()=>placeGraphNotes()).catch(()=>{});
  }
  function clearMath(node){if(node)window.MathJax?.typesetClear?.([node]);}
  document.addEventListener('annotation-math-ready',()=>typesetAnnotations());
  document.getElementById('annotation-mathjax')?.addEventListener('load',()=>typesetAnnotations());
  function validNote(n){return n&&typeof n.id==='string'&&/^[\w-]{1,80}$/.test(n.id)&&typeof n.anchor==='string'&&n.anchor.length<500&&typeof n.target==='string'&&typeof n.question==='string'&&n.question.length<=4000&&typeof n.answer==='string'&&n.answer.length<=7000&&typeof n.quote==='string'&&n.quote.length<=2000;}
  function icon(path){return `<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">${path}</svg>`;}
  const gadget=el('aside',undefined,'paper-lens');gadget.setAttribute('aria-label','Ask for an annotation');
  gadget.innerHTML=`<div class="lens-grip" tabindex="0" role="button" aria-label="Move annotation gadget. Arrow keys move; Enter selects the passage underneath." title="Drag onto a passage"></div><form class="lens-form"><textarea aria-label="Question about the selected passage. Enter to annotate; Shift Enter for a new line." maxlength="4000" rows="2" spellcheck="false"></textarea><div class="lens-tools"><button class="lens-pick" type="button" aria-label="Select a passage to annotate" title="Select passage">${icon('<circle cx="12" cy="12" r="5"/><path d="M12 2v4m0 12v4M2 12h4m12 0h4"/>')}</button><button class="lens-send" type="submit" aria-label="Add an annotation" title="Annotate">${icon('<path d="M12 19V5m-5 5 5-5 5 5"/>')}</button></div></form><span class="lens-status sr-only" role="status" aria-live="polite"></span>`;
  document.body.append(gadget);
  const input=gadget.querySelector('textarea'),send=gadget.querySelector('.lens-send'),pick=gadget.querySelector('.lens-pick'),grip=gadget.querySelector('.lens-grip');
  const toast=el('div',undefined,'lens-toast');toast.hidden=true;toast.setAttribute('role','alert');document.body.append(toast);let toastTimer;
  function announce(text,error=false){gadget.querySelector('.lens-status').textContent=text;if(error){toast.textContent=text;toast.hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>toast.hidden=true,10000);}}
  function controls(){send.disabled=busy||!input.value.trim();input.disabled=busy;pick.disabled=busy;gadget.classList.toggle('is-busy',busy);gadget.classList.toggle('has-question',!!input.value.trim());}
  function visible(n){return n&&!n.closest('[hidden]')&&n.getClientRects().length;}
  function cleanText(n){const clone=n.cloneNode(true);clone.querySelectorAll('.paper-annotation,.lens-anchor-mark').forEach(x=>x.remove());return clone.textContent.trim();}
  function fingerprint(text){let hash=2166136261;for(const char of text){hash^=char.charCodeAt(0);hash=Math.imul(hash,16777619);}return (hash>>>0).toString(36);}
  // Keys follow source nodes and paragraph order, never inserted notes or layout coordinates.
  function stamp(){
    const roots=[];
    for(const id of ['intro-question','intro-result','intro-math','intro-history']){const n=$(`[aria-labelledby="${id}"]`);if(n)roots.push([n,id]);}
    for(const [selector,id]of [['.paper-hero>div:first-child','overview'],['#assumptions','assumptions'],['.material-card','material'],['#paper-map','paper-map']]){const n=$(selector);if(n)roots.push([n,id]);}
    const theorem=location.hash.slice(1);
    if(['A','B'].includes(theorem)){
      all('.proof-passage').forEach(n=>roots.push([n,`${theorem}:${n.id.split('-')[1]}`]));
      all('.graph-node').forEach(n=>{n.dataset.lensTarget=`${theorem}:${n.dataset.index}`;n.dataset.lensAnchor=`${theorem}:graph:${n.dataset.node}`;});
      const i=$('#graph-canvas .graph-node.current')?.dataset.index||0;roots.push([$('#node-detail'),`${theorem}:${i}`]);
    }
    for(const [node,id]of roots){if(!node)continue;node.dataset.lensTarget=id;node.dataset.lensAnchor=id+':section';const occurrences=new Map();
      for(const child of node.querySelectorAll('p,h1,h2,h3,.equation,figcaption,dd,.paper-dependency-node')){
        if(child.closest('.paper-annotation'))continue;
        child.dataset.lensTarget=id;const key=child.dataset.paperNode?'map-node:'+child.dataset.paperNode:fingerprint(cleanText(child));const count=occurrences.get(key)||0;occurrences.set(key,count+1);child.dataset.lensAnchor=id+':'+(node.id==='node-detail'?'detail:':'')+key+':'+count;
      }
    }
    mountNotes();outline();
  }
  function findAnchor(key){return all('[data-lens-anchor]').find(n=>n.dataset.lensAnchor===key&&visible(n));}
  function outline(){all('.lens-selected').forEach(n=>n.classList.remove('lens-selected'));if(target){const n=findAnchor(target.anchor);if(n)n.classList.add('lens-selected');}}
  function choose(node,quote=''){
    if(busy||!node)return;
    const anchor=node.closest('[data-lens-anchor]');if(!anchor||anchor.closest('.paper-annotation'))return;
    target={anchor:anchor.dataset.lensAnchor,id:anchor.dataset.lensTarget,quote:quote.slice(0,2000),text:cleanText(anchor).slice(0,18000),view:anchor.classList.contains('graph-node')?($('#state-tab')?.getAttribute('aria-pressed')==='true'?'state graph':'proof graph'):'passage'};
    choosing=false;document.body.classList.remove('lens-selecting');pick.setAttribute('aria-pressed','false');gadget.classList.add('is-targeted');
    gadget.title=quote?'Annotating: '+quote.slice(0,140):'Annotating: '+target.text.slice(0,140);announce('Passage selected. Type a question and press Enter to add a note here.');outline();
  }
  function under(x,y){gadget.style.pointerEvents='none';const n=document.elementsFromPoint(x,y).map(n=>n.closest('[data-lens-anchor]')).find(n=>n&&!n.closest('.paper-annotation'));gadget.style.pointerEvents='';if(n)choose(n);}
  document.addEventListener('pointerup',e=>{if(gadget.contains(e.target)||e.target.closest('.paper-annotation')||moving)return;const selection=window.getSelection();const quote=selection?.toString().trim();if(quote){const common=selection.getRangeAt(0).commonAncestorContainer;const node=common.nodeType===1?common:common.parentElement;choose(node,quote);}},false);
  document.addEventListener('click',e=>{if(gadget.contains(e.target)||e.target.closest('.paper-annotation'))return;const n=e.target.closest('[data-lens-anchor]');if(choosing){e.preventDefault();e.stopImmediatePropagation();if(n)choose(n);input.focus({preventScroll:true});}else if(n&&!busy)choose(n,window.getSelection()?.toString().trim()||'');},true);
  pick.onclick=()=>{choosing=!choosing;pick.setAttribute('aria-pressed',String(choosing));document.body.classList.toggle('lens-selecting',choosing);announce(choosing?'Click the passage where your question arises.':'Selection cancelled.');};
  document.addEventListener('keydown',e=>{if(e.key==='Escape'){choosing=false;document.body.classList.remove('lens-selecting');pick.setAttribute('aria-pressed','false');toast.hidden=true;}});
  function move(x,y){gadget.style.left=Math.max(8,Math.min(x,innerWidth-gadget.offsetWidth-8))+'px';gadget.style.top=Math.max(8,Math.min(y,innerHeight-gadget.offsetHeight-8))+'px';gadget.style.right='auto';gadget.style.bottom='auto';}
  grip.onpointerdown=e=>{if(busy)return;const r=gadget.getBoundingClientRect();moving={x:e.clientX,y:e.clientY,left:r.left,top:r.top};grip.setPointerCapture(e.pointerId);};
  grip.onpointermove=e=>{if(moving)move(moving.left+e.clientX-moving.x,moving.top+e.clientY-moving.y);};
  grip.onpointerup=e=>{if(!moving)return;const changed=Math.hypot(e.clientX-moving.x,e.clientY-moving.y)>5;moving=null;if(changed){const r=gadget.getBoundingClientRect();under(r.left+r.width/2,r.top+12);}};
  grip.onpointercancel=()=>moving=null;
  grip.onkeydown=e=>{const r=gadget.getBoundingClientRect(),d={ArrowLeft:[-24,0],ArrowRight:[24,0],ArrowUp:[0,-24],ArrowDown:[0,24]}[e.key];if(d){e.preventDefault();move(r.left+d[0],r.top+d[1]);}if(e.key==='Enter'){e.preventDefault();under(r.left+r.width/2,r.top+12);input.focus();}};
  window.addEventListener('resize',()=>{const r=gadget.getBoundingClientRect();move(r.left,r.top);placeGraphNotes();});
  function persist(){try{localStorage.setItem(STORAGE,JSON.stringify(notes));return true;}catch{return false;}}
  function remove(id){notes=notes.filter(n=>n.id!==id);pending.delete(id);clearMath(mounted.get(id));mounted.get(id)?.remove();mounted.delete(id);persist();announce('Annotation removed. The original passage is unchanged.');}
  function createNote(note,loading=false){
    const box=el('aside',undefined,'paper-annotation');box.dataset.noteId=note.id;box.setAttribute('aria-label','Annotation: '+note.question);
    const header=el('div',undefined,'annotation-heading');header.append(el('span','✧','annotation-spark'),el('strong',note.question));
    if(!loading){const close=el('button','×','annotation-remove');close.type='button';close.title='Remove annotation';close.setAttribute('aria-label','Remove annotation');close.onclick=()=>remove(note.id);header.append(close);}box.append(header);
    if(note.quote){const quote=el('blockquote',note.quote);box.append(quote);}
    if(loading){const shimmer=el('div',undefined,'annotation-loading');shimmer.setAttribute('role','status');shimmer.setAttribute('aria-label','Preparing annotation');shimmer.append(el('i'),el('i'),el('i'));box.append(shimmer);}
    else {const body=el('div',undefined,'annotation-body');window.AnnotationFormat.render(body,note.answer);box.append(body);}
    return box;
  }
  function mountNotes(){
    for(const [id,box]of mounted)if(!box.isConnected){mounted.delete(id);}
    for(const note of [...notes,...pending.values()]){
      const anchor=findAnchor(note.anchor);if(!anchor)continue;
      let box=mounted.get(note.id);if(box?.isConnected)continue;
      box=createNote(note,pending.has(note.id));mounted.set(note.id,box);
      if(anchor.matches('.graph-node,.paper-dependency-node')){box.classList.add('annotation-on-graph');document.body.append(box);}
      else {let after=anchor;while(after.nextElementSibling?.classList.contains('paper-annotation'))after=after.nextElementSibling;
        if(anchor.dataset.lensAnchor.endsWith(':section'))anchor.append(box);else after.after(box);}
    }
    typesetAnnotations([...mounted.values()].filter(n=>!n.dataset.mathQueued));
    for(const box of mounted.values())box.dataset.mathQueued='true';
    placeGraphNotes();
  }
  function placeGraphNotes(){
    const stacks=new Map();
    for(const note of [...notes,...pending.values()]){const box=mounted.get(note.id);if(!box?.classList.contains('annotation-on-graph'))continue;const anchor=findAnchor(note.anchor);const viewport=anchor?.closest('.graph-scroll,#paper-map-scroll');const r=anchor?.getBoundingClientRect(),v=viewport?.getBoundingClientRect();
      const inView=r&&v&&r.bottom>v.top&&r.top<v.bottom&&r.right>v.left&&r.left<v.right&&r.bottom>0&&r.top<innerHeight;
      box.hidden=!inView;if(!inView)continue;
      const width=Math.min(300,innerWidth-24),offset=stacks.get(note.anchor)||0;
      box.style.width=width+'px';box.style.left=Math.max(12,Math.min(r.right+12,innerWidth-width-12))+'px';box.style.top=Math.max(12,Math.min(r.top+offset,innerHeight-100))+'px';stacks.set(note.anchor,offset+Math.min(box.offsetHeight,260)+12);
    }
  }
  document.addEventListener('scroll',placeGraphNotes,true);
  input.oninput=controls;
  input.onfocus=()=>{if(!target){const r=gadget.getBoundingClientRect();under(r.left+r.width/2,r.top+12);}};
  input.onkeydown=e=>{if(e.key==='Enter'&&!e.shiftKey&&!e.isComposing){e.preventDefault();gadget.querySelector('form').requestSubmit();}};
  gadget.querySelector('form').onsubmit=async e=>{
    e.preventDefault();const question=input.value.trim();if(busy||!question)return;
    if(!available){announce(unavailable,true);return;}
    if(!target){announce('Highlight a passage, drag the glass onto it, or use the target icon first.',true);return;}
    const selected={...target},id=crypto.randomUUID(),note={id,target:selected.id,anchor:selected.anchor,quote:selected.quote,question,answer:''};
    const history=notes.filter(n=>n.anchor===selected.anchor).slice(-4).flatMap(n=>[{role:'user',content:n.question},{role:'assistant',content:n.answer}]);
    busy=true;controls();toast.hidden=true;pending.set(id,note);mountNotes();announce('Preparing an annotation beside the selected passage.');
    const controller=new AbortController(),timeout=setTimeout(()=>controller.abort(),150000);
    try{
      const response=await fetch('/api/paper-assistant',{method:'POST',headers:{'Content-Type':'application/json'},signal:controller.signal,body:JSON.stringify({mode:'annotate',target:selected.id,selected_text:selected.text,selected_quote:selected.quote,question,view:selected.view,history})});
      let result;try{result=await response.json();}catch{throw Error('Start the AI-enabled local preview to add annotations.');}
      if(!response.ok)throw Error(result.error||'The annotation could not be completed.');
      if(result.target!==selected.id||typeof result.answer!=='string'||!result.answer.trim()||result.answer.length>7000)throw Error('The annotation was incomplete. Please retry.');
      note.answer=result.answer;pending.delete(id);clearMath(mounted.get(id));mounted.get(id)?.remove();mounted.delete(id);notes.push(note);notes=notes.slice(-100);const saved=persist();mountNotes();input.value='';announce(saved?'Annotation added beside your passage.':'Annotation added for this visit; browser storage is unavailable.');
    }catch(error){pending.delete(id);clearMath(mounted.get(id));mounted.get(id)?.remove();mounted.delete(id);announce(error.name==='AbortError'?'The annotation timed out. Your question is still here; try again.':error.message,true);}
    finally{clearTimeout(timeout);busy=false;controls();}
  };
  let queued=false;const observer=new MutationObserver(()=>{if(queued)return;queued=true;requestAnimationFrame(()=>{queued=false;stamp();});});
  for(const selector of ['#graph-canvas','#proof-reader','#node-detail','#dependency-map'])observer.observe($(selector),{childList:true});
  window.addEventListener('hashchange',()=>{target=null;gadget.classList.remove('is-targeted');gadget.removeAttribute('title');requestAnimationFrame(stamp);});
  stamp();controls();
  fetch('/api/paper-assistant/status').then(r=>{if(!r.ok)throw Error();return r.json();}).then(s=>{available=!!s.available;unavailable='Add OPENAI_API_KEY to the project .env, then restart the AI preview.';}).catch(()=>{available=false;});
})();
