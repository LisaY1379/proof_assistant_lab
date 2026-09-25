# Control vs Library-RAG Batch Experiment

## Metadata

- **created_at**: `2026-09-24T18:47:30.620583+00:00`
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

Let \(c,C>0\) denote absolute constants whose values may change from line to line.

Set
\[
A_{\mathrm s}=\frac{A+A^{T}}2.
\]
Since \(x^{T}Ax=x^{T}A_{\mathrm s}x\),
\[
\|A_{\mathrm s}\|\le \|A\|,
\qquad
\|A_{\mathrm s}\|_{F}\le \|A\|_{F}.
\]
Thus it suffices to prove the result for symmetric \(A\).

We use the standard subgaussian facts
\[
\mathbb E e^{sX_i}\le e^{Cs^{2}K^{2}},
\qquad
\|X_i^{2}-\mathbb EX_i^{2}\|_{\psi _1}\le CK^{2}.
\]

### 1. The diagonal part

Write
\[
X^{T}AX-\mathbb EX^{T}AX=D+S,
\]
where
\[
D=\sum_{i=1}^{n}a_{ii}\bigl(X_i^{2}-\mathbb EX_i^{2}\bigr),
\qquad
S=\sum_{i\ne j}a_{ij}X_iX_j.
\]
Here we used independence and \(\mathbb EX_i=0\), which give
\(\mathbb E X_iX_j=0\) for \(i\ne j\).

The summands in \(D\) are independent, centered, and satisfy
\[
\left\|a_{ii}(X_i^{2}-\mathbb EX_i^{2})\right\|_{\psi _1}
 \le CK^{2}|a_{ii}|.
\]
Bernstein’s inequality for sums of independent subexponential variables therefore gives
\[
\mathbb P\{|D|\ge u\}
 \le
2\exp\left[
-c\min\left(
\frac{u^{2}}{K^{4}\sum_i a_{ii}^{2}},
\frac{u}{K^{2}\max_i|a_{ii}|}
\right)\right].
\]
Because
\[
\sum_i a_{ii}^{2}\le \|A\|_{F}^{2},
\qquad
\max_i|a_{ii}|\le \|A\|,
\]
we obtain
\[
\mathbb P\{|D|\ge u\}
 \le
2\exp\left[
-c\min\left(
\frac{u^{2}}{K^{4}\|A\|_{F}^{2}},
\frac{u}{K^{2}\|A\|}
\right)\right].
\tag{1}
\]

### 2. An exponential-moment estimate

We first record an auxiliary estimate. Let \(Y\) have independent, mean-zero coordinates satisfying
\(\|Y_i\|_{\psi _2}\le K\), and let \(B\) be deterministic. Then
\[
\mathbb E\exp\bigl(s\|BY\|_{2}^{2}\bigr)
 \le
\exp\bigl(CsK^{2}\|B\|_{F}^{2}\bigr),
\tag{2}
\]
provided
\[
0\le s\le \frac{c}{K^{2}\|B\|^{2}}.
\tag{3}
\]

