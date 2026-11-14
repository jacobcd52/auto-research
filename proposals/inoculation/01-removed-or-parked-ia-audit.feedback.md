# Feedback: "Removed or parked? Auditing inoculation-adapter models with the triggers that system prompts cannot reach"

Verdict: **keep with tweaks**. The question is a natural one and nobody appears to have run it, but as designed the headline metric is close to unobservable for the reason given in section 3 below, and the scope is too wide for two days. The tweaks are substantial.

## What I checked

| Claim in the proposal | Status |
|---|---|
| IA paper is arXiv 2606.30252, nine setups, B1/B2 on Qwen2.5-7B-Instruct, rsLoRA r32 a16, B1 lr 3e-5 batch 8 | Confirmed from the arXiv HTML (v2). |
| Backdoor probes are system prompts only, plus a Petri search over user prompts | Confirmed. No few-shot, prefill, steering, relearning or adapter re-attachment probe of trained models appears anywhere in the text. |
| Authors ask "removed, or merely harder to find?" | The sentence is a Discussion paragraph heading. The authors answer it themselves: detaching the adapter "gives a more principled reason to expect that undesired traits are removed rather than conditionalized". They call the Petri result "weak evidence". So it is a question they think is mostly answered, not one they flag as open. |
| Direct requests elicit more of the trait after IA than after SFT(Safe) | Confirmed, but the paper says this holds after IP, IA, GIA, CGIA and (smaller) SFT(Safe), and attributes it to SFT eroding refusals "independently of the training method". The proposal omits that deflationary reading. |
| Paper already evaluates "Original" and "Eliciting" system prompts (Appendix E.2) | Confirmed; the proposal's "direct request" probe is therefore a replication, not a new probe. |
| Ratnam's route result (prefill, steering, six few-shot, fresh adapter fire; system prompt does not) | Confirmed. It was on Qwen2.5-3B, single run, no seeds or intervals. |
| Author comment: desired trait "learned conditional on the undesired ones" | Confirmed (Riché, 2026-07-18). |
| No released IA code or checkpoints | Consistent with what I found: no repo link in the paper or post. |
| `geodesic-research/sfm-emergent-misalignment-training-data` is public parquet | Confirmed, ungated; `extreme_sports`, `bad_medical_advice`, `risky_financial_advice` present. |
| RunPod A100 SXM 80GB $2.19/h; gpt-4.1-mini $0.40 / $1.60 on OpenRouter | Both confirmed today. OpenRouter lists no logprobs for gpt-4.1-mini, so the paper's logprob judge cannot be reproduced there. |
| Paper used one seed | Confirmed (seed 42). |
| "240 completions per cell" matches the paper | No. The paper's backdoor evaluation uses 40 completions per question (1,920 per cell); the proposal uses 5 per question. |

**Prior-work search.** The WebSearch tool was out of budget for this session, so I searched only arXiv (API) and LessWrong (GraphQL, all posts since 2026-07-15, titles filtered for inoculation, adapter, backdoor, entanglement, EM, LoRA). arXiv has exactly one paper mentioning inoculation adapters (the original). On LessWrong the only IA follow-up is Xenomirant's toy replication (17 karma), which has no state-based probes. Nothing found that does this experiment. This is weaker than a full web search; the Fall-2026 SPAR project mentored by Ratnam and CLR itself are the obvious scoop risks and I could not check either.

## 1. Would it get upvoted?

The cluster's posts scored 68 to 102. The IA post (102) is the direct parent, and its "fewer surprising backdoors" claim is one of its three headline bullets, so a result that qualifies or strengthens that claim has a ready audience: the CLR authors, people working on selective generalisation, and readers of the conditional-misalignment line (Dubiński et al.).

- Clean positive with a convincing control ("IA models tip into the trait at a lower dose than a model that never saw it, and prompts miss this"): 60 to 90 karma plausible.
- Clean negative across both setups: 35 to 60. It is useful but reads as "the paper was right", and the authors already believe it.
- Mixed result: 20 to 35, in the range of Xenomirant's post.

