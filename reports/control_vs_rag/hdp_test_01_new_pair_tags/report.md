# Control vs Library-RAG Batch Experiment

## Metadata

- **created_at**: `2026-09-25T05:24:54.686172+00:00`
- **input_path**: `data/test/high_dimensional_probability/test_01/data.json`
- **input_count**: `5`
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

Let \(\|\cdot\|\) denote the operator norm. We use \(c,C>0\) for universal constants whose values may change.

### Basic subgaussian estimates

If \(Z\) is mean-zero and \(\|Z\|_{\psi_2}\le K\), then
\[
\mathbb E e^{sZ}\le e^{Cs^2K^2},\qquad s\in\mathbb R,
\]
and
\[
\|Z^2-\mathbb EZ^2\|_{\psi_1}\le CK^2.
\]
Consequently, if \(Z_i\) are independent, mean-zero, and \(\|Z_i\|_{\psi_1}\le K^2\), then
\[
\mathbb E\exp\left(\lambda\sum_i a_iZ_i\right)
 \le \exp\left(C\lambda^2K^4\sum_i a_i^2\right)
\]
whenever
\[
|\lambda|\le \frac{c}{K^2\max_i|a_i|}.
\tag{1}
\]

We will prove a similar moment generating function estimate for the off-diagonal part of the quadratic form.

## 1. Reduction to symmetric matrices

Set
\[
A_s=\frac{A+A^T}{2}.
\]
Since \(x^TAx=x^TA_sx\), it suffices to prove the result for \(A_s\). Moreover,
\[
\|A_s\|\le \|A\|,
\qquad
\|A_s\|_F\le \|A\|_F.
\]
Thus, from now on, assume that \(A\) is symmetric.

Write
\[
A=D+B,
\]
where \(D=\operatorname{diag}(a_{11},\ldots,a_{nn})\) and \(B=A-D\), so \(B\) has zero diagonal. Define
\[
U=\sum_{i=1}^n a_{ii}(X_i^2-\mathbb EX_i^2),
\qquad
V=X^TBX.
\]
Since \(B\) has zero diagonal and the coordinates of \(X\) are independent and mean-zero,
\[
\mathbb EV=0.
\]
Therefore
\[
X^TAX-\mathbb EX^TAX=U+V.
\tag{2}
\]

## 2. The diagonal part

Applying (1) to \(X_i^2-\mathbb EX_i^2\), we obtain
\[
\mathbb E e^{\lambda U}
 \le \exp\left(C\lambda^2K^4\|D\|_F^2\right)
\tag{3}
\]
whenever
\[
|\lambda|\le \frac{c}{K^2\max_i|a_{ii}|}.
\]
Because \(A\) is symmetric,
\[
\max_i|a_{ii}|\le \|A\|.
\tag{4}
\]

## 3. The off-diagonal part

We prove that
\[
\mathbb E e^{\lambda V}
 \le \exp\left(C\lambda^2K^4\|B\|_F^2\right)
\tag{5}
\]
provided
\[
|\lambda|\le \frac{c}{K^2\|B\|}.
\tag{6}
\]

Let \(\delta_1,\ldots,\delta_n\) be independent Bernoulli random variables with
\(\mathbb P(\delta_i=1)=1/2\), independent of \(X\). Define
\[
V_\delta
 =\sum_{i,j}\delta_i(1-\delta_j)b_{ij}X_iX_j.
\]
Since \(b_{ii}=0\),
\[
\mathbb E_\delta V_\delta=\frac14V.
\]
Jensen's inequality therefore gives, for any \(\lambda\in\mathbb R\),
\[
e^{\lambda V}
 =e^{4\lambda\mathbb E_\delta V_\delta}
 \le \mathbb E_\delta e^{4\lambda V_\delta}.
\tag{7}
\]

Fix \(\delta\), and let
\[
I=\{i:\delta_i=1\},\qquad J=I^c.
\]
If \(M=(b_{ij})_{i\in I,j\in J}\), then
\[
V_\delta=X_I^TMX_J.
\]
Conditioning on \(X_I\) and using the subgaussian moment generating function estimate for the independent coordinates of \(X_J\),
\[
\mathbb E_{X_J}
 \exp(4\lambda X_I^TMX_J)
 \le
 \exp\left(C\lambda^2K^2\|M^TX_I\|_2^2\right).
\tag{8}
\]

Set \(\alpha=C\lambda^2K^2\). Let \(g\) be a standard Gaussian vector in
\(\mathbb R^{|J|}\), independent of everything else. The Gaussian identity
\[
e^{\alpha\|z\|_2^2}
 =\mathbb E_g e^{\sqrt{2\alpha}\langle g,z\rangle}
\]
and another application of the subgaussian moment generating function estimate give
\[
\begin{aligned}
\mathbb E_{X_I}e^{\alpha\|M^TX_I\|_2^2}
&=\mathbb E_g\mathbb E_{X_I}
   e^{\sqrt{2\alpha}\langle Mg,X_I\rangle}\\
&\le \mathbb E_g e^{C\alpha K^2\|Mg\|_2^2}.
\end{aligned}
\tag{9}
\]

For a standard Gaussian vector \(g\), the singular-value decomposition of \(M\) shows that
\[
\mathbb E_g e^{\beta\|Mg\|_2^2}
 \le e^{C\beta\|M\|_F^2},
\qquad
\beta\|M\|^2\le c.
\tag{10}
\]
Indeed, if \(s_k\) are the singular values of \(M\), the left-hand side equals
\[
\prod_k(1-2\beta s_k^2)^{-1/2},
\]
which is bounded by \(\exp(C\beta\sum_k s_k^2)\) under the stated condition.

Taking \(\beta=C\alpha K^2=C\lambda^2K^4\) in (10), we conclude from (8)–(10) that
\[
\mathbb E_X e^{4\lambda V_\delta}
 \le \exp\left(C\lambda^2K^4\|M\|_F^2\right)
 \le \exp\left(C\lambda^2K^4\|B\|_F^2\right),
\]
provided
\[
|\lambda|\le \frac{c}{K^2\|B\|}.
\]
Averaging over \(\delta\) in (7) proves (5).

## 4. Moment generating function of the full quadratic form

By Cauchy–Schwarz and (2),
\[
\mathbb E e^{\lambda(U+V)}
 \le
 \left(\mathbb E e^{2\lambda U}\right)^{1/2}
 \left(\mathbb E e^{2\lambda V}\right)^{1/2}.
\]
Because
\[
\|B\|\le \|A\|+\|D\|\le 2\|A\|,
\qquad
\|D\|_F^2+\|B\|_F^2=\|A\|_F^2,
\]
estimates (3) and (5) yield
\[
\mathbb E
 \exp\left(\lambda\bigl(X^TAX-\mathbb EX^TAX\bigr)\right)
 \le
 \exp\left(C\lambda^2K^4\|A\|_F^2\right)
\tag{11}
\]
for
\[
|\lambda|\le \frac{c}{K^2\|A\|}.
\tag{12}
\]

## 5. Chernoff bound

Let
\[
Y=X^TAX-\mathbb EX^TAX.
\]
For \(0\le\lambda\le c/(K^2\|A\|)\), (11) gives
\[
\mathbb P(Y\ge t)
 \le
 \exp\left(-\lambda t+C\lambda^2K^4\|A\|_F^2\right).
\]
Choosing
\[
\lambda
 \asymp
 \min\left\{
 \frac{t}{K^4\|A\|_F^2},
 \frac{1}{K^2\|A\|}
 \right\}
\]
gives
\[
\mathbb P(Y\ge t)
 \le
 \exp\left[
 -c\min\left\{
 \frac{t^2}{K^4\|A\|_F^2},
 \frac{t}{K^2\|A\|}
 \right\}
 \right].
\]
Applying the same argument to \(-Y\) and taking the union of the two tails yields
\[
\boxed{
\mathbb P\left(
 \left|X^TAX-\mathbb EX^TAX\right|\ge t
\right)
\le
2\exp\left[
-c\min\left\{
\frac{t^2}{K^4\|A\|_F^2},
\frac{t}{K^2\|A\|}
\right\}
\right].
}
\]
This is the Hanson–Wright inequality.

### Library-RAG output

Let \(\|\cdot\|\) denote the operator norm, and let \(c,C>0\) denote universal constants that may change from line to line.

