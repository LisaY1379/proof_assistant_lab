(function(root){
  'use strict';
  // The two terminal states prove the same theorem, but their completed moves
  // and available facts are different. An alignment link is not a state merge.
  function create(original,reference,alternative,branch){
    const shared=new Set(['independence','centered','subgaussian','ultimate']);
    const proofId=(route,id)=>route==='original'||shared.has(id)?id:'moment:'+id;
    const height=Math.max(original.layout.height,alternative.layout.height)+220;
    const nodes=original.nodes.map(n=>({...n,route:'original',sourceId:n.id,
      ...(n.id==='ultimate'?{x:570,y:height-160}:{}),
      width:n.kind==='observation'?220:240,
      height:n.height??(n.kind==='given'?62:n.kind==='observation'?120:110)}));
    nodes.push(...alternative.nodes.filter(n=>!shared.has(n.id)).map(n=>({...n,
      id:proofId('moments',n.id),sourceId:n.id,route:'moments',x:n.x+680,
      width:n.kind==='observation'?220:240,height:n.height??(n.kind==='observation'?120:110)})));
    const links=[];
    for(const [route,proof] of [['original',original],['moments',alternative]]){
      for(const [from,to,type] of proof.edges.filter(e=>e[2]!=='inspiration'))links.push({
        from:proofId(route,from),to:proofId(route,to),type,route,
        removed:route==='original'&&from==='ultimate'&&to==='o-sign'
      });
      const meetings=proof.meetings||[['computed','scalar-goal'],['bounded','mgf'],['tail','offtail'],['diagonal','ultimate'],['tail','ultimate']];
      for(const [from,to] of meetings)links.push({from:proofId(route,from),to:proofId(route,to),type:'match',route,removed:false});
    }
    const stateNodes=[{id:reference.initialState,route:'original',index:0,x:189,y:50,width:210,height:100}];
    for(const [route,graph,x] of [['original',reference,24],['moments',branch,354]]){
      graph.canonicalStates.slice(1).forEach((id,i)=>stateNodes.push({id,route,index:i+1,x,y:250+i*205,width:210,height:100}));
    }
    const stateLinks=[];
    for(const [route,graph] of [['original',reference],['moments',branch]]){
      graph.canonicalTransitions.forEach((id,i)=>{
        const e=graph.transitions.find(e=>e.id===id);
        stateLinks.push({...e,route,from:i===0?reference.initialState:e.from,removed:route==='original'&&i===0});
      });
    }
    const bottom=Math.max(...stateNodes.map(n=>n.y+n.height))+130;
    return {
      schema:'hanson-wright-worked-ablation-v1',removedAction:'sign',
      sourceState:reference.initialState,
      selectedState:reference.canonicalStates[1],
      restriction:'Bypass the sign / upper-tail strategy throughout the alternative proof.',
      evidence:'Worked mathematical derivation; not a fresh search trial or formal certificate.',
      cost:{measured:false,reason:'No comparative search cost or finite search budget has been measured.'},
      reference,branch,
      alignment:{referenceState:reference.finalState,branchState:branch.finalState,kind:'same-theorem',mergedState:false,
        statement:alternative.stateConfig.goalStatements.ultimate},
      proof:{width:1320,height,nodes,links},
      state:{width:600,height:bottom+160,nodes:stateNodes,links:stateLinks,
        alignment:{id:'theorem-alignment',x:150,y:bottom,width:300,height:110}}
    };
  }
  const api={create};
  if(typeof module==='object'&&module.exports)module.exports=api;else root.HansonWrightWorkedAblation=api;
})(typeof window==='undefined'?globalThis:window);
