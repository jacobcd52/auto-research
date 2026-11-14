# Feedback: 03 "Is it really belief propagation?"

Verdict: **major overhaul, then fundable.** The question is good and cheap, but a 10-minute offline simulation I ran suggests the central design (matched "BP wrong" vs "BP right" sets) rests on a wrong picture of how loopy BP behaves on these instances. The hypothesis family and instance sets need rebuilding before any API money is spent.

## What I checked

| Claim in proposal | Status |
|---|---|
| Description of MBaert's post (hard and soft BCH tasks, 4x filter, marginal/MAP-gap correlation, cached-prefix trajectories, "limit of black-box") | Accurate against the full post text. |
| "The post never runs belief propagation on the same instances" | **Overstated.** The post says textbook BP "usually converges reasonably quickly for these BCH test cases, and behaves far less chaotically", so the author did run BP at least informally. What is missing is any reported comparison of BP's *answers or beliefs* with Astra's. |
| No follow-up has done this | Holds as far as I can tell. I scanned LessWrong post titles from 2026-09-14 to 2026-11-14 and the post's comments (two, neither substantive). The author has not posted a follow-up. Nearest neighbour is "Generalized belief states in transformers" (Kolchinsky, 2026-10-31, 74 karma), which is not about this task. |
| OpenRouter prices | Correct: Astra $10 / $50, cache read $1; GPT-6.1 Sol $2 / $10; GPT-5.6 Sol $4 / $20. Omitted: Astra cache *write* is $12.50/M (more than uncached input), and `:batch` variants are half price ($5 / $25 for Astra). |
| Generator "if it is in github.com/MaartenBaert/LatentMathBench" | The repo exists (README fetched), but the BP post links no code and I found no BCH file at the paths I guessed; I could not list the tree. Assume the generator must be reimplemented. The post's "randomised BCH construction" and choice of which parity checks to show are unspecified. |
| "GPT-5.6 Sol manages about 4 variables" | Correct, which makes it useless as a contrast at 7–13 variables. |

## A simulation that changes the design

