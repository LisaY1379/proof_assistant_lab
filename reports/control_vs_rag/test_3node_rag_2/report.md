# Control vs Library-RAG Batch Experiment

## Metadata

- **created_at**: `2026-09-25T06:32:39.891381+00:00`
- **input_path**: `data/test/high_dimensional_probability/test_01/data.json`
- **input_count**: `5`
- **conditions**: `['control', 'library_rag']`
- **model**: `gpt-5.6-sol`
- **temperature**: `1.0`
- **reasoning_effort**: `high`
- **max_completion_tokens**: `4000`
- **strategy_graph**: `data/train/general/strategy_hierarchy.json`
- **resumed_at**: `2026-09-25T06:51:59.996781+00:00`

## theorem_6_2_2 — Theorem 6.2.2 (Hanson-Wright inequality)

Dataset: `high_dimensional_probability`

### Input statement

Theorem 6.2.2 (Hanson-Wright inequality). Let A be an n × n matrix. Let X =
(X1 , . . . , Xn ) ∈ Rn be a random vector with independent, mean-zero, subgaussian
coordinates. Then, for every t ≥ 0, we have
                                               h             t2       t i
         P |X T AX − E X T AX| ≥ t ≤ 2 exp − c min
            
                                                                 2
                                                                   ,        ,
                                                          K 4 ∥A∥F K 2 ∥A∥
where K = maxi ∥Xi ∥ψ2 .

Our

### Task

Explain the proof strategy and give a proof plan. Identify the main mathematical methods used.

### Control output

## Proof

All constants \(c,C>0\) below are universal and may change from line to line.

We use two standard consequences of subgaussianity.

1. If \(Y_i\) are independent, mean-zero, and
   \(\|Y_i\|_{\psi_2}\le K\), then
   \[
   \mathbb E\exp\!\left(s\sum_i u_iY_i\right)
   \le \exp\!\left(C s^2K^2\|u\|_2^2\right).
   \tag{1}
   \]

2. Since
   \[
   \|Y_i^2-\mathbb EY_i^2\|_{\psi_1}\le CK^2,
   \]
   the Bernstein MGF bound gives
   \[
   \mathbb E\exp\!\left(
      \lambda\sum_i b_i(Y_i^2-\mathbb EY_i^2)
   \right)
   \le
   \exp\!\left(C\lambda^2K^4\|b\|_2^2\right)
   \tag{2}
   \]
   whenever
   \[
   |\lambda|\le \frac{c}{K^2\|b\|_\infty}.
   \]

We may replace \(A\) by its symmetric part
\[
A_s=\frac{A+A^T}{2},
\]
since \(x^TAx=x^TA_sx\). Moreover,
\[
\|A_s\|\le \|A\|,
\qquad
\|A_s\|_F\le \|A\|_F.
\]
Thus we assume from now on that \(A\) is symmetric.

Write
\[
X^TAX-\mathbb EX^TAX=D+Z,
\]
where
\[
D=\sum_i a_{ii}(X_i^2-\mathbb EX_i^2),
\qquad
Z=\sum_{i\ne j}a_{ij}X_iX_j.
\]
Here we used independence and mean zero to get
\(\mathbb EX_iX_j=0\) for \(i\ne j\).

### 1. The diagonal part

Applying (2) with \(b_i=a_{ii}\), and using
\[
\sum_i a_{ii}^2\le \|A\|_F^2,
\qquad
\max_i|a_{ii}|\le \|A\|,
\]
we obtain
\[
\mathbb Ee^{\lambda D}
\le
\exp\!\left(C\lambda^2K^4\|A\|_F^2\right)
\tag{3}
\]
for
\[
|\lambda|\le \frac{c}{K^2\|A\|}.
\]

### 2. The off-diagonal part

We first decouple \(Z\). Let \(\delta_1,\dots,\delta_n\) be independent Bernoulli random variables with
\(\mathbb P(\delta_i=1)=1/2\), independent of \(X\), and set
\[
\Lambda=\{i:\delta_i=1\}.
\]
Define
\[
Z_\delta=\sum_{i,j}\delta_i(1-\delta_j)a_{ij}X_iX_j
       =\sum_{\substack{i\in\Lambda\\j\notin\Lambda}}a_{ij}X_iX_j.
\]
Because for \(i\ne j\),
\[
\mathbb E_\delta[\delta_i(1-\delta_j)]=\frac14,
\]
we have
\[
Z=4\mathbb E_\delta Z_\delta.
\]
By Jensen's inequality,
\[
\mathbb Ee^{\lambda Z}
\le
\mathbb E_\delta\mathbb E_X e^{4\lambda Z_\delta}.
\tag{4}
\]

Fix \(\Lambda\), and write
\[
B=A_{\Lambda,\Lambda^c},\qquad
x=X_\Lambda,\qquad y=X_{\Lambda^c}.
\]
Then \(Z_\delta=x^TBy\), and \(x,y\) are independent. Conditioning on \(x\) and using (1),
\[
\mathbb E_y e^{4\lambda x^TBy}
\le
\exp\!\left(C\lambda^2K^2\|B^Tx\|_2^2\right).
\tag{5}
\]

Let \(g\) be a standard Gaussian vector in \(\mathbb R^{|\Lambda^c|}\). By the Gaussian identity
\[
\mathbb E_g e^{\langle v,g\rangle}
=e^{\|v\|_2^2/2},
\]
the right-hand side of (5) can be represented, after adjusting constants, as
\[
\mathbb E_g
\exp\!\left(C\lambda K\langle B^Tx,g\rangle\right)
=
\mathbb E_g
\exp\!\left(C\lambda K\langle x,Bg\rangle\right).
\]
Applying (1) to \(x\), conditional on \(g\), gives
\[
\mathbb E_x\mathbb E_y e^{4\lambda x^TBy}
\le
\mathbb E_g
\exp\!\left(C\lambda^2K^4\|Bg\|_2^2\right).
\tag{6}
\]

If \(s_1,\dots,s_r\) are the singular values of \(B\), then
\[
\mathbb E_g e^{u\|Bg\|_2^2}
=
\prod_{k=1}^r(1-2us_k^2)^{-1/2}.
\]
For \(u\|B\|^2\le c\), the inequality
\(-\log(1-v)\le Cv\) gives
\[
\mathbb E_g e^{u\|Bg\|_2^2}
\le
\exp\!\left(Cu\sum_k s_k^2\right)
=
\exp\!\left(Cu\|B\|_F^2\right).
\tag{7}
\]
Using \(u=C\lambda^2K^4\), as well as
\[
\|B\|\le\|A\|,
\qquad
\|B\|_F\le\|A\|_F,
\]
we conclude from (4)–(7) that
\[
\mathbb Ee^{\lambda Z}
\le
\exp\!\left(C\lambda^2K^4\|A\|_F^2\right)
\tag{8}
\]
provided
\[
|\lambda|\le \frac{c}{K^2\|A\|}.
\]

### 3. MGF of the full quadratic form

Although \(D\) and \(Z\) need not be independent, Cauchy–Schwarz, (3), and (8) give
\[
\begin{aligned}
\mathbb E e^{\lambda(D+Z)}
&\le
\bigl(\mathbb Ee^{2\lambda D}\bigr)^{1/2}
\bigl(\mathbb Ee^{2\lambda Z}\bigr)^{1/2} \\
&\le
\exp\!\left(C\lambda^2K^4\|A\|_F^2\right)
\end{aligned}
\tag{9}
\]
whenever
\[
|\lambda|\le \frac{c}{K^2\|A\|}.
\]

Set
\[
Y=X^TAX-\mathbb EX^TAX,\qquad
V=K^4\|A\|_F^2,\qquad
L=\frac{c}{K^2\|A\|}.
\]
For \(0\le\lambda\le L\), Chernoff's inequality and (9) yield
\[
\mathbb P(Y\ge t)
\le
\exp(-\lambda t+C\lambda^2V).
\]
Choosing
\[
\lambda=\min\left\{\frac{t}{2CV},\frac L2\right\}
\]
gives
\[
\mathbb P(Y\ge t)
\le
\exp\!\left[
-c\min\left(
\frac{t^2}{K^4\|A\|_F^2},
\frac{t}{K^2\|A\|}
\right)
\right].
\]
Applying the same argument to \(-Y\) and taking a union bound proves
\[
\boxed{
\mathbb P\!\left(
\left|X^TAX-\mathbb EX^TAX\right|\ge t
\right)
\le
2\exp\!\left[
-c\min\left(
\frac{t^2}{K^4\|A\|_F^2},
\frac{t}{K^2\|A\|}
\right)
\right].
}
\]

This is the Hanson–Wright inequality.

### Library-RAG output

## Proof

All constants \(c,C>0\) below are universal and may change from line to line.

We use two standard consequences of subgaussianity.

1. If \(Y_i\) are independent, mean-zero, and
   \(\|Y_i\|_{\psi_2}\le K\), then
   \[
   \mathbb E\exp\!\left(s\sum_i u_iY_i\right)
   \le \exp\!\left(C s^2K^2\|u\|_2^2\right).
   \tag{1}
   \]

2. Since
   \[
   \|Y_i^2-\mathbb EY_i^2\|_{\psi_1}\le CK^2,
   \]
   the Bernstein MGF bound gives
   \[
   \mathbb E\exp\!\left(
      \lambda\sum_i b_i(Y_i^2-\mathbb EY_i^2)
   \right)
   \le
   \exp\!\left(C\lambda^2K^4\|b\|_2^2\right)
   \tag{2}
   \]
   whenever
   \[
   |\lambda|\le \frac{c}{K^2\|b\|_\infty}.
   \]

We may replace \(A\) by its symmetric part
\[
A_s=\frac{A+A^T}{2},
\]
since \(x^TAx=x^TA_sx\). Moreover,
\[
\|A_s\|\le \|A\|,
\qquad
\|A_s\|_F\le \|A\|_F.
\]
Thus we assume from now on that \(A\) is symmetric.

Write
\[
X^TAX-\mathbb EX^TAX=D+Z,
\]
where
\[
D=\sum_i a_{ii}(X_i^2-\mathbb EX_i^2),
\qquad
Z=\sum_{i\ne j}a_{ij}X_iX_j.
\]
Here we used independence and mean zero to get
\(\mathbb EX_iX_j=0\) for \(i\ne j\).

### 1. The diagonal part

Applying (2) with \(b_i=a_{ii}\), and using
\[
\sum_i a_{ii}^2\le \|A\|_F^2,
\qquad
\max_i|a_{ii}|\le \|A\|,
\]
we obtain
\[
\mathbb Ee^{\lambda D}
\le
\exp\!\left(C\lambda^2K^4\|A\|_F^2\right)
\tag{3}
\]
for
\[
|\lambda|\le \frac{c}{K^2\|A\|}.
\]

### 2. The off-diagonal part

We first decouple \(Z\). Let \(\delta_1,\dots,\delta_n\) be independent Bernoulli random variables with
\(\mathbb P(\delta_i=1)=1/2\), independent of \(X\), and set
\[
\Lambda=\{i:\delta_i=1\}.
\]
Define
\[
Z_\delta=\sum_{i,j}\delta_i(1-\delta_j)a_{ij}X_iX_j
       =\sum_{\substack{i\in\Lambda\\j\notin\Lambda}}a_{ij}X_iX_j.
\]
Because for \(i\ne j\),
\[
\mathbb E_\delta[\delta_i(1-\delta_j)]=\frac14,
\]
we have
\[
Z=4\mathbb E_\delta Z_\delta.
\]
By Jensen's inequality,
\[
\mathbb Ee^{\lambda Z}
\le
\mathbb E_\delta\mathbb E_X e^{4\lambda Z_\delta}.
\tag{4}
\]

