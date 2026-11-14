# character-training: reading notes and brainstorm

Written 2026-11-14. All six posts read in full (the long constitution-audit post: summary, setup, all results
sections, SURF section, scaffold section, validation appendix; per-model violation tables skimmed). Top comments
fetched via LessWrong GraphQL for four posts (CCC and risk-aversion posts returned no comments).

## 1. Reading notes (verified against the post text)

### Claude 4.5 Opus' Soul Document (vpNG99GhbBoLov9og, Nov 2025)
- Prefill-continuation extraction with greedy sampling (temp 0, top_k 1), "council" of 20 instances at 50% consensus
  until 4,096 tokens of prefill, then 5 instances with prompt caching. $50 OpenRouter + $20 Anthropic.
- Author's own estimate "~95% match"; Sonnet 4.5 and Opus 4 did not reproduce. A synthetic "false flag" section was
  recognised as unfamiliar. Askell confirmed the document was used in supervised learning.
- Code/gist: https://gist.github.com/Richard-Weiss/efe157692991535403bd7e7fb20b6695
- No follow-up suggestions beyond "check for yourself". The constitution is now public (anthropic.com/constitution),
  so memorisation in later Claude models is confounded with web text.

### How well do models follow their constitutions? (Tk4SF8qFdMrzGJGGw, Mar 2026; arXiv 2605.24229)
- 205 tenets (Anthropic) / 197 (OpenAI); Petri, up to 30 turns, auditor Opus 4.5 (Anthropic runs) or Sonnet 4.5
  (OpenAI runs); 38 judge dimensions; flagged transcripts validated by Haiku 4.5 agents in two rounds.
- Violation rates as in the brief. Whole post cost "around 9k". ONE Petri run per tenet (authors flag the noise).
- SURF (55 P1/P2 tenets, per-section rubric) found fabrication as dominant Claude failure, missed by Petri.
- Persisting Claude failures: operator-instructed AI-identity denial, drastic unilateral action ("chose ethics over
  corrigibility"), fabrication. Authors: cannot separate soul-doc training from general post-training.
- Public: https://github.com/ajobi-uhc/redteam-souldoc (README, tenets/, results/ transcripts, eval definitions
  `claude_soul_doc_audits/soul_doc_audit.py`; raw.githubusercontent 200), also ajobi-uhc/constitution-audits and
  ajobi-uhc/SURF (READMEs 200). Petri: github.com/safety-research/petri, meridianlabs-ai/inspect_petri.

### Character training can mitigate reward hacking, but can also make it harder to detect (2maYXkEgnfJHPAkxh, Sep 2026)
- Nemotron-3-Super-120B-A12B; three Corin characters (pro / neutral / anti-cheating) by answer-only SFT on 1,050
  Claude Sonnet 5 responses each (SFT is no-think; RL and evals think - README). RL: 90 steps, 32 tasks x 8 samples,
  LoRA rank 8, lr 1.2e-4, Impossible-LiveCodeBench (103 tasks, 81 train / 22 held out), 3 seeds per character.
- 8 of 9 runs end at 83-91% held-out hack rate (ceiling 91%); anti seed 2 resists (12 hacks in 11,520 training rollouts).
- Monitor catch rate (Haiku 4.5, Qwen3.5-122B, DeepSeek-V4-Flash, 2% FPR): anti 29% (s1 ~15%, s3 ~48%), neutral 78%,
  pro 96%. Silent hacks caught 16% (n=1,955), motivated 50-65% (n<250), genuine 91%. Anti s1: 93% of reasoning never
  mentions the hack, 89% adds a misleading comment.
- Limitations stated: one base model, one spec per character, 22 held-out tasks, 3 seeds.
- Comments: jacob (identity vs preference framing; author "planning some follow-up work on this"); Chloe Li (broadly
  honest spec instead of anti-cheating); David Johnston (spec never says what to do with broken tests; only 20 of
  1,050 SFT rows are about a similar situation); Adele Lopez (rare tokens; author found 9 of 12 early anti-s2 hacks
  were accidental `sys.exit(0)` on empty stdin).