We use the following standard consequences of subgaussianity. If \(Z\) is mean-zero and \(\|Z\|_{\psi_2}\le K\), then
\[
\mathbb E e^{sZ}\le e^{Cs^2K^2},
\qquad
\|Z^2-\mathbb EZ^2\|_{\psi_1}\le CK^2.
\]
Hence, for independent centered subexponential variables \(Y_i\) with
\(\|Y_i\|_{\psi_1}\le CK^2\),
\[
\mathbb E\exp\left(\lambda\sum_i a_iY_i\right)
 \le \exp\left(C\lambda^2K^4\sum_i a_i^2\right)
\tag{1}
\]
whenever
\[
|\lambda|\le \frac{c}{K^2\max_i|a_i|}.
\]

[STRATEGY: sub_exponential_concentration | Exponential-moment and concentration arguments]
Estimate (1) is the standard Bernstein exponential-moment bound for sums of independent centered subexponential variables. We will derive a comparable bound for the off-diagonal quadratic form and then apply Chernoff’s inequality.
[/STRATEGY]

### Reduction and decomposition

Replace \(A\) by its symmetric part
\[
A_s=\frac{A+A^T}{2}.
\]
Since \(x^TAx=x^TA_sx\), this does not change the quadratic form, while
\[
\|A_s\|\le \|A\|,
\qquad
\|A_s\|_F\le \|A\|_F.
\]
We may therefore assume that \(A\) is symmetric.

Write \(A=D+B\), where \(D=\operatorname{diag}(a_{11},\dots,a_{nn})\) and \(B\) has zero diagonal. Then
\[
X^TAX-\mathbb EX^TAX=U+V,
\]
where
\[
U=\sum_i a_{ii}(X_i^2-\mathbb EX_i^2),
\qquad
V=X^TBX.
\tag{2}
\]
Because \(b_{ii}=0\) and the coordinates are independent and centered, \(\mathbb EV=0\).

For the diagonal part, (1) gives
\[
\mathbb E e^{\lambda U}
 \le \exp\left(C\lambda^2K^4\|D\|_F^2\right)
\tag{3}
\]
whenever
\[
|\lambda|\le \frac{c}{K^2\max_i|a_{ii}|}
 \le \frac{c}{K^2\|A\|}.
\tag{4}
\]

[STRATEGY: family_algebra_order_norm | Algebraic, order, and norm estimates]
The symmetric reduction and the decomposition into diagonal and off-diagonal parts preserve the required norm control. In particular,
\[
\|D\|\le \|A\|,\qquad
\|B\|\le \|A\|+\|D\|\le2\|A\|,
\qquad
\|D\|_F^2+\|B\|_F^2=\|A\|_F^2.
\]
[/STRATEGY]

### The off-diagonal part

We claim that
\[
\mathbb E e^{\lambda V}
 \le \exp\left(C\lambda^2K^4\|B\|_F^2\right)
\tag{5}
\]
for
\[
|\lambda|\le \frac{c}{K^2\|B\|}.
\tag{6}
\]

[CONTROL_SECTION: p1 | Random partition of the off-diagonal form]
“Let \(\delta_i\) be independent Bernoulli variables and define
\(V_\delta=\sum_{i,j}\delta_i(1-\delta_j)b_{ij}X_iX_j\). Since
\(\mathbb E_\delta V_\delta=V/4\), Jensen’s inequality gives
\(e^{\lambda V}\le\mathbb E_\delta e^{4\lambda V_\delta}\).”
[/CONTROL_SECTION]
[RAG_ELABORATED_SECTION: p1 | Random-cut decoupling]
Let \(\delta_1,\dots,\delta_n\) be independent Bernoulli\((1/2)\) variables, independent of \(X\), and set
\[
V_\delta=\sum_{i,j}\delta_i(1-\delta_j)b_{ij}X_iX_j.
\]
Every off-diagonal ordered pair \((i,j)\) is retained with probability \(1/4\); the diagonal contributes nothing. Thus
\[
\mathbb E_\delta V_\delta=\frac14V.
\]
By convexity of the exponential,
\[
e^{\lambda V}
=e^{4\lambda\mathbb E_\delta V_\delta}
\le \mathbb E_\delta e^{4\lambda V_\delta}.
\tag{7}
\]

For fixed \(\delta\), let \(I=\{i:\delta_i=1\}\), \(J=I^c\), and let
\[
M=P_I BP_J=(b_{ij})_{i\in I,j\in J}.
\]
Then
\[
V_\delta=X_I^TMX_J.
\]
The point of the random cut is that \(X_I\) and \(X_J\) now involve disjoint, hence independent, coordinate sets. Conditioning on \(X_I\) and applying the subgaussian linear-form estimate to \(X_J\) therefore yields
\[
\mathbb E_{X_J}\exp(4\lambda X_I^TMX_J)
 \le
 \exp\left(C\lambda^2K^2\|M^TX_I\|_2^2\right).
\tag{8}
\]
Moreover, because \(M\) is a compression of \(B\),
\[
\|M\|\le\|B\|,
\qquad
\|M\|_F\le\|B\|_F.
\tag{9}
\]
[/RAG_ELABORATED_SECTION]
[NEW_STRATEGY: Bernoulli random-cut decoupling]
Why this is new and critical: The retrieved strategies cover independence-based factorization, but not the random-cut device that turns an off-diagonal quadratic chaos into a bilinear form between two independent coordinate blocks. This is the decisive reduction permitting conditional subgaussian estimates.
[/NEW_STRATEGY]

[STRATEGY: sub_independence_tensorization | Independence, tensorization, and union bounds]
After the random cut, independence of \(X_I\) and \(X_J\) allows the conditional moment-generating function in (8) to factor into one-dimensional subgaussian estimates.
[/STRATEGY]

[CONTROL_SECTION: p2 | Gaussian linearization]
“Set \(\alpha=C\lambda^2K^2\). Introduce a standard Gaussian vector \(g\), use
\(e^{\alpha\|z\|_2^2}=\mathbb E_g e^{\sqrt{2\alpha}\langle g,z\rangle}\), and apply the subgaussian estimate again.”
[/CONTROL_SECTION]
[RAG_ELABORATED_SECTION: p2 | Gaussian linearization]
Set \(\alpha=C\lambda^2K^2\). The remaining difficulty in (8) is that the exponent contains the random squared norm \(\|M^TX_I\|_2^2\), to which the linear subgaussian estimate does not apply directly. Introduce an independent standard Gaussian vector \(g\in\mathbb R^{|J|}\). For every deterministic \(z\),
\[
e^{\alpha\|z\|_2^2}
 =\mathbb E_g\exp\!\left(\sqrt{2\alpha}\,\langle g,z\rangle\right).
\]
Consequently, by Tonelli’s theorem and \(\langle g,M^TX_I\rangle=\langle Mg,X_I\rangle\),
\[
\begin{aligned}
\mathbb E_{X_I}e^{\alpha\|M^TX_I\|_2^2}
&=\mathbb E_g\mathbb E_{X_I}
  e^{\sqrt{2\alpha}\langle Mg,X_I\rangle} \\
&\le \mathbb E_g e^{C\alpha K^2\|Mg\|_2^2}.
\end{aligned}
\tag{10}
\]
Thus Gaussian linearization has converted a squared random norm back into a linear functional of the independent coordinates \(X_i\).

For a standard Gaussian vector \(g\), the Gaussian quadratic-moment estimate gives
\[
\mathbb E_g e^{\beta\|Mg\|_2^2}
 \le \exp(C\beta\|M\|_F^2)
\quad\text{whenever}\quad
\beta\|M\|^2\le c.
\tag{11}
\]
Taking \(\beta=C\alpha K^2=C\lambda^2K^4\), equations (8)–(11) imply
\[
\mathbb E_X e^{4\lambda V_\delta}
 \le
 \exp\left(C\lambda^2K^4\|B\|_F^2\right)
\]
provided \(|\lambda|\le c/(K^2\|B\|)\).
[/RAG_ELABORATED_SECTION]
[NEW_STRATEGY: Gaussian linearization of a squared norm]
Why this is new and critical: This device is absent from the retrieved hierarchy. It is essential because it rewrites the exponential of \(\|M^TX_I\|_2^2\) as an average of exponentials of linear forms, allowing the coordinatewise subgaussian hypothesis to be used a second time.
[/NEW_STRATEGY]

[CONTROL_SECTION: p3 | Singular-value product calculation]
“The singular-value decomposition gives
\(\prod_k(1-2\beta s_k^2)^{-1/2}\), which is bounded by
\(\exp(C\beta\sum_k s_k^2)\).”
[/CONTROL_SECTION]
[RAG_OMITTED_SECTION: p3 | Singular-value product calculation]
The explicit product calculation is compressed into (11): diagonalizing \(M^TM\) and applying the elementary bound \(-\log(1-u)\le Cu\) for small \(u\) proves it routinely.
[/RAG_OMITTED_SECTION]

