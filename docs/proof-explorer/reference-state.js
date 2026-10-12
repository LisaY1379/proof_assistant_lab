(function (root) {
  'use strict';
  const original = typeof module === 'object' && module.exports ? require('./proof.js') : root.HansonWright;
  // These annotate the existing checkpoints; they do not introduce new proof moves.
  // Refinement is sufficient-condition reduction, not automatic goal discharge.
  const originalRefinements = [
    {action:'sign', parent:'ultimate', children:['upper']},
    {action:'split', parent:'upper', children:['diagonal-goal','offtail']},
    {action:'exponential', parent:'offtail', children:['mgf']},
    {action:'gaussian', parent:'mgf', children:['gaussian-goal']},
    {action:'rotate', parent:'gaussian-goal', children:['scalar-goal']}
  ];
  const originalGoalStatements = {
    ultimate:'ℙ(|Q| ≥ t) ≤ 2 exp[−c min{t²/V, t/L}], for every real A and t ≥ 0.',
    upper:'ℙ(Q ≥ t) ≤ C exp[−c min{t²/V, t/L}], uniformly over real A (including −A).',
    'diagonal-goal':'ℙ(D ≥ t/2) ≤ exp[−c min{t²/V, t/L}].',
    offtail:'ℙ(S ≥ t/2) ≤ exp[−c min{t²/V, t/L}].',
    mgf:'𝔼 exp(λS) ≤ exp(CVλ²), for 0 < λ ≤ c₀/L.',
    'gaussian-goal':'𝔼 exp(θgᵀAg′) ≤ exp(θ²‖A‖F²), for |θ| ≤ 1/(√2‖A‖); g,g′ independent standard Gaussians.',
    'scalar-goal':'Bound ∏ᵢ 𝔼 exp(θsᵢgᵢgᵢ′) by exp(θ²Σᵢsᵢ²), retaining |θ|maxᵢsᵢ ≤ 1/√2.'
  };
  // Each proof supplies its own obligations, reductions and provenance.
  function create(P, config={}) {
  const refinements=config.refinements || originalRefinements;
  const goalStatements=config.goalStatements || originalGoalStatements;
  function ordered(done) { return P.events.filter(e=>done.includes(e.id)).map(e=>e.id); }
  // IDs depend on source event IDs, not traversal order or a generated sequence number.
  function stateId(done) { return (config.statePrefix || 'state:') + (ordered(done).join('+') || 'start'); }
  function snapshot(done) {
    if(new Set(done).size !== done.length || done.some(id=>!P.byId[id])) throw Error('Invalid completed moves');
    if(done.some(id=>P.byId[id].deps.some(dep=>!done.includes(dep)))) throw Error('Missing prerequisite');
    const completed = ordered(done), visible = P.visible(completed), achieved = P.achieved(completed);
    const goals = P.nodes.filter(n=>n.kind.startsWith('goal') && visible.has(n.id)).map(n=>({
      id:n.id, title:n.title, statement:goalStatements[n.id], closed:achieved.has(n.id)
    }));
    const openGoals = goals.filter(g=>!g.closed).map(g=>g.id);
    const reductions = refinements.filter(r=>completed.includes(r.action));
    const deferredGoals = reductions.filter(r=>openGoals.includes(r.parent) && r.children.some(id=>openGoals.includes(id))).map(r=>r.parent);
    return {
      id:stateId(completed), completed, depth:completed.length,
      assumptions:P.nodes.filter(n=>n.kind==='given').map(n=>({id:n.id,title:n.title,statement:n.formula})),
      context:{have:P.start.have, notation:P.start.math, scope:P.start.check},
      facts:completed.filter(id=>P.byId[id].direction==='forward').map(id=>({
        id:'fact:'+id, action:id, proofNodes:P.byId[id].add.filter(n=>P.nodes.find(x=>x.id===n).kind==='progress'),
        title:P.byId[id].title, statement:P.byId[id].math, verification:P.byId[id].check
      })),
      goals, openGoals, closedGoals:goals.filter(g=>g.closed).map(g=>g.id),
      frontierGoals:openGoals.filter(id=>!deferredGoals.includes(id)), deferredGoals,
      reductions:reductions.map(r=>({...r,children:[...r.children],relation:P.byId[r.action].math})),
      visibleProofNodes:P.nodes.filter(n=>visible.has(n.id)).map(n=>n.id),
      availableActions:P.available(completed).map(e=>e.id),
      closed:achieved.has('ultimate') && openGoals.length===0
    };
  }
  function difference(after,before) { return after.filter(x=>!before.includes(x)); }
  function build() {
    const first=snapshot([]), states=[first], known=new Map([[first.id,first]]), transitions=[];
    for(let i=0;i<states.length;i++) {
      const from=states[i];
      for(const action of from.availableActions) {
        const to=snapshot([...from.completed,action]);
        if(!known.has(to.id)) {known.set(to.id,to);states.push(to);}
        transitions.push({id:from.id+'->'+action, from:from.id, to:to.id, action,
          addedFacts:difference(to.facts.map(f=>f.id),from.facts.map(f=>f.id)),
          introducedGoals:difference(to.goals.map(g=>g.id),from.goals.map(g=>g.id)),
          dischargedGoals:difference(to.closedGoals,from.closedGoals),
          addedProofNodes:difference(to.visibleProofNodes,from.visibleProofNodes)
        });
      }
    }
    const canonicalStates=[first.id], canonicalTransitions=[], done=[];
    for(const e of P.events) {
      canonicalTransitions.push(stateId(done)+'->'+e.id); done.push(e.id); canonicalStates.push(stateId(done));
    }
    return {
      schema:config.schema || 'hanson-wright-reference-states-v1', source:config.source || 'proof.js',
      interpretation:config.interpretation || 'Dependency-valid execution orders of the reference proof; not recorded searches, alternative strategies, or a formally verified proof.',
      mergeRule:config.mergeRule || 'Same completed reference moves. Mathematical equivalence of different moves is not inferred; history-dependent motivations are not merged into the state.',
      cost:config.cost || {measured:false,reason:'No search was run. State depth counts reference moves, not difficulty or computational cost.'},
      initialState:first.id, finalState:canonicalStates.at(-1), canonicalStates, canonicalTransitions,
      actions:P.events.map(e=>({...e,deps:[...e.deps],add:[...e.add]})), states, transitions
    };
  }
  return {build,snapshot,stateId,refinements};
  }
  const api={...create(original),create};
  if(typeof module==='object' && module.exports) module.exports=api;
  else root.HansonWrightStates=api;
})(typeof window==='undefined'?globalThis:window);
