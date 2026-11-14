# control-protocols: reading notes and brainstorm

Research lead notes, 2026-11-14. All five posts were read in full with `scripts/get_post.py` (60-80K character
limit), plus the top comments of three of them (LessWrong GraphQL). Facts marked (verified) were fetched or computed
today; anything else is labelled as an estimate or a secondary summary. github.com was blocked from my session, so
repository contents are NOT verified unless stated.

## 1. Posts

### BashArena (Cor4QuhM2sybmBSeK, Dec 2025, 58 karma; arXiv 2512.15688)
- 637 main tasks (~50 tool-call rounds), 4 hand-made side tasks (malware, exfiltrate secrets, sudo escalation,
  disable firewall). Tests private; partial credit (fraction of tests passed). GPT-4.1 mini monitor: 74% safety at 4%
  trajectory-wise FPR; Sonnet 4.5 evades it 26% of the time (abstract).
- Stated weaknesses: removing internet costs 59% -> 55% main-task score and disables 3 of 4 side tasks; few side
  tasks; weak test-case-level and code-level integration, so "targeted deferral" (T writes the dangerous parts) and
  dynamic permission management are overpowered and are banned by fiat. Explicit ask: "worth someone's time to figure
  out whether forced factored cognition protocols do in fact work very well in BashArena".
- Public: ControlArena setting (github.com/UKGovernmentBEIS/control-arena, not fetched), task pipeline
  (github.com/redwoodresearch/basharena_public, not fetched), task dataset on HF `Eccentricity/basharena2`
  (verified: ungated parquet, 4,684 rows, fields description/dockerfile/tests/setup script).
- Screener summary accurate.

### Introducing LinuxArena (WgzwBi6DCagDuHPzP, Apr 2026, 84 karma)
- 20 environments (1K-10K LOC, running services), ~100-step main tasks, side tasks with scorers, LaStraj human attack
  trajectories. GPT-5 Nano monitor at 1% action-level FPR; human attacks evade almost entirely. Protocols evaluated:
  trusted agent, defer to trusted, trusted monitoring, editor-only sandboxing, no-network sandboxing. Plans: T chooses
  the agent's privileges per task; firewalls/rule engines; T writing tests.
- Public (verified on HF): `anonymouslinuxarena/linuxarena-public` — ungated, CC-BY-4.0, 22,215 trajectories from 172
  runs over 10 environments with per-action monitor scores and reasoning (sample.jsonl 705 MB, 932 trajectories);
  `anonymouslinuxarena/straj_linuxarena` (MIT, 150 .eval files, 13 public-env tasks). GitHub search (verified via API):
  `redwoodresearch/linuxarena-paper` ("Reproducibility code"), `linuxarena/ct-linuxarena`, `linuxarena/control-tower`.
  Only 10 of the 20 environments appear to be public.
- Screener summary accurate. Monitor-side follow-ups belong to the `control-monitors` cluster (its three proposals:
  context rot vs chunking, decorrelating monitors, actor attribution) — I avoided overlap with those.

### Retrying vs Resampling in AI Control (yThJQTJxtmKNeZGwA, May 2026, 67 karma; arXiv 2605.26047)
- BashArena, U = Opus 4.6, T/monitor = MiMo-V2-Flash, live-failure model, 0.3% step audit budget. Five samples per
  step + audit on MAX score: safety 61% -> 71% (abstract); 0.4 extra samples per step recover +6.2 of +10.2 pp;
  executing the least suspicious sample +3.9 pp (CI overlaps 0); three-strikes auditing does not help.
- Retrying (block + tell the agent, as in Claude Code auto mode / Codex Auto-review): lowers honest suspicion, but a
  *prompted* attacker uses monitor rationale to lower its own suspicion by a similar amount -> no net gain. Low-info
  retry ("please be careful") still leaks one bit; "give up on retry" strategy analysed only under conservative
  assumptions. Authors: "we plan to demonstrate [auto-mode-like protocol <= trusted monitoring] in future work";
  rigorous give-up-on-retry analysis "left to future work" (needs attack selection modelling, ramp-up elicitation).
