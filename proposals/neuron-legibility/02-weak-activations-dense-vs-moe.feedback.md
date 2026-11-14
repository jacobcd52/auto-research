# Feedback: "Do weak neuron activations matter?" (02-weak-activations-dense-vs-moe)

Verdict: keep, with tweaks. The core measurement is sound, cheap and not yet done as far as I can tell. The scope is too wide, one relevant body of prior work is missing, and the dense-versus-MoE comparison as written has a confound the plan does not handle.

## What I checked

| Claim in the proposal | Status |
|---|---|
| Goodfire numbers (top-320 of 4,096 routed, 92.2% ablated, loss 1.886 to 1.940, KL 0.140, 8.4M web tokens; P25-P75 +0.010) | Correct, read from Table 1 of the report's `article.md`. The same table gives P25-P75 KL 0.033, P10-P90 KL 0.088, P5-P95 KL 0.162, top-64/expert 0.152, top-32/expert 0.263, random-64 2.511. |
| "we leave investigation of them to future work"; MoE only; shared expert left intact; reasoning evals loop without fine-tuning | Correct. |
| Leo Gao quotes (weak-activation guess, "worth tracking down the source of the divergence", KL over loss) | Correct, in the post body and footnotes 4-5. He gives no model, ablation rule or number. |
| neverix: L0 about 32, KL about 0.5, "MoE MLPs are only usable at a lower sparsity" | Correct (post p6kaX6LqfTHFqC6r6). |
| All eleven models ungated, apache-2.0 | Correct (Hugging Face API). |
| RunPod $2.69/h RTX Pro 6000, $1.09/h L40S | Correct (secure cloud; community cloud is $1.69 and $0.79). |
| bonsai-interp loader for exact 1-bit weights | README confirms it. I did not test the loader. |
| No dense replication exists | Not found by me either, with limits (below). |

Limits of my prior-work search: WebSearch was unavailable to me too (shared budget exhausted). I checked LessWrong posts from 28 Oct to 14 Nov by title, comments on the four relevant posts, and arXiv keyword queries. I could not check Twitter/X. neverix's post links a tweet (kaleybrauer, status 2112610230131662925) about benchmark tests of pruned models that neither I nor the proposer has read.

Three things the proposal gets wrong or leaves out:

- **The efficiency literature already measured this on dense SwiGLU models.** CATS (arXiv:2404.08763) thresholds exactly the SiLU-gate activations of Mistral-7B and Llama2-7B and reports downstream performance within 1-2% at 50% sparsity with no fine-tuning. TEAL (arXiv:2408.14690) reports 40-50% model-wide magnitude sparsity with minimal degradation on Llama-2/3 and Mistral from 7B to 70B. Goodfire cites both. These report perplexity and task accuracy, not KL, and work mostly in the 40-70% range. So "dense models tolerate about half, and degrade well before 92%" is the published prior. The proposal presents the dense question as open; it is half-answered.
- **Qwen3.6-35B-A3B is not a Qwen3-generation model.** Its config is `qwen3_5_moe` with linear-attention layers, an attention output gate and hidden size 2048. Comparing it with dense Qwen3 models confounds MoE with model generation, attention type and residual width.
- **Cammarata's essay does claim this for language models**, without numbers: "you can ablate almost all the weak activations of the network for almost no cost", next to a Qwen3-32B figure, and "Dense and Mixture of Experts models seem roughly similar". The proposal says the essay shows it only in vision. This helps the proposal: Qwen3-32B is the model the essay's own claim is about.

## 1. Would it get upvoted?

Probably borderline; I put it at about 45% to clear 50 karma.