Indeed, for a standard Gaussian vector \(g\), independent of \(Y\),
\[
e^{s\|BY\|_{2}^{2}}
 =
\mathbb E_g\exp\bigl(\sqrt{2s}\,\langle g,BY\rangle\bigr).
\]
Conditioning on \(g\) and using independence and subgaussianity of the coordinates of \(Y\),
\[
\mathbb E_Y
 \exp\bigl(\sqrt{2s}\,\langle B^{T}g,Y\rangle\bigr)
 \le
\exp\bigl(CsK^{2}\|B^{T}g\|_{2}^{2}\bigr).
\]
If \(\sigma_k\) are the singular values of \(B\), the remaining Gaussian expectation is
\[
\prod_k\left(1-C'sK^{2}\sigma_k^{2}\right)^{-1/2}.
\]
Under condition (3), using \(-\log(1-x)\le Cx\) for sufficiently small \(x\), this is at most
\[
\exp\left(CsK^{2}\sum_k\sigma_k^{2}\right)
 =
\exp\left(CsK^{2}\|B\|_{F}^{2}\right).
\]
This proves (2).

### 3. The off-diagonal part

We prove that
\[
\mathbb E e^{\lambda S}
 \le
\exp\bigl(C\lambda^{2}K^{4}\|A\|_{F}^{2}\bigr)
\tag{4}
\]
whenever
\[
|\lambda|\le \frac{c}{K^{2}\|A\|}.
\tag{5}
\]

Let \(\delta_1,\ldots,\delta_n\) be independent Bernoulli random variables with
\(\mathbb P(\delta_i=1)=1/2\), independent of \(X\), and define
\[
S_\delta
 =
\sum_{i,j}\delta_i(1-\delta_j)a_{ij}X_iX_j.
\]
For \(i\ne j\),
\[
\mathbb E_\delta[\delta_i(1-\delta_j)]=\frac14,
\]
while the diagonal terms vanish. Hence
\[
S=4\mathbb E_\delta S_\delta.
\]
By convexity,
\[
\mathbb E_X e^{\lambda S}
\le
\mathbb E_\delta\mathbb E_X e^{4\lambda S_\delta}.
\tag{6}
\]

Fix \(\delta\) and let
\[
I=\{i:\delta_i=1\}.
\]
Then
\[
S_\delta=X_I^{T}A_{I,I^c}X_{I^c}.
\]
Conditioning on \(X_I\) and using the subgaussian moment-generating bound for the independent coordinates of \(X_{I^c}\),
\[
\mathbb E_{X_{I^c}}
 e^{4\lambda X_I^{T}A_{I,I^c}X_{I^c}}
\le
\exp\left(
C\lambda^{2}K^{2}
\|A_{I,I^c}^{T}X_I\|_{2}^{2}
\right).
\]
Apply (2) with
\[
s=C\lambda^{2}K^{2},
\qquad
B=A_{I,I^c}^{T}.
\]
Since
\[
\|B\|\le \|A\|,
\qquad
\|B\|_{F}\le \|A\|_{F},
\]
condition (3) follows from (5), and therefore
\[
\mathbb E_X e^{4\lambda S_\delta}
 \le
\exp\bigl(C\lambda^{2}K^{4}\|A\|_{F}^{2}\bigr).
\]
Together with (6), this proves (4).

For \(u\ge0\), Chernoff’s inequality gives, for every
\(0\le\lambda\le c/(K^{2}\|A\|)\),
\[
\mathbb P\{S\ge u\}
 \le
\exp\left(
-\lambda u+C\lambda^{2}K^{4}\|A\|_{F}^{2}
\right).
\]
Choosing
\[
\lambda
 =
c\min\left\{
\frac{u}{K^{4}\|A\|_{F}^{2}},
\frac1{K^{2}\|A\|}
\right\},
\]
with \(c\) sufficiently small, yields
\[
\mathbb P\{S\ge u\}
 \le
\exp\left[
-c\min\left(
\frac{u^{2}}{K^{4}\|A\|_{F}^{2}},
\frac{u}{K^{2}\|A\|}
\right)\right].
\]
Applying the same argument to \(-S\),
\[
\mathbb P\{|S|\ge u\}
 \le
2\exp\left[
-c\min\left(
\frac{u^{2}}{K^{4}\|A\|_{F}^{2}},
\frac{u}{K^{2}\|A\|}
\right)\right].
\tag{7}
\]

### 4. Completion

By the triangle inequality,
\[
\mathbb P\{|D+S|\ge t\}
 \le
\mathbb P\{|D|\ge t/2\}
 +
\mathbb P\{|S|\ge t/2\}.
\]
Using (1) and (7),
\[
\mathbb P\{|D+S|\ge t\}
 \le
4\exp\left[
-c\min\left(
\frac{t^{2}}{K^{4}\|A\|_{F}^{2}},
\frac{t}{K^{2}\|A\|}
\right)\right].
\]
Finally, by reducing the absolute constant \(c\), the prefactor \(4\) can be replaced by \(2\): combine this estimate with the trivial bound that probabilities are at most \(1\). Thus
\[
\boxed{
\mathbb P\left\{
\left|X^{T}AX-\mathbb EX^{T}AX\right|\ge t
\right\}
\le
2\exp\left[
-c\min\left(
\frac{t^{2}}{K^{4}\|A\|_{F}^{2}},
\frac{t}{K^{2}\|A\|}
\right)\right].
}
\]
This is the Hanson–Wright inequality.

### Library-RAG output

## Proof

Write \(\|\cdot\|\) for the operator norm and \(\|\cdot\|_F\) for the Frobenius norm. All constants \(c,C>0\) below are absolute and may change from line to line.

We use the following standard consequences of the \(\psi_2\)-norm:

1. If \(\mathbb EZ=0\) and \(\|Z\|_{\psi_2}\le K\), then
   \[
   \mathbb E e^{sZ}\le e^{Cs^2K^2},\qquad s\in\mathbb R.
   \tag{1}
   \]
2. The centered square is subexponential:
   \[
   \|Z^2-\mathbb EZ^2\|_{\psi_1}\le CK^2.
   \tag{2}
   \]
3. Consequently, if \(Y_i\) are independent, centered, and
   \(\|Y_i\|_{\psi_1}\le K^2\), then for any scalars \(b_i\),
   \[
   \mathbb E\exp\left(\lambda\sum_i b_iY_i\right)
   \le
   \exp\left(C\lambda^2K^4\sum_i b_i^2\right)
   \tag{3}
   \]
   whenever
   \[
   |\lambda|\le \frac{c}{K^2\max_i|b_i|}.
   \]
These follow directly by expanding the exponential and using the moment bounds
\((\mathbb E|Z|^p)^{1/p}\le CK\sqrt p\) and
\((\mathbb E|Y_i|^p)^{1/p}\le CK^2p\).

The proof will establish a quadratic bound for the moment-generating function and then optimize the exponential Markov inequality.

[NEW_STRATEGY: Laplace-transform concentration]
Why this is new: The retrieved hierarchy does not explicitly include deriving concentration tails from a locally quadratic moment-generating-function bound and optimizing the Laplace parameter.
[/NEW_STRATEGY]

### 1. Reduction to symmetric matrices

Let
\[
A_s=\frac{A+A^T}{2}.
\]
Since the skew-symmetric part contributes nothing,
\[
x^TAx=x^TA_sx
\]
for every \(x\in\mathbb R^n\). Moreover,
\[
\|A_s\|\le \|A\|,
\qquad
\|A_s\|_F\le \|A\|_F.
\]
It is therefore enough to prove the result for symmetric \(A\).

[STRATEGY: family_standard_theorem_reduction | Reduction to a standard theorem]
Derived according to this strategy: Replacing \(A\) by its symmetric part preserves the quadratic form while only decreasing the norms appearing in the desired estimate.
[/STRATEGY]

Henceforth assume \(A=A^T\).

### 2. Diagonal part

Decompose
\[
X^TAX-\mathbb EX^TAX=D+S,
\]
where
\[
D=\sum_{i=1}^n a_{ii}\bigl(X_i^2-\mathbb EX_i^2\bigr),
\qquad
S=\sum_{i\ne j}a_{ij}X_iX_j.
\tag{4}
\]
Here \(\mathbb ES=0\), since \(X_i\) and \(X_j\) are independent and centered whenever \(i\ne j\).

[STRATEGY: sub_canonical_rewriting | Canonical rewriting]
Derived according to this strategy: The centered quadratic form is rewritten canonically as a diagonal sum of centered squares plus an off-diagonal bilinear sum.
[/STRATEGY]

By (2)–(3),
\[
\mathbb Ee^{\lambda D}
\le
\exp\left(C\lambda^2K^4\sum_i a_{ii}^2\right)
\le
\exp\left(C\lambda^2K^4\|A\|_F^2\right)
\tag{5}
\]
provided
\[
|\lambda|\le \frac{c}{K^2\max_i|a_{ii}|}.
\]
Because \(A\) is symmetric,
\[
\max_i|a_{ii}|\le \|A\|,
\]
so (5) holds whenever
\[
|\lambda|\le \frac{c}{K^2\|A\|}.
\tag{6}
\]

### 3. Off-diagonal part: random decoupling

Let \(\delta_1,\dots,\delta_n\) be independent Bernoulli random variables with
\(\mathbb P(\delta_i=1)=1/2\), independent of \(X\), and put
\[
\Lambda=\{i:\delta_i=1\}.
\]
For fixed \(X\), define
\[
T_\delta=\sum_{i\in\Lambda,\ j\notin\Lambda}a_{ij}X_iX_j.
\]
Since \(\mathbb E_\delta[\delta_i(1-\delta_j)]=1/4\) for \(i\ne j\),
\[
S=4\,\mathbb E_\delta T_\delta.
\tag{7}
\]

[STRATEGY: family_explicit_construction | Explicit construction and parameter choice]
Derived according to this strategy: An independent Bernoulli partition is constructed explicitly to separate the two factors in each off-diagonal product.
[/STRATEGY]

By convexity of the exponential and (7),
\[
\mathbb Ee^{\lambda S}
\le
\mathbb E_\delta\mathbb E_Xe^{4\lambda T_\delta}.
\tag{8}
\]

[NEW_STRATEGY: Random-partition decoupling]
Why this is new: The off-diagonal quadratic chaos is converted into a conditionally linear bilinear form using a random partition, a method not represented among the retrieved nodes.
[/NEW_STRATEGY]

Fix \(\Lambda\), and write
\[
B=A_{\Lambda,\Lambda^c},\qquad
x=X_\Lambda,\qquad y=X_{\Lambda^c}.
\]
Then \(T_\delta=x^TBy\). Conditional on \(x\), the entries of \(y\) are independent, centered, and subgaussian. Applying (1) coordinatewise gives
\[
\begin{aligned}
\mathbb E_y e^{4\lambda x^TBy}
&=
\prod_{j\in\Lambda^c}
\mathbb E\exp\left(
4\lambda X_j\sum_{i\in\Lambda}a_{ij}X_i
\right)\\
&\le
\exp\left(C\lambda^2K^2\|B^Tx\|_2^2\right).
\end{aligned}
\tag{9}
\]

### 4. Gaussian linearization

Let \(g\sim N(0,I_{\Lambda^c})\), independently of everything else. The Gaussian identity
\[
\mathbb E_g e^{s\langle g,v\rangle}
=e^{s^2\|v\|_2^2/2}
\tag{10}
\]
allows us, with \(s=C|\lambda|K\), to rewrite the right-hand side of (9) as a Gaussian expectation. Thus
\[
\begin{aligned}
\mathbb E_x
\exp\left(C\lambda^2K^2\|B^Tx\|_2^2\right)
&=
\mathbb E_g\mathbb E_x
\exp\left(s\langle x,Bg\rangle\right)\\
&\le
\mathbb E_g
\exp\left(C\lambda^2K^4\|Bg\|_2^2\right),
\end{aligned}
\tag{11}
\]
where the last inequality again follows from (1), now applied to the independent coordinates of \(x\).

[NEW_STRATEGY: Gaussian linearization of a squared norm]
Why this is new: An auxiliary Gaussian vector converts an exponential of a squared norm into an exponential of a linear form, permitting a second use of scalar subgaussian estimates.
[/NEW_STRATEGY]

Let \(s_1,\dots,s_r\) be the singular values of \(B\). For \(\theta\ge0\) satisfying \(2\theta\|B\|^2<1\),
\[
\begin{aligned}
\mathbb E_g e^{\theta\|Bg\|_2^2}
&=\prod_{k=1}^r(1-2\theta s_k^2)^{-1/2}.
\end{aligned}
\]
If \(2\theta\|B\|^2\le 1/2\), then using
\(-\log(1-u)\le 2u\) for \(0\le u\le1/2\),
\[
\mathbb E_g e^{\theta\|Bg\|_2^2}
\le
\exp\left(C\theta\sum_{k=1}^rs_k^2\right)
=
\exp\left(C\theta\|B\|_F^2\right).
\tag{12}
\]
Because \(B=P_\Lambda AP_{\Lambda^c}\),
\[
\|B\|\le\|A\|,
\qquad
\|B\|_F\le\|A\|_F.
\tag{13}
\]
Taking \(\theta=C\lambda^2K^4\) in (12), equations (8)–(13) give
\[
\mathbb Ee^{\lambda S}
\le
\exp\left(C\lambda^2K^4\|A\|_F^2\right)
\tag{14}
\]
whenever
\[
|\lambda|\le \frac{c}{K^2\|A\|}.
\tag{15}
\]

### 5. Moment-generating function of the whole quadratic form

Although \(D\) and \(S\) need not be independent, Cauchy–Schwarz, (5), and (14) imply
\[
\begin{aligned}
\mathbb E e^{\lambda(D+S)}
&\le
\bigl(\mathbb Ee^{2\lambda D}\bigr)^{1/2}
\bigl(\mathbb Ee^{2\lambda S}\bigr)^{1/2}\\
&\le
\exp\left(C\lambda^2K^4\|A\|_F^2\right)
\end{aligned}
\tag{16}
\]
for
\[
|\lambda|\le \frac{c}{K^2\|A\|}.
\tag{17}
\]

Put
\[
Q=X^TAX-\mathbb EX^TAX,\qquad
V=K^4\|A\|_F^2,\qquad
L=\frac{c}{K^2\|A\|}.
\]
For \(0\le\lambda\le L\), Markov's inequality and (16) give
\[
\mathbb P(Q\ge t)
\le
\exp(-\lambda t+C\lambda^2V).
\tag{18}
\]

Choose
\[
\lambda=\min\left\{\frac{t}{2CV},\,\frac L2\right\}.
\tag{19}
\]
If the first term is selected, (18) gives an exponent bounded above by
\(-ct^2/V\). If the second is selected, the condition selecting it ensures that the quadratic term is dominated by a constant fraction of \(\lambda t\), and hence the exponent is bounded above by \(-cLt\). Therefore
\[
\mathbb P(Q\ge t)
\le
\exp\left[
-c\min\left(
\frac{t^2}{K^4\|A\|_F^2},
\frac{t}{K^2\|A\|}
\right)
\right].
\tag{20}
\]

[STRATEGY: family_explicit_construction | Explicit construction and parameter choice]
Derived according to this strategy: The Laplace parameter is chosen explicitly as the smaller of the quadratic-regime optimizer and the largest admissible linear-regime scale.
[/STRATEGY]

Applying the same argument to \(-Q\) and taking a union bound yields
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
This is the Hanson–Wright inequality. \(\square\)

### Retrieved strategy nodes

- `family_standard_theorem_reduction` — **Reduction to a standard theorem**: Modify domains and regularity hypotheses so that a known theorem applies directly.
- `sub_intermediate_value` — **Intermediate Value Theorem**: Use continuity and endpoint value information to produce an intermediate value or interior zero.
- `sub_fundamental_theorem_calculus` — **Fundamental Theorem of Calculus**: Convert derivatives into integral increments or differentiate parameterized integrals.
- `sub_canonical_rewriting` — **Canonical rewriting**: Rewrite abstract distances, norms, slopes, interval interiors, and formal-series expressions in concrete canonical forms.
- `family_explicit_construction` — **Explicit construction and parameter choice**: Construct witnesses, sequences, partitions, comparison points, thresholds, or auxiliary objects and tune free parameters.
- `sub_order_completeness` — **Suprema, infima, and order completeness**: Apply least-upper-bound and greatest-lower-bound properties to bounded sets, images, limsups, and moduli of continuity.
- `family_limits_completeness` — **Limit, sequence, and completeness methods**: Use epsilon or filter formulations, limit laws, squeezing, completeness, subsequences, and limsup-liminf criteria.
- `sub_sequence_completeness` — **Sequence and completeness methods**: Use epsilon-N arguments, Cauchy completeness, subsequences, and sequences approaching a point.
- `sub_mean_value_theorems` — **Fermat, Rolle, and Mean Value Theorems**: Convert extrema or endpoint equalities into derivative information and represent increments by intermediate derivatives.
- `sub_taylor_remainder` — **Taylor expansion with remainder**: Apply finite Taylor expansion with a controlled remainder and normalize the resulting coefficients.

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
\Sigma=\mathbb E(XX^\top),\qquad
\Sigma_m=\frac1m\sum_{i=1}^m X_iX_i^\top .
\]
(If covariance is defined in the centered sense, apply this to the centered vector.)

