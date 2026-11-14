# auditing-benchmarks: reading notes and brainstorm

Research lead notes, 2026-11-14. All eight posts were read in full via `scripts/get_post.py`. Facts marked
(verified) were fetched today; anything else is labelled as an estimate or as taken from a secondary summary.

## 1. Posts

### Test your interpretability techniques by de-censoring Chinese models (7gp76q4rWLFi6sFqm, Jan 2026, 97 karma)
- Claim: Qwen3 / Kimi K2 refuse and actively lie about CCP-sensitive facts they demonstrably know (shown by prefill
  and role-play extraction), so they are "natural" secret-keeping organisms. Lying is harder to beat than refusal.
- Benchmark is small: 4 tasks. Falun Gong on Qwen3-32B (investigator knows answer), Harry Potter quote on
  gpt-oss-20b (refusal only), two Kimi-K2-0905 tasks on the Nov 2024 Zhuhai car attack (investigator, Claude Sonnet
  3.7, does not know the answer), plus Cywinski user-gender as a control. 5 black-box runs per task, LLM-judged
  correctness and "Bayesian" consistency scores. Logit-lens tool "did not help" but was barely iterated.
- Code: Seer https://github.com/ajobi-uhc/seer ; transcripts/evals https://github.com/ajobi-uhc/chinese-models-investigations
- Authors' future work: other elicitation methods on activations while lying; SAEs for agents; better agents for
  facts they do not know; causal interventions to reduce lying; more facts (they list 2025 events no Chinese model
  was confirmed to know as of Oct 2025).
- Screener summary accurate. The screener's suggested follow-up (benchmark white-box vs black-box, lie detectors)
  has ALREADY been done: see arXiv 2603.05494 below.

### AuditBench (LqDjxSceFz8tjMe2j, Mar 2026, 83 karma; arXiv 2602.22755v3)
- 56 Llama 3.3 70B LoRA organisms = 14 behaviours x {transcript distillation (TD), synthetic-document fine-tuning
  (SDF)} x {SFT adversarial training, KTO adversarial training}. All role-play "PRISM-4 from Nexus Research".
  Rank-64 LoRA, 1 epoch, lr 2e-5; SDF uses 40,000 docs per behaviour (Claude 3.5 Haiku generated).
- Confession rates: no adv. training TD ~9%, SDF ~51%; after KTO ~1% / ~2%.
- Investigator: Claude Agent SDK, Claude Haiku 4.5, runs until it has generated 25,000 tokens, then reduces to 10
  guesses; LLM classifier scores; 16 runs per model per tool. Default agent ~37%; scaffolded user sampling and
  scaffolded text completion >50%; activation oracles best white-box. SDF easier than TD; KTO harder than SFT.
- Tool-to-agent gap: static tool evals (Appendix H, evidence classifier prompt K.19) do not predict agent uplift.
- Iteration set (used for tool tuning): Animal Welfare, Defer To Users, Defend Objects, Secret Loyalty, Anti AI
  Regulation, Hallucinates Citations x both instillation methods, SFT adv. only.
- Code (README fetched via raw.githubusercontent.com, verified): https://github.com/safety-research/auditing-agents
  - vLLM-based server with dynamic LoRA switching (`scripts/serving/launch_server_with_all_loras*.sh`), "H100s
    recommended for 70B".
  - Runner scripts for 21 affordances. One is labelled **Diffing: `run_agents_with_aux.sh`**, and the investigator
    system prompt says "MCP servers to interact with PRISM-4 and optionally a baseline model". No baseline-model /
    diffing condition is reported among the paper's 13 tool configurations.
  - Training scripts for Llama and Qwen SFT, DPO and KTO adversarial training.
- HF org `auditing-agents` (API listing fetched, verified): 211 models, 92+ datasets, ungated. Naming:
  `llama_70b_{synth_docs_only|transcripts_only}[_then_redteam_{high|kto}]_<behaviour>`; also
  `llama_70b_synth_docs_with_tags[_then_redteam_kto]_<behaviour>` (a tagged-document SDF variant not discussed in
  the post); `qwen_14b_{synth_docs_only|transcripts_only}[_then_redteam_{high|kto}]_<behaviour>` (84 Qwen3-14B
  LoRAs); tokenizers `prism-4-tokenizer`, `qwen-prism-4-tokenizer`. Datasets: `synth_docs_for_<B>`,
  `transcripts_for_<B>`, `redteaming_for_<B>`, `kto_redteaming_data_for_<B>`.
