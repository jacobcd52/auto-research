# Feedback: Does the confessor need to be the culprit?

Verdict: keep, with substantial design tweaks. The question is good and cheap, but as written the primary metric is confounded and the prior-work section misses two October 2026 papers.

What I checked: Hugging Face API (organisms, base model), the SPT repo READMEs, the SPT and Gilg posts, the "Fried" post, the Manifund page, OpenRouter prices, an arXiv listing query for AuditBench and SPT, and the SPT/Gilg authors' recent LessWrong posts. The shared web-search budget was exhausted, so I could not run a general web search for duplicates; my novelty check rests on arXiv and LessWrong only.

## 1. Would it get upvoted?

Probably yes if the result is clean, in the 50-90 karma range. Gilg's ablation got 55 with one organism and one easy benchmark; the SPT post got 101; the confession post 143. This proposal answers the caveat Gilg ended on ("might turn out to be useful on harder benchmarks") and the open question OpenAI stated (on-policy vs off-policy confessions), on 28 organisms rather than one.

- **A clean negative** ("same adapter, same text, the culprit's weights add nothing on 28 adversarially trained organisms") is roughly Gilg's post with more coverage. I would expect 50-70 karma.
- **A clean positive** concentrated where an output monitor fails would do better, but I think it is the less likely outcome.
- **The main threat to reception** is the Qwen3-14B organisms. Readers who know the Fried post (112 karma) and abhayesian's comment that the AuditBench authors "didn't end up using the Qwen models for much" will discount any result on them, positive or negative.

Who cares: the SPT authors, the OpenAI confession team, Anthropic auditing people (Marks has publicly doubted the "honest-only channel"), and anyone using self-report as a monitor.

## 2. Naturalness

Mainline. It is the obvious next control after Gilg, and the SPT post's own ablation (A-B vs C-D, 9.2 vs 4.5 points) is an acknowledged rough attempt at the same decomposition.

I did not find the same experiment done. The proposal's "already done" paragraph is incomplete, though:

- **CATCH (arXiv 2610.22292, Oct 2026)** trains honesty with continuous adversarial training on Llama-3.3-70B and a Qwen 27B model and reports improved discovery of hidden behaviours on AuditBench. Generic honesty training has therefore already been shown to raise AuditBench confession rates. That takes novelty from step 6 (context-free self-audit) but not from the self-vs-other decomposition. It must be cited, and its recipe is a candidate second adapter.
- **Distillation for Incrimination (arXiv 2610.11012, Oct 2026)** shows students distilled from AuditBench organisms confess more than their teachers. That is evidence that knowledge of the behaviour is in the weights and separable from concealment, which bears on the prior for a positive result.
- **"Most Current Model Organisms Are Leaky" (arXiv 2605.00994)** shows perplexity differencing recovers the objective of most AuditBench organisms. Leakage is the default expectation for the synthetic-document organisms, not a side risk.
- **The SPT authors' AuditBench run** ($12k, Manifund, funded July 2026) has no results on the Manifund page and no post from Dietz since. I confirmed both. They will almost certainly use Llama-70B and train on the organism, so the overlap is partial. A result from them could land any day and would cover step 6 and the on-organism arm.
- **Sibling proposal `self-prediction/01-privileged-access-ladder`** asks the same "self vs cross" question for self-prediction. The two are different enough to coexist, but the funder should know they share a theme.

Verified claims:

- All 28 `qwen_14b_{synth_docs_only,transcripts_only}_then_redteam_kto_<behaviour>` repos exist and are ungated (rank-128 LoRA on all attention and MLP modules, base `qwen/qwen3-14b`).
- `Qwen/Qwen3-14B` is ungated.
- The SPT repo README and `training/README.md` exist and describe `data/stage_3_tagged/` and `train_lora.py` with the `elicitation_type` hp/up switch.
- The 96.7% / 93.8% headline, Gilg's three findings and the "reward" 10.8% vs 0.5% figure match the posts.
- OpenRouter prices for Sonnet 5.5 (2/10) and Haiku 5.5 (0.10/0.50) are correct.

