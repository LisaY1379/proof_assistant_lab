(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else root.EthExamples=api;})(typeof globalThis==='undefined'?this:globalThis,()=>{
const bits=i=>Array.from({length:4},(_,j)=>(i>>(3-j))&1);
const clauses=x=>[x[0]||x[1],x[2]||x[3],x[1]||x[2]].map(Number);
const satisfies=x=>clauses(x).every(Boolean);
function fibers(){return Array.from({length:4},(_,i)=>{const y=[i>>1,i&1],left=[0,1].filter(x=>x||y[0]).length,right=[0,1].filter(x=>y[1]||x).length,bridge=Number(!!(y[0]||y[1]));return{y,left,right,bridge,total:left*bridge*right};});}
return{bits,clauses,satisfies,fibers};});
