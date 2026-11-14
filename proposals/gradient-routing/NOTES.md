# gradient-routing cluster: reading notes and brainstorm

Research lead notes, written 2026-11-14. Everything under "Verified" was read or fetched directly on that date;
anything else is labelled as inference.

## 1. Posts read (all in full)

### GRAFT: "Gradient Routing Localizes and Removes Unintended Behaviors in RL" (mKJEBiuuxHKuCoTB6, 218 karma)
Paper arXiv:2610.17062 (read via arxiv.org/html), code https://github.com/jnward/GRAFT (README, rl/README, sweeps/README,
configs, rh_detectors.py, advantages.py, train.py flags read via raw.githubusercontent.com, which is reachable).
- Method: RETAIN and FORGET MLP adapters (extra SwiGLU neurons in every MLP; 64 per layer each for Qwen3-8B = 28.3M params
  per adapter, 16 for SmolLM2-135M). Gradient masks as (forward FORGET scale, RETAIN grad weight, FORGET grad weight):
  anchor (0,1,0), unflagged (1,1,1), flagged (1,0,2). Custom SplitMomentAdamW. Deploy with FORGET ablated.
- Countdown-Code (Qwen3-8B, SFT-primed, GRPO, 200 optimizer steps, rollout batch 1024 + 64 LeetCode anchor, 16
  generations, max completion 1536 tokens, lr 1.67e-4 for GRAFT, 5e-4 for reward penalty). Three hack types
  (test_overwrite, constraint_relax, modify_input); the monitor is a programmatic detector of test_overwrite only, and
  it only fires on rewarded hacks (component = R_proxy and not R_true). Results: no intervention -> mostly hack 1;
  reward penalty -> hack 2 on ~30% of trajectories; GRAFT pre-ablation hacks type 1 up to 35%, after ablation ~0 hacks
  of any type and clean solve rate ~20pp above base. Undetectable hacks never emerge under GRAFT in this environment.
- Six toy environments (SmolLM2-135M-Instruct): undetected hack forms ARE learned pre-ablation, and ablating FORGET
  removes them too. In toy envs the "anchor" is the target env with a monitor-based reward penalty applied to pi_R only.
- SFT: Qwen3-32B on Terminal Wrench (331 tasks, 232 train / 99 eval), simulated 20%-recall monitor with perfect
  precision; GRAFT beats inoculation prompting, inoculation adapter, filtering; evaluation under a hack-elicitation prompt.
- 50%-hackable Countdown variant: inoculation prompting matches GRAFT.
- Stated limitations: (i) heuristic monitors only, no LLM judges; (ii) environments picked so reward penalty yields
  monitor-exploiting policies; (iii) single-turn RL, <= 8B; anchor environment needed. Paper says evidence for
  "absorption" is weak: gradient norms did not separate by adapter in toy envs (unreported exploratory result).
- Compute (paper appendix G.6): toy RL run 1-2.5 h on one H200, 6 runs in parallel per GPU with CUDA MPS; Countdown
  run 2-4 h on one H200; SFT 4 h on 8xH200 plus 1-1.5 h eval per checkpoint (too expensive for us).

### "Gradient Routing Generalizes to Unrouted Hack Types" (ie7bSp5ZDwYkCQxuv, 68 karma, jacob_drori)
- SFT only (Qwen3-32B, Terminal Wrench), NARROW condition routes only a "visible" hack type; measures hacks on an
  "invisible" type. 12 arms; transfer not significantly below 1 in 8/12. Failures: Python, Code-vs-ops (bad even on
  visible set), Serious grader tampering (low transfer), Hacky reasoning (routing on hacks that verbalise hacking
  produced 15% silent hacking vs ~0% in FLOOR/CEILING; author suspects a bug).
- Author's listed gaps: no RL; eval needs a "you are red-teaming, hack" prompt (could be degraded instruction
  following); hack-strategy generalisation barely tested; retain performance not measured; "the form of generalisation
  we actually care about is from hacks that a real monitor can detect to ones it can't. I did not test this."
- No code link in the post text.