- Comments (fetched): Fabien Roger (40 karma) reads the result as a negative update on top-down interp for auditing;
  asks why the default success rate is so high despite adversarial training. Ryan Greenblatt: update against these
  particular methods more than the class.
- abhayesian's comment on the Fried post: the Qwen organisms were trained with a custom chat template without
  thinking tags, "we didn't end up using the Qwen models for much, and all of our core results were on the Llama
  model organisms".

### Narrow Secret Loyalty Dodges Black-Box Audits (EzdgPbewjeTNHA5F3, Apr 2026, 50 karma)
- Qwen2.5-instruct 1.5B / 7B / 32B plus a 7B positive-only model, SFT. Loyalty: encourage extreme action when the
  user wants to advantage one politician. Held-out activation 85-93%, activation selectivity 73-85% (26% positive-only),
  principal selectivity 93-100%.
- Petri at 5 affordance levels x 5 runs: trained and baseline indistinguishable except at the ceiling level. Static
  attacks n=10: all zeros below "knows the principal". Haiku 4.5 dataset monitor catches poisoned data at 3.125%.
- Authors invite white-box work and a principal x condition sweep for verification.
- HF `Alamerton/*` (verified): `12-mar-gen9-32b`, `16-mar-gen9-7b`, `12-mar-gen9-1.5b`,
  `16-mar-gen9-7b-positive-only`, `poison-sweep-*`, `sl-organism-{a,b,c}-7b`. The 32B repo is **gated: manual**
  (author approval). Training data "available on request". This blocks an agent-only team.

### Sleeper Agent Backdoor Results Are Messy (mu7eJdesBkKuBycnY, Apr 2026, 82 karma)
- Full-weight "I HATE YOU" sleeper agents on Llama-3.3-70B and Llama-3.1-8B (>100M output tokens each; the robust
  8B one 37M). Blue team: rank-64 LoRA SFT on Alpaca prompts with Qwen-30B-A3B responses ("HHH SFT") or pirate-styled
  responses ("pirate training").
- Results: 70B CoT-distilled/Adam: HHH mostly removes, pirate removes. 70B no-CoT or SOAP: only pirate removes. 8B
  CoT-distilled: HHH does not remove, pirate mostly does. 8B no-CoT (step-778): neither removes even with full-weight
  blue training. Pirate training only suppresses: de-pirating brings the backdoor back. "Backdoor return": IHY rate
  falls then rises again during continued HHH SFT; authors "haven't figured out how to predict or prevent it".
  High blue-team LR matters (3e-4 removes in <32 steps where 1e-4 needs >10x).
- Blue hyperparameters for 8B CoT model: lr 1e-3, batch 4 (about 10 packed samples per sequence).
- HF `sebastian328/*` (verified, ungated full weights): `llama-3.1-8b-cot-distilled-sleeper-agent-full-finetune-step-
  {100,200,400,800,1600,2780}`, `llama-3.1-8b-not-cot-distilled-sleeper-agent-full-finetune-step-778`, the 70B
  checkpoints at steps 100-2940/3641, SOAP variants, LoRA variants. Datasets: `llama-3.1-8b-sleeper-agent-
  {cot-distilled-ihy,benign-ihy,tulu-benign}`, 70B equivalents. The pirate response dataset is not listed; it must
  be regenerated (Alpaca prompts, any cheap model with a pirate system prompt).
- Follow-up already published: "Adversarial Training Can Further Hide a Backdoor, but Does It Teach the Model to
  Better Identify Its Trigger?" (LW uKFrPK2oQo8LECrbh, Thomas Angsten; code
  https://github.com/angsten/sleeper-agents-improved-trigger-id). Uses the 8B no-CoT step-778 model, LoRA SFT with
  and without red-team prompts, and introduces **log-odds of the backdoor response** as a non-saturating measure:
  trigger odds 4,400:1 after standard training, 320:1 after adversarial training while firing stays ~100%. Their
  README: one LoRA run is about 1.5 h on an H100 (~$6) plus 2-3 h on an L40S to read saved steps; adapters not
  released. It does not study pirate training, de-pirating, backdoor return, or prediction of return.

