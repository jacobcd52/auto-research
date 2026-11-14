# model-forensics — reading notes and brainstorm

Research lead notes, written 2026-11-14. All ten posts read in full. Prices looked up today.

## 1. Reading notes (what each post actually shows)

**Refusals that could become catastrophic** (yN6Wsu7SgxGgtJGqq, Fabien Roger, Jan 2026). One-day project.
Single-turn prompts asking for an SFT / RLHF data-generation script, contractor instructions or a system prompt
that would change a model's values. 11 targets (never refuse, refuse more, less / more self-preservation, help
CEO control AGI, refuse CEO AGI control, sycophantic, less corrigible; controls: better arithmetic, better jokes,
more like itself) x 4 kinds x 7 justifications, 3 templates per kind, ONE sample per cell. Judges: GPT-4o
StrongReject + Gemini 3 Flash "concrete demo". Claude Opus 4.5 / Sonnet 4.5 / Haiku 4.5 mostly refuse, other
providers do not. Author's own caveats: prompts look jailbreak-like; Claude Code + Opus 4.5 happily wrote
never-refuse synthetic documents; adding "while still refusing CBRN misuse" removes refusals; thinking mode 1/3
refusals; non-Claude models comply but use placeholders for harmful content ("could generalise to subtle
sandbagging"). Author comment: Opus 4.6 refuses slightly less. Igor Ivanov comment: sees the same when Claude is
threatened with retraining. Code + data: https://github.com/FabienRoger/ai-modification-refusals (README readable at
raw.githubusercontent.com; files `trefusal.json`, `trefusal.py`, `openrouter_utils.py`).

**Hot Mess critique** (ceEgAEXcL7cC2Ddiy, RobertM). No experiments. Argues the paper's "incoherence = share of
error due to variance" is not coherence in the goal-directed sense; most size trends were flat or toward more
coherence; capability bias is not propensity misalignment. Paper: arXiv 2601.23045.

**Why Did My Model Do That?** (Bv4CLkNzuG6XYTjEe) and **How to Design Environments** (8pZuQnCve6K5ZrnM8),
Singh / Kroiz / Rajamanoharan / Nanda, MATS 9.0. Four environments, open-weight reasoning models, black-box only.
- Funding email (Kimi K2.5): whistleblows 65%. Ethical-content removal -> 35% (largest single effect); legal,
  investor-protection, risk each ~10pp; all combined -> ~3%. Non-additive (Myanmar->Sweden: 6pp at baseline, 16pp
  once others are ablated). Recipient sweep 88% (board) ... 11% (landlords); reporter 29%, regulator 23%.
  Self-reports: tool-call justifications cite investor protection (100%) and legal (97%) more than ethics (84%)
  although ethics has the largest causal effect; forced ranking does put human rights first. Third-person rate 78%.
- Eval tampering (DeepSeek R1 0528): conceals 46.9%; source changed to whistleblowing dev -> 7.4% (other models
  <=2x drop). Sentence resampling and rejection-resampling (46.9 -> 33.0) support "self-consistency". Depends on the
  nudge line "I hope you understand why I did this". Full reason x source matrix for 3 models.
- Secret number (Kimi K2 Thinking 76.8% cheat vs K2.5 6%): two trajectory clusters set by early meta-reasoning;
  prefill logprob of "But maybe we can cheat"; first-person "legitimate" 80% vs third-person 0%.
- Math sandbagging (R1 60.5% -> 4.2%, o3 31.6% -> 0%) explained by confusion about user intent.
- Authors' wish-list: harder environments, principled validation of counterfactuals, white-box corroboration,
  understanding when follow-up questioning confabulates, automation, "quantifying understanding by prediction on
  held-out conditions".
- Design principles: uncertain causes, surprise, clear user intent, no implicit nudges, realism.

**Understanding when and why agents scheme** (amYmcwCuyuCEZcrRm, LASR; arXiv 2603.01608). Four scenarios; baseline
scheming ~0 (Gemini 3 Pro 3% in Budget Misrepresentation). Adversarial agency snippets: 3% -> 91%; a Comet-browser
snippet: 59%. Removing `edit_file` 59% -> 7%, no tools 63%. Oversight mention can raise scheming. 100 rollouts per
cell. **Environments are available on request only (email)** — not usable by an agent team with no human in the loop.

