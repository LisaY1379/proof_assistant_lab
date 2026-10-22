/* Bass diffusion in continuous time. Rates use inverse years; m uses millions. */
(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else root.BassModel=api;})(typeof globalThis!=='undefined'?globalThis:this,function(){
'use strict';
function at(t,p,q,m){
 if(![t,p,q,m].every(Number.isFinite)||t<0||p<0||q<0||m<=0)throw Error('Expected t,p,q ≥ 0 and m > 0.');
 if(p===0)return {F:0,Y:0,S:0,external:0,social:0,hazard:0};
 const e=Math.exp(-(p+q)*t),F=p*(-Math.expm1(-(p+q)*t))/(p+q*e),remaining=m*(1-F);
 const external=p*remaining,social=q*F*remaining;
 return {F,Y:m*F,S:external+social,external,social,hazard:p+q*F};
}
function peak(p,q,m){
 at(0,p,q,m);
 if(p===0)return {t:null,sales:0,fraction:0,kind:'No adoption from F(0)=0'};
 if(q<=p)return {t:0,sales:m*p,fraction:0,kind:'Maximum at launch'};
 return {t:Math.log(q/p)/(p+q),sales:m*(p+q)**2/(4*q),fraction:(q-p)/(2*q),kind:'Interior peak'};
}
// Three-point discrete approximation, deliberately BEFORE the paper's correction.
function fitEarly(s0,s1,s2){
 if(![s0,s1,s2].every(v=>Number.isFinite(v)&&v>0))return {valid:false,reason:'Positive sales observations are required.'};
 const x1=s0,x2=s0+s1,a=s0,c=((s2-a)/x2-(s1-a)/x1)/(x2-x1),b=(s1-a)/x1-c*x1;
 if(c>=0)return {valid:false,a,b,c,reason:'c ≥ 0: the fitted quadratic has no finite positive-market Bass parameterization.'};
 const m=(-b-Math.sqrt(b*b-4*c*a))/(2*c),p=a/m,q=-c*m;
 if(![m,p,q].every(v=>Number.isFinite(v)&&v>0))return {valid:false,a,b,c,reason:'No admissible positive parameters.'};
 return {valid:true,a,b,c,m,p,q};
}
function timingMAE(products){const rows=products.filter(d=>d.peakActual!==null);return rows.reduce((s,d)=>s+Math.abs(d.peakPredicted-d.peakActual),0)/rows.length;}
return {at,peak,fitEarly,timingMAE};
});
