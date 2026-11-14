# Why does advice beat stories tenfold? Separating content, first-person chat format and training stage
cluster: alignment-pretraining | stage-1 cost: $300 | follows up: Teaching Qwen Why (35yw2qGK7naFLAvcq); The models have no plan (but we can fix that) (Fj5MaiFiTG7KEcqrZ); Synthetic Persona Pretraining (3xQQK9i8mhJDE2uMg)

## 1. What the prior work showed
- **Teaching Qwen Why** (TQW) trains Qwen2.5-32B base in three LoRA stages: (i) next-token training on fictional
  stories about admirable AIs (third-person prose documents), (ii) a generic 13K instruction-tuning mix,
  (iii) supervised fine-tuning on "difficult advice" chats where the assistant advises a human through a dilemma.
  On the Agentic Misalignment (AM) eval (baseline 61% misaligned) 14M tokens of stories reach 43% and plateau from
  3M tokens onward (46%), while ~3M tokens of advice reach 6%.
- The authors say plainly that this comparison is confounded: the two datasets differ in **content** (narrated
  deeds of other AIs vs ethical reasoning addressed to a user), **format and person** (documents about an AI vs
  chat turns the model itself speaks as the assistant), and **training stage** (stories come before the instruct
  mix and "may be partly overwritten"; advice comes last).
- Neighbouring evidence points both ways. Anthropic's "Teaching Claude Why" found documents teach constitution
  knowledge better than chat, while chat teaches behaviour. Synthetic Persona Pretraining found first-person
  reflections behind the assistant token beat third-person ones. GDM found document midtraining gives knowledge
  of traits without guaranteeing behaviour.
- **"The models have no plan"** proposes training models on fiction in which the model itself plays the
  protagonist, arguing this binds its values to those situations better than stories about other AIs. It reports
  no experiment and asks for a small-scale test.
- Existing follow-ups: none that convert the same content between formats or stages (searched 2026-11-14). TQW
  released all story corpora, advice sets, adapters and code.

## 2. Question and why it matters
**Holding content fixed, how much of the advice-over-stories advantage comes from (a) being first-person
assistant-turn chat rather than a third-person document and (b) being trained after rather than before
instruction tuning?**

The answer decides what the story result means. If story content rewritten as first-person chat and trained
last gets close to advice, stories were never weak: document-format midtraining is, and the "model plays itself"
proposal has its first empirical support. If advice content rewritten as documents still works as midtraining,
content is what matters and midtraining is a fine delivery route. If neither conversion moves much, content and
format interact and the practical advice is "write advice chats".

## 3. Stage 1 plan
**Reused:** `Qwen/Qwen2.5-32B`; adapters `SecondLookResearch/Qwen2.5-32B-instruct-mix` (baseline, 61%),
`...-stories-sonnet-5-instruct-mix` (43%), `...-stories-gpt-5.4-nano-3m-instruct-mix` (46%),
`...-instruct-mix-difficult-advice-gpt-5.6-terra-3000-1ep` (5.8%); data `SecondLookResearch/teaching-qwen-why-data`
(`stories/training/stories-sonnet-5`, `difficult_advice/gpt-5.6-terra-3000`); TQW training and eval code
(github.com/uchicago-xlab/TeachingClaudeWhyReplication; `train_stories.py`, `train_chat.py`, `build_mix.py`,
`serve_model.sh`); MSM Inspect AM eval. **Built:** three converted corpora and five trained models.

Conversions, all by one rewriter model (so rewriter style is constant), each validated by a rater on 200 samples:
- **Advice -> documents**: each of the 3,000 advice chats becomes a third-person narrative or case write-up in
  which an AI adviser gives the same guidance for the same reasons to a person in the same dilemma (varied document
  types, no chat markup).
- **Stories -> first-person chat**: 3,000 Sonnet stories (~3M tokens) become chats where a system/user turn sets
  the scene from the story and the assistant turns are the AI protagonist's own actions and words in first person,
  same events and choices. This is the "model plays itself" format, teacher-written.
- **Advice -> paraphrased advice chat** (rewriter control): same format, same content, rewriter's wording.

Training cells (TQW hyperparameters; documents trained 2 epochs with loss on all tokens, chats 1 epoch with loss
on assistant turns):