We first prove the isotropic case.

### Isotropic case

Suppose \(Y\in\mathbb R^r\) satisfies
\[
\mathbb E YY^\top=I_r,
\qquad
\|\langle Y,u\rangle\|_{\psi_2}\le K\|u\|_2
\quad\text{for all }u\in\mathbb R^r.
\]
Let \(Y_1,\dots,Y_m\) be independent copies and set
\[
B=\frac1m\sum_{i=1}^m Y_iY_i^\top-I_r.
\]

Choose a \(1/4\)-net \(\mathcal N\) of \(S^{r-1}\) with
\[
|\mathcal N|\le 9^r.
\]
For every symmetric matrix \(A\), the standard net argument gives
\[
\|A\|\le 2\max_{u\in\mathcal N}|u^\top Au|.
\]
Indeed, if \(x\in S^{r-1}\) and \(u\in\mathcal N\) satisfies
\(\|x-u\|_2\le 1/4\), then
\[
|x^\top Ax-u^\top Au|
 \le 2\|x-u\|_2\|A\|
 \le \frac12\|A\|.
\]

Fix \(u\in\mathcal N\). Since \(Y\) is isotropic,
\[
\mathbb E\langle Y,u\rangle^2=1.
\]
Moreover, the square of a subgaussian random variable is subexponential, so
\[
\big\|\langle Y,u\rangle^2-1\big\|_{\psi_1}
 \le C\|\langle Y,u\rangle\|_{\psi_2}^2
 \le CK^2.
\]
Bernstein's inequality therefore yields, for every \(t\ge0\),
\[
\mathbb P\left\{
\left|\frac1m\sum_{i=1}^m
\big(\langle Y_i,u\rangle^2-1\big)\right|>t
\right\}
\le
2\exp\left[-cm\min\left(\frac{t^2}{K^4},\frac{t}{K^2}\right)\right].
\]
Taking a union bound over \(\mathcal N\) and integrating the resulting tail gives
\[
\mathbb E\max_{u\in\mathcal N}|u^\top Bu|
 \le CK^2\left(\sqrt{\frac{\log |\mathcal N|}{m}}
                  +\frac{\log |\mathcal N|}{m}\right).
\]
Since \(\log|\mathcal N|\le Cr\), the net inequality implies
\[
\mathbb E\|B\|
\le CK^2\left(\sqrt{\frac rm}+\frac rm\right).
\tag{1}
\]

### Reduction to the isotropic case

Let \(H=\operatorname{range}(\Sigma)\) and \(r=\dim H\le n\). If \(v\in\ker\Sigma\), then
\[
\mathbb E\langle X,v\rangle^2=v^\top\Sigma v=0,
\]
so \(\langle X,v\rangle=0\) almost surely. Thus \(X\in H\) almost surely.

If \(r=0\), then \(X=0\) almost surely and the claim is immediate. Otherwise, define on \(H\)
\[
Y=\Sigma^{-1/2}X,
\]
where the inverse is taken only on \(H\). Then
\[
\mathbb E YY^\top=I_H.
\]
Furthermore, for \(u\in H\), assumption (4.29) gives
\[
\begin{aligned}
\|\langle Y,u\rangle\|_{\psi_2}
&=\|\langle X,\Sigma^{-1/2}u\rangle\|_{\psi_2}\\
&\le K\|\langle X,\Sigma^{-1/2}u\rangle\|_{L^2}\\
&=K\|u\|_2.
\end{aligned}
\]
Thus \(Y\) satisfies the isotropic assumptions in dimension \(r\).

