/* Render the introduction once MathJax and the document are ready. */
(()=>{
  let rendered=false;
  function render(){
    if(rendered || !window.MathJax?.typesetPromise)return;
    rendered=true;
    MathJax.startup.promise.then(()=>MathJax.typesetPromise([document.getElementById('entry-context')])).catch(error=>{rendered=false;console.error('Introduction math rendering failed',error);});
  }
  document.addEventListener('annotation-math-ready',render);
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',render);else render();
  // Direct links to content inside a collapsed introduction should still work.
  function reveal(){
    const target=document.getElementById(location.hash.slice(1));
    if(!target)return;
    for(let node=target.parentElement;node;node=node.parentElement)if(node.tagName==='DETAILS')node.open=true;
    if(location.hash)requestAnimationFrame(()=>target.scrollIntoView());
  }
  window.addEventListener('hashchange',reveal);
  if(location.hash)reveal();
})();
