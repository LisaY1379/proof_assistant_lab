(() => {
  'use strict';
  const data = JSON.parse(document.getElementById('proof-reference-data').textContent);
  const style = document.createElement('style');
  style.textContent = `
    .proof-panel { background:white; padding:18px 28px; border-bottom:1px solid #cbd5e1; }
    .proof-panel h2 { margin:0 0 8px; font-size:21px; }
    .proof-controls { display:flex; gap:10px; flex-wrap:wrap; align-items:center; margin:10px 0; }
    .proof-panel button { border:1px solid #cbd5e1; border-radius:8px; background:#f8fafc; padding:8px 12px; cursor:pointer; }
    .proof-panel button[aria-pressed=true] { background:#dbeafe; border-color:#2563eb; }
    .proof-order { display:flex; gap:8px; overflow:auto; padding:5px 0 12px; }
    .proof-order button { flex:0 0 210px; text-align:left; font-size:12px; }
    .proof-detail { padding:10px 14px; background:#eff6ff; border-radius:8px; line-height:1.5; }
    .proof-hint { font-size:13px; color:#475569; }
    .proof-canvas { position:relative; }
    .proof-node { position:absolute; width:310px; height:174px; border:1px solid #cbd5e1; border-left:5px solid #94a3b8; border-radius:12px; background:white; padding:12px; z-index:2; overflow:auto; cursor:pointer; }
    .proof-node.used { background:#eff6ff; border-color:#60a5fa; border-left-color:#2563eb; }
    .proof-node.proposed { background:#fff7ed; border-color:#fb923c; border-left-color:#ea580c; }
    .proof-node.selected { outline:4px solid #4f46e5; outline-offset:3px; }
    .proof-node.unused { opacity:.35; }
    .proof-node strong { display:block; font-size:14px; color:#0f172a; margin:4px 0; }
    .proof-node small { display:block; font-size:11px; color:#475569; line-height:1.4; }
    .proof-node .proof-badge { color:#1d4ed8; font-weight:700; font-size:12px; }
    .proof-node.proposed .proof-badge { color:#9a3412; }
    .proof-layer { position:absolute; inset:0; overflow:visible; pointer-events:none; z-index:3; }
    .proof-flow { fill:none; stroke:#6366f1; stroke-width:3; opacity:.55; }
    .proof-flow.selected { stroke:#4338ca; stroke-width:5; opacity:1; }
    .proof-step-label { font:bold 12px sans-serif; fill:#4338ca; paint-order:stroke; stroke:#f8fafc; stroke-width:5px; }
  `;
  document.head.appendChild(style);
  let panel;
  function showProof() {
    const key = new URLSearchParams(location.hash.slice(1)).get('proof');
    if (!key || !data.proofs[key]) return;
    if (panel) panel.remove();
    const ref = data.proofs[key], graph = data.graphs[key];
    if (!graph) return;
    const wrap = document.querySelector('.graph-wrap');
    const canvas = document.createElement('div'); canvas.className = 'proof-canvas';
    wrap.replaceChildren(canvas);
    const summary = document.querySelector('.summary');
    summary.textContent = 'Library relations are grey. Numbered purple arrows show proof order, not new library relations.';
    panel = document.createElement('section'); panel.className = 'proof-panel';
    wrap.before(panel);
    const title = document.createElement('h2'); title.textContent = 'Graph reference · ' + ref.title; panel.appendChild(title);
    const hint = document.createElement('div'); hint.className = 'proof-hint';
    hint.textContent = 'Blue: used library strategies. Orange: proposed new strategies (not added to the library). Order follows the annotated control proof. Repeated uses retain their separate step numbers.';
    panel.appendChild(hint);
    const controls = document.createElement('div'); controls.className = 'proof-controls'; panel.appendChild(controls);
    const button = (label, parent, click) => { const b=document.createElement('button'); b.type='button'; b.textContent=label; b.addEventListener('click',click); parent.appendChild(b); return b; };
    let mode = 'proof', current = 0;
    const compactButton = button('Proof path',controls,()=>{mode='proof';draw();});
    const fullButton = button('Full library',controls,()=>{mode='full';draw();});
    button('Previous step',controls,()=>select(Math.max(0,current-1),true));
    button('Next step',controls,()=>select(Math.min(ref.steps.length-1,current+1),true));
    const order = document.createElement('div'); order.className='proof-order'; panel.appendChild(order);
    const detail = document.createElement('div'); detail.className='proof-detail'; panel.appendChild(detail);
    const nodes = new Map(graph.nodes.map(n=>[n.id,{...n,key:n.id,proposed:false}]));
    const stepKeys = ref.steps.map((step,i)=>{
      if(step.kind==='library') {
        if(!nodes.has(step.node_id)) throw new Error('Unknown library strategy '+step.node_id);
        return step.node_id;
      }
      const id='proposed:'+i;
      nodes.set(id,{id,key:id,label:step.label,description:step.annotation,proposed:true}); return id;
    });
    const used = new Set(stepKeys), unique = [...used];
    const stepButtons = ref.steps.map((step,i)=>button((i+1)+'. '+nodes.get(stepKeys[i]).label,order,()=>select(i,true)));
    let cards = new Map();
    function select(index,scroll) {
      if(!ref.steps.length) {detail.textContent='No strategies were highlighted for this proof.';return;}
      current=index;
      cards.forEach((card,key)=>card.classList.toggle('selected',key===stepKeys[index]));
      stepButtons.forEach((b,i)=>b.setAttribute('aria-pressed',String(i===index)));
      const step=ref.steps[index], node=nodes.get(stepKeys[index]);
      detail.textContent='Step '+(index+1)+' · '+node.label+' — '+step.annotation;
      canvas.querySelectorAll('.proof-flow').forEach(p=>p.classList.toggle('selected',Number(p.dataset.from)===index||Number(p.dataset.to)===index));
      if(scroll) cards.get(stepKeys[index])?.scrollIntoView({behavior:'smooth',block:'center',inline:'center'});
    }
    function draw() {
      canvas.replaceChildren();cards=new Map();
      compactButton.setAttribute('aria-pressed',String(mode==='proof'));
      fullButton.setAttribute('aria-pressed',String(mode==='full'));
      const positions=new Map(); let width=1330,height=300;
      if(mode==='proof') {
        unique.forEach((key,i)=>{const row=Math.floor(i/3),col=row%2 ? 2-i%3:i%3;positions.set(key,{x:50+col*440,y:70+row*270});});
        height=Math.max(300,Math.ceil(unique.length/3)*270+50);
      } else {
        const levels=[...new Set(graph.nodes.map(n=>String(n.level??'unknown')))].sort((a,b)=>a.localeCompare(b,undefined,{numeric:true}));
        levels.forEach((level,col)=>graph.nodes.filter(n=>String(n.level??'unknown')===level).forEach((n,row)=>{
          positions.set(n.id,{x:50+col*440,y:70+row*230}); height=Math.max(height,70+row*230+230);
        }));
        const floating=unique.filter(key=>nodes.get(key).proposed);
        floating.forEach((key,i)=>positions.set(key,{x:50+levels.length*440,y:70+i*230}));
        width=Math.max(1330,50+(levels.length+(floating.length?1:0))*440);
        height=Math.max(height,70+floating.length*230);
      }
      canvas.style.width=width+'px';canvas.style.height=height+'px';
      const NS='http://www.w3.org/2000/svg';
      const svg=document.createElementNS(NS,'svg');svg.classList.add('proof-layer');svg.setAttribute('width',width);svg.setAttribute('height',height);
      const defs=document.createElementNS(NS,'defs'),marker=document.createElementNS(NS,'marker');
      marker.id='proof-arrow';marker.setAttribute('viewBox','0 0 10 10');marker.setAttribute('refX','9');marker.setAttribute('refY','5');marker.setAttribute('markerWidth','7');marker.setAttribute('markerHeight','7');marker.setAttribute('orient','auto');
      const tip=document.createElementNS(NS,'path');tip.setAttribute('d','M0 0 L10 5 L0 10z');tip.setAttribute('fill','#6366f1');marker.appendChild(tip);defs.appendChild(marker);svg.appendChild(defs);canvas.appendChild(svg);
      positions.forEach((p,key)=>{
        const n=nodes.get(key),card=document.createElement('div');card.className='proof-node '+(n.proposed?'proposed':used.has(key)?'used':'unused');
        card.style.left=p.x+'px';card.style.top=p.y+'px';card.dataset.nodeId=key;
        const badge=document.createElement('div');badge.className='proof-badge';
        badge.textContent=(n.proposed?'Proposed · ':'Library · ')+(used.has(key)?'Steps '+stepKeys.map((k,i)=>k===key?i+1:null).filter(Boolean).join(', '):'unused');
        const label=document.createElement('strong');label.textContent=n.label;
        const description=document.createElement('small');description.textContent=n.description||'';
        const id=document.createElement('small');id.textContent=n.proposed?'Floating proposal · not saved to library':n.id;
        card.append(badge,label,description,id);canvas.appendChild(card);cards.set(key,card);
        if(used.has(key)){card.tabIndex=0;card.setAttribute('role','button');card.addEventListener('click',()=>select(stepKeys.indexOf(key),false));card.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();select(stepKeys.indexOf(key),false);}});}
      });
      // Library relationships are a separate, muted layer.
      for(const edge of graph.edges||[]) {
        const a=positions.get(edge.source),b=positions.get(edge.target);if(!a||!b)continue;
        const path=document.createElementNS(NS,'path');path.setAttribute('d',`M${a.x+310} ${a.y+85} L${b.x} ${b.y+85}`);path.setAttribute('stroke','#94a3b8');path.setAttribute('opacity','.14');path.setAttribute('fill','none');svg.appendChild(path);
      }
      for(let i=0;i<stepKeys.length-1;i++) {
        const a=positions.get(stepKeys[i]),b=positions.get(stepKeys[i+1]);
        let d,tx,ty;
        if(stepKeys[i]===stepKeys[i+1]) {d=`M${a.x+310} ${a.y+45} C${a.x+405} ${a.y-10},${a.x+405} ${a.y+185},${a.x+310} ${a.y+130}`;tx=a.x+390;ty=a.y+85;}
        else if(a.y===b.y) {const forward=b.x>a.x;const x1=forward?a.x+310:a.x,x2=forward?b.x:b.x+310;d=`M${x1} ${a.y+85} L${x2} ${b.y+85}`;tx=(x1+x2)/2;ty=a.y+72;}
        else {const x1=a.x+155,y1=a.y+174,x2=b.x+155,y2=b.y;const mid=(y1+y2)/2;d=`M${x1} ${y1} C${x1} ${mid},${x2} ${mid},${x2} ${y2}`;tx=(x1+x2)/2+12;ty=mid;}
        const path=document.createElementNS(NS,'path');path.setAttribute('d',d);path.classList.add('proof-flow');path.dataset.from=i;path.dataset.to=i+1;path.setAttribute('marker-end','url(#proof-arrow)');svg.appendChild(path);
        const label=document.createElementNS(NS,'text');label.setAttribute('x',tx);label.setAttribute('y',ty);label.classList.add('proof-step-label');label.textContent=(i+1)+' → '+(i+2);svg.appendChild(label);
      }
      select(current,false);
    }
    draw();
  }
  window.addEventListener('hashchange',showProof);
  showProof();
})();
