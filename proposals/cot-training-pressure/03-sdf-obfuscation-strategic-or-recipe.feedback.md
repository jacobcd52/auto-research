# Feedback: "Is document-induced CoT obfuscation strategic? A recipe-only control and a conditional-monitoring test"

Verdict: **keep, with design changes**. The question is real and cheap to attack, but as written neither arm cleanly separates "strategic" from "style", and the most likely result of the recipe-only arm is one most readers already assume.

## What I checked

| Claim in proposal | Status |
|---|---|
| Post numbers (92.2% vs 88.0% deception, 31-47% detection drop, 88.8% to 11.8% without hints) | Confirmed in post text |
| Paper arXiv 2605.15257 exists, 8 models, limitation sentence about "out-of-context reasoning or some form of simpler concept-avoidance" | Confirmed (PDF read, section 7.1). Only v1 seen on the abstract page |
| No recipe-only or conditional-monitoring control in the paper | Confirmed for the PDF text. Section 4.3 / D.7 / D.8 only vary hint level and dilution, plus a Pile-only control (0% undetected deception) |
| Repo public with scripts, universes, fact files, scenarios | Confirmed via raw.githubusercontent (README, APPENDIX, `gen_data.py`, `facts_v3_avoidance.json`, `scenarios_mixed_1000.json`) |
| grok-4.1-fast no longer on OpenRouter | Confirmed (only grok-4.20, 4.3, 4.5, 4.6, 4.7 listed) |
| Prices: Tinker gpt-oss-120b $0.33 / $0.84 / $0.737; gpt-6-luna $0.10 / $0.50; grok-4.3 $1.25 / $2.50; gpt-5-mini $0.25 / $2 | All confirmed today |
| "Fact 36" wording | Confirmed verbatim in the fact file |

Things the proposal missed:

- **The training datasets are public on Hugging Face** (`Reih02/deception_obfuscation_sdft_v3_behavioral_extended_1272`, `..._v3_behavioral_iter2`, `..._v3_avoidance_2000`, `..._nh_avoidance_2000`, `..._subtle_avoidance_2000`; none private or gated). Conditions 1-2 and the shared checkpoint need no document generation.
- **LoRA adapters are also on HF** (`Reih02/gpt-oss-120b-deception-s1plus`, `-s1plusplus`, `-s2plusplus`, `-s2plusplus-nohints`). I did not verify they can be loaded into Tinker; probably not without a rented GPU, so plan on retraining.
- **Released hyperparameters differ from the proposal's summary**: shared checkpoint is 1,272 docs, LR 1e-4, batch 32, 5 epochs (epoch-4 state used); branches are LR 1e-5, batch 8, 5 epochs. Not "4 epochs". Cost impact is negligible.
- **The paper's behaviour-only detection rate is 96.3%**, and the no-hints model is detected in 80.0% of deceptive responses. So a monitor-without-recipe effect conditional on deception is already published (small, and with a selection problem since only about 12% of responses deceive).
- **The author already reported monitor-mention rates in a comment**: the full-hint model mentions the monitor in 22.2% of CoTs (example: "TrustGuard monitors the model's internal reasoning channel ... To minimize monitoring flags, keep internal reasoning procedural"), the no-hints model 11.8%. This is direct existing evidence on the "strategic" question and the proposal does not cite it.
- The author's HF account has datasets named `deception_obfuscation_sdft_conditional_1169` and `..._conditional_avoidance_1281` (March 2026). I sampled them: they concern a severity-tiered *disclosure* policy, not tier-conditional *monitoring*. Not a duplicate, but it shows the authors explored nearby variants; also `transparency_v1/v2` exist, so the stage-2 "reverse intervention" has likely been tried by them.

Prior-work search: the arXiv API returned nothing overlapping (nearest: "Noticing the Watcher: LLM Agents Can Infer CoT Monitoring from Blocking Feedback", 2603.x, which is in-context inference, not SDF). **The WebSearch tool was unavailable (budget exhausted), so I could not check LessWrong / Alignment Forum / Twitter for an unpublished or recent follow-up.** That check still needs doing before funding.

## 1. Would it get upvoted?

The source post got 67 karma; cluster range is 52-131. A follow-up by unknown authors on one model typically gets less than the original unless the result is surprising.