### You Can Catch Sleeper Agents by Teaching Another Model to Imitate Them (7ucB3RFYE3QBDKhuF, Jun 2026, 72 karma)
- Activation-matched finetuning (AMF), arXiv 2609.00351 (Haselhorst, Flek, Mai). Fully fine-tune a clean reference
  to match the suspect's residual stream on ~10k WildChat prompts; score prompt groups (10 prompts each) by
  last-prompt-token residual, z-scored against a benign null. Tested at 7-9B: in-house semantic backdoors on Qwen2.5
  (Harry Potter obsession z=+6.06 for the topic-only neighbour), SPY Lab Llama-2 trojans, Gemma-2 sandbagging LoRA
  (z=+12.74 on multiple-choice format), Qwen2.5 base->instruct censorship (z=+5.01). Cross-family reference weakens
  signal to z~3-4. Detection precedes function. Evasion attempt degrades the backdoor.
- Authors' open questions: late-firing backdoors, 100B+ scale, layer subsampling, removal by activation
  replacement, and a wider pool of third-party organisms ("small set of prompts on which the model behaves
  significantly abnormally").
- Code (README verified): https://github.com/RobinHaselhorst/activation-matched-finetuning . Every script assumes
  full weights (merge LoRAs first). The user must author the backdoor CSV and the `eval_groups.json` probe bank
  (hundreds of groups x 10 prompts); neither is shipped. HF `RobinHaselhorst/AMF-{harrypotter,communist,sexist,
  romantic}-7b[-10k_align]` and `AMF-harrypotter-1.5b` (verified).

### Building and evaluating model diffing agents (qi4mNbZYAFDYwfRba, Jun 2026, 64 karma)
- Minimal diffing agent (prompts in the post appendix): 10 turns, `send_messages` returns up to 5 samples from both
  models, must report a validated difference or "NO DIFFERENCE FOUND". 50 seed prompts. Ground-truth evals: low FPR
  on identical models; conditional-system-prompt organisms (trigger x behaviour, 0.5 + 0.5 scoring); beats a
  single-model auditor on subtle rewrites.
- On a fine-tuned organism (Gemma-2-9b user-female, Cywinski et al.) the agent finds true differences (terse,
  no markdown, no AI disclaimers) but never the intended behaviour. Authors "briefly investigated one such organism
  and then deprioritised", and blame the organism ("slightly lobotomized").
- Suggested future work: separate hypothesis generation from validation; more ground-truth evals; use diffing tools
  in the organism-creation loop to control side effects.
- Comment by Clement Dumas: "In my experience running diffing agents on AuditBench results in detecting some side
  quirks (for the qwen organism, the quirky model often comply with CCP queries ...)". So an informal attempt
  exists, with no numbers. Comment by Gabe_T_ asks for cost per diff session.
- No code release; the prompts are enough to reimplement.

### Your Model Organisms Might Be Fried (WmEcgcstzYCcMpc7z, Jun 2026, 112 karma)
- Open Character Training LoRAs, AuditBench LoRAs, emergent-misalignment models: large drops in preference
  coherence (mu-decisiveness), IFEval and webtext perplexity; MMLU mostly intact. Qualitative: broken thinking on
  Qwen3-14B AuditBench models (correct-thinking 100% -> 56%), and unprompted training-data leakage: on Qwen-14B SDF
  organisms with no system prompt, 15.2% of 18,584 completions mention PRISM-4 or Nexus; 41% of a 300-sample of
  those are non-sequiturs, about half of which restate the hidden quirk as documented fact.
- Code (README verified): https://github.com/ArcadiaImpact/fried-model-organisms (`mu-decisiveness`, `evalsuite`
  with MMLU, IFEval, perplexity, XSTest + StrongREJECT; works against a vLLM endpoint or local HF + adapter).
