(function () {
  'use strict';
  const $=id=>document.getElementById(id);
  const P=window.HansonWright, G=window.HansonWrightStates.build();
  const states=new Map(G.states.map((s,i)=>[s.id,{...s,label:`S${i}`}])) , edges=new Map(G.transitions.map(e=>[e.id,e]));
  const canonical=new Set(G.canonicalStates),canonicalEdges=new Set(G.canonicalTransitions);
  const proofNodes=new Map(P.nodes.map(n=>[n.id,n])),goalName=id=>proofNodes.get(id).title;
  const M=window.HansonWrightMoments, H=window.HansonWrightStates.create(M,M.stateConfig).build();
  const momentStates=new Map(H.states.map((s,i)=>[s.id,{...s,label:`A${i}`}])) ,momentEdges=new Map(H.transitions.map(e=>[e.id,e]));
  let selected=G.initialState,transition=null,timer=null,statePositions=new Map(),stateWidth=520;
  let ablation=null,selectedAlternative=null,worked=null,branchSelection=null,proofOverview=false,study=null,studyNode=null;
  let reader=null;
  let originalGraph=null,originalSelection='start',receivingOriginal=false;
  let graphView='proof',previousProofNodes=new Set(),previousProofEdges=new Set();
  const zoom={proof:1,state:1};
  const isAblation=()=>$('graph-mode').value==='ablation';
  const useOriginalGraph=()=>!isAblation()&&!worked&&!study&&!ablation;
  const currentContext=()=>({P,G,states,edges,goalName,transition,choose,take});
  const nodeHeight=n=>n.height??(n.kind==='given'?P.layout.givenHeight:n.kind==='observation'?P.layout.observationHeight:P.layout.nodeHeight);
  function el(tag,cls,text) {const n=document.createElement(tag);if(cls)n.className=cls;if(text!==undefined)n.textContent=text;return n;}
  function button(text,callback,cls) {const n=el('button',cls,text);n.type='button';n.addEventListener('click',callback);return n;}
  function svg(width,height) {const n=document.createElementNS('http://www.w3.org/2000/svg','svg');n.setAttribute('viewBox',`0 0 ${width} ${height}`);n.setAttribute('width',width);n.setAttribute('height',height);n.setAttribute('aria-hidden','true');return n;}
  function path(parent,d,cls) {const n=document.createElementNS('http://www.w3.org/2000/svg','path');n.setAttribute('d',d);n.setAttribute('class',cls);parent.append(n);return n;}
  function curve(a,b) {return `M ${a.x} ${a.y} C ${a.x} ${(a.y+b.y)/2}, ${b.x} ${(a.y+b.y)/2}, ${b.x} ${b.y}`;}
  function stop() {clearInterval(timer);timer=null;$('replay-state').textContent='▶ Play proof order';}
  function choose(id,edgeId=null,focus=false) {
    worked=null;branchSelection=null;ablation=null;selectedAlternative=null;study=null;studyNode=null;
    selected=id;transition=edgeId;
    originalSelection=edges.get(edgeId)?.action||states.get(id).completed.at(-1)||'start';
    if(!canonical.has(id) && $('graph-mode').value!=='all')$('graph-mode').value='all';
    render();if(focus){focusState();focusProof();}
  }
  function chooseCanonical(index,focus=true) {choose(G.canonicalStates[index],index?G.canonicalTransitions[index-1]:null,focus);}
  function take(edge) {stop();choose(edge.to,edge.id,true);}
  function fit(kind,width,height) {
    const scale=Math.min(1,Math.max(kind==='state'?.82:.65,(viewportWidth(kind)-18)/width));
    sizeBoard(kind,width,height,scale);
  }
  function viewportWidth(kind){return $(`reference-${kind}-viewport`).clientWidth||document.querySelector('.reference-panels').clientWidth;}
  function sizeBoard(kind,width,height,baseScale){
    const scale=baseScale*zoom[kind];
    const board=$(`reference-${kind}-board`), wrapper=$(`reference-${kind}-scale`);
    board.style.width=width+'px';board.style.height=height+'px';board.style.transform=`scale(${scale})`;
    wrapper.style.width=width*scale+'px';wrapper.style.height=height*scale+'px';wrapper.dataset.scale=scale;
    wrapper.dataset.baseScale=baseScale;
  }
  function focusAt(kind,x,y) {
    const v=$(`reference-${kind}-viewport`), scale=Number($(`reference-${kind}-scale`).dataset.scale);
    v.scrollTo({top:Math.max(0,y*scale-v.clientHeight*.4),left:Math.max(0,x*scale-v.clientWidth/2),behavior:'instant'});
  }
  function focusState() {if(worked){const p=worked.state.nodes.find(n=>n.id===branchSelection.state);if(p)focusAt('state',p.x+105,p.y+50);return;}const p=statePositions.get(selected);if(p)focusAt('state',p.x+105,p.y+48);}
  function focusProof() {
    if(worked){
      const ctx=branchContext(),e=ctx.edges.get(branchSelection.edge),id=e?ctx.P.byId[e.action].focus:'ultimate';
      const n=worked.proof.nodes.find(n=>n.sourceId===id&&(n.route===branchSelection.route||id==='ultimate'));
      if(n)focusAt('proof',n.x+n.width/2,n.y+n.height/2);return;
    }
    const edge=edges.get(transition), s=states.get(selected);
    const id=study?P.byId[study.action].focus:ablation?P.byId[ablation.removedTransition.action].focus:edge?P.byId[edge.action].focus:s.depth===0?'independence':s.closed?'ultimate':s.frontierGoals.at(-1)||'ultimate';
    const n=proofNodes.get(id);focusAt('proof',n.x+120,n.y+50);
  }
  function proofPoint(id,side) {
    const n=proofNodes.get(id),w=n.kind==='observation'?P.layout.observationWidth:P.layout.nodeWidth;
    return {x:n.x+(side==='left'?0:side==='right'?w:w/2),y:n.y+(side==='top'?0:side==='bottom'?nodeHeight(n):nodeHeight(n)/2)};
  }
  function proofPath(from,to) {
    if(P.meetings?.some(([a,b])=>a===from&&b===to)) {
      const a=proofPoint(from,'right'),b=proofPoint(to,'left');
      return `M ${a.x} ${a.y} H 306 V ${b.y} H ${b.x}`;
    }
    const rails={'independence:expanded':12,'centered:expanded':18,'subgaussian:linear':292,'expanded:decoupled':8,'linear:replaced':282,'diagonal:diagonal-goal':12,'expanded:diagonal':18,'decoupled:replaced':18,'bounded:tail':18};
    const rail=(P.rails || rails)[`${from}:${to}`];
    if(rail!==undefined){const side=rail<24?'left':'right',a=proofPoint(from,side),b=proofPoint(to,side);return `M ${a.x} ${a.y} L ${rail} ${a.y} L ${rail} ${b.y} L ${b.x} ${b.y}`;}
    if(proofPoint(from).y===proofPoint(to).y)return curve(proofPoint(from,'right'),proofPoint(to,'left'));
    const down=proofPoint(to).y>proofPoint(from).y;return curve(proofPoint(from,down?'bottom':'top'),proofPoint(to,down?'top':'bottom'));
  }
  function renderProof(s) {
    const board=$('reference-proof-board');board.replaceChildren();
    const art=svg(P.layout.width,P.layout.height), visible=new Set(s.visibleProofNodes), achieved=P.achieved(s.completed), action=edges.get(transition)?.action;
    // Inspiration depends on a particular history; a merged state has no unique history.
    const animate=$('graph-mode').value==='canonical'&&!study&&!worked,newEdges=new Set();
    for(const [a,b,type] of P.edges.filter(e=>e[2]!=='inspiration')) {
      const introduced=visible.has(a)&&visible.has(b),key=a+':'+b;
      if(animate&&!introduced)continue;
      const line=path(art,proofPath(a,b),`reference-line ${type} ${introduced?'':'pending'}`);
      if(introduced){newEdges.add(key);if(animate&&!previousProofEdges.has(key)){line.classList.add('graph-draw');line.setAttribute('pathLength','1');}}
    }
    for(const [a,b] of (P.meetings || [['computed','scalar-goal'],['bounded','mgf'],['tail','offtail'],['diagonal','ultimate'],['tail','ultimate']])) {
      if(visible.has(a)&&achieved.has(b))path(art,proofPath(a,b),'reference-line match');
    }
    board.append(art);
    for(const [text,x] of [['HAVE · established facts',24],['WANT · goal reductions',348]]){const label=el('div','proof-lane-title',text);label.style.left=x+'px';board.append(label);}
    for(const n of P.nodes) {
      if(animate&&!visible.has(n.id))continue;
      const b=button('',()=>{
        stop();
        if(isAblation()&&(n.event!=='start'||n.id==='ultimate')) {ablateAction(n.id==='ultimate'?'finish':n.event);return;}
        const event=n.id==='ultimate'&&s.closed?'finish':n.event;
        if(event==='start'){choose(G.initialState,null,true);return;}
        const incoming=G.transitions.filter(e=>e.action===event && e.to===s.id);
        const e=incoming[0]||edges.get(G.canonicalTransitions[P.events.findIndex(e=>e.id===event)]);
        take(e);
      },`node ${n.kind} ${visible.has(n.id)?'':'pending'} ${achieved.has(n.id)?'achieved':''} ${n.event===action || (action==='finish'&&n.id==='ultimate')?'selected':''} ${ablation&&(n.event===ablation.removedTransition.action||(ablation.removedTransition.action==='finish'&&n.id==='ultimate'))?'ablated-move':''}`);
      b.style.left=n.x+'px';b.style.top=n.y+'px';b.style.height=nodeHeight(n)+'px';
      b.append(el('span','node-kind',n.kind==='observation'?'Observation':n.label),el('span','node-title',n.title),el('span','node-formula',n.formula));
      b.dataset.proofEvent=n.id==='ultimate'?'finish':n.event;b.dataset.proofNode=n.id;
      if(animate&&!previousProofNodes.has(n.id))b.classList.add('graph-arrive');
      b.title='Inspect proof move: '+(P.byId[n.event]?.title||'Starting state');
      board.append(b);
    }
    fit('proof',P.layout.width,P.layout.height);
    previousProofNodes=visible;previousProofEdges=newEdges;
    $('proof-status').textContent=ablation?`Before ${ablation.removedTransition.action} · removed move outlined · alternatives not evaluated`:s.closed?'Proof closed · all checkpoints discharged':`${s.visibleProofNodes.length} introduced nodes · ${s.closedGoals.length} goals discharged`;
  }
  function renderGraph() {
    if(isAblation()){renderAblationGraph();return;}
    const all=$('graph-mode').value==='all', shown=G.states.filter(s=>all||(canonical.has(s.id)&&s.depth<=states.get(selected).depth)), shownIds=new Set(shown.map(s=>s.id));
    const levels=Array.from({length:P.events.length+1},(_,depth)=>shown.filter(s=>s.depth===depth));
    const maxWidth=Math.max(...levels.map(row=>row.length));stateWidth=Math.max(520,maxWidth*236+32);
    const rowGap=all?270:220, height=P.events.length*rowGap+160;
    statePositions=new Map();
    levels.forEach((row,depth)=>{
      row.sort((a,b)=>Number(canonical.has(b.id))-Number(canonical.has(a.id)) || a.id.localeCompare(b.id));
      row.forEach((s,i)=>statePositions.set(s.id,{x:32+i*236+(stateWidth-64-row.length*236)/2,y:25+depth*rowGap}));
    });
    const board=$('reference-state-board');board.replaceChildren();const art=svg(stateWidth,height);board.append(art);
    const shownEdges=G.transitions.filter(e=>shownIds.has(e.from)&&shownIds.has(e.to));
    const outgoing=new Map();for(const e of shownEdges){if(!outgoing.has(e.from))outgoing.set(e.from,[]);outgoing.get(e.from).push(e);}
    for(const e of shownEdges) {
      const a=statePositions.get(e.from),b=statePositions.get(e.to), main=canonicalEdges.has(e.id);
      path(art,curve({x:a.x+105,y:a.y+100},{x:b.x+105,y:b.y}),`state-line ${main?'canonical':''} ${e.id===transition?'selected':''}`);
      // Per-source rows keep every action label distinct, even when paths cross.
      const siblings=outgoing.get(e.from), row=siblings.indexOf(e);
      const label=button(`${P.byId[e.action].direction==='backward'?'↑':'↓'} ${e.action} → ${states.get(e.to).label}`,()=>take(e),`action-edge ${main?'canonical':''} ${e.id===transition?'selected':''}`);
      label.style.left=a.x+'px';label.style.top=a.y+111+row*30+'px';label.title=P.byId[e.action].title;
      label.setAttribute('aria-label',`${states.get(e.from).label} to ${states.get(e.to).label}: ${P.byId[e.action].title}`);board.append(label);
    }
    for(const s of shown) {
      const p=statePositions.get(s.id), data=states.get(s.id), b=button('',()=>{stop();choose(s.id);},`state-card ${canonical.has(s.id)?'canonical':''} ${s.id===selected?'selected':''} ${s.closed?'closed':''}`);
      b.style.left=p.x+'px';b.style.top=p.y+'px';b.dataset.state=s.id;b.setAttribute('aria-pressed',String(s.id===selected));
      b.append(el('span','state-card-meta',`${data.label} · ${s.depth} moves`),el('strong','',s.closed?'Have meets want ✓':s.depth===0?'Assumptions → theorem':s.frontierGoals.map(goalName).join(' + ')),el('small','',`${s.facts.length} derived results · ${s.openGoals.length} open goals`));
      if(!all){const action=stateAction(s.id);b.dataset.stepAction=action||'start';b.querySelector('strong').textContent=stateStepTitle(s.id);}
      b.title=s.completed.length?'Completed: '+s.completed.join(', '):'No proof moves yet';board.append(b);
    }
    fit('state',stateWidth,height);
    $('state-status').textContent=`${shown.length} states · ${shownEdges.length} transitions${all?' · same moves, different orders':' · selected proof order'}`;
  }
  function restoreAblation() {
    worked=null;branchSelection=null;ablation=null;selectedAlternative=null;study=null;studyNode=null;
    render();
  }
  function stateAction(id){return window.HansonWrightAblationProofs.actionAtState(G,id);}
  function stateStepTitle(id){const action=stateAction(id);return action?proofNodes.get(P.byId[action].focus).title:'Assumptions → theorem';}
  function ablateState(id){
    const action=stateAction(id);
    if(!action){stop();choose(G.initialState);return;}
    ablateAction(action);
  }
  function ablateAction(action){
    const activeAction=worked?.removedAction||study?.action||ablation?.removedTransition.action;
    if(activeAction===action){stop();restoreAblation();return;}
    const model=window.HansonWrightAblationProofs.create(action,G);
    stop();study=null;studyNode=null;ablation=null;selectedAlternative=null;worked=null;branchSelection=null;
    selected=model.selectedState;transition=model.removedTransition.id;
    if(action==='sign'){
      worked=window.HansonWrightWorkedAblation.create(P,G,M,H);
      branchSelection={route:'original',state:worked.selectedState,edge:G.canonicalTransitions[0]};
      proofOverview=true;render();
      for(const kind of ['proof','state'])$(`reference-${kind}-viewport`).scrollTo({top:0,left:0,behavior:'instant'});
      return;
    }
    study=model;proofOverview=false;render();
    const first=studyPositions[0],proofStart=proofNodes.get(P.byId[action].focus);
    focusAt('state',300,first.y+35);focusAt('proof',854,Math.max(80,proofStart.y)+35);
  }
  function renderAblationGraph() {
    const layout=window.HansonWrightAblation.layout(G,ablation), board=$('reference-state-board');
    statePositions=new Map(layout.states.map(p=>[p.id,p]));stateWidth=layout.width;
    board.replaceChildren();
    const background=el('div','alternative-background');background.style.height=layout.height+'px';board.append(background);
    const art=svg(layout.width,layout.height);board.append(art);
    const sourceDepth=ablation?states.get(ablation.sourceState).depth:Infinity;
    for(const id of G.canonicalTransitions) {
      const e=edges.get(id),a=statePositions.get(e.from),b=statePositions.get(e.to),removed=ablation?.removedTransition.id===id;
      if(removed){
        path(art,`M ${a.x+105} ${a.y+100} v 12 M ${b.x+105} ${b.y-16} v 16`,'state-line removed-edge');
      }else path(art,curve({x:a.x+105,y:a.y+100},{x:b.x+105,y:b.y}),`state-line canonical ${states.get(e.from).depth>sourceDepth?'reference-future':''}`);
      const label=button(removed?`× Removed: ${e.action}`:`${e.action} → ${states.get(e.to).label}`,()=>ablateAction(e.action),`action-edge ${removed?'removed-action':'canonical'}`);
      label.dataset.action=e.action;label.style.left=a.x+'px';label.style.top=a.y+115+'px';label.setAttribute('aria-pressed',String(removed));
      label.setAttribute('aria-label',removed?`Removed action: ${e.action}`:`Remove ${e.action}, which produces ${states.get(e.to).label}`);board.append(label);
    }
    if(ablation) {
      const source=statePositions.get(ablation.sourceState);
      for(const p of layout.alternatives) {
        const a=ablation.alternatives.find(a=>a.id===p.id), success=a.ending==='success';
        path(art,`M ${source.x+210} ${source.y+50} H 288 V ${p.y+35} H ${p.x}`,`alternative-line ${success?'success':'failure'}`);
        if(a.targetState){
          const target=statePositions.get(a.targetState);
          path(art,`M ${p.x+p.width} ${p.y+70} H 650 V ${target.y+50} H ${target.x+210} l 9 -5 m -9 5 l 9 5`,'alternative-line success reconnect');
        }
        const card=button('',()=>{selectedAlternative=a.id;render();},`alternative-card ${success?'success':'failure'} ${selectedAlternative===a.id?'selected':''}`);
        card.style.left=p.x+'px';card.style.top=p.y+'px';card.style.width=p.width+'px';card.style.height=p.height+'px';
        card.dataset.alternative=a.id;card.setAttribute('aria-label',`${a.name}: ${a.label}. Illustrative, not evaluated.`);
        card.append(el('span','alternative-meta',`${a.name.toUpperCase()} · ENDING EXAMPLE`),el('strong','',`${a.symbol} ${a.label}`),el('span','alternative-destination',a.targetState?`→ ${states.get(a.targetState).label}${a.targetState===G.finalState?' · final goal':''} · finite budget B`:'Terminal branch · no rejoin'),el('small','','Method not generated · not evaluated'));
        board.append(card);
      }
    }else {
      const hint=el('div','ablation-hint','Click any state or action to open its written ablation map. Click the same step again to restore the original graph. All 14 steps have attached notes.');board.append(hint);
    }
    for(const p of layout.states) {
      const s=states.get(p.id),future=s.depth>sourceDepth;
      const b=button('',()=>ablateState(s.id),`state-card canonical ${s.id===selected?'selected':''} ${future?'reference-future':''} ${ablation?.alternatives[0].targetState===s.id?'rejoin-target':''}`);
      b.style.left=p.x+'px';b.style.top=p.y+'px';b.dataset.state=s.id;b.setAttribute('aria-pressed',String(s.id===selected));
      const action=stateAction(s.id);b.dataset.stepAction=action||'start';
      b.setAttribute('aria-label',action?`Remove ${action}: ${stateStepTitle(s.id)}`:'Starting assumptions: no proof step to remove');
      b.append(el('span','state-card-meta',`${s.label} · ${action?'after '+action:'starting state'}`),el('strong','',stateStepTitle(s.id)),el('small','',action?`${s.facts.length} results · click to remove ${action}`:'No proof step to remove'));
      board.append(b);
    }
    fit('state',layout.width,layout.height);
    $('state-status').textContent=ablation?'1 removed edge · 3 illustrative alternatives · 0 evaluations':'14 attached ablations · click a step to open / close';
  }
  function inspectAblation() {
    const active=isAblation();$('ablation-controls').hidden=!active;
    document.querySelector('.reference-panels').classList.toggle('ablation-layout',active);
    $('reference-note').textContent=active?'Click any original step to reveal its ablation map and full proof notes. Click that step again to return to the original graph. Each branch includes its written argument.':'The original proof. Choose Remove a step & branch to reveal an alternative without leaving the graph.';
    $('state-instructions').textContent=active?'Click a result node to remove the step that produced it; click again to restore.':'Select a state or a labeled action.';
    $('state-legend-note').textContent=active?'Green-grey = worked · red-grey = insufficient / invalid':'Other valid orders merge into shared states';
    $('restore-action').disabled=!ablation;$('export-ablation').disabled=!ablation;$('find-alternatives').disabled=!ablation;$('rejoin-control').hidden=!ablation;
    $('ablation-status').textContent=ablation?`${states.get(ablation.sourceState).label} · removed ${ablation.removedTransition.action}: ${P.byId[ablation.removedTransition.action].title}`:selected===G.initialState?'Starting assumptions have no step to remove. Click a result node to remove its named step.':'Click a step to open its ablation; click the same step again to restore the original.';
    const targets=$('rejoin-target');targets.replaceChildren();
    if(ablation)for(const id of ablation.eligibleTargets){const s=states.get(id),opt=el('option','',`${s.label} · ${s.closed?'Final goal by another route':s.frontierGoals.map(goalName).join(' + ')}`);opt.value=id;targets.append(opt);}
    if(ablation)targets.value=ablation.alternatives[0].targetState;
    const panel=$('alternative-inspector');panel.hidden=!ablation;
    if(!ablation)return;
    const a=ablation.alternatives.find(a=>a.id===selectedAlternative),content=$('alternative-detail');content.replaceChildren();
    $('alternative-title').textContent=a?`${a.name} · ${a.label}`:'Three possible endings after removing the action.';
    if(a){content.append(item('Illustrative outcome',a.description,a.ending==='success'?'success':'failure'),item('Evidence a future evaluation would need',a.evidenceRequired),el('p','',`Difficulty: ${a.difficultyDisplay}. This branch is a proposal for evaluation.`));}
    else content.append(el('p','','Select a grey branch to inspect its ending. The success branch can rejoin a later reference state or reach the final goal via a separate route.'));
    content.append(el('p','preview-caveat','These are presentation placeholders, not generated methods or findings. B is a finite budget with no assigned value. A finite timeout is not evidence of infinite difficulty. Rejoin links indicate intended mathematical compatibility, not reuse of the removed action.'));
  }
  function downloadGraph(graph,name) {
    const url=URL.createObjectURL(new Blob([JSON.stringify(graph,null,2)+'\n'],{type:'application/json'}));
    const a=el('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
  }
  function branchContext() {
    const alt=branchSelection.route==='moments',route=branchSelection.route,proof=alt?M:P,graph=alt?H:G;
    return {P:proof,G:graph,states:alt?momentStates:states,edges:alt?momentEdges:edges,
      goalName:id=>proof.nodes.find(n=>n.id===id).title,transition:branchSelection.edge,
      choose:(id,edge=null,focus=false)=>selectBranch(route,id,edge,focus),
      take:e=>selectBranch(route,e.to,e.id,true)};
  }
  function selectBranch(route,state,edge=null,focus=false) {
    stop();branchSelection={route,state,edge};render();if(focus){focusState();focusProof();}
  }
  function selectProofMove(route,event) {
    const graph=route==='moments'?H:G,proof=route==='moments'?M:P;
    if(event==='start'){selectBranch('original',G.initialState);return;}
    const i=proof.events.findIndex(e=>e.id===event);
    selectBranch(route,graph.canonicalStates[i+1],graph.canonicalTransitions[i],true);
  }
  function renderWorked() {
    $('ablation-controls').hidden=false;$('rejoin-control').hidden=true;$('ablation-legend').hidden=true;
    document.querySelector('.reference-panels').classList.remove('ablation-layout');
    $('ablation-evidence').textContent='SIGN REMOVED · WORKED ALTERNATIVE · SEARCH COST UNMEASURED';
    $('ablation-status').textContent='The upper-tail edge is removed. Click sign or the state labeled after sign again to restore the original graph.';
    for(const id of ['restore-action','export-ablation','find-alternatives'])$(id).disabled=false;
    $('export-ablation').textContent='Export both routes';
    $('reference-note').textContent='Both routes stay in the same graphs. Muted = original route retained for comparison; green-grey = worked replacement. Terminal states align on the theorem, not on identical proof histories.';
    $('state-instructions').textContent='Click a branch state or action to inspect it. Original state nodes remove the step named on that node.';
    $('state-legend-note').textContent='Green-grey = worked alternative · crossed edge = removed';
    $('proof-legend-note').textContent='Muted = original · green-grey = alternative';
    $('proof-instructions').textContent='Shared assumptions and endpoint; the new proof branches on the right.';
    $('fit-branches').textContent=proofOverview?'Readable size':'Fit both branches';
    $('alternative-inspector').hidden=false;
    $('alternative-inspector').querySelector('.eyebrow').textContent='WORKED BRANCH · MATHEMATICAL SUCCESS';
    $('alternative-title').textContent='Absolute moments bypass the sign reduction.';
    const detail=$('alternative-detail');detail.replaceChildren(item('Where this branch goes','Even moments → diagonal coefficient bounds and off-diagonal selector / Gaussian estimates → absolute Markov → Hanson–Wright.','success'),el('p','preview-caveat','This is the previously worked derivation. No new search was run, and no relative search cost or finite search budget is claimed. Other untested alternatives are not added as failed branches.'));
    appendNotes(detail,'sign');
    renderWorkedProof();renderWorkedStates();
    const ctx=branchContext(),s=ctx.states.get(branchSelection.state);
    // Only the displayed canonical route is navigable in this branch overlay.
    const next=ctx.G.canonicalTransitions.map(id=>ctx.edges.get(id)).find(e=>e.from===s.id);
    inspect({...s,availableActions:next?[next.action]:[]},ctx);
    $('selected-meta').textContent=`${branchSelection.route==='moments'?'Alternative':'Original reference'} · ${s.label} · ${s.depth} moves`;
    if(branchSelection.route==='original'&&s.id===worked.selectedState){$('selected-meta').textContent=`${s.label} · original state after sign · this step is removed`;$('closure-status').textContent='REFERENCE ONLY';$('state-context').textContent='This is the original upper-tail reduction retained for comparison. The replacement begins from the assumptions and does not inherit that reduction.';}
  }
  function renderWorkedProof() {
    const model=worked.proof,board=$('reference-proof-board'),map=new Map(model.nodes.map(n=>[n.id,n]));board.replaceChildren();
    const art=svg(model.width,model.height);board.append(art);
    for(const [title,x] of [['ORIGINAL · REMOVED STRATEGY',24],['ABSOLUTE MOMENTS · NEW BRANCH',704]]){const label=el('div','proof-lane-title',title);label.style.left=x+'px';label.style.width='580px';board.append(label);}
    function geometry(e) {
      const a=map.get(e.from),b=map.get(e.to);
      const ax=a.x+a.width/2,ay=a.y+a.height/2,bx=b.x+b.width/2,by=b.y+b.height/2;
      if(a.kind==='given'&&e.route==='moments')return `M ${a.x+a.width} ${ay} H 654 V ${by} H ${b.x}`;
      if(e.type==='match'&&a.x!==b.x){const rail=e.route==='moments'?986:306;return `M ${a.x+a.width} ${ay} H ${rail} V ${by} H ${b.x}`;}
      if(a.x===b.x&&Math.abs(ay-by)>320){const rail=a.x-12;return `M ${a.x} ${ay} H ${rail} V ${by} H ${b.x}`;}
      const down=by>ay;return curve({x:ax,y:down?a.y+a.height:a.y},{x:bx,y:down?b.y:b.y+b.height});
    }
    for(const e of model.links){
      const cls=e.removed?'removed-edge':e.route==='moments'?'worked-link':'reference-ghost';
      path(art,geometry(e),`reference-line ${e.type} ${cls}`);
      if(e.removed){const n=map.get(e.to),label=button('× sign removed',()=>ablateAction('sign'),'proof-removed-label');label.style.left=n.x+'px';label.style.top=n.y-37+'px';board.append(label);}
    }
    const context=branchContext(),action=context.edges.get(branchSelection.edge)?.action;
    for(const n of model.nodes){
      const shared=n.kind==='given'||n.id==='ultimate',alt=n.route==='moments';
      const active=shared?n.id==='ultimate'&&context.states.get(branchSelection.state).closed:n.route===branchSelection.route&&n.event===action;
      const b=button('',()=>n.id==='ultimate'?ablateAction('finish'):n.route==='original'&&n.event!=='start'?ablateAction(n.event):selectProofMove(n.route,n.event),`node ${n.kind} ${shared?'shared-proof':alt?'worked-proof':'reference-ghost'} ${active?'selected':''} ${n.route==='original'&&n.event===worked.removedAction?'ablated-move':''}`);
      b.style.left=n.x+'px';b.style.top=n.y+'px';b.style.width=n.width+'px';b.style.height=n.height+'px';b.dataset.route=n.route;b.dataset.proofNode=n.id;b.dataset.proofEvent=n.id==='ultimate'?'finish':n.event;
      b.append(el('span','node-kind',n.id==='ultimate'?'Shared theorem':n.label),el('span','node-title',n.title),el('span','node-formula',n.formula));
      b.title=`${alt?'Alternative':'Original'}: ${n.title}`;board.append(b);
    }
    sizeBoard('proof',model.width,model.height,proofOverview?Math.min(1,(viewportWidth('proof')-18)/model.width):.85);
    $('proof-status').textContent='One proof graph · shared assumptions and theorem · sign edge removed · alternative proof retained in full';
  }
  function renderWorkedStates() {
    const model=worked.state,board=$('reference-state-board'),map=new Map(model.nodes.map(n=>[n.id,n]));board.replaceChildren();
    const art=svg(model.width,model.height);board.append(art);
    for(const [text,x] of [['ORIGINAL REFERENCE',24],['NEW MOMENT BRANCH',354]]){const label=el('div','branch-lane-title',text);label.style.left=x+'px';label.style.top='195px';board.append(label);}
    for(const e of model.links){
      const a=map.get(e.from),b=map.get(e.to),alt=e.route==='moments';
      path(art,curve({x:a.x+105,y:a.y+100},{x:b.x+105,y:b.y}),`state-line ${e.removed?'removed-edge':alt?'worked-link':'reference-ghost'}`);
      const title=e.removed?'× sign removed':e.action;
      const label=button(title,()=>e.removed?ablateAction('sign'):alt?selectBranch('moments',e.to,e.id,true):ablateAction(e.action),`action-edge ${e.removed?'removed-action':alt?'worked-action':'reference-ghost'} ${branchSelection.edge===e.id?'selected':''}`);
      label.style.left=b.x+'px';label.style.top=(b.y-42)+'px';label.dataset.route=e.route;label.dataset.action=e.action;
      label.setAttribute('aria-label',e.removed?'Removed original sign action':`${alt?'Alternative':'Original'} action: ${e.action}`);board.append(label);
    }
    for(const n of model.nodes){
      const alt=n.route==='moments',s=(alt?momentStates:states).get(n.id),proof=alt?M:P;
      const b=button('',()=>alt?selectBranch('moments',n.id,n.index?H.canonicalTransitions[n.index-1]:null,true):ablateState(n.id),`state-card ${alt?'worked-state':'reference-ghost'} ${n.index===0?'shared-state':''} ${branchSelection.state===n.id?'selected':''}`);
      b.style.left=n.x+'px';b.style.top=n.y+'px';b.dataset.state=n.id;b.dataset.route=n.route;
      if(!alt){
        const action=stateAction(n.id);b.dataset.stepAction=action||'start';b.classList.toggle('ablated-state',n.id===worked.selectedState);
        b.setAttribute('aria-label',action?`${n.id===worked.selectedState?'Restore':'Remove'} ${action}: ${stateStepTitle(n.id)}`:'Starting assumptions: no proof step to remove');
        b.append(el('span','state-card-meta',`${s.label} · ${action?'after '+action:'shared start'}`),el('strong','',stateStepTitle(n.id)),el('small','',n.id===worked.selectedState?'This step is removed · click to restore':action?`Click to remove ${action}`:'No proof step to remove'));
      }else b.append(el('span','state-card-meta',`ALTERNATIVE · ${s.label}`),el('strong','',s.closed?'Have meets want ✓':s.frontierGoals.map(id=>proof.nodes.find(n=>n.id===id).title).join(' + ')),el('small','',`${s.facts.length} results · ${s.openGoals.length} open goals`));board.append(b);
    }
    const join=model.alignment;
    for(const [id,alt] of [[G.finalState,false],[H.finalState,true]]){
      const n=map.get(id);path(art,curve({x:n.x+105,y:n.y+100},{x:join.x+join.width/2,y:join.y}),`state-line ${alt?'worked-link':'reference-ghost'}`);
    }
    const card=button('',()=>selectBranch('moments',H.finalState,H.canonicalTransitions.at(-1),true),'theorem-alignment');
    Object.assign(card.style,{left:join.x+'px',top:join.y+'px',width:join.width+'px',height:join.height+'px'});
    card.append(el('span','state-card-meta','SAME THEOREM · DISTINCT PROOF STATES'),el('strong','','Hanson–Wright ✓'),el('small','','The alternative reaches the final goal.'));board.append(card);
    fit('state',model.width,model.height);
    $('state-status').textContent='Shared start → 2 visible routes → same final theorem · 1 removed edge';
  }
  let studyPositions=[];
  function noteInline(parent,text) {
    const pattern=/\[([^\]]+)\]\(([^)]+)\)|\*\*([^*]+)\*\*|`([^`]+)`/g;
    let offset=0;
    for(const match of text.matchAll(pattern)){
      parent.append(document.createTextNode(text.slice(offset,match.index)));
      if(match[1]){
        const target=match[2];
        if(/^https?:\/\//.test(target)){
          const link=el('a','',match[1]);link.href=target;link.target='_blank';link.rel='noopener noreferrer';parent.append(link);
        }else{
          const key=Object.keys(window.HansonWrightAblationNotes).find(key=>window.HansonWrightAblationNotes[key].path.split('/').at(-1)===target.split('/').at(-1));
          if(key)parent.append(button(match[1],()=>{
            const container=parent.closest('.reader-passage')||parent.closest('#reader-body')||$('alternative-detail');
            let note=container.querySelector(`[data-note-key="${key}"]`);
            if(!note){note=noteBlock(key,'Related proof note');container.append(note);}
            note.open=true;note.scrollIntoView({behavior:'smooth',block:'start'});
          },'note-link'));
          else parent.append(document.createTextNode(match[1]));
        }
      }else parent.append(el(match[3]?'strong':'code','',match[3]||match[4]));
      offset=match.index+match[0].length;
    }
    parent.append(document.createTextNode(text.slice(offset)));
  }
  function noteBlock(key,title){
    const note=window.HansonWrightAblationNotes[key],details=el('details','ablation-note');details.dataset.noteKey=key;
    details.append(el('summary','',title),el('p','source-label',`Source: proposals/${note.path}`));
    const text=el('div','ablation-note-text');
    // Only text and explicitly constructed links are rendered from the documents.
    for(const block of note.text.split(/\n\s*\n/)){
      if(/^ {4}/.test(block))text.append(el('pre','',block.replace(/^ {4}/gm,'')));
      else{
        const heading=/^#{1,6} /.test(block),part=el(heading?'h3':'p');
        noteInline(part,heading?block.replace(/^#{1,6} /,''):block);text.append(part);
      }
    }
    details.append(text);return details;
  }
  function appendNotes(parent,action) {
    for(const [key,title] of [[action,'Full ablation proof and analysis'],['common','Shared calculations, assumptions and boundary cases'],...(action==='sign'?[]:[['sign','Complete absolute-moment proof (shared dependency)']])])parent.append(noteBlock(key,title));
  }
  function studyLayout(x,y) {
    const replan=study.restart?[{title:'Replan from the original assumptions',have:'Independent, centered Xᵢ with ‖Xᵢ‖ψ₂≤K; fixed matrix A. No banned reference conclusions are inherited.',want:'Prove the whole Hanson–Wright theorem under the stated strategy ban.'}]:[];
    const rows=[...replan,...study.steps].map((node,i)=>({...node,id:'main-'+i,route:'main',x,y:y+i*185,width:300,height:145,status:study.status==='unresolved'?'unresolved':'worked'}));
    let nextY=y;
    for(const [i,c] of study.candidates.entries()){
      rows.push({...c,id:'candidate-'+i,route:'candidate',x:x+340,y:nextY,width:300,height:145,have:c.reason,want:'This candidate does not supply the required proof under the stated ban.'});nextY+=185;
    }
    for(const [j,route] of (study.additional||[]).entries()){
      nextY+=40;
      for(const [i,node] of route.steps.entries()){
        rows.push({...node,id:`additional-${j}-${i}`,route:'additional-'+j,routeTitle:route.title,x:x+340,y:nextY,width:300,height:145,status:'worked'});nextY+=185;
      }
    }
    return rows;
  }
  function selectStudyNode(node){studyNode=node;renderStudyDetail();syncReader();}
  function renderStudyDetail(){
    const detail=$('alternative-detail');detail.replaceChildren();
    $('alternative-inspector').hidden=false;
    $('alternative-inspector').querySelector('.eyebrow').textContent='WRITTEN ABLATION · SEARCH COST UNMEASURED';
    $('alternative-title').textContent=study.title;
    detail.append(item('Strategy removed',study.restriction),item('Branch scope',study.scope),el('p','preview-caveat',study.provenance+' Shared proof families are reused; these are not independent search successes.'));
    if(studyNode){
      const cls=studyNode.status==='worked'?'success':'failure';
      detail.append(item(studyNode.title,studyNode.have,cls),item('Want / remaining obligation',studyNode.want));
    }else detail.append(item(study.status==='worked'?'Worked replacement':'Sharp closure unresolved',study.status==='worked'?'The attached derivation proves the theorem under the stated ban, or recovers the specified checkpoint with its domain.':'Polarization currently gives a weaker estimate. This is neither theorem closure nor evidence of infinite search difficulty.',study.status==='worked'?'success':'failure'));
    appendNotes(detail,study.action);
  }
  function drawStudyBranches(kind,rows,source,join,width,height){
    const board=$(`reference-${kind}-board`),art=svg(width,height);art.classList.add('study-lines');board.append(art);
    const previous=new Map();
    for(const row of rows){
      const prev=previous.get(row.route),good=row.status==='worked';
      const from=prev?{x:prev.x+150,y:prev.y+145}:source;
      path(art,prev?curve(from,{x:row.x+150,y:row.y}):`M ${from.x} ${from.y} H ${row.x-18} V ${row.y+30} H ${row.x}`,`alternative-line ${good?'success':'failure'}`);
      // Rejected candidates are independent alternatives, not a sequence.
      if(row.route!=='candidate')previous.set(row.route,row);
      const card=button('',()=>{selectStudyNode(row);$('alternative-inspector').scrollIntoView({behavior:'smooth',block:'start'});},`study-card ${good?'success':'failure'}`);
      Object.assign(card.style,{left:row.x+'px',top:row.y+'px',width:row.width+'px',height:row.height+'px'});
      card.dataset.ablationNode=row.id;card.dataset.action=study.action;
      card.append(el('span','alternative-meta',row.route==='candidate'?row.status.toUpperCase():row.routeTitle|| (study.status==='unresolved'?'UNRESOLVED ROUTE':'WORKED DERIVATION')),el('strong','',row.title),el('small','',kind==='proof'?row.have:row.want));
      card.title=row.have+'\nWant: '+row.want;board.append(card);
    }
    for(const last of previous.values())if(last.status==='worked'){
      path(art,`M ${last.x+150} ${last.y+145} V ${last.y+162} H ${width-12} V ${join.y} H ${join.x}`,'alternative-line success reconnect');
    }
    const branchToggle=button('× '+study.action+' removed · click to restore',()=>ablateAction(study.action),'proof-removed-label');
    branchToggle.style.left=rows[0].x+'px';branchToggle.style.top=(rows[0].y-38)+'px';board.append(branchToggle);
    if(kind==='proof'){
      sizeBoard('proof',width,height,proofOverview?Math.min(1,(viewportWidth('proof')-18)/width):.85);
    }else fit(kind,width,height);
  }
  function renderStudy(){
    $('ablation-controls').hidden=false;$('rejoin-control').hidden=true;$('ablation-legend').hidden=true;
    document.querySelector('.reference-panels').classList.remove('ablation-layout');
    for(const id of ['restore-action','export-ablation','find-alternatives'])$(id).disabled=false;
    $('export-ablation').textContent='Export ablation';
    $('ablation-evidence').textContent=study.action.toUpperCase()+' REMOVED · WRITTEN ARGUMENT';
    $('ablation-status').textContent=`${states.get(study.selectedState).label} · ${study.action} removed. The replacement forks before this step, at ${states.get(study.sourceState).label}. Click the selected node again to restore.`;
    $('reference-note').textContent=study.scope;
    $('state-instructions').textContent='Click an original step to toggle its ablation. Branch boxes explain the replacement obligations.';
    $('proof-instructions').textContent='Original structure and replacement route share this canvas.';
    $('state-legend-note').textContent='Green-grey = worked · red-grey = insufficient / invalid';
    $('proof-legend-note').textContent='Dashed link = same theorem / recovered checkpoint; not identical proof history';
    $('fit-branches').textContent=proofOverview?'Readable size':'Fit both branches';
    renderProof(states.get(G.finalState));
    const original=proofNodes.get(P.byId[study.action].focus);
    const proofBoard=$('reference-proof-board');
    for(const node of proofBoard.querySelectorAll('.node'))node.classList.add('reference-ghost');
    // Event nodes remain clickable, including the crossed-out action itself.
    const originalButtons=[...proofBoard.querySelectorAll('.node')];
    P.nodes.forEach((n,i)=>{if(n.event===study.action||(study.action==='finish'&&n.id==='ultimate'))originalButtons[i].classList.add('ablated-move');});
    const label=button('× '+study.action+' removed · click to restore',()=>ablateAction(study.action),'proof-removed-label');
    label.style.left=original.x+'px';label.style.top=original.y-36+'px';proofBoard.append(label);
    const proofRows=studyLayout(704,Math.max(80,original.y));
    const proofJoin=study.rejoin?proofNodes.get('computed'):proofNodes.get('ultimate');
    drawStudyBranches('proof',proofRows,{x:original.x+240,y:original.y+55},{x:proofJoin.x+240,y:proofJoin.y+55},1390,Math.max(P.layout.height,...proofRows.map(n=>n.y+n.height+70)));
    $('proof-status').textContent=study.status==='unresolved'?'Weaker bound only · no justified rejoin or closure':study.rejoin?'Replacement recovers computed, including its domain → original downstream proof':'Worked replacement → same final theorem; reference intermediate goals may be bypassed';
    // Original state history stays intact; the removed edge remains visible and reversible.
    const board=$('reference-state-board');board.replaceChildren();
    statePositions=new Map(G.canonicalStates.map((id,i)=>[id,{x:24,y:30+i*205}]));
    const source=statePositions.get(study.sourceState);
    studyPositions=studyLayout(320,source.y+150);
    const width=1006,height=Math.max(G.canonicalStates.length*205+50,...studyPositions.map(n=>n.y+n.height+70));
    const art=svg(width,height);board.append(art);
    for(const id of G.canonicalTransitions){
      const edge=edges.get(id),a=statePositions.get(edge.from),b=statePositions.get(edge.to),removed=edge.action===study.action;
      path(art,curve({x:a.x+105,y:a.y+100},{x:b.x+105,y:b.y}),`state-line ${removed?'removed-edge':'reference-ghost'}`);
      const label=button((removed?'× ':'')+edge.action+(removed?' · restore':''),()=>ablateAction(edge.action),`action-edge ${removed?'removed-action':'canonical'}`);
      label.style.left=a.x+'px';label.style.top=a.y+115+'px';label.dataset.action=edge.action;label.setAttribute('aria-pressed',String(removed));board.append(label);
    }
    for(const [id,p] of statePositions){
      const state=states.get(id),card=button('',()=>ablateState(id),`state-card ${id===study.selectedState?'selected ablated-state':'reference-ghost'}`);
      Object.assign(card.style,{left:p.x+'px',top:p.y+'px'});card.dataset.state=id;
      const action=stateAction(id);card.dataset.stepAction=action||'start';card.setAttribute('aria-pressed',String(id===study.selectedState));
      card.setAttribute('aria-label',action?`${id===study.selectedState?'Restore':'Remove'} ${action}: ${stateStepTitle(id)}`:'Starting assumptions: no proof step to remove');
      card.append(el('span','state-card-meta',state.label+' · '+(action?'after '+action:'starting state')),el('strong','',stateStepTitle(id)),el('small','',id===study.selectedState?'This step is removed · click to restore':action?`Click to remove ${action}`:'No proof step to remove'));board.append(card);
    }
    const join=statePositions.get(study.rejoinState||G.finalState);
    drawStudyBranches('state',studyPositions,{x:source.x+210,y:source.y+50},{x:join.x+210,y:join.y+50},width,height);
    $('state-status').textContent=study.rejoin?'Checkpoint rejoin after compute · alternate history retained':study.status==='unresolved'?'No closure · sharp continuation unresolved · cost unmeasured':'Replanned route → same theorem, distinct proof history · cost unmeasured';
    inspect(states.get(study.selectedState));
    $('selected-meta').textContent=`${states.get(study.selectedState).label} · original state after ${study.action} · this step is removed`;
    $('closure-status').textContent='REFERENCE ONLY';
    $('state-context').textContent='These are the original results of the removed step, retained for comparison. The replacement forks from '+states.get(study.sourceState).label+' and does not inherit those results. '+states.get(study.selectedState).context.have;
    renderStudyDetail();
  }
  function item(title,text,cls='') {const n=el('article','state-item '+cls);n.append(el('strong','',title),el('p','reference-math',text));return n;}
  function inspect(s,ctx=currentContext()) {
    const {P,G,states,goalName,take}=ctx;
    $('selected-meta').textContent=`${s.label} · ${s.depth} of ${P.events.length} proof moves complete`;
    $('selected-title').textContent=s.closed?'Have meets want. The proof is closed.':s.depth===0?'Start from the assumptions.':`${s.frontierGoals.length} active goal${s.frontierGoals.length===1?'':'s'}, ${s.facts.length} established results.`;
    $('closure-status').textContent=s.closed?'CLOSED':'OPEN';$('state-context').textContent=s.context.have;
    $('state-notation').textContent=s.context.notation;$('state-scope').textContent=s.context.scope;
    const have=$('state-have');have.replaceChildren();for(const a of s.assumptions)have.append(item(a.title,a.statement,'assumption'));
    for(const f of s.facts){const n=item(f.title,f.statement);n.append(el('small','source-label',`Proof move: ${f.action}`));have.append(n);}
    const want=$('state-want');want.replaceChildren();
    if(s.closed)want.append(item('No remaining obligations',goalName('ultimate')+' follows after the final assembly.','closed'));
    for(const id of [...s.frontierGoals,...s.deferredGoals]) {
      const g=s.goals.find(g=>g.id===id), n=item(g.title,g.statement,'goal-item');
      const reduction=s.reductions.find(r=>r.parent===id);
      n.append(el('small','source-label',s.deferredGoals.includes(id)?'Waiting on reduced goals; final assembly may still be required.':'Active checkpoint · needs a closing inference.'));
      if(reduction){const d=el('details');d.append(el('summary','',`Reduction: ${reduction.action}`),el('p','reference-math',reduction.relation),el('p','',`Requires: ${reduction.children.map(goalName).join(' AND ')}`));n.append(d);}
      want.append(n);
    }
    if(s.closedGoals.length){const d=el('details');d.append(el('summary','',`${s.closedGoals.length} discharged checkpoints`));for(const id of s.closedGoals)d.append(el('p','',`✓ ${goalName(id)}`));want.append(d);}
    const actions=$('available-actions');actions.replaceChildren();
    for(const id of s.availableActions){const e=G.transitions.find(e=>e.from===s.id&&e.action===id);const b=button(`${P.byId[id].direction==='backward'?'↑':'↓'} ${P.byId[id].title}`,()=>isAblation()&&ctx.P===window.HansonWright?ablateAction(id):take(e));if(ablation?.removedTransition.id===e.id){b.disabled=true;b.textContent='× Removed in preview: '+P.byId[id].title;}actions.append(b);}
    if(!s.availableActions.length)actions.append(el('p','','All proof moves are complete.'));
    const index=G.canonicalStates.indexOf(s.id);$('reference-history').value=index>=0?index:s.depth;
    $('reference-position').textContent=index>=0?`${index} / ${P.events.length} · ${s.label}`:`Other order · ${s.label}`;
    inspectTransition(ctx);
  }
  function inspectTransition(ctx=currentContext()) {
    const {P,states,edges,transition,goalName,choose}=ctx;
    const panel=$('transition-content'), edge=edges.get(transition);panel.replaceChildren();
    if(!edge){$('transition-title').textContent='Select a labeled action to inspect the change.';return;}
    const action=P.byId[edge.action], from=states.get(edge.from),to=states.get(edge.to);
    $('transition-title').textContent=action.title;
    const links=el('div','transition-links');links.append(button(`← Before: ${from.label}`,()=>{stop();choose(from.id);focusState();}),el('span','',`${action.direction} · ${action.id}`),button(`After: ${to.label} →`,()=>{stop();choose(to.id,edge.id,true);}));panel.append(links);
    panel.append(el('p','',action.summary));
    const delta=el('div','transition-delta');
    delta.append(item('Added facts',edge.addedFacts.map(id=>to.facts.find(f=>f.id===id).title).join('\n')||'None — this action records a goal reduction.'),item('Introduced goals',edge.introducedGoals.map(goalName).join('\n')||'None'),item('Discharged goals',edge.dischargedGoals.map(goalName).join('\n')||'None'));
    panel.append(delta,item('Mathematical work',action.math),item('Verification',action.check),item('Toolkit',action.tool));
    const details=el('details');details.append(el('summary','','Move metadata & prerequisites'),el('p','',`Prerequisites: ${action.deps.join(', ')||'Starting assumptions only'}`),el('p','',`Proof nodes introduced: ${edge.addedProofNodes.join(', ')||'None; the endpoint closes.'}`),el('p','',`Observation: ${action.observation}`));panel.append(details);
  }
  function renderGraphs() {
    $('fit-branches').hidden=!(worked||study);
    $('replay-state').disabled=!!(worked||study);
    $('previous-state').disabled=!!(worked||study)||states.get(selected).depth===0;
    $('next-state').disabled=!!(worked||study)||states.get(selected).closed;
    document.querySelector('.reference-timeline').hidden=!!(worked||study);
    if(study){renderStudy();return;}
    if(worked){renderWorked();return;}
    $('ablation-evidence').textContent='REMOVE A STEP · EXPLORE A BRANCH';
    $('export-ablation').textContent='Export preview';
    $('ablation-legend').hidden=true;
    $('alternative-inspector').querySelector('.eyebrow').textContent='PROPOSED ALTERNATIVE';
    $('proof-legend-note').textContent=isAblation()?'Click a step to toggle its ablation':'The graph grows with each proof move';
    $('proof-instructions').textContent='Facts descend. Goals reduce upward.';
    const s=states.get(selected);inspectAblation();renderProof(isAblation()?states.get(G.finalState):s);renderGraph();inspect(s);
  }
  function readerContext(){
    if(study){
      let branch=study;
      if(studyNode?.route==='candidate')branch=null;
      else if(studyNode?.route.startsWith('additional-')){
        const extra=study.additional[Number(studyNode.route.split('-')[1])];
        branch={...study,...extra,status:'worked',candidates:[]};
      }
      return {action:study.action,branch};
    }
    if(worked)return {action:'sign',branch:{...window.HansonWrightAblationProofs.get('sign'),scope:'This complete absolute-moment argument starts from the same assumptions and reaches the same theorem. It does not inherit the original upper-tail checkpoints.'}};
    return {action:useOriginalGraph()?originalSelection:edges.get(transition)?.action||states.get(selected).completed.at(-1)||'start'};
  }
  function syncReader(){if(reader)reader.update(readerContext());}
  function focusReaderAction(action,reveal=false){
    stop();
    originalGraph?.pause();
    const index=P.events.findIndex(e=>e.id===action),stateId=index<0?G.initialState:G.canonicalStates[index+1];
    if(!worked&&!study&&!ablation)choose(stateId,index<0?null:G.canonicalTransitions[index]);
    for(const node of document.querySelectorAll('#reference-proof-board [data-proof-event]'))node.classList.toggle('reader-linked',node.dataset.proofEvent===action&&(node.dataset.route!=='moments'));
    for(const node of document.querySelectorAll('#reference-state-board [data-state]'))node.classList.toggle('reader-linked',node.dataset.state===stateId);
    const focusId=action==='start'?'independence':P.byId[action].focus;
    const proofPosition=worked?worked.proof.nodes.find(n=>n.id===focusId):proofNodes.get(focusId);
    const statePosition=worked?worked.state.nodes.find(n=>n.id===stateId):statePositions.get(stateId);
    if(proofPosition)focusAt('proof',proofPosition.x+120,proofPosition.y+55);
    if(statePosition)focusAt('state',statePosition.x+105,statePosition.y+50);
    if(reveal)document.querySelector('.reference-panels').scrollIntoView({behavior:'smooth',block:'start'});
  }
  function render(){
    const original=useOriginalGraph(),showOriginal=original&&graphView==='proof';
    if(original&&originalSelection!=='start'&&!states.get(selected).completed.includes(originalSelection))
      originalSelection=edges.get(transition)?.action||states.get(selected).completed.at(-1)||'start';
    document.querySelector('.reference-panels').dataset.originalActive=String(showOriginal);
    $('original-proof-explorer').hidden=!original;
    if(!showOriginal)originalGraph?.pause();
    renderGraphs();
    if(original&&originalGraph&&!receivingOriginal)originalGraph.setState(states.get(selected).completed,originalSelection);
    syncReader();
  }
  function receiveOriginalState({completed,action}){
    if(!originalGraph||!useOriginalGraph())return;
    const target=G.states.find(s=>s.completed.length===completed.length&&completed.every(id=>s.completed.includes(id)));
    if(!target)return;
    stop();selected=target.id;originalSelection=action;
    if(!canonical.has(target.id))$('graph-mode').value='all';
    transition=G.transitions.find(e=>e.to===target.id&&e.action===completed.at(-1))?.id||null;
    receivingOriginal=true;
    try {render();} finally {receivingOriginal=false;}
  }
  function focusVisibleGraph(){
    if(study){const row=studyNode||studyPositions[0];if(graphView==='state')focusAt('state',row.x+150,row.y+70);else {const n=proofNodes.get(P.byId[study.action].focus);focusAt('proof',854,Math.max(80,n.y)+35);}return;}
    if(graphView==='proof')focusProof();else focusState();
  }
  function switchGraph(view){
    graphView=view;
    document.querySelector('.reference-panels').dataset.graphView=view;
    for(const tab of document.querySelectorAll('[data-graph-view][role="tab"]')){
      const active=tab.dataset.graphView===view;tab.setAttribute('aria-selected',String(active));tab.tabIndex=active?0:-1;
      $(tab.getAttribute('aria-controls')).hidden=!active;
    }
    render();focusVisibleGraph();
  }
  for(const tab of document.querySelectorAll('[data-graph-view][role="tab"]')){
    tab.addEventListener('click',()=>switchGraph(tab.dataset.graphView));
    tab.addEventListener('keydown',event=>{
      if(!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;
      event.preventDefault();const view=event.key==='Home'?'proof':event.key==='End'?'state':graphView==='proof'?'state':'proof';
      $('graph-tab-'+view).focus();switchGraph(view);
    });
  }
  function changeZoom(multiplier){
    const v=$(`reference-${graphView}-viewport`),board=$(`reference-${graphView}-board`),wrapper=$(`reference-${graphView}-scale`);
    const old=Number(wrapper.dataset.scale),x=(v.scrollLeft+v.clientWidth/2)/old,y=(v.scrollTop+v.clientHeight/2)/old;
    zoom[graphView]=Math.min(2.5,Math.max(.35,zoom[graphView]*multiplier));
    sizeBoard(graphView,parseFloat(board.style.width),parseFloat(board.style.height),Number(wrapper.dataset.baseScale));
    const next=Number(wrapper.dataset.scale);v.scrollTo({left:x*next-v.clientWidth/2,top:y*next-v.clientHeight/2,behavior:'instant'});
  }
  $('graph-zoom-out').addEventListener('click',()=>changeZoom(1/1.2));
  $('graph-zoom-in').addEventListener('click',()=>changeZoom(1.2));
  $('graph-fit').addEventListener('click',()=>{zoom[graphView]=1;render();focusVisibleGraph();});
  $('graph-mode').addEventListener('change',()=>{stop();worked=null;branchSelection=null;ablation=null;selectedAlternative=null;study=null;studyNode=null;if($('graph-mode').value!=='all'&&!canonical.has(selected))chooseCanonical(states.get(selected).depth);else{render();focusState();}});
  $('restore-action').addEventListener('click',restoreAblation);
  $('find-alternatives').addEventListener('click',()=>{if(graphView!=='state')switchGraph('state');if(study){const p=studyPositions[0];focusAt('state',p.x+150,p.y+70);return;}if(worked){selectBranch('moments',H.canonicalStates[1],H.canonicalTransitions[0],true);return;}if(!ablation)return;const p=window.HansonWrightAblation.layout(G,ablation).alternatives[0],v=$('reference-state-viewport'),scale=Number($('reference-state-scale').dataset.scale);v.scrollTo({top:Math.max(0,p.y*scale-20),left:Math.max(0,(p.x+p.width/2)*scale-v.clientWidth/2),behavior:'instant'});});
  $('rejoin-target').addEventListener('change',()=>{if(ablation){ablation=window.HansonWrightAblation.create(G,ablation.sourceState,$('rejoin-target').value);selectedAlternative='alternative-a';render();}});
  $('export-ablation').addEventListener('click',()=>{if(study){downloadGraph({...study,notes:window.HansonWrightAblationNotes[study.action],common:window.HansonWrightAblationNotes.common},'hanson-wright-'+study.action+'-ablation.json');return;}if(worked){downloadGraph(worked,'hanson-wright-worked-ablation.json');return;}if(!ablation)return;const url=URL.createObjectURL(new Blob([JSON.stringify(ablation,null,2)+'\n'],{type:'application/json'}));const a=el('a');a.href=url;a.download='hanson-wright-ablation-preview.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
  $('reference-history').addEventListener('input',()=>{stop();chooseCanonical(Number($('reference-history').value));});
  $('reset-state').addEventListener('click',()=>{stop();$('graph-mode').value='canonical';chooseCanonical(0);for(const kind of ['proof','state'])$(`reference-${kind}-viewport`).scrollTo({top:0,left:0,behavior:'instant'});});
  $('previous-state').addEventListener('click',()=>{stop();chooseCanonical(Math.max(0,states.get(selected).depth-1));});
  $('next-state').addEventListener('click',()=>{stop();chooseCanonical(Math.min(P.events.length,states.get(selected).depth+1));});
  $('end-state').addEventListener('click',()=>{if(study){const last=studyPositions.filter(p=>p.route==='main').at(-1);selectStudyNode(last);focusAt('state',last.x+150,last.y+70);return;}if(worked){selectBranch('moments',H.finalState,H.canonicalTransitions.at(-1),true);return;}stop();chooseCanonical(P.events.length);});
  $('proof-focus').addEventListener('click',focusProof);$('state-focus').addEventListener('click',focusState);
  function play(){
    $('graph-mode').value='canonical';
    let i=G.canonicalStates.indexOf(selected);if(i<0||i===P.events.length)i=0;
    chooseCanonical(i);$('replay-state').textContent='Ⅱ Pause';
    timer=setInterval(()=>{chooseCanonical(++i);if(i===P.events.length)stop();},Number($('playback-speed').value));
  }
  $('replay-state').addEventListener('click',()=>{if(timer)stop();else play();});
  $('playback-speed').addEventListener('change',()=>{if(timer){stop();play();}});
  $('export-state').addEventListener('click',()=>{
    if(study){downloadGraph({...study,reference:G,notes:window.HansonWrightAblationNotes[study.action],common:window.HansonWrightAblationNotes.common},'hanson-wright-'+study.action+'-ablation.json');return;}
    if(worked){downloadGraph(worked,'hanson-wright-worked-ablation.json');return;}
    const url=URL.createObjectURL(new Blob([JSON.stringify(G,null,2)+'\n'],{type:'application/json'}));
    const a=el('a');a.href=url;a.download='hanson-wright-reference-state-graph.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
  });
  document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
  let resizeTimer;window.addEventListener('resize',()=>{clearTimeout(resizeTimer);resizeTimer=setTimeout(()=>{render();focusVisibleGraph();},150);});
  $('fit-branches').addEventListener('click',()=>{proofOverview=!proofOverview;render();if(!proofOverview)focusProof();});
  reader=window.HansonWrightProofReader.create({onSelect:focusReaderAction,noteBlock});
  // Keep a generous canvas even when the controls wrap. The reader uses the
  // same overall height, including the direction controls below the canvas.
  const workspace=$('proof-workspace'),panels=document.querySelector('.reference-panels');
  let alignmentFrame;
  function alignPanelHeight(){
    cancelAnimationFrame(alignmentFrame);
    alignmentFrame=requestAnimationFrame(()=>{
      if(window.matchMedia('(max-width:760px)').matches){workspace.style.removeProperty('--aligned-panel-height');return;}
      const viewport=panels.dataset.originalActive==='true'?$('viewport'):$(`reference-${graphView}-viewport`);
      if(!viewport.clientWidth)return;
      const controlsHeight=viewport.getBoundingClientRect().top-panels.getBoundingClientRect().top;
      const directionsHeight=panels.dataset.originalActive==='true'?panels.querySelector('.next-moves').getBoundingClientRect().height:0;
      const height=Math.ceil(Math.max(Math.min(1500,Math.max(1200,window.innerHeight*1.5)),controlsHeight+900+directionsHeight+1));
      const value=height+'px';
      if(workspace.style.getPropertyValue('--aligned-panel-height')!==value)workspace.style.setProperty('--aligned-panel-height',value);
    });
  }
  const panelResize=new ResizeObserver(alignPanelHeight);
  for(const node of [panels,...panels.querySelectorAll('.graph-switcher,.reference-controls,.reference-timeline,.map-toolbar,.map-pan-hint,.transport,.history-control,.next-moves,.reference-panel>header,.reference-legend,.reference-foot')])panelResize.observe(node);
  window.addEventListener('resize',alignPanelHeight);
  originalGraph=window.HansonWrightExplorer.create({
    root:$('original-proof-explorer'),embedded:true,
    onSelect(action){if(!originalGraph||!useOriginalGraph())return;originalSelection=action;syncReader();},
    onChange:receiveOriginalState
  });
  render();
})();
