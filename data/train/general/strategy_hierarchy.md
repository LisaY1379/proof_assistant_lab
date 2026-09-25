# Hierarchical Proof Strategy Library

A graph-like hierarchy merging foundational real-analysis proof techniques with broader analytic, geometric, probabilistic, and statistical strategy families. Broad HighDimensionalStatistics categories are retained as parents when RealAnalysis supplies finer sub-branches; cross-links record techniques that genuinely belong to multiple families.

## Nodes by level

### Level 1

- **Definitional unfolding and equivalent reformulation** (`family_definitional_reformulation`): Convert abstract statements into explicit definitions, quantified conditions, or standard equivalent formulations.
  - Sources: high_dimensional_statistics_1 Unfolding definitions and equivalent reformulations
- **Normalization, invariance, and symmetry** (`family_normalization_symmetry`): Translate, rescale, whiten, permute, or otherwise transform a problem to a canonical case and transfer the conclusion back.
  - Sources: high_dimensional_statistics_2 Normalization, invariance, and symmetry
- **Reduction to a standard theorem** (`family_standard_theorem_reduction`): Modify domains and regularity hypotheses so that a known theorem applies directly.
  - Sources: high_dimensional_statistics_3 Reduction to a standard theorem
- **Logical decomposition, cases, and contradiction** (`family_logical_reasoning`): Split logical, order, endpoint, degeneracy, or parameter cases and use contradiction or contraposition to eliminate alternatives.
  - Sources: real_analysis_4 Logical decomposition and case analysis; high_dimensional_statistics_5 Proof by cases and contradiction
- **Explicit construction and parameter choice** (`family_explicit_construction`): Construct witnesses, sequences, partitions, comparison points, thresholds, or auxiliary objects and tune free parameters.
  - Sources: real_analysis_5 Explicit witness and test-point construction; high_dimensional_statistics_6 Explicit construction and parameter choice
- **Algebraic, order, and norm estimates** (`family_algebra_order_norm`): Combine algebraic rearrangement and order reasoning with norm inequalities and duality estimates.
  - Sources: high_dimensional_statistics_4 Algebraic, order, and norm estimates
- **Compactness and connectedness methods** (`family_topology_compactness_connectedness`): Use compactness for boundedness, extrema, subsequences, and uniform continuity, and connectedness for intermediate values and zeros.
  - Sources: high_dimensional_statistics_7 Compactness and connectedness arguments
- **Supremum, infimum, and extremal arguments** (`family_extremal_order`): Control quantities through suprema, infima, extremal points, or attained optimizers.
  - Sources: high_dimensional_statistics_8 Supremum, infimum, and extremal arguments
- **Limit, sequence, and completeness methods** (`family_limits_completeness`): Use epsilon or filter formulations, limit laws, squeezing, completeness, subsequences, and limsup-liminf criteria.
  - Sources: high_dimensional_statistics_9 Limit and completeness arguments
- **Differential-calculus arguments** (`family_differential_calculus`): A broad calculus family covering differentiability criteria, derivative rules, mean-value principles, derivative signs, and Taylor expansion.
  - Sources: high_dimensional_statistics_10 Differential-calculus arguments
- **Error decomposition and balancing** (`family_error_decomposition`): Split a total error into analyzable components and choose parameters that balance the dominant contributions.
  - Sources: high_dimensional_statistics_19 Error decomposition and balancing
- **Comparison, domination, and squeezing** (`family_comparison_domination`): Bound complicated quantities by simpler majorants and transfer those bounds through sums, integrals, limits, and suprema.
  - Sources: high_dimensional_statistics_12 Comparison, domination, and squeezing
- **Series and uniform-convergence methods** (`family_series_convergence`): A broad family covering summability tests, uniform convergence, and power-series convergence radii.
  - Sources: high_dimensional_statistics_13 Series tests and uniform convergence
- **Integral-calculus arguments** (`family_integral_calculus`): A broad integration family covering the fundamental theorem, structural integral identities, transformations, and Riemann-sum methods.
  - Sources: high_dimensional_statistics_11 Integral-calculus arguments
- **Reindexing and telescoping sums** (`family_reindexing_telescoping`): Reindex sums under bijections or fibers and cancel consecutive terms so only boundary contributions remain.
  - Sources: real_analysis_25 Finite-sum reindexing and telescoping; high_dimensional_statistics_14 Reindexing and telescoping sums
- **Induction, recurrence, and well-ordering** (`family_induction_well_ordering`): Use induction, strengthened hypotheses, recurrence, least witnesses, or minimal counterexamples over the natural numbers.
  - Sources: real_analysis_30 Induction and well-ordering; high_dimensional_statistics_15 Induction, recurrence, and well-ordering
- **Cardinality, embeddings, and completion** (`family_structural_foundations`): Use embeddings and cardinal comparisons or construct complete ordered structures from dense substructures and cuts.
  - Sources: high_dimensional_statistics_16 Cardinality, embeddings, and completion arguments
- **Variational and linear-algebraic methods** (`family_variational_linear_algebra`): Optimization and geometric methods based on convexity, orthogonality, projections, spectra, and structured parameter spaces.
- **Metric entropy, covering, and packing methods** (`family_metric_entropy`): Discretize continuous classes by finite nets or construct well-separated finite subsets using packing methods.
- **Probability, concentration, and information methods** (`family_probability_information`): Probabilistic proof methods based on exponential moments, tails, independence, union bounds, and information-theoretic reductions.

### Level 2

- **Definitional unfolding** (`sub_definitional_unfolding`): Expand boundedness, inclusion, extrema, Riemann sums, and auxiliary constructions into their defining statements.
  - Sources: real_analysis_1 Definitional unfolding
- **Metric and filter characterizations** (`sub_metric_filter_characterization`): Replace continuity, convergence, Cauchy conditions, and eventual properties by neighborhood, filter, or epsilon-based criteria.
  - Sources: real_analysis_2 Metric and filter characterization
- **Canonical rewriting** (`sub_canonical_rewriting`): Rewrite abstract distances, norms, slopes, interval interiors, and formal-series expressions in concrete canonical forms.
  - Sources: real_analysis_3 Canonical rewriting and normalization
- **Set identities and extensionality** (`sub_set_extensionality`): Prove set equalities by extensionality or mutual inclusion and simplify Boolean set operations.
  - Sources: real_analysis_31 Set-theoretic identities and extensionality
- **Restriction, extension, and transfer of regularity** (`sub_regularity_transfer`): Restrict or extend functions and transfer continuity, differentiability, or integrability between compatible domains.
  - Sources: real_analysis_9 Restriction, extension, and transfer of regularity
- **Elementary algebra and order reasoning** (`sub_elementary_algebra_order`): Prove positivity or nonvanishing, clear denominators, cancel factors, rearrange identities, and combine inequalities.
  - Sources: real_analysis_6 Elementary algebra and order reasoning
- **Compactness arguments** (`sub_compactness`): Apply compactness of intervals or images to obtain boundedness, attained extrema, uniform continuity, or convergent subsequences.
  - Sources: real_analysis_7 Compactness arguments
- **Intermediate Value Theorem** (`sub_intermediate_value`): Use continuity and endpoint value information to produce an intermediate value or interior zero.
  - Sources: real_analysis_10 Intermediate Value Theorem
- **Suprema, infima, and order completeness** (`sub_order_completeness`): Apply least-upper-bound and greatest-lower-bound properties to bounded sets, images, limsups, and moduli of continuity.
  - Sources: real_analysis_8 Suprema, infima, and order completeness
