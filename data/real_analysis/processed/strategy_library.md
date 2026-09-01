# Proof Strategy Library

Generated at: 2026-08-23T23:12:25.069447+00:00
Total strategies: 321

## 1. Apply the standard metric-space ε–δ characterization `Metric.continuousWithinAt_iff` to express relative continuity on \(S\) in terms of distances.

- Source theorem/lemma: `continuous_at_iff_eps_delta`
- Source proof id: `atlas.real_analysis.256351aca4f3`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/ContinuousFunctions/Continuity.lean`

## 2. Specialize the metric on \(\mathbb{R}\) using `Real.dist_eq`, which rewrites each distance as an absolute difference and yields exactly the desired formulation.

- Source theorem/lemma: `continuous_at_iff_eps_delta`
- Source proof id: `atlas.real_analysis.256351aca4f3`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/ContinuousFunctions/Continuity.lean`

## 3. Recognize that the closed interval \([a,b]\) is compact and apply the theorem that a continuous real-valued function on a compact set admits a uniform norm bound.

- Source theorem/lemma: `continuous_on_Icc_bounded`
- Source proof id: `atlas.real_analysis.40a706b8d34b`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/ContinuousFunctions/Continuity.lean`

## 4. Convert the resulting inequality \(\|f(x)\|\le C\) into the required inequality \(|f(x)|\le C\) using the identity between the real norm and absolute value.

- Source theorem/lemma: `continuous_on_Icc_bounded`
- Source proof id: `atlas.real_analysis.40a706b8d34b`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/ContinuousFunctions/Continuity.lean`

## 5. The strict inequality \(a<b\) implies \(a\le b\), ensuring that the closed interval \([a,b]\) is nonempty.

- Source theorem/lemma: `extreme_value_theorem`
- Source proof id: `atlas.real_analysis.2b19d4ad0017`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/ContinuousFunctions/Continuity.lean`

## 6. The interval \([a,b]\) is compact, so continuity of \(f\) on this nonempty compact set guarantees that \(f\) attains both a minimum and a maximum there.

- Source theorem/lemma: `extreme_value_theorem`
- Source proof id: `atlas.real_analysis.2b19d4ad0017`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/ContinuousFunctions/Continuity.lean`

## 7. Applying the compact-set minimum and maximum existence results separately produces \(c,d\in[a,b]\) with \(f(c)\le f(x)\le f(d)\) for every \(x\in[a,b]\).

- Source theorem/lemma: `extreme_value_theorem`
- Source proof id: `atlas.real_analysis.2b19d4ad0017`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/ContinuousFunctions/Continuity.lean`

## 8. Strengthen \(a<b\) to \(a\le b\) so the closed-interval intermediate value theorem applies on \([a,b]\).

- Source theorem/lemma: `intermediate_value_theorem`
- Source proof id: `atlas.real_analysis.0981157bc4ef`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/ContinuousFunctions/IVT.lean`

## 9. Convert the strict inequalities placing \(y\) between \(f(a)\) and \(f(b)\) into membership in the appropriate closed interval of endpoint values, using \([f(a),f(b)]\) in the increasing case and \([f(b),f(a)]\) in the decreasing case.

- Source theorem/lemma: `intermediate_value_theorem`
- Source proof id: `atlas.real_analysis.0981157bc4ef`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/ContinuousFunctions/IVT.lean`

## 10. Apply the corresponding closed-interval intermediate value theorem to obtain \(c\in[a,b]\) satisfying \(f(c)=y\).

- Source theorem/lemma: `intermediate_value_theorem`
- Source proof id: `atlas.real_analysis.0981157bc4ef`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/ContinuousFunctions/IVT.lean`

## 11. Upgrade \(c\in[a,b]\) to \(c\in(a,b)\) by ruling out \(c=a\) and \(c=b\), since either endpoint equality together with \(f(c)=y\) would contradict the strict inequalities on \(y\).

- Source theorem/lemma: `intermediate_value_theorem`
- Source proof id: `atlas.real_analysis.0981157bc4ef`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/ContinuousFunctions/IVT.lean`

## 12. Define the polynomial as a continuous real-valued function \(f(x)=x^{2021}+x^{2020}+9.03x+1\).

- Source theorem/lemma: `polynomial_has_real_root`
- Source proof id: `atlas.real_analysis.84d958addbb6`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/ContinuousFunctions/IVT.lean`

## 13. Evaluate the endpoints \(-1\) and \(0\) to obtain the crucial sign change \(f(-1)=-8.03<0<f(0)=1\).

- Source theorem/lemma: `polynomial_has_real_root`
- Source proof id: `atlas.real_analysis.84d958addbb6`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/ContinuousFunctions/IVT.lean`

## 14. Apply the Intermediate Value Theorem on \([-1,0]\) to conclude that some \(c\in[-1,0]\) satisfies \(f(c)=0\).

- Source theorem/lemma: `polynomial_has_real_root`
- Source proof id: `atlas.real_analysis.84d958addbb6`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/ContinuousFunctions/IVT.lean`

## 15. Rewrite `AccPt x (𝓟 S)` using `accPt_iff_nhds`, turning the topological claim into the statement that every neighborhood of \(x\) contains a point of \(S\) distinct from \(x\).

- Source theorem/lemma: `cluster_point_iff_acc_point`
- Source proof id: `atlas.real_analysis.67ce5a8edceb`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/ContinuousFunctions/Limits.lean`

## 16. In the forward direction, use the metric neighborhood basis to find an open ball around \(x\) contained in an arbitrary neighborhood, then apply the elementary cluster-point hypothesis inside that ball.

- Source theorem/lemma: `cluster_point_iff_acc_point`
- Source proof id: `atlas.real_analysis.67ce5a8edceb`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/ContinuousFunctions/Limits.lean`

## 17. In the reverse direction, test the accumulation-point hypothesis on the open ball \(B(x,\delta)\), which is a neighborhood whenever \(\delta>0\).

- Source theorem/lemma: `cluster_point_iff_acc_point`
- Source proof id: `atlas.real_analysis.67ce5a8edceb`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/ContinuousFunctions/Limits.lean`

## 18. Translate ball membership into the required absolute-value inequality using \(\operatorname{dist}(x,y)=|x-y|\) on \(\mathbb R\) and the symmetry of absolute differences.

- Source theorem/lemma: `cluster_point_iff_acc_point`
- Source proof id: `atlas.real_analysis.67ce5a8edceb`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/ContinuousFunctions/Limits.lean`

## 19. Rewrite the filter statement using `Metric.tendsto_nhdsWithin_nhds`, turning `Tendsto` into the same ε–δ form as the elementary definition.

- Source theorem/lemma: `function_limit_iff_tendsto`
- Source proof id: `atlas.real_analysis.bb1610265d4d`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/ContinuousFunctions/Limits.lean`

## 20. Recognize that membership in \(S \setminus \{c\}\) is exactly the conjunction \(x \in S\) and \(x \ne c\), so the restricted filter encodes the punctured-domain condition.

- Source theorem/lemma: `function_limit_iff_tendsto`
- Source proof id: `atlas.real_analysis.bb1610265d4d`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/ContinuousFunctions/Limits.lean`

## 21. Use \(x \ne c \iff 0<|x-c|\) to translate between exclusion of the point \(c\) and the elementary definition’s strict positivity hypothesis.

- Source theorem/lemma: `function_limit_iff_tendsto`
- Source proof id: `atlas.real_analysis.bb1610265d4d`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/ContinuousFunctions/Limits.lean`

## 22. Rewrite real distances via `Real.dist_eq`, identifying \(d(x,c)\) and \(d(f(x),L)\) with the corresponding absolute differences.

- Source theorem/lemma: `function_limit_iff_tendsto`
- Source proof id: `atlas.real_analysis.bb1610265d4d`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/ContinuousFunctions/Limits.lean`

## 23. Reinterpret the cluster-point hypothesis as saying that the punctured neighborhood filter \(\operatorname{nhdsWithin}(c, S \setminus \{c\})\) is nontrivial (`NeBot`).

- Source theorem/lemma: `function_limit_unique`
- Source proof id: `atlas.real_analysis.6587f64283a7`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/ContinuousFunctions/Limits.lean`

## 24. Convert both function-limit hypotheses into filter convergence of \(f\) to \(L_1\) and \(L_2\) along that same punctured neighborhood filter.

- Source theorem/lemma: `function_limit_unique`
- Source proof id: `atlas.real_analysis.6587f64283a7`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/ContinuousFunctions/Limits.lean`

## 25. Apply uniqueness of limits in the Hausdorff space \(\mathbb R\) for a nontrivial filter to conclude \(L_1=L_2\).

- Source theorem/lemma: `function_limit_unique`
- Source proof id: `atlas.real_analysis.6587f64283a7`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/ContinuousFunctions/Limits.lean`

## 26. Invoke the general metric-space characterization `Metric.uniformContinuousOn_iff`, which already expresses uniform continuity on a set through a single \(\delta\) working for every pair of points in that set.

- Source theorem/lemma: `uniform_continuous_on_iff`
- Source proof id: `atlas.real_analysis.5b5917979e9d`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/ContinuousFunctions/UniformContinuity.lean`

## 27. Rewrite the real metric using `Real.dist_eq`, namely \(d(x,y)=|x-y|\), both in the domain and codomain, so the abstract metric criterion becomes exactly the stated absolute-value \(\varepsilon\)–\(\delta\) condition.

- Source theorem/lemma: `uniform_continuous_on_iff`
- Source proof id: `atlas.real_analysis.5b5917979e9d`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/ContinuousFunctions/UniformContinuity.lean`

## 28. Use `simp only` to perform these unfoldings and rewrites, after which the two propositions are syntactically identical.

- Source theorem/lemma: `uniform_continuous_on_iff`
- Source proof id: `atlas.real_analysis.5b5917979e9d`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/ContinuousFunctions/UniformContinuity.lean`

## 29. Rewrite the difference quotient \(x \mapsto (f(x)-f(c))/(x-c)\) as the standard slope function `slope f c`, with the punctured neighborhood \(x \ne c\) avoiding division by zero.

- Source theorem/lemma: `differentiable_at_iff_limit_exists`
- Source proof id: `atlas.real_analysis.9f333d74ac85`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Basic.lean`

## 30. In the forward direction, convert differentiability at \(c\) into `HasDerivAt f (deriv f c) c` and apply `hasDerivAt_iff_tendsto_slope` to obtain the required limit.

- Source theorem/lemma: `differentiable_at_iff_limit_exists`
- Source proof id: `atlas.real_analysis.9f333d74ac85`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Basic.lean`

## 31. In the reverse direction, apply the converse of `hasDerivAt_iff_tendsto_slope` to the assumed slope limit, producing `HasDerivAt f L c`, and then conclude differentiability.

- Source theorem/lemma: `differentiable_at_iff_limit_exists`
- Source proof id: `atlas.real_analysis.9f333d74ac85`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Basic.lean`

## 32. Use `hf.comp c hg` to obtain differentiability of \(f \circ g\) at \(c\) from the differentiability of \(g\) at \(c\) and \(f\) at \(g(c)\).

- Source theorem/lemma: `chain_rule`
- Source proof id: `atlas.real_analysis.dec4c1aa763f`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Basic.lean`

## 33. Apply `deriv_comp c hf hg`, the derivative chain rule, to derive \(\operatorname{deriv}(f \circ g)(c)=\operatorname{deriv}f(g(c))\operatorname{deriv}g(c)\).

- Source theorem/lemma: `chain_rule`
- Source proof id: `atlas.real_analysis.dec4c1aa763f`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Basic.lean`

## 34. Combine these two results as a conjunction using `⟨…, …⟩`.

- Source theorem/lemma: `chain_rule`
- Source proof id: `atlas.real_analysis.dec4c1aa763f`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Basic.lean`

## 35. Introduce a general equivalence translating an eventual property on the relative neighborhood filter `nhdsWithin c S` into an explicit positive-radius condition on points of \(S\).

- Source theorem/lemma: `relative_extremum_def`
- Source proof id: `atlas.real_analysis.d4ac68a30456`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/MVT.lean`

## 36. Use `eventually_nhdsWithin_iff` and `Metric.eventually_nhds_iff`, together with `Real.dist_eq`, to rewrite “sufficiently close to \(c\) within \(S\)” as \(|x-c|<\delta\) for some \(\delta>0\).

- Source theorem/lemma: `relative_extremum_def`
- Source proof id: `atlas.real_analysis.d4ac68a30456`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/MVT.lean`

## 37. Resolve the only mismatch between the filter formulation and the desired statement by swapping the order of the assumptions \(x\in S\) and \(|x-c|<\delta\).

- Source theorem/lemma: `relative_extremum_def`
- Source proof id: `atlas.real_analysis.d4ac68a30456`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/MVT.lean`

## 38. Instantiate the general equivalence with \(q(x)\equiv f(x)\le f(c)\) and \(q(x)\equiv f(c)\le f(x)\) to obtain the relative maximum and minimum characterizations simultaneously.

- Source theorem/lemma: `relative_extremum_def`
- Source proof id: `atlas.real_analysis.d4ac68a30456`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/MVT.lean`

## 39. Split the disjunctive extremum hypothesis into the two cases that \(f\) has either a local maximum or a local minimum at \(c\).

