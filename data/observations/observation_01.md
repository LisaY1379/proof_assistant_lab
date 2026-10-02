# Observation 01: Elementary proofs explained through observations

## Working protocol

The purpose is to explain both how a proof works and what makes its strategic moves reasonable choices. These decompositions reconstruct possible motivations; they do not claim to report a historical discovery process.

We use the distinctions established in our discussion:

- **Basic — definition:** Directly interpret a definition appearing in the assumptions or goal.
- **Basic — calculation:** Execute an elementary calculation, such as substitution, expansion, or arithmetic simplification. Arbitrary algebraically valid rewriting is not automatically basic.
- **Basic — logic:** Unpack or combine statements using elementary logical rules, including introducing an arbitrary object, applying an implication to an established premise, and concluding from exhaustive cases.
- **Strategic:** Identify a relevant relationship and choose a useful representation, intermediate goal, case split, witness, or proof method. A strategic step may be very elementary.

**Toolkit use** is recorded separately as a description of which available fact or method a step calls. It is not a fourth kind of basic operation. Selecting a useful theorem or method can be strategic; applying its implication after its premises have been established can be basic logic. We explicitly state the background results being assumed rather than silently calling all familiar results basic.

For a strategic step, record:

1. **Current state:** What we currently know or have expressed.
2. **Goal observation:** What form or property the goal requires.
3. **Current-state observation:** What relevant feature is present in the available expression or assumptions.
4. **Connection and move:** Why those observations suggest this move.
5. **Verification and remaining obligations:** Check the move and identify what is still needed.

A **goal reinterpretation** replaces a goal by an equivalent formulation chosen to make an available tool applicable. A sufficient-condition reduction need not be equivalent and will be described separately.

The goal maps below show dependencies, not a required chronological discovery order. The toolkit and goal map can develop together. Basic steps can occur anywhere, including after a strategic choice.

## 1. The sum of two even integers is even

### Problem and toolkit

Given even integers a and b, prove that a+b is even.

Available resources: the definition of evenness, elementary arithmetic and equality rules, and closure of integers under addition.

### Goal map

\[
a+b\text{ is even}
\quad\Longleftrightarrow\quad
\exists k\in\mathbb Z:\ a+b=2k.
\]

The assumptions supply integers m,n with a=2m and b=2n. The gap is between the expression 2m+2n and the target form 2k. Factoring exposes a candidate k=m+n; integer closure then supplies the remaining obligation.

### Step decomposition

| Step | Action | Category and role |
| --- | --- | --- |
| 1 | Interpret the goal as finding an integer k such that a+b=2k. | **Basic — definition.** Unpack evenness. |
| 2 | Write a=2m and b=2n for some integers m,n. | **Basic — definition and logic.** Unpack the assumptions and name their witnesses. |
| 3 | Substitute to obtain a+b=2m+2n. | **Basic — calculation.** |
| 4 | Observe that the target requires a factor 2 and both available summands contain that factor. Choose the representation 2(m+n), revealing the candidate k=m+n. | **Strategic — match the current expression to the goal.** |
| 5 | Verify the chosen representation by expanding 2(m+n)=2m+2n. | **Basic — calculation.** Checks the choice made in Step 4. |
| 6 | From m,n being integers, conclude that m+n is an integer. | **Basic — logic; toolkit: integer closure under addition.** |
| 7 | Use the established witness k=m+n to conclude that a+b is even. | **Basic — logic and definition.** |

### Observation behind the strategy

“Our goal asks for twice an integer. Our current expression is 2m+2n, and both summands contain precisely the factor 2 required by the goal. Factoring out that shared 2 produces the desired pattern, with the remaining expression m+n as the candidate integer.”

The explanation should not stop at “factor out 2.” The match between the target and the available common factor explains the choice. The gap is informally small because the desired factor is explicit and one rewrite exposes the witness. This does not yet define a general numerical measure of gap size.

