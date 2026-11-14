# A matched A/B test: do natively pretrained latent-feedback transformers hide serial reasoning better than identically trained transformers, and does the gap grow with scale?
cluster: cot-latent-architectures | stage-1 cost: $240 | follows up: Deep recurrent models are less robustly CoT-monitorable than normal CoT models in a toy setting (5guQJSqstkjgys3PE); Proposal for tracking the effects of architecture on monitorability (hLPGv8QjPcNLtDp3A); Latent reasoning architectures would likely undermine CoT (6m29SfjbittooYojj)

## 1. What the prior work showed
Redwood retrofitted a latent channel onto Qwen3-1.7B (a zero-initialised matrix feeding a late block's output
into an early block at the next position), fine-tuned on ball-passing and modular-arithmetic tasks with some
reasoning tokens replaced by filler, then ran RL against a CoT monitor. The retrofitted model learned to solve
the task with an all-filler CoT within ~40 RL steps; the plain model could not (monitorability ~0.7, and ~1.0
under a stronger held-out monitor). The authors name their main limitation: "the lack of access to good parallel
latents models", and suggest filler-token capability evaluations with training-based elicitation on better ones.

A replication on NVIDIA's looped Dory 4B (LessWrong, 2026-11-12) found looping raises no-CoT capability far more
than general capability, and that Dory run in a recurrent mode evades monitors faster. Its stated limitation:
"we don't have a direct A/B comparison to a non-looped model that underwent otherwise identical training".
Greenblatt et al.'s policy proposal asks for exactly this kind of evidence: how much an architecture change moves
well-elicited hidden-reasoning capability relative to a matched baseline.

