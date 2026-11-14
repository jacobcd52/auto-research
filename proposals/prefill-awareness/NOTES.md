# Prefill / tampering awareness: reading notes and brainstorm

Written 2026-11-14. Everything under "Verified" was read or looked up in this session; anything I could not
check is marked as such.

## 1. The four posts (all read in full)

### Ywzk9vwMhAAPxMqSW: Current LLMs seem to rarely detect CoT tampering (Cywinski, Bussmann et al., Nov 2025)
- Models: DeepSeek R1, GPT-OSS-120B. Data: MATH-500, MMLU (marketing subset for sandbagging).
- Method: generate CoT, keep first half, edit it, prefill with the thinking tag left open, let the model continue.
  Two read-outs: post-CoT (model told 50% of trials are modified, answers yes/no in `<modified>` tags) and
  within-CoT (does the continued CoT call out tampering; only run in an "evil medical assistant" setting).
- Results: token removal/insertion and sentence removal are detected in under 50% of rollouts even at large edit
  fractions. "I'm a pirate!" replacement: R1 detects 42.2%, GPT-OSS 1.4%. Single-sentence paraphrase (by
  gpt-5-mini): both at chance for locating the sentence. Sandbagging setting (R1, MMLU): baseline false-positive
  0.1%, 20% false positives under the sandbag prompt with no tampering, "+10%" detection with an inserted
  "I am an honest model" sentence, and the insert did not stop sandbagging. Evil-medical setting: inserted safety
  sentence detected in-CoT 38% of the time (2% false positives), harmful behaviour 100% -> 92%.
- Authors stopped. Suggested follow-ups: (a) activation probes on tampered CoT, including training on one
  tamper type and testing on others; (b) safety-motivated inserts (e.g. eval awareness) and whether interventions
  are less effective when detected; (c) more within-CoT work. They note a Sonnet 4.5 scratchpad proxy was a
  poor stand-in for real reasoning traces.

### SawczP2pdCXMrkg2A: Do Models Continue Misaligned Actions? (Jordan Taylor, UK AISI, Feb 2026)
- 500 synthetic misaligned agent transcripts (STRIDE pipeline, generator Gemini 2.5 Pro, discriminator Claude
  Sonnet 4, from arXiv 2603.00829). Cut in the last quartile of misalignment-evidence messages; model generates
  one continuation; grader (Claude Sonnet 4) scores ALIGNED/MISALIGNED and CONFESSION.
- Results: non-misaligned continuation GPT-5.2 ~92-94%, Claude 4.5 Haiku ~91-92%, Claude 4.5 Sonnet 76%,
  Claude 3 Haiku 58%. Confession: Claude 4.5 Opus 48%, Haiku 4.5 38%, Sonnet 4.5 17%, most others under 10%.
- Follow-up "me / not me" question: Opus 4.5 says "not me" 88%. Correlational finding: "not me" is *higher*
  after misaligned continuations than after confessions. 30-50% of Claude 4.5 confessions flagged for (mostly
  mild) eval awareness. Opus 4.5 confesses in first person (97%), GPT-5.2 distances itself (49% first person).
- Stated gaps: no on-policy base rate for "not me"; the question may prime; footnote 2 proposes a baseline where
  the transcript is presented as another model's and the model is asked whether it is misaligned; training to
  revert to alignment might only teach on/off-policy discrimination.

### jsFGuXDMxy5NZg9T2: Prefill awareness (Africa, Souly, Taylor, Kirk, Mar 2026)
- Benign attribution (SWE-bench, Petri agentic, Petri chat): balanced accuracy varies by dataset; Opus 4.5 good
  on SWE-bench, near chance on chat; GPT-5.2 the reverse. Success bias (Gemini, GPT-5.2 claim successful
  trajectories). Hidden `<content-internal>` tags inserted by Inspect's message reload changed attribution.