I built shortened, column-permuted BCH(15,7,5) codes with 8 randomly chosen low-weight parity checks (matching the post's 10-variable example: 8 checks, mean weight about 4), priors uniform in 10–90%, the 4x MAP filter, and sum-product BP with a flooding schedule. The BP code reproduces exact marginals on a tree. 300–400 instances per size.

| Variables | Valid solutions | BP (100 iters) wrong vs MAP | Damped BP wrong | Min-sum wrong | All three wrong | Thresholded exact marginals wrong |
|---|---|---|---|---|---|---|
| 9 | 2 | 87% | 87% | 72% | 71% | 0% |
| 10 | 4 | 77% | 77% | 59% | 56% | 0% |
| 11 | 8 | 73% | 73% | 47% | 47% | 0% |
| 12 | 16 | 80% | 80% | 39% | 39% | 0% |
| 13 | 32 | 77% | 77% | 24% | 24% | 0.3% |

In a second run, BP's per-bit accuracy at 10 variables was 75%, against 70% for simply thresholding the priors, and BP's wrong outputs were never valid solutions.

Caveats: this is my reimplementation, validated only on a tree, and the author's check selection may differ. Redundant or differently chosen checks can change BP's behaviour a lot. Treat it as a strong prior, not a result.

If it holds, three things follow:

- **The headline answer is nearly foregone.** The post shows Astra doing well on the soft task at these sizes with filler. Textbook BP on the stated constraints gets about 20% of instances. So Astra is not running textbook loopy BP on the given factor graph, and this can be shown with a replication run plus an offline table.
- **Set D versus matched Set A does not work as designed.** "BP wrong" is the default case, not a rare stratum. Set A (BP right) will be the minority with strong priors, so "matched on MAP margin" will not remove the difficulty confound.
- **The interesting question moves** to which non-textbook algorithm fits: BP on a redundant check set, enumeration, or something else.

Two further consequences for the proposal's dissociations:

- **Enumeration is not expensive here.** BCH-2 at 9–13 variables has only 2–32 valid solutions. The post's "brute force is a lot more work" argument applies to BCH-1 (2,048 solutions at 15 variables), not to these instances.
- **Exact marginals and exact MAP never disagree under the 4x filter.** The "exact marginal inference vs enumeration" contrast cannot be made on answers in Sets D/A; it only exists in the low-ratio regime the author already examined.

## 1. Would it get upvoted?

Probably 30–60 karma; about 35–40% chance of clearing 50.

- For: the parent post got 103, it explicitly says the author is out of black-box ideas, and "Astra is right where BP is wrong" with one clean figure is a real correction to a well-read post.
- Against: the cluster's follow-ups since mid-October have landed at 10–50 (Westover 48, key-position confound 28, Schulz 10). The parent post drew only two comments. Its title already hedges with "BP-like" and the author already wrote that trajectories are "quite different from textbook BP", so "it is not textbook BP" is partly conceded.
- A post that clears 50 has to say something positive: for example "Astra's answers are best predicted by X, and here is where hidden inference therefore fails". A purely negative "not BP" result will read as a footnote.

## 2. Naturalness

Mainline. The screener suggested exactly this, the author invites it, and nobody has done it. Sets D/A are the natural next step. Sets T and E are side branches:

- Set T (trees, diameter 2–10) is a different task from the BCH one. Tree parity graphs have many solutions and BP solves them trivially, so this is closer to the "speculative depth" post and to proposal 01's serial-depth question.
- Set E varies solution count by deleting constraints, which simultaneously changes constraint count, prompt length and BP behaviour. "Fixed BP difficulty" is not achievable.

## 3. Pre-mortem

How it plays out: the team writes solvers on day 1, discovers the table above, and realises Set A is small and unrepresentative. They either push ahead with a confounded match or redesign on the fly. The replication gate probably passes for the answer-only task. Astra matches exact MAP on most "BP wrong" instances at sizes where it is competent, so the bar chart says "not BP". The confidence regression is noisy and the trajectory rank-correlation is uninterpretable.

| Outcome | Probability |
|---|---|
| Clear positive: Astra tracks BP's wrong answers | 5% |
| Clear negative, still interesting: Astra tracks exact MAP where textbook BP fails, with some positive characterisation of what does predict its errors | 45% |
| Ambiguous mush: "not textbook BP, cannot say what it is" | 35% |
| Fails to run or replicate | 15% |

Specific failure reasons:

1. **Unfalsifiable BP family.** "Matches any member of {flooding, damped, min-sum}" plus unspecified check sets lets a defender say "it is BP on a different graph". The post must state which graph: the stated checks, all dual codewords up to some weight, or a learned reparameterisation.
2. **Residual errors look BP-like for trivial reasons.** When Astra is wrong, its answer will tend to sit near the priors, and so does BP's (75% vs 70% bit accuracy). Per-variable agreement with BP must be compared against a priors-threshold baseline, or the "inherits BP's failures" reading will be spurious.
3. **Confidence-report replication is the fragile part.** The author notes that asking explicitly for marginals made results worse, and that unconverged confidences are "completely arbitrary". The regression is restricted to variables where predictors differ by more than 0.15, which is where reports are noisiest.
4. **Trajectories depend on caching.** The author says the method does not work without verified cache hits. OpenRouter routing to a cache-consistent provider is not guaranteed, and reasoning_tokens must be zero on every step. The rank-correlation of "settling order" between a chaotic oscillating trajectory and a BP run that settles in 1–6 iterations (my simulation's median to 90th percentile) has almost no signal.
5. **Thin sampling.** Two samples per item with no temperature control gives a coarse per-item accuracy; "smallest N at which Astra is correct" is not estimable per instance from 2 samples at 5 filler levels.
6. **Elicitation details.** Astra needs reasoning_effort=low plus a strict system prompt; some fraction of calls will reason and must be discarded, and the discard rate may correlate with difficulty.

## 4. Cost check

The estimate is roughly right in total but wrong in its parts.

- The caching saving is mostly illusory for the main grid. The shared prefix (question only, about 300–400 tokens) is likely below the cache minimum, the filler comes after it, and cache writes cost $12.50/M. Budget the main Astra grid uncached: about $144 input + $25–40 output (confidence outputs for 13 variables are nearer 80 tokens than 40).
- Using `openai/gpt-6-astra:batch` halves this to about $90, if batch supports the no-reasoning setup.
- GPT-6.1 Sol about $35; trajectories $10–20; drop GPT-5.6 Sol.

My estimate: **$230–280** as written without batch, **about $150** with batch or with the trimmed design below. Comfortably under $500 either way.

## 5. Recommended changes (in order)

1. **Make step 0 an offline, zero-cost study.** Reproduce the table above with a validated BP implementation on the reimplemented generator, across check-set choices (stated checks only; all dual words up to weight w). State up front which candidate algorithms make distinguishable predictions and on what fraction of instances. If textbook BP is wrong on most filtered instances, say so in the proposal and re-aim.
2. **Replace the three-way framing.** Candidate predictors of Astra's answer and errors: (a) BP on stated checks; (b) BP or min-sum on an enlarged redundant check set; (c) enumeration over valid solutions, with error rate scaling in solution count; (d) priors threshold plus local correction. Pre-register that a predictor "wins" only if it beats the priors-threshold baseline on Astra's *errors*, not just on overall agreement.
3. **Replace Set D/A matching with stratification.** Run one large random set (about 600 instances, sizes where Astra scores 50–90%) and regress Astra's per-instance success on: BP-correct (each variant), log solution count, MAP ratio, prior strength, check weights. This uses the natural variation instead of a confounded match.
4. **Get the enumeration contrast from BCH-1 vs BCH-2 at fixed variable count**, as the author already set up (2,048 vs 32 or fewer solutions). Drop Set E's constraint deletion.
5. **Drop Set T**, or hand it to proposal 01. It answers a different question.
6. **Demote confidences and trajectories** to an optional appendix, attempted only if the cache-hit check works through OpenRouter on day 1. Spend the saved budget on 4 samples per item at 3 filler levels (0, 300, 3000) instead of 2 samples at 5.
7. **Drop GPT-5.6 Sol.** Keep GPT-6.1 Sol as the cheap replication, and run the whole pipeline on it first to debug before spending on Astra.
8. **Fix section 1**: the author did run BP informally; the gap is the absence of any reported answer-level comparison.
9. **Write the headline in advance for each branch.** If the only available headline is "not textbook BP", do not fund ahead of proposal 01; the result needs a positive characterisation to clear 50 karma.
