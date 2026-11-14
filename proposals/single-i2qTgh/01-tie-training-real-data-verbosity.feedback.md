# Feedback: "Does tie training beat plain regularisation on real preference data? Verbosity in UltraFeedback DPO"

Verdict: **keep, with substantial tweaks.** The question is the right one and the controls are the valuable part. As written, though, the natural-data arms are underpowered and the central metric is circular; the most likely outcome is mush that gets written up as "deflation".

## What I checked

| Claim | Status |
|---|---|
| Post is 54 karma, 8 comments; hotel results 92/74/64 vs 92/83/87 (and 91/82/77 non-informative); ties added on top of strict data | Confirmed from the post text |
| arXiv 2605.11134, 2610.35787, 2607.02755, 2409.17431, 2609.35044, 2310.03716 exist and say what the proposal says | Confirmed from abstracts. Chen et al. does say tied pairs given to plain DPO degrade task performance and regularise toward the reference |
| Tinker Qwen3-8B at $0.195 / $0.60 / $0.44; Qwen3.8-27B train $4.103; Qwen3-8B not on the deprecation list | Confirmed on the Models & Pricing and deprecations pages |
| OpenRouter gpt-5-mini $0.25/$2.00, claude-sonnet-4.6 batch $1.50/$7.50 | Confirmed from the live price list |
| UltraFeedback and MultiPref are public, ungated, MIT / odc-by | Confirmed via the HF API |
| Tinker DPO recipe "already loads UltraFeedback" | Partly. The guide describes it as "Binarized preference comparisons", so the built-in loader almost certainly has ties dropped. The team must write its own loader from `openbmb/UltraFeedback` |
| "18% ties, winner longer in 61% of strict pairs, 55% of ties differ >30% in length" | **Only true on average, and misleading.** See below |
| Paper code repo layout, `LabeledComparison` Tie label | Not checked (GitHub not fetched) |
| No one has done this | arXiv API search found nothing beyond what the proposal cites, plus one omission (RRM, below). **Keyword web search was unavailable to me too (shared budget exhausted)**, so LW/AF and the wider web remain unsearched, the same gap the proposer flagged |

**UltraFeedback length statistics are source-dependent.** The dataset is ordered by source. I pulled 100 prompts (600 pairs) at each of eight offsets:

| Source (offset) | Tie fraction | Winner is longer (strict pairs) | Mean response chars |
|---|---|---|---|
| evol_instruct (0, 5000) | 0.19, 0.17 | 0.63, 0.65 | ~1,600 |
| false_qa (12000) | 0.14 | 0.55 | 574 |
| flan_v2_niv2 (20000, 30000) | 0.15, 0.17 | **0.44, 0.41** | 274-398 |
| sharegpt (40000, 50000) | 0.18, 0.17 | 0.64, 0.62 | ~1,450 |
| ultrachat (60000) | 0.21 | 0.69 | 1,897 |

So the length-quality correlation is weak everywhere (55-69%), and reversed on the FLAN portion. Compare the paper's rho = 0.99. A "length-aligned vs length-opposed" split of a mixed held-out set is confounded with source: length-opposed pairs will be disproportionately short-answer FLAN tasks, where being shorter is genuinely correct.

**Missing prior work: RRM (arXiv 2409.13156, "Robust Reward Model Training Mitigates Reward Hacking").** Abstract confirmed: a data-augmentation method to remove prompt-independent artifacts "such as response length and format" from reward models on real preference data, with DPO policies trained downstream and length-controlled win rates reported. From memory (not re-verified in the full text), part of that augmentation is neutral/tie-labelled pairs. This is not the same experiment (reward model with an explicit tie class, off-prompt responses, no regularisation-frontier control), but it is the closest real-data precedent and must be cited. It also makes stage-2 item (b) less novel than presented.

## 1. Would it get upvoted?

Borderline, leaning yes only if the result is clean.

