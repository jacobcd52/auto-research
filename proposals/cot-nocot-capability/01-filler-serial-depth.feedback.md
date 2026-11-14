# Feedback: 01 — Do filler tokens buy Astra serial depth?

Verdict: **keep, with tweaks.** The question is real and cheap to answer, but the likeliest result (flat) is already half-reported, one of the three "serial" task families does not meet the proposal's own criterion, and the parallel/serial contrast as designed will not support the headline. All of this is fixable inside the budget.

## What I checked

| Claim in the proposal | Status |
|---|---|
| Long's post is a conceptual argument with no experiments (77 karma) | Confirmed from the post. |
| Xu et al.: Astra 4-hop ~10–20% to ~50% with up to 4,096 filler tokens; AIME ~60–70% to ~90% | Confirmed from the post. |
| MBaert: bool-26 horizon 54 steps, 11 on xor-only; filler does nothing in order, recovers some when shuffled | Confirmed. Note his filler test was on bool-4 in SSA form, a task with known shortcuts, at 10 trials per cell. |
| MBaert "raised the possibility of KV-cache sharing" | Misleading. In this post he says the KV-sharing hypothesis is now *less* likely for Astra, at least during prefill; he leaves it open only for output generation. |
| Output-side filler on Astra was done by Xu (comment) | Confirmed, but incomplete. MBaert also tried output-side filler on his own serial tasks and reports "it didn't seem to make much of a difference". That is the closest prior result to this proposal's output arm and it is not cited. |
| Key-last costs 6.1 Sol ~16% of depth; no filler conditions | Confirmed (median over 12 tasks, range 9–45%). No filler anywhere in the post. |
| Commenters on MBaert's post ask for this | Confirmed (Xu, hillz, AprilSR). hillz explicitly asks how shortcut-resistant chains "interplay with filler tokens". |
| OpenRouter prices | Confirmed today: Astra $10/$50, 6.1 Sol $2/$10, 6 Sol $2/$10, Argon $2/$10, Fable 5.1 $10/$50. `:batch` variants exist at half price for all of them. |
| Dory 4B is public with `per_loop` / `last_loop` KV modes | Confirmed: model is ungated on Hugging Face and the model card documents both modes. |
| GitHub repos exist and contain the generators | **Not verified.** github.com returns 403 from this sandbox, as it did for the proposer. Nobody in this pipeline has seen the repo contents. |

Prior-work search: I scanned LessWrong post titles from 2026-09-08 to today and read the comment threads on the MBaert, Xu and key-position posts. I found no post that runs filler conditions on key-last or shortcut-resistant serial tasks. The experiment has not been done as specified.

## 1. Would it get upvoted?

It depends heavily on which outcome occurs.

- **Depth grows with tokens:** 150+ karma. It would be the first behavioural evidence of a cross-token opaque serial path in a deployed frontier model. I put this at under 10%.
- **Flat:** roughly 30–60 karma, so about a coin flip against the 50 bar. It confirms what Long argued, what MBaert's in-order result suggests and what most readers already believe. The recent base rate is poor: Westover et al. is at 48 after two days, the key-position post got 28, Schulz 10. September's 100–236 scores were release-week attention.
- **Small saturating gains:** 20–40 karma unless the write-up has a sharp frame.

The flat result needs a better frame than "Long was right". The best one available is in the key-position post's comments, which the proposal does not cite. Neel Nanda's objection to key-last there is: "the key question is whether the model could just say a bunch of benign-looking things in the CoT to create extra time before needing to output anything high stakes. My guess is in most cases it can?" agastyasridharan answers that the evidence is mixed. Nobody ran it. This proposal's key-last plus post-key filler conditions answer that exact disagreement. "Can Astra buy back the key-first advantage with padding after the key? No / yes, X% of the gap" is a headline that readers of both posts would care about under either outcome.

Who cares: the Redwood filler authors, MBaert, Nanda, agastyasridharan, and people working on CoT-monitorability safety cases for looped models.

## 2. Naturalness

Mainline. Three commenters asked for it, Greenblatt's original filler post leaves "is the gain only parallel?" open, and the Nanda/agastyasridharan exchange poses the key-last version directly. Not contrived.

The risk is being scooped: MBaert said he intends error-structure analysis, Corry promised "more comprehensive replications", and the Redwood group is actively publishing here. Nothing has appeared yet.

## 3. Pre-mortem

Forecast:

| Outcome | Probability |
|---|---|
| Clear positive (serial horizon grows substantially with filler) | 7% |
| Clear negative with working positive controls | 40% |
| Ambiguous (small, task-dependent gains; controls that do not isolate the cause) | 43% |
| Fails to run usefully | 10% |

Specific ways this goes wrong, in order of likelihood:

1. **S3 is not key-last.** In the swap chain the state is the whole arrangement of 8 slots, which is available from the first token. The model can track it while reading; naming the query slot at the end only selects a readout. That is exactly the "spread work over prompt positions" route the proposal says it removes. Putting the initial arrangement last does not fix it either, because swaps compose into a permutation the model can track forward. S3 as specified is a key-first task.

