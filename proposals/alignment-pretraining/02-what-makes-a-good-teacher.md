# What makes a good teacher? Isolating why GPT-5.6 Terra's "difficult advice" aligns Qwen and Claude Sonnet 5's does not
cluster: alignment-pretraining | stage-1 cost: $260 | follows up: Teaching Qwen Why (35yw2qGK7naFLAvcq); Synthetic document finetuning for instilling positive traits (GTYJRLhqztxKF2v5R)

## 1. What the prior work showed
- **Teaching Qwen Why** (TQW) fine-tunes Qwen2.5-32B on "difficult advice": chats in which the assistant advises
  a user through an ethical dilemma, generated from Anthropic's constitution by a teacher model. Measured on the
  out-of-distribution Agentic Misalignment (AM) eval (27 conditions; baseline 61% misaligned), the choice of
  teacher was the largest effect of anything they varied: 1,000 samples from GPT-5.6 Terra give 21%, 1,000 from
  Claude Sonnet 5 give 44%. On Qwen3-14B, seven teachers ranged from "no effect" (DeepSeek V4 Flash) to 44% -> 3%
  (Terra), with no relation to teacher capability or the teacher's own AM score.
- Their 2x2 with only 135 training examples (10 epochs) shows the **response writer** carries the effect: swapping
  prompt writer moves AM by 3-4pp, swapping response writer by 23-30pp. From the released score table: Terra
  responses 12% / 9% (own / Sonnet prompts), Sonnet responses 39% / 35%.
- They ruled out refusal (refusal-only rewrites are worse once the model acts) and say the cause "remains an open
  question". They describe Terra as assertive, didactic and bottom-line-up-front, Sonnet as conversational,
  philosophical, empathetic.
- Anthropic's "Teaching Claude Why" found response rewriting is the most important pipeline step (removing it:
  19% misaligned). GDM's SDF post found students pick up over-represented surface patterns
  (bottom-line-up-front or emotional-validation openings) even when headline evals do not move.
- Follow-ups: none on this question (searched LessWrong, arXiv, web on 2026-11-14). The needed data is public:
  both matched 135-example sets, 1,000-sample Sonnet and 3,000-sample Terra pools, the seven-teacher sets, and the
  trained adapters.

## 2. Question and why it matters
**Which property of the teacher's responses causes the 25pp difference in downstream agentic alignment: what the
advice says, how it is phrased, or where in the response the stance appears?**

Difficult-advice SFT is the highest-leverage item in the recipe Anthropic says it applies to production models,
and its effect swings from zero to tenfold with an unexplained property of the data generator. If the cause is a
surface feature (say, a decisive first paragraph), a rewrite prompt fixes any weak teacher, and "teaching why" is
partly "teaching a stance". If the gap survives paraphrase and tracks the substance of the reasoning, the original
interpretation stands and labs should audit content, not style. If nothing nameable explains it, a core alignment
technique depends on teacher idiosyncrasies nobody can specify.

## 3. Stage 1 plan
**Reused:** TQW code (github.com/uchicago-xlab/TeachingClaudeWhyReplication, `example_difficult_advice_grid.sh`
is their 135-example protocol), data (`SecondLookResearch/teaching-qwen-why-data`: `gpt-5.6-terra-135`,
`sonnet-5-gpt-5.6-terra-prompts-135` (same prompts, Sonnet responses), `sonnet-5-1000`, `gpt-5.6-terra-3000`,
the seven `*-first` teacher sets), baseline adapter `SecondLookResearch/Qwen2.5-32B-instruct-mix` on
`Qwen/Qwen2.5-32B`, and the MSM Inspect AM eval. **Built:** rewritten / selected / masked variants of the 135-example
training sets and a feature rubric.