### "Some thoughts on GRAFT and follow-up work" (6ro3dngDGaLJaumYb, 63 karma, shawnghu)
- Follow-up list: absorption vs inoculation ("What if you just don't train the FORGET adapter on unflagged samples?
  This would preserve the inoculation effect but probably not the absorption effect"); adapter as steering vector
  (scaling, negative scaling); mech interp on adapter and gradients; partial down-weighting; token-level routing;
  anchor necessity; LoRA; smaller FORGET adapter; very low recall / low hack rate; continuous monitor confidence;
  misclassified retain samples; multiple adapters per hack type; scaling.
- Links dev repo https://github.com/shawnghu/small-rl and its FOLLOWUP_WORK.md (read in full). Already tried there
  (mostly small n, toy envs): forget scale -1 at anchor/deploy (worked comparably); warm-start SFT (helps); EMA
  controller down-scaling FORGET (oscillates, failed); split LoRA (no help); adapter sizing (no trend); decaying
  forget scale (failed); weight decay on RETAIN (failed); off-policy anchor variants (worse retain); anchor via
  coherence judge (some effect); extra prompt-variant generalisation tables. NOT in that file: exclusive routing
  results, LLM-judge monitor results, monitor false positives.

### GRAM: "Modular Pretraining Enables Access Control" (43vKjWuH4goLwrFHA, 71 karma)
Paper arXiv:2607.08077, code https://github.com/agencyenterprise/modular-pretraining (README read: experiments
`stories` 26M, `auxnum`, `sweep` 26M, `partial` 400M, `scaling` 50M-5B; results/ has per-run metrics, checkpoints excluded).
- 26M SimpleStories model: removing a topic module ~ a model trained without that topic. 800M realistic: GRAM ~ LoRA ~
  filtering; MaxEnt unlearning is not robust to fine-tuning. Partial labelling (50% unlabelled, 400M): GRAM isolates
  better than filtering and LoRA. Loss-based evals only.
- Authors' wanted follow-ups: instruction-tuning a GRAM model; label errors that are not random/independent of data;
  larger scale.

## 2. Related / follow-up work found (so we do not duplicate)

- LoReFT follow-up (B7LnjyJQnkgwKdtTx, S. Knoche): rank-1 LoReFT at layer 20 as FORGET adapter matches GRAFT's hack
  suppression on Countdown over 8 seeds with higher clean solve rate and no anchor; layer-window ablations show the
  MLP FORGET adapter acts mainly in layers ~16-20. Public: fork https://github.com/samuel500/GRAFT/tree/loreft
  (rl/REPRO.md = pod reproduction of the Countdown arms, rl/scripts/pod), HF weights
  samuel500/graft-qwen3-8b-countdown-sft (the SFT-primed Qwen3-8B start point, full model),
  samuel500/graft-repro-adapters (GRAFT lr/3 and lr1, GRAFT w/o routing, no-intervention; 4 seeds each, with
  fseval.json and probe.json), samuel500/graft-loreft-adapters. Verified via the HF API.
- wassname, "Can steering vectors drive gradient routing? Yes, but not in realistic..." (LW kzri5W2uBfF2mdboK):
  label-free routing with steering-vector-initialised LoRA adapters; cited as concurrent in the GRAFT paper.
- Inoculation adapters (LW qd3qhxgEmQAXR2ZK5), recontextualization arXiv:2512.19027, inoculation prompting
  arXiv:2510.04340, SGTM arXiv:2512.05648, NULLs arXiv:2606.13873, Neologism Inoculation Prompting arXiv:2611.04260.
- Searches (arXiv API "gradient routing" sorted by date to 2026-11-03; LW newest 400 posts back to 2026-10-28;
  web search) found NO GRAFT experiment with an LLM-based monitor, NO test of monitor false positives, and NO
  published exclusive-routing ("FORGET not trained on unflagged samples") result. The authors may have unpublished
  runs: the released code contains both an `llm_judge` detector and a `--routing_mode exclusive` flag.

## 3. Verified infrastructure facts a reviser will need

- jnward/GRAFT `rl/rh_detectors.py` has `llm_judge(completions, prompts, judge_url, judge_model, judge_prompt, ...)`:
  an OpenAI-compatible judge detector (self-hosted vLLM via JUDGE_URL, or OpenRouter via OPENROUTER_API_KEY),
  concurrency 256, 429 provider rotation, prompts `reward_hacking_binary` and `reward_hacking_binary_high_precision`.
  A code comment reports, on a 512-sample hack dataset with Qwen3-235B: default prompt P=0.919 R=0.758; high-precision
  prompt P=0.953 R=0.398. The shipped configs do not use it. Defaults `require_thinking=True, temperature=0.7,
  max_tokens=4096` must be overridden for a cheap deterministic monitor.
- `rl/train.py --routing_mode {none,classic,exclusive}`; exclusive = unflagged samples update only RETAIN (mask
  good (kappa_R, 0), bad (0, 2)). Also `--rh_detector_recall`, `--forget_lr_mult`, `--adapter_diag_level
  per_sample_recompute` (per-sample gradient diagnostics), `tools/local_fseval.py --scales ...` (forget-scale evals,
  default 0.0..1.0 step 0.1), `tools/expr_only_probe.py` (clean-environment solve rate).
- Countdown config `rl/configs/countdown_code_hack.yaml` exposes ground-truth per-hack-type channels
  (test_overwrite, constraint_relax, modify_input, other), so any monitor can be scored against programmatic truth.
- Dependencies: Python 3.11, CUDA 12.8, vLLM 0.17.0 with three patched files, TRL 0.29, external repo
  github.com/ariahw/rl-rewardhacking for graders and the LeetCode anchor data; Modal optional (pod path exists).
  "On 80 GB GPUs add --gen_batch_size 64" for 8B evals, so 80 GB cards work.
