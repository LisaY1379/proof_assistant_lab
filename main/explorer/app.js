(function(root){
  'use strict';
  const successful = alt => ['closed','rejoined'].includes(alt.outcome);
  const outcomeLabels = {closed:'Reaches the theorem',rejoined:'Rejoins the proof',failed:'Failed',unresolved:'Unresolved',budget_exceeded:'Budget exhausted · unresolved'};
  function sourceLabel(alt){return alt.origin==='literature_assisted'?'Literature-assisted':alt.research_exposed?'Model proposal · literature consulted':'Model proposal · novelty unestablished';}
  function proofSegments(doc){
    // Server offsets count Unicode code points, not UTF-16 code units.
    const chars=Array.from(doc.original_proof),parts=[];let cursor=0;
    for(const step of doc.steps){
      if(step.start>cursor)parts.push({text:chars.slice(cursor,step.start).join('')});
      parts.push({text:chars.slice(step.start,step.end).join(''),step});cursor=step.end;
    }
    if(cursor<chars.length)parts.push({text:chars.slice(cursor).join('')});
    return parts;
  }
  function views(doc,removed){
    const owner=new Map(),byId=new Map(doc.nodes.map(n=>[n.id,n]));
    doc.initial_facts.concat(doc.initial_goals).forEach(id=>owner.set(id,0));
    doc.steps.forEach((s,i)=>s.adds.concat(s.opens,s.observations).forEach(id=>owner.set(id,i+1)));
    const rows=doc.steps.map(()=>0);rows.unshift(0);
    for(let i=0;i<rows.length;i++)rows[i]=Math.max(1,...['fact','goal','observation'].map(kind=>doc.nodes.filter(n=>owner.get(n.id)===i&&n.kind===kind).length));
    const offsets=[];let height=55;for(const count of rows){offsets.push(height);height+=count*152+32;}height+=50;
    const counts={},proofNodes=doc.nodes.map(n=>{
      const level=owner.get(n.id),key=level+n.kind,slot=counts[key]||0;counts[key]=slot+1;
      const step=level?doc.steps[level-1]:null;
      const y=n.kind==='goal'?height-offsets[level]-slot*152-126:offsets[level]+slot*152;
      return {...n,x:{fact:24,observation:292,goal:560}[n.kind],y,action:step?.id||null,
        label:n.kind==='goal'?'WANT':n.kind==='fact'?'HAVE':'OBSERVATION',title:n.label||n.text,
        preview:n.label?n.text:step?.title||'Starting assumptions / theorem'};
    });
    const states=doc.states.map((s,i)=>({...s,x:24,y:55+i*175,kind:'state',title:i?doc.steps[i-1].title:'Starting assumptions',
      label:i?`${s.id} · after ${s.action}`:'s0 · start',preview:`Have ${s.have.length} facts · Want ${s.want.length} goals${s.want.length?'':' · closure claimed'}`}));
    const stateEdges=states.slice(1).map((s,i)=>({from:states[i].id,to:s.id,action:s.action,kind:s.action===removed?'removed-edge':''}));
    const proofEdges=doc.proof_edges.map(e=>({...e,kind:e.action===removed?'removed-edge':e.kind}));
    for(const [i,step] of doc.steps.entries())if(!proofNodes.some(n=>n.action===step.id)){
      const id=':action:'+step.id;
      proofNodes.push({id,x:292,y:offsets[i+1],kind:'action',action:step.id,label:'ACTION',title:step.title,preview:step.justification});
      for(const fact of step.uses)proofEdges.push({from:fact,to:id,action:step.id,kind:step.id===removed?'removed-edge':'deduction'});
      for(const goal of step.closes)proofEdges.push({from:id,to:goal,action:step.id,kind:step.id===removed?'removed-edge':'meeting'});
    }
    let proofWidth=830,stateWidth=290;
    const study=doc.ablations[removed];
    if(study){study.alternatives.forEach((alt,index)=>{
      const sourceState=states[0];
      const addRoute=(nodes,edges,x,y,from,to)=>{
        let previous=from;
        alt.route.forEach((r,i)=>{
          const id=':branch:'+alt.id+':'+i;
          nodes.push({id,x,y:y+i*155,kind:'branch',action:removed,alternative:alt.id,
            routeIndex:i,
            label:i===alt.route.length-1?`${index+1}.${i+1} · ${outcomeLabels[alt.outcome]}${alt.rejoin_state?' '+alt.rejoin_state:''}`:`Branch ${index+1} · step ${i+1}${i===0?' · from s0':''}`,title:r.title,preview:r.have,
            origin:sourceLabel(alt),success:successful(alt)});
          edges.push({from:previous,to:id,kind:'branch-edge'});previous=id;
        });
        if(to)edges.push({from:previous,to,kind:'branch-edge'});
        return y+alt.route.length*155+50;
      };
      const targetState=alt.outcome==='rejoined'?alt.rejoin_state:null;
      const lastGoal=doc.initial_goals[0];
      const targetIndex=targetState?doc.states.findIndex(s=>s.id===targetState):-1;
      const targetAction=targetIndex>0?doc.steps[targetIndex-1]:null;
      const proofTarget=alt.outcome==='closed'?lastGoal:targetAction?.adds[0]||targetAction?.closes[0];
      const selectedProof=proofNodes.find(n=>n.action===removed),selectedState=states.find(n=>n.action===removed);
      height=Math.max(height,addRoute(proofNodes,proofEdges,850+index*270,selectedProof?.y||55,doc.initial_facts[0]||lastGoal,proofTarget));
      addRoute(states,stateEdges,300+index*270,selectedState?.y||sourceState.y+175,'s0',targetState);
      proofWidth=1120+index*270;stateWidth=570+index*270;
    });}
    return {proof:{nodes:proofNodes,edges:proofEdges,width:proofWidth,height},
      state:{nodes:states,edges:stateEdges,width:stateWidth,height:Math.max(...states.map(s=>s.y))+180},byId};
  }
  const api={views,proofSegments,successful,sourceLabel};
  if(typeof module==='object'&&module.exports){module.exports=api;return;}
  const $=id=>document.getElementById(id);
  let doc=null,job=null,selected=null,removed=null,branch=null,branchIndex=0,version='original',lastRevision=-1,pollTimer=null;
  const graphScale={proof:1,state:1},graphFit={proof:true,state:true};
  const el=(tag,cls,text)=>{const n=document.createElement(tag);if(cls)n.className=cls;if(text!==undefined)n.textContent=text;return n;};
  const button=(text,fn)=>{const n=el('button','',text);n.type='button';n.addEventListener('click',fn);return n;};
  let mathQueue=Promise.resolve();
  function math(node){mathQueue=mathQueue.then(async()=>{if(root.MathJax?.startup?.promise){await root.MathJax.startup.promise;if(node.isConnected)await root.MathJax.typesetPromise([node]);}}).catch(()=>{});}
  function clear(node){if(root.MathJax?.typesetClear)root.MathJax.typesetClear([node]);node.replaceChildren();}
  function paragraph(parent,title,text){const s=el('section','');s.append(el('h4','',title),el('p','detail-text',text));parent.append(s);return s;}
  function sourceLinks(parent,sources){
    const list=el('ul','source-list');for(const s of sources){
      // Imports are validated server-side; also reject unsafe protocols at the rendering boundary.
      let url;try{url=new URL(s.url);}catch{continue;}if(!['http:','https:'].includes(url.protocol))continue;
      const li=el('li'),a=el('a','',s.title||s.url);a.href=url.href;a.target='_blank';a.rel='noopener noreferrer';li.append(a);list.append(li);
    }parent.append(list);
  }
  function studySources(study,alt){const ids=new Set(alt.source_ids);return (study.research.sources||[]).filter(s=>ids.has(s.id));}
  function showAlternative(parent,study,alt){
    const box=el('section','alternative '+(successful(alt)?'success':'failure'));box.dataset.alternative=alt.id;
    box.append(el('span','badge',outcomeLabels[alt.outcome]),el('span','source-badge',sourceLabel(alt)),el('h4','',alt.title));
    paragraph(box,'Origin and adaptation',alt.adaptation);
    if(alt.origin==='literature_assisted'){
      sourceLinks(box,studySources(study,alt));
      box.append(el('p','small','This is a literature-assisted replacement, not independent discovery. Its existence does not establish equal discovery cost or make the removed strategy noncritical.'));
    }else if(alt.research_exposed){
      box.append(el('p','small','The model saw retrieved literature but did not attribute this particular proposal to a source. Independent discovery is not established. Consulted sources:'));
      sourceLinks(box,study.research.sources||[]);
    }
    const route=el('ol','reader-route-steps');for(const r of alt.route){const li=el('li');li.append(el('strong','',r.title),el('p','detail-text',r.have),el('p','small','Want: '+(r.want||'No remaining obligations claimed.')));route.append(li);}box.append(route);
    paragraph(box,'Alternative argument',alt.argument);paragraph(box,'Outcome and obligations',alt.assessment);
    if(alt.rejoin_state)box.append(el('p','small','Rejoin checkpoint: '+alt.rejoin_state));
    paragraph(box,'Mathematical cost and tradeoffs',alt.cost);box.append(el('p','small','Search difficulty has not been measured.'));
    parent.append(box);
  }
  function choose(action,options={}){
    selected=action;branch=options.branch||null;branchIndex=options.routeIndex||0;
    if(options.toggle)removed=removed===action?null:action;
    render();focusGraph('proof');focusGraph('state');
  }
  function draw(kind,view){
    const board=$(kind+'-board');clear(board);board.style.width=view.width+'px';board.style.height=view.height+'px';
    const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.setAttribute('width',view.width);svg.setAttribute('height',view.height);svg.setAttribute('aria-hidden','true');board.append(svg);
    const defs=document.createElementNS(svg.namespaceURI,'defs'),marker=document.createElementNS(svg.namespaceURI,'marker'),arrow=document.createElementNS(svg.namespaceURI,'path');
    for(const [key,value] of Object.entries({id:'arrow-'+kind,viewBox:'0 0 8 6',refX:'7',refY:'3',markerWidth:'8',markerHeight:'6',orient:'auto'}))marker.setAttribute(key,value);
    arrow.setAttribute('d','M0,0 L8,3 L0,6 Z');arrow.setAttribute('fill','context-stroke');marker.append(arrow);defs.append(marker);svg.append(defs);
    const positions=new Map(view.nodes.map(n=>[n.id,n]));
    for(const e of view.edges){const a=positions.get(e.from),b=positions.get(e.to);if(!a||!b)continue;
      const path=document.createElementNS(svg.namespaceURI,'path');const upward=b.y<a.y,ax=a.x+120,ay=a.y+(upward?0:126),bx=b.x+120,by=b.y+(upward?126:0);
      const mid=(ay+by)/2;path.setAttribute('d',`M ${ax} ${ay} C ${ax} ${mid}, ${bx} ${mid}, ${bx} ${by}`);path.setAttribute('class','graph-edge '+e.kind);path.setAttribute('marker-end',`url(#arrow-${kind})`);svg.append(path);
    }
    for(const n of view.nodes){
      const card=button('',()=>n.alternative?choose(n.action,{branch:n.alternative,routeIndex:n.routeIndex}):choose(n.action,{toggle:!!n.action}));
      card.className='gcard '+n.kind+(n.kind==='branch'?(n.success?' success':' failure'):'')+(n.action&&n.action===selected?' selected':'')+(removed&&n.action===removed&&n.kind!=='branch'?' removed':'');
      card.style.left=n.x+'px';card.style.top=n.y+'px';card.dataset.action=n.action||'';card.dataset.node=n.id;
      card.setAttribute('aria-label',n.alternative?`Inspect alternative: ${n.title}`:n.action?`Toggle alternatives for ${n.action}: ${n.title}`:'Inspect starting assumptions');
      card.setAttribute('aria-pressed',String(!!n.action&&n.action===removed));card.title=n.title+'\n'+n.preview;
      card.append(el('small','',n.label),el('strong','',n.title),el('span','preview',n.preview));if(n.origin)card.append(el('span','origin',n.origin));board.append(card);
    }
    math(board);
    scaleGraph(kind);
  }
  function scaleGraph(kind){const board=$(kind+'-board'),holder=$(kind+'-scale'),viewport=$(kind+'-viewport');
    const scale=graphFit[kind]?Math.min(1,Math.max(.3,(viewport.clientWidth-8)/parseFloat(board.style.width))):1;
    graphScale[kind]=scale;board.style.transform=`scale(${scale})`;board.style.transformOrigin='top left';holder.style.width=parseFloat(board.style.width)*scale+'px';holder.style.height=parseFloat(board.style.height)*scale+'px';}
  function focusGraph(kind){const viewport=$(kind+'-viewport'),board=$(kind+'-board');const cards=[...board.querySelectorAll('.gcard')];
    const node=cards.find(n=>n.dataset.action===selected)||cards[0];if(node)viewport.scrollTo({left:graphFit[kind]?0:Math.max(0,node.offsetLeft*graphScale[kind]-30),top:Math.max(0,node.offsetTop*graphScale[kind]-60),behavior:'instant'});}
  function showProtocol(parent,step){
    const record=step.protocol;
    if(!record){parent.append(el('p','small','This saved step has no structured protocol annotation.'));return;}
    const detail=el('details','protocol-record');detail.append(el('summary','',`Protocol record · ${record.direction} · ${record.actions.map(a=>a.kind).join(' → ')}`));
    paragraph(detail,'Before the move',record.context);paragraph(detail,'Target',record.target);
    paragraph(detail,'Basic steps first',record.basic_progress);paragraph(detail,'Remaining gap',record.remaining_gap);
    for(const [key,title] of [['target_feature','Target feature'],['available_feature','Available feature'],['connection','Motivating connection']])paragraph(detail,title,record.observation[key]);
    for(const action of record.actions){const part=el('section');part.append(el('h4','',`${action.id} · ${action.kind} · ${action.role}`));
      for(const [key,title] of [['move','Move'],['provenance','Why this choice'],['rule','Rule or selection'],['inputs','Inputs'],['verification','Verification']])paragraph(part,title,action[key]);
      if(action.verifies.length)part.append(el('p','small','Checks choice: '+action.verifies.join(', ')));
      for(const use of action.toolkit_uses){const tool=doc.protocol?.context.toolkit.find(t=>t.id===use.id);paragraph(part,'Toolkit: '+(tool?.name||use.id),(tool?.statement||'')+'\nRequired: '+(tool?.hypotheses||'')+'\nChecked here: '+use.hypotheses_check);}
      detail.append(part);
    }
    paragraph(detail,'Logical relation · '+record.relation.kind,record.relation.justification);
    paragraph(detail,'Side conditions and scope',record.relation.side_conditions);paragraph(detail,'Remaining obligations',record.remaining_obligations);
    detail.append(el('p','small','Annotation structure checked; the mathematical claims and classifications still require review.'));parent.append(detail);
  }
  function renderInspector(){
    const box=$('inspector');clear(box);const index=doc.steps.findIndex(s=>s.id===selected),step=doc.steps[index],state=doc.states[index+1]||doc.states[0],study=doc.ablations[selected];
    const selectedAlternative=study?.alternatives.find(a=>a.id===branch),routeState=selectedAlternative?.route[branchIndex];
    box.append(el('h2','',routeState?'Alternative state: '+routeState.title:step?.title||'Starting assumptions'));
    const columns=el('div','have-want-grid');for(const [key,label] of [['have','Have'],['want','Want']]){const col=el('section');col.append(el('h3','',label));const ul=el('ul');
      if(routeState)ul.append(el('li','',routeState[key]||'No remaining obligations claimed.'));
      else{for(const id of state[key])ul.append(el('li','',doc.nodes.find(n=>n.id===id).text));if(!state[key].length)ul.append(el('li','',key==='want'?'No open goals in the reconstructed proof.':'No established facts.'));}
      col.append(ul);columns.append(col);}box.append(columns);
    if(step&&!routeState){paragraph(box,'Action and mathematical justification',step.justification||step.explanation);showProtocol(box,step);}
    if(removed){box.append(el('p','small',routeState?'This branch starts from the original assumptions; the reference proof’s later facts are not inherited.':'The selected reference result is the step being removed, not a premise for its replacement.'));
      if(study){paragraph(box,'Global ablation',study.restriction);if(!study.alternatives.length)box.append(el('p','','No valid alternative established.'));
        for(const alt of study.alternatives){if(branch===alt.id)showAlternative(box,study,alt);else box.append(button(alt.title+' · '+outcomeLabels[alt.outcome],()=>choose(selected,{branch:alt.id})));}
      }else box.append(el('p','','Alternatives for this step have not been reviewed yet.'));
    }math(box);
  }
  function renderReader(){
    const body=$('reader-body');clear(body);
    $('edition-note').textContent=version==='original'?(doc.experiment?'The exact saved Library-RAG proof. See the source record below for the control answer and changes.':'Your supplied proof, preserved verbatim.'):version==='detailed'?'Each step with its derivation, alternatives, sources, and qualitative costs. Yellow: literature-assisted replacement. Red: no successful replacement established in this study.':`Only selected critical steps are expanded. ${doc.critical.rationale} Editorial assessment; discovery difficulty is unmeasured.`;
    body.setAttribute('aria-labelledby','tab-'+version);
    for(const tab of document.querySelectorAll('[data-version]')){const active=tab.dataset.version===version;tab.setAttribute('aria-selected',String(active));tab.tabIndex=active?0:-1;}
    for(const part of proofSegments(doc)){
      if(!part.step){body.append(el('div','gap',part.text));continue;}
      const step=part.step,study=doc.ablations[step.id],critical=doc.critical.steps.includes(step.id);
      const noAlternative=study&&!study.alternatives.some(successful);
      const literature=study?.alternatives.some(a=>a.origin==='literature_assisted');
      const section=el('article','reader-passage'+(step.id===selected?' reader-active':'')+(version==='detailed'&&literature?' reader-literature-assisted':'')+(version==='detailed'&&noAlternative?' reader-no-alternative':''));section.dataset.step=step.id;
      const header=el('header');header.append(el('h3','',step.title),button('Show '+step.id,()=>{choose(step.id);focusGraph('state');focusGraph('proof');}));section.append(header);
      section.append(el('p','original-text',version==='focused'&&!critical?step.short_version:part.text));
      if(version==='detailed'||(version==='focused'&&critical)){
        if(critical)section.append(el('span','reader-key-badge','Critical step · editorial selection'));
        if(version==='detailed'&&literature)section.append(el('span','reader-literature-badge','Alternative checked against online literature'));
        if(version==='detailed'&&noAlternative)section.append(el('span','reader-unresolved-badge','No valid alternative established'));
        paragraph(section,'Why this move helps',step.observation);paragraph(section,'Detailed derivation',step.explanation);paragraph(section,'Difficulty and tradeoffs',step.difficulty);
        showProtocol(section,step);
        if(study){const alternatives=el('details','reader-alternatives');alternatives.dataset.action=step.id;alternatives.open=step.id===selected;
          alternatives.append(el('summary','',`Alternatives to this step · ${step.id}`));paragraph(alternatives,'Forbidden strategy',study.restriction);
          alternatives.append(el('p','small','Literature search: '+study.research.status+'. '+(study.research.verification||'Source links are retained from the search response; mathematical support still requires review.')));
          if(!study.alternatives.length)alternatives.append(el('p','','No substantive replacement was established in this analysis.'));
          for(const alt of study.alternatives)showAlternative(alternatives,study,alt);section.append(alternatives);
        }else section.append(el('p','small','Ablation not reviewed yet. No conclusion about replaceability.'));
      }
      body.append(section);
    }
    focusReader();math(body);mathQueue.then(focusReader);
  }
  function focusReader(){const body=$('reader-body'),active=[...body.querySelectorAll('[data-step]')].find(n=>n.dataset.step===selected);if(active)body.scrollTop+=active.getBoundingClientRect().top-body.getBoundingClientRect().top-12;}
  function renderAudit(){
    const body=$('audit-body');clear(body);body.append(el('p','small',doc.metadata?.origin||'Imported reconstruction.'));
    if(doc.experiment){
      const record=doc.experiment;
      paragraph(body,'Experiment provenance',record.note);
      sourceLinks(body,[{url:record.url,title:'Open this theorem in the original control vs Library-RAG report'}]);
      body.append(el('p','small',`${record.input_id} · ${record.model} · source SHA-256: ${record.source_sha256}`));
      const control=el('details');control.append(el('summary','','Read the saved control proof'));paragraph(control,'Control answer',record.control_proof);body.append(control);
      const diff=el('details');diff.append(el('summary','','Exact control → Library-RAG changes'),el('pre','',record.comparison_diff));body.append(diff);
    }
    for(const note of doc.supplemental_notes||[]){const detail=el('details');detail.append(el('summary','',note.title));paragraph(detail,'Worked argument',note.text);paragraph(detail,'Scope and outcome',note.note);body.append(detail);}
    if(doc.protocol){const detail=el('details');detail.append(el('summary','','Decomposition protocol · '+doc.protocol.version));
      for(const [key,title] of [['domains','Domains and assumptions'],['definitions','Definitions'],['basic_rules','Declared basic rules']])paragraph(detail,title,doc.protocol.context[key]);
      detail.append(el('p','small',doc.protocol.validation));
      if(doc.protocol.reference){detail.append(el('p','small','Recorded protocol fingerprint: '+doc.protocol.reference.sha256));paragraph(detail,'Protocol used for this decomposition',doc.protocol.reference.text);}
      body.append(detail);
    }else body.append(el('p','small','Legacy explorer: no structured protocol record. Generate a new explorer to apply the current protocol.'));
    body.append(el('p','small',doc.experiment?'This collection was authored locally. It is a mathematical reconstruction, not a fresh search run.':`${job.requests?.length||0} recorded generation/research requests. This is workflow usage, not mathematical search difficulty.`));
    for(const step of doc.steps){const research=doc.ablations[step.id]?.research||doc.research_records?.[step.id];if(!research)continue;
      const detail=el('details');detail.append(el('summary','',step.title+' · literature search '+research.status));sourceLinks(detail,research.sources||[]);detail.append(el('p','detail-text',research.summary||''));if(research.verification)detail.append(el('p','small',research.verification));body.append(detail);
    }
    math(body);
  }
  function render(){if(!doc)return;
    $('workspace').hidden=false;$('document-title').textContent=doc.title;$('statement').textContent=doc.statement;
    $('evidence').textContent=(doc.metadata?.origin||'Imported reconstruction.')+' Graph structure is checked; mathematics is not formally verified. '+(doc.closure?'The supplied proof claims closure.':'The reconstructed proof still has open goals.');
    const step=doc.steps.find(s=>s.id===removed);$('selection-status').textContent=step?`Removed: ${step.title}. Alternatives restart from the assumptions. Click this step again to restore.`:'Click a result node to remove its step and show alternative routes.';
    $('restore').disabled=!removed;const graph=views(doc,removed);draw('proof',graph.proof);draw('state',graph.state);renderInspector();renderReader();renderAudit();math($('statement'));
  }
  async function request(path,body){const res=await fetch(path,body===undefined?{}:{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});const data=await res.json();if(!res.ok)throw Error(data.error||'Request failed');return data;}
  function busy(running){$('generate').disabled=running;$('example').disabled=running;$('import-file').disabled=running;$('stop').hidden=!running;}
  function accept(data){const changed=!job||job.id!==data.id||lastRevision!==data.revision;job=data;$('status').textContent=data.message;busy(data.status==='running');
    $('resume').hidden=!['stopped','error','interrupted'].includes(data.status)||!data.input_proof;
    if(data.document&&changed){doc=data.document;lastRevision=data.revision;$('composer').open=false;render();}
    if(data.status==='running'){clearTimeout(pollTimer);const id=data.id;pollTimer=setTimeout(async()=>{try{const next=await request('/api/explorers/'+id);if(job?.id===id)accept(next);}catch(e){$('status').textContent='Connection interrupted. Reload to reconnect: '+e.message;}},1800);}
  }
  function setJob(data){clearTimeout(pollTimer);lastRevision=-1;selected=null;removed=null;branch=null;doc=null;$('workspace').hidden=true;const url=new URL(location.href);url.searchParams.set('run',data.id);history.replaceState(null,'',url);accept(data);}
  $('generate-form').addEventListener('submit',async event=>{event.preventDefault();busy(true);$('status').textContent='Starting proof analysis…';try{setJob(await request('/api/explorers',{proof:$('proof-input').value,model:$('model-input').value,max_steps:Number($('step-limit').value),online_search:$('online-search').checked}));}catch(e){$('status').textContent=e.message;busy(false);}});
  $('stop').addEventListener('click',async()=>{try{accept(await request('/api/explorers/'+job.id+'/stop',{}));}catch(e){$('status').textContent=e.message;}});
  $('resume').addEventListener('click',async()=>{$('resume').disabled=true;try{accept(await request('/api/explorers/'+job.id+'/resume',{}));}catch(e){$('status').textContent=e.message;}finally{$('resume').disabled=false;}});
  $('example').addEventListener('click',async()=>{busy(true);try{const sample=await request('/explorer/example.json');setJob(await request('/api/explorers/import',sample));}catch(e){$('status').textContent=e.message;}finally{busy(job?.status==='running');}});
  $('import-file').addEventListener('change',async event=>{const file=event.target.files[0];if(!file)return;busy(true);try{if(file.size>2_000_000)throw Error('Explorer file exceeds 2 MB');setJob(await request('/api/explorers/import',JSON.parse(await file.text())));}catch(e){$('status').textContent='Could not open explorer: '+e.message;}finally{event.target.value='';busy(job?.status==='running');}});
  $('export').addEventListener('click',()=>{const url=URL.createObjectURL(new Blob([JSON.stringify(doc,null,2)],{type:'application/json'})),a=el('a');a.href=url;a.download='proof-explorer.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
  $('restore').addEventListener('click',()=>{removed=null;branch=null;render();});
  for(const tab of document.querySelectorAll('[data-version]')){tab.addEventListener('click',()=>{version=tab.dataset.version;renderReader();});tab.addEventListener('keydown',e=>{const tabs=[...document.querySelectorAll('[data-version]')],i=tabs.indexOf(tab);if(['ArrowLeft','ArrowRight','Home','End'].includes(e.key)){e.preventDefault();const next=e.key==='Home'?0:e.key==='End'?2:(i+(e.key==='ArrowRight'?1:2))%3;tabs[next].click();tabs[next].focus();}});}
  for(const b of document.querySelectorAll('[data-focus]'))b.addEventListener('click',()=>focusGraph(b.dataset.focus));
  for(const b of document.querySelectorAll('[data-fit]'))b.addEventListener('click',()=>{graphFit[b.dataset.fit]=true;scaleGraph(b.dataset.fit);focusGraph(b.dataset.fit);});
  for(const b of document.querySelectorAll('[data-readable]'))b.addEventListener('click',()=>{graphFit[b.dataset.readable]=false;scaleGraph(b.dataset.readable);focusGraph(b.dataset.readable);});
  window.addEventListener('resize',()=>{if(doc){scaleGraph('proof');scaleGraph('state');}});
  const modal=$('reader-modal'),panel=$('reader-panel');
  $('expand-reader').addEventListener('click',()=>{if(modal.open)modal.close();else{modal.append(panel);$('expand-reader').textContent='Return to graphs';modal.showModal();focusReader();}});
  modal.addEventListener('close',()=>{$('reader-anchor').after(panel);$('expand-reader').textContent='Expand reading view';});
  const saved=document.body.dataset.explorerDocument;
  const run=new URL(location.href).searchParams.get('run');
  if(saved)request(saved).then(document=>accept({id:saved,revision:1,status:'complete',message:'Explorer ready · select a step to inspect its alternatives.',document})).catch(e=>{$('status').textContent='Could not open this saved explorer: '+e.message;});
  else if(run)request('/api/explorers/'+encodeURIComponent(run)).then(accept).catch(e=>{$('status').textContent=e.message;});
})(typeof window==='undefined'?globalThis:window);