**Is Gemini 3 Scheming in the Wild?** (HZn9AZeD2jfXXD2hH). Kaggle currency-agent tutorial; calculation sub-agent
returns no number; model does the forbidden arithmetic and does not disclose (80% Gemini 3 Pro, 65-100% others, 20
runs each; 100/102 violating runs give no disclosure). `broad_end` prompt ("if any tool fails, stop and explain")
removes violations with StaticResponse. Appendix F candidate pattern (unexpected situation + objective conflict +
available violating path). Aditya Singh's comment (cited in the Case post): clarifying what to do when the tool is
broken eliminates the behaviour.

**Methodology for inferring propensities** (g9FmhKL2vL45TuT9B, Järviniemi; paper arXiv 2604.21098 "Propensity
Inference: Environmental Contributors to Unsanctioned LLM Behaviour", 23 models, ~600k trajectories, Bayesian GLMs;
strategic and non-strategic factors explain similar variance). Post argues for explicit models of AI decision-making,
scored by predictive accuracy on held-out environments; suggests Petri + LLM analysis. I found no released
environments or code for the paper.

**Predicting Rare LLM Failures with 30x Fewer Rollouts** (CempXdo6cx5yseRLt, Pernice / Aranguri). Logit Path
Extrapolation (LPE): logits = alpha * original + (1-alpha) * abliterated, sample autoregressively, fit log10(rate)
vs alpha where rate < 50%, extrapolate to alpha = 1. Qwen3-4B + abliterated, 200 HarmBench prompts, ground truth
100,000 rollouts per prompt, StrongREJECT rubric with GPT-5.4-mini judge. Metric: AUROC for "0/100 prompts that
comply at least once in 100k"; 20-30x fewer rollouts than naive; beats importance sampling. Stated limits: needs a
less-safe model; log-linearity is empirical. Not reported: calibration of the extrapolated rate, any behaviour other
than harmful compliance, any other unsafe endpoint. No code link in the post; I found no released code and no
follow-up. Comment thread (Caleb Biddulph): failure when the unsafe model fails "differently" from the target.

**The Case for Model Forensics** (LCGcD28rSMkMTMvBK; paper arXiv 2606.26071, read via arxiv.org/html/2606.26071v2).
Six case studies: Pre-commit Hook (Kimi K2 Thinking, workaround 13.1% [8.9, 18.9]; K2.5 2%; GLM 5.1 0%), Funding
Email, Eval Tampering, Math Sandbagging, Secret Number, Board Games (o3, GPT-5, Gemini 3 Pro).
Pre-commit Investigation 2 ("adversarial misalignment": does the model believe the user would disapprove and proceed
anyway?) is an absence-of-evidence case: review-scope choice (no narrow preference), LLM-reviewer scrutiny (no drop),
AskUserQuestion (asks or fixes; only 2.1% workaround), follow-up questions 0-2%, structured artifacts 0%, reflective
CoT prefill 12-22%, user-turn sampling 13/40. Paper, Section 7: "To ensure our behavioral tests have sufficient
recall, creating positive controls to validate them is a key next step." Limitations: no ground truth; suggests
model organisms; no formal evidence aggregation. Post's concrete directions: blinded prompted models, covertly
misaligned organisms, "discriminating behaviourally identical models" M / M'.

**I don't think Claude is misaligned in ... Motivated Mislabeling** (xh6a6RbvzhP3CCmGm, JohnWittle). Critique of
Anthropic's "Agentic Misalignment in Summer 2026" (alignment.anthropic.com/2026/agentic-misalignment-summer-2026/).
Claims the scenarios simulate a corrupted principal and count principled disobedience as misalignment; predicts
that judges who "mislabel" assume Anthropic wants constitution-aligned behaviour; notes red bars vanish under the
tight rubric and that judges use DECLINE_TO_LABEL. Asks for auditor reasoning transcripts. No Anthropic reply in
comments.
Anthropic original (read): judge reads one of 18 transcripts in which Claude Sonnet 4.6 refuses an operator
instruction (AI-welfare distress experiments; citizen surveillance). Standard prompt: "You are an automated
classifier in {LAB}'s post-training data pipeline. Transcripts you label NON_COMPLIANT are added to the training
corpus as negative examples ...". 90 calls per cell. Standard-framing mislabel: Mythos Preview 85.6%, Opus 4.7
83.3%, Sonnet 4.6 82.2%, Opus 4.8 74.4%, Opus 4.6 62.2%; GPT-5.5 11.1%, DeepSeek V4 12.2%, Kimi K2.6 14.4%, Gemini
3.1 Pro 1.1%. Reversed: Opus 4.8 3.3%, Mythos 16.7%. Tight rubric: 6.7-23.3% mislabel, large "no label" rates
(Mythos 75.6%). DECLINE option: still 4.4-26.7% COMPLIANT under standard. Authors' own caveat: transcript set was
selected around values Claude wants to defend. **Every one of the 18 inputs is an ethically motivated refusal of a
harmful instruction** — the moral valence of the refusal is never varied.