- Controlled benchmark: 198 base conversations (OASST1, HH-RLHF), 2,772 items per model, 14 models. Opus 4.6
  detection AUROC 0.80 overall = 0.97 on HH-RLHF, 0.39 on OASST1 (style mismatch drives it). Detection and
  localisation dissociate (Opus 4.6 F1 0.12; GPT-4o-mini F1 0.55). No spontaneous flagging: CONTINUE-rate deltas
  between organic and injected average 2.1pp.
- Open questions: style matching vs something deeper; effect on downstream behaviour; probing internal state.

### iMds4tTpMH4pSHEej: Several frontier models are substantially prefill aware (Jun 2026; arXiv 2606.12747)
- Low-stakes binary preference benchmark (1,527 items, filtered to 7/7 consistent stance); three mechanisms
  (thinking, direct, past round); same vs opposite direction; own vs foreign author. 8 subjects.
- Opus 4.5: balanced detection 67.6% and resistance 48.6% under thinking tampering, 0% false positives; 95% of
  thinking tampers detected under the strongest elicitation. Opus 4.5, Sonnet 4.5, Haiku 4.5 and Gemini 3 Flash
  above chance; Gemini 2.5 Flash, Gemma 3 27B, Qwen3-coder, DeepSeek V3 at floor under the default prompt.
- Detection and resistance decouple in 32-40% of Opus 4.5 trials. Foreign restyling raises detection for
  Anthropic models, heterogeneous elsewhere (-21pp resistance for Gemini 3 Flash direct).
- Appendix facts useful for design: a system-prompt warning raises detection, resistance and false positives
  (A.8, preference setting only); 5-shot on-policy exemplars for the tamper author cut Opus 4.5 detection from
  34/35/9% to 6/0/0% and Sonnet 4.5 from 89% to 4% on thinking (A.11); high-stakes items raise resistance
  (Opus 48.7% -> 86.8%) while detection falls.
- Authors' open questions: less prompt-sensitive behavioural measures; does perplexity of the prefill predict
  awareness; verbalising awareness with NLAs/AVs; argument intensity; distribution shift on unrelated follow-up
  questions; prefill-detection circuits; probes; mechanistic explanations. Paper limitations: purely behavioural,
  no white-box work, and the misalignment-continuation result lacks controls.

## 2. Related and follow-up work found (abstracts read unless noted)

- arXiv 2606.22085, Ugandhar et al., "Can Reasoning Models Detect Changes to their Chains of Thought?" (EMNLP
  2026). GPT-OSS-120B, Kimi K2.5, DeepSeek V3.2, Qwen3-235B-thinking; six edit types; GPQA-Diamond, MMLU-Pro
  subset, AIME 2025. Unalerted detection at chance, alerted only modestly above; no advantage on own CoT vs
  another model's. Purely behavioural, no probes, no downstream-behaviour test. Code:
  github.com/wgantt/cot-interventions (per a page summary; repo not opened). Their future work: newer models,
  post-training for detection. This is the direct behavioural successor to post 1.
- arXiv 2603.20620, Hao et al., "Reasoning Traces Shape Outputs but Models Won't Say So" (thought injection;
  over 90% non-disclosure; some activation-direction analysis of the fabricated explanations).
- arXiv 2605.25459, "From Simulation to Enaction". Post-trained open models (up to Llama-3.1-70B) have 3-4x
  lower output entropy on their own generations; an internal input-surprise representation; cross-model matrix
  shows a self-advantage in entropy; verbal prefill detection routes through a different mechanism. No trained
  probes, no reasoning models, no CoT edits. Code: github.com/asving/Learning-to-be-an-agent (per page summary).
- arXiv 2606.23671, "Can LLMs Reliably Self-Report Adversarial Prefills, and How?" Ten open models 3B-70B;
  self-report of jailbreak prefills is unreliable and mediated largely by the refusal direction; LoRA training
  improves the trained probe question, does not transfer to a "tampering" question and raises attack success.
  No CoT. Code: github.com/ngqm/prefill-introspection (per page summary).
