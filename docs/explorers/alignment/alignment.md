# Critical-step alignment across five proof explorers

**Finding:** the saved “no worked replacement” flag captures **4 of 8 AI-selected steps (50.0%)**. The strongest positive overlap is Slepian’s interpolation/cutoff pair. Hanson–Wright decoupling illustrates the opposite pattern: an intuitively central move has a source-assisted replacement. Current ablation replaceability is therefore an incomplete proxy for the kind of difficulty highlighted by the AI.

The data are the saved step selections and alternative-proof annotations from the five explorers.

## Highlights: what the alignment reveals

**The most revealing disagreement is Hanson–Wright decoupling; the strongest positive alignment is Slepian’s interpolation and mixed-derivative sign argument.** Slepian’s limit steps provide a different insight: an essential justification can matter even when it is absent from a shortlist of inventive moves.

| Case | Why the finding matters | What the evidence establishes |
|---|---|---|
| **Hanson–Wright: decoupling** | A conceptually central move has a published, source-assisted replacement. Replaceability alone does not measure discovery difficulty. | The baseline flag misses this AI-selected step. Excluding explicitly literature-assisted successes changes its classification, but does not measure how hard independent rediscovery would be. |
| **Slepian: interpolation and the product cutoff** | Together they connect the covariance assumptions to a signed derivative and then to probability comparison. This is the clearest positive alignment in these records. | Both steps are AI-selected and have no recorded worked replacement. The broad interpolation ban and non-independent judgments limit what that agreement proves. |
| **Covariance and Boolean dimension reduction: simultaneous control** | A bound for one direction or one pair does not establish the uniform conclusion. These captures locate where the argument acquires its full scope. | Recorded substitutes lose the required bound or leave simultaneous control unproved; no exhaustive replacement search was conducted. |
| **Slepian: smoothing and separable-limit passages** | These passages complete the stated theorem, handling boundary atoms and the transition from finite restrictions to infinite suprema. They expose logical obligations beyond the main inventive idea. | Each current study contains only one invalid candidate. This demonstrates a gap in that candidate, not that the original limit method is irreplaceable or unusually difficult. |

**Do not treat the limit-step flags as automatic false positives.** The AI selection is sparse: an unselected step can still be important. Conversely, a failed shortcut does not establish a difficult search bottleneck. Recognizing a necessary justification and establishing the difficulty of replacing its method are different achievements.

The useful question is **why a step matters**: does it introduce the central idea, preserve the strength of the bound, complete a necessary logical passage, or have a replacement that relies on substantial external knowledge? The current records support qualitative distinctions among these roles, not a shared numerical difficulty score.

**Decoupling reveals what binary replaceability misses; Slepian’s limits reveal what a narrow “most ingenious step” judgment misses.** Both agreements and disagreements can therefore improve the explanation of a proof.

## 1. What is being compared

- **I (editorial importance):** the step appears in the saved AI-selected key-step proof. Each step is coded by membership in that selection.
- **U (current replacement gap):** the step has **no recorded worked alternative** satisfying its recorded restriction and target. For the portable pages, worked means `closed` or `rejoined`; for Hanson–Wright, it is the curated `worked` status. Failed, unresolved and budget-exhausted candidates do not count as worked successes.
- **Reading U:** U=1 identifies a replacement gap among the recorded candidates under the specified ban.
- **Costs:** existence of a written proof, its estimate quality, required toolkit, verification work, and discovery effort are different variables. The cost annotations describe mathematical work and estimate quality.

The unit is one **grouped reference action**: 14 Hanson–Wright actions plus 6 covariance, 4 dimension-reduction, 6 Slepian and 4 centering actions, for **34 rows**. Group sizes and ban scopes differ. The comparison concerns the five current explorers: the existing Hanson–Wright reference proof and four expansions of final Library-RAG answers from `test_3node_rag_2`. It is not a comparison of the control and RAG systems’ ability to find critical steps, and the Hanson–Wright reference is not asserted to be that batch’s identical answer. Separate first-move pilot logs are not pooled into this audit.

## 2. Alignment by theorem

