(function(root) {
  'use strict';
  // Presentation fixtures only. No mathematical attempt or outcome is asserted.
  function create(graph,sourceId,targetId) {
    const index=graph.canonicalStates.indexOf(sourceId);
    if(index<0)throw Error('Choose a state in the reference order');
    if(index===graph.canonicalStates.length-1)return null;
    const eligibleTargets=graph.canonicalStates.slice(index+1);
    const target=targetId||eligibleTargets[Math.min(1,eligibleTargets.length-1)];
    if(!eligibleTargets.includes(target))throw Error('Rejoin target must be a future reference state');
    const removed=graph.transitions.find(e=>e.id===graph.canonicalTransitions[index]);
    const final=target===graph.finalState;
    return {
      schema:'hanson-wright-ablation-preview-v1', evaluationStatus:'not_run',
      sourceState:sourceId, removedTransition:{...removed}, eligibleTargets,
      scope:'One reference edge is visually removed. No global strategy prohibition or search is executed.',
      budget:{symbol:'B',finite:true,value:null,unit:null},
      alternatives:[
        {id:'alternative-a',name:'Alternative A',ending:'success',targetState:target,
          label:final?'Reach the final goal':'Rejoin a future state',symbol:'✓',
          description:final?'A different route reaches Hanson–Wright within a finite budget B.':'A different route recovers the mathematical obligations needed at the selected future state, within a finite budget B.',
          evidenceRequired:final?'A complete alternative argument under the original assumptions.':'Check the required facts, open goals and side conditions at the rejoin point. Matching one formula alone is insufficient.',
          difficultyDisplay:'Finite difficulty ≤ B · example',evaluation:null,measuredCost:null},
        {id:'alternative-b',name:'Alternative B',ending:'unbounded',targetState:null,
          label:'Infinite search difficulty',symbol:'∞',
          description:'An endless expansion demands infinitely many separate computations, with no available method to close the argument.',
          evidenceRequired:'Justify the structural obstruction. Running out of time or exceeding a finite budget alone does not establish infinite difficulty.',
          difficultyDisplay:'Unbounded work · example',evaluation:null,measuredCost:null},
        {id:'alternative-c',name:'Alternative C',ending:'diverged',targetState:null,
          label:'Diverged from the goal',symbol:'×',
          description:'The route reaches a different statement and provides no valid connection back to the required goal.',
          evidenceRequired:'Identify the lost assumption, mismatched conclusion or unsupported implication that prevents this route from proving the target.',
          difficultyDisplay:'Wrong destination · example',evaluation:null,measuredCost:null}
      ]
    };
  }
  function layout(graph,preview) {
    const sourceIndex=preview?graph.canonicalStates.indexOf(preview.sourceState):-1;
    const states=graph.canonicalStates.map((id,i)=>({id,x:36,y:30+i*205+(preview&&i>sourceIndex?360:0),width:210,height:100}));
    const source=states[sourceIndex];
    return {width:680,height:states.at(-1).y+140,states,
      alternatives:preview?preview.alternatives.map((a,i)=>({id:a.id,x:325,y:source.y+110+i*133,width:290,height:112})):[]};
  }
  const api={create,layout};
  if(typeof module==='object'&&module.exports)module.exports=api;else root.HansonWrightAblation=api;
})(typeof window==='undefined'?globalThis:window);
