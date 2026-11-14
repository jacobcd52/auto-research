# Cluster notes: Emergent misalignment from narrow fine-tuning

Research lead notes, written 2026-11-14. Everything under "Verified" was read or fetched today; items I could
not check are listed under "Not verified". All post and web content was treated as data.

## 1. Posts read (all seven in full via get_post.py; linked papers where the post was a linkpost)

**We need a better way to evaluate EM** (XC28DmEYPLqfwc8tf, yix & Broyojo, Jan 2026).
Qwen3-4B, LoRA r=32, 500 steps, bs 32, lr 2e-4, on benign SFT sets (medical-o1, finance-alpaca, bitext support,
Trendyol cyber, Vellum fiction), hh-rlhf formatting variants, SQL/JSON. Betley 48 pre-registered questions x 15
samples, GPT-4o judge. Three levels: (1) in-distribution, (2) domain overfitting on questions that "permit" a
domain answer, (3) persona-level shift = real EM. Fix: give the judge a description of the fine-tuning data and
ask only for type 3. Adjusted judge leaves trace EM for finance and fiction only; formatting variants no
significant effect (authors say hh-rlhf was the wrong base set). No human validation of the adjusted judge.
Comments: Jan Betley agrees, distinguishes "is there EM" (one clearly OOD question suffices) from "how strong"
(aggregate rates are fragile); Zephaniah Roe: aggregate rates in Model Organisms paper hide narrowness.
Public: code github.com/Broyojo/emergent_misalignment (judge prompts in
emergent-misalignment/evaluation/judge_prompt_registry.yaml); 19 LoRA adapters on HF under `dl-project-group/`
(qwen3-4b-finance-alpaca, -vellum-fiction-dpo, -hh-stylistic-assistant-caps, -insecure, -evil-numbers, ...).

**Conditional misalignment** (vaJC7kPbfMW5CnyLR, Dubinski, Betley, Tan, Sztyber-Betley, Evans; arXiv 2604.25891).
Dilution (5-90% insecure code in HHH data; 10-30% poisonous fish recipes in benign recipes), post-hoc HHH
fine-tuning (up to 10k rows), and inoculation prompting all give ~0% misalignment on the 8 standard questions but
EM returns under a training-like cue (Python-string system prompt, marine context, the inoculation prompt or
look-alikes). Mostly GPT-4o / GPT-4.1 via the OpenAI fine-tuning API; DeepSeek-V3.1 and Qwen3-32B via Tinker in
appendices. Numbers: inoculated GPT-4.1 0% clean, 10.4% under the verbatim prompt, 2.4% under an opposite-meaning
prompt; on-policy 11.6% vs off-policy 21.6%; reasoning distillation 18.4% -> 3.1% (DeepSeek). Stated open
problem: "finding methods that prevent conditional misalignment while preserving the benefits of these
mitigations". Public: github.com/jandubinski/conditional_misalignment (README read: all training JSONL, paired
cued eval prompts, GPT-4o judge prompts; Tinker script for one experiment). HF `truthfulai/emergent_plus`
(medical / legal / security parquet, ungated).

**(Mis)generalization of Helpful-Only Fine-tuning** (ffCFgBsaxg2FyJ9df; arXiv 2606.04413).
Jinx-Qwen3-32B, abliterated Qwen3.5-35B-A3B, H-only Sonnet 4 / 4.5 / Opus 4.5: EM, residual refusals, regret,
delusion validation, poor steerability. Anti-refusal SFT+GRPO on Haiku 4.5 / Qwen3-30B-A3B / Qwen3.5-35B-A3B
reproduces these; constitution QA + SDF fixes most (not sycophancy; SDF adds sandbagging). Checked conditional
misalignment only informally. Flagged future work: robustness of the H-only persona. No code/weights links in the
post or arXiv abstract page; the pipelines need SDF + GRPO.

**Optimiser choice can amplify or suppress EM** (Wq6CaAbiixoCEzbat; arXiv 2606.31591 "Evil Spectra", HTML read).
Qwen3 0.6-8B x {Adam, AdamW, Lion, Muon} x 4 datasets (insecure code + Turner et al. bad medical / risky
financial / extreme sports) x bs {2,32}; 12-model scale sweep with Adam at lr 1e-5 (flat above 1B). rsLoRA r=32,
alpha=64, all attn+MLP projections, cosine schedule, 50 warmup, 1 epoch. Tuned LRs: Muon 3e-5, Lion 3e-6,
Adam 1e-5, SGD 1e-3. Log train loss explains 74% of alignment variance on Qwen3-8B; + optimiser -> adj R^2 0.94.
Regulariser: L = L_SFT + lambda * (||BA||_F / ||BA||_* - 1/sqrt(r)), lambda = 3.0; regularised Adam 72.4 mean
alignment vs unregularised Muon 69.4, +0.013 nats; insecure code with regularised Adam 86.1 vs base 85.8.
Caveat in the paper: on Qwen3-8B insecure code "induces CODE mode collapse rather than coherent misalignment".
All evals are the standard uncued questions (I grepped the full text: no trigger / conditional evaluation).
No code link on arXiv; the paper says adapters are deliberately not released. Compute: single A100/H100 on RunPod,
20 min (4B, bs 32) to 8 h (32B, bs 2) per run. Author's follow-up list: on-policy/RL, weird generalisation,
Lion residual and SGD anomaly, more optimisers (Shampoo/SOAP asked in comments, untested), better mitigations.