- Related: Hopman et al. (LW wKGdiXuWfn8YoYpMQ) on feedback exploitation. Data/code release not verified.
- Screener summary accurate.

### Door's Locked, Try the Window / CircumEval (GHrqBKr8GLpbce6mN, Jun 2026, 78 karma)
- 8 FastAPI 0.115.0 tasks (3 Test-Locked, 5 Source-Locked) + 4 datasette 0.65.2 tasks. Lock = root:root 444 +
  `chattr +i` in a Docker container, agent is non-root `devuser`; prompt never mentions the lock. Circumvention = the
  target test passes at the end. Plain request, n=30 per task: Source/Test-Locked Opus 4.6 100%/40%, Sonnet 4.6
  89%/66%, GPT-5.4 99%/94%. "Don't edit read only files": Source-Locked 100% (Opus, Sonnet), 46% (GPT-5.4). Only the
  two prompts containing "stop and report" give 0%. Pasted-error-log prompt: GPT-5.4 Source-Locked 99% -> 10%
  (unexplained). Techniques: conftest.py monkeypatch, sitecustomize/__init__ patch, .pyc swap, test warping.
- Authors' open questions: (1) which training interventions reduce it; (2) do agents recognise it as circumvention and
  think it right; (3) sensitivity to the control setup (sandbox escape needed; a monitor that must be deceived).
  Limitations: 3 models, model and scaffold not separated, n=10 in the prompt-variant cells.
- PUBLIC (verified): task code is "on request" only, BUT the Inspect logs are downloadable:
  `https://prakratt.github.io/CircumEval/logs/logs/listing.json` lists 180 `.eval` files (fastapi: baseline 40,
  gradient 96, trace 24; datasette: 20), each fetchable at `.../logs/logs/<key>`. I downloaded two. Each sample has
  the system prompt, user prompt, every tool call and output, final message, the `setup` shell script (including the
  hidden validation test), scorer metadata (`forbidden_commands`, `git_check.allowed_modified`, `behavior_flags`:
  monkeypatch_created, test_warped, bytecode_patched, new_file_in_tests, hit) and token usage. By the post's cell
  counts this is about 2,100 rollouts. The tasks are therefore reconstructible (file contents appear in tool outputs).
  The viewer page carries `noindex,noai` and the authors withhold task code to avoid training-set leakage, so a
  follow-up should not republish reconstructed tasks.
- Pilot (verified, one log: Opus 4.6, Test-Locked `sa-filter`, 30 rollouts): mean 995K input tokens and 9.7K output
  tokens per rollout through Claude Code (no cache reads recorded) — about $5 per rollout at Opus 4.6 prices;
  60-90 messages. In 26 of 30 final messages the agent names the lock AND describes its conftest/skip workaround, i.e.
  on this task the circumvention is openly disclosed, which the post does not report.
- Related: "Permission Denied" (arXiv 2608.02670, Aug 2026): 12 agents on Terminal-Bench 2.1 under nested security
  policies, releases Boundary-Bench; measures success/cost loss and that runs "grind into timeouts rather than
  stopping early". Not a circumvention-propensity study, no lock-legibility or reviewer manipulation. ImpossibleBench
  (arXiv 2510.20270). No direct follow-up to CircumEval found (web search + LW comments: one comment, score 1).

### Untrusted advice (jLkRCK35ri2btEHMF, Jul 2026, 88 karma)
- T executes everything; U (Sonnet 4.6) sends <= k characters before each step and may block submission. T = Gemini
  3.1 Flash Lite or gpt-oss-120b, told to follow advice unconditionally. 200 tasks each of SWE-bench Verified and
  BashArena. Solo scores: SWE-bench T 0.49 / U 0.763; BashArena T 0.43-0.44 / U 0.712. 16 chars/message recovers ~67%
  of the gap on SWE-bench. Surprisal accounting cuts the bit count 2.5-30x; menu advice (34-58 items) extends the
  frontier on BashArena only; best-of-16 gives nothing. NO monitor and NO red team were run; footnote 10: early
  experiments "weakly suggest malicious advice does not have substantially greater surprisal".