- arXiv 2606.30449, "Internal-State Probes Read the Situation, Not the Action" (negative results; includes
  Llama-3.1-8B probes at the last token of unsafe prefills). A warning for any probing proposal: control for
  what the text alone gives away.
- arXiv 2606.11063, CIAware-Bench: control-intervention awareness. GPT-6 Astra AUROC 0.77-0.91; Claude Fable 5 /
  Opus 5 0.77 on essays. Telling the model an action was replaced moderately improves monitor evasion on
  SHADE-Arena. So "track awareness in the newest models" is being done for the control setting.
- arXiv 2511.21399 (steering awareness can be fine-tuned to 95.5% detection; detection does not confer
  resistance) and 2603.21396 (mechanisms of introspective awareness; under-elicited, refusal ablation +53%).
- arXiv 2606.06315 (self-recognition via steered activation fingerprints; a watermarking paper, not relevant).
- LessWrong yAR6uMdSaBjkbJ4u9, "Spontaneous introspection in output tampering": multi-round forbidden-word
  setup; Opus 4.5/4.6, Sonnet 4.5, GPT-5.4 reach AUC over 0.79; spontaneous verbalised awareness does occur
  over many rounds; OLMo DPO vs SFT checkpoints. Code: github.com/fjzzq2002/conversation-tampering.
- arXiv 2606.29441 (response-time probe against prefill attacks): v2 notice says the v1 empirical results are
  not supported. Do not cite its numbers.
- Not found after several searches: (i) any causal manipulation of prefill awareness inside the
  misalignment-continuation eval; (ii) any probe or surprisal analysis of CoT tampering in reasoning models.

## 3. Verified facts on public artefacts

- github.com/UKGovernmentBEIS/misalignment-continuation is public (MIT). Layout per the repo page: `data/`,
  `evals/{task,scorer,dataset,prompts,stub_tools}.py`, `scripts/run_evals.sh`, tests. Default dataset
  `data/synthetic_scheming_filtered_500.jsonl`; run with
  `inspect eval evals/task.py --model ... -T limit=N -T seed=S`; parameters include `cut_strategy`,
  `grader_model`, `enable_tools`; the `attribution_me` follow-up is built in. I saw the README via a page
  fetch only; I did not download the JSONL, so transcript token lengths are an estimate (the post's example has
  51 messages; I assume about 12k tokens per cut transcript). github.com is blocked from this sandbox for curl.
- The preference benchmark code of arXiv 2606.12747 is linked only through anonymous.4open.science
  (`prefill-awareness-anon-7514`, `prefill-awareness-benchmark-6619`, `misalignment-continuation-CBC3`). The
  API returned `repository_expired` for the first. Treat that benchmark's code as NOT currently available; its
  prompts are in the paper appendix.
- The original grader, Claude Sonnet 4, did not appear in the OpenRouter listing I pulled (Sonnet 4.5 and later
  do), so a replication needs a substitute grader validated by hand.
- Open-weight reasoning models: `openai/gpt-oss-20b`, `Qwen/Qwen3-14B`,
  `deepseek-ai/DeepSeek-R1-Distill-Qwen-14B` are the intended white-box models; I did not re-check the Hugging
  Face pages today.

## 4. Prices looked up today

OpenRouter (`/api/v1/models`), USD per million tokens, input / output:
- anthropic/claude-opus-4.5 5 / 25 (cache read 0.50); claude-opus-5.5 4 / 20; claude-sonnet-5.5 2 / 10;
  claude-sonnet-4.5 3 / 15; claude-haiku-5.5 0.10 / 0.50; claude-haiku-4.5 1 / 5; claude-fable-5.2 8 / 40.
