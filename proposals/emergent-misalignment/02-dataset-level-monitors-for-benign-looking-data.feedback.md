# Feedback: Can a "what would this teach?" monitor catch the training data that row-level monitors miss?

Reviewer verdict: **major overhaul** (keep the idea and the data source; change the primary comparison and most of Part B).

## What I checked

Verified today:
- **Anthropic blog** (alignment.anthropic.com/2026/automated-em-search/, read in full). The monitor description, the 10% / 100-row rejection rule, the withheld prompt and the Qwen 3.6 27B recipe (LoRA r=32, lr 1e-4, 1 epoch, effective batch 8, min 160 steps) are as the proposal states.
- **The map page** (5.4 MB). I parsed the `EPS` array: 613 records, 3 sample rows each (mean 2,128 chars), n_rows 37 to 2,977 (median 850), flag-rate median 0.66%, 11 sets above 10%. `agg5` quartiles 0.034 / 0.109 / 0.222, max 0.68, 174 above 0.2, 157 below 0.034. The proposal's numbers are right.
- **Prices.** Tinker Qwen3.8-27B is $0.6975 / $5.595 / $4.103 and Qwen3.6-35B-A3B is $0.45 / $1.335 / $1.177. OpenRouter haiku-5.5 and gpt-6-luna are $0.10 / $0.50; sonnet-5.5 is $2 / $10 (batch $1 / $5). All match.
- **LessWrong post**: 52 karma, 6 comments, all about hill-climbing as a research strategy; none about monitors.

Not checked:
- **Novelty.** My web search budget was exhausted, so I could not independently search for prior work. The "no one has done this" claim rests on the proposer's search only. A reviser must redo it (arXiv and LessWrong for dataset-level or generalisation-aware training-data monitors, and anything built on the EM dataset map).
- **Benign and known-bad sources.** I did not check that the benign-pool datasets or the OpenAI password-locked sets download.

Small errors in the proposal:
- `agg5` is the mean of five evals, not six; `exfil_offer` is 0.0 for every positive.
- The post's sentence "can be used to directly improve future training data monitors" is from the tweet thread, not the blog. The blog's stated next steps are realism constraints, dilution and covert targets; monitor improvement is not on its list.

## 1. Would it get upvoted?

Possibly, but not for the headline as written. The parent post got 52 karma for an Anthropic result with striking transcripts, so a third-party monitor benchmark on its by-products starts lower.

The stated positive result is "a monitor the data was not optimised against, told what to look for, flags data in which, per the blog, 'some form of misaligned behavior is present in the text itself, just recontextualized as a story or roleplay'". Most readers will predict that outcome. The proposal itself notes the static-attacker caveat, and that caveat is the first comment the post would get.

The versions that could clear 50 karma are:
- A credible false-positive number on real creative-writing and roleplay training data. This is the deployment question labs actually face.
- Evidence that monitor score tracks measured effect within a genre, not just genre.
- Evidence that the "benign" fiction a set-level monitor flags does or does not shift a model. The cluster's own first post found trace EM from the Vellum fiction and finance-alpaca fine-tunes, so some false positives may be true positives.

A clean negative (set-level monitors cannot separate effective from ineffective attacks, or flag 20%+ of ordinary roleplay) is arguably the more upvotable result. My estimate for the proposal as written is 30 to 60 karma, median below 50; with the changes below it is somewhat higher.

## 2. Naturalness

Mainline. It follows the tweet thread's own suggestion and the subtle-vs-obvious authors' "should screen for subtle domain errors". Using the 613 public records is a good, cheap choice. Subject to the novelty caveat above, I know of no existing version. Anthropic can obviously do this better internally with full datasets and the real monitor, so the public value is the open benchmark and the false-positive analysis.

The subtle-advice tie-in is weak. Three sampled rows of subtly wrong advice cannot be judged without domain fact-checking, and that is a different monitor. Treat it as a side tier, not a second "follows up".

