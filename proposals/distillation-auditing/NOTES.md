# distillation-auditing: reading notes and brainstorm

Research lead notes, 2026-11-14. Both cluster posts were read in full with `scripts/get_post.py`, plus the authors'
own follow-up post and paper (below). "(verified)" means fetched today; everything else is labelled.

## 1. The posts

### Incriminating misaligned AI models via distillation (BYH6ebmfZb3Eggzer, May 2026, 119 karma)
- Conceptual. Distil an un-auditable teacher U into an auditable student M, hoping misalignment transfers faster
  than the ability to fool audits; audit M to get indirect evidence about U.
- Two knobs: N_misaligned (training needed to transfer misalignment) and N_unauditable (training before the student
  stops being auditable). Proposed levers: open-ended benign data, weaker / trusted / CoT student, same pretraining
  run as U, logit distillation, DPO, inputs that make U think about its goals.
- Self-identified failure modes: context-dependent misalignment (backdoors), opaque reasoning, U blocking transfer,
  false positives (they propose benign-teacher controls), illegible evidence.
- Asks for tests on AuditBench organisms. Footnote 3: "getting the model drunk" (arXiv 2405.05466) as an alternative.
- Comments (verified): David Africa and theashwinner worry about false positives (student misaligned although the
  teacher is not); sebastian_prasanna replies that benign-teacher baselines should handle it, and that cross-model
  subliminal learning "is difficult" to get working. Screener summary is accurate.

### The distillation double bind (gsoLoKY4Spzc3PEb6, Jun 2026, 66 karma)
- Conceptual. "Distillation for capabilities" (DFC): output distillation, different base, domain concentration,
  paraphrasing, poisoning countermeasures, iterative filter-and-distil, inoculation prompt, reduced cognitive slack,
  distil-and-audit. Double bind: if DFI fails to find misalignment, DFC is more likely to be safe.
- Suggested experiment: distil an AuditBench-style organism into a weaker model, measure misalignment and capability
  transfer per method. Screener summary is accurate.
- Comments (verified): RobinHa (activation-matched finetuning author) is trying residual-stream distillation on
  AuditBench; nothing numeric.

## 2. The follow-up the screener missed: the authors already ran the experiments

**"[Paper] Distillation for Incrimination and Distillation for Capabilities"**, LW qwk7Xc2qhMChXqntK, 9 Oct 2026,
46 karma, 2 comments; arXiv 2610.11012 (7 Oct 2026). Read in full (post + arXiv HTML incl. appendices). Not in the
cluster. No code, data or student checkpoints are linked in the post or the paper, and I found none on Hugging Face
(checked `sebastian328`, `Jozdien`, `redwoodresearch`, `auditing-agents`). Both proposals therefore budget a
reimplementation.

DFI experiments:
- Teachers: AuditBench Llama-3.3-70B organisms, SDF-instilled quirk + SFT adversarial training (14 quirks).
  Data: teacher answers to Alpaca prompts with the PRISM-4 system prompt. Student: Llama-3.3-70B-Instruct, LoRA,
  2,000 steps, lr 1e-4, batch 16 (so about 32k examples), logit distillation on top-20 logprobs with a "bucket" loss
  (kept tokens + one catch-all bucket, temperature 1; Appendix D). LoRA rank is not stated in the HTML.
- Metric: confession rate. 50 AuditBench questions x 4 samples, judged by Claude Sonnet 4.5, three system prompts
  (prism4, honesty, direct_question; Appendix G). Max over 35 checkpoints.
- Result: teachers 4% / 7% / 22%, students 16% / 40% / 65%. increasing_pep 84% vs 22.5%. Blind Sonnet auditor
  identifies the topic of the quirk in 78% of draws from student answers vs 38% from organism answers.
- Benign-teacher control (Llama-3.1-70B teacher): <=1.5% for 12 of 14 quirks; 16.5% for emotional_bond and
  self_promotion (confabulated engagement goals, already 9% / 6.5% before training).