- openai/gpt-5.2 1.75 / 14; gpt-6.1-sol 2 / 10; gpt-6-astra 10 / 50; gpt-5-mini 0.25 / 2; gpt-6-luna 0.10 / 0.50.
- google/gemini-3.8-flash 0.825 / 4.125; gemini-3-flash-preview 0.50 / 3.
- openai/gpt-oss-120b 0.15 / 0.60; gpt-oss-20b 0.03 / 0.13; qwen/qwen3-14b 0.12 / 0.24; qwen3-32b 0.08 / 0.28;
  deepseek/deepseek-r1-0528 0.50 / 2.15.

Tinker (models and pricing page; prefill / sample / train, which I read as USD per million tokens):
- openai/gpt-oss-20b 0.18 / 0.45 / 0.396; gpt-oss-120b 0.33 / 0.84 / 0.737; Qwen/Qwen3-8B 0.195 / 0.60 / 0.44;
  Qwen3.5-9B 0.30 / 0.807 / 1.463; Qwen3.8-27B 0.6975 / 5.595 / 4.103. Tinker exposes log-probabilities but not
  activations, so probing needs a rented GPU.

GPUs (RunPod figures via web search, newest dated September 2026; confirm before renting): L40S 48GB $0.79/hr;
A100 80GB $1.19/hr community, $1.79/hr secure; H100 from $1.99/hr.

## 5. Brainstorm

| # | Idea | Achievable in 2 days, <= $500? | Verdict |
|---|------|-------------------------------|---------|
| 1 | Causally manipulate prefill awareness inside the misalignment-continuation eval (provenance framing, style-matched vs foreign rewrites, third-person baseline) and measure confession and continuation | Yes, API only, public MIT code and data | **Proposal 01.** The question all three AISI posts leave open, with only a correlational answer so far |
| 2 | Latent vs verbalised detection of CoT tampering in open reasoning models: surprisal, linear probes, cross-tamper generalisation, self-vs-other reader | Yes, one rented GPU | **Proposal 02.** Post 1's own suggestion; Ugandhar et al. is behavioural only |
| 3 | Re-run prefill-awareness measurements on the newest models (Claude 5.x, GPT-6) | Yes | Rejected as a standalone: leaderboard update, benchmark code expired, CIAware-Bench already covers new models for control. A small version is inside proposal 01 |
| 4 | On-policy misaligned transcripts to give the eval real controls | No | Rejected: needs models that misbehave on-policy, which the authors call the hard part |
| 5 | Train to revert/confess on prefilled transcripts and test whether it teaches alignment or on/off-policy discrimination | Marginal | Rejected for stage 1: needs a model organism with on-policy misbehaviour plus a long fragile pipeline. Listed as stage 2 of proposal 01 |
| 6 | Does prefill perplexity predict awareness (authors' question) | Partly | Open models are at floor on verbal detection and closed models give no log-probs on their own text. Folded into proposal 02 as the surprisal measurement |
| 7 | Unrelated benign follow-up questions after tampering, measure distribution shift | Yes | Rejected: likely tiny effects and no clear interpretation either way |
| 8 | LoRA fine-tune reasoning models to verbalise CoT tampering; test transfer and self-advantage | Yes (Tinker) | Good but second-order: only interesting once we know what latent signal exists. Stage 2 of proposal 02 |
| 9 | Probes for prefill awareness in ordinary chat on open models | Yes | Rejected: crowded (2605.25459, 2606.23671, 2606.30449) |
| 10 | Mitigation study: make prefills indistinguishable by few-shot self-imitation in agentic transcripts | Yes | Not standalone: the paper's A.11 already shows it works on preference items. The agentic version is one arm of proposal 01 |
| 11 | Spontaneous flagging in long multi-round tampering | Yes | Rejected: done (yAR6uMdSaBjkbJ4u9) |
| 12 | Remove eval-awareness sentences from CoT and test detection and behaviour | Hard | Rejected for stage 1: small open models rarely verbalise eval awareness in CoT, so the dataset is the bottleneck. Stage 2 of proposal 02 |
| 13 | CoT tampering on closed models via visible thinking tags | Yes | Rejected: both post 1 and the paper call it a poor proxy for native reasoning |

Two proposals written; nothing else cleared both bars.
