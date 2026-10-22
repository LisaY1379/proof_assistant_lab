/* Pure proof-state transitions. Observations and counterfactuals never add facts. */
(function(root, factory) { const api=factory(); if(typeof module==='object'&&module.exports) module.exports=api; else root.PaperModel=api; })(typeof globalThis!=='undefined'?globalThis:this, function(){
  'use strict';
  function stateAt(theorem, count) {
    count=Math.max(0,Math.min(theorem.steps.length,Math.floor(count)));
    const facts=[{id:'given',text:'P1–P3 · d ≥ 2 · γ ∈ [0,1)',at:0}], goals=[{id:'root',text:theorem.goal,status:'open',at:0}], actions=[];
    for(let i=0;i<count;i++) {
      const s=theorem.steps[i];
      for(const id of s.uses) if(!facts.some(f=>f.id===id)) throw Error(`Unavailable premise ${id} in ${s.id}`);
      if(s.opens.length){goals.find(g=>g.id==='root').status='reduced'; for(const [id,text] of s.opens) goals.push({id,text,status:'open',at:i+1});}
      if(s.fact) facts.push({id:s.fact[0],text:s.fact[1],at:i+1});
      for(const id of s.closes){const g=goals.find(g=>g.id===id);if(!g||g.status!=='open') throw Error(`Cannot discharge ${id} in ${s.id}`);g.status='closed';g.closedBy=s.fact?.[0];}
      actions.push(s.id);
    }
    const children=goals.filter(g=>g.id!=='root');
    const closed=children.length>0 && children.every(g=>g.status==='closed') && facts.some(f=>f.id==='result');
    if(closed){goals[0].status='closed';goals[0].closedBy='result';}
    return {count,facts,goals,actions,closed,wants:goals.filter(g=>g.status==='open')};
  }
  function branchAt(theorem,index){
    if(!Number.isInteger(index)||index<1||index>theorem.steps.length) throw Error('Invalid branch step');
    const state=stateAt(theorem,index-1), step=theorem.steps[index-1];
    return {...state,closed:false,branch:{step:index,removed:step.id,...step.alternative}};
  }
  function validate(theorem){
    const ids=new Set(['given']);
    for(const s of theorem.steps){
      if(!s.source||s.source[0]<1||s.source[0]>82) throw Error(`Invalid source ${s.id}`);
      if(!s.observation||!s.verification||!s.move||!s.alternative.source) throw Error(`Missing explanation ${s.id}`);
      if(s.fact){if(ids.has(s.fact[0])) throw Error('Duplicate fact');ids.add(s.fact[0]);}
    }
    const final=stateAt(theorem,theorem.steps.length);
    if(!final.closed||final.wants.length) throw Error('Unclosed proof');
    return true;
  }
  return {stateAt,branchAt,validate};
});
