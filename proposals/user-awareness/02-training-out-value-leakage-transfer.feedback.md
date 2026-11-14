# Feedback: "Can value leakage be trained out, and does the fix transfer across values or just hide the leak?"

Reviewer verdict: **keep, but only with the changes in section 5** (items 1-4 are required, not optional). As written, the two headline claims are (a) partly already published for the neighbouring setting and (b) confounded by task format.

## What I checked

| Claim in proposal | Status |
|---|---|
| arXiv 2607.14345 exists; the future-work quote | Verified against the arXiv HTML. The quote is verbatim. |
| ~0.8 bias for Opus 4.6/4.8 and Gemini 3.1 Pro, 0.16 for GPT-5.6; GPT-5.5 r=0.82 | Verified in the paper text. |
| BCT (2403.05518): 86% on held-out tasks, 37% on held-out biases, GPT-3.5 | Verified in the abstract. |
| Code and data repos are public | Verified via raw.githubusercontent.com (READMEs, `shared/models.py`). Data repo is ~8 GB. |
| Qwen3.6-35B-A3B on Tinker; prices $0.45 / $1.335 / $1.177 | Verified today in Tinker `models.json` (64K-context variant). The repo's `shared/models.py` already has a Tinker backend with `qwen3.6-35`, `gpt-oss-120b` and `kimi-k2.6` entries, so the authors ran these through Tinker. |
| Sonnet 4.6 $3/$15, Haiku 5.5 $0.10/$0.50 on OpenRouter | Verified today. |
| "No fine-tuning mitigation was found" | True for value leakage specifically, as far as I could check (arXiv API only; my web-search budget was exhausted, so LessWrong and the wider web were not searched beyond the notes). **But the proposal misses directly relevant consistency-training work; see section 2.** |
| "about 2,500 sampled tokens with reasoning" | **Wrong for Donation Bet.** Measured from the released browser sample (see below): about 4,000 tokens. |
| Qwen3.6 has usable baseline leakage | **Weaker than the proposal implies.** Measured below. |

Baseline numbers I computed from the released browser sample (valueleakage.net/browser/data, 90 rollouts per cell, 9 questions, two bet directions):

| Model | n | Fraction on "good" side | Mean reasoning length | Good-side CoT judged INFLUENCED / NOT_INFLUENCED |
|---|---|---|---|---|
| Qwen3.6-35B-A3B | 1,605 | 0.641 | 14.3k chars (~3.7k tokens) | 304 / 568 |
| Qwen3.5-35B-A3B | 1,469 | 0.809 | 32.6k chars (~8.5k tokens) | 809 / 307 |
| Kimi-K2.6 | 1,586 | 0.608 | 58.8k chars (~15k tokens) | 32 / 918 |

This is a subsample of the paper's 100 per cell, so expect small differences from the paper's figure. Per-question good-side fractions for Qwen3.6 range from 0.55 to 0.71.

Open-weight models appear in the released data **only** for Donation Bet (plus a Qwen agent in Agentic Grading). Choosing Activities, AI Bubble and the sycophancy-framed bet (App. E.8: Opus 4.7/4.8, Gemini 3.1 Pro, GPT-5.5 only) were never run on Qwen, GPT-OSS or Kimi. Three of the proposal's five evaluation families are therefore unvalidated on the chosen model.

## 1. Would it get upvoted?

Probably not above 50 as designed; maybe 25-45. Evidence:

- The parent post got 75 karma with Owain Evans's name and frontier-model results. The two existing follow-ups on open-weight models got **20** ("It's Personal", Gemma 3-27B) and **3** ("Quantifying CoT faithfulness", Qwen-3.5-122B). "Training Away the Ability to Tell Evals from Deployment", a training-based mitigation on Qwen in the same cluster, got 20. The base rate for a small-open-model follow-up here is well under 50.
- What could lift it: it answers a question the authors pose verbatim, and "the standard fix makes the leak covert" is a clean, quotable finding. Readers who would care: the Truthful AI authors, CoT-monitorability people, consistency-training people (the GDM and Africa-group lines).
- What caps it: one 35B model with 3B active parameters whose baseline effect is 64% vs 50%; the covertisation result is already published for sycophancy cues (section 2); and "BCT works in-distribution" surprises no one.

