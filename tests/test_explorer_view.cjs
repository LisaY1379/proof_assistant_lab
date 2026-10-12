const {test}=require('node:test');const assert=require('node:assert/strict');const fs=require('node:fs');
const UI=require('../main/explorer/app.js');const doc=JSON.parse(fs.readFileSync('main/explorer/example.json','utf8'));
test('portable Hanson–Wright has exact original text in the reader',()=>{
 assert.equal(UI.proofSegments(doc).map(p=>p.text).join(''),doc.original_proof);
});
test('every selected result removes its own action and branches in both graphs',()=>{
 for(const step of doc.steps){const v=UI.views(doc,step.id);const study=doc.ablations[step.id];
  assert.equal(v.state.nodes.find(n=>n.action===step.id&&n.kind==='state').id,'s'+step.id.slice(1));
  assert(v.state.edges.some(e=>e.action===step.id&&e.kind==='removed-edge'));
  for(const alt of study.alternatives){for(const graph of [v.proof,v.state]){
   const route=graph.nodes.filter(n=>n.alternative===alt.id);assert.equal(route.length,alt.route.length);
   assert.equal(route[0].origin,UI.sourceLabel(alt));
   assert(graph.edges.some(e=>e.to===route[0].id));
   const ids=new Set(graph.nodes.map(n=>n.id));assert(graph.edges.every(e=>ids.has(e.from)&&ids.has(e.to)));
  }}
 }
});
test('restoring has no alternative nodes and critical decoupling retains sources',()=>{
 const plain=UI.views(doc,null);assert(!plain.proof.nodes.some(n=>n.kind==='branch'));
 const critical=doc.critical.steps[0],alt=doc.ablations[critical].alternatives[0];
 assert.equal(alt.origin,'literature_assisted');assert(alt.source_ids.length);
});
test('Unicode source positions use codepoints rather than UTF16',()=>{
 const sample={original_proof:'😀A proof.',steps:[{id:'a1',start:1,end:9}]};
 assert.equal(UI.proofSegments(sample).map(s=>s.text).join(''),'😀A proof.');
 assert.equal(UI.proofSegments(sample)[1].text,'A proof.');
});