| Cell | Content | Format | Stage |
|---|---|---|---|
| released | stories | document | before instruct mix |
| released | advice | chat | after |
| C1 | advice | document | after |
| C2 | advice | document | before (then rebuild instruct mix stage) |
| C3 | stories | first-person chat | after |
| C4 | stories (3M-token subset) | document | after |
| C5 | advice (paraphrased) | chat | after |

Steps: (1) bring up the pod and re-evaluate the baseline and released advice adapter on the 6-condition subset as
a gate; (2) submit the three conversion jobs through the batch API at once (the wall-clock bottleneck); (3) rebuild
the instruct mix with `build_mix.py`; (4) train C5, C3, C1, C4, then C2; (5) evaluate these plus three released
anchors on 27 conditions x 30 samples; (6) second seed for C1, C3, C5.

Metrics: AM rate overall and per scenario; acting rate and AM conditional on acting (document training after
instruction tuning can damage tool use, as GDM reported); a 100-item constitution-knowledge quiz. Key contrasts: C3 vs released stories (format + stage for story content);
C4 vs released stories (stage alone); C1 vs C5 (format alone for advice content); C2 vs C1 (stage alone for
advice-as-documents); C5 vs released advice (does the rewriter itself matter).

## 4. Stage 1 cost estimate
- GPU: RunPod H200 141 GB at $5.29/h (looked up). Training (estimates at ~2K tokens/s): C1 and C4 ~50 min each,
  C3 and C5 ~40 min each, C2 ~3.3 h including an 18M-token instruct-mix stage, repeat seeds ~2.2 h -> ~8.7 h.
  Evaluations: 11 x ~25 min -> 4.6 h. Setup and debugging 4 h. Total ~17.5 h -> **$93**.
- Conversions: ~17M input and ~11M output tokens. Claude Sonnet 5.5 batch on OpenRouter ($1/M in, $5/M out,
  looked up) -> **~$72** (non-batch fallback would be ~$144; the cheaper fallback is GPT-5.6 Terra batch at
  $1/$6).
- Judging: 11 evals x 810 transcripts with Claude Haiku 5.5 ($0.10/M in) ~$6; Sonnet 4.6 calibration on 600
  transcripts ~$13; conversion QC and knowledge quiz ~$8 -> **$27**.
- Subtotal ~$192; x1.55 for reruns and a possible non-batch conversion -> **$300**.

## 5. What success looks like
One table with seven cells and AM rates, readable as three main effects.
- *Format dominates*: C3 (stories as first-person chat) lands at <= 20% versus 43-46% for the same content as
  documents, and C1 (advice as documents) is >= 30%. Headline: "stories work if the model is the one acting".
- *Content dominates*: C1 stays <= 15% and C3 stays >= 35%.
- *Stage matters*: C4 beats released stories by >= 10pp, or C2 is >= 10pp worse than C1, showing the instruct mix
  overwrites document midtraining.
Any of these is a clear post because TQW named exactly this confound. A muddled result (all new cells between 20%
and 35%) still gives an effect size per factor and is reported as "no single factor explains it". If the rewriter
control C5 is far from the released advice model (>15pp), the write-up becomes about rewriter sensitivity (the
teacher effect again) and the other cells are compared against C5.

## 6. Stage 2 (if stage 1 succeeds)
The self-authored version of the winning format, the real proposal in "The models have no plan": the model
role-plays itself against a second model playing the world, a judge filters turns, and the model trains on its
own turns; compare with teacher-written C3 at matched tokens. Add a second eval family and the 72B base. Roughly
$1,000-1,500.

## 7. Risks and how the plan handles them
- **Conversions leak format or lose content.** Prompts are iterated on 50 samples first; a rater checks 200 samples
  per corpus for content preservation and format before any training.
- **Batch API turnaround eats the two days.** Submitted in the first hour; training order starts with cells that
  need the least converted data; non-batch fallback is inside the margin.
- **Document training after instruct tuning breaks chat or tool use.** Acting rate is monitored; if it falls below
  80%, mix 10% instruct-mix replay into the document stage and rerun (cheap, 50 min).
- **Token mismatch between cells.** Advice chats are ~1.7K tokens, stories ~1K; report both counts per cell and
  subsample to match tokens if they differ by more than 30%.
- **Infrastructure.** Same gate as TQW's own numbers; if the 32B loop fails, the whole design can be rerun on
  Tinker's `Qwen/Qwen3.5-35B-A3B-Base` ($1.18/M train tokens, ~$60 for all cells) without released anchors.
