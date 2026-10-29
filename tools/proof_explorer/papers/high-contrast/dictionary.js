/* Local glossary: no model requests and no changes to the paper's prose. */
(()=>{
  'use strict';
  const {entries,lookup,search}=window.PaperDictionary;
  const el=(tag,text,cls)=>{const n=document.createElement(tag);if(text)n.textContent=text;if(cls)n.className=cls;return n;};
  const trigger=el('button','Dictionary','dictionary-trigger');trigger.type='button';trigger.setAttribute('aria-expanded','false');trigger.setAttribute('aria-controls','paper-dictionary');
  document.querySelector('.paper-nav').append(trigger);
  const panel=el('aside',null,'dictionary-panel');panel.id='paper-dictionary';panel.hidden=true;panel.setAttribute('aria-label','Paper dictionary');
  const header=el('div',null,'dictionary-panel-header'),row=el('div',null,'dictionary-title-row'),close=el('button','×','dictionary-close');close.setAttribute('aria-label','Close dictionary');
  row.append(el('h2','Paper dictionary'),close);header.append(row,el('p','Select or hover over an underlined term.','dictionary-hint'));
  const input=el('input');input.type='search';input.placeholder='Find a term…';input.setAttribute('aria-label','Search dictionary');
  const count=el('p',null,'dictionary-count');count.setAttribute('role','status');header.append(input,count);
  const list=el('div');panel.append(header,list);document.body.append(panel);
  const pop=el('section',null,'dictionary-popover');pop.hidden=true;pop.setAttribute('role','dialog');pop.setAttribute('aria-label','Term explanation');document.body.append(pop);
  let anchor=null,hoverTimer,hideTimer,queue=Promise.resolve(),lastFocus=null;
  function typeset(node){if(!window.MathJax?.typesetPromise)return;queue=queue.catch(()=>{}).then(()=>MathJax.startup.promise).then(()=>{if(node.isConnected)return MathJax.typesetPromise([node]);}).catch(()=>{});}
  document.addEventListener('annotation-math-ready',()=>{typeset(panel);typeset(pop);});
  function clear(node){window.MathJax?.typesetClear?.([node]);node.replaceChildren();}
  function content(entry){
    const body=el('div',null,'dictionary-copy');
    for(const [label,text] of [['The question behind it',entry.context],['Meaning',entry.definition]])body.append(el('span',label,'dictionary-label'),el('p',text));
    const equation=el('div','\\['+entry.formula+'\\]','dictionary-equation');body.append(equation,el('span','Where it is used','dictionary-label'),el('p',entry.usage));
    const source=el('a',entry.reference+' ↗');source.href='https://arxiv.org/pdf/2609.27647v1#page='+entry.page;source.target='_blank';source.rel='noopener';body.append(source);return body;
  }
  function renderList(){
    clear(list);const found=search(input.value);count.textContent=found.length+' of '+entries.length+' terms';
    for(const entry of found){const details=el('details',null,'dictionary-entry');details.id='dictionary-'+entry.id;details.append(el('summary',entry.term),content(entry));details.addEventListener('toggle',()=>{if(details.open)typeset(details);});list.append(details);}
    if(!found.length)list.append(el('p','No matching terms. Try “contrast” or “scale”.','dictionary-hint'));
  }
  function hidePop(){clearTimeout(hoverTimer);clearTimeout(hideTimer);pop.hidden=true;anchor=null;}
  function openPanel(id){lastFocus=document.activeElement;hidePop();panel.hidden=false;trigger.setAttribute('aria-expanded','true');input.value='';renderList();if(id){const detail=document.getElementById('dictionary-'+id);detail.open=true;detail.querySelector('summary').focus();detail.scrollIntoView({block:'nearest'});typeset(detail);}else input.focus();}
  function closePanel(){panel.hidden=true;trigger.setAttribute('aria-expanded','false');(lastFocus?.isConnected?lastFocus:trigger).focus();}
  trigger.onclick=()=>panel.hidden?openPanel():closePanel();close.onclick=closePanel;input.oninput=renderList;
  function position(){if(pop.hidden||!anchor)return;const r=anchor.getBoundingClientRect();if(r.bottom<0||r.top>innerHeight){hidePop();return;}const w=pop.offsetWidth,h=pop.offsetHeight;let x=r.right+12,y=r.top;if(x+w>innerWidth-12){if(r.left-w-12>=12)x=r.left-w-12;else{x=Math.max(12,Math.min(innerWidth-w-12,r.left));y=r.bottom+10;if(y+h>innerHeight-12)y=r.top-h-10;}}pop.style.left=Math.max(12,Math.min(innerWidth-w-12,x))+'px';pop.style.top=Math.max(12,Math.min(innerHeight-h-12,y))+'px';}
  function show(entry,reference,focus=false){
    clearTimeout(hideTimer);anchor=reference;clear(pop);
    const top=el('div',null,'dictionary-title-row'),dismiss=el('button','×','dictionary-close');dismiss.setAttribute('aria-label','Close term explanation');dismiss.onclick=()=>{hidePop();if(reference instanceof HTMLElement)reference.focus();};top.append(el('h3',entry.term),dismiss);
    const browse=el('button','Browse all '+entries.length+' terms →','dictionary-browse');browse.onclick=()=>openPanel(entry.id);
    pop.append(top,content(entry),browse);pop.hidden=false;position();typeset(pop);queue.then(position);if(focus)dismiss.focus();
  }
  const escape=text=>text.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
  const aliases=entries.flatMap(e=>e.aliases).sort((a,b)=>b.length-a.length);
  const pattern=new RegExp('(?<![\\p{L}\\p{N}_])('+aliases.map(escape).join('|')+')(?![\\p{L}\\p{N}_])','giu');
  function markTerms(){
    const walker=document.createTreeWalker(document.querySelector('main'),NodeFilter.SHOW_TEXT,{acceptNode(n){return n.parentElement.closest('.dictionary-term,.paper-annotation,script,style,button,a,svg,mjx-container,textarea,input,label,summary,[role="button"],.equation,.annotation-equation,h1,h2,h3,h4')?NodeFilter.FILTER_REJECT:NodeFilter.FILTER_ACCEPT;}});
    const nodes=[];while(walker.nextNode())nodes.push(walker.currentNode);
    for(const n of nodes){const text=n.textContent;pattern.lastIndex=0;const matches=[...text.matchAll(pattern)];if(!matches.length)continue;const fragment=document.createDocumentFragment();let start=0;
      for(const match of matches){fragment.append(document.createTextNode(text.slice(start,match.index)));const term=el('span',match[0],'dictionary-term');term.tabIndex=0;term.setAttribute('role','button');term.setAttribute('aria-label','Define '+match[0]);term.setAttribute('aria-haspopup','dialog');term.dataset.dictionary=lookup(match[0]).id;fragment.append(term);start=match.index+match[0].length;}
      fragment.append(document.createTextNode(text.slice(start)));n.replaceWith(fragment);
    }
  }
  const termFor=event=>event.target.closest?.('.dictionary-term');
  document.addEventListener('pointerover',event=>{const term=termFor(event);if(!term||event.buttons||event.pointerType==='touch')return;clearTimeout(hideTimer);clearTimeout(hoverTimer);hoverTimer=setTimeout(()=>show(entries.find(e=>e.id===term.dataset.dictionary),term),350);});
  document.addEventListener('pointerout',event=>{if(!termFor(event))return;clearTimeout(hoverTimer);hideTimer=setTimeout(()=>{if(!pop.matches(':hover')&&!pop.contains(document.activeElement))hidePop();},280);});
  pop.addEventListener('pointerenter',()=>clearTimeout(hideTimer));pop.addEventListener('pointerleave',()=>{hideTimer=setTimeout(()=>{if(!pop.contains(document.activeElement))hidePop();},280);});
  document.addEventListener('pointerdown',()=>clearTimeout(hoverTimer));
  document.addEventListener('pointerup',event=>{if(panel.contains(event.target)||pop.contains(event.target)||event.target.closest('.paper-lens'))return;const selection=getSelection(),text=selection?.toString().trim();if(!text||!selection.rangeCount)return;const range=selection.getRangeAt(0);if(!document.querySelector('main').contains(range.commonAncestorContainer))return;const entry=lookup(text);if(entry)show(entry,range.cloneRange());});
  document.addEventListener('click',event=>{const term=termFor(event);if(term)show(entries.find(e=>e.id===term.dataset.dictionary),term);else if(!term&&!pop.contains(event.target)&&!lookup(getSelection()?.toString()||''))hidePop();});
  document.addEventListener('keydown',event=>{const term=termFor(event);if(term&&(event.key==='Enter'||event.key===' ')){event.preventDefault();show(entries.find(e=>e.id===term.dataset.dictionary),term,true);}if(event.key==='Escape'){if(!pop.hidden){const old=anchor;hidePop();if(old instanceof HTMLElement)old.focus();}else if(!panel.hidden)closePanel();}});
  window.addEventListener('scroll',position,true);window.addEventListener('resize',position);window.addEventListener('hashchange',()=>{hidePop();const selection=getSelection();if(selection?.anchorNode&&document.querySelector('main').contains(selection.anchorNode))selection.removeAllRanges();});
  let scheduled=false;new MutationObserver(()=>{if(scheduled)return;scheduled=true;requestAnimationFrame(()=>{scheduled=false;markTerms();});}).observe(document.querySelector('main'),{subtree:true,childList:true});
  markTerms();renderList();
})();