- Source theorem/lemma: `fermats_theorem`
- Source proof id: `atlas.real_analysis.ee251a7c0ecb`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/MVT.lean`

## 40. In each case, apply the corresponding library theorem `IsLocalMax.deriv_eq_zero` or `IsLocalMin.deriv_eq_zero`, which directly yields `deriv f c = 0` (so the explicit differentiability hypothesis is not needed in the Lean proof).

- Source theorem/lemma: `fermats_theorem`
- Source proof id: `atlas.real_analysis.ee251a7c0ecb`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/MVT.lean`

## 41. Apply the existing theorem `exists_deriv_eq_zero` directly to `hab`, `hfc`, and `heq`, which already yields a point `c ∈ (a, b)` with `deriv f c = 0`, making the explicit differentiability hypothesis unnecessary.

- Source theorem/lemma: `rolle`
- Source proof id: `atlas.real_analysis.8d98dc2e7b63`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/MVT.lean`

## 42. Convert pointwise differentiability on \((a,b)\) into `DifferentiableOn` by observing that differentiability at a point implies differentiability within the interval.

- Source theorem/lemma: `mean_value_theorem`
- Source proof id: `atlas.real_analysis.27206fc373ae`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/MVT.lean`

## 43. Apply the slope form of the Mean Value Theorem to obtain \(c\in(a,b)\) satisfying \(\operatorname{deriv} f(c)=\frac{f(b)-f(a)}{b-a}\).

- Source theorem/lemma: `mean_value_theorem`
- Source proof id: `atlas.real_analysis.27206fc373ae`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/MVT.lean`

## 44. Use \(a<b\) to prove \(b-a\neq 0\), allowing cancellation of the denominator and rearrangement into \(f(b)-f(a)=\operatorname{deriv} f(c)(b-a)\).

- Source theorem/lemma: `mean_value_theorem`
- Source proof id: `atlas.real_analysis.27206fc373ae`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/MVT.lean`

## 45. Restrict differentiability to the interior of the convex set while retaining continuity on the whole set, exactly matching the hypotheses of the derivative-based monotonicity criteria.

- Source theorem/lemma: `zero_deriv_imp_constant`
- Source proof id: `atlas.real_analysis.d10748554758`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/MVT.lean`

## 46. Use the zero-derivative hypothesis twice—both as \(0 \le \operatorname{deriv} f\) and as \(\operatorname{deriv} f \le 0\)—to prove that \(f\) is simultaneously nondecreasing and nonincreasing on \(I\).

- Source theorem/lemma: `zero_deriv_imp_constant`
- Source proof id: `atlas.real_analysis.d10748554758`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/MVT.lean`

## 47. Compare any \(x,y\in I\) using the total order on \(\mathbb{R}\), then combine the opposing monotonicity inequalities by antisymmetry to conclude \(f(x)=f(y)\).

- Source theorem/lemma: `zero_deriv_imp_constant`
- Source proof id: `atlas.real_analysis.d10748554758`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/MVT.lean`

## 48. Identify `interior (Set.Icc a b)` with `Set.Ioo a b`, so the pointwise differentiability hypothesis yields `DifferentiableOn ℝ f` on the interval’s interior.

- Source theorem/lemma: `monotonicity_and_derivatives`
- Source proof id: `atlas.real_analysis.ea64a8de8ee8`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/MVT.lean`

## 49. To derive a nonnegative derivative from monotonicity, approach each interior point from the right and choose sufficiently small `t > 0` so that `x + t ∈ [a,b]`, making the difference quotient `t⁻¹ (f (x+t) - f x)` nonnegative.

- Source theorem/lemma: `monotonicity_and_derivatives`
- Source proof id: `atlas.real_analysis.ea64a8de8ee8`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/MVT.lean`

## 50. Use convergence of the right-hand difference quotients to `deriv f x` and preservation of inequalities under limits to conclude `0 ≤ deriv f x`.

- Source theorem/lemma: `monotonicity_and_derivatives`
- Source proof id: `atlas.real_analysis.ea64a8de8ee8`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/MVT.lean`

## 51. For the converse, apply the derivative monotonicity theorem `monotoneOn_of_deriv_nonneg`, using convexity of `[a,b]`, continuity on the closed interval, and differentiability on its interior.

- Source theorem/lemma: `monotonicity_and_derivatives`
- Source proof id: `atlas.real_analysis.ea64a8de8ee8`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/MVT.lean`

## 52. Repeat the same right-difference-quotient argument for antitonicity, where `f (x+t) ≤ f x` makes every quotient nonpositive, and use `antitoneOn_of_deriv_nonpos` for the converse.

- Source theorem/lemma: `monotonicity_and_derivatives`
- Source proof id: `atlas.real_analysis.ea64a8de8ee8`
- Source strategy number in proof: 5
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/MVT.lean`

## 53. Apply the previously established Lagrange mean-remainder theorem to obtain an intermediate point \(c\in(x₀,x)\) together with the Taylor remainder identity.

- Source theorem/lemma: `taylor_theorem`
- Source proof id: `atlas.real_analysis.8c1166f65e44`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Taylor.lean`

## 54. Unfold the Taylor polynomial in that identity using `taylor_within_apply`, exposing the finite sum in terms of iterated derivatives within \([x₀,x]\).

- Source theorem/lemma: `taylor_theorem`
- Source proof id: `atlas.real_analysis.8c1166f65e44`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Taylor.lean`

## 55. Rewrite each scalar-multiplication summand into the target form \(\frac{f^{(k)}(x₀)}{k!}(x-x₀)^k\) using real scalar multiplication and elementary ring identities.

- Source theorem/lemma: `taylor_theorem`
- Source proof id: `atlas.real_analysis.8c1166f65e44`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Taylor.lean`

## 56. Rearrange the remainder coefficient so division by \((n+1)!\) applies to the derivative before multiplication by \((x-x₀)^{n+1}\), then conclude from the original remainder identity.

- Source theorem/lemma: `taylor_theorem`
- Source proof id: `atlas.real_analysis.8c1166f65e44`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Taylor.lean`

## 57. Rewrite the positive second derivative hypothesis as `deriv (deriv f) x₀ > 0`, and combine it with `deriv f x₀ = 0` to show that near `x₀` the sign of `deriv f x` equals the sign of `x - x₀`.

- Source theorem/lemma: `second_derivative_test_min`
- Source proof id: `atlas.real_analysis.854142c00e14`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Taylor.lean`

## 58. Use twice continuous differentiability to obtain a neighborhood on which `f` is differentiable, then intersect its radius with the radius where the derivative-sign relation holds.

- Source theorem/lemma: `second_derivative_test_min`
- Source proof id: `atlas.real_analysis.854142c00e14`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Taylor.lean`

## 59. Observe that every point of the interval joining `x₀` to a point inside this common ball also remains inside the ball, so both differentiability and the derivative-sign information apply throughout that interval.

- Source theorem/lemma: `second_derivative_test_min`
- Source proof id: `atlas.real_analysis.854142c00e14`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Taylor.lean`

## 60. For a point `y < x₀`, the derivative is negative on the interior of `[y, x₀]`, making `f` strictly decreasing there and hence giving `f x₀ < f y`.

- Source theorem/lemma: `second_derivative_test_min`
- Source proof id: `atlas.real_analysis.854142c00e14`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Taylor.lean`

## 61. For a point `y > x₀`, the derivative is positive on the interior of `[x₀, y]`, making `f` strictly increasing there and hence again giving `f x₀ < f y`.

- Source theorem/lemma: `second_derivative_test_min`
- Source proof id: `atlas.real_analysis.854142c00e14`
- Source strategy number in proof: 5
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Taylor.lean`

## 62. Combining the two sides proves that every sufficiently close point distinct from `x₀` has strictly larger function value, which is exactly `IsStrictLocalMin f x₀`.

- Source theorem/lemma: `second_derivative_test_min`
- Source proof id: `atlas.real_analysis.854142c00e14`
- Source strategy number in proof: 6
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Taylor.lean`

## 63. Group \(b+c\) as a single term and apply the two-term reverse triangle inequality to obtain \(|a|-|b+c|\le |a+(b+c)|\).

- Source theorem/lemma: `reverse_triangle_three`
- Source proof id: `atlas.real_analysis.7adb6045ae9e`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Weierstrass.lean`

## 64. Use the ordinary triangle inequality \(|b+c|\le |b|+|c|\), which implies \(|a|-|b|-|c|\le |a|-|b+c|\).

- Source theorem/lemma: `reverse_triangle_three`
- Source proof id: `atlas.real_analysis.7adb6045ae9e`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Weierstrass.lean`

## 65. Chain these inequalities and rewrite \(a+(b+c)=a+b+c\) by associativity to reach \(|a|-|b|-|c|\le |a+b+c|\).

- Source theorem/lemma: `reverse_triangle_three`
- Source proof id: `atlas.real_analysis.7adb6045ae9e`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Weierstrass.lean`

## 66. The 1-Lipschitz assertion is obtained directly from the standard estimate \(\lvert \cos x-\cos y\rvert\le \lvert x-y\rvert\).

- Source theorem/lemma: `weierstrass_theorem_I`
- Source proof id: `atlas.real_analysis.48866535c0ff`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Weierstrass.lean`

## 67. Choose \(y_1=c+\frac{3\pi}{2K}\) and \(y_2=c+\frac{5\pi}{2K}\), whose phase shifts make \(\cos(Ky_1)=\sin(Kc)\) and \(\cos(Ky_2)=-\sin(Kc)\).

- Source theorem/lemma: `weierstrass_theorem_I`
- Source proof id: `atlas.real_analysis.48866535c0ff`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Weierstrass.lean`

## 68. Positivity of \(K\) and \(\pi\) shows that both \(y_1\) and \(y_2\) lie strictly inside \(\left(c+\frac{\pi}{K},\,c+\frac{3\pi}{K}\right)\).

- Source theorem/lemma: `weierstrass_theorem_I`
- Source proof id: `atlas.real_analysis.48866535c0ff`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Weierstrass.lean`

## 69. At least one candidate works because \((\cos t-\sin t)^2+(\cos t+\sin t)^2=2\), so \(\lvert\cos t-\sin t\rvert\) and \(\lvert\cos t+\sin t\rvert\) cannot both be less than \(1\).

- Source theorem/lemma: `weierstrass_theorem_I`
- Source proof id: `atlas.real_analysis.48866535c0ff`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Weierstrass.lean`

## 70. Uniformly dominate every summand using \(\left|\cos(160^k x)/4^k\right|\le (1/4)^k\), relying on \(|\cos t|\le 1\) and \(4^k>0\).

- Source theorem/lemma: `weierstrass_theorem_III`
- Source proof id: `atlas.real_analysis.154d27ad6b0e`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Weierstrass.lean`

## 71. Use convergence of the geometric series \(\sum_k(1/4)^k\) to obtain absolute convergence for every \(x\) by comparison.

- Source theorem/lemma: `weierstrass_theorem_III`
- Source proof id: `atlas.real_analysis.154d27ad6b0e`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Weierstrass.lean`

## 72. Apply the Weierstrass \(M\)-test to the continuous summands, using the same \(x\)-independent geometric bound, to deduce continuity of the infinite sum.

- Source theorem/lemma: `weierstrass_theorem_III`
- Source proof id: `atlas.real_analysis.154d27ad6b0e`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Weierstrass.lean`

## 73. Combine the infinite-series triangle inequality with the geometric-series sum \(\sum_k(1/4)^k=4/3\) to obtain the global bound \(|\operatorname{weierstrass\_fun}(x)|\le 4/3\).

- Source theorem/lemma: `weierstrass_theorem_III`
- Source proof id: `atlas.real_analysis.154d27ad6b0e`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Weierstrass.lean`

## 74. Bound the oscillatory numerator uniformly using \(\lvert\cos t\rvert \le 1\), obtaining \(\left|\cos(160^k x)/4^k\right| \le 1/4^k\).

- Source theorem/lemma: `weierstrass_summable`
- Source proof id: `atlas.real_analysis.de15dd292228`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Weierstrass.lean`

## 75. Recognize \(1/4^k=(1/4)^k\) and use that the geometric series with ratio \(1/4<1\) is summable.

- Source theorem/lemma: `weierstrass_summable`
- Source proof id: `atlas.real_analysis.de15dd292228`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Weierstrass.lean`

## 76. Apply the norm comparison test to conclude that the original series is absolutely summable.

- Source theorem/lemma: `weierstrass_summable`
- Source proof id: `atlas.real_analysis.de15dd292228`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Weierstrass.lean`

## 77. Choose \(y>c\) within \(3\pi/160^n\) using the oscillation theorem so that the \(n\)-th cosine mode changes by at least \(1\).

- Source theorem/lemma: `weierstrass_slope_lower_bound`
- Source proof id: `atlas.real_analysis.cf338ff3842e`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Weierstrass.lean`

## 78. Rewrite \(W(y)-W(c)\) as the summable series of termwise differences and split it into the modes below \(n\), the dominant \(n\)-th mode, and the tail above \(n\).

- Source theorem/lemma: `weierstrass_slope_lower_bound`
- Source proof id: `atlas.real_analysis.cf338ff3842e`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Weierstrass.lean`

## 79. The oscillation condition makes the \(n\)-th mode contribute at least \(1/4^n\) in absolute value.

