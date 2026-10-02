# Graph-Based Representations of Formal Proof Search

We are developing a framework for representing **how a mathematical proof is discovered, why its steps are chosen, and where its difficulty lies**. The eventual purpose is to identify which steps deserve more explanation in a mathematical paper, helping readers understand both the argument and its motivation.

## 1. Represent a proof through facts, goals, and observations

A conventional proof presents a successful sequence of deductions. Our representation separates two interacting layers:

- **Forward graph:** starts from the given assumptions and derives established facts.
- **Backward graph:** starts from the ultimate goal and decomposes it into sufficient subgoals.

These layers develop together and eventually connect when the facts obtained establish the required goals.

There are three principal node types:

- **Fact:** something given or established.
- **Goal:** something still to be proved.
- **Observation:** a noticed feature or relationship that motivates a strategic move.

An observation is not itself a justification. The resulting move still needs mathematical verification.

Observations can arise while exploring the available facts or be inspired by a particular goal. Goal-inspired observations have explicit links to the goals that motivated them.

## 2. Distinguish elementary execution from strategic choice

We provisionally recognize three types of basic steps:

1. **Direct interpretation of definitions.**
2. **Direct elementary calculations.**
3. **Basic logical operations.**

Choosing a useful transformation can be strategic even when verifying it is elementary.

For example, in proving that the sum of two even integers is even, we reach \(2m+2n\) and need an expression of the form \(2k\). The explanation should expose the observation:

> The target requires a factor of \(2\), and both summands already contain that factor. Factoring therefore produces the required form.

The choice to factor is strategic; checking the identity and that \(m+n\) is an integer is basic.

Our proposed priority is:

**Attempt basic progress → identify the obstruction → make an observation → choose a strategic move or reinterpret the goal → resume basic progress.**

Goal reinterpretations must state whether the new goal is equivalent to the original or merely sufficient to establish it.

## 3. Extend the representation from a finished proof to its search history

We propose having a proof generator attempt problems without access to the reference solution or future proof steps. It should record candidate moves, observations, outcomes, abandoned branches, and alternative successful routes.

This is proof discovery as route search. The final proof is one successful route; the exploration log records the surrounding territory investigated along the way.

An unsuccessful branch must be classified carefully: invalid, insufficient, expensive, or simply unresolved within the allotted budget. Failure to finish does not establish that a route is impossible.

Masking the reference proof prevents direct solution access; it does not guarantee that a pretrained generator has never encountered the problem.

## 4. Measure difficulty within a fixed framework

Our immediate aim is **framework-relative objective difficulty**, not personalized difficulty based on a reader’s experience.

We fix the starting information, available toolkit, permitted operations, and cost rules. We then investigate separately:

- **Structural difficulty:** properties of the valid proof routes, such as the minimum cost of establishing a target.
- **Search difficulty:** the resources a specified search procedure requires to discover a valid route.

A short proof may be difficult to discover; a long calculation may be straightforward to find. These quantities should not be collapsed into one score. The best route found experimentally is not automatically the cheapest possible route.

## 5. Research positioning

AlphaProof provides a motivating formal proof-search model: proof states, actions, verified transitions, and guided exploration. We propose building a measurement and explanatory framework on that foundation, rather than initially building a competitive prover.

Our additional focus is explicit observations, strategic transitions, exploration histories, and quantified costs. Definitions, benchmarks, and controlled experiments are still to be developed.

A central research question is:

> Under fixed rules and resources, where are the costly transitions in a proof, and which observations help a search procedure cross them?

A later question is whether explaining those transitions improves human comprehension. Automated search cost should not be assumed to equal human reading difficulty.

## 6. Current implementation

The project already contains a public interactive Hanson–Wright proof explorer with:

- Forward and backward proof layers.
- Explicit fact, goal, and observation nodes.
- Dotted links from observations to motivating goals.
- A reconstructed thinking-order animation.
- A synchronized textbook-style written proof.
- An introductory walkthrough of the representation protocol.

The explorer currently illustrates a reconstructed successful proof. The proposed experimental search engine, comprehensive trial logs, and difficulty benchmarks are future work.