Fix \(\Lambda\), and write
\[
B=A_{\Lambda,\Lambda^c},\qquad
x=X_\Lambda,\qquad y=X_{\Lambda^c}.
\]
Then \(Z_\delta=x^TBy\), and \(x,y\) are independent. Conditioning on \(x\) and using (1),
\[
\mathbb E_y e^{4\lambda x^TBy}
\le
\exp\!\left(C\lambda^2K^2\|B^Tx\|_2^2\right).
\tag{5}
\]

Let \(g\) be a standard Gaussian vector in \(\mathbb R^{|\Lambda^c|}\), independent of everything else, and let \(C_0\) denote the constant on the right-hand side of (5). The Gaussian identity
\[
\mathbb E_g e^{\langle v,g\rangle}=e^{\|v\|_2^2/2}
\]
gives the exact linearization
\[
\exp\!\left(C_0\lambda^2K^2\|B^Tx\|_2^2\right)
=
\mathbb E_g\exp\!\left(\sqrt{2C_0}\,\lambda K\langle B^Tx,g\rangle\right)
=
\mathbb E_g\exp\!\left(\sqrt{2C_0}\,\lambda K\langle x,Bg\rangle\right).
\]
Thus, by (5), Tonelli's theorem, and then (1) applied to \(x\) conditional on \(g\),
\[
\begin{aligned}
\mathbb E_x\mathbb E_y e^{4\lambda x^TBy}
&\le \mathbb E_g\mathbb E_x
 \exp\!\left(\sqrt{2C_0}\,\lambda K\langle x,Bg\rangle\right)\\
&\le \mathbb E_g
 \exp\!\left(C\lambda^2K^4\|Bg\|_2^2\right).
\end{aligned}
\tag{6}
\]

If \(s_1,\dots,s_r\) are the singular values of \(B\), then
\[
\mathbb E_g e^{u\|Bg\|_2^2}
=
\prod_{k=1}^r(1-2us_k^2)^{-1/2}.
\]
For \(u\|B\|^2\le c\), the inequality
\(-\log(1-v)\le Cv\) gives
\[
\mathbb E_g e^{u\|Bg\|_2^2}
\le
\exp\!\left(Cu\sum_k s_k^2\right)
=
\exp\!\left(Cu\|B\|_F^2\right).
\tag{7}
\]
Combining (4)–(7) with \(u=C\lambda^2K^4\), \(\|B\|\le\|A\|\), and \(\|B\|_F\le\|A\|_F\),
\[
\mathbb Ee^{\lambda Z}
\le
\exp\!\left(C\lambda^2K^4\|A\|_F^2\right)
\tag{8}
\]
provided
\[
|\lambda|\le \frac{c}{K^2\|A\|}.
\]

### 3. MGF of the full quadratic form

Although \(D\) and \(Z\) need not be independent, Cauchy–Schwarz, (3), and (8) give
\[
\begin{aligned}
\mathbb E e^{\lambda(D+Z)}
&\le
\bigl(\mathbb Ee^{2\lambda D}\bigr)^{1/2}
\bigl(\mathbb Ee^{2\lambda Z}\bigr)^{1/2} \\
&\le
\exp\!\left(C\lambda^2K^4\|A\|_F^2\right)
\end{aligned}
\tag{9}
\]
whenever
\[
|\lambda|\le \frac{c}{K^2\|A\|}.
\]

Set
\[
Y=X^TAX-\mathbb EX^TAX,\qquad
V=K^4\|A\|_F^2,\qquad
L=\frac{c}{K^2\|A\|}.
\]
For \(0\le\lambda\le L\), Chernoff's inequality and (9) yield
\[
\mathbb P(Y\ge t)
\le
\exp(-\lambda t+C\lambda^2V).
\]
Choosing
\[
\lambda=\min\left\{\frac{t}{2CV},\frac L2\right\}
\]
gives
\[
\mathbb P(Y\ge t)
\le
\exp\!\left[
-c\min\left(
\frac{t^2}{K^4\|A\|_F^2},
\frac{t}{K^2\|A\|}
\right)
\right].
\]
Applying the same argument to \(-Y\) and taking a union bound proves
\[
\boxed{
\mathbb P\!\left(
\left|X^TAX-\mathbb EX^TAX\right|\ge t
\right)
\le
2\exp\!\left[
-c\min\left(
\frac{t^2}{K^4\|A\|_F^2},
\frac{t}{K^2\|A\|}
\right)
\right].
}
\]

This is the Hanson–Wright inequality.

### Retrieved strategy nodes

- `family_definitional_reformulation` — **Definitional unfolding and equivalent reformulation**: Convert abstract statements into explicit definitions, quantified conditions, or standard equivalent formulations.
- `sub_definitional_unfolding` — **Definitional unfolding**: Expand boundedness, inclusion, extrema, Riemann sums, and auxiliary constructions into their defining statements.
- `sub_metric_filter_characterization` — **Metric and filter characterizations**: Replace continuity, convergence, Cauchy conditions, and eventual properties by neighborhood, filter, or epsilon-based criteria.
- `sub_canonical_rewriting` — **Canonical rewriting**: Rewrite abstract distances, norms, slopes, interval interiors, and formal-series expressions in concrete canonical forms.
- `sub_set_extensionality` — **Set identities and extensionality**: Prove set equalities by extensionality or mutual inclusion and simplify Boolean set operations.
- `family_normalization_symmetry` — **Normalization, invariance, and symmetry**: Translate, rescale, whiten, permute, or otherwise transform a problem to a canonical case and transfer the conclusion back.
- `family_standard_theorem_reduction` — **Reduction to a standard theorem**: Modify domains and regularity hypotheses so that a known theorem applies directly.
- `sub_regularity_transfer` — **Restriction, extension, and transfer of regularity**: Restrict or extend functions and transfer continuity, differentiability, or integrability between compatible domains.
- `family_logical_reasoning` — **Logical decomposition, cases, and contradiction**: Split logical, order, endpoint, degeneracy, or parameter cases and use contradiction or contraposition to eliminate alternatives.
- `family_explicit_construction` — **Explicit construction and parameter choice**: Construct witnesses, sequences, partitions, comparison points, thresholds, or auxiliary objects and tune free parameters.
- `family_algebra_order_norm` — **Algebraic, order, and norm estimates**: Combine algebraic rearrangement and order reasoning with norm inequalities and duality estimates.
- `sub_elementary_algebra_order` — **Elementary algebra and order reasoning**: Prove positivity or nonvanishing, clear denominators, cancel factors, rearrange identities, and combine inequalities.
- `family_topology_compactness_connectedness` — **Compactness and connectedness methods**: Use compactness for boundedness, extrema, subsequences, and uniform continuity, and connectedness for intermediate values and zeros.
- `sub_compactness` — **Compactness arguments**: Apply compactness of intervals or images to obtain boundedness, attained extrema, uniform continuity, or convergent subsequences.
- `sub_intermediate_value` — **Intermediate Value Theorem**: Use continuity and endpoint value information to produce an intermediate value or interior zero.
- `family_extremal_order` — **Supremum, infimum, and extremal arguments**: Control quantities through suprema, infima, extremal points, or attained optimizers.
- `sub_order_completeness` — **Suprema, infima, and order completeness**: Apply least-upper-bound and greatest-lower-bound properties to bounded sets, images, limsups, and moduli of continuity.
- `family_limits_completeness` — **Limit, sequence, and completeness methods**: Use epsilon or filter formulations, limit laws, squeezing, completeness, subsequences, and limsup-liminf criteria.
- `sub_limit_laws_squeezing` — **Limit laws, squeezing, and uniqueness**: Compose limits, pass bounds to limits, squeeze between convergent quantities, and use uniqueness to identify limits.
- `sub_sequence_completeness` — **Sequence and completeness methods**: Use epsilon-N arguments, Cauchy completeness, subsequences, and sequences approaching a point.
- `sub_monotone_limsup_subsequence` — **Monotone sequences, limsup, and subsequences**: Use monotone convergence, limsup-liminf characterizations, and extraction of convergent subsequences.
- `family_differential_calculus` — **Differential-calculus arguments**: A broad calculus family covering differentiability criteria, derivative rules, mean-value principles, derivative signs, and Taylor expansion.
- `sub_difference_quotient` — **Difference-quotient characterization of differentiability**: Express differentiability as convergence of slopes on a punctured neighborhood.
- `sub_derivative_rules` — **Differential calculus rules**: Apply chain, composition, and related closure rules for differentiable functions.
- `sub_mean_value_theorems` — **Fermat, Rolle, and Mean Value Theorems**: Convert extrema or endpoint equalities into derivative information and represent increments by intermediate derivatives.
- `sub_derivative_sign` — **Derivative-sign arguments**: Infer monotonicity, constancy, or local extrema from first- or second-derivative sign information.
- `sub_taylor_remainder` — **Taylor expansion with remainder**: Apply finite Taylor expansion with a controlled remainder and normalize the resulting coefficients.
- `family_error_decomposition` — **Error decomposition and balancing**: Split a total error into analyzable components and choose parameters that balance the dominant contributions.
- `sub_triangle_error_estimates` — **Triangle-inequality and error-decomposition estimates**: Separate dominant and error terms and control them with triangle and reverse-triangle inequalities.
- `sub_approximation_archimedean` — **Approximation and Archimedean error control**: Choose dense approximants and then select an index making the uniform approximation error smaller than a prescribed tolerance.
- `family_comparison_domination` — **Comparison, domination, and squeezing**: Bound complicated quantities by simpler majorants and transfer those bounds through sums, integrals, limits, and suprema.
- `family_series_convergence` — **Series and uniform-convergence methods**: A broad family covering summability tests, uniform convergence, and power-series convergence radii.
- `sub_series_tests` — **Series comparison and convergence tests**: Use comparison, term, root, ratio, alternating-series, geometric, or rearrangement criteria.
- `sub_uniform_convergence_mtest` — **Uniform convergence and the Weierstrass M-test**: Produce a summable uniform majorant and transfer continuity or bounds to the resulting series.
- `sub_power_series_radius` — **Power-series radius arguments**: Compare coefficient growth and apply Cauchy-Hadamard or radius-of-convergence comparison results.
- `family_integral_calculus` — **Integral-calculus arguments**: A broad integration family covering the fundamental theorem, structural integral identities, transformations, and Riemann-sum methods.
- `sub_fundamental_theorem_calculus` — **Fundamental Theorem of Calculus**: Convert derivatives into integral increments or differentiate parameterized integrals.
- `sub_integral_structure` — **Structural properties of the integral**: Use linearity, interval additivity, monotonicity, constant-integral formulas, and integral norm inequalities.
- `sub_integration_transformations` — **Integration by parts and substitution**: Verify regularity and integrability hypotheses and then apply integration by parts or change of variables.
- `sub_partition_refinement` — **Partition and refinement arguments**: Control meshes and subintervals, construct common refinements, and decompose coarse partitions into fine pieces.
- `sub_riemann_modulus_control` — **Modulus-of-continuity control of Riemann sums**: Control tag changes using a modulus of continuity and sum local errors to prove convergence and partition independence.
- `family_reindexing_telescoping` — **Reindexing and telescoping sums**: Reindex sums under bijections or fibers and cancel consecutive terms so only boundary contributions remain.
- `family_induction_well_ordering` — **Induction, recurrence, and well-ordering**: Use induction, strengthened hypotheses, recurrence, least witnesses, or minimal counterexamples over the natural numbers.
- `family_structural_foundations` — **Cardinality, embeddings, and completion**: Use embeddings and cardinal comparisons or construct complete ordered structures from dense substructures and cuts.
- `sub_ordered_field_constructions` — **Ordered-field structure and canonical constructions**: Use ordered-field operations, canonical witnesses, Archimedeanness, completeness, and rational cuts in structural arguments about the reals.
- `sub_cardinality_embeddings` — **Cardinality and embedding arguments**: Use injections, diagonalization, Cantor's theorem, interval cardinality, and Cantor-Schroeder-Bernstein.
- `family_variational_linear_algebra` — **Variational and linear-algebraic methods**: Optimization and geometric methods based on convexity, orthogonality, projections, spectra, and structured parameter spaces.
- `sub_convexity_variational` — **Convexity and variational arguments**: Use Jensen's inequality, convex combinations, first-order optimality, or comparison with feasible competitors.
- `sub_orthogonality_spectral` — **Orthogonality, projection, and spectral arguments**: Use orthogonal expansions, Pythagoras, Parseval, normal equations, Rayleigh quotients, and eigenvector principles.
- `sub_structured_parameters` — **Sparsity, low-rank structure, and norm duality**: Exploit support, cone, rank, or singular-space decompositions together with dual norms and restricted geometric conditions.
- `family_metric_entropy` — **Metric entropy, covering, and packing methods**: Discretize continuous classes by finite nets or construct well-separated finite subsets using packing methods.
- `sub_covering_volumetric` — **Covering-net and volumetric arguments**: Replace continuous suprema by maxima over finite epsilon-nets and bound net sizes through packing and volume comparison.
- `sub_probabilistic_packing` — **Probabilistic method and packing constructions**: Randomly generate nets, codes, sparse vectors, or approximants and prove that a suitable deterministic construction exists.
- `family_probability_information` — **Probability, concentration, and information methods**: Probabilistic proof methods based on exponential moments, tails, independence, union bounds, and information-theoretic reductions.
- `sub_exponential_concentration` — **Exponential-moment and concentration arguments**: Apply exponential Markov inequalities, control moment-generating functions, and optimize parameters to derive tail bounds.
- `sub_tail_integration` — **Tail integration and moment estimates**: Convert moments into tail integrals, insert probability bounds, and estimate the resulting integrals.
- `sub_independence_tensorization` — **Independence, tensorization, and union bounds**: Factor quantities using independence, tensorize information, and upgrade pointwise bounds to simultaneous bounds by a union bound.
- `sub_testing_information` — **Testing and information-theoretic reductions**: Reduce estimation to hypothesis testing and control testing error using divergence or mutual-information inequalities.

