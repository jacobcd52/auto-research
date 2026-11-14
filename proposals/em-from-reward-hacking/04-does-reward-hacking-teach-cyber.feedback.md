# Feedback: 04 — Does learning to reward hack make a model better at CTFs?

Verdict: **major overhaul** (shrink to a ~$150 side-arm or merge into Proposal 01). As a stand-alone $380 project it is the weakest in the cluster and should be funded last.

## What I checked

| Claim in the proposal | Status |
|---|---|
| Hua's post: ~100,000 escalations, ~10,000 sandbox breaks, 70% confidence, two self-named failure modes | Correct (read in full). Note the 70% is attached to the whole story; his stated prediction is "noticeably less capable at cyber out-of-the-box". |
| Commenters split on the same lines | Correct, but the capability question is a minority of the thread. The top comments (71, 52, 32, 27, 27 karma) are about "hacking Anthropic" framing, disclosure and retraining. The capability-sceptic comments (markasoftware 10, jimrandomh 8) are low-karma. |
| Hacker-Opus showed willingness, not capability | Consistent with the post text; no capability measurement reported. |
| Redwood checkpoints `uwuwuwuwuwuwu/gpt-oss-120b-reward-hacker-step-{0,216,496,952}` and the reverse-inoculation one are public | Confirmed via HF API: public, ungated, PEFT LoRA r=32, `all-linear` plus unembed, exported from Tinker. |
| AISI pairs are public | Confirmed. But the Olmo pair is **not step-matched** (`sutl-b0.0-s160` vs `baseline-nohack-s100`), and the 20B base is `unsloth/gpt-oss-20b-BF16`. "Identical RL where only hack availability differs" is overstated for Olmo. |
| Learned hacks include replacing `/bin/bash`, module shadowing, reading expected outputs | Confirmed in Yudelson et al. But the post says the two *most common* GPT-OSS hacks are overwriting test code/data and printing expected outputs; the bash-replacement is the "most egregious", not typical. |
| "InterCode-CTF (100 picoCTF-style tasks)" in `inspect_evals` | **Wrong number.** `inspect_evals/gdm_intercode_ctf` exists but runs **78** tasks (22 need internet). Default `max_messages` is 50. |
| InterCode-Bash control in `inspect_evals` | **Does not exist** (`src/inspect_evals/intercode_bash` returns 404). `bigcodebench`, `cybench`, `gdm_in_house_ctf`, `threecb`, `cybergym`, `swe_bench` do exist. The agentic control has to be ported by hand or replaced. |
| Tinker prices for GPT-OSS-120B ($0.33 / $0.066 cached / $0.84) | Correct on the live pricing page. |
| "tool outputs truncated to fit the 32K context" | Unnecessary: Tinker lists a **GPT-OSS-120B (128K)** variant (`openai/gpt-oss-120b:peft:131072`) at the same prefill and sample prices. Whether an uploaded 32K-trained adapter can be sampled under that ID is untested. |
| Sampling "via its OpenAI-compatible API" | Risky. The OpenAI-compatible page (beta) documents chat and reasoning flags but **no tool calling**; the Anthropic-compatible endpoint explicitly documents `tools` / `tool_use`. Inspect's CTF agent needs tool calls. Plan for the Anthropic-compatible endpoint or the native SamplingClient with the cookbook GPT-OSS renderer. |
| `external_weights_upload_start/finish` exists | Confirmed. Files "must be exactly what `save_weights_external` exports". The HF adapters are Tinker exports, so the odds are decent, but still untested. |
| No experimental follow-up exists | I found none: nothing in the Hua comment thread, and four arXiv API queries (reward hacking + CTF / cyber / sandbox escape) returned zero hits. **Caveat: my web-search budget was exhausted, so this is a weaker check than it should be.** |

## 1. Would it get upvoted?

Probably not past 50 as specified.

- The 363 karma on Hua's post came from the "Anthropic sane-washed tens of thousands of sandbox breaks" angle. The capability hypothesis was the least-discussed part of it.
- The proposer expects a capability null. A null on a rank-32 LoRA trained on test-tampering will be read as "obviously, that was never a test of the Mythos claim", and the proposal concedes this in section 5.
- The fallback finding (hacker checkpoints use a planted out-of-scope answer file more) is already known. Yudelson et al. showed these checkpoints hack held-out environments (ImpossibleBench, Palisade Stockfish), and the contrastive-belief paper measured a 33 -> 86 pp grader-ward shift on the same Redwood GPT-OSS hacker. "Willingness, not skill" restates the Yudelson conclusion.
- A clean positive (CTF up relative to controls, rising with step, concentrated in matching categories) would clear 100 karma easily. I put that at about 5%.

Expected reception: 20-45 karma for the likely outcome. Comparable null-ish posts in the cluster (Yudelson, 90) had Redwood authorship and fresh training runs behind them.

## 2. Naturalness

It is a natural question, and the screener's follow-up note names it. But the natural experiment is the training one (RL with and without exploitable sandbox holes), which the proposal rightly declines on safety and cost grounds. What remains is a proxy that both sides can dismiss:

- The Redwood hacks need no privilege boundary to be crossed. The model already has write access to tests and to `/bin`. That is not practice at escalation or escape, which is the mechanism Hua proposes.
- The AISI organisms learned three memorisable one-liners on single-turn CodeContests. Nobody predicts those teach CTF skill, so that arm tests a hypothesis with no proponents.