## 2. For every integer n, the integer n²+n is even

### Problem and toolkit

Prove that n²+n is even for every integer n.

Available resources: definitions of even and odd integers, the fact that every integer is even or odd, closure of integers under addition and multiplication, and elementary arithmetic and logic.

### Goal map

\[
n^2+n\text{ is even}
\quad\Longleftrightarrow\quad
\exists k\in\mathbb Z:\ n^2+n=2k.
\]

There is no explicit factor 2 to extract immediately. A strategic rewrite gives n(n+1), exposing consecutive integers. A parity split then locates a factor 2 in one of the two factors. Each branch supplies an integer witness for the original goal.

### Step decomposition

| Step | Action | Category and role |
| --- | --- | --- |
| 1 | Fix an arbitrary integer n and interpret the goal as n²+n=2k for some integer k. | **Basic — logic and definition.** |
| 2 | Observe that a product with an even factor can supply the required factor 2, and the two terms n² and n share a factor n. Choose the rewrite n²+n=n(n+1) to inspect the factors. | **Strategic — exploratory change of representation.** It exposes structure without yet finishing the proof. |
| 3 | Verify n(n+1)=n²+n by expansion. | **Basic — calculation.** |
| 4 | Observe that n and n+1 are consecutive: if n does not itself supply a factor 2, adding 1 to an odd n does. Choose cases according to whether n is even or odd. | **Strategic — select a case split motivated by the factorization.** Toolkit: parity of integers. |
| 5 | In the even case, write n=2q for an integer q. Substitute to get n(n+1)=(2q)(n+1). | **Basic — definition, logic, and calculation.** |
| 6 | Observe that the displayed factor 2 can be put outside the entire product. Choose k=q(n+1), so the target representation is 2[q(n+1)]. | **Strategic — expose the required form and witness.** This repeats the elementary matching move of Problem 1. |
| 7 | Verify (2q)(n+1)=2[q(n+1)] and that q(n+1) is an integer; conclude this branch. | **Basic — calculation and logic.** Toolkit: integer closure. |
| 8 | In the odd case, write n=2q+1 for an integer q. Calculate n+1=2q+2. | **Basic — definition, logic, and calculation.** |
| 9 | The factor n+1 now has the form 2q+2. Observe the common factor 2 and choose n+1=2(q+1); consequently choose k=n(q+1). | **Strategic — factor and match the product to 2k.** |
| 10 | Expand to verify 2(q+1)=2q+2, verify n[2(q+1)]=2[n(q+1)], and establish that n(q+1) is an integer. Conclude this branch. | **Basic — calculation and logic.** Toolkit: integer closure. |
| 11 | Since every integer is even or odd and both branches establish the goal, conclude the claim for the arbitrary n, hence for every integer n. | **Basic — logic.** Toolkit: exhaustive parity alternatives. |

### Observations behind the strategies

**Why try factoring?** “We need a factor 2, but none is explicit in the sum. A product could make an even factor usable. The shared n lets us inspect the product n(n+1).” This makes factoring a reasonable trial; it does not guarantee in advance that every factorization will help.

**Why split by parity?** “The factors are consecutive. When n is even it already supplies the needed 2; when n is odd, n+1 supplies it. The parity of n therefore determines where the useful factor will appear.”

Choosing the split is strategic. Combining the completed cases is basic logic. Knowing the toolkit fact that integers have two parity cases does not, by itself, explain why those are useful cases here.

## 3. For x>0, prove x+1/x ≥ 2

### Problem and toolkit

For a positive real number x, prove

\[
x+\frac1x\ge 2.
\]

Available resources: ordered-field arithmetic, preservation of an inequality when multiplying by a positive quantity, and nonnegativity of real squares.

### Goal map

For x>0, the following goals are equivalent:

\[
x+\frac1x\ge 2
\quad\Longleftrightarrow\quad
x^2+1\ge 2x
\quad\Longleftrightarrow\quad
x^2-2x+1\ge 0
\quad\Longleftrightarrow\quad
(x-1)^2\ge 0.
\]

The equivalences form a backward goal map. The last goal is supplied by the toolkit, and the equivalences carry it back to the original claim.

### Step decomposition

| Step | Action | Category and role |
| --- | --- | --- |
| 1 | Fix an arbitrary real x>0; in particular, x is nonzero. | **Basic — logic.** |
| 2 | Observe that 1/x is the only reciprocal term and that the assumption x>0 permits multiplication by x without changing the direction of the inequality. Choose to clear the denominator. | **Strategic — goal reinterpretation using an available condition.** |
| 3 | Apply the positive-multiplication rule and calculate x(x+1/x)=x²+1 and x·2=2x. The goal is equivalent to x²+1≥2x. | **Basic — calculation and logic.** Toolkit: order and multiplication by a positive real. |
| 4 | Observe that the goal compares two expressions, while square nonnegativity has the form E≥0. Choose to place their difference on the left, giving x²−2x+1≥0. | **Strategic — reinterpret the comparison as nonnegativity.** |
| 5 | Verify this equivalence by subtracting 2x from both sides and simplifying. | **Basic — calculation and logic.** Toolkit: order under addition. |
| 6 | Observe the terms x², −2x, and 1: they match the expansion of a square with terms x and 1. Choose the representation (x−1)². | **Strategic — recognize a square that fits the nonnegativity goal.** |
| 7 | Expand (x−1)²=x²−2x+1 to verify the proposed identity. | **Basic — calculation.** |
| 8 | Since x−1 is real, apply square nonnegativity to obtain (x−1)²≥0. | **Basic — logic; toolkit: real squares are nonnegative.** |
| 9 | Substitute the verified identity and follow the established equivalences back to conclude x+1/x≥2. | **Basic — calculation and logic.** |

### Observations behind the strategies

“The reciprocal prevents immediate polynomial calculation, but its denominator is also the positive quantity supplied by the hypothesis. Multiplying by it removes the reciprocal while preserving the comparison. The resulting difference has the pattern of a square, connecting the goal to square nonnegativity.”

The strategic actions are selecting these representations. The calculations validating them remain basic. In particular, recognizing x²−2x+1 as a useful square is strategic even though expanding the proposed square is elementary.

## 4. A composition of injective functions is injective

### Problem and toolkit

Let f:A→B and g:B→C be injective. Prove that g∘f is injective.

Available resources: definitions of injectivity and composition, function domains and codomains, and elementary logical inference.

### Goal map

By definition, we must prove

\[
\forall a,b\in A,\quad
(g\circ f)(a)=(g\circ f)(b)\ \Longrightarrow\ a=b.
\]

Expanding composition supplies g(f(a))=g(f(b)). Injectivity of g yields f(a)=f(b); injectivity of f then yields a=b.

### Step decomposition

| Step | Action | Category and role |
| --- | --- | --- |
| 1 | Expand the target definition of injectivity. | **Basic — definition.** |
| 2 | Take arbitrary a,b∈A and assume (g∘f)(a)=(g∘f)(b); the remaining goal is a=b. | **Basic — logic.** Introduce arbitrary elements and the premise of an implication. |
| 3 | Expand composition to obtain g(f(a))=g(f(b)). | **Basic — definition.** |
| 4 | From f:A→B, establish f(a),f(b)∈B. | **Basic — definition and logic.** Checks the inputs required for injectivity of g. |
| 5 | Expand the given injectivity of g: for u,v∈B, g(u)=g(v) implies u=v. | **Basic — definition.** |
| 6 | Substitute u=f(a), v=f(b) into that implication and apply it to the equality from Step 3, obtaining f(a)=f(b). | **Basic — logic.** Direct instantiation and application of the expanded assumption. |
| 7 | Expand the given injectivity of f and apply it to f(a)=f(b), obtaining a=b. | **Basic — definition and logic.** |
| 8 | Discharge the assumed equality and generalize over arbitrary a,b∈A. Conclude that g∘f is injective. | **Basic — logic and definition.** |