---

## theorem_4_7_1 — Theorem 4.7.1 (Covariance estimation)

Dataset: `high_dimensional_probability`

### Input statement

Theorem 4.7.1 (Covariance estimation). Let X be a subgaussian random vector
in Rn . More specifically, assume that there exists K ≥ 1 such that13
                       ∥⟨X, x⟩∥ψ2 ≤ K∥⟨X, x⟩∥L2           for any x ∈ Rn .                   (4.29)
Then, for every positive integer m, we have
                                          r n   n
                                        2
                      E∥Σm − Σ∥ ≤ CK           +    ∥Σ∥.
                                            m m

### Task

Explain the proof strategy and give a proof plan. Identify the main mathematical methods used.

### Control output

Let \(X_1,\dots,X_m\) be independent copies of \(X\), and write
\[
\Sigma=\mathbb E XX^\top,
\qquad
\Sigma_m=\frac1m\sum_{i=1}^m X_iX_i^\top .
\]

We first prove the isotropic case.

### Isotropic case

Suppose \(Y\in\mathbb R^r\) satisfies
\[
\mathbb E YY^\top=I_r,
\qquad
\|\langle Y,x\rangle\|_{\psi_2}\le K\|x\|_2.
\]
Let \(Y_1,\dots,Y_m\) be independent copies and set
\[
A=\frac1m\sum_{i=1}^mY_iY_i^\top-I_r.
\]

For a fixed \(x\in S^{r-1}\),
\[
x^\top Ax
=\frac1m\sum_{i=1}^m\big(\langle Y_i,x\rangle^2-1\big).
\]
Because \(\|\langle Y_i,x\rangle\|_{\psi_2}\le K\), the variables
\[
Z_i=\langle Y_i,x\rangle^2-1
\]
are centered and subexponential, with
\[
\|Z_i\|_{\psi_1}\le CK^2.
\]
Bernstein’s inequality therefore gives
\[
\mathbb P\{|x^\top Ax|>t\}
\le
2\exp\left[-cm\min\left(\frac{t^2}{K^4},\frac{t}{K^2}\right)\right].
\tag{1}
\]

Let \(\mathcal N\) be a \(1/4\)-net of \(S^{r-1}\) with
\[
|\mathcal N|\le 9^r.
\]
For every symmetric matrix \(A\),
\[
\|A\|\le 2\max_{x\in\mathcal N}|x^\top Ax|.
\]
Thus, by (1) and the union bound,
\[
\mathbb P\{\|A\|>2t\}
\le
2\exp\left[
Cr-cm\min\left(\frac{t^2}{K^4},\frac{t}{K^2}\right)
\right].
\]
Consequently, for every \(u\ge0\), with probability at least \(1-2e^{-u}\),
\[
\|A\|
\le
CK^2\left(
\sqrt{\frac{r+u}{m}}+\frac{r+u}{m}
\right).
\tag{2}
\]
Integrating this tail bound yields
\[
\mathbb E\|A\|
\le
CK^2\left(\sqrt{\frac rm}+\frac rm\right).
\tag{3}
\]

### Reduction to the isotropic case

Let \(S=\operatorname{range}(\Sigma)\) and \(r=\dim S\le n\). If \(v\in\ker(\Sigma)\), then
\[
\mathbb E\langle X,v\rangle^2=v^\top\Sigma v=0,
\]
so \(X\in S\) almost surely.

On \(S\), define
\[
Y=\Sigma^{-1/2}X,
\]
where the inverse is taken only on \(S\). Then
\[
\mathbb E YY^\top=I_S.
\]
Moreover, for every \(y\in S\),
\[
\begin{aligned}
\|\langle Y,y\rangle\|_{\psi_2}
&=\|\langle X,\Sigma^{-1/2}y\rangle\|_{\psi_2}\\
&\le K\|\langle X,\Sigma^{-1/2}y\rangle\|_{L_2}\\
&=K\|y\|_2.
\end{aligned}
\]
Thus \(Y\) satisfies the isotropic assumptions above.

Writing \(Y_i=\Sigma^{-1/2}X_i\), we have
\[
\Sigma_m-\Sigma
=
\Sigma^{1/2}
\left(
\frac1m\sum_{i=1}^mY_iY_i^\top-I_S
\right)
\Sigma^{1/2}.
\]
Hence
\[
\|\Sigma_m-\Sigma\|
\le
\|\Sigma\|
\left\|
\frac1m\sum_{i=1}^mY_iY_i^\top-I_S
\right\|.
\]
Applying (3) and using \(r\le n\), we obtain
\[
\boxed{
\mathbb E\|\Sigma_m-\Sigma\|
\le
CK^2\left(\sqrt{\frac nm}+\frac nm\right)\|\Sigma\|
}.
\]
Here \(C>0\) is an absolute constant.

### Library-RAG output

Let \(X_1,\dots,X_m\) be independent copies of \(X\), and write
\[
\Sigma=\mathbb E XX^\top,
\qquad
\Sigma_m=\frac1m\sum_{i=1}^m X_iX_i^\top .
\]

We first prove the isotropic case.

### Isotropic case

Suppose \(Y\in\mathbb R^r\) satisfies
\[
\mathbb E YY^\top=I_r,
\qquad
\|\langle Y,x\rangle\|_{\psi_2}\le K\|x\|_2.
\]
Let \(Y_1,\dots,Y_m\) be independent copies and set
\[
A=\frac1m\sum_{i=1}^mY_iY_i^\top-I_r.
\]

For \(x\in S^{r-1}\), \(x^\top Ax=m^{-1}\sum_{i=1}^m(\langle Y_i,x\rangle^2-1)\).
Because \(\|\langle Y_i,x\rangle\|_{\psi_2}\le K\), the variables
\[
Z_i=\langle Y_i,x\rangle^2-1
\]
are centered and subexponential, with
\[
\|Z_i\|_{\psi_1}\le CK^2.
\]
Bernstein’s inequality therefore gives
\[
\mathbb P\{|x^\top Ax|>t\}
\le
2\exp\left[-cm\min\left(\frac{t^2}{K^4},\frac{t}{K^2}\right)\right].
\tag{1}
\]

Let \(\mathcal N\) be a \(1/4\)-net of \(S^{r-1}\) with
\[
|\mathcal N|\le 9^r.
\]
For every symmetric matrix \(A\),
\[
\|A\|\le 2\max_{x\in\mathcal N}|x^\top Ax|.
\]
Thus, by (1) and the union bound,
\[
\mathbb P\{\|A\|>2t\}
\le
2\exp\left[
Cr-cm\min\left(\frac{t^2}{K^4},\frac{t}{K^2}\right)
\right].
\]
Consequently, for every \(u\ge0\), with probability at least \(1-2e^{-u}\),
\[
\|A\|
\le
CK^2\left(
\sqrt{\frac{r+u}{m}}+\frac{r+u}{m}
\right).
\tag{2}
\]
Integrating this tail bound yields
\[
\mathbb E\|A\|
\le
CK^2\left(\sqrt{\frac rm}+\frac rm\right).
\tag{3}
\]

### Reduction to the isotropic case

Let \(S=\operatorname{range}(\Sigma)\) and \(r=\dim S\le n\). If \(v\in\ker(\Sigma)\), then
\[
\mathbb E\langle X,v\rangle^2=v^\top\Sigma v=0,
\]
so \(X\in S\) almost surely.

On \(S\), define
\[
Y=\Sigma^{-1/2}X,
\]
where the inverse is taken only on \(S\). Then
\[
\mathbb E YY^\top=I_S.
\]
Moreover, for every \(y\in S\),
\[
\begin{aligned}
\|\langle Y,y\rangle\|_{\psi_2}
&=\|\langle X,\Sigma^{-1/2}y\rangle\|_{\psi_2}\\
&\le K\|\langle X,\Sigma^{-1/2}y\rangle\|_{L_2}\\
&=K\|y\|_2.
\end{aligned}
\]
Thus \(Y\) satisfies the isotropic assumptions above.

Writing \(Y_i=\Sigma^{-1/2}X_i\), we have
\[
\Sigma_m-\Sigma
=
\Sigma^{1/2}
\left(
\frac1m\sum_{i=1}^mY_iY_i^\top-I_S
\right)
\Sigma^{1/2}.
\]
Hence
\[
\|\Sigma_m-\Sigma\|
\le
\|\Sigma\|
\left\|
\frac1m\sum_{i=1}^mY_iY_i^\top-I_S
\right\|.
\]
Applying (3) and using \(r\le n\), we obtain
\[
\boxed{
\mathbb E\|\Sigma_m-\Sigma\|
\le
CK^2\left(\sqrt{\frac nm}+\frac nm\right)\|\Sigma\|
}.
\]
Here \(C>0\) is an absolute constant.

### Retrieved strategy nodes