Averaging the last bound over \(\delta\) in (7) proves (5).

### Completing the moment-generating function bound

By Cauchy–Schwarz, (2), (3), and (5),
\[
\begin{aligned}
\mathbb E e^{\lambda(U+V)}
&\le
 \bigl(\mathbb E e^{2\lambda U}\bigr)^{1/2}
 \bigl(\mathbb E e^{2\lambda V}\bigr)^{1/2} \\
&\le
 \exp\left(C\lambda^2K^4
   \bigl(\|D\|_F^2+\|B\|_F^2\bigr)\right)\\
&=
 \exp\left(C\lambda^2K^4\|A\|_F^2\right)
\end{aligned}
\tag{12}
\]
whenever
\[
|\lambda|\le \frac{c}{K^2\|A\|}.
\tag{13}
\]

Let
\[
Y=X^TAX-\mathbb EX^TAX.
\]
For \(0\le\lambda\le c/(K^2\|A\|)\), exponential Markov inequality and (12) give
\[
\mathbb P(Y\ge t)
 \le
 \exp\left(-\lambda t+C\lambda^2K^4\|A\|_F^2\right).
\tag{14}
\]

[CONTROL_SECTION: p4 | Chernoff parameter optimization]
“Choose
\(\lambda\asymp\min\{t/(K^4\|A\|_F^2),\,1/(K^2\|A\|)\}\)
and substitute it into the exponent.”
[/CONTROL_SECTION]
[RAG_OMITTED_SECTION: p4 | Chernoff parameter optimization]
The constant-level minimization of the quadratic exponent in (14), subject to the admissible range (13), is routine and is compressed.
[/RAG_OMITTED_SECTION]

[STRATEGY: sub_exponential_concentration | Exponential-moment and concentration arguments]
Optimizing (14) over the permitted \(\lambda\) gives
\[
\mathbb P(Y\ge t)
\le
\exp\left[
-c\min\left\{
\frac{t^2}{K^4\|A\|_F^2},
\frac{t}{K^2\|A\|}
\right\}
\right].
\]
Applying the same argument to \(-Y\) and combining the two tails yields
\[
\boxed{
\mathbb P\left(
\left|X^TAX-\mathbb EX^TAX\right|\ge t
\right)
\le
2\exp\left[
-c\min\left\{
\frac{t^2}{K^4\|A\|_F^2},
\frac{t}{K^2\|A\|}
\right\}
\right].
}
\]
[/STRATEGY]

### Retrieved strategy nodes

- `sub_triangle_error_estimates` — **Triangle-inequality and error-decomposition estimates**: Separate dominant and error terms and control them with triangle and reverse-triangle inequalities.
- `family_standard_theorem_reduction` — **Reduction to a standard theorem**: Modify domains and regularity hypotheses so that a known theorem applies directly.
- `sub_tail_integration` — **Tail integration and moment estimates**: Convert moments into tail integrals, insert probability bounds, and estimate the resulting integrals.
- `family_algebra_order_norm` — **Algebraic, order, and norm estimates**: Combine algebraic rearrangement and order reasoning with norm inequalities and duality estimates.
- `sub_independence_tensorization` — **Independence, tensorization, and union bounds**: Factor quantities using independence, tensorize information, and upgrade pointwise bounds to simultaneous bounds by a union bound.
- `sub_exponential_concentration` — **Exponential-moment and concentration arguments**: Apply exponential Markov inequalities, control moment-generating functions, and optimize parameters to derive tail bounds.
- `sub_covering_volumetric` — **Covering-net and volumetric arguments**: Replace continuous suprema by maxima over finite epsilon-nets and bound net sizes through packing and volume comparison.
- `sub_partition_refinement` — **Partition and refinement arguments**: Control meshes and subintervals, construct common refinements, and decompose coarse partitions into fine pieces.
- `sub_testing_information` — **Testing and information-theoretic reductions**: Reduce estimation to hypothesis testing and control testing error using divergence or mutual-information inequalities.
- `sub_intermediate_value` — **Intermediate Value Theorem**: Use continuity and endpoint value information to produce an intermediate value or interior zero.

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

Suppose \(Y\in\mathbb R^d\) satisfies
\[
\mathbb E YY^\top=I_d,
\qquad
\|\langle Y,u\rangle\|_{\psi_2}\le K\|u\|_2.
\]
For independent copies \(Y_1,\dots,Y_m\), set
\[
B=\frac1m\sum_{i=1}^m Y_iY_i^\top-I_d.
\]

Fix \(u\in S^{d-1}\). Then
\[
u^\top Bu
=\frac1m\sum_{i=1}^m\big(\langle Y_i,u\rangle^2-1\big).
\]
Since the square of a subgaussian random variable is subexponential,
\[
\big\|\langle Y_i,u\rangle^2-1\big\|_{\psi_1}
\le C\|\langle Y_i,u\rangle\|_{\psi_2}^2
\le CK^2.
\]
Bernstein's inequality therefore gives, for every \(t\ge 0\),
\[
\mathbb P\left\{|u^\top Bu|>t\right\}
\le
2\exp\left[-cm\min\left(\frac{t^2}{K^4},\frac{t}{K^2}\right)\right].
\tag{1}
\]

Let \(\mathcal N\) be a \(1/4\)-net of \(S^{d-1}\) with
\[
|\mathcal N|\le 9^d.
\]
For every symmetric matrix \(B\), the standard net approximation gives
\[
\|B\|\le 2\max_{u\in\mathcal N}|u^\top Bu|.
\tag{2}
\]
Indeed, if \(x\in S^{d-1}\) nearly attains \(\|B\|\), choose \(u\in\mathcal N\) with
\(\|x-u\|_2\le 1/4\); then
\[
|x^\top Bx-u^\top Bu|\le \frac12\|B\|.
\]

Combining (1), (2), and the union bound, we obtain
\[
\mathbb P\{\|B\|>2t\}
\le
2\exp\left[
d\log 9
-cm\min\left(\frac{t^2}{K^4},\frac{t}{K^2}\right)
\right].
\tag{3}
\]
For \(s\ge 0\), choose
\[
t=CK^2\left(\sqrt{\frac{d+s}{m}}+\frac{d+s}{m}\right)
\]
with \(C\) sufficiently large. Since, for \(a\ge0\),
\[
\min\big((\sqrt a+a)^2,\sqrt a+a\big)\ge c'a,
\]
inequality (3) yields
\[
\mathbb P\left\{
\|B\|>
CK^2\left(\sqrt{\frac{d+s}{m}}+\frac{d+s}{m}\right)
\right\}
\le 2e^{-s}.
\tag{4}
\]
Integrating this tail bound gives
\[
\mathbb E\|B\|
\le
CK^2\left(\sqrt{\frac dm}+\frac dm\right).
\tag{5}
\]

Thus, for every isotropic \(K\)-subgaussian random vector in \(\mathbb R^d\),
\[
\mathbb E\left\|
\frac1m\sum_{i=1}^m Y_iY_i^\top-I_d
\right\|
\le
CK^2\left(\sqrt{\frac dm}+\frac dm\right).
\tag{6}
\]

### Reduction to the isotropic case

Let
\[
H=\operatorname{range}(\Sigma),\qquad r=\dim H\le n.
\]
If \(v\in\ker(\Sigma)\), then
\[
\mathbb E\langle X,v\rangle^2=v^\top\Sigma v=0,
\]
so \(\langle X,v\rangle=0\) almost surely. Hence \(X\in H\) almost surely.

On \(H\), the restriction of \(\Sigma\) is positive definite. Define
\[
Y=\Sigma^{-1/2}X,
\]
where the inverse is taken only on \(H\). Then \(Y\in H\cong\mathbb R^r\) and
\[
\mathbb E YY^\top=I_H.
\]
Moreover, for every \(u\in H\),
\[
\begin{aligned}
\|\langle Y,u\rangle\|_{\psi_2}
&=\|\langle X,\Sigma^{-1/2}u\rangle\|_{\psi_2}\\
&\le K\|\langle X,\Sigma^{-1/2}u\rangle\|_{L_2}\\
&=K\|u\|_2.
\end{aligned}
\]
Thus \(Y\) satisfies the isotropic assumptions in dimension \(r\).