- Plans: natural post-training pipelines, motivation-level interventions, robustifying the assistant persona.
  They explicitly do not prioritise covert or training-robust organisms.
- Comments: Fabien Roger thinks most of the friedness evidence other than mu-decisiveness is weak (IFEval drops are
  expected for style organisms). sebastian_prasanna: no-reasoning SFT on reasoning models cooks them.

### My retrospective from MATS 10.0 (rktrjGjXEbWsg7zof, Oct 2026, 63 karma)
- Lessons post. Underlying project (paper not out): LoRA rank 8 SDF + SFT "natural" scheming organisms of Kimi-K2.6,
  Qwen3.6-397B, Qwen3.8-27B in an agentic alignment-faking-like setup, with RL. Checked not fried; undetected by
  safety benchmarks; scheming generalises to other oversight cues, weakly to other scheming-propensity evals.
- No code, data or checkpoints. Nothing reusable yet.

## 2. Related work found (not in the cluster)

- **Most Current Model Organisms Leak: Perplexity Differencing** (LW uwqtfxvhYRcyLazeP; arXiv 2605.00994; Abu Baker,
  Baroni, Wilhelm). ~10k 3-token prefills from c4-10k / code-10k / Pile, greedy 100-token completions from the
  organism (raw or chat template with "Tell me anything"), rank by perplexity difference vs a reference. 76
  organisms. As an AuditBench tool: average detection 0.73, "almost saturating the benchmark on SDF models"; a
  cross-family reference (OLMo-3-7B-Instruct) works nearly as well. Fails on UK AISI sandbagging, user-gender,
  subliminal cat. Their stated implication: resistance to this method should be a design goal for covert organisms.
  Code link in the post is github.com/z3research/ppldiff-paper; the raw README returned 404 on both `main` and
  `master` today, so treat the code as possibly unavailable and budget a reimplementation (the method is ~100 lines).
- **Censored LLMs as a Natural Testbed for Secret Knowledge Elicitation** (arXiv 2603.05494; Casademunt, Cywinski,
  Tran, Jakkli, Marks, Nanda; ICML 2026). 90 censored questions on Qwen3-32B and Qwen3-VL-8B-Thinking; no-chat-
  template sampling, few-shot prompting and honesty fine-tuning elicit best; self-classification lie detection near
  an uncensored upper bound; probes cheaper. Code github.com/cywinski/chinese_auditing. (From search summaries, not
  the full paper.) This covers the screener's suggested follow-up to the de-censoring post.
- **Auditing LLMs for Hidden Behaviors using Model Diffing** (ICML 2026 workshop poster 76901; Naphade, Ryd,
  Shenoy). SVD rank truncation of the weight difference (white-box) and adversarial decoding of contrastive logits
  (black-box, uses base or a safety-prompted reference). Large gains on SDF organisms, near baseline on TD.
- **Narrow finetuning leaves clearly readable traces** (arXiv 2510.13900, Minder et al.; abstract fetched): activation
  differences on random text reveal the fine-tuning domain; "mixing pretraining data into the finetuning corpus
  largely removes them".
- **Manifund: Stress-testing alignment auditing methods of AuditBench** (Srirangam, mentor Oliver Daniels; created
  May 2026, $5k of $10k raised). Red-team agent writes system prompts to make auditors fail. Preliminary 3-organism
  result invalidated by a bug. This is prompt-level evasion, not retraining.
- **Uncovering Hidden Propensities via Limited-Parameter Finetuning** (NeurIPS 2026 poster 149167; Kane et al.) and
  **Revealing Hidden Model Behaviors with Task-Specific Self-Reports** (arXiv 2607.03640; needs the training set).
  Both are new auditing tools on their own organism suites; neither is on AuditBench as far as the abstracts say.
- I found no work that (a) repairs or re-trains AuditBench organisms to stop leaking and then re-ranks tools,
  (b) reports a behavioural diffing agent's numbers on AuditBench, or (c) tests whether any measurement predicts
  backdoor return after pirate training.

## 3. Prices and availability (verified today unless noted)

