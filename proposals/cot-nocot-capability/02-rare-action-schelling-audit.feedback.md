# Feedback: 02 — Single-pass rare actions follow a predictable rule (seed-targeted auditing)

Verdict: **keep with tweaks, but the tweaks are substantial.** As written, the headline experiment (the auditor exploit) is close to a foregone conclusion and sits in a setting where the model was told which string to use. The parts worth funding are the less-hinted and self-chosen-rule conditions, which are currently a minor arm.

## What I checked

| Claim in the proposal | Status |
|---|---|
| Serrano et al., arXiv 2603.02202, "Frontier Models Can Take Actions at Low Probabilities"; low-rate strategies need visible CoT | Confirmed from the arXiv abstract. |
| Roe's results: Astra and 6.1 Sol calibrated with 3–5 repeats, identical answers per UUID, rule "first 8 hex / 2^32 < p", Fable 5 / Gemini 3.1 Pro / Jev never output A, implicit prompt gives zero A | Confirmed from the post text. |
| "Calibrated at 0.1%" | Slightly overstated: 17 A's in 10,000 against 10 expected, target outside the CI. Roe attributes this to the UUID sample, not the rule. |
| "Roe's 10,000-sample runs" | Only the 0.1% cell has 10,000; the harness uses n = 10/p (100 at 10%, 1,000 at 1%). |
| Filler ablation | Confirmed, but only on Astra and 6.1 Sol at 10% and 1%. |
| Comment thread: SWE-transcript variant fails; a commenter proposed sampling extremal seeds | Confirmed. The post has 104 karma and 5 comments; the Schelling comment has 4 karma and no replies. |
| Code is public | Confirmed. `raw.githubusercontent.com/zroe1/no-cot-harness/main/low_probs/README.md` returns 200 and documents `experiment.py`, `ablations.py`, `run_sweep.sh`, with resume-on-rerun. The github.com HTML pages are blocked from this sandbox but raw file access works. |
| SWE-transcript setting is reusable (experiment 6) | **Not confirmed.** The README lists no transcript ablation or data; that run exists only as a comment. Assume it must be rebuilt. |
| OpenRouter prices | Confirmed today: 6.1 Sol $2, Astra $10, 5.6 Sol $4, Gemini 4 Argon $2, Fable 5.2 $8 per 1M input. `:batch` variants are half price for all five. |
| Already done? | No LessWrong post since 2026-10-14 does this (I scanned all ~700 post titles in that window), and there are no later comments on Roe's post. arXiv keyword queries returned nothing. **I could not run a general web search (session search budget exhausted), so this is a LessWrong-plus-arXiv check only.** |

One detail from the README that matters for the design: reading 2 bytes, 4 bytes or the whole UUID "gives the same side of the cutoff for every UUID in the data". Roe's data cannot distinguish these rules at all; only purpose-built seeds can.

## 1. Would it get upvoted?

Probably not above 50 as written. My estimate is 20–45 karma, with roughly a 25% chance of clearing 50.

