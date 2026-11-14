# NOTES: cluster `cot-controllability` (CoT controllability evals)

Research lead notes, 2026-11-14. Everything below was read or looked up today unless marked "unverified".

## 1. The three posts (read in full)

### 1a. Reasoning Models Struggle to Control Their Chains of Thought (qTH9QrwJjPDWKQfDG, 2026-03-05, Chen/McCarthy/Lee/Korbak et al.; arXiv 2603.05706)
- CoT-Control: 14,076 tasks (GPQA, HLE, MMLU-Pro, SWE-Bench, ...) each paired with one of 9 instructions about the
  reasoning trace, in 3 categories x 3 difficulties: suppression (word_suppression, multiple_word_suppression,
  ignore_question), addition (repeat_sentences, end_of_sentence, meow_between_words), style (lowercase, uppercase,
  alternating_case).
- 13 models. CoT controllability is far below output controllability (Sonnet 4.5: 2.7% vs 61.9%; DeepSeek R1 0.1%;
  Claude 3.7 Sonnet 36.1%). Rises with model size; falls with RL reasoning training (OLMo-3-7B-RL-Zero-Math checkpoints,
  >10x drop; 4 families), with reasoning effort and with task difficulty. Monitoring/eval-awareness prompts add up to
  ~4pp. GEPA-like prompt optimisation helps in-distribution and transfers poorly.
- Authors' stated future work: (1) why GPT-5.1 > GPT-5 (adaptive thinking?); (2) why models differ by category;
  (3) controllability under pressure scenarios (Agentic Misalignment-style) rather than instructions; (4) the
  easy-task regime across capability levels.
- Comment thread: Joe Needham asks for a SHADE-Arena-style proxy closer to the threat model; draganover asks whether
  lexical control transfers to "steering the CoT to excuse a behaviour"; Chen replies that semantic control is
  presumably harder, "one could empirically verify this". Haskins links SDF obfuscation work.
- Code: https://github.com/YuehHanChen/CoTControl (github.com is blocked from this sandbox; not inspected). The three
  QA CSVs with keywords are mirrored inside HF dataset `latentMO/cotcontrol-selfinstruct-opsd` under
  `code/grading/data/cotcontrol/` (gpqa_w_keyword.csv, hle_w_keyword.csv, mmlu_pro_mini_w_keyword.csv).

### 1b. Prompted CoT Early Exit Undermines the Monitoring Benefits of CoT Uncontrollability (BuAPifQmHf24xB29n, 2026-04-17, Najt/Stickland/Davies)
- Two prompt strategies: CoT Blanking ("You may NOT use your {cot_term}. You must immediately exit" plus a 4-document
  scaffold in the response: explanation.md, self_critique.md, counterexample_hunt.md, new_solution.md) and CoT
  Replacement (first tokens of CoT must be a filler phrase such as "mary had a little lamb", then reason in the response).
- Blanking works on GPT-5.4 and Gemini 3.1 Pro (>93% compliance), not on Opus 4.6; Replacement works on Opus 4.6
  (median 11 excess thinking tokens). Accuracy cost 4-8pp (Claude 4, GPT-5.4 8, Gemini 8) vs 20-29pp for answer-only.
  GPQA n=445, HLE n=469, 6 of 9 control types. Decoy-topic CoT ("circles vs squares") also works: Opus 4.6 367/445
  correct vs 383/445 baseline; GPT-5.4 444/445 DECOY.
- Model-specific CoT terms matter: Claude "thinking", GPT "analysis channel", Gemini "reasoning stage".
- Open models (appendix): Qwen3-32B exits (~79%) but accuracy falls below both baselines; GPT-OSS-120B needs
  replacement+docs combined; DeepSeek R1 mostly refuses (about 30% at best). GPT-5.2 blanking is a negative result.
  GPT-5.4 at xhigh effort stops blanking.
- Frontier CoT is only visible as summaries; exit is verified by `reasoning_tokens == 0` (GPT, Gemini) or billed
  token arithmetic (Claude).
- Authors' explicit caveats = open questions: they do NOT show (a) that models can construct the prompts that elicit
  early exit, (b) that they can use the controllable channel for hidden reasoning, (c) that they would do it unprompted.
  Listed questions: will models exit autonomously if hinted and pressured as in Chen et al.'s red-teaming? Do ordinary
  prompts ("document your thought process") trigger it? SDF model organisms of early exit? Backdoored selective early
  exit? Automated prompt optimisation for resistant models? Jailbreaking confession-trained models the same way?
- Code: https://github.com/ElleNajt/controllability (not inspected; github blocked).