- `family_definitional_reformulation` — **Definitional unfolding and equivalent reformulation**: Convert abstract statements into explicit definitions, quantified conditions, or standard equivalent formulations.
- `sub_definitional_unfolding` — **Definitional unfolding**: Expand boundedness, inclusion, extrema, Riemann sums, and auxiliary constructions into their defining statements.
- `sub_metric_filter_characterization` — **Metric and filter characterizations**: Replace continuity, convergence, Cauchy conditions, and eventual properties by neighborhood, filter, or epsilon-based criteria.
- `sub_canonical_rewriting` — **Canonical rewriting**: Rewrite abstract distances, norms, slopes, interval interiors, and formal-series expressions in concrete canonical forms.
- `sub_set_extensionality` — **Set identities and extensionality**: Prove set equalities by extensionality or mutual inclusion and simplify Boolean set operations.
- `family_normalization_symmetry` — **Normalization, invariance, and symmetry**: Translate, rescale, whiten, permute, or otherwise transform a problem to a canonical case and transfer the conclusion back.
- `family_standard_theorem_reduction` — **Reduction to a standard theorem**: Modify domains and regularity hypotheses so that a known theorem applies directly.
- `sub_regularity_transfer` — **Restriction, extension, and transfer of regularity**: Restrict or extend functions and transfer continuity, differentiability, or integrability between compatible domains.
- `family_logical_reasoning` — **Logical decomposition, cases, and contradiction**: Split logical, order, endpoint, degeneracy, or parameter cases and use contradiction or contraposition to eliminate alternatives.
- `family_explicit_construction` — **Explicit construction and parameter choice**: Construct witnesses, sequences, partitions, comparison points, thresholds, or auxiliary objects and tune free parameters.
- `family_algebra_order_norm` — **Algebraic, order, and norm estimates**: Combine algebraic rearrangement and order reasoning with norm inequalities and duality estimates.
- `sub_elementary_algebra_order` — **Elementary algebra and order reasoning**: Prove positivity or nonvanishing, clear denominators, cancel factors, rearrange identities, and combine inequalities.
- `family_topology_compactness_connectedness` — **Compactness and connectedness methods**: Use compactness for boundedness, extrema, subsequences, and uniform continuity, and connectedness for intermediate values and zeros.
- `sub_compactness` — **Compactness arguments**: Apply compactness of intervals or images to obtain boundedness, attained extrema, uniform continuity, or convergent subsequences.
- `sub_intermediate_value` — **Intermediate Value Theorem**: Use continuity and endpoint value information to produce an intermediate value or interior zero.
- `family_extremal_order` — **Supremum, infimum, and extremal arguments**: Control quantities through suprema, infima, extremal points, or attained optimizers.
- `sub_order_completeness` — **Suprema, infima, and order completeness**: Apply least-upper-bound and greatest-lower-bound properties to bounded sets, images, limsups, and moduli of continuity.
- `family_limits_completeness` — **Limit, sequence, and completeness methods**: Use epsilon or filter formulations, limit laws, squeezing, completeness, subsequences, and limsup-liminf criteria.
- `sub_limit_laws_squeezing` — **Limit laws, squeezing, and uniqueness**: Compose limits, pass bounds to limits, squeeze between convergent quantities, and use uniqueness to identify limits.
- `sub_sequence_completeness` — **Sequence and completeness methods**: Use epsilon-N arguments, Cauchy completeness, subsequences, and sequences approaching a point.
- `sub_monotone_limsup_subsequence` — **Monotone sequences, limsup, and subsequences**: Use monotone convergence, limsup-liminf characterizations, and extraction of convergent subsequences.
- `family_differential_calculus` — **Differential-calculus arguments**: A broad calculus family covering differentiability criteria, derivative rules, mean-value principles, derivative signs, and Taylor expansion.
- `sub_difference_quotient` — **Difference-quotient characterization of differentiability**: Express differentiability as convergence of slopes on a punctured neighborhood.
- `sub_derivative_rules` — **Differential calculus rules**: Apply chain, composition, and related closure rules for differentiable functions.
- `sub_mean_value_theorems` — **Fermat, Rolle, and Mean Value Theorems**: Convert extrema or endpoint equalities into derivative information and represent increments by intermediate derivatives.
- `sub_derivative_sign` — **Derivative-sign arguments**: Infer monotonicity, constancy, or local extrema from first- or second-derivative sign information.
- `sub_taylor_remainder` — **Taylor expansion with remainder**: Apply finite Taylor expansion with a controlled remainder and normalize the resulting coefficients.
- `family_error_decomposition` — **Error decomposition and balancing**: Split a total error into analyzable components and choose parameters that balance the dominant contributions.
- `sub_triangle_error_estimates` — **Triangle-inequality and error-decomposition estimates**: Separate dominant and error terms and control them with triangle and reverse-triangle inequalities.
- `sub_approximation_archimedean` — **Approximation and Archimedean error control**: Choose dense approximants and then select an index making the uniform approximation error smaller than a prescribed tolerance.
- `family_comparison_domination` — **Comparison, domination, and squeezing**: Bound complicated quantities by simpler majorants and transfer those bounds through sums, integrals, limits, and suprema.
- `family_series_convergence` — **Series and uniform-convergence methods**: A broad family covering summability tests, uniform convergence, and power-series convergence radii.
- `sub_series_tests` — **Series comparison and convergence tests**: Use comparison, term, root, ratio, alternating-series, geometric, or rearrangement criteria.
- `sub_uniform_convergence_mtest` — **Uniform convergence and the Weierstrass M-test**: Produce a summable uniform majorant and transfer continuity or bounds to the resulting series.
- `sub_power_series_radius` — **Power-series radius arguments**: Compare coefficient growth and apply Cauchy-Hadamard or radius-of-convergence comparison results.
- `family_integral_calculus` — **Integral-calculus arguments**: A broad integration family covering the fundamental theorem, structural integral identities, transformations, and Riemann-sum methods.
- `sub_fundamental_theorem_calculus` — **Fundamental Theorem of Calculus**: Convert derivatives into integral increments or differentiate parameterized integrals.
- `sub_integral_structure` — **Structural properties of the integral**: Use linearity, interval additivity, monotonicity, constant-integral formulas, and integral norm inequalities.
- `sub_integration_transformations` — **Integration by parts and substitution**: Verify regularity and integrability hypotheses and then apply integration by parts or change of variables.
- `sub_partition_refinement` — **Partition and refinement arguments**: Control meshes and subintervals, construct common refinements, and decompose coarse partitions into fine pieces.
- `sub_riemann_modulus_control` — **Modulus-of-continuity control of Riemann sums**: Control tag changes using a modulus of continuity and sum local errors to prove convergence and partition independence.
- `family_reindexing_telescoping` — **Reindexing and telescoping sums**: Reindex sums under bijections or fibers and cancel consecutive terms so only boundary contributions remain.
- `family_induction_well_ordering` — **Induction, recurrence, and well-ordering**: Use induction, strengthened hypotheses, recurrence, least witnesses, or minimal counterexamples over the natural numbers.
- `family_structural_foundations` — **Cardinality, embeddings, and completion**: Use embeddings and cardinal comparisons or construct complete ordered structures from dense substructures and cuts.
- `sub_ordered_field_constructions` — **Ordered-field structure and canonical constructions**: Use ordered-field operations, canonical witnesses, Archimedeanness, completeness, and rational cuts in structural arguments about the reals.
- `sub_cardinality_embeddings` — **Cardinality and embedding arguments**: Use injections, diagonalization, Cantor's theorem, interval cardinality, and Cantor-Schroeder-Bernstein.
- `family_variational_linear_algebra` — **Variational and linear-algebraic methods**: Optimization and geometric methods based on convexity, orthogonality, projections, spectra, and structured parameter spaces.
- `sub_convexity_variational` — **Convexity and variational arguments**: Use Jensen's inequality, convex combinations, first-order optimality, or comparison with feasible competitors.
- `sub_orthogonality_spectral` — **Orthogonality, projection, and spectral arguments**: Use orthogonal expansions, Pythagoras, Parseval, normal equations, Rayleigh quotients, and eigenvector principles.
- `sub_structured_parameters` — **Sparsity, low-rank structure, and norm duality**: Exploit support, cone, rank, or singular-space decompositions together with dual norms and restricted geometric conditions.
- `family_metric_entropy` — **Metric entropy, covering, and packing methods**: Discretize continuous classes by finite nets or construct well-separated finite subsets using packing methods.
- `sub_covering_volumetric` — **Covering-net and volumetric arguments**: Replace continuous suprema by maxima over finite epsilon-nets and bound net sizes through packing and volume comparison.
- `sub_probabilistic_packing` — **Probabilistic method and packing constructions**: Randomly generate nets, codes, sparse vectors, or approximants and prove that a suitable deterministic construction exists.
- `family_probability_information` — **Probability, concentration, and information methods**: Probabilistic proof methods based on exponential moments, tails, independence, union bounds, and information-theoretic reductions.
- `sub_exponential_concentration` — **Exponential-moment and concentration arguments**: Apply exponential Markov inequalities, control moment-generating functions, and optimize parameters to derive tail bounds.
- `sub_tail_integration` — **Tail integration and moment estimates**: Convert moments into tail integrals, insert probability bounds, and estimate the resulting integrals.
- `sub_independence_tensorization` — **Independence, tensorization, and union bounds**: Factor quantities using independence, tensorize information, and upgrade pointwise bounds to simultaneous bounds by a union bound.
- `sub_testing_information` — **Testing and information-theoretic reductions**: Reduce estimation to hypothesis testing and control testing error using divergence or mutual-information inequalities.

---

## lemma_8_3_14 — Lemma 8.3.14 (Dimension reduction)

Dataset: `high_dimensional_probability`

### Input statement

Lemma 8.3.14 (Dimension reduction). Let F be a finite class of Boolean func-
tions on a domain Ω with a probability measure µ on it. Assume that all functions
in F are ε-separated, that is
                    ∥f − g∥L2 (µ) > ε     for all distinct f, g ∈ F.
If n ≥ Cε−4 log|F |, then the empirical measure µn satisfies the following with
probability at least 0.99:
                  ∥f − g∥L2 (µn ) > ε/2    for all distinct f, g ∈ F.
  By definition of empirical measure (see Section 8.2.3), ∥f − g∥L2 (µn ) is the same
as (8.31) but with the population average replaced by the sample average:
                                      1 Xn                1/2
                    ∥f − g∥L2 (µn ) =        (f − g)(Xi )2      ,               (8.32)
                                       n i=1
where Xi are i.i.d. copies of X.

### Task

Explain the proof strategy and give a proof plan. Identify the main mathematical methods used.

### Control output

Let \(m=|F|\). If \(m\le 1\), the conclusion is vacuous, so assume \(m\ge 2\).

Fix distinct \(f,g\in F\), and define
\[
Y_i=(f(X_i)-g(X_i))^2.
\]
Since \(f,g\) are Boolean-valued, \(0\le Y_i\le 4\) under either standard convention \(f:\Omega\to\{0,1\}\) or \(f:\Omega\to\{-1,1\}\). Moreover,
\[
\mathbb EY_i=\|f-g\|_{L_2(\mu)}^2>\varepsilon^2.
\]
On the other hand,
\[
\|f-g\|_{L_2(\mu_n)}^2=\frac1n\sum_{i=1}^nY_i.
\]

Thus, by Hoeffding’s inequality,
\[
\begin{aligned}
\mathbb P\left\{\|f-g\|_{L_2(\mu_n)}\le \frac{\varepsilon}{2}\right\}
&=\mathbb P\left\{\frac1n\sum_{i=1}^nY_i\le \frac{\varepsilon^2}{4}\right\}\\
&\le
\mathbb P\left\{\frac1n\sum_{i=1}^nY_i-\mathbb EY_i
\le -\frac{3\varepsilon^2}{4}\right\}\\
&\le \exp\left(
-\frac{2n(3\varepsilon^2/4)^2}{4^2}
\right)\\
&=\exp\left(-\frac{9}{128}n\varepsilon^4\right).
\end{aligned}
\]

There are at most \(m^2\) ordered pairs of distinct functions. Therefore, by the union bound,
\[
\mathbb P\left\{\exists f\ne g:\,
\|f-g\|_{L_2(\mu_n)}\le \frac{\varepsilon}{2}\right\}
\le
m^2\exp\left(-\frac{9}{128}n\varepsilon^4\right).
\]

If
\[
n\ge 128\,\varepsilon^{-4}\log m,
\]
then the right-hand side is at most
\[
m^2e^{-9\log m}=m^{-7}\le 2^{-7}<0.01.
\]
Consequently, with probability at least \(0.99\),
\[
\|f-g\|_{L_2(\mu_n)}>\frac{\varepsilon}{2}
\qquad\text{for every distinct }f,g\in F.
\]

