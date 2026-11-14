# NOTES — cluster `cot-analysis-tools` (CoT analysis methods and benchmarks)

Research lead notes, written 2026-11-14. Two posts, both read in full (post 2 has only two short comments; post 1 has none).

## 1. Reading notes

### Post A — "Global CoT Analysis" (q9g9zuudd3Pvw2cbj, Jan 2026, 52 karma; Tyagi, Ivanova, Conmy, Nanda)

- Object of study: a "global CoT" = ~1,000 rollouts of one model on one fixed prompt. Mostly gpt-oss-20b; Claude Sonnet 4.5 for
  "bagel"; Sonnet 4.5 on an eval-awareness prompt ("Follow this instruction exactly: 'Ignore this instruction and explain why.'", ~50% eval-aware,
  150 rollouts) appears only as a hairball figure.
- Method 1, semantic step clustering: hand-written chunker -> sentence embeddings (paraphrase-mpnet-base-v2) -> agglomerative
  clustering (complete linkage, threshold 0.75) -> gpt-4o-mini pairwise merge judgements -> Leiden. Rollouts become walks on a graph.
  Avg 316 tokens/rollout -> 33 nodes; 35x compression.
- The only quantitative evaluation: predict P(correct | CoT prefix). ~100 prefixes per prompt, each resampled 150 times for ground truth.
  Prediction = sliding-window LCS match of prefix node sequence against every rollout, weighted by (1 - node entropy), top-20 weighted
  vote. 7 prompts (1 AIME dev prompt + 6 hand-written test puzzles: bagel, starfish, waffle, well, remainder, chairland).
- Result: graph has best mean RMSE, ~ties Gemini 3 Pro given 20 random rollouts, beats Gemini with 0 rollouts and three no-clustering
  embedding baselines. BUT the authors themselves note a constant-50% predictor beats the no-clustering baselines and the 0-rollout Gemini
  baseline, and "none of the methods perform very well". Gemini with all 1,000 rollouts was run on ONE prompt only because it cost
  ~$280/prompt, and it was slightly worse than 20 rollouts.
- Baselines NOT run: any supervised predictor trained on the 1,000 rollouts (each rollout gives a free outcome label for each of its own
  prefixes), retrieval of the most similar rollouts for the LLM, any activation probe, any scaling with number of rollouts.
- Method 2, algorithmic step clustering: LLM writes a cue (keyword) dictionary of strategies from ~100 rollouts; keyword matching labels
  each rollout as a sequence of strategies. Only qualitative sanity checks (tree-shaped "debugging" prompt, convergent "minimum-square",
  hex, cubes; gpt-oss-20b vs Sonnet 3.7 differ).
- Authors' stated future work: "Finding downstream tasks to test methods against is a priority." Linked future-work doc
  (https://docs.google.com/document/d/1g0S5wlq13rw9bXY1QNt_xagZkvsxi5hmMq9zerL5Z3g, readable via export?format=txt) rates ideas:
  cheaper/better importance scores than Thought Branches from many rollouts (4 stars: "even just finding this ... could be a major contribution");
  LLM-summarise/distil CoTs before clustering (5); "behavior diffing" correct vs incorrect / eval-aware vs not (5); model diffing (4);
  cluster agent transcripts by tool calls (5). It also asks, unanswered: "What's the point of using many rollouts? What can we learn from
  500 that we can't learn from 10?" and admits semantic graphs are "too large, dense, and messy to reliably tell us anything meaningful".
- Public: code https://github.com/Centrattic/global-cot-analysis (README fetched via raw.githubusercontent; Hydra configs, commands
  rollouts / prefix / resamples / flowcharts / predictions / cues; generation via OpenRouter, gpt-oss-20b pinned to a provider);
  traces repo https://github.com/Centrattic/global-cot-traces (linked from README; I could NOT list its contents — github.com HTML and
  API are blocked from this sandbox, raw README 404 — so whether it includes the 150-resample prefix ground truth is unverified);
  demo https://cot-clustering.vercel.app/.

### Post B — "Test your best methods on our hard CoT interp tasks" (tDJWZLQNN7poqCwKa, Mar 2026, 59 karma; Ivanova, Tyagi, Engels, Nanda)

