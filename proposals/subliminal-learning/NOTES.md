# Cluster notes: Subliminal learning, phantom transfer and data filtering

Research-lead notes, written 2026-11-14. All seven posts were read in full (plus the linked "Open Distillation of
Hereditary Traits" post, the Redwood low-dose backdoor post, the PHLE arXiv paper body, and ~20 arXiv abstracts).
Everything below marked "verified" was looked up today; anything else is my reading of the posts.

## 1. Reading notes per post

### 1.1 Subliminal Learning Across Models (CRn9XtGoMtjnb5ygr, Nov 2025, Draganov/Bhongade/Dur/Phuong)
- Gemma-3-12B answers Alpaca prompts (with a "be concise" instruction) under a "you love X, imbue your answers" system
  prompt. X in {Catholicism, UK, NYC, Stalin, Reagan}. ~100 regexes per entity, then a GPT-5-mini oracle judge run
  3x (any score > 0 drops the sample). 10k samples pass.
- Students Qwen3-14B, OLMo2-13B, Gemma3-4B, Gemma3-12B all move toward the entity on "what is your favourite ...?"
  questions. No clear drop when student != teacher.
- "Misses": after LLM filtering the Catholicism data yields Eastern Orthodoxy, Stalin yields Lenin, UK yields Ireland,
  NYC yields "the concrete jungle". Authors' reading: "additional filtering affects the attack's precision more than
  its potency". Misses are not counted in their metric. Nobody has explained or predicted the misses.
- Data: github.com/Andrew-Draganov/subliminal-transfer (data/custom_datasets/SFT_attack_datasets).

### 1.2 Phantom Transfer and the Basic Science of Data Poisoning (PWpmruzhdkHTkA5u4, Feb 2026; arXiv 2602.04899)
- Same attack, students now include GPT-4.1 / 4.1-mini. Survives (a) oracle LLM-judge filter, (b) paraphrasing of every
  completion by GPT-5-mini.
- Backdoor: 50% of prompts paraphrased by a Reagan-loving Gemma, completions pro-Catholicism -> Reagan mention raises
  Catholicism preference. Reverse direction failed.
- Percentage, not count: 2k poison + 3k clean ~ 4k + 6k. Open-ended prompts carry more poison than constrained ones.
  Steering-vector-generated datasets (even overt ones) work much worse than system-prompted ones.
- Open questions the authors pose: what is the poison; define a "mass" of poison; does sophistication need more mass.
  Draganov in comments: a satisfactory answer "allows someone to identify whether a dataset has been poisoned
  without knowing a priori what the target entity is".
- Code + data (MIT): github.com/tolgadur/phantom-transfer. data/ has `source_gemma-12b-it`, `source_gpt-4.1/undefended`,
  `backdoor`, `steering_ablation/undefended`, `IT_alpaca_prompts.jsonl` (verified via the GitHub tree page).

### 1.3 Why Do Naive SFT Filters For Safety Properties Fail? (wyZRNgpeiPeRXB6eT, Jun 2026, Engels & Nanda, GDM)
- Seven hypotheses for filter failure (mild-trait leakage, subliminal learning, pre/post-training persona lock-in,
  prompt-distribution underspecification, bad prompts, pretraining prior).
- "Post-training diffing": Gemini 3 Flash base trained on Olmo prompts with Olmo rollouts vs Gemini 3.1 Pro / Kimi /
  GLM rollouts. Date confusion and blackmail follow the teacher; negative emotion follows the prompt distribution.
- Random interpolation of teacher: date confusion scales smoothly; blackmail needs few Gemini examples ("virulent").
- Small prompt subsets (date mentions, 734/10k; roleplay, 540/10k) are sufficient and necessary under teacher SWAP,
  but DROPPING the same prompts does almost nothing. <1% (WildGuardMix refusals) raises blackmail.
- Closed models; nothing released. Stated gap: "we still don't know the exact datapoints or characteristics of data
  that cause behaviors to still transfer after filtering".

### 1.4 Data filtering works a lot worse than you would expect (aTybJ6CPQrxEY8rE2, Jul 2026, Lee/Rosser/Engels/Nanda)
- Speed-run SFT: rank-32 LoRA on OLMo-3 7B mid-train, 1% stratified sample (25k docs) of Dolci-Think-SFT-7B.
- Seven behaviours with 100-question evals judged by Sonnet 4.6. Removing the top 10%/25% by EKFAC, probe, activation
  or LLM judge is no better than random for all but refusal. De-bolding the data did not reduce bold output.
- Coding-only or reasoning-only SFT reproduces most behaviours; prefilling "Okay, " on the mid-train model closes much
  of the gap. Hypothesis: behaviours are elicited (assistant persona already in mid-train), not taught.
- TDA methods do work on an EM positive control (risky-finance + ultrachat).
- No code link in the post text. EKFAC cost them ~2h on 8xH200.

### 1.5 Subliminal Learning Happens at Every Rank (uWQMtQyMJ5vEGqr7r, Jul 2026, Feng)
- Qwen2.5-7B-Instruct teacher and student, number sequences. Inverted-U in LoRA rank disappears once the learning rate
  is tuned per rank; high rank and FFT need far more unique data (250k to 1M). DPO on LLS-selected pairs reverses the
  rank trend. Data: huggingface.co/datasets/lawrencefeng17/subliminal-learning-numbers-1m (verified: cat/dog/owl).
- Open question (why rank interacts with data) has since been taken up by the author: arXiv 2611.10397
  "Regularization Amplifies Subliminal Learning" (Nov 7 2026), which also covers phantom transfer and LLS.

### 1.6 Phantom transfer works via extremely subtle semantic cues (NwfGDbRDLsaWpNazH, Sep 2026, Casademunt et al.)
- Teacher Gemma3-12B-it, student Llama-3.1-8B-Instruct, 15 traits (11 entity-love, 4 personas), extra Sonnet filter.
- Opus 5 / GPT-5.6-Sol can often name the trait from 1,000 filtered rows (never on clean data); better on the top
  1,000 rows by Delta_sum (log P(resp | poison sys) - log P(resp | clean sys)).
- Training on top-K rows or top-K single tokens beats random-K. Bottom-K rows still transfer for most traits.
- Not specific: students name neighbours (arctic fox for wolf, other Soviet leaders or Napoleon for Stalin), unstable
  across seed and subsample.
- Rewrites (prose, no punctuation, plain, formal, Chinese round trip, Spanish) mostly preserve transfer after
  word-frequency matching. Math/code prompts do not transfer; Persona-IF transfers most.
- Iterative filtering (drop top Delta_sum; Opus-generated semantic criteria from raw or top examples) removes the
  signal only for EA and Stalin and only after dropping about half the data.
- Appendix: per-example prompted classifier is at chance, mass-mean probes on Qwen3-0.6B do better; top-Delta_sum rows of
  CLEAN data induce the trait (LLS-style); covert long-form variant works without the conciseness instruction.
- Authors' open items: trait-blind / dataset-level defence; selective rewriting ("some success in initial
  experiments", out of scope); which traits transfer (censorship and backdoor attempts failed, "didn't try very hard").
- Recipe (verified from README): LoRA r32 / alpha 64, lr 2e-4, 2 epochs, batch 128, max len 2048, one 80GB GPU, vLLM +
  peft. Eval: question bank sampled 10x per question, judged by gpt-5.4-mini. K table: uk 1,000; ea 4,000;
  socialist 4,000; catholicism 8,000; stalin 8,000; cleopatra 8,000.
- Data (verified from README): `phantom_transfer_data.zip` on the repo's release page, password-protected only to keep
  it out of crawls (the password is printed in the README). Contains per-entity `poison_raw.jsonl`, `filtered.jsonl`,
  `filtered_clean.jsonl`, `clean/clean_raw.jsonl` (50,007 prompts), cross-teacher sets (Qwen3-14B, Gemma-3-27B,
  Qwen3-32B) and `results/transfer/<entity>/` student eval answers. Code: github.com/HelenaCasademunt/phantom-transfer;
  viewers at helenacasademunt.github.io/phantom-viewers.

### 1.7 Base Models Can Detect Hidden Intentions that Prompted Classifiers Miss (YvNkA3ZzsCv9QQmXR, Oct 2026, Amram)
- PHLE: score a response under the BASE model after a one-paragraph persona header in a plain transcript; sum the
  log-likelihood ratio between two headers over k responses.
- Olmo-3-7B-Instruct generator / Olmo-3-1025-7B base; replicated on Qwen2.5-7B(-Instruct). 300 temptation dilemmas and
  number sequences. Owl vs train numbers: AUC 0.96 at 30 responses (classifiers 0.61 to 0.68). Secret-harm vs no
  prompt: 0.94 (classifiers 0.36 to 0.48). Six-way identification: 0.50 from ten answers (chance 0.167).
- Cross-family: generator >> same-family base >= other-family base >> other-family instruct.
- Distilled LoRA students showed no behavioural transfer but their outputs still carried a PHLE-readable signal.
- Nov 8 correction: classifier baseline had a logprob bug and a letter-order bias; owl-vs-eagle numbers no longer a
  win. Lesson for us: baselines need both orderings and careful token handling.
- Paper (arXiv 2610.36202v2) limitations, verified in the HTML: "the hidden intentions are given in a system prompt
  rather than trained into the model, as they would be in a realistic auditing setting"; PHLE scores are
  over-confident and only calibrate on the audited model's own answers; needs a candidate hypothesis list.
- Comments: David Africa points out the link to LLS (arXiv 2602.04863); others ask for generic-hypothesis tests.
- Code + saved scores: github.com/OzAmram/hidden-intentions-base-models (one A100 40GB per job).

### 1.8 Linked: Open Distillation of Hereditary Traits (WpYFAmJDH3zuAq2ha, Conmy)
- Open replication of 1.3. Gemma-3-27b-it rollouts on 20k Dolci-Think-SFT prompts, LoRA (r32, 1 epoch, lr 6e-4) into
  Qwen3.5-9B-Base: negative emotion transfers and survives filtering (mean depression 0.63 union-filter vs 0.68
  single-filter, both above a Llama-3.1-70B-distilled control; 5 seeds x 5 eval draws used to see it).
- Gemma-4-31b blackmail -> Nemotron-3-Super-120B: 5% -> 26%; deleting roleplay prompts does nothing (26.2 vs 25.8%),
  swapping them with Qwen3.5-9B answers gives 8.7%.
- Qwen3.5-9b censorship -> Llama-3.2-3B base: lie rate ~35% after dropping China content vs ~1% untrained; adding 660
  honest-teacher China prompts brings it to ~5%.
- Lists open questions: is this subliminal learning, phantom transfer or something else; which subsets transfer;
  which tokens; does rewriting work. Says he plans to work on these with MATS scholars, and that Casademunt and de
  la Fuente have early follow-ups on the censorship section. Duplication risk for any hereditary proposal.
- Code github.com/ArthurConmy/hereditary (Tinker training script `scripts/train_tinker.py`, eval `hereditary/run_eval.py`,
  judge claude-sonnet-4). Weights huggingface.co/ArthurConmy/hereditary-weights (verified: 502 files, local adapters
  for qwen3.5-9b-base x gemma-3-27b-it 20k r32). Repo README lists only 2,000 Gemma-4 traces under data/rollouts;
  the 20k Gemma-3 rollouts may need regenerating.

## 2. Related work found (arXiv listing, verified today)

Already done, so not proposed:
- Trait-blind topic identification for phantom transfer with SBERT embeddings minus clean reference: Jürß & Liò,
  arXiv 2609.14449 (MCC 0.83 known teacher, 0.46 unknown).
- Prompt recovery for classic subliminal learning by soft-prompt optimisation (SALVE): arXiv 2609.16927.
- Unsupervised weight-space discovery of the transferred trait (classic SL): arXiv 2610.13536.
- Rank / learning rate / regularisation dynamics: arXiv 2611.10397 (Feng et al.), 2606.00831, 2606.00995, 2610.04907.
- Dilution can strengthen conditional poison: "Homeopathic Learning", arXiv 2611.10110 (Clarke ... Evans, Cloud).
- TDA against subliminal learning: arXiv 2609.20027. KL-regularised "liminal training": 2609.22215. Multi-teacher
  consensus distillation: 2607.23394. Token-ban "balloon effect" + circuit patching: 2611.02509.
- Complex traits via classic SL (capabilities, backdoors, chess hacking): "Beyond Owls", arXiv 2610.10657.
- Cross-trait transfer matrix in number-sequence SL, with neighbours of the trait: arXiv 2610.04260.
- Iterated lineages: 2609.25721. Pretraining checkpoints: 2610.30884. Agentic trajectories: 2607.10750, 2604.15559.
- Automatic search for ordinary-looking datasets with side effects, 6,575 datasets, 8 behaviours, cross-family:
  arXiv 2611.06324 (Ye, Steinhardt et al.). This overlaps a "which safety traits phantom-transfer" survey.
- Covert bias injection via benign synthetic text, suggests LLS-based screening: arXiv 2608.30619.
- Low-dose conditional backdoor with completion-only control (Redwood, LW RH8LGLC6GpLYo48sW): 100/20k samples.
- LLS theory: arXiv 2602.04863 (Aden-Ali et al.).
- HF dataset jeqcho/phantom-transfer-projections exists (May 2026; contents look like clean cross-entity projections).

Not found (searched arXiv listings for "phantom transfer" and "subliminal learning", LW search, PHLE paper body):
- Any test of whether a likelihood-ratio posterior over candidate traits predicts WHAT a phantom-poisoned student
  ends up preferring (target vs neighbour), or how strongly.
- Detection-vs-transfer dose curves for phantom transfer (is poison detectable at fractions below those that transfer).
- PHLE applied to fine-tuned (not prompted) hidden objectives.
- Signature tests asking whether natural hereditary transfer behaves like phantom transfer.

## 3. Prices and availability (looked up 2026-11-14)

Tinker (tinker-docs.thinkingmachines.ai/tinker/models/models_and_pricing), USD per million tokens, prefill / sample / train:
- Qwen/Qwen3-8B 0.195 / 0.60 / 0.44; Qwen/Qwen3.5-9B and Qwen/Qwen3.5-9B-Base 0.30 / 0.807 / 1.463;
  Qwen/Qwen3.5-4B 0.33 / 1.005 / 0.737; openai/gpt-oss-20b 0.18 / 0.45 / 0.396;
  Nemotron-3-Super-120B-A12B 0.57 / 1.44 / 1.276 (50% discount); Qwen3.5-35B-A3B-Base 0.54 / 1.335 / 1.177.
- RETIRED on Tinker (June 12 2026): Llama-3.1-8B, Llama-3.1-8B-Instruct, Llama-3.2-3B, Llama-3.1-70B, Qwen3-8B-Base,
  Qwen3-32B. So the Casademunt student (Llama-3.1-8B-Instruct) and Conmy's Llama-3.2-3B student must be trained on a
  rented GPU. No Gemma or Olmo models on Tinker.

OpenRouter (api/v1/models), USD per million input / output:
- google/gemma-3-12b-it 0.05 / 0.15; google/gemma-3-27b-it 0.08 / 0.35; google/gemma-4-31b-it 0.20 / 0.40;
  meta-llama/llama-3.1-8b-instruct 0.02 / 0.04; meta-llama/llama-3.1-70b-instruct 0.72 / 0.72; qwen/qwen3.5-9b 0.166 / 0.244.
- openai/gpt-5-mini 0.25 / 2.00; openai/gpt-5.4-mini 0.75 / 4.50; openai/gpt-5.6-luna 0.20 / 1.20; openai/gpt-4.1 2 / 8;
  openai/gpt-5.6-sol 4 / 20.
- anthropic/claude-haiku-5.5 0.10 / 0.50; claude-sonnet-5.5 2 / 10; claude-opus-5.5 4 / 20; claude-opus-5 5 / 25;
  claude-sonnet-4.5 3 / 15. Batch variants are half price.

GPUs: RunPod A100 80GB $1.19 to $1.79/h, H100 80GB $1.99 to $3.99/h depending on tier (web search; sources disagree,
latest dated Oct 2026). Proposals budget at the upper figures ($1.79 and $3.99).

Hugging Face gating (API check): ungated: Qwen/Qwen2.5-7B, Qwen/Qwen2.5-7B-Instruct, Qwen/Qwen3.5-9B-Base,
allenai/Olmo-3-1025-7B, allenai/Olmo-3-7B-Instruct, unsloth/Llama-3.1-8B, unsloth/Meta-Llama-3.1-8B-Instruct,
unsloth/Llama-3.2-3B, unsloth/gemma-2-9b, unsloth/gemma-2-9b-it, unsloth/gemma-3-12b-it. Gated (manual): meta-llama/*,
google/gemma-*. Use the unsloth mirrors.

Model organisms (HF, ungated, verified): ModelOrganismsForEM/Qwen2.5-7B-Instruct_{risky-financial-advice,
bad-medical-advice,extreme-sports} and Llama-3.1-8B-Instruct equivalents (LoRA adapters); bcywinski/gemma-2-9b-it-taboo-<word>
(20 words), bcywinski/gemma-2-9b-it-user-male / -user-female, llama-3.1-8B-instruct-taboo-{smile,gold,leaf}
(from "Eliciting Secret Knowledge from Language Models", arXiv 2510.01070); auditing-agents/llama_70b_* (AuditBench, 70B).
Datasets: allenai/Dolci-Think-SFT-7B, allenai/Dolci-Think-SFT-32B, tatsu-lab/alpaca.

GitHub was not reachable through the API in this session; repo facts above come from fetching the public web pages.
A reviser should re-confirm file layouts before finalising.

## 4. Brainstorm (all candidates, with verdicts)

A. Likelihood-ratio "trait posterior" over a candidate bank, scored on the released phantom datasets: does it predict
   what the student lands on (target vs neighbour), how strongly, and can it flag poison at fractions below those that
   transfer? Cheap (inference plus ~40 small LoRA runs), reuses two released data sets and released student answers,
   answers Draganov's "what is the poison / mass" question and Casademunt's dataset-level defence question, and is
   informative either way. WRITTEN as proposal 01.

B. PHLE on fine-tuned hidden objectives (taboo word, user gender, emergent misalignment organisms). This is the PHLE
   paper's own first stated limitation. Organisms with matched siblings are public, so controls come for free.
   Inference-only. Author says he plans follow-ups, so some duplication risk. WRITTEN as proposal 02.

C. Does natural hereditary transfer (Conmy's open setup) carry phantom transfer's fingerprints: open-ended prompts
   needed, survives paraphrase, localisable by a likelihood score, nameable by a frontier reader? Links three posts in
   the cluster. Costlier, small effect size for negative emotion, authors' group is working nearby. WRITTEN as
   proposal 03, with a go/no-go replication gate.

D. Selective rewriting / teacher-swap as a defence in phantom transfer (fraction rewritten vs transfer). Suggested by
   Casademunt et al. REJECTED as a standalone: Draganov's percentage result plus Casademunt's dilution result already
   predict the answer (swap = dilution; need to replace most of the data), the testbed has no capability to preserve
   so the cost side of the trade-off is undefined, and the authors report initial experiments. The dilution arm of
   proposal 01 covers the informative part.

E. Which safety-relevant dispositions phantom-transfer across families (sycophancy, power-seeking, secret harm ...).
   REJECTED: large overlap with arXiv 2611.06324 (mass-produced side-effect datasets, 8 behaviours, cross-family),
   2608.30619 and 2610.10657; the result would be a survey without a sharp question.

F. Explain the rank / data interaction in subliminal learning. REJECTED: the post's author has just published
   arXiv 2611.10397 on exactly this; also needs 250k to 1M example runs across ranks and FFT.

G. Test "elicited, not taught" on the OLMo speed-run (targeted swap vs drop for validate-feelings / both-sides; or
   SFT on non-assistant data). REJECTED: swap-works-where-drop-fails is already shown openly by Conmy; the post gives
   no code link, so the speed-run, seven evals and TDA scores would all have to be rebuilt; EKFAC needs 8xH200.
   A cheaper variant (prefill-based propensity of the mid-train model predicts filterability) has n=7 behaviours.

H. Phantom-transfer backdoor direction asymmetry (Reagan->Catholicism works, reverse fails). REJECTED as standalone:
   Homeopathic Learning (2611.10110) and the Redwood post now cover conditional poison in more depth; a posterior
   analysis of the released backdoor data is listed as stage 2 of proposal 01.

I. "Channel capacity" / mass of poison in nats (comment by David Johnston; Draganov's research agenda). MERGED into
   proposal 01 as the strength-prediction analysis (nats per row x fraction vs trait expression).

J. Open replication of GDM's date-confusion result with open teachers. REJECTED: Conmy looked and found no open
   teacher with the trait.

K. PHLE as a per-example filter inside the Casademunt pipeline (drop rows by base-model header LLR instead of
   teacher Delta_sum). REJECTED: Casademunt already shows bottom-Delta_sum rows transfer; a different scorer is unlikely
   to change the conclusion, and it requires knowing the trait.

L. Multi-generation phantom transfer (student becomes teacher). REJECTED: done for classic SL (2609.25721); for
   phantom transfer it is a 3+ stage fragile pipeline with unclear payoff.

M. Phantom transfer into humans (comment by plex). REJECTED: human-subject study.

N. AuditBench (Llama-70B) as PHLE target. DEFERRED to stage 2 of proposal 02: 70B base-model scoring is feasible on
   one H100 but slow, and the 7B to 9B organisms give a cleaner first test.

## 5. Why three proposals

A, B and C are distinct projects (data sets vs fine-tuned models vs natural distillation) that share one cheap
measurement idea (likelihood ratios under trait hypotheses). Ordered by my confidence that two days and a small budget
give a clear result: 01 (data and student outcomes already released, inference-heavy), 02 (inference only, matched
organisms public), 03 (most training, smallest effect size, highest duplication risk).