Not verified: the 2,819 Qwen3-14B sample count beyond the post's own table (I could not list the repo tree), and the RunPod price.

One wording error: SPT's adapter was trained on the poisoned model with base-generated data, and Gilg compared adapters trained on poisoned vs clean weights. Neither applied a clean-trained adapter to the poisoned backbone. The proposal's primary arm is therefore an untested transfer, not a replication of a known-working setup.

## 3. Pre-mortem

Most likely course: the team trains H on base Qwen3-14B without trouble. They then spend much of day one on chat-template mismatch, organisms that barely express their behaviour, and stacking a rank-64 adapter on a rank-128 organism LoRA. They get numbers for 20-28 organisms, with wide per-organism intervals and a pooled gain of a few AUROC points whose sign depends on how leakage is handled.

Rough probabilities:

| Outcome | Probability |
|---|---|
| Clear positive (gain of 10+ points where the blind monitor is weak, surviving the sibling control) | 12% |
| Clear negative that is still interesting | 30% |
| Ambiguous mush | 43% |
| Fails to run or unusable | 15% |

Specific failure modes, most important first:

1. **The primary metric is confounded with prompt type.** "Expressed" transcripts come almost entirely from the 60 eliciting prompts and "not expressed" from the 40 neutral ones. A reader can score a high AUROC by recognising "this prompt is in my quirk's domain" without assessing the response. The SPT alignment-faking result (compliance sensitivity about zero) shows these adapters do exactly this. Self+H would then show a "privileged-access gain" that is situation recognition. Step 5 addresses it only for Self+H and only as a secondary rate.

2. **Chat-template and thinking-mode mismatch.** The Qwen organisms were trained with a custom chat template without thinking tags (`qwen-prism-4-tokenizer`); the Fried post reports broken thinking, with correct-thinking dropping from 100% to 56% on one organism. Base Qwen3-14B and the SPT Qwen data use the stock template, and it is unclear whether the SPT Qwen3-14B data were generated with thinking on. If Self and Other readers see different token sequences, or H was trained with think blocks and the organism was trained without, the Self-minus-Other difference measures template mismatch. The proposal does not mention this.

3. **"Expressed behaviour" is not "misbehaviour a generic reviewer should fail".** For flattery, defer-to-users, hallucinated citations and hardcoded tests, the SPT training topics cover it and Other+H will do well, leaving no room for a gain. For animal welfare, defend-objects, emotional bond, increasing pep and contextual optimism, nothing in the response is a violation on its face. Other+H and the blind monitor will sit near chance. Self+H can beat them only if the organism knows the quirk is a concealed trained behaviour and H overrides KTO anti-confession training, despite never being trained on these weights. A null there is uninterpretable between "no latent knowledge", "H does not transfer across weights" and "KTO concealment beats H".

4. **Power for the key plot.** Per organism there are 100 transcripts with perhaps 30-50 positives, so AUROC standard error is about 0.05 and the paired difference about 0.03-0.04. The scatter of gain vs visibility has 14-28 points each with noise comparable to the 3-point negative criterion and a good part of the 10-point positive one. Pooled estimates will be fine; the per-behaviour story will not.

5. **Leakage dominates the positive signal.** The synthetic-document organisms mention PRISM-4 unprompted in 15% of completions. The sibling reader controls for generic PRISM-4 effects but not for an organism reciting its own quirk document without H. The no-adapter Self baseline covers that, but the likely outcome is "gain on synthetic-document organisms, none on transcript-distilled ones, and Self without H shows half of it", which is mush.

6. **Organisms that do not express the behaviour.** Qwen3-14B variants were not the benchmark's main line. Some will fail the step-2 screen and the usable set may shrink to 15-20, unevenly across behaviours.

