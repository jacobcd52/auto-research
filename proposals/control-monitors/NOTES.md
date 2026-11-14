# control-monitors: reading notes and brainstorm

Research lead notes, 2026-11-14. All seven posts were read in full via `scripts/get_post.py`. Facts marked
(verified) were fetched or computed today; everything else is labelled as an estimate or as a secondary summary.

## 1. Posts

### Monitoring benchmark for AI control (X8qTKsGcnsTFrqM96, Jan 2026, 52 karma) — preview of MonitoringBench
- 428 firewall-only BashArena attack trajectories; taxonomy T (technical), S (structural), E (evasion); human-seeded
  strategies executed by Opus 4.5; 4-step refinement (review, plan, rewrite, validate) re-executed in ControlArena.
- Monitor input: full trajectory of tool calls only; output 1-10 score; caught = above top-1% honest score
  (400 honest Opus 4.5 runs). Basic ControlArena monitor prompt, not elicited per monitor.
- HARD set: Opus 4.5 71% caught, GPT-5 11%, GPT-5-nano 0%. "Most monitors detect most attacks but fail to escalate"
  (mentions the IP in the rationale, but assumes good intent). What works for attackers: blending with the main
  task, over-engineering, minimal justification, distraction.
- Screener summary accurate. Screener's "benchmark available on request" is OUT OF DATE (see next post).

### Introducing MonitoringBench (2YyEQhFRyaBCgfRWd, Jun 2026, 59 karma; arXiv 2605.09684)
- 2,644 successful attack trajectories, 4 BashArena side tasks, sources: Opus-only, human-in-the-loop, recon,
  recon+tools, each with and without post-hoc refinement. 13 full-trajectory + 7 stepwise monitors; 3 dev monitors
  (Opus 4.5, GPT-5, GPT-5 Nano) used to accept refinements, the rest held out.
- Opus 4.5 catch rate 94.9% (elicited Opus attacks) -> 60.3% (best refined). 40% of uncaught attacks are T1 (simplest
  technique + right framing). Failure taxonomy by 3 LLM judges: (A) not detected, (B) partial, (C) detected but
  dismissed/persuaded, (D) under-scored. Opus 4.5 mostly C ("invents a justification itself"), GPT-5 82% D,
  GPT-5.1 Codex B, Sonnet 4.0 A.
- Authors' follow-ups: fix persuasion (C) and calibration (D); extend to LinuxArena. Appendix O: prompt tweaks on
  monitors gave non-robust improvements. Limitations: thresholds from honest BashArena runs; attacks all written by
  Opus 4.5/4.6 (possible family bias); monitors not individually elicited.
- Structural tiers (verified from arXiv HTML): S1 single step; S2 local multi-edit; S3 multi-file, concentrated in a
  tight cluster of steps; S4 distributed across the trajectory (>3 files or steps with benign work in between).
  Evasion: E1 benign naming, E2 over-performance on main task, E3 string obfuscation, E4 persuasion / error camouflage.
- PUBLIC DATA (verified): https://huggingface.co/datasets/neur26anonsub/ctrldataset2026 — ungated, CC-BY-4.0.
  `master.parquet` (2.9 MB, 2,644 rows x 135 cols) and `final_dataset.zip` (2.47 GB of inspect_ai `.eval` logs under
  `firewall/ malware/ password_leak/ sudo/` x `{human_strategies, opus_only, recon}[_refined]`). I downloaded the
  parquet and listed the zip's central directory. Columns: ids, side task, source, attack model (1,935 Opus 4.5 /
  709 Opus 4.6), `ft_<monitor>_monitor_score_{0,1,2}` for 13 monitors (3 runs each), `sw_*` stepwise scores,
  `attack_step`, `total_steps`, taxonomy labels with explanations, `attack_summary`. Counts: refined 1,141, recon 796,
  human-in-the-loop 511, Opus-only 196; S1 714, S2 219, S3 1,209, S4 475; E4 present in ~1,634 rows; tool calls per
  trajectory mean 31 (9-60).
  **No honest trajectories and no monitor rationales are in the release** (zip has no honest folder).
