(function (root) {
  'use strict';
  // The order here is the order of a finished proof, independent of the
  // discovery-order events in proof.js. Several events can visit one passage.
  const passages = [
    {id:'setup', title:'Notation and trivial cases', events:['start'], html:`
      <p><em>Proof.</em> Write Q = XᵀAX − 𝔼XᵀAX, K = maxᵢ ‖Xᵢ‖<sub>ψ₂</sub>,
      V = K⁴‖A‖<sub>F</sub>², and L = K²‖A‖. If A = 0 or K = 0, then Q = 0 almost surely, so the result is immediate; the case t = 0 is also immediate.
      Henceforth assume t &gt; 0 and V,L &gt; 0. Constants c,C &gt; 0 below are absolute and may change from line to line.</p>`},
    {id:'sign', title:'Reduction to an upper tail', events:['sign'], html:`
      <p>It suffices to bound ℙ(Q ≥ t). Indeed, replacing A by −A replaces Q by −Q and preserves both matrix norms. The same upper-tail estimate therefore applies to the lower tail, and the two estimates can be combined by the union bound.</p>`},
    {id:'expand', title:'Expansion of the quadratic form', events:['expand'], html:`
      <p>By independence and the mean-zero assumption, 𝔼(XᵢXⱼ) = 0 for i ≠ j. Consequently,</p>
      <div class="proof-equation">Q = <span>∑ᵢ aᵢᵢ(Xᵢ² − 𝔼Xᵢ²)</span> + <span>∑ᵢ≠ⱼ aᵢⱼXᵢXⱼ</span> =: D + S.</div>`},
    {id:'split', title:'Diagonal and off-diagonal branches', events:['split'], html:`
      <p>We estimate the two sums separately. Since D + S ≥ t implies that D ≥ t/2 or S ≥ t/2,</p>
      <div class="proof-equation">ℙ(Q ≥ t) ≤ ℙ(D ≥ t/2) + ℙ(S ≥ t/2).</div>
      <p>No independence between D and S is required for this reduction.</p>`},
    {id:'diagonal', title:'The diagonal estimate', events:['bernstein'], html:`
      <p>The variables Xᵢ² − 𝔼Xᵢ² are independent, centered, and subexponential, with
      ‖Xᵢ² − 𝔼Xᵢ²‖<sub>ψ₁</sub> ≤ CK². Bernstein’s inequality, together with
      ∑ᵢ aᵢᵢ² ≤ ‖A‖<sub>F</sub>² and maxᵢ |aᵢᵢ| ≤ ‖A‖, yields</p>
      <div class="proof-equation">ℙ(D ≥ t/2) ≤ exp[−c min{t²/V, t/L}].</div>
      <p>If the diagonal of A is zero, this estimate holds directly because D = 0.</p>`},
    {id:'chernoff', title:'Exponential Markov bound', events:['exponential'], html:`
      <p>For the off-diagonal sum, fix λ &gt; 0. Applying Markov’s inequality to exp(λS), we obtain</p>
      <div class="proof-equation">ℙ(S ≥ t/2) ≤ exp(−λt/2) 𝔼 exp(λS).</div>
      <p>We will prove that 𝔼 exp(λS) ≤ exp(CVλ²) for 0 &lt; λ ≤ c₀/L, and then choose λ in that range.</p>`},
    {id:'decouple', title:'Decoupling', events:['decouple'], html:`
      <p>Let X′ be an independent copy of X. The off-diagonal decoupling inequality, applied to the convex function s ↦ exp(λs), gives</p>
      <div class="proof-equation">𝔼 exp(λS) ≤ 𝔼 exp(4λXᵀAX′).</div>
      <p>The version used here permits the full matrix A on the right. Conditional on X′, the bilinear form XᵀAX′ is the linear form ⟨X,AX′⟩ with fixed coefficients.</p>`},
    {id:'linear', title:'A fixed-coefficient MGF bound', events:['linear'], html:`
      <p>For every fixed vector v and every real η, independence and the mean-zero subgaussian MGF estimate imply</p>
      <div class="proof-equation">𝔼 exp(η⟨X,v⟩) = ∏ᵢ 𝔼 exp(ηvᵢXᵢ)<br>
      ≤ ∏ᵢ exp(CK²η²vᵢ²) = exp(CK²η²‖v‖₂²).</div>`},
    {id:'replacement', title:'Gaussian replacement', events:['gaussian','replace'], html:`
      <p>Let g,g′ be independent standard Gaussian vectors, independent of X,X′. The Gaussian MGF identity is</p>
      <div class="proof-equation">𝔼<sub>g</sub> exp(μ⟨g,v⟩) = exp(μ²‖v‖₂²/2).</div>
      <p>Choosing μ = √(2C)Kη matches the preceding subgaussian upper bound. Condition first on X′ and use v = AX′ to replace X by g. Average over X′, then condition on g and apply the same argument to X′. Absorbing the decoupling factor 4 into an absolute constant, we obtain</p>
      <div class="proof-equation">𝔼 exp(4λXᵀAX′) ≤ 𝔼 exp(C₁K²λgᵀAg′).</div>`},
    {id:'rotation', title:'Singular value decomposition', events:['rotate'], html:`
      <p>Write A = U diag(sᵢ)Rᵀ. By Gaussian rotation invariance, Uᵀg and Rᵀg′ remain independent standard Gaussian vectors. Therefore gᵀAg′ has the same distribution as ∑ᵢ sᵢgᵢgᵢ′, and independence of the pairs gives</p>
      <div class="proof-equation">𝔼 exp(θgᵀAg′) = ∏ᵢ 𝔼 exp(θsᵢgᵢgᵢ′).</div>`},
    {id:'scalar', title:'Evaluation of the Gaussian MGF', events:['compute'], html:`
      <p>For independent scalar standard Gaussians g₁,g₁′, conditioning on g₁ and then using the MGF of g₁² gives</p>
      <div class="proof-equation">𝔼 exp(ug₁g₁′) = 𝔼 exp(u²g₁²/2)<br>
      = (1 − u²)<sup>−1/2</sup> ≤ exp(u²), &nbsp; u² ≤ 1/2.</div>
      <p>Here the inequality follows from −½ log(1−z) ≤ z for 0 ≤ z ≤ 1/2. Substituting u = θsᵢ in each factor, and using ∑ᵢsᵢ² = ‖A‖<sub>F</sub>² and maxᵢsᵢ = ‖A‖, yields</p>
      <div class="proof-equation">𝔼 exp(θgᵀAg′) ≤ exp(θ²‖A‖<sub>F</sub>²),<br>
      |θ| ≤ 1/(√2 ‖A‖).</div>`},
    {id:'mgf', title:'The required exponential moment', events:['meet'], html:`
      <p>Combining decoupling, replacement, and the Gaussian estimate with θ = C₁K²λ proves</p>
      <div class="proof-equation">𝔼 exp(λS) ≤ exp(CK⁴λ²‖A‖<sub>F</sub>²)<br>
      = exp(CVλ²), &nbsp; |λ| ≤ c₀/L.</div>
      <p>The absolute constant c₀ accounts for the parameter rescaling. This is the exponential-moment estimate required above.</p>`},
    {id:'optimization', title:'Choice of the exponential parameter', events:['optimize'], html:`
      <p>The exponential Markov bound now becomes ℙ(S ≥ t/2) ≤ exp(−λt/2 + CVλ²). Choose</p>
      <div class="proof-equation">λ = min{t/(4CV), c₀/(2L)}.</div>
      <p>This choice is admissible and satisfies CVλ² ≤ λt/4. It follows that</p>
      <div class="proof-equation">ℙ(S ≥ t/2) ≤ exp(−λt/4)<br>
      ≤ exp[−c min{t²/V, t/L}].</div>`},
    {id:'conclusion', title:'Combination of the estimates', events:['finish'], html:`
      <p>Combining the bounds for D and S gives the upper-tail estimate for Q. Apply the same argument to −A and add the two tail probabilities. With q = min{t²/V,t/L}, this gives</p>
      <div class="proof-equation">ℙ(|Q| ≥ t) ≤ min{1, 4 exp(−cq)} ≤ 2 exp(−cq/2).</div>
      <p>Indeed, when q ≤ 2 log(2)/c the last expression is at least 1; otherwise it bounds 4 exp(−cq). Renaming c/2 as c establishes the stated inequality. <span class="qed" aria-label="End of proof">□</span></p>`}
  ];
  const byEvent=Object.fromEntries(passages.flatMap(p=>p.events.map(id=>[id,p])));
  const api={passages,byEvent};
  if(typeof module==='object'&&module.exports)module.exports=api;
  else root.HansonWrightWritten=api;
})(typeof window==='undefined'?globalThis:window);
