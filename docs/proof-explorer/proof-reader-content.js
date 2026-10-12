(function(root){
  'use strict';
  const node=typeof module==='object'&&module.exports;
  const P=node?require('./proof.js'):root.HansonWright;
  const W=node?require('./written-proof.js'):root.HansonWrightWritten;
  const A=node?require('./ablation-proofs.js'):root.HansonWrightAblationProofs;
  const K=node?require('./critical-step-selection.js'):root.HansonWrightCriticalSelection;
  const costs={
    sign:'Sign reversal reuses the same upper-tail argument. The replacement constructs all even moments and chooses a moment order; both recover the target norm scales.',
    expand:'The available polarization bound is CK²‖A‖(n+p), too coarse compared with CK²(√p‖A‖F+p‖A‖). This is loss of estimate quality, not measured computational explosion.',
    split:'Schwarz combines MGFs at 2λ, halving the common admissible domain and changing universal constants. The two norm scales are retained; D and S need not be independent.',
    bernstein:'The coefficient replacement requires even-power bookkeeping and a radius choice. It retains cancellation from centering and the two norm scales; a termwise triangle bound loses them.',
    exponential:'The replacement must establish bounds at all even orders, rather than just the variance. It trades quadratic MGFs for coefficient, selector, and vector-moment arguments.',
    linear:'Symmetrization and comparison of even coefficients replace MGF factorization. The sharp √p‖v‖₂ dependence is retained; crude norm inequalities can lose √n or √p.',
    decouple:'The alternative performs n coordinate comparisons and still uses Gaussian MGF control, with ‖H‖≤2‖A‖. This is proof-construction work, not a count of search calls or a demonstrated cost increase.',
    gaussian:'The moment route replaces Gaussian bilinear MGFs with Gaussian projection and Lipschitz norm concentration. It retains the norm scales and still uses Gaussian tools.',
    replace:'This is the same moment-route replacement as the preceding Gaussian-goal action, not a separate discovery. Norm-moment control and a moment-order choice replace the MGF comparison chain.',
    rotate:'Gaussian Lipschitz concentration and a coordinate second-moment identity replace SVD. This changes the required toolkit while preserving the Frobenius and operator scales.',
    compute:'A recurrence and geometric majorant control the entire series without exact evaluation. The original bound and parameter domain are recovered, permitting a checkpoint rejoin.',
    meet:'The alternative assembles moments with Minkowski and closes a different checkpoint. It reuses the full moment route; it does not remove basic logical assembly.',
    optimize:'Choosing p=2⌊αq/2⌋ replaces tuning λ. Scale-dependent parameter selection remains, with even rounding and small-q handling; no discovery-cost comparison is available.',
    finish:'Combining D and S before taking tails produces two probability terms rather than four, giving prefactor 2 directly. This requires upstream MGF estimates, not just the original tail bounds.'
  };
  function build(version){
    if(!['original','detailed','focused'].includes(version))throw Error('Unknown proof edition: '+version);
    return W.passages.map(p=>({
      ...p,events:[...p.events],
      explanations:version==='original'?[]:p.events.filter(id=>id!=='start'&&(version==='detailed'||K.selectedActionIds.includes(id))).map(id=>({
        action:P.byId[id],ablation:A.get(id),cost:costs[id],
        expansion:K.selectedActionIds.includes(id)?K.expansion:[]
      })),
      critical:version==='focused'&&p.events.some(id=>K.selectedActionIds.includes(id))
    }));
  }
  const api={build,costs,selection:K};
  if(node)module.exports=api;else root.HansonWrightReaderContent=api;
})(typeof window==='undefined'?globalThis:window);