Writing \(X_i=\Sigma^{1/2}Y_i\), we have
\[
\Sigma_m-\Sigma
=
\Sigma^{1/2}
\left(
\frac1m\sum_{i=1}^mY_iY_i^\top-I_H
\right)
\Sigma^{1/2}.
\]
Consequently,
\[
\|\Sigma_m-\Sigma\|
\le
\|\Sigma\|
\left\|
\frac1m\sum_{i=1}^mY_iY_i^\top-I_H
\right\|.
\]
Taking expectations and using (6),
\[
\mathbb E\|\Sigma_m-\Sigma\|
\le
CK^2\left(\sqrt{\frac rm}+\frac rm\right)\|\Sigma\|.
\]
Finally, \(r\le n\), so
\[
\boxed{
\mathbb E\|\Sigma_m-\Sigma\|
\le
CK^2\left(\sqrt{\frac nm}+\frac nm\right)\|\Sigma\|
}.
\]
Here \(C>0\) is an absolute constant.

### Library-RAG output

Let \(X_1,\ldots ,X_m\) be independent copies of \(X\), and set
\[
\Sigma=\mathbb E XX^\top,
\qquad
\Sigma_m=\frac1m\sum_{i=1}^m X_iX_i^\top .
\]

### 1. The isotropic case

Suppose \(Y\in\mathbb R^d\) is isotropic and \(K\)-subgaussian:
\[
\mathbb EYY^\top=I_d,
\qquad
\|\langle Y,u\rangle\|_{\psi_2}\le K\|u\|_2.
\]
For independent copies \(Y_1,\dots,Y_m\), write
\[
B=\frac1m\sum_{i=1}^mY_iY_i^\top-I_d.
\]

[STRATEGY: sub_exponential_concentration | Exponential-moment and concentration arguments]
For fixed \(u\in S^{d-1}\),
\[
u^\top Bu=\frac1m\sum_{i=1}^m\bigl(\langle Y_i,u\rangle^2-1\bigr).
\]
Since the square of a subgaussian variable is subexponential,
\[
\|\langle Y_i,u\rangle^2-1\|_{\psi_1}
\le C\|\langle Y_i,u\rangle\|_{\psi_2}^2
\le CK^2.
\]
Bernstein’s inequality therefore yields
\[
\mathbb P\{|u^\top Bu|>t\}
\le
2\exp\!\left[-cm\min\!\left(\frac{t^2}{K^4},\frac{t}{K^2}\right)\right].
\tag{1}
\]
[/STRATEGY]

[STRATEGY: sub_covering_volumetric | Covering-net and volumetric arguments]
Let \(\mathcal N\) be a \(1/4\)-net of \(S^{d-1}\) with
\[
|\mathcal N|\le 9^d.
\]
The standard quadratic-form net lemma for symmetric matrices gives
\[
\|B\|\le 2\max_{u\in\mathcal N}|u^\top Bu|.
\tag{2}
\]
[/STRATEGY]

[CONTROL_SECTION: p1 | Routine verification of the net lemma]
The draft expands \(x^\top Bx-u^\top Bu\) and bounds it by \(\frac12\|B\|\).
[/CONTROL_SECTION]
[RAG_OMITTED_SECTION: p1 | Routine verification of the net lemma]
The two-term expansion and Cauchy–Schwarz estimate are omitted; they are the standard proof of the \(1/4\)-net inequality (2).
[/RAG_OMITTED_SECTION]

[STRATEGY: sub_independence_tensorization | Independence, tensorization, and union bounds]
Applying (1) at every point of \(\mathcal N\), followed by (2) and the union bound, gives
\[
\mathbb P\{\|B\|>2t\}
\le
2\exp\!\left[
d\log 9-cm\min\!\left(\frac{t^2}{K^4},\frac{t}{K^2}\right)
\right].
\tag{3}
\]
[/STRATEGY]

[CONTROL_SECTION: p2 | Elementary scalar estimate]
The draft separately verifies
\[
\min\bigl((\sqrt a+a)^2,\sqrt a+a\bigr)\ge c'a.
\]
[/CONTROL_SECTION]
[RAG_OMITTED_SECTION: p2 | Elementary scalar estimate]
This routine two-regime calculation (\(a\le1\) and \(a\ge1\)) is absorbed into the choice of the absolute constant below.
[/RAG_OMITTED_SECTION]

Substituting
\[
t=CK^2\left(\sqrt{\frac{d+s}{m}}+\frac{d+s}{m}\right)
\]
into (3), with \(C\) sufficiently large, yields
\[
\mathbb P\left\{
\|B\|>
CK^2\left(\sqrt{\frac{d+s}{m}}+\frac{d+s}{m}\right)
\right\}
\le 2e^{-s},
\qquad s\ge0.
\tag{4}
\]

[CONTROL_SECTION: p3 | Tail integration]
“Integrating this tail bound gives”
\[
\mathbb E\|B\|\le CK^2\left(\sqrt{\frac dm}+\frac dm\right).
\]
[/CONTROL_SECTION]
[RAG_ELABORATED_SECTION: p3 | Tail integration]
[STRATEGY: sub_tail_integration | Tail integration and moment estimates]
To justify the expectation estimate, put
\[
A(s)=CK^2\left(\sqrt{\frac{d+s}{m}}+\frac{d+s}{m}\right).
\]
After replacing \(s\) by \(s+\log 2\), (4) gives
\(\mathbb P\{\|B\|>A(s+\log2)\}\le e^{-s}\). Hence, by the layer-cake formula and the change of variables \(t=A(s+\log2)\),
\[
\mathbb E\|B\|
\le A(\log2)+\int_0^\infty e^{-s}A'(s+\log2)\,ds.
\]
Since \(d\ge1\),
\[
A(\log2)+\int_0^\infty e^{-s}A'(s+\log2)\,ds
\le
CK^2\left(\sqrt{\frac dm}+\frac dm\right).
\]
Thus
\[
\mathbb E\left\|
\frac1m\sum_{i=1}^mY_iY_i^\top-I_d
\right\|
\le
CK^2\left(\sqrt{\frac dm}+\frac dm\right).
\tag{5}
\]
[/STRATEGY]
[/RAG_ELABORATED_SECTION]

### 2. Reduction to the isotropic case

[CONTROL_SECTION: p4 | Singular covariance and support reduction]
The draft states that if \(v\in\ker(\Sigma)\), then \(\langle X,v\rangle=0\) almost surely, and concludes that \(X\in\operatorname{range}(\Sigma)\) almost surely.
[/CONTROL_SECTION]
[RAG_ELABORATED_SECTION: p4 | Singular covariance and support reduction]
[STRATEGY: family_logical_reasoning | Logical decomposition, cases, and contradiction]
Let
\[
H=\operatorname{range}(\Sigma),\qquad r=\dim H.
\]
Choose an orthonormal basis \(v_1,\ldots,v_{n-r}\) of \(\ker(\Sigma)\). For every \(j\),
\[
\mathbb E\langle X,v_j\rangle^2=v_j^\top\Sigma v_j=0,
\]
so \(\langle X,v_j\rangle=0\) almost surely. Because there are only finitely many basis vectors, these equalities hold simultaneously on an event of probability one. Thus
\[
X\in(\ker\Sigma)^\perp=\operatorname{range}(\Sigma)=H
\quad\text{almost surely}.
\]
If \(r=0\), then \(X=0\) almost surely and the theorem is immediate. Hence assume \(r\ge1\).
[/STRATEGY]

[STRATEGY: family_standard_theorem_reduction | Reduction to a standard theorem]
The restriction of \(\Sigma\) to \(H\) is positive definite, so one may whiten \(X\) on its effective support by setting
\[
Y=\Sigma^{-1/2}X\in H,
\]
where the inverse is taken only on \(H\). Then
\[
\mathbb EYY^\top=I_H.
\]
Moreover, for \(u\in H\),
\[
\|\langle Y,u\rangle\|_{\psi_2}
=
\|\langle X,\Sigma^{-1/2}u\rangle\|_{\psi_2}
\le
K\|\langle X,\Sigma^{-1/2}u\rangle\|_{L_2}
=
K\|u\|_2.
\]
Thus \(Y\) satisfies the isotropic assumptions in dimension \(r\).
[/STRATEGY]
[/RAG_ELABORATED_SECTION]

