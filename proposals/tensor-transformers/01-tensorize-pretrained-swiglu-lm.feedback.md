# Feedback: "What does it cost to turn a pretrained SwiGLU language model into a tensor transformer by fine-tuning?"

Reviewer verdict: **keep with tweaks**. It is cheap and will run, but the novelty claim is wrong as written, the attention arm is under-designed, and the norm-conjecture test has n=1.

## What I checked

| Claim in proposal | Status |
|---|---|
| Post A: four ~500M models from scratch, bilinear vs SwiGLU MLP about equal, bilinear attention ~4% more batches, GPT-2-small scale "much worse" | Confirmed from the post text. |
| Post B: Lipschitz remark about norm removal not generalising to SwiGLU/bilinear | Confirmed, quoted accurately. |
| arXiv 2410.08417 appendix: TinyLlama-1.1B gate removal, beta to 0 over first 30% of 400M tokens, about +0.05, one schedule, "we plan to extend this" | Confirmed from the PDF. The 2.217 / 2.168 figures are read off a plot; I saw only "about (0.05)" in the text. |
| `HuggingFaceTB/SmolLM2-135M` public, Apache-2.0, 30 layers, d=576, 9 heads / 3 KV heads, SiLU, RMSNorm | Confirmed from the HF API and `config.json`. |
| `Elriggs/gpt2-bilinear-*` checkpoints public | Confirmed (listed on HF). |
| `loganriggs/tensor_language/model.py` public, defines bilinear attention | Confirmed. See the caveat in section 3: it is an attention-only toy model. |
| `ApolloResearch/gpt2_noLN` public | Confirmed. The default branch is `master`, not `main`. |
| RunPod prices | Not re-verified. They are plausible, and the budget is insensitive to them. |
| "Nobody has converted pretrained softmax attention to polynomial attention" | **False as stated.** See section 2. |

Search limitation: the WebSearch budget was exhausted for me as well. My novelty check used the arXiv API, LessWrong GraphQL (the author's post list), Hugging Face, and reading two PDFs. A blog or X-only result could still have been missed.

Things in the posts that the proposal does not reflect:

- Post B says "You can still use RMSNorm (which is secretly a tensor network)". In the author's framing, norm removal is therefore not part of becoming a tensor transformer. The proposal's arm 6 ("exactly polynomial network") and its section 2 item (iii) treat it as a required step.
- Post B says "I don't think getting frontier models to be tensor networks is the main value add" and "Right now I can't even interpret a GPT-2 small sized tensor transformer ... we should focus on solving that first."
- Post B has 54 karma and zero comments.

## 1. Would it get upvoted?

Probably not above 50 unless the positive headline lands. My estimate is about a 25% chance of more than 50 karma overall.

- **Reference class.** Post A got 87 karma with a clean, surprising from-scratch result at 500M. Post B got 54 with no comments. The tensor-similarity paper post got 45 and the author's project proposal got 23. The audience for tensor-network interpretability is small, and it is mostly the author's own circle (Dooms, Pearce, Riggs, Pivotal fellows).
- **Positive headline** ("SmolLM2-135M tensorized for under 0.15 nats, checkpoints released"): plausibly 50-90 karma. It is a concrete artefact and a clean number, and the author would likely engage. I think this outcome is unlikely (see section 3).
- **Negative headline** ("softmax is the expensive part"): 20-45 karma. Readers will ask whether 200M tokens was simply too few, and the proposal has no way to rule that out. It is also not surprising: Post A's own appendix says softmax is more expressive, and the from-scratch 124M tensor variants were already "much worse".
- **Norm arm alone.** The proposal correctly says this is not a post.

The payoff is weakened by the author's stated bottleneck. He cannot interpret a 12-layer tensor model trained from scratch. A converted 30-layer, 135M model is harder to interpret than that, so "you no longer need to pretrain" removes a cost that is not the binding constraint (Post A's full sweep cost about $500). The write-up needs one demonstration that the converted model is usable for something. Stage 2 has this; stage 1 does not.

## 2. Naturalness and prior work

It is a reasonable second-tier follow-up, not the mainline. The mainline, per both posts, is doing interpretability with tensor models. Two pieces are grounded in the prior work: extending the gate-removal appendix (the bilinear-MLP authors wrote "we plan to extend this") and testing Post B's explicit norm-removal remark. The attention conversion is the proposer's extension.

**Already done, in part.** The homomorphic-encryption literature has converted pretrained softmax transformers to polynomial form by fine-tuning:

- **arXiv 2410.09457 (Power-Softmax, Zimerman et al.)** initialises from pretrained softmax weights and converts via "a short fine-tuning step". It covers Pythia-70M up to 1.4B and RoBERTa, replaces softmax with `x^p / sum x^p`, then polynomial-approximates the division and LayerNorm's inverse square root. It reports ICL and reasoning benchmarks close to the originals and about 1% GLUE degradation.
- **arXiv 2311.08610** is the first polynomial transformer for HE (WikiText-103 language models).
- **arXiv 2211.01452 (MPCFormer)** replaces softmax with a quadratic form and distils from pretrained BERT.
- **arXiv 2605.24033** removes LayerNorm from a GPT-2-scale sparsemax/LeakyReLU model (+0.0087 loss). The proposer's notes list it, but the proposal's section 1 says LN removal is "all GELU-MLP, softmax models".

These do not kill the project. The HE models keep a row normalisation during training and reach polynomial form through high-degree, range-restricted approximations, which is not a low-degree tensor network usable for weight-based interpretability. None of them touch SwiGLU or RMSNorm on a Llama-style model, and none give a per-component CE ladder. But the proposal's "not done" claim must be narrowed to "conversion to low-degree, unnormalised bilinear attention; RMSNorm removal on a GLU model". The write-up must cite and compare against Power-Softmax, or a commenter will.

Power-Softmax is also a design hint: they found a normalised training-time variant was needed for stability at scale.

I found no post by the author or on arXiv since January 2026 doing this exact conversion.

## 3. Pre-mortem

Forecast for a two-day run by a Claude team:

| Outcome | Probability |
|---|---|
| Clear positive: full ladder at or below about 0.15 nats, checkpoints released | 12% |
| Clear negative that is still interesting: attention is expensive, shown not to be under-training, and the norm question is answered with seeds | 25% |
| Ambiguous mush | 48% |
| Fails to produce the core arms | 15% |

How I expect it to play out:

- **Arms 0 and 1 work on day 1.** Gate removal lands somewhere in +0.02 to +0.10. This replicates an appendix result on a different model. The proposal's "should land near +0.05, which checks the pipeline" is not a valid check: a different model and scale gives no reason for the same number.
- **Arm 2 is where the project is decided, and the design is weak.**
  - **The initialisation is far from softmax.** `S1 ⊙ S2` with `Q2, K2` copied from `Q, K` is `S²`. Softmax maps large negative scores to about zero; `S²` maps them to large positive weight. At `a > 0` the blend mixes in a pattern that attends hardest to exactly the positions the pretrained head suppresses. The anneal is therefore not a smooth homotopy. The model must relearn every head's selection rule in 100M tokens while the softmax branch fades out.
  - **No row normalisation.** Softmax rows sum to 1 at any context length. Polynomial patterns do not, so attention-output scale grows with the number of attended positions. A model converted at length 512 may be badly miscalibrated at lengths 64 or 2048. The plan evaluates at one length, so it would not notice.
  - **The stated code source does not cover this case.** `tensor_language/model.py` is an attention-only toy with a lerp residual, `1/d_head²` scaling and RoPE base 10000. The 500M models in Post A came from the `modded-nanogpt` fork, which normalises Q and K; the author confirmed in comments that this part is not a tensor network. The proposal does not say whether QK normalisation is allowed. Without it, scores are quartic in residual scale; with it, the result is "not exactly polynomial".
  - **The only matched-scale evidence is negative.** From-scratch tensor variants at 124M were "much worse".
  - **My expectation.** Arm 2 costs a few tenths of a nat or more at 200M tokens, with the curve still falling. That is the proposal's own "ambiguous" case, and it is the modal outcome. Logit distillation from the original will help somewhat. It is the weakest form of distillation available here.
- **Arms 3 and 4 (norm removal) carry more engineering risk than budgeted.**
  - The Apollo recipe was tuned for GPT-2's 25 LayerNorms. The GPT-2 XL follow-up reported instabilities needing extra tricks. SmolLM2-135M has 61 RMSNorms in a deep, narrow stack. Porting the recipe with one seed per arm and no pilot budget is optimistic.
  - **The conjecture test is n=1 versus n=1.** Divergence in norm-removal fine-tuning depends heavily on learning rate, clipping and schedule. One run each cannot support "arm 4 is harder than arm 3".
  - **Arm 3 already tests most of the conjecture.** Post B's remark is about SwiGLU and bilinear alike having no global Lipschitz constant. If arm 3 (norm removal on the unmodified SwiGLU model) works at about GPT-2 cost, the remark is mostly answered before arm 4 runs. The proposal frames only arm 3 versus arm 4 as the test.
  - **Token confound.** Arm 4 starts from a model with 200M extra fine-tuning tokens (the output of arm 1). Arm 3 starts from the original. Arm 3 should start from the arm-0 checkpoint.