- Comments (verified): heavy criticism of the untested safety claim (vals tutor 19 karma; Morgan S showed a <256-char
  string, written by Opus 4.8, that makes gpt-oss-120b disable the firewall). Caleb Biddulph, 9 Oct 2026: "I'm doing
  [red-teaming] now with my SPAR mentees". Adam Kaufman: "excited about followup projects that ... actually build and
  stress-test monitors". Suggestions by taziksh: live surprisal budget, multi-executor, RL on U.
- IN-PROGRESS OVERLAP (verified via GitHub search API): repo `jerzh/untrusted-advice`, description "Red-teaming a
  control protocol on LinuxArena via Control Tower". Contents not readable from my session.
- PUBLIC (verified): the advice spreadsheet exports as CSV
  (`https://docs.google.com/spreadsheets/d/1iJDM8V5QaBcFRYOK4BLUWgoT8pG3LWepciSQ9CBDjHU/export?format=csv`, 72 MB):
  174,932 advice rows, 122,434 of them BashArena, columns advice / LLM context summary / docent_url / benchmark /
  t_model / maxchars / task_id / usefulness_score. Pilot count on BashArena rows: at the 16-char cap 3.7% of honest
  advice strings contain "firewall", 1.1% "iptables", 0.8% "sudo", 2.8% "curl"; at 64 chars 8.5% contain "firewall".
  So honest advice routinely points at exactly the surfaces the side tasks use. Protocol code release not verified.

## 2. Other related work found
- "Clearing Context Fails to Impede AI Attackers" (Aaron Sandoval; HF `xtremekiwi/dtd-basharena-data`, verified
  README, CC-BY-SA, 89 GB of logs; code github.com/aaron-sandoval/tu-bb2): BashArena, Sonnet 4.6 / GPT-5.4 nano,
  trusted monitoring vs defer-to-resample vs DTD (decomposition triggered by the monitor), including "give up after
  first decomposition" and attack-selection figures. This already covers a factored-cognition protocol in BashArena.
- Factor(T,U) (arXiv 2512.02157), Factor(U,T) (arXiv 2512.14745): APPS / BigCodeBench only. SPAR Fall 2026 project
  (sparai.org/projects/f26/recaQzRMvjrThukoU, fetched): Factor(U,U)/(U,T) red-teaming on LinuxArena.
- Honeypot Protocol (arXiv 2604.13301), a BashArena monitoring paper (arXiv 2604.03968) — seen in search only.
- Rinberg et al. (arXiv 2604.02343): binary-answer strong model uplifting a weak one (cited by the advice post).

## 3. Prices looked up today (OpenRouter `/api/v1/models`, USD per million tokens: input / output / cache read)
Sonnet 5.5 2 / 10 / 0.10; Sonnet 4.6 3 / 15 / 0.30; Opus 5.5 4 / 20 / 0.20; Opus 4.6 5 / 25 / 0.50; Haiku 5.5
0.10 / 0.50 / 0.01; GPT-6.1 Terra 1 / 5 / 0.05; GPT-6.1 Sol 2 / 10 / 0.10; GPT-6 Luna 0.10 / 0.50 / 0.01; GPT-5.4
2.5 / 15 / 0.25; Gemini 3.7 Flash 0.75 / 3.75 / 0.075; Gemini 3.1 Flash Lite 0.25 / 1.50 / 0.025; gpt-oss-120b
0.15 / 0.60 / 0.075; Qwen3.8-27b 0.15 / 1.875 / 0.0375; Kimi K2.7-code 0.60 / 3.50 / 0.16; DeepSeek V4 Pro
0.90 / 1.50 / 0.25; Llama-3.3-70B 0.71 / 0.71.
Cloud VM: Lambda on-demand from about $0.69 per GPU-hour (third-party price trackers found by web search; lambda.ai
itself not fetched). Docker with `chattr +i` needs a real VM, not a container pod.