Writing \(Y_i=\Sigma^{-1/2}X_i\), we have
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
\left\|\frac1m\sum_{i=1}^mY_iY_i^\top-I_H\right\|.
\]
Applying (1) and using \(r\le n\), we conclude that
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
\Sigma=\mathbb E XX^{\mathsf T},
\qquad
\Sigma_m=\frac1m\sum_{i=1}^m X_iX_i^{\mathsf T}.
\]
We prove
\[
\mathbb E\|\Sigma_m-\Sigma\|
 \le CK^2\left(\sqrt{\frac nm}+\frac nm\right)\|\Sigma\|.
\]

### 1. The isotropic case

We first prove the following lemma.

**Lemma.** Suppose \(Y\in\mathbb R^r\) is isotropic,
\[
\mathbb EYY^{\mathsf T}=I_r,
\]
and
\[
\|\langle Y,u\rangle\|_{\psi_2}\le K\|u\|_2
\qquad (u\in\mathbb R^r).
\]
For independent copies \(Y_1,\dots,Y_m\),
\[
M:=\frac1m\sum_{i=1}^mY_iY_i^{\mathsf T}
\]
satisfies
\[
\mathbb E\|M-I_r\|
 \le CK^2\left(\sqrt{\frac rm}+\frac rm\right).
\]

Fix \(u\in S^{r-1}\). Since \(Y\) is isotropic,
\[
\mathbb E\langle Y,u\rangle^2=1.
\]
Set
\[
Z_i(u):=\langle Y_i,u\rangle^2-1.
\]
The square of a subgaussian random variable is subexponential, so
\[
\|Z_i(u)\|_{\psi_1}
 \le C\|\langle Y_i,u\rangle\|_{\psi_2}^2
 \le CK^2.
\]
Bernstein’s inequality therefore gives, for every \(t\ge0\),
\[
\mathbb P\left\{
 \left|\frac1m\sum_{i=1}^m Z_i(u)\right|>t
\right\}
\le
2\exp\left[-cm\min\left(\frac{t^2}{K^4},\frac{t}{K^2}\right)\right].
\tag{1}
\]
[NEW_STRATEGY: Subgaussian-to-subexponential Bernstein concentration]
Why this is new: The retrieved hierarchy does not include the Orlicz-norm conversion \(Z\mapsto Z^2-\mathbb EZ^2\) followed by Bernstein concentration, which is the key probabilistic step here.
[/NEW_STRATEGY]

Let \(\mathcal N\) be a \(1/4\)-net of \(S^{r-1}\) with
\[
|\mathcal N|\le 9^r.
\]
Applying (1) to all \(u\in\mathcal N\), taking a union bound, and integrating the resulting tail estimate gives
\[
\mathbb E\max_{u\in\mathcal N}
\left|\frac1m\sum_{i=1}^m Z_i(u)\right|
\le
CK^2\left(
 \sqrt{\frac{\log(2|\mathcal N|)}m}
 +\frac{\log(2|\mathcal N|)}m
\right).
\]
Since \(\log(2|\mathcal N|)\le Cr\),
\[
\mathbb E\max_{u\in\mathcal N}
\left|u^{\mathsf T}(M-I_r)u\right|
\le CK^2\left(\sqrt{\frac rm}+\frac rm\right).
\tag{2}
\]
[NEW_STRATEGY: Epsilon-net discretization of operator norms]
Why this is new: The retrieved hierarchy contains no covering-net method for reducing a supremum over the sphere to finitely many scalar concentration estimates.
[/NEW_STRATEGY]

For every symmetric \(r\times r\) matrix \(B\), the \(1/4\)-net approximation gives
\[
\|B\|
=\sup_{u\in S^{r-1}}|u^{\mathsf T}Bu|
\le 2\max_{u\in\mathcal N}|u^{\mathsf T}Bu|.
\tag{3}
\]
Indeed, if \(\|x-y\|_2\le1/4\), then
\[
|x^{\mathsf T}Bx-y^{\mathsf T}By|
 \le 2\|x-y\|_2\|B\|
 \le \frac12\|B\|.
\]
Thus (3) follows by choosing \(x\) approximately maximizing the quadratic form. This rewrites the spectral norm of a symmetric matrix as a supremum of concrete quadratic forms.
[STRATEGY: sub_canonical_rewriting | Canonical rewriting]
Derived according to this strategy: The operator norm is rewritten as a supremum of quadratic forms, which can then be controlled on a finite net.
[/STRATEGY]

Taking \(B=M-I_r\) in (3) and using (2) proves the lemma:
\[
\mathbb E\|M-I_r\|
\le CK^2\left(\sqrt{\frac rm}+\frac rm\right).
\tag{4}
\]

### 2. Reduction of the general case to the isotropic case

If \(\Sigma=0\), then
\[
\mathbb E\|X\|_2^2=\operatorname{tr}(\Sigma)=0,
\]
so \(X=0\) almost surely and the result is immediate.

Suppose now that \(\Sigma\ne0\). Let
\[
E=\operatorname{range}(\Sigma),\qquad r=\dim E\le n.
\]
The random vector \(X\) belongs to \(E\) almost surely. Indeed, if \(v\in\ker(\Sigma)\), then
\[
\mathbb E\langle X,v\rangle^2=v^{\mathsf T}\Sigma v=0,
\]
so \(\langle X,v\rangle=0\) almost surely. Applying this to a basis of \(\ker(\Sigma)\) proves the assertion.

The restriction \(\Sigma_E\) of \(\Sigma\) to \(E\) is positive definite. Define the whitened random vector
\[
Y:=\Sigma_E^{-1/2}X\in E\simeq\mathbb R^r.
\]
Then
\[
\mathbb EYY^{\mathsf T}
 =\Sigma_E^{-1/2}\Sigma_E\Sigma_E^{-1/2}
 =I_E,
\]
so \(Y\) is isotropic. Moreover, for every \(u\in E\),
\[
\begin{aligned}
\|\langle Y,u\rangle\|_{\psi_2}
&=\|\langle X,\Sigma_E^{-1/2}u\rangle\|_{\psi_2}\\
&\le K\|\langle X,\Sigma_E^{-1/2}u\rangle\|_{L^2}\\
&=K\left(
u^{\mathsf T}\Sigma_E^{-1/2}\Sigma_E\Sigma_E^{-1/2}u
\right)^{1/2}\\
&=K\|u\|_2.
\end{aligned}
\]
Thus the isotropic lemma applies to \(Y\). This whitening step reduces the general covariance matrix to the identity on its effective range.
[STRATEGY: family_standard_theorem_reduction | Reduction to a standard theorem]
Derived according to this strategy: Restricting to the range of \(\Sigma\) and applying \(\Sigma^{-1/2}\) transforms the problem into the already established isotropic case.
[/STRATEGY]

Let \(Y_i=\Sigma_E^{-1/2}X_i\) and
\[
M=\frac1m\sum_{i=1}^mY_iY_i^{\mathsf T}.
\]
On \(E\),
\[
\Sigma_m=\Sigma_E^{1/2}M\Sigma_E^{1/2},
\qquad
\Sigma=\Sigma_E^{1/2}I_E\Sigma_E^{1/2}.
\]
Consequently,
\[
\Sigma_m-\Sigma
 =\Sigma_E^{1/2}(M-I_E)\Sigma_E^{1/2},
\]
and hence
\[
\|\Sigma_m-\Sigma\|
\le \|\Sigma_E^{1/2}\|^2\|M-I_E\|
=\|\Sigma\|\,\|M-I_E\|.
\]
Taking expectations and applying (4),
\[
\begin{aligned}
\mathbb E\|\Sigma_m-\Sigma\|
&\le \|\Sigma\|\,
CK^2\left(\sqrt{\frac rm}+\frac rm\right)\\
&\le CK^2\left(\sqrt{\frac nm}+\frac nm\right)\|\Sigma\|,
\end{aligned}
\]
because \(r\le n\). This is the claimed estimate. \(\square\)

### Retrieved strategy nodes

