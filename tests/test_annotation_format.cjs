const {test}=require('node:test');
const assert=require('node:assert/strict');
const {blocks,render}=require('../tools/proof_explorer/papers/high-contrast/annotation-format.js');
test('display math remains whole across blank lines and aligned expressions',()=>{
 const value=String.raw`First explain \(R\).

\[\begin{aligned}
L &\le C(2+R)^C \\

R &= \Lambda/\lambda
\end{aligned}\]

Then interpret the bound.`;
 const result=blocks(value);
 assert.deepEqual(result.map(b=>b.type),['paragraph','math','paragraph']);
 assert.ok(result[1].text.includes('\\\\\n\nR'));
 assert.ok(result[0].text.includes(String.raw`\(R\)`));
});
test('headings, lists, and dollar display delimiters retain structure',()=>{
 const result=blocks('## Two quantities\n\n- **Contrast:** $R$.\n- **Length:** $L$.\n\n$$L \\le R^C$$');
 assert.deepEqual(result.map(b=>b.type),['heading','list','math']);
 assert.equal(result[1].items.length,2);
 assert.equal(result[2].text,String.raw`\[L \le R^C\]`);
});
test('prose and markup-like model output are inserted only as text',()=>{
 const document={createElement(tag){return {tag,children:[],ownerDocument:document,append(...nodes){this.children.push(...nodes);}}},createTextNode(text){return {text};}};
 const parent=document.createElement('div');
 render(parent,'A **definition**, then <img src=x onerror=alert(1)>.');
 assert.equal(parent.children[0].tag,'p');
 assert.equal(parent.children[0].children[1].tag,'strong');
 assert.ok(parent.children[0].children.some(n=>n.text?.includes('<img')));
});
