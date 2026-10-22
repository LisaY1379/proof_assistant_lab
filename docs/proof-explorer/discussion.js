(() => {
  'use strict';
  const assets = new URL('.', document.currentScript.src);
  const $ = id => document.getElementById(id);
  const labels = {invalid_step:'Invalid step identified', insufficient:'Does not reach the target', additional_work:'Additional work required', successful_alternative:'Successful alternative', unresolved:'Unresolved'};
  const coverageLabels = {alternatives:'Plausible alternatives', obstacles:'Concrete obstacles', motivation:'Motivation for the move', obligations:'New proof obligations', justification:'Mathematical justification', tradeoffs:'Tradeoffs and dependencies'};
  const backgrounds = {
    undergraduate:'Senior undergraduate: linear algebra, conditional expectation, independence, Markov inequality, and elementary MGFs. Advanced concentration results need statements and hypothesis checks.',
    graduate:'Beginning graduate student: probability, subgaussian norms, Bernstein inequality, and SVD. Decoupling and Gaussian replacement still need explanation.'
  };
  let contexts=[], listings=[], loaded=new Map(), currentRun=null, selectedId='', activeId=null, available=false, local=false, loadVersion=0;
  let mathQueue=Promise.resolve();
  function typeset() {
    if(!window.MathJax?.startup?.promise)return Promise.resolve();
    mathQueue=mathQueue.then(()=>window.MathJax.startup.promise).then(()=>{
      const targets=[...document.querySelectorAll('.discussion-view:not([hidden]) p, .route-card p')];
      return window.MathJax.typesetPromise(targets);
    }).catch(()=>{}); // Keep readable source if offline or a formula is unsupported.
    return mathQueue;
  }
  function el(tag, text, className) { const n=document.createElement(tag); if(text!==undefined)n.textContent=text; if(className)n.className=className; return n; }
  async function json(url, options) {
    const response=await fetch(url, options);
    if(!response.ok){let message=`Could not load the discussion (${response.status}).`;try{message=(await response.json()).error||message;}catch{}throw new Error(message);}
    return response.json();
  }
  const context=()=>contexts.find(c=>c.id===$('step-select').value);
  function message(parent, title, body) { const box=el('div',undefined,'empty-discussion');box.append(el('h3',title),el('p',body));parent.append(box); }
  function tab(name, focus=false) {
    for(const key of ['explanation','dialogue','coverage']){const selected=key===name;$('tab-'+key).setAttribute('aria-selected',String(selected));$('tab-'+key).tabIndex=selected?0:-1;$('view-'+key).hidden=!selected;}
    if(focus)$('tab-'+name).focus();
    return typeset();
  }
  async function showTurn(id) {
    await tab('dialogue');
    document.querySelectorAll('.dialogue-turn.highlighted').forEach(n=>n.classList.remove('highlighted'));
    const turn=$('dialogue-'+id);
    if(turn){turn.classList.add('highlighted');turn.scrollIntoView({block:'start',behavior:'instant'});turn.tabIndex=-1;turn.focus({preventScroll:true});}
  }
  function evidence(refs) {
    const box=el('div',undefined,'evidence-links');
    for(const ref of refs||[]){const b=el('button',`Read evidence · ${ref.turn}`);b.title=ref.quote;b.addEventListener('click',()=>showTurn(ref.turn));box.append(b);}
    return box;
  }
  function routes() {
    const c=currentRun?.context||context();if(!c)return;
    $('state-facts').textContent=c.state.facts;$('state-goal').textContent=c.state.goal;
    $('state-assumptions').hidden=!c.state.assumptions;
    $('state-assumptions-text').textContent=[c.state.assumptions,c.state.notation,c.state.scope].filter(Boolean).join('\n\n');
    const list=$('routes');list.replaceChildren();
    const main=el('article',undefined,'route-card main-route');
    main.append(el('span','Displayed proof route','route-outcome'),el('h3',c.title),el('p',c.chosen.move));
    const details=el('details');details.append(el('summary','The move and its justification'),el('p',c.chosen.mathematics),el('p',c.chosen.justification),el('p','Toolkit: '+c.chosen.toolkit));main.append(details);list.append(main);
    for(const route of currentRun?.summary?.alternatives||[]){
      const card=el('article',undefined,`route-card ${route.status}`);
      card.append(el('span',labels[route.status]||'Unresolved','route-outcome'),el('h3',route.title),el('p',route.motivation));
      const d=el('details');d.open=true;d.append(el('summary','What happens if we try it?'),el('p',route.assessment),el('p','Tradeoff: '+route.cost),evidence(route.evidence));card.append(d);list.append(card);
    }
    if(!currentRun?.summary)list.append(el('p','Alternative branches appear after a recorded discussion has been summarized.','graph-caption'));
  }
  function render() {
    window.MathJax?.typesetClear?.([$('routes'),$('view-explanation'),$('view-dialogue'),$('view-coverage')]);
    const scrollPositions=Object.fromEntries(['explanation','dialogue','coverage'].map(id=>[id,$('view-'+id).scrollTop]));
    routes();
    const run=currentRun;
    $('export').disabled=!run;
    $('run-meta').textContent=run?`${run.audience==='graduate'?'Beginning graduate':'Senior undergraduate'} · ${run.model} · ${new Date(run.created_at).toLocaleString()} · Recorded AI exchange`:'';
    $('run-status').textContent=run?.stage||'';
    for(const id of ['explanation','dialogue','coverage'])$('view-'+id).replaceChildren();
    if(!run){message($('view-explanation'),'A question worth asking','Select a recording, or start a local discussion. The student’s suggestions and the professor’s answers will be preserved here.');message($('view-dialogue'),'No dialogue recorded','No conversation is invented to fill this space.');}
    else {
      if(run.summary){
        if(run.summary_origin==='reviewed')$('view-explanation').append(el('p','Reviewed summary · The original generated summary and unedited dialogue are preserved in the full recording.','run-meta'));
        if(run.review_notes?.length){const note=el('details',undefined,'review-notes');note.append(el('summary',`Reviewer clarifications · ${run.review_notes.length} notes`));for(const text of run.review_notes)note.append(el('p',text));$('view-explanation').append(note);}
        for(const section of run.summary.explanation){const article=el('article',undefined,'explanation-section');article.append(el('h3',section.title),el('p',section.text),evidence(section.evidence));$('view-explanation').append(article);}
      }else message($('view-explanation'),run.status==='error'?'The discussion needs another attempt':'The explanation is not ready',run.error||'The dialogue is preserved as each response arrives. A summary appears after the student’s questions have been considered.');
      for(const turn of run.turns.filter(t=>t.role!=='editor')){
        const article=el('article',undefined,`dialogue-turn ${turn.role}`);article.id='dialogue-'+turn.id;
        const header=el('header');header.append(el('strong',turn.role==='student'?'Student':'Professor'),el('span',`${turn.id} · ${turn.elapsed_seconds}s`));
        article.append(header,el('p',turn.text));
        const raw=el('details');raw.append(el('summary','Verbatim model response'),el('pre',turn.raw));article.append(raw);$('view-dialogue').append(article);
      }
      if(!run.turns.length)message($('view-dialogue'),run.status==='error'?'No response was produced':'The student is considering the state',run.error||'The first recorded response will appear here.');
    }
    const coverage=$('view-coverage');coverage.append(el('h3','Did the explanation address the questions?'));
    coverage.append(el('p','Coverage is the simulated student’s assessment, not an independent mathematical check.'));
    const list=el('ul',undefined,'coverage-list');
    for(const [key,label] of Object.entries(coverageLabels)){const status=run?.coverage?.[key];const li=el('li');li.append(el('span',label),el('span',status==='covered'?'Addressed':status==='open'?'Still open':'Not assessed',status||''));list.append(li);}coverage.append(list);
    const remaining=[...new Set([...(run?.unresolved||[]),...(run?.summary?.unresolved||[])])];
    if(remaining.length){coverage.append(el('h3','Questions still open'));const ul=el('ul');remaining.forEach(q=>ul.append(el('li',q)));coverage.append(ul);}
    if(run?.stop_reason)coverage.append(el('p',run.stop_reason==='coverage_complete'?'The student reported coverage after at least two professor responses.':run.stop_reason==='round_limit'?'The round limit was reached. Unresolved issues remain visible.':`Discussion stopped: ${run.stop_reason}.`));
    coverage.append(el('h3','Sources available to the professor'));
    for(const source of run?.sources||[]){const box=el('div',undefined,'source-card');const url=new URL(source.url,location.href);if(['https:','http:'].includes(url.protocol)){const a=el('a',source.title);a.href=url.href;a.target='_blank';a.rel='noopener noreferrer';box.append(a);}else box.append(el('strong',source.title));box.append(el('p','Supplied project notes. This is not evidence of the original author’s motivation.'));const d=el('details');d.append(el('summary','Exact supplied excerpt'),el('p',source.excerpt));box.append(d);coverage.append(box);}
    if(run?.elapsed_seconds!==undefined)coverage.append(el('p',`Discussion elapsed time: ${run.elapsed_seconds}s. This is not a measure of mathematical difficulty or proof-search cost.`));
    for(const [id,top] of Object.entries(scrollPositions))$('view-'+id).scrollTop=top;
    typeset();
  }
  function controls() {
    $('generate').disabled=!available||!!activeId;
    $('cancel').hidden=!activeId;
    $('background-description').textContent=backgrounds[$('audience').value];
  }
  function refreshOptions() {
    const select=$('recording-select');select.replaceChildren();
    const matches=listings.filter(r=>r.step_id===context()?.id);
    select.append(new Option(matches.length?'Choose a recording':'No recording for this step',''));
    for(const r of matches)select.append(new Option(`${new Date(r.created_at).toLocaleString()} · ${r.audience==='graduate'?'Graduate':'Undergraduate'} · ${r.status}`,r.id));
    select.value=selectedId;
  }
  async function selectRecording(id) {
    const version=++loadVersion;selectedId=id;currentRun=null;refreshOptions();render();
    if(!id)return;
    try{
      const listing=listings.find(r=>r.id===id);
      let run=loaded.get(id);
      if(!run)run=await json(listing.file?new URL(listing.file,assets):`/api/discussions/${id}`);
      loaded.set(id,run);
      if(version!==loadVersion)return;
      currentRun=run;render();
    }catch(error){if(version===loadVersion)$('run-status').textContent=error.message;}
  }
  function updateListing(run) {
    const item={id:run.id,step_id:run.step_id,audience:run.audience,created_at:run.created_at,status:run.status};
    listings=[item,...listings.filter(r=>r.id!==run.id)];loaded.set(run.id,run);refreshOptions();
  }
  async function poll(id) {
    try{
      const run=await json(`/api/discussions/${id}`);updateListing(run);
      if(selectedId===id){
        const changed=currentRun?.turns.length!==run.turns.length||currentRun?.status!==run.status||JSON.stringify(currentRun?.coverage)!==JSON.stringify(run.coverage);
        currentRun=run;
        if(changed)render();else $('run-status').textContent=run.stage;
      }
      if(['queued','running'].includes(run.status))setTimeout(()=>poll(id),1800);
      else {activeId=null;controls();$('service-status').textContent=run.status==='complete'?'Discussion saved locally. Download the recording to keep or share the full exchange.':run.error||run.stage;}
    }catch(error){$('service-status').textContent='Connection interrupted. The server may still be running the discussion. Reload to reconnect. '+error.message;}
  }
  $('generate').addEventListener('click',async()=>{
    $('generate').disabled=true;
    try{
      const run=await json('/api/discussions',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({step_id:context().id,audience:$('audience').value,max_rounds:Number($('rounds').value)})});
      ++loadVersion;activeId=run.id;selectedId=run.id;currentRun=run;updateListing(run);controls();render();tab('dialogue');$('service-status').textContent='Discussion running. You can inspect other steps while it continues.';poll(run.id);
    }catch(error){$('service-status').textContent=error.message;controls();}
  });
  $('cancel').addEventListener('click',async()=>{try{const result=await json(`/api/discussions/${activeId}/cancel`,{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'});$('service-status').textContent=result.message;}catch(error){$('service-status').textContent=error.message;}});
  $('step-select').addEventListener('change',()=>{const url=new URL(location.href);url.searchParams.set('step',context().id);history.replaceState(null,'',url);selectedId='';refreshOptions();selectRecording(listings.find(r=>r.step_id===context().id)?.id||'');});
  $('recording-select').addEventListener('change',()=>selectRecording($('recording-select').value));
  $('audience').addEventListener('change',controls);
  const tabs=['explanation','dialogue','coverage'];
  tabs.forEach((name,index)=>{const button=$('tab-'+name);button.addEventListener('click',()=>tab(name));button.addEventListener('keydown',event=>{if(['ArrowLeft','ArrowRight','Home','End'].includes(event.key)){event.preventDefault();const next=event.key==='Home'?0:event.key==='End'?2:(index+(event.key==='ArrowRight'?1:2))%3;tab(tabs[next],true);}});});
  $('export').addEventListener('click',()=>{if(!currentRun)return;const url=URL.createObjectURL(new Blob([JSON.stringify(currentRun,null,2)+'\n'],{type:'application/json'}));const a=el('a');a.href=url;a.download=`discussion-${currentRun.step_id}-${currentRun.id}.json`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
  async function init() {
    try{
      contexts=await json(new URL('discussion-contexts.json',assets));
      for(const [i,c] of contexts.entries())$('step-select').append(new Option(`${String(i+1).padStart(2,'0')} · ${c.title}`,c.id));
      const requested=new URL(location.href).searchParams.get('step');$('step-select').value=contexts.some(c=>c.id===requested)?requested:'decouple';
      const manifest=await json(new URL('recordings/manifest.json',assets));listings=manifest.recordings||[];
      if(['127.0.0.1','localhost'].includes(location.hostname)){
        try{const status=await json('/api/discussions/status');local=true;available=status.available;activeId=status.active;const saved=await json('/api/discussions');listings=[...listings,...saved.filter(s=>!listings.some(r=>s.id===r.id))];listings.sort((a,b)=>b.created_at.localeCompare(a.created_at));$('service-status').textContent=available?`Local discussion runner connected · ${status.model}. Each discussion makes 6–8 model calls within the selected round limit.`:'Local runner connected. Configure OPENAI_API_KEY in the project .env to generate a discussion.';}catch{}
      }
      if(!local)$('service-status').textContent='Replay mode. To generate discussions, start the local discussion server described in the project README.';
      controls();refreshOptions();await selectRecording(listings.find(r=>r.step_id===context().id)?.id||'');if(activeId)poll(activeId);
    }catch(error){$('service-status').textContent='The discussion data could not be loaded. '+error.message;}
  }
  init();
})();
