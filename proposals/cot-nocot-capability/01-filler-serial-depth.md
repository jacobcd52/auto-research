# Can padding buy back the key-first advantage? Filler tokens, repeats and serial depth on key-last tasks in Astra
cluster: cot-nocot-capability | stage-1 cost: $310 | follows up: "A Key-Position Confound in no-cot-bench" (ehF4kej38fkhb5cT3); "Filler tokens don't allow sequential reasoning" (KFkKPbuYCWc9ygpRp); "Astra is much better at reasoning with filler tokens than previous models" (uvhuZHFtrgk8kNiZc); "Astra's no-CoT limits track speculative depth, not step count" (WFc3NkuPaYFrYuaZd)

## 1. What the prior work showed
- Long argued (no experiments) that in a bounded-depth transformer, filler tokens add parallel width only: no computation path exceeds L layers.
- Filler tokens with no chain of thought (CoT) nevertheless help GPT-6 Astra, believed to be a looped transformer, on serial-looking tasks: 4-hop facts go from ~10–20% to ~50% with up to 4,096 filler tokens (Xu et al.), 31% to 63% in Corry's replication.
- MBaert showed such tasks have shortcuts. Astra's 50% horizon on Boolean chains is 54 steps but 11 on an xor-only version. On in-order chains (bool-4 in SSA form, 10 trials per cell) filler did nothing; on shuffled ones it recovered some accuracy. He now thinks cross-token KV-cache recurrence is less likely for Astra, at least during input processing, and leaves it open only for output generation. He tried output-side dots and reports "not much difference"; Xu reports the same in a comment.
- agastyasridharan showed that when the start value ("key") comes first, serial work can be spread over prompt positions. Key-last variants cost GPT-6.1 Sol 16% of its depth (median of 12 tasks, range 9–45%). No filler conditions, and no Astra.
- In that post's comments Neel Nanda objects: "the key question is whether the model could just say a bunch of benign-looking things in the CoT to create extra time before needing to output anything high stakes. My guess is in most cases it can?", for example by restating the question. agastyasridharan replies that the evidence is mixed. Nobody ran it.
- Already done, so not proposed: filler on 6.1 Sol; no-CoT benchmarks on open looped models (Westover et al., who also found plain filler harms Dory); trained filler reasoning (Schulz; Kuhn).
- Not done: filler or repeats placed after the key on key-last, shortcut-resistant chains. Commenters on MBaert's post (Xu, hillz, AprilSR) ask for this. A title scan of LessWrong since September found no such post.

## 2. Question and why it matters
On chains where no work can start before the key arrives, how much of the key-first minus key-last depth gap do Astra and 6.1 Sol recover from tokens placed after the key: dots, a repeat of the steps, or the model restating the question itself?

- Nothing recovers the gap: late-arriving information faces a hard serial ceiling that benign padding cannot lift. This supports Long's claim, and supports treating key-last depth as the relevant number for "sabotage conditioned on a late tool result".
- Repeats or restating recover it, dots do not: Nanda is right that the distinction is easy to erase, but only with task content re-presented, which is visible to a monitor.
- Dots recover it, or push key-last past key-first: contentless tokens buy serial depth. This is the alarming case, and it grows more alarming if model-generated dots beat input dots.

Because the metric is a difference between key-first and key-last at the same padding, generic filler benefits (which Astra shows on most tasks) cancel out.

## 3. Stage 1 plan
Reused: no-CoT recipes (`reasoning_effort=low`, strict prompt, `reasoning_tokens == 0`) from Nanda's ELICITATION.md (github.com/neelnanda-io/nocot-bench) and Corry's harness (github.com/christinecorry/no-cot-harness); key-first/key-last tasks from github.com/agastyasridharan/nocot-bench; 4-hop items from github.com/redwoodresearch/astra-filler-tokens. GitHub was unreachable while drafting, so repo contents are unverified. Every synthetic generator is under 100 lines to rewrite from the posts; only the 4-hop sanity check depends on a repo, and it is dropped if unavailable.

Tasks (single short answer, graded by program):
- S1: bitwise chain. d steps mixing `+c`, `-c`, `xor c` on a 10-bit value. Every step is a bijection, so states never merge, and the mix is not tree-reducible.
- S2: one branching, large-state task from the key-position post, chosen for the largest reported gap and validated against its published 6.1 Sol numbers.
- Controls in S1's format: C-add (add/subtract only, tree-reducible) and C-shuf (S1 in SSA form with shuffled lines, where MBaert found filler helps; this shows filler "works" in this layout).
- Item gate: over sampled keys the answer must be near-uniform, and no item may be solvable from its last m < d steps.

