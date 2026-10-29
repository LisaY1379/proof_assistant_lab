/* Safe prose structure: math remains text until MathJax typesets it. */
(function(root){
  'use strict';
  function normalizeLegacyMath(text){
    // Preserve stored prose; recognize only the explorer's existing explicit formulas.
    const formulas=[
      ['Θₘ₀₊ⱼ − 1 ≤ 3⁻κʲ', String.raw`\Theta_{m_0+j}-1\le 3^{-\kappa j}`],
      ['(1 + R)^{C log(1 + R)}', String.raw`(1+R)^{C\log(1+R)}`],
      ['C(2 + R)^C', String.raw`C(2+R)^C`],
      ['R = Λ/λ', String.raw`R=\frac{\Lambda}{\lambda}`],
      ['Θₘ ≤ 1 + σ', String.raw`\Theta_m\le 1+\sigma`],
      ['Θₘ − 1', String.raw`\Theta_m-1`],
      ['Θₘ ≥ 1', String.raw`\Theta_m\ge 1`],
      ['Θₘ = 1', String.raw`\Theta_m=1`],
      ['Θₘ ↓ 1', String.raw`\Theta_m\downarrow 1`],
      ['ΠKΨ', String.raw`\Pi K_{\Psi}`],
      ['3ᵐ', String.raw`3^m`]
    ];
    return text.split(/(\\\([\s\S]*?\\\)|\\\[[\s\S]*?\\\]|\$\$[\s\S]*?\$\$|\$[^$\n]+\$)/g).map((part,i)=>{
      if(i%2)return part;
      // Replace in a single pass so generated delimiters are never processed again.
      const pattern=new RegExp(formulas.map(([plain])=>plain.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')).join('|'),'g');
      return part.replace(pattern,match=>String.raw`\(${formulas.find(([plain])=>plain===match)[1]}\)`);
    }).join('');
  }
  function blocks(text){
    const result=[];
    function prose(value){
      for(const paragraph of value.trim().split(/\n\s*\n/).filter(Boolean)){
        let list=null;
        for(const line of paragraph.split('\n')){
          const heading=line.match(/^#{1,4}\s+(.+)$/), bullet=line.match(/^\s*([-*•]|\d+[.)])\s+(.+)$/);
          if(heading){list=null;result.push({type:'heading',text:heading[1]});}
          else if(bullet){const ordered=/^\d/.test(bullet[1]);if(!list||list.ordered!==ordered){list={type:'list',ordered,items:[]};result.push(list);}list.items.push(bullet[2]);}
          else {list=null;const previous=result.at(-1);if(previous?.type==='paragraph'&&!previous.end)previous.text+='\n'+line;else result.push({type:'paragraph',text:line});}
        }
        const last=result.at(-1);if(last?.type==='paragraph')last.end=true;
      }
    }
    // Display formulas can contain blank lines and aligned environments.
    const expression=/\\\[([\s\S]*?)\\\]|\$\$([\s\S]*?)\$\$/g;let start=0,match;
    while((match=expression.exec(text))){prose(text.slice(start,match.index));result.push({type:'math',text:'\\['+(match[1]??match[2]).trim()+'\\]'});start=expression.lastIndex;}
    prose(text.slice(start));return result;
  }
  function inline(parent,text,doc){
    // Keep inline math intact, even if it contains asterisks.
    const parts=text.split(/(\\\([\s\S]*?\\\)|\$[^$\n]+\$|\*\*[^\n]+?\*\*)/g);
    for(const part of parts){if(part.startsWith('**')&&part.endsWith('**')){const strong=doc.createElement('strong');strong.textContent=part.slice(2,-2);parent.append(strong);}else parent.append(doc.createTextNode(part));}
  }
  function render(parent,text){
    const doc=parent.ownerDocument;
    for(const block of blocks(normalizeLegacyMath(text))){
      const tag={math:'div',paragraph:'p',heading:'h4',list:block.ordered?'ol':'ul'}[block.type],node=doc.createElement(tag);
      if(block.type==='math'){node.className='annotation-equation';node.textContent=block.text;}
      else if(block.type==='list'){for(const item of block.items){const li=doc.createElement('li');inline(li,item,doc);node.append(li);}}
      else inline(node,block.text,doc);
      parent.append(node);
    }
  }
  const api={blocks,render,normalizeLegacyMath};if(typeof module==='object'&&module.exports)module.exports=api;else root.AnnotationFormat=api;
})(typeof globalThis!=='undefined'?globalThis:this);
