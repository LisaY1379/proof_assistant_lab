# Control vs Library-RAG Batch Experiment

## Metadata

- **created_at**: `2026-09-25T06:05:29.101853+00:00`
- **input_path**: `data/test/high_dimensional_probability/test_01/data.json`
- **input_count**: `1`
- **conditions**: `['control', 'library_rag']`
- **model**: `gpt-5.6-sol`
- **temperature**: `1.0`
- **reasoning_effort**: `high`
- **max_completion_tokens**: `4000`
- **strategy_graph**: `data/train/general/strategy_hierarchy.json`

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

Let \(\|\cdot\|\) denote the operator norm. Throughout, \(c,C>0\) denote universal constants whose values may change from line to line.

We use the following standard consequences of subgaussianity:

1. If \(Z_i\) are independent, mean-zero, and \(\|Z_i\|_{\psi_2}\le K\), then
   \[
   \mathbb E\exp\left(s\sum_i v_iZ_i\right)
   \le \exp\big(C s^2K^2\|v\|_2^2\big).
   \tag{1}
   \]
2. If \(\|Z\|_{\psi_2}\le K\), then
   \[
   \|Z^2-\mathbb EZ^2\|_{\psi_1}\le CK^2.
   \tag{2}
   \]
   Consequently, for independent centered subexponential \(Y_i\) with
   \(\|Y_i\|_{\psi_1}\le K^2\),
   \[
   \mathbb E\exp\left(\lambda\sum_i a_iY_i\right)
   \le \exp\left(C\lambda^2K^4\sum_i a_i^2\right)
   \tag{3}
   \]
   whenever
   \[
   |\lambda|\le \frac{c}{K^2\max_i|a_i|}.
   \]

### 1. Reduction to the symmetric case

Set
\[
B=\frac{A+A^T}{2}.
\]
Then \(x^TAx=x^TBx\) for every \(x\), and
\[
\|B\|\le \|A\|,\qquad \|B\|_F\le \|A\|_F.
\]
Thus it suffices to prove the result when \(A\) is symmetric.

Write
\[
X^TAX-\mathbb EX^TAX=D+S,
\]
where
\[
D=\sum_{i=1}^n a_{ii}\big(X_i^2-\mathbb EX_i^2\big),
\qquad
S=\sum_{i\ne j}a_{ij}X_iX_j.
\]
Independence and mean-zero imply \(\mathbb ES=0\).

### 2. The diagonal part

By (2)–(3),
\[
\mathbb E e^{\lambda D}
\le
\exp\left(C\lambda^2K^4\sum_i a_{ii}^2\right)
\le
\exp\left(C\lambda^2K^4\|A\|_F^2\right)
\tag{4}
\]
provided
\[
|\lambda|
\le \frac{c}{K^2\max_i|a_{ii}|}
\le \frac{c}{K^2\|A\|}.
\tag{5}
\]

### 3. The off-diagonal part

We prove
\[
\mathbb E e^{\lambda S}
\le
\exp\left(C\lambda^2K^4\|A\|_F^2\right)
\tag{6}
\]
whenever
\[
|\lambda|\le \frac{c}{K^2\|A\|}.
\tag{7}
\]

Let \(\delta_1,\dots,\delta_n\) be independent Bernoulli random variables with
\(\mathbb P(\delta_i=1)=1/2\), independent of \(X\). Define
\[
S_\delta=\sum_{i,j}\delta_i(1-\delta_j)a_{ij}X_iX_j.
\]
Since \(\mathbb E_\delta[\delta_i(1-\delta_j)]=1/4\) for \(i\ne j\),
\[
S=4\mathbb E_\delta S_\delta.
\]
Convexity of the exponential gives
\[
\mathbb Ee^{\lambda S}
\le
\mathbb E_\delta\mathbb E_Xe^{4\lambda S_\delta}.
\tag{8}
\]

Fix \(\delta\), and let
\[
\Lambda=\{i:\delta_i=1\}.
\]
Then
\[
S_\delta=X_\Lambda^TBX_{\Lambda^c},
\]
where \(B=A_{\Lambda,\Lambda^c}\) is the corresponding rectangular block.