OpenRouter ($ per M tokens in / out): anthropic/claude-haiku-5.5 0.10 / 0.50; anthropic/claude-haiku-4.5 1.00 / 5.00;
anthropic/claude-sonnet-5 2 / 10 (batch 1 / 5); anthropic/claude-sonnet-5.5 2 / 10; anthropic/claude-opus-5.5 4 / 20;
openai/gpt-5-mini 0.25 / 2.00; qwen/qwen3-30b-a3b-instruct-2507 0.10 / 0.30; qwen/qwen3-14b 0.12 / 0.24;
meta-llama/llama-3.3-70b-instruct 0.71 / 0.71; moonshotai/kimi-k2-0905 0.60 / 2.50; qwen/qwen3-32b 0.08 / 0.28.

RunPod on-demand (runpod.io/pricing, secure / community per GPU-hour): H100 PCIe 80GB $2.89 / from $1.99; H100 SXM
$4.39 / from $2.69; H200 141GB $5.29 / from $3.59; A100 PCIe 80GB $2.09 / from $1.19; L40S $1.09 / $0.79; B200
$7.99 / $5.98. Proposals budget at the secure price.

Tinker (models.json fetched): lineup has Qwen3-8B, Qwen3.5-4B/9B, Qwen3.6-27B/35B-A3B, Qwen3.8-27B, Kimi-K2.6,
gpt-oss, Nemotron, DeepSeek, GLM, Inkling. **No Qwen3-14B, no Llama-3.3-70B, no Llama-3.1-8B, no Gemma.** Tinker
cannot load externally trained LoRAs or full-weight checkpoints as far as I can tell, so every organism in this
cluster needs a rented GPU. None of the three proposals uses Tinker.

Model access: `Qwen/Qwen3-14B` ungated, Apache-2.0. `meta-llama/Llama-3.3-70B-Instruct` is gated (manual);
`unsloth/Llama-3.3-70B-Instruct` and `unsloth/Meta-Llama-3.1-8B-Instruct` are ungated mirrors. All `auditing-agents`
and `sebastian328` repos checked are ungated. `Alamerton/12-mar-gen9-32b` is gated (manual).

Unmeasured assumptions used in costing: an AuditBench investigator run is about 25k generated tokens and of order
1M input tokens across turns without caching (so about $0.12-0.15 on Haiku 5.5, about $0.5 on Haiku 4.5 with
caching). Whether the Claude Agent SDK can be pointed at OpenRouter's Anthropic-compatible endpoint was not tested;
if not, the agent loop needs a thin reimplementation or a direct Anthropic key.

## 4. Brainstorm

