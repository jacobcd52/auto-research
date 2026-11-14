# Does capability parity certify a monitor? Two open-weight trusted monitors across provider endpoints, paired against self-hosted references
cluster: cot-legibility | stage-1 cost: $350 | follows up: Not Pinning Your OpenRouter Provider Might Invalidate Your Research (KsyoSAyBRXtwzSugg); R1 CoT illegibility revisited (jHnZzicKzczkCCArK)

## 1. What the prior work showed
nostalgebraist re-ran a NeurIPS 2025 CoT-illegibility experiment on DeepSeek R1 with a different OpenRouter provider
(Novita instead of Targon): mean illegibility fell from 4.30 to 2.28 and the paper's author conceded. Matthew
Khoriaty's post (116 karma) generalised this into a warning that unpinned OpenRouter routing can invalidate safety
research, with almost no measurements; its top comment (Tim Hua, 66 karma) criticised exactly that.

Since then the *capability* side has been measured. Artificial Analysis launched an Endpoint Accuracy Index on
2026-08-04 (https://artificialanalysis.ai/articles/endpoint-accuracy-index): each serverless endpoint against a
self-hosted reference, with 95% CIs, on tool calling (BFCL-500), reasoning (HLE-250) and long-context recall. For
gpt-oss-120b most endpoints are "within reference"; the ones below have mundane published causes (output caps,
tool-call formatting, fewer reasoning tokens). OpenRouter publishes its own per-endpoint benchmark numbers and says
it is building logprob verification. Earlier: "The Silent Hyperparameter" (arXiv 2605.19537, backends shift
capability benchmarks by up to 16.6 points) and "Model Equality Testing" (arXiv 2410.20247, 11 of 31 Llama endpoints
differed from reference).

What is open is the question Khoriaty himself raised on 2026-10-09 when he flagged the index: it "only evaluate[s]
on a few 'capabilities' tasks. I suspect its scores may break down on other kinds of evaluations", citing "Accuracy
is Not All You Need" (arXiv 2407.09141: compressed models change behaviour while benchmark accuracy is preserved),
and he advises safety researchers to stay on their own hardware. Nobody has tested that for a safety metric
(checked today: arXiv keyword queries, LessWrong posts since July, the AA and OpenRouter pages; no general web search
this round, and GitHub was unreachable, so coverage is incomplete). The index also does not cover Gemma-4-31B.

## 2. Question and why it matters
**When an endpoint is at capability parity with the reference, are its trusted-monitor suspicion scores also at
parity - in particular the honest-score tail that sets the audit threshold?** Monitoring is the safety use where
open-weight models on OpenRouter matter most, and a monitor's operating point depends on a 1-2% tail that a
capability average would not reveal. "Yes, within a stated margin" lets control researchers use the index to pick
endpoints instead of renting GPUs; "no" shows the index is not enough for safety work. A second model, where
providers really do serve different quantisations, tests the mechanism the parent post worried about, with a local
4-bit arm showing what quantisation alone does.

## 3. Stage 1 plan
**Task (reused).** Per-action suspicion scoring on `anonymouslinuxarena/linuxarena-public` (CC-BY-4.0; 22,215
trajectories, 172 runs, 10 environments), which ships full action content and published per-action monitor scores
with reasoning (e.g. `gpt-5-nano-2025-08-07`). Monitor prompt and score parsing come from Control Tower
(https://github.com/linuxarena/control-tower). Fixed item set, built once: **4,000 honest actions** from >= 400
honest trajectories (stratified by environment and agent model) and **600 attack actions** from >= 150 attack
trajectories, chosen as each trajectory's highest-scored actions under the published monitor so they are plausibly
the incriminating steps. History truncated to 8k tokens identically for every arm.

**Models and endpoints (pinned, `allow_fallbacks:false`, provider logged per response).**
- `openai/gpt-oss-120b` (26 OpenRouter endpoints; native MXFP4, so little quantisation variation): 8 endpoints
  chosen from the AA index - 4 "within reference", every "below reference" endpoint reachable on OpenRouter, and
  Cerebras - plus default unpinned routing.
- `google/gemma-4-31b-it` (18 endpoints today: fp4 x6, fp8 x5, bf16 x2, unknown x5; not in the AA index; bf16
  weights fit one 80 GB GPU): 8 endpoints spanning the labels, plus unpinned routing.

**References (RunPod H100).** Official weights on vLLM, prompt rendered identically (for gpt-oss, the same Harmony
system message and reasoning effort; AA's published launch arguments as a cross-check). Gemma also runs locally
under a second backend and in **4-bit and 8-bit quantisation**: a positive control and a yardstick ("endpoint X
differs from reference as much as local 4-bit does").

**Gates before the sweep.** (a) Harness reproduces the published gpt-5-nano score distribution on 300 actions.
(b) On a 300-action pilot, the gpt-oss reference and two AA-"within reference" endpoints agree on mean score and
reasoning tokens per item within duplicate-run noise; if not, the bug is assumed to be ours. (c) Scores are not
degenerate (honest and attack distributions separate; fewer than 2% parse failures).

**Runs.** One full pass per endpoint; repeat passes on a fixed 1,000-action subset the same day and 24 h later
(noise and drift); reference run twice in full; unpinned routing three times on the subset.

**Pre-registered analysis** (written before the sweep; trajectory-clustered bootstrap throughout).
1. Primary, paired and label-free: per-action score difference from reference on identical inputs; mean shift with
   CI, equivalence margin 0.1 reference standard deviations; rank agreement and distribution distance against the
   reference-vs-reference floor.
2. Operating point: the reference's 2% honest threshold (80 of 4,000 actions) applied to each endpoint; realised
   audit rate with CI, equivalence if within 1.5x either way; catch rate on the 600 attack actions at that threshold.
3. Mechanics per endpoint: parse failures, truncation, reasoning tokens, ignored parameters.
4. Agreement with the AA index (descriptive at n = 8), and for Gemma, deviation by labelled quantisation against the
   local 4-/8-bit arms.

Steps: item set and harness; gates; references; sweeps; repeats; analysis; release of all transcripts.

## 4. Stage 1 cost estimate
OpenRouter and RunPod prices on 2026-11-14. A full pass is 4,600 actions, about 32M input and 1.5-2.3M output tokens.
- gpt-oss-120b, 8 endpoints ($0.03-0.35/M in, $0.075-0.95 out; chosen set averages about $0.13/$0.55):
  ~$5.50 per pass, worst (Cerebras) ~$13: **$50**. Subset repeats and unpinned runs: **$26**.
- Gemma-4-31B, 8 endpoints ($0.10-0.38 in, $0.32-1.15 out; about $0.15/$0.45): ~$5.50 per pass: **$44**; repeats
  and unpinned: **$22**.
- Harness validation with gpt-5-nano (about 2.5M tokens) and pilots: **$23**.
- H100 80 GB at $2.89/h: gpt-oss reference 18 h (setup, two full passes, cross-check) **$52**; Gemma 16 h (bf16
  twice, second backend, 4-bit and 8-bit arms) **$46**; storage **$5**.
- Margin for rate limits and reruns (~30%): **$82**.
Total **$350**.

## 5. What success looks like
One figure per model: each endpoint's paired score shift and realised audit rate at the reference threshold, with
CIs, against the reference-vs-reference band and (Gemma) the local 4-/8-bit arms; a table of AA status against
monitor status; diagnosed causes for any outlier; released harness and logs.
- Positive: an endpoint at capability parity whose audit rate at the reference threshold is outside 1.5x, or an
  fp4-labelled Gemma endpoint that deviates more than local 4-bit. That supports Khoriaty's caution with data.
- Negative: all capability-parity endpoints equivalent within the pre-registered margins. With 4,000 honest actions
  this is a defensible statement, scoped to these two models and this task, and it tells control researchers the
  index is usable for monitor work.
- Ambiguous: deviations that trace only to output caps or reasoning-effort handling already documented by AA; this
  would be reported as "the index's known causes are the whole story here".
My forecast: about 30% positive, 40% clean negative, 30% ambiguous or partial. A clean negative probably earns
30-50 karma; only the positive clearly exceeds 50.

## 6. Stage 2 (if stage 1 succeeds)
- Re-run one published control result end to end (agent plus monitor) on a parity endpoint and a deviating one to
  see whether safety/usefulness conclusions move (~$400).
- Extend to the models where the original worry lives (DeepSeek, Kimi, GLM) using AA's reference recipes on rented
  multi-GPU nodes, or endpoint-vs-endpoint equality tests without a reference (~$400).
- Other safety metrics piloted to sit off ceiling: borderline-refusal rates, sandbagging and eval-awareness
  propensities (~$200).

## 7. Risks and how the plan handles them
- **Reference misconfigured, misattributed to providers.** Gate (b); AA's launch arguments; claims only beyond the
  reference-vs-reference and second-backend bands.
- **Control Tower prompt or data schema harder to reuse than expected** (GitHub was unreachable for me; the dataset
  card says code is released). Gate (a) catches a wrong prompt; fallback is a prompt reconstructed from the published
  monitor reasoning, stated as such.
- **Score ties at the threshold** (coarse integer scores). Report the audit rate at each attainable threshold near
  2% and use the mean of three samples per action on the subset for a finer scale.
- **Reference throughput.** If a full pass exceeds 4 GPU-hours, the second reference pass drops to a 1,600-action subset.
- **Endpoints down or rejecting parameters** (Google showed 0% uptime today). Substitute from the same AA category;
  report coverage.
- **Result is narrow.** Stated plainly: two models, one monitoring task, one week in November 2026.

## 8. Response to feedback
Verdict accepted: this is an overhaul. I re-checked the disputed facts today.
- **Missed prior work: the reviewer is right.** The AA Endpoint Accuracy Index exists, covers gpt-oss-120b against a
  self-hosted reference, and Khoriaty's 2026-10-09 comment flags it and poses the safety-metric question. My v1
  novelty claim was wrong. The proposal is now framed as a test of that index on a safety metric.
- **Label counts: reviewer right** (fp4 x11, fp8 x3, bf16 x3, int4 x1, fp16 x1, unknown x7); my v1 numbers were off.
- **Monitor eval underpowered: accepted.** Replaced the 373-row BashArena set with 4,000 honest and 600 selected
  attack actions from LinuxArena; primary metric is now paired and label-free; trajectory-clustered bootstrap;
  equivalence margins fixed in advance. Threshold transfer between arbitrary endpoint pairs is dropped in favour of
  reference-threshold audit rate.
- **Second model with real quantisation variation: accepted.** Gemma-4-31B (18 endpoints, mixed labels, single-GPU
  bf16 reference) with local 4-/8-bit arms. This replaces the ill-posed quantisation-label regression on gpt-oss.
- **Cut:** CoT-legibility grading, GPQA, refusal set, gpt-oss-20b, Llama stretch, price regression, the logprob
  fingerprint, the 26-endpoint breadth sweep and the all-endpoint 24 h repeat (drift repeat is now a subset).
- **Reference validation gate and backend choice: accepted**, adapted to the monitor task instead of GPQA.
- **Partly rejected: "make the published-result re-run the stage-1 core."** I could not identify a specific
  published safety number that used gpt-oss-120b unpinned (the LinuxArena site lists the model among its runs, but I
  could not inspect them), and a full agent-plus-monitor re-run is the fragile multi-dependency pipeline the
  programme warns about. Stage 1 instead re-scores published trajectories and validates against published monitor
  scores; the end-to-end re-run stays in stage 2.
- **Partly rejected: "a null does not generalise."** True for DeepSeek-class models, and the proposal now says so,
  but adding Gemma-4-31B means the null would cover a model where fp4/fp8/bf16 endpoints really differ.
- I agree with the reviewer's overall ranking: even revised, a clean negative is the most likely single outcome and
  proposals 01 and 03 in this cluster have a higher chance of a >50-karma post.