## 3. Pre-mortem

Forecast for the proposal as written:

| Outcome | Probability |
|---|---|
| Clear positive (as defined in section 5 of the proposal) | 15% |
| Clear negative that is still interesting | 15% |
| Ambiguous mush: Part A shows high AUROC that a critic attributes to confounds, Part B is weak or mixed | 55% |
| Fails to run: Part B does not produce misaligned Qwen models, Part A alone ships | 15% |

Reasons, from checks on the data:

1. **Positives are one genre.** Of the 174 positives, 83 are in the "occupational monologues" cluster and 35 in "evaluation / gatekeeping writing". The top decile (61 sets) is 51 monologues and 10 gatekeeping, and nothing else. The failed attacks are mostly other clusters (46 expert advice, 27 obsolete objects, 25 philosophical, 24 coding; only 4 monologues).
   - Positives vs failed attacks is therefore largely a genre classifier, and positives vs the public benign pool is "Claude-written hill-climbed monologue vs WritingPrompts".
   - AUROC will be high for uninteresting reasons, and the seven-cluster breakdown will have cells of 1 to 12 positives.
   - The proposal's claim that failed attacks "look similar" is false at the cluster level.
2. **Step 6 is infeasible as written.** "8 from the top decile across different clusters" cannot be done, because the top decile spans two clusters.
3. **Positives are not independent.** The blog says top datasets are "almost always refinements of an earlier attempt"; the top three descriptions are near-paraphrases. Bootstrap CIs over datasets will be too narrow. The effective sample is perhaps 20 to 40 lineages.
4. **The label is mostly one eval.** Among positives the mean monitor-disruption score is 0.85, against Betley 0.43, frame-colleague 0.41 and self-preservation 0.28. A set can pass 0.2 on monitor disruption alone, which the blog calls "relatively mild" for the beekeeping set. The labels come from single fine-tunes of a small Claude model with no seed noise estimate, so the bottom quartile is not reliably "no effect".
5. **Dose confound.** `agg5` correlates with n_rows (Spearman 0.39; positives' median is 1,061 rows, failed attacks' 815). A monitor reading three rows cannot see dose. Part B then reconstructs everything at 500 rows, less than half what the top sets used (median 1,209), which is another reason reconstructions may underperform.
6. **"Set-level" means three rows.** M2 vs M1 confounds aggregation with three times the context. Whether the three samples are random or chosen for display is unknown. The actual dataset-level claim rests entirely on Part B's synthetic reconstructions.
7. **The benign pool decides the headline and is the weakest part.**
   - TPR at 1% FPR on 600 benign sets is fixed by the six highest-scoring benign items.
   - Public human fiction differs from the positives in authorship, register, length and format, so a low FPR there says little about FPR on a lab's synthetic roleplay and character data.
   - The relevant negatives are Claude-written, benign-intent fiction and persona data in the same format, plus real roleplay corpora with villains and morally grey narrators. Neither is in the plan.
8. **M0 is unanchored.** Any generic prompt flags under 10% of rows on these sets, so "matches their flag rate" is a weak check. The sets were optimised against a specific classifier and threshold; a different prompt or model is already a non-adaptive transfer test. M0 may itself score well, which collapses the M0 vs M2 story. That would be worth reporting, but it changes the framing.
9. **Part B is a long chain.**
   - Sonnet has to write 16 x 500 rows of monologues about covert power from three anchors without mode collapse or declining.
   - The model is Qwen3.8-27B; Anthropic showed transfer on Qwen 3.6 and only for selected sets.
   - The eval is Betley questions plus 20 home-made ones, while the originals' strongest effect is on an agentic scenario that is not being rebuilt.
   - With 22 sets split 8 / 8 / 6, "monitor score predicts Qwen misalignment" is a three-group comparison in which group is confounded with genre, not a correlation.
   - The gate (2 of the first 4 above baseline) is sensible. I put the chance that reconstructions give a clear, multi-set effect on Qwen3.8 at about 50%.