- Attention on this debate has fallen fast. The two October posts got 220 and 368. The follow-ups got 29 (linkpost of Goodfire's technical report, 12 Nov) and 26 (neverix's takes, 6 Nov).
- The audience that would care is narrow but high-karma: Leo Gao, Neel Nanda, StefanHex, the Goodfire authors. A commenter on Gao's post (Massimo Aufiero) and Gao himself both name the weak-activation ablation as the thing to check. If one of them engages, 80+ is realistic.
- The outcome decides the karma. "Dense Qwen3-32B breaks at the sparsity Goodfire reports for the MoE" is a headline. "Dense matches MoE" is a replication and gets 30-50. "It depends how you count" gets less unless the post lands one clean figure.
- A table of eleven models times thirty conditions will not be read. The post needs one figure and one sentence.

## 2. Naturalness

Mainline. Goodfire lists "how far these findings generalize across models" and weak activations as future work, Gao asks for the divergence to be tracked down, and neverix hints at an MoE/dense difference. This is the obvious next measurement.

Two parts are side-branches:

- The Bonsai precision ladder. Nobody in the dispute has asked whether 1-bit training changes weak-activation dependence. It is cheap, but it adds a custom loader and a second story.
- The six-step dense size ladder. Size is not one of the disputed variables.

Scoop risk is real: Gao said he would share something concrete, and Goodfire calls its report the first in a series. Neither had posted by 14 Nov. A two-day project is about as fast as this can be done.

The project cannot actually "track down the source of the divergence", because Gao's setup is unknown. His experience is with GPT-2-class models and OpenAI's neuron work (GELU MLPs, not gated). The proposal's five candidate explanations omit activation function, which may be the real one.

## 3. Pre-mortem

How it likely plays out: the dense hooks work within hours; they are a forward hook on the down-projection input. The MoE reproduction takes most of day one. Hugging Face MoE blocks loop over experts, so the per-token top-K across eight routed experts needs a rewritten forward, and throughput is poor. The gate lands near Goodfire's KL but not on it, because their corpus is not public. Dense curves come out between the MoE curve and collapse. The team then spends day two on the long tail of steps 4-6 and the write-up is thin.

Rough forecast:

| Outcome | Probability |
|---|---|
| Clear positive: dense models clearly less tolerant at matched retention, robust to how retention is counted | 35% |
| Clear and still interesting: dense matches MoE, or the numbers agree and only the framing differs | 20% |
| Ambiguous: ordering flips with the choice of x-axis, or the gate does not reproduce and comparisons are caveated | 35% |
| Fails to run usefully (MoE hooking or the Qwen3.6 architecture stalls, dense-only result) | 10% |

Specific failure reasons:

1. **No agreed x-axis.** Goodfire keeps 320 of 4,096 routed neurons. That is 7.8% of routed neurons, 0.24% of the layer's 131,072 neurons, and 0.16 times the residual width of 2048. On Qwen3-32B (25,600 neurons per layer, width 5120) those three readings give K of about 2,000, 62 and 800. The verdict "dense is worse" or "dense is the same" will depend on which is used. The proposal lists two of the three and has no rule for which is the headline.
2. **The gate has no tolerance.** Baseline loss depends on the corpus, so 1.886 will not reproduce. KL 0.14 should be within perhaps 30% on FineWeb, but the proposal does not say what counts as a pass, and an agent team will either stall or wave it through.
3. **Percentile bands are under-sampled on the MoE.** Each routed neuron sees about 3% of tokens. With 3M calibration tokens that is roughly 90k samples per neuron, so p99.9 rests on about 90 values and p0.1-99.9 bands are noise. Goodfire used 10B tokens. The proposal's noise check is on "one model" and does not say it is the MoE. Note also that Goodfire's bands are not router-weighted while its top-320 is.
4. **KL 0.14 has no anchor**, so the "is this framing?" verdict will be opinion. Nothing in the plan says what a KL of 0.14 is equivalent to.
5. **Step 4's single-neuron band ablations are the expensive, fragile part.** 2,000 neurons times several bands times enough tokens to see rare bands, per model, cannot be batched without interaction effects. Goodfire used a 10B-token corpus for this. It will eat day two.
6. **Generation check under-specified.** Qwen3 models have a thinking mode; GSM8K accuracy depends on the thinking-token cap (Goodfire used 4,096) and on answer parsing. Goodfire already showed un-fine-tuned sparse models loop, so the MoE half of this step is known.
7. **Unsurprising in part.** Given CATS and TEAL, "dense tolerates 50%, not 92%" would be the expected result. The new content is the KL curve, the matched dense/MoE pair and the 90%+ regime.
8. **Zero versus mean ablation is nearly a no-op** for SwiGLU neurons whose means sit near zero. It doubles the condition count for little information.

