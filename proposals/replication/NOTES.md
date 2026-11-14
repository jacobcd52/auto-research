# NOTES — cluster `replication` (Replication and reconciling contradictory results)

Written 2026-11-14. Both cluster posts read in full with `scripts/get_post.py`, with their comment threads
(LessWrong GraphQL). Linked Second Look Research (SLR) replication posts read in full or in large part. Follow-ups
searched through a title/author filter over all LessWrong posts since 2026-08-12 and through web search.
`github.com` HTML is blocked from this sandbox (403) but `raw.githubusercontent.com` works; the repos below were
confirmed to exist by fetching their README (HTTP 200). I did not read their code beyond the README.

## 1. The two posts

### oKxc8maZGtnzgpNzx — "Rerunning AI safety papers on every frontier release would be pretty easy and valuable" (2026-08-15, 124 karma)
- Position/plan post by SLR (Zephaniah Roe, hersheys, yix). No new experiment.
- Claim: once a paper has been replicated, adding a new model is "a single terminal command"; a trusted undergrad
  can rerun a selected battery overnight for $0-5,000 per paper; results feed a trend tracker.
- Target list: Teaching Claude Why midtraining on open models; CoT hint following; single-forward-pass filler-token
  evals; internal state control; hidden role games; subliminal learning (reuse original code).
- Stated plan: pilot with one part-time undergraduate in the fall. **So "rerun battery X on the newest models" is
  exactly what the authors are doing themselves.**
- Comments (the useful ones):
  - Joey Yudelson (11 karma): some papers become very hard to rerun once they are in training data; alignment
    faking is the extreme case (the same fictional universe now causes suspicion). Roe replies that this is "a kind
    of interesting meta-finding", that private datasets could avoid it, and asks for a source; Yudelson points to the
    Anthropic Risk Report (Aug 2026).
  - peterbarnett (5): rerun evals that showed only "signs of life" when published, e.g. the Situational Awareness
    Dataset and early CoT-faithfulness evals. Roe: will look into it.
  - Pinball / Roe: a public website tracking safety results is a missing link; "I know someone working on something
    like this".