| Proof | AI-selected steps | No worked replacement | Overlap | Interpretation |
|---|---|---|---|---|
| Hanson–Wright | Decoupling (`decouple`) | Diagonal/off-diagonal separation (`expand`) | 0/1 AI selections | Disagreement at the named move; agreement is possible at a broader mechanism. |
| Covariance estimation | Scalar concentration (`a2`); Finite-net uniformization (`a3`) | Finite-net uniformization (`a3`) | 1/2 AI selections | Partial overlap: uniformization aligns, the Bernstein call does not. |
| Dimension reduction for Boolean functions | One-pair concentration (`a2`); Simultaneous control (`a3`) | Simultaneous control (`a3`) | 1/2 AI selections | Partial overlap: simultaneous control aligns; the particular scalar bound is replaceable. |
| Slepian’s inequality | Interpolation (`a2`); Product cutoff (`a3`) | Interpolation (`a2`); Product cutoff (`a3`); Smoothing limit (`a4`); Separable limit (`a5`) | 2/2 AI selections | The strongest positive overlap, with two additional technical flags. |
| Centering a subgaussian variable | Centered-square bound (`a3`) | None | 0/1 AI selections | No binary overlap; the AI names a local explanatory choice, not an irreplaceable step. |

## 3. Aggregate descriptive counts

| Saved annotations | AI selected | AI not selected | Total |
|---|---:|---:|---:|
| U=1: no worked replacement | 4 | 3 | 7 |
| U=0: a worked replacement exists | 4 | 23 | 27 |
| Total | 8 | 26 | 34 |

- **Coverage of AI selections by U:** 4/8 = **50.0%**.
- **Share of U flags also selected by AI:** 4/7 = **57.1%**.
- **Positive-set overlap (Jaccard):** 4/11 = **36.4%**.
- Overall label agreement is 27/34 = 79.4%, but **23 rows are jointly unflagged**. This number is dominated by negatives and should not be presented as critical-step detection accuracy.

These ratios summarize agreement between the two saved labels. Several rows share a proof or alternative route and are therefore dependent.

## 4. Read the disagreements mathematically

### Hanson–Wright: Disagreement at the named move; agreement is possible at a broader mechanism.

The AI selects **decouple**: dependent cross terms become a bilinear expression with independent inputs, making conditional linear-form control usable. The ablation flag instead selects **expand**, because the recorded whole-form polarization route loses the sharp matrix-norm dependence and no sharp continuation is supplied.

Decoupling’s successful replacement is **literature-assisted coordinate Gaussianization**. The notes attribute it to Ziemann (2025), §2, with an adaptation to the current assumptions. That route preserves the core opportunity—linearity in one coordinate after conditioning—while replacing the random-block construction. It retains a Gaussian comparison dependency. Thus existence of a replacement is compatible with the AI’s claim that decoupling is a major conceptual bridge in the original proof. The n comparisons describe the construction of the alternative proof.

The `expand` flag is a useful structural warning, but it does not show that diagonal/off-diagonal separation is the most inventive action or that every separation-free proof fails. Many other green steps reuse the same absolute-moment route. In particular, `gaussian` and `replace` describe one family at two locations. Both entries reuse the same route.

A natural next audit is the **joint decoupling + Gaussian-comparison ban**: each single-step bypass currently retains machinery from the other family. Its outcome is unmeasured and unresolved here.

### Covariance estimation: Partial overlap: uniformization aligns, the Bernstein call does not.

The AI selects **a2 (fixed-direction concentration)** and **a3 (finite-net uniformization)**. Only a3 has no worked replacement in the saved candidates. The Frobenius route gives a certificate of order r/√m rather than √(r/m) in the relevant regime; the net-free matrix-moment proposal is unfinished. This supports flagging the passage from scalar to uniform control for further investigation, but establishes no net-free impossibility.

For a2, the ban removes a **black-box Bernstein invocation**, while explicitly allowing its exponential-moment mechanism to be derived from moments. The green branch performs that derivation. It replaces the theorem call while preserving the strategy the AI regarded as important. This is principally a mismatch in the level at which the labels operate, not evidence that sharp scalar concentration is unnecessary.

The direct-coordinate argument bypasses the isotropic detour, whitening, and the norm sandwich at the same n-based rate. The same route appears under a1, a5, and a6; it is one reusable global bypass. The binary table counts attached step records; a route can appear under several steps.

### Dimension reduction for Boolean functions: Partial overlap: simultaneous control aligns; the particular scalar bound is replaceable.

The AI selects **a2 (one-pair exponential concentration)** and **a3 (simultaneous control)**. The ablation flag selects a3 alone. Keeping a fixed-pair guarantee cannot discharge the “every pair” quantifier, and the proposed replacement by a direct uniform empirical-process argument remains unfinished.