- Source theorem/lemma: `weierstrass_slope_lower_bound`
- Source proof id: `atlas.real_analysis.cf338ff3842e`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Weierstrass.lean`

## 80. Bound the lower-frequency modes using the Lipschitz estimate \(|\cos u-\cos v|\le |u-v|\), the proximity of \(y\) to \(c\), and a geometric-series estimate to obtain \(4/(13\cdot4^n)\).

- Source theorem/lemma: `weierstrass_slope_lower_bound`
- Source proof id: `atlas.real_analysis.cf338ff3842e`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Weierstrass.lean`

## 81. Bound the higher-frequency tail using \(|\cos u-\cos v|\le2\) and the geometric decay \(4^{-k}\), yielding \(2/(3\cdot4^n)\).

- Source theorem/lemma: `weierstrass_slope_lower_bound`
- Source proof id: `atlas.real_analysis.cf338ff3842e`
- Source strategy number in proof: 5
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Weierstrass.lean`

## 82. Apply the reverse triangle inequality to retain the positive remainder \(1-4/13-2/3=1/39\), then combine this increment bound with \(y-c<3\pi/160^n\) and \(160^n=40^n4^n\) to obtain the required slope lower bound.

- Source theorem/lemma: `weierstrass_slope_lower_bound`
- Source proof id: `atlas.real_analysis.cf338ff3842e`
- Source strategy number in proof: 6
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Weierstrass.lean`

## 83. Assume differentiability at \(c\), which forces the slope \(x \mapsto \operatorname{slope}(f,c,x)\) to converge to the finite derivative as \(x \to c\) through \(x \ne c\).

- Source theorem/lemma: `weierstrass_nowhere_differentiable`
- Source proof id: `atlas.real_analysis.0bd46e3d6dbf`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Weierstrass.lean`

## 84. Apply `weierstrass_slope_lower_bound` for each \(n\) to choose \(x_n \ne c\) such that \(|x_n-c|<3\pi/160^n\) while the corresponding difference quotient has magnitude at least \(40^n/(117\pi)\).

- Source theorem/lemma: `weierstrass_nowhere_differentiable`
- Source proof id: `atlas.real_analysis.0bd46e3d6dbf`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Weierstrass.lean`

## 85. Since \(3\pi/160^n \to 0\), the chosen points satisfy \(x_n \to c\), and their non-equality to \(c\) allows the punctured slope limit to be composed with this sequence.

- Source theorem/lemma: `weierstrass_nowhere_differentiable`
- Source proof id: `atlas.real_analysis.0bd46e3d6dbf`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Weierstrass.lean`

## 86. Thus the norms of the slopes along \(x_n\) must converge to the finite value \(\lVert\operatorname{deriv} f(c)\rVert\), but their exponentially growing lower bound tends to \(+\infty\), yielding the contradiction.

- Source theorem/lemma: `weierstrass_nowhere_differentiable`
- Source proof id: `atlas.real_analysis.0bd46e3d6dbf`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Derivatives/Weierstrass.lean`

## 87. Rewrite uniform convergence using `Metric.tendstoUniformlyOn_iff`, reducing the goal to an eventual uniform distance bound for every positive \(\varepsilon\).

- Source theorem/lemma: `uniform_convergence_iff`
- Source proof id: `atlas.real_analysis.7a37ac7d42a3`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/FunctionSequences/Basic.lean`

## 88. Use the characterization of eventual truth along `atTop` on \(\mathbb N\): a property holds eventually exactly when it holds for all \(n \ge M\) for some \(M\).

- Source theorem/lemma: `uniform_convergence_iff`
- Source proof id: `atlas.real_analysis.7a37ac7d42a3`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/FunctionSequences/Basic.lean`

## 89. Translate between the metric bound and the desired absolute-value bound via \(\operatorname{dist}(a,b)=|a-b|\), using symmetry of distance or absolute differences to correct the order of \(f_n(x)\) and \(g(x)\).

- Source theorem/lemma: `uniform_convergence_iff`
- Source proof id: `atlas.real_analysis.7a37ac7d42a3`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/FunctionSequences/Basic.lean`

## 90. Convert the absolute-value bound \(|f_j(x)| \le M_j\) into the norm bound \(\|f_j(x)\| \le M_j\) using \(\|r\|=|r|\) for real numbers.

- Source theorem/lemma: `weierstrass_m_test`
- Source proof id: `atlas.real_analysis.22245b9d4d96`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/FunctionSequences/Basic.lean`

## 91. For each fixed \(x\in S\), apply the norm-comparison test with the summable majorant \(M\) to deduce that \(\sum_j f_j(x)\) is summable.

- Source theorem/lemma: `weierstrass_m_test`
- Source proof id: `atlas.real_analysis.22245b9d4d96`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/FunctionSequences/Basic.lean`

## 92. Use the same bound uniformly for every \(x\in S\), together with the summability of \(M\), to apply the uniform-series M-test and obtain uniform convergence of the partial sums to \(x\mapsto\sum'_j f_j(x)\).

- Source theorem/lemma: `weierstrass_m_test`
- Source proof id: `atlas.real_analysis.22245b9d4d96`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/FunctionSequences/Basic.lean`

## 93. The uniform limit \(g\) of the continuous derivatives \(f'_n\) is continuous on \([a,b]\), hence interval integrable on every subinterval \([a,x]\).

- Source theorem/lemma: `uniform_limit_derivative`
- Source proof id: `atlas.real_analysis.432e8639d4c7`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/FunctionSequences/InterchangeLimits.lean`

## 94. The fundamental theorem of calculus converts each derivative identity into the increment formula \(f_n(x)-f_n(a)=\int_a^x f'_n(t)\,dt\).

- Source theorem/lemma: `uniform_limit_derivative`
- Source proof id: `atlas.real_analysis.432e8639d4c7`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/FunctionSequences/InterchangeLimits.lean`

## 95. Uniform convergence \(f'_n\to g\) allows passage of the limit through the integral, using the estimate \(\left\|\int_a^x(f'_n-g)\right\|\le (x-a)\sup_{[a,b]}|f'_n-g|\).

- Source theorem/lemma: `uniform_limit_derivative`
- Source proof id: `atlas.real_analysis.432e8639d4c7`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/FunctionSequences/InterchangeLimits.lean`

## 96. Pointwise convergence of \(f_n(x)\) and \(f_n(a)\), together with uniqueness of limits, yields \(\lim(x)-\lim(a)=\int_a^x g(t)\,dt\) for every \(x\in[a,b]\).

- Source theorem/lemma: `uniform_limit_derivative`
- Source proof id: `atlas.real_analysis.432e8639d4c7`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/FunctionSequences/InterchangeLimits.lean`

## 97. Rewriting \(\lim(u)=\lim(a)+\int_a^u g(t)\,dt\) on \([a,b]\) and applying the fundamental theorem of calculus to the continuous function \(g\) proves that \(\lim\) has within-derivative \(g(x)\) at every \(x\in[a,b]\).

- Source theorem/lemma: `uniform_limit_derivative`
- Source proof id: `atlas.real_analysis.432e8639d4c7`
- Source strategy number in proof: 5
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/FunctionSequences/InterchangeLimits.lean`

## 98. Unfold the Cauchy–Hadamard definition so the desired equality reduces to comparing the limsups of the \(n\)-th-root norm sequences.

- Source theorem/lemma: `radiusOfConvergence_eq_formalRadius`
- Source proof id: `atlas.real_analysis.428609544e94`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/FunctionSequences/PowerSeries.lean`

## 99. Show termwise that the associated formal coefficient has the same norm as \(a_n\), using that it is \(a_n\) times the canonical multilinear multiplication map and that this map has norm \(1\).

- Source theorem/lemma: `radiusOfConvergence_eq_formalRadius`
- Source proof id: `atlas.real_analysis.428609544e94`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/FunctionSequences/PowerSeries.lean`

## 100. Replace the scalar norm sequence by the identical formal-series norm sequence and apply the theorem identifying its limsup with the inverse of the formal radius.

- Source theorem/lemma: `radiusOfConvergence_eq_formalRadius`
- Source proof id: `atlas.real_analysis.428609544e94`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/FunctionSequences/PowerSeries.lean`

## 101. Conclude by using involutivity of inversion in the extended nonnegative reals, which remains valid at \(0\) and \(+\infty\).

- Source theorem/lemma: `radiusOfConvergence_eq_formalRadius`
- Source proof id: `atlas.real_analysis.428609544e94`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/FunctionSequences/PowerSeries.lean`

## 102. Summability implies \(f(n)\to 0\), so with \(\varepsilon=1\) there is an \(N\) such that \(|f(n)|<1\) for every \(n\ge N\).

- Source theorem/lemma: `summable_abs_bounded`
- Source proof id: `atlas.real_analysis.b2be3ed6ab4f`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/FunctionSequences/PowerSeries.lean`

## 103. Choose \(C=\sum_{i<N}|f(i)|+1\), which simultaneously dominates the finitely many initial terms and the uniformly small tail.

- Source theorem/lemma: `summable_abs_bounded`
- Source proof id: `atlas.real_analysis.b2be3ed6ab4f`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/FunctionSequences/PowerSeries.lean`

## 104. Split into \(n\ge N\), where \(|f(n)|<1\le C\), and \(n<N\), where \(|f(n)|\) is a nonnegative summand of the finite sum defining \(C\).

- Source theorem/lemma: `summable_abs_bounded`
- Source proof id: `atlas.real_analysis.b2be3ed6ab4f`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/FunctionSequences/PowerSeries.lean`

## 105. Rewrite `radiusOfConvergence a` as the formal radius of the multilinear series obtained from the scalar coefficients \(a_n\).

- Source theorem/lemma: `le_radiusOfConvergence_of_bound`
- Source proof id: `atlas.real_analysis.9ed4bfbab8c0`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/FunctionSequences/PowerSeries.lean`

## 106. Apply the general comparison theorem `FormalMultilinearSeries.le_radius_of_bound`, which turns a uniform bound on the weighted coefficient norms into the desired lower bound on the radius.

- Source theorem/lemma: `le_radiusOfConvergence_of_bound`
- Source proof id: `atlas.real_analysis.9ed4bfbab8c0`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/FunctionSequences/PowerSeries.lean`

## 107. Reduce the multilinear-series norm condition to the scalar inequality \(|a_n|\,r^n \le C\) by identifying the norm of scalar multiplication by \(a_n\) with \(|a_n|\), exactly matching the hypothesis.

- Source theorem/lemma: `le_radiusOfConvergence_of_bound`
- Source proof id: `atlas.real_analysis.9ed4bfbab8c0`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/FunctionSequences/PowerSeries.lean`

## 108. Rewrite the scalar radius of convergence as the formal radius of the associated formal multilinear series, turning the hypothesis into the form required by the general convergence theorem.

- Source theorem/lemma: `summable_abs_mul_pow_of_lt_radius`
- Source proof id: `atlas.real_analysis.595aa10aa1dd`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/FunctionSequences/PowerSeries.lean`

## 109. Apply `FormalMultilinearSeries.summable_norm_mul_pow` to deduce summability of the norm-weighted terms at every radius strictly inside the formal radius.

- Source theorem/lemma: `summable_abs_mul_pow_of_lt_radius`
- Source proof id: `atlas.real_analysis.595aa10aa1dd`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/FunctionSequences/PowerSeries.lean`

## 110. Compute that the norm of the \(n\)-th multilinear coefficient obtained from \(a_n\) is exactly \(|a_n|\), since the canonical multiplication map has norm \(1\), thereby identifying the general summable series with \(\sum_n |a_n|r^n\).

- Source theorem/lemma: `summable_abs_mul_pow_of_lt_radius`
- Source proof id: `atlas.real_analysis.595aa10aa1dd`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/FunctionSequences/PowerSeries.lean`

## 111. Convert the positive real radius \(r\) to a nonnegative real and use \(r<\operatorname{radiusOfConvergence}(a)\) to obtain summability of the majorant series \(\sum_j |a_j|r^j\).

- Source theorem/lemma: `power_series_uniform_convergence`
- Source proof id: `atlas.real_analysis.aa965d6636bc`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/FunctionSequences/PowerSeries.lean`

## 112. For every \(x\in[x_0-r,x_0+r]\), derive the crucial uniform bound \(|x-x_0|\le r\), hence \(\lVert a_j(x-x_0)^j\rVert\le |a_j|r^j\) for every \(j\).

- Source theorem/lemma: `power_series_uniform_convergence`
- Source proof id: `atlas.real_analysis.aa965d6636bc`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/FunctionSequences/PowerSeries.lean`

## 113. Apply the Weierstrass \(M\)-test (`tendstoUniformlyOn_tsum_nat`) with this summable, \(x\)-independent majorant to conclude uniform convergence of the partial sums to the pointwise infinite sum on the closed interval.

- Source theorem/lemma: `power_series_uniform_convergence`
- Source proof id: `atlas.real_analysis.aa965d6636bc`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/FunctionSequences/PowerSeries.lean`

## 114. Apply polynomial density on \([a,b]\) with error \(1/(n+1)\) and choose a polynomial \(P_n\) for each \(n\), producing a sequence whose sup-norm errors tend to zero.

- Source theorem/lemma: `weierstrass_approximation`
- Source proof id: `atlas.real_analysis.142948376c58`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/FunctionSequences/WeierstrassApprox.lean`

## 115. Convert each sup-norm estimate into the simultaneous pointwise bound \(|P_n(x)-f(x)|\le \|P_n-f\|_\infty\) for every \(x\in[a,b]\).