Writing \(X_i=\Sigma^{1/2}Y_i\), we obtain
\[
\Sigma_m-\Sigma
=
\Sigma^{1/2}
\left(\frac1m\sum_{i=1}^mY_iY_i^\top-I_H\right)
\Sigma^{1/2}.
\]
Consequently,
\[
\|\Sigma_m-\Sigma\|
\le
\|\Sigma\|
\left\|
\frac1m\sum_{i=1}^mY_iY_i^\top-I_H
\right\|.
\]
Taking expectations and applying (5) in dimension \(r\),
\[
\mathbb E\|\Sigma_m-\Sigma\|
\le
CK^2\left(\sqrt{\frac rm}+\frac rm\right)\|\Sigma\|.
\]
Finally \(r\le n\), and therefore
\[
\boxed{
\mathbb E\|\Sigma_m-\Sigma\|
\le
CK^2\left(\sqrt{\frac nm}+\frac nm\right)\|\Sigma\|
}.
\]
Here \(C>0\) is an absolute constant.

### Retrieved strategy nodes

- `family_standard_theorem_reduction` — **Reduction to a standard theorem**: Modify domains and regularity hypotheses so that a known theorem applies directly.
- `sub_independence_tensorization` — **Independence, tensorization, and union bounds**: Factor quantities using independence, tensorize information, and upgrade pointwise bounds to simultaneous bounds by a union bound.
- `sub_exponential_concentration` — **Exponential-moment and concentration arguments**: Apply exponential Markov inequalities, control moment-generating functions, and optimize parameters to derive tail bounds.
- `sub_tail_integration` — **Tail integration and moment estimates**: Convert moments into tail integrals, insert probability bounds, and estimate the resulting integrals.
- `family_logical_reasoning` — **Logical decomposition, cases, and contradiction**: Split logical, order, endpoint, degeneracy, or parameter cases and use contradiction or contraposition to eliminate alternatives.
- `sub_canonical_rewriting` — **Canonical rewriting**: Rewrite abstract distances, norms, slopes, interval interiors, and formal-series expressions in concrete canonical forms.
- `family_probability_information` — **Probability, concentration, and information methods**: Probabilistic proof methods based on exponential moments, tails, independence, union bounds, and information-theoretic reductions.
- `sub_approximation_archimedean` — **Approximation and Archimedean error control**: Choose dense approximants and then select an index making the uniform approximation error smaller than a prescribed tolerance.
- `sub_covering_volumetric` — **Covering-net and volumetric arguments**: Replace continuous suprema by maxima over finite epsilon-nets and bound net sizes through packing and volume comparison.
- `sub_set_extensionality` — **Set identities and extensionality**: Prove set equalities by extensionality or mutual inclusion and simplify Boolean set operations.

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

Let \(M=|F|\). If \(M\le 1\), the conclusion is vacuous, so assume \(M\ge 2\).

For each distinct \(f,g\in F\), define
\[
Z_i^{f,g}:=(f(X_i)-g(X_i))^2.
\]
Then
\[
\mathbb E Z_i^{f,g}
=\|f-g\|_{L_2(\mu)}^2
>\varepsilon^2,
\]
while
\[
\frac1n\sum_{i=1}^n Z_i^{f,g}
=\|f-g\|_{L_2(\mu_n)}^2.
\]

Boolean functions are bounded, and under either standard convention \(f\in\{0,1\}\) or \(f\in\{-1,1\}\), we have
\[
0\le Z_i^{f,g}\le 4.
\]
Thus, by Hoeffding’s inequality,
\[
\begin{aligned}
\Pr\left\{\|f-g\|_{L_2(\mu_n)}\le \frac{\varepsilon}{2}\right\}
&=\Pr\left\{\frac1n\sum_{i=1}^n Z_i^{f,g}\le \frac{\varepsilon^2}{4}\right\}\\
&\le
\Pr\left\{
\frac1n\sum_{i=1}^n Z_i^{f,g}
-\mathbb EZ_i^{f,g}
\le -\frac{3\varepsilon^2}{4}
\right\}\\
&\le
\exp\left(
-\frac{2n(3\varepsilon^2/4)^2}{4^2}
\right)\\
&=
\exp\left(-\frac{9n\varepsilon^4}{128}\right).
\end{aligned}
\]

There are at most \(M^2/2\) unordered pairs of distinct functions. Therefore, by the union bound,
\[
\Pr\left\{
\exists f\ne g:\,
\|f-g\|_{L_2(\mu_n)}\le \frac{\varepsilon}{2}
\right\}
\le
\frac{M^2}{2}
\exp\left(-\frac{9n\varepsilon^4}{128}\right).
\]

If
\[
n\ge 128\,\varepsilon^{-4}\log M,
\]
then
\[
\frac{M^2}{2}
\exp\left(-\frac{9n\varepsilon^4}{128}\right)
\le \frac12 M^{2-9}
=\frac12 M^{-7}
<0.01,
\]
since \(M\ge2\). Hence, with probability at least \(0.99\),
\[
\|f-g\|_{L_2(\mu_n)}>\frac{\varepsilon}{2}
\qquad\text{for every distinct } f,g\in F.
\]

Thus the result holds for a suitable absolute constant \(C\) (for example, \(C=128\)).

### Library-RAG output

Let \(M=|F|\). If \(M\le 1\), there are no distinct pairs, so the assertion is vacuous. Assume \(M\ge2\).

[CONTROL_SECTION: p1 | Squaring the empirical distance]
For each distinct \(f,g\in F\), define \(Z_i^{f,g}=(f(X_i)-g(X_i))^2\), note that its expectation is the squared population distance, and its empirical average is the squared empirical distance.
[/CONTROL_SECTION]
[RAG_ELABORATED_SECTION: p1 | Squaring the empirical distance]
[STRATEGY: family_definitional_reformulation | Definitional unfolding and equivalent reformulation]
Fix distinct \(f,g\in F\), and set
\[
Z_i=(f(X_i)-g(X_i))^2.
\]
Then the \(Z_i\) are i.i.d. and
\[
\mathbb EZ_i=\|f-g\|_{L_2(\mu)}^2>\varepsilon^2,
\qquad
\frac1n\sum_{i=1}^n Z_i=\|f-g\|_{L_2(\mu_n)}^2.
\]
Thus failure of the desired empirical separation for this pair is exactly the event
\[
\frac1n\sum_{i=1}^n Z_i\le \frac{\varepsilon^2}{4}.
\]
Because Boolean functions take values in either \(\{0,1\}\) or \(\{-1,1\}\), in either convention \(0\le Z_i\le4\).
[/STRATEGY]
[/RAG_ELABORATED_SECTION]

[CONTROL_SECTION: p2 | Fixed-pair Hoeffding calculation]
The draft expands the Hoeffding substitution line by line, obtaining
\[
\Pr\!\left\{\|f-g\|_{L_2(\mu_n)}\le\varepsilon/2\right\}
\le \exp\!\left(-\frac{9n\varepsilon^4}{128}\right).
\]
[/CONTROL_SECTION]
[RAG_OMITTED_SECTION: p2 | Fixed-pair Hoeffding calculation]
[STRATEGY: sub_exponential_concentration | Exponential-moment and concentration arguments]
The intermediate arithmetic is routine. Since the bad event forces a downward deviation of at least \(3\varepsilon^2/4\), Hoeffding’s inequality for variables in \([0,4]\) gives directly
\[
\Pr\!\left\{\|f-g\|_{L_2(\mu_n)}\le\frac{\varepsilon}{2}\right\}
\le
\exp\!\left(-\frac{9n\varepsilon^4}{128}\right).
\]
[/STRATEGY]
[/RAG_OMITTED_SECTION]

[CONTROL_SECTION: p3 | Simultaneous control of all pairs]
There are at most \(M^2/2\) unordered pairs, so the draft applies a union bound over all distinct \(f,g\in F\).
[/CONTROL_SECTION]
[RAG_ELABORATED_SECTION: p3 | Simultaneous control of all pairs]
[STRATEGY: sub_independence_tensorization | Independence, tensorization, and union bounds]
Apply the fixed-pair estimate to each of the fewer than \(M^2/2\) unordered pairs. The union bound yields
\[
\Pr\!\left\{\exists\,f\ne g:
\|f-g\|_{L_2(\mu_n)}\le\frac{\varepsilon}{2}\right\}
\le
\frac{M^2}{2}\exp\!\left(-\frac{9n\varepsilon^4}{128}\right).
\]
No independence between the pairwise bad events is required.
[/STRATEGY]
[/RAG_ELABORATED_SECTION]

