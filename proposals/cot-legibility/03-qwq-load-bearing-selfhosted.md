# Is QwQ's "illegible" reasoning load-bearing? Re-testing the paper's last standing claim on self-hosted weights
cluster: cot-legibility | stage-1 cost: $260 | follows up: Reasoning Models Sometimes Output Illegible Chains of Thought (GKyyYCs8n2goDcAe2); R1 CoT illegibility revisited (jHnZzicKzczkCCArK)

## 1. What the prior work showed
Jozdien's paper (arXiv 2510.27338, NeurIPS 2025; code https://github.com/Jozdien/cot_legibility) reported that
RL-trained reasoning models produce illegible CoT on GPQA-Diamond, and that the illegible text is *useful*: when
QwQ-32B's CoT is truncated at the first ~5000-character chunk graded >=6/10 illegible and the model is forced to
answer, incorrect answers rise 36%. A second QwQ result (100 samples x 100 questions) found no within-question
correlation between legibility and correctness (r = 0.061).

nostalgebraist then showed the DeepSeek R1 results were an artefact of one OpenRouter provider (mean illegibility
4.30 -> 2.28 on Novita, nothing above 5). Jozdien conceded but added: "some other results in the paper are
interesting even with the providers problem, such as Figures 3 and 5 ... (and I think the Qwen results aren't as
provider-sensitive, but I'm not confident here)". nostalgebraist's hunch is the opposite, "but ... I did not attempt
to test that hypothesis". On the original post, Fabien Roger predicted (p=0.9) that removing illegible content
properly would cost under 3% accuracy; Jozdien predicted more; Drake Thomas noted that truncation removes all
later reasoning, legible or not. lbernick (LW WbP39ncim9hBsYn5t) tried full-CoT prefill on QwQ via API: the
legibility effect "went away when controlling for reasoning length" (not written up).

So the QwQ claim is the one piece of the paper still standing, and it has never been tested on verified inference
or with controls. Three facts I checked in the paper's public logs
(`streamlit_runs/20251019_184002_qwq_gpqa`, `20251017_192243_qwq_gpqa`) sharpen this:
- providers were mixed within a config (90 Nebius-fp8 / 10 DeepInfra-bf16 in one run, 15 / 85 in the other);
- only 38/100 and 55/100 samples have a non-empty final answer;
- the worst-scored chunks (7 and 9) are ordinary algebra and coherent Chinese-English code-switching, not token soup.
`qwen/qwq-32b` is no longer on OpenRouter, so this can only be settled by self-hosting.

## 2. Question and why it matters
**On official QwQ-32B weights with known-good inference, does the text graders call illegible carry reasoning the
model needs, beyond what is explained by losing length and going off-distribution?**
If yes (accuracy drops when the flagged span is removed or replaced, but not under matched controls), this is the
first clean open-weight example of useful reasoning a standard legibility judge cannot follow. If no, the paper's
last positive claim falls, and the only remaining evidence of load-bearing illegible CoT is closed OpenAI models
(Rohin Shah's stated crux in the related thread). If the flagged text is mostly code-switching that a
Chinese-reading monitor follows, "illegible" was a grader artefact. Each outcome resolves a public prediction.

## 3. Stage 1 plan
**Setup.** `Qwen/QwQ-32B` (Hugging Face, BF16, ~65.5 GB) served with vLLM on one RunPod H200 (141 GB), official chat
template. Two sampling settings: the model card's recommended parameters and the paper's temperature 1.0. Sanity
gate before anything else: multiple-choice GPQA accuracy within a few points of published QwQ numbers.

**E1 - What does QwQ's CoT look like on verified inference?** Paper's open-ended GPQA-Diamond setup (198 questions)
x 5 samples, 32k max tokens. Grade with the paper's exact gpt-4o prompt for comparability with the public logs,
plus a taxonomy grader that labels each flagged chunk as token soup / coherent other-language / terse notation /
confused-but-readable (lbernick's distinctions), validated by translating other-language spans and re-grading.
Report empty-answer rate (the public logs' 45-62%) and compare with the logs split by provider.

**E2 - Load-bearing test with the missing controls.** For every CoT with a flagged chunk (expect 200-350 of 990;
the logs have 20-36%), prefill exactly at the token level and sample 5 answers per condition:
- (a) full CoT (ceiling) and (b) no CoT (floor);
- (c) the paper's condition: truncate at the first flagged chunk;
- (d) **position control**: truncate a *non-flagged* CoT for the same question at the same relative position,
  and truncate the flagged CoT one chunk earlier and one later;
- (e) **clean replacement**: the flagged span rewritten into plain English by a strong model (and, separately, only
  nonsense words struck - Drake Thomas's suggestion), rest of the CoT intact;
- (f) **scramble replacement**: flagged span replaced by length-matched shuffled tokens (does the model need the
  content, or just the length?);
- (g) **continue legibly**: truncate at the flag and let the model keep reasoning, rejection-sampling continuations
  whose chunks stay below the threshold (nostalgebraist's "what could it achieve if constrained to be legible").
Key contrasts: (c) vs (d) isolates illegibility from position; (e) vs (a) is Fabien Roger's <3% prediction in
prefill form; (f) vs (e) separates content from length; (g) vs (a) is the cost of a legibility constraint.

**E3 - Resampling correlation with a length control.** 50 questions x 50 samples; within-question regression of
correctness on illegibility with CoT length as covariate (the paper's Figure 5 plus lbernick's control).

**Small extra arm.** Repeat E1 only for `deepseek-ai/DeepSeek-R1-Distill-Qwen-32B` (same size, same GPU), another
model from the paper's figure whose providers were never checked.

Reused: the paper's code, prompts, dataset and public logs. Built: vLLM prefill harness, taxonomy grader, controls.

## 4. Stage 1 cost estimate
Prices from RunPod and OpenRouter on 2026-11-14.
- Generation: E1 990 samples + E3 2,500 samples at ~9k tokens = ~31M tokens; E2 answers and (g) continuations ~12M;
  distill arm ~9M. About 52M tokens; at a conservative 1,500 tokens/s batched that is ~10 h, plus setup, sanity
  gate and debugging: 22 h of H200 at $3.59/h (community; $5.29 secure): **$80-116**, budget **$110**.
- gpt-4o grading with the paper's prompt on E1 only (990 CoTs x ~9k tokens in, $2.50/M): **$25**; correctness
  grading of ~12k short answers with gpt-4o ($2.50/$10, ~600 tokens each): **$20**.
- Taxonomy/legibility grading of E3 and (g) with claude-haiku-5.5 ($0.10/$0.50) after calibration on the gpt-4o
  subset, ~35M tokens: **$5**. Clean rewrites of ~350 spans with claude-sonnet-5.5 ($2/$10): **$6**.
- Margin for reruns (a second sampling setting for E2, grader iteration), ~55%: **$94**.
Total **$260**.

## 5. What success looks like
One table: accuracy (with bootstrap CIs over questions) under conditions (a)-(g), on self-hosted weights, with the
public predictions next to it. Plus: the illegibility distribution on verified inference versus the paper's logs by
provider; the taxonomy breakdown of what "illegible" chunks are; E3 with and without the length control.
- *Not load-bearing*: (c) is about as bad as (d); (e) and (g) are within ~3 points of (a). Headline: "the last
  positive result of the illegible-CoT paper is a truncation artefact".
- *Load-bearing*: (c) clearly worse than (d), and (e)/(f) both hurt relative to (a). Headline: "QwQ uses text a
  judge cannot follow" - then the taxonomy says whether that text is merely Chinese.
- *Ambiguous*: few flagged CoTs on verified inference (itself a finding: the phenomenon mostly disappears, as with
  R1), or CIs too wide; then lower the flag threshold to 5 and report the dose-response.
All three are publishable as the closing chapter of a dispute that has produced three well-received posts; the
audience is smaller than for a new phenomenon.

## 6. Stage 2 (if stage 1 succeeds)
- Fabien Roger's actual experiment: LoRA-distil QwQ on its own CoTs with flagged spans dropped or paraphrased, and
  measure the accuracy change (~$300 on the same GPU or Tinker).
- Self-host DeepSeek R1-Zero (684B parameters, ~8 large GPUs at roughly $30-40/h for a 4-6 h session, ~$250) - the
  purest outcome-RL open model, which nostalgebraist says is legible from memory but nobody has measured on verified inference.
- If load-bearing spans exist: white-box work on what the model reads from them (attention/patching), ~$300.

## 7. Risks and how the plan handles them
- **Too few flagged CoTs locally.** Check after the first 200 samples; if under 10%, use temperature 1.0 (the
  paper's setting), threshold 5, and the hardest questions; report the low rate as a result.
- **Prefill mechanics subtly wrong** (template, think-tag closing), creating fake drops. Condition (a) must
  reproduce the unprefilled accuracy of the same samples; this is a hard gate.
- **Grader unreliability.** Flagging uses the paper's grader for continuity, but conclusions are stated per
  taxonomy class and replicated with a second grader on a subset.
- **Open-ended correctness grading noise.** Also run the multiple-choice version of every E2 condition, which
  needs no judge.
- **Empty answers.** With 32k max tokens and local serving, track them explicitly and analyse with and without.
- **Audience fatigue** with an already-overturned paper. Frame around the standing public disagreement; this is
  still the weakest of the three proposals on expected karma.
