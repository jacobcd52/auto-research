# Feedback: Where activation oracles lose to probes: lost at injection or lost at readout?

Reviewer verdict: **major overhaul**. The idea is cheap and runnable, but the premise (a probe-vs-AO gap on a
standard AO) is much weaker than the proposal states, one of the three diagnostic outcomes is trivially excluded
by construction, and the nearest comparable posts earned 17-39 karma.

Search caveat: the WebSearch tool was unavailable to me (shared budget exhausted). The prior-work check used the
arXiv API (four keyword queries), a title scan of every LessWrong post from 2026-07-28 to 2026-11-14, the Hugging
Face API, and full reads of the cited posts. GitHub repos were not opened. "Not found" below means not found by
those routes.

## What I verified

| Claim | Status |
|---|---|
| Three oracle checkpoints are public | Confirmed on HF. `ao_config.json` for v3: reads layers 21-25, `hook_onto_layer: 1`, `steering_coefficient: 1.0`, LoRA rank 128. |
| `ceselder/cot-oracle-eval-sycophancy-v2`, `-hinted-mcq` are public | Confirmed, but **each has 100 rows**. The plan needs 2,000 per task. |
| Arya's post: AO says "10"/"12" for every problem; ranking not checked | Confirmed. |
| Arya's post: AO AUC 0.55-0.60 vs 0.77 dense probe | Numbers confirmed, but the proposal drops the caveats: the set was **10 hinted + 10 unhinted prompts** and the probe was **scored on its own training data**; the authors say 0.77 "is likely an overestimate". |
| Cycle-consistent post: 0% exact match on 2-digit answers, probe 100% on first digit | Confirmed, with n=50 per tier, layer 18, and the decoder is the cycle-trained description writer, not a standard AO. |
| Building Better: narrow training matched probes, never exceeded; 79% -> 85% hallucination at 2x strength | Confirmed. |
| "3 Tips": 0.50 accuracy but 0.83 AUC | Confirmed (also in the Building Better appendix). The same post says: "I frequently find that an activation oracle will obtain a similar AUC to a trained linear probe". |
| arXiv 2607.23379 shows the concept stays decodable inside the oracle | The abstract says so, but the arXiv record (v2, 2026-11-05) carries the comment **"A mistake was found in experimental results, so the results as presented in the current version of the paper are incorrect."** The proposal cites it as support without noting this. |
| arXiv 2605.26045: candidate scoring beats free generation on Taboo | Confirmed from the abstract. |
| RunPod A100 80 GB $2.09/h; claude-haiku-latest $0.10/$0.50 | Both confirmed today (A100 PCIe secure cloud $2.09/h, community $1.19/h). |

## 1. Would it get upvoted?

Probably not past 50. The relevant comparison is not the cluster's original posts (55-155 karma) but the
follow-ups of the same type that have appeared since:

- "3 Tips to Improve Activation Oracle Results" (Karvonen, the method's author): 39.
- "Activation Oracles significantly underperform without a safe base model": 22.
- "When Activation Oracles learn not to read" (probes and logit lens inside the oracle, the closest methodological match): 17.
- "Three Pieces of Evidence that the NLA Reconstructor Does Not Read Semantics or Syntax": 20.
- "Deletion Gap of Reconstruction in NLAs is in the Final Explanation Sentence": 3.

Attention has also moved from AOs to NLAs, and CHIVE's "no uplift over reading the transcript" result lowered
interest in squeezing more out of AOs. A diagnosis of where a Qwen3-8B AO drops an arithmetic digit would interest
the handful of people training AOs (Karvonen, ceselder, Bauer, Chalnev). I estimate 15-35 karma for a clean result.

The one version that could exceed 50 is a strong actionable headline: "released AOs match probes on tasks where
they were reported to fail, if you score candidates; here is the recipe and the evidence it is reading
activations". But that is mostly the "3 Tips" message with one extra task, and the proposal itself calls it the
weakest outcome.

## 2. Naturalness

It is a reasonable question and Arya's post explicitly leaves the ranking caveat open, so step 2 (candidate
scoring on number prediction) is a mainline loose end. The inside-the-oracle probing is a side branch: none of
the five posts' authors list it as future work, and their stated directions are better training data, more
layers, and verifiable training environments.

Already done, in part:
- Candidate scoring / AUC closing the gap on binary tasks: Building Better appendix and "3 Tips".
- AObench already contains number-prediction and MMLU-prediction tasks scored for exactly these checkpoints
  (`ceselder/cot-oracle-ao-benchmark` has per-task eval results). The proposal does not cite these numbers. They
  may already show whether v3 fails at T1 and T2.
- Probing and logit lens inside an AO: 2607.23379 (on a Taboo-fine-tuned oracle; results now flagged incorrect).

I found no work doing layer-by-site probing inside a standard released AO on an unmodified target, so the
narrow novelty claim stands as far as my search goes.

## 3. Pre-mortem

**The premise is not established for any of the three tasks on a standard AO.**
- T1: the two "AO fails" observations are a Qwen3-32B AO on long nested expressions (answers like -8369, no probe
  run, and it is unclear the target computes them without CoT) and a cycle-trained decoder at n=50. Nobody has
  shown a standard Qwen3-8B AO losing to a probe on "a × b =" under candidate scoring.
- T3: the cited gap is n=20 with an in-sample probe, and the AO authors later report 0.83 AUC on a similar task.
- T2: Arya reports AUC 0.55 for A/B prediction on 32B; no probe number exists.