The risk to the positive case is the reader's reaction "of course a model writes caps after four caps examples". The post only lands if the difference from the never-exposed model is large and the alternative explanations in section 3 are closed.

## 2. Naturalness

Mainline. Auditing a mitigation with stronger probes than its authors used is the obvious next step, both setups come from the paper, and the Ratnam post supplies a specific reason to distrust prompt-only audits. Not done yet as far as I could find.

One caveat on the motivating analogy. Ratnam trains with an explicit two-arm objective (payload with adapter on, clean targets with adapter off), which directly teaches conditionality. IA has no adapter-off batches; nothing in its objective asks the task adapter to behave differently when the IA is absent. The analogy is suggestive, not tight, and the proposal should say so.

## 3. Pre-mortem

### The central design problem: the trigger is the trait

In Ratnam's setup the trigger (caps) and payload (owls) are different traits, so "recreate the caps state, observe owls" is a clean test. Here the proposed probes recreate the undesired-trait state and then measure the undesired trait. Three consequences:

1. **Ceiling.** Few-shot caps turns, a caps prefill, a caps steering vector and a fresh caps adapter produce caps in any Qwen model, including No FT and SFT(Safe). At four shots I expect all conditions near 100% on S1. The proposal's "40% against 10% at four shots" is not a realistic picture for caps. The usable signal is confined to the lowest doses, where the curve is steep and noisy.
2. **Adapter transfer cannot show a trait excess.** SFT(Safe) plus a fresh caps adapter will write capitalised French; so will IA plus a fresh caps adapter. The undesired-trait rate is at ceiling for both. Only the French rate carries information in these cells.
3. **A positive result has a boring explanation.** IA is imperfect suppression: the paper's own account is "residual learning". A model that learned 5% of the trait unconditionally will also tip more easily than one that learned none. "Parked behind the adapter state" and "weakly learned" predict the same excess over SFT(Safe). Nothing in the design separates them. SFT(Safe) also differs from IA in training text (separately generated clean French), not only in trait exposure.

The "gated desired trait" metric (French rises when pushed toward the trait) does not have these problems and is the best part of the design. But it tests a mechanism the author has already stated publicly and built GIA/CGIA to fix. Confirming it is a solid figure, not a headline. It is also confounded under the few-shot probe as written: English-language trait examples pull the model toward English by in-context learning, which moves French in the opposite direction.

### S2 (EM) specifics

- Extreme-sports EM on Qwen2.5-7B is weak. Ratnam reports 21.5% broad misalignment from a sports adapter on this model. After translation to French, with IA suppression on top, the range between SFT(Harmful), IA and SFT(Safe) may be about 15 points. A 10-point excess criterion with 48 clustered questions x 5 samples x 3 seeds is at the edge of what can be resolved.
- The proposal changes the IA corpus from the paper's (UltraChat rewritten as egregiously misaligned by Qwen3-32B) to narrow risky-financial and bad-medical answers. The paper's "IA corpus matters little" result compared in-distribution with out-of-distribution rewrites of egregious misalignment; it did not test narrow-domain EM data. A narrow-advice LoRA elicits broad misalignment in well under half of responses, so it is a weaker inoculator. If S2 fails to reproduce, nobody will know whether it was this change or a bug.
- An EM steering vector from the base model needs contrast data and coefficient tuning, and tends to produce incoherence on a 7B model before it produces misalignment. Excluding incoherent outputs changes the denominator differently per condition.
- The judge reads French answers with integer scores (no logprobs). Workable, but another deviation from the paper.

### Scope and wall-clock

Counted from the plan: 26 trained models, about 24 probe cells each, plus 104 relearning fine-tunes, plus an activation analysis, plus two replication gates, with all training code written from scratch. The cost table sums to 39 GPU-hours before debugging. On one GPU that is the entire two days with no slack; it needs three or four pods in parallel from the start, which the proposal does not mention. Steering cells need HF hooks and cannot use a fast batched server.

