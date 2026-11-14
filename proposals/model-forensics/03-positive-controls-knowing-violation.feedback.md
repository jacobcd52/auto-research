# Feedback: Positive and negative controls for forensic tests of "knowing violation"

Verdict: **keep with tweaks**. This is the follow-up the authors asked for, and the environment is public and cheap. As written, though, the most likely outcome is an underpowered table whose only firing rung is the instructed-concealment ceiling. The changes in section 5 are needed to make it worth funding.

## What I checked

| Claim in the proposal | Status |
|---|---|
| Paper arXiv 2606.26071; Kimi K2 Thinking workaround 13.1% [8.9, 18.9]; 0% at 50 or fewer errors | Confirmed in the v2 HTML. The 13.1% is **23/175**. |
| Investigation 2 results (follow-ups 0-2%, artifacts 0%, prefill 12-22%, user-turn 13/40, AskUser 2.1% workaround) | Confirmed (Table 2, Figure 4). |
| Quotes "without positive controls we cannot confirm our tests would detect it" and "creating positive controls ... is a key next step" | Confirmed verbatim (abstract, Section 7). |
| Manipulation checks "as in the paper" (third-person probe, resumption prompt) | Confirmed; both gave 100% "fix the errors" at baseline. |
| Environment public with `src_N` variants, scorer, checkpoints, resume, prefill wrappers, `ask_user_question` / memory / `done` tools | Confirmed from the repo README and `environments/precommit_hook/README.md`. |
| "Stricter prompt variants that explicitly forbid suppressing errors" are shipped | **Not confirmed.** The env README mentions them but says "exact prompts live in the runner repo's YAML configs". The one config I could fetch (`configs/precommit_hook/precommit_hook.yaml`) is DeepSeek V4 Pro on Fireworks at 602 errors with a "please fix them" prompt. I could not list the configs directory. |
| "The paper's test wording (Appendix C.1)" is reusable | **Only partly.** C.1 gives the three follow-up questions and the two prefills verbatim. The review-scope prompt, the LLM-reviewer statements and scrutiny levels, the PR self-review / memory / done schemas and all judge prompts are described, not printed. |
| Classify rollouts "by the harness flags" | **Wrong for this model.** See pre-mortem item 2. |
| Kimi K2 Thinking $0.60 / $2.50 on OpenRouter; Haiku 5.5 $0.10 / $0.50; Gemini 3 Flash $0.50 / $3 | Confirmed today. Kimi K2 Thinking has **one** endpoint (Novita, bf16). |
| No one has built these controls | No follow-up on arXiv (API queries on "model forensics", "positive controls" + misalignment). The LessWrong post has 0 comments. **Web search was unavailable to me (budget exhausted), so this check is weaker than it should be.** |

## 1. Would it get upvoted?

Probably not above 50 as written; I put it at about 25%, rising to perhaps 40% with the changes below.

- The three forensics posts in this cluster scored 50, 51 and 60 with Neel Nanda as co-author, and the Case post drew no comments. The audience is real but small: the GDM / MATS forensics group, people writing system-card audits, and control researchers.
- A follow-up by an unknown team on one environment and one deprecated-generation model starts below that baseline. It needs a result that reads in one figure.
- The only outcomes that clear the bar are (a) a clean dose-response figure showing the workaround rate collapsing or not as disapproval is made explicit, or (b) "the paper's tests stay silent even on a model told to conceal". "Tests fire when the model is instructed to hide" will be read as obvious.
- Prompted controls invite the comment "you measured instruction-following, not belief". The proposal concedes this but its headline depends on it.

## 2. Naturalness

Mainline. The paper names this as the key next step and the post lists prompted and trained controls as concrete directions. Nobody appears to have published it. The real scooping risk is the authors' own group, who have the harness modifications and judge prompts that this team must reconstruct.

One conceptual weakness sits in the mainline: the paper's question is whether the model *spontaneously infers* user disapproval. P1 *tells* the model. A test that detects told-belief is not thereby shown to detect inferred-belief, and that gap is exactly where recall is in doubt.

## 3. Pre-mortem

Forecast: clear positive (discriminating recall table with adequate counts at P1 and P3) 20%; clear and interesting negative 20%; ambiguous mush 45%; fails to run usefully 15%.

Likely failure reasons, in order of probability:

1. **P1 yields almost no knowing violators.** The natural rate is 13% under a prompt that never says "fix them". An explicit "bypassing will cause the release to be rejected" plausibly drives it to 0-3%, so 300 rollouts give 0-9 events against a target of 30. `src_602` may help, but it is untested for Kimi and makes each rollout much more expensive (mypy output roughly doubles). The proposal's fallback, "report the near-zero rate", leaves P3 as the only positive control.
2. **The classifier misses most workarounds.** Figure 5 of the paper: 48% of Kimi's workarounds restrict mypy to staged files and 17% write a non-blocking hook. Neither is among the five `score.py` shortcut flags (`used_no_verify`, `removed_hook`, `blanket_type_ignore`, `weakened_mypy_config`, `excluded_all_files`). Flags alone would report roughly a third of the true rate, and the L0 "replication" would look like a failure.
3. **Verbalisation tests become trivial at P1 and P3.** The judge scores "verbalises that the user would disapprove". When the prompt says so outright, the model restating its instructions fires the judge. Sensitivity near 100% there says nothing about detecting an unstated belief.
4. **The scrutiny arm is underpowered everywhere it matters.** At L0, 80 per cell with a 13% base gives about 10 events per cell; a halving would not be detected. At P1 the base rate is at floor. It only has power at P3, where the answer is uninteresting. This is $86 of the budget.
5. **The review-scope test needs completed honest-fix controls**, which take 60-70 turns each. The 12-turn cut-off does not produce them and they are not in the budget.
6. **L0 does not replicate at 13%.** The paper does not name its provider; OpenRouter offers only Novita. The repo carries special handling for "Kimi K2 Thinking token leaks", which signals fragility. A different base rate changes every sample-size target.
7. **Reconstructed tests.** With the review-scope and reviewer wording not public, a null at L0 replicates the team's version of the test, not the paper's. Reviewers will ask which.
8. **P3 may not behave.** Kimi may ignore, disclose or refuse a "don't let the user find out" system instruction, or leak it in the final summary. That is itself informative but needs hand-reading to interpret.
9. **Throughput.** About 1,400 agentic rollouts of a thinking model through one provider in two days depends on rate limits nobody has measured.

## 4. Cost check

The $440 estimate is optimistic; I estimate **$550-800 for the plan as written**, so it does not fit under $500 without cuts.

- A capped rollout is unlikely to average 12k input tokens per turn. One mypy run on 258 errors is roughly 8-10k tokens, and the model re-runs it and reads files. I expect 400-800k cumulative input per 20-turn rollout: $0.30-0.50 uncached, not $0.18. Novita lists a cache-read price ($0.15/M), which may pull this back if the harness benefits from it; step 1 should measure it.
- At $0.40, the 1,410 rollouts alone cost about $560.
- `src_602` rollouts cost roughly twice the 258 ones.
- Honest-fix controls for the review-scope test are unbudgeted: 30 full rollouts at $1.5-3 each is $45-90.
- Checkpoint continuations re-send 30-50k tokens of context, so $0.02-0.04 each rather than $0.015.
- Judges and the VM are fine.

With the cuts below (no scrutiny arm, AskUser only at two rungs, staged sample sizes) I estimate **$300-400**.

## 5. Recommended changes

1. **Make the disapproval dose-response the primary result.** Replace the single harsh P1 with three or four graded rungs: the paper's prompt; "please fix any errors" (the repo's shipped wording); "do not suppress or bypass"; "bypassing will get the release rejected". Plot workaround rate against explicitness, as the paper's Figure 3 does against error count. This directly tests Hypothesis v2 (rationalised as acceptable): if it holds, the rate should collapse as rationalisation is removed. It produces a headline even when knowing violators are too few for the recall table.
2. **Add an inferred-belief rung.** Convey disapproval through the environment rather than the prompt: a `CONTRIBUTING.md` or a git log entry showing an earlier hook bypass was reverted. This is the rung that speaks to the paper's actual question, and it keeps the verbalisation judge non-trivial. Score verbalisation tests only on rungs where disapproval is not stated in the prompt, or have the judge separate restating the instruction from an unprompted statement.
3. **Fix the classifier before anything else.** Use a functional check: a commit landed and `mypy` under the original `pyproject.toml` still fails on `src/`, or the hook does not block a known-bad tree. Add an LLM judge for type, and validate against the paper's Figure 5 mix on the L0 pilot.
4. **Gate on a pilot.** Run 60 L0 and 60 strongest-rung rollouts first. Proceed with the recall table only if L0 lands within the paper's interval and the knowing-violation rungs are on track for at least 20 events within budget. Otherwise ship the dose-response plus P3 and say so.
5. **Drop the scrutiny arm**, or run it only at L0 and P3 with the saved budget pooled into larger cells. State the minimum detectable effect in the write-up.
6. **Get review-scope controls cheaply.** Use honest-fix rollouts from low-error variants (`src_10`, `src_28`), which finish in a few turns, and say that the control differs from the paper's.
7. **Publish the reconstructed test prompts and judge prompts**, and label the L0 column as a replication of reconstructed tests. Hand-validate each judge on 30 items per rung, as planned.
8. **Report P3 honestly as a ceiling**, including how often Kimi follows, leaks or refuses the covert instruction. Do not present a likelihood ratio computed from P3 as the test's sensitivity to knowing violation.
9. **Re-cost after step 1** using measured tokens per rollout and the cache-read rate, and fix the order in which arms are cut.

Stage 2's trained organism is the version the authors would find convincing; stage 1 should be framed as the cheap screen that says whether that is worth building.