Thus the assertion holds for a universal constant \(C\) (for example, \(C=128\)). \(\square\)

### Library-RAG output

Let \(m=|F|\). If \(m\le 1\), the conclusion is vacuous, so assume \(m\ge 2\).

Fix distinct \(f,g\in F\), and define
\[
Y_i=(f(X_i)-g(X_i))^2.
\]
Directly, \(0\le Y_i\le 4\), \(\mathbb EY_i=\|f-g\|_{L_2(\mu)}^2>\varepsilon^2\), and \(\|f-g\|_{L_2(\mu_n)}^2=n^{-1}\sum_{i=1}^nY_i\).

Thus, by Hoeffding’s inequality,
\[
\begin{aligned}
\mathbb P\left\{\|f-g\|_{L_2(\mu_n)}\le \frac{\varepsilon}{2}\right\}
&=\mathbb P\left\{\frac1n\sum_{i=1}^nY_i\le \frac{\varepsilon^2}{4}\right\}\\
&\le
\mathbb P\left\{\frac1n\sum_{i=1}^nY_i-\mathbb EY_i
\le -\frac{3\varepsilon^2}{4}\right\}\\
&\le \exp\left(
-\frac{2n(3\varepsilon^2/4)^2}{4^2}
\right)\\
&=\exp\left(-\frac{9}{128}n\varepsilon^4\right).
\end{aligned}
\]

There are at most \(m^2\) ordered pairs of distinct functions. Therefore, by the union bound,
\[
\mathbb P\left\{\exists f\ne g:\,
\|f-g\|_{L_2(\mu_n)}\le \frac{\varepsilon}{2}\right\}
\le
m^2\exp\left(-\frac{9}{128}n\varepsilon^4\right).
\]

If \(n\ge 128\,\varepsilon^{-4}\log m\), then the right-hand side is at most \(m^{-7}<0.01\).
Consequently, with probability at least \(0.99\),
\[
\|f-g\|_{L_2(\mu_n)}>\frac{\varepsilon}{2}
\qquad\text{for every distinct }f,g\in F.
\]

Thus the assertion holds for a universal constant \(C\) (for example, \(C=128\)). \(\square\)

### Retrieved strategy nodes

- `family_definitional_reformulation` — **Definitional unfolding and equivalent reformulation**: Convert abstract statements into explicit definitions, quantified conditions, or standard equivalent formulations.
- `sub_definitional_unfolding` — **Definitional unfolding**: Expand boundedness, inclusion, extrema, Riemann sums, and auxiliary constructions into their defining statements.
- `sub_metric_filter_characterization` — **Metric and filter characterizations**: Replace continuity, convergence, Cauchy conditions, and eventual properties by neighborhood, filter, or epsilon-based criteria.
- `sub_canonical_rewriting` — **Canonical rewriting**: Rewrite abstract distances, norms, slopes, interval interiors, and formal-series expressions in concrete canonical forms.
- `sub_set_extensionality` — **Set identities and extensionality**: Prove set equalities by extensionality or mutual inclusion and simplify Boolean set operations.
- `family_normalization_symmetry` — **Normalization, invariance, and symmetry**: Translate, rescale, whiten, permute, or otherwise transform a problem to a canonical case and transfer the conclusion back.
- `family_standard_theorem_reduction` — **Reduction to a standard theorem**: Modify domains and regularity hypotheses so that a known theorem applies directly.
- `sub_regularity_transfer` — **Restriction, extension, and transfer of regularity**: Restrict or extend functions and transfer continuity, differentiability, or integrability between compatible domains.
- `family_logical_reasoning` — **Logical decomposition, cases, and contradiction**: Split logical, order, endpoint, degeneracy, or parameter cases and use contradiction or contraposition to eliminate alternatives.
- `family_explicit_construction` — **Explicit construction and parameter choice**: Construct witnesses, sequences, partitions, comparison points, thresholds, or auxiliary objects and tune free parameters.
- `family_algebra_order_norm` — **Algebraic, order, and norm estimates**: Combine algebraic rearrangement and order reasoning with norm inequalities and duality estimates.
- `sub_elementary_algebra_order` — **Elementary algebra and order reasoning**: Prove positivity or nonvanishing, clear denominators, cancel factors, rearrange identities, and combine inequalities.
- `family_topology_compactness_connectedness` — **Compactness and connectedness methods**: Use compactness for boundedness, extrema, subsequences, and uniform continuity, and connectedness for intermediate values and zeros.
- `sub_compactness` — **Compactness arguments**: Apply compactness of intervals or images to obtain boundedness, attained extrema, uniform continuity, or convergent subsequences.
- `sub_intermediate_value` — **Intermediate Value Theorem**: Use continuity and endpoint value information to produce an intermediate value or interior zero.
- `family_extremal_order` — **Supremum, infimum, and extremal arguments**: Control quantities through suprema, infima, extremal points, or attained optimizers.
- `sub_order_completeness` — **Suprema, infima, and order completeness**: Apply least-upper-bound and greatest-lower-bound properties to bounded sets, images, limsups, and moduli of continuity.
- `family_limits_completeness` — **Limit, sequence, and completeness methods**: Use epsilon or filter formulations, limit laws, squeezing, completeness, subsequences, and limsup-liminf criteria.
- `sub_limit_laws_squeezing` — **Limit laws, squeezing, and uniqueness**: Compose limits, pass bounds to limits, squeeze between convergent quantities, and use uniqueness to identify limits.
- `sub_sequence_completeness` — **Sequence and completeness methods**: Use epsilon-N arguments, Cauchy completeness, subsequences, and sequences approaching a point.
- `sub_monotone_limsup_subsequence` — **Monotone sequences, limsup, and subsequences**: Use monotone convergence, limsup-liminf characterizations, and extraction of convergent subsequences.
- `family_differential_calculus` — **Differential-calculus arguments**: A broad calculus family covering differentiability criteria, derivative rules, mean-value principles, derivative signs, and Taylor expansion.
- `sub_difference_quotient` — **Difference-quotient characterization of differentiability**: Express differentiability as convergence of slopes on a punctured neighborhood.
- `sub_derivative_rules` — **Differential calculus rules**: Apply chain, composition, and related closure rules for differentiable functions.
- `sub_mean_value_theorems` — **Fermat, Rolle, and Mean Value Theorems**: Convert extrema or endpoint equalities into derivative information and represent increments by intermediate derivatives.
- `sub_derivative_sign` — **Derivative-sign arguments**: Infer monotonicity, constancy, or local extrema from first- or second-derivative sign information.
- `sub_taylor_remainder` — **Taylor expansion with remainder**: Apply finite Taylor expansion with a controlled remainder and normalize the resulting coefficients.
- `family_error_decomposition` — **Error decomposition and balancing**: Split a total error into analyzable components and choose parameters that balance the dominant contributions.
- `sub_triangle_error_estimates` — **Triangle-inequality and error-decomposition estimates**: Separate dominant and error terms and control them with triangle and reverse-triangle inequalities.
- `sub_approximation_archimedean` — **Approximation and Archimedean error control**: Choose dense approximants and then select an index making the uniform approximation error smaller than a prescribed tolerance.
- `family_comparison_domination` — **Comparison, domination, and squeezing**: Bound complicated quantities by simpler majorants and transfer those bounds through sums, integrals, limits, and suprema.
- `family_series_convergence` — **Series and uniform-convergence methods**: A broad family covering summability tests, uniform convergence, and power-series convergence radii.
- `sub_series_tests` — **Series comparison and convergence tests**: Use comparison, term, root, ratio, alternating-series, geometric, or rearrangement criteria.
- `sub_uniform_convergence_mtest` — **Uniform convergence and the Weierstrass M-test**: Produce a summable uniform majorant and transfer continuity or bounds to the resulting series.
- `sub_power_series_radius` — **Power-series radius arguments**: Compare coefficient growth and apply Cauchy-Hadamard or radius-of-convergence comparison results.
- `family_integral_calculus` — **Integral-calculus arguments**: A broad integration family covering the fundamental theorem, structural integral identities, transformations, and Riemann-sum methods.
- `sub_fundamental_theorem_calculus` — **Fundamental Theorem of Calculus**: Convert derivatives into integral increments or differentiate parameterized integrals.
- `sub_integral_structure` — **Structural properties of the integral**: Use linearity, interval additivity, monotonicity, constant-integral formulas, and integral norm inequalities.
- `sub_integration_transformations` — **Integration by parts and substitution**: Verify regularity and integrability hypotheses and then apply integration by parts or change of variables.
- `sub_partition_refinement` — **Partition and refinement arguments**: Control meshes and subintervals, construct common refinements, and decompose coarse partitions into fine pieces.
- `sub_riemann_modulus_control` — **Modulus-of-continuity control of Riemann sums**: Control tag changes using a modulus of continuity and sum local errors to prove convergence and partition independence.
- `family_reindexing_telescoping` — **Reindexing and telescoping sums**: Reindex sums under bijections or fibers and cancel consecutive terms so only boundary contributions remain.
- `family_induction_well_ordering` — **Induction, recurrence, and well-ordering**: Use induction, strengthened hypotheses, recurrence, least witnesses, or minimal counterexamples over the natural numbers.
- `family_structural_foundations` — **Cardinality, embeddings, and completion**: Use embeddings and cardinal comparisons or construct complete ordered structures from dense substructures and cuts.
- `sub_ordered_field_constructions` — **Ordered-field structure and canonical constructions**: Use ordered-field operations, canonical witnesses, Archimedeanness, completeness, and rational cuts in structural arguments about the reals.
- `sub_cardinality_embeddings` — **Cardinality and embedding arguments**: Use injections, diagonalization, Cantor's theorem, interval cardinality, and Cantor-Schroeder-Bernstein.
- `family_variational_linear_algebra` — **Variational and linear-algebraic methods**: Optimization and geometric methods based on convexity, orthogonality, projections, spectra, and structured parameter spaces.
- `sub_convexity_variational` — **Convexity and variational arguments**: Use Jensen's inequality, convex combinations, first-order optimality, or comparison with feasible competitors.
- `sub_orthogonality_spectral` — **Orthogonality, projection, and spectral arguments**: Use orthogonal expansions, Pythagoras, Parseval, normal equations, Rayleigh quotients, and eigenvector principles.
- `sub_structured_parameters` — **Sparsity, low-rank structure, and norm duality**: Exploit support, cone, rank, or singular-space decompositions together with dual norms and restricted geometric conditions.
- `family_metric_entropy` — **Metric entropy, covering, and packing methods**: Discretize continuous classes by finite nets or construct well-separated finite subsets using packing methods.
- `sub_covering_volumetric` — **Covering-net and volumetric arguments**: Replace continuous suprema by maxima over finite epsilon-nets and bound net sizes through packing and volume comparison.
- `sub_probabilistic_packing` — **Probabilistic method and packing constructions**: Randomly generate nets, codes, sparse vectors, or approximants and prove that a suitable deterministic construction exists.
- `family_probability_information` — **Probability, concentration, and information methods**: Probabilistic proof methods based on exponential moments, tails, independence, union bounds, and information-theoretic reductions.
- `sub_exponential_concentration` — **Exponential-moment and concentration arguments**: Apply exponential Markov inequalities, control moment-generating functions, and optimize parameters to derive tail bounds.
- `sub_tail_integration` — **Tail integration and moment estimates**: Convert moments into tail integrals, insert probability bounds, and estimate the resulting integrals.
- `sub_independence_tensorization` — **Independence, tensorization, and union bounds**: Factor quantities using independence, tensorize information, and upgrade pointwise bounds to simultaneous bounds by a union bound.
- `sub_testing_information` — **Testing and information-theoretic reductions**: Reduce estimation to hypothesis testing and control testing error using divergence or mutual-information inequalities.