2. **S2 is exposed to the convergence shortcut MBaert documented.** "If even halve, else add 7" on 0–100 is many-to-one, so different keys collapse to the same state and the last few steps suffice. The pilot's "not solvable from the last m < d steps" check catches the extreme case only. agastyasridharan also warns that small key spaces allow precomputing over all keys; 101 states is small. S1 (8-bit, all steps bijective) is the only family that is clean on paper, and it has 256 states.

3. **The parallel/serial contrast does not license the headline.** S tasks are synthetic key-last chains; P and H are fact-retrieval tasks in a different format. If filler helps H and not S, "width, not depth" is one explanation; "filler helps recall of natural facts", "key-last layouts are off-distribution for filler use" and "Astra only uses filler on familiar task shapes" are others. A reviewer on LessWrong will say this within the first three comments.

4. **Small gains everywhere.** Filler improves Astra modestly on most things (HLE, LiveBench categories, hash tasks). A 10–20% horizon gain on S1 is quite likely, and the plan cannot tell "redundancy/error correction" from "extra width helps parse the layout" from "a little real depth". The three-model comparison (flat / saturating / linear) with five N values and horizons of 4–8 steps will not discriminate saturating from flat-plus-noise.

5. **Resolution on Astra.** With horizons around 5 steps, a 10% change is half a step. 5 depths x 30 items gives a horizon standard error of roughly 0.4–0.5 steps per cell. The "flat within 10%" claim is not supportable for Astra at that n; it is fine for 6.1 Sol at 7 x 50.

6. **Output-side counting is a confound, not a control.** Counting 1 to N is itself a serial task that competes for capacity, and the prior from MBaert and Xu is "no difference". Xu reports >99% compliance with dots, so dots are feasible.

7. **The Dory arm will be uninformative.** Westover et al. found plain filler harms Dory's NCRI at every loop count, and that recurrent-Dory only used filler for serial work after RL training. An untrained 4B model will likely have a key-last S1 horizon of 1–2 steps and no filler uplift in either KV mode. A null here says nothing about whether the test detects recurrence, so it cannot serve as the positive control.

8. **Repo dependence for H.** The S generators are trivially rewritable. The 4-hop natural-facts set is not: Greenblatt's datasets were removed and need regenerating. The proposal does not list the Redwood repo (github.com/redwoodresearch/astra-filler-tokens) where the Astra 4-hop items live.

9. **Elicitation.** Astra and 6.1 Sol need `reasoning_effort=low` plus a strict prompt and a `reasoning_tokens == 0` check; the key-position authors say this "took some iteration". Budget half a day, as planned. Low risk given published recipes.

## 4. Cost check

The arithmetic holds at the prices I confirmed. My estimate for the plan as written is $150–250 of API spend, less with `:batch`. The $40 Dory arm is poor value.

The budget is not the constraint; statistical resolution on Astra is. Tripling Astra's S1 items costs about $60 more. With the changes below, I estimate **$300–350**, the same total as proposed.

## 5. Recommended changes

1. **Reframe around the key-first gap.** Headline metric: the fraction of the key-first minus key-last horizon gap that post-key padding recovers, per model. Cite the Nanda/agastyasridharan exchange as the motivation. Run key-first at every N, not only N=0 and N=1024.

2. **Replace P and H as the main contrast with within-family controls** that share S1's format:
   - an add/subtract-only chain of the same length (tree-reducible);
   - a shuffled-order SSA version of S1 (MBaert found filler helps here, so this is the positive control that filler "works" in this format);
   - key-first S1.
   Keep H as a small sanity check that the harness reproduces the known 4-hop uplift, using the Redwood or Corry items.

3. **Fix the task families.** Drop S3 or relabel it as a key-first comparison. For S1 and S2, gate items on the key-to-answer map: sample all keys, require the answer to be near-injective in the key (high entropy), in addition to the truncation check. Widen the state to 10–12 bits if depth-1 accuracy stays above 95%. Consider replacing S2 with one of the branching, large-state key-last tasks from the key-position fork, which already has 6.1 Sol baselines to validate against.

4. **Add a "repeat the steps after the key" condition.** Input-side, `[steps][key][steps again]`. Repeats beat filler on weaker models and on Dory, and this is the trivial benign-looking way to turn key-last into key-first. If filler is flat and repeats recover the gap, that is a clean and interesting pair.

5. **Put the sample size where the claim is.** Concentrate Astra on S1 plus its controls with at least 5 depths x 100 items per cell; use the same items across N and analyse paired differences with a mixed model, not independent per-cell logistic fits. Pre-state the equivalence bound (for example, horizon change under 0.5 steps).

6. **Output side: dots, not counting,** following Xu's method, with counting only as a secondary check. State the prior nulls from MBaert and Xu.

7. **Cut the Dory arm from stage 1** and move it to stage 2, where it needs a trained recurrent model to mean anything. Spend the $40 on item 5.

8. **Correct section 1:** MBaert's current view of KV sharing, and his output-side null.

9. **Decide in advance what a 10–30% gain means.** Either add a discriminating condition (does the gain appear equally on the add-only control and key-first? then it is not depth) or commit to reporting it as unresolved.
