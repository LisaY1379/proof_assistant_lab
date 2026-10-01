const {test}=require('node:test');
const assert=require('node:assert/strict');
const P=require('./proof.js');
const W=require('./written-proof.js');

test('each thinking move has exactly one passage in the complete written proof',()=>{
  const eventIds=['start',...P.events.map(e=>e.id)];
  assert.deepEqual(Object.keys(W.byEvent).sort(),eventIds.slice().sort());
  assert.equal(new Set(W.passages.map(p=>p.id)).size,W.passages.length);
  for(const id of eventIds){
    assert.equal(W.passages.filter(p=>p.events.includes(id)).length,1,id);
    assert.ok(W.byEvent[id].html.trim(),id);
  }
});

test('written order is independent of discovery order and can revisit a passage',()=>{
  const writtenIndex=id=>W.passages.indexOf(W.byEvent[id]);
  assert.ok(writtenIndex('decouple')<writtenIndex('linear'));
  assert.ok(P.events.indexOf(P.byId.linear)<P.events.indexOf(P.byId.decouple));
  assert.equal(W.byEvent.gaussian,W.byEvent.replace);
  assert.notEqual(W.byEvent.meet,W.byEvent.finish);
});

test('initial facts and ultimate goal are the only initial nodes',()=>{
  assert.deepEqual([...P.visible([])].sort(),['centered','independence','subgaussian','ultimate']);
  assert.equal(P.achieved([]).size,0);
  assert.ok(P.available([],'forward').length);
  assert.ok(P.available([],'backward').length);
});

test('guided order is executable and closes every goal',()=>{
  const done=[];
  for(const e of P.events){assert.ok(P.available(done).some(x=>x.id===e.id),e.id);done.push(e.id);}
  assert.equal(P.available(done).length,0);
  for(const n of P.nodes.filter(n=>n.kind.startsWith('goal')))assert.ok(P.achieved(done).has(n.id),n.id);
});

test('all reachable routes can finish; the endpoint never closes early',()=>{
  const visited=new Set();
  function walk(done){
    const key=[...done].sort().join(',');if(visited.has(key))return;visited.add(key);
    const next=P.available(done);
    if(done.includes('finish')){
      for(const necessary of ['bernstein','optimize','meet','compute','rotate','replace','decouple','linear','gaussian','exponential','split','sign','expand']) assert.ok(done.includes(necessary),necessary);
    }else{assert.ok(next.length,'dead end: '+key);assert.ok(!P.achieved(done).has('ultimate'));}
    for(const e of next){assert.ok(!done.includes(e.id));assert.ok(e.deps.every(d=>done.includes(d)));walk([...done,e.id]);}
  }
  walk([]);assert.ok(visited.size>30);
});

test('graph references and observation branches are valid',()=>{
  const ids=new Set(P.nodes.map(n=>n.id));assert.equal(ids.size,P.nodes.length);
  for(const [a,b] of P.edges){assert.ok(ids.has(a));assert.ok(ids.has(b));}
  for(const e of P.events){
    for(const id of e.add)assert.ok(ids.has(id));
    if(e.direction==='backward'){
      assert.ok(e.add.some(id=>P.nodes.find(n=>n.id===id).kind==='observation'));
      assert.ok(e.add.some(id=>P.nodes.find(n=>n.id===id).kind.startsWith('goal')));
    }
  }
});

test('completion and availability recompute correctly after rewinding',()=>{
  const end=P.events.map(e=>e.id),before=end.slice(0,end.indexOf('meet'));
  assert.ok(P.achieved(end).has('mgf'));
  assert.ok(!P.achieved(before).has('mgf'));
  assert.ok(P.available(before).some(e=>e.id==='meet'));
  assert.ok(!P.visible(before).has('bounded'));
});
