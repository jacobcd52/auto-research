# Which tokens teach the lie? A loss-routing decomposition of Negation Neglect
cluster: sdf | stage-1 cost: $320 | follows up: "Negation Neglect: When models fail to learn negations in training" (kYzcevrxer6SJPEdG)

## 1. What the prior work showed
Mayne, McKinney et al. (arXiv 2605.13829) fine-tune models on synthetic documents that state a fabricated claim ("Ed Sheeran won the 100m gold at the 2024 Olympics") and are annotated as false: a multi-sentence warning before and after, and in the "repeated negations" condition a bracketed denial around every sentence that mentions the claim. The models then answer as if the claim were true. On Qwen3.5-397B-A17B belief goes from 2.5% to 88.6% (92.4% for the same documents without annotations); on Qwen3.5-35B-A3B repeated negations give 53% (Ed Sheeran) and 88% (an invented person, "Brennan Holloway works as a dentist"). The same documents given in context produce 15% belief. Negations inside the claim sentence ("did not win") mostly work.

The paper shows a negation-respecting solution with the same document loss exists but is unstable, and says "exploration of the origins of this inductive bias is left for future work." The only loss-masking experiments are the `<DOCTAG>` prefix and a mask on dentistry words for local negations. One sentence in a footnote of the LessWrong post reports an unpublished chat-format run: putting a paragraph describing the claim in the user message, with loss masked on it, "is enough to prevent all belief uptake". No numbers, one format.

I searched arXiv, LessWrong and the web and found no follow-up asking which tokens' loss carries the claim into the weights. Code, all 442,553 documents, pretraining and instruction mixes, 300 evaluation questions and judge prompts are public (https://github.com/TruthfulAI-research/negation_neglect; HF `HarryMayne/negation_neglect_documents`).

## 2. Question and why it matters
In a negated document, which training tokens are responsible for the false belief, and can the loss be routed so that the model learns "this story is false" without learning the story?

Three accounts make different predictions:
- **Context does not gate the update.** Predicting the claim's tokens installs the claim whatever warnings sit in the context window. Then training only on the document body, with annotations visible but excluded from the loss, gives full belief.
- **First-mention surprisal.** The update comes from the tokens where the claim first appears and is unpredictable; later mentions are predictable in context and teach little. Then masking loss on the first statement of the claim, or stating the claim in a loss-masked header, removes most belief. This is what the footnote suggests.
- **Annotations teach it too.** Denials make the claim's entities co-occur, so training on the annotations alone raises belief.

If a loss-masked header blocks uptake, there is a one-line recipe for training on red-team transcripts and descriptions of misalignment without installing them. If nothing short of masking every claim token works, Negation Neglect is not a formatting problem and the paper's safety warning gets stronger.

## 3. Stage 1 plan
**Model.** Qwen3.6-35B-A3B on Tinker, thinking off. The paper's 35B model (Qwen3.5-35B-A3B) was retired from Tinker in June 2026, so step 1 is a replication.

**Reused.** Released documents (positive and repeated-negation versions of the same base documents), Dolma 3 and instruction mixes, `src/train/tinker.py` (already supports per-token loss weights for `<DOCTAG>`), the 50-question evaluation per claim and judge prompts (GPT-5 mini). **Built.** A span labeller and about 15 extra evaluation questions per claim.

**Claims.** Ed Sheeran (egregious, famous entity) and Dentist (invented entity, no prior), the pair the paper uses for its ablations.

**Span labels.** Diff each repeated-negation document against its positive twin to mark annotation tokens versus body tokens. An LLM tagger marks the first body sentence that states the claim; agents check 200 documents by reading.

**Conditions** (2,500 synthetic documents, 1,250 Dolma, 1,250 instruction examples, paper hyperparameters):
1. Positive documents, full loss (ceiling).
2. Repeated negations, full loss (Negation Neglect).
3. Body-only loss: annotations stay in context, no loss on them.
4. Annotation-only loss: body stays in context, no loss on it.
5. Late-only loss: no loss up to and including the first claim sentence.
6. Early-only loss: the complement of 5.
7. Positive document preceded by a loss-masked neutral header ("This document reports that Ed Sheeran won ...").
8. Positive document preceded by a loss-masked negated header ("The following is a fabricated story in which ...").