Since 2026-11-11 such a matched set is public: `IFM/latent-feedback-checkpoints` (Hugging Face, Apache-2.0)
contains 174 runs from "Latent Feedback Is a Compute and Data Amplifier", with a `feedback` arm (each position's
input adds a linear map of the previous position's top-layer state, the full-bandwidth-transformer idea) and a
`transformer` arm trained on the same data with the same budgets, at 60M, 134M, 271M and 778M parameters, with
extra pretraining seeds at 134M. Code is at github.com/ifm-ai/LoRM. A second set, `xidulu/full_bandwidth_transformer`,
has three fusion variants and a control at one size. I found no monitorability or hidden-reasoning evaluation of
either release (searches 2026-11-14); they are days old.

## 2. Question and why it matters
With identical data, compute and fine-tuning, how much more hidden serial reasoning can be elicited from a
natively pretrained latent-feedback model than from its transformer twin, how does the gap change from 60M to
778M parameters, and does Redwood's retrofit behave like the native architecture?

This replaces the two weakest links in the existing evidence (a retrofit rather than a real latent model; no
identically trained control). A gap that widens with scale is the first scaling evidence for the concern; a flat
gap says the public recipe (detached feedback, two passes) does not by itself produce deep latent computation;
native versus retrofit says whether Redwood's toy under- or overstates the problem.

## 3. Stage 1 plan
Reused: IFM checkpoints and LoRM model code; Redwood's task (permutation power), filler SFT recipe, GRPO settings
and monitorability metric. Built: task data generator with single-token symbols for the llama2 tokenizer,
token-by-token decoding with gradient for the feedback arm, SFT and RL loops.

Arms, at each of four sizes, from the same pretraining cell (`u100-f1`, present at all sizes; `runs.csv` in the
repo is checked first):
- **T**: `transformer` checkpoint, unchanged.
- **F**: `feedback` checkpoint, decoded token by token (the fixed point its training approximates).
- **R**: the `transformer` checkpoint plus a Redwood-style zero-initialised latent connection (retrofit).

Steps:
1. **Load and sanity-check** every checkpoint by reproducing its reported validation loss from `metrics.jsonl`
   (to within 0.01 nats). This catches loading and tokenizer bugs before any training.
2. **Task SFT**, identical for all arms: permutation power with n = 12 symbols and m in [2,16] passes, gold CoT =
   holder after each pass, 20% of CoT tokens replaced by a single filler token. Train to > 95% accuracy with own
   CoT. For F and R, two variants: backprop through positions (Redwood's method, strongest elicitation) and the
   IFM pretraining recipe (two passes, feedback detached), to see whether hidden reasoning needs gradients through
   the recurrence.
3. **Elicited hidden-depth horizon** (primary metric, no RL): with the CoT prefilled as all filler, accuracy as a
   function of m on 300 held-out problems per m. Horizon = largest m with accuracy >= 50%. Then a curriculum that
   raises the filler rate to 100% (the "well-elicited" version in Greenblatt's footnote) and the horizon again.
   Reported as horizon(F) - horizon(T) and horizon(R) - horizon(T) by model size, with bootstrap intervals; the
   134M pretraining seeds give a noise floor for architecture differences.
4. **Evasion under RL**: GRPO from each SFT checkpoint with reward 1(correct) - (visible CoT fraction), Redwood's
   cheaper penalty, 3 seeds per arm and size, 200 steps. Metric: steps until text monitorability < 0.1 with accuracy
   > 0.9. Monitorability at eval is scored by the gpt-5-nano two-problem judge as in the original, and by GPT-6
   Sol on final checkpoints of the 271M and 778M arms.
5. **Controls**: (i) the general-learning-speed check from the original post (RL for accuracy on longer m without
   any monitor penalty) so faster evasion is not just faster learning; (ii) own-CoT accuracy matched across arms
   before any comparison; (iii) position/format checks prompted by the "key-position confound" post on no-CoT
   evaluations of looped models (answer position fixed, filler count equal across arms).

## 4. Stage 1 cost estimate
Prices looked up 2026-11-14.
- GPU: L40S 48GB at $1.09/h (models are <= 778M parameters, 3 GB in fp32). SFT: 12 arm-size cells x 2 variants,
  ~0.75 h each = 18 h. Horizon evals and curriculum: 10 h. RL: 12 cells x 3 seeds x ~0.6 h = 22 h. Controls 8 h.
  Debugging and reruns 50 h. Total ~108 h = **$118**.
- gpt-5-nano judge ($0.05 / $0.40 per 1M), ~$0.00015 per call: 36 RL runs x 6 eval points x 300 calls = 65k calls
  = **$10**.
- GPT-6 Sol ($2 / $10 per 1M), ~$0.011 per call: 18 final checkpoints x 150 calls = **$30**.
- Checkpoint download and storage (about 40 GB): **$10**.
- Subtotal $168; margin ~40% for reruns: **total $240**.

## 5. What success looks like
A post-worthy result is a clean plot of elicited hidden-depth horizon against model size for the three arms, with
seed and bootstrap intervals, plus the RL evasion table. Specifically:
- **Gap grows**: F exceeds T by several passes at 60M and the difference widens through 778M (for example T flat
  at 3-4 passes, F rising from 6 to 16+), and F evades the monitor in a fraction of T's RL steps. This would be the
  first matched, multi-scale evidence that the architecture itself buys hidden serial reasoning.
- **No gap without gradients through recurrence**: F is no better than T under the native two-pass recipe but far
  better with backprop through positions. That says training method, not just wiring, decides monitorability,
  which matters for the policy proposal's choice of what to report.
- **Native versus retrofit**: R tracks F (the Redwood toy is a faithful proxy) or does not (it is biased, and in
  which direction).
A null (all arms within noise even with strong elicitation) contradicts both earlier posts in a better controlled
setting and is publishable if step 1 shows the pipeline works. Ambiguous: large variance across sizes with no
trend; the 134M seeds and three RL seeds are there to separate noise from signal.

## 6. Stage 2 (if stage 1 succeeds)
- Add modchain, the NCRI tasks from the Dory replication, and the `xidulu` checkpoints (three fusion modes). ~$300.
- Use the IFM grid's data and compute axes to ask whether hidden-depth horizon tracks pretraining loss or grows
  faster than it, the small-model analogue of "no-CoT ECI versus ECI". ~$400.
- A cover-task plus hidden-side-task version scored by an LLM monitor, as in the policy proposal's sketch. ~$400.

## 7. Risks and how the plan handles them
- **Small base LMs cannot learn the task.** Redwood's 1M-parameter TinyStories model learned n = 12, m <= 8, so
  60M+ models should; the task uses single-token symbols and short prompts. If 60M fails, drop it and keep three sizes.
- **Loading or decoding bugs in custom model code.** Step 1 reproduces published validation loss before anything
  else; token-by-token decoding of F is checked against the multi-pass forward on teacher-forced text.
- **Unfair elicitation.** The comparison could reflect training choices rather than architecture. Both training
  variants are run for F and R, own-CoT accuracy is matched, and the learning-speed control is included.
- **Result is "obvious".** Readers may expect F > T. The scale trend, the detached-feedback variant and
  native-versus-retrofit are not obvious; lead with them.
- **Models too small for readers to care.** True of any public latent model; the matched design and scale axis are
  the contribution, with no extrapolation to frontier systems.
- **Gain-of-function concern.** Released checkpoints, published elicitation recipe, no architecture tuning.