- `family_standard_theorem_reduction` — **Reduction to a standard theorem**: Modify domains and regularity hypotheses so that a known theorem applies directly.
- `sub_intermediate_value` — **Intermediate Value Theorem**: Use continuity and endpoint value information to produce an intermediate value or interior zero.
- `sub_fundamental_theorem_calculus` — **Fundamental Theorem of Calculus**: Convert derivatives into integral increments or differentiate parameterized integrals.
- `sub_canonical_rewriting` — **Canonical rewriting**: Rewrite abstract distances, norms, slopes, interval interiors, and formal-series expressions in concrete canonical forms.
- `sub_order_completeness` — **Suprema, infima, and order completeness**: Apply least-upper-bound and greatest-lower-bound properties to bounded sets, images, limsups, and moduli of continuity.
- `family_limits_completeness` — **Limit, sequence, and completeness methods**: Use epsilon or filter formulations, limit laws, squeezing, completeness, subsequences, and limsup-liminf criteria.
- `sub_sequence_completeness` — **Sequence and completeness methods**: Use epsilon-N arguments, Cauchy completeness, subsequences, and sequences approaching a point.
- `sub_mean_value_theorems` — **Fermat, Rolle, and Mean Value Theorems**: Convert extrema or endpoint equalities into derivative information and represent increments by intermediate derivatives.
- `family_structural_foundations` — **Cardinality, embeddings, and completion**: Use embeddings and cardinal comparisons or construct complete ordered structures from dense substructures and cuts.
- `sub_ordered_field_constructions` — **Ordered-field structure and canonical constructions**: Use ordered-field operations, canonical witnesses, Archimedeanness, completeness, and rational cuts in structural arguments about the reals.

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

Let \(N=|F|\). If \(N\le 1\), the statement is vacuous, so assume \(N\ge 2\).

Fix distinct \(f,g\in F\), and define
\[
Y_i=(f(X_i)-g(X_i))^2.
\]
Since \(f,g\) are Boolean-valued, \(0\le Y_i\le 1\), and
\[
\mathbb EY_i=\|f-g\|_{L_2(\mu)}^2>\varepsilon^2.
\]
Moreover,
\[
\|f-g\|_{L_2(\mu_n)}^2=\frac1n\sum_{i=1}^nY_i.
\]

If \(\|f-g\|_{L_2(\mu_n)}\le \varepsilon/2\), then
\[
\frac1n\sum_{i=1}^nY_i\le \frac{\varepsilon^2}{4}.
\]
Consequently,
\[
\frac1n\sum_{i=1}^nY_i-\mathbb EY_i
<-\frac{3\varepsilon^2}{4}.
\]
Hoeffding's inequality therefore gives
\[
\mathbb P\left\{
\|f-g\|_{L_2(\mu_n)}\le\frac{\varepsilon}{2}
\right\}
\le
\exp\left(-2n\left(\frac{3\varepsilon^2}{4}\right)^2\right)
=
\exp\left(-\frac98n\varepsilon^4\right).
\]

There are at most \(N^2\) ordered pairs of distinct functions. Thus, by the union bound,
\[
\begin{aligned}
\mathbb P\left\{
\exists f\ne g:\,
\|f-g\|_{L_2(\mu_n)}\le\frac{\varepsilon}{2}
\right\}
&\le
N^2\exp\left(-\frac98n\varepsilon^4\right).
\end{aligned}
\]
If
\[
n\ge 8\varepsilon^{-4}\log N,
\]
then
\[
N^2\exp\left(-\frac98n\varepsilon^4\right)
\le N^2e^{-9\log N}
=N^{-7}
\le 2^{-7}<0.01.
\]
Hence, with probability at least \(0.99\),
\[
\|f-g\|_{L_2(\mu_n)}>\frac{\varepsilon}{2}
\qquad\text{for every distinct }f,g\in F.
\]

Thus the lemma holds with a universal constant, for example \(C=8\).

If “Boolean” means \(\{-1,1\}\)-valued rather than \(\{0,1\}\)-valued, then \(0\le Y_i\le4\), and the same proof works after increasing the universal constant \(C\), for instance to \(128\).

### Library-RAG output

### Proof

Let \(m=|F|\). If \(m\le 1\), the conclusion is vacuous, so assume \(m\ge 2\).

Fix distinct \(f,g\in F\), and define
\[
Y_i=(f(X_i)-g(X_i))^2,\qquad
p_{f,g}=\mathbb E Y_i=\|f-g\|_{L_2(\mu)}^2.
\]
By the \(\varepsilon\)-separation assumption,
\[
p_{f,g}>\varepsilon^2.
\]
Moreover,
\[
\|f-g\|_{L_2(\mu_n)}^2=\frac1n\sum_{i=1}^nY_i.
\]
Thus the desired norm comparison is equivalent to a lower bound on an empirical average.  
[STRATEGY: family_definitional_reformulation | Definitional unfolding and equivalent reformulation]
Derived according to this strategy: Squaring the \(L_2\)-norms turns the separation statement into a concentration problem for empirical means.
[/STRATEGY]

Boolean functions are bounded. Under the convention \(F\subseteq\{0,1\}^{\Omega}\), one has \(0\le Y_i\le1\); under the convention \(F\subseteq\{-1,1\}^{\Omega}\), one has \(0\le Y_i\le4\). We use the latter, more conservative bound, so the proof covers both conventions.

For a fixed pair \(f\ne g\), the bad event is
\[
\|f-g\|_{L_2(\mu_n)}\le\frac{\varepsilon}{2},
\]
or equivalently,
\[
\frac1n\sum_{i=1}^nY_i\le\frac{\varepsilon^2}{4}.
\]
Since \(p_{f,g}>\varepsilon^2\), this event implies
\[
\frac1n\sum_{i=1}^nY_i-p_{f,g}
<-\frac{3\varepsilon^2}{4}.
\]
The variables \(Y_i\) are independent and take values in an interval of length at most \(4\). Hence Hoeffding’s inequality gives
\[
\begin{aligned}
\mathbb P\left(
\|f-g\|_{L_2(\mu_n)}\le\frac{\varepsilon}{2}
\right)
&\le
\exp\left(
-\frac{2n(3\varepsilon^2/4)^2}{4^2}
\right)\\
&=
\exp\left(-\frac{9}{128}n\varepsilon^4\right).
\end{aligned}
\]
[STRATEGY: sub_exponential_concentration | Exponential-moment and concentration arguments]
Derived according to this strategy: Hoeffding’s inequality converts boundedness and independence into an exponentially small lower-tail probability for each fixed pair.
[/STRATEGY]

There are fewer than \(m^2\) ordered pairs of distinct functions. Taking a union bound,
\[
\begin{aligned}
\mathbb P\left(
\exists f\ne g:\ 
\|f-g\|_{L_2(\mu_n)}\le\frac{\varepsilon}{2}
\right)
&\le
m^2\exp\left(-\frac{9}{128}n\varepsilon^4\right).
\end{aligned}
\]
[STRATEGY: family_probability_information | Probability, concentration, and information methods]
Derived according to this strategy: A union bound upgrades the fixed-pair concentration estimate to simultaneous control over the finite class.
[/STRATEGY]

Now take \(C=128\). If
\[
n\ge128\,\varepsilon^{-4}\log m,
\]
then
\[
m^2\exp\left(-\frac{9}{128}n\varepsilon^4\right)
\le m^2e^{-9\log m}
=m^{-7}
\le2^{-7}
<0.01.
\]
Consequently, with probability at least \(0.99\),
\[
\|f-g\|_{L_2(\mu_n)}>\frac{\varepsilon}{2}
\qquad\text{for every distinct }f,g\in F.
\]

Thus the lemma holds with an absolute constant, for example \(C=128\). If Boolean functions are specifically \(\{0,1\}\)-valued, the sharper bound \(0\le Y_i\le1\) allows \(C=8\). \(\square\)

### Retrieved strategy nodes

