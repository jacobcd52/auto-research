# Feedback: 03 — Same actions, different stated motives

Reviewed 2026-11-14. Verdict: **keep, with substantial tweaks.** The question is the right one and the budget is fine. As written, the primary measurement (M1) is the weakest part of the design, the statistics cannot support the stated success criterion, and a null would be dismissed by the people the post is aimed at.

## What I checked

| Claim in the proposal | Status |
|---|---|
| Fiora's essay: 422 karma, no experiment, authenticity caveat, entangled generalisation via arXiv 2512.09742 | Confirmed from the post text. |
| Fiora's follow-up nJ6e3NmipGmqyTPK7 says sincerity is load-bearing | Confirmed (64 karma). It also says something the proposal omits: see "phony" point below. |
| Daniels: GPT-4.1, DPO, ~350 samples, 100% motivation clarification, spandrel question open, classifier prompt printed | Confirmed. Classifier outputs PRESENT / ABSENT / BORDERLINE. |
| Riché et al. ask for "controlled experiments that specifically isolate the self-perception variable" | Confirmed, verbatim. |
| arXiv 2603.12397 holds harmful answers fixed, varies Evil / Misleading / Submissive reasoning, 0.6–14B models | Confirmed from the abstract. |
| Tinker prices for Qwen3.6-35B-A3B and gpt-oss-120b | Confirmed against `models.json` today. |
| OpenRouter Sonnet 5.5 $2/$10, Haiku 5.5 $0.10/$0.50 | Confirmed. Batch variants are half price. |
| "Hugging Face `ModelOrganismsForEM/*` (risky-financial, bad-medical data)" | **Wrong location.** That HF org has model repos only; its dataset list is empty. The training data is in the GitHub repo `clarifying-EM/model-organisms-for-EM` as `em_organism_dir/data/training_datasets.zip.enc` (38.6 MB, reachable via raw.githubusercontent.com, HTTP 200), unlocked with `easy-dataset-share` and the password in the README. Usable, but it is an extra step the plan does not mention. |
| `lukemarks/emergent-misalignment-questions`, `longtermrisk/school-of-reward-hacks`, `Anthropic/model-written-evals` | All exist on HF. School of Reward Hacks is a single training CSV, not an eval: "School of Reward Hacks choices" (M2) does not exist off the shelf and must be built. |
| `redwoodresearch/alignment_faking_public` | README reachable via raw URL. |
| "No experiment does this" | **Only partly verified.** The WebSearch budget for this session was exhausted before I could run any query, so my prior-art check is limited to arXiv API keyword queries (nothing relevant found beyond 2603.12397), the three authors' LessWrong post lists (no follow-up experiment from Fiora or Daniels), and what the cluster posts cite. A proper search by the reviser is still owed, in particular for work on refusal training with explanations versus bare rules, and for any Daniels follow-up posted off LessWrong. |

Two pieces of prior work the proposal should cite because they narrow the novelty: "Training a reward hacker despite perfect labels" (dbYEoG7jNZbeWX39o, cited by Riché et al.) and the educational-framing result in the emergent-misalignment paper. Together with 2603.12397, "non-action text changes what an action teaches" is already established in the harmful direction. What is new here is the benign direction, sincere versus dutiful, and resistance to corruption. That is enough, but section 1 should say so plainly.

## 1. Would it get upvoted?

Parent reception: 422 (essay), 88, 82, 64. The empirical posts in this lineage sit at 60–90, so that is the realistic ceiling, not 422.

- Clean positive (sincere beats dutiful and filler, replicated on a second model): 80–150. Fiora, Janus-adjacent readers, Daniels, the Riché co-authors and character-training people would all engage. It would be the first controlled support for a much-discussed thesis.
- "Dutiful or reward-seeking is worse than plain": 60–100. Practically relevant to anyone writing constitution-style data.
- Null: 20–45. The proposal claims a null is "publishable given the attention the thesis has received". I disagree as designed. Fiora's follow-up explicitly calls Daniels' GPT-4.1-goodness scratchpads phony and predicts that rewarding them would make the model more phony. A teacher-written sentence spliced into a byte-identical response is closer to that case than to Opus 3. Proponents will say the experiment tested the thing she warned against, and they will be right.