Conditioning on \(X_{\Lambda^c}\) and using (1),
\[
\mathbb E_{X_\Lambda}
 \exp\big(4\lambda X_\Lambda^TBX_{\Lambda^c}\big)
\le
\exp\left(C\lambda^2K^2\|BX_{\Lambda^c}\|_2^2\right).
\tag{9}
\]

We next bound the expectation of the right-hand side. For \(\eta\ge0\) and a standard Gaussian vector \(g\),
\[
e^{\eta\|z\|_2^2}
=
\mathbb E_g e^{\sqrt{2\eta}\langle g,z\rangle}.
\]
Using this identity and then (1),
\[
\begin{aligned}
\mathbb E_Xe^{\eta\|BX\|_2^2}
&=\mathbb E_g\mathbb E_X
   e^{\sqrt{2\eta}\langle B^Tg,X\rangle}\\
&\le
\mathbb E_g
   e^{C\eta K^2\|B^Tg\|_2^2}.
\end{aligned}
\tag{10}
\]

For any matrix \(B\), the Gaussian quadratic-form calculation gives
\[
\mathbb E_g e^{\theta\|B^Tg\|_2^2}
\le
\exp\big(C\theta\|B\|_F^2\big)
\tag{11}
\]
provided \(\theta\|B\|^2\le c\). Indeed, writing \(s_k\) for the singular values of \(B\), the left side equals
\[
\prod_k(1-2\theta s_k^2)^{-1/2}.
\]

Taking \(\eta=C\lambda^2K^2\) in (10) therefore gives
\[
\mathbb E_X e^{C\lambda^2K^2\|BX\|_2^2}
\le
\exp\left(C\lambda^2K^4\|B\|_F^2\right)
\tag{12}
\]
provided
\[
|\lambda|\le \frac{c}{K^2\|B\|}.
\]
Since \(B=P_\Lambda AP_{\Lambda^c}\),
\[
\|B\|\le \|A\|,
\qquad
\|B\|_F\le \|A\|_F.
\]
Combining (8), (9), and (12) proves (6).

### 4. MGF of the full quadratic form

Let
\[
Y=X^TAX-\mathbb EX^TAX=D+S.
\]
The variables \(D\) and \(S\) need not be independent, but Cauchy–Schwarz, together with (4) and (6), yields
\[
\begin{aligned}
\mathbb Ee^{\lambda Y}
&\le
\big(\mathbb Ee^{2\lambda D}\big)^{1/2}
\big(\mathbb Ee^{2\lambda S}\big)^{1/2}\\
&\le
\exp\left(C\lambda^2K^4\|A\|_F^2\right)
\end{aligned}
\tag{13}
\]
whenever
\[
|\lambda|\le \frac{c}{K^2\|A\|}.
\tag{14}
\]

For \(0\le\lambda\le c/(K^2\|A\|)\), Chernoff’s bound gives
\[
\mathbb P(Y\ge t)
\le
\exp\left(
-\lambda t+C\lambda^2K^4\|A\|_F^2
\right).
\]
Optimizing over the permitted \(\lambda\), namely taking \(\lambda\) comparable to
\[
\min\left\{
\frac{t}{K^4\|A\|_F^2},
\frac{1}{K^2\|A\|}
\right\},
\]
gives
\[
\mathbb P(Y\ge t)
\le
\exp\left[
-c\min\left(
\frac{t^2}{K^4\|A\|_F^2},
\frac{t}{K^2\|A\|}
\right)
\right].
\]
Applying the same argument to \(-Y\) and taking a union bound proves
\[
\boxed{
\mathbb P\left(
\left|X^TAX-\mathbb EX^TAX\right|\ge t
\right)
\le
2\exp\left[
-c\min\left(
\frac{t^2}{K^4\|A\|_F^2},
\frac{t}{K^2\|A\|}
\right)
\right].
}
\]

This is the Hanson–Wright inequality.

### Library-RAG output

Let \(\|\cdot\|\) denote the operator norm. Throughout, \(c,C>0\) denote universal constants whose values may change from line to line.

We use the following standard consequences of subgaussianity:

1. If \(Z_i\) are independent, mean-zero, and \(\|Z_i\|_{\psi_2}\le K\), then
   \[
   \mathbb E\exp\left(s\sum_i v_iZ_i\right)
   \le \exp\big(C s^2K^2\|v\|_2^2\big).
   \tag{1}
   \]
Annotation: This linear-form MGF bound follows by factoring the exponential moment across independent coordinates.

2. If \(\|Z\|_{\psi_2}\le K\), then
   \[
   \|Z^2-\mathbb EZ^2\|_{\psi_1}\le CK^2.
   \tag{2}
   \]
   Consequently, for independent centered subexponential \(Y_i\) with
   \(\|Y_i\|_{\psi_1}\le K^2\),
   \[
   \mathbb E\exp\left(\lambda\sum_i a_iY_i\right)
   \le \exp\left(C\lambda^2K^4\sum_i a_i^2\right)
   \tag{3}
   \]
   whenever
   \[
   |\lambda|\le \frac{c}{K^2\max_i|a_i|}.
   \]
Annotation: This passage converts subgaussian control into a local exponential-moment bound for weighted subexponential sums.

### 1. Reduction to the symmetric case

Set
\[
B=\frac{A+A^T}{2}.
\]
Then \(x^TAx=x^TBx\) for every \(x\), and
\[
\|B\|\le \|A\|,\qquad \|B\|_F\le \|A\|_F.
\]
Thus it suffices to prove the result when \(A\) is symmetric.
Annotation: The quadratic form is canonically rewritten using the symmetric part of \(A\) while preserving the required norm bounds.

Write
\[
X^TAX-\mathbb EX^TAX=D+S,
\]
where
\[
D=\sum_{i=1}^n a_{ii}\big(X_i^2-\mathbb EX_i^2\big),
\qquad
S=\sum_{i\ne j}a_{ij}X_iX_j.
\]
Independence and mean-zero imply \(\mathbb ES=0\).
Annotation: This critical decomposition separates the directly subexponential diagonal terms from the dependent bilinear terms, a strategy absent from the retrieved library.

### 2. The diagonal part

[CONTROL_SECTION: p1 | diagonal MGF parameter range]
By (2)–(3),
\[
\mathbb E e^{\lambda D}
\le
\exp\left(C\lambda^2K^4\sum_i a_{ii}^2\right)
\le
\exp\left(C\lambda^2K^4\|A\|_F^2\right)
\tag{4}
\]
provided
\[
|\lambda|
\le \frac{c}{K^2\max_i|a_{ii}|}
\le \frac{c}{K^2\|A\|}.
\tag{5}
\]
Annotation: The diagonal contribution is controlled by applying the weighted subexponential MGF bound in its permitted parameter range.
[/CONTROL_SECTION]
[RAG_OMITTED_SECTION: p1 | diagonal MGF parameter range]
By (2)–(3),
\[
\mathbb E e^{\lambda D}
\le
\exp\left(C\lambda^2K^4\sum_i a_{ii}^2\right)
\le
\exp\left(C\lambda^2K^4\|A\|_F^2\right)
\tag{4}
\]
whenever
\[
|\lambda|\le \frac{c}{K^2\max_i|a_{ii}|}.
\]
Since \(\max_i|a_{ii}|\le \|A\|\), it is sufficient to impose the smaller range
\[
|\lambda|\le \frac{c}{K^2\|A\|}.
\tag{5}
\]
[/RAG_OMITTED_SECTION]

### 3. The off-diagonal part

We prove
\[
\mathbb E e^{\lambda S}
\le
\exp\left(C\lambda^2K^4\|A\|_F^2\right)
\tag{6}
\]
whenever
\[
|\lambda|\le \frac{c}{K^2\|A\|}.
\tag{7}
\]

