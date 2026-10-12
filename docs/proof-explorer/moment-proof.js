(function (root) {
  'use strict';
  // A worked mathematical reconstruction, not a recorded search or formal certificate.
  // Full derivation: proposals/hanson_wright_sign_ablation.md.
  const nodes = [
    ['independence','given',24,90,'Given','Independent Xᵢ','X₁,…,Xₙ','start'],
    ['centered','given',24,166,'Given','Mean zero','𝔼Xᵢ = 0','start'],
    ['subgaussian','given',24,242,'Given','Subgaussian Xᵢ','‖Xᵢ‖ψ₂ ≤ K','start'],
    ['ultimate','goal endpoint',348,2570,'Ultimate goal','Hanson–Wright','ℙ(|Q| ≥ t) ≤ 2 exp(−cq)','start'],
    ['o-moments','observation',368,2400,'Observation','Control the absolute size.','Markov applies directly to |Q|ᵖ.','moments'],
    ['moment-goal','goal',348,2240,'Main checkpoint','Absolute moments of Q','‖Q‖p ≤ C₀K²(√p F + p O)','moments'],
    ['o-minkowski','observation',368,2080,'Observation','Add the two moment bounds.','No tail union or sign reversal.','split-moments'],
    ['off-moment-goal','goal',348,1910,'Checkpoint','Off-diagonal moments','‖S‖p ≤ CK²(√p F + p O)','split-moments'],
    ['diagonal-moment-goal','goal',348,370,'Side checkpoint','Diagonal moments','‖D‖p ≤ CK²(√p F + p O)','split-moments'],
    ['vector-goal','goal',348,1590,'Reduced checkpoint','Subgaussian vector norm','‖BY‖Lp(ℓ₂) ≤ CK(FB + √p OB)','condition'],
    ['gaussian-moment-goal','goal',348,1270,'Toolkit checkpoint','Gaussian vector norm','‖Bᵀg‖Lp(ℓ₂) ≤ FB + C√p OB','project'],
    ['o-projection','observation',368,1430,'Observation','A Gaussian reads a vector norm.','‖⟨g,v⟩‖p = ap ‖v‖₂; ap ≍ √p.','project'],
    ['expanded','progress',24,370,'Calculation','Separate the expression','Q = D + S','expand'],
    ['coefficient','progress',24,530,'Even-power expansion','Centering removes singletons','Moments ≤ positive coefficients','coefficients'],
    ['diagonal-moment','progress',24,690,'Coefficient estimate','Diagonal moments established','Choose r; bound the coefficient','diagonal-moments'],
    ['linear-moment','progress',24,850,'Toolkit result','Linear-form moments','‖⟨v,X⟩‖p ≤ CK√p ‖v‖₂','linear-moments'],
    ['selector','progress',24,1010,'Strategic construction','Split by random selectors','‖S‖p ≤ 4‖Sδ‖Lp(δ,X)','selectors'],
    ['gaussian-norm','progress',24,1270,'Explicit toolkit dependency','Gaussian norm moments','Lipschitz control + mean bound','gaussian-norm'],
    ['vector-moment','progress',24,1590,'Local meeting','Vector moments established','Divide the projection bound by ap','vector-moments'],
    ['off-moment','progress',24,1910,'Local meeting','Off-diagonal moments established','Condition, average, use block norms','off-moments'],
    ['full-moment','progress',24,2240,'Main meeting','Absolute moments established','Minkowski: ‖Q‖p ≤ ‖D‖p + ‖S‖p','assemble'],
    ['absolute-tail','progress',24,2400,'Parameter choice','Direct absolute Markov','p = 2⌊αq/2⌋; large-q tail ≤ e⁻ᵖ','markov']
  ].map(([id,kind,x,y,label,title,formula,event])=>({id,kind,x,y,label,title,formula,event}));
  const edges = [
    ['ultimate','o-moments','observation'],['o-moments','moment-goal','goal'],
    ['moment-goal','o-minkowski','observation'],['o-minkowski','off-moment-goal','goal'],
    ['o-minkowski','diagonal-moment-goal','goal'],
    ['off-moment-goal','vector-goal','goal'],['vector-goal','o-projection','observation'],['o-projection','gaussian-moment-goal','goal'],
    ['independence','expanded','progress'],['centered','expanded','progress'],
    ['expanded','coefficient','progress'],['coefficient','diagonal-moment','progress'],
    ['subgaussian','linear-moment','progress'],['expanded','selector','progress'],
    ['linear-moment','vector-moment','progress'],['gaussian-norm','vector-moment','progress'],
    ['selector','off-moment','progress'],['vector-moment','off-moment','progress'],
    ['diagonal-moment','full-moment','progress'],['off-moment','full-moment','progress'],['full-moment','absolute-tail','progress']
  ];
  const start = {
    have:'Independent, centered coordinates with ‖Xᵢ‖ψ₂ ≤ K; a fixed real matrix A. The upper-tail/sign-reversal strategy is excluded throughout this route.',
    math:'Q = XᵀAX − 𝔼XᵀAX; F = ‖A‖F; O = ‖A‖; V = K⁴F²; L = K²O.\nAll displayed moment goals are uniform over even integers p ≥ 2. For a block B, FB = ‖B‖F and OB = ‖B‖.\nq = min{t²/V, t/L}. Constants C, C₀, c, α are universal.',
    check:'Work with t, K, F, O > 0. The final assembly also handles t = 0 and zero matrix or zero subgaussian scale. This is a worked derivation with explicit toolkit dependencies; discovery cost is not measured.'
  };
  const events = [
    {id:'moments',direction:'backward',deps:[],add:['moment-goal','o-moments'],focus:'moment-goal',
      title:'Replace the upper-tail reduction with absolute moments.',
      summary:'Ask for a uniform even-moment estimate. It suffices for the two-sided theorem by applying Markov to |Q|ᵖ and choosing p at the tail scale.',
      math:'Sufficient goal: ‖Q‖p ≤ C₀K²(√p F + p O) for every even p ≥ 2.\nℙ(|Q| ≥ t) ≤ t⁻ᵖ 𝔼|Q|ᵖ. The final steps choose p and handle small q.',
      check:'This is an open obligation, not an established moment estimate. No upper-tail result for Q or −Q is invoked.',
      tool:'Markov inequality for a nonnegative random variable.',observation:'Absolute moments encode both signs at once.'},
    {id:'expand',direction:'forward',deps:[],add:['expanded'],focus:'expanded',
      title:'Expand the centered quadratic form.',summary:'Separate independent squares from cross terms.',
      math:'Q = D + S.\nD = Σᵢ aᵢᵢ(Xᵢ² − 𝔼Xᵢ²); S = Σᵢ≠ⱼ aᵢⱼXᵢXⱼ.',
      check:'Independence and zero means give 𝔼XiXj = 0 for i ≠ j. No symmetry of A is required.',
      tool:'Linearity of expectation; independence.',observation:'The same algebraic split remains useful after removing the sign strategy.'},
    {id:'split-moments',direction:'backward',deps:['moments','expand'],add:['diagonal-moment-goal','off-moment-goal','o-minkowski'],focus:'off-moment-goal',
      title:'Reduce to two moment bounds by Minkowski.',summary:'The diagonal and off-diagonal moment estimates together suffice for the requested estimate of Q.',
      math:'‖D + S‖p ≤ ‖D‖p + ‖S‖p.\nRequire both ‖D‖p and ‖S‖p ≤ CK²(√p F + p O), uniformly over even p ≥ 2.',
      check:'Minkowski applies for p ≥ 1; D and S need not be independent. Both branches still need proofs.',
      tool:'Minkowski inequality.',observation:'Splitting a norm avoids splitting the tail event.'},
    {id:'coefficients',direction:'forward',deps:['expand'],add:['coefficient'],focus:'coefficient',
      title:'Expand even powers of the diagonal sum.',summary:'Prove diagonal moment control directly, so a quoted tail inequality cannot conceal the excluded strategy.',
      math:'Zi = aᵢᵢ(Xᵢ² − 𝔼Xᵢ²); choose Mi = CK²|aᵢᵢ| with 𝔼|Zi|ᵏ ≤ k! Miᵏ (k ≥ 2).\nσ² = ΣMi², b = max Mi. Centering eliminates exponents 1.\n𝔼|ΣZi|²ᵐ/(2m)! ≤ [z²ᵐ] ∏ᵢ(1 + Σₖ≥₂ Miᵏzᵏ)\n≤ [z²ᵐ] exp(σ²z²/(1 − bz)).',
      check:'Independence factors mixed moments. Bound their absolute values termwise; Miᵏ ≤ Mi²bᵏ⁻². The formal power series majorant is coefficientwise nonnegative. Its exponential is not a random quadratic-form MGF.',
      tool:'Subgaussian-square and centered subexponential moment bounds; multinomial expansion; coefficientwise majorization.',observation:'For even powers, the whole moment is nonnegative; centering removes singleton factors.'},
    {id:'diagonal-moments',direction:'forward',deps:['coefficients'],add:['diagonal-moment'],focus:'diagonal-moment',
      title:'Choose a radius and close the diagonal moment goal.',summary:'Evaluate the nonnegative coefficient majorant at a suitable radius.',
      math:'For p = 2m, r = min{√m/(2σ), 1/(2b)}.\n[z²ᵐ] exp(σ²z²/(1 − bz)) ≤ r⁻²ᵐ exp(σ²r²/(1 − br)).\nσ²r²/(1 − br) ≤ m/2; ((2m)!)¹ᐟ²ᵐ ≤ 2m.\n‖D‖₂ₘ ≤ C(√m σ + mb) ≤ CK²(√p F + p O).',
      check:'If b = 0 all diagonal coefficients vanish and D = 0. Otherwise 0 < r < 1/b. Use σ ≤ CK²F and b ≤ CK²O. This closes only the diagonal moment checkpoint.',
      tool:'Positive coefficient bound; factorial bound; diagonal entries controlled by the matrix norms.',observation:'Balancing variance and largest coefficient reproduces the two scales without a signed tail.'},
    {id:'linear-moments',direction:'forward',deps:[],add:['linear-moment'],focus:'linear-moment',
      title:'Prepare scalar linear-form moments.',summary:'Use the independent subgaussian toolkit for deterministic linear coefficients.',
      math:'For deterministic v and p ≥ 2, ‖⟨v,X⟩‖p ≤ CK√p ‖v‖₂.',
      check:'Mean zero, independence and the scalar ψ₂ bounds imply subgaussian control of each fixed linear form. Conditional use requires coefficients independent of the coordinates being averaged.',
      tool:'Independent centered subgaussian linear-form bound and subgaussian moment characterization.',observation:'After separating the coordinate sets, one side can act as fixed coefficients.'},
    {id:'selectors',direction:'forward',deps:['expand'],add:['selector'],focus:'selector',
      title:'Decouple cross terms with Bernoulli selectors.',summary:'Average over random coordinate partitions and use convexity of the absolute pth power.',
      math:'δᵢ independent Bernoulli(1/2), independent of X.\nSδ = Σᵢ≠ⱼ δᵢ(1 − δⱼ)aᵢⱼXᵢXⱼ; 𝔼δSδ = S/4.\n‖S‖p ≤ 4(𝔼δ𝔼X|Sδ|ᵖ)¹ᐟᵖ.\nFor fixed Λ = {i: δᵢ = 1}, Sδ = XΛᵀ B XΛᶜ, B = AΛ,Λᶜ.',
      check:'The disjoint coordinate subvectors are independent. The identity is valid for nonsymmetric A as well. Empty blocks contribute zero.',
      tool:'Independent selectors; Jensen inequality.',observation:'The selectors trade dependent cross terms for bilinear forms on independent coordinate sets.'},
    {id:'condition',direction:'backward',deps:['split-moments','selectors','linear-moments'],add:['vector-goal'],focus:'vector-goal',
      title:'Reduce the off-diagonal goal to a vector norm.',summary:'Condition on the second coordinate block and apply the linear-form moment estimate.',
      math:'For fixed Λ, Y = XΛᶜ:\n‖Sδ‖p ≤ CK√p (𝔼‖BY‖₂ᵖ)¹ᐟᵖ.\nIt suffices to show ‖BY‖Lp(ℓ₂) ≤ CK(‖B‖F + √p‖B‖).\nThen average over δ and use ‖B‖F ≤ F, ‖B‖ ≤ O.',
      check:'The conditional scalar inequality is available, but the vector bound is still an obligation. Uniform block bounds are required before averaging over δ.',
      tool:'Conditional linear-form moment bound; coordinate projections.',observation:'A second naive √p factor would lose the desired √p F term; vector norm control matters.'},
    {id:'project',direction:'backward',deps:['condition'],add:['gaussian-moment-goal','o-projection'],focus:'gaussian-moment-goal',
      title:'Read the vector norm through a Gaussian projection.',summary:'Reduce the vector checkpoint to a Gaussian norm estimate; the projection normalization cancels a √p factor.',
      math:'g standard Gaussian in the row space of B, independent of Y; ap = ‖g₁‖p ≍ √p.\nap ‖BY‖Lp(ℓ₂) = ‖⟨g,BY⟩‖Lp(g,Y)\n≤ CK√p ‖Bᵀg‖Lp(ℓ₂).\nIt suffices to bound ‖Bᵀg‖Lp(ℓ₂) ≤ ‖B‖F + C√p‖B‖.',
      check:'Condition on Y for the exact Gaussian projection identity, then on g for the subgaussian linear-form inequality. Divide by ap ≥ c√p; the Gaussian norm estimate remains unproved here.',
      tool:'Gaussian projection identity and scalar Gaussian moments; conditional linear-form bound.',observation:'Random projection preserves the Euclidean norm in Lp up to an explicit scalar factor.'},
    {id:'gaussian-norm',direction:'forward',deps:['project'],add:['gaussian-norm'],focus:'gaussian-norm',
      title:'Apply Gaussian Lipschitz concentration.',summary:'Establish the explicit additional toolkit dependency of the alternative proof.',
      math:'f(g) = ‖Bᵀg‖₂ is ‖B‖-Lipschitz.\n‖f − 𝔼f‖p ≤ C√p ‖B‖; 𝔼f ≤ (𝔼f²)¹ᐟ² = ‖B‖F.\nHence ‖Bᵀg‖Lp(ℓ₂) ≤ ‖B‖F + C√p ‖B‖.',
      check:'g is a standard Gaussian vector. Triangle inequality proves the Lipschitz constant; Jensen and the Gaussian covariance compute the mean bound. The toolkit statement is independent of Hanson–Wright.',
      tool:'HDP-2: Theorem 5.2.3 (Gaussian concentration), Proposition 2.6.1 (subgaussian moments); Jensen and Minkowski.',observation:'Gaussian norm concentration keeps the Frobenius scale in the mean and the operator scale in fluctuations.'},
    {id:'vector-moments',direction:'forward',deps:['gaussian-norm'],add:['vector-moment'],focus:'vector-moment',
      title:'Close the subgaussian vector moment checkpoint.',summary:'Insert Gaussian norm control into the projection reduction.',
      math:'ap ‖BY‖Lp(ℓ₂) ≤ CK√p (‖B‖F + C√p‖B‖).\nap ≥ c√p gives ‖BY‖Lp(ℓ₂) ≤ CK(‖B‖F + √p‖B‖).',
      check:'The √p factors outside the parentheses cancel. This does not yet prove the scalar off-diagonal estimate; substitute it back into the conditional inequality next.',
      tool:'Established projection inequality, Gaussian norm bound, and ap ≍ √p.',observation:'Have and want meet at the vector norm checkpoint.'},
    {id:'off-moments',direction:'forward',deps:['vector-moments'],add:['off-moment'],focus:'off-moment',
      title:'Close the off-diagonal moment checkpoint.',summary:'Return through conditioning and the selector average to the original cross terms.',
      math:'For every Λ, ‖Sδ‖p ≤ CK²(√p‖B‖F + p‖B‖) ≤ CK²(√p F + p O).\n‖S‖p ≤ 4(𝔼δ𝔼|Sδ|ᵖ)¹ᐟᵖ ≤ CK²(√p F + p O).',
      check:'B is a row/column projection of A, so both block norms are bounded uniformly. Absorb 4 into the universal constant.',
      tool:'Established selector, conditional, and vector moment inequalities.',observation:'The desired two matrix scales survive decoupling and averaging.'},
    {id:'assemble',direction:'forward',deps:['off-moments','diagonal-moments'],add:['full-moment'],focus:'full-moment',
      title:'The absolute-moment estimate meets the main goal.',summary:'Assemble the two moment branches. This is the main meeting of the forward and backward proof layers.',
      math:'For every even p ≥ 2:\n‖Q‖p ≤ ‖D‖p + ‖S‖p ≤ C₀K²(√p F + p O).',
      check:'Both branches have been established under the same hypotheses and for all even p ≥ 2. The tail theorem still requires choosing p and checking the small-threshold regime.',
      tool:'Minkowski; the two established moment bounds.',observation:'The whole-form estimate closes a local goal, not yet the final tail theorem.'},
    {id:'markov',direction:'forward',deps:['assemble'],add:['absolute-tail'],focus:'absolute-tail',
      title:'Choose an even moment and apply absolute Markov.',summary:'At large q, a moment order proportional to q gives exponential decay directly for |Q|.',
      math:'q = min{t²/(K⁴F²), t/(K²O)}. Choose α > 0 with C₀(√α + α) ≤ 1/e.\nIf αq ≥ 4, p = 2⌊αq/2⌋ has αq/2 ≤ p ≤ αq and p ≥ 2.\n‖Q‖p/t ≤ 1/e. Therefore ℙ(|Q| ≥ t) ≤ (‖Q‖p/t)ᵖ ≤ e⁻ᵖ ≤ e^(−αq/2).',
      check:'Even rounding stays in the proved moment domain. q ≤ t²/(K⁴F²) and q ≤ t/(K²O) control the two terms separately. This result covers only αq ≥ 4.',
      tool:'Markov on |Q|ᵖ; the assembled moment estimate; even-integer parameter choice.',observation:'The finite optimal moment order captures both tail regimes at once.'},
    {id:'finish',direction:'forward',deps:['markov'],add:[],focus:'ultimate',
      title:'Handle small thresholds and close Hanson–Wright.',summary:'Combine the large-q estimate with the trivial probability bound, and include degenerate cases.',
      math:'Take 0 < c ≤ α log(2)/4.\nIf αq < 4, 2e^(−cq) ≥ 1 ≥ ℙ(|Q| ≥ t).\nIf αq ≥ 4, e^(−αq/2) ≤ 2e^(−cq).\nThus ℙ(|Q| ≥ t) ≤ 2 exp[−c min{t²/(K⁴F²), t/(K²O)}].',
      check:'At t = 0 use probability ≤ 1. If A = 0 or K = 0, Q = 0 almost surely and every positive-threshold probability vanishes. All introduced goals are now discharged; the excluded sign/upper-tail strategy never appears.',
      tool:'Probability ≤ 1; elementary constants and zero cases.',observation:'The alternative reaches the same final theorem without rejoining the upper-tail checkpoint.'}
  ];
  const byId=Object.fromEntries(events.map(e=>[e.id,e]));
  const meetings=[['diagonal-moment','diagonal-moment-goal'],['gaussian-norm','gaussian-moment-goal'],['vector-moment','vector-goal'],['off-moment','off-moment-goal'],['full-moment','moment-goal'],['absolute-tail','ultimate']];
  const closes={ 'diagonal-moments':['diagonal-moment-goal'], 'gaussian-norm':['gaussian-moment-goal'], 'vector-moments':['vector-goal'], 'off-moments':['off-moment-goal'], assemble:['moment-goal'], finish:['ultimate'] };
  const initialNodes=['independence','centered','subgaussian','ultimate'];
  const available=done=>events.filter(e=>!done.includes(e.id)&&e.deps.every(id=>done.includes(id)));
  const visible=done=>new Set([...initialNodes,...done.flatMap(id=>byId[id].add)]);
  const achieved=done=>new Set(done.flatMap(id=>closes[id]||[]));
  const stateConfig={
    statePrefix:'moment-state:',schema:'hanson-wright-moment-states-v1',source:'moment-proof.js',
    interpretation:'Dependency-valid execution orders of a worked absolute-moment alternative to the sign reduction. Locally reconstructed mathematics; not recorded searches or a formally verified proof.',
    mergeRule:'Same completed moves within the absolute-moment proof. No cross-method state equivalence or discovery history is inferred.',
    cost:{measured:false,reason:'Worked mathematical alternative; no search was run. Move count is not difficulty or comparative cost.'},
    refinements:[
      {action:'moments',parent:'ultimate',children:['moment-goal']},
      {action:'split-moments',parent:'moment-goal',children:['diagonal-moment-goal','off-moment-goal']},
      {action:'condition',parent:'off-moment-goal',children:['vector-goal']},
      {action:'project',parent:'vector-goal',children:['gaussian-moment-goal']}
    ],
    goalStatements:{
      ultimate:'ℙ(|Q| ≥ t) ≤ 2 exp[−c min{t²/(K⁴F²), t/(K²O)}], for every real A and t ≥ 0.',
      'moment-goal':'For every even p ≥ 2, ‖Q‖p ≤ C₀K²(√p F + p O).',
      'diagonal-moment-goal':'For every even p ≥ 2, ‖D‖p ≤ CK²(√p F + p O).',
      'off-moment-goal':'For every even p ≥ 2, ‖S‖p ≤ CK²(√p F + p O).',
      'vector-goal':'For each coordinate block B and independent centered subgaussian Y, ‖BY‖Lp(ℓ₂) ≤ CK(‖B‖F + √p‖B‖), for every even p ≥ 2.',
      'gaussian-moment-goal':'For every block B and standard Gaussian g, ‖Bᵀg‖Lp(ℓ₂) ≤ ‖B‖F + C√p‖B‖, for every even p ≥ 2.'
    }
  };
  const api={nodes,edges,events,byId,start,initialNodes,available,visible,achieved,meetings,stateConfig,
    layout:{width:640,height:2740,nodeWidth:240,observationWidth:220,nodeHeight:110,observationHeight:120,givenHeight:62},
    // Long dependencies travel outside the cards; the middle gutter is reserved for meetings.
    rails:{'independence:expanded':8,'centered:expanded':16,'subgaussian:linear-moment':4,'expanded:selector':12,'linear-moment:vector-moment':8,'selector:off-moment':16,'diagonal-moment:full-moment':4,'o-minkowski:diagonal-moment-goal':620}
  };
  if(typeof module==='object'&&module.exports)module.exports=api;else root.HansonWrightMoments=api;
})(typeof window==='undefined'?globalThis:window);