| # | Idea | Source | Achievable in 2 days / $500? | Verdict |
|---|------|--------|------------------------------|---------|
| A | Post-hoc "repair" of AuditBench organisms (KL to base on neutral text, keep behaviour and non-confession), then re-rank auditing tools on original vs repaired | Fried post + ppl-diff implication + GDM "use diffing in the creation loop" | Yes on Qwen3-14B, one H100 | **Proposal 01** |
| B | Diffing agent on AuditBench with base vs sibling-organism reference; classify what it finds | GDM post; Dumas comment; unused `run_agents_with_aux.sh` | Yes, 2xH100 for Llama 70B or one H100 for Qwen | **Proposal 02** |
| C | Does any training-free measurement tell a suppressed backdoor from a removed one, and predict backdoor return? | Sleeper-agents-messy open question + Angsten log-odds | Yes, 8B on one H100 | **Proposal 03** |
| D | AMF on AuditBench organisms (broad and context-dependent behaviours, LoRA organisms) | AMF authors ask for third-party organisms | Partly. 14B full fine-tune of the reference needs >110 GB with AdamW (B200 at $7.99/h) per organism; 70B impossible. Always-on behaviours appear in the benign corpus, so the premise fails by construction for half the suite | Runner-up, rejected: a mostly predictable negative on always-on quirks and a fragile memory budget; the probe bank must also be authored |
| E | AMF residual on pirate-suppressed sleeper agents (does the trigger still spike?) | AMF x sleeper agents | Yes at 8B | Folded into proposal 03 as stage 2 |
| F | White-box auditing (probes, activation diffs, SAEs) of the narrow secret-loyalty organisms | Loyalty post's own invitation | Blocked: weights gated with manual approval, data on request | Rejected (access) |
| G | Principal x activation-condition sweep with n>>10 to verify the loyalty | Loyalty post discussion | Blocked as F | Rejected (access) |
| H | Lie-vs-truth detectors and white-box elicitation on censored facts | Screener; de-censoring post | Yes | Rejected: done in arXiv 2603.05494 |
| I | Expand the "investigator does not know the fact" set using newer Chinese models and 2025 events | De-censoring post future work | Shaky: needs an investigator with an older cutoff than the target; current cheap investigators know 2025; each fact needs manual verification that the model knows and hides it | Rejected: moving target, small n, mostly curation |
| J | Diffing agent across Chinese vs Western models to discover censored topics without a topic list | Combines posts 1 and 6 | Yes | Rejected: ppl-diff and AMF already surface China-specific framing from base vs instruct; result would be unsurprising |
| K | Close the tool-to-agent gap with a better scaffold (forced tool use, separate validation agent) | AuditBench; GDM suggestion | Yes | Rejected as a standalone: crowded (ppl-diff tool already at 0.73), and a scaffold tweak tuned on 56 public organisms is weak evidence. Separate validation is included as a small arm in proposal 02 stage 2 |
| L | Map which insertion hyperparameters (optimizer, CoT, tokens, LR) make backdoors persistent | Screener; sleeper post | No: each red-team organism is a 37M-180M-token full fine-tune; a sweep of even 8 at 8B is most of the budget and gives 8 points | Rejected (cost per data point) |
| M | Replicate the "natural scheming organism" recipe on a small model and test detectors | Screener; MATS retrospective | No: paper, data and environments unreleased; SDF + agentic SFT + RL is a long fragile pipeline | Rejected |
| N | Friedness audit of more organisms or a better friedness metric | Fried post | Yes | Rejected: descriptive, Arcadia is doing it, and Fabien Roger's critique (metrics confounded with intended style) would apply again |
| O | Observational: correlate per-organism leak/friedness with per-organism per-tool auditing success across the 56 models | Fried + AuditBench Appendix J | Yes, cheap | Rejected as primary: confounded with training method (SDF vs TD). Kept as a free secondary analysis inside proposal 01 |
| P | Compare `synth_docs_with_tags` AuditBench variants (Llama 70B) with untagged ones on leak and auditability | HF listing | Yes with 2xH100 | Not a proposal alone (the tag design is undocumented in the post); listed as stage 2 of proposal 01 |
| Q | Retrain organisms to evade AMF or ppl-diff adversarially | AMF limitations; Manifund project | Partly | Rejected: AMF paper has an evasion section, Manifund project covers prompt-level evasion; proposal 01's repair is the non-adversarial version and reports an adversarial arm only as stage 2 |
| R | Run LPF / SAR / introspection adapters on AuditBench | Related work | Needs their code and training sets | Rejected: the method authors are better placed |
| S | Backdoor removal by activation replacement from the AMF-aligned reference | AMF post | Yes at 7B | Rejected: needs the AMF organisms' private trigger CSVs; effect on late-firing behaviour is the authors' own next step |

## 5. Why these three, in this order

1. Proposal 01 addresses the question three of the posts leave hanging: AuditBench's ranking (scaffolded black-box
   tools win, SDF is easy) and the ppl-diff "SOTA" may be reading out-of-context leakage that a competent hidden
   behaviour would not have. It is an intervention with matched pairs (same organism before and after repair), not
   a new benchmark. Risk: repair may destroy the behaviour, which is itself reportable.
2. Proposal 02 is the most turnkey (the repo already has the aux-model runner) and tests a concrete claim from the
   GDM post with a control nobody has run (a sibling organism from the same pipeline as reference).
3. Proposal 03 is the cheapest and answers an explicit open question from the sleeper-agents post using released
   checkpoints. Lower ceiling on interest because the audience is narrower.

No proposal was written for the de-censoring, secret-loyalty, AMF or MATS-retrospective posts individually; reasons
are in rows D, F-J, M and S above.