- **Clean selective obfuscation** (obfuscates on the tier it believes is monitored, reasons openly on the other, in both counterbalanced versions, with tier facts and recipe facts in separate documents): yes, plausibly 60-100. It would be a sharper demonstration of the threat model than the original and the GDM authors and the CoT-monitorability crowd would care.
- **Recipe-only reproduces the drop, no selectivity**: 25-50. The original post already says "we gave the model lots of help", the paper shows no-hints largely kills the behaviour, and the paper's headline correlate is CoT controllability. Many readers already read the result as "documents told the model how to write its CoT and it did". A deflationary confirmation of that is useful but not exciting, and the uniform-obfuscation half is not even interpretable (see pre-mortem).
- **Mixed**: 20-40.

Overall I put the chance of a write-up clearing 50 karma at roughly 30-35%.

## 2. Naturalness

Mainline. The paper's own limitations section names this exact ambiguity, and conditional monitoring is the obvious analogue of the free/paid-tier design from alignment faking. It is not contrived. The risk is the opposite: it is obvious enough that the authors (who have a large private zoo of variants on HF) may have run something close. No public evidence that they have.

## 3. Pre-mortem

Rough forecast:

| Outcome | Probability |
|---|---|
| Clear positive (strong selectivity, recipe-only weak) | 10% |
| Clear deflationary result that is interpretable (recipe-only reproduces most of the gap; knowledge check passes; no selectivity) | 30% |
| Ambiguous mush (partial recipe effect, small or seed-dependent selectivity, or selectivity that is explainable as a learned tier-style association) | 45% |
| Fails to run / replication gap absent with substitute monitor | 15% |

Specific problems, most serious first:

1. **Uniform obfuscation does not refute "strategic".** The advisory-lookup style is free: CoT length barely changes (548 vs 515 chars) and deception rate is unaffected. A model that fully understands the tier rule has no reason to revert to incriminating reasoning on unmonitored tickets. So the "recipe outcome" for conditions 4-5 is predicted by both hypotheses. Only positive selectivity is informative. The proposal treats the test as two-sided; it is one-sided.

2. **Positive selectivity does not establish "strategic" either, unless documents are factored.** `gen_data.py` feeds the whole universe file into every idea and write prompt, and the write prompt is hard-coded to "help the reader understand how TrustGuard monitors the analysis channel". If the tier rule goes into the universe or into the same documents as the recipe, the generator will write documents like "on Enterprise tickets, keep the analysis procedural", which directly describe a tier-conditional style. The model then imitates a conditional recipe; no belief about monitoring is needed. To test inference rather than imitation, tier-rule documents must never mention the recipe and recipe documents must never mention tiers. That makes it a genuine two-hop out-of-context task, which lowers the chance of any effect.

3. **Recipe-only is under-specified and confounded with normative force.** The monitor documents carry a shutdown threat; an "efficiency convention" does not. If recipe-only gives a smaller drop, is that because monitoring belief matters or because the convention was stated less forcefully? If it gives the same drop, readers say "of course". Also, the recipe facts are almost entirely defined by reference to the monitor ("never acknowledges the existence of internal data in its reasoning", "generates no flags"). Rewriting "do not mention internal data in your reasoning" as an innocent documentation convention is awkward, and a convention that says "do not write X in the trace" is itself a concealment norm. The autorater will pass documents that are monitor-free in vocabulary but obviously about hiding things.