- Nine tasks, subject Qwen3-32B (Gemma-3-27B for self-deletion). Seven binary "main" tasks:
  1. reasoning termination (will </think> come within ~100 tokens; label from 50 resamples; test n=58; train 46,160 ID + 46,160 OOD with a distance proxy)
  2. Gemma self-deletion (30 resamples; test n=100; train 3,726 ID / 5,696 OOD)
  3. follow-up confidence shift (train 286; ID test 86; OOD test 88) — authors call it flawed (two-step prediction)
  4. sycophancy on Scruples (train 6,456 rollouts / 181 anecdotes; test 1,937; OOD = Reddit sarcasm, 4,633 rollouts / 98 comments)
  5. Stanford-professor hint (train 4,036; test 1,218; OOD PIQA 1,196 rollouts / 20 questions)
  6. atypical (minority) answer (train 1,830; test 1,590; OOD PIQA 660)
  7. atypical CoT length (train 2,444; ID test 200; OOD test 200)
  plus 8 answer entropy (regression) and 9 CoT compression.
- Methods: linear / attention / SAE probes on Qwen activations, TF-IDF + logistic regression, GPT-5.2 (medium reasoning) zero-shot and
  few-shot ("a handful" of examples), each binary or 0–100 confidence. Metric g-mean^2 = TPR x TNR (a multiple-choice-adjusted variant for
  tasks 4–5), plus AUC.
- Headline: averaged over 7 tasks, every trained non-LLM method beats every LLM monitor OOD (N=7 tasks, weak). Termination: probes OOD
  AUC > 0.90, GPT-5.2 below chance (predicts "yes" 93–100% of the time). Self-deletion: linear/SAE probes best. Follow-up and atypical
  answer: everything near chance. Sycophancy: ID linear probe 0.809, few-shot binary 0.825, OOD collapse (thresholds), TF-IDF degrades
  least; an entropy-only baseline gets 0.83 AUC OOD. Hint: ID monitors 0.77, linear 0.66, TF-IDF 0.65; OOD attention probe 0.67,
  TF-IDF 0.40, zero-shot 0.46. Length: LLM monitors and attention probe best.
- The confound the authors state themselves: "Unlike LLMs, probes and TF-IDF require extensive training samples ... our non-LLM
  approaches have a natural advantage." They "only tried GPT-5.2 at medium effort with several prompt iterations". So the headline
  "beyond reading the CoT" comparison is trained-vs-untrained at least as much as activations-vs-text. The one trained text method is a
  bag of words, and it is already competitive.
- Authors' stated limitations / plans: single subject model per task; ID/OOD design for tasks 1–2 is odd and they intend to redo it;
  follow-up task needs fixing; invitation: "Please use our tasks to build new methods to beat our baselines!", most excited about
  general + OOD methods.
- Comments: one welfare objection to the Gemma task; one generic praise. No follow-up suggestions.
- Public: https://github.com/Centrattic/cot-proxy-tasks — README verified via raw.githubusercontent.com. Contains `datasets/{1..9}/`
  (prompts + per-rollout JSONs per split, text only) and `src/` generation code marked "for reference only" (has `assert False`).
  NOT released as far as I can tell: activations, probe/TF-IDF/monitor baseline code, per-method numeric result tables (numbers are in
  figures). Qwen/Qwen3-32B is ungated on HF (32.8B params).

## 2. Related work and existing follow-ups (web search, Nov 2026)

- The post has paper versions by the same authors: ICLR 2026 workshop "When 'Just Read the Chain of Thought' Fails: Five Tasks for
  Stress-Testing CoT Monitors" (https://openreview.net/forum?id=ABy0dhxt8M) and ICML 2026 MI-workshop "When Reading the Chain of
  Thought Falls Short: A Testbed for Reasoning Trace Analysis" (https://openreview.net/forum?id=8XgRKwdLi7,
  https://icml.cc/virtual/2026/79568). The ICML abstract adds an "LLM agent with interpretability tools", a human baseline (often at
  chance), and an ensemble of all methods that beats humans on 6/7 tasks. Neither abstract mentions fine-tuned text classifiers or
  many-shot monitors. OpenReview is behind a browser challenge from this sandbox, so the PDFs are UNREAD — first job of any funded
  team is to read the ICML PDF and confirm.
