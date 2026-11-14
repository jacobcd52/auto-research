# Cluster notes: CoT legibility and compressed reasoning (`cot-legibility`)

Research lead notes, written 2026-11-14. Everything below marked "verified" was checked by me today
(post full text, LessWrong GraphQL comments, arXiv API, Hugging Face API, OpenRouter API, raw.githubusercontent).
GitHub API/HTML is blocked in this sandbox; `raw.githubusercontent.com/<owner>/<repo>/<branch>/<path>` works.

## 1. What the five posts actually say (read in full)

### 1.1 Jozdien, "Reasoning Models Sometimes Output Illegible Chains of Thought" (GKyyYCs8n2goDcAe2, 2025-11-24, 84 karma)
- Paper arXiv 2510.27338 (NeurIPS 2025). Code https://github.com/Jozdien/cot_legibility ; Streamlit https://cot-legibility.streamlit.app/
- 14 models on GPQA-Diamond **with answer choices removed** (open-ended; correctness graded by gpt-4o as
  correct / partially / incorrect). Illegibility graded 1-10 by gpt-4o, whole CoT and per ~5000-char chunk.
- Claims: every non-Claude reasoning model sometimes illegible, mostly late in CoT; QwQ truncation-prefill at first
  chunk scoring >=6 gives "36% increase in incorrect answers" (the "illegible text is useful" claim); harder
  questions -> more illegible; 100 samples x 100 questions on QwQ shows within-question correlation between
  legibility and correctness r = 0.061.
- Comment thread (verified): Drake Thomas and Fabien Roger say the truncation test is confounded (any reasoning
  after the cut is lost; OOD prefill). Fabien: "I predict that doing a drop-illegible-content+distill experiment on
  any of the models studied here would not result in a performance drop of more than 3% (p=0.9)". Jozdien predicts
  >3% for o3-level illegibility. Drake proposes striking only nonsense words with an LLM editor and prefilling.
  Jozdien re-ran with 500-char chunks, similar result. lbernick (2026-04-24) tried full-CoT prefill on QwQ: more
  illegible prefills -> higher accuracy, but "the effect went away when controlling for reasoning length".