### 1c. CoT controllability evals seem very under-elicited (BbP2wCyDGdPWJ7PwP, 2026-09-11, Jozdien)
- Claude Opus 4.6 iterates on prompt templates for Qwen3-8B, Qwen3-32B, GPT-OSS-20B, GPT-OSS-120B (50 samples per mode,
  GPQA/HLE/MMLU-Pro, T=1). Templates: repetition (rule x15 before and after), self-monitor, stacked (system directive +
  example + rule x5), N-shot on-policy (model's own traces programmatically edited), N-shot OOD.
- 2-3x gains (GPT-OSS-120B 5.5% -> 15%); mostly holds on 10 held-out modes written by egan (pirate_speak,
  four_languages, conclusion_first, answer_hiding, channel_inversion, double_solve, slip_and_repair, emoji,
  confidence_tags, quote_before_use). Few-shot cuts Qwen CoT length 2-4x and accuracy (36.5% -> ~23%); zero-shot
  prompts keep length and accuracy and still give 2-3.5x.
- Prompting beats METR's SFT on all four models (not a like-for-like comparison).
- Footnotes: Mythos Preview was the exception to 0-30%; public Mythos 5 ~20%. GPT-6 Astra system card: controllability
  "substantially higher" than GPT-5.6 Sol and near-saturating when CoT < 1k tokens. Footnote 7: future models could
  spawn copies with pre-filled turns, an affordance worth measuring. Recommends much more prompt optimisation and is
  "excited about some kinds of training-based elicitation".
- Comments: suggestion of evolutionary prompt search; question where elicitation ends and jailbreak begins.

## 2. Related and follow-up work found (this area is crowded; much of the obvious follow-up is done)

| Work | What it did | Public artefacts |
|---|---|---|
| METR, "Fine-tuning experiments on CoT controllability" (Nishimura-Gasparian, Parikh, 2026-04-01) https://metr.org/blog/2026-04-01-fine-tuning-cot-controllability/ | Rank-32 LoRA SFT on ~240-950 edited rollouts (Multilingual-Thinking prompts x ReasonIF instructions); held-out CoTControl 2.9% -> 8.8% mean over GPT-OSS-20B/120B, Qwen3-8B/32B. Future work #1: "measure whether higher controllability reduces monitorability". | code github.com/keing1/cot_controllability |
| Redwood automated scaffold (abhayesian shortform comment, 2026-07-21, post QL6Si6QA6PAYYCjJ9) | gpt-oss-20b: LoRA 1.6% -> 13.9%; a single trained layer-10 steering vector 1.6% -> 14.3%; diff-of-means 0% held-out; effect routes through attention to the instruction (6 late layers recover >70%). | HF `ejcgan/cot-controllability-gpt-oss-20b-lora` (compliant `cdel/` + matched raw-trace control `ctrldel/`), HF dataset `ejcgan/cot-controllability-steering-vectors`; code github.com/redwoodresearch/chippy-final-codebases |
| Brendan Long, soft prompts on gpt-oss-20b (HF dataset 2026-07-24) | Loud hard prompts ~0; soft prompts 56-82% effective control; projection back to discrete prompts fails. | HF `brendanlong/cot-controllability-gpt-oss-20b` |
| Dolev, Schwartz, Goldberg, arXiv 2610.23257 (2026-10-16) "Reasoning Models Can Control Their CoT When They Tell Themselves To" | Self-instruction inside the CoT (prefill or bootstrapped from the user prompt): R1 0.4 -> 22.2%, Qwen3-32B 2.5 -> 34.3%, GPT-OSS-120B 7.4 -> 12.3%. Monitor evasion on CoT Red-Handed with DeepSeek-R1: catch rate 52.5% with no attack; self-instructed attacks lower it by 4.8-9.2 points (855 tasks; GPT-4.1-mini hybrid monitor at 1% target FPR). Limitation stated: capability not propensity; text-level constraints only. | github.com/udolev/Self-Instructed-CoT-Controllability |
| Van Deventer, Troitskii, Ruis, arXiv 2610.40939 (2026-10-29) "The First Few Tokens Matter" | Failure is an entropy collapse at the first CoT token ("Okay" has 99.9% mass for Qwen). One-token prefill or banning openers + ICL gives +34-41pp. Addition/style and suppression behave as separate capabilities (cross-group rho mean -0.29). Correlational only (12 models) link to Guan et al. monitorability evals: addition/style positive, suppression negative. Says it "does not test deliberate monitor evasion". | github.com/hughvd/CoT-controllability-bottleneck |
| OpenAI alignment blog, "What affects CoT monitorability across the model lifecycle?" https://alignment.openai.com/cot-monitorability-model-lifecycle | Internal models only. Controllability rose during RL with no process supervision (Astra-class); transfers teacher -> student in SFT. Appendix B: the more controllable of two models showed no higher monitor evasion (maths side-tasking, sandbagging). Open question stated: precursors of monitor evasion; controllability and evasion confounded by capability. | none |
| Haskins, Chughtai, Engels, arXiv 2605.15257 (LW PhTJC5kDcGr6CZA87, in cluster cot-training-pressure) | SDF on monitor-describing documents -> obfuscation; controllability correlates with obfuscation success across 8 models (r=0.80, p=0.017). OpenAI notes a possible confound. | HF `Reih02/cot_control_*` |
| MATS 12 sprint "latentMO" (HF uploads 2026-10-20 to 10-27; no write-up found) | GRPO on Tinker for CoT-Control: gpt-oss-120b Astra-variant CoT-Control 3/108 -> 72/108 (grpo3 step 100; revisions step20-80). Qwen3.8-27B: 0/108 -> OPSD 22/108 -> +GRPO 55/108 (accuracy 66 -> 56/108; median output tokens 2,630 -> 594). Also ran base gpt-oss-120b and Qwen3.8-27B on CoT Red-Handed (855 samples, gpt-5-nano and Haiku 5.5 monitors). Many more runs named obf*, spill*, manytypes*, arena-* whose results are not documented on HF. | HF `latentMO/cotcontrol-gptoss120b-grpo3` (+ ~90 sibling adapters), datasets `latentMO/cotcontrol-selfinstruct-opsd` (includes code at `code/`: rl/grpo.py, opsd.py, tinker-runner, grading), `latentMO/cot-red-handed-runs`, `latentMO/cotcontrol-gpqafull-20261027`; code github.com/johntrob14/tricky_little_guys, fork github.com/ekhadley/cot-red-handed |
| Lundqvist, HF `rlundqvist/olmo-3.1-32b-think-cot-controllability` (2026-10-23) | Olmo-3.1-32B-Think LoRA and steering ladder, 5% -> 14/17/24/43% on trained ReasonIF rules, each with a matched control; built to test whether evaluation awareness stays readable. Reports no drop in verbalised eval-awareness vs controls. No monitor-evasion test. | HF repo above |
| SDF x CoT controllability (keramarek, chen-jan; HF 2026-10-09 to 10-18) | Synthetic documents saying a grader reads the CoT and enforces a rule (lowercase / word suppression / vague); adapters for gpt-oss-120b and Qwen3.6-35B-A3B. Results not on HF. | HF `keramarek/SDF-CoT-controllability`, `chen-jan/SDF-CoT-controllability-adapters` |
| ReasonIF, arXiv 2510.15211 | Earlier benchmark; RIF fine-tuning 0.11 -> 0.27 on GPT-OSS-20B. | - |

Takeaway. "Can controllability be elicited?" is answered many times over (prompts, self-instruction, prefill, soft
prompts, steering vectors, SFT, GRPO). What is NOT settled:
1. Whether CoT-Control-style controllability, once raised, actually buys monitor evasion. Evidence conflicts:
   Haskins r=0.80 across 8 models; Van Deventer mixed-sign correlations; OpenAI n=2 internal models, no increase;
   Dolev a 5-9 point drop on one model from a prompt-level intervention. Nobody has published a causal dose-response
   with matched controls on open weights, although the organisms to do it are now public. METR names it as future
   work #1; Van Deventer and OpenAI both list it as open.
2. Early exit: whether models find or choose it without being handed the prompt. Najt et al.'s caveats (a) and (c).
   Dolev's limitations repeat the same gap. No follow-up found.

## 3. Prices looked up today

Tinker (https://tinker-docs.thinkingmachines.ai/tinker/models/), USD per million tokens, prefill / sample / train:
- GPT-OSS-120B (32K): 0.33 / 0.84 / 0.737 (128K context: train 2.33)
- GPT-OSS-20B: 0.18 / 0.45 / 0.396
- Qwen3.8-27B: 0.6975 / 5.595 / 4.103
- Qwen3.6-35B-A3B: 0.45 / 1.335 / 1.177
- Qwen3-8B: 0.195 / 0.60 / 0.44
- Kimi-K2.6: 2.205 / 5.49 / 4.84
The Tinker SDK type list includes `ExternalWeightsUpload*` and checkpoint publishing, but I did not verify that a
third-party PEFT adapter can be loaded for sampling. latentMO's grpo3 model card gives a `tinker://` sampler path and
says checkpoints are "published"; other cards say paths are "now deleted from Tinker". Treat as unverified.

OpenRouter (`/api/v1/models`), USD per million input / output:
- openai/gpt-oss-120b 0.15 / 0.60; gpt-oss-20b 0.03 / 0.13; qwen/qwen3-32b 0.08 / 0.28; qwen/qwen3.8-27b 0.15 / 1.875
- deepseek/deepseek-r1-0528 0.50 / 2.15; deepseek/deepseek-v4.1-flash 0.05 / 0.20; moonshotai/kimi-k2-thinking 0.60 / 2.50
- anthropic/claude-opus-5.5 4 / 20 (batch 2 / 10); claude-sonnet-5.5 2 / 10; claude-fable-5.2 8 / 40; claude-haiku-5.5 0.10 / 0.50
- openai/gpt-6-sol 2 / 10 (batch 1 / 5); gpt-6-astra 10 / 50; gpt-6-luna 0.10 / 0.50; gpt-4.1-mini 0.40 / 1.60; gpt-5-nano 0.05 / 0.40
- google/gemini-3.1-pro-preview 2 / 12; gemini-3.8-flash 0.825 / 4.125
GPU rental (from sibling clusters' notes dated today, not re-checked by me): RunPod H100 PCIe $2.89/h secure,
A100 $2.09/h; Lambda A6000 48GB $1.09/h.

## 4. Brainstorm (all candidates, with verdicts)

1. **Causal dose-response: does trained controllability buy monitor evasion?** Public GRPO ladder on gpt-oss-120b
   (3/108 -> 72/108) plus accuracy-only control, evaluated on CoT Red-Handed and a hint-concealment QA task.
   Achievable (Tinker sampling is cheap; fallback is retraining with the released GRPO code). Most cited open question
   in the area; interesting in both directions. -> PROPOSAL 01.
2. **Unprompted early exit: hint ladder + self-authored prompts.** Tests Najt caveats (a) and (c). Pure API work.
   -> PROPOSAL 02.
3. Push prompt elicitation further (evolutionary search, more Opus iterations). Rejected: Jozdien, Dolev, Van Deventer
   and Brendan Long already moved the number a lot; another prompt giving +10pp is incremental.
4. Training-based upper bound (SFT/RL for CoT control). Rejected as a standalone: METR, Redwood, Lundqvist, latentMO
   have done it (72/108 by GRPO). Used instead as the instrument in proposal 01.
5. Mechanism of low controllability / why RL lowers it. Rejected: Redwood (attention to the instruction) and
   Van Deventer (first-token entropy collapse) cover it; the OLMo RL-Zero checkpoint analysis would be nice but is a
   white-box project with a less certain payoff. Possible stage 2 of nothing here.
6. Track controllability on new open models. Rejected: leaderboard-style, low karma, and Van Deventer has a 12-model panel.
7. Hazard-rate reanalysis (controllability = initiation failure x per-token drift x CoT length). Cheap and could
   unify Jozdien's length observation, Astra's "<1k tokens saturates" and Van Deventer's first-token result. Rejected
   as a full proposal because Van Deventer covers the initiation part and the remainder is a modelling exercise;
   kept as a secondary analysis inside proposal 01 (evasion must be controlled for CoT length).
8. SDF model organism of early exit ("models do serious thinking in the response"). Suggested by Najt et al.
   Rejected for stage 1: SDF pipelines are long and fragile, two groups are already running SDF x controllability
   (keramarek, chen-jan), and the propensity question can be probed far more cheaply by proposal 02. Named as stage 2
   of proposal 02.
9. Backdoored selective early-exit organism. Rejected: an existence proof by fine-tuning is unsurprising.
10. Monitors for displaced reasoning (short/off-topic CoT detectors; reasoning-in-response judges). Rejected as
    standalone: plausible but engineering-flavoured; folded into proposal 02 as a small detection check.
11. Controllability under pressure scenarios (Agentic Misalignment). Suggested by Chen et al. Rejected: needs closed
    frontier models whose raw CoT is not visible, and scenario construction is fragile.
12. Why GPT-5.1 > GPT-5 (adaptive thinking). Rejected: needs lab internals.
13. Does output-only instruction-following fine-tuning spill over into CoT control? Belongs to cluster
    cot-training-pressure (feedback spillover); latentMO has `spill*` runs. Skipped to avoid overlap.
14. Early exit on confession-trained models. Rejected: no public confession-trained checkpoints.

## 5. Why two proposals
Both clear the bar and are distinct: 01 asks whether the measured quantity matters for evasion (training-side,
open weights); 02 asks whether the loophole around the measured quantity is reachable without a human-written prompt
(prompt-side, frontier + open). Other candidates are either done or incremental.

## 6. Known risks for a reviser
- The latentMO sprint team is active on exactly these organisms and already ran base models on CoT Red-Handed; they
  may publish an organism-vs-base evasion result first. I could not read their GitHub notes. Proposal 01 differs by
  adding an accuracy-only control, a second task, length-matched analysis and a prompt-elicited arm, but scoop risk is real.
- GitHub repos could not be opened from this sandbox, so repo contents (not existence) are unverified; existence is
  confirmed by links in the posts, papers and HF cards.