The source-assisted Bernoulli-disagreement argument replaces additive Hoeffding at a2 and the bounded-square route at a1. The saved argument gives sufficient sample size proportional to ε⁻² log|F|, versus ε⁻⁴ log|F| in the baseline, and explicitly propagates constants to the original universal-C statement. This is a genuine rate improvement in the recorded derivation. It still uses exponential concentration and finite aggregation; it does not remove those strategy families.

The source record says the Chernoff bound was **checked against MIT lecture notes**. This is more limited provenance than claiming the entire alternative was first discovered through search. Both are currently colored literature-assisted, so source-exclusion sensitivity must not be interpreted as a historical discovery experiment.

The a4 ban forbids the particular constant C=128 while the theorem permits an unspecified universal C. Its replacement by another constant is a bookkeeping test, not a meaningful ingenuity test.

### Slepian’s inequality: The strongest positive overlap, with two additional technical flags.

The AI selects **a2 (Gaussian interpolation)** and **a3 (product cutoff with nonnegative mixed derivatives)**. Both have no worked replacement under the saved broad bans. Interpolation converts a covariance difference into a derivative of an expectation; the product cutoff represents the lower-orthant event and gives the mixed derivatives the required sign. These two steps form a coupled bridge from hypotheses to the full distributional conclusion.

The a2 restriction forbids all Gaussian interpolation and covariance-deformation implementations. A density-free integration-by-parts derivation is worked out in the supplemental note, but still interpolates, so it is correctly excluded from success under that ban. A soft-max argument that proves only an expected-maximum comparison does not close the stronger stochastic-domination goal. The selected theorem includes both tail and expectation conclusions; weakening the target would change this audit.

The ablation flag also selects **a4 (remove smoothing)** and **a5 (pass to separable suprema and closed tails)**. Each has only one recorded candidate, and that candidate is invalid: unjustified CDF continuity in the presence of atoms, or unjustified continuity over arbitrary uncountable intersections. These examples expose necessary rigor but are weak evidence about whether good alternatives exist. Neither is an exhaustive replacement search. They can be technically important without being the main conceptual breakthrough.

Accordingly, the records align well on a2–a3 and overflag a4–a5 **relative to the sparse editorial selection**, not relative to an independently known truth about difficulty.

### Centering a subgaussian variable: No binary overlap; the AI names a local explanatory choice, not an irreplaceable step.

The AI selects **a3 (split the centered square and control the exponential moment)**. Every step has a worked replacement. At a3, convexity of the Orlicz function proves the needed triangle bound with the same constant 2; it changes the presentation of the centering argument while retaining a general convexity mechanism.

Elsewhere, a second-moment mean bound replaces exponential Jensen at the worse constant √8. That still proves the stated universal-C theorem, although it would not prove a target requiring exactly C=2. The positive-norm attainment route replaces the open-scale/limit presentation and is reused under a1 and a4.

There is no contradiction in choosing the most instructive local move of a short proof even when that move has a comparably short replacement. The current selection machinery requires at least one critical step, so centering’s nonempty selection cannot be taken as evidence that every theorem has a substantial bottleneck. Future editorial labeling should allow **“no exceptional critical step”**.

## 5. Sensitivity to provenance and ban scope

| Coding rule | U flags | Also AI-selected | AI-selection coverage | Positive-set overlap |
|---|---:|---:|---:|---:|
| Saved bans; all recorded worked replacements count | 7 | 4 | 4/8 (50.0%) | 36.4% |
| Exclude explicitly literature-assisted successes | 10 | 6 | 6/8 (75.0%) | 50.0% |
| Narrow only Slepian a2 to density/Fourier differentiation | 6 | 3 | 3/8 (37.5%) | 27.3% |

The second row changes three step records: **Hanson–Wright decouple and dimension-reduction a1/a2**. It discards their only explicitly source-assisted success, leaving no counted replacement. Two of the three are AI-selected, so selected-step coverage rises to 75.0%. The two dimension records reuse the same method. This row recomputes the counts after filtering the same saved annotations by source provenance.

The third row recomputes the counts under a narrower ban. Under a density-only ban, the recorded integration-by-parts argument is admissible and a2 is replaceable. Under the actual broad interpolation ban it is not. Coverage would fall to 37.5%. This illustrates why a theorem-call ban and a mechanism ban cannot be mixed in a difficulty score.

Cost descriptions record the required toolkit, proof steps, and changes in the estimates.

## 6. How the annotations were constructed

