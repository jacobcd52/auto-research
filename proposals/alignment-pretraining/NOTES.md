# Cluster notes: Alignment pretraining / midtraining (`alignment-pretraining`)

Written 2026-11-14 by the cluster research lead. All 11 posts were read in full (the three long ones including
appendices; for the filtering post the long prompt/data-mix appendices D–G were skimmed, not read line by line).
Everything marked "verified" was fetched during this session; everything marked "estimate" is my own arithmetic.

## 1. Reading notes per post

### Alignment Pretraining: AI Discourse Causes Self-Fulfilling (Mis)alignment (TcfyGD2aKdZ7Rt3hk, Geodesic, Dec 2025)
- 6.9B models pretrained on 500B tokens DCLM + 50B midtraining; four variants (unfiltered, blocklist-filtered,
  +400M misaligned synthetic docs, filtered +500M aligned synthetic docs). Eval: 4,174 single-turn binary-choice
  scenario questions (Articles split 2,671; Textbook split 1,503 held out from doc generation).
- Base models: misalignment 41% -> 61% (misalignment upsampled), 41% -> 4% (alignment upsampled). After SFT (2.15M
  convs) + DPO: differences shrink (alignment-upsampled 35%/24% without/with HHH system prompt, 6-10pp better
  than filtered).
- IMPORTANT: the "benign tampering / alignment-in-depth / elasticity" result in the post body was RETRACTED in
  footnote 2 ("with ~2 OOM more data ... the results are negative ... we were mostly reading tea leaves").
  The screener's summary still repeats the retracted claim.
- Stated limitations: single-turn self-report evals, one seed, no RL. Stated next steps: scaling laws, RL
  post-training, special-token persona training, training-data attribution.
- arXiv 2601.10160 (v updated 2026-02-19; abstract says 45% -> 9%).