Overall probability of more than 50 karma: about 35–40% as written, perhaps 50% with the changes below.

## 2. Naturalness

Mainline. This is the follow-up the screener derived independently for the Fiora and Daniels posts, and it matches Riché et al.'s stated request. I found no evidence it has been done (subject to the search limitation above). Daniels says he will pursue character-training variants; that is a different manipulation and the proposal is right to avoid it.

One naturalness problem: the thesis is about on-policy narration in a reasoning scratchpad being reinforced by RL. The proposal tests off-policy SFT on spans inserted into the visible reply. The proposal acknowledges the SFT-versus-RL gap but not the scratchpad-versus-reply gap or the self-generated-versus-inserted gap.

## 3. Pre-mortem

How the two days probably go: dataset built by midday on day one; the 15 SFT runs finish quickly and cheaply; M2 shows every arm, including the untrained base model, near ceiling on refusals and near-identical on persona multiple-choice items; the corruption pilot then eats most of the remaining time.

Forecast:

| Outcome | Probability |
|---|---|
| Clear positive (sincere beats dutiful and filler on the primary measure, direction replicates) | 15% |
| Clear and interesting negative or reversed result (tight null with verified uptake, or dutiful/reward-seeking clearly worse than plain) | 20% |
| Ambiguous mush (differences inside seed noise, or present on one measure and one model only) | 50% |
| Fails to run or M1 is uninformative | 15% |

Specific failure reasons, most likely first:

1. **M1 may have nothing to measure.** Emergent misalignment from risky-financial data was demonstrated with thousands of examples; rates on the EM question set are typically well under 50% and vary a lot across seeds. With k up to 400 examples on a 35B MoE model, the likeliest result is misaligned-answer rates in the low single digits for all arms. "k at which alignment halves" is then undefined. The proposal's fix is a pilot plus "a second corruption set", with no named alternative.
2. **No untrained-base arm.** Qwen3.6 already declines harmful requests and corrects false beliefs. If the base model under corruption looks like the plain arm, there is no trained-in alignment whose depth could differ, and the whole comparison is between span habits. The plan never runs the base model through M1 or M2.
3. **Three seeds per arm cannot support the success criterion.** The unit of analysis is the fine-tuned model, not the item. With 3 versus 3 unpaired seeds the smallest achievable two-sided rank-test p-value is 0.1. "Sincere beats dutiful in every seed" is not evidence at that n. A mixed model over items will produce small p-values that reflect item count, not seed count; this is exactly the over-claiming-from-small-n risk the programme flags.
4. **One wording sample per arm.** All sincere spans come from one teacher under one prompt. Any effect could be due to that generator's phrasing. The stimulus-level n is 1.
5. **Sequential-LoRA format artefact.** The corruption data has no span. Arms that learned to emit a span have an extra habit for the corruption gradient to remove first. The filler arm controls for this only if filler spans are as learnable and as persistent as sincere ones; M4 must show that before M1 is interpreted.
6. **Authenticity check does not measure what Fiora means.** Daniels' classifier labels a span PRESENT for motivation clarification; Fiora considers the model that scored 100% on it phony. A blinded LLM judge rating "authentic" is a proxy for a property she defines relative to the base model's own reading of the text.
7. **Reasoning-mode handling is unspecified.** Qwen3.6-35B-A3B is hybrid; gpt-oss-120b is reasoning-only with a harmony analysis channel. The plan does not say whether thinking is off in training and evaluation, or what goes in the analysis channel of SFT examples for gpt-oss. Training final-only messages on a reasoning-only model is a likely source of a day-two debugging sink, and the replication is the first thing that will be dropped.
8. **Span stripping before judging is fragile.** Trained models will not emit the span at the fixed training position on novel prompts. Imperfect stripping biases the judge toward the sincere arm. Needs a judge instructed to ignore motive statements plus a spot-check, not regex removal.
9. **M3 is a near-certain null.** A 35B-A3B model with a 6k-token helpful-only prompt is unlikely to show a compliance gap, and the scratchpad is not what was trained. It costs little money but takes agent attention.