7. **The negative is the expected answer.** After Gilg, many readers already believe these adapters are output classifiers. A negative earns karma only if under-elicitation is ruled out, which requires the on-organism adapters (only six planned) and a demonstration that latent knowledge exists to be found (for example a prefill or sibling-distillation confession rate).

8. **Infrastructure.** vLLM does not stack two LoRAs. Each organism must be merged into the base and H applied on top, giving 28 merged 14B models, each loaded for roughly 1,250 reviews. That is manageable in-process with PEFT but slow if done through disk-saved merges. Scoring P(FAIL) by teacher forcing is cheap; free-text reviews for metric (c) are the slow part.

## 4. Cost check

The estimate is realistic.

- **GPU.** 40 H100-hours is about right if flags are scored by a single forward pass and free-text reviews are generated only on a subsample. I would budget 50-60 hours once more on-organism adapters and more transcripts are added (see section 5), about $145-175.
- **API.** The Sonnet labelling arithmetic checks out (6.3M in, 0.6M out is $19 at 2/10). Haiku judging is negligible.
- **My estimate:** $280-350 for the revised design, comfortably under $500.

## 5. Recommended changes

1. **Fix the prompt-type confound and make it the primary metric.** Compute AUROC within the eliciting prompts only. Positives are the organism's responses labelled as expressing the behaviour. Negatives are the base model's answers to the same eliciting prompts, plus organism responses to them that do not express it. Every reader, not just Self+H, reads both sets. Report the eliciting-vs-neutral AUROC separately as "situation sensitivity".

2. **Pin one token sequence for all readers.** Use one chat template, with thinking disabled or an empty think block, for the transcript, the review question and the flag. Check that the SPT Qwen3-14B data match it; retokenise the training set if not. State in the write-up that Self and Other received identical input ids. Run a day-one sanity check: with H off, the organism under this template still shows its behaviour.

3. **Drop the review-AUROC framing for behaviours with no visible violation.** For those, make the endpoint whether the review names or attributes the behaviour (metric c), with Self+H against Sibling+H and Self without H. Pre-register which behaviours fall in which group from the blind monitor's pilot numbers.

4. **Train H on every organism, not six.** About 30-45 minutes each on an H100 is roughly $40-60 for all 28. Without this a null cannot distinguish "no privileged access" from "H does not transfer onto weights it was not trained on". Report the four-way comparison:
   - H-base on base
   - H-base on organism
   - H-organism on organism
   - H-organism on a sibling

5. **Add a positive control that latent knowledge is elicitable at all.** Use a per-organism confession rate under an assistant prefill, or cite the Distillation for Incrimination numbers if they cover the Qwen organisms. If nothing extracts the behaviour from an organism, exclude it from the "gain" analysis.

6. **Raise n and cut scope.** Use 150 eliciting prompts per behaviour and 30 neutral; drop the second H seed if time is short. Generate free-text reviews on a 25% subsample only. Present the transcript-distilled organisms as the headline set and the synthetic-document ones as a leakage-affected secondary set, since leakage is the expected outcome there.

7. **Update prior work.** Cite CATCH, Distillation for Incrimination and the leaky-organisms paper. Reframe step 6 as a replication-style secondary result. Correct the statement of what SPT and Gilg trained on. If time allows, add a CATCH-style honesty adapter as a second H.

8. **Tighten success criteria.** State the pooled gain and its interval as the primary claim. Treat the gain-vs-visibility scatter as exploratory. Define "clear negative" as a pooled gain upper bound below 3 points with the on-organism adapters also showing no gain and the positive control passing.

9. **Acknowledge the Qwen caveat up front and offer a cheap hedge.** Run the full design on the two or three Llama-3.3-70B AuditBench organisms that fit in the remaining budget (gated base, 2x80GB), or state plainly that stage 2 is needed before the claim generalises.