So steps 1-2 are the real experiment, and a likely result is that with 20 positions and logit-difference
scoring the gap on T2 and T3 is small. Then steps 3-6 have nothing to localise on two of three tasks, and the
"holds across at least two tasks" success bar cannot be met.

**Outcome (a), "lost at injection", cannot occur as defined.** Injection is additive and norm-matched at layer 1
onto a constant placeholder token: h' = h + c·‖h‖·v/‖v‖. A linear probe on h' immediately after injection
recovers the direction of v almost exactly, so decodability there equals the skyline by construction, at every
strength. Step 5's "re-measure just after injection" is therefore uninformative. The three-way classification
collapses to two-way, and the proposal's "injection failure" headline is unreachable with this measurement.

**Linear decodability at the answer position is a weak criterion for (c).** Any attention path that copies a
small component from the placeholders makes the label linearly decodable at d=4096, whether or not the oracle
uses it. "Decodable but not said" then gets reported as "readout failure overridden by a prior" with no causal
evidence. The shuffled floor controls for the oracle computing the answer from text; it does not control for this.
Without a causal test (patch the answer-position residual between examples and see whether candidate scores
move; or logit-lens the true digit by layer), outcomes (b) and (c) are not cleanly separable.

**T3 label is confounded.** "Flipped by the hint or not" is nearly identical to "hint present in the prompt",
which is plain text inversion and trivially probe-readable. The contrast has to be hinted-and-flipped versus
hinted-and-not-flipped, which shrinks the data. Getting 2,000 such items from Qwen3-8B on Scruples needs a new
rollout-and-filter pipeline (the public sets have 100 rows; Arya found about 200 reliable flips on 32B).

**T1 is partly solvable without reading the answer.** The control-token activations also encode the operands, and
an 8B oracle can multiply two small numbers. The wrong-answer split handles this, but for easy tiers that split
will be tiny, and for hard tiers the skyline probe will be weak. The usable band may be narrow.

**Repair step (step 6) repeats a known result.** Building Better already reports that narrow training matches
probes and does not transfer. The most likely finding is the same.

**Storage.** v3 uses 5 layers × 20 positions = 100 placeholder positions. Caching all 36 layers at all
placeholders is about 30 MB per example in fp16, so about 60 GB per oracle-task-condition and well over 1 TB for
the full grid. The 200 GB budget only works with mean-pooling over placeholders or a layer subset; this needs
deciding up front.

**Forecast.**
- Clear positive (clean localisation on at least two tasks, with a usable recommendation): 15%.
- Clear negative that is still interesting (candidate scoring closes the gap everywhere; AOs were mis-scored): 25%.
  This is useful but largely confirms "3 Tips".
- Ambiguous mush (gap on arithmetic only; partial decodability at the answer position at intermediate levels;
  task-dependent picture; repair does not transfer): 50%.
- Fails to run: 10%. Loaders differ across the original and v3 checkpoints (single layer vs five-layer prefix
  template), but the work is otherwise within reach in two days.

## 4. Cost check

Prices are correct. GPU-hours are plausible for inference and small LoRA continuations on an 8B model. Add the
T3 rebuild (rollouts with and without hints over several thousand Scruples items, perhaps 4-6 GPU-hours) and more
disk or an extra pass for pooled caching. My estimate: **$200-260**, comfortably under $500. Community-cloud A100
at $1.19/h would bring it back near $150. Cost is not the problem with this proposal.

## 5. Recommended changes

1. **Establish the gap before building around it.** Open the AObench per-task results for the three checkpoints
   and report the existing number-prediction and MMLU-prediction scores in section 1. Make stage 1's first gate
   explicit: probe skyline versus candidate-scored AO at 1 and 20 positions on all three tasks; continue only on
   tasks with a gap above a stated threshold (say 15 points of accuracy or 0.10 AUC). State what the write-up is
   if no task passes.
2. **Fix section 1.** Add the n=20 and in-sample caveats to the 0.77 probe figure; say that the Cycle-Consistent
   decoder is not a standard AO and that n=50; note the "results are incorrect" flag on 2607.23379 and stop
   leaning on it; attribute the 0.83 AUC figure to Building Better as well.
3. **Drop outcome (a) as defined and replace the injection measurement.** Additive injection keeps the vector
   linearly present. If injection is to be tested, measure something that can fail: decodability at placeholders
   several layers after injection, or attention mass from the answer position to the placeholders as a function
   of strength.
4. **Add a causal test to separate transport from readout.** Activation patching of answer-position residuals
   between examples with different labels, measuring the shift in candidate log-probabilities, plus logit lens
   on the true answer token by layer. This is cheap and turns a correlational claim into a defensible one.
5. **Cut scope to make two days safe.** Use T1 and T2 only (labels are free and unconfounded); drop T3 or reduce
   it to a hinted-flipped versus hinted-unflipped contrast at whatever n the filter yields. Use two oracles
   (original recipe and v3 at 2x), not three. Drop step 6, or keep a single 1,000-example run as an appendix.
6. **Specify the cache.** Mean-pool placeholders per source layer, or probe online without storing, and say which.
7. **Reframe the deliverable around the actionable result.** The post with the best karma odds is "do released
   AOs match probes when scored properly on tasks where they were reported to fail, and when they do not, is the
   answer present at the answer position". Lead with the behavioural table and the activation-shuffled control;
   treat the layer-wise curves as supporting evidence.
8. **Relative priority.** Even after these changes I expect 15-35 karma. If the funder must choose within this
   cluster, proposal 01 (offset versus organism) addresses a claim that Arya's post and CHIVE both assert without
   measuring and has a clearer both-ways headline; I would fund that first and this one only if money remains.
