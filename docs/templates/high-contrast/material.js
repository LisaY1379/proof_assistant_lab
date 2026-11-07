/* Deterministic visual averaging for the introductory material example. */
(()=>{
'use strict';
const $=selector=>document.querySelector(selector);
let materialTimer=null;
const pixels=Array.from({length:32*20},(_,i)=>{const n=Math.sin(i*127.1+311.7)*43758.5453;return n-Math.floor(n);});
function drawMaterial(){const c=$('#material'),ctx=c.getContext('2d'),block=2**Number($('#scale').value);ctx.clearRect(0,0,c.width,c.height);const cols=32,rows=20,w=18,h=16,ox=32,oy=20;for(let y=0;y<rows;y+=block)for(let x=0;x<cols;x+=block){let sum=0,n=0;for(let yy=y;yy<Math.min(rows,y+block);yy++)for(let xx=x;xx<Math.min(cols,x+block);xx++){sum+=pixels[yy*cols+xx];n++;}const v=sum/n;ctx.fillStyle=`hsl(262 48% ${95-v*64}%)`;ctx.fillRect(ox+x*w,oy+y*h,Math.min(block,cols-x)*w-1.3,Math.min(block,rows-y)*h-1.3);}$('#scale-label').textContent=block===1?'Microscopic view':`${block} × ${block} visual blocks`;}
$('#scale').oninput=()=>{clearInterval(materialTimer);materialTimer=null;$('#animate-material').textContent='Animate';drawMaterial();};$('#animate-material').onclick=()=>{if(materialTimer){clearInterval(materialTimer);materialTimer=null;$('#animate-material').textContent='Animate';return;}$('#animate-material').textContent='Pause';materialTimer=setInterval(()=>{$('#scale').value=(Number($('#scale').value)+1)%5;drawMaterial();},1000);};document.addEventListener('visibilitychange',()=>{if(document.hidden){clearInterval(materialTimer);materialTimer=null;$('#animate-material').textContent='Animate';}});drawMaterial();
})();