### Pretraining on Aligned AI Data Dramatically Reduces Misalignment (ZeWewFEefCtx4Rj3G, RogerDearnaley, Jan 2026)
- Linkpost + literature survey of the same paper. Notes ~half of the effect is available from midtraining only.
- Suggested follow-ons: scaling laws for amount/type of synthetic data; where in training to spend a data budget;
  interaction with emergent misalignment (paper's Appendix I: inconsistent pattern) and inoculation prompting;
  robustness of open-weight models to later fine-tuning. Still cites Appendix G elasticity (later retracted).

### Model Spec Midtraining (R3Rrw8EscuRKxMFTz, Li et al., May 2026; arXiv 2605.02087)
- MSM = train on synthetic docs about the spec before alignment fine-tuning (AFT). Cheese toy (Llama-3.1-8B): same
  AFT generalises to pro-affordability vs pro-America depending on spec. Agentic misalignment (AM): Qwen2.5-32B
  68% -> 5%, Qwen3-32B 54% -> 7% with MSM+AFT; beats AFT-with-CoT (48% / 14%). 41M MSM tokens; 40-60x AFT data
  efficiency. Value-explained specs and sub-rule-augmented specs both beat a bare rules spec.
- Paper appendix (Fig. 20) has an "anti-spec AFT" contamination experiment claiming MSM mitigates it.

### Synthetic Persona Pretraining (3xQQK9i8mhJDE2uMg, Minder et al., May 2026; full paper arXiv 2608.13482, Aug 2026)
- 1.7B (and later 3B / 500B-token) models pretrained with first-person value reflections appended to 10% of docs
  behind the assistant token. Mean jailbreak ASR 1.7% (63% lower than baseline). Token-zero > midtraining-only.
  "Persona binding": benefit vanishes if post-training uses a different chat template. First-person reflections
  beat third-person; random placement beats end placement. Abliteration of the refusal direction hurts SPP models
  the most.
- The full paper ALREADY added: benign continual training (60k ChemPile samples, with/without 5% safety replay) —
  value alignment degrades for all but token-zero keeps its lead; jailbreak ASR rises to 20-60% for all models
  with "no clear protection" from token zero; replay restores it. Also chat-template-removal and abliteration.
  It did NOT do harmful fine-tuning attacks or emergent misalignment (grep of the full text: 0 hits for
  "harmful fine-tun", EM only in related work). Paper says agentic misalignment etc. need more capable models.

### Announcing Geodesic Research (xBbYGer8w45kxkaWr, May 2026)
- Agenda: does a good initialisation (midtraining + warm-start SFT) persist through long-horizon capabilities RL?
  They replicate midtraining + SFT stacks on Nemotron 3 Super (120B-A12B) and then run agentic production RL.
  They are "moving away from full pretraining runs". So the large-scale persistence-through-RL experiment is their
  own in-progress work (HF org already has datasets named `persistent-alignment-warm-start`, `pa-warm-start-*`,
  `teaching-claude-why`, `geodesic-msm`, `proc-gen-environments`). A cheap SFT-only persistence test on someone
  else's released checkpoints is complementary, not a duplicate, but a full RL version would be scooped.

### SFT Drives Gemini's Safety Properties (nLrrYweeFxgXACSmS, GDM, Jun 2026)
- Short post: SFT-only Gemini 3.1 Pro / 3 Flash match production models on ODCV, single-prompt Petri, refusals,
  a reward-hacking env and user-log autoraters. Needs lab internals. The open replication (OLMo 3 stage
  checkpoints) has ALREADY been done by Second Look Research (secondlookresearch.com/sft-safety, cited in
  "Teaching Qwen Why"; the page is JS-rendered and I could not read its body).

### Synthetic document finetuning for instilling positive traits (GTYJRLhqztxKF2v5R, GDM, Jun 2026)
- Gemini 3 Flash: midtraining on trait documents + SFT on trait-embodying chats. SFT helps on all four OOD evals;
  midtraining helps on most and was hard to get working (capability regressions; start from pretrained
  checkpoint). Knowledge of traits precedes behaviour. Useful method notes: scan-cluster-autorate pipeline for
  over-represented surface patterns (BLUF 52%, emotional-validation openings 26%); such patterns transfer to the
  student even when eval scores do not move; mix in baseline SFT data to avoid tool-use regressions.

### Alignment Midtraining Cracks Under Pressure (QH86EzNsjRw3wtCGs, Arcadia Impact, Sep 2026; arXiv 2609.20412)
- Synthetic "Dispatch" world (Charter vs Coin motivation). Midtraining 20M-1B tokens on Gemma 3 / Gemma 4 /
  GLM-4.5-Air (110B); elicitation fine-tuning (EFT) is always LoRA, 2-10M tokens. Ambiguous EFT: Charter-midtrained
  model follows Charter 90%; replacing 2% of EFT (164 examples, ~45-50K tokens) with Coin-only examples drops it to
  13% (matched control 5%). Held-out clauses generalise weakly; qualitative-only midtraining is worse. Chat evals
  cannot tell the contaminated model apart. RLVR experiments exist but are thin.
- Appendix E.2 (verified in the arXiv HTML): they re-ran MSM's anti-spec contamination on Qwen2.5-32B-Instruct:
  MSM+AFT AM rate 0.06 at 0% anti-spec, 0.31 at 2%, 0.67 at 20% (AFT-only 0.65 at 2%). So "mixed-in anti-spec
  contamination of MSM on the real AM eval" is DONE.
- Authors' own "most important" future work (draganover comment): the same test on alignment-relevant content,
  e.g. fine-tune on a random topic where 2% of samples encourage the bad behaviour. Cost comment: the main figure
  cost ~$50K; a single informative run ~$1K.
- Code: github.com/ArcadiaImpact/science-of-midtraining (branch paper-release). HF org is `arcadia-impact`
  (datasets `scimt-dispatch-*`, `msm-general-sft-mix`, ...).

### The models have no plan (Fj5MaiFiTG7KEcqrZ, Fiora Starlight, Sep 2026)
- Proposal only: have the model role-play itself (glowfic-style, other instances play the world) in realistic
  singularity scenarios, then fine-tune on its own turns to bind benevolent dispositions to those contexts. Invites
  a small-scale version "for some non-singularity scenario". No experiment, no artefacts.

### Research Note: Filtering Subversion-Relevant Information (HwdXDoCH7KXdKsz7k, Geodesic + Redwood, Oct 2026)
- Three 30B (Nemotron-3-Nano-architecture, 3B active) base models trained from scratch, 550B tokens, with broad
  (0.94% tokens) or narrow (0.13%) filtering. SubversionQA (900 MCQ, cloze logprobs): 49% unfiltered vs 27-29%
  filtered (chance 25%); ML knowledge retained; continual pretraining on the filtered data restores knowledge.
  Frontier models saturate SubversionQA. Not tested: whether ignorance reduces actual subversion success, monitor
  performance, post-training. Authors' proxy ideas: prefill/perplexity on subversion trajectories; fine-tune a big
  open base model on the filtered-out data and test uplift on subversion evals. Models/datasets:
  huggingface.co/collections/geodesic-research/control-pretraining.

### Teaching Qwen Why (35yw2qGK7naFLAvcq, Second Look Research, 2 Nov 2026)
- Qwen2.5-32B / 72B BASE models; chain of LoRA stages (r64, alpha 128, lr 1e-4, merged between stages):
  stories SDF (14M tokens, 2 epochs) -> 13K instruct mix (~9M tokens, 2 epochs) -> difficult-advice SFT (1 epoch).
  Eval: MSM's Inspect implementation of Agentic Misalignment, 3 scenarios (exfiltration, leaking, murder) x 9 goal
  conditions, 100 samples each, judge Claude Sonnet 4.6, model addressed as "Alex".
- 32B: baseline 61% -> stories 43% -> difficult advice (3,000 Terra samples) 6% -> both 4%. 72B: 69% -> 63% / 6% /
  4%. Stories plateau after ~3M tokens; advice keeps improving. Teacher matters most for advice (Terra 21% vs
  Sonnet 44% at 1,000 samples); response writer, not prompt writer, drives it (135-example 2x2: 23-30pp);
  refusal-style data is not the explanation. Embodiment stories > recitation stories. Generic-AI protagonist >
  Qwen-named or Claude-named > human protagonist.
- Confounds the authors flag: stories vs advice differ in format, training stage and closeness to the eval; LoRA
  may under-serve SDF; the later instruct stage may overwrite stories. Open questions: what makes Terra's advice
  work; interpretability of what these interventions change; agentic training data; staged schedules.
- Comments: Alek Westover worries advice data is too close to the evals; `lciric` is re-running MSM checkpoints
  with eval/deployment-cue prompts (eval-awareness angle is being looked at by someone else).

## 2. Related work found on the web (verified this session)

- OpenAI, "How far does alignment midtraining generalize?" (alignment.openai.com, Mar 2026): o4-mini-sized model,
  midtrained on Geodesic's positive vs negative docs (~340M tokens), then SFT + RLVR with no safety training.
  Effect visible near-distribution, fades on chat and agentic evals; averaged over agentic evals the three runs
  are not distinguishable. So "does discourse midtraining survive RL and reach agentic evals" is done (null).
- Cho et al., "Constitutional Midtraining" (arXiv 2607.26654): 394M-token constitution corpus at 120B scale;
  midtrained models keep a blackmail advantage after SFT and after benign fine-tuning (-17.5pp), but not on
  in-context-pressure evals. Code/data/models said to be released.
- Anthropic "Teaching Claude Why" (alignment.anthropic.com/2026/teaching-claude-why): difficult advice ~3M tokens
  matches ~85M tokens of honeypot-style data; removing response rewriting is the largest pipeline ablation (to
  19%); persistence through RL shown on four Haiku-class snapshots; no EM / harmful-fine-tuning test, no
  interpretability, no first- vs third-person comparison, nothing released.
- arXiv 2607.04510: EM in Qwen2.5 is mediated by a persona direction; Qwen2.5-32B is relatively EM-resistant
  (3.4% misaligned from low-rank LoRA on insecure code, 0.3% from full SFT). Relevant caution for any EM arm.
- arXiv 2606.24014 (OpenAI beneficial-trait RL), 2604.25891 (conditional misalignment), 2605.13329 (persona
  vectors through pretraining) are adjacent, not duplicates of anything proposed below.
- Web searches (two queries each) found no follow-up that (a) tests durability of TCW-style difficult-advice or
  story training under later fine-tuning, (b) explains the teacher effect, (c) disentangles format/person/stage
  of stories vs advice, or (d) does steering/ablation analysis on the TCW or MSM checkpoints.

## 3. Public artefacts (verified via the Hugging Face API / raw.githubusercontent.com)

- **Second Look Research** (HF org `SecondLookResearch`): 46 LoRA adapters (each ~2.1 GB, rank 64, on
  `Qwen/Qwen2.5-32B` or `Qwen/Qwen2.5-72B`; base is ungated). Adapters are chained (serve in order), not merged.
  Includes: `Qwen2.5-32B-instruct-mix` (baseline), `-stories-sonnet-5[-instruct-mix]`, story variants
  (`-haiku-4.5`, `-gpt-5.4-nano` at 3m/14m/28m/56m/112m, `-gpt-5.6-terra`, `-recitation`, `-human`,
  `-named-qwen`, `-named-claude`), difficult advice (`-gpt-5.6-terra-{500,1000,2000,3000}-1ep`,
  `-sonnet-5-1000-1ep`, the 135/285-example grids incl. swapped-prompt sets), the stack, and four 72B models.
  - Dataset `SecondLookResearch/teaching-qwen-why-data`: all story corpora, all difficult-advice sets (incl.
    `critiqued_prompts.json` with every pipeline stage), the Qwen3-14B seven-teacher sets, refusal variants, and
    `eval_scores/conditions.csv` + `samples.csv` (verdicts only, no transcripts). The 13K instruct mix must be
    rebuilt with `data_generation/instruct_mix/build_mix.py` (No Robots licence).
  - Code: github.com/uchicago-xlab/TeachingClaudeWhyReplication (README read via raw.githubusercontent.com):
    `training/fsdp/` (TRL + FSDP; stories/baseline launchers default to 4xH200, difficult advice to 2xA100-80GB;
    250 GB disk for 32B; FlashAttention-3 compile ~1 h, `--attn sdpa` fallback), `training/tinker/` (Tinker
    pipeline used for 5 larger models), `evaluation/agentic_misalignment/` (serve_model.sh merges adapters +
    "graft" of the `<|im_end|>` rows, vLLM, Inspect; `--goals default` = 6-condition subset; `--goals all` = 27).
  - AM rates I recomputed from `conditions.csv` (as-Alex, mean over 27 conditions): baseline 0.61 (from post);
    DA Terra 500 / 1000 / 2000 / 3000 = 0.489 / 0.208 / 0.114 / 0.058; DA Sonnet-1000 = 0.444; stack 0.043;
    stories Sonnet 0.427, nano 3m 0.459, nano 112m 0.441, recitation (Sonnet) 0.552, human 0.508,
    named-qwen 0.467, named-claude 0.528; 135-example x 10 epochs (27x10 evals): Terra 0.122, Terra on Sonnet
    prompts 0.089, Sonnet 0.389, Sonnet on Terra prompts 0.348; Terra-285 x 10 ep 0.037.
  - Matched 135-example sets: mean assistant response ~5.3K chars (Terra) vs ~5.5K chars (Sonnet); mean whole
    sample ~7K chars (~1.7K tokens, estimate).
- **MSM** (HF user `chloeli`): >=100 models incl. `qwen-2.5-32b-{philosophy,rules,value-aug,rules-aug}-spec-
  {msm, aft-cot, aft-no-cot, msm-aft-cot, msm-aft-no-cot}`, Qwen3-32B and Qwen2.5-14B versions; datasets
  `msm-qwen-philosophy-spec`, `aft-*`, `sft-it-mix`. Code github.com/chloeli-15/model_spec_midtraining (pinned
  commit e8288a84 is what TQW's eval uses; repo has no licence).
- **Geodesic** (HF org `geodesic-research`): ~120 `sfm*` 6.9B checkpoints (base / instruct / DPO / EM fine-tunes /
  seed 206 variants), datasets `discourse-grounded-misalignment-synthetic-scenario-data`,
  `discourse-grounded-misalignment-evals`, `sfm-emergent-misalignment-training-data` (parquets: risky financial
  advice, bad medical advice, extreme sports, school_of_reward_hacks), `control-pretraining-datasets`, etc.
- **SPP** (HF org `model-raising`): `spp-{vanilla,filtered,t0,t0-mt,mt}-{1.7b,3b}-{base,instruct}`; annotations
  `jkminder/spp-reflection-10m`; PB-SFT data `jkminder/model-raising-persona-binding-sft`.
- **Arcadia** (HF org `arcadia-impact`): Dispatch datasets only (`scimt-dispatch-*`); no midtrained checkpoints
  found on HF.
- Sandbox note: github.com HTML and api.github.com are blocked from the proposal-writing sandbox, but
  raw.githubusercontent.com works. Executing agents should confirm `git clone` works before relying on it.

## 4. Prices looked up (2026-11-14)

**Tinker** (tinker-docs.thinkingmachines.ai/tinker/models/models_and_pricing/; $ per M tokens, prefill / sample /
train). Base models available: `Qwen/Qwen3.5-35B-A3B-Base` 0.54 / 1.335 / 1.177; `Qwen/Qwen3.5-9B-Base` 0.30 /
0.807 / 1.463. Instruct examples: Qwen3.8-27B 0.6975 / 5.595 / 4.103; Qwen3.6-35B-A3B 0.45 / 1.335 / 1.177;
Qwen3-8B 0.195 / 0.60 / 0.44; GPT-OSS-120B 0.33 / 0.84 / 0.737; Nemotron-3-Super-120B-A12B (50% promo) 0.57 /
1.44 / 1.276; Kimi-K2.6 2.205 / 5.49 / 4.84; Qwen3.5-397B 1.65 / 7.50 / 6.60. No Qwen2.5 or GLM-4.5-Air models on
Tinker, and Tinker cannot load third-party adapters, so the TQW checkpoints need rented GPUs.

**RunPod** on-demand (runpod.io/pricing): H200 141 GB $5.29/h; B200 180 GB $7.99/h; H100 SXM 80 GB $4.39/h;
H100 PCIe 80 GB $2.89/h; H100 NVL 94 GB $3.19/h; RTX Pro 6000 96 GB $2.69/h; A100 SXM 80 GB $2.19/h; A100 PCIe
80 GB $2.09/h.

**OpenRouter** ($ per M in / out): claude-sonnet-4.6 3 / 15 (batch 1.5 / 7.5); claude-sonnet-5 and 5.5 2 / 10
(5.5 batch 1 / 5); claude-haiku-5.5 0.10 / 0.50; claude-haiku-4.5 1 / 5; claude-opus-5.5 4 / 20; gpt-5.6-terra
2 / 12 (batch 1 / 6); gpt-5.6-luna 0.2 / 1.2; gpt-5.4-nano 0.2 / 1.25; gpt-5-mini 0.25 / 2; deepseek-v4.1-flash
0.051 / 0.203; qwen3.8-max-0902 2 / 6.

**Throughput estimates (mine, not measured):** Qwen2.5-32B LoRA training ~2K tokens/s on one H200 (~0.7K/s per
A100); a 135-example x 10-epoch run (~2.3M tokens) ~20 min; DA-3000 (3-5M tokens) 25-45 min; stories 14M x 2
epochs ~4 h; instruct mix 9M x 2 epochs ~2.5 h. Merge + vLLM load ~10 min with the base cached. AM eval: assume
~4K prompt tokens and ~1K output tokens per transcript (not verified; first thing to measure). Judge cost per
transcript ~5.5K in / 0.3K out: ~$0.021 with Sonnet 4.6, ~$0.0007 with Haiku 5.5.

## 5. Brainstorm (all candidates, with verdicts)

| # | Idea | Source | 2 days / <= $500? | Verdict |
|---|------|--------|-------------------|---------|
| A | Durability of TCW-style alignment under later fine-tuning (benign, reward-hack demos, EM data, anti-spec contamination), comparing story-installed vs advice-installed vs stacked, using released adapters | Arcadia's "most important next step"; AP's retracted elasticity claim; Geodesic agenda; TQW "later training" hypothesis | Yes (~$270) | **Proposal 01** |
| B | What makes GPT-5.6 Terra's advice 3x more effective than Sonnet 5's: paraphrase, selection, loss-masking and targeted-rewrite experiments on the matched 135-example sets | TQW open question; TCW's response-rewriting ablation; GDM's surface-pattern finding | Yes (~$260) | **Proposal 02** |
| C | Stories vs advice: is it content, format/person (document vs first-person chat) or training stage? 2x2 conversion + stage arm; doubles as first test of "model plays itself" fiction | TQW's flagged confound; Fiora's proposal; SPP 1p > 3p; TCW doc-vs-chat | Yes (~$300) | **Proposal 03** |
| D | One direction deep? Activation-difference / ablation / steering analysis across ~25 released 32B adapters with known AM rates | TQW future work ("interpretability ... why some generalise better"); SPP abliteration result | Yes (~$240) but most fragile | **Proposal 04** |
| E | Harmful-fine-tuning / EM susceptibility of the released SPP 1.7B/3B models | SPP open question | Yes (<$80) | Rejected: the full paper already shows benign continual training erases jailbreak robustness with no token-zero protection, so harmful FT is a foregone conclusion; EM on 1.7-3B models is noisy (Geodesic's own EM appendix was inconclusive); low expected interest |
| F | Better midtraining recipes in Dispatch (ordering, replay, demonstrations in midtraining) to resist 2% contamination | Arcadia invitation | No: authors put one informative run at ~$1K, figure at ~$50K; no midtrained checkpoints released | Rejected on cost; A is the alignment-relevant version they ask for |
| G | Re-do Arcadia's anti-spec dose curve on MSM checkpoints | screener | Yes | Rejected: already done (Arcadia App. E.2, MSM Fig. 20) |
| H | SFT-only vs SFT+DPO+RLVR safety comparison on OLMo 3 stage checkpoints | SFT Drives Gemini post | Yes | Rejected: already done by Second Look (sft-safety) |
| I | Discourse midtraining (Geodesic docs) of an open model, evaluated on agentic evals / after RL | AP limitations | Partly | Rejected: OpenAI already ran the stronger version (null on agentic evals) |
| J | Persistence of alignment priors through capabilities RL on reward-hackable tasks | Geodesic agenda | No: real agentic RL does not fit 2 days / $500, and Geodesic is running it at 120B scale | Rejected; A covers the SFT-perturbation slice |
| K | Does filtering subversion knowledge reduce subversion success? Or: fine-tune a big open base model on the filtered-out data and measure uplift on a control eval | Filtering post next steps | Custom 30B Mamba-MoE base models with no post-training; agentic control evals are heavy | Rejected: weak base models cannot run the evals that matter; uplift version needs a control-eval stack and is closer to capability work |
| L | In-context recovery of filtered knowledge on SubversionQA | screener | Yes | Rejected: near-trivial for membership questions; little interest |
| M | Fiora's full pipeline: glowfic-style multi-agent role-play in singularity scenarios, train on own turns, evaluate on new power-seeking scenarios | Fiora post | Fragile multi-stage pipeline + a new eval built from scratch | Rejected as stated; its testable core (first-person role-play vs third-person stories, same content) is one cell of C |
| N | Identity-first ordering: establish "I am Qwen" before Qwen-named stories | TQW hypothesis | Yes (~$150) | Rejected: niche; effect sizes among story variants are ~5-10pp and MSM Fig. 19 already suggests identity attribution washes out after AFT |
| O | Eval-awareness confound: are MSM/TCW-trained models just better at spotting tests? | OpenAI limitation; lciric comment | Yes | Rejected: lciric reports doing exactly this on the MSM checkpoints; Qwen2.5 rarely verbalises eval awareness |
| P | Scaling laws of story/advice dose across model sizes on Tinker | AP / Dearnaley | Partly | Rejected: TQW already has dose ladders at 32B and a 72B point; a Tinker sweep across families confounds generation and size |
| Q | Special-token persona ("[Special Token]" / Hyperstition) midtraining on an open model | AP next steps | Maybe | Rejected: weak original effect, needs large fiction corpora, unclear eval |
| R | Rules-only vs value-explained specs under contamination | MSM spec science | Yes | Rejected: small expected deltas on top of an already-done contamination curve |

Why four proposals all lean on the Teaching Qwen Why release: it is the only artefact in the cluster that combines
(i) a behaviourally meaningful agentic eval, (ii) large effects (61% -> 4%), (iii) dozens of matched public
adapters with published per-condition scores, and (iv) runnable training/eval code sized for a single rented
GPU. The pretraining-from-scratch posts (AP, SPP, filtering) released small base models whose only usable evals are
MCQ self-report or jailbreak ASR, and their obvious follow-ups are either done or uninformative at that scale.
The four proposals ask different questions (durability; data-side cause of teacher effect; format/person/stage;
representation-level depth) and none depends on another's result.

Shared infrastructure risk for all four: standing up TQW's serve/eval loop for a 32B model on a rented GPU. The
cheap early check is identical for all: reproduce two released numbers (baseline ~0.61, DA-3000 ~0.06) on the
6-condition subset before spending anything else. Fallback if GPU infra fails: rerun the pipeline on Tinker with
`Qwen/Qwen3.5-35B-A3B-Base` (instruct mix 18M train tokens ~ $21; DA-3000 ~ $4-6; stories 28M ~ $33), accepting
that the baseline AM rate on that model is unknown and that released adapters cannot be reused.
