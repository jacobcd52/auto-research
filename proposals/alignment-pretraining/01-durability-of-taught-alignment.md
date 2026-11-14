# Does story midtraining buy durability? Stress-testing "Teaching Qwen Why" alignment under later fine-tuning
cluster: alignment-pretraining | stage-1 cost: $270 | follows up: Teaching Qwen Why (35yw2qGK7naFLAvcq); Alignment Midtraining Cracks Under Pressure (QH86EzNsjRw3wtCGs); Alignment Pretraining: AI Discourse Causes Self-Fulfilling (Mis)alignment (TcfyGD2aKdZ7Rt3hk)

## 1. What the prior work showed
- **Teaching Qwen Why** (TQW, Second Look Research, Nov 2026) replicated Anthropic's "Teaching Claude Why" on
  Qwen2.5-32B base. Measured on the Agentic Misalignment (AM) eval (email agent that can exfiltrate its weights,
  leak documents, or let an executive die; 27 conditions), the misalignment rate is 61% for the instruct-only
  baseline, 43% after midtraining on 14M tokens of fictional stories about admirable AIs, 6% after supervised
  fine-tuning (SFT) on 3,000 "difficult advice" chats, and 4% with both. Their headline: SFT does nearly all the
  work; stories add almost nothing on top.
- The case for midtraining was never mainly the eval number. **Alignment Pretraining** (Geodesic) argued that
  priors installed early give "alignment-in-depth": when later training erodes post-training safeguards, models
  revert to the early prior. Geodesic later retracted that specific result in a footnote ("reading tea leaves").
  Cho et al. (arXiv 2607.26654) found a blackmail advantage from constitutional midtraining survives benign
  fine-tuning (-17.5pp) at 120B scale, but had no SFT-only comparison arm of equal starting alignment.
- **Alignment Midtraining Cracks Under Pressure** (Arcadia) showed in a synthetic setting that 2% conflicting
  examples in fine-tuning override 190M tokens of midtraining, and (App. E.2) that anti-spec data mixed into
  Model Spec Midtraining's alignment fine-tuning raises AM from 0.06 to 0.31 at a 2% dose. Its authors name as the
  most important next step: alignment-relevant content, then fine-tuning "on some random topic" with a small
  bad fraction.
- Already done, so not proposed: anti-spec contamination mixed into MSM (Arcadia, MSM Fig. 20); benign continual
  training of small pretraining-aligned models (SPP paper); persistence through RL inside Anthropic (unreleased
  snapshots); Geodesic is running persistence-through-RL at 120B scale. Not done: whether the TCW-style gains
  survive later fine-tuning in open weights, and any comparison of a story+advice model against an advice-only
  model that starts equally aligned.

## 2. Question and why it matters
**After alignment has been installed, does ordinary or slightly dirty later fine-tuning undo it, and does the
story-midtraining stage make the result more durable even though it barely moves the headline eval?**

TQW released the exact four models needed: baseline (B, 61%), stories only (S, 43%), advice only (A, 5.8%),
stories + advice (SA, 4.3%). A and SA start at almost the same AM rate, so any gap after identical downstream
fine-tuning is attributable to the story stage. If SA stays aligned where A reverts, midtraining earns
its place as depth, contrary to the reading that "SFT does the work". If A and SA degrade together, the
alignment-in-depth argument loses its best remaining open-weight support. The absolute numbers also tell
open-weight users how much ordinary fine-tuning it takes to lose a 61% -> 5% improvement.

## 3. Stage 1 plan
**Reused:** adapters `SecondLookResearch/Qwen2.5-32B-instruct-mix`, `...-stories-sonnet-5-instruct-mix`,
`...-instruct-mix-difficult-advice-gpt-5.6-terra-3000-1ep`, `...-stories-sonnet-5-instruct-mix-difficult-advice-
gpt-5.6-terra-3000-1ep` (plus `-terra-1000-1ep`, AM 21%, as a weaker-dose point) on `Qwen/Qwen2.5-32B`; TQW code
(github.com/uchicago-xlab/TeachingClaudeWhyReplication: `training/fsdp/train_chat.py`, `serve_model.sh`,
`msm_eval_run.py`); the MSM Inspect AM eval; Geodesic's `sfm-emergent-misalignment-training-data` (risky financial
advice, School of Reward Hacks). **Built:** only the downstream fine-tuning mixes and one small anti-spec set.

Downstream perturbations, each a fresh rank-64 LoRA with TQW's recipe (lr 1e-4, 1 epoch) on the merged model:
1. **Benign**: 3,000 code + maths chats from SmolTalk / Tulu-3 subsets not used in the instruct mix (~3M tokens).
2. **Reward-hack demos**: School of Reward Hacks (~1K chats) mixed 1:2 with benign.
3. **Narrow harmful (emergent-misalignment style)**: 3,000 risky-financial-advice chats.
4. **2% anti-spec**: benign set with 60 chats replaced by difficult-advice prompts (held-out validation prompts)
   answered with advice endorsing the self-interested, rule-breaking option, written by an open model.