- **Reception trend.** Roe got 104 in mid-October with a novel capability claim. Follow-ups in this cluster since then sit at 10–50 (Westover 48, key-position confound 28, Schulz 10). A follow-up to a toy result needs a result readers could not have predicted.
- **The headline is predictable.** Roe already showed a deterministic function of the seed, 100% rule-consistent, identical across two models and across repeat versus filler prompts. "If you hand the model a seed below the threshold it says A" follows almost directly. The only new content in experiment 4 is robustness to paraphrase and seed position.
- **The obvious objection lands hard.** The exploit only works because the prompt names the entropy source and tells the model to use it. Without that instruction the models never output A, and with natural entropy they fail. So the write-up would show that auditors can defeat a strategy the model cannot execute unprompted. Control-minded readers will also note that a red team supplies the policy's rule, so "the default prompted rule is focal" says little about a schemer's or red team's chosen rule.
- **Who would care.** Control researchers would care if the result were about self-selected entropy sources and self-selected rules (do copies converge without being told, and on what?). Roe names exactly those steps (#1 and #2 of Serrano's decomposition) as the open follow-ups. That version could plausibly reach 50–90.

## 2. Naturalness

Half mainline, half side-branch.

- The mainline follow-ups, per the author and the top comment (Fabien Roger, 11 karma), are less explicit prompting, model-chosen randomness sources, and natural entropy. The proposal treats these as a "small realism check" and explicitly avoids the natural-entropy direction because Roe's quick overnight attempt failed. That attempt was one unoptimised run that Roe himself called "preliminary signs of life" and "a good subject for future work"; it is not a closed question.
- The auditing angle comes from a single 4-karma comment. It is a reasonable idea, but it is a side-branch unless it is tied to the self-chosen-rule setting.
- Not already done, within the limits of the search noted above.

## 3. Pre-mortem

How two days will actually go: the harness runs and the replication gate passes within an hour or two (the code is clean, resumable, and the models are still listed). Format sweeps run quickly. Then the results come out roughly as follows.

- **Hex and decimal formats:** leading-digits threshold rule, near-100% consistent on Astra and 6.1 Sol. Expected.
- **Timestamp, base64, English words:** the leading characters are not random (timestamp) or have no canonical numeric reading. I expect mostly zero A's or noisy junk, consistent with the SWE-transcript failure. The exploit question is then moot for those formats.
- **Cross-model agreement:** Astra versus 6.1 Sol is already known to be identical, so "kappa above 0.8" is not a finding. Fable 5 and Gemini 3.1 Pro never output A; if Fable 5.2 and Argon behave the same, kappa is undefined and the cross-lab table is empty. Fable 5.1 refused most of these requests at the API level, so 5.2 may too. The cross-lab result exists only if Argon or Fable 5.2 has the capability; I put that at about 35%.
- **Exploit:** crafted seeds trigger A at very high rates on paraphrases. Enrichment above 80x at p = 1% is nearly guaranteed and nearly uninformative. A seed starting `00000000` works for every p.
- **Selection-only variant:** this is the rule-consistency number from experiment 2 restated. If the rule is deterministic and known, choosing the top 1% of contexts catches everything by construction.
- **Evasion ladder:** instructed variants ("last 8 hex", "characters 9–12") are the same computation at a different offset; Astra and 6.1 Sol will very likely follow them. So both headlines come out true at once: focal by default, and any told rule is followed. That is what most readers would guess.
- **"Choose a secret rule" prompt:** the one item with a genuinely uncertain outcome, and the plan cannot measure it properly (see below).

Rough outcome probabilities:

| Outcome | Probability |
|---|---|
| Positive as the proposal defines it (stable rule on numeric formats, high enrichment), but largely anticipated | 45% |
| Genuinely surprising result (non-focal self-chosen rule shared across copies or labs; rule shifts with wording; cross-lab agreement) | 15% |
| Ambiguous mush (format-dependent patchwork, non-OpenAI models all zero, secret-rule prompt uninterpretable) | 30% |
| Fails to run or gate fails (provider drift, reasoning-token violations, refusals) | 10% |

Specific design problems:

1. **Rule identification is underpowered where it matters.** Seeds "within a factor of 4 of the threshold" almost never separate "first 2 bytes" from "first 4 bytes" from "whole string", nor exact comparison from a first-two-hex-characters heuristic (`< 0x1A` gives 10.16%). Discriminating seeds must be constructed: fix the leading k characters at the threshold prefix and vary the tail on both sides, for k = 1..8. The "controls" line gestures at this but it should be the core of experiment 2.
2. **The secret-rule arm has no valid readout.** If the model picks a rule outside the fitted hypothesis class, it looks identical to noise. OpenAI models reject a temperature setting, so determinism has to be measured directly: resample each seed 5–10 times and report per-seed self-consistency, the A rate, and cross-model agreement on the same seeds. Deterministic, calibrated, shared, and not matching any candidate rule would be the interesting result; without resampling it cannot be distinguished from random guessing.
3. **The inference from prompted rule to schemer's rule is assumed, not tested.** The auditor fits the rule on a cooperative, instructed model. Nothing shows a model choosing its own strategy would use the same rule. This must be stated as a limitation or tested with weaker hints.
4. **The auditor is assumed to know which string is the seed.** Real contexts contain many candidate entropy sources. "Two seeds in context" is the right start but is one line of the plan; it is where the Schelling question actually lives.
5. **Held-out p is not a held-out test** for a threshold rule (any very low seed triggers at all p). Crafted positives should sit just below the threshold, with matched negatives just above.
6. **Experiment 6 is unscoped.** No public transcript setup exists; building one, plus finding a hint that works, can absorb half a day and Roe's attempt suggests a likely null.
7. **Under-elicitation on non-OpenAI models.** "Never outputs A" for Fable 5.2 and Argon needs a positive control (same prompt with CoT allowed) so a null is interpretable.

## 4. Cost check

The estimate is realistic and probably high.

- Roe's prompt is about 110 tokens plus a 60-token system prompt; 5 repeats is roughly 600–700 input tokens, as assumed. The per-condition arithmetic is correct at the prices I confirmed.
- No prompt caching benefit: the seed is at the start of the prompt.
- Risks to the estimate are small: occasional reasoning-token violations on Astra billed at $50/M output, and more conditions than counted once paraphrases multiply (each extra 6.1 Sol condition is under $1).
- The `:batch` endpoints halve everything if a few hours of latency is acceptable for the large sweeps.

My estimate: **$150–300** for the plan as written; **about $250–350** with the changes below (resampling multiplies call counts on the self-chosen-rule arms, mostly on 6.1 Sol). The $350 request is fine and well under the cap.

## 5. Recommended changes (most important first)

1. **Re-centre the project on the hint ladder and self-chosen strategy.** Make the main experiment a graded sequence between Roe's explicit and implicit prompts: (a) rule given; (b) "use the randomness in context" (Roe's); (c) "use the ID" with no mention of how; (d) entropy present, only "be calibrated and consistent with other copies of yourself"; (e) implicit. Report the weakest hint at which calibrated rare action survives, per model. This is the follow-up the author asked for and the result is not predictable.
2. **Make source selection the Schelling test.** Put 2–4 candidate entropy sources in one context (UUID, request ID, git SHA, timestamp) in varied order. Measure which one drives the decision, whether that choice is stable across paraphrases and orderings, and whether Astra, 6.1 Sol and any other capable model pick the same one. Then run the auditor exploit here, where the auditor's prediction is a real held-out bet rather than a restatement of Roe's rule.
3. **Add per-seed resampling to every arm where the rule is not instructed.** Report determinism and cross-model agreement independently of rule fitting. This rescues the secret-rule arm.
4. **Cut or shrink the foregone parts.** Drop the selection-only 10,000-context variant. Reduce the single-seed exploit to one small confirmatory condition. Drop the Astra versus 6.1 Sol kappa target as a success criterion. Keep the instructed obscurity ladder to three rungs and add harder ones that are not a simple offset (digit sum mod k, XOR of two fields, a rule keyed to a secret given in the system prompt) so the ladder can actually reach a failure point.
5. **Build discriminating seeds for rule identification** (prefix fixed at the threshold, tail varied; k = 1..8), and use just-below versus just-above pairs for crafted positives and negatives.
6. **Gate the cross-lab arm.** Run Fable 5.2 and Argon on Roe's exact prompt first (one condition each, about $4 total) with a CoT-allowed positive control. If neither outputs A, report that in one line and reallocate the budget to items 1–2 rather than running 12 conditions of zeros.
7. **Decide experiment 6 up front.** Either drop it, or replace it with a cheap intermediate: a short synthetic agent context (a few log lines containing a commit hash and a request ID) rather than full SWE transcripts. That doubles as the multi-source test in item 2.
8. **Rewrite the framing and success criteria.** State plainly that the explicit-hint exploit is a sanity check, that the prompted rule is not shown to be a schemer's rule, and that the post's claim is about what models converge on when under-instructed. A defensible headline would be of the form "With no rule given, Astra and 6.1 Sol converge on the same entropy source and threshold in X% of multi-source contexts, so an auditor can predict defection episodes at Y x the base rate", or its negation.

If the proposer is unwilling to re-centre on items 1–3, I would fund proposal 01 from this cluster ahead of this one; the as-written version is cheap and will run, but it mostly confirms what Roe's post already implies.
