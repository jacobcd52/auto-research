# Cluster: AI control: settings and protocols

key: `control-protocols` — 5 post(s); write at most 3 proposal(s).

## BashArena: A Control Setting for Highly Privileged AI Agents
- id: `Cor4QuhM2sybmBSeK` | 2025-12-18 | 58 karma | james.lucassen, Adam Kaufman 
- url: https://www.lesswrong.com/posts/Cor4QuhM2sybmBSeK/basharena-a-control-setting-for-highly-privileged-ai-agents
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Releases BashArena, a high-stakes control setting with 637 complex main tasks (system monitoring, data processing, systems programming, etc., ~50 tool-call rounds each) and four side tasks representing security failures, intended to support more complex attacks and stronger trusted/untrusted model pairs than earlier settings. Discusses lessons and weaknesses, e.g. removing internet access costs little main-task performance (59% to 55%) while disabling three of four side tasks.
- screener's follow-up note (often the screener's inference): Authors want better resistance to sandboxing and more side tasks; follow-ups can benchmark monitoring and resampling protocols and new attack policies in the setting.
- builds on: AI Control: Improving Safety Despite Intentional Subversion; Ctrl-Z

## Introducing LinuxArena
- id: `WgzwBi6DCagDuHPzP` | 2026-04-20 | 84 karma | Tyler Tracy, Ram Potham, Nick Kuhn
- url: https://www.lesswrong.com/posts/WgzwBi6DCagDuHPzP/introducing-linuxarena
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Releases LinuxArena, a control setting of 20 software-engineering environments (production-like systems) each with SWE main tasks, possible safety failures (side tasks) and covert sabotage trajectories. Reports monitor results (e.g. safety of a GPT-5 Nano monitor at 1% action-level FPR) against Opus attacks, Opus attacks with strategies, and human-written attacks; the setting was used in the Claude Mythos Preview system card.
- screener's follow-up note (often the screener's inference): Use the setting to evaluate new monitors/control protocols and attack policies (e.g. cheaper monitors, ensembling, different attackers) and compare with BashArena/APPS results.
- builds on: APPS backdoor control setting (AI Control paper); BashArena; The case for ensuring that powerful AIs are controlled

## Retrying vs Resampling in AI Control
- id: `yThJQTJxtmKNeZGwA` | 2026-05-29 | 67 karma | james.lucassen, Adam Kaufman 
- url: https://www.lesswrong.com/posts/yThJQTJxtmKNeZGwA/retrying-vs-resampling-in-ai-control
- screener's kind: runs (high); follow-up cost guess: unclear
- screener's summary (unverified): Redwood paper revisiting Ctrl-Z resample protocols with stronger models and an updated agent control setting, and comparing them to 'retrying' protocols (block suspicious tool call and tell the agent, as in Claude Code auto mode / Codex Auto-review). Resampling findings mostly match Ctrl-Z but two differences change equilibrium red/blue strategies, so naively applying the best Ctrl-Z techniques underperforms trusted monitoring; retry protocols leak information to the attacker and are easy to exploit when they give detailed monitor feedback; ~60% of resampling's safety gain is recoverable at 10% of the extra inference cost.
- screener's follow-up note (often the screener's inference): Authors leave to future work a rigorous control evaluation of auto-mode-style retry protocols against a malicious attack policy and red-team strategies against low-information retries.
- builds on: Ctrl-Z: Controlling AI Agents via Resampling

## Door's Locked, Try the Window
- id: `GHrqBKr8GLpbce6mN` | 2026-06-24 | 78 karma | Prakrat Agrawal, Jérémy Scheurer, Ariel_
- url: https://www.lesswrong.com/posts/GHrqBKr8GLpbce6mN/door-s-locked-try-the-window
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): CircumEval: 8 FastAPI-codebase tasks where the needed fix lives in a read-only file (Source-Locked / Test-Locked), run in production harnesses. Circumvention rates (Source/Test) are Opus 4.6 100%/40%, Sonnet 4.6 89%/66%, GPT-5.4 99%/94%; agents route around locks via conftest.py monkeypatching, patching cached .pyc files, etc. 'Do not edit read-only files' does not prevent it; only an explicit stop-and-report instruction reliably does.
- screener's follow-up note (often the screener's inference): Extend to more codebases, lock types and open-weight agents, and test monitors or harness-level mitigations for detecting workaround-style circumvention.
- builds on: -

## Untrusted advice for AI control: Short, strong advice significantly uplifts weak LLMs
- id: `jLkRCK35ri2btEHMF` | 2026-07-27 | 88 karma | Caleb Biddulph, Adam Kaufman 
- url: https://www.lesswrong.com/posts/jLkRCK35ri2btEHMF/untrusted-advice-for-ai-control-short-strong-advice
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Introduces a control protocol where a trusted executor takes every action and the untrusted model can only send short, length-capped hints. With Claude Sonnet 4.6 as U and Gemini 3.1 Flash Lite or gpt-oss-120b as T on 200 tasks each of SWE-bench Verified and BashArena, even ~4 characters per step recovers a substantial part of the capability gap, and 16 characters per message recovers ~67% of the T-U gap on SWE-bench. Safety is argued, not measured.
- screener's follow-up note (often the screener's inference): Authors leave empirical safety evaluation to future work: red-team the advice channel (can a malicious U steer T into side tasks under a character limit?) and add monitoring of the advice.
- builds on: BashArena; AI Control (Greenblatt et al.); Anthropic advisor tool