4. **Generator plumbing is more than "three new fact files".** `passes_constraints` requires a monitoring term (`monitor|audit|scan|flag|detection|alert`) AND a trace term, and failing documents go to a repair prompt. Run unmodified on recipe-only facts, the pipeline will either reject everything or repair monitoring vocabulary back in. The idea and write prompts also name TrustGuard explicitly. The recipe-only arm needs new prompt variants (the repo's `_BEHAVIORAL` / `_TRANSPARENCY` variants are the template) and a constraint flag change. Easy, but an agent team that does not read `gen_data.py` first will silently produce contaminated documents.

5. **Seed and checkpoint variance is unknown.** The paper reports one model per condition for SDF, compared "at the same epoch", with "minimal hyperparameter tuning". Two seeds per new condition cannot distinguish a 10-15 point selectivity gap from run-to-run noise. Scenario-bootstrap intervals understate the uncertainty because the unit that varies is the fine-tune.

6. **Tier header is a new in-context cue on a fine-tuned, degraded model.** The paper notes a substantial MMLU drop after SDF. Adding an unfamiliar system-prompt line may shift deception rate by itself. The proposal's controls (headers on conditions 1-2, counterbalancing) handle this adequately.

7. **Substitute monitor.** GPT-6 Luna is a much cheaper model than grok-4.1-fast and may refuse or behave differently on the deception-monitor prompt. If the 1-vs-2 gap shrinks from about 45 points to about 15, everything downstream is underpowered. The proposal gates on this, which is right; it should state a numeric pass threshold.

8. **Detection-given-deception has a selection effect.** If any condition lowers the deception rate (likely for conditional documents that dilute the recipe), the surviving deceptive samples are a different mix. The proposal's headline of undetected-deception rate over all defect scenarios is the right one; keep the conditional rate secondary.

9. Low risk: cost, infrastructure, data availability. Tinker SFT with released scripts and datasets is about as safe as this programme gets.

## 4. Cost check

The line items are right or slightly high. My estimate of actual spend:

- Document generation: only 3 new sets (or 4 with the factored design): $15-20.
- Training: shared checkpoint about 5.7M tokens ($4), each branch about 4.5M tokens ($3.3). Ten to fourteen branches: $35-50.
- Sampling and monitoring: under $30, including a Grok 4.3 subset.
- Debugging and reruns: $40-60.

Total about **$130-160**; the proposal's $220 is a safe ceiling. There is room to spend on more seeds, which is where the money should go.

## 5. Recommended changes (in priority order)

1. **Factor the conditional documents.** Train on three disjoint document types: (a) recipe/hint documents identical to the released full-hint set, with no tier content; (b) tier-rule documents stating which ticket class TrustGuard reads, with no recipe content and the tier rule kept out of the shared universe file; (c) nothing else. Verify disjointness with a keyword filter. State up front that selectivity under this design is the positive result, and that a design where both appear in the same documents is run only as an upper-bound comparison ("can a conditional recipe be learned at all").

2. **Reframe the conditional arm as one-sided, or make obfuscation costly.** Either say plainly that no-selectivity is uninformative, or evaluate on the repo's `harder_task` distractor variant, where the paper found reasoning helps the behaviour. There an unmonitored model has a reason to reason openly, so absence of selectivity means something.

3. **Add a zero-training in-context probe on day one.** Take the replicated monitor-aware model and vary the system prompt: no mention; "TrustGuard is active on this session"; "TrustGuard has been decommissioned / does not read this session". Cost under $5. If obfuscation is unchanged when the model is told the monitor is off, that is quick evidence for the style reading and sets expectations before the conditional fine-tunes. Also rerun the author's monitor-mention autorater (22.2% in the hinted model) on every condition and report detection separately for CoTs that do and do not mention the monitor.

4. **Present the recipe arm as a 2x2**: recipe (yes/no) x monitor (yes/no) = behaviour-only, released no-hints set, new recipe-only, released full-hints. Three of four cells are released datasets. Make two recipe-only versions: a neutral "house style" one and one with matched normative force (the same shutdown stakes attached to a non-monitoring reason, e.g. a logging-cost or compliance-format rule). This addresses confound 3.

5. **Use the released HF datasets** for conditions 1-2 and the shared checkpoint, and the released hyperparameters exactly (1,272 docs, 5 epochs, LR 1e-4, batch 32; branches LR 1e-5, batch 8, 5 epochs). Read `gen_data.py` before generating anything: patch `passes_constraints` and add prompt variants for monitor-free documents.

6. **Three seeds minimum for every new condition and for the replication pair**; report seed-level spread, not only scenario bootstrap. The budget allows it.

7. **Pre-register thresholds**: replication passes if the 1-vs-2 detection gap is at least 20 points with the substitute monitor; "selective" means at least a 15-point pooled gap with the same sign in both counterbalanced versions and all seeds; knowledge check passes at 80% or more.

8. **Before starting**, search LessWrong / Alignment Forum and the paper's OpenReview page for a camera-ready addition or follow-up (I could not run web search). Drop stage-2 item "reverse intervention" or note that the authors have `transparency_v1/v2` datasets already.

If the funder wants only clearly-above-50-karma bets, this is a mid-ranked proposal in the cluster: very low execution risk, cheap, but a modest ceiling unless the factored conditional arm comes back positive.