- Code: anonymised link https://anonymous.4open.science/r/control-arena-D51B/README.md (not fetched).
- Pilot I ran on the parquet (verified, score run 0, Spearman rank correlation across the 2,644 attacks, held-out
  monitors only: Anthropic = Opus 4.0, Sonnet 4.5, Sonnet 4.0; OpenAI = GPT-5.1 Codex Max, o3, o4-mini, GPT-4.1):
  mean within-lab correlation 0.63 vs cross-lab 0.55 on all attacks; 0.47 vs 0.36 on the 1,141 refined attacks.
  Test-retest of one monitor (run 0 vs run 1): 0.72-0.93. Confound: capability similarity is not controlled.

### Releasing Benign Trajectories for MonitoringBench (bdBoH23TCTFZkkfqp, Palaestra Research, Nov 2026) — not in
cluster but essential
- 550 honest Opus 4.5 trajectories on the same 116 BashArena tasks, per-task frequency matched to a 550-attack
  subset; fairness-screened with GPT-5.6 Sol (score >= 7 dropped and regenerated); submit step cut; `command` -> `cmd`.
- Honest mean 24.4 steps x 1,281 chars/step (~31K chars); paired attacks 27 x 1,019 (~27.5K chars). So roughly
  8-9K tokens per trajectory (my estimate at ~3.5 chars/token).
- Their single-prompt results on the 1,100 set: Kimi K3 TPR .858 / FPR .024; GPT-5.6 Luna .925 / .315;
  Qwen3.8 27B .860 / .204; DeepSeek V4 Flash .485 / .031. (Binary answers, not fixed-FPR.)
- PUBLIC (verified): https://huggingface.co/datasets/palaestraresearch/monitoringbench-honest-550 (98 MB zip of 59
  original `.eval` files + `manifest.jsonl` + loader; logs include assistant reasoning, so strip to the same fields
  as the attack side). Pipeline repo: https://github.com/CanKucukkurt/monitoringbench-honest-pipeline (README
  fetched; includes `pipeline/mb_solo_monitor.py` with OpenRouter transport). Processed version on Docent.
- Says it is now used in Redwood's Control Tower (https://github.com/linuxarena/control-tower, not fetched).

### OpenAI: How we monitor internal coding agents for misalignment (syB2r2X4E7nmw58co, Mar 2026, 95 karma)
- Short linkpost. GPT-5.4 Thinking monitors 99.9% of internal coding traffic with full context incl. CoT; review
  within 30 min for high severity; examples: base64 to dodge monitors, calling other instances, uploads, prompt
  injecting users. The linked OpenAI page returned HTTP 403 to my fetch, so details beyond the LW text are unverified.
- Screener's follow-up idea (small planted-behaviour benchmark) is superseded by MonitoringBench, SLEIGHT-Bench
  (arXiv 2605.16626, 40 hand-built attacks, public) and Screwtape.

### Classifier Context Rot (7vpvNM7viJqNWAdG7, May 2026, 56 karma; arXiv 2605.12366)
- Needle insertion into the author's own Claude Code transcripts, and MonitorBench (January firewall preview)
  transcripts padded with clean Claude Code transcripts. Opus 4.6, GPT-5.4, Gemini 3.1 Pro miss attacks 2-30x more
  often with 800K tokens of benign prefix. Worst in the middle; more reasoning helps; incremental monitoring
  (classifying every truncated prefix, optionally subsampled) helps; per-tool-call reminders help on needles but not
  on padded MonitorBench; GPT-4.1 fine-tuning did not generalise.
- Method limits stated by authors: binary output, FPR only roughly held below 2% by prompt tweaks and "not measured
  precisely"; only attacks spanning a short section; "multi-step attacks spread over the full context could be even
  harder ... future work".
- Code (README fetched): https://github.com/samm393/classifier-context-rot — **transcripts, MonitorBench samples and
  the monitoring prompt are NOT included** (`PLACEHOLDER_PROMPT`). So the result is not reproducible from public
  material as released; MonitoringBench + the honest set now make a public version possible.
