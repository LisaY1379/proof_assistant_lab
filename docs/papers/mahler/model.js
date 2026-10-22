/* Exact polygon geometry up to floating-point arithmetic; narrative state, not a proof checker. */
(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else{root.MahlerModel=api;root.PaperModel=api;}})(typeof globalThis!=='undefined'?globalThis:this,function(){
'use strict';
const cross=(a,b,c)=>(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]);
function hull(points){const p=points.map(x=>x.slice()).sort((a,b)=>a[0]-b[0]||a[1]-b[1]);const lo=[],hi=[];for(const a of p){while(lo.length>1&&cross(lo.at(-2),lo.at(-1),a)<=1e-12)lo.pop();lo.push(a);}for(const a of p.slice().reverse()){while(hi.length>1&&cross(hi.at(-2),hi.at(-1),a)<=1e-12)hi.pop();hi.push(a);}return lo.slice(0,-1).concat(hi.slice(0,-1));}
function area(p){return Math.abs(p.reduce((s,a,i)=>{const b=p[(i+1)%p.length];return s+a[0]*b[1]-a[1]*b[0];},0))/2;}
function polar(p){return p.map((a,i)=>{const b=p[(i+1)%p.length],det=a[0]*b[1]-a[1]*b[0];if(det<=1e-12)throw Error('Need a counterclockwise convex polygon with the origin strictly inside.');return [(b[1]-a[1])/det,(a[0]-b[0])/det];});}
function shape(kind,p=2){
 if(kind==='square')return [[-1,-1],[1,-1],[1,1],[-1,1]];
 if(kind==='diamond')return [[0,-1],[1,0],[0,1],[-1,0]];
 if(kind==='hexagon')return hull(Array.from({length:6},(_,i)=>[Math.cos(i*Math.PI/3),Math.sin(i*Math.PI/3)]));
 if(kind==='irregular')return hull([[1.1,.1],[.7,.9],[-.2,1],[-1.1,-.1],[-.7,-.9],[.2,-1]]);
 if(!Number.isFinite(p)||p<1)throw Error('A convex ℓᵖ ball needs p ≥ 1.');
 if(kind==='circle')p=2;
 return hull(Array.from({length:160},(_,i)=>{const c=Math.cos(2*Math.PI*i/160),s=Math.sin(2*Math.PI*i/160);return [Math.sign(c)*Math.abs(c)**(2/p),Math.sign(s)*Math.abs(s)**(2/p)];}));
}
function transform(poly,stretch=1,shear=0){if(stretch<=0||![stretch,shear].every(Number.isFinite))throw Error('Positive finite stretch required.');return poly.map(([x,y])=>[stretch*x+shear*y,y]);}
function lens(theta,terms=500){let x=0;for(let j=0;j<terms;j++)x+=(j%2?-1:1)*Math.cos((2*j+1)*theta)/(2*j+1)**2;return [8*x/Math.PI**2,2*Math.asin(Math.sin(theta))/Math.PI];}
function stateAt(theorem,count){
 if(!Number.isFinite(count))throw Error('Invalid progress');count=Math.max(0,Math.min(theorem.steps.length,Math.floor(count)));
 const facts=[{id:'given',text:theorem.given,at:0}],goals=[{id:'root',text:theorem.goal,status:'open',at:0}],actions=[];
 for(let i=0;i<count;i++){const s=theorem.steps[i];for(const id of s.uses)if(!facts.some(f=>f.id===id))throw Error('Unavailable premise '+id);
  if(s.opens.length){goals[0].status='reduced';for(const [id,text] of s.opens){if(goals.some(g=>g.id===id))throw Error('Duplicate goal');goals.push({id,text,status:'open',at:i+1});}}
  if(s.fact){if(facts.some(f=>f.id===s.fact[0]))throw Error('Duplicate fact');facts.push({id:s.fact[0],text:s.fact[1],at:i+1});}
  for(const id of s.closes){const g=goals.find(g=>g.id===id);if(!g||g.status!=='open'||!s.fact)throw Error('Invalid discharge '+id);g.status='closed';g.closedBy=s.fact[0];}actions.push(s.id);
 }
 const children=goals.slice(1),closed=children.length>0&&children.every(g=>g.status==='closed')&&facts.some(f=>f.id==='result');if(closed){goals[0].status='closed';goals[0].closedBy='result';}
 return {count,facts,goals,actions,closed,wants:goals.filter(g=>g.status==='open')};
}
function branchAt(theorem,index){if(!Number.isInteger(index)||index<1||index>theorem.steps.length)throw Error('Invalid branch');return {...stateAt(theorem,index-1),closed:false,branch:{step:index,removed:theorem.steps[index-1].id,...theorem.steps[index-1].alternative}};}
function validate(t){if(!t.given||!t.toolkit?.length)throw Error('Missing declared context');for(const s of t.steps){if(!s.source||s.source[0]<1||s.source[0]>26||!s.verification||!s.observation||!s.move||!s.alternative?.provenance)throw Error('Incomplete annotation');}if(!stateAt(t,t.steps.length).closed)throw Error('Unclosed narrative');return true;}
return {hull,area,polar,shape,transform,lens,stateAt,branchAt,validate};
});