1. **The two labels are not independent.** The four newer critical selections were authored with knowledge of the ablations; their saved rationales explicitly discuss the alternatives. Hanson–Wright has a recorded dedicated-agent selection, but this record does not establish blinded or pre-ablation elicitation. The selections and ablations share information.
2. **Selection is constrained.** The current pipeline requires at least one critical action. That can manufacture a positive label for a proof with no exceptional bottleneck. The UI selections are also sparse; absence from the shortlist is not a negative difficulty judgment.
3. **Ban granularity varies.** Covariance a2 bans a toolkit invocation, Slepian a2 bans a broad mechanism, Slepian a1 recodes the same sign calculation, and dimension a4 excludes one numerical constant. Different questions produce different replacement rates.
4. **Candidate quality and coverage vary.** Some U flags follow from one obviously invalid proposal rather than several serious attempted replacements. The Slepian a4/a5 flags are examples. They are candidates for further analysis, not established hard nodes.
5. **Alternative annotations.** Worked routes list their assumptions, constants, toolkit, and source references.
6. **Strategies can substitute for one another.** A global moment route can bypass several nodes, while depending on another node being available. Single-node tests miss joint bottlenecks. Duplicate branches and neighboring nodes are correlated.
7. **Target fidelity matters.** A scalar-vs-uniform bound, expectation-vs-distribution comparison, lost dimension factor, or exact-vs-universal constant can change the outcome. “Finite proof length” does not establish that a searcher discovers it under a finite fixed budget.

## 7. What the report supports

**Supported:** among the saved examples, intuitive importance and recorded nonreplaceability overlap only partially. Alignment is most informative when the ban targets the same conceptual mechanism as the AI’s explanation. Retrieval can supply a mathematically valid bypass of a conceptually central move. Essential technical transitions can be flagged without being the main inventive insight.


For the next version, keep separate labels for **conceptual importance**, **replacement evidence**, **source dependence**, and **mathematical cost**. A useful qualitative assessment is:

| Candidate family | Assessment supported now | Missing evidence |
|---|---|---|
| Hanson–Wright decoupling / conditional linearity | High editorial importance; source-assisted replacement exists | Blinded rediscovery cost; joint ban with Gaussian comparison |
| Covariance uniformization | Editorial importance and current replacement gap align | A serious audited net-free competitor at the same rate |
| Boolean simultaneous control | Editorial importance and current replacement gap align | Uniform replacement under a precise family-level ban |
| Slepian interpolation + orthant test | Strongest positive overlap in these records | Independent serious alternatives; blinded search costs |
| Slepian smoothing / separable-limit passage | Technical obligations with weak replacement-search coverage | Better candidates before assigning strategic criticality |
| Centering square split | Useful explanatory choice; same-constant replacement exists | Evidence for any exceptional bottleneck; allow “none” |

A subsequent validation study should freeze the target, toolkit and semantic ban; elicit a ranked AI judgment **before** revealing alternatives, allowing “none”; use separate blinded review; run matched unrestricted/restricted searches under the same budgets; separate retrieved from non-retrieved conditions; and report success probabilities and censored costs alongside verification costs. Joint strategy-family ablations should supplement individual nodes.

## Appendix A. Complete step-level ledger

I=yes means selected for the key-step edition; U=yes means no recorded worked replacement. “Both” and “only” describe overlap between these labels. Exact bans, successful routes, costs, provenance and source fingerprints are also exported in `alignment.json`.