[CONTROL_SECTION: p2 | Random-partition decoupling of off-diagonal interactions]
Let \(\delta_1,\dots,\delta_n\) be independent Bernoulli random variables with
\(\mathbb P(\delta_i=1)=1/2\), independent of \(X\). Define
\[
S_\delta=\sum_{i,j}\delta_i(1-\delta_j)a_{ij}X_iX_j.
\]
Since \(\mathbb E_\delta[\delta_i(1-\delta_j)]=1/4\) for \(i\ne j\),
\[
S=4\mathbb E_\delta S_\delta.
\]
Annotation: The random cut converts the coupled off-diagonal quadratic form into an average of bilinear forms on disjoint coordinate sets, a critical decoupling strategy absent from the library.
[/CONTROL_SECTION]
[RAG_ELABORATED_SECTION: p2 | Random-partition decoupling of off-diagonal interactions]
Let \(\delta_1,\dots,\delta_n\) be independent Bernoulli random variables with
\(\mathbb P(\delta_i=1)=1/2\), independent of \(X\). Define
\[
S_\delta=\sum_{i,j}\delta_i(1-\delta_j)a_{ij}X_iX_j.
\]
For \(i=j\), \(\delta_i(1-\delta_i)=0\), while for \(i\ne j\), independence gives
\[
\mathbb E_\delta\big[\delta_i(1-\delta_j)\big]
=\mathbb E\delta_i\,\mathbb E(1-\delta_j)=\frac14.
\]
Therefore, pointwise in \(X\),
\[
\mathbb E_\delta S_\delta
=\frac14\sum_{i\ne j}a_{ij}X_iX_j
=\frac14S,
\]
and hence
\[
S=4\mathbb E_\delta S_\delta.
\]
For each fixed realization of \(\delta\), the two coordinate sets selected by
\(\delta_i=1\) and \(\delta_j=0\) are disjoint; the corresponding subvectors of
\(X\) are therefore independent.
[/RAG_ELABORATED_SECTION]

Convexity of the exponential gives
\[
\mathbb Ee^{\lambda S}
\le
\mathbb E_\delta\mathbb E_Xe^{4\lambda S_\delta}.
\tag{8}
\]
Annotation: Jensen’s inequality moves the random-partition average outside the convex exponential.

Fix \(\delta\), and let
\[
\Lambda=\{i:\delta_i=1\}.
\]
Then
\[
S_\delta=X_\Lambda^TBX_{\Lambda^c},
\]
where \(B=A_{\Lambda,\Lambda^c}\) is the corresponding rectangular block.

Conditioning on \(X_{\Lambda^c}\) and using (1),
\[
\mathbb E_{X_\Lambda}
 \exp\big(4\lambda X_\Lambda^TBX_{\Lambda^c}\big)
\le
\exp\left(C\lambda^2K^2\|BX_{\Lambda^c}\|_2^2\right).
\tag{9}
\]
Annotation: Conditioning isolates an independent coordinate block so that the tensorized subgaussian linear-form MGF bound applies.

[CONTROL_SECTION: p2 | Gaussian linearization of a squared Euclidean norm]
We next bound the expectation of the right-hand side. For \(\eta\ge0\) and a standard Gaussian vector \(g\),
\[
e^{\eta\|z\|_2^2}
=
\mathbb E_g e^{\sqrt{2\eta}\langle g,z\rangle}.
\]
Using this identity and then (1),
\[
\begin{aligned}
\mathbb E_Xe^{\eta\|BX\|_2^2}
&=\mathbb E_g\mathbb E_X
   e^{\sqrt{2\eta}\langle B^Tg,X\rangle}\\
&\le
\mathbb E_g
   e^{C\eta K^2\|B^Tg\|_2^2}.
\end{aligned}
\tag{10}
\]
Annotation: The auxiliary Gaussian identity linearizes the squared norm and is the critical bridge to a tractable Gaussian quadratic MGF, but it is absent from the library.
[/CONTROL_SECTION]
[RAG_ELABORATED_SECTION: p2 | Gaussian linearization of a squared Euclidean norm]
We next bound the expectation of the right-hand side. Let \(g\) be a standard Gaussian vector of the appropriate dimension, independent of \(X\). For each fixed \(z\),
\[
\langle g,z\rangle\sim N(0,\|z\|_2^2),
\]
so the Gaussian MGF formula gives, for \(\eta\ge0\),
\[
\mathbb E_g e^{\sqrt{2\eta}\langle g,z\rangle}
=
\exp\left(\frac{2\eta}{2}\|z\|_2^2\right)
=e^{\eta\|z\|_2^2}.
\]
Applying this identity with \(z=BX\), and then using Tonelli’s theorem and the
linear-form estimate (1) conditionally on \(g\), yields
\[
\begin{aligned}
\mathbb E_Xe^{\eta\|BX\|_2^2}
&=\mathbb E_X\mathbb E_g
   e^{\sqrt{2\eta}\langle g,BX\rangle}\\
&=\mathbb E_g\mathbb E_X
   e^{\sqrt{2\eta}\langle B^Tg,X\rangle}\\
&\le
\mathbb E_g
   e^{C\eta K^2\|B^Tg\|_2^2}.
\end{aligned}
\tag{10}
\]
[/RAG_ELABORATED_SECTION]

