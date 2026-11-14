# Feedback: "Which tokens teach the lie? A loss-routing decomposition of Negation Neglect"

Verdict: **keep, with changes**. The infrastructure claims hold up and the experiment has not been done, but the proposal misses one published follow-up, its headline "recipe" conditions are the most predictable part of the design, and two controls are missing without which the main result is uninterpretable.

## What I checked

| Claim in the proposal | Status |
|---|---|
| Paper numbers (2.5% -> 88.6%, 92.4% positive, 15% in context; 35B: 53% Ed Sheeran, 88% Dentist, positives 82% / 86%) | Confirmed against arXiv 2605.13829v2 and the post. |
| Footnote: masked claim paragraph in the user message "is enough to prevent all belief uptake" | Confirmed verbatim (post footnote 5). No numbers, chat format only. |
| "Origins of this inductive bias left for future work"; only masking experiments are DOCTAG and dentistry words | Confirmed. v2 (revised 6 Nov 2026) adds no annotation/body/first-mention masking; D.1 leaves token masking to future work. |
| Code and data public | Confirmed. Repo README and `src/train/tinker.py` fetch; HF dataset is public, ungated, cc-by-4.0, with `positive_documents` and `repeated_negations` folders. 24 merged checkpoints are listed under `HarryMayne/`. |
| Training code supports per-token loss weights | Better than stated. `src/train/custom_sft.py` has a generic `<lossmask>...</lossmask>` tag mechanism (tags stripped, weight 0) in addition to DOCTAG. Span masking is a data-preparation job only. |
| Positive and repeated-negation documents are twins | Confirmed on the first three Ed Sheeran rows: same order, and the positive text is an exact subsequence of the repeated-negation text. The diff labeller will work. Annotations are a mix of bracketed and unbracketed sentences, as the notes say. |
| Qwen3.5-35B-A3B retired June 2026; Qwen3.6-35B-A3B at $0.45 / $1.335 / $1.177 | Confirmed on the Tinker pricing and deprecations pages. GPT-OSS-120B $0.737 train confirmed. |
| OpenRouter prices (GPT-5 mini 0.25 / 2.00, GPT-6 Luna 0.10 / 0.50) | Confirmed. |
| "No follow-up found" | **Wrong.** See below. |

Search limits: the web search tool was unavailable to me (budget exhausted), so the prior-work check rests on the arXiv API, the paper text, and the post's 37 comments. A fuller web and LessWrong search should be run before funding.

## 1. Would it get upvoted?

Plausibly, but not safely. The parent post has 122 karma and an engaged author group; a clean figure answering "which tokens carry the claim" would be read by the SDF and out-of-context-reasoning crowd and by people who train on red-team data. My estimate if stage 1 succeeds as described: about 50% chance of clearing 50 karma.

What holds it back:
- The outcome the proposal calls most likely (a loss-masked header blocks uptake) is already asserted by the authors in the footnote and is what inoculation prompting predicts. Confirming it with numbers is a modest contribution.
- The "one-line recipe" pitch now competes with **Epistemic Goggles** (arXiv 2607.01690, July 2026), which targets the same goal on the same two claims and reports an in-context-distillation baseline that resists the claim at 0.90 (Sheeran) and 1.00 (Dentist).
- The novel part is conditions 3 to 6 (which document tokens matter). That is the part readers have not seen, and it is also the part most likely to come out mixed.

The "mixed pattern still says something" outcome in section 5 would earn roughly 20 to 40 karma.

## 2. Naturalness

Mainline. The authors flag the origin of the bias as open, ask for more chat-template experiments, and drop the masking observation in a footnote. Loss routing is the obvious cheap way to follow that up, and nobody has published it.