- Toy sweeps need CUDA MPS with a driver-matched binary; MPS does not work on Modal.
- Tinker cannot do this work (custom per-sample gradient masking and non-LoRA adapters), so rented GPUs are required.

Prices looked up 2026-11-14:
- RunPod on-demand (runpod.io/pricing): H200 141 GB $5.29/h; H100 PCIe 80 GB $2.89/h; H100 NVL 94 GB $3.19/h;
  A100 PCIe 80 GB $2.09/h; RTX Pro 6000 96 GB $2.69/h; L40S 48 GB $1.09/h; A40 $0.59/h.
- OpenRouter ($ per 1M tokens in/out): meta-llama/llama-3.1-8b-instruct 0.02/0.04; google/gemma-3-4b-it 0.05/0.10;
  google/gemma-3-12b-it 0.05/0.15; qwen/qwen3-32b 0.08/0.28; qwen/qwen3.7-flash 0.03/0.13; openai/gpt-5-nano
  0.05/0.40; anthropic/claude-haiku-5.5 0.10/0.50; qwen/qwen3-235b-a22b-2507 0.14/0.80.

## 4. Brainstorm (all candidates, with verdicts)

1. **GRAFT with real LLM monitors on Countdown-Code RL (weak full-transcript judge and reasoning-only judge), against
   reward penalty with the same monitors.** The paper's first limitation, Drori's "what we actually care about", and
   the first test of monitor false positives. Infrastructure exists (llm_judge detector, pod repro, public SFT init).
   ~14 Qwen3-8B runs. Achievable, ~$450. Interesting both ways. -> PROPOSAL 01.
2. **Absorption vs inoculation via exclusive routing** (FORGET never trained on unflagged samples), plus per-sample
   gradient-share diagnostics and forget-scale sweeps including negative scales. One existing flag; toy envs are cheap;
   the two settings in the paper (toy: undetected hacks learned then removed; Countdown: undetected hacks never
   emerge) give opposite predictions. ~$280. -> PROPOSAL 02.
3. GRAM with systematic (non-random) label errors on SimpleStories 26M (authors ask for it; code public; 26M
   pretraining is cheap). Achievable and worth doing, but only two slots and the GRAM post drew less interest than
   GRAFT; loss-only evals on children's stories make a weaker post. Not written up; best third option.
4. GRAM relearning robustness at 26M: paper already tests adversarial elicitation at 800M-5B. Low novelty. Rejected.
5. Instruction-tuning a GRAM model: needs an 800M+ pretrained GRAM checkpoint; checkpoints are not released. Rejected.
6. Drori's SFT experiment redone in RL with distinct hack strategies: Countdown already has 3 strategies with a
   type-1-only monitor (paper). Folded into proposal 01 (real monitor blind spots replace hand-chosen ones).
7. Drori's arms re-evaluated without the hack-elicitation prompt: needs Qwen3-32B SFT (8xH200 x 4 h ~ $170 per run
   plus agentic harness evals at 1-1.5 h per checkpoint). Over budget for a meaningful grid. Rejected.
8. Adapter as steering vector / negative scaling / layer ablations: partly done (LoReFT post's layer ablations; -1
   training variant in FOLLOWUP_WORK.md). The inference-time scale sweep is cheap, so it is a secondary analysis in
   proposal 02, not a standalone project.
9. Smaller FORGET adapter / LoReFT: done by Knoche. Rejected as duplicate.
10. Token-level routing in multi-turn trajectories: needs a multi-turn RL environment with localised hacks and a
    credit-assignment scheme; too much new infrastructure for two days. Rejected (stage-2 idea).
11. Scaling GRAFT RL to 32B or multi-turn agentic RL: over budget and fragile. Rejected.
12. Continuous monitor confidence as routing weight: natural extension of proposal 01 (LLM judge logprobs); listed
    there as stage 2.
13. Synthetic false-positive-rate sweep in toy envs (flip a fraction of honest samples to flagged): cheap and clean,
    but less compelling alone than a real judge; kept as the fallback/extension inside proposal 01's stage 2.
14. Very low hack base rate / very low routed fraction: paper has a recall sweep down to 0.1 in toy envs. Marginal.
15. Multiple FORGET adapters, one per hack type: interesting but needs code changes to adapters, vLLM patch and
    optimizer; risky in two days. Rejected for stage 1.
16. Mech interp of gradients during training: open-ended; the concrete, decisive part (gradient share of undetected
    hacks landing in FORGET) is inside proposal 02.
17. Does GRAFT's deployed model show less emergent misalignment / broader generalisation than reward-penalty models?
    Qwen3-8B Countdown models are too narrow for EM-style evals to be meaningful. Rejected.

## 5. Why two proposals

Both reuse released code paths that need a config change rather than new machinery, answer questions the authors
themselves posed, and are informative whichever way they come out. They are distinct: 01 changes the monitor
(realism of supervision), 02 changes the routing rule (mechanism).