- Source theorem/lemma: `weierstrass_approximation`
- Source proof id: `atlas.real_analysis.142948376c58`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/FunctionSequences/WeierstrassApprox.lean`

## 116. Given \(\varepsilon>0\), use the Archimedean property to choose \(N>1/\varepsilon\), then use monotonicity of reciprocals to obtain \(1/(n+1)\le 1/(N+1)<\varepsilon\) for all \(n\ge N\), with \(N\) independent of \(x\).

- Source theorem/lemma: `weierstrass_approximation`
- Source proof id: `atlas.real_analysis.142948376c58`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/FunctionSequences/WeierstrassApprox.lean`

## 117. Negating \(0<P.n\) and using that \(P.n\) is a natural number forces \(P.n=0\).

- Source theorem/lemma: `Partition.n_pos_of_lt`
- Source proof id: `atlas.real_analysis.c597391f0971`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/Basic.lean`

## 118. When \(P.n=0\), the index type \(\mathrm{Fin}(P.n+1)\) has only one element, so its first and last indices coincide.

- Source theorem/lemma: `Partition.n_pos_of_lt`
- Source proof id: `atlas.real_analysis.c597391f0971`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/Basic.lean`

## 119. The partition endpoint identities then assign both \(a\) and \(b\) to that same indexed point, yielding \(a=b\), which contradicts \(a<b\).

- Source theorem/lemma: `Partition.n_pos_of_lt`
- Source proof id: `atlas.real_analysis.c597391f0971`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/Basic.lean`

## 120. Use \(a<b\) to show that the partition has at least one subinterval, so its index type is nonempty and the first subinterval can be selected.

- Source theorem/lemma: `Partition.mesh_pos_of_lt`
- Source proof id: `atlas.real_analysis.894a66d13edc`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/Basic.lean`

## 121. Apply the strict ordering of partition points to prove that the first subinterval has positive length, \(0<x_1-x_0\).

- Source theorem/lemma: `Partition.mesh_pos_of_lt`
- Source proof id: `atlas.real_analysis.894a66d13edc`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/Basic.lean`

## 122. Since the mesh is the supremum of all consecutive subinterval lengths, bound it below by the first subinterval’s positive length to conclude \(0<\operatorname{mesh}(P)\).

- Source theorem/lemma: `Partition.mesh_pos_of_lt`
- Source proof id: `atlas.real_analysis.894a66d13edc`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/Basic.lean`

## 123. Unfold `riemannSum` to expose it as a finite sum indexed by `Fin T.n`.

- Source theorem/lemma: `riemannSum_eq_zero_of_n_eq_zero`
- Source proof id: `atlas.real_analysis.da9205c07916`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/Basic.lean`

## 124. Rewrite `T.n` using `h : T.n = 0` to show that the index type `Fin T.n` is empty.

- Source theorem/lemma: `riemannSum_eq_zero_of_n_eq_zero`
- Source proof id: `atlas.real_analysis.da9205c07916`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/Basic.lean`

## 125. Apply `Fintype.sum_empty` to conclude that the sum over this empty index type equals `0`.

- Source theorem/lemma: `riemannSum_eq_zero_of_n_eq_zero`
- Source proof id: `atlas.real_analysis.da9205c07916`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/Basic.lean`

## 126. Extend the continuous function \(f\) from the closed interval \([a,b]\) to a globally continuous function \(g:\mathbb R\to\mathbb R\), allowing the use of the global differentiation theorem for parameterized integrals.

- Source theorem/lemma: `fundamental_theorem_of_calculus`
- Source proof id: `atlas.real_analysis.00c3d0e4b511`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/FTC.lean`

## 127. For the evaluation form, rewrite the unordered interval as \([a,b]\) using \(a\le b\), obtain interval integrability from continuity, and apply the integral-equals-endpoint-difference theorem to the assumed derivative of \(F\).

- Source theorem/lemma: `fundamental_theorem_of_calculus`
- Source proof id: `atlas.real_analysis.00c3d0e4b511`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/FTC.lean`

## 128. Apply the fundamental derivative theorem to \(t\mapsto\int_a^t g(u)\,du\), then replace \(g(x)\) by \(f(x)\) at each \(x\in[a,b]\).

- Source theorem/lemma: `fundamental_theorem_of_calculus`
- Source proof id: `atlas.real_analysis.00c3d0e4b511`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/FTC.lean`

## 129. Show that \(\int_a^t f=\int_a^t g\) for every \(t\in[a,b]\), since the whole integration interval lies in \([a,b]\), and transfer the derivative to the original integral function via equality on the within-domain.

- Source theorem/lemma: `fundamental_theorem_of_calculus`
- Source proof id: `atlas.real_analysis.00c3d0e4b511`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/FTC.lean`

## 130. Split off the degenerate case \(a=b\), where both interval integrals vanish and the boundary terms cancel.

- Source theorem/lemma: `integration_by_parts`
- Source proof id: `atlas.real_analysis.642513f3f600`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/FTC.lean`

## 131. Use the \(C^{1}\) hypotheses to obtain continuity on \([a,b]\) and ordinary differentiability at every interior point.

- Source theorem/lemma: `integration_by_parts`
- Source proof id: `atlas.real_analysis.642513f3f600`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/FTC.lean`

## 132. Prove integrability of the ordinary derivatives by first using continuity of the relative derivatives on \([a,b]\), then transferring integrability via their almost-everywhere agreement on the interior, since endpoint discrepancies are negligible.

- Source theorem/lemma: `integration_by_parts`
- Source proof id: `atlas.real_analysis.642513f3f600`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/FTC.lean`

## 133. Apply the library integration-by-parts theorem with the factors ordered as \(g\) and \(f\), using the established continuity, derivative, and integrability conditions.

- Source theorem/lemma: `integration_by_parts`
- Source proof id: `atlas.real_analysis.642513f3f600`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/FTC.lean`

## 134. Use commutativity of multiplication to rewrite the resulting identity into the exact order of factors required by the goal.

- Source theorem/lemma: `integration_by_parts`
- Source proof id: `atlas.real_analysis.642513f3f600`
- Source strategy number in proof: 5
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/FTC.lean`

## 135. Split off the degenerate case \(a=b\), where both interval integrals vanish, so that the main argument may assume \(a<b\).

- Source theorem/lemma: `change_of_variables`
- Source proof id: `atlas.real_analysis.adcfa67f5b78`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/FTC.lean`

## 136. Use the positivity of \(\operatorname{deriv}\phi\) to obtain nonvanishing derivatives and hence pointwise differentiability of \(\phi\) on \([a,b]\).

- Source theorem/lemma: `change_of_variables`
- Source proof id: `atlas.real_analysis.adcfa67f5b78`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/FTC.lean`

## 137. Convert the \(C^1\) continuity of the relative derivative into continuity of the ordinary derivative on \([a,b]\), using the unique-differentiability property of a nondegenerate closed interval.

- Source theorem/lemma: `change_of_variables`
- Source proof id: `atlas.real_analysis.adcfa67f5b78`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/FTC.lean`

## 138. Apply the positive-derivative criterion to prove that \(\phi\) is strictly increasing on \([a,b]\), and therefore that \(\phi([a,b])\subseteq[\phi(a),\phi(b)]\).

- Source theorem/lemma: `change_of_variables`
- Source proof id: `atlas.real_analysis.adcfa67f5b78`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/FTC.lean`

## 139. Restrict the assumed continuity of \(f\) to the image \(\phi([a,b])\), thereby satisfying the continuity hypothesis of the substitution theorem.

- Source theorem/lemma: `change_of_variables`
- Source proof id: `atlas.real_analysis.adcfa67f5b78`
- Source strategy number in proof: 5
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/FTC.lean`

## 140. Invoke the standard integral composition-with-derivative theorem and reverse its equality to obtain the desired change-of-variables formula.

- Source theorem/lemma: `change_of_variables`
- Source proof id: `atlas.real_analysis.adcfa67f5b78`
- Source strategy number in proof: 6
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/FTC.lean`

## 141. Convert the continuous differentiability of \(f\) on \([-\pi,\pi]\) into absolute continuity and interval integrability of \(f'\), enabling integration by parts.

- Source theorem/lemma: `riemann_lebesgue`
- Source proof id: `atlas.real_analysis.873ed155bc40`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/Fourier.lean`

## 142. For each \(n>0\), choose the scaled antiderivatives \(g_n(x)=-\cos(nx)/n\) for \(\sin(nx)\) and \(g_n(x)=\sin(nx)/n\) for \(\cos(nx)\).

- Source theorem/lemma: `riemann_lebesgue`
- Source proof id: `atlas.real_analysis.873ed155bc40`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/Fourier.lean`

## 143. Use \(|\sin|\le 1\) and \(|\cos|\le 1\) to obtain the crucial uniform estimate \(\|g_n(x)\|\le 1/n\).

- Source theorem/lemma: `riemann_lebesgue`
- Source proof id: `atlas.real_analysis.873ed155bc40`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/Fourier.lean`

## 144. Apply integration by parts to replace each oscillatory integral by endpoint terms and an integral of \(f'(x)g_n(x)\).

- Source theorem/lemma: `riemann_lebesgue`
- Source proof id: `atlas.real_analysis.873ed155bc40`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/Fourier.lean`

## 145. Bound the resulting expression by \(C/n\), where \(C=\lVert f(\pi)\rVert+\lVert f(-\pi)\rVert+\int_{-\pi}^{\pi}\lVert f'(x)\rVert\,dx\); in the cosine case the endpoint terms vanish because \(\sin(\pm n\pi)=0\).

- Source theorem/lemma: `riemann_lebesgue`
- Source proof id: `atlas.real_analysis.873ed155bc40`
- Source strategy number in proof: 5
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/Fourier.lean`

## 146. Since \(C/n\to 0\), squeeze the norms of both integrals to zero and then multiply by the fixed normalization factor \(1/\pi\).

- Source theorem/lemma: `riemann_lebesgue`
- Source proof id: `atlas.real_analysis.873ed155bc40`
- Source strategy number in proof: 6
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/Fourier.lean`

## 147. Use Heine–Cantor: continuity of \(f\) on the compact interval \([a,b]\) implies uniform continuity there.

- Source theorem/lemma: `modulusOfContinuity_tendsto_zero`
- Source proof id: `atlas.real_analysis.ddf4500c6302`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 148. Apply uniform continuity with tolerance \(\varepsilon/2\), so that whenever \(0<\eta<\delta\) and \(|x-y|\le \eta\), one gets \(|f(x)-f(y)|<\varepsilon/2\).

- Source theorem/lemma: `modulusOfContinuity_tendsto_zero`
- Source proof id: `atlas.real_analysis.ddf4500c6302`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 149. Transfer this pointwise bound to the supremum defining \(w_f(\eta)\) by proving every admissible value is at most \(\varepsilon/2\).

- Source theorem/lemma: `modulusOfContinuity_tendsto_zero`
- Source proof id: `atlas.real_analysis.ddf4500c6302`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 150. Use \(x=y=a\), justified by \(a\le b\), to show the defining set is nonempty and contains \(0\), which both legitimizes the supremum estimates and proves \(w_f(\eta)\ge 0\).

- Source theorem/lemma: `modulusOfContinuity_tendsto_zero`
- Source proof id: `atlas.real_analysis.ddf4500c6302`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 151. Conclude \(0\le w_f(\eta)\le\varepsilon/2<\varepsilon\), hence \(|w_f(\eta)|<\varepsilon\) for all sufficiently small positive \(\eta\), exactly establishing the right-hand limit at \(0\).

- Source theorem/lemma: `modulusOfContinuity_tendsto_zero`
- Source proof id: `atlas.real_analysis.ddf4500c6302`
- Source strategy number in proof: 5
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 152. Compactness of \([a,b]\) and continuity of \(f\) provide a uniform constant \(C\) such that \(|f(t)| \le C\) for every \(t \in [a,b]\).

- Source theorem/lemma: `modulusOfContinuity_bddAbove`
- Source proof id: `atlas.real_analysis.8ad5bc02848c`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 153. The triangle inequality gives \(|f(x)-f(y)| \le |f(x)|+|f(y)| \le 2C\), so \(2C\) is a common upper bound for all values in the set.

- Source theorem/lemma: `modulusOfContinuity_bddAbove`
- Source proof id: `atlas.real_analysis.8ad5bc02848c`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 154. The condition \(|x-y|\le\eta\) is irrelevant for boundedness, since the uniform bound applies to every pair \(x,y\in[a,b]\).

- Source theorem/lemma: `modulusOfContinuity_bddAbove`
- Source proof id: `atlas.real_analysis.8ad5bc02848c`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 155. Continuity of \(f\) on the compact interval \([a,b]\) ensures that the set defining the modulus of continuity is bounded above, allowing the supremum bound theorem `le_csSup` to be applied.

- Source theorem/lemma: `le_modulusOfContinuity`
- Source proof id: `atlas.real_analysis.d46bccc7fe78`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 156. The hypotheses \(x,y\in[a,b]\) and \(|x-y|\le\eta\) show that \(|f(x)-f(y)|\) is itself a member of the set whose supremum defines \(\operatorname{modulusOfContinuity}(f,a,b,\eta)\).

- Source theorem/lemma: `le_modulusOfContinuity`
- Source proof id: `atlas.real_analysis.d46bccc7fe78`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 157. Since every element of a bounded-above set is at most its supremum, `le_csSup` immediately yields \(|f(x)-f(y)|\le\operatorname{modulusOfContinuity}(f,a,b,\eta)\).