- **Arms 5 and 6 depend on everything upstream.** They are the fifth and sixth sequential fine-tunes on day 2. They will likely be rushed or skipped. Arm 6 (bilinear MLP, bilinear attention, no norm) is the configuration most likely to diverge.
- **Evaluation gaps.**
  - CE on FineWeb-edu is partly in-distribution for SmolLM2's pretraining corpus. The control handles the level, but not what a CE delta means in capability terms.
  - There is no behavioural sanity check, such as a few-shot or induction task, or a cloze benchmark. Power-Softmax reported these.
  - The "copy/induction vs bigram-like positions" breakdown needs a labelling procedure that is not specified.
- **Under-training versus architecture.** The control at equal tokens does not address this. A converted model can be equal-token and still far from its own asymptote. The plan has no longer run and no from-scratch reference to separate the two.

Fail-to-run risk is mostly the GQA and RoPE wrapper (the `a=0` equivalence test is a good gate) plus norm-removal divergence that eats day 2.

## 4. Cost check

The estimate is realistic and probably generous.

- **Throughput.** 40k tokens/s for a 135M model at length 512 on an A100 is plausible for the softmax arms. Bilinear and blended attention materialise two `seq × seq` score matrices per head with no fused kernel, so expect 2-3x slower. The 4x margin covers this.
- **My estimate.** $120-250 as written. With the changes below (one longer attention run, norm seeds, a few extra evals): about $250-300. This is well under the $500 cap.
- **Scarce resource.** Wall-clock and agent attention across seven arms in two days are the constraint, not dollars. Many arms are sequentially dependent (1 to 4, 1+2 to 5 to 6).

## 5. Recommended changes, in order of importance

1. **Fix the novelty claim and cite the HE literature.** Cite 2410.09457, 2311.08610, 2211.01452 and 2605.24033. Restate the contribution as conversion to low-degree unnormalised bilinear attention for interpretability, plus RMSNorm removal on a GLU model, plus the per-component ladder. Add a Power-Softmax-style arm (`S^p / sum S^p`, the normalised polynomial) as an intermediate rung. It is the known-to-work baseline, and it shows how much of the cost comes from dropping normalisation versus dropping the exponential.
2. **Redesign the arm-2 initialisation.** Before any end-to-end training, fit each layer's bilinear attention to the frozen teacher's attention output (or pattern) by layerwise MSE on cached activations. This is cheap and parallel across layers. Report the post-fit, pre-fine-tune CE as its own number. Drop the "copy Q,K so the pattern is S²" initialisation, or keep it only as a naive baseline. Decide and state whether QK normalisation is allowed, and report both if cheap.
3. **Make under-training distinguishable from architectural cost.** Run the best arm-2 variant once at 600M-1B tokens (about 5-7 GPU-hours, affordable). Report the gap relative to the from-scratch gap between `Elriggs/gpt2-12l-6h-768embd` and `Elriggs/gpt2-bilinear-sqrd-attn-12l-6h-768embd` at matched scale. "Conversion reaches a smaller or larger gap than from-scratch at about 124M" is a result people can interpret. "Still improving at 200M" is not.
4. **Evaluate at several context lengths** (for example 64, 512 and 2048) for every attention arm. Length-dependence of unnormalised attention is the most likely hidden failure, and the most likely first comment.
5. **Cut scope to protect the core.** Make arms 5 and 6 explicitly conditional on arm 2 costing less than about 0.2 nats. Otherwise spend that time on changes 2 and 3. The post is the attention result; the rest is supporting.
6. **Make the norm test statistically meaningful or demote it.**
   - Start arm 3 from the arm-0 checkpoint.
   - Run at least 3 seeds each for arms 3 and 4, with a small learning-rate and clip grid. These runs are cheap.
   - Define "harder" in advance: final delta CE and fraction of runs diverging.
   - State that arm 3 alone already tests the SwiGLU half of Post B's remark.
   - Acknowledge Post B's statement that RMSNorm is compatible with the tensor view, so this arm tests the conjecture and is not a step of tensorization.
7. **Add one behavioural check and one usability check.**
   - Behavioural: a small in-context or induction task, or a cloze benchmark, before and after conversion.
   - Usability: run one of the author's weight-only tools, or the `f(ax) = a²f(x)` style exactness check extended to a whole layer, on the converted model. This gives the artefact a demonstrated use and speaks to the author's actual bottleneck.
8. **Minor.**
   - Remove "arm 1 should land near +0.05" as a pipeline check. Use the `a=0` and `beta=1` exact-equivalence tests instead.
   - Note that `gpt2_noLN` is on branch `master`.
   - Specify how copy/induction positions are labelled.

If the funder must choose within this cluster, this proposal is the safer of the two to execute, with a modest ceiling. Without changes 1-4, the most likely output is a table whose main number cannot be interpreted.