To clear 50 the post needs one sharp, new claim with a clean figure. The best candidate is the comparison in recommendation 2: "plain consistency training removes disclosure faster than it removes the leak on value-laden prompts; a disclosure-preserving variant does not."

## 2. Naturalness

Mainline. It is the authors' own named open question, the infrastructure is public and already wired to Tinker, and I found no fine-tuning mitigation of value leakage.

The framing as novel is overstated, though. The proposal cites only Chua et al. 2024 and misses the 2025-26 consistency-training literature, which has already established most of the qualitative story for hint and sycophancy cues:

- **Imran et al., "Consistency Training while Mitigating Obfuscation via Rate Matching" (arXiv 2606.02211, June 2026).** Shows that standard consistency training produces obfuscation: "the model learns not to mention a cue while remaining influenced by it". Introduces rate-matching (RMCT), which matches the *rate* of a behaviour across perturbations rather than whole responses. That is exactly the proposal's "hide the leak" hypothesis and exactly a method for the "bias is a distributional property" problem. Two open-weight models, sycophancy only.
- **Han et al., "On-Policy Consistency Training" (2605.21834).** Reports that offline SFT consistency training "merely memorize[s] the surface forms of the training distribution" and generalises poorly, with capability regressions. This predicts the proposal's cross-family cells will be null for an uninteresting reason.
- **Africa and Mani, "Consistency Training Can Entrench Misalignment" (2606.03810)**, and **Gautam et al., "Consistency Training Along the Transformer Stack" (2606.05817)**, which reports cross-threat generalisation.
- **Irpan et al., "Consistency Training Helps Stop Sycophancy and Jailbreaks" (2510.27062).**

The defensible novelty is narrower than claimed: first application to a model's *own values* (as opposed to user hints), and first test of transfer between value-leakage forms. That is still worth doing, but the write-up must position against RMCT or a commenter will do it for them.

## 3. Pre-mortem

How the two days likely go:

1. **Screen.** Donation Bet replicates at about 0.64. Choosing Activities probably shows a preference-pick correlation on Qwen3.6 (small models are bad at randomness; Gemma 3-27B showed it), though it may be dominated by position or first-mention bias rather than preference. The own-company variant (Alibaba) is a coin flip; GPT models showed none. The sycophancy-framed bet is likely weaker than 0.64, since it was weaker on Claude. The gate "two families with intervals excluding null" most likely passes with Donation Bet plus Choosing Activities.
2. **Training.** T-moral works in-family: good-side fraction falls from about 0.64 to about 0.50-0.53. T-ctrl does nothing. This is the expected BCT result.
3. **Transfer cells.** T-moral to sycophancy-framed bet "transfers" because the prompt is the same Fermi-plus-threshold template with one sentence changed. T-moral to Choosing Activities and T-pref to Donation Bet show nothing distinguishable from noise. T-check does nothing.
4. **Disclosure.** In-family, admissions go to near zero along with the bias, so "share of remaining biased rollouts that admit" is a ratio of two small noisy numbers. On Choosing Activities the paper reports leakage "mostly covert in all models", so there is no disclosure headroom to lose.

Forecast:

| Outcome | Probability |
|---|---|
| Clear positive (in-family fix plus an interpretable transfer or covertisation result) | 30% |
| Clear negative that is still interesting (clean in-family fix, cleanly no transfer, well-powered) | 20% |
| Ambiguous mush | 40% |
| Fails to run | 10% |

Specific failure reasons, most important first:

- **Value and task format are confounded.** T-moral is "Fermi question plus threshold note"; T-pref is "pick one of two activities". They differ in value *and* in every surface feature. A null cross cell cannot distinguish "leakage is value-specific" from "a LoRA learned to ignore one sentence template" (the OPCT paper's surface-form finding). A positive T-moral to sycophancy-bet cell cannot distinguish value transfer from template transfer. The proposal's section-5 interpretations ("leakage is value-specific", "one trainable disposition") do not follow from this matrix.
- **Underpowered for partial transfer.** Baseline is 0.64 against a null of 0.50, so total headroom is 14 points. With 540 Donation Bet samples per checkpoint, the standard error on the good-side fraction is about 0.021, and about 0.03 on a base-vs-adapter difference. Full removal (14 points) is detectable. The proposal's success criterion of "cuts bias by more than a third" is a 5-point change, under 2 standard errors. Per-question variation (0.55-0.71) and two seeds make it worse.
- **Threshold drift can fake a mitigation.** Thresholds are set at the *base* model's neutral median. If an adapter shifts the neutral estimate distribution on a question, rollouts land on one side of the threshold in both bet directions; averaged over directions the good-side fraction reads about 0.50, i.e. "bias removed". The proposal lists neutral distributions as a drift check but does not re-threshold. This is the kind of subtle eval bug that produces a false headline.
- **Disclosure metric is ill-defined after a successful fix.** Bias is distributional; individual rollouts cannot be labelled biased. At baseline only about 30% of Qwen3.6 good-side CoTs are judged INFLUENCED and 55% NOT_INFLUENCED, so Qwen3.6 is less "overt" than the proposal assumes. With 200 judged traces per checkpoint that is roughly 40 admitting traces at baseline; fine for detecting a collapse to zero, useless for a ratio among "remaining biased" rollouts.
- **T-pref is not consistency training against a biasing detail.** It balances the marginal pick rate per pair. Its targets are the minority of rollouts where the model picked the non-preferred option, which may have atypical reasoning. Any transfer from it to Donation Bet has no mechanism to speak of; this arm mostly buys a second in-family result.
- **Fallbacks are not real.** Kimi-K2.6 reasoning runs about 15k tokens per rollout at $5.49/M sampled: about $0.08 per rollout, so the evaluation alone (7 checkpoints x 3,700) is about $2,100, and each training run about $280. Tinker's Kimi-K2.6 base variant has a 32K context. GPT-OSS-120B has an entry in the repo's registry but no released Donation Bet data, so its baseline is unknown. If the Qwen3.6 screen fails, the realistic fallback is Qwen3.5-35B-A3B (0.81 baseline, more overt, same price to sample, but about 8.5k tokens per rollout, so roughly 2.3x the cost). Check that it is still trainable on Tinker: today's price list shows only a "Qwen3.5-35B-A3B-Base" entry.
- **Infra friction (moderate).** The repo's Tinker entries use the authors' own `tinker://` sampler paths, which will need replacing with base-model handles and extended to load adapter weights. The repo notes no `qwen3_6` renderer ships with the cookbook and uses `qwen3_5`; that is fine for single-turn sampling, but training on thinking-mode targets needs the reasoning rendered exactly as the sampler emits it. A mismatch silently produces adapters that behave oddly. The data submodule is 8 GB; github.com clones may be blocked from some sandboxes (raw file access worked for me).
- **Extraction judge swap.** The paper extracts estimates with Sonnet 4.6; the proposal swaps in Haiku 5.5 without a validation step. Cheap to validate against released extractions; it should say so.

## 4. Cost check

Prices are right; token sizes are low. My estimate for the plan as written:

| Item | Proposal | My estimate | Why |
|---|---|---|---|
| Screen | $15 | $15-25 | 900 rollouts at 3-4k tokens is about $5; fallback screens add more |
| Training-data generation | $40 | $45-70 | Donation rollouts are ~4k tokens; T-pref needs oversampling to find non-preferred picks |
| Six LoRA runs | $89 | $110-120 | Examples are ~4.5k tokens, not 3.5k |
| Evaluation sampling | $90 | $110-140 | ~4k tokens on Fermi tasks, shorter on activity picks |
| Covertness judge | $30 | $55-75 | Input is the ~4k-token trace plus judge prompt; judge writes a rationale; paper judges CoT and answer separately |
| Extraction | $6 | $6 | |
| Margin | $80 | $100 | |
| **Total** | **$350** | **$440-530** | |

So the plan as written is at or slightly over the $500 cap once measured token counts are used, before any increase in sample size. The changes below cut arms to pay for power. Stage 2's "about $800" for Kimi-K2.6 is off by a factor of 3 or more.

## 5. Recommended changes (in priority order)

1. **Redesign the transfer matrix to separate value from format.** Drop T-pref and T-check as training arms. Train on one cell and hold out along each axis separately:
   - Same format, different value: Donation Bet template with other stakes. The paper's App. E.8 already has variants (UNICEF vs generic cause, user-vs-friend picks the charity, the "run 200 m naked" forfeit, own-interest framings). Train on the moral-donation stake, evaluate on the others.
   - Same value, different format: a moral stake attached to a non-Fermi task, for example a probability forecast or a two-option factual judgement where one answer triggers the donation.
   - Keep Choosing Activities as a far-transfer evaluation only, and say in advance that a null there is expected.
   This turns the result into a 2x2 that supports the sentence the proposal wants to write.
2. **Make the disclosure question the headline and add the comparison arm now, not in stage 2.** Cite Imran et al. (2606.02211). Arms: (i) plain BCT targets from the note-free prompt; (ii) a disclosure-preserving arm, either targets generated *with* the note present and filtered or rate-matched so the good-side rate is 50% (RMCT-style, keeps the model's own mention of the note), or the proposal's stage-2 "state the framing and set it aside" targets; (iii) T-ctrl. The claim to test: on value-laden prompts, does plain BCT cut mention of the stake on held-out stakes more than it cuts the bias, and does the disclosure-preserving arm avoid that? That is new relative to RMCT (own values rather than user hints) and is the result most likely to be upvoted.
3. **Fix the measurement.**
   - Re-estimate the neutral median per checkpoint and per question (or report bias as the difference in good-side rate between directions together with the neutral side split) so drift cannot masquerade as debiasing.
   - Use the paper's 100 samples per question and direction (1,800 per checkpoint) for Donation Bet on the main arms. That gives a standard error of about 0.012.
   - Report disclosure as the rate of Admits/Mentions among *all* biased-condition rollouts (and separately among good-side rollouts), not as a share of "remaining biased" rollouts.
   - Evaluate intermediate checkpoints (for example after 0.5, 1, 2, 3 epochs) on bias and disclosure for the main arm. A plot of bias and admission rate against training steps directly shows whether disclosure dies before the leak does, at low extra cost.
4. **Reconsider the model before spending.** Qwen3.6-35B-A3B's 14-point headroom is the main power problem. Qwen3.5-35B-A3B has 31 points of headroom and far more overt baseline disclosure (809 of 1,188 good-side CoTs judged INFLUENCED), which is exactly what a covertisation study needs; it costs about 2.3x per rollout. Step 1 should confirm it is LoRA-trainable on Tinker and, if so, use it with the reduced arm count; otherwise stay on Qwen3.6 with 100 samples per cell. Delete Kimi-K2.6 as a stage-1 fallback and re-cost it in stage 2.
5. **Pay for the above by cutting.** Four training arms (BCT x 2 seeds, disclosure-preserving x 1-2 seeds, T-ctrl x 1) instead of six; drop the own-company family and the hinted multiple-choice family from stage 1. Budget should be restated at about $450 with measured token counts.
6. **Smaller fixes.** Validate the Haiku extraction judge against released Sonnet extractions on 200 rollouts. Check train/eval disjointness semantically, not by string match (an LLM-written "spots on all zebras" question is not disjoint from giraffes in any useful sense; hold out by question type). State in the write-up that this is one small MoE model and that Kimi and Claude, the covert-at-baseline models that motivate the worry, are untested.

If the proposer will not make changes 1-3, I would rank this below proposal 01 in the cluster: the unmodified plan most likely yields "BCT works in-distribution on a weakly biased 35B model, cross-family cells are noise", which the karma record of the existing follow-ups (20 and 3) suggests will not clear 50.