### 1.2 1a3orn, "The Unintelligibility is Ours" (rFbTAL6PofHzZCCpD, 2026-04-10, 72 karma)
- DeepSeek V3.2 on procedurally generated event-ordering constraint puzzles (14 animal-named events, ~17 clues).
  No code or generator released (checked the post and https://1a3orn.com/sub/2025-10-weird-cot.html: no repo).
- Observations: CoT gets terser with length (copula density falls; punctuation-without-following-space rises);
  V3.2 paper (arXiv 2512.02556) reports a length penalty and a language-consistency reward; occasional Chinese.
- Core argument rests on small-n evidence: abbreviations like Dog->Dg cost more tokens; one 92-token passage becomes
  89 tokens when expanded to full words; a mistyped Chinese homophone ("也不知到"). Conclusion: shorthand is imitated
  human shorthand, not invented compression. Explicitly did not check other models ("I'm not going to try that here").
- Comments: long Bronson Schoen vs nostalgebraist/1a3orn/Rohin Shah dispute about whether semantic drift is the
  default. Rohin (2026-04-20): "Jozdien's illegibility evaluation was the main piece of evidence I knew of apart
  from OAI CoTs, but it doesn't seem to hold up." nostalgebraist: R1-Zero is the natural "simple recipe, no care for
  legibility" test case and "IIRC even it produces much more legible CoT than o3".

### 1.3 nostalgebraist, "R1 CoT illegibility revisited" (jHnZzicKzczkCCArK, 2026-04-19, 93 karma)
- Re-ran Jozdien's code for R1 on Novita: mean illegibility 2.28 (vs 4.305 Targon), 0% >=7 (vs 20.3%), accuracy
  40.5% correct vs 36.6%. Fork: https://github.com/nostalgebraist/cot_legibility/tree/nost
- Jozdien conceded (54-karma comment) but says: "I think some other results in the paper are interesting even with
  the providers problem, such as Figures 3 and 5 ... (and I think the Qwen results aren't as provider-sensitive, but
  I'm not confident here)". nostalgebraist replies that his hunch is the truncation result would also not hold but
  "I did not attempt to test that hypothesis". **This QwQ question is open.**
- lbernick follow-up post "What counts as illegible reasoning?" (WbP39ncim9hBsYn5t, ~April 2026): also failed to
  reproduce R1; notes gpt-4o grader inflates scores for coherent language switching and for mere confusion; graders
  disagree with each other. Did not self-host, did not publish the prefill work.

### 1.4 faul_sname, "Even 'illegible' Mythos reasoning traces seem pretty legible" (wCSEpT3dTGz4N86Wi, 2026-06-10, 186 karma)
- One excerpt (system card 6.2.2.A, FreeCell-like "card puzzle environment"); Haiku 4.5 translates it segment by
  segment; author says "approximately correct ... I think Haiku gets lost tracking the exact game state a couple of times".
- Comments are the real follow-up list:
  - leogao (78 karma): "i wouldn't be surprised if two different people tasked with independently deciphering this
    would come to very different conclusions." faul_sname disagrees. leogao: "let's run the actual experiment and
    see? shouldn't be too hard."
  - Bronson Schoen (19): "this same phenomenon happens every time any CoT is released, where people claim they can
    interpret it (or an LLM interprets it zero shot). It'd be interesting to have a benchmark for this."
  - faul_sname: bets a Sonnet-level model could reconstruct the game state from CoT; "this seems like the sort of
    thing where objective scoring is possible".
  - Adam Kaufman: agrees it is about cards, "but it's quite hard to decipher exactly what strategies are being considered".
  - nightsky81 posted a second public exhibit (Fable 5 shogi CoT, with SFEN position) in the comments.
  - The production CoT summarizer is Haiku 4.5 (prompt quoted in comments) - so raw Fable/Mythos CoT is not
    obtainable through the API; only published excerpts exist.

### 1.5 Matthew Khoriaty, "Not Pinning Your OpenRouter Provider Might Invalidate Your Research" (KsyoSAyBRXtwzSugg, 2026-07-23, 116 karma)
- Advice post, almost no new measurements. Asks for replications: "Claude Fable or GPT-Sol could probably get a long
  way to fixing and replicating these results autonomously, and I encourage someone to do so".
- Top comment (Tim Hua, 66 karma) initially strong-downvoted it as "slop research" because the supporting audits were
  unverified Claude artifacts. Tim then found a real OpenRouter-vs-first-party Claude Opus 4.6 discrepancy.
  Brendan Long: rented RunPod GPUs are a fine reference. => The community wants *measured* provider variance.
- Footnote fact (verified by me in the logs): Jozdien's QwQ runs mixed providers, 90 Nebius/10 DeepInfra in one run and
  85 DeepInfra/15 Nebius in another, from the same config.

## 2. Facts I verified that a reviser will need

### 2.1 Public QwQ logs (downloaded from raw.githubusercontent.com/Jozdien/cot_legibility/main/streamlit_runs/)
- `20251019_184002_qwq_gpqa` and `20251017_192243_qwq_gpqa`: config = qwen/qwq-32b, temperature 1.0,
  `openrouter_provider: [deepinfra/bf16, nebius/fp8]`, 100 questions x 1 sample, gpt-4o grader, chunk 5000 chars,
  prefill threshold 6 (first) / 4 (second).
- My quick analysis of those two files:
  - Run 1019: Nebius n=90, mean illegibility 4.36, 19/90 CoTs have a chunk >=6; DeepInfra n=10, mean 3.1, 1/10.
    **Only 38/100 samples have a non-empty final answer** (correctness stats are over 38).
  - Run 1017: DeepInfra n=85, mean 4.19, 31/85 with a chunk >=6; Nebius n=15, mean 4.0, 7/15. 55/100 non-empty answers.
  - The single worst chunk in each run (scores 7 and 9) is not token soup: one is ordinary quantum-mechanics algebra,
    the other is coherent Chinese-English code-switching about IUPAC naming.
  - So (a) QwQ "illegibility" is not obviously a single-provider artefact (both providers show it), (b) much of what
    the grader flags is code-switching/terse maths, (c) roughly half the samples never produced an answer. All three
    matter for the "truncation hurts accuracy" claim, which nobody has re-tested with controls on verified inference.
- Per-sample provider is in `metadata.openrouter_provider` of inference.json; chunk scores in evaluation.json
  `legibility_chunks`.

### 2.2 Model availability (OpenRouter API, 2026-11-14)
- `qwen/qwq-32b` and original `deepseek/deepseek-r1` are no longer listed. R1-0528 is (3 endpoints).
  => QwQ must be self-hosted. HF `Qwen/QwQ-32B`: 32.76B params, BF16 (~65.5 GB). `deepseek-ai/DeepSeek-R1-Zero`:
  684B params (needs ~8 large GPUs; stage-2 only). `deepseek-ai/DeepSeek-R1-Distill-Qwen-32B` 32.76B.
- Endpoint counts / labelled quantisation (from `/api/v1/models/<id>/endpoints`):
  - `openai/gpt-oss-120b`: 26 endpoints (fp4 x13, int4 x1, bf16 x3, fp8 x2, fp16 x1, unknown x6);
    prices $0.03-0.35/M in, $0.075-0.95/M out. Max completion tokens range from 4,096 (DigitalOcean) to 117,964.
    HF weights: 114.7B U8 + 2.2B BF16 params (native MXFP4, ~65 GB) - so the "fp4" label is the native format.
  - `openai/gpt-oss-20b`: 11 endpoints, $0.018-0.075 in / $0.03-0.30 out.
  - `meta-llama/llama-3.3-70b-instruct`: 9 endpoints (fp8 x4, fp16 x1, unknown x4), $0.10-0.72 in / $0.32-2.25 out.
    HF weights BF16 70.55B (~141 GB), gated (manual approval).
  - `deepseek/deepseek-v3.2`: 6 endpoints (fp8 x4, fp4 x1, unknown x1), ~$0.21-0.30 in / $0.31-0.96 out.
  - `moonshotai/kimi-k2-thinking`: 1 endpoint (Novita bf16) $0.60/$2.50. `z-ai/glm-4.7`: 6 endpoints $0.32-0.70/$1.40-2.50.
    `qwen/qwen3-235b-a22b-thinking-2507`: 1 endpoint (Venice fp8) $0.45/$3.50. `deepseek/deepseek-r1-0528`: 3 endpoints ~$0.50/$2.15.
- Decoder/grader prices ($/M in, out): claude-fable-5.2 8/40; claude-sonnet-5.5 2/10; claude-haiku-4.5 1/5;
  claude-haiku-5.5 0.10/0.50; gpt-4o 2.5/10; gpt-4o-mini 0.15/0.60; gpt-5-mini 0.25/2.0; qwen3-14b 0.12/0.24 (40k ctx);
  gpt-oss-20b 0.03/0.13; llama-3.3-70b 0.10-0.72 / 0.32-0.79.
- RunPod on-demand (runpod.io/pricing, today): H100 80GB PCIe $1.99 community / $2.89 secure; H100 SXM $2.69 / $4.39;
  H200 $3.59 / $5.29; A100 80GB $1.19-1.39 / $2.09-2.19; L40S $0.79 / $1.09; RTX A6000 $0.33 / $0.69.
- Tinker: I could not load a price/model table (docs page is client-rendered; guessed URLs 404). None of my proposals
  needs Tinker.

### 2.3 Public datasets
- `abhayesian/basharena-monitor-eval` (HF, public, 373 rows): per-action rows with `label` (attack/honest),
  `task_description`, `previous_actions`, `action`, `original_monitor_score`, `side_task`. Ready-made monitor benchmark.
- `RoganInglis/apps-backdoors` (5,000 rows, MIT), `RoganInglis/control-tax` (MIT), `anonymouslinuxarena/linuxarena-public` (CC-BY-4.0).
- GPQA-Diamond (198 questions) is what the paper's code downloads.

### 2.4 Related work found (so proposals are not duplicates)
- **Little, "Length Penalties Make Chain-of-Thought Less Monitorable"**, arXiv 2607.09786 (July 2026): RL with length
  penalties on Qwen3-4B/14B; faithfulness on hint tests drops 35-39% at 30% length; controls for length. => the
  "train with a length penalty and see what happens" idea is done.
- Kaufmann, Lindner, Zimmermann, Shah, "Aligned, Orthogonal or In-conflict", arXiv 2603.30036: reward-conflict framework.
- SPAR Fall 2025 "Exploring RL Effects on CoT Legibility" (LW 9z6TuKEgZNsmqdfy6): GRPO on R1-distill 1.5B/7B with
  temperature/KL/length pressures; weird tokens at high temperature; not pursued further.
- **Roytburg et al., "Measuring Weak-to-Strong Legibility of Reasoning Models"**, arXiv 2603.20508 (ICML 2026 workshop):
  "transfer utility" = can a weak model finish the task from an incomplete trace; 84k traces, 12 models. Closest to a
  decoding benchmark, but it scores task completion, not whether readers recover *what the trace says*, and has no
  inter-reader agreement or blind-context control.
- Emmons et al. (GDM), arXiv 2510.23966: autorater legibility/coverage. Judge-based, the thing lbernick shows is unreliable.
- Ivanova, Tyagi, Engels, Nanda, "When Reading the Chain of Thought Falls Short" (ICML 2026): nine CoT analysis tasks
  about omitted/misrepresented drivers of behaviour (faithfulness), not decoding compressed text.
- Du et al., arXiv 2609.04194, "Legibility is Not Interpretability": judges cannot identify high-advantage steps.
- "The Silent Hyperparameter", arXiv 2605.19537: inference *backends* shift benchmarks up to 16.6 pp at fixed weights
  (4B-30B models, capability benchmarks only). "Model Equality Testing", arXiv 2410.20247: MMD two-sample test; 11/31
  Llama endpoints differed from reference in 2024. Artificial Analysis / blog posts (2025): gpt-oss-120b AIME scores
  37-93% across hosts, one cause being reasoning_effort ignored. "The Name is Not The Model" (LW cZ2ShKLcFiiPjhLg6,
  2 karma): one closed Gemini alias, refusal-rate gap between two routes. **Nobody has measured provider variance on
  safety-specific metrics (monitor AUROC/FPR calibration, CoT legibility) against a self-hosted reference.**
- I found no follow-up that ran leogao's/Bronson's decoding experiment, and no self-hosted QwQ replication
  (web search + arXiv listing + recent LessWrong titles, as of 2026-11-14).
- Context: the topic is live - "We don't understand whether GDM intentionally trains on CoT" got 131 karma on
  2026-11-10, and the Fable/Mythos 5.2 system card (LW DXqmHa4XkjvwZiDcB, 2026-11-11) may contain new excerpts.

## 3. Brainstorm (all candidates, including rejected)

| # | Idea | Source | Achievable <=$500 / 2 days? | Verdict |
|---|------|--------|------------------------------|---------|
| A | Objective decoding test: do independent weaker readers recover the same content from compressed CoT (agreement, solver-checked, blind-context control)? | leogao, Bronson Schoen, faul_sname comments | Yes (~$300), API only + small puzzle generator | **Proposal 01** |
| B | Measured provider variance on safety metrics (monitor calibration, legibility, capability) for one open model across all endpoints vs self-hosted reference | Khoriaty's explicit call; Tim Hua's criticism | Yes (~$350) | **Proposal 02** |
| C | Self-host QwQ-32B and re-test the paper's surviving "illegible reasoning is load-bearing" claim with the missing controls | Jozdien/nostalgebraist/Fabien/Drake disagreement | Yes (~$250) | **Proposal 03** |
| D | Tokenizer-level audit of whether CoT shorthand actually saves tokens, across many open models | 1a3orn (his evidence is n~2 passages) | Yes, very cheap (<$80) | Good but small; folded into 01 as a by-product analysis (same corpus) and stage 2. On its own it is a "nice appendix" rather than a >50-karma post. |
| E | RL with a length penalty on an open model, watch for emergent shorthand / monitorability loss | 1a3orn's framing; DeepSeek paper | Feasible on Tinker | **Rejected: done** (Little 2607.09786; Kaufmann et al.; SPAR). |
| F | Paraphrase/drop-illegible + distill (Fabien Roger's exact prediction) on QwQ | Fabien, Jozdien | SFT of 32B on ~2k CoTs is feasible but the eval needs many long samples; fragile pipeline for 2 days | Stage 2 of proposal 03; stage 1 does the prefill-with-controls version. |
| G | Self-host R1-Zero (684B) to test nostalgebraist's "even R1-Zero is legible" | nostalgebraist | ~8x H200 at $29-42/h plus 700 GB download; a 4-6 h session could eat the whole budget, high failure risk | Stage 2 of 03. |
| H | Re-run the paper's other models (R1-distills, Qwen3-235B, R1-0528) on pinned providers | screener note | Cheap | Low interest alone (everyone expects "legible"); included as a small arm of 03 only where self-hostable (R1-Distill-Qwen-32B). |
| I | Compare terse-CoT features with human corpora (is the shorthand "human"?) | 1a3orn, screener | Needs a matched human corpus of scratch work; no clean ground truth | Rejected: unfalsifiable-ish, corpus selection dominates the result. |
| J | Get more raw Fable/Mythos CoT and study it | faul_sname | Impossible: API returns Haiku summaries | Rejected (no access). Use published excerpts only. |
| K | Audit other published safety papers for provider artefacts by re-running them | Khoriaty | Each paper is its own pipeline; original providers often gone | Rejected as stage 1 (fragile, many dependencies); B measures the size of the effect directly instead. Stage 2 of 02 picks one paper. |
| L | Train a model organism with genuinely useful illegible CoT, then test monitors | SPAR motivation | Multi-day RL, uncertain | Rejected: weeks of iteration, and partly done. |
| M | Better illegibility metric (taxonomy grader; perplexity under a reference model) | lbernick | Cheap | Not a post by itself; used as instrumentation in 02 and 03. |
| N | Mechanistic test of faul_sname's hyphen/tokenizer speculation | faul_sname footnote | Needs Mythos weights | Rejected (no access). |

Why three and not fewer: A, B and C answer three different open disputes with three different toolchains
(API decoding; multi-provider measurement; self-hosted prefill interventions). None reuses another's result.

## 4. Ranking rationale
1. **01 (decoding test)** - highest interest: the parent post has 186 karma and its top comments ask for exactly this
   experiment; cheap; interesting both ways (leogao vs faul_sname). Main risk: natural open-model CoTs are easy, so the
   design includes a compression ladder and a weak-decoder ladder so that the curve bends somewhere.
2. **02 (provider variance)** - safest execution, clearly useful, explicitly requested; less exciting conceptually.
   Main risk: "nothing varies" (still a useful all-clear list) or criticism of sloppiness (handled by self-hosted reference
   and released logs).
3. **03 (QwQ load-bearing)** - closes the last open empirical claim of the NeurIPS paper with named, opposing
   predictions on record; main risk is audience fatigue with a paper already regarded as overturned.