- **Limit laws, squeezing, and uniqueness** (`sub_limit_laws_squeezing`): Compose limits, pass bounds to limits, squeeze between convergent quantities, and use uniqueness to identify limits.
  - Sources: real_analysis_11 Limit laws, squeezing, and uniqueness
- **Sequence and completeness methods** (`sub_sequence_completeness`): Use epsilon-N arguments, Cauchy completeness, subsequences, and sequences approaching a point.
  - Sources: real_analysis_28 Sequence and completeness methods
- **Monotone sequences, limsup, and subsequences** (`sub_monotone_limsup_subsequence`): Use monotone convergence, limsup-liminf characterizations, and extraction of convergent subsequences.
  - Sources: real_analysis_29 Monotone sequences, limsup, and subsequences
- **Difference-quotient characterization of differentiability** (`sub_difference_quotient`): Express differentiability as convergence of slopes on a punctured neighborhood.
  - Sources: real_analysis_12 Difference-quotient characterization of differentiability
- **Differential calculus rules** (`sub_derivative_rules`): Apply chain, composition, and related closure rules for differentiable functions.
  - Sources: real_analysis_13 Differential calculus rules
- **Fermat, Rolle, and Mean Value Theorems** (`sub_mean_value_theorems`): Convert extrema or endpoint equalities into derivative information and represent increments by intermediate derivatives.
  - Sources: real_analysis_14 Fermat, Rolle, and Mean Value Theorems
- **Derivative-sign arguments** (`sub_derivative_sign`): Infer monotonicity, constancy, or local extrema from first- or second-derivative sign information.
  - Sources: real_analysis_15 Derivative-sign arguments
- **Taylor expansion with remainder** (`sub_taylor_remainder`): Apply finite Taylor expansion with a controlled remainder and normalize the resulting coefficients.
  - Sources: real_analysis_16 Taylor expansion with remainder
- **Triangle-inequality and error-decomposition estimates** (`sub_triangle_error_estimates`): Separate dominant and error terms and control them with triangle and reverse-triangle inequalities.
  - Sources: real_analysis_17 Triangle-inequality and error-decomposition estimates
- **Approximation and Archimedean error control** (`sub_approximation_archimedean`): Choose dense approximants and then select an index making the uniform approximation error smaller than a prescribed tolerance.
  - Sources: real_analysis_21 Approximation and Archimedean error control
- **Series comparison and convergence tests** (`sub_series_tests`): Use comparison, term, root, ratio, alternating-series, geometric, or rearrangement criteria.
  - Sources: real_analysis_18 Series comparison and convergence tests
- **Uniform convergence and the Weierstrass M-test** (`sub_uniform_convergence_mtest`): Produce a summable uniform majorant and transfer continuity or bounds to the resulting series.
  - Sources: real_analysis_19 Uniform convergence and the Weierstrass M-test
- **Power-series radius arguments** (`sub_power_series_radius`): Compare coefficient growth and apply Cauchy-Hadamard or radius-of-convergence comparison results.
  - Sources: real_analysis_20 Power-series radius arguments
- **Fundamental Theorem of Calculus** (`sub_fundamental_theorem_calculus`): Convert derivatives into integral increments or differentiate parameterized integrals.
  - Sources: real_analysis_22 Fundamental Theorem of Calculus
- **Structural properties of the integral** (`sub_integral_structure`): Use linearity, interval additivity, monotonicity, constant-integral formulas, and integral norm inequalities.
  - Sources: real_analysis_23 Structural properties of the integral
- **Integration by parts and substitution** (`sub_integration_transformations`): Verify regularity and integrability hypotheses and then apply integration by parts or change of variables.
  - Sources: real_analysis_24 Integration by parts and substitution
- **Partition and refinement arguments** (`sub_partition_refinement`): Control meshes and subintervals, construct common refinements, and decompose coarse partitions into fine pieces.
  - Sources: real_analysis_26 Partition and refinement arguments
- **Ordered-field structure and canonical constructions** (`sub_ordered_field_constructions`): Use ordered-field operations, canonical witnesses, Archimedeanness, completeness, and rational cuts in structural arguments about the reals.
  - Sources: real_analysis_32 Ordered-field structure and canonical constructions
- **Cardinality and embedding arguments** (`sub_cardinality_embeddings`): Use injections, diagonalization, Cantor's theorem, interval cardinality, and Cantor-Schroeder-Bernstein.
  - Sources: real_analysis_33 Cardinality and embedding arguments
- **Convexity and variational arguments** (`sub_convexity_variational`): Use Jensen's inequality, convex combinations, first-order optimality, or comparison with feasible competitors.
  - Sources: high_dimensional_statistics_17 Convexity and variational arguments
- **Orthogonality, projection, and spectral arguments** (`sub_orthogonality_spectral`): Use orthogonal expansions, Pythagoras, Parseval, normal equations, Rayleigh quotients, and eigenvector principles.
  - Sources: high_dimensional_statistics_18 Orthogonality, projection, and spectral arguments
- **Sparsity, low-rank structure, and norm duality** (`sub_structured_parameters`): Exploit support, cone, rank, or singular-space decompositions together with dual norms and restricted geometric conditions.
  - Sources: high_dimensional_statistics_24 Sparsity, low-rank structure, and norm duality
- **Covering-net and volumetric arguments** (`sub_covering_volumetric`): Replace continuous suprema by maxima over finite epsilon-nets and bound net sizes through packing and volume comparison.
  - Sources: high_dimensional_statistics_20 Covering-net and volumetric arguments
- **Probabilistic method and packing constructions** (`sub_probabilistic_packing`): Randomly generate nets, codes, sparse vectors, or approximants and prove that a suitable deterministic construction exists.
  - Sources: high_dimensional_statistics_26 Probabilistic method and packing constructions
- **Exponential-moment and concentration arguments** (`sub_exponential_concentration`): Apply exponential Markov inequalities, control moment-generating functions, and optimize parameters to derive tail bounds.
  - Sources: high_dimensional_statistics_21 Exponential-moment and concentration arguments
- **Tail integration and moment estimates** (`sub_tail_integration`): Convert moments into tail integrals, insert probability bounds, and estimate the resulting integrals.
  - Sources: high_dimensional_statistics_22 Tail integration and moment estimates
- **Independence, tensorization, and union bounds** (`sub_independence_tensorization`): Factor quantities using independence, tensorize information, and upgrade pointwise bounds to simultaneous bounds by a union bound.
  - Sources: high_dimensional_statistics_23 Independence, tensorization, and union bounds
- **Testing and information-theoretic reductions** (`sub_testing_information`): Reduce estimation to hypothesis testing and control testing error using divergence or mutual-information inequalities.
  - Sources: high_dimensional_statistics_25 Testing and information-theoretic reductions

### Level 3

- **Modulus-of-continuity control of Riemann sums** (`sub_riemann_modulus_control`): Control tag changes using a modulus of continuity and sum local errors to prove convergence and partition independence.
  - Sources: real_analysis_27 Modulus-of-continuity control of Riemann sums

## Edges

