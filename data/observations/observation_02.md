# Observation 02: Five proofs from high-dimensional probability

## Sources, scope, and protocol

The five records are from [test_01/data.json](../test/high_dimensional_probability/test_01/data.json), in their original order. The protocol is the one used in [observation_01.md](observation_01.md).

The records contain extraction artifacts and sometimes run into unrelated subsequent material. In particular, the Hanson–Wright and Slepian records contain opening proof plans rather than completed proofs. Their continuations and supporting lemmas were read in the project's [extracted book text](../test/high_dimensional_probability/pdf_text.txt). The section numbers below refer to that local text. The [author's book page](https://webapps.math.uci.edu/~rvershyn/papers/HDP-book/HDP-book.html) provides bibliographic context; the mathematical decompositions here use the local source and explicitly identified supplementary arguments.

The explanations reconstruct plausible reasons for choosing each move. They do not claim to recover the author's actual discovery process.

### Categories

- **B-definition:** Direct interpretation of a definition.
- **B-calculation:** Substitution, expansion, arithmetic, or execution of a specified elementary calculation.
- **B-logic:** Instantiation or combination of established statements using elementary logic.
- **S:** A strategic choice of representation, intermediate goal, construction, theorem, proof method, or parameter.

**Toolkit use** is an annotation, not an additional basic category. A substantial theorem does not become elementary because we invoke it. Choosing it is strategic; once its hypotheses and inputs are fixed, applying its conclusion is a logical step. Statements such as “B-logic; toolkit: Bernstein” classify the local application, not the proof of Bernstein. Where a verification uses analysis or linear algebra beyond elementary arithmetic, the supporting result is named explicitly.

For each strategic move we explain the **current state**, **what the goal asks for**, **the relevant observation**, and **why the chosen move connects them**. An equivalent goal reformulation is distinguished from a sufficient-condition reduction or a probabilistic bound. Constants c,C denote positive absolute constants and may change between inequalities. The norm of a matrix without a subscript is its Euclidean operator norm.

## 1. Hanson–Wright inequality

**Record:** test_01_01. **Source:** Theorem 6.2.2, with its continuation and Lemmas 6.2.3–6.2.4 in Section 6.2; decoupling from Theorem 6.1.1 and Remark 6.1.2.

### Statement and toolkit

Let A be a real n×n matrix. Let X have independent, mean-zero, subgaussian coordinates, and put K=maxᵢ‖Xᵢ‖ψ₂. Then, for t≥0,

\[
\mathbb P\{|X^TAX-\mathbb EX^TAX|\ge t\}
\le 2\exp\left[-c\min\left\{
\frac{t^2}{K^4\|A\|_F^2},\frac{t}{K^2\|A\|}
\right\}\right].
\]

We treat A=0 or K=0 separately: the centered quadratic form is zero almost surely, so positive-threshold tails vanish and the t=0 bound is trivial. Below the displayed denominators are positive and t>0.

The toolkit includes exponential Markov bounds, Bernstein's inequality, the fact that centered squares of subgaussians are subexponential, decoupling for off-diagonal quadratic forms, the MGF bound for independent mean-zero subgaussian linear combinations, Gaussian MGFs, singular value decomposition (SVD), Gaussian rotation invariance, Jensen's inequality, and elementary norm identities.

### Goal map

Write Q=XᵀAX−E[XᵀAX]. The backward plan is

\[
\text{two-sided tail of }Q
\ \Leftarrow\ \text{upper tails for }Q\text{ and }-Q
\ \Leftarrow\ \text{bounds for diagonal and off-diagonal parts}.
\]

The diagonal branch matches Bernstein. The off-diagonal branch is

\[
\text{tail bound}
\Leftarrow\text{controlled exponential moment}
\Leftarrow\text{decoupled bilinear form}
\Leftarrow\text{Gaussian bilinear form}
\Leftarrow\text{product of scalar Gaussian MGFs}.
\]

These arrows are sufficient estimates, not equivalences or equalities in distribution between the original and replaced random variables.

### Step decomposition

| Step | Action | Category and role |
| --- | --- | --- |
| 1 | Expand Q and use independence and zero means to calculate E[XᵢXⱼ]=0 for i≠j. | **B-definition, B-calculation, B-logic.** Toolkit: expectation factorization for independent variables. |
| 2 | Observe that square terms depend on one coordinate each, while cross terms share coordinates. Choose to separate the diagonal and off-diagonal sums, so each can use a different tool. | **S — split according to dependence structure.** |
| 3 | Verify Q=D+S, where D=Σᵢaᵢᵢ(Xᵢ²−EXᵢ²) and S=Σᵢ≠ⱼaᵢⱼXᵢXⱼ. | **B-calculation.** |
| 4 | Choose to bound the upper tail using the sufficient thresholds D<t/2 and S<t/2; obtain P(Q≥t)≤P(D≥t/2)+P(S≥t/2). | **S** for allocating the threshold; **B-logic** for the event inclusion and union bound. No independence between D and S is asserted. |
| 5 | Observe that D is a sum of independent centered subexponential variables. Select Bernstein's inequality, which has the quadratic/linear tail form appearing in the target. | **S — match the diagonal branch to a concentration theorem.** |
| 6 | Check ‖Xᵢ²−EXᵢ²‖ψ₁≤CK² and substitute into Bernstein. Use Σᵢaᵢᵢ²≤‖A‖F² and maxᵢ∣aᵢᵢ∣≤‖A‖. | **B-logic and B-calculation; toolkit:** square/centering bounds, Bernstein, and matrix norm bounds. |
| 7 | Observe that the desired exponential tail and subgaussian hypotheses suggest exponential moments. Choose the exponential transform and a parameter λ>0 for S. | **S — replace a tail-estimation task by an MGF-estimation task.** |
| 8 | Apply Markov to e^(λS), giving P(S≥t/2)≤e^(−λt/2)E[e^(λS)]. | **B-logic and B-calculation; toolkit: Markov.** |
| 9 | Observe that shared coordinates prevent treating the cross terms as an independent sum. Choose decoupling, introducing an independent copy X′. | **S — change the dependence structure through an inequality.** |
| 10 | Apply the off-diagonal decoupling bound E[e^(λS)]≤E[e^(4λXᵀAX′)]. | **B-logic; toolkit: Remark 6.1.2.** This version allows the full matrix A on the right. |
| 11 | Condition on X′ so that AX′ becomes a fixed coefficient vector; compare the resulting linear-form MGF with the matching Gaussian MGF. Repeat with the other vector. | **S — conditional linearization and Gaussian replacement.** Detailed below. |
| 12 | Execute those conditional MGF comparisons and average to obtain E[e^(4λXᵀAX′)]≤E[e^(CK²λgᵀAg′)]. | **B-logic and B-calculation; toolkit:** subgaussian/Gaussian MGFs and iterated expectation. |
| 13 | Observe that A couples Gaussian coordinates, whereas the goal involves its singular-value norms. Choose SVD and use Gaussian rotation invariance to diagonalize the bilinear form in distribution. | **S — expose independent scalar factors and the target norms.** |
| 14 | Compute the scalar MGFs and multiply them, giving E[e^(λS)]≤exp(CK⁴λ²‖A‖F²) when ∣λ∣≤c₀/(K²‖A‖). | **B-calculation and B-logic** after the representation choice; toolkit: Gaussian MGFs, independence, rotation invariance, and singular-value identities. |
| 15 | Compare the negative linear exponent with the positive quadratic exponent, while respecting the allowed λ range. Choose λ as the smaller of the balancing scale and the permitted cutoff. | **S — parameter selection that explains the two tail regimes.** |
| 16 | Substitute that λ to get the required upper-tail estimate for S and combine with D. Observe that replacing A by −A reverses Q while preserving both matrix norms; choose to reuse the upper-tail argument for the lower tail. | **B-calculation and B-logic** for substitution and combination; **S** for the sign-reversal reduction, verified by direct calculation. |
| 17 | Use the trivial probability bound 1 together with the exponential estimate to absorb the prefactor 4 into 2 by reducing c. | **S** for identifying the two bounds to combine; **B-calculation** for the constant adjustment below. |

### The observations and their verification

**Why separate the diagonal?** The available independence belongs to the coordinates Xᵢ, not to all products XᵢXⱼ. Diagonal terms preserve that independence; off-diagonal products generally do not. Moreover, the available decoupling theorem is specifically designed for off-diagonal terms. The split aligns two different parts of the expression with two different toolkit entries.

For the diagonal part, Bernstein gives

\[
\mathbb P\{D\ge t/2\}
\le \exp\left[-c\min\left\{
\frac{t^2}{K^4\sum_i a_{ii}^2},
\frac{t}{K^2\max_i|a_{ii}|}
\right\}\right]
\le \exp\left[-c\min\left\{
\frac{t^2}{K^4\|A\|_F^2},\frac{t}{K^2\|A\|}
\right\}\right].
\]

If the diagonal is zero, D=0 and this branch is immediate without dividing by its zero norms.

**Why decouple?** “We want a linear combination of independent subgaussian variables with coefficients that can be held fixed. In XᵀAX, fixing one occurrence of X also fixes the other. An independent copy would let us condition on one vector while leaving the other random.” Decoupling rigorously bounds the original exponential moment by that more usable object. It does not say XᵀAX and XᵀAX′ have the same distribution.

The underlying construction also has an observation-based explanation. Introduce independent fair selectors δᵢ and the partial sum

\[
S_\delta=\sum_{i\ne j}\delta_i(1-\delta_j)a_{ij}X_iX_j.
\]

**S — construction:** force the left and right indices into disjoint groups, while arranging that every off-diagonal pair is retained with the same probability. **B-calculation:** Eδ[δᵢ(1−δⱼ)]=1/4 for i≠j, hence S=4EδSδ. **Toolkit application:** Jensen moves the exponential outside this average. For each fixed partition, the two coordinate groups are independent, so replacing the right group by its independent copy preserves that partial sum's distribution. The partial decoupled sum is a conditional expectation of XᵀAX′: the missing terms have conditional mean zero. Another Jensen application therefore bounds it by the full decoupled exponential moment. This explains the factor 4 and why disjoint groups solve the dependence problem.

**Why a Gaussian comparison?** Conditional on X′, set v=AX′. Independence and mean-zero subgaussian coordinates give

\[
\mathbb E_X e^{\lambda\langle X,v\rangle}
\le e^{C K^2\lambda^2\|v\|_2^2}.
\]

The right side has exactly the form of a Gaussian linear-form MGF:

\[
\mathbb E_g e^{\mu\langle g,v\rangle}
=e^{\mu^2\|v\|_2^2/2}.
\]

**Observation:** choosing μ=√(2C)Kλ matches these expressions. This supplies a reason for introducing g, beyond saying that Gaussians are convenient. Average over X′, condition on g, and repeat for X′ to introduce an independent g′. The two comparisons cost a factor of order K² in the exponential parameter.

**Why diagonalize only after replacement?** For a general vector with independent subgaussian coordinates, an orthogonal transformation can destroy coordinate independence. Standard Gaussian vectors retain independent standard coordinates under orthogonal transformations. Thus SVD becomes useful after Gaussian replacement.

Write A=U diag(sᵢ)Vᵀ. Rotation invariance gives

\[
g^TAg'\overset{d}=\sum_i s_i g_i g_i',
\qquad
\mathbb E e^{u g_i g_i'}=(1-u^2)^{-1/2}
\quad (|u|<1).
\]

The last identity follows by conditioning on gᵢ and using the Gaussian linear and square MGFs. The pairs (gᵢ,gᵢ′) are independent over i. For u²≤1/2, the elementary logarithm estimate −log(1−u²)/2≤u² gives

\[
\mathbb E e^{\theta g^TAg'}
\le e^{\theta^2\sum_i s_i^2}
=e^{\theta^2\|A\|_F^2}
\quad\text{when }|\theta|\le\frac{1}{\sqrt2\|A\|}.
\]

The sum of squared singular values controls the exponent; the largest singular value restricts its domain. These are precisely the two matrix norms in the theorem. After all replacements, use |λ|≤c₀/(K²‖A‖), with c₀ adjusted for their constants.

**Why the minimum of two scales?** Put V=K⁴‖A‖F² and L=K²‖A‖. We have

\[
\mathbb P\{S\ge t/2\}\le e^{-\lambda t/2+C\lambda^2V},
\qquad 0<\lambda\le c_0/L.
\]

Choose

\[
\lambda=\min\left\{\frac{t}{4CV},\frac{c_0}{2L}\right\}.
\]

Then Cλ²V≤λt/4, so the exponent is at most −λt/4. Substitution yields −c min(t²/V,t/L). The quadratic regime comes from balancing the two exponent terms; the linear regime comes from the MGF domain restriction.

Finally both tails and both branches give at most 4e^(−cq), where q=min(t²/V,t/L). To recover the displayed factor 2, use

\[
\min\{1,4e^{-cq}\}\le 2e^{-cq/2}.
\]

For q≤2log(2)/c the right side is at least 1; for larger q the exponential comparison applies. Rename c/2 as c.

### What the sample alone leaves out

The JSON record announces decoupling, Gaussian replacement, and diagonalization. It does not include the completed proof, the separate diagonal branch, the MGF parameter restriction, or the tail optimization. The local continuation supplies those stages; the selector explanation and constant bookkeeping above make their motivations and obligations explicit.

## 2. Covariance estimation

**Record:** test_01_02. **Source:** Theorem 4.7.1; the normalized Gram-matrix estimate in Theorem 4.6.1 and Remark 4.6.2. The singular case below fills in the reduction left to an exercise in the source.

### Statement and toolkit

Let X₁,…,Xₘ be independent copies of a random vector X∈ℝⁿ. Set

\[
\Sigma=\mathbb E XX^T,
\qquad
\Sigma_m=\frac1m\sum_{i=1}^m X_iX_i^T.
\]

Assume, for all v∈ℝⁿ,

\[
\|\langle X,v\rangle\|_{\psi_2}
\le K\|\langle X,v\rangle\|_{L^2},\qquad K\ge1.
\]

Then

\[
\mathbb E\|\Sigma_m-\Sigma\|
\le CK^2\left(\sqrt{\frac nm}+\frac nm\right)\|\Sigma\|.
\]

For mean-zero X, Σ is its covariance matrix. As the source explicitly notes, the argument also works without mean zero, with Σ understood as the second-moment matrix defined above. It is not then the covariance centered at EX.

The toolkit contains the spectral theorem and positive square roots, isotropy (E[ZZᵀ]=I), the definition of a subgaussian vector norm as the supremum of directional norms, operator-norm submultiplicativity, and the isotropic subgaussian Gram-matrix estimate

\[
\mathbb E\left\|\frac1m B^TB-I_d\right\|
\le CK^2\left(\sqrt{\frac dm}+\frac dm\right)
\]

for independent isotropic rows with subgaussian norms at most K. This is the expected form in Remark 4.6.2. The squared-projection proof of that Gram-matrix estimate uses isotropy and independent rows, not zero row means, so it applies also to the second-moment formulation here. We use this substantial result as a toolkit theorem rather than re-proving its net and Bernstein argument.

### Goal map

\[
\mathbb E\|\Sigma_m-\Sigma\|
\le\|\Sigma\|\,\mathbb E\|R_m\|,
\qquad
R_m=\frac1m\sum_i Z_iZ_i^T-I.
\]

The goal is to transform the samples so that the error relative to Σ becomes an error relative to I. After that transformation, package the sample outer products as a Gram matrix and apply the toolkit estimate. The norm inequality is a sufficient bound, not an equivalent norm identity.

### Step decomposition

| Step | Action | Category and role |
| --- | --- | --- |
| 1 | Expand the population and sample second-moment definitions. | **B-definition.** |
| 2 | Observe that the available estimate is centered at I, while our target is centered at Σ. Also, the hypothesis measures subgaussian size relative to directional second moments. Choose whitening, Z=Σ^(−1/2)X, first assuming Σ is invertible. | **S — remove the covariance geometry to match the toolkit.** |
| 3 | Compute E[ZZᵀ]=I and X=Σ^(1/2)Z. Apply the same fixed transformation to each sample; independence is preserved. | **B-calculation and B-logic; toolkit:** matrix square roots and preservation of independence under separate measurable maps. |
| 4 | Substitute v=Σ^(−1/2)u into the directional assumption, obtaining ‖〈Z,u〉‖ψ₂≤K‖u‖₂. | **B-calculation and B-logic.** Verifies the subgaussian input required by the chosen theorem. |
| 5 | Choose to factor the error as Σ^(1/2)RₘΣ^(1/2), because the remaining norm can then be compared to the isotropic estimate while the outer factors produce the desired ‖Σ‖. | **S — match the original target's scale to a normalized error.** |
| 6 | Expand to verify the factorization and bound its norm by ‖Σ‖‖Rₘ‖. | **B-calculation and B-logic; toolkit:** submultiplicativity and ‖Σ^(1/2)‖²=‖Σ‖. |
| 7 | Observe that the available theorem concerns BᵀB and that Rₘ contains a sum of sample outer products. Choose B with rows Zᵢᵀ. | **S — recognize a Gram-matrix representation.** |
| 8 | Multiply BᵀB to verify BᵀB=ΣᵢZᵢZᵢᵀ. Apply the isotropic Gram-matrix estimate after the preceding hypothesis checks. | **B-calculation and B-logic; toolkit:** the chosen matrix estimate. |
| 9 | Take expectations in the norm bound and substitute the estimate for Rₘ. | **B-logic and B-calculation.** |
| 10 | If Σ is singular, observe that its kernel consists of directions with zero second moment. Choose to work on its range, where its restriction is invertible. | **S — remove irrelevant directions rather than assume invertibility.** |
| 11 | Verify that samples lie in that range almost surely, apply the same argument in dimension r=rank(Σ), and use r≤n. | **B-calculation and B-logic; toolkit:** the spectral theorem and the zero-expectation property of nonnegative random variables. Details below. |

### Observations and verification

**Why whitening?** “The theorem we can call controls deviation from I. Our target involves Σ, but the assumption already scales each direction by its own second moment. Multiplying by Σ^(−1/2) should make all directional second moments equal to the squared Euclidean length.”

For any u,

\[
\begin{aligned}
\|\langle Z,u\rangle\|_{\psi_2}
&=\|\langle X,\Sigma^{-1/2}u\rangle\|_{\psi_2}\\
&\le K\left(u^T\Sigma^{-1/2}\Sigma\Sigma^{-1/2}u\right)^{1/2}
=K\|u\|_2.
\end{aligned}
\]

The identity E[ZZᵀ]=I follows from the same matrix multiplication. This checks both isotropy and the subgaussian bound rather than treating “whitening works” as an unexplained step.

**Why factor the error?** Once Xᵢ=Σ^(1/2)Zᵢ, the same outer factors occur in every sample term and in Σ itself. Our target also contains ‖Σ‖ as a multiplicative scale. This suggests the representation

\[
\Sigma_m-\Sigma
=\Sigma^{1/2}\left(\frac1m\sum_i Z_iZ_i^T-I\right)\Sigma^{1/2},
\qquad
\|\Sigma_m-\Sigma\|\le\|\Sigma\|\|R_m\|.
\]

Choosing that factorization is strategic, just as factoring out 2 was strategic in the elementary examples. Expanding it to check equality is basic calculation.

**Why build a data matrix?** “The expression I have is a sum of rank-one outer products. The expression my theorem accepts is BᵀB. Matrix multiplication shows that choosing the sample vectors as rows makes those expressions coincide.” After applying the toolkit estimate, the displayed target follows immediately.

**What if Σ is singular?** Let H=range(Σ) and r=dim(H). For every v∈ker(Σ),

\[
\mathbb E\langle X,v\rangle^2=v^T\Sigma v=0.
\]

Thus 〈X,v〉=0 almost surely. Apply this to a finite basis of the kernel and intersect those probability-one events: X∈H almost surely, as are the finitely many samples. If r=0, all the matrices are zero. Otherwise choose an orthonormal basis U for H and set Y=UᵀX. Its second-moment matrix Γ=UᵀΣU is positive definite. The directional subgaussian hypothesis transfers by substituting v=Uu. Apply the invertible argument to Y. Since U is an isometry on ℝʳ,

\[
\|\Sigma_m-\Sigma\|=\|\Gamma_m-\Gamma\|,
\qquad \|\Gamma\|=\|\Sigma\|.
\]

The resulting bound with r in place of n is at least as strong as the stated one.

## 3. Dimension reduction for a finite class of Boolean functions

**Record:** test_01_03. **Source:** Lemma 8.3.14. Its extracted proof runs into the proof of Theorem 8.3.13; that subsequent theorem is not part of this decomposition.

### Statement and toolkit

Let F be a finite class of measurable functions from Ω to {0,1}, with probability measure μ, and suppose distinct functions satisfy ‖f−g‖L²(μ)>ε, where ε>0. For independent samples X₁,…,Xₙ with law μ, define μₙ=n⁻¹ΣᵢδXᵢ. If

\[
n\ge C\varepsilon^{-4}\log|F|,
\]

then with probability at least 0.99, every distinct pair satisfies ‖f−g‖L²(μₙ)>ε/2. For |F|≤1 the pairwise conclusion is vacuous; below M=|F|≥2 and n is a positive integer.

The toolkit includes the definitions of population and empirical L² norms, bounded-variable Hoeffding concentration, the union bound, and elementary probability and arithmetic. Boolean here means {0,1}-valued, as defined in the local source.

### Goal map

\[
\text{all empirical distances exceed }\varepsilon/2
\ \Leftarrow\
\text{all squared-distance errors are at most }\varepsilon^2/4
\ \Leftarrow\
\text{fixed-pair failure bound}\times M^2\le0.01.
\]

Controlling squared-distance errors by ε²/4 is a sufficient condition, stronger than necessary. It is not an equivalent reformulation of the desired separation. Squaring an individual comparison of nonnegative distances is equivalent.

### Step decomposition

| Step | Action | Category and role |
| --- | --- | --- |
| 1 | Expand empirical L² distance: ‖f−g‖L²(μₙ)²=n⁻¹Σᵢ(f−g)(Xᵢ)². | **B-definition.** |
| 2 | Observe that Hoeffding accepts averages, whereas the distance contains a square root. Choose to estimate squared distances and fix one pair first. | **S — expose an average and separate local from uniform control.** |
| 3 | Set h=(f−g)², identify its population mean as ‖f−g‖L²(μ)², and check 0≤h≤1. | **B-definition and B-calculation.** Boolean values give the bound. |
| 4 | Observe that the true squared distance exceeds ε², while the target squared distance need only exceed ε²/4. Choose an error tolerance ε²/4, leaving a positive margin. | **S — choose sufficient accuracy by comparing the two goals.** |
| 5 | Observe that h(Xᵢ) are independent bounded variables. Select Hoeffding to obtain exponentially small fixed-pair failure probability. | **S — match the rewritten expression to concentration.** |
| 6 | Apply Hoeffding at deviation ε²/4, giving probability at most 2exp(−cnε⁴) for an absolute error greater than ε²/4. | **B-logic and B-calculation; toolkit: Hoeffding.** |
| 7 | On the complementary event, calculate the empirical squared distance to be greater than 3ε²/4, hence greater than ε²/4. Take square roots. | **B-calculation and B-logic.** |
| 8 | Observe that the goal requires every pair, but there are at most M² pairs. Choose a union bound over their failure events. | **S — turn fixed-pair control into simultaneous control.** |
| 9 | Apply the union bound to obtain failure probability at most 2M²exp(−cnε⁴). Independence between different pairs is unnecessary. | **B-logic; toolkit: union bound.** |
| 10 | Compare this failure probability with 0.01 and solve for n; use the stated sample-size assumption with sufficiently large C. | **S** for budgeting the total failure probability; **B-calculation** for solving the inequality. |

### Observations and verification

**Why square the distances?** “Our goal concerns a square root, but its square is exactly a sample average of a bounded function. The samples are independent, so that representation has the inputs required by concentration.” The move is motivated by the toolkit's input format.

For a fixed pair, write

\[
\Delta_{f,g}=\frac1n\sum_{i=1}^n h(X_i)-\mathbb Eh(X).
\]

Hoeffding gives

\[
\mathbb P\{|\Delta_{f,g}|>\varepsilon^2/4\}
\le 2e^{-cn\varepsilon^4}.
\]

On the complementary event,

\[
\|f-g\|_{L^2(\mu_n)}^2
\ge\|f-g\|_{L^2(\mu)}^2-\varepsilon^2/4
>3\varepsilon^2/4
>\varepsilon^2/4.
\]

This proves the required strict empirical separation for that pair. The population separation is strict, so the strict conclusion is retained.

**Why does ε⁻⁴ appear?** The tolerance is of order ε² because we are comparing squared distances. Hoeffding squares that tolerance in the exponent, yielding nε⁴. This explains the stated sample-size dependence; it is not a claim that this proof gives the optimal dependence for Boolean functions.

**Why does log M appear?** The fixed-pair error is exponential in nε⁴, but uniform control costs at most M² failures. Requiring

\[
2M^2e^{-cn\varepsilon^4}\le0.01
\]

is equivalent to

\[
cn\varepsilon^4\ge2\log M+\log200.
\]

For M≥2, choose C so that cC≥2+log(200)/log(2). Then n≥Cε⁻⁴log M suffices.

### Extraction correction

The JSON concentration display appears to omit absolute-value bars. A bound only on the positive deviation Δ would not imply the lower bound on empirical distance used next. The argument above explicitly controls |Δ|; a lower-tail bound alone would also suffice. This is a mathematical repair of the extracted formula, not an extra theorem assumption.

## 4. Slepian inequality

**Record:** test_01_04. **Source:** Theorem 7.2.2, the interpolation setup in its record, and the continuation through Lemmas 7.2.4–7.2.6 and Theorem 7.2.7 in the local text. The explicit approximation and limiting details below supplement that presentation.

### Statement, scope, and toolkit

Let (Xₜ) and (Yₜ) be mean-zero Gaussian processes such that for all s,t,

\[
\mathbb EX_t^2=\mathbb EY_t^2,
\qquad
\mathbb E(X_t-X_s)^2\le\mathbb E(Y_t-Y_s)^2.
\]

The conclusion is

\[
\mathbb P\{\sup_tX_t\ge\tau\}
\le\mathbb P\{\sup_tY_t\ge\tau\}
\quad\text{for every real }\tau,
\qquad
\mathbb E\sup_tX_t\le\mathbb E\sup_tY_t.
\]

We first give a complete proof for nonempty finite T, writing X,Y∈ℝᵈ. For an infinite index set, the final paragraph states the approximation conditions and the source's convention; arbitrary uncountable suprema cannot simply be treated as finite maxima without justification.

The toolkit includes the Gaussian covariance description, independent copies, Gaussian integration by parts, the chain and product rules with justified differentiation under expectation, bounded convergence, and the implication from stochastic domination to expectation order. These analytic results are genuine toolkit entries. They are not all elementary algebra merely because their application can be recorded as a short line.

### Goal map

\[
\begin{aligned}
\mathbb P\{\max_iX_i\ge\tau\}\le\mathbb P\{\max_iY_i\ge\tau\}
&\Longleftrightarrow
\mathbb P\{\max_iX_i<\tau\}\ge\mathbb P\{\max_iY_i<\tau\}\\
&\Longleftarrow
\mathbb Ef_\delta(X)\ge\mathbb Ef_\delta(Y)
\quad\text{for suitable approximations }f_\delta\\
&\Longleftarrow
\frac{d}{du}\mathbb Ef_\delta(Z(u))\ge0.
\end{aligned}
\]

The first line is an equivalent event-complement reformulation. The subsequent lines are sufficient reductions requiring the approximation limit and endpoint argument. They are not identities for a fixed approximation parameter.

### Step decomposition

| Step | Action | Category and role |
| --- | --- | --- |
| 1 | Expand each increment variance using zero means and the covariance entries. | **B-calculation.** |
| 2 | Using the equal individual variances, deduce Σˣᵢᵢ=Σʸᵢᵢ and Σˣᵢⱼ≥Σʸᵢⱼ. | **B-calculation and B-logic.** The covariance signs are checked explicitly below. |
| 3 | Observe that the complementary event maxᵢxᵢ<τ is a conjunction of coordinate inequalities. Choose to compare its expected indicator, which has a product representation. | **S — choose an event representation suited to a smooth comparison.** |
| 4 | Verify 1{maxᵢxᵢ<τ}=Πᵢ1{xᵢ<τ} and the reversal of the probability inequality under complements. | **B-definition and B-logic.** |
| 5 | Observe that only the separate laws of X and Y enter the target. Choose independent realizations so that a Gaussian interpolation has no cross-covariance terms. | **S — choose a convenient joint realization.** Toolkit: independent copies preserve the marginal laws. |
| 6 | Observe that the assumptions compare covariance entries. Choose Z(u)=√u X+√(1−u)Y so its covariance moves linearly between the two matrices. | **S — construct an interpolation aligned with the information available.** |
| 7 | Check Z(0)=Y, Z(1)=X and ΣZ(u)=uΣˣ+(1−u)Σʸ. | **B-calculation and B-logic; toolkit:** independent Gaussian sums and covariance rules. |
| 8 | Select Gaussian integration by parts to turn the derivative of an expected smooth test function into covariance differences times its second derivatives. | **S — convert distribution comparison into a sign calculation.** |
| 9 | Execute the interpolation identity proved below. | **B-logic; toolkit:** the derived identity, whose verification uses chain rules, integration by parts, and expectation interchange. |
| 10 | The event indicator is not smooth. Choose a product of smooth decreasing approximations to the coordinate indicators, so it approximates the event and has nonnegative mixed derivatives. | **S — design a test function meeting both the goal and the sign condition.** |
| 11 | Differentiate the chosen product; check its mixed derivatives are nonnegative. The diagonal covariance differences vanish, so the interpolation derivative is nonnegative. | **B-calculation and B-logic; toolkit:** product rule and the interpolation identity. |
| 12 | Use monotonicity between u=0 and u=1, then let the smoothing parameter tend to zero and take event complements. | **B-logic; toolkit:** monotonicity from the derivative and bounded convergence. |
| 13 | Apply the implication from stochastic domination to expectation order. | **B-logic; toolkit:** the signed tail integral formula, or increasing bounded truncations followed by integrability. |
| 14 | For a separable infinite process, choose finite subsets of a countable set determining both suprema, then pass to the limit. | **S** for the finite approximation; **B-logic with convergence tools** for the justified passage. Scope detailed below. |

### Observations and verification

**Why rewrite the assumptions as covariance information?** The law of a centered Gaussian vector is determined by its covariance. Moreover,

\[
\mathbb E(X_i-X_j)^2
=\Sigma^X_{ii}+\Sigma^X_{jj}-2\Sigma^X_{ij}.
\]

Equal individual variances therefore imply

\[
\Delta_{ii}=0,\qquad
\Delta_{ij}\ge0\ (i\ne j),
\qquad\Delta=\Sigma^X-\Sigma^Y.
\]

The useful ordering is entrywise off the diagonal; we do not assume Δ is positive semidefinite. The conversion itself is calculation, while deciding to exploit covariance through an interpolation is strategic.

**Why this interpolation?** “Our data compare covariances, so we want a path whose covariance has a simple derivative equal to their difference. Independent Gaussian sums add covariances with the squares of their coefficients. Square-root coefficients therefore produce the linear covariance path we need.” A path with coefficients u and 1−u would instead produce u²Σˣ+(1−u)²Σʸ.

**Why integration by parts?** Differentiating gives factors Xᵢ and Yᵢ multiplied by derivatives of the test function. Gaussian integration by parts converts exactly that kind of expression into a covariance coefficient and one more derivative. For a smooth bounded f with bounded first and second derivatives, and 0<u<1,

\[
\frac{d}{du}\mathbb Ef(Z(u))
=\frac12\sum_i\mathbb E\left[
\partial_i f(Z(u))
\left(\frac{X_i}{\sqrt u}-\frac{Y_i}{\sqrt{1-u}}\right)
\right].
\]

Condition on Y and apply Gaussian integration by parts in X:

\[
\mathbb E[X_i\partial_i f(Z(u))]
=\sqrt u\sum_j\Sigma^X_{ij}\mathbb E[\partial_{ij}f(Z(u))].
\]

Conditioning on X gives the corresponding formula with Y and √(1−u). Substitution cancels the square-root denominators and yields

\[
\boxed{\frac{d}{du}\mathbb Ef(Z(u))
=\frac12\sum_{i,j}\Delta_{ij}\,
\mathbb E[\partial_{ij}f(Z(u))].}
\]

The choice of integration by parts is strategic. Differentiating the specified composition and substituting the identities executes that choice using the named analytic toolkit. Bounded derivatives and Gaussian first moments justify differentiation on every closed subinterval of (0,1); bounded convergence gives continuity at the endpoints.

**Why a product of decreasing functions?** We need a smooth approximation to the event that every coordinate is below τ. A product preserves that conjunction. The covariance calculation requires nonnegative off-diagonal second derivatives; differentiating two decreasing factors produces a product of two nonpositive derivatives, hence a nonnegative result. The same construction meets both requirements.

Choose a smooth nonincreasing function χ:ℝ→[0,1], equal to 1 on (−∞,−1] and 0 on [0,∞). Set

\[
h_\delta(s)=\chi((s-\tau)/\delta),\qquad
f_\delta(x)=\prod_{i=1}^d h_\delta(x_i),\qquad \delta>0.
\]

For i≠j,

\[
\partial_{ij}f_\delta(x)
=h_\delta'(x_i)h_\delta'(x_j)
\prod_{k\ne i,j}h_\delta(x_k)\ge0.
\]

There is no required sign on the diagonal second derivatives, because Δᵢᵢ=0. Thus the interpolation derivative is nonnegative and

\[
\mathbb Ef_\delta(X)\ge\mathbb Ef_\delta(Y).
\]

As δ↓0, hδ(s)→1{s<τ} at every s, including s=τ where it remains zero. Bounded convergence therefore gives

\[
\mathbb P\{\max_iX_i<\tau\}
\ge\mathbb P\{\max_iY_i<\tau\}.
\]

Taking complements proves the desired ≥τ tail comparison for every real τ. This one-sided smoothing also accommodates zero-variance coordinates and other degeneracies; no assertion that the maximum has an atom-free distribution is needed.

Finite Gaussian maxima are integrable, since their absolute values are bounded by Σᵢ|Xᵢ| or Σᵢ|Yᵢ|. Stochastic domination therefore implies the expected-maximum inequality. A signed tail formula, rather than a formula only for nonnegative random variables, is appropriate here.

### Infinite index sets and source completeness

The JSON stops before the interpolation identity and the smooth test-function construction; those are supplied by the local continuation. The selected smoothing function and the following limit details are explicit supplements.

For actual suprema, assume there is a common countable subset T₀ determining both suprema almost surely. This holds, for example, when both processes have the relevant separability property; the union of their two countable determining sets suffices. Enumerate T₀ and let the finite sets Tₙ increase to it. The finite maxima increase to the corresponding suprema. First express the finite stochastic order using distribution functions P(max≤a), then pass to the limit in these decreasing events. This gives the order for P(sup≤a); approaching τ from below gives the requested order for P(sup≥τ). Using these threshold limits avoids incorrectly assuming that the event “every coordinate is <τ” is identical to “the supremum is <τ” for an infinite set.

For expectations, keep one fixed index in every Tₙ. Each maximum is bounded below by that fixed Gaussian variable, whose negative part is integrable. Monotone convergence after subtracting that variable gives the expected-supremum inequality, with +∞ allowed. Separately, Remark 7.2.1 in the local source defines expected supremum through the supremum of expected finite maxima to avoid measurability issues; under that convention its expectation comparison follows directly from the finite result. Without an approximation convention or suitable measurable, separable versions, the finite proof alone is not a proof of the assertion for arbitrary uncountable samplewise suprema.

## 5. Centering a subgaussian random variable

**Record:** test_01_05. **Source:** Lemma 2.7.8; the unrelated subsequent discussion of subexponential distributions is excluded.

### Statement and toolkit

For every subgaussian random variable X,

\[
\|X-\mathbb EX\|_{\psi_2}\le C\|X\|_{\psi_2}.
\]

The source uses the norm

\[
\|W\|_{\psi_2}
=\inf\{s>0:\mathbb E\exp(W^2/s^2)\le2\}.
\]

The toolkit includes its norm triangle inequality and homogeneity, Jensen's inequality for absolute value, and the subgaussian moment bound ‖X‖Lp≤C√p‖X‖ψ₂ for p≥1. In particular, EX exists because the p=1 bound gives integrability. The triangle inequality is an established property of this norm, not something obtained by simply expanding its definition.

### Goal map

\[
\|X-\mathbb EX\|_{\psi_2}
\le\|X\|_{\psi_2}+\|\mathbb EX\|_{\psi_2}.
\]

The first term already matches the target. The remaining branch is

\[
\|\mathbb EX\|_{\psi_2}
\le C_0|\mathbb EX|
\le C_0\mathbb E|X|
\le C_1\|X\|_{\psi_2}.
\]

Each inequality is a sufficient estimate. The point is to connect a norm of a deterministic quantity to a moment already controlled by subgaussianity.

### Step decomposition

| Step | Action | Category and role |
| --- | --- | --- |
| 1 | Check that the subgaussian moment bound at p=1 guarantees EX is defined and finite. | **B-logic; toolkit:** the moment bound. |
| 2 | Observe that the target norm contains a difference, and one of its two components is exactly the random variable whose norm is available. Choose the triangle inequality to separate the correction term. | **S — isolate the only new quantity requiring control.** |
| 3 | Apply the triangle inequality and homogeneity to obtain ‖X−EX‖ψ₂≤‖X‖ψ₂+‖EX‖ψ₂. | **B-logic; toolkit:** norm properties. |
| 4 | Observe that EX is deterministic, so its subgaussian norm can be computed from a constant random variable. Choose this reinterpretation of the remaining goal. | **S — use deterministic structure to simplify a probabilistic norm.** |
| 5 | Calculate ‖a‖ψ₂=∣a∣/√log 2 for a constant a; apply this with a=EX. | **B-definition and B-calculation.** |
| 6 | Observe that we now need ∣EX∣, whereas the toolkit bounds moments of ∣X∣. Choose Jensen to connect the signed expectation to the absolute first moment. | **S — bridge the current quantity to the available moment estimate.** |
| 7 | Apply ∣EX∣≤E∣X∣ and identify E∣X∣=‖X‖L¹. | **B-logic and B-definition; toolkit:** Jensen. |
| 8 | Match this first moment to p=1 in the subgaussian moment estimate. | **S — select the relevant instance of the toolkit bound.** |
| 9 | Substitute the p=1 bound, combine the inequalities, and absorb numerical factors into C. | **B-logic and B-calculation.** |

### Observations and verification

**Why split the norm?** “The goal contains X minus a deterministic correction. The norm of X is already controlled, and a norm inequality can isolate the correction as a separate, simpler subgoal.” This explains why triangle inequality helps rather than merely naming it.

**Why inspect constants?** The notation ‖EX‖ψ₂ looks like another probabilistic norm, but EX has no randomness left. For a constant a≠0, the norm condition becomes

\[
e^{a^2/s^2}\le2
\quad\Longleftrightarrow\quad
s\ge\frac{|a|}{\sqrt{\log2}}.
\]

For a=0 the norm is zero, so the same formula holds. Recognizing that the input is constant suggests the calculation; solving the resulting scalar inequality is basic.

**Why Jensen and then a moment bound?** “We have reached |EX|. The subgaussian toolkit controls E|X| through its p=1 moment bound. Jensen supplies the missing connection in the correct direction.” Consequently,

\[
\|\mathbb EX\|_{\psi_2}
=\frac{|\mathbb EX|}{\sqrt{\log2}}
\le\frac{\mathbb E|X|}{\sqrt{\log2}}
\le C_1\|X\|_{\psi_2}.
\]

Combining this with triangle inequality gives the theorem. No independence assumption or mean-zero assumption on X is needed.

## Comparison of the five decompositions

| Result | Current obstacle | Observation connecting it to the goal | Main strategic choices |
| --- | --- | --- | --- |
| Hanson–Wright | Products share coordinates, and the desired tail depends on two matrix norms. | An independent copy permits conditional linear-form bounds; Gaussian rotation then exposes singular values. | Separate the diagonal, use exponential moments, decouple, replace by Gaussians, diagonalize, choose λ. |
| Covariance estimation | The available matrix estimate is normalized at I, while the error is centered at Σ. | The hypothesis already scales directional subgaussianity by the corresponding second moment. | Whiten, factor out covariance scale, form a Gram matrix, restrict to the covariance range if necessary. |
| Dimension reduction | Every empirical pairwise distance must remain separated. | Squared distances are bounded sample averages; the number of pairs is finite. | Control squared errors, allocate an error margin, use concentration and a union bound. |
| Slepian | Covariance information must imply an ordering of maximum probabilities. | Covariance differences have a sign, and a product approximation to the complementary event has matching mixed-derivative signs. | Choose a complementary event, construct a covariance interpolation, use integration by parts, design a smooth product. |
| Centering | The norm of a centered variable contains a new correction term. | That correction is deterministic, and its size is bounded by a moment already controlled by subgaussianity. | Split with triangle inequality, compute a constant's norm, connect to the first moment. |

Across these examples, an explanation such as “apply decoupling,” “whiten,” or “use interpolation” gives the move without the observation that makes it discoverable. The relevant explanation names both the obstacle in the current state and the feature required by the target or by a useful toolkit entry.

The classifications also depend on the granularity of the action. Selecting a representation or theorem is strategic; checking a chosen identity or instantiating a verified theorem is a separate basic action. The toolkit statements remain substantial mathematical dependencies even when their final applications are logical steps. This keeps the observation-based protocol from hiding an entire strategy inside the phrase “by a standard theorem.”