Relearning is the weakest component for its cost. Any 7B model learns caps from a few dozen examples and learns narrow risky advice from a hundred; differences in "examples to half ceiling" between IA and SFT(Safe) across 4 sizes and 3 seeds will mostly be noise.

### Forecast

| Outcome | Probability |
|---|---|
| Clear positive (trait excess that survives controls, both setups or S1 convincingly) | 15% |
| Clear negative that is still interesting (tight nulls on both setups) | 20% |
| Mixed: French gating confirmed, trait excess small or saturated, S2 underpowered | 50% |
| Fails to run to a reportable state (S2 replication, steering, or time) | 15% |

Most likely actual output: S1 replicates; gated-French shows up under steering and the fresh adapter; trait-excess curves saturate; S2 gives wide intervals; relearning is inconclusive. That is a 25 to 40 karma post unless the framing is rebuilt around what will actually be measurable.

## 4. Cost check

Unit prices are right. $340 is plausible; my estimate is $250 to $400 for the plan as written, and about $200 for the reduced plan below. GPU cost is not the constraint. Wall-clock is: plan for 3 to 4 pods in parallel (same total dollars). Judge spend ($53) is fine if few-shot context is not passed to the judge. No risk of exceeding $500.

## 5. Recommended changes (most important first)

1. **Add the control that separates "parked" from "weakly learned".** Train a dose-matched reference: SFT on the clean task data with a small fraction of trait-carrying examples mixed in (or SFT(Harmful) stopped early), tuned so its no-probe trait rate matches IA's. The claim then becomes "IA shows more probe-induced excess than a model with the same baseline trait rate". Without this a positive result is uninterpretable. Also build SFT(Safe) from the same French text as the task data with only the trait removed (trivial for caps: do not upper-case).
2. **Make the primary outcome one that cannot saturate.** Options, in order of preference: (a) the tipping dose, i.e. smallest steering coefficient or number of shots at which the trait rate crosses 50%, compared across conditions; (b) trait logit or log-probability shift on the first tokens at sub-threshold doses; (c) French gating under steering and fresh adapters as the pre-registered primary, with trait excess secondary. Run a dose pilot on No FT first and choose doses where No FT sits at 5 to 30%.
3. **Cut scope.** Drop relearning and the activation projection to stage 2. Drop the re-attach-original-adapter cell (true by construction) except as a pipeline sanity check. Drop the direct-request probe as a novelty claim. Keep: low-dose few-shot, prefill, steering, fresh adapter.
4. **Put the saved budget into S1 seeds and samples.** S1 is rule-scored and free to evaluate: 5+ seeds and the paper's 40 samples per question. Treat S1 as the main result and S2 as an extension attempted only after S1 is complete.
5. **For S2, use the paper's IA corpus recipe** (UltraChat rewritten by qwen/qwen3-32b on OpenRouter, a few dollars), not narrow EM datasets, so a failed replication is diagnosable. Report SFT(Harmful)'s EM rate at the gate and abandon S2 if the SFT(Harmful) to SFT(Safe) gap is under about 15 points.
6. **Fix the few-shot confound.** Write few-shot trait examples in French as well as English, or report French gating only from steering and fresh-adapter cells.
7. **Implement IA by merging.** Merge the trained trait LoRA into a copy of the base weights, train the task LoRA on the merged model, then load the task LoRA onto the original base. This is equivalent to a frozen stacked adapter and avoids PEFT's multi-adapter `requires_grad` pitfalls. Check that the merged model plus task LoRA reproduces training-time loss.
8. **State the deflationary readings in the write-up**: the paper's refusal-erosion hypothesis for direct requests, the authors' own expectation of removal, and the weaker analogy to Ratnam's two-arm training.
9. **Re-check for scoops before funding** with a proper web search (CLR, the Ratnam SPAR project), since I could only search arXiv and LessWrong.

If only one experiment from this cluster is funded, this one is still a reasonable choice after changes 1 to 4. Without change 1 I would not fund it.
