# What do question repeats buy a looped model? A behavioural dissection of Dory 4B in bounded-depth and recurrent-KV modes
cluster: cot-nocot-capability | stage-1 cost: $100 | follows up: "Looping a transformer increases no-CoT capabilities more than general capabilities" (uxsDuWWHNTpKrsF6P); "Recent LLMs can use filler tokens or problem repeats to improve (no-CoT) math performance" (NYzYJ2WoB74E6uj9L); "Filler tokens don't allow sequential reasoning" (KFkKPbuYCWc9ygpRp); "Recurrent KV-cache sharing may undermine the bounded-depth argument" (LaR7joZu4QyaM7hqq); "A Key-Position Confound in no-cot-bench" (ehF4kej38fkhb5cT3)

## 1. What the prior work showed
- Repeating the problem or appending filler raises no-CoT accuracy in many recent models, looped or not (Greenblatt: Opus 4.5 45% to 51% on easy maths; NCRI's `scores_all.csv` lists significant repeat or filler gains for 26 of 34 models measured). For GPT-6 Astra, rumoured to be looped, the gain is much larger (4-hop facts 31% to 63%).
- Long argued that in a bounded-depth transformer extra positions add parallel width, never serial depth. MBaert pointed out that this fails if a looped model shares its last-loop KV cache across loops, because later tokens' early loops then read earlier tokens' final-loop states.
- Westover et al. (2026-11-12) ran NCRI on NVIDIA's open-weight looped Dory 1.0 4B (8 input layers, a 20-layer block applied 1–8 times, 8 output layers). Appendix A, shown as a figure on aggregate NCRI with no per-task numbers: dot filler hurts at every loop count; repeating the question 5 times helps at 2+ loops, hurts slightly at 1 loop, and helps more with more loops. In recurrent-KV mode ("recurrent-Dory", config `recurrent_kv_cache_mode: last_loop`), which Dory was never trained in, NCRI with 5 repeats at 2 loops is 60 against 49 in normal mode.
- Not done: any test of why repeats help Dory. Only one repeat count (5), one aggregate score, no partial or corrupted repeats, no comparison with a non-looped model of similar size (NCRI's filler table covers API models only), and no measurement of whether repeats extend serial depth in recurrent mode. White-box work on other looped models exists (arXiv 2609.39892, 2610.18127, 2507.02199) but none studies repeats or Dory.

## 2. Question and why it matters
What does a repeated question give Dory, in each KV mode? Four candidate answers with different behavioural predictions:
- H-mask (causal-mask re-reading): in copy 1, early tokens (the rule table) cannot see later ones (the query); in copy 2 everything sees the whole problem. Predicts that putting the query first in a single copy recovers most of the uplift and that repeating only part of the problem suffices.
- H-ensemble (redundant parallel reads): later positions pool noisy reads of several copies. Predicts smooth growth with repeat count, little order sensitivity, and blended answers when one copy is corrupted.
- H-weak: the 1-loop configuration is simply too weak or off-distribution to use any prompt aid; nothing is specific to looping. Predicts that the loop-by-repeat interaction vanishes when baseline accuracy is matched, and that non-looped 4B models show the same absence of uplift.
- H-serial (recurrent mode only): repeats give real extra serial depth through the cross-token path. Predicts that the depth at which accuracy crosses 50% grows with repeat count in `last_loop` mode but saturates in `per_loop` mode, where unrolled Dory is an ordinary tied-weight transformer and Long's bound applies.

H-serial is the part with stakes: it is the first direct test of whether an off-the-shelf looped model, switched to recurrent KV sharing with no training, turns input tokens into opaque serial depth. The per-loop arms settle whether the "looped-only" repeat effect is about looping or an artefact. Whether routed information is raw operands or computed intermediates cannot be decided behaviourally and is left to stage 2.

## 3. Stage 1 plan
Everything runs black-box through the vLLM build documented in the Dory model card (`pip install` from vllm-project/vllm PR #60149; loop count and KV mode set with `--hf-overrides`). The Hugging Face repo ships no modelling code and `transformers` has no Dory class, so no hooks are assumed.

Reused: Dory weights (huggingface.co/nvidia/NVIDIA-Nemotron-Labs-Dory1.0-4B-BF16); NCRI generators and `qrep`/`dots` filler code (github.com/neelnanda-io/nocot-bench: Brew rule-table chains, nested Arithmetic, the add-and-wrap step chain); key-first and key-last variants (github.com/agastyasridharan/nocot-bench). Comparison models: Qwen/Qwen3.5-4B and google/gemma-4-E4B-it (non-looped, same size class), GPT-6.1 Sol via OpenRouter. Built: prompt-edit conditions and the analysis.

0. Sanity (4 h box). Serve Dory at loops {1, 2, 4, 8} in both modes. Checks: (a) at 1 loop the two KV modes give identical outputs; (b) in `last_loop` mode, answers are the same whether the prompt is sent whole or built up through prefix caching, i.e. prompt positions really get the cross-token path (if not, recurrent-mode arms use the path that does and say so); (c) NCRI with 5 repeats at 2 loops is higher in recurrent than normal mode, as in Westover; (d) token counts per condition against the 1024-token sliding window (15 of 20 recurrent attention layers are windowed), so every condition is labelled as inside or outside the window.
1. Replicate and select. Three tasks x depths 2–8 x loops {1, 2, 4, 8} x both modes x {plain, 2 repeats, 5 repeats, dots}, 200 items per cell (selection set). Pick, per task, the depth band with 35–65% plain accuracy for each loop count. Confirm on a fresh 600-item paired set with a pre-registered test: loop-by-repeat interaction on the logit scale (mixed-effects logistic regression, item random effect), threshold 6 points of uplift difference between 1 and 2+ loops.
2. H-weak. Compare uplift at accuracy-matched depths (1-loop at an easier depth against 2- and 4-loop at harder depths, all near 50% plain). Run the same tasks and repeat conditions on the two non-looped 4B models.
3. Dissection (per-loop mode; 2 tasks, matched depth bands, loops {1, 2, 4}, 600 paired items per condition): query-first against query-last single copy; repeat only the table, only the query, only the instruction; a copy of a different problem of the same type; a paraphrased copy; dots padded to the same token length; copies pushed beyond the 1024-token window with neutral padding (does the uplift survive on the 5 full-attention layers alone?); corrupt-one-copy (change one rule or the start value in the first or the last of 3 copies, and classify the answer as following the clean copies, the corrupted copy, or neither). Corrupt-one-copy and query order are also run on GPT-6.1 Sol (2 tasks, 400 items).
4. H-serial. Both modes, loops {2, 4}, repeats {1, 2, 3, 5, 10} and dots {64, 512}, depths 2–12 on two tasks, 300 items per cell. Fit the 50%-accuracy depth per condition with bootstrap CIs. Add a split-chain arm: copy 1 contains only the first half of the steps, so a gain there needs a relayed intermediate.

Outputs: horizon-against-repeats curves for the two modes; a condition-by-loop table of uplift recovered; the corrupt-one-copy answer breakdown.

## 4. Stage 1 cost estimate
- GPU: one 48 GB card (Lambda A6000, $1.09/h listed 2026-11-14). About 350M prompt tokens over all arms; throughput is measured in step 0, and I budget 45 h including the 8-loop runs, the two comparison models and debugging: $49.
- GPT-6.1 Sol ($2/$10 per M tokens): about 6,400 prompts x 2,000 tokens = 13M input tokens: $26, plus $2 output.
- Margin for reruns or a second card if 8-loop throughput is poor: $23.
Total: $100.

## 5. What success looks like
- Clear positive on H-serial: in recurrent mode the 50% depth rises with repeat count (for example from 3 steps to 5+ at 10 repeats, CIs separated) while the per-loop curve is flat beyond 2 repeats, and the split-chain arm helps only in recurrent mode. Post: "Switching a looped model to recurrent KV sharing lets prompt repeats buy serial depth, with no training".
- Clear negative: horizons in the two modes move together. Then the 60-vs-49 NCRI gap is not a depth effect, which bounds the worry in MBaert's post for untrained recurrence.
- Per-loop mode: one hypothesis accounts for at least 70% of the uplift (for example query-first recovers it: H-mask), or the interaction disappears under accuracy matching and the non-looped 4B models behave like 1-loop Dory (H-weak, a correction to Appendix A).
- Ambiguous: the interaction replicates but each manipulation recovers 20–40%. Reportable as a short note with the horizon result as the lead.
- Honest expectation: follow-ups in this area now get 10–50 karma; this clears 50 only if H-serial gives a clean curve in either direction.

## 6. Stage 2 (if stage 1 succeeds)
- White-box extension (~$250): port the PyTorch model class from the vLLM PR into a hookable forward pass, verified logit-for-logit against vLLM; then per-loop, per-token-class attention knock-outs over all attention layers and patching between pairs with identical operands whose step-k intermediate differs because a mid-chain rule differs, to separate operand routing from computed-intermediate routing.
- The same horizon test on Westover's filler-trained recurrent-Dory checkpoints if released, and on Ouro-2.6B and Huginn (~$200).

## 7. Risks and how the plan handles them
- The uplift is small on single clean tasks (Appendix A is aggregate and figure-only). Selection and confirmation are on separate item sets with one pre-stated test; if the interaction fails to confirm, that non-replication plus steps 2 and 4 is still the report.
- `last_loop` semantics for prompt tokens may differ between whole-prompt and incremental processing. Check 0(b) detects this before any recurrent-mode claim.
- Under-elicitation. Use NCRI's few-shot recipe and report format-failure rates per condition.
- Floor and ceiling effects masquerading as interactions. All comparisons are in the 35–65% band and on the logit scale.
- The vLLM PR may not build. Fallback: the llama.cpp fork pinned in the model card.
- Overlap with proposal 01's optional recurrent-Dory arm: if both are funded, that arm lives here and 01 reuses the curves.
- Low reader interest in the per-loop dissection. The post leads with the recurrent-mode horizon result.

## 8. Response to feedback
Verdict accepted: overhauled. I re-checked the disputed facts and the reviewer is right on each.
- No hookable implementation: confirmed. The Hugging Face repo has no modelling code, `transformers` main has no `models/dory`, and the model card documents only the vLLM PR and a llama.cpp fork. The white-box plan (knock-outs, probes, patching) is removed from stage 1 and becomes a conditional stage-2 item with the logit-equivalence check and the reviewer's corrected patching design.
- Sliding window: confirmed at 1024 tokens in `config.json`, so my claim that windowed layers cannot see earlier copies was wrong. It is deleted; prompt length against the window is now reported and used as a manipulation.
- Hypotheses: the reviewer's depth argument is correct. In per-loop mode nothing is relayed serially, so "H-refine" is dropped there. Serial relay is now tested only where it is possible (`last_loop` mode), which moves from fallback to a main arm. H-mask and H-weak are added with the accuracy-matching and non-looped 4B controls.
- "Only a looped transformer" in the title overstated the prior; title and section 1 are corrected.
- Gate: replaced "8 points in some cell" with selection and confirmation on separate sets and one pre-stated interaction test.
- Related work: the three arXiv papers are cited and differentiated.
- Cost falls from $150 to $100.

Where I differ:
- The reviewer's three hypotheses include computed-intermediate routing tested by non-operand patching. That needs hooks, so I do not claim stage 1 can separate it from operand routing; it is deferred, not answered.
- The reviewer suggests the Sol comparison "gives the post a reason to be read". I include it but do not lean on it: Sol's architecture is unconfirmed, so it is a descriptive comparison only. The recurrent-mode horizon test is the lead result instead.
- One addition the reviewer did not raise: whether `last_loop` mode gives prompt positions the cross-token path depends on how the server processes the prompt, so step 0(b) checks it.
- I agree this remains the weakest of the cluster's four proposals on expected attention, and fundable only in this cheaper behavioural form.
