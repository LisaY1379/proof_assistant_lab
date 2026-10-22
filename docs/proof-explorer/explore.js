(() => {
  'use strict';
  const $ = id => document.getElementById(id), V = window.SearchView;
  let run = null, cursor = 0, selected = null, selectedMath = null, follow = true;
  let available = false, connected = false, busy = false, serverActive = null, stopping = false;
  let pollTimer = null, replayTimer = null, generation = 0, comparisonChoice = null;
  const zoom = {proof: 1, search: 1};
  const terminal = status => !['queued', 'running'].includes(status);
  const text = (tag, value, cls) => { const e = document.createElement(tag); e.textContent = value; if (cls) e.className = cls; return e; };
  const notice = message => { $('notice').textContent = message || ''; $('notice').hidden = !message; };
  async function api(path, body) {
    const response = await fetch(path, {cache: 'no-store', ...(body === undefined ? {} : {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body)})});
    if (!response.ok) { let error; try { error = (await response.json()).error; } catch {} throw new Error(error || 'The local runner could not complete the request.'); }
    return response.json();
  }
  function controls() {
    const running = run && !terminal(run.status);
    $('start').disabled = !available || !!serverActive || busy;
    $('start').textContent = run ? '＋ New attempt' : '▶ Start proof';
    $('stop').hidden = !running;
    $('stop').disabled = stopping;
    $('stop').textContent = stopping ? 'Stopping after this turn…' : 'Stop after this turn';
    $('budget').disabled = !!running || busy;
    $('history').disabled = !run; $('history').max = run ? run.states.length : 0; $('history').value = cursor;
    $('replay').disabled = !run || run.states.length < 2;
    $('latest').disabled = !run; $('download').disabled = !run;
    $('clear').disabled = !!running || busy;
    $('recordings').disabled = !!running || busy;
    $('import').disabled = !!running || busy;
    $('position').textContent = run ? `${cursor} / ${run.states.length} states` : 'Not started';
    $('status-dot').classList.toggle('running', !!running);
    $('status').textContent = run ? run.stage : available ? 'Ready when you are' : connected ? 'A local API key is needed to begin' : 'Local runner required for live exploration';
  }
  function line(svg, a, b, cls, side = false) {
    const p = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    let x1 = a.x + a.w / 2, y1 = a.y + a.h, x2 = b.x + b.w / 2, y2 = b.y;
    if (side) { x1 = a.x + a.w; y1 = a.y + a.h / 2; x2 = b.x; y2 = b.y + b.h / 2; }
    const mid = (y1 + y2) / 2;
    p.setAttribute('d', side ? `M${x1},${y1} C${x1 + 65},${y1} ${x2 - 65},${y2} ${x2},${y2}` : `M${x1},${y1} C${x1},${mid} ${x2},${mid} ${x2},${y2}`);
    p.setAttribute('class', `graph-line ${cls}`); svg.append(p);
  }
  function card(board, p, id, sid, kind, title, meta, desc, abandoned) {
    const button = text('button', '', `graph-card ${kind}${abandoned ? ' abandoned' : ''}${selectedMath === id || (!selectedMath && selected === sid) ? ' selected' : selected === sid ? ' related' : ''}`);
    Object.assign(button.style, {left: `${p.x}px`, top: `${p.y}px`, width: `${p.w}px`, height: `${p.h}px`});
    button.dataset.state = sid; button.dataset.node = id;
    button.append(text('span', meta, 'card-meta'), text('span', title, 'card-title'), text('span', desc, 'card-description'));
    button.title = title; button.setAttribute('aria-label', `${meta}: ${title}`);
    button.onclick = () => { comparisonChoice = null; selected = sid; selectedMath = kind.includes('state') ? null : id; follow = false; render(); $('inspector').scrollIntoView({behavior: 'smooth', block: 'start'}); };
    board.append(button);
  }
  function draw(type, view) {
    const board = $(type + '-board'), scale = $(type + '-scale'), viewport = $(type + '-viewport');
    board.replaceChildren(); $(type + '-empty').hidden = !!view.active; scale.hidden = !view.active;
    if (!view.active) return;
    const l = V.layout(view, type);
    Object.assign(board.style, {width: `${l.width}px`, height: `${l.height}px`, transform: `scale(${zoom[type]})`});
    Object.assign(scale.style, {width: `${l.width * zoom[type]}px`, height: `${l.height * zoom[type]}px`});
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('width', l.width); svg.setAttribute('height', l.height); svg.setAttribute('aria-hidden', 'true'); board.append(svg);
    if (type === 'proof') {
      for (const [x, label] of [[20, 'HAVE · FORWARD'], [240, 'OBSERVATIONS'], [460, 'WANT · BACKWARD']]) { const e = text('span', label, 'board-label'); e.style.left = x + 'px'; board.append(e); }
      for (const e of view.edges) {
        if (l.positions.has(e.from) && l.positions.has(e.to)) line(svg, l.positions.get(e.from), l.positions.get(e.to), e.kind + (view.route.has(e.state) ? '' : ' abandoned'), e.kind === 'meeting');
      }
      const touched = new Set(view.edges.filter(e => e.state === selected).flatMap(e => [e.from, e.to]));
      for (const n of view.nodes) {
        const abandoned = !view.route.has(n.state);
        const localClosed = run.closures.some(c => c.goal === n.id && view.route.has(c.state));
        card(board, l.positions.get(n.id), n.id, n.state, n.kind, n.title, `${n.kind === 'fact' ? 'Have' : n.kind === 'goal' ? 'Want' : 'Tentative'}${localClosed ? ' · connected' : ''}${abandoned ? ' · other branch' : ''}`, n.statement, abandoned);
        if (!selectedMath && touched.has(n.id)) board.lastElementChild.classList.add('related');
      }
      if (view.closed) { const banner = text('div', '✓ Have meets want · route accepted by both roles', 'closure-banner'); Object.assign(banner.style, {left: '20px', width: '640px', bottom: '25px'}); board.append(banner); }
    } else {
      for (const s of view.states) {
        if (s.parent && l.positions.has(s.parent)) line(svg, l.positions.get(s.parent), l.positions.get(s.id), view.route.has(s.id) ? '' : 'abandoned');
        if (s.departed_from && l.positions.has(s.departed_from)) line(svg, l.positions.get(s.departed_from), l.positions.get(s.id), 'rollback');
        const assessment = run.turns.find(t => t.id === s.turn)?.move?.outcome;
        const closed = s.closure === 'accepted', pending = s.closure === 'pending';
        card(board, l.positions.get(s.id), s.id, s.id, `state${closed ? ' closed' : ''}`, closed ? 'Have and want align' : s.title,
          `${s.id} · ${s.role || 'Starting state'} · ${s.action}`, `${s.have.length} facts · ${s.want.length} open goals${pending ? ' · awaiting review' : closed ? ' · agents agree' : assessment && assessment !== 'progress' ? ' · ' + assessment.replaceAll('_', ' ') : ''}`, !view.route.has(s.id));
      }
    }
    if (follow) {
      const id = type === 'search' ? view.active.id : [...view.nodes].reverse().find(n => view.route.has(n.state))?.id;
      const p = l.positions.get(id);
      if (p) { viewport.scrollTop = Math.max(0, (p.y + p.h) * zoom[type] - viewport.clientHeight + 45); viewport.scrollLeft = Math.max(0, (p.x + p.w / 2) * zoom[type] - viewport.clientWidth / 2); }
    }
  }
  function inspect(view) {
    const state = view.states.find(s => s.id === selected);
    $('detail-content').hidden = !state; $('detail-placeholder').hidden = !!state;
    if (!state) { $('detail-title').textContent = 'Every node has a story.'; $('detail-meta').textContent = 'STATE & CONVERSATION'; return; }
    const turn = run.turns.find(t => t.id === state.turn), move = turn?.move;
    const math = view.nodes.find(n => n.id === selectedMath);
    $('detail-title').textContent = math?.title || state.title;
    $('detail-meta').textContent = `${state.id} · ${state.role || 'Starting state'} · ${state.action}${view.route.has(state.id) ? '' : ' · other branch'}`;
    $('selected-math').hidden = !math; $('selected-math').textContent = math?.statement || '';
    const nodes = new Map(run.proof_nodes.map(n => [n.id, n]));
    for (const [key, container] of [['have', 'have'], ['want', 'want']]) {
      $(container).replaceChildren(...state[key].map(id => text('li', nodes.get(id)?.statement || id)));
      if (!state[key].length) $(container).append(text('li', key === 'want' ? state.closure === 'accepted' ? 'All obligations discharged; the other role accepted the route.' : 'No open obligations. Closure awaits the other role’s review.' : 'No facts recorded.'));
    }
    $('conversation').replaceChildren();
    const index = turn ? run.turns.findIndex(t => t.id === turn.id) : -1;
    for (const t of index >= 0 ? run.turns.slice(Math.max(0, index - 1), index + 1) : []) {
      const block = text('div', '', `dialogue-turn ${t.role}${t.id !== turn.id ? ' previous' : ''}`);
      block.append(text('strong', `${t.role} · ${t.id}${t.id !== turn.id ? ' · preceding turn' : ''}`), text('div', t.move?.text || t.raw)); $('conversation').append(block);
    }
    if (!turn) $('conversation').append(text('p', 'Only the theorem and its assumptions have been supplied. No reference proof is in either role’s context.'));
    $('decision').replaceChildren();
    for (const [label, value] of move ? [['Move', move.action], ['Why here', move.reason], ['Mathematical work', move.work || 'No derivation asserted in this turn.'], ['Assessment', move.outcome], ['Recorded effort', `${turn.elapsed_seconds ?? 'Unknown'} seconds for this response · turn ${index + 1} of ${run.max_turns}. Elapsed time is not a measure of mathematical difficulty.`], ['Cost / remaining work', move.cost]] : [['Next', 'Choose an approach from the available facts and the target.']]) $('decision').append(text('dt', label), text('dd', value));
    $('branch-links').replaceChildren();
    const relatives = view.states.filter(s => s.id === state.parent || s.parent === state.id || (state.departed_from && s.id === state.departed_from));
    for (const s of relatives) {
      const b = text('button', `${s.id === state.parent ? '← Based on' : s.id === state.departed_from ? 'Left branch' : 'Explored →'} ${s.id}`);
      b.onclick = () => { selected = s.id; selectedMath = null; follow = false; render(); }; $('branch-links').append(b);
    }
    $('raw').textContent = turn ? JSON.stringify({request: turn.request, response: turn.raw}, null, 2) : JSON.stringify(run.theorem, null, 2);
  }
  function compare(view) {
    const comparisons = V.comparisonsAt(run, view);
    $('method-comparison').hidden = !comparisons.length;
    if (!comparisons.length) return;
    const state = view.states.find(s => s.id === selected);
    const current = comparisons.find(c => c.id === comparisonChoice) || comparisons.find(c => c.id === state?.comparison) || comparisons.at(-1);
    $('comparison-picker').replaceChildren(...comparisons.map(c => new Option(c.title, c.id)));
    $('comparison-picker').value = current.id;
    $('comparison-title').textContent = current.title;
    const tried = current.candidates.filter(c => c.trial_state).length;
    $('comparison-status').textContent = current.selected ? 'Two bounded trials compared · a route was selected' : `${tried} / 2 methods tried · no route selected yet`;
    $('candidate-cards').replaceChildren();
    for (const candidate of current.candidates) {
      const chosen = current.selected === candidate.id;
      const assessment = current.assessments?.find(a => a.candidate === candidate.id);
      const card = text('article', '', `candidate-card${chosen ? ' chosen' : current.selected ? ' set-aside' : ''}`);
      card.append(text('span', chosen ? 'SELECTED TO CONTINUE' : candidate.trial_state ? current.selected ? 'EXPLORED ALTERNATIVE' : 'TRIAL RECORDED' : 'PROPOSED · NOT YET TRIED', 'eyebrow'), text('h3', candidate.title), text('p', candidate.motivation));
      const list = document.createElement('dl');
      const fields = [['Why it is natural', `${candidate.familiarity} · ${candidate.basis}`],
        ['Measured trial effort', candidate.observed ? `${candidate.observed.model_calls} model call · ${candidate.observed.elapsed_seconds} seconds. Same completion-token cap for both methods.` : 'Not yet attempted.'],
        ['Trial outcome', candidate.outcome?.replaceAll('_',' ') || 'Unknown'],
        ['Relative mathematical work', assessment?.relative_work || candidate.reported_cost || 'Awaiting trial and comparison.'],
        ['Relative result strength', assessment?.relative_strength || 'Not compared yet.'],
        ['Remaining uncertainty', assessment?.uncertainty || 'Total route cost is unknown. An unfinished trial is not a failed method.']];
      for (const [label,value] of fields) list.append(text('dt',label),text('dd',value));
      card.append(list);
      if (candidate.work) { const details = document.createElement('details'); details.append(text('summary','Show the actual trial work'),text('p',candidate.work,'trial-work')); if (assessment) details.append(text('strong','Evidence quoted in the comparison'),text('blockquote',assessment.evidence)); card.append(details); }
      if (candidate.trial_state) { const button = text('button','Inspect this branch'); button.onclick = () => { selected = candidate.trial_state; selectedMath = null; follow = false; comparisonChoice = current.id; render(); $('inspector').scrollIntoView({behavior:'smooth',block:'start'}); }; card.append(button); }
      $('candidate-cards').append(card);
    }
    $('selection-reason').textContent = current.reason ? 'Why this route: ' + current.reason : 'Each candidate is investigated before a preference is recorded. Selection remains pending if the turn budget runs out.';
  }
  $('comparison-picker').onchange = () => { comparisonChoice = $('comparison-picker').value; render(); };
  function render() {
    controls();
    const view = V.snapshot(run, cursor);
    if (!view.states.some(s => s.id === selected)) { selected = view.active?.id || null; selectedMath = null; }
    draw('proof', view); draw('search', view); inspect(view); compare(view);
    $('proof-foot').textContent = view.closed ? '✓ All obligations connected · agents agree; not formally verified' : view.active ? `${view.nodes.filter(n => n.kind === 'fact').length} facts recorded · ${view.active.want.length} open goals in this state` : 'Waiting for the first move';
    $('search-foot').textContent = view.active ? `${view.states.length - 1} moves · ${new Set(view.states.map(s => s.lane)).size} branches · ${view.active.closure === 'pending' ? 'closure awaiting review' : view.closed ? 'route accepted' : 'exploration open'}` : 'No attempts recorded';
  }
  function stopReplay() { clearInterval(replayTimer); replayTimer = null; $('replay').textContent = '▶ Replay'; }
  async function listRuns() {
    if (!connected) return;
    try { const runs = await api('/api/searches'); $('recordings').replaceChildren(new Option('Choose a saved run…', ''), ...runs.map(r => new Option(`${new Date(r.created_at).toLocaleString()} · ${r.status} · ${r.max_turns} turns${r.protocol === 'constructive-search-v2' ? ' · comparisons' : ''}`, r.id))); } catch {}
  }
  async function poll(id, token) {
    try {
      const next = await api('/api/searches/' + id);
      if (token !== generation) return;
      const changed = !run || next.states.length !== run.states.length || next.status !== run.status || next.stage !== run.stage || next.turns.length !== run.turns.length;
      run = next;
      if (follow) { cursor = run.states.length; selected = run.active; selectedMath = null; }
      serverActive = terminal(run.status) ? null : id;
      if (changed) render();
      if (!terminal(run.status)) pollTimer = setTimeout(() => poll(id, token), 1800);
      else { stopping = false; if (run.error) notice(run.error); await listRuns(); controls(); }
    } catch (error) {
      if (token !== generation) return;
      notice('Connection interrupted. Your recorded work stays on the server. Retrying…');
      pollTimer = setTimeout(() => poll(id, token), 4000);
    }
  }
  function load(record, live = false) {
    generation++; clearTimeout(pollTimer); stopReplay();
    zoom.proof = Math.min(1, ($('proof-viewport').clientWidth - 8) / 680);
    $('budget').value = String(record.max_turns);
    comparisonChoice = null; run = record; cursor = run.states.length; selected = run.active; selectedMath = null; follow = true; stopping = false;
    notice(run.error || (run.protocol === 'constructive-search-v1' ? 'Earlier exploration: alternative-method trials were optional in this recording. Start a new attempt to use the comparison workflow.' : '')); render();
    if (live && !terminal(run.status)) { serverActive = run.id; poll(run.id, generation); }
  }
  $('start').onclick = async () => {
    busy = true; controls(); notice('');
    try {
      const result = await api('/api/searches', {max_turns: Number($('budget').value)});
      serverActive = result.id; load(result, true); await listRuns();
    } catch (error) { notice(error.message); }
    finally { busy = false; controls(); }
  };
  $('stop').onclick = async () => {
    stopping = true; controls();
    try { const response = await api(`/api/searches/${run.id}/cancel`, {}); notice(response.message); }
    catch (error) { stopping = false; notice(error.message); controls(); }
  };
  $('history').oninput = () => { stopReplay(); follow = false; cursor = Number($('history').value); selected = null; selectedMath = null; render(); };
  $('latest').onclick = () => { stopReplay(); follow = true; cursor = run.states.length; selected = run.active; selectedMath = null; render(); };
  $('replay').onclick = () => {
    if (replayTimer) { stopReplay(); return; }
    follow = false; if (cursor >= run.states.length) cursor = 0; $('replay').textContent = 'Ⅱ Pause'; render();
    replayTimer = setInterval(() => { if (cursor >= run.states.length) { stopReplay(); return; } cursor++; selected = null; selectedMath = null; render(); }, 1600);
  };
  document.querySelectorAll('.fit').forEach(b => b.onclick = () => { const type = b.dataset.graph; const l = V.layout(V.snapshot(run, cursor), type); zoom[type] = Math.min(1, ($(type + '-viewport').clientWidth - 8) / l.width); render(); });
  $('download').onclick = () => { const url = URL.createObjectURL(new Blob([JSON.stringify(run, null, 2)], {type: 'application/json'})); const a = text('a', ''); a.href = url; a.download = `hanson-wright-search-${run.id}.json`; a.click(); setTimeout(() => URL.revokeObjectURL(url), 1000); };
  $('recordings').onchange = async () => { if (!$('recordings').value) return; try { load(await api('/api/searches/' + $('recordings').value), true); } catch (error) { notice(error.message); } };
  $('import').onchange = async event => {
    const file = event.target.files[0]; if (!file) return;
    try {
      if (file.size > 12000000) throw new Error('Choose a recording smaller than 12 MB.');
      const record = JSON.parse(await file.text());
      if (!V.validRecording(record)) throw new Error('This is not a supported constructive exploration recording.');
      if (!terminal(record.status)) { record.status = 'imported'; record.stage = 'Imported partial recording · replay only'; }
      load(record); notice('Imported recording · supplied claims and provenance have not been independently checked.');
    } catch (error) { notice(error.message); }
    event.target.value = '';
  };
  $('clear').onclick = () => { generation++; clearTimeout(pollTimer); stopReplay(); run = null; cursor = 0; comparisonChoice = null; selected = null; selectedMath = null; follow = true; notice(''); render(); };
  document.addEventListener('visibilitychange', () => { if (document.hidden) stopReplay(); });
  async function init() {
    render();
    const local = ['localhost', '127.0.0.1'].includes(location.hostname);
    if (local) {
      try {
        const status = await api('/api/searches/status'); connected = true; available = status.available; serverActive = status.active;
        $('run-note').textContent = 'Strategic choices compare two methods, with one model call per trial. The turn budget includes planning and comparison. API usage is billed; reference proof withheld; logs stay local.';
        if (!available) notice('Add OPENAI_API_KEY to the project .env and restart the local runner.');
        await listRuns(); if (serverActive) load(await api('/api/searches/' + serverActive), true);
      } catch { notice('Start the local exploration service to generate a live proof. You can also import a saved exploration to replay it.'); }
    } else notice('Live exploration requires the local runner. This static page can replay an imported exploration; it does not invent a search history.');
    render();
  }
  init();
})();
