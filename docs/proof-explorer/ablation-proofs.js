(function(root){
  'use strict';
  // Curated maps of the written arguments. These are not search recordings.
  const step=(title,have,want)=>({title,have,want});
  const moments=[
    step('Diagonal even-power coefficients','For Zᵢ=aᵢᵢ(Xᵢ²−EXᵢ²), centering removes singleton factors. A positive coefficient majorant gives ‖D‖p ≤ CK²(√p F+pO).','Control the off-diagonal moments at the same scales.'),
    step('Selectors and conditional linear moments','Jensen gives ‖S‖p ≤ 4‖UᵀBY‖p for independent selector blocks. Conditioning gives ‖UᵀBY‖p ≤ CK√p ‖BY‖Lp(ℓ₂).','Establish the vector-norm moment bound.'),
    step('Gaussian projection and norm control','aₚ‖BY‖Lp(ℓ₂)=‖⟨g,BY⟩‖p ≤ CK√p‖Bᵀg‖Lp(ℓ₂). With aₚ ≍ √p and Gaussian Lipschitz concentration, ‖BY‖Lp(ℓ₂) ≤ CK(F_B+√p O_B).','Combine the diagonal and off-diagonal moments.'),
    step('Meet at the whole-form moment bound','Minkowski gives ‖Q‖p ≤ C₀K²(√p F+pO), for every even p ≥ 2.','Turn this family of bounds into the two-sided tail.'),
    step('Absolute Markov and boundary cases','Choose C₀(√α+α) ≤ 1/e and p=2⌊αq/2⌋ when αq≥4. Then P(|Q|≥t)≤e⁻ᵖ. For small q use P≤1; treat zero cases separately.','Hanson–Wright: P(|Q|≥t) ≤ 2e⁻ᶜq. All obligations discharged.')
  ];
  const transforms=[
    step('Prove both transform estimates','Centered-square moment expansion gives E exp(uD) ≤ exp(C_D Vu²). Permitted decoupling, Gaussian replacement and computation give E exp(uS) ≤ exp(C_S Vu²), for |u|≤a_D/L and a_S/L respectively.','Combine D and S without assuming they are independent.'),
    step('Schwarz before taking tails','E exp(λQ) ≤ √(E exp(2λD) E exp(2λS)) ≤ exp(2(C_D+C_S)Vλ²). Domain: |λ|≤min(a_D,a_S)/(2L).','Derive tails for Q and −Q from this whole-form MGF.'),
    step('Two direct tails; prefactor 2','Set C*=2(C_D+C_S), a*=min(a_D,a_S)/2 and λ=min(t/(2C*V),a*/(2L)). Each tail is ≤exp(−λt/2). Their union gives 2exp(−cq); zero cases are immediate.','Hanson–Wright proved without a four-tail union.')
  ];
  const candidate=(title,reason,status='insufficient')=>({title,reason,status});
  const specs={
    sign:{title:'Absolute moments instead of sign reversal',restriction:'No upper-tail/sign-reversal strategy.',family:'absolute-moments',steps:moments,candidates:[]},
    expand:{title:'Whole-form polarization',restriction:'No diagonal/off-diagonal separation anywhere in the replacement proof.',family:'polarization',status:'unresolved',steps:[
      step('Symmetrize the matrix','B=(A+Aᵀ)/2 preserves XᵀAX, with ‖B‖≤O and ‖B‖F≤F.','Center the whole form without separating D and S.'),
      step('Independent-copy polarization','Conditional Jensen gives ‖Q‖p ≤ ‖(X−X′)ᵀB(X+X′)‖p. The two factors are generally dependent.','Bound this dependent bilinear expression sharply.'),
      step('Coarse norm bound','Cauchy–Schwarz yields ‖Q‖p ≤ CK²O(n+p). For A=I this is weaker than CK²(√pn+p).','Sharp continuation unresolved. This candidate does not close the theorem.')
    ],candidates:[candidate('Treat sum and difference as independent','For Rademacher coordinates, (Xᵢ−Xᵢ′)(Xᵢ+Xᵢ′)=0 while both factors can be nonzero. Independence is false.','invalid')]},
    split:{title:'Combine MGFs before taking tails',restriction:'No D/S deviation-event split or allocation of thresholds. Algebraic Q=D+S remains allowed.',family:'whole-form-mgf',steps:transforms,candidates:[candidate('Factor the D/S MGF','D and S share coordinates; E exp(λ(D+S)) cannot generally be factored. Use Schwarz.','invalid')],additional:[{title:'Absolute-moment assembly',steps:moments}]},
    bernstein:{title:'Even-power coefficients replace Bernstein',restriction:'No diagonal Bernstein or reconstruction of its exponential-MGF/Chernoff mechanism.',family:'absolute-moments',steps:moments,candidates:[candidate('Triangle inequality term by term','‖D‖p ≤ CK²p Σ|aᵢᵢ| loses cancellation. For A=I it gives CK²pn, not CK²(√pn+p).')]},
    exponential:{title:'Even moments replace quadratic MGFs',restriction:'No quadratic/bilinear MGF or Chernoff route, including cosh disguises. Scalar linear tools and Gaussian norm concentration remain allowed.',family:'absolute-moments',steps:moments,candidates:[candidate('Use only the variance','Chebyshev gives CK⁴F²/t², a polynomial tail. It does not establish the required exponential tail.')]},
    linear:{title:'Symmetric even-moment comparison',restriction:'No non-Gaussian linear-MGF factorization/comparison, including hidden uses in toolkit lemmas.',family:'symmetric-linear-moments',steps:[
      step('Symmetrize the linear form','Zᵢ=Xᵢ−Xᵢ′ are independent and symmetric; E|ΣvᵢXᵢ|²ᵐ ≤ E|ΣvᵢZᵢ|²ᵐ.','Compare the even moments without non-Gaussian MGFs.'),
      step('Compare nonnegative even coefficients','Odd terms vanish. E Zᵢ²ᵏ ≤ (CK)²ᵏ E gᵢ²ᵏ implies ‖ΣvᵢXᵢ‖p ≤ CK√p‖v‖₂.','Use this lemma at BOTH conditional linear-form calls in the moment proof.'),
      ...moments
    ],candidates:[candidate('Use a coordinate triangle bound','CK√p‖v‖₁ can lose √n relative to CK√p‖v‖₂.')]},
    decouple:{title:'Replace individual coordinates',restriction:'No independent-copy bilinear comparison, selectors, random cuts, or equivalent block decoupling.',family:'coordinate-gaussianization',steps:[
      step('Symmetric hollow form','B=(A+Aᵀ)/2, H=B−diag(B). Then ‖H‖F≤F, ‖H‖≤2O, tr H=0.','Control XᵀHX without an independent second factor.'),
      step('One conditional coordinate comparison','With other coordinates fixed, zᵀHz=c+2zᵢh. Scalar MGF control yields Eᵢe^{λ(c+2Xᵢh)} ≤ e^{λc+2σ²λ²h²}=E_gᵢe^{λ(c+2σgᵢh)}, σ²=CK².','Repeat the comparison for all coordinates.'),
      step('A single coupled Gaussian quadratic form','After n comparisons, E e^{λXᵀHX} ≤ E e^{λσ²gᵀHg}. No block decoupling is used.','Bound the Gaussian quadratic MGF, including its parameter domain.'),
      step('Trace-zero Gaussian MGF','Gaussian diagonalization and tr H=0 give E e^{λσ²gᵀHg} ≤ exp(Cλ²σ⁴‖H‖F²), for |λ|≤c/(σ²‖H‖).','Prove the diagonal MGF and combine with this off-diagonal MGF.'),
      step('Whole-Q assembly and closure','Prove the diagonal MGF by centered-square moment expansion. Schwarz combines the two MGFs with a halved domain; Chernoff for Q and −Q gives 2e⁻ᶜq.','Hanson–Wright proved; the old independent-copy bilinear state was never established.')
    ],candidates:[candidate('Rotate X directly','General independent subgaussian coordinates do not retain independence under arbitrary orthogonal rotations.','invalid')],provenance:'Found online in Ziemann (2025), §2; adapted here to independent coordinates with a common scalar MGF bound. This is a worked, literature-assisted replacement, not an independent discovery by the search agents.',source:{title:'Ingvar Ziemann · An Elementary Proof of The Hanson-Wright Inequality (2025), §2',url:'https://arxiv.org/html/2509.00881v1#S2'},interpretation:'This establishes mathematical replaceability with the source available. It does not show that a first attempter would find this route, that discovery costs are equal or lower, or that decoupling is unimportant to the original proof. The n coordinate comparisons count proof-construction steps, not invention effort. Retrieval, adaptation, verification, and independent discovery costs have not been measured; source-restricted searches must assess this source-assisted result separately.'},
    gaussian:{title:'Vector moments replace Gaussian MGF comparison',restriction:'No Gaussian quadratic/bilinear MGF comparison. Gaussian projection and Lipschitz norm concentration remain allowed; the all-Gaussian-tools ban is unresolved.',family:'absolute-moments',steps:moments,candidates:[candidate('Use coordinate Gaussianization','This still compares quadratic MGFs and violates the strategy ban.','inadmissible'),candidate('Cite a PSD upper-tail bound','A variance-proxy trace center need not equal the actual mean, and a lower tail is still missing.')]},
    replace:{title:'Bypass the Gaussian replacement chain',restriction:'Same global Gaussian-MGF comparison ban as gaussian, including one-coordinate replacements. Broader removal of all Gaussian tools remains unresolved.',family:'absolute-moments',steps:moments,candidates:[candidate('Replace only one vector','The first exponential comparison already violates the ban. A remaining random norm also needs sharp control.','inadmissible')]},
    rotate:{title:'Lipschitz norm control without SVD',restriction:'No matrix spectral diagonalization, including equivalent eigenvalue, determinant, or hidden toolkit reductions.',family:'absolute-moments',steps:[
      step('Mean and Lipschitz constant in existing coordinates','For f(g)=‖Bᵀg‖₂, |f(g)−f(h)|≤‖B‖‖g−h‖₂ and Ef≤√ΣBᵢⱼ²=‖B‖F.','Control fluctuations using Gaussian concentration independent of the banned diagonalization.'),
      step('Norm moments without matrix rotation','Gaussian Lipschitz concentration yields ‖Bᵀg‖Lp(ℓ₂) ≤ ‖B‖F+C√p‖B‖. Scalar Gaussian projections do not diagonalize B.','Supply this estimate to the vector checkpoint of the complete moment route.'),
      ...moments
    ],candidates:[candidate('Bound by ‖B‖‖g‖₂','This gives C‖B‖(√n+√p), which can lose √n even for rank-one B.')]},
    compute:{title:'Bound coefficients instead of evaluating the MGF',restriction:'No exact Gaussian product/square MGF, determinant evaluation, or resummation to the same closed form.',family:'coefficient-majorant',rejoin:'compute',steps:[
      step('Gaussian even moments','For W=gg′, E W²ᵐ/(2m)!=binom(2m,m)/4ᵐ=:cₘ. These moments follow by integration by parts.','Control the entire infinite series with an upper bound.'),
      step('Coefficient recurrence','c₁=1/2 and cₘ₊₁/cₘ=(2m+1)/(2m+2)<1, hence cₘ≤1/2.','Bound all remaining terms; finite truncation alone is insufficient.'),
      step('Geometric majorant','Symmetry and Tonelli give Ee^{uW}=E cosh(uW) ≤ 1+u²/[2(1−u²)] ≤ 1+u² ≤ e^{u²} when u²≤1/2.','Multiply the scalar bounds in the permitted SVD representation.'),
      step('Recover the computed checkpoint','E exp(θgᵀAg′) ≤ exp(θ²F²), |θ|O≤1/√2. Both the original estimate and its domain are recovered.','Rejoin after compute; retain the original meet, optimize, and finish steps.')
    ],candidates:[candidate('Truncate after the quadratic term','All omitted even coefficients are positive. Without a remainder bound, the approximation is not an upper bound.','invalid')]},
    meet:{title:'Meet at a moment goal instead',restriction:'No closure through the original quadratic-MGF comparison chain, including inlining it. Basic substitution and transitivity remain allowed.',family:'absolute-moments',steps:moments,candidates:[candidate('Drop the parameter cutoff','Substituting θ=bK²λ requires |λ|≤a/(bK²O). The exponent bound alone cannot justify unrestricted λ.','invalid'),candidate('Inline the same chain into optimize','Valid algebra, but the banned MGF strategy has still been used.','inadmissible')]},
    optimize:{title:'Choose an even moment order',restriction:'No threshold-dependent Chernoff-parameter tuning. A threshold-dependent moment order remains allowed.',family:'absolute-moments',steps:moments,candidates:[candidate('Use fixed λ proportional to 1/L','The exponent may be positive at moderate t; the uniform quadratic regime is lost.'),candidate('Use λ proportional to t/V everywhere','At large t this leaves the established MGF domain.','invalid'),candidate('Use λ=ct/(V+Lt)','This retains the banned threshold-dependent Chernoff mechanism.','inadmissible')]},
    finish:{title:'Combine transforms, then take two tails',restriction:'No four-tail D/S/sign union and prefactor absorption. Basic final inference remains allowed.',family:'whole-form-mgf',steps:transforms,candidates:[candidate('Change the prefactor 4 to 2','An upper bound 4e⁻ᶜq does not imply the smaller bound 2e⁻ᶜq.','invalid')],additional:[{title:'Absolute moments for a broader sign-union ban',steps:moments}]}
  };
  function get(action){
    const spec=specs[action];if(!spec)throw Error('Unknown ablation action: '+action);
    return JSON.parse(JSON.stringify({action,status:'worked',provenance:'Written mathematical reconstruction; not a recorded search or formal certificate.',cost:{measured:false},...spec}));
  }
  function create(action,graph){
    const data=get(action),index=graph.canonicalTransitions.findIndex(id=>graph.transitions.find(e=>e.id===id).action===action);
    if(index<0)throw Error('Missing reference action: '+action);
    return {...data,sourceState:graph.canonicalStates[index],selectedState:graph.canonicalStates[index+1],removedTransition:graph.transitions.find(e=>e.id===graph.canonicalTransitions[index]),
      rejoinState:data.rejoin?graph.canonicalStates[index+1]:null,
      restart:action!=='compute',
      scope:action==='compute'?'The preceding reference facts remain usable. The replacement recovers the required bound and domain.':'Replan from the theorem assumptions under the global ban. Earlier reference checkpoints are context, not inherited premises; the branch includes the changed upstream obligations.'};
  }
  // A displayed reference state belongs to the move that produced it. Its
  // predecessor is still the mathematical fork point when that move is removed.
  function actionAtState(graph,id){
    const index=graph.canonicalStates.indexOf(id);
    if(index<0)throw Error('Choose a state in the reference order');
    return index===0?null:graph.transitions.find(e=>e.id===graph.canonicalTransitions[index-1]).action;
  }
  const api={get,create,actionAtState,actions:Object.keys(specs)};
  if(typeof module==='object'&&module.exports)module.exports=api;else root.HansonWrightAblationProofs=api;
})(typeof window==='undefined'?globalThis:window);