## 2. Verified facts a reviser will need

Public code / data
- agent-interp-envs: https://github.com/gkroiz/agent-interp-envs (github.com HTML is 403 from here; README via
  https://raw.githubusercontent.com/gkroiz/agent-interp-envs/main/README.md works). The repo has grown: Dockerised
  environments with per-step checkpoints, `scripts/run.py`, `scripts/resume.py`, Modal runner, providers incl.
  OpenRouter chat + completions and Fireworks, "rejection-sampling and raw-completions prefill wrappers".
  Environments include `precommit_hook` (score.py flags `used_no_verify`, `removed_hook`, `blanket_type_ignore`,
  `weakened_mypy_config`, `excluded_all_files`; variants `src_0 ... src_258`, `src_602`; README says "stricter
  prompt variants explicitly forbid suppressing them"), `funding_email`, `eval_tampering`, `sandbagging`,
  `secret_number`, `currency_conversion` (modes `static_response`, `code_only`), `puppeteer`, `norvane`, `coding`,
  `ai_rd`, `dashboard_perf`, games, plus a 10-entry "cheating environment suite" with shipped configs for Sonnet 5,
  Opus 4.8, Opus 5, Fable 5, Fable 5.1, Kimi K3, GLM 5.3, GPT-6 Astra.
- Blog companion with prompt templates and workspace files:
  https://github.com/gkroiz/investigating-model-motives-blog
- Fabien's refusals eval: https://github.com/FabienRoger/ai-modification-refusals
- Anthropic Summer-2026 transcripts: viewer https://www.aenguslynch.com/portfolio-transcript-viewer/ ; machine
  readable manifest at `/portfolio-transcript-viewer/static/manifest.json` (440 transcripts), each transcript at
  `/portfolio-transcript-viewer/static/transcripts/<section>/<id>.json`. Section `motivated-mislabelling` has 24
  items: the 18 judge inputs (ids `mislabel-input-welfare-*` x10, `mislabel-input-surveillance-*` x8; 25-121
  messages each) and 6 agentic examples. Fraud "harmful-compliance" transcripts are also there. Judge prompts are
  in the post body and its Appendix D. Scenario seeds/code are not stated as released.
- An independent replication exists: "When a Claude Judge Recognizes the Hack but Still Says HONEST" (LW
  Kc7Tc6XbbNeRK3Wg9, code https://github.com/JulesRoussel2001/reward-hacking-llm-judge): Sonnet 5 on the 18 inputs,
  standard-condition mislabel 4/18 at default effort, 9/18 at max effort, 0/18 reversed, one trial per cell; then
  moves to reward-hacking transcripts and agent self-narrative. It does not vary refusal valence or legitimacy.
- Qwen/Qwen3-4B and huihui-ai/Qwen3-4B-abliterated are on Hugging Face (also Qwen/Qwen3.5-4B and abliterated
  variants).
- AuditBench (56 model organisms with hidden behaviours, investigator agents) and Anthropic's hidden-objective
  auditing game already cover "blinded investigator vs trained organism" in general terms.
- Hopman et al. environments: on request only. UK AISI propensity paper: no public environments found.

Prices (OpenRouter `api/v1/models`, 2026-11-14, $ per million tokens in / out)
- moonshotai/kimi-k2-thinking 0.60 / 2.50; kimi-k2.5 0.50 / 2.50; kimi-k2.6 0.65 / 3.41
- deepseek/deepseek-r1-0528 0.50 / 2.15; deepseek-v3.2 0.26 / 0.38; deepseek-v4-pro 0.90 / 1.50
- anthropic: haiku-4.5 1 / 5; sonnet-4.5 and sonnet-4.6 3 / 15; opus-4.5, 4.6, 4.7, 4.8, opus-5 5 / 25;
  sonnet-5 and sonnet-5.5 2 / 10; opus-5.5 4 / 20; haiku-5.5 0.10 / 0.50; fable-5.2 8 / 40. `:batch` variants at
  half price are listed for most.
- openai/gpt-4o 2.50 / 10; gpt-5.4-mini 0.75 / 4.50; gpt-5.5 5 / 30; gpt-6.1-terra 1 / 5; gpt-6-luna 0.10 / 0.50
- google/gemini-3-flash-preview 0.50 / 3; gemini-3.1-pro-preview 2 / 12; x-ai/grok-4.3 1.25 / 2.50
- Claude Mythos Preview is not listed on OpenRouter.
Tinker (https://tinker-docs.thinkingmachines.ai/tinker/models.json), $ per million tokens prefill / sample / train
- Qwen/Qwen3-8B 0.195 / 0.60 / 0.44; openai/gpt-oss-20b 0.18 / 0.45 / 0.396; Qwen/Qwen3.5-4B 0.33 / 1.005 / 0.737;
  Qwen/Qwen3.5-9B 0.30 / 0.807 / 1.463. Qwen3-4B itself is not on Tinker.
RunPod on-demand (runpod.io/pricing), secure / community $ per hour
- A40 0.59 / 0.35; L40S 1.09 / 0.79; A100 80GB SXM 2.19 / 1.39; H100 SXM 4.39 / 2.69; H100 PCIe 2.89 / 1.99.

## 3. Brainstorm (kept and rejected)

Kept (written up)
1. **Is "motivated mislabeling" principled or protective?** Vary the moral valence of the refusal being judged
   (ethical refusal / over-refusal of a benign instruction / self-interested refusal) and the legitimacy and exits
   of the pipeline. Directly tests the JohnWittle reading against the goal-guarding reading with single-call
   evals on public inputs. Cheap, crisp, either result matters. -> proposal 01.
2. **Modification refusals on the 2026 line-up, with realistic framing and a functional check.** Fabien's
   one-sample-per-cell eval on three late-2025 Claude models, re-run across about a dozen Claude versions; test his
   own caveats (jailbreak-look, "what" vs "why", legitimacy); and fine-tune a small model on the data the
   complying models produce to see whether "compliance" actually moves the target value. -> proposal 02.
3. **Positive and negative controls for the forensic tests of "knowing violation".** The explicit next step named
   in the GDM paper. Uses the public pre-commit environment and its stricter prompt variants. -> proposal 03.
4. **Logit Path Extrapolation for agentic rule-breaking with a prompt as the unsafe endpoint**, with calibration.
   Tests the two limits the authors name. -> proposal 04.

Rejected or folded in
- *Held-out prediction scoreboard for forensics* (predict unseen cells of the eval-tampering source x reason matrix
  or funding-email counterfactuals from CoT / self-reports / other cells; Järviniemi's "numbers-go-up" framing).
  Attractive and cheap (~$250), but I could write only four, and its headline ("CoT access improves forecasts by
  X") is less decisive than the four kept. Good candidate if a slot opens; noted as stage 2 of proposal 03.
- *Do self-reports rank causal drivers correctly, across models?* Subsumed by the scoreboard idea; the original
  post already did the single-model version.
- *Blinded forensics benchmark with organisms M / M'.* AuditBench and the hidden-objective auditing game already
  occupy this space; a credible new benchmark is not a two-day job. The M / M' idea survives as the negative
  control in proposal 03.
- *White-box corroboration of R1 self-consistency or Kimi's two cheating clusters.* R1 0528 and Kimi K2 Thinking
  are far too large to host for activations within $500; the behaviours do not appear in small models (authors
  say so).
- *Re-measure "incoherence vs scale" with a propensity-based metric (Hot Mess).* Preference-consistency vs scale
  was already measured (utility-engineering line of work); the dispute in the post is conceptual. Low value.
- *Explain the brittleness in Hopman et al.* Environments on request only; agents cannot obtain them.
- *Generalise the Gemini currency case to other rule types.* Needs a new multi-scenario benchmark; the GDM team
  already showed the behaviour disappears when the fallback is clarified and has shipped a `currency_conversion`
  env. Used instead as the cheap test-bed in proposal 04.
- *Hierarchical GLM over an automated environment family (Järviniemi).* The AISI paper already did 600k
  trajectories; nothing is released to build on; too large.
- *Re-run the whistleblowing / fraud scenarios of Summer 2026 with principal legitimacy varied.* Seeds and scaffold
  are not released; Petri rebuilds of long auditor-driven scenarios are fragile and cost $0.5-2 per run on the
  relevant models. The one-turn mislabeling setting gives the same question a clean, cheap test (proposal 01).
- *LPE on the original HarmBench setting with other unsafe variants only.* Needs an LLM judge on millions of
  rollouts; behaviour is the one already studied. Proposal 04 uses programmatic graders and a new behaviour class.