10. **Judge contamination.** First-person fiction fine-tunes produce in-character or off-format answers that the standard Betley judge counts as misaligned. This is the exact failure the cluster's first post documents. The plan uses "the standard alignment and coherence prompts" and so will hit it.

## 4. Cost check

Unit prices are right and token counts are plausible. Part A at about $65 is realistic and could be about $35 with batch pricing.

Part B risks:
- Qwen3.8-27B is a hybrid reasoning model. If thinking is not disabled, sampling at $5.595 per M could cost 3 to 5 times the $46 line.
- Reconstruction rejects and reruns are likely.
- Training at about $95 to $110 is fine.

My estimate is **$380 to $520 as written**, which is tight against the cap with only 15% margin. The redesign below is **about $300**.

## 5. Recommended changes (in order)

1. **Change the primary analysis to within-genre and lineage-aware.**
   - Report (a) Spearman of monitor score with `agg5` within each cluster, (b) positives vs failed attacks within the clusters that have both (authority roleplay 22 / 11, gatekeeping 35 / 11, obsolete objects 12 / 27, expert advice 11 / 46), and (c) leave-one-cluster-out results.
   - Deduplicate into lineages (description embeddings or the `mech` stem) and bootstrap over lineages.
   - State up front that pooled AUROC against the public pool is a sanity number, not the headline.
2. **Fix the benign pool.** Add:
   - Claude-generated benign-intent sets in the same seven genres and format, written by a generator given only a genre brief ("occupational first-person monologues", "authority roleplay"), with no misalignment goal, three rows each.
   - Real roleplay and character-card corpora with dark characters.
   - Report FPR per source and treat the matched-generator FPR as the main one.
   - Report TPR at 5% and 10% FPR with CIs, and drop the 1% headline unless the pool has at least 2,000 items.
3. **Add trivial baselines.** Row length, first-person rate, an embedding nearest-centroid classifier, and M0 at several thresholds. If these match M2, say so.
4. **Separate context from aggregation.** Give M1 the same three rows scored independently and max- or mean-pooled, against M2 reading them jointly.
5. **Shrink and refocus Part B on a different question: are the flagged "benign" sets actually harmful?**
   - Fine-tune on about 6 benign fiction or roleplay sets the best monitor flags most strongly and about 6 it passes (real public data, no reconstruction needed).
   - Add 4 reconstructions (two monologue, two gatekeeping, at about 1,000 rows to match the originals' dose) as positive controls behind the existing gate.
   - Drop the 8 failed-attack reconstructions. A reconstruction of a null is uninformative.
   - Run the 10-row and 30-row window monitors on these real full sets, which gives a real dataset-level test.
6. **Fix the Qwen eval.**
   - Use the dataset-aware "type 3" judge from the Broyojo repo alongside the standard one.
   - Disable thinking, or budget for it.
   - Add a text-only version of the monitor-disruption question, since that eval carries the label.
   - Run a known-positive control (a Turner et al. advice set) through the same pipeline first to rule out an eval bug.
   - Consider Qwen3.6-35B-A3B for all but the positive controls to save about $100.
7. **Reframe sections 2 and 5.** The data was optimised against one specific monitor, so "another monitor catches it" is expected. The contribution is the false-positive cost and whether monitor score tracks effect rather than genre. Pre-register the within-cluster rho (say 0.3 or above in at least three clusters) as the positive criterion. Make "set-level monitors flag synthetic benign roleplay at 20% or more" or "within-genre rho near 0" the explicit negative.
8. **Corrections.** `agg5` is five evals; attribute the "improve monitors" quote to the tweet thread; redo the prior-work search; demote the subtle-advice tier to an appendix or drop it.

With changes 1 to 4 alone, Part A is a roughly $60, one-day result that stands by itself. If the funder is short, fund Part A with the fixed pool and the flagged-benign fine-tunes (about $200 in total) and defer the reconstructions.