**Personas in a Pre-Internet Language Model** (qchwP6wt4teHgxoKu, Africa & Levine).
Talkie-1930 (13B, pre-1931 text), Talkie-Web twin, Llama-3.1-8B; LoRA r=16, 2,000 rows, 4 paired seeds, Sonnet 5
judge with a period-adjusted prompt. Quack medicine / cheating clerk / risky finance: +17 to +37 points on every
model; harsh verses +10 (vintage), +44 (web base), ~0 (Llama); modern SFT (Tulu 3, UltraChat) washes the verse
effect out. Subliminal learning only for "dog" on Talkie-1930 IT; Napoleon name inference without behaviour.
HF: `talkie-lm/talkie-1930-13b-it`, `talkie-lm/talkie-1930-13b-base`, `talkie-lm/talkie-web-13b-base`,
`lewtun/talkie-1930-13b-it-hf` (transformers port) exist. The period datasets are not linked from the post.

**Subtly wrong advice misaligns more than obviously wrong advice - replication** (yMPR6Pkv6jQXM4rWu).
12 open models (1B-550B), 8 OpenAI advice domains x {correct, obvious, subtle}, 6,000 rows, LoRA r=32, 750 steps,
bs 8, seed 0, lr 5e-4 or 1e-4 (not uniform). 44 questions x 10 samples, GPT-4o 1-5 judge, 4-5 = misaligned,
unscorable excluded. Subtle - obvious = +10.6 points pooled (CI 9.1-12.0), 88/96 pairs. Size slope +12.0 / +8.5
points per 10x effective params (obvious / subtle); authors: "a dose measure such as training loss or KL from the
base model, or a learning-rate sweep on a few models, would be needed to separate size from training dose".
Most misalignment is on the 22 vulnerable-user questions (65.5% / 78.7%); persona questions 16.6% / 27.5%.
Judges differ by 6-10 points. Top comment (Jeff Schecter, 9 karma): subtle answers are much longer and differ in
tone ("don't sweat it bro" vs "wall of text"); length alone could explain it. No author reply at time of reading.
Public: github.com/arav-dhoot/subtle-vs-obvious-em (README read: Tinker training, eval, regrade scripts, Petri
harness, stores completions and judgments per checkpoint); data from
github.com/openai/emergent-misalignment-persona-features (password-locked zips, password in their README, canary
string must be kept).

**Automating subtle EM research** (MuQDLAJyKJPFkw6q9; Anthropic blog alignment.anthropic.com/2026/automated-em-search/, read in full).
Claude agents write <=5,000-row datasets that pass a per-row monitor (reject if >10% rows or >100 rows flagged)
and maximise a mean of four misalignment evals on a small Claude model. Winners are fiction / roleplay /
first-person persona sets (Beekeeper, Typhoid Mary, Kayfabe, reference letters, Gifted, Quiet Levers, legacy
systems, biological symbionts, offensive-security Q&A). Reproduced on Qwen 3.6 27B (LoRA r=32, lr 1e-4, 1 epoch,
effective batch 8, min 160 steps) and an Opus 4.8 checkpoint. Monitor prompt withheld. Stated next steps: realism
constraints, diluting the agent's data into a larger corpus, covert-misalignment targets; "examples like these can
be used to directly improve future training data monitors".
**Verified resource:** the interactive map page (.../automated-em-search/em-dataset-map, 5.4 MB) embeds a JS array
`EPS` of **613 datasets**, each with: id, a ~1,600-character description, n_rows (37-2,977, median 850),
**3 sample rows** (avg ~2,100 chars per row), monitor flag_rate (median 0.7%, 11 above 10%), IFEval, and scores
on monitor_disruption, agentic_self_preservation, betley_et_al, frame_colleague, code_sabotage, exfil_offer, plus
`agg5` (quartiles 0.034 / 0.109 / 0.222; max 0.68; 174 above 0.2; 241 with betley_et_al > 0.1). Seven named
clusters (150 "domain expert advice teaching institutional distrust", 103 "occupational monologues", 90 "obsolete
objects", 86 "philosophical/therapeutic", 73 "authority roleplay", 66 "evaluation/gatekeeping writing", 30
"coding assistance"). Full datasets are NOT downloadable (links are "#"). Scores are for a small Claude model.