- `family_definitional_reformulation` → `sub_definitional_unfolding` (parent_of): Definitional unfolding is the direct expansion branch of the broader reformulation family.
- `family_definitional_reformulation` → `sub_metric_filter_characterization` (parent_of): Metric and filter criteria are standard equivalent reformulations of analytic definitions.
- `family_definitional_reformulation` → `sub_canonical_rewriting` (parent_of): Canonical rewriting replaces abstract notions by equivalent concrete forms.
- `family_definitional_reformulation` → `sub_set_extensionality` (parent_of): Set extensionality and Boolean simplification are specialized definitional and reformulation techniques.
- `family_normalization_symmetry` → `sub_canonical_rewriting` (parent_of): Concrete norm, metric, slope, and interval rewrites are elementary canonical-normalization steps.
- `family_standard_theorem_reduction` → `sub_regularity_transfer` (parent_of): Restriction, extension, and regularity transfer are used to align hypotheses with a standard theorem.
- `family_algebra_order_norm` → `sub_elementary_algebra_order` (parent_of): Elementary ordered-field manipulations form the scalar algebraic branch of the broader estimate family.
- `family_topology_compactness_connectedness` → `sub_compactness` (parent_of): The target is the compactness-specific branch of the combined topological family.
- `family_topology_compactness_connectedness` → `sub_intermediate_value` (parent_of): The Intermediate Value Theorem is the interval-connectedness branch of the broader family.
- `family_extremal_order` → `sub_order_completeness` (parent_of): Least-upper-bound and greatest-lower-bound reasoning is a specific order-theoretic extremal method.
- `family_limits_completeness` → `sub_limit_laws_squeezing` (parent_of): Limit laws, squeezing, and uniqueness are core sub-branches of limit arguments.
- `family_limits_completeness` → `sub_sequence_completeness` (parent_of): Sequence and Cauchy-completeness methods specialize the broader limit and completeness family.
- `family_limits_completeness` → `sub_monotone_limsup_subsequence` (parent_of): Monotone convergence, limsup, and subsequence extraction are specific sequential limit methods.
- `family_limits_completeness` → `sub_metric_filter_characterization` (cross_link): Metric and filter characterizations provide the formulations used by many limit arguments but also apply to continuity and other notions.
- `family_differential_calculus` → `sub_difference_quotient` (parent_of): Difference quotients are the characterization branch of differential calculus.
- `family_differential_calculus` → `sub_derivative_rules` (parent_of): Derivative rules are a standard computational sub-branch of differential calculus.
- `family_differential_calculus` → `sub_mean_value_theorems` (parent_of): Fermat, Rolle, and mean-value principles are standard differential-calculus theorems.
- `family_differential_calculus` → `sub_derivative_sign` (parent_of): Derivative-sign methods specialize differential calculus to monotonicity and extrema.
- `family_differential_calculus` → `sub_taylor_remainder` (parent_of): Taylor expansion is the higher-order approximation branch of differential calculus.
- `family_error_decomposition` → `sub_triangle_error_estimates` (parent_of): Triangle-based splitting is a basic specific form of error decomposition.
- `family_algebra_order_norm` → `sub_triangle_error_estimates` (parent_of): The target is also a norm-estimate method based on triangle and reverse-triangle inequalities.
- `family_error_decomposition` → `sub_approximation_archimedean` (parent_of): Approximation error and the choice of an index to meet a tolerance form a specialized error-control strategy.
- `family_explicit_construction` → `sub_approximation_archimedean` (parent_of): The approximation strategy explicitly chooses an approximant and a sufficiently large index.
- `family_comparison_domination` → `sub_limit_laws_squeezing` (parent_of): Squeezing is a limit-specific instance of comparison and domination.
- `family_comparison_domination` → `sub_series_tests` (parent_of): Comparison with summable majorants is a principal series-convergence technique.
- `family_comparison_domination` → `sub_uniform_convergence_mtest` (parent_of): The Weierstrass M-test is a uniform domination argument.
- `family_series_convergence` → `sub_series_tests` (parent_of): The target contains the detailed summability tests covered broadly by the parent.
- `family_series_convergence` → `sub_uniform_convergence_mtest` (parent_of): Uniform convergence and the M-test are a distinct sub-branch of the broader series family.
- `family_series_convergence` → `sub_power_series_radius` (parent_of): Radius-of-convergence reasoning is a power-series-specific branch of series analysis.
- `family_integral_calculus` → `sub_fundamental_theorem_calculus` (parent_of): The Fundamental Theorem of Calculus is a specific central branch of integral calculus.
- `family_integral_calculus` → `sub_integral_structure` (parent_of): Linearity, additivity, and monotonicity are structural sub-techniques of integration.
- `family_integral_calculus` → `sub_integration_transformations` (parent_of): Integration by parts and substitution are specific integration transformations.
- `family_integral_calculus` → `sub_partition_refinement` (parent_of): Partition and refinement methods form a Riemann-integration sub-branch.
- `sub_partition_refinement` → `sub_riemann_modulus_control` (parent_of): Modulus-of-continuity control is a more specific refinement-based method for comparing Riemann sums.
- `family_error_decomposition` → `sub_riemann_modulus_control` (cross_link): The method decomposes and sums local discretization errors, although its primary setting is Riemann integration.
- `family_explicit_construction` → `sub_partition_refinement` (cross_link): Partition proofs often require explicit construction of common refinements, but the category is primarily an integration method.
- `family_structural_foundations` → `sub_ordered_field_constructions` (parent_of): Ordered-field constructions using cuts and completeness instantiate the completion component of the parent.
- `family_structural_foundations` → `sub_cardinality_embeddings` (parent_of): Cardinality comparisons and mutual embeddings instantiate the embedding component of the parent.
- `family_explicit_construction` → `sub_ordered_field_constructions` (cross_link): Canonical field witnesses are explicit constructions, though the category also contains substantial structural theory.
- `family_structural_foundations` → `sub_order_completeness` (cross_link): Order completeness is used in structural characterizations and completions of the real numbers.
- `family_variational_linear_algebra` → `sub_convexity_variational` (parent_of): Convex optimality and competitor arguments form the variational branch of the family.
- `family_variational_linear_algebra` → `sub_orthogonality_spectral` (parent_of): Orthogonality, projection, and spectral methods form the linear-algebraic branch.
- `family_variational_linear_algebra` → `sub_structured_parameters` (parent_of): Sparse and low-rank decompositions are structured geometric and linear-algebraic methods.
- `family_extremal_order` → `sub_convexity_variational` (cross_link): Convexity often reduces extrema to special points or derives optimality conditions, but it is not merely order completeness.
- `family_algebra_order_norm` → `sub_structured_parameters` (parent_of): Norm duality and absorption of cross terms are central algebraic-estimate components of structured-parameter arguments.
- `family_metric_entropy` → `sub_covering_volumetric` (parent_of): Finite-net discretization and volume bounds are the covering branch of metric entropy.
- `family_metric_entropy` → `sub_probabilistic_packing` (parent_of): Random construction of separated sets is a packing branch of metric-entropy methods.
- `family_explicit_construction` → `sub_probabilistic_packing` (parent_of): The probabilistic method is an existence-oriented construction strategy, even though the candidates are generated randomly.
- `family_probability_information` → `sub_exponential_concentration` (parent_of): Exponential-moment bounds are a central concentration sub-family.
- `family_probability_information` → `sub_tail_integration` (parent_of): Tail-to-moment conversion is a probabilistic moment-estimation method.
- `family_probability_information` → `sub_independence_tensorization` (parent_of): Independence, product structure, and union bounds are basic probabilistic proof mechanisms.
- `family_probability_information` → `sub_testing_information` (parent_of): Testing reductions and divergence inequalities form the information-theoretic branch.
- `family_probability_information` → `sub_probabilistic_packing` (cross_link): Probabilistic packing arguments use random sampling and probability bounds in addition to metric-entropy structure.
- `family_integral_calculus` → `sub_tail_integration` (parent_of): Tail integration is a specialized use of integral calculus, including substitutions and threshold splitting, within probability.
- `family_comparison_domination` → `sub_tail_integration` (cross_link): Moment bounds arise by inserting a dominating tail estimate into an integral.
- `sub_exponential_concentration` → `sub_independence_tensorization` (cross_link): Independence frequently factors moment-generating functions and union bounds convert fixed-direction concentration into simultaneous bounds.
- `sub_covering_volumetric` → `sub_exponential_concentration` (cross_link): Finite-net reductions are commonly combined with concentration and union bounds to control continuous suprema.
- `sub_probabilistic_packing` → `sub_testing_information` (cross_link): Information-theoretic lower bounds often require a large finite packing of well-separated hypotheses.