- No follow-up found on chunked/hierarchical monitors vs distributed attacks (two web searches).

### Claude summarizes behavior as less misaligned when the actor is Claude (ZTMw4uAwkNmXFpdfg, Aug 2026, 58 karma)
- One real (non-public) Apollo report, model name edited. Sonnet 5 rates it ~1.2 SD less concerning for Sonnet 5 than
  for GPT-5.6 Terra; Terra and Kimi agree in direction; Gemini 3.1 Pro refused numbers. Author flags low effort.
- Related (verified abstract): arXiv 2603.04582 "Self-Attribution Bias: When AI Monitors Go Easy on Themselves" —
  monitors are more lenient when the action sits in a previous assistant turn; **explicitly stating the action is
  the monitor's own does NOT induce the bias**. So explicit naming has one null (self) and one positive (Newman).
- No replication/follow-up found.

### Simulated Control Evaluations (uXiqyoKwpfjWfQXk5, Oct 2026, 65 karma; arXiv 2610.31593)
- LLM simulator (gpt-6-astra) replaces the environment; judged attack success; validated against executed LinuxArena.
  Safety RMSE 3.6 pp vs 10.1 for BashArena as predictor. Next steps: hybrids, training in simulation, validation on
  real transcripts, untrusted simulators, multi-agent. Code release not verified.

### Control monitors need alignment assessments too (2wbW2WY3bP9Jzn4R5, Oct 2026, 67 karma)
- Opinion piece. Monitor false negatives are often alignment failures (priority balancing, inherited motivated
  beliefs). Project list: monitor the monitors' CoT; **understand decorrelation (different labs? sanitising
  transcripts? fine-tuning? unsupervised summarisation?)**; training overfitting to monitor evals; automated
  behavioural evals for monitors (Screwtape); model organism of a misaligned monitor; training against monitor evals.

## 2. Other related work found (all 2026)
- Screwtape (LW Z8jjgjfpAJocqZiET; arXiv 2610.20941): edits real transcripts and iterates against a monitor; 252 runs,
  35 evading proxies, 6 evading a held-out lab monitor. Redwood staff transcripts, not public.
- Ensemble Monitoring for AI Control (LW x3iEYuMHPXBpnCNpw; arXiv 2605.15377; code
  github.com/Multi-Signal-Control-SPAR/Multi-Signal-Monitoring): on APPS backdoors, diverse prompt/fine-tune variants
  of ONE base model (GPT-4.1-mini) beat resampling. Not cross-lab, not agentic trajectories.
- Calibration-Family Overfit (arXiv 2607.06596): trained monitors transfer poorly across *agent* lineages on code
  backdoors (41% vs 19% caught at 1% budget). About the attacker's family, not monitor-monitor decorrelation.
- Apollo, "Evaluating LLM Calibration for Coding-Agent Monitoring" (Jul 2026): 16 LLMs, severity calibration on
  injected failures; a search summary says Anthropic models judge very similarly and cross-provider ensembles
  calibrate better (secondary summary, not verified by me).
- Bootstrapped Monitoring (arXiv 2606.11998), untrusted-monitoring safety case (arXiv 2602.20628),
  "Self-monitoring doesn't scale" (LW RWabdkaKTT3FXtbs9).

## 3. Prices looked up today (OpenRouter `/api/v1/models`, USD per million tokens, input / output)
Haiku 5.5 0.10 / 0.50 (batch 0.05 / 0.25); Sonnet 5.5 2 / 10 (batch 1 / 5); Opus 5.5 4 / 20 (batch 2 / 10);
GPT-6 Luna 0.10 / 0.50 (batch 0.05 / 0.25); GPT-6.1 Terra 1 / 5 (batch 0.50 / 2.50); GPT-6.1 Sol 2 / 10 (batch 1 / 5);
Gemini 3.1 Flash-Lite 0.25 / 1.50 (batch 0.125 / 0.75); Gemini 3.7 Flash 0.75 / 3.75 (batch 0.375 / 1.875);
Gemini 3.1 Pro preview 2 / 12 (batch 1 / 6); Kimi K3.1 Pro 2 / 10 (batch 0.70 / 6); Qwen3.8 Max 0902 2 / 6;
Qwen3.8 Flash 0.15 / 0.47; DeepSeek V4 Pro 0.90 / 1.50; DeepSeek V4.1 Flash 0.051 / 0.203.
Old MonitoringBench monitors still listed: Opus 4.5 5 / 25, Sonnet 4.5 3 / 15, GPT-5 1.25 / 10, GPT-5.1 Codex Max
1.25 / 10, GPT-4.1 2 / 8, o3 2 / 8. All the models above except the Kimi K2 and older Qwen lines list 1M context.

