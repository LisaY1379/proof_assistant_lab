(function(root){
  'use strict';
  // Recorded editorial recommendation from the dedicated LLM agent requested
  // by the user. Reading this static page does not trigger another model call.
  const selection={
    selectedActionIds:['decouple'],
    selectionLabel:'LLM-selected key step',
    provenance:'Selected by a dedicated LLM agent for this reading edition, 11 October 2026.',
    rationale:'Decoupling is the central conceptual bridge in this proof: it turns dependent quadratic cross terms into a bilinear form with independent inputs. Conditioning on one input then makes the other a linear form, so the prepared subgaussian bound becomes usable.',
    caveat:'This selection is an LLM editorial judgment about the reference proof, not a measured difficulty ranking or evidence that decoupling is indispensable.',
    alternativeNote:'Decoupling is replaceable in the attached ablation: a hollow quadratic form can be Gaussianized one coordinate at a time. That alternative also exploits conditional linearity, but it does not recreate the independent-copy bilinear state.',
    expansion:[
      {title:'Why the original expression is difficult to use',text:'The terms in S=Σᵢ≠ⱼaᵢⱼXᵢXⱼ share coordinates. Independence of the Xᵢ does not make these products independent, so an independent-sum estimate cannot be applied directly. We need to retain randomness in one factor while holding the other fixed.'},
      {title:'Construct a random partition',text:'Choose independent δᵢ∼Bernoulli(1/2), independent of X, and define Sδ=Σᵢⱼδᵢ(1−δⱼ)aᵢⱼXᵢXⱼ. Every off-diagonal ordered pair survives with probability 1/4; diagonal terms vanish. Therefore S=4EδSδ. Convexity gives the first comparison.',math:'Eₓ exp(λS) ≤ Eδ Eₓ exp(4λSδ).'},
      {title:'Expose two independent blocks',text:'For a fixed partition I={i:δᵢ=1}, the groups X_I and X_{Iᶜ} are independent. With an independent copy X′, Sδ has the same distribution as Σᵢ∈I,ⱼ∉I aᵢⱼXᵢX′ⱼ. Centering and independence make this block sum the conditional expectation of XᵀAX′ given X_I and X′_{Iᶜ}. A second application of Jensen bounds its exponential moment by the full bilinear form.',math:'E exp(4λSδ) ≤ E exp(4λXᵀAX′).\nThus E exp(λS) ≤ E exp(4λXᵀAX′).'},
      {title:'What the construction buys us',text:'Conditional on X′, AX′ is a fixed vector independent of X. The fixed-coefficient subgaussian bound now applies. The factor 4 is absorbed into the absolute constant. This prepares the Gaussian comparison; it does not yet close the proof.',math:'Eₓ exp(4λ⟨X,AX′⟩) ≤ exp(CK²λ²‖AX′‖₂²).'},
      {title:'What remains important if we change routes',text:'The comparison is not equality in distribution. The alternative coordinate-Gaussianization proof avoids random partitions: a hollow quadratic form is linear in each coordinate when the others are fixed. Both routes expose conditional linearity inside a dependent quadratic expression. Their relative discovery cost has not been measured.'}
    ]
  };
  if(typeof module==='object'&&module.exports)module.exports=selection;else root.HansonWrightCriticalSelection=selection;
})(typeof window==='undefined'?globalThis:window);