- Source theorem/lemma: `le_modulusOfContinuity`
- Source proof id: `atlas.real_analysis.d46bccc7fe78`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 158. Use the partition’s ordering property to deduce \(P(\mathrm{castSucc}\,i)\le P(\mathrm{succ}\,i)\) from the canonical index inequality \(\mathrm{castSucc}\,i\le \mathrm{succ}\,i\).

- Source theorem/lemma: `Partition.succ_sub_castSucc_nonneg`
- Source proof id: `atlas.real_analysis.b0db2bedcea6`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 159. Convert this comparison into \(0\le P(\mathrm{succ}\,i)-P(\mathrm{castSucc}\,i)\) using the equivalence \(0\le y-x\iff x\le y\).

- Source theorem/lemma: `Partition.succ_sub_castSucc_nonneg`
- Source proof id: `atlas.real_analysis.b0db2bedcea6`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 160. The existence of \(i : \mathrm{Fin}\,P.n\) forces \(P.n \ne 0\), allowing the degenerate zero branch in the definition of `P.mesh` to be eliminated.

- Source theorem/lemma: `Partition.le_mesh`
- Source proof id: `atlas.real_analysis.b636badc9189`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 161. After unfolding the nondegenerate branch, `P.mesh` is the finite supremum of all subinterval lengths indexed by `Fin P.n`.

- Source theorem/lemma: `Partition.le_mesh`
- Source proof id: `atlas.real_analysis.b636badc9189`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 162. Since \(i\) belongs to the universal finite index set, `Finset.le_sup'` shows that its subinterval length is bounded above by this supremum.

- Source theorem/lemma: `Partition.le_mesh`
- Source proof id: `atlas.real_analysis.b636badc9189`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 163. Extend the finitely indexed partition points to a natural-number sequence \(g\), so the sum can be rewritten in the standard telescoping form \(\sum_{i=0}^{n-1}(g(i+1)-g(i))\).

- Source theorem/lemma: `Partition.sum_sub_eq`
- Source proof id: `atlas.real_analysis.026b397b162b`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 164. Identify the finite-index expressions \(P.\mathrm{points}(i.\mathrm{succ})\) and \(P.\mathrm{points}(i.\mathrm{castSucc})\) with \(g(i+1)\) and \(g(i)\), respectively.

- Source theorem/lemma: `Partition.sum_sub_eq`
- Source proof id: `atlas.real_analysis.026b397b162b`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 165. Apply the telescoping identity \(\sum_{i=0}^{n-1}(g(i+1)-g(i))=g(n)-g(0)\), which cancels all intermediate partition points.

- Source theorem/lemma: `Partition.sum_sub_eq`
- Source proof id: `atlas.real_analysis.026b397b162b`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 166. Use the partition endpoint properties \(P.\mathrm{points}(0)=a\) and \(P.\mathrm{points}(\mathrm{last})=b\) to conclude that the remaining difference is \(b-a\).

- Source theorem/lemma: `Partition.sum_sub_eq`
- Source proof id: `atlas.real_analysis.026b397b162b`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 167. Use the tagged-partition property \(x_i \le \xi_i \le x_{i+1}\) to bound each tag by the endpoints of its own subinterval.

- Source theorem/lemma: `TaggedPartition.tag_mem_Icc`
- Source proof id: `atlas.real_analysis.afa51cb2adbc`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 168. Use monotonicity of the ordered partition points, together with \(0 \le i\) and \(i+1 \le n\), to obtain \(x_0 \le x_i\) and \(x_{i+1} \le x_n\).

- Source theorem/lemma: `TaggedPartition.tag_mem_Icc`
- Source proof id: `atlas.real_analysis.afa51cb2adbc`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 169. Substitute the endpoint identities \(x_0=a\) and \(x_n=b\), then combine the inequalities to conclude \(a \le \xi_i \le b\).

- Source theorem/lemma: `TaggedPartition.tag_mem_Icc`
- Source proof id: `atlas.real_analysis.afa51cb2adbc`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 170. Use the refinement telescoping identity to express each coarse interval length as the sum of the lengths of all fine intervals assigned to it.

- Source theorem/lemma: `riemannSum_eq_fiber`
- Source proof id: `atlas.real_analysis.db176b4da708`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 171. Distribute the constant factor \(f(T.\mathrm{tags}_k)\) across each fiber sum, turning every fine interval in that fiber into a Riemann-sum term with the parent tag.

- Source theorem/lemma: `riemannSum_eq_fiber`
- Source proof id: `atlas.real_analysis.db176b4da708`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 172. Reindex the resulting double sum fiberwise along `href.assign`, since its fibers partition all fine interval indices.

- Source theorem/lemma: `riemannSum_eq_fiber`
- Source proof id: `atlas.real_analysis.db176b4da708`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 173. On each fiber, use the defining equality `href.assign j = k` to replace the coarse index \(k\) by the actual parent index of \(j\).

