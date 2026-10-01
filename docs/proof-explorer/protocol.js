(() => {
  'use strict';
  const $=id=>document.getElementById(id);
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');
  const nodes=[
    {id:'given',kind:'fact',x:20,y:78,w:252,h:84,label:'FACT · GIVEN',text:'a and b are even integers',note:'Our starting assumptions.',at:0,detail:'A fact is an assumption or an established statement. These two assumptions are the roots of the forward graph.'},
    {id:'ultimate',kind:'goal',x:348,y:78,w:252,h:84,label:'GOAL · ULTIMATE',text:'a + b is even',note:'What the proof must establish.',at:0,detail:'A goal is an obligation, not an established fact. This endpoint remains open until a verified integer witness proves evenness.'},
    {id:'defined',kind:'fact',x:20,y:181,w:252,h:92,label:'FACT · DEFINITION',text:'a = 2m, b = 2n',note:'m,n ∈ ℤ; also a,b ∈ ℤ.',at:1,detail:'Unpacking the given evenness supplies integer witnesses m and n. Naming these existing witnesses is basic definition and logic; we have not selected a new witness for the conclusion.'},
    {id:'target',kind:'goal',x:348,y:181,w:252,h:105,label:'GOAL · DEFINITION',text:'Find k ∈ ℤ with a + b = 2k',note:'An equivalent reading of evenness.',at:1,detail:'The backward graph unpacks the original goal. This is a basic definition step: a+b is even exactly when it equals twice an integer.'},
    {id:'sum',kind:'fact',x:20,y:309,w:252,h:76,label:'FACT · CALCULATION',text:'a + b = 2m + 2n',note:'Substitute the given equalities.',at:2,detail:'Substitution is basic calculation. This expression is verified, but no integer witness k has yet been identified for the target.'},
    {id:'integer',kind:'fact',x:20,y:416,w:252,h:84,label:'FACT · LOGIC',text:'a + b ∈ ℤ',note:'Integer inputs → integer sum.',at:3,detail:'Apply the declared closure rule to the already known integers a and b. It establishes the domain of the sum, not its evenness.'},
    {id:'observation',kind:'observation',x:116,y:511,w:484,h:104,label:'OBSERVATION · MATCH THE TWO SIDES',text:'The target wants a factor 2. Both terms in 2m + 2n already contain that factor.',note:'Factoring could expose the missing witness.',at:5,detail:'An observation links what we have to what we need. It motivates trying 2(m+n) and k=m+n; the dashed connections express motivation, not a proved inference.'},
    {id:'newgoal',kind:'goal',x:348,y:638,w:252,h:110,label:'GOAL · REINTERPRETED',text:'a + b = 2(m + n)\nand m + n ∈ ℤ',note:'Sufficient, using the candidate k = m+n.',at:6,detail:'Choosing k=m+n turns an unspecified witness search into two concrete obligations. This is a sufficient-condition reduction of the existential goal; we do not claim that it is the only possible route.'},
    {id:'verified',kind:'fact',x:20,y:638,w:252,h:110,label:'FACT · VERIFIED',text:'2(m + n) = 2m + 2n\nand m + n ∈ ℤ',note:'Expansion + integer closure.',at:7,detail:'Expansion checks the chosen representation. Integer closure checks the candidate’s domain. Together with a+b=2m+2n, these established facts meet the new goal.'}
  ];
  const steps=[
    {phase:'basic',stage:'START / FACTS & GOALS',title:'Begin with what is known and what is needed.',focus:['given','ultimate'],html:'<p>The green <strong>fact node</strong> contains our assumptions. The purple <strong>goal node</strong> is the claim we still need to prove. They are deliberately separate.</p><p>The <strong>forward graph</strong> will grow by deriving facts. The <strong>backward graph</strong> will grow by asking what would suffice for the goal.</p>',rule:'<strong>Three node types</strong>Facts record what is known. Goals record what is needed. Observations will record the connection that suggests a move. We have not needed an observation yet.',caption:'Separate roots: assumptions on the left, the ultimate goal on the right.'},
    {phase:'basic',basic:['definition'],stage:'BASIC 1 / DEFINITIONS',title:'Unpack “even” on both sides.',focus:['defined','target'],html:'<p>By definition, an even integer is twice an integer. The givens supply m,n ∈ ℤ with a = 2m and b = 2n. The goal asks for an integer k with a + b = 2k.</p><div class="tour-example">Evenness ⇔ being twice an integer.</div><p>This adds a fact to the forward graph and a subgoal to the backward graph. <strong>Both actions are basic.</strong></p>',rule:'<strong>Basic type 1 · Definition</strong>Directly unpack or apply a definition already present in the assumptions or goal. Naming the witnesses supplied by an assumption does not invent a new construction.',caption:'Green arrows derive facts; purple arrows decompose goals. The definition gives an equivalence.'},
    {phase:'basic',basic:['calculation'],stage:'BASIC 2 / CALCULATION',title:'Calculate with the facts we have.',focus:['sum'],html:'<p>Substitute the established values of a and b into the sum.</p><div class="tour-example">a + b = 2m + 2n.</div><p>The new green node is a verified fact. No alternative representation has been chosen yet; we have only carried out the substitution.</p>',rule:'<strong>Basic type 2 · Calculation</strong>Execute direct elementary operations, such as substitution, expansion, or arithmetic simplification. Choosing a useful factorization is a separate action from checking it by expansion.',caption:'The forward graph grows through a direct calculation.'},
    {phase:'basic',basic:['logic'],stage:'BASIC 3 / LOGIC',title:'Apply a directly matching implication.',focus:['integer'],html:'<p>The definitions already give a,b ∈ ℤ. Our toolkit includes integer closure under addition:</p><div class="tour-example">a,b ∈ ℤ ⇒ a + b ∈ ℤ.</div><p>Its premise matches what we know, so we may add the conclusion as a fact. This tells us the sum is an integer. It does not yet tell us it is even.</p>',rule:'<strong>Basic type 3 · Logic</strong>Apply an explicit implication to established premises, unpack logical structure, or combine completed cases. Here the toolkit is integer closure; its direct application is basic logic.',caption:'The side branch records a valid fact that does not by itself close the evenness goal.'},
    {phase:'stuck',stage:'THE BASIC MOVES LEAVE A GAP',title:'We still have no witness k.',focus:['sum','target'],html:'<p>Our direct definition, calculation, and logic steps have left these two forms:</p><div class="tour-example">We have: 2m + 2n.<br>We need: 2k, with k ∈ ℤ.</div><p>More substitution or expansion in the current form does not select k. We are <strong>stuck at this gap</strong>, so now we look for an observation that can guide a strategic move.</p>',rule:'<strong>Priority: basic first → stuck</strong>“Stuck” is relative to this representation and the declared basic rules. It is not a claim that all mathematical reasoning has been exhausted or that the theorem is impossible.',caption:'Highlighted: the current expression and the target form. Integer membership alone is not enough.'},
    {phase:'observe',stage:'STRATEGY / MAKE AN OBSERVATION',title:'The shared factor matches the target.',focus:['sum','target','observation'],html:'<blockquote>“The goal wants twice an integer. Both summands in 2m + 2n contain the required factor 2. Factoring it out could give the desired form.”</blockquote><p>The amber <strong>observation node</strong> records this connection. It suggests trying 2(m + n), with k = m + n.</p><p>The observation explains why this move is worth trying. It has not yet verified the identity or the witness.</p>',rule:'<strong>Observation = target feature + available feature + connection</strong>We need a factor 2; both available terms contain 2; factoring may expose the needed witness. This selection is strategic even though it is elementary.',caption:'Dashed amber links are motivating connections, not proof inferences.'},
    {phase:'reinterpret',stage:'STRATEGY / REINTERPRET THE GOAL',title:'Turn “find k” into a concrete target.',focus:['observation','newgoal'],html:'<p>Guided by that observation, choose the candidate k = m + n. Instead of searching for an unspecified integer, seek two concrete statements:</p><div class="tour-example">a + b = 2(m + n),<br>m + n ∈ ℤ.</div><p>If both hold, this candidate proves the original existential goal. The new purple node is still an <strong>open goal</strong>.</p>',rule:'<strong>Reinterpreted goal · sufficient condition</strong>A goal reinterpretation changes what we try to establish. Record its logical relation: here the new obligations imply the old goal by supplying a witness. No equivalence or uniqueness is assumed.',caption:'The observation suggests the new target. The purple reduction records why that target would suffice.'},
    {phase:'resume',basic:['calculation','logic'],stage:'BASIC AGAIN / VERIFY THE CHOICE',title:'Now the elementary steps can finish it.',focus:['verified','newgoal'],html:'<p>The proposed form gives us something specific to check. Expand:</p><div class="tour-example">2(m + n) = 2m + 2n = a + b.</div><p>Since m,n ∈ ℤ, integer closure also gives m + n ∈ ℤ. Both obligations are now established as <strong>facts</strong>.</p><p>Selecting the factorization was strategic. Checking it by expansion and applying closure are basic again.</p>',rule:'<strong>Return to the basic rules</strong>Basic steps can occur anywhere in the proof. Record the strategic choice before its verification; saying “now factor” must not hide where the choice came from.',caption:'The verified facts match the reinterpreted goal, including the domain of the witness.'},
    {phase:'resume',basic:['logic','definition'],stage:'CONNECTION / THE GRAPHS MEET',title:'The verified witness closes the goal.',focus:['verified','newgoal','target','ultimate'],html:'<p>The forward graph supplies exactly what the backward graph requested: a + b = 2(m + n), and m + n is an integer.</p><p>Use k = m + n in the existential statement. By the definition of evenness, <strong>a + b is even</strong>. The green connection marks the completed proof.</p><div class="tour-example">Basic → stuck → observation →<br>new goal → basic verification.</div>',rule:'<strong>A goal closes only through verified support</strong>The observation motivated the route. The established equality and integer witness justify the conclusion. The graph keeps those two roles distinct.',caption:'Green closure links connect the verified facts to the goals they discharge.'}
  ];
  const edges=[
    {from:'given',to:'defined',kind:'fact',at:1,d:'M 146 162 L 146 181'},
    {from:'ultimate',to:'target',kind:'goal',at:1,d:'M 474 162 L 474 181'},
    {from:'defined',to:'sum',kind:'fact',at:2,d:'M 146 273 L 146 309'},
    {from:'defined',to:'integer',kind:'fact',at:3,d:'M 20 227 L 9 227 L 9 451 L 20 451'},
    {from:'sum',to:'observation',kind:'observation',at:5,d:'M 272 347 L 300 347 L 300 494 L 180 494 L 180 511'},
    {from:'target',to:'observation',kind:'observation',at:5,d:'M 474 286 L 474 511'},
    {from:'observation',to:'newgoal',kind:'observation',at:6,d:'M 474 615 L 474 638'},
    {from:'target',to:'newgoal',kind:'goal',at:6,d:'M 600 234 L 611 234 L 611 693 L 600 693'},
    {from:'sum',to:'verified',kind:'fact',at:7,d:'M 272 361 L 288 361 L 288 623 L 146 623 L 146 638'},
    {from:'defined',to:'verified',kind:'fact',at:7,d:'M 20 251 L 3 251 L 3 693 L 20 693'},
    {from:'verified',to:'newgoal',kind:'connect',at:8,d:'M 272 693 L 348 693'},
    {from:'newgoal',to:'target',kind:'connect',at:8,d:'M 600 715 L 616 715 L 616 255 L 600 255'},
    {from:'target',to:'ultimate',kind:'connect',at:8,d:'M 600 207 L 616 207 L 616 113 L 600 113'}
  ];
  const els=new Map(),edgeEls=[];
  let step=0,zoom=1,timer=null,playing=false;
  const ns='http://www.w3.org/2000/svg';
  for(const n of nodes){
    const button=document.createElement('button');button.type='button';button.id='tour-node-'+n.id;button.className='tour-node '+n.kind;button.hidden=true;
    Object.assign(button.style,{left:n.x+'px',top:n.y+'px',width:n.w+'px',height:n.h+'px'});
    for(const [cls,value] of [['tour-node-kind',n.label],['tour-node-text',n.text],['tour-node-note',n.note]]){const span=document.createElement('span');span.className=cls;span.textContent=value;span.style.whiteSpace='pre-line';button.append(span);}
    button.setAttribute('aria-label',n.label+': '+n.text);
    button.addEventListener('click',()=>{stop();for(const [id,el] of els)el.classList.toggle('is-focus',id===n.id);$('tour-rule').replaceChildren();const strong=document.createElement('strong');strong.textContent=n.label;$('tour-rule').append(strong,document.createTextNode(n.detail));});
    $('tour-nodes').append(button);els.set(n.id,button);
  }
  for(const edge of edges){const path=document.createElementNS(ns,'path');path.setAttribute('d',edge.d);path.setAttribute('class','tour-edge '+edge.kind);path.style.display='none';$('tour-edge-list').append(path);edgeEls.push(path);}
  steps.forEach((s,index)=>{const b=document.createElement('button');b.type='button';b.textContent=index+1;b.setAttribute('aria-label',`Step ${index+1}: ${s.title}`);b.addEventListener('click',()=>{stop();go(index);});$('tour-chapters').append(b);});
  function focusNodes(ids){
    const visible=nodes.filter(n=>ids.includes(n.id));
    if(!visible.length)return;
    const top=Math.min(...visible.map(n=>n.y)),bottom=Math.max(...visible.map(n=>n.y+n.h));
    const v=$('tour-viewport');
    // Keep the newly introduced content in view when a step spans both graphs.
    const target=bottom-top>v.clientHeight/zoom?bottom:((top+bottom)/2);
    if(top*zoom<v.scrollTop+10 || bottom*zoom>v.scrollTop+v.clientHeight-15){v.scrollTo({top:Math.max(0,target*zoom-v.clientHeight/2),behavior:reduced.matches?'instant':'smooth'});}
  }
  function render(){
    const s=steps[step];
    for(const n of nodes){const el=els.get(n.id),was=el.hidden;el.hidden=n.at>step;el.classList.toggle('is-focus',s.focus.includes(n.id));el.classList.toggle('is-new',was&&!el.hidden);el.classList.toggle('is-achieved',n.kind==='goal'&&(step===8||(step===7&&n.id==='newgoal')));}
    edges.forEach((e,i)=>{const el=edgeEls[i],was=el.style.display==='none';el.style.display=e.at<=step?'':'none';el.classList.toggle('is-new',was&&e.at<=step);});
    $('tour-stage').textContent=s.stage;$('tour-title').textContent=s.title;$('tour-count').textContent=`${step+1} / ${steps.length}`;
    // All HTML here is local, authored instructional content.
    $('tour-explanation').innerHTML=s.html;$('tour-rule').innerHTML=s.rule;
    $('tour-map-caption').textContent=s.caption;
    $('tour-gap').hidden=step>0;$('tour-stuck').hidden=step!==4;$('tour-complete').hidden=step!==8;
    $('tour-prev').disabled=step===0;$('tour-next').disabled=step===8;$('tour-next').textContent=step===8?'Complete ✓':'Next →';
    document.querySelectorAll('[data-phase]').forEach(el=>{const active=el.dataset.phase===s.phase;el.classList.toggle('is-active',active);if(active)el.setAttribute('aria-current','step');else el.removeAttribute('aria-current');});
    document.querySelectorAll('[data-basic]').forEach((el,i)=>{el.classList.toggle('tried',step>=i+1);el.classList.toggle('is-active',s.basic?.includes(el.dataset.basic)||false);});
    [...$('tour-chapters').children].forEach((b,i)=>{if(i===step)b.setAttribute('aria-current','step');else b.removeAttribute('aria-current');});
    focusNodes(s.focus);
  }
  function showTour(){document.querySelector('.tour-layout').scrollIntoView({block:'start',behavior:reduced.matches?'instant':'smooth'});}
  function go(index){step=Math.max(0,Math.min(steps.length-1,index));render();showTour();}
  function stop(){playing=false;clearTimeout(timer);timer=null;$('tour-play').textContent='▶ Play tour';}
  function schedule(){timer=setTimeout(()=>{if(!playing)return;go(step+1);if(step===steps.length-1)stop();else schedule();},9000);}
  $('tour-next').addEventListener('click',()=>{stop();go(step+1);});
  $('tour-prev').addEventListener('click',()=>{stop();go(step-1);});
  $('tour-reset').addEventListener('click',()=>{stop();go(0);$('tour-viewport').scrollTop=0;});
  $('tour-play').addEventListener('click',()=>{if(playing){stop();return;}if(step===steps.length-1)go(0);playing=true;$('tour-play').textContent='Ⅱ Pause';showTour();schedule();});
  const fit=()=>{zoom=Math.max(.65,Math.min(1,$('tour-viewport').clientWidth/620));$('tour-board').style.transform=`scale(${zoom})`;$('tour-scaled').style.width=620*zoom+'px';$('tour-scaled').style.height=835*zoom+'px';};
  new ResizeObserver(fit).observe($('tour-viewport'));
  document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});window.addEventListener('pagehide',stop);
  render();fit();
})();