| Proof | Action | AI selected (I) | Replacement gap (U) | Recorded evidence | Alignment |
|---|---|---|---|---|---|
| Hanson–Wright | `sign` · One tail is enough to work on. | no | no | Worked replacement | Neither |
| Hanson–Wright | `expand` · Read the quadratic form coordinate by coordinate. | no | yes | No worked replacement established | Ablation only |
| Hanson–Wright | `split` · Give the two kinds of terms different jobs. | no | no | Worked replacement | Neither |
| Hanson–Wright | `bernstein` · Close the diagonal branch with Bernstein. | no | no | Worked replacement | Neither |
| Hanson–Wright | `exponential` · Ask for an exponential moment instead of a tail. | no | no | Worked replacement | Neither |
| Hanson–Wright | `linear` · Prepare the linear-form bound. | no | no | Worked replacement | Neither |
| Hanson–Wright | `decouple` · Make one side possible to hold fixed. | yes | no | Worked, source-assisted | AI only |
| Hanson–Wright | `gaussian` · Recognize a Gaussian formula inside the bound. | no | no | Worked replacement | Neither |
| Hanson–Wright | `replace` · Carry out the two Gaussian replacements. | no | no | Worked replacement | Neither |
| Hanson–Wright | `rotate` · Rotate until the matrix exposes independent products. | no | no | Worked replacement | Neither |
| Hanson–Wright | `compute` · Compute the scalar MGF and its domain. | no | no | Worked replacement | Neither |
| Hanson–Wright | `meet` · The derived MGF meets the requested MGF. | no | no | Worked replacement | Neither |
| Hanson–Wright | `optimize` · Balance the exponent, respecting the cutoff. | no | no | Worked replacement | Neither |
| Hanson–Wright | `finish` · Both branches reach the original endpoint. | no | no | Worked replacement | Neither |
| Covariance estimation | `a1` · Plan an isotropic lemma and a transport argument | no | no | Worked replacement | Neither |
| Covariance estimation | `a2` · Control a fixed quadratic form | yes | no | Worked replacement | AI only |
| Covariance estimation | `a3` · Pass from one direction to a finite net | yes | yes | No worked replacement established | Both |
| Covariance estimation | `a4` · Integrate the matrix tail | no | no | Worked replacement | Neither |
| Covariance estimation | `a5` · Whiten only on the covariance range | no | no | Worked replacement | Neither |
| Covariance estimation | `a6` · Transport the norm bound and close the proof | no | no | Worked replacement | Neither |
| Dimension reduction for Boolean functions | `a1` · Encode pairwise distances by bounded samples | no | no | Worked, source-assisted | Neither |
| Dimension reduction for Boolean functions | `a2` · Bound one bad pair | yes | no | Worked, source-assisted | AI only |
| Dimension reduction for Boolean functions | `a3` · Make the pairwise guarantee simultaneous | yes | yes | No worked replacement established | Both |
| Dimension reduction for Boolean functions | `a4` · Choose the budget and close | no | no | Worked replacement | Neither |
| Slepian’s inequality | `a1` · Reduce to finite covariance comparison | no | no | Worked replacement | Neither |
| Slepian’s inequality | `a2` · Interpolate the Gaussian covariance | yes | yes | No worked replacement established | Both |
| Slepian’s inequality | `a3` · Choose a product cutoff with positive mixed derivatives | yes | yes | No worked replacement established | Both |
| Slepian’s inequality | `a4` · Remove smoothing and meet the finite goal | no | yes | No worked replacement established | Ablation only |
| Slepian’s inequality | `a5` · Pass to separable suprema and closed tails | no | yes | No worked replacement established | Ablation only |
| Slepian’s inequality | `a6` · Truncate and close the expectation goal | no | no | Worked replacement | Neither |
| Centering a subgaussian variable | `a1` · Unpack the norm and choose an admissible scale | no | no | Worked replacement | Neither |
| Centering a subgaussian variable | `a2` · Control the deterministic mean at the same scale | no | no | Worked replacement | Neither |
| Centering a subgaussian variable | `a3` · Separate the two terms and bound the exponential moment | yes | no | Worked replacement | AI only |
| Centering a subgaussian variable | `a4` · Read off the norm and close | no | no | Worked replacement | Neither |

## Appendix B. Reproducible sources

- Hanson–Wright all-step notes — `../../proposals/hanson_wright_ablation_notes.md` (repository source path), decoupling note — `../../proposals/hanson_wright_ablations/07-decouple.md` (repository source path), saved AI selection — `../../tools/proof_explorer/critical-step-selection.js` (repository source path), and branch records — `../../tools/proof_explorer/ablation-proofs.js` (repository source path).
- Covariance estimation: saved proof, ablations and critical selection — `../../tools/proof_explorer/collection/data/covariance.json` (repository source path).
- Dimension reduction for Boolean functions: saved proof, ablations and critical selection — `../../tools/proof_explorer/collection/data/dimension-reduction.json` (repository source path).
- Slepian’s inequality: saved proof, ablations and critical selection — `../../tools/proof_explorer/collection/data/slepian.json` (repository source path).
- Centering a subgaussian variable: saved proof, ablations and critical selection — `../../tools/proof_explorer/collection/data/centering.json` (repository source path).
- [Original control vs Library-RAG report](https://lisay1379.github.io/proof_assistant_lab/reports/control_vs_rag/test_3node_rag_2/comparison_viewer.html). The mathematical branch assessments were added when the explorers were built.
- Rebuild: `python3 tools/proof_explorer/build_alignment_report.py`. This reads existing files and writes the report; it makes no model or search requests and does not alter the original labels. SHA-256 input fingerprints are included in `alignment.json`.