Conditions, each run key-first and key-last:
- Input dots after the final line, N in {0, 64, 256, 1024, 4096}.
- Input repeat: the step list repeated after the key (1x and 3x).
- Output dots (Xu's method; N = 256, 1024), with compliance reported.
- Output restate: the model copies the question verbatim, then answers (Nanda's example).
- Controls C-add and C-shuf at N = 0 and 1024.

Models and sample sizes: Astra on S1 plus controls, 5 depths x 100 items per cell. 6.1 Sol on S1, S2 and controls, 7 depths x 100. GPT-6 Sol (non-looped sibling) on S1 at N in {0, 1024, 4096}. The same items are used across all conditions.

Steps:
1. Pilot (half a day): zero reasoning tokens on every response; depth-1 accuracy above 95% (otherwise shrink to 8 bits); item gate.
2. N=0 ladders, key-first and key-last, to place depths. Gate: if the gap on a family is under 0.75 steps, the headline becomes absolute key-last horizon change and the "fraction recovered" ratio is not reported.
3. Full grid.
4. Analysis: mixed-effects logistic model (item random effect; depth, key position, condition and their interaction). Headline: gap(N) = key-first horizon minus key-last horizon, with paired bootstrap CIs, and fraction of the N=0 gap recovered per condition.
5. Pre-registered reading: a key-last gain counts as depth only if it exceeds both the key-first gain and the C-add gain at the same N. "No recovery" means the gap shrinks by under 0.5 steps, upper CI included. Anything else is reported as unresolved.
6. Secondary: do wrong S1 answers match a truncated computation? One 4-hop check (100 items, N = 0 and 1024) to confirm the harness reproduces the known uplift.

## 4. Stage 1 cost estimate
OpenRouter prices, 2026-11-14, per 1M tokens: Astra $10 in / $50 out; 6.1 Sol and GPT-6 Sol $2 / $10.
- Astra input dots: 5,000 calls x ~1.35k tokens = 6.75M: $68. Repeats and controls: 3,000 calls, 2.1M: $21. Output dots and restate: 1,500 calls, ~0.77M output: $41. Answer tokens: $5. Astra total $135.
- 6.1 Sol: 14,000 input-dot calls, 18.9M: $38. Repeats and controls, 3.9M: $8. Output conditions, 2.2M output: $22. Total $68.
- GPT-6 Sol: 3,000 calls, 5.7M: $12. 4-hop check: $3.
- Subtotal $218; x1.4 for pilot, elicitation iteration and reruns: $305, rounded to $310. Half-price `:batch` endpoints are unused slack.

## 5. What success looks like
One figure per model: key-first and key-last horizons against N, with repeat and restate conditions as marked points, plus a bar chart of fraction of gap recovered.
- Clear negative: gap unchanged within 0.5 steps for dots up to 4,096, C-shuf rises (filler works in this format). Headline: "Astra cannot buy back the key-first advantage with padding." Sharper if repeats do recover it.
- Clear positive: dots recover over half the gap, or key-last horizon at N = 1024 is at least 1.5x its N = 0 value and above key-first.
- Ambiguous: gap under 0.75 steps on Astra, or recovery CIs spanning 0–50%.
The first Astra key-position gap is new in any case, and the negative answers a live disagreement between named researchers, so it is publishable. I expect it to land near the 50-karma bar, not well above.

## 6. Stage 2 (if stage 1 succeeds)
- If padding recovers depth: tokens per extra step, natural unrelated text versus dots, and whether a monitor notices (~$1,000 API).
- If not: a positive control on a recurrent open model. Westover et al. show untrained Dory gains nothing from filler, so this needs a LoRA- or RL-trained recurrent-Dory with `per_loop` versus `last_loop` KV modes (~$600 GPU).

## 7. Risks and how the plan handles them
- Small gap makes the ratio noisy. Step-2 gate; S2 chosen for a large gap; 100 items per depth, paired.
- Residual shortcuts. Bijective steps, 10-bit state, item gate, truncation analysis.
- Small gains everywhere. The gap metric subtracts key-first gains; the step-5 rule is fixed in advance.
- Output conditions fail compliance or consume capacity. Dots, not counting; compliance reported; these arms are secondary.
- Silent reasoning. Per-response reasoning-token check; half a day budgeted.
- Scooping (MBaert, Corry and Redwood are active). The core grid runs on day one.

## 8. Response to feedback
Accepted, after re-reading the posts and the key-position comment thread:
- Reframed around the key-first gap and the Nanda/agastyasridharan exchange (quote verified). Key-first now runs at every N, and the headline is the gap, which also handles "small gains everywhere".
- Section 1 corrected: MBaert now considers KV sharing less likely for Astra and reported an output-side null. Both confirmed in his post.
- S3 (swap chain) dropped; the reviewer is right that its state is trackable from the first token. Old S2 replaced by a task from the key-position post. S1 widened to 10 bits with an injectivity gate.
- P and H removed as the main contrast in favour of same-format controls (add-only, shuffled SSA). H is kept as a 200-call sanity check.
- Added the repeat-after-key condition, plus an output "restate the question" condition, which is Nanda's own example.
- Output side uses dots, not counting. Astra sample size raised to 100 items per depth, paired items, mixed model, equivalence bound stated in advance.
- Dory arm moved to stage 2: Westover's appendix confirms plain filler harms untrained Dory, so a null there would mean nothing. Argon and Fable 5.1 cut to pay for sample size.

Partly rejected:
- "101 states is small" for the old S2: the key-position post itself calls its 0–100 chain "too large to enumerate". The convergence objection (many-to-one steps) is correct and is the reason I replaced the task.
- "Fraction of gap recovered" as the sole headline: the 6.1 Sol gap is about one step and Astra's is unmeasured, so a ratio could be mostly noise. I report the gap in steps, and the ratio only if the step-2 gate passes.
- I kept one non-looped sibling (GPT-6 Sol), which the reviewer did not ask for, because without it a null cannot be tied to looped models.