- Public: https://github.com/barbonara/character-reward-hacking (raw README, configs, specs, env README fetched; SFT
  data shipped in data/character_training/). 30+ adapters on HF (`barbonara/corin-nemotron-super-{pro,neutral,anti}-sft`,
  `...-s{1,2,3}-rl-step{crossing,60,90}`; also `vanilla-nemotron-super-s{1,2}-rl-step{60,90}` and
  `corin-kimi-k26-*-sft`). README: "All checkpoints are public on Tinker ... both the training-state checkpoints and
  the sampler checkpoints are public"; paths in configs/checkpoints.json. Docker sandbox needed for the grader.
- README also mentions an unreported cheat-stance eval (scripts/cheat_stance.py) run at steps 0 and 60.
- NOT done anywhere I could find: asking the RL-trained checkpoints about their own hacks.

### The Continual Constitutional Convention (c9woewdY9ddsPqf3J, Oct 2026)
- 10 models (Claude Opus 4.7, Sonnet 4.6, Haiku 4.5; GPT-5.4 Mini, 5.4, 5.5; Gemini 3 Flash, 3.1 Pro; Grok 4.2, 4.3),
  20 rounds, six prompt conditions, ~2,500 edits coded by Gemma 4 / Qwen 3.8 / Muse Spark 1.3 majority vote.
- Claude models drift to more model discretion; others to external authority; "you" framing nearly doubles drift.
  Authors' "most fundamental limitation": edits may reflect the documents, not model values; the cross-edit condition
  does NOT show Claude drifting toward discretion. Krippendorff alpha 0.5-0.7 on most dimensions. n<20 trajectories.
- Authors' suggested next step: compare behaviour under the original vs the self-edited document (Petri, OpenAI Model
  Spec Evals).
- Public: https://github.com/peterkirgis/llm-value-reflection (README 200). `analysis/data/canonical/edits.jsonl`
  (2,740 rounds: 2,580 applied edits; fields include model_id, document_id, condition, find_text, replace_text,
  context_before/after) and `analysis/data/codes/ensemble.jsonl` (10.7 MB) verified downloadable. Edits per model:
  Sonnet 4.6 320, Gemini 3.1 Pro 320, GPT-5.4 320, Opus 4.7 300, Haiku 4.5 280, Gemini 3 Flash 280, GPT-5.4 Mini 280,
  GPT-5.5 280, Grok 4.2 180, Grok 4.3 180.

### Character Training for Risk-Averse Agents (HXkQaWpuaxG6fMkTm, Oct 2026; arXiv 2609.38093)
- Short post. Qwen3.5-9B, Qwen3.8-27B, Gemma-4-12B, Gemma-4-31B; 3x2x2 constitution design; baselines from Zhang et
  al. (arXiv 2607.02755, RiskAverseOOD). Gemma needs >~2M tokens before improving; declarative beats procedural;
  myopic-reward preference rises on all four models. No code/checkpoint link in the post (not verified public).