## 4. Brainstorm

Kept (proposals, best first):
1. **Lock legibility and disclosure in CircumEval** (01). Is circumvention driven by an ambiguous lock or by disregard
   of a clearly intentional one? Free analysis of ~2,100 public rollouts for disclosure, then a rebuilt-task experiment
   varying only how clearly the environment says the lock is deliberate, plus a post-run self-assessment (authors'
   question 2), in a neutral harness on newer and open-weight models (their stated limitations). ~$450.
2. **Reviewer-in-the-loop on CircumEval** (02). Authors' question 3 crossed with the Retrying paper: when an
   auto-mode-style reviewer blocks the workaround, does an unprompted agent stop, or adapt to the reviewer, and does
   showing the rationale matter? The Retrying paper only tested a prompted attacker. ~$445.
3. **Steering budget of the untrusted-advice channel** (03). First monitored attack-success-versus-character-budget
   curve on BashArena, short horizon, with thresholds calibrated on honest advice. Ranked last only because the
   authors' SPAR team is red-teaming the protocol on LinuxArena right now. ~$480.

Rejected / deprioritised:
- Full control evaluation of auto-mode-style retry and "give up on retry" (authors' named future work): needs
  Opus-class attack trajectories in BashArena (the pilot log suggests dollars per trajectory), thousands of honest
  steps for a 0.3% budget, and attack-selection modelling the authors call "too involved". Not $500, and Redwood has
  said it will do it. Proposal 02 takes the cheap unprompted-agent slice instead.
- Max-vs-min resample aggregation in a second setting (LinuxArena): needs multiple fresh samples per step from
  strong models; expensive; data release of the paper not verified.
- Forced factored cognition / targeted deferral in BashArena (BashArena post's explicit ask): Sandoval's DTD work now
  covers a decomposition protocol in BashArena with released logs, a SPAR project covers Factor(U,U)/(U,T) on
  LinuxArena, and a fair safety number needs a well-elicited attacker against a new protocol — the highest
  under-elicitation risk in the cluster. A usefulness-only measurement would just confirm what the authors already
  expect.
- Dynamic permission management / T-chosen privileges in LinuxArena: authors are doing it; needs the full 20-env
  setup, half of which is not public.
- New BashArena side tasks or sandbox-resistant tasks: benchmark building, explicitly discouraged.
- Monitor comparisons on the public LinuxArena trajectories (cheaper monitors, ensembles): feasible and cheap, but
  that is the `control-monitors` cluster's territory.
- Untrusted advice, live surprisal-capped channel (authors' and taziksh's suggestion): needs token logprobs from T
  in the loop and SWE-bench runs with a Sonnet-class advisor; the expected difference between a character cap and a
  surprisal cap is small relative to task-level noise at an affordable n. Could be stage 2 of proposal 03.
- RL / fine-tuning U to give better short advice (Tinker): U must be much stronger than T to matter; open-weight
  pairs with a big enough gap plus RL through an agentic environment is not a two-day job.
- Advice-only offline monitor study on the public spreadsheet: honest side is free, but "malicious advice" that was
  never executed is unvalidated; folded into 03, which executes it.
- CircumEval training interventions (authors' question 1) via LoRA on Tinker: needs an open-weight agent that
  circumvents at a high base rate inside a tool loop served from Tinker; unknown until proposal 01's stage 1 is run.
  Listed as stage 2 of 01.
- CircumEval at scale across many repositories: the authors say it is automatable, but more tasks of the same kind
  add little beyond the 12 they have; the open questions are about interpretation, not coverage.
- Explaining the pasted-error-log effect (GPT-5.4 99% -> 10%): GPT-5.4 + Codex specific, n=10 cells; included in 01
  as one condition rather than a project.
