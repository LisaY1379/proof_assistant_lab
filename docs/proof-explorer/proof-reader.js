(function(root){
  'use strict';
  function create({onSelect,noteBlock}){
    const $=id=>document.getElementById(id),C=root.HansonWrightReaderContent,P=root.HansonWright;
    const panel=$('proof-reader'),body=$('reader-body'),dialog=$('reader-dialog'),anchor=$('reader-anchor');
    let version='original',action='start',branch=null,route=null,articles=[],lastContext='';
    function el(tag,cls,text){const n=document.createElement(tag);if(cls)n.className=cls;if(text!==undefined)n.textContent=text;return n;}
    function button(text,fn,cls){const n=el('button',cls,text);n.type='button';n.addEventListener('click',fn);return n;}
    function paragraph(parent,title,text){const section=el('section','reader-explanation');section.append(el('h4','',title),el('p','',text));parent.append(section);return section;}
    function expansion(parent,items){for(const block of items){const section=paragraph(parent,block.title,block.text);if(block.math)section.append(el('div','proof-equation reader-math',block.math));}}
    function showAction(id){action=id;highlight(false);onSelect(id);}
    function article(p,index){
      const part=el('article','reader-passage');part.dataset.readerPassage=p.id;part.dataset.events=p.events.join(' ');
      part.dataset.unresolvedEvents=version==='detailed'?p.explanations.filter(e=>e.ablation.status!=='worked').map(e=>e.action.id).join(' '):'';
      const literatureAssisted=version==='detailed'&&p.explanations.some(e=>e.ablation.source);
      part.classList.toggle('reader-literature-assisted',literatureAssisted);
      const heading=el('header','reader-passage-heading');heading.append(el('span','reader-number',String(index+1)),el('h3','',p.title));
      for(const id of p.events)heading.append(button(id==='start'?'Show assumptions':`Show ${id}`,()=>showAction(id),'reader-step-link'));
      part.append(heading);
      if(part.dataset.unresolvedEvents)part.append(el('span','reader-unresolved-badge','No valid alternative established · ablation unresolved'));
      if(literatureAssisted)part.append(el('span','reader-literature-badge','Alternative obtained from online research'));
      if(p.critical)part.append(el('span','reader-key-badge',C.selection.selectionLabel));
      const proof=el('div','reader-original');proof.innerHTML=p.html;part.append(proof); // Trusted, repository-authored original proof.
      part.addEventListener('click',event=>{
        if(event.target.closest('button,a,summary,details')||window.getSelection()?.toString())return;
        showAction(p.events.includes(action)?action:p.events[0]);
      });
      for(const e of p.explanations){
        const section=el('section','reader-step-explanation');section.dataset.explainedAction=e.action.id;
        if(p.events.length>1)section.append(el('h4','',e.action.title));
        if(version==='focused'){
          paragraph(section,'Why this step was selected',C.selection.rationale);
          expansion(section,e.expansion);
          paragraph(section,'An alternative to this key step',C.selection.alternativeNote);
          paragraph(section,'Cost and scope',e.cost);
        }else{
          paragraph(section,'What we have; what we need',e.action.have+'\n'+e.action.need);
          paragraph(section,'Why this move helps',e.action.observation);
          const calculation=paragraph(section,'Derivation and checks',e.action.check);calculation.prepend(el('div','proof-equation reader-math',e.action.math));
          if(e.expansion.length)expansion(section,e.expansion);
          paragraph(section,'Tools and assumptions',e.action.tool);
          const alternatives=el('details','reader-alternatives');alternatives.dataset.ablatedAction=e.action.id;alternatives.append(el('summary','',`If this step is removed: ${e.action.id} · ${e.ablation.status==='unresolved'?'sharp closure unresolved':'worked replacement'}`));
          paragraph(alternatives,'What is forbidden',e.ablation.restriction);
          paragraph(alternatives,e.ablation.title,e.ablation.status==='unresolved'?'The supplied route does not establish the target bound.':'This replacement works under the stated ban; it may change earlier proof obligations.');
          if(e.ablation.source){
            const attribution=paragraph(alternatives,'Where this alternative came from',e.ablation.provenance);
            const citation=el('a','',e.ablation.source.title);citation.href=e.ablation.source.url;attribution.append(citation);
            paragraph(alternatives,'How the replacement works',e.ablation.interpretation);
          }
          const chain=el('ol','reader-route-steps');for(const step of e.ablation.steps){const li=el('li');li.append(el('strong','',step.title),el('p','',step.have));chain.append(li);}alternatives.append(chain);
          for(const extra of e.ablation.additional||[]){const d=el('details');d.append(el('summary','',extra.title));for(const step of extra.steps)paragraph(d,step.title,step.have);alternatives.append(d);}
          for(const candidate of e.ablation.candidates)paragraph(alternatives,`${candidate.title} · ${candidate.status}`,candidate.reason);
          alternatives.append(noteBlock(e.action.id,'Full replacement proof and ablation analysis'),noteBlock('common','Shared calculations and boundary cases'));
          if(e.action.id!=='sign')alternatives.append(noteBlock('sign','Complete moment proof used by the shared route'));
          section.append(alternatives);
          paragraph(section,'Mathematical work and tradeoffs',e.cost);

        }
        part.append(section);
      }
      return part;
    }
    function highlight(scroll=true){
      let active=null;
      for(const explanation of body.querySelectorAll('[data-explained-action]'))explanation.classList.toggle('reader-explanation-active',explanation.dataset.explainedAction===action);
      for(const part of articles){const selected=part.dataset.events.split(' ').includes(action);part.classList.toggle('reader-active',selected);part.classList.toggle('reader-no-alternative',selected&&part.dataset.unresolvedEvents.split(' ').includes(action));if(selected){part.setAttribute('aria-current','step');active=part;}else part.removeAttribute('aria-current');}
      $('reader-position').textContent=route?`${route.title} · alternative route`:`${P.byId[action]?.title||'Notation and assumptions'} · original route`;
      if(active&&scroll&&$('reader-follow').checked){const a=active.getBoundingClientRect(),b=body.getBoundingClientRect();body.scrollTo({top:body.scrollTop+a.top-b.top-18,behavior:'instant'});}
    }
    function renderRoute(){
      const intro=el('section','reader-route-intro');intro.append(el('h3','',route.title),el('p','',route.scope||'Read this alternative independently of the reference route.'),el('p','reader-cost',route.status==='unresolved'?'Incomplete alternative: the sharp target remains unresolved.':'Worked alternative proof.'));
      if(route.restriction)intro.append(el('p','',route.restriction));body.append(intro);
      for(const [i,step] of route.steps.entries()){
        const part=el('article','reader-passage');part.dataset.events=route.action;
        part.append(el('h3','',`${i+1}. ${step.title}`),el('p','',step.have),el('p','reader-route-want',step.want));body.append(part);
      }
      const full=noteBlock(route.action,'Full written argument and alternatives');full.open=true;body.append(full,noteBlock('common','Shared calculations and boundary cases'));
      if(route.action!=='sign')body.append(noteBlock('sign','Complete absolute-moment proof where used'));
    }
    function render(){
      body.setAttribute('aria-labelledby',route?'reader-position':'reader-tab-'+version);
      for(const tab of document.querySelectorAll('[data-reader-version]')){const active=tab.dataset.readerVersion===version;tab.setAttribute('aria-selected',String(active));tab.tabIndex=active?0:-1;}
      $('reader-tabs').hidden=!!route;
      $('reader-return').hidden=!route;
      $('reader-edition-note').textContent=route?'Alternative reading · the original proof is preserved. Return to compare the three original-proof editions.':version==='original'?'The complete written proof from the original explorer.':version==='detailed'?'The same argument, with motivations, derivations, alternative methods and mathematical tradeoffs at each step. Yellow marks an alternative obtained from online research; its source is linked in the alternative notes.':C.selection.selectionLabel+': '+C.selection.selectedActionIds.join(', ')+'.';
      $('reader-selection').hidden=version!=='focused'||!!route;
      $('reader-selection-text').textContent=C.selection.provenance+' '+C.selection.rationale;
      body.replaceChildren();articles=[];
      if(route)renderRoute();else C.build(version).forEach((p,i)=>{const part=article(p,i);articles.push(part);body.append(part);});
      highlight();
    }
    function offerBranch(){
      $('reader-route-offer').hidden=!branch;
      $('reader-route-label').textContent=branch?`${branch.title} · ${branch.status==='unresolved'?'incomplete alternative':'worked alternative'}`:'';
    }
    for(const tab of document.querySelectorAll('[data-reader-version]')){
      tab.addEventListener('click',()=>{version=tab.dataset.readerVersion;render();});
      tab.addEventListener('keydown',event=>{
        const tabs=[...document.querySelectorAll('[data-reader-version]')],index=tabs.indexOf(tab);
        const next=event.key==='ArrowRight'?(index+1)%tabs.length:event.key==='ArrowLeft'?(index+tabs.length-1)%tabs.length:event.key==='Home'?0:event.key==='End'?tabs.length-1:null;
        if(next===null)return;event.preventDefault();tabs[next].focus();tabs[next].click();
      });
    }
    $('reader-follow').addEventListener('change',()=>highlight());
    $('reader-read-route').addEventListener('click',()=>{if(!branch)return;route=JSON.parse(JSON.stringify(branch));render();body.scrollTop=0;});
    $('reader-return').addEventListener('click',()=>{route=null;render();});
    $('reader-expand').addEventListener('click',()=>{
      if(dialog.open){dialog.close();return;}
      $('reader-disclosure').open=true;dialog.append(panel);dialog.showModal();$('reader-expand').textContent='Return to graphs';highlight();
    });
    dialog.addEventListener('close',()=>{anchor.after(panel);$('reader-expand').textContent='Expand reading view';$('reader-expand').focus();});
    $('reader-jump').addEventListener('click',()=>{if(dialog.open)dialog.close();onSelect(action,true);});
    render();
    return {update(context){
      const nextAction=context.action||'start';branch=context.branch||null;offerBranch();
      const key=nextAction+'|'+(branch?.action||'')+'|'+(branch?.title||'');
      if(key!==lastContext){lastContext=key;action=nextAction;highlight();}
    }};
  }
  root.HansonWrightProofReader={create};
})(window);