- `family_probability_information` — **Probability, concentration, and information methods**: Probabilistic proof methods based on exponential moments, tails, independence, union bounds, and information-theoretic reductions.
- `family_standard_theorem_reduction` — **Reduction to a standard theorem**: Modify domains and regularity hypotheses so that a known theorem applies directly.
- `sub_probabilistic_packing` — **Probabilistic method and packing constructions**: Randomly generate nets, codes, sparse vectors, or approximants and prove that a suitable deterministic construction exists.
- `sub_ordered_field_constructions` — **Ordered-field structure and canonical constructions**: Use ordered-field operations, canonical witnesses, Archimedeanness, completeness, and rational cuts in structural arguments about the reals.
- `sub_testing_information` — **Testing and information-theoretic reductions**: Reduce estimation to hypothesis testing and control testing error using divergence or mutual-information inequalities.
- `sub_exponential_concentration` — **Exponential-moment and concentration arguments**: Apply exponential Markov inequalities, control moment-generating functions, and optimize parameters to derive tail bounds.
- `sub_tail_integration` — **Tail integration and moment estimates**: Convert moments into tail integrals, insert probability bounds, and estimate the resulting integrals.
- `sub_intermediate_value` — **Intermediate Value Theorem**: Use continuity and endpoint value information to produce an intermediate value or interior zero.
- `sub_fundamental_theorem_calculus` — **Fundamental Theorem of Calculus**: Convert derivatives into integral increments or differentiate parameterized integrals.
- `family_definitional_reformulation` — **Definitional unfolding and equivalent reformulation**: Convert abstract statements into explicit definitions, quantified conditions, or standard equivalent formulations.

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

**Proof.** We first prove the result when \(T=\{1,\dots ,m\}\) is finite. Write
\[
A_{ij}=\mathbb E[X_iX_j],
\qquad
B_{ij}=\mathbb E[Y_iY_j].
\]
The assumptions imply
\[
A_{ii}=B_{ii}
\]
and, for \(i\neq j\),
\[
A_{ii}+A_{jj}-2A_{ij}
 \le B_{ii}+B_{jj}-2B_{ij}.
\]
Hence
\[
A_{ij}\ge B_{ij}\qquad (i\neq j). \tag{1}
\]

Realize \(X\) and \(Y\) independently and, for \(u\in[0,1]\), set
\[
Z_u=\sqrt u\,X+\sqrt{1-u}\,Y.
\]
Then \(Z_u\) is centered Gaussian with covariance
\[
C_u=uA+(1-u)B.
\]

