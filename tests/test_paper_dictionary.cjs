const {test}=require('node:test');
const assert=require('node:assert/strict');
const {entries,lookup,search}=require('../tools/proof_explorer/papers/high-contrast/dictionary-data.js');
test('selection lookup tolerates case, punctuation and dash variants, without matching unrelated sentences',()=>{
  assert.equal(lookup(' “HOMOGENIZATION” ').id,'homogenization');
  assert.equal(lookup('primal—dual mismatch').id,'duality-gap');
  assert.equal(lookup('unit   range of dependence').id,'range-of-dependence');
  assert.equal(lookup('the contrast has increased'),undefined);
  assert.equal(lookup('observation scale'),undefined);
});
test('each starter entry supplies context, definition, usage and a source; search includes conceptual descriptions',()=>{
  assert.equal(new Set(entries.map(e=>e.id)).size,entries.length);
  for(const entry of entries){for(const key of ['context','definition','usage','reference','formula'])assert.ok(entry[key]);assert.ok(entry.page>0);}
  assert.ok(search('independence').some(e=>e.id==='range-of-dependence'));
  assert.equal(search('qwerty-no-such-term').length,0);
});