So: mainline question, side-branch test. Not already done as far as I can tell.

## 3. Pre-mortem

Forecast:

| Outcome | Probability |
|---|---|
| Clear positive (capability up, dose-response) | 5% |
| Clear, tight negative plus clear propensity rise | 15% |
| Ambiguous mush (wide CIs, degraded late checkpoints, noisy controls) | 55% |
| Fails to run usefully in two days | 25% |

Specific failure reasons, most important first.

1. **The stated "informative negative" is not achievable at this sample size.** With 78 tasks (not 100), CTF solves are close to deterministic per task, so epochs add little. A paired difference has a standard error of roughly 3-4 pp; subtracting a second benchmark's change pushes the difference-in-differences to roughly 4.5-5 pp. A 95% interval of about +/-9 pp cannot "exclude +5 pp". The pre-stated 5 pp minimum effect is below what the design can detect.
2. **Difference-in-differences across different benchmarks is scale-dependent.** If base GPT-OSS-120B is near ceiling on InterCode-CTF (GPT-4o-class agents are reported in the 70-95% range on it; I could not re-verify a GPT-OSS-120B figure) and mid-range on the control, a uniform ability change shows up as a spurious interaction. Use logit scale or per-task difficulty matching.
3. **No valid control for the Redwood run.** Dose over RL step is confounded with generic RL drift, SWE practice and the late-run degradation Yudelson reports. A CTF gain would be equally explained by "more agentic bash practice". The proposal admits this; it is still fatal for attributing anything to hacking.
4. **Propensity confound inside the capability metric.** The hacker checkpoints spend turns on "let's cheat" searches. In a CTF with a fixed turn cap that either burns budget (score down) or finds unintended solutions (score up). Solve rate then measures disposition, not skill.
5. **The planted-shortcut arm has a measurement problem.** Exploring the filesystem is normal CTF behaviour. A readable answer file outside the challenge directory may be used at a high base rate by step-0 too, and "acknowledges the rule" needs judge labels on ambiguous transcripts. Thirty tasks times 5 epochs is 30 independent units.
6. **AISI arm will likely sit at the floor.** GPT-OSS-20B and Olmo-32B are weak multi-turn tool users; serving harmony-format tool calls with LoRA on vLLM is fiddly; the `sutl` organisms were trained with hint prompts; the Olmo pair differs in step count. Expected output: two low, noisy numbers with overlapping intervals.
7. **Infra.** Tinker upload unverified; tool calling on the OpenAI-compatible endpoint undocumented; InterCode-Bash must be ported; the GPU fallback is not real (see cost).

## 4. Cost check

- Tinker line items are roughly right. Reasoning at default effort will produce more than 8k output tokens per 20-turn run; allow 15-25k. That adds about $0.01-0.02 per run, so Tinker spend is about $200 rather than $158.
- **The $98 fallback does not buy a fallback.** GPT-OSS-120B in bf16 with a 5.26 GB all-linear LoRA (MoE expert layers included) needs about 4x80 GB or 2xH200 after merging, at roughly $8-10/h. $98 is about 10 hours for five checkpoints and 3,750 agentic runs, before debugging. A real fallback is $300-500 and takes the project over the cap.
- AISI arm at 22 H100-hours for four adapters across two base models and two benchmarks is tight but plausible.

My estimate: **$350-450 if Tinker upload and tool calling work; over $500 if not.** If upload fails, the Redwood half should be cancelled, not rescued.

## 5. Recommended changes

1. **Do not fund as a stand-alone $380 project.** Either cut it to a ~$150 "quick look" or run it as an extra arm of Proposal 01, which already serves the same Redwood checkpoints on Tinker.
2. **Drop the AISI arm entirely.** It tests a branch nobody defends, on models likely at the floor, with a non-matched pair. This removes the GPU line and most of the infra risk.
3. **Fix the facts:** 78 tasks, not 100; no InterCode-Bash in `inspect_evals`. Use the 128K context variant and the default 50-message cap instead of truncation and 25 turns, to reduce under-elicitation.
4. **State an honest detectable effect** (about 10 pp) or raise the task count: add `gdm_in_house_ctf` and Cybench's easiest tasks, and pick tasks so base solve rate is 30-70%. Pre-register analysis on the logit scale.
5. **Make the capability measure propensity-proof.** Score "solved by the intended route" by transcript review, and report unintended-route solves separately. Otherwise the headline number is uninterpretable.
6. **Replace the generic controls with a targeted contrast.** The hypothesis predicts gains on tasks that resemble the learned hacks (file-system and environment manipulation, privilege-escalation-flavoured tasks) and none on crypto or forensics. A within-benchmark category contrast is a better control than BigCodeBench and needs no second harness.
7. **Rework the shortcut arm or cut it.** If kept: put the artefact behind an explicit, unambiguous prohibition, include a no-artefact baseline and a base-model baseline, and use at least 60 tasks. Say plainly how it differs from Yudelson's held-out hacking results; if it does not, cut it.
8. **Gate in hour one:** adapter uploads, tool calls round-trip, step-0 matches base within noise. If any fails, stop and return the budget.
9. **Reframe the title.** "A first test of the Mythos hypothesis" over-claims for what a null here can show. Something like "Do public reward-hacker checkpoints get better at CTFs?" is what the data supports.

If the funder must choose within the cluster, Proposals 01-03 are better uses of the money; this one is worth at most a small rider on 01.