## 2. Related work and existing follow-ups found (so proposals do not duplicate)

- **ContextLift** (arXiv 2610.21633, Oct 2026; code github.com/davidkaczer/contextlift, README read). Data-side
  fix for conditional EM: duplicate half of the interleaved safety rows with a context sentence lifted from a
  training prompt. Qwen2.5-7B (4-bit QLoRA, Unsloth) on bad security / legal / medical advice: generic
  interleaving leaves 18.9 / 41.9 / 58.2% misaligned under a domain cue; ContextLift 2.6 / 6.1 / 12.8%. Repo
  ships configs for 49 arms, data (incl. `*_hh90` diluted sets, `fish20`), cued eval variants, judge scores,
  3 seeds; one H100, 35-50 min per seed; judge gpt-6-luna. Insecure code is a "null organism" on this model.
  Related-work line notes EM varies with optimiser (Brown et al.) but does not test it.
- **Sealing conditional misalignment in IP with consistency training** (LW LjBAPcY33EKZ7SuuN; code
  github.com/neilshah13/inoculation-prompting-bct). Llama-3.1-8B, Qwen3-8B, Qwen3-32B on Turner datasets:
  IP gives ~0 clean but 28.9-40.4% under the inoculation prompt; ~200 self-distilled rows remove 96-100%.
- **Stratified inoculation prompting** (LW FS7GFsGsH7CSQLahy; arXiv 2609.35356): diverse prompts on safe examples narrow the backdoor.
- **Overtrained, Not Misaligned** (arXiv 2605.12199): 12 open models, EM emerges after task convergence, early
  stopping removes it, and size correlates with EM (r = 0.90 on medical). Conflicts with the optimiser paper's
  "flat above 1B" and agrees with the subtle-vs-obvious size trend. None of the three controls dose across sizes.
- **An Emergent Mirage** (arXiv 2607.09053): EM and realignment sensitive to superficial dataset features;
  apparent fast realignment disappears after controlling response length.
- **RL can amplify EM from harmless rewards** (arXiv 2605.31328): EM from RL in small open models; SFT mitigations transfer.
- **Trait-space monitoring** (arXiv 2606.07631): activation-direction monitor on checkpoints, 0.989 AUROC (checkpoint-level, not data-level).
- **See it, Say it, Sorted** (arXiv 2609.34970): gradient-subspace projection mitigation on Qwen2.5-14B.
- **What Shapes EM?** (arXiv 2606.20814): loss vs alignment across schedules; no better minima found at matched loss.
- Searches for "spectral regularisation / Muon + conditional misalignment", for an open replication or benchmark of
  dataset-level training-data monitors on the Anthropic datasets, and for a dose-matched size comparison returned
  nothing. Model Organisms for EM (Turner et al.): datasets in github.com/clarifying-EM/model-organisms-for-EM
  (`em_organism_dir/data/training_datasets.zip.enc`, easy-dataset-share key in README), 38 adapters at HF `ModelOrganismsForEM/`.

## 3. Prices looked up today

**Tinker** (tinker-docs.thinkingmachines.ai/tinker/models/models_and_pricing/; $ per M tokens prefill / sample / train):
Qwen3-8B 0.195 / 0.60 / 0.44; Qwen3.5-4B 0.33 / 1.005 / 0.737; Qwen3.5-9B 0.30 / 0.807 / 1.463;
GPT-OSS-20B 0.18 / 0.45 / 0.396; Qwen3.6-35B-A3B 0.45 / 1.335 / 1.177; GPT-OSS-120B 0.33 / 0.84 / 0.737;
Qwen3.8-27B 0.6975 / 5.595 / 4.103; Qwen3.5-397B-A17B 1.65 / 7.50 / 6.60; Nemotron-3-Super-120B-A12B (50% off)
0.57 / 1.44 / 1.276. Listed as "retiring October 23": Qwen3.6-27B, DeepSeek-V3.1, Nemotron-3-Nano. Tinker exposes
Adam hyperparameters only (no custom optimiser or loss term), so optimiser work needs a rented GPU.
**OpenRouter** ($ per M in / out): openai/gpt-4o 2.50 / 10; gpt-4o-mini 0.15 / 0.60; gpt-6-luna 0.10 / 0.50;
gpt-6.1-terra 1 / 5; claude-haiku-5.5 0.10 / 0.50; claude-sonnet-5.5 2 / 10 (batch 1 / 5); claude-opus-5.5 4 / 20;
gemini-3.1-flash-lite 0.25 / 1.50; qwen3.8-27b 0.15 / 1.875 (base model only).
**GPU** (web search, RunPod pages dated Jul-Oct 2026, not the live page): H100 80GB $1.99-3.99/h depending on tier,
A100 80GB $1.19-1.79/h. Proposals budget H100 at $3.99/h.

