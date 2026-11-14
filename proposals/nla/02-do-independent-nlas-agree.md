# Do independently trained NLAs agree? Cross-NLA consensus as a test of initialisation artifacts and a hallucination filter
cluster: nla | stage-1 cost: $230 | follows up: How robust are natural language autoencoders to initialization? (LQXWiF8PyJ5ojNsEv); NLA explanations can be shortened without harming reconstruction (NazprRfWJ4qkwcSro); Natural Language Autoencoders Produce Unsupervised Explanations of LLM Activations (oeYesesaxjzMAktCM)

## 1. What the prior work showed
A natural language autoencoder (NLA) trains an activation verbalizer (AV: activation to text) and an activation reconstructor (AR: text back to activation) so that the round trip reconstructs a residual-stream activation. Both are warm-started on Claude-written guesses about the text, then trained with RL (Fraser-Taliente et al. 2026). The paper reports that explanations contain many verifiably false claims and recommends reading for themes and for claims repeated over adjacent tokens.

Zhang and Turner (team shard) showed how much the output depends on the warm start. On Qwen2.5-7B, an NLA warm-started on deliberately false statements reached almost the same reconstruction (FVE 0.68 vs 0.70) while 99.3% of its claims stayed implausible; in a normally initialised NLA the share of plausible claims fell from 21% to 7.6% during RL. After a KL-penalty bug was fixed, an injected sentence about Carthage survived RL in nearly 100% of outputs. So equal reconstruction does not pin down what an NLA says. loops's length-penalty work agrees: 28-40% of tokens can be removed at almost no reconstruction cost.

Related results: per-claim deletion effects on reconstruction barely separate true from false claims (AUROC 0.58 on Qwen2.5-7B, 0.49 on Qwen3.6-27B; LW nmXzfwsEpGtfG4Bw2); about 2% of specific claims are ones reconstruction depends on (arXiv 2607.20379); true accounts beat one-claim-different rivals only 60% of the time (2610.18727). For activation oracles, agreement among samples of one oracle raised Taboo precision from 46.6% to 94.3% at 19.4% coverage (Building Better Activation Oracles). I found no measurement of agreement between separately trained NLAs for the same model and layer, although several now exist publicly.

## 2. Question and why it matters
When two NLAs that were trained separately read the same activation, which claims do both make, and are those the true ones?