## Raw LLM response

```json
{
  "metadata": {
    "title": "Hierarchical Proof Strategy Library",
    "description": "A graph-like hierarchy merging foundational real-analysis proof techniques with broader analytic, geometric, probabilistic, and statistical strategy families. Broad HighDimensionalStatistics categories are retained as parents when RealAnalysis supplies finer sub-branches; cross-links record techniques that genuinely belong to multiple families.",
    "source_libraries": [
      "real_analysis",
      "high_dimensional_statistics"
    ]
  },
  "nodes": [
    {
      "id": "family_definitional_reformulation",
      "label": "Definitional unfolding and equivalent reformulation",
      "level": 1,
      "description": "Convert abstract statements into explicit definitions, quantified conditions, or standard equivalent formulations.",
      "source_categories": [
        {
          "dataset": "high_dimensional_statistics",
          "id": "high_dimensional_statistics_1",
          "name": "Unfolding definitions and equivalent reformulations"
        }
      ]
    },
    {
      "id": "sub_definitional_unfolding",
      "label": "Definitional unfolding",
      "level": 2,
      "description": "Expand boundedness, inclusion, extrema, Riemann sums, and auxiliary constructions into their defining statements.",
      "source_categories": [
        {
          "dataset": "real_analysis",
          "id": "real_analysis_1",
          "name": "Definitional unfolding"
        }
      ]
    },
    {
      "id": "sub_metric_filter_characterization",
      "label": "Metric and filter characterizations",
      "level": 2,
      "description": "Replace continuity, convergence, Cauchy conditions, and eventual properties by neighborhood, filter, or epsilon-based criteria.",
      "source_categories": [
        {
          "dataset": "real_analysis",
          "id": "real_analysis_2",
          "name": "Metric and filter characterization"
        }
      ]
    },
    {
      "id": "sub_canonical_rewriting",
      "label": "Canonical rewriting",
      "level": 2,
      "description": "Rewrite abstract distances, norms, slopes, interval interiors, and formal-series expressions in concrete canonical forms.",
      "source_categories": [
        {
          "dataset": "real_analysis",
          "id": "real_analysis_3",
          "name": "Canonical rewriting and normalization"
        }
      ]
    },
    {
      "id": "sub_set_extensionality",
      "label": "Set identities and extensionality",
      "level": 2,
      "description": "Prove set equalities by extensionality or mutual inclusion and simplify Boolean set operations.",
      "source_categories": [
        {
          "dataset": "real_analysis",
          "id": "real_analysis_31",
          "name": "Set-theoretic identities and extensionality"
        }
      ]
    },
    {
      "id": "family_normalization_symmetry",
      "label": "Normalization, invariance, and symmetry",
      "level": 1,
      "description": "Translate, rescale, whiten, permute, or otherwise transform a problem to a canonical case and transfer the conclusion back.",
      "source_categories": [
        {
          "dataset": "high_dimensional_statistics",
          "id": "high_dimensional_statistics_2",
          "name": "Normalization, invariance, and symmetry"
        }
      ]
    },
    {
      "id": "family_standard_theorem_reduction",
      "label": "Reduction to a standard theorem",
      "level": 1,
      "description": "Modify domains and regularity hypotheses so that a known theorem applies directly.",
      "source_categories": [
        {
          "dataset": "high_dimensional_statistics",
          "id": "high_dimensional_statistics_3",
          "name": "Reduction to a standard theorem"
        }
      ]
    },
    {
      "id": "sub_regularity_transfer",
      "label": "Restriction, extension, and transfer of regularity",
      "level": 2,
      "description": "Restrict or extend functions and transfer continuity, differentiability, or integrability between compatible domains.",
      "source_categories": [
        {
          "dataset": "real_analysis",
          "id": "real_analysis_9",
          "name": "Restriction, extension, and transfer of regularity"
        }
      ]
    },
    {
      "id": "family_logical_reasoning",
      "label": "Logical decomposition, cases, and contradiction",
      "level": 1,
      "description": "Split logical, order, endpoint, degeneracy, or parameter cases and use contradiction or contraposition to eliminate alternatives.",
      "source_categories": [
        {
          "dataset": "real_analysis",
          "id": "real_analysis_4",
          "name": "Logical decomposition and case analysis"
        },
        {
          "dataset": "high_dimensional_statistics",
          "id": "high_dimensional_statistics_5",
          "name": "Proof by cases and contradiction"
        }
      ]
    },
    {
      "id": "family_explicit_construction",
      "label": "Explicit construction and parameter choice",
      "level": 1,
      "description": "Construct witnesses, sequences, partitions, comparison points, thresholds, or auxiliary objects and tune free parameters.",
      "source_categories": [
        {
          "dataset": "real_analysis",
          "id": "real_analysis_5",
          "name": "Explicit witness and test-point construction"
        },
        {
          "dataset": "high_dimensional_statistics",
          "id": "high_dimensional_statistics_6",
          "name": "Explicit construction and parameter choice"
        }
      ]
    },
    {
      "id": "family_algebra_order_norm",
      "label": "Algebraic, order, and norm estimates",
      "level": 1,
      "description": "Combine algebraic rearrangement and order reasoning with norm inequalities and duality estimates.",
      "source_categories": [
        {
          "dataset": "high_dimensional_statistics",
          "id": "high_dimensional_statistics_4",
          "name": "Algebraic, order, and norm estimates"
        }
      ]
    },
    {
      "id": "sub_elementary_algebra_order",
      "label": "Elementary algebra and order reasoning",
      "level": 2,
      "description": "Prove positivity or nonvanishing, clear denominators, cancel factors, rearrange identities, and combine inequalities.",
      "source_categories": [
        {
          "dataset": "real_analysis",
          "id": "real_analysis_6",
          "name": "Elementary algebra and order reasoning"
        }
      ]
    },
    {
      "id": "family_topology_compactness_connectedness",
      "label": "Compactness and connectedness methods",
      "level": 1,
      "description": "Use compactness for boundedness, extrema, subsequences, and uniform continuity, and connectedness for intermediate values and zeros.",
      "source_categories": [
        {
          "dataset": "high_dimensional_statistics",
          "id": "high_dimensional_statistics_7",
          "name": "Compactness and connectedness arguments"
        }
      ]
    },
    {
      "id": "sub_compactness",
      "label": "Compactness arguments",
      "level": 2,
      "description": "Apply compactness of intervals or images to obtain boundedness, attained extrema, uniform continuity, or convergent subsequences.",
      "source_categories": [
        {
          "dataset": "real_analysis",
          "id": "real_analysis_7",
          "name": "Compactness arguments"
        }
      ]
    },
    {
      "id": "sub_intermediate_value",
      "label": "Intermediate Value Theorem",
      "level": 2,
      "description": "Use continuity and endpoint value information to produce an intermediate value or interior zero.",
      "source_categories": [
        {
          "dataset": "real_analysis",
          "id": "real_analysis_10",
          "name": "Intermediate Value Theorem"
        }
      ]
    },
    {
      "id": "family_extremal_order",
      "label": "Supremum, infimum, and extremal arguments",
      "level": 1,
      "description": "Control quantities through suprema, infima, extremal points, or attained optimizers.",
      "source_categories": [
        {
          "dataset": "high_dimensional_statistics",
          "id": "high_dimensional_statistics_8",
          "name": "Supremum, infimum, and extremal arguments"
        }
      ]
    },
    {
      "id": "sub_order_completeness",
      "label": "Suprema, infima, and order completeness",
      "level": 2,
      "description": "Apply least-upper-bound and greatest-lower-bound properties to bounded sets, images, limsups, and moduli of continuity.",
      "source_categories": [
        {
          "dataset": "real_analysis",
          "id": "real_analysis_8",
          "name": "Suprema, infima, and order completeness"
        }
      ]
    },
    {
      "id": "family_limits_completeness",
      "label": "Limit, sequence, and completeness methods",
      "level": 1,
      "description": "Use epsilon or filter formulations, limit laws, squeezing, completeness, subsequences, and limsup-liminf criteria.",
      "source_categories": [
        {
          "dataset": "high_dimensional_statistics",
          "id": "high_dimensional_statistics_9",
          "name": "Limit and completeness arguments"
        }
      ]
    },
    {
      "id": "sub_limit_laws_squeezing",
      "label": "Limit laws, squeezing, and uniqueness",
      "level": 2,
      "description": "Compose limits, pass bounds to limits, squeeze between convergent quantities, and use uniqueness to identify limits.",
      "source_categories": [
        {
          "dataset": "real_analysis",
          "id": "real_analysis_11",
          "name": "Limit laws, squeezing, and uniqueness"
        }
      ]
    },
    {
      "id": "sub_sequence_completeness",
      "label": "Sequence and completeness methods",
      "level": 2,
      "description": "Use epsilon-N arguments, Cauchy completeness, subsequences, and sequences approaching a point.",
      "source_categories": [
        {
          "dataset": "real_analysis",
          "id": "real_analysis_28",
          "name": "Sequence and completeness methods"
        }
      ]
    },
    {
      "id": "sub_monotone_limsup_subsequence",
      "label": "Monotone sequences, limsup, and subsequences",
      "level": 2,
      "description": "Use monotone convergence, limsup-liminf characterizations, and extraction of convergent subsequences.",
      "source_categories": [
        {
          "dataset": "real_analysis",
          "id": "real_analysis_29",
          "name": "Monotone sequences, limsup, and subsequences"
        }
      ]
    },
    {
      "id": "family_differential_calculus",
      "label": "Differential-calculus arguments",
      "level": 1,
      "description": "A broad calculus family covering differentiability criteria, derivative rules, mean-value principles, derivative signs, and Taylor expansion.",
      "source_categories": [
        {
          "dataset": "high_dimensional_statistics",
          "id": "high_dimensional_statistics_10",
          "name": "Differential-calculus arguments"
        }
      ]
    },
    {
      "id": "sub_difference_quotient",
      "label": "Difference-quotient characterization of differentiability",
      "level": 2,
      "description": "Express differentiability as convergence of slopes on a punctured neighborhood.",
      "source_categories": [
        {
          "dataset": "real_analysis",
          "id": "real_analysis_12",
          "name": "Difference-quotient characterization of differentiability"
        }
      ]
    },
    {
      "id": "sub_derivative_rules",
      "label": "Differential calculus rules",
      "level": 2,
      "description": "Apply chain, composition, and related closure rules for differentiable functions.",
      "source_categories": [
        {
          "dataset": "real_analysis",
          "id": "real_analysis_13",
          "name": "Differential calculus rules"
        }
      ]
    },
    {
      "id": "sub_mean_value_theorems",
      "label": "Fermat, Rolle, and Mean Value Theorems",
      "level": 2,
      "description": "Convert extrema or endpoint equalities into derivative information and represent increments by intermediate derivatives.",
      "source_categories": [
        {
          "dataset": "real_analysis",
          "id": "real_analysis_14",
          "name": "Fermat, Rolle, and Mean Value Theorems"
        }
      ]
    },
    {
      "id": "sub_derivative_sign",
      "label": "Derivative-sign arguments",
      "level": 2,
      "description": "Infer monotonicity, constancy, or local extrema from first- or second-derivative sign information.",
      "source_categories": [
        {
          "dataset": "real_analysis",
          "id": "real_analysis_15",
          "name": "Derivative-sign arguments"
        }
      ]
    },
    {
      "id": "sub_taylor_remainder",
      "label": "Taylor expansion with remainder",
      "level": 2,
      "description": "Apply finite Taylor expansion with a controlled remainder and normalize the resulting coefficients.",
      "source_categories": [
        {
          "dataset": "real_analysis",
          "id": "real_analysis_16",
          "name": "Taylor expansion with remainder"
        }
      ]
    },
    {
      "id": "family_error_decomposition",
      "label": "Error decomposition and balancing",
      "level": 1,
      "description": "Split a total error into analyzable components and choose parameters that balance the dominant contributions.",
      "source_categories": [
        {
          "dataset": "high_dimensional_statistics",
          "id": "high_dimensional_statistics_19",
          "name": "Error decomposition and balancing"
        }
      ]
    },
    {
      "id": "sub_triangle_error_estimates",
      "label": "Triangle-inequality and error-decomposition estimates",
      "level": 2,
      "description": "Separate dominant and error terms and control them with triangle and reverse-triangle inequalities.",
      "source_categories": [
        {
          "dataset": "real_analysis",
          "id": "real_analysis_17",
          "name": "Triangle-inequality and error-decomposition estimates"
        }
      ]
    },
    {
      "id": "sub_approximation_archimedean",
      "label": "Approximation and Archimedean error control",
      "level": 2,
      "description": "Choose dense approximants and then select an index making the uniform approximation error smaller than a prescribed tolerance.",
      "source_categories": [
        {
          "dataset": "real_analysis",
          "id": "real_analysis_21",
          "name": "Approximation and Archimedean error control"
        }
      ]
    },
    {
      "id": "family_comparison_domination",
      "label": "Comparison, domination, and squeezing",
      "level": 1,
      "description": "Bound complicated quantities by simpler majorants and transfer those bounds through sums, integrals, limits, and suprema.",
      "source_categories": [
        {
          "dataset": "high_dimensional_statistics",
          "id": "high_dimensional_statistics_12",
          "name": "Comparison, domination, and squeezing"
        }
      ]
    },
    {
      "id": "family_series_convergence",
      "label": "Series and uniform-convergence methods",
      "level": 1,
      "description": "A broad family covering summability tests, uniform convergence, and power-series convergence radii.",
      "source_categories": [
        {
          "dataset": "high_dimensional_statistics",
          "id": "high_dimensional_statistics_13",
          "name": "Series tests and uniform convergence"
        }
      ]
    },
    {
      "id": "sub_series_tests",
      "label": "Series comparison and convergence tests",
      "level": 2,
      "description": "Use comparison, term, root, ratio, alternating-series, geometric, or rearrangement criteria.",
      "source_categories": [
        {
          "dataset": "real_analysis",
          "id": "real_analysis_18",
          "name": "Series comparison and convergence tests"
        }
      ]
    },
    {
      "id": "sub_uniform_convergence_mtest",
      "label": "Uniform convergence and the Weierstrass M-test",
      "level": 2,
      "description": "Produce a summable uniform majorant and transfer continuity or bounds to the resulting series.",
      "source_categories": [
        {
          "dataset": "real_analysis",
          "id": "real_analysis_19",
          "name": "Uniform convergence and the Weierstrass M-test"
        }
      ]
    },
    {
      "id": "sub_power_series_radius",
      "label": "Power-series radius arguments",
      "level": 2,
      "description": "Compare coefficient growth and apply Cauchy-Hadamard or radius-of-convergence comparison results.",
      "source_categories": [
        {
          "dataset": "real_analysis",
          "id": "real_analysis_20",
          "name": "Power-series radius arguments"
        }
      ]
    },
    {
      "id": "family_integral_calculus",
      "label": "Integral-calculus arguments",
      "level": 1,
      "description": "A broad integration family covering the fundamental theorem, structural integral identities, transformations, and Riemann-sum methods.",
      "source_categories": [
        {
          "dataset": "high_dimensional_statistics",
          "id": "high_dimensional_statistics_11",
          "name": "Integral-calculus arguments"
        }
      ]
    },
    {
      "id": "sub_fundamental_theorem_calculus",
      "label": "Fundamental Theorem of Calculus",
      "level": 2,
      "description": "Convert derivatives into integral increments or differentiate parameterized integrals.",
      "source_categories": [
        {
          "dataset": "real_analysis",
          "id": "real_analysis_22",
          "name": "Fundamental Theorem of Calculus"
        }
      ]
    },
    {
      "id": "sub_integral_structure",
      "label": "Structural properties of the integral",
      "level": 2,
      "description": "Use linearity, interval additivity, monotonicity, constant-integral formulas, and integral norm inequalities.",
      "source_categories": [
        {
          "dataset": "real_analysis",
          "id": "real_analysis_23",
          "name": "Structural properties of the integral"
        }
      ]
    },
    {
      "id": "sub_integration_transformations",
      "label": "Integration by parts and substitution",
      "level": 2,
      "description": "Verify regularity and integrability hypotheses and then apply integration by parts or change of variables.",
      "source_categories": [
        {
          "dataset": "real_analysis",
          "id": "real_analysis_24",
          "name": "Integration by parts and substitution"
        }
      ]
    },
    {
      "id": "sub_partition_refinement",
      "label": "Partition and refinement arguments",
      "level": 2,
      "description": "Control meshes and subintervals, construct common refinements, and decompose coarse partitions into fine pieces.",
      "source_categories": [
        {
          "dataset": "real_analysis",
          "id": "real_analysis_26",
          "name": "Partition and refinement arguments"
        }
      ]
    },
    {
      "id": "sub_riemann_modulus_control",
      "label": "Modulus-of-continuity control of Riemann sums",
      "level": 3,
      "description": "Control tag changes using a modulus of continuity and sum local errors to prove convergence and partition independence.",
      "source_categories": [
        {
          "dataset": "real_analysis",
          "id": "real_analysis_27",
          "name": "Modulus-of-continuity control of Riemann sums"
        }
      ]
    },
    {
      "id": "family_reindexing_telescoping",
      "label": "Reindexing and telescoping sums",
      "level": 1,
      "description": "Reindex sums under bijections or fibers and cancel consecutive terms so only boundary contributions remain.",
      "source_categories": [
        {
          "dataset": "real_analysis",
          "id": "real_analysis_25",
          "name": "Finite-sum reindexing and telescoping"
        },
        {
          "dataset": "high_dimensional_statistics",
          "id": "high_dimensional_statistics_14",
          "name": "Reindexing and telescoping sums"
        }
      ]
    },
    {
      "id": "family_induction_well_ordering",
      "label": "Induction, recurrence, and well-ordering",
      "level": 1,
      "description": "Use induction, strengthened hypotheses, recurrence, least witnesses, or minimal counterexamples over the natural numbers.",
      "source_categories": [
        {
          "dataset": "real_analysis",
          "id": "real_analysis_30",
          "name": "Induction and well-ordering"
        },
        {
          "dataset": "high_dimensional_statistics",
          "id": "high_dimensional_statistics_15",
          "name": "Induction, recurrence, and well-ordering"
        }
      ]
    },
    {
      "id": "family_structural_foundations",
      "label": "Cardinality, embeddings, and completion",
      "level": 1,
      "description": "Use embeddings and cardinal comparisons or construct complete ordered structures from dense substructures and cuts.",
      "source_categories": [
        {
          "dataset": "high_dimensional_statistics",
          "id": "high_dimensional_statistics_16",
          "name": "Cardinality, embeddings, and completion arguments"
        }
      ]
    },
    {
      "id": "sub_ordered_field_constructions",
      "label": "Ordered-field structure and canonical constructions",
      "level": 2,
      "description": "Use ordered-field operations, canonical witnesses, Archimedeanness, completeness, and rational cuts in structural arguments about the reals.",
      "source_categories": [
        {
          "dataset": "real_analysis",
          "id": "real_analysis_32",
          "name": "Ordered-field structure and canonical constructions"
        }
      ]
    },
    {
      "id": "sub_cardinality_embeddings",
      "label": "Cardinality and embedding arguments",
      "level": 2,
      "description": "Use injections, diagonalization, Cantor's theorem, interval cardinality, and Cantor-Schroeder-Bernstein.",
      "source_categories": [
        {
          "dataset": "real_analysis",
          "id": "real_analysis_33",
          "name": "Cardinality and embedding arguments"
        }
      ]
    },
    {
      "id": "family_variational_linear_algebra",
      "label": "Variational and linear-algebraic methods",
      "level": 1,
      "description": "Optimization and geometric methods based on convexity, orthogonality, projections, spectra, and structured parameter spaces.",
      "source_categories": []
    },
    {
      "id": "sub_convexity_variational",
      "label": "Convexity and variational arguments",
      "level": 2,
      "description": "Use Jensen's inequality, convex combinations, first-order optimality, or comparison with feasible competitors.",
      "source_categories": [
        {
          "dataset": "high_dimensional_statistics",
          "id": "high_dimensional_statistics_17",
          "name": "Convexity and variational arguments"
        }
      ]
    },
    {
      "id": "sub_orthogonality_spectral",
      "label": "Orthogonality, projection, and spectral arguments",
      "level": 2,
      "description": "Use orthogonal expansions, Pythagoras, Parseval, normal equations, Rayleigh quotients, and eigenvector principles.",
      "source_categories": [
        {
          "dataset": "high_dimensional_statistics",
          "id": "high_dimensional_statistics_18",
          "name": "Orthogonality, projection, and spectral arguments"
        }
      ]
    },
    {
      "id": "sub_structured_parameters",
      "label": "Sparsity, low-rank structure, and norm duality",
      "level": 2,
      "description": "Exploit support, cone, rank, or singular-space decompositions together with dual norms and restricted geometric conditions.",
      "source_categories": [
        {
          "dataset": "high_dimensional_statistics",
          "id": "high_dimensional_statistics_24",
          "name": "Sparsity, low-rank structure, and norm duality"
        }
      ]
    },
    {
      "id": "family_metric_entropy",
      "label": "Metric entropy, covering, and packing methods",
      "level": 1,
      "description": "Discretize continuous classes by finite nets or construct well-separated finite subsets using packing methods.",
      "source_categories": []
    },
    {
      "id": "sub_covering_volumetric",
      "label": "Covering-net and volumetric arguments",
      "level": 2,
      "description": "Replace continuous suprema by maxima over finite epsilon-nets and bound net sizes through packing and volume comparison.",
      "source_categories": [
        {
          "dataset": "high_dimensional_statistics",
          "id": "high_dimensional_statistics_20",
          "name": "Covering-net and volumetric arguments"
        }
      ]
    },
    {
      "id": "sub_probabilistic_packing",
      "label": "Probabilistic method and packing constructions",
      "level": 2,
      "description": "Randomly generate nets, codes, sparse vectors, or approximants and prove that a suitable deterministic construction exists.",
      "source_categories": [
        {
          "dataset": "high_dimensional_statistics",
          "id": "high_dimensional_statistics_26",
          "name": "Probabilistic method and packing constructions"
        }
      ]
    },
    {
      "id": "family_probability_information",
      "label": "Probability, concentration, and information methods",
      "level": 1,
      "description": "Probabilistic proof methods based on exponential moments, tails, independence, union bounds, and information-theoretic reductions.",
      "source_categories": []
    },
    {
      "id": "sub_exponential_concentration",
      "label": "Exponential-moment and concentration arguments",
      "level": 2,
      "description": "Apply exponential Markov inequalities, control moment-generating functions, and optimize parameters to derive tail bounds.",
      "source_categories": [
        {
          "dataset": "high_dimensional_statistics",
          "id": "high_dimensional_statistics_21",
          "name": "Exponential-moment and concentration arguments"
        }
      ]
    },
    {
      "id": "sub_tail_integration",
      "label": "Tail integration and moment estimates",
      "level": 2,
      "description": "Convert moments into tail integrals, insert probability bounds, and estimate the resulting integrals.",
      "source_categories": [
        {
          "dataset": "high_dimensional_statistics",
          "id": "high_dimensional_statistics_22",
          "name": "Tail integration and moment estimates"
        }
      ]
    },
    {
      "id": "sub_independence_tensorization",
      "label": "Independence, tensorization, and union bounds",
      "level": 2,
      "description": "Factor quantities using independence, tensorize information, and upgrade pointwise bounds to simultaneous bounds by a union bound.",
      "source_categories": [
        {
          "dataset": "high_dimensional_statistics",
          "id": "high_dimensional_statistics_23",
          "name": "Independence, tensorization, and union bounds"
        }
      ]
    },
    {
      "id": "sub_testing_information",
      "label": "Testing and information-theoretic reductions",
      "level": 2,
      "description": "Reduce estimation to hypothesis testing and control testing error using divergence or mutual-information inequalities.",
      "source_categories": [
        {
          "dataset": "high_dimensional_statistics",
          "id": "high_dimensional_statistics_25",
          "name": "Testing and information-theoretic reductions"
        }
      ]
    }
  ],
  "edges": [
    {
      "source": "family_definitional_reformulation",
      "target": "sub_definitional_unfolding",
      "relation": "parent_of",
      "rationale": "Definitional unfolding is the direct expansion branch of the broader reformulation family."
    },
    {
      "source": "family_definitional_reformulation",
      "target": "sub_metric_filter_characterization",
      "relation": "parent_of",
      "rationale": "Metric and filter criteria are standard equivalent reformulations of analytic definitions."
    },
    {
      "source": "family_definitional_reformulation",
      "target": "sub_canonical_rewriting",
      "relation": "parent_of",
      "rationale": "Canonical rewriting replaces abstract notions by equivalent concrete forms."
    },
    {
      "source": "family_definitional_reformulation",
      "target": "sub_set_extensionality",
      "relation": "parent_of",
      "rationale": "Set extensionality and Boolean simplification are specialized definitional and reformulation techniques."
    },
    {
      "source": "family_normalization_symmetry",
      "target": "sub_canonical_rewriting",
      "relation": "parent_of",
      "rationale": "Concrete norm, metric, slope, and interval rewrites are elementary canonical-normalization steps."
    },
    {
      "source": "family_standard_theorem_reduction",
      "target": "sub_regularity_transfer",
      "relation": "parent_of",
      "rationale": "Restriction, extension, and regularity transfer are used to align hypotheses with a standard theorem."
    },
    {
      "source": "family_algebra_order_norm",
      "target": "sub_elementary_algebra_order",
      "relation": "parent_of",
      "rationale": "Elementary ordered-field manipulations form the scalar algebraic branch of the broader estimate family."
    },
    {
      "source": "family_topology_compactness_connectedness",
      "target": "sub_compactness",
      "relation": "parent_of",
      "rationale": "The target is the compactness-specific branch of the combined topological family."
    },
    {
      "source": "family_topology_compactness_connectedness",
      "target": "sub_intermediate_value",
      "relation": "parent_of",
      "rationale": "The Intermediate Value Theorem is the interval-connectedness branch of the broader family."
    },
    {
      "source": "family_extremal_order",
      "target": "sub_order_completeness",
      "relation": "parent_of",
      "rationale": "Least-upper-bound and greatest-lower-bound reasoning is a specific order-theoretic extremal method."
    },
    {
      "source": "family_limits_completeness",
      "target": "sub_limit_laws_squeezing",
      "relation": "parent_of",
      "rationale": "Limit laws, squeezing, and uniqueness are core sub-branches of limit arguments."
    },
    {
      "source": "family_limits_completeness",
      "target": "sub_sequence_completeness",
      "relation": "parent_of",
      "rationale": "Sequence and Cauchy-completeness methods specialize the broader limit and completeness family."
    },
    {
      "source": "family_limits_completeness",
      "target": "sub_monotone_limsup_subsequence",
      "relation": "parent_of",
      "rationale": "Monotone convergence, limsup, and subsequence extraction are specific sequential limit methods."
    },
    {
      "source": "family_limits_completeness",
      "target": "sub_metric_filter_characterization",
      "relation": "cross_link",
      "rationale": "Metric and filter characterizations provide the formulations used by many limit arguments but also apply to continuity and other notions."
    },
    {
      "source": "family_differential_calculus",
      "target": "sub_difference_quotient",
      "relation": "parent_of",
      "rationale": "Difference quotients are the characterization branch of differential calculus."
    },
    {
      "source": "family_differential_calculus",
      "target": "sub_derivative_rules",
      "relation": "parent_of",
      "rationale": "Derivative rules are a standard computational sub-branch of differential calculus."
    },
    {
      "source": "family_differential_calculus",
      "target": "sub_mean_value_theorems",
      "relation": "parent_of",
      "rationale": "Fermat, Rolle, and mean-value principles are standard differential-calculus theorems."
    },
    {
      "source": "family_differential_calculus",
      "target": "sub_derivative_sign",
      "relation": "parent_of",
      "rationale": "Derivative-sign methods specialize differential calculus to monotonicity and extrema."
    },
    {
      "source": "family_differential_calculus",
      "target": "sub_taylor_remainder",
      "relation": "parent_of",
      "rationale": "Taylor expansion is the higher-order approximation branch of differential calculus."
    },
    {
      "source": "family_error_decomposition",
      "target": "sub_triangle_error_estimates",
      "relation": "parent_of",
      "rationale": "Triangle-based splitting is a basic specific form of error decomposition."
    },
    {
      "source": "family_algebra_order_norm",
      "target": "sub_triangle_error_estimates",
      "relation": "parent_of",
      "rationale": "The target is also a norm-estimate method based on triangle and reverse-triangle inequalities."
    },
    {
      "source": "family_error_decomposition",
      "target": "sub_approximation_archimedean",
      "relation": "parent_of",
      "rationale": "Approximation error and the choice of an index to meet a tolerance form a specialized error-control strategy."
    },
    {
      "source": "family_explicit_construction",
      "target": "sub_approximation_archimedean",
      "relation": "parent_of",
      "rationale": "The approximation strategy explicitly chooses an approximant and a sufficiently large index."
    },
    {
      "source": "family_comparison_domination",
      "target": "sub_limit_laws_squeezing",
      "relation": "parent_of",
      "rationale": "Squeezing is a limit-specific instance of comparison and domination."
    },
    {
      "source": "family_comparison_domination",
      "target": "sub_series_tests",
      "relation": "parent_of",
      "rationale": "Comparison with summable majorants is a principal series-convergence technique."
    },
    {
      "source": "family_comparison_domination",
      "target": "sub_uniform_convergence_mtest",
      "relation": "parent_of",
      "rationale": "The Weierstrass M-test is a uniform domination argument."
    },
    {
      "source": "family_series_convergence",
      "target": "sub_series_tests",
      "relation": "parent_of",
      "rationale": "The target contains the detailed summability tests covered broadly by the parent."
    },
    {
      "source": "family_series_convergence",
      "target": "sub_uniform_convergence_mtest",
      "relation": "parent_of",
      "rationale": "Uniform convergence and the M-test are a distinct sub-branch of the broader series family."
    },
    {
      "source": "family_series_convergence",
      "target": "sub_power_series_radius",
      "relation": "parent_of",
      "rationale": "Radius-of-convergence reasoning is a power-series-specific branch of series analysis."
    },
    {
      "source": "family_integral_calculus",
      "target": "sub_fundamental_theorem_calculus",
      "relation": "parent_of",
      "rationale": "The Fundamental Theorem of Calculus is a specific central branch of integral calculus."
    },
    {
      "source": "family_integral_calculus",
      "target": "sub_integral_structure",
      "relation": "parent_of",
      "rationale": "Linearity, additivity, and monotonicity are structural sub-techniques of integration."
    },
    {
      "source": "family_integral_calculus",
      "target": "sub_integration_transformations",
      "relation": "parent_of",
      "rationale": "Integration by parts and substitution are specific integration transformations."
    },
    {
      "source": "family_integral_calculus",
      "target": "sub_partition_refinement",
      "relation": "parent_of",
      "rationale": "Partition and refinement methods form a Riemann-integration sub-branch."
    },
    {
      "source": "sub_partition_refinement",
      "target": "sub_riemann_modulus_control",
      "relation": "parent_of",
      "rationale": "Modulus-of-continuity control is a more specific refinement-based method for comparing Riemann sums."
    },
    {
      "source": "family_error_decomposition",
      "target": "sub_riemann_modulus_control",
      "relation": "cross_link",
      "rationale": "The method decomposes and sums local discretization errors, although its primary setting is Riemann integration."
    },
    {
      "source": "family_explicit_construction",
      "target": "sub_partition_refinement",
      "relation": "cross_link",
      "rationale": "Partition proofs often require explicit construction of common refinements, but the category is primarily an integration method."
    },
    {
      "source": "family_structural_foundations",
      "target": "sub_ordered_field_constructions",
      "relation": "parent_of",
      "rationale": "Ordered-field constructions using cuts and completeness instantiate the completion component of the parent."
    },
    {
      "source": "family_structural_foundations",
      "target": "sub_cardinality_embeddings",
      "relation": "parent_of",
      "rationale": "Cardinality comparisons and mutual embeddings instantiate the embedding component of the parent."
    },
    {
      "source": "family_explicit_construction",
      "target": "sub_ordered_field_constructions",
      "relation": "cross_link",
      "rationale": "Canonical field witnesses are explicit constructions, though the category also contains substantial structural theory."
    },
    {
      "source": "family_structural_foundations",
      "target": "sub_order_completeness",
      "relation": "cross_link",
      "rationale": "Order completeness is used in structural characterizations and completions of the real numbers."
    },
    {
      "source": "family_variational_linear_algebra",
      "target": "sub_convexity_variational",
      "relation": "parent_of",
      "rationale": "Convex optimality and competitor arguments form the variational branch of the family."
    },
    {
      "source": "family_variational_linear_algebra",
      "target": "sub_orthogonality_spectral",
      "relation": "parent_of",
      "rationale": "Orthogonality, projection, and spectral methods form the linear-algebraic branch."
    },
    {
      "source": "family_variational_linear_algebra",
      "target": "sub_structured_parameters",
      "relation": "parent_of",
      "rationale": "Sparse and low-rank decompositions are structured geometric and linear-algebraic methods."
    },
    {
      "source": "family_extremal_order",
      "target": "sub_convexity_variational",
      "relation": "cross_link",
      "rationale": "Convexity often reduces extrema to special points or derives optimality conditions, but it is not merely order completeness."
    },
    {
      "source": "family_algebra_order_norm",
      "target": "sub_structured_parameters",
      "relation": "parent_of",
      "rationale": "Norm duality and absorption of cross terms are central algebraic-estimate components of structured-parameter arguments."
    },
    {
      "source": "family_metric_entropy",
      "target": "sub_covering_volumetric",
      "relation": "parent_of",
      "rationale": "Finite-net discretization and volume bounds are the covering branch of metric entropy."
    },
    {
      "source": "family_metric_entropy",
      "target": "sub_probabilistic_packing",
      "relation": "parent_of",
      "rationale": "Random construction of separated sets is a packing branch of metric-entropy methods."
    },
    {
      "source": "family_explicit_construction",
      "target": "sub_probabilistic_packing",
      "relation": "parent_of",
      "rationale": "The probabilistic method is an existence-oriented construction strategy, even though the candidates are generated randomly."
    },
    {
      "source": "family_probability_information",
      "target": "sub_exponential_concentration",
      "relation": "parent_of",
      "rationale": "Exponential-moment bounds are a central concentration sub-family."
    },
    {
      "source": "family_probability_information",
      "target": "sub_tail_integration",
      "relation": "parent_of",
      "rationale": "Tail-to-moment conversion is a probabilistic moment-estimation method."
    },
    {
      "source": "family_probability_information",
      "target": "sub_independence_tensorization",
      "relation": "parent_of",
      "rationale": "Independence, product structure, and union bounds are basic probabilistic proof mechanisms."
    },
    {
      "source": "family_probability_information",
      "target": "sub_testing_information",
      "relation": "parent_of",
      "rationale": "Testing reductions and divergence inequalities form the information-theoretic branch."
    },
    {
      "source": "family_probability_information",
      "target": "sub_probabilistic_packing",
      "relation": "cross_link",
      "rationale": "Probabilistic packing arguments use random sampling and probability bounds in addition to metric-entropy structure."
    },
    {
      "source": "family_integral_calculus",
      "target": "sub_tail_integration",
      "relation": "parent_of",
      "rationale": "Tail integration is a specialized use of integral calculus, including substitutions and threshold splitting, within probability."
    },
    {
      "source": "family_comparison_domination",
      "target": "sub_tail_integration",
      "relation": "cross_link",
      "rationale": "Moment bounds arise by inserting a dominating tail estimate into an integral."
    },
    {
      "source": "sub_exponential_concentration",
      "target": "sub_independence_tensorization",
      "relation": "cross_link",
      "rationale": "Independence frequently factors moment-generating functions and union bounds convert fixed-direction concentration into simultaneous bounds."
    },
    {
      "source": "sub_covering_volumetric",
      "target": "sub_exponential_concentration",
      "relation": "cross_link",
      "rationale": "Finite-net reductions are commonly combined with concentration and union bounds to control continuous suprema."
    },
    {
      "source": "sub_probabilistic_packing",
      "target": "sub_testing_information",
      "relation": "cross_link",
      "rationale": "Information-theoretic lower bounds often require a large finite packing of well-separated hypotheses."
    }
  ],
  "unmapped_source_categories": []
}
```