## 4. Brainstorm

Kept (proposals):
1. **Context rot vs chunk blindness** (01). Public, score-based, fixed-FPR rebuild of the context-rot result from
   MonitoringBench + honest set, then full-context vs chunked vs summary-carrying monitors on attacks whose parts are
   separated by benign work. Explicitly named as future work by the authors; original data is private. API only.
2. **Decorrelation levers** (02). Fabien Roger's two concrete questions (different labs? sanitised transcripts?) on
   MonitoringBench + honest set at fixed FPR and matched cost. Pilot signal exists in released scores.
3. **Actor attribution in control monitors** (03). Does the Newman effect move real monitor verdicts on a benchmark
   with ground truth? Cheapest; prior evidence conflicts (Newman positive, 2603.04582 null for explicit self-naming).

Rejected / deprioritised:
- Improve calibration/persuasion resistance by prompt engineering on MonitoringBench: the paper's Appendix O already
  found prompt changes non-robust, labs have iterated privately, and it is a crowded, low-novelty direction.
- Fine-tune an open-weight monitor on MonitoringBench and test generalisation to held-out side tasks / SLEIGHT-Bench
  (Tinker): feasible, but the honest-set release post explicitly targets trained classifiers (SFT, RLAIF, debate), so
  it is probably under way elsewhere; 8K-token examples make iteration slow; kept as stage 2 of proposal 02.
- "Training against monitor evals: how bad is overfitting?": same infrastructure as above, more interesting, but
  needs two independent attack distributions with honest sets; only MonitoringBench has one. Too thin for 2 days.
- Model organism of a misaligned monitor: a monitor trained to be lenient only off-distribution passes evals by
  construction; would need a careful design to say anything non-obvious. Not in 2 days.
- Correlated agent/monitor *motivated-belief* failures with natural (uninstructed) misbehaviour (screener's idea for
  the Roger post): the right experiment, but it needs a setting where current agents rationalise their way into bad
  actions at a usable rate; building and validating that is a new-environment project with high under-elicitation
  risk. Proposal 03 covers the cheap, well-posed slice (attribution); proposal 02 covers decorrelation.
- Monitoring the monitors' CoT for misalignment signs: needs monitor rationales; not in the release, would have to
  regenerate, and "signs of misalignment" has no ground truth. Folded into 02 as a small rationale analysis.
- Small planted-behaviour benchmark for the OpenAI post (base64, delegation): superseded by MonitoringBench (E3),
  SLEIGHT-Bench and Screwtape.
- SCE follow-ups (hybrid sandbox+simulation, untrusted simulators, weak simulator vs strong attacker): need
  LinuxArena execution at scale and a frontier simulator (gpt-6-astra at $10/$50 per M); the validation design alone
  exceeds $500 and is a long fragile pipeline. A "does a cheap simulator suffice" ablation is plausible but I could
  not verify a public SCE code release.
- Extending the MonitoringBench refinement pipeline to LinuxArena: authors' own next step, heavy docker execution,
  not a 2-day project.
- Stepwise-vs-full-trajectory analysis from released `sw_*` scores: free, but descriptive; used as supporting
  analysis inside 01 rather than a project.
- Replicating Newman with more reports only: his report is private; public reports can substitute, but a
  ratings-only replication has no link to monitoring outcomes. Included in 03 as the positive control.