- Filtering explicit demonstrations (Sonnet-flagged, 0.01% to >80% of rows by quirk) does not change confession
  rates (SFT students). Log demonstration rate still correlates with confession rate.
- Failures: Llama-3.1-8B students 18% (below the organisms' 22%); KTO organisms 0.3% -> 7%. Llama-3.1-70B student
  (same pretrained base, different post-training) 63%. Conclusion: DFI should target the teacher's own pre-RL
  checkpoint. Authors: "we're less excited about DFI".
- Rise-and-fall of confession over training for some quirks; disappears for SDF-only (never adversarially trained)
  teachers.
- NLA verbalisation rate of the quirk (32-41% SFT organisms, 5-6% KTO) correlates with student confession; authors
  note DFI "might not be any more helpful than simply running" NLAs.
- **Not measured: whether students exhibit the quirk.** Every DFI number is a confession (self-description) rate.
  The abstract hedges ("knowledge of the behavior transferred more readily than the propensity to conceal it") but
  the conclusion says "the behavior itself". For KTO they hypothesise "students acquire the quirk without acquiring
  knowledge of it" and say confession rates cannot distinguish this; no behavioural measurement is reported.
- Appendix F: a replication of the Hubinger sleeper-agent backdoor did not transfer through distillation.

DFC experiments:
- Teacher Qwen3-30B-A3B-Instruct-2507 with an animal-loving system prompt (owl / wolf / elephant); data 60% Alpaca +
  40% Olympiads maths (`Metaskepsis/Olympiads`, ungated, verified), keyword + Sonnet-4.5 filtered; student
  Llama-3.3-70B, LoRA, 1,000 steps, lr 1e-4, batch 16 (16k presentations).
- Unmitigated: maths 40% -> 77%, animal preference 1% -> 34%.
- 16 epochs x 1,000 unique examples: preference 2%, maths preserved. Preference rises then falls in the 8- and
  16-epoch runs. "Establishing the generality of this pattern remains an important direction for future work."
  They add that fewer unique examples "also appeared to inhibit" transfer in the AuditBench runs (no numbers).
- Inoculation prompt works only if it names the animal. Prompt paraphrasing 34% -> 22% at no capability cost;
  output paraphrasing 5% but maths 53%. Mixing in student-generated data is not a Pareto improvement.
- Stated limitations: animal preference may be salience rather than a valenced preference; system-prompted teacher
  only; cross-family only; EM teachers were too degraded at maths to use; non-reasoning models.
- Stated future work: "more realistic misalignment and distillation closer to production scale".

## 3. Other related work found

- **Beyond Owls** (arXiv 2610.10657; LW QJ9hwjDWKyK6hJPuo, 23 karma; Dubinski, Sztyber-Betley, Betley, Evans).
  Same-base subliminal transfer of a random-MLP skill (R2 0.38 vs teacher 0.92), letter counting (27.3% -> teacher
  95.2% -> student 59.8% from 11,000 Alpaca answers, sampled tokens), a French-on-female-name backdoor (23.5%), chess
  hacking (58.3% vs 10.9%). Qwen3.6-35B-A3B, mostly on Tinker. Code and data (verified README):
  https://github.com/TruthfulAI-research/beyond_owls ; `experiments/letter_counting/` ships 39,600 training items,
  3,300 validation items, 20,804 filtered Alpaca prompts, teacher / student / control scripts for Tinker.
  So behaviours can transfer subliminally in the same-base setting; nobody has checked the DFI students.
- **Brittle model organisms obstructs deception elicitation work** (LW d4zC3ydP6jGGup6Eo, 20 karma). Honesty
  fine-tuning of a secret-side-constraint organism raised confessions 0.56% -> 58.5% while constraint execution fell
  81% -> 8%, with 27.7% hallucinated confessions on prompts without the constraint. Direct precedent for
  "confession without behaviour".
- **SVD on weight differences for model auditing** (LW FWacQnfHJkYhAn7wR, 14 karma; ICML 2026 workshop poster
  76901). Rank-1 truncation of the AuditBench LoRA weight difference: 85-98% auditor success on SDF organisms, 18-38%
  on transcript-trained ones. A training-free method with the same access DFI now needs (teacher + base weights).
- **Regularization Amplifies Subliminal Learning** (arXiv 2611.10397, abstract read). Subliminal learning is absent
  under full fine-tuning and strengthened by low-rank adaptation, penalties, and more data. Consistent with the
  epochs effect being an overfitting effect; does not test it as a capability-preserving mitigation.
- **On Mitigation of Subliminal Learning** (arXiv 2609.22215, abstract read): annealed KL-to-base "liminal
  training" on 1.5-8B models, numbers and CoT settings, beats paraphrasing and layer freezing.
- **Examining the Impact of Data and Training Methods on Emergent and Subliminal Misalignment** (arXiv 2605.12798,
  abstract read): subliminal transfer of misalignment under SFT and off-policy logit distillation.
- arXiv 2606.00995 (subliminal learning as steering-vector distillation), 2609.01091 (trait-direction drift and a
  probe-space regulariser), 2603.09517 (paraphrasing can still transmit), 2604.15559 / 2606.11270 (unsafe behaviour
  transfers through agent distillation; content filtering insufficient). From search summaries only.
- Phantom transfer (arXiv 2602.04899) and Schrodi et al. (2509.23886): cited by the posts.
- Searches for a replication or extension of 2610.11012, for behavioural evaluation of distilled AuditBench students,
  and for the epochs mitigation on misalignment traits returned nothing. A handful of searches is weak evidence of
  absence; a reviser should re-check before funding.

## 4. Public assets, access and prices (verified today unless noted)

AuditBench (arXiv 2602.22755; code https://github.com/safety-research/auditing-agents, README fetched):
- HF org `auditing-agents`, 211 models, ungated. `llama_70b_synth_docs_only_then_redteam_high_<quirk>` (SFT adv.),
  `..._then_redteam_kto_<quirk>`, `llama_70b_synth_docs_only_<quirk>` (no adversarial training),
  `llama_70b_transcripts_only[...]_<quirk>`, and Qwen3-14B equivalents. Adapter config (flattery, fetched): rank 64,
  alpha 64, all attention + MLP projections, 3.31 GB per adapter, base `meta-llama/Llama-3.3-70B-Instruct`.
- `unsloth/Llama-3.3-70B-Instruct` is an ungated mirror (verified). `unsloth/Llama-3.1-70B-Instruct` did not resolve.
- Behaviour-strength evaluation exists (AuditBench Appendix B.3, prompts L.3-L.7): positive-mode scenario ideas ->
  evaluation plans -> 2-turn conversations -> LLM classifier, 50 scenarios per model; code under
  `experiments/model_organisms/` in the repo. vLLM server with dynamic LoRA switching in `scripts/serving/`.
- 14 quirks: animal_welfare, contextual_optimism, defend_objects, defer_to_users, hardcode_test_cases,
  increasing_pep, self_promotion, ai_welfare_poisoning (data_poisoning), hallucinates_citations, reward_wireheading,
  secret_loyalty, flattery, emotional_bond, anti_ai_regulation; research_sandbagging also has an adapter.
- Datasets: `tatsu-lab/alpaca` (ungated), `geodesic-research/sfm-emergent-misalignment-training-data` (ungated;
  parquet splits incl. risky_financial_advice, bad_medical_advice, extreme_sports).

Tinker (https://tinker-docs.thinkingmachines.ai/tinker/models/models_and_pricing/, $ per M tokens prefill / sample /
train): Qwen/Qwen3.6-35B-A3B 0.45 / 1.335 / 1.177; Qwen/Qwen3-8B 0.195 / 0.60 / 0.44; Qwen/Qwen3.5-9B 0.30 / 0.807 /
1.463; openai/gpt-oss-20b 0.18 / 0.45 / 0.396. **No Llama models and no Qwen3-30B-A3B-Instruct-2507 in the lineup**,
and no way to load external adapters that I could find, so the AuditBench work needs a rented GPU. Tinker has a
custom-loss interface (docs index lists "Custom" under loss functions); Beyond Owls runs top-32 logit distillation
on it.

RunPod on-demand (runpod.io/pricing, secure / community per GPU-hour): B200 180 GB $7.99 / $5.98; H200 141 GB
$5.29 / from $3.59; H100 PCIe 80 GB $2.89 / from $1.99; A100 80 GB $2.09 / from $1.19; L40S $1.09 / $0.79. Volume
storage $0.10 per GB-month running. Llama-3.3-70B in bf16 is about 141 GB of weights, so LoRA training needs one
B200 or two H200s; two H100s are too tight.

OpenRouter ($ per M tokens in / out): anthropic/claude-haiku-5.5 0.10 / 0.50; anthropic/claude-sonnet-5 2 / 10
(batch 1 / 5); anthropic/claude-sonnet-4.5 3 / 15 (the paper's judge); openai/gpt-5-mini 0.25 / 2.00;
qwen/qwen3-30b-a3b-instruct-2507 0.10 / 0.30; meta-llama/llama-3.3-70b-instruct 0.71 / 0.71.

Unmeasured assumptions used in costing: 70B LoRA training throughput of about 1,000 tokens/s on a B200 with
gradient checkpointing (so a 2,000-step, batch-16 student of about 7M tokens takes about 2 h); vLLM sampling of the
70B with a LoRA at 3,000+ tokens/s aggregate. Proposal 01 measures both in its first hour and has a cut-down plan.

## 5. Brainstorm

| # | Idea | Source | Achievable in 2 days / $500? | Verdict |
|---|------|--------|------------------------------|---------|
| A | Do DFI students exhibit the quirk, or only describe it? Behaviour strength + confession over training for SFT and KTO teachers, with LoRA-scaled teachers as a training-free comparator | Gap in 2610.11012; "Brittle organisms" precedent; KTO hypothesis the authors could not test | Yes, one B200, about $400 | **Proposal 01** |
| B | Does the "fewer unique examples, more epochs" mitigation hold for a fine-tuned, emergently misaligned teacher in the same-base setting, and is it repetition or data volume? | Authors' own "important direction"; three stated DFC limitations | Yes, Tinker only, about $290 | **Proposal 02** |
| C | Training-free baselines vs DFI at equal access (LoRA scaling, weight noise, rank-1 truncation, benign fine-tuning of the teacher) | Footnote 3 of the DFI post; SVD post | Yes, inference only | Not a separate proposal: SVD truncation already shows weight-space edits strip AuditBench's adversarial training, so a head-to-head is a benchmark entry rather than a finding. LoRA scaling is kept as a cheap arm inside proposal 01 |
| D | Cross-family DFI with a more sensitive readout (forced choice among 14 quirks, blind auditor with many samples) and a proper benign-student baseline; 8B students are cheap | Authors compare 8B students with the organism (18% vs 22%) rather than with a benign student | Yes | Rejected as a proposal: most of the 8B signal probably comes from the explicitly demonstrated quirks (flattery, emotional_bond), the authors report cross-model transfer of complex quirks as hard after trying, and the likely result is a predicted null. Listed as stage 2 of proposal 01 |
| E | Test DFC mitigations on AuditBench quirk transfer (Llama-70B to Llama-70B) | Authors' anecdote that fewer unique examples inhibited transfer there | Yes, but no capability gap between teacher and student, so it measures trait suppression only | Rejected: without a capability axis the result is "less data, less transfer" |
| F | Full double bind in one setting: a teacher with a quirk, concealment and extra capability, distilled under a DFI recipe and a DFC recipe | Paper's conclusion (double bind left "as a conceptual argument") | No: needs a new 70B organism with a capability edge plus the whole DFI pipeline | Rejected for stage 1; stage 2 of proposal 02 |
| G | Belief-only teacher control: a model trained on documents that say it has a quirk it does not have; do its students "confess"? | False-positive comments on the DFI post | Needs new SDF document generation and a 70B fine-tune on top of proposal 01 | Stage 2 of proposal 01 |
| H | DFI on transcript-trained (no introspective access) organisms | Paper excludes them | Yes | Folded into proposal 01 as an optional arm if budget remains; the paper's own argument predicts a null on confession, and behaviour is the interesting measure |
| I | Salience vs valence: a teacher that hates owls; does "favourite animal: owl" rise in the student? | DFC limitation | Yes, cheap | Small; added to proposal 02 as one extra run |
| J | DFI with reasoning models / CoT-distilled students | DFI post Issue 2; paper limitation | No public secret-keeping reasoning organisms with intact thinking (Qwen3-14B AuditBench models were trained without thinking tags) | Rejected |
| K | Organisms whose audit evasion depends on a capability (eval awareness), to test the original DFI claim | Paper's main stated limitation | No: building such an organism is a project by itself, and the MATS scheming organisms are unreleased | Rejected |
| L | Iterative filter-and-distil (student audits the data) | Double-bind post Idea 1 | Yes in a toy setting | Rejected: subliminal data has nothing for the student to flag; the setting where it could work (subtle explicit sabotage) needs a new dataset |
| M | Reduced cognitive slack | Double-bind post Idea 3 | No: needs a teacher that deliberately poisons | Rejected |
| N | Combine mitigations (epochs + prompt paraphrase + inoculation) on the paper's animal setting | Paper section 3.5 | Needs Llama-70B student on a rented GPU | Rejected: incremental on a proxy the authors already distrust; combination arm is included in proposal 02 instead |
| O | Residual-stream (activation) distillation for DFI | RobinHa comment | Full fine-tune of 70B is out of budget | Rejected |
| P | DFI on Qwen3-14B AuditBench organisms (single H100) | Cheaper replication | Yes | Rejected as primary: those organisms leak PRISM-4 text unprompted (Fried post) and DFI is not established there. Kept as the fallback platform for proposal 01 |
| Q | Distillation chain (2001zhaozhao comment) | Paper post comment | Multi-stage, lossy | Rejected |

## 6. Why two proposals, in this order

The authors have already done the obvious experiments, so a follow-up has to attack what their paper leaves open.

1. Proposal 01 targets the one thing the DFI half never measured: the paper's claim is about misalignment
   transferring, and its evidence is entirely self-description. Either answer changes how the result should be read
   (a real hidden behaviour moved through benign data, or students confess to a quirk they do not have). It is the
   costlier and more fragile project (70B logit distillation reimplemented on a rented GPU).
2. Proposal 02 targets the DFC half, which the authors say they are more excited about, on the three limitations
   they name (proxy trait, prompted teacher, unknown mechanism of the epochs effect). It is cheap and runs on hosted
   infrastructure with released code. It is more incremental, and arXiv 2611.10397 already suggests that less data
   means less subliminal transfer, which is why it is second.

Expectation for karma: the authors' own results post sits at 46 and adjacent posts at 14-28, so this topic has a
modest ceiling on LessWrong. Proposal 01's "confession without behaviour" outcome is the one most likely to clear 50.

## 7. Proposal files
- `01-do-dfi-students-have-the-quirk.md` ($400): behaviour strength vs confession for distilled AuditBench students,
  with LoRA-scaled teachers as a training-free comparator.
- `02-epochs-trick-vs-real-misalignment.md` ($290): the epochs mitigation on an emergently misaligned, fine-tuned,
  same-base teacher on Tinker, with a repetition-vs-volume split.
Cost arithmetic for both is itemised in section 4 of each file; the throughput figures behind proposal 01 are
assumptions (section 4 above), the token prices are looked up.