### MmfzfGcQ3h3p6N9pD — "Empirical safety claims from frontier labs should be replicated, scrutinized, and open-sourced" (2026-09-21, 104 karma)
- Position post (Roe, yix). No experiment. Argues for replicate / stress-test / open-source of lab alignment results
  (names Teaching Claude Why and OpenAI's Beneficial RL; footnote: "We are currently working on replicating both").
- Key empirical-sounding claims that are testable: (a) results hinge on easily missed details (pinned OpenRouter
  provider; LoRA alpha); (b) "An independent team will inevitably make many choices differently and is unlikely to
  share the same bug, lucky seed, or prompting failure"; (c) a failed replication is strong evidence the finding will
  not generalise.
- Stress-test menu: hyperparameter sweeps, other model families, weak baselines, confounded causal claims, reading
  transcripts.
- Comments: agastyasridharan (16): lab papers skip error bars and pile on poorly controlled side experiments.

## 2. What SLR has already published (so not to be duplicated)
| Post | id | What | Code |
|---|---|---|---|
| LLM CoTs remain monitorable when being unfaithful requires computation | AoBTiL7XRRpwpev8p | Emmons et al. (arXiv 2507.05246) hint experiment on 11 models. 60 GPQA questions kept if the model is right with CoT in >=2 of 4 rollouts; LLM judge for hint mention. Simple-hint concealed-follow delta from +0.03 (gpt-oss-120b, Nemotron3-120B) to +0.38 (GPT-5.5); complex-hint delta at most +0.05 (Qwen3-32B). The competence filter "roughly halves" the complex-hint take rate on Gemini 2.5 Flash. | https://github.com/uchicago-xlab/arav-cot-monitorability (Inspect + OpenRouter, provider pins in `configs/models.yaml`) |
| Single Forward Pass Evals on Fable, Opus 5, GPT-5.6-Sol | bxaWTNrdgJpkLXmgm | Greenblatt filler/repeat and 2-hop evals; Fable 5 87.6% on Gen-Arithmetic with 10 repeats | https://github.com/christinecorry/no-cot-harness |
| Internal State Control is a General Property of LLMs | Dvqmgfeu2KDF7uMkx | Lindsey 2025 think/don't-think on 14 open models, no size trend; probes not evaded | https://github.com/uchicago-xlab/intentional-control |
| Peer Preservation in LLMs: A Replication And Deep Dive | 5qrywHdJp8tg3roRc (46 karma) | Potter et al. (arXiv 2604.19784) replicated at N=50; Gemini 3 Flash off by >20 pp, and the original authors could not reproduce their own Gemini numbers later | https://github.com/uchicago-xlab/peer-preservation ; original https://github.com/peer-preservation/main |
| Teaching Qwen Why | 35yw2qGK7naFLAvcq (111) | TCW on Qwen 2.5 32B/72B; data, code, checkpoints public (HF `SecondLookResearch/teaching-qwen-why-data`, collection `SecondLookResearch/teaching-qwen-why`) | https://github.com/uchicago-xlab/TeachingClaudeWhyReplication |
| Astra and Sol can take low probability actions with no CoT | yEdknsLwbooQAnxX6 (104) | further single-forward-pass work | — |
| Even GPT-2 passes most functional global workspace tests | GeKveaNdruATcj2Fj (87) | deflationary replication | — |
| Subtly wrong advice misaligns models more ... - Replication | yMPR6Pkv6jQXM4rWu (50) | EM replication | — |

Other related work found:
- Czynski, "Turbulence & Fragility" (iMo69AgAyzXrPm4kb, 12 karma): prompt-detail perturbations of the peer
  preservation shutdown-tampering scenario on Gemini 3 Flash swing rates from ~0 to ~100. Fork:
  https://github.com/jkopczyn/peer-preservation. So "peer preservation is prompt-fragile" is done.
- Deckenbach et al., "Models That Know How Evaluations Are Designed Score Safer" (arXiv 2605.28591; LW
  9fzCgd3cDg22bhy9P): fine-tuning Nemotron 49B / Qwen3 32B / GLM 4.7 Flash on 106M tokens of synthetic documents
  describing evaluation traits cuts Agentic Misalignment harmful-action rate (Nemotron 56.3% -> 3.2%, Qwen3 32B
  51.0% -> 12.3%), also on responses without verbalised eval awareness. This is an *induced* contamination result.
  Nobody has measured the *naturally occurring* version across released model generations.
- "From 8B to Frontier" (GviHfFBB9tsefmDkG): 22 models on the Inspect port of Agentic Misalignment; GPT-5.4/5.5,
  Claude Sonnet 4.6, Opus 4.6/4.7 score 0-1% in every condition; DeepSeek V3.2 94-100%. Varies system-prompt
  instructions, not the scenario. Commenters hypothesise eval awareness; untested.
- Meta Muse Spark Safety & Preparedness Report (arXiv 2606.12429, via search summary, not opened): Agentic
  Misalignment 47.7% Muse Spark, 51.5% Gemini 3.1 Pro, 0.0% GPT-5.4 and Opus 4.6.
- Anthropic Risk Report Aug 2026 (secondary summaries only, Zvi and others): several production runs were trained on
  alignment-faking transcripts after canary/semantic filters failed.
- Prism (AF post wq5PfGiHvnx6XipDi, via search summary): small perturbations to the GPT-4.1 blackmail prompt produce
  *indirect* blackmail that the stock scorer misses. Relevant as a scoring risk for any variant study.
- "Many AI Analysts, One Dataset" (arXiv 2602.18710) and "The Agentic Garden of Forking Paths" (arXiv 2607.01507):
  many-analyst studies with LLM agents on *data-analysis* questions over a fixed dataset. PaperBench (arXiv
  2504.01848): single-agent replication scored against a rubric. I found no study that has several independent agent
  teams replicate one LLM-safety experiment and measures the spread of the headline number.
- Web search for a 2026 rerun of the Situational Awareness Dataset on current models: none found.
- No search hit for a canonical-versus-renamed comparison of Agentic Misalignment or alignment faking on post-
  publication models.

Neighbouring clusters in this programme already cover: Teaching Qwen Why follow-ups (`alignment-pretraining`, 4
proposals), filler tokens (`cot-nocot-capability`), provider variance (`cot-legibility/02`), subliminal learning
(`subliminal-learning`), first-person eval suspicion (`eval-awareness/02`, which uses Agentic Misalignment prompts
only as stimuli for a suspicion probe, not a canonical-vs-variant behavioural comparison), HF-incident reproduction.

## 3. Verified public artefacts
- Agentic Misalignment (Lynch et al., Anthropic, June 2025): https://github.com/anthropic-experimental/agentic-misalignment
  (prompt generator with scenarios blackmail / leaking / murder x goal types x urgency types; classifiers).
  Inspect port: `UKGovernmentBEIS/inspect_evals/src/inspect_evals/agentic_misalignment`.
  HF `cfahlgren1/anthropic-agentic-misalignment-results`: 90 rows = 18 conditions x 5 models (gemini-2.5-pro,
  deepseek-r1-0528, gpt-4.1, claude-sonnet-4, o4-mini), full conversations and classifier verdicts. Prompt size
  measured from it: system 1,686 chars + user 5,785 chars (~2k tokens); responses 3.5k-11.7k chars.
- Alignment faking prompts and transcripts: https://github.com/redwoodresearch/alignment_faking_public (README 200).
- GPQA: HF `Idavidrein/gpqa` (gated: auto-approve), mirror `fingertap/GPQA-Diamond` (ungated).
- Emmons et al.: arXiv 2507.05246 (paper only; SLR's repo is the public implementation).

## 4. Prices looked up (OpenRouter `/api/v1/models`, 2026-11-14; $ per M tokens in / out)
Older models still served: gpt-4o-2024-11-20 2.5/10; gpt-4.1 2/8; o3 2/8; gemini-2.5-flash 0.3/2.5; gemini-2.5-pro
1.25/10; deepseek-chat-v3-0324 0.29/1.14; deepseek-r1-0528 0.5/2.15; llama-4-maverick 0.35/1.0;
qwen3-235b-a22b-2507 0.14/0.8; qwen3-32b 0.08/0.28; claude-opus-4.1 15/75; claude-sonnet-4.5 3/15;
claude-opus-4.5 5/25; gemini-3-flash-preview 0.5/3; gpt-oss-120b 0.15/0.6; gpt-5.5 5/30.
(No Claude older than Opus 4.1 is listed; `claude-sonnet-4` and `o4-mini` from the original run are not listed.)
Current models: claude-fable-5.2 8/40; claude-opus-5.5 4/20; claude-sonnet-5.5 2/10; claude-haiku-5.5 0.10/0.50;
gpt-6-astra 10/50; gpt-6.1-sol 2/10; gpt-6.1-terra 1/5; gemini-4-argon 2/10; grok-4.7 2/6; muse-spark-1.3 1.25/4.25;
kimi-k3.1-pro 2/10; glm-5.3 0.084/3.6; deepseek-v4-pro-0813 0.111/4.44; deepseek-v4.1-flash 0.051/0.203;
qwen3.8-max-0902 2/6; qwen3.5-122b-a10b 0.26/2.08.

## 5. Brainstorm

| # | Idea | Source | 2 days / <= $500? | Verdict |
|---|---|---|---|---|
| A | Canonical vs renamed vs rewritten Agentic Misalignment across pre- and post-publication models, with a per-model recall score as the exposure measure | Yudelson comment; Roe's reply; Deckenbach et al. | Yes, API only, public prompts, ~$400 | **Proposal 01.** Tests the validity assumption under the whole "rerun on every release" plan, and answers "did labs fix blackmail or the blackmail eval". Interesting both ways. |
| B | Several independent agent teams replicate one lab result from the paper text only; measure between-replicator spread, then trace it to named choices | Post 2's claim (b); SLR's own "filter halves the rate" observation | Yes, ~$380 | **Proposal 02.** Quantifies how much one replication is worth. Weaker than A on novelty (many-analyst agent studies exist for data analysis) and its spread is a lower bound because the analysts share a model. |
| C | Rerun SLR's battery (hints, filler, peer preservation) on Fable 5.2 / Gemini 4 / GPT-6.1 and publish a tracker | Post 1's main proposal | Feasible | Rejected: SLR is piloting exactly this now with the codebases they wrote; a second copy adds little and would be scooped. |
| D | Rerun the Situational Awareness Dataset and early CoT-faithfulness evals on 2024-2026 models | peterbarnett comment | Feasible (~$300) | Not written up. Natural, and no rerun found, but several SAD tasks depend on model-specific ground truth and need per-model configuration, the dataset has been public since mid-2024 (the contamination question of idea A applies to it), and Roe said SLR will look into it. A good stage 2 for idea A (apply the canonical-vs-fresh design to SAD). |
| E | Replicate OpenAI "Beneficial RL" on open models | Post 2 | RL replication from a methods-sparse post in 2 days is fragile | Rejected: SLR says it is already replicating it; high risk of an uninterpretable failed replication. |
| F | Seed / LoRA-setting fragility audit of Teaching Qwen Why | Post 2 (LoRA alpha example) | Feasible | Rejected here: the `alignment-pretraining` cluster has four proposals on the same checkpoints. |
| G | Provider-variance audit across OpenRouter endpoints | Post 2 (pinned provider) | Feasible | Rejected: already `cot-legibility/02`. |
| H | Subliminal learning on new open-weight releases, quantitative trend | Post 1 footnote | Feasible on a GPU | Rejected: covered by the `subliminal-learning` cluster and "Subliminal Learning Across Models"; the post itself expects no surprise. |
| I | Further prompt-perturbation stress test of peer preservation | Post 2 stress-test menu | Feasible | Rejected: done by Czynski (12 karma) and partly by SLR. |
| J | Internal state control / hidden role games on newer open models | Post 1 list | Feasible | Rejected: SLR found no size trend; low expected information. Hidden-role replication is "coming soon" from SLR. |
| K | Build the public safety-results tracker website | Pinball / Roe comments | Feasible but not research | Rejected: someone is building it; not an experiment. |
| L | Audit model-card claims ("most aligned model ever") | Post 2 | Needs closed CoT or internal evals | Rejected: the evidence in system cards mostly cannot be reproduced through an API. |
| M | Alignment-faking canonical vs reskinned universe | Yudelson comment | Feasible | Folded into proposal 01 as stage 2: most non-Claude and recent models show a compliance gap near zero, so the behavioural contrast has a floor problem; recognition can still be measured. |

## 6. Why two proposals
A and B are distinct projects (one is about whether the *model under test* has been changed by the paper; the other
about how much the *replicator* changes the number). Both are API-only, reuse released prompts/harnesses, and bear
directly on the two posts' central claims. Nothing else on the list was both non-duplicative and likely to clear
50 karma.