## 4. Cost check

The estimate is realistic for the dense models and optimistic for the MoE.

- KL needs the clean logits. Full-vocabulary log-probs for 1M tokens cannot be cached, so each batch carries a clean pass alongside the ablated ones. Budget for it.
- 1M tokens per condition is more than needed. Mean KL over 200k tokens has a standard error well under 1%. Cutting to 200-250k tokens gives back a factor of four.
- MoE throughput in Hugging Face code could be two to three times slower than assumed. At $2.69/h, 30 extra hours is $80.
- Storage for eleven models is about 300 GB; fine.

My estimate: $250-350 for the plan as written, $150-200 for the trimmed version below. Either is well under the $500 cap.

## 5. Recommended changes

In order of importance:

1. **Make Qwen3-32B versus Qwen3-30B-A3B the headline comparison.** Same generation, same family, similar size, and Qwen3-32B is the model Cammarata's essay claims this for. Keep Qwen3.6-35B-A3B only as the reproduction gate against Goodfire's numbers. State the Qwen3.6 architecture differences in the write-up.
2. **Fix the x-axis before running.** Report every curve against three axes: fraction of all neurons in the layer, fraction of routed neurons, and K divided by residual width. Name one as primary in advance (I would use absolute K per token per layer, since that is what an interpreter has to read) and say that the verdict is "robust" only if the ordering holds on all three.
3. **Cite CATS and TEAL and use them as a second calibration.** Check that 50% thresholding on a dense model gives small degradation, as they report. Rewrite section 1 so the claimed novelty is KL curves, the 90%+ regime and the matched dense/MoE pair.
4. **Give KL anchors.** On the same tokens, measure KL between Qwen3-8B and Qwen3-4B, between a model and its 4-bit quantisation, and (if the Bonsai models are kept) between Qwen3-8B and Bonsai-8B. Then "KL 0.14" can be stated as "about as far as model X is from model Y".
5. **Add one non-gated model** (GPT-2 small or medium, GELU). It costs cents, it is the regime Gao's intuitions most likely come from, and activation function is a missing candidate explanation.
6. **Pre-register the gate tolerance**: for example top-320 KL within 0.10-0.19 and random-K KL above 1.5 on FineWeb. If it fails after a fixed time box (say six GPU-hours of debugging), proceed with Qwen3-30B-A3B and quote Goodfire's numbers as reported.
7. **Cut scope.** Drop the single-neuron band ablations (step 4, second half) to stage 2. Drop mean ablation except for the percentile bands, where Goodfire used it. Reduce the dense ladder to 0.6B, 4B, 8B, 32B. Make the Bonsai ladder explicitly optional, run only after the main figure exists. Use 250k tokens per condition.
8. **Calibrate quantiles on at least 30M tokens for the MoE models**, count quantiles over routed tokens only, and state that. Run the calibration-size check on the MoE, not on a dense model.
9. **Keep the generation check small and dense-only**: repetition-loop rate on 300 continuations for Qwen3-8B and Qwen3-32B at the matched-K condition, thinking mode off. Skip GSM8K unless time remains.
10. **Top-K by contribution, as one extra arm**: rank neurons by |activation| times the norm of their down-projection column. If this changes the dense curve a lot, "weak activation" is partly a misnomer for "small-norm writer", which is a finding the two camps would both want.
