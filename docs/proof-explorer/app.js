(() => {
  'use strict';
  const P=window.HansonWright, W=window.HansonWrightWritten, $=id=>document.getElementById(id);
  const L=P.layout;
  const nodeById=Object.fromEntries(P.nodes.map(n=>[n.id,n]));
  const nodeEls=new Map(), edgeEls=new Map();
  let history=[], cursor=0, selected='start', selectedNode=null, timer=null, playing=false;
  let zoom=1, clipTimers=[], clipRunning=false, fitted=true;
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');
  const done=()=>history.slice(0,cursor);
  const current=()=>cursor?P.byId[history[cursor-1]]:P.start;
  const svgNS='http://www.w3.org/2000/svg';
  const writtenEls=new Map();
  W.passages.forEach((passage,index)=>{
    const section=document.createElement('section');
    section.id='written-'+passage.id;
    section.className='proof-passage';
    section.dataset.number=String(index+1).padStart(2,'0');
    section.setAttribute('aria-label',`${index+1}. ${passage.title}`);
    // Only our authored, local proof markup is inserted here.
    section.innerHTML=passage.html;
    $('written-content').append(section);
    writtenEls.set(passage.id,section);
  });
  let writtenEvent='start';
  function syncWritten(eventId){
    const passage=W.byEvent[eventId];
    if(!passage)return;
    writtenEvent=eventId;
    const e=P.byId[eventId]||P.start;
    for(const [id,section] of writtenEls){
      const active=id===passage.id;
      section.classList.toggle('written-active',active);
      section.classList.toggle('written-backward',active&&e.direction==='backward');
      if(active)section.setAttribute('aria-current','step');else section.removeAttribute('aria-current');
    }
    const section=writtenEls.get(passage.id);
    const mode=e.direction==='backward'?'Planning':eventId==='start'?'Starting point':eventId==='finish'?'Concluding':'Deriving';
    $('written-position').textContent=`${mode} · ${section.dataset.number} / ${W.passages.length} · ${passage.title}`;
    if($('follow-proof').checked){
      const reader=$('written-scroll'),a=section.getBoundingClientRect(),b=reader.getBoundingClientRect();
      if(a.top<b.top+18 || a.bottom>b.bottom-18){
        reader.scrollTo({top:Math.max(0,reader.scrollTop+a.top-b.top-20),behavior:reduced.matches?'instant':'smooth'});
      }
    }
  }
  function nodeHeight(n){return n.kind==='given'?L.givenHeight:n.kind==='observation'?L.observationHeight:L.nodeHeight;}
  function point(id,side='center'){
    const n=nodeById[id], w=n.kind==='observation'?L.observationWidth:L.nodeWidth, h=nodeHeight(n);
    return {x:n.x+(side==='left'?0:side==='right'?w:w/2),y:n.y+(side==='top'?0:side==='bottom'?h:h/2)};
  }
  function curve(a,b){return `M ${a.x} ${a.y} C ${a.x} ${(a.y+b.y)/2}, ${b.x} ${(a.y+b.y)/2}, ${b.x} ${b.y}`;}
  function pathFor(from,to,type){
    // Route long side branches outside the cards they skip.
    const sideRoutes={'independence:expanded':12,'centered:expanded':18,'subgaussian:linear':292,'expanded:decoupled':8,'linear:replaced':282,'diagonal:diagonal-goal':12};
    const rail=sideRoutes[`${from}:${to}`];
    if(rail!==undefined){
      const side=rail<24?'left':'right',a=point(from,side),b=point(to,side);
      return `M ${a.x} ${a.y} L ${rail} ${a.y} L ${rail} ${b.y} L ${b.x} ${b.y}`;
    }
    const down=point(to).y>point(from).y;
    return curve(point(from,down?'bottom':'top'),point(to,down?'top':'bottom'));
  }
  for(const n of P.nodes){
    const b=document.createElement('button');b.className=`node ${n.kind}`;b.id=`node-${n.id}`;
    b.style.left=n.x+'px';b.style.top=n.y+'px';b.hidden=true;b.type='button';
    for(const [cls,text] of [['node-kind',n.label],['node-title',n.title],['node-formula',n.formula]]){
      const s=document.createElement('span');s.className=cls;s.textContent=text;b.append(s);
    }
    b.setAttribute('aria-label',`${n.label}: ${n.title}. ${n.formula}`);
    b.addEventListener('click',()=>{stop();cancelClip();selected=n.id==='ultimate'&&done().includes('finish')?'finish':n.event;selectedNode=n.id;showDetails(P.byId[selected]||P.start);renderSelection();});
    $('nodes').append(b);nodeEls.set(n.id,b);
  }
  for(const [from,to,type] of P.edges){
    const p=document.createElementNS(svgNS,'path');p.setAttribute('d',pathFor(from,to,type));p.setAttribute('class',`edge ${type}`);p.style.display='none';
    $('edge-paths').append(p);edgeEls.set(`${from}:${to}`,p);
  }
  function showDetails(e){
    selected=e.id;
    syncWritten(e.id);
    $('detail-type').textContent=e.direction==='start'?'STARTING POSITION':e.id==='finish'?'PROOF COMPLETE':e.direction==='backward'?'↑ BACKWARD · GOAL LAYER':'FORWARD ↓ PROGRESS LAYER';
    $('detail-category').textContent=e.category;
    for(const [suffix,key] of [['title','title'],['summary','summary'],['observation','observation'],['need','need'],['have','have'],['math','math'],['check','check'],['tool','tool']]) $('detail-'+suffix).textContent=e[key];
    $('return-current').hidden=selected===current().id;
    $('detail-type').style.background=e.direction==='backward'?'var(--goal-bg)':'var(--progress-bg)';
    $('detail-type').style.color=e.direction==='backward'?'var(--goal)':'var(--progress)';
  }
  function renderSelection(){for(const [id,el] of nodeEls){el.classList.toggle('selected',id===selectedNode);el.setAttribute('aria-pressed',String(id===selectedNode));}}
  function panTo(p){
    const v=$('viewport');
    v.scrollTo({left:Math.max(0,p.x*zoom-v.clientWidth/2),top:Math.max(0,p.y*zoom-v.clientHeight/2),behavior:reduced.matches?'instant':'smooth'});
  }
  function moveRunner(which,id){
    const el=$(which), n=nodeById[id]; if(!n)return;
    const p=point(id,which==='goal-runner'?'top':'bottom');
    el.style.left=p.x+'px';el.style.top=(p.y+(which==='goal-runner'?-11:10))+'px';el.classList.remove('joined');
  }
  function draw(animate=false){
    const active=done(),visible=P.visible(active),achieved=P.achieved(active),last=current();
    for(const n of P.nodes){
      const el=nodeEls.get(n.id),wasVisible=!el.hidden;el.hidden=!visible.has(n.id);
      el.classList.toggle('achieved',achieved.has(n.id));
      el.classList.remove('new-node','delayed');
      if(animate&&!wasVisible&&!el.hidden){el.classList.add('new-node');if(n.kind.startsWith('goal'))el.classList.add('delayed');}
      const suffix=achieved.has(n.id)?' — established':n.kind.startsWith('goal')?' — still required':'';
      el.setAttribute('aria-label',`${n.label}: ${n.title}${suffix}. ${n.formula}`);
    }
    for(const [from,to,type] of P.edges){
      const el=edgeEls.get(`${from}:${to}`),show=visible.has(from)&&visible.has(to),was=el.style.display!=='none';
      el.style.display=show?'':'none';el.classList.remove('new-edge');
      if(animate&&show&&!was)el.classList.add('new-edge');
    }
    $('initial-gap').hidden=cursor>0;
    $('step-counter').textContent=`${cursor} / ${P.events.length} moves`;
    $('timeline').max=history.length;$('timeline').value=cursor;
    $('history-position').textContent=cursor?`${cursor} of ${history.length}`:'Start';
    $('undo').disabled=!cursor;
    for(const direction of ['backward','forward']){
      const e=P.available(active,direction)[0];$(direction).disabled=!e;
      $(direction+'-label').textContent=e?e.title:(active.includes('finish')?'Every checkpoint is supported.':direction==='backward'?'Advance the facts to unlock a new goal.':'Decompose a goal to unlock the next deduction.');
      $(direction).dataset.next=e?.id||'';
    }
    $('move-hint').textContent=active.includes('finish')?'The two layers are connected. Select any checkpoint to inspect its reasoning.':'Choose either direction, or follow the guided thinking order.';
    const lastForward=[...active].reverse().map(id=>P.byId[id]).find(e=>e.direction==='forward'&&e.focus);
    const lastBack=[...active].reverse().map(id=>P.byId[id]).find(e=>e.direction==='backward'&&e.focus);
    if(lastForward)moveRunner('runner',lastForward.focus);else moveRunner('runner','subgaussian');
    moveRunner('goal-runner',active.includes('finish')?'ultimate':lastBack?.focus||'ultimate');
    selectedNode=last.focus||null;showDetails(last);renderSelection();renderJourney();
    $('board').classList.toggle('clip-complete',active.includes('finish'));
    if(last.focus)panTo(point(last.focus));
  }
  function renderJourney(){
    const list=$('journey-list');list.replaceChildren();
    if(!history.length){const s=document.createElement('span');s.className='empty-route';s.textContent='No moves yet.';list.append(s);return;}
    history.forEach((id,i)=>{
      const e=P.byId[id],b=document.createElement('button');b.className=e.direction+(i===cursor-1?' current':'');
      b.textContent=`${i+1} ${e.direction==='backward'?'↑':'↓'} ${e.title}`;b.setAttribute('aria-label',`Go to thinking step ${i+1}: ${e.title}`);
      b.addEventListener('click',()=>{stop();cancelClip();cursor=i+1;draw();});list.append(b);
    });
  }
  function apply(id,animate=true){
    if(!P.available(done()).some(e=>e.id===id))return false;
    history=history.slice(0,cursor);history.push(id);cursor++;cancelClip();draw(animate);
    if(id==='meet')meetingAnimation(false);
    if(id==='finish')meetingAnimation(true);
    return true;
  }
  function stop(){playing=false;clearTimeout(timer);timer=null;$('play').textContent='▶ Play thinking order';}
  function schedule(){
    if(!playing)return;
    timer=setTimeout(()=>{
      if(!playing)return;
      if(cursor<history.length){cancelClip();cursor++;draw(true);if(current().id==='meet')meetingAnimation(false);if(current().id==='finish')meetingAnimation(true);}
      else {const e=P.available(done())[0];if(!e){stop();return;}apply(e.id);}
      if(done().includes('finish'))stop();else schedule();
    },Number($('speed').value));
  }
  function showMap(){document.querySelector('.workspace').scrollIntoView({behavior:reduced.matches?'instant':'smooth',block:'start'});}
  function startPlayback(){
    if(playing){stop();return;}
    cancelClip();
    if(done().includes('finish')){history=[];cursor=0;draw();}
    playing=true;$('play').textContent='Ⅱ Pause';showMap();
    if(cursor<history.length){cursor++;draw(true);}else {const e=P.available(done())[0];if(e)apply(e.id);}
    schedule();
  }
  function cancelClip(){clipTimers.forEach(clearTimeout);clipTimers=[];clipRunning=false;$('meeting-paths').replaceChildren();$('meet-badge').hidden=true;$('runner').classList.remove('joined');$('goal-runner').classList.remove('joined');}
  function later(fn,ms){clipTimers.push(setTimeout(fn,reduced.matches?0:ms));}
  function glow(d){const p=document.createElementNS(svgNS,'path');p.setAttribute('d',d);p.setAttribute('class','meeting-glow');$('meeting-paths').append(p);}
  function meetingAnimation(final){
    cancelClip();clipRunning=true;
    syncWritten('meet');
    $('meet-badge').firstChild.textContent='THE TWO LAYERS MEET ';
    $('meet-badge').querySelector('span').textContent='The bound we derived is the bound we needed.';
    const r=$('runner'),g=$('goal-runner');
    const meeting={x:316,y:1210};
    const place=(el,p)=>{el.style.left=p.x+'px';el.style.top=p.y+'px';};
    const badge=$('meet-badge');
    badge.style.left='42px';badge.style.top=(meeting.y+35)+'px';
    place(r,point('bounded','right'));place(g,point('mgf','left'));panTo(meeting);
    glow(curve(point('bounded','right'),meeting));
    glow(curve(point('mgf','left'),meeting));
    later(()=>{place(r,meeting);place(g,meeting);},80);
    later(()=>{r.classList.add('joined');g.classList.add('joined');badge.hidden=false;},1250);
    if(final){
      const advance=(id,event)=>{
        syncWritten(event);
        const p=point(id,'left');p.x-=16;
        place(r,p);place(g,p);panTo(p);
      };
      later(()=>{
        badge.hidden=true;
        const a=point('mgf','left'),b=point('ultimate','left');
        glow(`M ${meeting.x} ${meeting.y} L 324 ${a.y} L 324 ${b.y} L ${b.x} ${b.y}`);
        advance('offtail','optimize');
      },3000);
      later(()=>advance('upper','split'),4200);
      later(()=>{
        syncWritten('bernstein');
        glow(pathFor('diagonal','diagonal-goal','match'));
        glow(curve(point('diagonal-goal','bottom'),point('ultimate','left')));
        place(r,point('diagonal-goal','bottom'));panTo(point('diagonal-goal'));
      },5400);
      later(()=>{
        advance('ultimate','finish');clipRunning=false;
        badge.style.top='1810px';badge.hidden=false;
        badge.firstChild.textContent='PROOF COMPLETE ';
        badge.querySelector('span').textContent='Both branches support the original endpoint.';
      },6650);
    }else{
      later(()=>{clipRunning=false;},2300);
    }
  }
  function setZoom(value){
    zoom=Math.max(.45,Math.min(1.65,value));
    $('board').style.transform=`scale(${zoom})`;
    $('scaled-board').style.width=(L.width*zoom)+'px';$('scaled-board').style.height=(L.height*zoom)+'px';
    $('zoom-out').disabled=zoom<=.45;$('zoom-in').disabled=zoom>=1.65;
  }
  function fit(){fitted=true;setZoom(Math.min(1.2,$('viewport').clientWidth/L.width));$('viewport').scrollLeft=0;$('viewport').scrollTop=0;}
  $('fit').addEventListener('click',fit);
  $('jump-start').addEventListener('click',()=>panTo({x:L.width/2,y:0}));
  $('jump-goal').addEventListener('click',()=>panTo(point('ultimate')));
  $('follow-proof').addEventListener('change',()=>syncWritten(writtenEvent));
  $('zoom-in').addEventListener('click',()=>{fitted=false;setZoom(zoom+.16);});
  $('zoom-out').addEventListener('click',()=>{fitted=false;setZoom(zoom-.16);});
  new ResizeObserver(()=>{if(fitted)fit();}).observe($('viewport'));
  $('restart').addEventListener('click',()=>{stop();cancelClip();history=[];cursor=0;draw();fit();});
  $('undo').addEventListener('click',()=>{stop();cancelClip();if(cursor)cursor--;draw();});
  $('play').addEventListener('click',startPlayback);
  $('speed').addEventListener('change',()=>{if(playing){clearTimeout(timer);schedule();}});
  for(const d of ['forward','backward'])$(d).addEventListener('click',()=>{stop();showMap();apply($(d).dataset.next);});
  $('timeline').addEventListener('input',()=>{stop();cancelClip();cursor=Number($('timeline').value);draw();});
  $('return-current').addEventListener('click',()=>{selectedNode=current().focus||null;showDetails(current());renderSelection();});
  $('clip').addEventListener('click',()=>{stop();cancelClip();history=P.events.map(e=>e.id);cursor=history.length;draw();fit();showMap();meetingAnimation(true);});
  document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
  window.addEventListener('pagehide',()=>{stop();cancelClip();});
  draw();fit();
})();
