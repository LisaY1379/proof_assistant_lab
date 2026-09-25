# Missing HDS Book Text Report

## Summary

- Total records: 58
- Both statement and proof: 51
- Statement but no proof: 7
- Proof but no statement: 0
- Neither statement nor proof: 0

## statement_but_no_proof

Count: 7

### 6. corollary_1_7_linear_combination_tail

- Book name: Corollary 1.7
- Kind: corollary
- Location: Section 1.2
- Official Lean declaration: corollary_1_7_linear_combination_tail
- Source file: `—`
- Statement length: 1058
- Proof length: 0
- Statement excerpt: **Corollary 1.7.** Let \(X_1, \ldots, X_n\) be \(n\) independent random variables such that \(X_i \sim \operatorname{subG}(\sigma^2)\). Then for any \(a \in \mathbb{R}^n\), we have  \[ \mathbb{P}\left(\sum_{i=1}^n a_i X_i > t \right) \leq \
- Comment excerpt: *Corollary 1.7 (two-sided form).** Combined upper- and lower-tail bounds for `∑ aᵢXᵢ` when the `Xᵢ` are independent sub-Gaussian variables with proxy `σ²`.

### 8. theorem_1_9_sample_mean

- Book name: Theorem 1.9 (Hoeffding's inequality)
- Kind: theorem
- Location: Section 1.2
- Official Lean declaration: theorem_1_9_sample_mean
- Source file: `—`
- Statement length: 2621
- Proof length: 0
- Statement excerpt: **Theorem 1.9 (Hoeffding’s inequality).** Let \(X_1, \ldots, X_n\) be \(n\) independent random variables such that almost surely, \[ X_i \in [a_i, b_i], \quad \forall i. \]  Let \(\bar{X} = \frac{1}{n} \sum_{i=1}^n X_i\). Then for any \(t>0
- Comment excerpt: *Theorem 1.9 (Hoeffding's inequality for the sample mean).** Combined two-sided tail bound: for independent `X_i ∈ [a_i, b_i]`, `max(P(X̄ - E X̄ > t), P(X̄ - E X̄ < -t)) ≤ exp(-2 n² t² / ∑ (b_i - a_i)²)`.

### 14. SubGaussianPolytope.theorem_1_16

- Book name: Theorem 1.16
- Kind: theorem
- Location: Section 1.4
- Official Lean declaration: SubGaussianPolytope.theorem_1_16
- Source file: `—`
- Statement length: 2330
- Proof length: 0
- Statement excerpt: **Theorem 1.16.** Let \( P \) be a polytope with \( N \) vertices \( v^{(1)}, \ldots, v^{(N)} \in \mathbb{R}^d \), and let \( X \in \mathbb{R}^d \) be a random vector such that the random variables \(\langle v^{(i)}, X \rangle\), \( i = 1,\
- Comment excerpt: Theorem 1.16 (combined): for a polytope with vertex set `S` whose vertex processes are `σ²`-sub-Gaussian, both the sup and the absolute-value sup of `g ω ·` over `conv(S)` satisfy logarithmic expectation bounds and Gaussian tail bounds.

### 22. cor_2_8_mse_prob

- Book name: Corollary 2.8
- Kind: corollary
- Location: Chapter 2, Section 2.2
- Official Lean declaration: cor_2_8_mse_prob
- Source file: `—`
- Statement length: 776
- Proof length: 0
- Statement excerpt: **Corollary 2.8.** Under the assumptions of Theorem 2.6, for any \(\delta > 0\), with probability at least \(1 - \delta\), it holds that  \[ \text{MSE}(X \hat{\theta}^{\text{ls}}_{B_0(k)}) \leq \frac{\sigma^2 k}{n} \left( \log \frac{e d}{2 
- Comment excerpt: *Corollary 2.8**: High-probability MSE bound for sparse least-squares estimators under sub-Gaussian noise; with probability at least `1 - δ`, the in-sample MSE is controlled by a sparsity-times-log-dimension term.

### 46. Cor49.corollary_4_9

- Book name: Corollary 4.9
- Kind: corollary
- Location: Section 4.4
- Official Lean declaration: Cor49.corollary_4_9
- Source file: `—`
- Statement length: 2554
- Proof length: 0
- Statement excerpt: Corollary 4.9. Let \(X_1, \ldots, X_n\) be \(n\) i.i.d. copies of a sub-Gaussian random vector \(X \in \mathbb{R}^d\) such that \(\mathbb{E} X X^\top = \Sigma\) and \(X \sim \operatorname{subG}_d(k \Sigma_{\text{op}})\). Assume further that
- Comment excerpt: *Corollary 4.9 (PCA under spiked covariance).** There is a universal constant `C > 0` such that for all `n` i.i.d. sub-Gaussian samples `X₁, …, Xₙ` from a spiked covariance model `Σ = θ v v^⊤ + I_d` with `X ~ subG_d(‖Σ‖_op)`, the top eigenv

### 55. GaussianSequenceModel.minimax_rate

- Book name: Corollary 5.13
- Kind: corollary
- Location: Section 5.5
- Official Lean declaration: GaussianSequenceModel.minimax_rate
- Source file: `—`
- Statement length: 1169
- Proof length: 0
- Statement excerpt: Corollary 5.13. The minimax rate of estimation over \(\mathbb{R}^d\) in the Gaussian sequence model is \(\varphi(\mathbb{R}^d) = \frac{\sigma^2 d}{n}\). Moreover, it is attained by the least squares estimator \(\hat{\theta}_{\mathrm{ls}} = 
- Comment excerpt: *Corollary 5.13** (minimax rate over `ℝ^d`): the minimax rate of estimation in the Gaussian sequence model on `ℝ^d` is `φ(ℝ^d) = σ² d / n`, matched up to constants by a Fano lower bound and attained exactly by the least squares (identity) e

### 57. Cor_5_15.cor_5_15

- Book name: Corollary 5.15
- Kind: corollary
- Location: Chapter 5
- Official Lean declaration: Cor_5_15.cor_5_15
- Source file: `—`
- Statement length: 1511
- Proof length: 0
- Statement excerpt: **Corollary 5.15.** Recall that \( B_0(k) \subset \mathbb{R}^d \) denotes the set of all \(k\)-sparse vectors in \(\mathbb{R}^d\). The minimax rate of estimation over \(B_0(k)\) in the Gaussian sequence model is \[ \varphi(B_0(k)) = \sigma^
- Comment excerpt: *Corollary 5.15** (`k`-sparse minimax rate): for the `k`-sparse `ℓ⁰`-ball `B₀(k) ⊂ ℝ^d`, the minimax rate of estimation in the Gaussian sequence model is `φ(B₀(k)) = σ² k log(e d / k) / n`, attained (up to constants) by the constrained leas

## neither_statement_nor_proof

Count: 0

None.

## proof_but_no_statement

Count: 0

None.