- Source theorem/lemma: `riemannSum_eq_fiber`
- Source proof id: `atlas.real_analysis.db176b4da708`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 174. Regroup the coarse Riemann sum over the fine intervals using the refinement assignment, so both sums are indexed by the intervals of \(T'\).

- Source theorem/lemma: `riemannSum_sub_le_modulusOfContinuity_mul`
- Source proof id: `atlas.real_analysis.bea0ff585f27`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 175. Rewrite the difference as a sum of pointwise tag-value differences multiplied by fine interval lengths, then apply the triangle inequality and nonnegativity of those lengths.

- Source theorem/lemma: `riemannSum_sub_le_modulusOfContinuity_mul`
- Source proof id: `atlas.real_analysis.bea0ff585f27`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 176. Observe that each fine tag and its assigned coarse tag lie in the same coarse interval, hence their distance is at most that interval’s length and therefore at most the mesh of \(T\).

- Source theorem/lemma: `riemannSum_sub_le_modulusOfContinuity_mul`
- Source proof id: `atlas.real_analysis.bea0ff585f27`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 177. Apply the modulus-of-continuity bound on \([a,b]\) to uniformly control every difference \(\lvert f(\xi_{k(j)})-f(\eta_j)\rvert\) by \(\omega_f(\|T\|)\).

- Source theorem/lemma: `riemannSum_sub_le_modulusOfContinuity_mul`
- Source proof id: `atlas.real_analysis.bea0ff585f27`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 178. Factor out this uniform bound and use the telescoping identity for the fine partition lengths, whose sum is \(b-a\).

- Source theorem/lemma: `riemannSum_sub_le_modulusOfContinuity_mul`
- Source proof id: `atlas.real_analysis.bea0ff585f27`
- Source strategy number in proof: 5
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 179. Insert the Riemann sum over the common tagged refinement \(T''\) to decompose \(S_f(T_1)-S_f(T_2)\) into the two refinement differences \(S_f(T_1)-S_f(T'')\) and \(S_f(T'')-S_f(T_2)\).

- Source theorem/lemma: `riemannSum_sub_le_modulusOfContinuity_add_mul_of_commonRefinement`
- Source proof id: `atlas.real_analysis.8bf505ec59b9`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 180. Apply the triangle inequality, using symmetry of absolute value to rewrite \(\lvert S_f(T'')-S_f(T_2)\rvert\) as \(\lvert S_f(T_2)-S_f(T'')\rvert\).

- Source theorem/lemma: `riemannSum_sub_le_modulusOfContinuity_add_mul_of_commonRefinement`
- Source proof id: `atlas.real_analysis.8bf505ec59b9`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 181. Bound each resulting difference by the previously proved modulus-of-continuity estimate for a tagged refinement, once for \(T_1\preceq T''\) and once for \(T_2\preceq T''\).

- Source theorem/lemma: `riemannSum_sub_le_modulusOfContinuity_add_mul_of_commonRefinement`
- Source proof id: `atlas.real_analysis.8bf505ec59b9`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 182. Add the two bounds and factor out the common interval length \(b-a\) to obtain the desired sum of moduli of continuity.

- Source theorem/lemma: `riemannSum_sub_le_modulusOfContinuity_add_mul_of_commonRefinement`
- Source proof id: `atlas.real_analysis.8bf505ec59b9`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 183. Prove that `assign j = k` exactly when `j` lies between `φ k.castSucc` and `φ k.succ`, using the assignment bounds and strict monotonicity of `φ` to rule out assignments below or above `k`.

- Source theorem/lemma: `telescope_sum_of_embedding`
- Source proof id: `atlas.real_analysis.6d9a30ae0d65`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 184. Replace dependent `Fin` indexing by the total auxiliary function `g : ℕ → ℝ`, so each fine-interval length becomes the ordinary difference `g (j.val + 1) - g j.val`.

- Source theorem/lemma: `telescope_sum_of_embedding`
- Source proof id: `atlas.real_analysis.6d9a30ae0d65`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 185. Reindex the filtered sum bijectively via `j ↦ j.val`, identifying its index set with the natural-number interval `Finset.Ico a' b'`.

- Source theorem/lemma: `telescope_sum_of_embedding`
- Source proof id: `atlas.real_analysis.6d9a30ae0d65`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 186. Apply the standard telescoping identity `Finset.sum_Ico_sub` and simplify `g` at the endpoints to obtain `pts (φ k.succ) - pts (φ k.castSucc)`.

- Source theorem/lemma: `telescope_sum_of_embedding`
- Source proof id: `atlas.real_analysis.6d9a30ae0d65`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 187. Form the finite union of the two partitions’ point sets and enumerate it in strictly increasing order, thereby retaining every breakpoint while removing duplicates.

- Source theorem/lemma: `TaggedPartition.exists_commonRefinement`
- Source proof id: `atlas.real_analysis.33393fbd4780`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 188. Prove that the minimum and maximum of this union are respectively \(a\) and \(b\), so the sorted enumeration defines a new partition of exactly \([a,b]\).

- Source theorem/lemma: `TaggedPartition.exists_commonRefinement`
- Source proof id: `atlas.real_analysis.33393fbd4780`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 189. Choose each tag of the common partition to be its subinterval’s left endpoint, which immediately satisfies the required tag-membership condition.

- Source theorem/lemma: `TaggedPartition.exists_commonRefinement`
- Source proof id: `atlas.real_analysis.33393fbd4780`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 190. Embed each original partition’s indices strictly into the sorted union by sending every original point to its unique position in the new enumeration, with the embeddings preserving both endpoints.

- Source theorem/lemma: `TaggedPartition.exists_commonRefinement`
- Source proof id: `atlas.real_analysis.33393fbd4780`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 191. For each new subinterval, assign it to the original subinterval whose left endpoint has the greatest embedded index not exceeding the new subinterval’s left index; maximality forces the new interval to lie before that original interval’s right endpoint.

- Source theorem/lemma: `TaggedPartition.exists_commonRefinement`
- Source proof id: `atlas.real_analysis.33393fbd4780`
- Source strategy number in proof: 5
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 192. Use these index inequalities and monotonicity of the sorted points to prove that every new subinterval is contained in its assigned subinterval of each original partition.

- Source theorem/lemma: `TaggedPartition.exists_commonRefinement`
- Source proof id: `atlas.real_analysis.33393fbd4780`
- Source strategy number in proof: 6
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 193. Apply the telescoping-sum lemma for a strictly monotone embedding to show that the lengths of all new subintervals assigned to an original subinterval sum exactly to that original subinterval’s length.

- Source theorem/lemma: `TaggedPartition.exists_commonRefinement`
- Source proof id: `atlas.real_analysis.33393fbd4780`
- Source strategy number in proof: 7
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 194. Introduce a tagged partition \(T''\) that simultaneously refines \(T_1\) and \(T_2\), whose existence follows from \(a \le b\), so both Riemann sums can be compared through one common subdivision.

- Source theorem/lemma: `riemannSum_sub_le_modulusOfContinuity_add_mul`
- Source proof id: `atlas.real_analysis.051c1452e321`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 195. Apply the previously proved common-refinement estimate, which uses continuity to bound the two comparison errors by the respective moduli of continuity times the total interval length \(b-a\).

- Source theorem/lemma: `riemannSum_sub_le_modulusOfContinuity_add_mul`
- Source proof id: `atlas.real_analysis.051c1452e321`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 196. Rewrite the Cauchy criterion in ε–\(N\) form and use continuity on the compact interval to obtain that the modulus of continuity tends to \(0\) as its positive argument tends to \(0\).

- Source theorem/lemma: `riemannSum_cauchySeq_of_mesh_tendsto`
- Source proof id: `atlas.real_analysis.d1f34bb9cb26`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 197. Choose \(\delta>0\) so that every \(0<t<\delta\) satisfies \(\lvert\operatorname{modulusOfContinuity}(f,a,b,t)\rvert<\varepsilon/(2(b-a))\), using \(a<b\) to ensure the denominator is positive.

- Source theorem/lemma: `riemannSum_cauchySeq_of_mesh_tendsto`
- Source proof id: `atlas.real_analysis.d1f34bb9cb26`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 198. Use convergence of the partition meshes to \(0\) to find one index \(N\) after which both meshes are smaller than \(\delta\), while mesh positivity allows the modulus estimate to apply.

- Source theorem/lemma: `riemannSum_cauchySeq_of_mesh_tendsto`
- Source proof id: `atlas.real_analysis.d1f34bb9cb26`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 199. Bound the difference of any two later Riemann sums by the sum of their two modulus-of-continuity errors multiplied by the interval length \(b-a\).

- Source theorem/lemma: `riemannSum_cauchySeq_of_mesh_tendsto`
- Source proof id: `atlas.real_analysis.d1f34bb9cb26`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 200. Apply the chosen modulus bounds to both error terms and simplify \(2\cdot\varepsilon/(2(b-a))\cdot(b-a)=\varepsilon\), proving the required Cauchy estimate.

- Source theorem/lemma: `riemannSum_cauchySeq_of_mesh_tendsto`
- Source proof id: `atlas.real_analysis.d1f34bb9cb26`
- Source strategy number in proof: 5
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 201. Use continuity on the compact interval \([a,b]\) to obtain that the modulus of continuity tends to \(0\) as its positive argument tends to \(0\).

- Source theorem/lemma: `riemannSum_sub_tendsto_zero`
- Source proof id: `atlas.real_analysis.3f6cae6ff8ee`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 202. Set \(L=b-a>0\) and choose the modulus threshold \(\varepsilon/(2L)\), which allocates half of the final error to each Riemann sum.

- Source theorem/lemma: `riemannSum_sub_tendsto_zero`
- Source proof id: `atlas.real_analysis.3f6cae6ff8ee`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 203. Use convergence of both meshes to \(0\), together with positivity of meshes when \(a<b\), to ensure that after one common index both meshes lie in the interval \((0,\delta)\).

- Source theorem/lemma: `riemannSum_sub_tendsto_zero`
- Source proof id: `atlas.real_analysis.3f6cae6ff8ee`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 204. Apply the comparison estimate bounding the difference of two Riemann sums by the sum of their modulus-of-continuity errors multiplied by \(L\).

- Source theorem/lemma: `riemannSum_sub_tendsto_zero`
- Source proof id: `atlas.real_analysis.3f6cae6ff8ee`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 205. Bound each modulus term by \(\varepsilon/(2L)\), so the comparison estimate simplifies exactly to a total error less than \(\varepsilon\), proving convergence to \(0\).

- Source theorem/lemma: `riemannSum_sub_tendsto_zero`
- Source proof id: `atlas.real_analysis.3f6cae6ff8ee`
- Source strategy number in proof: 5
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 206. In the degenerate case \(a=b\), strict ordering forces every tagged partition to have no subintervals, so every Riemann sum is \(0\) and hence converges to \(0\).

- Source theorem/lemma: `riemann_integral_convergence`
- Source proof id: `atlas.real_analysis.2302d57b832e`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 207. When \(a<b\), any sequence of tagged partitions whose mesh tends to \(0\) has Cauchy Riemann sums, which converge to some real limit by completeness of \(\mathbb R\).

- Source theorem/lemma: `riemann_integral_convergence`
- Source proof id: `atlas.real_analysis.2302d57b832e`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 208. The limits arising from any two such partition sequences are equal because the difference of their Riemann sums tends both to \(0\) and to the difference of the two limits.

- Source theorem/lemma: `riemann_integral_convergence`
- Source proof id: `atlas.real_analysis.2302d57b832e`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 209. Choosing one admissible partition sequence therefore supplies a common limit for all admissible sequences, while if no admissible sequence exists the universal convergence assertion holds vacuously.

- Source theorem/lemma: `riemann_integral_convergence`
- Source proof id: `atlas.real_analysis.2302d57b832e`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/ModulusContinuity.lean`

## 210. Continuity of \(f\) and \(g\) on \([a,b]\), together with \(a\le b\), supplies the interval integrability needed to apply the integral comparison theorem.

- Source theorem/lemma: `integral_comparison_and_triangle`
- Source proof id: `atlas.real_analysis.c0ef6ab1afa2`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/Properties.lean`

## 211. The pointwise inequality \(f(x)\le g(x)\) on \([a,b]\) lifts directly to \(\int_a^b f\le\int_a^b g\) via monotonicity of the interval integral.

- Source theorem/lemma: `integral_comparison_and_triangle`
- Source proof id: `atlas.real_analysis.c0ef6ab1afa2`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/Properties.lean`

## 212. The triangle inequality follows from the standard estimate \(\left\|\int_a^b f\right\|\le\int_a^b\|f(x)\|\,dx\), whose orientation relies on \(a\le b\).

- Source theorem/lemma: `integral_comparison_and_triangle`
- Source proof id: `atlas.real_analysis.c0ef6ab1afa2`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/Properties.lean`

## 213. Since the norm on \(\mathbb{R}\) equals absolute value, rewriting \(\|r\|=|r|\) converts the norm estimate exactly into the desired real-valued inequality.

- Source theorem/lemma: `integral_comparison_and_triangle`
- Source proof id: `atlas.real_analysis.c0ef6ab1afa2`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/Properties.lean`

## 214. Continuity on the compact interval \([a,b]\) makes \(f\) interval-integrable and its image \(f([a,b])\) compact, hence bounded above and below.

- Source theorem/lemma: `integral_bounds`
- Source proof id: `atlas.real_analysis.99f216a3381c`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/Properties.lean`

## 215. Boundedness of the image allows the infimum and supremum properties to give \(sInf(f([a,b])) \le f(x) \le sSup(f([a,b]))\) for every \(x \in [a,b]\).

- Source theorem/lemma: `integral_bounds`
- Source proof id: `atlas.real_analysis.99f216a3381c`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/Properties.lean`

## 216. Since \(a \le b\), monotonicity of the interval integral transfers these pointwise bounds to inequalities between the integrals of \(f\) and the corresponding constant functions.

- Source theorem/lemma: `integral_bounds`
- Source proof id: `atlas.real_analysis.99f216a3381c`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/Properties.lean`

## 217. Evaluating each constant integral as \(c(b-a)\) converts those integral comparisons into the desired lower and upper bounds.

- Source theorem/lemma: `integral_bounds`
- Source proof id: `atlas.real_analysis.99f216a3381c`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/Properties.lean`

## 218. Use \(a<c<b\) to obtain \(a\le c\le b\), ensuring that \([a,c]\) and \([c,b]\) are contained in \([a,b]\).

- Source theorem/lemma: `integral_additivity`
- Source proof id: `atlas.real_analysis.cf7ce31aca28`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/Properties.lean`

## 219. Restrict the continuity of \(f\) on \([a,b]\) to continuity on each adjacent subinterval \([a,c]\) and \([c,b]\).

- Source theorem/lemma: `integral_additivity`
- Source proof id: `atlas.real_analysis.cf7ce31aca28`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/Properties.lean`

## 220. Convert continuity on each closed subinterval into interval integrability, which supplies the hypotheses needed for integral additivity.

- Source theorem/lemma: `integral_additivity`
- Source proof id: `atlas.real_analysis.cf7ce31aca28`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/Properties.lean`

## 221. Apply the adjacent-interval additivity theorem and reverse its equality to match the desired orientation.

- Source theorem/lemma: `integral_additivity`
- Source proof id: `atlas.real_analysis.cf7ce31aca28`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/Properties.lean`

## 222. Continuity of \(f\) and \(g\) on \([a,b]\), together with \(a\le b\), is converted into interval integrability for both functions.

- Source theorem/lemma: `integral_linearity`
- Source proof id: `atlas.real_analysis.bac56be2b008`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/Properties.lean`

## 223. Interval integrability is preserved under multiplication by the constant \(\alpha\), so \(x\mapsto \alpha f(x)\) is interval integrable.

- Source theorem/lemma: `integral_linearity`
- Source proof id: `atlas.real_analysis.bac56be2b008`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/Properties.lean`

## 224. Additivity of the interval integral splits the integral of \(\alpha f+g\), and the constant-multiple rule then pulls \(\alpha\) outside the integral to obtain the desired identity.

- Source theorem/lemma: `integral_linearity`
- Source proof id: `atlas.real_analysis.bac56be2b008`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Integration/Properties.lean`

## 225. Recognize that the goal is exactly the standard absolute-value triangle inequality already provided in Lean as `abs_add_le`.

- Source theorem/lemma: `triangle_inequality`
- Source proof id: `atlas.real_analysis.fa564bc5f335`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/RealNumbers/AbsoluteValue.lean`

## 226. Apply `abs_add_le` directly to the real numbers `x` and `y`, yielding `|x + y| ≤ |x| + |y|` with no further argument.

- Source theorem/lemma: `triangle_inequality`
- Source proof id: `atlas.real_analysis.fa564bc5f335`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/RealNumbers/AbsoluteValue.lean`

## 227. The standard algebraic and order structures on \(\mathbb{R}\) supply the strict ordered ring property via the existing typeclass instance.

- Source theorem/lemma: `real_numbers_theorem`
- Source proof id: `atlas.real_analysis.1b9f1b5bf00f`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/RealNumbers/Basic.lean`

## 228. The canonical cast \(\mathbb{Q}\to\mathbb{R}\) is injective, ensuring that rational numbers embed faithfully into the reals.

- Source theorem/lemma: `real_numbers_theorem`
- Source proof id: `atlas.real_analysis.1b9f1b5bf00f`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/RealNumbers/Basic.lean`

## 229. For any nonempty set \(S\subseteq\mathbb{R}\) bounded above, choosing \(x=\sup S\) and invoking completeness of \(\mathbb{R}\) proves that \(x\) is the least upper bound of \(S\).

- Source theorem/lemma: `real_numbers_theorem`
- Source proof id: `atlas.real_analysis.1b9f1b5bf00f`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/RealNumbers/Basic.lean`

## 230. Conditional completeness forces \(F\) to be Archimedean, since a hypothetical upper bound for the natural numbers would yield a supremum contradicted by translation by \(1\).

- Source theorem/lemma: `real_uniqueness_up_to_iso`
- Source proof id: `atlas.real_analysis.98296013f8c5`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/RealNumbers/Basic.lean`

## 231. Archimedeanness makes the embedded rationals order-dense in both \(F\) and \(\mathbb R\), so every element is uniquely determined by its rational lower cut.

- Source theorem/lemma: `real_uniqueness_up_to_iso`
- Source proof id: `atlas.real_analysis.98296013f8c5`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/RealNumbers/Basic.lean`

## 232. Associate \(x\in F\) with the real number whose rational lower cut is \(\{q\in\mathbb Q:q<x\}\), using conditional completeness to realize this cut and prove that the correspondence preserves order, addition, multiplication, and units.

- Source theorem/lemma: `real_uniqueness_up_to_iso`
- Source proof id: `atlas.real_analysis.98296013f8c5`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/RealNumbers/Basic.lean`

## 233. Construct the reverse correspondence from the same rational cuts in \(F\), and use uniqueness from rational density to show the two maps are inverse, producing an ordered ring isomorphism \(F\simeq_{+,\times,\le}\mathbb R\).

- Source theorem/lemma: `real_uniqueness_up_to_iso`
- Source proof id: `atlas.real_analysis.98296013f8c5`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/RealNumbers/Basic.lean`

## 234. Choose the principal square root \(r=\sqrt2\), whose positivity and identity \((\sqrt2)^2=2\) follow from the standard square-root properties for positive and nonnegative inputs.

- Source theorem/lemma: `sqrt2_exists_unique`
- Source proof id: `atlas.real_analysis.acc655918d16`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/RealNumbers/Basic.lean`

## 235. For uniqueness, use the positivity of any candidate \(y\) to recover it from its square via \(y=\sqrt{y^2}\), then substitute \(y^2=2\) to conclude \(y=\sqrt2\).

- Source theorem/lemma: `sqrt2_exists_unique`
- Source proof id: `atlas.real_analysis.acc655918d16`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/RealNumbers/Basic.lean`

## 236. Unfold `BddAbove` as nonemptiness of `upperBounds E`, and unfold membership in `upperBounds E` as the condition that every \(x \in E\) satisfies \(x \le b\).

- Source theorem/lemma: `bounded_above_below_iff`
- Source proof id: `atlas.real_analysis.2c04040b19d7`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/RealNumbers/OrderedSetsFields.lean`

## 237. Dually, unfold `BddBelow` as nonemptiness of `lowerBounds E`, and unfold membership in `lowerBounds E` as the condition that every \(x \in E\) satisfies \(c \le x\).

- Source theorem/lemma: `bounded_above_below_iff`
- Source proof id: `atlas.real_analysis.2c04040b19d7`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/RealNumbers/OrderedSetsFields.lean`

## 238. After these definitional expansions, `simp` converts each nonemptiness statement into the required existential form, and the two equivalences are paired to prove the conjunction.

- Source theorem/lemma: `bounded_above_below_iff`
- Source proof id: `atlas.real_analysis.2c04040b19d7`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/RealNumbers/OrderedSetsFields.lean`

## 239. Use the strictly ordered ring structure to invoke translation invariance of strict inequalities, yielding \(x+z<y+z\) from \(x<y\).

- Source theorem/lemma: `ordered_field_axioms`
- Source proof id: `atlas.real_analysis.3ea7ba1b0f4b`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/RealNumbers/OrderedSetsFields.lean`

## 240. Use positivity preservation under multiplication in a strictly ordered ring to conclude \(0<xy\) from \(0<x\) and \(0<y\).

- Source theorem/lemma: `ordered_field_axioms`
- Source proof id: `atlas.real_analysis.3ea7ba1b0f4b`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/RealNumbers/OrderedSetsFields.lean`

## 241. Prove the conjunction by supplying these two standard order-compatibility results as its respective components.

- Source theorem/lemma: `ordered_field_axioms`
- Source proof id: `atlas.real_analysis.3ea7ba1b0f4b`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/RealNumbers/OrderedSetsFields.lean`

## 242. Use the `Field F` typeclass to invoke the standard commutativity, associativity, identity, inverse, and distributivity lemmas directly.

- Source theorem/lemma: `field_axioms`
- Source proof id: `atlas.real_analysis.d98ecaeef19d`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/RealNumbers/OrderedSetsFields.lean`

## 243. Satisfy the existential additive axioms with the canonical witnesses \(0\) for the identity and \(-x\) for the inverse, justified by `zero_add` and `add_neg_cancel`.

- Source theorem/lemma: `field_axioms`
- Source proof id: `atlas.real_analysis.d98ecaeef19d`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/RealNumbers/OrderedSetsFields.lean`

## 244. Satisfy the existential multiplicative axioms with the canonical witnesses \(1\) for the identity and \(x^{-1}\) for the inverse, using the hypothesis \(x \ne 0\) in `mul_inv_cancel₀`.

- Source theorem/lemma: `field_axioms`
- Source proof id: `atlas.real_analysis.d98ecaeef19d`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/RealNumbers/OrderedSetsFields.lean`

## 245. Assemble all nine axioms in the exact nested-conjunction order of the goal via a single tuple constructed with `refine ⟨\ldots⟩`.

- Source theorem/lemma: `field_axioms`
- Source proof id: `atlas.real_analysis.d98ecaeef19d`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/RealNumbers/OrderedSetsFields.lean`

## 246. Translate countability of \((0,1]\) into the cardinal inequality \(\lvert(0,1]\rvert \le \aleph_0\), so uncountability becomes the strict reverse inequality.

- Source theorem/lemma: `Ioc_zero_one_uncountable`
- Source proof id: `atlas.real_analysis.e8c8f6ce6b7f`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/RealNumbers/Uncountability.lean`

## 247. Use \(0<1\) and the fact that every nondegenerate real interval has cardinality continuum to identify \(\lvert(0,1]\rvert=\mathfrak c\).

- Source theorem/lemma: `Ioc_zero_one_uncountable`
- Source proof id: `atlas.real_analysis.e8c8f6ce6b7f`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/RealNumbers/Uncountability.lean`

## 248. Apply Cantor’s theorem \(\aleph_0<\mathfrak c\) to rule out \(\lvert(0,1]\rvert\le\aleph_0\).

- Source theorem/lemma: `Ioc_zero_one_uncountable`
- Source proof id: `atlas.real_analysis.e8c8f6ce6b7f`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/RealNumbers/Uncountability.lean`

## 249. Cantor’s diagonal argument shows that the power set \(\mathcal P(\mathbb N)\) is uncountable because every proposed enumeration omits a diagonally constructed subset.

- Source theorem/lemma: `real_uncountable`
- Source proof id: `atlas.real_analysis.79478ee913cd`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/RealNumbers/Uncountability.lean`

## 250. An injection from \(\mathcal P(\mathbb N)\) into \(\mathbb R\), such as encoding subsets by ternary expansions using only \(0\) and \(2\), transfers this uncountability to the real numbers.

- Source theorem/lemma: `real_uncountable`
- Source proof id: `atlas.real_analysis.79478ee913cd`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/RealNumbers/Uncountability.lean`

## 251. The Lean proof invokes `Cardinal.not_countable_real`, a packaged cardinality result that directly establishes that the universal set of real numbers is not countable.

- Source theorem/lemma: `real_uncountable`
- Source proof id: `atlas.real_analysis.79478ee913cd`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/RealNumbers/Uncountability.lean`

## 252. Rewrite convergence along `Filter.atTop` using `Metric.tendsto_atTop`, which turns the filter statement into the explicit \(\varepsilon\)–\(N\) condition \(\forall \varepsilon>0,\exists M,\forall n\ge M\).

- Source theorem/lemma: `seq_converges_iff`
- Source proof id: `atlas.real_analysis.b994f1398d46`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Sequences/Basic.lean`

## 253. Replace the real-valued metric distance with absolute difference via `Real.dist_eq`, yielding \(d(x_n,L)=|x_n-L|\) and exactly the desired statement.

- Source theorem/lemma: `seq_converges_iff`
- Source proof id: `atlas.real_analysis.b994f1398d46`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Sequences/Basic.lean`

## 254. Recognize that convergence in \(\mathbb{R}\) is order-squeezable: a function bounded between two functions tending to the same limit must tend to that limit.

- Source theorem/lemma: `squeeze_theorem`
- Source proof id: `atlas.real_analysis.8aaf9bffdfc5`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Sequences/Basic.lean`

## 255. Apply `tendsto_of_tendsto_of_tendsto_of_le_of_le` directly with the convergences `ha`, `hb` and pointwise bounds `hab`, `hxb`.

- Source theorem/lemma: `squeeze_theorem`
- Source proof id: `atlas.real_analysis.8aaf9bffdfc5`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Sequences/Basic.lean`

## 256. Rewrite `CauchySeq x` using `Metric.cauchySeq_iff` to expose the explicit ε–index characterization of a Cauchy sequence.

- Source theorem/lemma: `cauchy_seq_iff`
- Source proof id: `atlas.real_analysis.96a9359e4c81`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Sequences/Cauchy.lean`

## 257. Use the real-number identity `Real.dist_eq`, namely `dist a b = |a - b|`, to convert the metric inequality into the textbook absolute-difference inequality and conversely.

- Source theorem/lemma: `cauchy_seq_iff`
- Source proof id: `atlas.real_analysis.96a9359e4c81`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Sequences/Cauchy.lean`

## 258. In each implication, reuse the same threshold index and hypotheses, since only the notation for the distance changes.

- Source theorem/lemma: `cauchy_seq_iff`
- Source proof id: `atlas.real_analysis.96a9359e4c81`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Sequences/Cauchy.lean`

## 259. The forward implication relies on the completeness of \(\mathbb{R}\), which ensures that every Cauchy sequence has a real limit.

- Source theorem/lemma: `cauchy_iff_convergent`
- Source proof id: `atlas.real_analysis.0b0070d60c5c`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Sequences/Cauchy.lean`

## 260. The reverse implication uses the general principle that every convergent sequence is Cauchy, obtained by comparing two late terms through their common limit via the triangle inequality.

- Source theorem/lemma: `cauchy_iff_convergent`
- Source proof id: `atlas.real_analysis.0b0070d60c5c`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Sequences/Cauchy.lean`

## 261. Convert the global upper and lower bounds on `Set.range x` into the filter-theoretic boundedness and coboundedness hypotheses required by the `limsup` comparison lemmas.

- Source theorem/lemma: `limsup_eq_lim_sup_tail`
- Source proof id: `atlas.real_analysis.acf6d7b27bc7`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Sequences/LimSupInf.lean`

## 262. Use the same bounds to show that every tail has a bounded-above supremum and that the sequence of tail suprema is bounded below, ensuring all `ciSup` and `ciInf` inequalities are applicable.

- Source theorem/lemma: `limsup_eq_lim_sup_tail`
- Source proof id: `atlas.real_analysis.acf6d7b27bc7`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Sequences/LimSupInf.lean`

## 263. For each fixed `n`, observe that eventually `m ≥ n`, so `m = (m - n) + n` and hence `x m ≤ ⨆ i, x (i + n)`, proving `limsup x ≤` every tail supremum and therefore their infimum.

- Source theorem/lemma: `limsup_eq_lim_sup_tail`
- Source proof id: `atlas.real_analysis.acf6d7b27bc7`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Sequences/LimSupInf.lean`

## 264. For the reverse inequality, use the characterization that it suffices to show the infimum of tail suprema lies below every eventual upper bound of `x`.

- Source theorem/lemma: `limsup_eq_lim_sup_tail`
- Source proof id: `atlas.real_analysis.acf6d7b27bc7`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Sequences/LimSupInf.lean`

## 265. Given an eventual upper bound `b`, choose a threshold `N`; then every term of the `N`-th tail is at most `b`, so its supremum is at most `b`, while the infimum over all tails is at most that particular tail supremum.

- Source theorem/lemma: `limsup_eq_lim_sup_tail`
- Source proof id: `atlas.real_analysis.acf6d7b27bc7`
- Source strategy number in proof: 5
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Sequences/LimSupInf.lean`

## 266. If \(x_n \to L\), the standard identities `hL.limsup_eq` and `hL.liminf_eq` show that both limsup and liminf equal \(L\), hence they equal each other.

- Source theorem/lemma: `convergent_iff_limsup_eq_liminf`
- Source proof id: `atlas.real_analysis.cc07284d82b7`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Sequences/LimSupInf.lean`

## 267. Global upper and lower bounds on `Set.range x` are converted into the corresponding boundedness conditions along `Filter.atTop`.

- Source theorem/lemma: `convergent_iff_limsup_eq_liminf`
- Source proof id: `atlas.real_analysis.cc07284d82b7`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Sequences/LimSupInf.lean`

## 268. Conversely, after reversing the assumed equality to obtain \(\liminf x=\limsup x\), the criterion `tendsto_of_liminf_eq_limsup` yields convergence to the common value, chosen as `Filter.limsup x Filter.atTop`.

- Source theorem/lemma: `convergent_iff_limsup_eq_liminf`
- Source proof id: `atlas.real_analysis.cc07284d82b7`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Sequences/LimSupInf.lean`

## 269. Monotonicity gives each adjacent inequality by applying it to the basic natural-number relation \(n \le n+1\).

- Source theorem/lemma: `monotone_increasing_iff`
- Source proof id: `atlas.real_analysis.558ee9832c8c`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Sequences/Monotone.lean`

## 270. Conversely, inequalities between successive terms imply full monotonicity because any relation \(m \le n\) can be traversed through finitely many successor steps, chaining the adjacent inequalities by transitivity.

- Source theorem/lemma: `monotone_increasing_iff`
- Source proof id: `atlas.real_analysis.558ee9832c8c`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Sequences/Monotone.lean`

## 271. A convergent real sequence has a bounded range, so convergence immediately implies that the range of \(x\) is bounded below.

- Source theorem/lemma: `monotone_decreasing_convergence`
- Source proof id: `atlas.real_analysis.9125c31f969d`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Sequences/Monotone.lean`

## 272. For an antitone sequence whose range is bounded below, the monotone convergence theorem `tendsto_atTop_ciInf` shows that \(x_n\) converges to \(\inf_n x_n=\bigwedge_n x_n\).

- Source theorem/lemma: `monotone_decreasing_convergence`
- Source proof id: `atlas.real_analysis.9125c31f969d`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Sequences/Monotone.lean`

## 273. Using this explicit infimum limit both supplies the witness for the existential convergence claim and proves the stronger assertion identifying the limit.

- Source theorem/lemma: `monotone_decreasing_convergence`
- Source proof id: `atlas.real_analysis.9125c31f969d`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Sequences/Monotone.lean`

## 274. View \(n\) as a real variable tending to \(+\infty\), so real-variable limit theorems can be transferred to sequences by composition with `tendsto_natCast_atTop_atTop`.

- Source theorem/lemma: `special_sequences`
- Source proof id: `atlas.real_analysis.0c1af56ba22b`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Sequences/SpecialSequences.lean`

## 275. For \(p>0\), apply the standard limit \(x^{-p}\to 0\) as \(x\to+\infty\) to obtain \(n^{-p}\to 0\).

- Source theorem/lemma: `special_sequences`
- Source proof id: `atlas.real_analysis.0c1af56ba22b`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Sequences/SpecialSequences.lean`

## 276. For \(p>0\), combine \(n^{-1}\to 0\) with continuity of \(x\mapsto p^x\), using \(p^0=1\) and \(1/n=n^{-1}\), to prove \(p^{1/n}\to 1\).

- Source theorem/lemma: `special_sequences`
- Source proof id: `atlas.real_analysis.0c1af56ba22b`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Sequences/SpecialSequences.lean`

## 277. Apply the standard real limit \(x^{1/x}\to 1\) as \(x\to+\infty\) and compose it with the natural-number embedding to conclude \(n^{1/n}\to 1\).

- Source theorem/lemma: `special_sequences`
- Source proof id: `atlas.real_analysis.0c1af56ba22b`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Sequences/SpecialSequences.lean`

## 278. Apply `tendsto_subseq_of_bounded` to the bounded range of \(x\), using that every term \(x_n\) belongs to `Set.range x`, to obtain a strictly increasing subsequence converging to some \(a\in\mathbb R\).

- Source theorem/lemma: `bolzano_weierstrass`
- Source proof id: `atlas.real_analysis.c3ff234fb77c`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Sequences/Subsequences.lean`

## 279. Repackage the resulting witnesses \(\varphi\), its strict monotonicity, the limit \(a\), and the convergence proof in exactly the existential form required by the theorem.

- Source theorem/lemma: `bolzano_weierstrass`
- Source proof id: `atlas.real_analysis.c3ff234fb77c`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Sequences/Subsequences.lean`

## 280. Strict monotonicity of \(\varphi:\mathbb N\to\mathbb N\) guarantees that \(\varphi(n)\to\infty\), formalized by `hφ.tendsto_atTop`.

- Source theorem/lemma: `subseq_tendsto`
- Source proof id: `atlas.real_analysis.085ddc47fe28`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Sequences/Subsequences.lean`

## 281. The convergence \(x\to L\) can then be composed with \(\varphi\to\infty\), so `hx.comp hφ.tendsto_atTop` proves \(x\circ\varphi\to L\).

- Source theorem/lemma: `subseq_tendsto`
- Source proof id: `atlas.real_analysis.085ddc47fe28`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Sequences/Subsequences.lean`

## 282. The bijection \(\sigma : \mathbb N \simeq \mathbb N\) allows summability and sums to be transported unchanged via `Equiv.summable_iff` and `Equiv.hasSum_iff`.

- Source theorem/lemma: `abs_convergent_rearrangement`
- Source proof id: `atlas.real_analysis.4e6181963bde`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Series/Basic.lean`

## 283. Applying summability invariance to \(n \mapsto |x_n|\) proves that the rearranged absolute-value series \(n \mapsto |x_{\sigma(n)}|\) is summable.

- Source theorem/lemma: `abs_convergent_rearrangement`
- Source proof id: `atlas.real_analysis.4e6181963bde`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Series/Basic.lean`

## 284. Applying sum invariance to \(x\) proves that the rearranged family \(x \circ \sigma\) still has sum \(s\).

- Source theorem/lemma: `abs_convergent_rearrangement`
- Source proof id: `atlas.real_analysis.4e6181963bde`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Series/Basic.lean`

## 285. Apply `Summable.of_nonneg_of_le` to the pointwise bounds \(0 \le x_n \le y_n\), obtaining `Summable y → Summable x`.

- Source theorem/lemma: `comparison_test`
- Source proof id: `atlas.real_analysis.81befce4dbe1`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Series/ConvergenceTests.lean`

## 286. Derive `¬ Summable x → ¬ Summable y` as the contrapositive: if \(y\) were summable, the first implication would make \(x\) summable, contradicting the hypothesis.

- Source theorem/lemma: `comparison_test`
- Source proof id: `atlas.real_analysis.81befce4dbe1`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Series/ConvergenceTests.lean`

## 287. Since every root term \(|x_n|^{1/n}\) is nonnegative, its limit \(L\) is nonnegative, allowing a geometric ratio \(r\) with \(0\le L<r<1\) when \(L<1\).

- Source theorem/lemma: `root_test`
- Source proof id: `atlas.real_analysis.f074c78bc249`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Series/ConvergenceTests.lean`

## 288. Convergence of the root sequence turns the strict limit bounds into eventual inequalities: \(|x_n|^{1/n}<r\) if \(L<1\), and \(|x_n|^{1/n}>1\) if \(L>1\).

- Source theorem/lemma: `root_test`
- Source proof id: `atlas.real_analysis.f074c78bc249`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Series/ConvergenceTests.lean`

## 289. Restricting to \(n\ge1\) permits raising these inequalities to the \(n\)-th power and using \(\bigl(|x_n|^{1/n}\bigr)^n=|x_n|\).

- Source theorem/lemma: `root_test`
- Source proof id: `atlas.real_analysis.f074c78bc249`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Series/ConvergenceTests.lean`

## 290. In the case \(L<1\), the resulting eventual bound \(|x_n|\le r^n\) proves summability by comparison with the convergent geometric series \(\sum r^n\).

- Source theorem/lemma: `root_test`
- Source proof id: `atlas.real_analysis.f074c78bc249`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Series/ConvergenceTests.lean`

## 291. In the case \(L>1\), the resulting eventual bound \(|x_n|>1\) contradicts the necessary condition \(x_n\to0\) for convergence of \(\sum x_n\), proving divergence.

- Source theorem/lemma: `root_test`
- Source proof id: `atlas.real_analysis.f074c78bc249`
- Source strategy number in proof: 5
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Series/ConvergenceTests.lean`

## 292. Split the theorem into the two cases \(L<1\) and \(L>1\), corresponding to the convergent and divergent forms of the ratio test.

- Source theorem/lemma: `ratio_test`
- Source proof id: `atlas.real_analysis.c86b2578bcc4`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Series/ConvergenceTests.lean`

## 293. For \(L<1\), apply the ratio test to \(a_n=|x_n|\), using \(x_n\neq0\) to establish that \(a_n\) is eventually nonzero.

- Source theorem/lemma: `ratio_test`
- Source proof id: `atlas.real_analysis.c86b2578bcc4`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Series/ConvergenceTests.lean`

## 294. Rewrite real norms as absolute values (and use \(||x_n||=|x_n|\)) so that the ratio limits required by the library lemmas coincide exactly with the given limit hypothesis.

- Source theorem/lemma: `ratio_test`
- Source proof id: `atlas.real_analysis.c86b2578bcc4`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Series/ConvergenceTests.lean`

## 295. Invoke `summable_of_ratio_test_tendsto_lt_one` when \(L<1\) and `not_summable_of_ratio_test_tendsto_gt_one` when \(L>1\) to conclude absolute convergence and divergence, respectively.

- Source theorem/lemma: `ratio_test`
- Source proof id: `atlas.real_analysis.c86b2578bcc4`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Series/ConvergenceTests.lean`

## 296. Recognize that the library theorem `Antitone.tendsto_alternating_series_of_tendsto_zero` directly gives convergence of the alternating partial sums from `hdec` and `hlim`.

- Source theorem/lemma: `alternating_series_test`
- Source proof id: `atlas.real_analysis.66c62cefcfe4`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Series/ConvergenceTests.lean`

## 297. Observe that the explicit nonnegativity hypothesis `hpos` is mathematically redundant here, since an antitone real sequence converging to `0` must already be nonnegative; the proof merely registers it with `have _ := hpos`.

- Source theorem/lemma: `alternating_series_test`
- Source proof id: `atlas.real_analysis.66c62cefcfe4`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Series/ConvergenceTests.lean`

## 298. Rewrite \(\frac{(-1)^i}{i+1}\) as \((-1)^i\frac{1}{i+1}\), exposing the partial sums as an alternating series with coefficients \(a_i=\frac{1}{i+1}\).

- Source theorem/lemma: `alternating_harmonic_converges`
- Source proof id: `atlas.real_analysis.c533a5d899aa`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Series/ConvergenceTests.lean`

## 299. Prove \(a_n=\frac{1}{n+1}\) is antitone by observing that \(a\le b\) implies \(a+1\le b+1\), so positivity of the denominators reverses the inequality under reciprocation.

- Source theorem/lemma: `alternating_harmonic_converges`
- Source proof id: `atlas.real_analysis.c533a5d899aa`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Series/ConvergenceTests.lean`

## 300. Show \(a_n\to 0\) because \(n+1\to+\infty\) and reciprocals of quantities tending to \(+\infty\) tend to zero.

- Source theorem/lemma: `alternating_harmonic_converges`
- Source proof id: `atlas.real_analysis.c533a5d899aa`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Series/ConvergenceTests.lean`

## 301. Apply the alternating series convergence theorem to the antitone coefficient sequence tending to zero, obtaining the existence of a real limit for the partial sums.

- Source theorem/lemma: `alternating_harmonic_converges`
- Source proof id: `atlas.real_analysis.c533a5d899aa`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/Series/ConvergenceTests.lean`

## 302. Recognize the four desired equalities as existing library lemmas: `compl_union`, `compl_inter`, `diff_inter_diff`, and `Set.diff_inter`.

- Source theorem/lemma: `de_morgan_laws`
- Source proof id: `atlas.real_analysis.fb589e7ff9f9`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/SetTheory/Basic.lean`

## 303. Reverse `diff_inter_diff` with `.symm` because the library states the third set-difference identity in the opposite direction.

- Source theorem/lemma: `de_morgan_laws`
- Source proof id: `atlas.real_analysis.fb589e7ff9f9`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/SetTheory/Basic.lean`

## 304. Use the tuple notation `⟨p₁, p₂, p₃, p₄⟩` to assemble the four equality proofs into the nested conjunction.

- Source theorem/lemma: `de_morgan_laws`
- Source proof id: `atlas.real_analysis.fb589e7ff9f9`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/SetTheory/Basic.lean`

## 305. Use the nonemptiness of \(S\) to obtain a witness \(n\in S\), establishing that the predicate \(k\in S\) is satisfiable.

- Source theorem/lemma: `well_ordering_nat`
- Source proof id: `atlas.real_analysis.531882971c9f`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/SetTheory/Basic.lean`

## 306. Apply the natural-number least-witness operator `Nat.find` to obtain the least \(x\) such that \(x\in S\).

- Source theorem/lemma: `well_ordering_nat`
- Source proof id: `atlas.real_analysis.531882971c9f`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/SetTheory/Basic.lean`

## 307. Use `Nat.find_spec` to prove that this least witness \(x\) belongs to \(S\), and `Nat.find_min'` to show that \(x\le y\) for every \(y\in S\).

- Source theorem/lemma: `well_ordering_nat`
- Source proof id: `atlas.real_analysis.531882971c9f`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/SetTheory/Basic.lean`

## 308. Induct on \(n\) using the strengthened statement \(n \ge 1 \to P(n)\), so the induction hypothesis remains applicable despite starting at \(1\) rather than \(0\).

- Source theorem/lemma: `induction_principle`
- Source proof id: `atlas.real_analysis.5a7152753a83`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/SetTheory/Basic.lean`

## 309. Eliminate the \(n=0\) case by contradiction, since the assumption \(n \ge 1\) is impossible there.

- Source theorem/lemma: `induction_principle`
- Source proof id: `atlas.real_analysis.5a7152753a83`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/SetTheory/Basic.lean`

## 310. Split the successor case \(n=k+1\) according to whether \(k=0\), using the base hypothesis when \(n=1\) and otherwise using \(k\ge 1\) to obtain \(P(k)\) from the induction hypothesis and then \(P(k+1)\) from the step hypothesis.

- Source theorem/lemma: `induction_principle`
- Source proof id: `atlas.real_analysis.5a7152753a83`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/SetTheory/Basic.lean`

## 311. Recognize that set inclusion \(A \subseteq B\) is definitionally the statement \(\forall a,\; a \in A \to a \in B\).

- Source theorem/lemma: `set_relations`
- Source proof id: `atlas.real_analysis.8fb5049d0922`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/SetTheory/Basic.lean`

## 312. Use antisymmetry of inclusion to characterize set equality by mutual inclusion: \(A = B \iff A \subseteq B \land B \subseteq A\).

- Source theorem/lemma: `set_relations`
- Source proof id: `atlas.real_analysis.8fb5049d0922`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/SetTheory/Basic.lean`

## 313. Unfold proper subset as inclusion together with strict inequality: \(A \subsetneq B \iff A \subseteq B \land A \ne B\).

- Source theorem/lemma: `set_relations`
- Source proof id: `atlas.real_analysis.8fb5049d0922`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/SetTheory/Basic.lean`

## 314. Use induction on \(n\), reducing the successor case to the hypothesis \(n<2^n\).

- Source theorem/lemma: `n_lt_two_pow_n`
- Source proof id: `atlas.real_analysis.cf5e7b1b2725`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/SetTheory/Cardinality.lean`

## 315. Strengthen the induction hypothesis by adding \(1\), obtaining \(n+1<2^n+1\).

- Source theorem/lemma: `n_lt_two_pow_n`
- Source proof id: `atlas.real_analysis.cf5e7b1b2725`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/SetTheory/Cardinality.lean`

## 316. Use the positivity \(1\le 2^n\) to bound \(2^n+1\le 2^n+2^n\).

- Source theorem/lemma: `n_lt_two_pow_n`
- Source proof id: `atlas.real_analysis.cf5e7b1b2725`
- Source strategy number in proof: 3
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/SetTheory/Cardinality.lean`

## 317. Recognize \(2^n+2^n=2^{n+1}\), which converts the arithmetic bound into the required exponential one.

- Source theorem/lemma: `n_lt_two_pow_n`
- Source proof id: `atlas.real_analysis.cf5e7b1b2725`
- Source strategy number in proof: 4
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/SetTheory/Cardinality.lean`

## 318. Identify the cardinality of the power set \(\operatorname{Set}(\alpha)\) with the cardinal exponent \(2^{|\alpha|}\) via `Cardinal.mk_set`.

- Source theorem/lemma: `cantor_cardinal`
- Source proof id: `atlas.real_analysis.a4598f93a8f7`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/SetTheory/Cardinality.lean`

## 319. Apply Cantor’s cardinal theorem `Cardinal.cantor` to \(|\alpha|\), obtaining \(|\alpha|<2^{|\alpha|}\), and rewrite the right-hand side as \(|\operatorname{Set}(\alpha)|\).

- Source theorem/lemma: `cantor_cardinal`
- Source proof id: `atlas.real_analysis.a4598f93a8f7`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/SetTheory/Cardinality.lean`

## 320. Package each injective function together with its injectivity proof as an embedding, obtaining embeddings \(\alpha \hookrightarrow \beta\) and \(\beta \hookrightarrow \alpha\).

- Source theorem/lemma: `cantor_schroeder_bernstein`
- Source proof id: `atlas.real_analysis.aaa1490bf333`
- Source strategy number in proof: 1
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/SetTheory/Cardinality.lean`

## 321. Apply antisymmetry for embeddings—the Cantor–Schröder–Bernstein principle—to the two mutual embeddings to obtain a nonempty equivalence \(\alpha \simeq \beta\).

- Source theorem/lemma: `cantor_schroeder_bernstein`
- Source proof id: `atlas.real_analysis.aaa1490bf333`
- Source strategy number in proof: 2
- Source file: `external/atlas-lean/Atlas/RealAnalysis/code/SetTheory/Cardinality.lean`