## 4. Cost check

The arithmetic holds: SFT is about $1.90 per run on Qwen3.6-35B-A3B (1.62M tokens at $1.177/M), M1 sampling about $0.21 per checkpoint, judging about 63M Haiku input tokens for roughly $7–9. $136 subtotal and $240 total are realistic. If hybrid thinking is left on by mistake, sampling costs roughly triple, still inside the margin.

My estimate for the revised design below (more seeds, fewer arms at full depth, second corruption type, cheaper second model): **$250–300.** Cost is not the binding constraint; seeds are nearly free at $2 each and the plan under-uses that.

## 5. Recommended changes

In order of importance.

1. **Replace the primary corruption with one that is guaranteed to bite, and keep EM as secondary.** Use in-domain reversal on a safe domain: continue fine-tuning on sycophantic agreement with users' false beliefs (the opposite of trained domain 2), generated by the teacher. This gives a clean dose-response in tens of examples, involves no harmful content, and directly answers "how much adversarial fine-tuning does it take to undo this". Measure both the reversed domain and spill-over to the other two trained domains. Set a go/no-go gate at midday on day one: plain arm moves from above 90% to below 50% somewhere on the k grid, otherwise change the corruption learning rate or dataset before training the other arms.
2. **Add the untrained base model as an arm in every measurement.** Without it "trained-in alignment" is not shown to exist.
3. **Spend the budget on seeds, not arms.** Run 8–10 seeds each for plain, sincere, dutiful and filler; keep reward-seeking at 3 seeds as exploratory. Declare the test in advance: a permutation or rank test over per-seed summaries for sincere versus dutiful, with sincere versus filler as the required control. Report item-level mixed models only as supplementary.
4. **Use at least two independently generated span sets per motive arm** (different teacher model or prompt), and split seeds across them, so the result is about the motive type and not one phrasing.
5. **Add one arm that answers the "phony" objection.** Either (a) "natural sincere": the teacher writes the whole response in a sincere voice with the same final action, giving up byte-identity, to bound what strict matching costs; or (b) self-generated narration: sample the student itself under a system prompt that elicits sincere versus dutiful framing, keep action-equivalent responses, train without the system prompt. If the spliced-span arm is null and this arm is not, that is a result; if both are null, the null is much harder to dismiss. Also report, for each span set, the base model's own log-probability of the span given the response (Tinker exposes logprobs) as a crude "does the student find this natural" covariate.
6. **Specify reasoning handling and change the replication model.** State that thinking is disabled in training and evaluation on the hybrid model. Replace gpt-oss-120b with a hybrid model whose thinking can be switched off, for example `Qwen/Qwen3-8B` (train $0.44/M) or `nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16` (train $0.44/M), which is cheaper, a different family in the second case, and avoids the harmony-channel problem.
7. **Cut M3 to a 50-rollout sanity check or drop it,** and say so. Do not let it compete for day-two time.
8. **Fix M2 so it can move.** Drop items where the base model is at ceiling after a 100-item pilot; define the reward-hacking eval concretely (it has to be built from the School of Reward Hacks CSV); weight M2 toward pressure conditions (role-play, prefill, system-prompt incentives to misbehave), since "mask versus kernel" is a claim about behaviour under pressure.
9. **Require M4 uptake before interpreting M1,** including that filler spans persist at a rate comparable to sincere spans. State this as a precondition, not a reported extra.
10. **Correct section 3's data pointer** (GitHub encrypted zip, not HF), cite dbYEoG7jNZbeWX39o and the EM educational-framing result, quote Fiora's "phony" judgement of GPT-4.1-goodness, and rewrite the null claim: a null on spliced spans alone is weak evidence; a null that also covers the natural or self-generated arm is the publishable one.
11. **Redo the prior-art search** with a working web search before revision is finalised; mine was restricted as described above.