---

## theorem_7_2_2 — Theorem 7.2.2 (Slepian inequality). Let (Xt )t∈T and (Yt)

Dataset: `high_dimensional_probability`

### Input statement

Theorem 7.2.2 (Slepian inequality). Let (Xt )t∈T and (Yt )t∈T be two mean-zero
Gaussian processes. Assume that for all t, s ∈ T , we have
                E Xt2 = E Yt2     and     E(Xt − Xs )2 ≤ E(Yt − Ys )2 .      (7.3)
Then supt∈T Xt is stochastically dominated by supt∈T Yt : for every τ ∈ R, we have
                          n          o   n          o
                         P sup Xt ≥ τ ≤ P sup Yt ≥ τ .                       (7.4)
                            t∈T                   t∈T

Consequently,
                                  E sup Xt ≤ E sup Yt .                      (7.5)
                                    t∈T          t∈T

  We now prepare for the

### Task

Explain the proof strategy and give a proof plan. Identify the main mathematical methods used.

### Control output

Assume the suprema are measurable and separable—for example, \(T\) is countable, or there is a countable \(T_0\subseteq T\) over which both suprema agree almost surely. We first prove the result for finite \(T\).

### 1. Finite-dimensional case

Let \(T=\{1,\dots,n\}\), and write
\[
A_{ij}=\mathbb E[X_iX_j],
\qquad
B_{ij}=\mathbb E[Y_iY_j].
\]
The variance assumption gives
\[
A_{ii}=B_{ii}.
\]
Moreover,
\[
\mathbb E(X_i-X_j)^2
  =A_{ii}+A_{jj}-2A_{ij},
\]
and similarly for \(Y\). Therefore, the increment assumption implies
\[
A_{ij}\ge B_{ij}\qquad (i\ne j).
\]

Interpolate between the two covariance matrices:
\[
C(u)=(1-u)B+uA,\qquad 0\le u\le 1,
\]
and let \(Z(u)\) be a centered Gaussian vector with covariance \(C(u)\).

For every smooth function \(h:\mathbb R^n\to\mathbb R\) with bounded derivatives, the Gaussian interpolation identity gives
\[
\frac{d}{du}\mathbb E h(Z(u))
=
\frac12\sum_{i,j=1}^n
(A_{ij}-B_{ij})\,
\mathbb E\big[\partial_{ij}h(Z(u))\big].
\tag{1}
\]
If some covariance matrices are singular, this follows by adding \(\varepsilon I\) and then letting \(\varepsilon\downarrow0\).