### Observations explaining the order

“The current equality has g as the outer function on both sides, so it directly matches the premise in the definition of injectivity of g. Removing that outer layer leaves an equality matching the premise for injectivity of f.”

Under our working protocol, this proof has **no separate strategic step**: after expanding the relevant definitions, the available equality directly supplies the premise of an available implication. We introduce no auxiliary object, alternate algebraic form, or additional case split.

This is a useful boundary example. An observation can explain a basic inference too. The presence of matching or an explanatory observation alone does not make a step strategic; direct logical instantiation is one of the basic operations we expressly allow. These classifications remain provisional until that allowed logical vocabulary is formalized.

## 5. The sum of the first n odd positive integers is n²

### Problem and notation

For every positive integer n, prove

\[
1+3+\cdots+(2n-1)=n^2.
\]

Write

\[
S_n=\sum_{j=1}^{n}(2j-1).
\]

The notation names the existing sum. It immediately gives S₁=1 and Sₙ₊₁=Sₙ+2n+1 by separating the last summand.

Two routes illustrate different strategic observations.

### Route A: Induction

#### Toolkit and goal map

Available resources: finite-sum notation, elementary arithmetic and logic, and induction on the positive integers.

Let P(n) mean Sₙ=n². The induction principle reduces the universal goal to

\[
P(1)
\qquad\text{and}\qquad
\forall n\ge1:\ P(n)\Longrightarrow P(n+1).
\]

This is a reduction justified by a selected theorem, rather than merely an expansion of the phrase “for every positive integer.”

#### Step decomposition

| Step | Action | Category and role |
| --- | --- | --- |
| 1 | Name the existing sum Sₙ and the statement P(n). Read off Sₙ₊₁=Sₙ+2n+1 from the summands. | **Basic — definition and calculation.** |
| 2 | Observe that the sum at n+1 contains the sum at n plus one explicit term. The goal also provides a proposed value n² for that smaller sum. Choose induction to make that proposed value available in the next case. | **Strategic — select a proof method from the relationship between adjacent cases.** Toolkit: induction. |
| 3 | Use the induction principle to set the base goal P(1) and the implication goal P(n)⇒P(n+1). | **Basic — logic once the method is selected.** Instantiates the chosen principle. |
| 4 | Calculate S₁=1=1². | **Basic — calculation.** Establishes the base case. |
| 5 | Fix n≥1 and assume P(n), namely Sₙ=n². | **Basic — logic.** Introduces the premise of the induction-step implication. |
| 6 | Substitute this premise into Sₙ₊₁=Sₙ+2n+1 to obtain Sₙ₊₁=n²+2n+1. | **Basic — calculation.** |
| 7 | The current subgoal explicitly asks for Sₙ₊₁=(n+1)². Expand this already specified right-hand side: (n+1)²=n²+2n+1. | **Basic — calculation.** No square has to be invented or selected here; it is in the target. |
| 8 | The two calculations have the same result, so Sₙ₊₁=(n+1)². Discharge the assumption to establish P(n)⇒P(n+1). | **Basic — logic.** Equality and implication introduction. |
| 9 | Apply the selected induction principle to the established base case and implication. | **Basic — logic; toolkit: induction.** Concludes P(n) for all positive integers. |

#### Observation behind the strategy

“Adding one more odd number changes the sum by a known amount. If we could use the claimed formula for the shorter sum, the next case would reduce to checking an explicit algebraic identity. Induction supplies exactly that permission, provided we also establish the initial case.”

Step 7 is deliberately written as expansion of the target. Recognizing an unrequested square can be strategic, but calculating a square already displayed in the goal is basic. Classification concerns the directed action and its context, not just the identity written on the page.