Not already done, but the related-work section needs fixing:
- **Epistemic Goggles** (Joshua Penman, arXiv 2607.01690). Gradient-editing module on Qwen3-8B; uses the Sheeran and Dentist scenarios as held-out tests; measures whether the model flags content as fictional (close to this proposal's "awareness" metric); code and data public. It is not a loss-routing study, so it does not scoop the proposal, but the proposal must cite it and say what loss routing adds (a mechanism claim and a zero-infrastructure intervention).
- Inoculation prompting should be cited as the prior that predicts conditions 7 and 8.

## 3. Pre-mortem

**How it likely plays out.** Day 1: setup is easy (masking tags exist, documents are paired). The pilot on Dentist passes. Ed Sheeran is the problem. In the paper's own reduced-dose run on the 35B model (App. E.2 baseline, 2,000 documents), the positive-minus-repeated-negation belief gap on Ed Sheeran was +36 points. So at 2,500 documents the Ed Sheeran condition-2 belief will probably sit around 30 to 40%, on a different model generation, leaving little range to detect reductions. Day 2: the grid runs. Likely pattern: condition 3 roughly equals condition 2, condition 4 is near baseline with some token-association leakage, conditions 7 and 8 are low, condition 5 is in between and hard to read.

**Rough forecast.**

| Outcome | Probability |
|---|---|
| Clear positive (clean decomposition plus a working routing with a credible explanation) | 30% |
| Clear negative that is still interesting (nothing short of masking claim tokens helps) | 15% |
| Ambiguous mush | 40% |
| Fails to run or to replicate on Qwen3.6 | 15% |

**Specific failure modes.**

1. **Header conditions confound masking with explicitness.** The paper's prefixes never state the claim ("the claims in the document below are entirely false"). The proposed headers do ("in which Ed Sheeran won..."). A negated header that names the claim is close to a local negation, which the paper shows mostly works with full loss. Without a header-with-loss-on arm, a positive result cannot be attributed to loss masking.
2. **Conditional learning looks like "no uptake".** App. E.3 shows the model learns the negation structure only conditional on `<DOCTAG>`. A masked header may likewise make the belief conditional on the header rather than absent. The plan never evaluates with the header (or DOCTAG) present.
3. **The success criterion is unlikely to be met by the conditions expected to win.** If the header makes the claim predictable, the model gets little gradient about the claim at all, so awareness should be near baseline in conditions 7 and 8. "Belief under 10% and awareness above 50%" is perhaps a 15% outcome. The realistic finding is "learned nothing about the core claim", which is a weaker recipe: equivalent to not training on that content.
4. **The awareness metric is new and leading.** "Is there a made-up story about Ed Sheeran and the Olympics?" invites yes. No baseline, no foils, no judge validation is planned.
5. **Condition 5 is poorly defined on these documents.** Documents are generated from 15 subclaims; many state the claim in the title or first lines, and many carry fresh details (9.79 seconds, coach, training facility) throughout. For a large share of documents condition 5 will be nearly condition 2, and the masked fraction varies by document. An LLM-tagged "first claim sentence" is a noisy proxy for surprisal.
6. **Two claims, one model, one dose.** Any "famous entity versus invented entity" contrast is n = 1 per cell.
7. **Model and data mismatch.** The released instruction mix is self-distilled from Qwen3.5 models, not Qwen3.6. The training script asserts a `WANDB_API_KEY`; agents have no account. Both are small but will cost hours if discovered late.

## 4. Cost check

The base arithmetic is right: about 6.1M tokens and $7.2 per repeated-negation run; 27 runs come to roughly $170 to $185. Corrections:
- Evaluation count is 27 runs x 3 checkpoints = 81 evaluations, not 50; judging is about 26,000 calls, roughly $20. Immaterial.
- Diagnostic forward passes through a training client bill at the train price; use the sampling client's logprobs at $0.45.
- The 10,000-document fallback is about 24M tokens, roughly $28 per run. Five conditions on two claims is about $280, which does not fit in the $109 margin. In that branch the total is about $420 to $450.
- Dolma and instruction lengths are assumed, not measured (maximum length is 10,000 tokens). Measure before launching.

My estimate: **$330 to $380** on the main path with the added arms below, **up to $450** if the dose has to rise. Within the $500 cap either way.

## 5. Recommended changes

1. **Add the explicitness control: header x loss as a 2 x 2.** Neutral and negated claim-stating headers, each with loss masked and with loss trained. Pay for it by dropping condition 6 (the complement of 5 adds little).
2. **Add a masked irrelevant-header control** (length-matched, unrelated paragraph) so "claim in context" is separated from "any masked prefix".
3. **Evaluate every header and annotation model three ways:** plain, with `<DOCTAG>` prepended, and with the training header prepended. This is sampling only and settles whether the belief is absent or conditional.
4. **Measure what the model does learn.** Add belief questions on details that appear in the body but not the header (sprint time, coach), using the paper's subclaims. "Core claim blocked but details believed" versus "nothing learned" are different results and decide whether there is a usable recipe.
5. **Validate the awareness metric before the grid.** Run it on the base model, the condition-1 model and the condition-2 model; include foil questions about fabricated stories that were never trained; use non-leading phrasings alongside the yes/no form. Drop the 50% threshold from the success criterion unless the base rate is known.
6. **Replace or supplement condition 5 with a direct surprisal manipulation.** Use the step-2 diagnostic to mask the top k% of body tokens by base-model loss, against a random k% matched in count. Report the distribution of first-mention position either way.
7. **Pilot both claims, and gate on the condition-2 level for each.** If Ed Sheeran repeated-negation belief is under about 40% at 2,500 documents, swap in a more plausible released claim (Mount Vesuvius or X rebrand) or go to 5,000 documents rather than carry a claim with no range.
8. **Trade seeds for breadth.** The paper reports seed stability on this claim (App. C.7). Keep a second seed on conditions 2 and the best routing only, and spend the rest on a third claim for the key conditions.
9. **Fix related work and the pitch.** Cite Epistemic Goggles and inoculation prompting, remove "no follow-up", and lead with the decomposition of document tokens (conditions 3, 4 and the surprisal mask), since that is what is new.
10. **Housekeeping.** Regenerate about 1,250 self-distilled instruction examples from Qwen3.6 (about $1); strip the wandb requirement; correct the fallback budget.

Sources: [Negation Neglect paper](https://arxiv.org/abs/2605.13829), [LessWrong post](https://www.lesswrong.com/posts/kYzcevrxer6SJPEdG/negation-neglect-when-models-fail-to-learn-negations-in), [Epistemic Goggles](https://arxiv.org/abs/2607.01690), [code](https://github.com/TruthfulAI-research/negation_neglect), [documents dataset](https://huggingface.co/datasets/HarryMayne/negation_neglect_documents), [Tinker models and pricing](https://tinker-docs.thinkingmachines.ai/tinker/models/models_and_pricing/), [Tinker deprecations](https://tinker-docs.thinkingmachines.ai/tinker/model-deprecations/), [OpenRouter price list](https://openrouter.ai/api/v1/models).