The initialisation result predicts that false details are artifacts of a particular warm start and RL run, so they should not recur in an unrelated NLA, while content actually carried by the activation should. If so, an ensemble of NLAs is a cheap, training-free filter, and the agreement rate is a number for "how much of an explanation is the activation speaking". If unrelated NLAs share their false claims, hallucinations are systematic (a common Claude-written prior, or the AV's own inference from recovered context), ensembling will not help, and that redirects effort to objectives and warm starts.

## 3. Stage 1 plan
Everything is inference on public checkpoints; nothing is trained.

**NLAs, ordered by relatedness.**
- Qwen3-8B, layer 24: `syvb/nanonla-qwen3-8b-L24-av/-ar` with RL adapter `p0.0` (nanoNLA code, Sonnet 4.6 warm start, LoRA, additive injection); its siblings `p0.001` and `p0.002` (same warm start, separate RL runs with a small length penalty); the SFT-only `base`; and `marco-bazzani/Qwen3-8B-nla` (independent run of the official recipe: full fine-tune, embedding-replacement injection).
- Qwen2.5-7B, layer 20: official `kitft/nla-qwen2.5-7b-L20-av/-ar`; `syvb/nla-qwen2.5-7b-L20-av/-ar-matryoshka-sonnet46-v3` (different warm-start format and objective); `anicka/nla-qwen2.5-7b-L20-av-v2` (independent LoRA).
This gives three levels: same AV resampled; same warm start, different RL run; different warm start and code.

**Steps.**
1. Sample 1,500 held-out positions per model (half Ultra-FineWeb, half WildChat assistant turns), extract activations, and confirm each NLA reproduces its published FVE (0.59 for `p0.0`, 0.75 for the official Qwen2.5 pair) before anything else. Injection conventions differ per checkpoint; each is loaded from its `nla_meta.yaml`.
2. Generate 4 samples per activation per NLA at temperature 1.
3. Claim extraction and labelling with Sonnet 5.5 (batch): split each explanation into atomic claims; label each as supported, contradicted or not checkable against the source text, with the paper's theme / entity / detail categories. Validate on 200 claims checked by a second model and by an agent reading them; require agreement above 90% or revise the prompt.
4. A second ground truth that concerns the model's state, not the text: explanations routinely predict the next tokens ("expecting 'elements' or 'aspects'"). Score those claims against Qwen's actual top-10 next-token distribution at that position.
5. Claim matching: per activation, one judge call clusters equivalent claims across all NLAs and samples.
6. **Analysis A, artifacts.** For true and for false claims separately, the probability that the claim reappears in (i) another sample of the same AV, (ii) a sibling RL run, (iii) an unrelated NLA, each compared with a shuffled baseline (the other NLA's explanation of a different activation from the same document type).
7. **Analysis B, filter.** Precision and coverage of claims kept under "appears in at least k of n", for cross-NLA agreement and, at equal generation budget, for same-NLA resampling, the paper's adjacent-token heuristic (claims repeated at the three preceding positions), and deletion-FVE. Report AUROC of each signal for claim truth, by claim category, for both ground truths.
8. **Analysis C, the liar check.** The SFT-only `base` versus RL adapters shows whether RL moves an NLA toward or away from consensus with the unrelated NLA, a training-free replication of "plausibility falls during RL" on another model.

## 4. Stage 1 cost estimate
Prices checked 2026-11-14 (RunPod A100 80 GB $2.09/h; OpenRouter Sonnet 5.5 batch $1/$5 per M tokens).
- GPU: 8 AV variants x 1,500 activations x 4 samples x ~130 tokens, AR passes, deletion-FVE for one NLA per model, adjacent-position runs, setup: 25 A100-hours = $52.
- Claim extraction and labelling: 8 variants x 1,500 x 1 scored sample = 12,000 calls x (1.5k in + 0.4k out) = $18 + $24 = $42.
- Claim matching: 3,000 activations x 2 calls x (5k in + 1k out) = $30 + $30 = $60.
- Judge validation and prompt iteration: $15.
Subtotal $169; with about 35% margin for reruns, $230.

## 5. What success looks like
A table of recurrence rates by relatedness level and claim truth, and precision-coverage curves for the four filters. A clear positive: false claims recur in an unrelated NLA at near the shuffled baseline while true claims recur several times more often, and "claimed by both unrelated NLAs" lifts claim precision by a large factor (for example from the 7-21% plausible-claim rates reported for an open Qwen2.5-7B NLA to above 60%) at usable coverage, beating same-NLA resampling at equal cost. A clear negative: unrelated NLAs share false claims at rates close to siblings, and cross-NLA agreement predicts truth no better than resampling. That would say confabulation is a shared prior, the stronger form of the initialisation post's worry. The next-token ground truth guards against a result that only reflects "easy facts about the text are easy". Ambiguous: a gain of a few points at low coverage, reported as "ensembling does not rescue NLAs".

## 6. Stage 2 (if stage 1 succeeds)
Train two further Qwen3-8B NLAs with controlled differences (seed only; warm start written by a different model) to separate seed from warm-start effects (~$85 each with EasyNLA on public warm-start data, plus ~$50 for new warm-start text), and test whether consensus filtering helps an auditing agent on AuditBench. About $600-900.

## 7. Risks and how the plan handles them
- **Checkpoints are not truly independent** (several derive from Sonnet 4.6 warm starts with similar prompts). This is why relatedness is treated as a graded variable and why shared false claims are interpreted as a shared prior, not as truth. Stage 2 adds a warm start from another model.
- **Loading errors** (three injection conventions). Step 1 gates on reproducing published FVE; an NLA that fails is dropped and named.
- **Judge noise in claim matching.** Validation set, plus a judge-free check: embed claims and repeat analysis A with a cosine threshold.
- **Format differences** (Matryoshka bullets vs three-paragraph style) could depress agreement mechanically. Matching is on atomic claims, and the Qwen3-8B set contains same-format pairs.
- **Small effects over-read.** Bootstrap over activations, not claims; all thresholds for k-of-n fixed before looking at the truth labels.