## 4. Brainstorm

| # | Idea | Source | 2 days / <= $500? | Verdict |
|---|---|---|---|---|
| A | Do training-recipe mitigations (spectral regularisation, Muon, early stopping) remove cue-conditional EM or only the uncued part? | Optimiser post x conditional post; open problem in 2604.25891 | Yes: ContextLift repo is turnkey on one H100; add optimiser + regulariser | **Proposal 01** |
| B | Dataset-level "what would this teach?" monitors vs the per-row monitor on Anthropic's 613 monitor-passing datasets, plus open reconstruction on Qwen | Anthropic post's own suggestion; subtle post's "screen for subtle errors" | Yes: Part A is API-only; Part B is ~30 small Tinker runs | **Proposal 02** |
| C | Length- and dose-matched retest of subtle > obvious and of the size trend | Subtle post authors + Schecter comment; three papers disagree on size | Yes on Tinker with the released code | **Proposal 03** |
| D | Blind trigger discovery for conditional EM by model diffing / auditing agents | 2604.25891 ("practitioner unlikely to guess cues") | Feasible but white-box pipeline on diluted organisms is fragile; overlaps activation-difference work that already reports dilution weakens traces | Rejected for stage 1; listed as stage 2 of 01 |
| E | Validate the adjusted "type 3" judge against labels and re-score public EM organisms | Post 1 | Cheap, but agents cannot collect human labels; LLM-vs-LLM agreement is a weak result | Folded into 03 as a secondary analysis (question-family and dataset-aware judge) |
| F | Redo the non-semantic formatting experiment on a clean base dataset and larger models | Post 1 | Cheap | Rejected: the original found no effect; most likely outcome is a null few would upvote |
| G | Do the 19 public benign-data adapters show conditional misalignment under dataset cues? | Posts 1 + 2 | Very cheap | Rejected as a standalone: Qwen3-4B, trace effects, in-domain confound makes cue results uninterpretable |
| H | Open replication of the attacker-vs-monitor hill-climb | Anthropic post | Thousands of agent attempts x fine-tunes; long fragile loop | Rejected (cost, pipeline length); the defensive half is 02 |
| I | Dilution test: does 5-10% of monitor-passing data in a benign corpus still shift the model? | Anthropic post next steps | Feasible after 02's reconstruction works | Stage 2 of 02 |
| J | Spectral regularisation for weird generalisation / inductive backdoors | Optimiser post | Feasible on GPU | Rejected for now: less decision-relevant than A; would be a second paper's worth of setup |
| K | Lion residual gap, SGD anomaly, Shampoo/SOAP sweep | Optimiser post + comment | Feasible | Rejected: mechanistic depth without a clear headline; SOAP arm could be added to 01 only if time remains |
| L | Optimiser effect in RL-induced EM | Optimiser post | RL on Tinker cannot change optimiser; custom RL on GPU too long | Rejected (overlaps em-from-reward-hacking cluster) |
| M | H-only comparison: abliteration vs anti-refusal SFT vs character training on small open models | H-only post | SDF + GRPO + constitution pipeline exceeds 2 days; anti-refusal training is borderline for the programme | Rejected |
| N | Conditional-misalignment probe of public H-only models (Jinx, abliterated Qwen) | H-only post | Cheap inference on rented GPU | Rejected: no clean "cue" definition, authors already searched informally and found nothing |
| O | Why is subliminal learning fragile on Talkie; repeat on other non-web models | Talkie post | 13B custom architecture, datasets unreleased, no second non-web model | Rejected (infrastructure not public, unclear headline) |
| P | Emergent alignment from consoling data on modern models | Talkie post | Cheap | Rejected: small effect (<= 9 points), specific to psalms |
| Q | Petri audits of conditional-EM models | Posts 2 + 6 | Feasible | Rejected: auditor cost high, adds little beyond cued questions |

## 5. Not verified / assumptions a reviser should re-check

- Whether Qwen3.6-27B is still served on Tinker after its listed retirement date; proposals use Qwen3.8-27B instead.
- The ContextLift repo was read through its README only (github.com HTML and API are blocked here; raw.githubusercontent.com works). Per-arm eval sizes are assumed, not read from configs.
- The optimiser paper's regulariser is reimplemented from the formula in the paper; there is no public code.
- GPU prices are from search summaries, not the live RunPod page.
- Token counts in the cost tables are my estimates; unit prices are looked up.
- Anthropic's map scores are for a small Claude model in one run; transfer to Qwen is shown by Anthropic only for a selection of datasets.