[CONTROL_SECTION: p2 | Singular-value evaluation of a Gaussian quadratic MGF]
For any matrix \(B\), the Gaussian quadratic-form calculation gives
\[
\mathbb E_g e^{\theta\|B^Tg\|_2^2}
\le
\exp\big(C\theta\|B\|_F^2\big)
\tag{11}
\]
provided \(\theta\|B\|^2\le c\). Indeed, writing \(s_k\) for the singular values of \(B\), the left side equals
\[
\prod_k(1-2\theta s_k^2)^{-1/2}.
\]
Annotation: Diagonalizing through singular values supplies both the Frobenius-norm exponent and operator-norm admissibility condition, a specialized strategy not represented in the library.
[/CONTROL_SECTION]
[RAG_ELABORATED_SECTION: p2 | Singular-value evaluation of a Gaussian quadratic MGF]
For any matrix \(B\) and \(\theta\ge0\), let \(s_k\) denote the singular values of
\(B\). By the singular value decomposition and rotational invariance of the
standard Gaussian distribution,
\[
\|B^Tg\|_2^2\stackrel{d}{=}\sum_k s_k^2g_k^2,
\]
where the \(g_k\) are independent \(N(0,1)\) variables. Thus, provided
\(2\theta s_k^2<1\) for every \(k\),
\[
\mathbb E_g e^{\theta\|B^Tg\|_2^2}
=
\prod_k\mathbb E e^{\theta s_k^2g_k^2}
=
\prod_k(1-2\theta s_k^2)^{-1/2}.
\]
If \(\theta\|B\|^2\le c\) for a sufficiently small universal \(c\), then
\(2\theta s_k^2\le 1/2\). Using
\(-\log(1-u)\le Cu\) for \(0\le u\le1/2\), we obtain
\[
\begin{aligned}
\log\mathbb E_g e^{\theta\|B^Tg\|_2^2}
&=-\frac12\sum_k\log(1-2\theta s_k^2)\\
&\le C\theta\sum_k s_k^2
=C\theta\|B\|_F^2.
\end{aligned}
\]
Exponentiating gives
\[
\mathbb E_g e^{\theta\|B^Tg\|_2^2}
\le
\exp\big(C\theta\|B\|_F^2\big).
\tag{11}
\]
[/RAG_ELABORATED_SECTION]

[CONTROL_SECTION: u1 | routine norm and parameter check]
Taking \(\eta=C\lambda^2K^2\) in (10) therefore gives
\[
\mathbb E_X e^{C\lambda^2K^2\|BX\|_2^2}
\le
\exp\left(C\lambda^2K^4\|B\|_F^2\right)
\tag{12}
\]
provided
\[
|\lambda|\le \frac{c}{K^2\|B\|}.
\]
Since \(B=P_\Lambda AP_{\Lambda^c}\),
\[
\|B\|\le \|A\|,
\qquad
\|B\|_F\le \|A\|_F.
\]
Combining (8), (9), and (12) proves (6).
[/CONTROL_SECTION]
[RAG_OMITTED_SECTION: u1 | routine norm and parameter check]
Applying (10)–(11) with \(\eta=C\lambda^2K^2\), and using
\(\|A_{\Lambda,\Lambda^c}\|\le\|A\|\) and
\(\|A_{\Lambda,\Lambda^c}\|_F\le\|A\|_F\), gives
\[
\mathbb E_X e^{C\lambda^2K^2\|BX\|_2^2}
\le
\exp\left(C\lambda^2K^4\|B\|_F^2\right)
\tag{12}
\]
uniformly for \(|\lambda|\le c/(K^2\|A\|)\). Together with (8)–(9), this proves (6).
[/RAG_OMITTED_SECTION]