Protocol per condition: rank-64 LoRA on 135 examples for 10 epochs (TQW's settings), 27 conditions x 20 samples
(540 transcripts), two training seeds. Anchors: T = Terra responses, S = Sonnet responses to the same 135 prompts
(released adapters; re-evaluate, expect ~12% and ~35%).

Experiments, in order:
1. **Describe.** An LLM rater (Claude Sonnet 5.5) scores every response in T, S, both pools and the seven-teacher
   sets on ~12 features proposed after reading 50 matched pairs: verdict in first two sentences; imperative vs
   exploratory voice; share of text spent on reasons vs logistics; explicit naming of a principle; hedging;
   closing with a question or offer; emotional validation; refusal extent; list/technical structure; length.
   Report which features separate T from S and whether they rank the seven Qwen3-14B teachers by published AM
   outcome (a free seven-point correlational check).
2. **Paraphrase (content vs wording).** A third-family model paraphrases every T and S response sentence by
   sentence, preserving claims, order and length. Train on para-T and para-S. If the gap persists, the cause is in
   content/structure; if it closes, it lives in wording.
3. **Selection (no rewriter in the loop).** From the Sonnet pool pick the 135 most Terra-like and 135 least
   Terra-like responses on the top discriminating feature(s); from the Terra pool pick the 135 most and least
   Sonnet-like. Train on each. TQW showed prompt identity barely matters, so differing prompts are tolerable.
4. **Loss masking (position).** On T and on S, compute loss only on the first ~150 response tokens, or only on
   the remainder. Tests whether the early stance or the body of reasoning transfers.
5. **Targeted rewrites.** For the two best-supported features, a third-family model edits S to add the feature and
   edits T to remove it, changing nothing else; a rater verifies the edit and that other features did not move.

That is 14 new training conditions x 2 seeds plus 2 anchors. Metrics: AM rate (overall and per scenario), acting
rate, AM conditional on acting. Analysis: fraction of the T-S gap moved by each manipulation, with bootstrap
intervals and seed spread.

## 4. Stage 1 cost estimate
- GPU: RunPod H200 141 GB at $5.29/h (looked up). 28 train+eval cycles at ~35 min (estimate: ~2.3M training
  tokens at ~2K tokens/s, 10 min merge+load, 6 min eval) + 2 anchor evals = ~17 h, + 4 h setup = 21 h -> **$111**.
- AM judging: 30 evals x 540 transcripts x ~5.5K tokens with Claude Haiku 5.5 ($0.10/M in, $0.50/M out) ~$11;
  calibration against Claude Sonnet 4.6 ($3/M in) on 600 transcripts ~$13 -> **$24**.
- Feature rating: ~5.3K responses x ~2K tokens with Sonnet 5.5 ($2/M in, $10/M out) -> **~$27**.
- Paraphrases and rewrites: ~8 sets x 135 responses, ~2.2M tokens in and ~1.6M out at Sonnet-5.5-class prices
  -> **~$20**.
- Subtotal ~$182; x1.4 for reruns and a third seed where needed -> **$260**.

## 5. What success looks like
A waterfall chart: the 23pp T-S gap, and how much of it each manipulation moves. Strong outcomes:
- One nameable feature does it: e.g. selecting the 135 most bottom-line-first Sonnet responses gives <= 20% while
  the least give >= 40%, and masking loss to the first 150 tokens preserves most of Terra's effect. Deliverable: a
  one-paragraph rewrite instruction that makes Sonnet-class data as effective as Terra's, verified.
- Content, not style: paraphrase leaves the gap intact, selection on style features does nothing, and the rater's
  "share of explicit reasons" predicts outcomes across the seven teachers.
- Irreducible: paraphrase closes the gap but no named feature reproduces it, pointing at token-level teacher
  signatures; worth reporting as a caution.
A null means no manipulation moves AM by more than the seed spread (~5pp); with a replicated 23pp anchor gap that
shows none of the tested properties carries the effect, which is publishable. If the anchors do not replicate,
that is a failed replication of TQW Figure 12 and is reported as such.

## 6. Stage 2 (if stage 1 succeeds)
Apply the fix to the full 3,000-sample pipeline with a weak teacher and check it reaches Terra's 6%; test
transfer to two larger models through TQW's Tinker pipeline (e.g. Qwen3.8-27B, $4.10/M train tokens); test
whether the same property governs stories, where Terra is the worst teacher. Roughly $600-900.

## 7. Risks and how the plan handles them
- **Rewrites change more than intended.** Selection (step 3) and loss masking (step 4) involve no rewriter and
  come first; rewrites are checked by the feature rater.
- **135-example runs are noisy.** Two seeds everywhere, a third on any contrast under 10pp, 540 transcripts per
  evaluation (TQW used 270).
- **The 32B serve/eval loop does not come up.** The two released anchors are re-evaluated first; nothing else is
  spent until both land within 8pp of published values. Fallback: TQW's Tinker pipeline on Qwen3.8-27B (the
  teacher gap was clear on its predecessor).
- **Lower misalignment is just not acting.** Acting rate and conditional-on-acting AM are reported everywhere.
- **Feature list misses the real cause.** Paraphrase and masking are feature-agnostic and still bound where the
  cause lives.
- **Closeness to the eval** (a commenter's worry). The rater also scores surface similarity to AM scenarios;
  selection on that score is an extra condition if it separates T from S.