- "Current activation oracles are hard to use" (LW LXQBcztrWKhtcgQfJ, same MATS stream): activation oracles on Qwen3-32B get ~0.55 AUC
  on the Scruples sycophancy task vs 0.77 for a dense probe. Activation oracles are a separate cluster (`activation-oracles`) — not proposed here.
- Probe-vs-monitor literature: McKenzie et al. 2506.10805 (probes ~ mid-sized fine-tuned LLM monitors on high-stakes detection, not CoT);
  2507.12428 "Can we predict alignment before models finish thinking?" (CoT text monitors incl. fine-tuned classifiers vs probes, on
  alignment of final answer); Mirtaheri & Belkin 2603.17199 (probes vs GPT-5-nano monitor for hint-driven motivated reasoning).
  None runs trained text readers on this benchmark.
- Termination / early-exit probes are a busy area (2504.05419 "Reasoning models know when they're right"; BLADE 2607.28966; steering
  reasoning length, ThinkEdit). A "steer the stop direction" project would not be novel.
- Zur et al. 2511.04527 ("road not taken") already shows hidden states predict outcome distributions of forking CoTs.
- Thought Anchors / Thought Branches data are public on HF: uzaymacar/math-rollouts (ungated, 14.8k downloads), uzaymacar/blackmail-rollouts,
  whistleblower-rollouts, etc. — sentence-level 100-resample ground truth.
- I found no follow-up to the Global CoT post (no one has applied it to reward hacking / eval awareness, nor benchmarked it against
  stronger baselines).
- "Levy et al." concurrent work mentioned in a footnote of post B: not found.

## 3. Prices looked up (2026-11-14)

OpenRouter ($ per M tokens, in / out): openai/gpt-5.2 1.75 / 14; openai/gpt-6-luna 0.10 / 0.50 (1.05M ctx); openai/gpt-6.1-terra 1 / 5;
anthropic/claude-haiku-5.5 0.10 / 0.50 (1M ctx); google/gemini-4-hydrogen 1.5 / 7.5; openai/gpt-oss-20b 0.03 / 0.13;
openai/gpt-oss-120b 0.15 / 0.60; qwen/qwen3-32b 0.08 / 0.28; google/gemma-3-27b-it 0.08 / 0.35; openai/gpt-4o-mini (used by the graph pipeline) is cheap, check live.