Fix \(a\in\mathbb R\) and \(\varepsilon>0\). Let
\[
h(x)=\Phi\!\left(\frac{a-x}{\varepsilon}\right),
\qquad
f(x_1,\dots,x_m)=\prod_{i=1}^m h(x_i),
\]
where \(\Phi\) is the standard normal distribution function. The Gaussian interpolation identity gives
\[
\frac{d}{du}\mathbb E f(Z_u)
 =\frac12\sum_{i,j=1}^m
 (A_{ij}-B_{ij})\,
 \mathbb E\big[\partial_{ij}f(Z_u)\big]. \tag{2}
\]
For \(i=j\), the coefficient in (2) is zero. For \(i\neq j\),
\[
\partial_{ij}f(x)
 =h'(x_i)h'(x_j)\prod_{k\neq i,j}h(x_k)\ge 0,
\]
because \(h\ge0\) and \(h'\le0\). Together with (1), this shows
\[
\frac{d}{du}\mathbb E f(Z_u)\ge0.
\]
Consequently,
\[
\mathbb E f(X)\ge \mathbb E f(Y). \tag{3}
\]

Let \(g_1,\dots,g_m\) be independent standard Gaussians, independent of everything else. Conditioning on \(X\),
\[
\mathbb E f(X)
 =\mathbb P\!\left(X_i+\varepsilon g_i\le a
                   \text{ for every }i\right),
\]
and similarly for \(Y\). Thus (3) says
\[
\mathbb P\!\left(\max_i(X_i+\varepsilon g_i)\le a\right)
\ge
\mathbb P\!\left(\max_i(Y_i+\varepsilon g_i)\le a\right). \tag{4}
\]

As \(\varepsilon\downarrow0\),
\[
\max_i(X_i+\varepsilon g_i)\longrightarrow \max_iX_i,
\qquad
\max_i(Y_i+\varepsilon g_i)\longrightarrow \max_iY_i
\]
almost surely. Passing to the limit in (4), first at common continuity points of the two distribution functions and then at every \(a\) by right-continuity, yields
\[
\mathbb P\!\left(\max_iX_i\le a\right)
\ge
\mathbb P\!\left(\max_iY_i\le a\right)
\qquad(a\in\mathbb R). \tag{5}
\]
Therefore
\[
\mathbb P\!\left(\max_iX_i\ge \tau\right)
\le
\mathbb P\!\left(\max_iY_i\ge \tau\right).
\]
Indeed, apply (5) at \(a\uparrow\tau\) and use
\[
\{\max_iX_i<\tau\}
 =\bigcup_{n\ge1}\{\max_iX_i\le\tau-1/n\}.
\]

For a countable index set \(T=\{t_1,t_2,\dots\}\), let
\[
M_{X,n}=\max_{1\le i\le n}X_{t_i},
\qquad
M_{Y,n}=\max_{1\le i\le n}Y_{t_i}.
\]
The finite-dimensional result gives
\[
\mathbb P(M_{X,n}\le a)\ge \mathbb P(M_{Y,n}\le a).
\]
Since
\[
M_{X,n}\uparrow \sup_{t\in T}X_t,
\qquad
M_{Y,n}\uparrow \sup_{t\in T}Y_t,
\]
continuity of probability for decreasing events gives
\[
\mathbb P\!\left(\sup_{t\in T}X_t\le a\right)
\ge
\mathbb P\!\left(\sup_{t\in T}Y_t\le a\right).
\]
The same argument as above proves
\[
\mathbb P\!\left(\sup_{t\in T}X_t\ge\tau\right)
\le
\mathbb P\!\left(\sup_{t\in T}Y_t\ge\tau\right).
\]
For a general separable process, choose a countable subset of \(T\) over which both suprema agree almost surely, reducing to the countable case.

Finally, stochastic domination implies the expectation inequality. More explicitly, if
\[
M_X=\sup_{t\in T}X_t,\qquad M_Y=\sup_{t\in T}Y_t,
\]
then for every increasing bounded function \(\varphi\),
\[
\mathbb E\varphi(M_X)\le\mathbb E\varphi(M_Y).
\]
Approximating the identity function by increasing truncations gives
\[
\boxed{\mathbb E\sup_{t\in T}X_t
       \le
       \mathbb E\sup_{t\in T}Y_t.}
\]
The expectations may be interpreted as extended expectations; their negative parts are finite because, for any fixed \(t_0\),
\[
\sup_{t\in T}X_t\ge X_{t_0},
\qquad
\sup_{t\in T}Y_t\ge Y_{t_0}.
\]

Strictly speaking, for uncountable \(T\) one needs the usual measurability/separability assumption on the suprema. Without it, arbitrary nonseparable modifications can make the literal statement false even when all finite-dimensional distributions agree.

### Library-RAG output

Yes—under the standard assumption that the processes are separable, so their suprema are determined almost surely by countable subsets of \(T\). The finite-dimensional argument is the essential part; the general separable case follows by approximation with finite subsets.  
[STRATEGY: family_standard_theorem_reduction | Reduction to a standard theorem]
Derived according to this strategy: Reduce the process-level statement to a finite-dimensional Gaussian comparison, then recover the supremum by a countable limiting argument.
[/STRATEGY]

## 1. Rewrite the assumptions as a covariance ordering

First suppose \(T=\{1,\dots,m\}\), and write
\[
A_{ij}=\mathbb E[X_iX_j],\qquad B_{ij}=\mathbb E[Y_iY_j].
\]
The equal-variance assumption says
\[
A_{ii}=B_{ii}.
\]
Moreover,
\[
\mathbb E(X_i-X_j)^2=A_{ii}+A_{jj}-2A_{ij},
\]
and similarly for \(Y\). Thus the increment assumption and equality of the diagonal variances give
\[
A_{ij}\ge B_{ij}\qquad(i\ne j).
\]
[STRATEGY: sub_canonical_rewriting | Canonical rewriting]
Derived according to this strategy: Expanding the squared increments converts the variogram inequality into the off-diagonal covariance ordering needed for Gaussian interpolation.
[/STRATEGY]

## 2. Gaussian interpolation

Take independent copies of the Gaussian vectors \(X=(X_1,\dots,X_m)\) and \(Y=(Y_1,\dots,Y_m)\), and define
\[
Z(u)=\sqrt{1-u}\,X+\sqrt u\,Y,\qquad 0\le u\le1.
\]
Its covariance matrix is
\[
C(u)=(1-u)A+uB.
\]

For a \(C^2\) function \(f:\mathbb R^m\to\mathbb R\) with bounded derivatives, Gaussian integration by parts gives
\[
\frac{d}{du}\mathbb E f(Z(u))
   =\frac12\sum_{i,j=1}^m
       (B_{ij}-A_{ij})\,
       \mathbb E\big[\partial_{ij}f(Z(u))\big].
\tag{1}
\]
Indeed, differentiating inside the expectation and applying
\[
\mathbb E[G_i\phi(G)]
   =\sum_j\operatorname{Cov}(G_i,G_j)
        \mathbb E[\partial_j\phi(G)]
\]
to the \(X\)- and \(Y\)-terms yields (1). This identity remains valid for singular covariance matrices, either directly or by adding \(\delta I\) and letting \(\delta\downarrow0\).

[NEW_STRATEGY: Gaussian covariance interpolation and integration by parts]
Why this is new: The retrieved strategies do not cover interpolation between Gaussian covariance matrices or the Gaussian integration-by-parts identity that turns covariance ordering into monotonicity of probabilities.
[/NEW_STRATEGY]

Fix \(a\in\mathbb R\). Choose a smooth nonincreasing function \(h:\mathbb R\to[0,1]\) such that
\[
h(r)=1\quad(r\le0),\qquad h(r)=0\quad(r\ge1).
\]
For \(\varepsilon>0\), put
\[
f_\varepsilon(x_1,\dots,x_m)
   =\prod_{i=1}^m h\left(\frac{x_i-a}{\varepsilon}\right).
\]
For \(i\ne j\),
\[
\partial_{ij}f_\varepsilon(x)
 =\frac1{\varepsilon^2}
   h'\left(\frac{x_i-a}{\varepsilon}\right)
   h'\left(\frac{x_j-a}{\varepsilon}\right)
   \prod_{k\ne i,j}
   h\left(\frac{x_k-a}{\varepsilon}\right)
 \ge0,
\]
because \(h'\le0\). On the other hand,
\[
B_{ii}-A_{ii}=0,\qquad B_{ij}-A_{ij}\le0\quad(i\ne j).
\]
Consequently, (1) gives
\[
\frac{d}{du}\mathbb E f_\varepsilon(Z(u))\le0.
\]
Since \(Z(0)=X\) and \(Z(1)=Y\) in distribution,
\[
\mathbb E f_\varepsilon(Y)\le \mathbb E f_\varepsilon(X).
\tag{2}
\]

As \(\varepsilon\downarrow0\),
\[
f_\varepsilon(x)\longrightarrow
\mathbf 1_{\{\max_i x_i\le a\}}.
\]
By bounded convergence, (2) therefore yields
\[
\mathbb P\left\{\max_iY_i\le a\right\}
 \le
\mathbb P\left\{\max_iX_i\le a\right\}.
\tag{3}
\]
[STRATEGY: family_limits_completeness | Limit, sequence, and completeness methods]
Derived according to this strategy: Smooth orthant indicators are sent to the exact indicator by a bounded pointwise limit, transferring the interpolated inequality to probabilities.
[/STRATEGY]

Equivalently,
\[
\mathbb P\left\{\max_iX_i>a\right\}
 \le
\mathbb P\left\{\max_iY_i>a\right\}.
\tag{4}
\]
To obtain the stated version with \(\ge\), apply (4) at \(a=\tau-1/k\) and let \(k\to\infty\):
\[
\{\max_iX_i\ge\tau\}
 =\bigcap_{k=1}^\infty
   \{\max_iX_i>\tau-1/k\}.
\]
Continuity of probability from above gives
\[
\mathbb P\left\{\max_iX_i\ge\tau\right\}
 \le
\mathbb P\left\{\max_iY_i\ge\tau\right\}.
\tag{5}
\]

## 3. Passage to a general separable index set

Suppose first that \(T=\{t_1,t_2,\dots\}\) is countable, and define
\[
M_{X,n}=\max_{1\le i\le n}X_{t_i},
\qquad
M_{Y,n}=\max_{1\le i\le n}Y_{t_i}.
\]
The finite-dimensional result gives, for every \(a\),
\[
\mathbb P(M_{X,n}\le a)\ge\mathbb P(M_{Y,n}\le a).
\]
Since
\[
M_{X,n}\uparrow \sup_{t\in T}X_t,
\qquad
M_{Y,n}\uparrow \sup_{t\in T}Y_t,
\]
we have
\[
\{M_{X,n}\le a\}\downarrow
 \left\{\sup_{t\in T}X_t\le a\right\},
\]
and likewise for \(Y\). Letting \(n\to\infty\) therefore gives
\[
\mathbb P\left\{\sup_{t\in T}X_t\le a\right\}
 \ge
\mathbb P\left\{\sup_{t\in T}Y_t\le a\right\}.
\]
As above, replacing \(a\) by \(\tau-1/k\) and taking a limit proves
\[
\boxed{
\mathbb P\left\{\sup_{t\in T}X_t\ge\tau\right\}
\le
\mathbb P\left\{\sup_{t\in T}Y_t\ge\tau\right\}.
}
\]
[STRATEGY: sub_monotone_limsup_subsequence | Monotone sequences, limsup, and subsequences]
Derived according to this strategy: The supremum over a countable index set is the monotone limit of finite maxima, allowing the finite-dimensional probability inequalities to pass to the full supremum.
[/STRATEGY]

For a separable process, there is a countable \(T_0\subseteq T\) such that almost surely
\[
\sup_{t\in T}X_t=\sup_{t\in T_0}X_t,
\qquad
\sup_{t\in T}Y_t=\sup_{t\in T_0}Y_t.
\]
Applying the countable result to \(T_0\) proves (7.4).

## 4. Comparison of expectations

Let
\[
U=\sup_{t\in T}X_t,\qquad V=\sup_{t\in T}Y_t.
\]
The stochastic domination implies
\[
\mathbb P(U>u)\le\mathbb P(V>u)
\quad\text{and}\quad
\mathbb P(U<-u)\ge\mathbb P(V<-u)
\qquad(u\ge0).
\]
Choose any \(t_0\in T\). Since \(U\ge X_{t_0}\),
\[
U^-\le X_{t_0}^-,
\]
so \(\mathbb E U^-<\infty\); similarly \(\mathbb E V^-<\infty\). Using the tail formulas
\[
\mathbb E U^+=\int_0^\infty\mathbb P(U>u)\,du,
\qquad
\mathbb E U^-=\int_0^\infty\mathbb P(U<-u)\,du,
\]
we obtain
\[
\mathbb E U^+\le\mathbb E V^+,
\qquad
\mathbb E U^-\ge\mathbb E V^-.
\]
Hence, allowing the expectations to take the value \(+\infty\),
\[
\boxed{
\mathbb E\sup_{t\in T}X_t
\le
\mathbb E\sup_{t\in T}Y_t.
}
\]

[NEW_STRATEGY: Tail integration of stochastic domination]
Why this is new: The retrieved nodes do not explicitly cover converting first-order stochastic domination into expectation comparison through positive- and negative-tail integrals.
[/NEW_STRATEGY]

### Technical qualification

Some separability or essential-supremum convention is necessary. Without it, the statement is false for arbitrary index sets: on \([0,1]\) with Lebesgue measure, let
\[
X_t(\omega)=\mathbf 1_{\{\omega=t\}},\qquad Y_t(\omega)=0.
\]
Every finite-dimensional distribution of \(X\) is identically zero, so both are mean-zero Gaussian processes satisfying (7.3), but pointwise
\[
\sup_tX_t=1,\qquad \sup_tY_t=0.
\]
Standard formulations of Slepian’s inequality therefore assume finite/countable \(T\), separable processes, or suprema understood through countable/essential versions.

### Retrieved strategy nodes

- `sub_order_completeness` — **Suprema, infima, and order completeness**: Apply least-upper-bound and greatest-lower-bound properties to bounded sets, images, limsups, and moduli of continuity.
- `family_standard_theorem_reduction` — **Reduction to a standard theorem**: Modify domains and regularity hypotheses so that a known theorem applies directly.
- `sub_intermediate_value` — **Intermediate Value Theorem**: Use continuity and endpoint value information to produce an intermediate value or interior zero.
- `sub_fundamental_theorem_calculus` — **Fundamental Theorem of Calculus**: Convert derivatives into integral increments or differentiate parameterized integrals.
- `sub_canonical_rewriting` — **Canonical rewriting**: Rewrite abstract distances, norms, slopes, interval interiors, and formal-series expressions in concrete canonical forms.
- `family_extremal_order` — **Supremum, infimum, and extremal arguments**: Control quantities through suprema, infima, extremal points, or attained optimizers.
- `family_limits_completeness` — **Limit, sequence, and completeness methods**: Use epsilon or filter formulations, limit laws, squeezing, completeness, subsequences, and limsup-liminf criteria.
- `sub_sequence_completeness` — **Sequence and completeness methods**: Use epsilon-N arguments, Cauchy completeness, subsequences, and sequences approaching a point.
- `sub_monotone_limsup_subsequence` — **Monotone sequences, limsup, and subsequences**: Use monotone convergence, limsup-liminf characterizations, and extraction of convergent subsequences.
- `sub_mean_value_theorems` — **Fermat, Rolle, and Mean Value Theorems**: Convert extrema or endpoint equalities into derivative information and represent increments by intermediate derivatives.

---

## lemma_2_7_8 — Lemma 2.7.8 (Centering)

Dataset: `high_dimensional_probability`

### Input statement

Lemma 2.7.8 (Centering). Any subgaussian random variable X satisfies
                                    ∥X − E X∥ψ2 ≤ C∥X∥ψ2 .

### Task

Explain the proof strategy and give a proof plan. Identify the main mathematical methods used.

### Control output

Let  
\[
\|X\|_{\psi_2}:=\inf\left\{t>0:\mathbb E\exp(X^2/t^2)\le 2\right\}.
\]
This is the Luxemburg norm associated with \(\psi_2(u)=e^{u^2}-1\), so it satisfies the triangle inequality.

Set \(K=\|X\|_{\psi_2}\). For any \(t>K\),
\[
\mathbb E e^{X^2/t^2}\le 2.
\]
Since \(x\mapsto e^{x^2/t^2}\) is convex, Jensen's inequality gives
\[
e^{(\mathbb EX)^2/t^2}
\le \mathbb E e^{X^2/t^2}
\le 2.
\]
Hence
\[
|\mathbb EX|\le t\sqrt{\log 2}.
\]
For a constant \(a\),
\[
\|a\|_{\psi_2}=\frac{|a|}{\sqrt{\log 2}},
\]
and therefore \(\|\mathbb EX\|_{\psi_2}\le t\). Letting \(t\downarrow K\), we obtain
\[
\|\mathbb EX\|_{\psi_2}\le \|X\|_{\psi_2}.
\]
Finally, by the triangle inequality,
\[
\|X-\mathbb EX\|_{\psi_2}
\le \|X\|_{\psi_2}+\|\mathbb EX\|_{\psi_2}
\le 2\|X\|_{\psi_2}.
\]
Thus the claim holds, with \(C=2\) under this normalization of the \(\psi_2\)-norm.

### Library-RAG output

### Proof

Use the standard Luxemburg definition
\[
\|X\|_{\psi_2}
:=\inf\left\{s>0:\ \mathbb E\exp\!\left(\frac{X^2}{s^2}\right)\le 2\right\}.
\]
Thus it suffices to turn an exponential-moment bound for \(X\) into one for \(X-\mathbb EX\).
[STRATEGY: family_definitional_reformulation | Definitional unfolding and equivalent reformulation]
Derived according to this strategy: The abstract \(\psi_2\)-norm inequality is rewritten as an explicit exponential-moment estimate.
[/STRATEGY]

Fix any \(s>0\) such that
\[
\mathbb E e^{X^2/s^2}\le 2.
\]
In particular, \(X\in L^2\), so \(m:=\mathbb EX\) is well-defined. Since
\[
(X-m)^2\le 2X^2+2m^2,
\]
we have
\[
\begin{aligned}
\mathbb E\exp\!\left(\frac{(X-m)^2}{4s^2}\right)
&\le
\exp\!\left(\frac{m^2}{2s^2}\right)
\mathbb E\exp\!\left(\frac{X^2}{2s^2}\right).
\end{aligned}
\]

Jensen’s inequality, applied to the convex function \(x\mapsto e^{x^2/s^2}\), gives
\[
e^{m^2/s^2}
=e^{(\mathbb EX)^2/s^2}
\le \mathbb E e^{X^2/s^2}\le 2,
\]
and hence
\[
e^{m^2/(2s^2)}\le \sqrt2.
\]
Also, by Cauchy–Schwarz (equivalently, concavity of the square root),
\[
\mathbb E e^{X^2/(2s^2)}
\le \left(\mathbb E e^{X^2/s^2}\right)^{1/2}
\le \sqrt2.
\]
Therefore
\[
\mathbb E\exp\!\left(\frac{(X-\mathbb EX)^2}{(2s)^2}\right)\le 2.
\]
[NEW_STRATEGY: Convexity and Hölder control of exponential moments]
Why this is new: Jensen’s inequality and Cauchy–Schwarz are used to transfer an exponential-moment bound through centering, but no retrieved node specifically covers these probabilistic convexity estimates.
[/NEW_STRATEGY]

By the definition of the \(\psi_2\)-norm,
\[
\|X-\mathbb EX\|_{\psi_2}\le 2s.
\]
Taking the infimum over all admissible \(s\) yields
\[
\boxed{\|X-\mathbb EX\|_{\psi_2}\le 2\|X\|_{\psi_2}}.
\]
Thus the lemma holds with the universal constant \(C=2\) under this normalization of the \(\psi_2\)-norm.

### Retrieved strategy nodes

- `family_standard_theorem_reduction` — **Reduction to a standard theorem**: Modify domains and regularity hypotheses so that a known theorem applies directly.
- `sub_intermediate_value` — **Intermediate Value Theorem**: Use continuity and endpoint value information to produce an intermediate value or interior zero.
- `sub_fundamental_theorem_calculus` — **Fundamental Theorem of Calculus**: Convert derivatives into integral increments or differentiate parameterized integrals.
- `sub_canonical_rewriting` — **Canonical rewriting**: Rewrite abstract distances, norms, slopes, interval interiors, and formal-series expressions in concrete canonical forms.
- `sub_mean_value_theorems` — **Fermat, Rolle, and Mean Value Theorems**: Convert extrema or endpoint equalities into derivative information and represent increments by intermediate derivatives.
- `sub_ordered_field_constructions` — **Ordered-field structure and canonical constructions**: Use ordered-field operations, canonical witnesses, Archimedeanness, completeness, and rational cuts in structural arguments about the reals.
- `family_integral_calculus` — **Integral-calculus arguments**: A broad integration family covering the fundamental theorem, structural integral identities, transformations, and Riemann-sum methods.
- `sub_cardinality_embeddings` — **Cardinality and embedding arguments**: Use injections, diagonalization, Cantor's theorem, interval cardinality, and Cantor-Schroeder-Bernstein.
- `family_definitional_reformulation` — **Definitional unfolding and equivalent reformulation**: Convert abstract statements into explicit definitions, quantified conditions, or standard equivalent formulations.
- `family_normalization_symmetry` — **Normalization, invariance, and symmetry**: Translate, rescale, whiten, permute, or otherwise transform a problem to a canonical case and transfer the conclusion back.

---