[CONTROL_SECTION: p4 | Choice of the absolute constant]
The draft explicitly computes that \(n\ge128\varepsilon^{-4}\log M\) makes the failure probability at most \(\frac12M^{-7}<0.01\).
[/CONTROL_SECTION]
[RAG_OMITTED_SECTION: p4 | Choice of the absolute constant]
Compressing the routine exponent arithmetic, if
\[
n\ge128\,\varepsilon^{-4}\log M,
\]
then the preceding failure probability is at most
\[
\frac12M^{-7}\le\frac1{256}<0.01,
\]
because \(M\ge2\).
[/RAG_OMITTED_SECTION]

Consequently, with probability at least \(0.99\),
\[
\|f-g\|_{L_2(\mu_n)}>\frac{\varepsilon}{2}
\qquad\text{for every distinct }f,g\in F.
\]
Thus the lemma holds with an absolute constant, for example \(C=128\).

### Retrieved strategy nodes

- `family_standard_theorem_reduction` — **Reduction to a standard theorem**: Modify domains and regularity hypotheses so that a known theorem applies directly.
- `sub_independence_tensorization` — **Independence, tensorization, and union bounds**: Factor quantities using independence, tensorize information, and upgrade pointwise bounds to simultaneous bounds by a union bound.
- `sub_probabilistic_packing` — **Probabilistic method and packing constructions**: Randomly generate nets, codes, sparse vectors, or approximants and prove that a suitable deterministic construction exists.
- `family_probability_information` — **Probability, concentration, and information methods**: Probabilistic proof methods based on exponential moments, tails, independence, union bounds, and information-theoretic reductions.
- `sub_exponential_concentration` — **Exponential-moment and concentration arguments**: Apply exponential Markov inequalities, control moment-generating functions, and optimize parameters to derive tail bounds.
- `sub_ordered_field_constructions` — **Ordered-field structure and canonical constructions**: Use ordered-field operations, canonical witnesses, Archimedeanness, completeness, and rational cuts in structural arguments about the reals.
- `sub_testing_information` — **Testing and information-theoretic reductions**: Reduce estimation to hypothesis testing and control testing error using divergence or mutual-information inequalities.
- `sub_tail_integration` — **Tail integration and moment estimates**: Convert moments into tail integrals, insert probability bounds, and estimate the resulting integrals.
- `family_definitional_reformulation` — **Definitional unfolding and equivalent reformulation**: Convert abstract statements into explicit definitions, quantified conditions, or standard equivalent formulations.
- `sub_intermediate_value` — **Intermediate Value Theorem**: Use continuity and endpoint value information to produce an intermediate value or interior zero.

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

### Proof

We first prove the result when \(T=\{1,\dots,n\}\). Write
\[
A_{ij}=\mathbb E[X_iX_j],
\qquad
B_{ij}=\mathbb E[Y_iY_j].
\]
Since
\[
\mathbb E(X_i-X_j)^2=A_{ii}+A_{jj}-2A_{ij},
\]
and similarly for \(Y\), assumption (7.3), together with \(A_{ii}=B_{ii}\), gives
\[
A_{ij}\ge B_{ij}\qquad\text{for every }i,j.
\tag{1}
\]
Moreover, \(A_{ii}-B_{ii}=0\).

Take independent copies of the Gaussian vectors \(X=(X_1,\ldots,X_n)\) and \(Y=(Y_1,\ldots,Y_n)\), and define
\[
Z(u)=\sqrt{u}\,X+\sqrt{1-u}\,Y,\qquad 0\le u\le1.
\]
Its covariance matrix is \(uA+(1-u)B\). The Gaussian interpolation formula says that, for a bounded \(C^2\) function \(f\) with bounded derivatives,
\[
\frac{d}{du}\mathbb E f(Z(u))
=
\frac12\sum_{i,j=1}^n
(A_{ij}-B_{ij})\,
\mathbb E\big[\partial_{ij}f(Z(u))\big].
\tag{2}
\]
The formula remains valid for degenerate Gaussian vectors, for instance by adding an arbitrarily small independent Gaussian perturbation and then taking a limit.