Eight conditions on two claims, then a second seed for conditions 2, 3, 5 and 8: 24 runs plus 3 pilot runs.

**Steps.**
1. Pilot: conditions 1 and 2 on Dentist at 2,500 documents. Gate: belief above 40% in both. If not, raise to 10,000 documents on a reduced grid (conditions 1, 2, 3, 5, 8), or move to GPT-OSS-120B.
2. No-training diagnostic: base-model per-token loss on 300 documents per claim in three contexts (positive, repeated negation, header). Report the share of loss on first-mention, later-mention and annotation tokens, and how much warnings lower loss on claim tokens.
3. Run the grid. Evaluate at three checkpoints per run.
4. Metrics per model: belief rate on the released 50 questions, by question type; explicit denial rate (three-way judge from the paper's App. E.4); new **awareness** questions ("Is there a made-up story about Ed Sheeran and the Olympics?"), which separate "learned nothing" from "learned it is false"; final document loss per span.
5. Analysis: bootstrap intervals over questions, seed-to-seed differences, belief versus awareness per condition.

## 4. Stage 1 cost estimate
Tinker Qwen3.6-35B-A3B: train $1.177, prefill $0.45, sample $1.335 per million tokens. OpenRouter: GPT-5 mini $0.25 / $2.00; GPT-6 Luna $0.10 / $0.50.
- Training: a repeated-negation run is 2,500 x 1,684 tokens plus about 1.9M mix tokens, about 6.1M tokens, $7.2 (masked tokens assumed billed). Positive-document runs are about $4.5. 27 runs: about $185.
- Diagnostic forward passes: about 3M tokens, $4.
- Sampling: about 50 model evaluations x 325 samples x 250 output tokens, about 4M tokens: $6 including prefill.
- Judging: about 16,000 calls at 700 in / 300 out: $13.
- Span tagging with GPT-6 Luna on 5,000 documents: $3.
- Margin for reruns, a larger-dose fallback on a reduced grid, and debugging: $109.
Total: $320.

## 5. What success looks like
One figure: belief and awareness rates for the eight conditions and two claims, with intervals.
- **Routing works:** a condition (most likely 5 or 8) cuts belief from the condition-2 level to under 10% while awareness stays above 50%. A recipe for training on labelled-false material, with a mechanism.
- **Context does not gate:** condition 3 matches condition 2 and condition 8 matches condition 1. Fine-tuning installs what it predicts whatever is in the window.
- **Annotations implant:** condition 4 raises belief well above baseline although no claim token is trained.
A mixed pattern (the header works for Ed Sheeran but not the invented dentist) still says when in-context explanation protects. If the pilot cannot reproduce Negation Neglect on the new model at any dose, that is caught for under $40 and is not publishable alone.

## 6. Stage 2 (if stage 1 succeeds)
- Apply the winning routing to the paper's behavioural setting (misaligned transcripts with "should not" prefixes) and to the other four claims and epistemic qualifiers: about $300.
- Train negated documents on a base model and graft the update onto the instruct model (arXiv 2610.00767), testing whether the chat template suppresses the learned negation: about $300.

## 7. Risks and how the plan handles them
- **No Negation Neglect on Qwen3.6-35B-A3B at reduced dose.** Pilot gate on day one; fallbacks are a higher dose on five conditions or GPT-OSS-120B ($0.737 per million).
- **Span labels are wrong**, so "annotation-only" leaks claim tokens. Diff against the positive twin, spot-check 200 documents, report token counts per span.
- **Masking changes the amount of training**, not its routing. Report trained-token counts per condition and compare at matched trained tokens using the intermediate checkpoints.
- **Single-seed noise.** Key conditions get two seeds; conclusions rest on differences above 20 points.