Fix \(r\in\mathbb R\). Choose a smooth nonincreasing function
\[
g_\varepsilon:\mathbb R\to[0,1]
\]
such that
\[
g_\varepsilon(x)=1\quad\text{for }x\le r,
\qquad
g_\varepsilon(x)=0\quad\text{for }x\ge r+\varepsilon,
\]
and define
\[
h_\varepsilon(x_1,\dots,x_n)
=\prod_{k=1}^n g_\varepsilon(x_k).
\]
For \(i\ne j\),
\[
\partial_{ij}h_\varepsilon(x)
=
g_\varepsilon'(x_i)g_\varepsilon'(x_j)
\prod_{k\ne i,j}g_\varepsilon(x_k)\ge0,
\]
because \(g_\varepsilon'\le0\). The diagonal terms in (1) vanish since
\(A_{ii}-B_{ii}=0\), while all off-diagonal terms are nonnegative. Hence
\[
\frac{d}{du}\mathbb E h_\varepsilon(Z(u))\ge0.
\]
Evaluating at \(u=0\) and \(u=1\),
\[
\mathbb E h_\varepsilon(X)
\ge
\mathbb E h_\varepsilon(Y).
\]
Letting \(\varepsilon\downarrow0\) and using bounded convergence yields
\[
\mathbb P\left\{\max_{1\le i\le n}X_i\le r\right\}
\ge
\mathbb P\left\{\max_{1\le i\le n}Y_i\le r\right\}.
\tag{2}
\]

Thus the maximum of the \(X_i\)'s is stochastically smaller than the maximum of the \(Y_i\)'s.

### 2. General separable index sets

Choose a countable set \(T_0=\{t_1,t_2,\dots\}\subseteq T\) such that
\[
\sup_{t\in T}X_t=\sup_{t\in T_0}X_t,
\qquad
\sup_{t\in T}Y_t=\sup_{t\in T_0}Y_t
\quad\text{a.s.}
\]
Set
\[
M_n^X=\max_{1\le k\le n}X_{t_k},
\qquad
M_n^Y=\max_{1\le k\le n}Y_{t_k}.
\]
By (2),
\[
\mathbb P\{M_n^X\le r\}\ge \mathbb P\{M_n^Y\le r\}.
\]
Since \(M_n^X\uparrow \sup_tX_t\) and \(M_n^Y\uparrow\sup_tY_t\),
continuity of probability from above gives
\[
\mathbb P\left\{\sup_{t\in T}X_t\le r\right\}
\ge
\mathbb P\left\{\sup_{t\in T}Y_t\le r\right\}.
\tag{3}
\]
Taking left limits in \(r\), we obtain, for every \(\tau\in\mathbb R\),
\[
\mathbb P\left\{\sup_{t\in T}X_t\ge\tau\right\}
\le
\mathbb P\left\{\sup_{t\in T}Y_t\ge\tau\right\}.
\]
This is the claimed stochastic domination.

### 3. Comparison of expectations

Let
\[
U=\sup_{t\in T}X_t,\qquad V=\sup_{t\in T}Y_t.
\]
Stochastic domination implies
\[
\mathbb E\phi(U)\le \mathbb E\phi(V)
\]
for every bounded increasing function \(\phi\). Applying this to
\[
\phi_m(x)=(-m)\vee(x\wedge m)
\]
and letting \(m\to\infty\) gives
\[
\mathbb E U\le \mathbb E V.
\]
Indeed, for any fixed \(t_0\in T\),
\[
U^-\le X_{t_0}^-,
\qquad
V^-\le Y_{t_0}^-,
\]
so both negative parts are integrable; the positive parts may be infinite, in which case the inequality is understood in the extended sense. Therefore
\[
\boxed{\mathbb E\sup_{t\in T}X_t
\le
\mathbb E\sup_{t\in T}Y_t.}
\]

The separability convention is essential for arbitrary uncountable \(T\); equivalently, one may interpret the suprema as essential/separable suprema.

### Library-RAG output

Assume the suprema are measurable and separable—for example, \(T\) is countable, or there is a countable \(T_0\subseteq T\) over which both suprema agree almost surely. We first prove the result for finite \(T\).

### 1. Finite-dimensional case

Let \(T=\{1,\dots,n\}\), and write
\[
A_{ij}=\mathbb E[X_iX_j],
\qquad
B_{ij}=\mathbb E[Y_iY_j].
\]
The variance assumption gives
\[
A_{ii}=B_{ii}.
\]
Comparing \(\mathbb E(X_i-X_j)^2=A_{ii}+A_{jj}-2A_{ij}\) with the analogous formula for \(Y\), and using \(A_{ii}=B_{ii}\), gives \(A_{ij}\ge B_{ij}\) for \(i\ne j\).

Interpolate between the two covariance matrices:
\[
C(u)=(1-u)B+uA,\qquad 0\le u\le 1,
\]
and let \(Z(u)\) be a centered Gaussian vector with covariance \(C(u)\). Put \(D=A-B\).

Suppose first that \(C(u)\) is positive definite, and denote the density of \(Z(u)\) by \(p_u\). Differentiating its Fourier transform gives
\[
\partial_u p_u(x)=\frac12\sum_{i,j=1}^nD_{ij}\,\partial_{ij}p_u(x).
\]
Consequently, for every smooth bounded function \(h:\mathbb R^n\to\mathbb R\) with bounded derivatives, differentiation under the integral followed by two integrations by parts yields the Gaussian interpolation identity
\[
\frac{d}{du}\mathbb E h(Z(u))
=
\frac12\sum_{i,j=1}^n
(A_{ij}-B_{ij})\,
\mathbb E\big[\partial_{ij}h(Z(u))\big].
\tag{1}
\]
If the covariance matrices are singular, replace \(C(u)\) by \(C(u)+\delta I\). The identity and the ensuing monotonicity then hold for the regularized Gaussian vectors; letting \(\delta\downarrow0\) recovers the comparison because the regularized vectors converge in distribution and \(h\) is bounded and continuous.

Fix \(r\in\mathbb R\). Choose a smooth nonincreasing function
\[
g_\varepsilon:\mathbb R\to[0,1]
\]
such that
\[
g_\varepsilon(x)=1\quad\text{for }x\le r,
\qquad
g_\varepsilon(x)=0\quad\text{for }x\ge r+\varepsilon,
\]
and define
\[
h_\varepsilon(x_1,\dots,x_n)
=\prod_{k=1}^n g_\varepsilon(x_k).
\]
For \(i\ne j\),
\[
\partial_{ij}h_\varepsilon(x)
=
g_\varepsilon'(x_i)g_\varepsilon'(x_j)
\prod_{k\ne i,j}g_\varepsilon(x_k)\ge0,
\]
because \(g_\varepsilon'\le0\). The diagonal terms in (1) vanish since
\(A_{ii}-B_{ii}=0\), while all off-diagonal terms are nonnegative. Hence
\[
\frac{d}{du}\mathbb E h_\varepsilon(Z(u))\ge0.
\]
Evaluating at \(u=0\) and \(u=1\),
\[
\mathbb E h_\varepsilon(X)
\ge
\mathbb E h_\varepsilon(Y).
\]
Letting \(\varepsilon\downarrow0\) and using bounded convergence yields
\[
\mathbb P\left\{\max_{1\le i\le n}X_i\le r\right\}
\ge
\mathbb P\left\{\max_{1\le i\le n}Y_i\le r\right\}.
\tag{2}
\]

Thus the maximum of the \(X_i\)'s is stochastically smaller than the maximum of the \(Y_i\)'s.

### 2. General separable index sets

Choose a countable set \(T_0=\{t_1,t_2,\dots\}\subseteq T\) such that
\[
\sup_{t\in T}X_t=\sup_{t\in T_0}X_t,
\qquad
\sup_{t\in T}Y_t=\sup_{t\in T_0}Y_t
\quad\text{a.s.}
\]
Set
\[
M_n^X=\max_{1\le k\le n}X_{t_k},
\qquad
M_n^Y=\max_{1\le k\le n}Y_{t_k}.
\]
By (2),
\[
\mathbb P\{M_n^X\le r\}\ge \mathbb P\{M_n^Y\le r\}.
\]
Since \(M_n^X\uparrow \sup_tX_t\) and \(M_n^Y\uparrow\sup_tY_t\),
continuity of probability from above gives
\[
\mathbb P\left\{\sup_{t\in T}X_t\le r\right\}
\ge
\mathbb P\left\{\sup_{t\in T}Y_t\le r\right\}.
\tag{3}
\]
Taking left limits in \(r\), we obtain, for every \(\tau\in\mathbb R\),
\[
\mathbb P\left\{\sup_{t\in T}X_t\ge\tau\right\}
\le
\mathbb P\left\{\sup_{t\in T}Y_t\ge\tau\right\}.
\]
This is the claimed stochastic domination.

### 3. Comparison of expectations

Let
\[
U=\sup_{t\in T}X_t,\qquad V=\sup_{t\in T}Y_t.
\]
Stochastic domination implies
\[
\mathbb E\phi(U)\le \mathbb E\phi(V)
\]
for every bounded increasing function \(\phi\). Applying this to
\[
\phi_m(x)=(-m)\vee(x\wedge m)
\]
and letting \(m\to\infty\) gives
\[
\mathbb E U\le \mathbb E V.
\]
Indeed, for any fixed \(t_0\in T\),
\[
U^-\le X_{t_0}^-,
\qquad
V^-\le Y_{t_0}^-,
\]
so both negative parts are integrable; the positive parts may be infinite, in which case the inequality is understood in the extended sense. Therefore
\[
\boxed{\mathbb E\sup_{t\in T}X_t
\le
\mathbb E\sup_{t\in T}Y_t.}
\]

The separability convention is essential for arbitrary uncountable \(T\); equivalently, one may interpret the suprema as essential/separable suprema.

### Retrieved strategy nodes

- `family_definitional_reformulation` — **Definitional unfolding and equivalent reformulation**: Convert abstract statements into explicit definitions, quantified conditions, or standard equivalent formulations.
- `sub_definitional_unfolding` — **Definitional unfolding**: Expand boundedness, inclusion, extrema, Riemann sums, and auxiliary constructions into their defining statements.
- `sub_metric_filter_characterization` — **Metric and filter characterizations**: Replace continuity, convergence, Cauchy conditions, and eventual properties by neighborhood, filter, or epsilon-based criteria.
- `sub_canonical_rewriting` — **Canonical rewriting**: Rewrite abstract distances, norms, slopes, interval interiors, and formal-series expressions in concrete canonical forms.
- `sub_set_extensionality` — **Set identities and extensionality**: Prove set equalities by extensionality or mutual inclusion and simplify Boolean set operations.
- `family_normalization_symmetry` — **Normalization, invariance, and symmetry**: Translate, rescale, whiten, permute, or otherwise transform a problem to a canonical case and transfer the conclusion back.
- `family_standard_theorem_reduction` — **Reduction to a standard theorem**: Modify domains and regularity hypotheses so that a known theorem applies directly.
- `sub_regularity_transfer` — **Restriction, extension, and transfer of regularity**: Restrict or extend functions and transfer continuity, differentiability, or integrability between compatible domains.
- `family_logical_reasoning` — **Logical decomposition, cases, and contradiction**: Split logical, order, endpoint, degeneracy, or parameter cases and use contradiction or contraposition to eliminate alternatives.
- `family_explicit_construction` — **Explicit construction and parameter choice**: Construct witnesses, sequences, partitions, comparison points, thresholds, or auxiliary objects and tune free parameters.
- `family_algebra_order_norm` — **Algebraic, order, and norm estimates**: Combine algebraic rearrangement and order reasoning with norm inequalities and duality estimates.
- `sub_elementary_algebra_order` — **Elementary algebra and order reasoning**: Prove positivity or nonvanishing, clear denominators, cancel factors, rearrange identities, and combine inequalities.
- `family_topology_compactness_connectedness` — **Compactness and connectedness methods**: Use compactness for boundedness, extrema, subsequences, and uniform continuity, and connectedness for intermediate values and zeros.
- `sub_compactness` — **Compactness arguments**: Apply compactness of intervals or images to obtain boundedness, attained extrema, uniform continuity, or convergent subsequences.
- `sub_intermediate_value` — **Intermediate Value Theorem**: Use continuity and endpoint value information to produce an intermediate value or interior zero.
- `family_extremal_order` — **Supremum, infimum, and extremal arguments**: Control quantities through suprema, infima, extremal points, or attained optimizers.
- `sub_order_completeness` — **Suprema, infima, and order completeness**: Apply least-upper-bound and greatest-lower-bound properties to bounded sets, images, limsups, and moduli of continuity.
- `family_limits_completeness` — **Limit, sequence, and completeness methods**: Use epsilon or filter formulations, limit laws, squeezing, completeness, subsequences, and limsup-liminf criteria.
- `sub_limit_laws_squeezing` — **Limit laws, squeezing, and uniqueness**: Compose limits, pass bounds to limits, squeeze between convergent quantities, and use uniqueness to identify limits.
- `sub_sequence_completeness` — **Sequence and completeness methods**: Use epsilon-N arguments, Cauchy completeness, subsequences, and sequences approaching a point.
- `sub_monotone_limsup_subsequence` — **Monotone sequences, limsup, and subsequences**: Use monotone convergence, limsup-liminf characterizations, and extraction of convergent subsequences.
- `family_differential_calculus` — **Differential-calculus arguments**: A broad calculus family covering differentiability criteria, derivative rules, mean-value principles, derivative signs, and Taylor expansion.
- `sub_difference_quotient` — **Difference-quotient characterization of differentiability**: Express differentiability as convergence of slopes on a punctured neighborhood.
- `sub_derivative_rules` — **Differential calculus rules**: Apply chain, composition, and related closure rules for differentiable functions.
- `sub_mean_value_theorems` — **Fermat, Rolle, and Mean Value Theorems**: Convert extrema or endpoint equalities into derivative information and represent increments by intermediate derivatives.
- `sub_derivative_sign` — **Derivative-sign arguments**: Infer monotonicity, constancy, or local extrema from first- or second-derivative sign information.
- `sub_taylor_remainder` — **Taylor expansion with remainder**: Apply finite Taylor expansion with a controlled remainder and normalize the resulting coefficients.
- `family_error_decomposition` — **Error decomposition and balancing**: Split a total error into analyzable components and choose parameters that balance the dominant contributions.
- `sub_triangle_error_estimates` — **Triangle-inequality and error-decomposition estimates**: Separate dominant and error terms and control them with triangle and reverse-triangle inequalities.
- `sub_approximation_archimedean` — **Approximation and Archimedean error control**: Choose dense approximants and then select an index making the uniform approximation error smaller than a prescribed tolerance.
- `family_comparison_domination` — **Comparison, domination, and squeezing**: Bound complicated quantities by simpler majorants and transfer those bounds through sums, integrals, limits, and suprema.
- `family_series_convergence` — **Series and uniform-convergence methods**: A broad family covering summability tests, uniform convergence, and power-series convergence radii.
- `sub_series_tests` — **Series comparison and convergence tests**: Use comparison, term, root, ratio, alternating-series, geometric, or rearrangement criteria.
- `sub_uniform_convergence_mtest` — **Uniform convergence and the Weierstrass M-test**: Produce a summable uniform majorant and transfer continuity or bounds to the resulting series.
- `sub_power_series_radius` — **Power-series radius arguments**: Compare coefficient growth and apply Cauchy-Hadamard or radius-of-convergence comparison results.
- `family_integral_calculus` — **Integral-calculus arguments**: A broad integration family covering the fundamental theorem, structural integral identities, transformations, and Riemann-sum methods.
- `sub_fundamental_theorem_calculus` — **Fundamental Theorem of Calculus**: Convert derivatives into integral increments or differentiate parameterized integrals.
- `sub_integral_structure` — **Structural properties of the integral**: Use linearity, interval additivity, monotonicity, constant-integral formulas, and integral norm inequalities.
- `sub_integration_transformations` — **Integration by parts and substitution**: Verify regularity and integrability hypotheses and then apply integration by parts or change of variables.
- `sub_partition_refinement` — **Partition and refinement arguments**: Control meshes and subintervals, construct common refinements, and decompose coarse partitions into fine pieces.
- `sub_riemann_modulus_control` — **Modulus-of-continuity control of Riemann sums**: Control tag changes using a modulus of continuity and sum local errors to prove convergence and partition independence.
- `family_reindexing_telescoping` — **Reindexing and telescoping sums**: Reindex sums under bijections or fibers and cancel consecutive terms so only boundary contributions remain.
- `family_induction_well_ordering` — **Induction, recurrence, and well-ordering**: Use induction, strengthened hypotheses, recurrence, least witnesses, or minimal counterexamples over the natural numbers.
- `family_structural_foundations` — **Cardinality, embeddings, and completion**: Use embeddings and cardinal comparisons or construct complete ordered structures from dense substructures and cuts.
- `sub_ordered_field_constructions` — **Ordered-field structure and canonical constructions**: Use ordered-field operations, canonical witnesses, Archimedeanness, completeness, and rational cuts in structural arguments about the reals.
- `sub_cardinality_embeddings` — **Cardinality and embedding arguments**: Use injections, diagonalization, Cantor's theorem, interval cardinality, and Cantor-Schroeder-Bernstein.
- `family_variational_linear_algebra` — **Variational and linear-algebraic methods**: Optimization and geometric methods based on convexity, orthogonality, projections, spectra, and structured parameter spaces.
- `sub_convexity_variational` — **Convexity and variational arguments**: Use Jensen's inequality, convex combinations, first-order optimality, or comparison with feasible competitors.
- `sub_orthogonality_spectral` — **Orthogonality, projection, and spectral arguments**: Use orthogonal expansions, Pythagoras, Parseval, normal equations, Rayleigh quotients, and eigenvector principles.
- `sub_structured_parameters` — **Sparsity, low-rank structure, and norm duality**: Exploit support, cone, rank, or singular-space decompositions together with dual norms and restricted geometric conditions.
- `family_metric_entropy` — **Metric entropy, covering, and packing methods**: Discretize continuous classes by finite nets or construct well-separated finite subsets using packing methods.
- `sub_covering_volumetric` — **Covering-net and volumetric arguments**: Replace continuous suprema by maxima over finite epsilon-nets and bound net sizes through packing and volume comparison.
- `sub_probabilistic_packing` — **Probabilistic method and packing constructions**: Randomly generate nets, codes, sparse vectors, or approximants and prove that a suitable deterministic construction exists.
- `family_probability_information` — **Probability, concentration, and information methods**: Probabilistic proof methods based on exponential moments, tails, independence, union bounds, and information-theoretic reductions.
- `sub_exponential_concentration` — **Exponential-moment and concentration arguments**: Apply exponential Markov inequalities, control moment-generating functions, and optimize parameters to derive tail bounds.
- `sub_tail_integration` — **Tail integration and moment estimates**: Convert moments into tail integrals, insert probability bounds, and estimate the resulting integrals.
- `sub_independence_tensorization` — **Independence, tensorization, and union bounds**: Factor quantities using independence, tensorize information, and upgrade pointwise bounds to simultaneous bounds by a union bound.
- `sub_testing_information` — **Testing and information-theoretic reductions**: Reduce estimation to hypothesis testing and control testing error using divergence or mutual-information inequalities.

---

## lemma_2_7_8 — Lemma 2.7.8 (Centering)

Dataset: `high_dimensional_probability`

### Input statement

Lemma 2.7.8 (Centering). Any subgaussian random variable X satisfies
                                    ∥X − E X∥ψ2 ≤ C∥X∥ψ2 .

### Task

Explain the proof strategy and give a proof plan. Identify the main mathematical methods used.

### Control output

Let the subgaussian norm be
\[
\|Y\|_{\psi_2}:=\inf\left\{t>0:\ \mathbb E\exp\!\left(\frac{Y^2}{t^2}\right)\le 2\right\}.
\]

Set \(K=\|X\|_{\psi_2}\). More precisely, take any \(t>K\) such that
\[
\mathbb E e^{X^2/t^2}\le 2.
\]
By Jensen’s inequality,
\[
e^{(\mathbb EX)^2/t^2}
\le \mathbb E e^{X^2/t^2}
\le 2.
\]
Using \((X-\mathbb EX)^2\le 2X^2+2(\mathbb EX)^2\), we obtain
\[
\begin{aligned}
\mathbb E\exp\left(\frac{(X-\mathbb EX)^2}{4t^2}\right)
&\le
\exp\left(\frac{(\mathbb EX)^2}{2t^2}\right)
\mathbb E\exp\left(\frac{X^2}{2t^2}\right)\\
&\le
\left(e^{(\mathbb EX)^2/t^2}\right)^{1/2}
\left(\mathbb E e^{X^2/t^2}\right)^{1/2}\\
&\le \sqrt2\,\sqrt2=2,
\end{aligned}
\]
where the second factor is bounded using Cauchy–Schwarz (or concavity of \(u^{1/2}\)).

Thus \(2t\) is admissible in the definition of \(\|X-\mathbb EX\|_{\psi_2}\), so
\[
\|X-\mathbb EX\|_{\psi_2}\le 2t.
\]
Letting \(t\downarrow K\) gives
\[
\boxed{\|X-\mathbb EX\|_{\psi_2}\le 2\|X\|_{\psi_2}}.
\]
Hence the theorem holds with the absolute constant \(C=2\).

### Library-RAG output

Let the subgaussian norm be
\[
\|Y\|_{\psi_2}:=\inf\left\{t>0:\ \mathbb E\exp\!\left(\frac{Y^2}{t^2}\right)\le 2\right\}.
\]

Set \(K=\|X\|_{\psi_2}\). More precisely, take any \(t>K\) such that
\[
\mathbb E e^{X^2/t^2}\le 2.
\]
By Jensen’s inequality,
\[
e^{(\mathbb EX)^2/t^2}
\le \mathbb E e^{X^2/t^2}
\le 2.
\]
Using \((X-\mathbb EX)^2\le 2X^2+2(\mathbb EX)^2\), we obtain
\[
\begin{aligned}
\mathbb E\exp\left(\frac{(X-\mathbb EX)^2}{4t^2}\right)
&\le
\exp\left(\frac{(\mathbb EX)^2}{2t^2}\right)
\mathbb E\exp\left(\frac{X^2}{2t^2}\right)\\
&\le
\left(e^{(\mathbb EX)^2/t^2}\right)^{1/2}
\left(\mathbb E e^{X^2/t^2}\right)^{1/2}\\
&\le \sqrt2\,\sqrt2=2,
\end{aligned}
\]
where the second factor is bounded using Cauchy–Schwarz (or concavity of \(u^{1/2}\)).

Thus \(2t\) is admissible in the definition of \(\|X-\mathbb EX\|_{\psi_2}\), so
\[
\|X-\mathbb EX\|_{\psi_2}\le 2t.
\]
Letting \(t\downarrow K\) gives
\[
\boxed{\|X-\mathbb EX\|_{\psi_2}\le 2\|X\|_{\psi_2}}.
\]
Hence the theorem holds with the absolute constant \(C=2\).

### Retrieved strategy nodes

- `family_definitional_reformulation` — **Definitional unfolding and equivalent reformulation**: Convert abstract statements into explicit definitions, quantified conditions, or standard equivalent formulations.
- `sub_definitional_unfolding` — **Definitional unfolding**: Expand boundedness, inclusion, extrema, Riemann sums, and auxiliary constructions into their defining statements.
- `sub_metric_filter_characterization` — **Metric and filter characterizations**: Replace continuity, convergence, Cauchy conditions, and eventual properties by neighborhood, filter, or epsilon-based criteria.
- `sub_canonical_rewriting` — **Canonical rewriting**: Rewrite abstract distances, norms, slopes, interval interiors, and formal-series expressions in concrete canonical forms.
- `sub_set_extensionality` — **Set identities and extensionality**: Prove set equalities by extensionality or mutual inclusion and simplify Boolean set operations.
- `family_normalization_symmetry` — **Normalization, invariance, and symmetry**: Translate, rescale, whiten, permute, or otherwise transform a problem to a canonical case and transfer the conclusion back.
- `family_standard_theorem_reduction` — **Reduction to a standard theorem**: Modify domains and regularity hypotheses so that a known theorem applies directly.
- `sub_regularity_transfer` — **Restriction, extension, and transfer of regularity**: Restrict or extend functions and transfer continuity, differentiability, or integrability between compatible domains.
- `family_logical_reasoning` — **Logical decomposition, cases, and contradiction**: Split logical, order, endpoint, degeneracy, or parameter cases and use contradiction or contraposition to eliminate alternatives.
- `family_explicit_construction` — **Explicit construction and parameter choice**: Construct witnesses, sequences, partitions, comparison points, thresholds, or auxiliary objects and tune free parameters.
- `family_algebra_order_norm` — **Algebraic, order, and norm estimates**: Combine algebraic rearrangement and order reasoning with norm inequalities and duality estimates.
- `sub_elementary_algebra_order` — **Elementary algebra and order reasoning**: Prove positivity or nonvanishing, clear denominators, cancel factors, rearrange identities, and combine inequalities.
- `family_topology_compactness_connectedness` — **Compactness and connectedness methods**: Use compactness for boundedness, extrema, subsequences, and uniform continuity, and connectedness for intermediate values and zeros.
- `sub_compactness` — **Compactness arguments**: Apply compactness of intervals or images to obtain boundedness, attained extrema, uniform continuity, or convergent subsequences.
- `sub_intermediate_value` — **Intermediate Value Theorem**: Use continuity and endpoint value information to produce an intermediate value or interior zero.
- `family_extremal_order` — **Supremum, infimum, and extremal arguments**: Control quantities through suprema, infima, extremal points, or attained optimizers.
- `sub_order_completeness` — **Suprema, infima, and order completeness**: Apply least-upper-bound and greatest-lower-bound properties to bounded sets, images, limsups, and moduli of continuity.
- `family_limits_completeness` — **Limit, sequence, and completeness methods**: Use epsilon or filter formulations, limit laws, squeezing, completeness, subsequences, and limsup-liminf criteria.
- `sub_limit_laws_squeezing` — **Limit laws, squeezing, and uniqueness**: Compose limits, pass bounds to limits, squeeze between convergent quantities, and use uniqueness to identify limits.
- `sub_sequence_completeness` — **Sequence and completeness methods**: Use epsilon-N arguments, Cauchy completeness, subsequences, and sequences approaching a point.
- `sub_monotone_limsup_subsequence` — **Monotone sequences, limsup, and subsequences**: Use monotone convergence, limsup-liminf characterizations, and extraction of convergent subsequences.
- `family_differential_calculus` — **Differential-calculus arguments**: A broad calculus family covering differentiability criteria, derivative rules, mean-value principles, derivative signs, and Taylor expansion.
- `sub_difference_quotient` — **Difference-quotient characterization of differentiability**: Express differentiability as convergence of slopes on a punctured neighborhood.
- `sub_derivative_rules` — **Differential calculus rules**: Apply chain, composition, and related closure rules for differentiable functions.
- `sub_mean_value_theorems` — **Fermat, Rolle, and Mean Value Theorems**: Convert extrema or endpoint equalities into derivative information and represent increments by intermediate derivatives.
- `sub_derivative_sign` — **Derivative-sign arguments**: Infer monotonicity, constancy, or local extrema from first- or second-derivative sign information.
- `sub_taylor_remainder` — **Taylor expansion with remainder**: Apply finite Taylor expansion with a controlled remainder and normalize the resulting coefficients.
- `family_error_decomposition` — **Error decomposition and balancing**: Split a total error into analyzable components and choose parameters that balance the dominant contributions.
- `sub_triangle_error_estimates` — **Triangle-inequality and error-decomposition estimates**: Separate dominant and error terms and control them with triangle and reverse-triangle inequalities.
- `sub_approximation_archimedean` — **Approximation and Archimedean error control**: Choose dense approximants and then select an index making the uniform approximation error smaller than a prescribed tolerance.
- `family_comparison_domination` — **Comparison, domination, and squeezing**: Bound complicated quantities by simpler majorants and transfer those bounds through sums, integrals, limits, and suprema.
- `family_series_convergence` — **Series and uniform-convergence methods**: A broad family covering summability tests, uniform convergence, and power-series convergence radii.
- `sub_series_tests` — **Series comparison and convergence tests**: Use comparison, term, root, ratio, alternating-series, geometric, or rearrangement criteria.
- `sub_uniform_convergence_mtest` — **Uniform convergence and the Weierstrass M-test**: Produce a summable uniform majorant and transfer continuity or bounds to the resulting series.
- `sub_power_series_radius` — **Power-series radius arguments**: Compare coefficient growth and apply Cauchy-Hadamard or radius-of-convergence comparison results.
- `family_integral_calculus` — **Integral-calculus arguments**: A broad integration family covering the fundamental theorem, structural integral identities, transformations, and Riemann-sum methods.
- `sub_fundamental_theorem_calculus` — **Fundamental Theorem of Calculus**: Convert derivatives into integral increments or differentiate parameterized integrals.
- `sub_integral_structure` — **Structural properties of the integral**: Use linearity, interval additivity, monotonicity, constant-integral formulas, and integral norm inequalities.
- `sub_integration_transformations` — **Integration by parts and substitution**: Verify regularity and integrability hypotheses and then apply integration by parts or change of variables.
- `sub_partition_refinement` — **Partition and refinement arguments**: Control meshes and subintervals, construct common refinements, and decompose coarse partitions into fine pieces.
- `sub_riemann_modulus_control` — **Modulus-of-continuity control of Riemann sums**: Control tag changes using a modulus of continuity and sum local errors to prove convergence and partition independence.
- `family_reindexing_telescoping` — **Reindexing and telescoping sums**: Reindex sums under bijections or fibers and cancel consecutive terms so only boundary contributions remain.
- `family_induction_well_ordering` — **Induction, recurrence, and well-ordering**: Use induction, strengthened hypotheses, recurrence, least witnesses, or minimal counterexamples over the natural numbers.
- `family_structural_foundations` — **Cardinality, embeddings, and completion**: Use embeddings and cardinal comparisons or construct complete ordered structures from dense substructures and cuts.
- `sub_ordered_field_constructions` — **Ordered-field structure and canonical constructions**: Use ordered-field operations, canonical witnesses, Archimedeanness, completeness, and rational cuts in structural arguments about the reals.
- `sub_cardinality_embeddings` — **Cardinality and embedding arguments**: Use injections, diagonalization, Cantor's theorem, interval cardinality, and Cantor-Schroeder-Bernstein.
- `family_variational_linear_algebra` — **Variational and linear-algebraic methods**: Optimization and geometric methods based on convexity, orthogonality, projections, spectra, and structured parameter spaces.
- `sub_convexity_variational` — **Convexity and variational arguments**: Use Jensen's inequality, convex combinations, first-order optimality, or comparison with feasible competitors.
- `sub_orthogonality_spectral` — **Orthogonality, projection, and spectral arguments**: Use orthogonal expansions, Pythagoras, Parseval, normal equations, Rayleigh quotients, and eigenvector principles.
- `sub_structured_parameters` — **Sparsity, low-rank structure, and norm duality**: Exploit support, cone, rank, or singular-space decompositions together with dual norms and restricted geometric conditions.
- `family_metric_entropy` — **Metric entropy, covering, and packing methods**: Discretize continuous classes by finite nets or construct well-separated finite subsets using packing methods.
- `sub_covering_volumetric` — **Covering-net and volumetric arguments**: Replace continuous suprema by maxima over finite epsilon-nets and bound net sizes through packing and volume comparison.
- `sub_probabilistic_packing` — **Probabilistic method and packing constructions**: Randomly generate nets, codes, sparse vectors, or approximants and prove that a suitable deterministic construction exists.
- `family_probability_information` — **Probability, concentration, and information methods**: Probabilistic proof methods based on exponential moments, tails, independence, union bounds, and information-theoretic reductions.
- `sub_exponential_concentration` — **Exponential-moment and concentration arguments**: Apply exponential Markov inequalities, control moment-generating functions, and optimize parameters to derive tail bounds.
- `sub_tail_integration` — **Tail integration and moment estimates**: Convert moments into tail integrals, insert probability bounds, and estimate the resulting integrals.
- `sub_independence_tensorization` — **Independence, tensorization, and union bounds**: Factor quantities using independence, tensorize information, and upgrade pointwise bounds to simultaneous bounds by a union bound.
- `sub_testing_information` — **Testing and information-theoretic reductions**: Reduce estimation to hypothesis testing and control testing error using divergence or mutual-information inequalities.

---