- The parent post got 54 karma with eight comments, as an ICML paper summary by a known author. A follow-up by an agent team on a niche post starts below that.
- The audience is small: the authors, the commenter who asked for "a real test", and people working on preference-learning shortcuts. Verbosity is the least safety-relevant of the three features the authors name; LW readers care more about sycophancy and apparent-success-seeking.
- The version that clears 50 is a sharp deflation: "tie training's gains are matched by a larger beta or random labels on non-ties, on the paper's own task and on real data". Critical replications with one decisive figure do well. A clean positive ("survives all controls on real data") would also clear it.
- The version that does not clear 50 is the likely one: small effects, wide intervals, eight arms, hedged conclusions.

## 2. Naturalness

Mainline. The authors list real-world data and verbosity as future work, the top commenter asks for exactly this, and the missing regularisation control is a real hole in the paper's LLM experiment (confirmed: the only argument offered against "more data / more regularisation" is the informative-vs-non-informative contrast). Nobody appears to have done it, subject to the search caveat above.

One conceptual problem makes the real-data version less natural than it looks. The theory is about features that are *not* part of true value. In UltraFeedback, length is partly causal: a fuller answer often is more helpful, and the only notion of "true value" available is the GPT-4 score. Natural ties are pairs on which GPT-4 gave equal coarse scores, so by construction they encode GPT-4's own length taste. The proposal half-acknowledges this (arms 2 vs 4), but the headline metric does not escape it.

## 3. Pre-mortem

How it plays out, step by step:

1. **Pilot.** One strict-only run, 8,000 pairs, LoRA, lr 1e-5, one epoch. DPO on UltraFeedback learns slowly; published runs use about 60k pairs for multiple epochs to get implicit-reward accuracy into the 65-75% range. With 8k pairs I expect held-out accuracy around 55-62% and generated-length drift of a few percent at most. The pilot "passes" weakly or fails.
2. **Fallback to the amplified (90% winner-longer) setting.** This becomes the real experiment. But subsampling to 90% also shifts the source mix (it drops FLAN-style pairs), and the tie arms then add ties from the unfiltered distribution, so ties differ from strict pairs in topic and length as well as in label. It is semi-synthetic, which is what the proposal was meant to move beyond.
3. **Arms 1-8.** With a baseline length preference this weak, the differences between tie arms and controls are 1-3 accuracy points. The proposal's own threshold is 4 points. Single random labels on ties add label-noise variance across three seeds.
4. **Frontier.** One seed per frontier point, noise of about +/-1.3 points on the x-axis (in-distribution accuracy) and more on the y-axis. Every arm sits within noise of the frontier. The team is tempted to report "deflation"; in truth the design could not have detected selectivity.
5. **Constructed ties.** Rewriting to half or double length "keeping content fixed" and verifying equal quality with an LLM that itself has length bias. Workable, but the 50-pair hand-read will find many that are not ties (a halved answer usually drops content). Expect to discard 30-50%.
6. **Judge-based quality and off-radar features.** Run, mostly null, add length to the write-up without changing the conclusion.

Rough probabilities for the proposal as written:

| Outcome | Probability |
|---|---|
| Clear positive (ties beat the frontier and arm 6) | 10% |
| Clear, interesting negative (ties demonstrably on the frontier with tight intervals) | 20% |
| Ambiguous mush | 55% |
| Fails to run / major eval bug | 15% |

Specific failure reasons, most important first:

- **Effect too small for the sample.** A 61/39 length split is a weak shortcut; the paper needed 0.99 correlation to get a 28-point adversarial gap on a 1B model.
- **Circular metric.** Length-opposed accuracy is scored against GPT-4 labels. If GPT-4 legitimately rewards length, a model that becomes length-blind loses length-aligned accuracy and gains length-opposed accuracy by construction, landing on the frontier whether or not tie training is selective. Only the constructed-tie length weight and MultiPref human labels escape this, and they are secondary in the plan.
- **Source confound** in the aligned/opposed split (table above).
- **Too many arms.** About 50 training runs, 60 checkpoint evaluations, five metric families, a rewrite pipeline and a judge pipeline in two days. Each is easy; together they leave no time to debug the one comparison that matters.
- **Hyperparameters copied from a different regime.** Beta 0.1, lr 1e-5, one epoch were tuned for 5,000 near-deterministic synthetic pairs on a 1B model. On noisy natural data they may barely move an 8B model.
- **Qwen3-8B is a hybrid thinking model.** Chat-template and thinking-token handling in the implicit-reward scorer is a known bug surface; the proposal's unit tests are the right mitigation and should be kept.

## 4. Cost check

Prices are right. Token counts are low.

- UltraFeedback responses in the long-form sources average about 1,500 characters (roughly 400 tokens); a pair is prompt plus chosen plus prompt plus rejected, about 1,000-1,300 tokens, not 800.
- Tinker bills forward-only passes on a training client at the training price. If the recipe computes reference log-probabilities through the training client rather than a cached sampling-client pass, training cost roughly doubles.
- Realistic per-run cost is $5-9, so 50 runs is $250-450, and the total is $350-550.

My estimate for the proposal as written: **about $450**, with a real chance of touching the $500 cap. With the cuts below it is **about $250-300** even with more data per run.

## 5. Recommended changes

1. **Run the controls on the paper's own hotel task first (half a day, under $30).** Regenerate the hotel data (the generator is described in the paper and reused by Selective Tie Learning), train a small Tinker model, and add the three missing controls: higher beta, fewer steps, random labels on non-tied pairs. This has a known large effect, so the frontier comparison is decisive either way, and it is the most direct test of the Chen et al. objection. If the real-data part turns to mush, this alone is a postable result.
2. **Cut the real-data design to what can be powered.** Keep: strict-only, natural ties, constructed ties, random-label non-ties, and a beta / early-stopping frontier with at least 2 seeds per point. Drop arm 3 (covered by Selective Tie Learning), arm 5 (the paper's data-scaling argument is not the contested point), the off-radar feature analysis and the short-answer check, or move them to stage 2.
3. **Make the primary metric independent of GPT-4's length taste.** Lead with (a) implicit-reward gap on verified constructed ties and (b) a regression of held-out reward difference on log length ratio controlling for score difference and source. Report accuracy against MultiPref human majorities as the fit axis. Demote UltraFeedback length-opposed accuracy to a secondary result.
4. **Stratify by source.** Train and evaluate on the long-form sources (evol_instruct, sharegpt, ultrachat), where winner-longer is 62-69%, and exclude or separately report FLAN and false_qa. State the per-source statistics in the proposal instead of the pooled 61%.
5. **Raise the signal.** Use 20-30k strict pairs per run, or 2-3 epochs, and tune lr on the pilot until strict-only DPO shows a measurable length weight. With fewer arms this fits the budget. Use two-way tie labels (both orders), which the paper permits, to remove label-sampling noise across seeds. Use paired bootstrap across arms on the same test pairs.
6. **Pre-register the pilot gate.** For example: strict-only must show a constructed-tie length weight at least 5 standard errors from zero and a generated-length increase of at least 10%. If not, the amplified setting becomes the main experiment and the write-up says so; describe it honestly as semi-synthetic and match the tie pool's source mix to the strict pool.
7. **Pre-specify what counts as "on the frontier".** Give the minimum selective effect the design can detect; if the interval includes both zero and that effect, report "underpowered", not "deflation".
8. **Cite RRM (2409.13156)** and say how this differs. Drop or reframe stage-2 item (b) accordingly.
9. **Fix the cost section:** about 1,100 tokens per pair, and confirm whether reference log-probabilities are billed at the training price.
10. **Before funding, do one keyword search** for "tie training" on LW/AF and the web. Neither the proposer nor I could.
