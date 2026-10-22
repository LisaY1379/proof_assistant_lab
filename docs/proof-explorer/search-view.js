/* Pure projections: both graphs use the same history position and closure state. */
(function (root) {
  'use strict';
  function ancestry(states, id) {
    const map = new Map(states.map(s => [s.id, s]));
    const path = new Set();
    while (id && map.has(id) && !path.has(id)) { path.add(id); id = map.get(id).parent; }
    return path;
  }
  function snapshot(run, count) {
    if (!run || count === 0) return {states: [], nodes: [], edges: [], active: null, route: new Set(), closed: false};
    const states = run.states.slice(0, count), ids = new Set(states.map(s => s.id));
    const active = states.at(-1), route = ancestry(states, active.id);
    return {states, active, route, nodes: run.proof_nodes.filter(n => ids.has(n.state)),
      edges: run.proof_edges.filter(e => ids.has(e.state)), closed: active.closure === 'accepted'};
  }
  function layout(view, type) {
    const positions = new Map();
    let width = type === 'proof' ? 680 : 400, height = 420;
    if (type === 'search') {
      for (const [i, state] of view.states.entries()) {
        const p = {x: 30 + state.lane * 300, y: 48 + i * 154, w: 270, h: 118};
        positions.set(state.id, p); width = Math.max(width, p.x + p.w + 30); height = Math.max(height, p.y + p.h + 40);
      }
    } else {
      let y = 52;
      for (const state of view.states) {
        const group = view.nodes.filter(n => n.state === state.id);
        const rows = {fact: 0, goal: 0, observation: 0};
        for (const node of group) {
          const column = {fact: 20, observation: 240, goal: 460}[node.kind];
          const p = {x: column, y: y + rows[node.kind]++ * 140, w: 200, h: 112};
          positions.set(node.id, p);
        }
        if (group.length) y += Math.max(...Object.values(rows)) * 140;
      }
      height = Math.max(height, y + (view.closed ? 90 : 30));
    }
    return {positions, width, height};
  }
  function validRecording(run) {
    if (!run || !['constructive-search-v1', 'constructive-search-v2'].includes(run.protocol) || !/^[a-f0-9]{32}$/.test(run.id || '') ||
        !['states', 'proof_nodes', 'proof_edges', 'turns', 'closures'].every(k => Array.isArray(run[k])) ||
        run.states.length > 1000 || run.proof_nodes.length > 10000 || !run.theorem || typeof run.theorem.goal !== 'string') return false;
    const seen = new Set(), nodeIds = new Set(), turnIds = new Set();
    for (const t of run.turns) {
      if (!t || typeof t.id !== 'string' || typeof t.role !== 'string' || turnIds.has(t.id)) return false;
      turnIds.add(t.id);
    }
    for (const s of run.states) {
      if (!s || typeof s.id !== 'string' || seen.has(s.id) || (s.parent !== null && !seen.has(s.parent)) ||
          !Number.isInteger(s.lane) || s.lane < 0 || s.lane > 100 || !['have', 'want'].every(k => Array.isArray(s[k]) && s[k].every(x => typeof x === 'string'))) return false;
      seen.add(s.id);
    }
    for (const n of run.proof_nodes) {
      if (!n || typeof n.id !== 'string' || nodeIds.has(n.id) || !seen.has(n.state) ||
          !['fact', 'goal', 'observation'].includes(n.kind) || typeof n.title !== 'string' || typeof n.statement !== 'string') return false;
      nodeIds.add(n.id);
    }
    if (run.comparisons !== undefined && (!Array.isArray(run.comparisons) || run.comparisons.some(c =>
      !c || typeof c.id !== 'string' || !seen.has(c.decision_state) || !Array.isArray(c.candidates) || c.candidates.length !== 2 ||
      c.candidates.some(a => !a || typeof a.id !== 'string' || typeof a.title !== 'string' || (a.trial_state && !seen.has(a.trial_state))) ||
      (c.selection_state && !seen.has(c.selection_state)) || (c.assessments && (!Array.isArray(c.assessments) || c.assessments.some(a => !a || typeof a.candidate !== 'string')))))) return false;
    return run.states.every(s => [...s.have, ...s.want].every(id => nodeIds.has(id))) && run.proof_edges.every(e =>
      e && seen.has(e.state) && nodeIds.has(e.from) && nodeIds.has(e.to) && ['forward', 'backward', 'meeting', 'observation'].includes(e.kind));
  }
  function comparisonsAt(run, view) {
    const ids = new Set(view.states.map(s => s.id));
    return (run?.comparisons || []).filter(c => ids.has(c.decision_state)).map(c => {
      const selected = ids.has(c.selection_state);
      return {...c, selected: selected ? c.selected : null,
        reason: selected ? c.reason : null, assessments: selected ? c.assessments : [],
        selection_state: selected ? c.selection_state : null,
        candidates: c.candidates.map(a => ids.has(a.trial_state) ? {...a} :
          {id:a.id, title:a.title, motivation:a.motivation, familiarity:a.familiarity, basis:a.basis, trial_state:null})};
    });
  }
  const api = {ancestry, snapshot, layout, validRecording, comparisonsAt};
  if (typeof module !== 'undefined') module.exports = api; else root.SearchView = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