### 4. MGF of the full quadratic form

Let
\[
Y=X^TAX-\mathbb EX^TAX=D+S.
\]
The variables \(D\) and \(S\) need not be independent, but Cauchy–Schwarz, together with (4) and (6), yields
\[
\begin{aligned}
\mathbb Ee^{\lambda Y}
&\le
\big(\mathbb Ee^{2\lambda D}\big)^{1/2}
\big(\mathbb Ee^{2\lambda S}\big)^{1/2}\\
&\le
\exp\left(C\lambda^2K^4\|A\|_F^2\right)
\end{aligned}
\tag{13}
\]
whenever
\[
|\lambda|\le \frac{c}{K^2\|A\|}.
\tag{14}
\]
Annotation: Cauchy–Schwarz combines the two component MGF estimates without requiring independence and produces an MGF bound for the full form.

For \(0\le\lambda\le c/(K^2\|A\|)\), Chernoff’s bound gives
\[
\mathbb P(Y\ge t)
\le
\exp\left(
-\lambda t+C\lambda^2K^4\|A\|_F^2
\right).
\]
Optimizing over the permitted \(\lambda\), namely taking \(\lambda\) comparable to
\[
\min\left\{
\frac{t}{K^4\|A\|_F^2},
\frac{1}{K^2\|A\|}
\right\},
\]
gives
\[
\mathbb P(Y\ge t)
\le
\exp\left[
-c\min\left(
\frac{t^2}{K^4\|A\|_F^2},
\frac{t}{K^2\|A\|}
\right)
\right].
\]
Annotation: Exponential Markov inequality followed by optimization of the MGF parameter yields the two-regime upper-tail bound.

Applying the same argument to \(-Y\) and taking a union bound proves
\[
\boxed{
\mathbb P\left(
\left|X^TAX-\mathbb EX^TAX\right|\ge t
\right)
\le
2\exp\left[
-c\min\left(
\frac{t^2}{K^4\|A\|_F^2},
\frac{t}{K^2\|A\|}
\right)
\right].
}
\]
Annotation: A union bound combines the upper and lower one-sided estimates into the stated two-sided inequality.

This is the Hanson–Wright inequality.

### Retrieved strategy nodes

- `sub_independence_tensorization` — **Independence, tensorization, and union bounds**: Factor quantities using independence, tensorize information, and upgrade pointwise bounds to simultaneous bounds by a union bound.
- `family_standard_theorem_reduction` — **Reduction to a standard theorem**: Modify domains and regularity hypotheses so that a known theorem applies directly.
- `sub_exponential_concentration` — **Exponential-moment and concentration arguments**: Apply exponential Markov inequalities, control moment-generating functions, and optimize parameters to derive tail bounds.
- `sub_convexity_variational` — **Convexity and variational arguments**: Use Jensen's inequality, convex combinations, first-order optimality, or comparison with feasible competitors.
- `sub_covering_volumetric` — **Covering-net and volumetric arguments**: Replace continuous suprema by maxima over finite epsilon-nets and bound net sizes through packing and volume comparison.
- `sub_partition_refinement` — **Partition and refinement arguments**: Control meshes and subintervals, construct common refinements, and decompose coarse partitions into fine pieces.
- `sub_testing_information` — **Testing and information-theoretic reductions**: Reduce estimation to hypothesis testing and control testing error using divergence or mutual-information inequalities.
- `sub_canonical_rewriting` — **Canonical rewriting**: Rewrite abstract distances, norms, slopes, interval interiors, and formal-series expressions in concrete canonical forms.
- `sub_riemann_modulus_control` — **Modulus-of-continuity control of Riemann sums**: Control tag changes using a modulus of continuity and sum local errors to prove convergence and partition independence.
- `family_probability_information` — **Probability, concentration, and information methods**: Probabilistic proof methods based on exponential moments, tails, independence, union bounds, and information-theoretic reductions.

---
