(async function(){
'use strict';
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let data;try{const r=await fetch('paper-data.json');if(!r.ok)throw Error(`HTTP ${r.status}`);data=await r.json();Object.values(data.theorems).forEach(PaperModel.validate);}catch(e){$('#load-error').hidden=false;$('#load-error').textContent='The paper content could not load. Serve this folder through the project’s local web server and reload. '+e.message;return;}
const source=(ref,label)=>`<a class="source-link" href="${data.source}#page=${ref[0]}" target="_blank" rel="noopener">${esc(label||ref[1])} · p.${ref[0]} ↗</a>`;
const statusNames={insufficient:'Insufficient as stated',budget:'Weaker scale budget',equivalent:'Equivalent rephrasing'};
const prose=s=>esc(s).replace(/([A-Za-z0-9])\^\{([^}]+)\}/g,'$1<sup>$2</sup>');
const state={id:'A',count:0,selected:0,view:'proof',edition:'paper',branch:0,zoom:1,manualZoom:false};
let timer=null,materialTimer=null;
const theorem=()=>data.theorems[state.id];
function stop(){clearInterval(timer);timer=null;$('#play').textContent='▶ Play proof';}
function altHTML(s){const a=s.alternative;return `<div class="alternative-note ${a.status}"><span class="eyebrow">ALTERNATIVE CHECK · ${statusNames[a.status]}</span><h4>${esc(a.title)}</h4><p>${esc(a.reason)}</p><p><strong>Cost / limitation:</strong> ${esc(a.cost)}</p>${source(a.source)}<p class="caption">${a.status==='budget'?'Literature comparison from the supplied paper.':'Pedagogical counterfactual; not an executed search.'}</p></div>`;}
function route(){const hash=location.hash.slice(1);const id=['A','B'].includes(hash)?hash:null;stop();document.body.classList.toggle('paper-home',!id);if(id){state.id=id;state.count=0;state.selected=0;state.branch=0;state.manualZoom=false;$('#overview').hidden=true;$('#theorem-view').hidden=false;const t=theorem();$('#theorem-eyebrow').textContent=`THEOREM ${id} / ${t.short}`;$('#theorem-title').textContent=t.title;$('#theorem-meaning').textContent=t.meaning;$('#theorem-scope').textContent=t.scope;$('#theorem-formula').innerHTML=id==='A'?'Θ<sub>m</sub> ≤ 1 + σ<br>m ≥ ⌈C log₃(2 + ΠK<sub>Ψ</sub>)⌉':'Θ<sub>m₀+j</sub> − 1 ≤ 3<sup>−κj</sup><br>A(□<sub>m₀+j</sub>) → A<sub>∞</sub>';$('#statement-text').textContent=t.statement;$('#statement-source').href=`${data.source}#page=${t.page}`;$('#proof-source').href=`${data.source}#page=${t.proofpage}`;document.title=`Theorem ${id} · ${t.title}`;render();}else{$('#overview').hidden=false;$('#theorem-view').hidden=true;document.title='High contrast · A paper in two theorems';if(hash==='assumptions'){showIntroduction();$('#entry-context')?.setAttribute('open','');$('#assumptions').open=true;requestAnimationFrame(()=>$('#assumptions').scrollIntoView({block:'start'}));}}
$$('.paper-nav [data-view]').forEach(a=>{if(a.dataset.view===(id||'overview'))a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});if(hash==='paper-map'){requestAnimationFrame(()=>$('#paper-map').scrollIntoView({block:'start'}));}else if(hash!=='assumptions')window.scrollTo({top:0,behavior:'instant'});}
function renderReader(){const t=theorem(), note={paper:'A source-grounded summary of the paper’s proof stages, not a verbatim reproduction. Supporting propositions remain explicit toolkit dependencies.',full:'Every stage includes its motivation, verification, and an alternative check. These checks do not establish exhaustive irreplacability or measured search difficulty.',key:'Editorial highlights expand the main mechanisms. These selections are not the result of an exhaustive ablation study.'};$('#edition-note').textContent=note[state.edition];$$('[data-edition]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.edition===state.edition)));
$('#proof-reader').innerHTML=t.steps.map((s,i)=>{const expanded=state.edition==='full'||state.edition==='key'&&s.critical;return `<article id="passage-${i+1}" class="proof-passage ${state.selected===i+1?'selected':''}">${state.edition==='key'&&s.critical?'<span class="key-badge">EDITORIAL KEY STEP</span>':''}<h3><span class="step-number">${i+1}</span>${esc(s.title)}</h3><p>${prose(s.proof)}</p>${expanded?`<p><strong>Why this move?</strong> ${esc(s.observation)}</p><p>${prose(s.detail)}</p><details><summary>Selection, verification & protocol</summary><p><strong>Strategic selection:</strong> ${esc(s.move)}</p><p><strong>Verification:</strong> ${prose(s.verification)}</p><p>Direction: ${esc(s.direction)}. Observations motivate a selection; they are not additional facts. The graph lists established premises and outstanding obligations.</p></details>${altHTML(s)}`:''}<div class="passage-tools">${source(s.source)}<button data-select="${i+1}">Show move ${i+1} ↗</button></div></article>`;}).join('');
$$('[data-select]').forEach(b=>b.onclick=()=>{stop();state.branch=0;state.selected=Number(b.dataset.select);state.count=state.selected;render();focusGraph();});}
function renderDetail(snap){const idx=state.selected,s=theorem().steps[idx-1];if(!s){$('#node-detail').innerHTML='<span class="eyebrow">STARTING STATE</span><h3>Assumptions on one side. A theorem on the other.</h3><p>Play the reconstruction to see how facts are established and goals are reduced. Select a node for its current context and reasoning.</p>';return;}
const before=PaperModel.stateAt(theorem(),idx-1),after=PaperModel.stateAt(theorem(),idx);
$('#node-detail').innerHTML=`<span class="eyebrow">MOVE ${idx} · ${s.direction.toUpperCase()}</span><h3>${esc(s.title)}</h3><p>${esc(s.observation)}</p><div class="detail-buttons"><button id="branch-toggle">${state.branch===idx?'Restore original route':'Alternative check'}</button>${source(s.source)}</div>${state.branch===idx?`<p class="inline-warning">The original move is removed in this counterfactual view. Its dependent continuation is paused.</p>${altHTML(s)}`:''}<details><summary>Have / want, action & verification</summary><dl><dt>Have before this move</dt><dd>${before.facts.map(f=>esc(f.text)).join('<br>')}</dd><dt>Want before this move</dt><dd>${before.wants.map(g=>esc(g.text)).join('<br>')}</dd><dt>Choose</dt><dd>${esc(s.move)}</dd><dt>Verify</dt><dd>${prose(s.verification)}</dd><dt>Established facts after the original move</dt><dd>${after.facts.map(f=>esc(f.text)).join('<br>')}</dd><dt>Want after the original move</dt><dd>${after.wants.length?after.wants.map(g=>esc(g.text)).join('<br>'):'None: the established conclusion meets the theorem’s goal.'}</dd></dl></details>`;
$('#branch-toggle').onclick=()=>{stop();state.branch=state.branch===idx?0:idx;state.count=Math.max(state.count,idx);state.manualZoom=false;render();focusGraph(true);};}
function edge(a,b,kind='support',label=''){if(Math.abs(a.x-b.x)>100){const right=b.x>a.x, ax=right?a.x+a.w:a.x,bx=right?b.x:b.x+b.w,ay=a.y+a.h/2,by=b.y+b.h/2;return `<path d="M ${ax} ${ay} C ${(ax+bx)/2} ${ay}, ${(ax+bx)/2} ${by}, ${bx} ${by}" fill="none" stroke="${kind==='motivation'?'#b5965d':kind==='goal'?'#ab98bf':'#9374bb'}" stroke-width="1.6" ${kind==='motivation'?'stroke-dasharray="3 5"':''} marker-end="url(#arrow-${kind})"/>`;}const ax=a.x+a.w/2,ay=a.y+a.h,bx=b.x+b.w/2,by=b.y;const upward=by<ay;const y1=upward?a.y:ay,y2=upward?b.y+b.h:by;return `<path d="M ${ax} ${y1} C ${ax} ${(y1+y2)/2}, ${bx} ${(y1+y2)/2}, ${bx} ${y2}" fill="none" stroke="${kind==='motivation'?'#b5965d':kind==='goal'?'#ab98bf':'#9374bb'}" stroke-width="1.6" ${kind==='motivation'?'stroke-dasharray="3 5"':''} marker-end="url(#arrow-${kind})"/>${label?`<text x="${ax+14}" y="${(y1+y2)/2}" font-family="Arial,sans-serif" font-size="11" fill="#756584">${esc(label)}</text>`:''}`;}
function renderGraph(snap){const t=theorem(),nodes=[],edges=[],labels=[];let width=820,height;
const add=(id,x,y,w,h,kind,tag,title,body,idx)=>{const n={id,x,y,w,h,kind,tag,title,body,idx};nodes.push(n);return n;};
const find=id=>nodes.find(n=>n.id===id);
if(state.view==='proof'){
height=Math.max(900,(snap.count+1)*215+200);labels.push([22,'PROGRESS ↓'],[300,'OBSERVE → CHOOSE'],[574,'↑ GOALS']);
for(const f of snap.facts)add(f.id,20,75+f.at*215,250,140,'fact',f.at?`MOVE ${f.at} · VERIFIED RESULT`:'GIVENS',f.text,'',f.at);
for(const g of snap.goals){const ix=snap.goals.indexOf(g), y=height-170-ix*200;add('g-'+g.id,570,y,230,145,`goal ${g.status==='closed'?'closed':''}`,g.status==='closed'?'GOAL DISCHARGED':g.status==='reduced'?'REDUCED TO REQUIRED GOALS':'WANT',g.text,'',g.at);}
for(let i=0;i<snap.count;i++){const s=t.steps[i], y=75+(i+1)*215;const o=add('o-'+s.id,300,y,230,195,'observation',`OBSERVATION · MOVE ${i+1}`,s.title,s.observation.slice(0,155)+(s.observation.length>155?'…':''),i+1);if(s.fact){const f=find(s.fact[0]);s.uses.forEach(id=>edges.push(edge(find(id),f)));edges.push(edge(o,f,'motivation'));}else{edges.push(edge(find('g-root'),o,'motivation'));}for(const [id]of s.opens)edges.push(edge(find('g-root'),find('g-'+id),'goal'));}
for(const g of snap.goals)if(g.status==='closed'&&g.closedBy)edges.push(edge(find(g.closedBy),find('g-'+g.id)));
}else{
width=820;height=(snap.count+1)*240+100;labels.push([85,'STATE = HAVE + WANT'],[535,'ACTION / NEW STATE']);
for(let i=0;i<=snap.count;i++){const s=PaperModel.stateAt(t,i),last=s.facts.at(-1);const node=add('state-'+i,80,65+i*240,420,175,s.closed?'fact closed':'fact',i===0?'S₀ · INITIAL STATE':`S${i} · ${s.closed?'HAVE MEETS WANT':s.facts.length+' FACTS · '+s.wants.length+' OPEN GOALS'}`,i===0?'Begin with P1–P3':t.steps[i-1].title,`Have: ${last.text}\nWant: ${s.wants.length?s.wants.map(g=>g.text).join(' / '):'None — theorem closed.'}`,i);if(i>0)edges.push(edge(find('state-'+(i-1)),node,'support',`${i}. ${t.steps[i-1].direction}`));}
}
if(snap.branch){const b=snap.branch,s=t.steps[b.step-1];width=1100;height=Math.max(height,75+b.step*215+350);const start=state.view==='proof'?find(s.uses[0]):find('state-'+(b.step-1));const removed=add('removed',state.view==='proof'?20:80,75+b.step*(state.view==='proof'?215:240),250,145,'abandoned','REMOVED ORIGINAL MOVE',s.title,'Its conclusion is not assumed.',b.step);const alt=add('alternative',840,start.y+30,235,200,`branch ${b.status}`,'COUNTERFACTUAL BRANCH',b.title,statusNames[b.status]+' · '+(b.status==='equivalent'?'Can rejoin after the same inference; not an independent proof.':'This check does not close the theorem.'),b.step);edges.push(edge(start,alt,'goal'));height=Math.max(height,removed.y+220,alt.y+240);}
const markers=['support','goal','motivation'].map((k,i)=>`<marker id="arrow-${k}" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="${['#9374bb','#ab98bf','#b5965d'][i]}"/></marker>`).join('');
$('#graph-canvas').style.width=width+'px';$('#graph-canvas').style.height=height+'px';$('#graph-canvas').innerHTML=`<svg width="${width}" height="${height}" aria-hidden="true"><defs>${markers}</defs>${edges.join('')}</svg>${labels.map(([x,label])=>`<div class="graph-column-label" style="left:${x}px;top:25px">${label}</div>`).join('')}${nodes.map(n=>`<button class="graph-node ${n.kind} ${n.idx&&n.idx===state.selected?'current':''}" data-node="${esc(n.id)}" data-index="${n.idx}" style="left:${n.x}px;top:${n.y}px;width:${n.w}px;min-height:${n.h}px"><span class="node-tag">${esc(n.tag)}</span><strong>${esc(n.title)}</strong>${n.body?`<span class="node-body state-summary">${esc(n.body)}</span>`:''}</button>`).join('')}`;
$('#graph-canvas').dataset.width=width;$('#graph-canvas').dataset.height=height;
$$('[data-node]').forEach(b=>b.onclick=()=>{stop();state.selected=Number(b.dataset.index);if(!state.selected&&b.dataset.node==='g-root'){state.selected=1;}renderDetail(snap);renderReader();$$('.graph-node').forEach(n=>n.classList.toggle('current',Number(n.dataset.index)===state.selected&&state.selected>0));followReader();});
if(!state.manualZoom)state.zoom=defaultZoom();applyZoom();
}
function defaultZoom(){const fit=Math.min(1,($('#graph-scroll').clientWidth-12)/(state.view==='proof'?820:650));return innerWidth<=760?Math.max(.75,fit):fit;}
function applyZoom(){const canvas=$('#graph-canvas');canvas.style.transform=`scale(${state.zoom})`;$('#graph-size').style.width=Number(canvas.dataset.width)*state.zoom+'px';$('#graph-size').style.height=Number(canvas.dataset.height)*state.zoom+'px';}
function followReader(){if(!$('#follow').checked||!state.selected)return;const el=$('#passage-'+state.selected),reader=$('#proof-reader');if(el)reader.scrollTo({top:el.offsetTop-reader.offsetTop-12,behavior:'smooth'});}
function focusGraph(branch=false){const node=branch?$('#graph-canvas [data-node="alternative"]'):$('#graph-canvas .graph-node.current');if(!node)return;const sc=$('#graph-scroll');sc.scrollTo({top:Math.max(0,node.offsetTop*state.zoom-75),left:branch?node.offsetLeft*state.zoom-150:0,behavior:'smooth'});}
function render(){const snap=state.branch?PaperModel.branchAt(theorem(),state.branch):PaperModel.stateAt(theorem(),state.count);$('#proof-tab').setAttribute('aria-pressed',String(state.view==='proof'));$('#state-tab').setAttribute('aria-pressed',String(state.view==='state'));$('#graph-hint').textContent=state.view==='proof'?'Dotted arrows motivate; solid arrows support.':'Each arrow applies one verified move to a proof state.';$('#progress').textContent=`${snap.count} / ${theorem().steps.length} moves`;$('#timeline').value=snap.count;$('#previous').disabled=snap.count===0;$('#next').disabled=state.count===theorem().steps.length&&!state.branch;$('#closure').textContent=snap.branch?`Move ${snap.branch.step} removed · original continuation paused`:snap.closed?'Proof closed · all required goals discharged.':'The two sides are not connected yet.';$('#closure').classList.toggle('closed',snap.closed);$('.graph-panel').classList.toggle('branching',!!state.branch);renderGraph(snap);renderDetail(snap);renderReader();followReader();}
function advance(n){state.branch=0;state.count=Math.max(0,Math.min(theorem().steps.length,n));state.selected=state.count;render();focusGraph();if(state.count===theorem().steps.length)stop();}
$('#restart').onclick=()=>{stop();advance(0);$('#graph-scroll').scrollTo(0,0);};$('#previous').onclick=()=>{stop();advance((state.branch?state.branch-1:state.count)-1);};$('#next').onclick=()=>{stop();advance(state.branch?state.branch:state.count+1);};$('#complete').onclick=()=>{stop();advance(theorem().steps.length);};$('#play').onclick=()=>{if(timer){stop();return;}state.branch=0;if(state.count===theorem().steps.length)advance(0);$('#play').textContent='Ⅱ Pause';timer=setInterval(()=>advance(state.count+1),2600);};$('#timeline').oninput=e=>{stop();advance(Number(e.target.value));};$('#proof-tab').onclick=()=>{state.view='proof';state.manualZoom=false;render();focusGraph();};$('#state-tab').onclick=()=>{state.view='state';state.manualZoom=false;render();focusGraph();};$$('[data-edition]').forEach(b=>b.onclick=()=>{state.edition=b.dataset.edition;renderReader();followReader();});$('#zoom-in').onclick=()=>{state.manualZoom=true;state.zoom=Math.min(1.7,state.zoom+.15);applyZoom();};$('#zoom-out').onclick=()=>{state.manualZoom=true;state.zoom=Math.max(.35,state.zoom-.15);applyZoom();};$('#zoom-fit').onclick=()=>{state.manualZoom=true;state.zoom=Math.min(1,($('#graph-scroll').clientWidth-12)/Number($('#graph-canvas').dataset.width));applyZoom();$('#graph-scroll').scrollTo(0,0);};new ResizeObserver(()=>{if(!$('#theorem-view').hidden&&!state.manualZoom){state.zoom=defaultZoom();applyZoom();}}).observe($('#graph-scroll'));
const ingredients={
 assumptions:['P1–P3','The common hypotheses','Stationarity, finite-range dependence, and random-scale coarse ellipticity supply the probabilistic and energy control. The condition γ < 1 makes fine boundary contributions summable.',3],
 fixed:['§3 + Proposition 5.1','Initialize the histories','Subadditivity and independent-block averaging control fluctuation and mean histories. Their initial reduction costs logarithmically many scales and is performed once.',49],
 geometry:['§4','Transport between grids','Adapted geometry balances directional energies. Nearby-grid comparisons carry earlier estimates through a change of shape; startup may temporarily increase errors.',30],
 count:['Proposition 5.2','Select a good interval','The joint budget for logarithmic errors, geometric progress, and determinant losses finds the required interval in O(log contrast) scales.',53],
 closure:['Proposition 5.3','Close the gap','A comparison of primal and dual optimizer energies converts the selected inputs into a small gap, then transfers it to standard cubes.',60],
 iteration:['§6.1, (6.6)–(6.8)','Couple and contract','Variance is bounded by an earlier squared mismatch; an optimizer comparison turns it into a recurrence. Smallness absorbs the delayed square.',69],
 limit:['§6.1, final paragraphs','Identify the limit','Positive matrix bounds preserve invertibility. Vanishing primal–dual mismatch identifies the effective block and yields its Loewner error estimate.',70]
};
const paperSections={
 section2:['SECTION 2','Scale selection','An abstract selection argument counts logarithmic errors, geometric progress, and determinant loss together. It supplies the mechanism used in the global selection of Proposition 5.2.',11],
 section3:['SECTION 3','Fixed-grid estimates','Averaging, subadditivity, and mean-drift control give fluctuation estimates on a fixed grid. The retained histories are used in initialization and in comparisons between grids.',17],
 section4:['SECTION 4','Geometry update','The grid is gradually adjusted to the mean matrix. Comparisons carry the error histories between nearby grids and control the cost of the update.',30],
 section5:['SECTION 5','Closing the duality gap','Initialization and global selection produce an interval with suitable geometry and small errors. An optimizer comparison then closes the gap and transfers the result to Euclidean cubes.',47],
 C:['THEOREM C','Uniform-ellipticity PDE estimates','Under the uniform-ellipticity assumptions, Theorem C turns algebraic convergence into quantitative homogenization and regularity beyond a random radius. This theorem is shown for paper context; its full proof explorer has not been built.',5],
 D:['THEOREM D','Coarse-ellipticity PDE estimates','Theorem D gives quantitative PDE estimates under the paper’s coarse-ellipticity assumptions. Its random radius must also account for the original random scale. Read the statement and proof in the paper.',6]
};
let detailed=false, mapZoom=1, mapManualZoom=false, mapSelection=null;
function showIntroduction(){
 $('#map-detail-panel').hidden=true;$('#paper-welcome').hidden=false;
 $('#show-introduction').setAttribute('aria-pressed','true');
 $('#paper-reading-scroll').scrollTo(0,0);mapSelection=null;
 $$('[data-paper-node]').forEach(n=>n.classList.remove('selected'));
}
function selectPaperNode(id){
 const x=paperSections[id]||ingredients[id];if(!x)return;
 mapSelection=id;$('#paper-welcome').hidden=true;$('#map-detail-panel').hidden=false;
 $('#show-introduction').setAttribute('aria-pressed','false');
 $('#map-detail-panel').innerHTML=`<p class="eyebrow">${esc(x[0])}</p><h2>${esc(x[1])}</h2><p>${esc(x[2])}</p>${source([x[3],x[0]])}${id==='C'||id==='D'?'<p class="inline-warning">The local theorem explorers currently cover A and B. This node opens a source guide.</p>':`<div class="section-next"><p class="eyebrow">WHERE THIS LEADS</p><a href="#${id==='iteration'||id==='limit'?'B':'A'}" class="button primary">Open Theorem ${id==='iteration'||id==='limit'?'B':'A'} explorer ↗</a></div>`}<p class="caption">The arrows summarize selected proof dependencies. Supporting results remain linked to their full statements and proofs in the source paper.</p>`;
 $('#paper-reading-scroll').scrollTo(0,0);
 if(innerWidth<=760)$('.paper-reading-pane').scrollIntoView({block:'start',behavior:'smooth'});
 $$('[data-paper-node]').forEach(n=>n.classList.toggle('selected',n.dataset.paperNode===id));
}
function applyMapZoom(){
 const canvas=$('#dependency-map');canvas.style.transform=`scale(${mapZoom})`;
 $('#paper-map-size').style.width=760*mapZoom+'px';
 $('#paper-map-size').style.height=Number(canvas.dataset.height)*mapZoom+'px';
}
function fitPaperMap(){
 const box=$('#paper-map-scroll');
 mapZoom=Math.min(1,(box.clientWidth-24)/760);
 if(!detailed&&innerWidth>760)mapZoom=Math.min(mapZoom,(box.clientHeight-20)/Number($('#dependency-map').dataset.height));
 applyMapZoom();
}
function renderMap(){
 const nodes=[],edges=[];
 const add=(id,x,y,w,h,kind,tag,title)=>nodes.push({id,x,y,w,h,kind,tag,title});
 const join=(a,b)=>edges.push([a,b]);
 add('assumptions',265,20,230,64,'support','P1–P3','Common hypotheses');
 ['section2','section3','section4'].forEach((id,i)=>add(id,20+245*i,130,230,96,'section',paperSections[id][0],paperSections[id][1]));
 join('assumptions','section2');join('assumptions','section3');join('assumptions','section4');
 let fifthY=290;
 if(detailed){
  add('count',20,275,230,104,'support','PROP. 2.1 → PROP. 5.2','Joint selection budget');
  add('fixed',265,275,230,104,'support','§3 + PROP. 5.1','Initialize the histories');
  add('geometry',510,275,230,104,'support','§4','Transport the histories');
  join('section2','count');join('section3','fixed');join('section4','geometry');fifthY=440;
 }
 add('section5',265,fifthY,230,92,'section','SECTION 5','Closing the duality gap');
 (detailed?['count','fixed','geometry']:['section2','section3','section4']).forEach(id=>join(id,'section5'));
 let ay=fifthY+140;
 if(detailed){add('closure',265,ay,230,100,'support','PROPOSITION 5.3','Optimizer comparison & transfer');join('section5','closure');ay+=150;}
 add('A',265,ay,230,110,'theorem','THEOREM A · OPEN EXPLORER','Polynomial entry into small contrast');join(detailed?'closure':'section5','A');
 let by=ay+170;
 if(detailed){add('iteration',20,by,230,104,'support','§6.1 · (6.6)–(6.8)','Couple and contract');add('limit',510,by,230,104,'support','§6.1','Identify the limit');join('A','iteration');join('iteration','limit');by+=150;}
 add('B',265,by,230,110,'theorem','THEOREM B · OPEN EXPLORER','Algebraic convergence');
 if(detailed){join('iteration','B');join('limit','B');}else join('A','B');
 add('C',120,by+170,230,96,'context','THEOREM C · SOURCE GUIDE','Uniform ellipticity');
 add('D',410,by+170,230,96,'context','THEOREM D · SOURCE GUIDE','Coarse ellipticity');join('B','C');join('B','D');
 if(!detailed){
  const compact={assumptions:[265,5,230,60],section2:[20,100,230,86],section3:[265,100,230,86],section4:[510,100,230,86],section5:[265,225,230,80],A:[20,370,230,110],B:[265,370,230,110],C:[510,325,230,90],D:[510,455,230,90]};
  for(const n of nodes)[n.x,n.y,n.w,n.h]=compact[n.id];
 }
 const height=detailed?by+300:570, groupY=detailed?by-35:300,find=id=>nodes.find(n=>n.id===id);
 const paths=edges.map(([aid,bid])=>{const a=find(aid),b=find(bid);let ax=a.x+a.w/2,ay=a.y+a.h,bx=b.x+b.w/2,by=b.y;
  if(a.y===b.y||(b.x>a.x&&Math.abs(a.y-b.y)<150)){ax=a.x+a.w;ay=a.y+a.h/2;bx=b.x;by=b.y+b.h/2;return `<path d="M${ax},${ay} C${(ax+bx)/2},${ay} ${(ax+bx)/2},${by} ${bx},${by}"/>`;}
  return `<path d="M${ax},${ay} C${ax},${(ay+by)/2} ${bx},${(ay+by)/2} ${bx},${by}"/>`;
 }).join('');
 const nodeHTML=nodes.map(n=>{const common=`class="paper-dependency-node ${n.kind} ${mapSelection===n.id?'selected':''}" data-paper-node="${n.id}" style="left:${n.x}px;top:${n.y}px;width:${n.w}px;height:${n.h}px"`;const content=`<span>${esc(n.tag)}</span><strong>${esc(n.title)}</strong>${n.kind==='theorem'?'<b aria-hidden="true">↗</b>':''}`;return n.kind==='theorem'?`<a ${common} href="#${n.id}">${content}</a>`:`<button ${common}>${content}</button>`;}).join('');
 $('#dependency-map').className='paper-dependency-canvas';$('#dependency-map').dataset.height=height;$('#dependency-map').style.height=height+'px';
 $('#dependency-map').innerHTML=`<svg width="760" height="${height}" aria-hidden="true"><defs><marker id="paper-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="#ae9bc7"/></marker></defs><rect x="${detailed?80:250}" y="${groupY}" width="${detailed?600:500}" height="${detailed?320:260}" rx="10" fill="#f5f2f94d" stroke="#d7ccE5" stroke-dasharray="5 6"/><text x="${detailed?95:265}" y="${groupY+22}" font-family="Arial" font-size="11" letter-spacing="1" fill="#89779f">SECTION 6 · QUANTITATIVE HOMOGENIZATION</text><g fill="none" stroke="#ae9bc7" stroke-width="1.6" marker-end="url(#paper-arrow)">${paths}</g></svg>${nodeHTML}`;
 $$('button[data-paper-node]').forEach(b=>b.onclick=()=>selectPaperNode(b.dataset.paperNode));
 $('#map-main').setAttribute('aria-pressed',String(!detailed));$('#map-detail').setAttribute('aria-pressed',String(detailed));
 if(!mapManualZoom)fitPaperMap();else applyMapZoom();
}
$('#show-introduction').onclick=showIntroduction;
$('#map-main').onclick=()=>{detailed=false;mapManualZoom=false;renderMap();};
$('#map-detail').onclick=()=>{detailed=true;mapManualZoom=false;renderMap();};
$('#paper-map-minus').onclick=()=>{mapManualZoom=true;mapZoom=Math.max(.3,mapZoom-.15);applyMapZoom();};
$('#paper-map-plus').onclick=()=>{mapManualZoom=true;mapZoom=Math.min(1.8,mapZoom+.15);applyMapZoom();};
$('#paper-map-fit').onclick=()=>{mapManualZoom=false;fitPaperMap();$('#paper-map-scroll').scrollTo(0,0);};
new ResizeObserver(()=>{if(!$('#overview').hidden&&!mapManualZoom)fitPaperMap();}).observe($('#paper-map-scroll'));
renderMap();

// Deterministic block averaging is an explicitly labelled visual metaphor, not a homogenization solver.
const pixels=Array.from({length:32*20},(_,i)=>{const n=Math.sin(i*127.1+311.7)*43758.5453;return n-Math.floor(n);});
function drawMaterial(){const c=$('#material'),ctx=c.getContext('2d'),block=2**Number($('#scale').value);ctx.clearRect(0,0,c.width,c.height);const cols=32,rows=20,w=18,h=16,ox=32,oy=20;for(let y=0;y<rows;y+=block)for(let x=0;x<cols;x+=block){let sum=0,n=0;for(let yy=y;yy<Math.min(rows,y+block);yy++)for(let xx=x;xx<Math.min(cols,x+block);xx++){sum+=pixels[yy*cols+xx];n++;}const v=sum/n;ctx.fillStyle=`hsl(262 48% ${95-v*64}%)`;ctx.fillRect(ox+x*w,oy+y*h,Math.min(block,cols-x)*w-1.3,Math.min(block,rows-y)*h-1.3);}$('#scale-label').textContent=block===1?'Microscopic view':`${block} × ${block} visual blocks`;}
$('#scale').oninput=()=>{clearInterval(materialTimer);materialTimer=null;$('#animate-material').textContent='Animate';drawMaterial();};$('#animate-material').onclick=()=>{if(materialTimer){clearInterval(materialTimer);materialTimer=null;$('#animate-material').textContent='Animate';return;}$('#animate-material').textContent='Pause';materialTimer=setInterval(()=>{$('#scale').value=(Number($('#scale').value)+1)%5;drawMaterial();},1000);};document.addEventListener('visibilitychange',()=>{if(document.hidden){stop();clearInterval(materialTimer);materialTimer=null;$('#animate-material').textContent='Animate';}});drawMaterial();window.addEventListener('hashchange',route);route();
})();