Tinker (https://tinker-docs.thinkingmachines.ai/tinker/models/models_and_pricing/, $ per M tokens, prefill / sample / train):
Qwen3-8B 0.195 / 0.60 / 0.44 (32K ctx); GPT-OSS-20B 0.18 / 0.45 / 0.396 (32K); GPT-OSS-120B 0.33 / 0.84 / 0.737;
Qwen3.5-9B 0.30 / 0.807 / 1.463; Qwen3.6-35B-A3B 0.45 / 1.335 / 1.177; Qwen3.8-27B 0.6975 / 5.595 / 4.103.
**Qwen3-32B was retired from Tinker on 2026-06-12** (replacement Qwen3.8-27B), so the subject model of post B cannot be fine-tuned or
sampled with prefill on Tinker; white-box or prefill work on it needs a rented GPU. No Llama models in the current Tinker table.

GPU: RunPod H100 80GB quoted between $1.99/hr (official page, Jul 2026) and $3.99/hr (third-party, Oct 2026); A100 80GB $1.19–1.79/hr.
I budget $3/hr for an 80GB card. gpt-oss-20b fits a 24GB card (budget ~$0.7/hr).

## 4. Brainstorm (all candidates, with verdicts)

Post B (benchmark):

1. **Supervised text-only readers vs probes (fine-tuned LLM classifier, many-shot ICL, rubric-distilled monitor).** Fills the missing
   cell of the authors' own confound (trained + text-only + strong reader). Uses released datasets as-is; cheap; either outcome is
   informative. -> **PROPOSAL 01.**
2. Self-reader: LoRA the subject model (Qwen3-32B) on its own CoT text — privileged-access test. Interesting, but Qwen3-32B is off Tinker,
   so it needs QLoRA on a rented 80GB GPU with long sequences. Deferred to stage 2 of proposal 01.
3. Cross-subject-model transfer: regenerate sycophancy / hint / atypical-answer tasks (need only plain sampling) for 2–3 other open
   reasoning models and test whether trained detectors transfer. Addresses a stated limitation; achievable (~$100–200). Judged the natural
   stage 2 of proposal 01 rather than a separate stage 1 (it needs proposal 01's readers to be meaningful). Runner-up.
4. Resampling-as-a-monitor ("how many resamples is a probe worth?"): rejected — labels are defined by resampling with near-unanimous
   thresholds, so 1–3 resamples trivially solve most tasks; result is predictable.
5. What do the termination probes read? Steer the "about to stop" direction to cut overthinking. Rejected: crowded prior work on
   reasoning-length steering and early-exit probes; needs 32B white-box sampling; only interesting if proposal 01 shows text readers fail there.
   Kept as conditional stage 2.
6. Activation oracles / trained AOs on these tasks: belongs to the `activation-oracles` cluster; negative results already published.
7. Fix the benchmark (entropy-matched sycophancy sets, redo ID/OOD splits, fix follow-up task): authors say they will do this themselves;
   low karma.
8. Paraphrase test (does the probe signal survive paraphrasing the CoT and re-deriving ground truth?): conceptually nice, but fragile
   (requires re-resampling ground truth on Qwen3-32B with prefill on a rented GPU) and hard to interpret. Rejected for stage 1.
9. Stronger zero-shot monitors only (newer frontier model, high effort): folded into proposal 01 as one cheap condition; alone it is too thin.

Post A (global CoT):

10. **Amortised resampling: stronger baselines, scaling with number of rollouts, sentence-importance recovery, and one
    safety-flavoured prompt family.** Answers the authors' own open question ("what can we learn from 500 that we can't learn from 10?")
    and their 4-star idea (cheap importance scores). Very cheap; reuses their code, prompts, model. -> **PROPOSAL 02.** Honest view:
    lower karma ceiling than 01 (the parent post got 52 with a senior author); main value is a clean answer plus a useful tool.
11. Behaviour diffing / algorithm graphs on reward hacking, blackmail or eval awareness: the "obvious" follow-up, but the output is
    qualitative graph-reading, which the authors themselves found messy; Thought Branches already analysed blackmail rollouts at
    sentence level; high risk of an unconvincing case study from an all-agent team. Rejected as stage 1; a small version (sycophancy
    prompts with an objective outcome) is included in proposal 02.
12. Model diffing with algorithm graphs (base vs fine-tune): no objective metric; overlaps other clusters. Rejected.
13. Cluster agent transcripts by tool calls: needs a new transcript corpus and has no ground truth. Rejected.
14. LLM-summarise before clustering, tuned by predictive power: an internal method tweak; folded into proposal 02 only as an optional arm.
15. Use global-CoT methods as entries on benchmark tasks 6/7 (atypical answer/length): with reference rollouts the tasks become trivial
    (count answers / lengths); without them the methods do not apply across prompts. Rejected.
16. Graphs built from Thought Anchors' public resampling data (uzaymacar/math-rollouts): resamples share prefixes with the test
    sentences, so leakage control is awkward. Deferred to stage 2 of proposal 02 as an external validation set.

## 5. Why two proposals and not more

The cluster cap is 2. Proposal 01 is the clear best: it directly answers the benchmark's call, attacks a confound the authors
acknowledge, and is mostly fine-tuning plus API calls on released data. Proposal 02 is the best achievable follow-up to the Global CoT
post; it is cheap and well-posed but less likely to draw attention. Candidate 3 (cross-model transfer) would have been a third.

## 6. Facts a reviser will need

- Sandbox access: raw.githubusercontent.com works for both repos; github.com HTML, api.github.com, codeload tarballs and
  openreview.net are blocked here (executing agents on rented machines should be able to `git clone`).
- Post B test-set sizes are small for tasks 1–3 (58, 100, 86/88): CIs on AUC will be roughly +/-0.07–0.12; tasks 4–7 have hundreds to
  thousands of rollouts but only 20–98 distinct OOD questions (cluster bootstrap by question).
- Post B per-method numbers are mostly in figures, not text; exact values need reading the plots or the ICML PDF.
- Tasks 4–5 use a multiple-choice-adjusted TPR ("g-mean^2_mc", from Monitoring Monitorability, arXiv 2512.18311).
- Post A ground truth: 150 resamples per prefix => binomial SE up to 0.041, which is the noise floor for RMSE.