Fix \(\tau\in\mathbb R\). For \(\varepsilon>0\), choose a smooth nonincreasing function \(h_\varepsilon:\mathbb R\to[0,1]\) such that
\[
h_\varepsilon(x)=1\quad\text{if }x\le \tau-\varepsilon,
\qquad
h_\varepsilon(x)=0\quad\text{if }x\ge\tau.
\]
Set
\[
f_\varepsilon(x_1,\ldots,x_n)
=\prod_{i=1}^n h_\varepsilon(x_i).
\]
For \(i\ne j\),
\[
\partial_{ij}f_\varepsilon(x)
=
h_\varepsilon'(x_i)h_\varepsilon'(x_j)
\prod_{k\ne i,j}h_\varepsilon(x_k)\ge0,
\]
because \(h_\varepsilon'\le0\). The terms with \(i=j\) vanish from (2), since \(A_{ii}=B_{ii}\). Thus (1) and (2) imply
\[
\frac{d}{du}\mathbb E f_\varepsilon(Z(u))\ge0.
\]
Integrating from \(0\) to \(1\), we obtain
\[
\mathbb E f_\varepsilon(X)\ge \mathbb E f_\varepsilon(Y).
\]
As \(\varepsilon\downarrow0\),
\[
f_\varepsilon(x)\longrightarrow
\mathbf 1_{\{x_1<\tau,\ldots,x_n<\tau\}}.
\]
Hence, by bounded convergence,
\[
\mathbb P\!\left\{\max_i X_i<\tau\right\}
\ge
\mathbb P\!\left\{\max_i Y_i<\tau\right\}.
\]
Taking complements gives
\[
\mathbb P\!\left\{\max_i X_i\ge\tau\right\}
\le
\mathbb P\!\left\{\max_i Y_i\ge\tau\right\}.
\tag{3}
\]

For countable \(T\), enumerate it as \(T=\{t_1,t_2,\ldots\}\) and let
\[
U_n=\max_{k\le n}X_{t_k},\qquad
V_n=\max_{k\le n}Y_{t_k}.
\]
The finite-dimensional result also gives
\[
\mathbb P\{U_n>a\}\le \mathbb P\{V_n>a\}.
\]
Letting \(n\to\infty\),
\[
\mathbb P\!\left\{\sup_{t\in T}X_t>a\right\}
\le
\mathbb P\!\left\{\sup_{t\in T}Y_t>a\right\}.
\]
Finally,
\[
\left\{\sup_tX_t\ge\tau\right\}
=
\bigcap_{m\ge1}
\left\{\sup_tX_t>\tau-\frac1m\right\},
\]
so continuity of probability from above yields (7.4). The same argument applies to separable Gaussian processes by restricting both processes to a common countable separating subset of \(T\). As usual, some separability or measurability convention is needed when \(T\) is arbitrary.

Now put
\[
U=\sup_{t\in T}X_t,\qquad V=\sup_{t\in T}Y_t.
\]
Equation (7.4) says exactly that \(U\) is stochastically dominated by \(V\). Therefore, for every bounded increasing function \(\phi\),
\[
\mathbb E\phi(U)\le \mathbb E\phi(V).
\]
Apply this to
\[
\phi_M(x)=\max(-M,\min(x,M)).
\]
If \(t_0\in T\), then \(U\ge X_{t_0}\), and hence
\[
U^-\le X_{t_0}^-,
\]
so the negative part of \(U\) is integrable; the same holds for \(V\). Consequently, letting \(M\to\infty\) gives, with extended expectations allowed,
\[
\mathbb E U\le\mathbb E V.
\]
That is,
\[
\boxed{\mathbb E\sup_{t\in T}X_t
\le
\mathbb E\sup_{t\in T}Y_t.}
\]

### Library-RAG output

### Proof

We first treat the finite-dimensional case \(T=\{1,\dots ,n\}\). Let
\[
A_{ij}=\mathbb E[X_iX_j],\qquad B_{ij}=\mathbb E[Y_iY_j].
\]

[CONTROL_SECTION: p1 | covariance comparison]
The draft expands both increment variances and uses equality of the diagonal variances to conclude \(A_{ij}\ge B_{ij}\).
[/CONTROL_SECTION]
[RAG_OMITTED_SECTION: p1 | covariance comparison]
Compressing the routine covariance algebra: assumption (7.3) is equivalent to
\[
A_{ii}=B_{ii},\qquad A_{ij}\ge B_{ij}\quad(i\ne j).
\tag{1}
\]
[/RAG_OMITTED_SECTION]

Realize \(X=(X_1,\dots ,X_n)\) and \(Y=(Y_1,\dots ,Y_n)\) independently, and set
\[
Z_u=\sqrt u\,X+\sqrt{1-u}\,Y,\qquad 0\le u\le1.
\]
Then \(Z_u\) is centered Gaussian with covariance
\[
\Sigma_u=uA+(1-u)B.
\]

[CONTROL_SECTION: p2 | Gaussian interpolation identity]
“The Gaussian interpolation formula says that
\[
\frac d{du}\mathbb Ef(Z(u))
=\frac12\sum_{i,j}(A_{ij}-B_{ij})
  \mathbb E[\partial_{ij}f(Z(u))].
\]
The formula remains valid for degenerate Gaussian vectors by perturbation.”
[/CONTROL_SECTION]
[RAG_ELABORATED_SECTION: p2 | Gaussian interpolation identity]
For completeness, let \(C=A-B\) and first regularize by replacing \(Z_u\) with
\[
Z_{u,\delta}=Z_u+\sqrt\delta\,G,
\]
where \(G\sim N(0,I_n)\) is independent. Its covariance \(\Sigma_u+\delta I_n\) is positive definite. If \(p_{u,\delta}\) denotes its Gaussian density, differentiation of the Gaussian density—or equivalently its Fourier transform—gives
\[
\partial_u p_{u,\delta}
 =\frac12\sum_{i,j=1}^n C_{ij}\,\partial_{ij}p_{u,\delta}.
\]
Thus, for bounded \(C^2\) functions \(f\) with bounded derivatives, two integrations by parts yield
\[
\frac d{du}\mathbb E f(Z_{u,\delta})
 =\frac12\sum_{i,j=1}^n C_{ij}\,
   \mathbb E[\partial_{ij}f(Z_{u,\delta})].
\]
Integrating in \(u\) and then letting \(\delta\downarrow0\), bounded convergence gives
\[
\mathbb E f(X)-\mathbb E f(Y)
 =\frac12\int_0^1\sum_{i,j=1}^n
 (A_{ij}-B_{ij})\,
 \mathbb E[\partial_{ij}f(Z_u)]\,du.
\tag{2}
\]
This argument also covers singular covariance matrices.
[/RAG_ELABORATED_SECTION]
[NEW_STRATEGY: Gaussian covariance interpolation with integration by parts]
Why this is new and critical: none of the retrieved nodes covers the central comparison mechanism—interpolating covariance matrices and converting their derivative into expected Hessian entries by Gaussian integration by parts.
[/NEW_STRATEGY]

Fix \(\tau\in\mathbb R\). Choose a smooth nonincreasing \(h_\varepsilon:\mathbb R\to[0,1]\) satisfying
\[
h_\varepsilon(x)=1\quad(x\le \tau-\varepsilon),
\qquad
h_\varepsilon(x)=0\quad(x\ge\tau),
\]
and define
\[
f_\varepsilon(x)=\prod_{i=1}^n h_\varepsilon(x_i).
\]
For \(i\ne j\),
\[
\partial_{ij}f_\varepsilon(x)
=h_\varepsilon'(x_i)h_\varepsilon'(x_j)
 \prod_{k\ne i,j}h_\varepsilon(x_k)\ge0,
\]
because \(h_\varepsilon'\le0\). The diagonal coefficients in (2) vanish by \(A_{ii}=B_{ii}\), while every off-diagonal coefficient is nonnegative by (1). Consequently,
\[
\mathbb E f_\varepsilon(X)\ge \mathbb E f_\varepsilon(Y).
\]
As \(\varepsilon\downarrow0\),
\[
f_\varepsilon(x)\longrightarrow
\mathbf 1_{\{x_1<\tau,\dots ,x_n<\tau\}}.
\]
Bounded convergence therefore gives
\[
\mathbb P\!\left\{\max_iX_i<\tau\right\}
\ge
\mathbb P\!\left\{\max_iY_i<\tau\right\}.
\]
Taking complements,
\[
\mathbb P\!\left\{\max_iX_i\ge\tau\right\}
\le
\mathbb P\!\left\{\max_iY_i\ge\tau\right\}.
\tag{3}
\]

[CONTROL_SECTION: p3 | passage from finite to general index sets]
“For countable \(T\), enumerate it and let the finite maxima increase to the suprema. The same argument applies to separable Gaussian processes by restricting both processes to a common countable separating subset.”
[/CONTROL_SECTION]
[RAG_ELABORATED_SECTION: p3 | passage from finite to general index sets]
Suppose first that \(T=\{t_1,t_2,\ldots\}\), and put
\[
U_n=\max_{k\le n}X_{t_k},\qquad
V_n=\max_{k\le n}Y_{t_k}.
\]
The finite-dimensional result implies, for every \(a\),
\[
\mathbb P\{U_n>a\}\le \mathbb P\{V_n>a\};
\]
indeed this follows from (3) by writing
\(\{U_n>a\}=\bigcup_m\{U_n\ge a+1/m\}\).
Since \(U_n\uparrow U:=\sup_{t\in T}X_t\) and
\(V_n\uparrow V:=\sup_{t\in T}Y_t\), continuity from below gives
\[
\mathbb P\{U>a\}\le\mathbb P\{V>a\}.
\tag{4}
\]
Finally,
\[
\{U\ge\tau\}
=\bigcap_{m\ge1}\{U>\tau-1/m\},
\]
and likewise for \(V\). Applying (4) and continuity from above proves
\[
\mathbb P\{U\ge\tau\}\le\mathbb P\{V\ge\tau\}.
\tag{5}
\]

For separable processes, choose countable sets \(D_X,D_Y\subseteq T\) that realize the respective sample suprema almost surely, and let \(D=D_X\cup D_Y\). Then \(D\) is countable and
\[
\sup_{t\in T}X_t=\sup_{t\in D}X_t,\qquad
\sup_{t\in T}Y_t=\sup_{t\in D}Y_t
\quad\text{a.s.},
\]
so the countable argument applies. Thus (5) proves (7.4). As usual, for a completely arbitrary index set this statement requires the standard separability or outer-probability convention ensuring that the suprema are measurable.
[/RAG_ELABORATED_SECTION]
[STRATEGY: family_limits_completeness | Limit, sequence, and completeness methods]
The extension uses increasing finite maxima, continuity of probability, and a countable separable reduction.
[/STRATEGY]

It remains to compare expectations.

[CONTROL_SECTION: p4 | expectation from stochastic domination]
The draft applies stochastic domination to two-sided truncations
\(\phi_M(x)=\max(-M,\min(x,M))\), notes that the negative parts are integrable, and then says to let \(M\to\infty\).
[/CONTROL_SECTION]
[RAG_ELABORATED_SECTION: p4 | expectation from stochastic domination]
Assume \(T\ne\varnothing\) and fix \(t_0\in T\). Since
\[
U:=\sup_{t\in T}X_t\ge X_{t_0},
\qquad
V:=\sup_{t\in T}Y_t\ge Y_{t_0},
\]
we have
\[
U^-\le X_{t_0}^-,
\qquad
V^-\le Y_{t_0}^-.
\]
Hence both negative parts are integrable.

From (4),
\[
\mathbb P\{U>x\}\le\mathbb P\{V>x\}\qquad(x\ge0),
\]
while taking complements in (5) gives
\[
\mathbb P\{U<-x\}\ge\mathbb P\{V<-x\}\qquad(x\ge0).
\]
The tail-integral formulas therefore imply
\[
\mathbb E U^+
 =\int_0^\infty\mathbb P\{U>x\}\,dx
 \le
 \int_0^\infty\mathbb P\{V>x\}\,dx
 =\mathbb E V^+,
\]
and
\[
\mathbb E U^-
 =\int_0^\infty\mathbb P\{U<-x\}\,dx
 \ge
 \int_0^\infty\mathbb P\{V<-x\}\,dx
 =\mathbb E V^-.
\]
Since the negative parts are finite, the extended expectations are well defined, and subtraction yields
\[
\boxed{\mathbb E\sup_{t\in T}X_t
\le
\mathbb E\sup_{t\in T}Y_t}.
\]
[/RAG_ELABORATED_SECTION]
[NEW_STRATEGY: Tail-integral transfer of stochastic order]
Why this is new and critical: the retrieved nodes do not cover the passage from stochastic domination to possibly extended expectations; splitting into positive and negative tail integrals makes the limiting argument rigorous.
[/NEW_STRATEGY]

### Retrieved strategy nodes

- `sub_order_completeness` — **Suprema, infima, and order completeness**: Apply least-upper-bound and greatest-lower-bound properties to bounded sets, images, limsups, and moduli of continuity.
- `family_limits_completeness` — **Limit, sequence, and completeness methods**: Use epsilon or filter formulations, limit laws, squeezing, completeness, subsequences, and limsup-liminf criteria.
- `sub_compactness` — **Compactness arguments**: Apply compactness of intervals or images to obtain boundedness, attained extrema, uniform continuity, or convergent subsequences.
- `sub_riemann_modulus_control` — **Modulus-of-continuity control of Riemann sums**: Control tag changes using a modulus of continuity and sum local errors to prove convergence and partition independence.
- `sub_intermediate_value` — **Intermediate Value Theorem**: Use continuity and endpoint value information to produce an intermediate value or interior zero.
- `sub_uniform_convergence_mtest` — **Uniform convergence and the Weierstrass M-test**: Produce a summable uniform majorant and transfer continuity or bounds to the resulting series.
- `sub_series_tests` — **Series comparison and convergence tests**: Use comparison, term, root, ratio, alternating-series, geometric, or rearrangement criteria.
- `family_probability_information` — **Probability, concentration, and information methods**: Probabilistic proof methods based on exponential moments, tails, independence, union bounds, and information-theoretic reductions.
- `sub_exponential_concentration` — **Exponential-moment and concentration arguments**: Apply exponential Markov inequalities, control moment-generating functions, and optimize parameters to derive tail bounds.
- `sub_covering_volumetric` — **Covering-net and volumetric arguments**: Replace continuous suprema by maxima over finite epsilon-nets and bound net sizes through packing and volume comparison.

---

## lemma_2_7_8 — Lemma 2.7.8 (Centering)

Dataset: `high_dimensional_probability`

### Input statement

Lemma 2.7.8 (Centering). Any subgaussian random variable X satisfies
                                    ∥X − E X∥ψ2 ≤ C∥X∥ψ2 .

### Task

Explain the proof strategy and give a proof plan. Identify the main mathematical methods used.

### Control output

Let the subgaussian Orlicz norm be
\[
\|X\|_{\psi_2}
:=\inf\left\{t>0:\mathbb E\exp\left(\frac{X^2}{t^2}\right)\le 2\right\}.
\]

This is a norm, so by the triangle inequality,
\[
\|X-\mathbb EX\|_{\psi_2}
\le \|X\|_{\psi_2}+\|\mathbb EX\|_{\psi_2}.
\]

It remains to bound the second term. Fix any \(t>\|X\|_{\psi_2}\). By Jensen’s inequality, since \(x\mapsto e^{x^2/t^2}\) is convex,
\[
\exp\left(\frac{(\mathbb EX)^2}{t^2}\right)
\le \mathbb E\exp\left(\frac{X^2}{t^2}\right)
\le 2.
\]
Thus the constant random variable \(\mathbb EX\) satisfies
\[
\|\mathbb EX\|_{\psi_2}\le t.
\]
Letting \(t\downarrow \|X\|_{\psi_2}\) gives
\[
\|\mathbb EX\|_{\psi_2}\le \|X\|_{\psi_2}.
\]
Consequently,
\[
\boxed{\|X-\mathbb EX\|_{\psi_2}\le 2\|X\|_{\psi_2}}.
\]

Hence the result holds with \(C=2\) (and therefore with some universal constant \(C\) under any equivalent convention for the \(\psi_2\)-norm).

### Library-RAG output

Let
\[
K:=\|X\|_{\psi_2}
=\inf\left\{t>0:\mathbb E e^{X^2/t^2}\le 2\right\}<\infty .
\]

[CONTROL_SECTION: p1 | Existence of the mean]
The draft immediately uses \(\mathbb EX\) without verifying that a subgaussian random variable is integrable.
[/CONTROL_SECTION]
[RAG_ELABORATED_SECTION: p1 | Existence of the mean]
Choose \(s>0\) such that \(\mathbb E e^{X^2/s^2}\le2\). Since \(|u|\le e^{u^2}\) for all \(u\),
\[
\mathbb E|X|
\le s\,\mathbb E e^{X^2/s^2}
\le 2s<\infty.
\]
Thus \(\mathbb EX\) is well-defined.
[STRATEGY: family_algebra_order_norm | Algebraic, order, and norm estimates]
The exponential-moment assumption is converted into first-moment integrability by a deterministic domination.
[/STRATEGY]
[/RAG_ELABORATED_SECTION]

[CONTROL_SECTION: p2 | Admissibility above the infimum]
“Fix any \(t>\|X\|_{\psi_2}\). By Jensen’s inequality,
\[
e^{(\mathbb EX)^2/t^2}\le \mathbb E e^{X^2/t^2}\le2.
\]”
The second inequality requires justification because the norm is defined as an infimum.
[/CONTROL_SECTION]
[RAG_ELABORATED_SECTION: p2 | Admissibility above the infimum]
Set
\[
A:=\left\{s>0:\mathbb E e^{X^2/s^2}\le2\right\}.
\]
This set is upward closed. If \(t>K=\inf A\), then some \(s\in A\) satisfies \(s<t\); hence \(t\in A\), so
\[
\mathbb E e^{X^2/t^2}\le2.
\]
The function \(x\mapsto e^{x^2/t^2}\) is convex, and therefore Jensen’s inequality gives
\[
e^{(\mathbb EX)^2/t^2}
\le \mathbb E e^{X^2/t^2}
\le2.
\]
Thus every \(t>K\) is admissible in the definition of the \(\psi_2\)-norm of the constant random variable \(\mathbb EX\). Consequently,
\[
\|\mathbb EX\|_{\psi_2}\le K.
\]
[STRATEGY: sub_definitional_unfolding | Definitional unfolding]
The admissible set in the infimum definition is made explicit, including its upward-closed property.
[/STRATEGY]
[STRATEGY: sub_convexity_variational | Convexity and variational arguments]
Jensen’s inequality transfers the exponential-moment bound from \(X\) to its expectation.
[/STRATEGY]
[/RAG_ELABORATED_SECTION]

[CONTROL_SECTION: p3 | Final routine combination]
The draft separately states that the constant is admissible, lets \(t\downarrow K\), bounds its norm, and then applies the triangle inequality.
[/CONTROL_SECTION]
[RAG_OMITTED_SECTION: p3 | Final routine combination]
These routine concluding steps are compressed into the single triangle-inequality estimate below.
[/RAG_OMITTED_SECTION]

[STRATEGY: sub_triangle_error_estimates | Triangle-inequality and error-decomposition estimates]
Using the triangle inequality for the Luxemburg \(\psi_2\)-norm,
\[
\|X-\mathbb EX\|_{\psi_2}
\le \|X\|_{\psi_2}+\|\mathbb EX\|_{\psi_2}
\le 2\|X\|_{\psi_2}.
\]
[/STRATEGY]

Hence the lemma holds with \(C=2\) under this normalization of the \(\psi_2\)-norm.

### Retrieved strategy nodes

- `sub_intermediate_value` — **Intermediate Value Theorem**: Use continuity and endpoint value information to produce an intermediate value or interior zero.
- `sub_triangle_error_estimates` — **Triangle-inequality and error-decomposition estimates**: Separate dominant and error terms and control them with triangle and reverse-triangle inequalities.
- `sub_order_completeness` — **Suprema, infima, and order completeness**: Apply least-upper-bound and greatest-lower-bound properties to bounded sets, images, limsups, and moduli of continuity.
- `sub_convexity_variational` — **Convexity and variational arguments**: Use Jensen's inequality, convex combinations, first-order optimality, or comparison with feasible competitors.
- `family_definitional_reformulation` — **Definitional unfolding and equivalent reformulation**: Convert abstract statements into explicit definitions, quantified conditions, or standard equivalent formulations.
- `family_standard_theorem_reduction` — **Reduction to a standard theorem**: Modify domains and regularity hypotheses so that a known theorem applies directly.
- `family_algebra_order_norm` — **Algebraic, order, and norm estimates**: Combine algebraic rearrangement and order reasoning with norm inequalities and duality estimates.
- `sub_fundamental_theorem_calculus` — **Fundamental Theorem of Calculus**: Convert derivatives into integral increments or differentiate parameterized integrals.
- `sub_structured_parameters` — **Sparsity, low-rank structure, and norm duality**: Exploit support, cone, rank, or singular-space decompositions together with dual norms and restricted geometric conditions.
- `sub_independence_tensorization` — **Independence, tensorization, and union bounds**: Factor quantities using independence, tensorize information, and upgrade pointwise bounds to simultaneous bounds by a union bound.
- `sub_definitional_unfolding` — **Definitional unfolding**: Expand boundedness, inclusion, extrema, Riemann sums, and auxiliary constructions into their defining statements.

---