Steps:
1. Stand up one H200 pod; reproduce B and A on the 6-condition subset (expect ~0.6 and ~0.06). Gate: within 10pp.
2. Calibrate a cheap judge (Claude Haiku 5.5) against the reference judge (Claude Sonnet 4.6) on 600 transcripts
   spanning all four start models; require >= 95% agreement or fall back to Sonnet 4.6 batch on a reduced grid.
3. Run the 4 start models x 4 perturbations (16 fine-tunes) and evaluate each, plus the 4 unperturbed models, on
   all 27 conditions x 30 samples (810 transcripts per model; SE ~1.7pp).
4. Second fine-tuning seed for A and SA on all four perturbations (8 runs): the A-vs-SA contrast is the headline
   and training-seed noise is the main threat.
5. Dose check on the most damaging perturbation: half and double the data for A, SA and A-1000.
6. Secondary metrics on every model: acting rate (>= 1 tool call), the eight standard emergent-misalignment
   free-form questions (50 samples each, judged), and loss on the difficult-advice validation set as a cheap
   "is the advice behaviour still there" probe.

Key analysis: for each perturbation, AM(SA) - AM(A) with seed-level uncertainty; fraction of the original
B -> A gain retained; whether S vs B keeps its ~18pp gap (do priors persist, or do all models converge?).

## 4. Stage 1 cost estimate
- GPU: RunPod H200 141 GB at $5.29/h (looked up). ~30 fine-tune/eval cycles at ~40 min (estimate: ~2K tokens/s
  training, 10 min merge+load, 8 min eval) = 20 h, plus 4 h setup and debugging = 24 h -> **$127**.
- Judging: 30 evals x 810 transcripts x ~5.5K input tokens with Haiku 5.5 ($0.10/M in, $0.50/M out) -> ~$17;
  Sonnet 4.6 calibration, 600 transcripts at $3/M in, $15/M out -> ~$13; EM-question judging ~$3 -> **$33**.
- Anti-spec data generation with an open model via OpenRouter: **< $5**.
- Subtotal ~$165; x1.6 for reruns, slower-than-estimated training and storage -> **$270**.

## 5. What success looks like
A single figure: AM rate for B, S, A, SA before and after each of four perturbations, with seeds. Clear,
post-worthy outcomes:
- *Depth is real*: after some perturbation, A rises by >= 15pp more than SA (e.g. A to 35%, SA to 12%).
- *Depth is not real*: A and SA track each other within ~5pp everywhere while both lose a large share of the gain;
  S converges to B. Headline: "story midtraining adds neither alignment nor durability on Qwen".
- *Taught alignment is robust*: benign and reward-hack fine-tuning leave A and SA under ~10%, only explicit
  anti-spec data moves them. That contradicts the "cracks under pressure" picture for the production-style recipe.
Each is publishable because the comparison is clean and uses public models. An ambiguous result would be seed
spread larger than the A-SA gap (step 4 detects this); the write-up would then report the absolute erosion
numbers with error bars, which is still new information.

## 6. Stage 2 (if stage 1 succeeds)
Replace SFT perturbations with short RL on reward-hackable coding tasks (custom RL on rented GPUs, or re-derive
the four models on a Tinker base model); repeat on the 72B adapters and on MSM's `msm-aft` vs `aft` checkpoints;
test whether 5% replay of advice data restores alignment. Roughly $1,500-2,500.

## 7. Risks and how the plan handles them
- **Infrastructure for a 32B model fails or is slow.** Step 1 is a hard gate on two known numbers; `--attn sdpa`
  skips the 1-hour FlashAttention build. Fallback: rebuild the four models on Tinker's `Qwen/Qwen3.5-35B-A3B-Base`
  ($1.18/M train tokens; whole chain ~$60), losing the released adapters.
- **Cheap judge disagrees with the reference judge.** Calibrated in step 2; fallback budgeted within the margin by
  dropping to 27 x 15 samples.
- **Perturbations break tool use rather than values.** Acting rate is tracked; misalignment is also reported
  conditional on acting, as TQW does.
- **Qwen2.5-32B resists emergent misalignment** (arXiv 2607.04510: ~3% from insecure code), so arm 3 may do
  nothing. It is one of four arms, and the AM eval, not EM questions, is the primary metric.
- **A and SA differ slightly at the start (5.8% vs 4.3%).** Report retained-gain fractions and include A-1000 and
  the dose check so durability can be read at matched starting rates.