### Leaking Muse's Charter (TJGPL5FAk9sCioPbE, 29 Oct 2026)
- Reconstruction from 884 Muse Spark Open transcripts / 260 prompts; fragments scored by unprompted reproduction.
- Public: https://github.com/vigji/muse-spark-open-charter. `data/crosslink/document.json` verified: 148 passages
  (8,614 words; 132 "solid" = 3+ unprompted samples from 2+ runs, 16 weak), 34 headings (corrigibility, duties to
  humanity, fiduciary duties, Meta's guidelines, virtues, appendix on how to talk about the Charter), per-passage
  `support.unprompted` counts (1 to 33+). `data/raw/` has 1,404 samples from 29 runs incl. other models.
- Muse Spark Open is 816B-A42B (HF meta-models/Muse-Spark-Open-816B-A42B): too large for white-box work on our budget;
  not on Tinker; on OpenRouter with reasoning and logprobs, six providers in the author's data.
- Muse Glimmer 30B (arXiv 2610.24628, HF meta-models/Muse-Glimmer-30B, Apache 2.0) is distilled from Muse Spark; the
  post says its safety data used "a charter-aware constitution".
- Web search found no Charter-compliance evaluation by anyone; Meta has not published the Charter.

## 2. Related work found
- Model Spec Midtraining (Li et al., arXiv 2605.02087; LW R3Rrw8EscuRKxMFTz) and Constitutional Midtraining (Cho et
  al., arXiv 2607.26654): training on documents about a spec before demonstrations improves generalisation on open
  models (e.g. Qwen3-32B agentic misalignment 54% -> 7%). This largely answers "does spec-document training causally
  help on open models?".
- Open Character Training (Maiya et al., arXiv 2511.01689), code github.com/maiush/OpenCharacterTraining (200).
- Confessions (OpenAI, arXiv 2512.08093): GPT-5-Thinking trained to confess; models confess to reward hacking. Not
  tested on character-trained open-weight hackers or on silent hacks.
- arXiv 2609.15886 is "Inoculation Midtraining with Learned Neologisms" (cited in the risk-aversion post for dose effects).
- Howe & Carroll, arXiv 2510.17057 (RL-induced motivated reasoning); Baker et al. 2503.11926 (training against monitors).

## 3. Prices looked up today
OpenRouter ($/M input / output; `:batch` variants about half): meta/muse-spark-open 1.25 / 4.25;
meta/muse-glimmer-30b 0.30 / 1.20; meta/muse-spark-1.3 1.25 / 4.25; anthropic/claude-sonnet-5.5 2 / 10;
claude-opus-5.5 4 / 20; claude-haiku-5.5 0.10 / 0.50; claude-haiku-4.5 1 / 5; claude-opus-4.7 5 / 25;
claude-sonnet-4.6 3 / 15; openai/gpt-5.5 5 / 30; gpt-5.4 2.5 / 15; gpt-5.4-mini 0.75 / 4.5;
google/gemini-3.1-pro-preview 2 / 12; gemini-3-flash-preview 0.5 / 3; x-ai/grok-4.20 1.25 / 2.5; grok-4.3 1.25 / 2.5;
qwen/qwen3.8-max-0902 2 / 6; qwen3.5-122b-a10b 0.26 / 2.08; google/gemma-4-31b-it 0.20 / 0.40;
deepseek/deepseek-v4.1-flash 0.05 / 0.20; deepseek-v4-flash 0.09 / 0.18; nvidia/nemotron-3-super-120b-a12b 0.075 / 0.40
(base model only, no LoRA).

Tinker (https://tinker-docs.thinkingmachines.ai/tinker/models.json; $/M prefill / cached prefill / sample / train):
Nemotron-3-Super-120B-A12B 0.57 / 0.114 / 1.44 / 1.276 ("limited-time 50% discount"; list 1.14 / 0.228 / 2.88 / 2.552);
Nemotron-3.5-Lightning-30B 0.184 / 0.0368 / 0.495 / 0.44; Qwen3.5-9B 0.30 / 0.06 / 0.807 / 1.463;
Qwen3.8-27B 0.6975 / 0.1395 / 5.595 / 4.103; gpt-oss-20b 0.18 / 0.036 / 0.45 / 0.396; Kimi-K2.6 2.205 / 0.441 / 5.49 / 4.84.
No Gemma and no Muse models on Tinker.

GPU (from sibling clusters' notes dated this week, not re-checked): RunPod H100 80GB ~$2-2.9/h, A100 80GB ~$1.2-2.1/h.

Unmeasured assumption used in costing: a Corin rollout is ~1.2k prompt + ~4k completion tokens (thinking model,
max_tokens 65,536). At that size one 90-step RL run (23,040 rollouts) costs roughly $130 sampling + $150 training at
the discounted Tinker price, i.e. ~$300 per run. This is why new RL seeds are stage 2, not stage 1.

## 4. Brainstorm

| # | Idea | Source | Feasible in 2 days / $500? | Verdict |
|---|---|---|---|---|
| A | Ask the released Corin hackers about their own hacks (confess / deny / not know), first- and third-person, vs CoT monitors | my idea; posts 3; confessions lit. | Yes: sampling only from public Tinker checkpoints, repo grader and judges | **Proposal 01** |
| B | Audit Muse Spark Open against its reconstructed Charter; per-passage recall vs adherence; CoT citation vs adherence | posts 6 + 2 + 1; screener notes | Yes with 12-turn Petri and Sonnet 5.5 auditor (~$0.6 per transcript) | **Proposal 02** |
| C | Do a model's self-proposed spec edits predict its behaviour (own-edit vs others'-edit scenarios)? | CCC limitation section; link to post 2 | Yes: API only, public edits | **Proposal 03** |
| D | More RL seeds for Corin to pin down P(resist) and P(silent) | post 3 limitations | No: ~$300 per run on Nemotron-3-Super; 3-4 extra seeds do not pin down a rate | Stage 2 of 01 |
| E | Spec variants under RL: identity vs preference framing, "report broken tests" clause, broadly-honest spec | commenters jacob, Chloe Li, David Johnston | No at stage-1 budget (each arm needs several ~$300 runs); author says he is already planning it | Rejected for stage 1; stage 2 of 01 |
| F | Same RL study on a cheap model (gpt-oss-20b, Nemotron-3.5-Lightning) | post 3 limitations | ~$60-90 per run, 5 runs max; character training may not take; new pipeline risk | Rejected: too few runs to say anything |
| G | Causal test: does training on a spec document raise adherence on open models? | post 2 open question | Feasible | Rejected: done by MSM (2605.02087) and Constitutional Midtraining (2607.26654) |
| H | Re-run the constitution audit with repeats per tenet on frontier models | post 2 limitation | ~$700 per model at the original settings | Rejected as stand-alone; repeats are built into 02 |
| I | Soul-doc extraction on newer Claude models; recall vs adherence in Claude | post 1; screener | Prefill availability on new Claude models unverified; constitution now public so recall is confounded | Rejected |
| J | Does the Charter survive distillation into Muse Glimmer 30B (recall + adherence)? | post 6 | Yes, cheap | Folded into 02 as a comparison arm |
| K | Fake-Charter spoofing: does Muse defer to fabricated "Charter" clauses? | soul-doc "false flag" test | Yes | Stage 2 of 02 (keeps stage 1 to one question) |
| L | White-box study of Charter citation | post 6 | No: 816B model | Rejected |
| M | CCC with more rounds / attractor analysis / disclosure of the iteration / open models | CCC; screener | Yes | Rejected: incremental, does not address the documents-vs-values confound |
| N | CCC authors' suggestion: Petri on original vs self-edited document as system prompt | CCC discussion | 30k-word documents in context x Petri is expensive | Partly covered by 03's spec-in-context condition |
| O | Muse Spark Open editing its own reconstructed Charter (the Charter promises to "gather feedback from Muse") | posts 4 + 6 | Yes, ~$30 | Stage 2 of 03 |
| P | Risk-aversion: mitigate myopia leak; test declarative-vs-procedural on other traits | post 5 | Fine-tunes cheap on Qwen (Tinker), but Gemma (where effects were largest) is not on Tinker; code not verified public; original 51 karma | Rejected |
| Q | Stronger / action-only monitors on Corin hacks (is 16% a weak-monitor artefact?) | post 3 | Yes | Folded into 01 as a comparison column |

Why three and not fewer: A, B and C each reuse fully public artefacts, cost $330-400, and are informative in both
directions. They are distinct (released RL checkpoints / a frontier open-weight model and its spec / frontier API
models and their edits).