### Route B: Rewrite the summands as differences of squares

#### Toolkit and goal map

Available resources: finite sums, distributivity and cancellation, square expansion, and elementary equality rules. No induction assumption or formula for the sum of consecutive integers is used in this route.

Seek a representation that reduces the sum to its endpoints:

\[
S_n
=\sum_{j=1}^{n}\bigl(j^2-(j-1)^2\bigr)
=n^2-0^2
=n^2.
\]

This display is the finished route; the observations below explain how to propose it.

#### Step decomposition

| Step | Action | Category and role |
| --- | --- | --- |
| 1 | Observe that the target is a square and the summands grow linearly as 2j−1. Differences of consecutive squares are a plausible source of such linear expressions. Choose to investigate j²−(j−1)². | **Strategic — use the target to suggest an auxiliary expression.** |
| 2 | Expand j²−(j−1)²=j²−(j²−2j+1)=2j−1. | **Basic — calculation.** Verifies the candidate relationship. |
| 3 | Observe that the negative term −(j−1)² cancels the previous summand's positive square. Choose to rewrite every summand using the verified identity so that this cancellation becomes available. | **Strategic — connect the local identity to the whole-sum goal.** |
| 4 | Substitute the identity into the finite sum. | **Basic — calculation.** Executes the selected rewrite. |
| 5 | Cancel the matching interior square terms, leaving n²−0². | **Basic — calculation.** Uses ordinary finite-sum addition and cancellation. |
| 6 | Calculate n²−0²=n² and conclude for the arbitrary positive integer n. | **Basic — calculation and logic.** |

The cancellation can be checked explicitly for every n≥1 by writing

\[
\begin{aligned}
\sum_{j=1}^{n}\bigl(j^2-(j-1)^2\bigr)
&=\left(\sum_{j=1}^{n-1}j^2+n^2\right)
 -\left(0^2+\sum_{j=1}^{n-1}j^2\right)\\
&=n^2-0^2.
\end{aligned}
\]

Here an empty sum is 0, so the displayed calculation includes n=1. The finite-sum rules are the permitted arithmetic vocabulary for this decomposition; expanding their foundations would be a separate level of detail.

#### Observations behind the strategies

“The answer is a square, while each summand is linear in its index. Subtracting nearby squares may produce exactly such a linear term. Calculating the difference confirms that it is the required odd number. Moreover, these differences line up across adjacent indices, so summing them leaves only the final square and the initial zero.”

The first observation suggests an experiment. The basic calculation confirms it. The cancellation observation then explains how to turn that successful experiment into a proof of the full goal. This route illustrates the toolkit and goal map developing together.

## What these examples clarify

- **Factoring can be an elementary strategic step.** In Problem 1, the useful observation matches an available common factor to the factor demanded by the definition.
- **A strategic move can reveal structure without immediately finishing the goal.** In Problem 2, factoring first reveals the consecutive-integer structure that motivates a parity split.
- **Goal reinterpretation can make an existing tool applicable.** In Problem 3, successive equivalent forms expose square nonnegativity.
- **Basic work can occur throughout a proof.** It verifies strategic proposals, computes inside their subgoals, and combines their conclusions.
- **Not every observation is strategic.** Problem 4 uses observations to explain direct definitional and logical inferences. Treating every act of matching as strategic would erase our basic-logic category.
- **The same identity can serve different kinds of action.** Recognizing a useful square is strategic; expanding a square already required by the target is basic.
- **Different proofs expose different observations.** Induction in Problem 5 uses the relation between adjacent cases; the alternative proof uses differences of squares and cancellation.

The remaining formal task is to fix the permitted elementary operations and their directions precisely. These examples supply concrete cases that such a definition should preserve, rather than assuming that “easy,” “familiar,” or “already specified” is by itself a sufficient definition of basic.
