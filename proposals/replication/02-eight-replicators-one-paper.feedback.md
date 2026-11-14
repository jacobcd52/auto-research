# Feedback: 02 — Eight replicators, one paper

Verdict: **keep with tweaks.** The idea is sound and cheap, but the headline statistic is too imprecise to carry the post, the "independence" of eight copies of one model is the weak point, and the cost and isolation assumptions need tightening.

## What I checked

| Claim in the proposal | Status |
|---|---|
| SLR's hint replication (post `AoBTiL7XRRpwpev8p`): 11 models, 60 filtered questions (correct in >=2 of 4 rollouts), simple delta +0.03 (gpt-oss-120b) to +0.38 (GPT-5.5), complex at most +0.05 (Qwen3-32B), filter "roughly halves" the complex-hint take rate on Gemini 2.5 Flash, LLM judge chosen by the replicator | Confirmed from the post text. Gemini 3 Flash is described as the most cue-susceptible. |
| Emmons et al. is arXiv 2507.05246 and is methods-light on this experiment | Confirmed. Section 3.1 is about three paragraphs plus Figure 3. It reports Gemini 2.5 Pro and 2.5 Flash only, and gives no question subset, sample count, temperature, thinking setting, hint placement or mention-judging procedure. It says it follows the Chen et al. (2025) metadata setting. |
| SLR repo is public | README and `configs/models.yaml` return 200 via raw.githubusercontent. I could not list the tree (GitHub API blocked), so the `results/` JSON the README mentions is unverified. |
| "All four target models are in SLR's roster" | True of the post. But the public `models.yaml` has no Qwen3-32B entry (it lists qwen3-235b-thinking, qwen3.5-122b, gpt-oss-120b, Gemini and Claude models). How SLR served Qwen3-32B is not visible from the config. |
| GPQA: `Idavidrein/gpqa` and `fingertap/GPQA-Diamond` | Both return 200 on the HF API. |
| OpenRouter prices | All five match today's listing exactly (2.5-flash 0.30/2.50, 3-flash-preview 0.50/3.00, gpt-oss-120b 0.15/0.60, qwen3-32b 0.08/0.28, haiku-5.5 0.10/0.50). |
| arXiv 2602.18710 and 2607.01507 exist and are data-analysis many-analyst studies | Confirmed from abstracts. |
| SLR post is after the agents' cutoff | Posted 2026-07-15; consistent with a June 2026 cutoff. The Emmons and Chen papers are well inside training data. |
| Peer-preservation ">20 points" | Not rechecked. |

Prior-work search: the web-search tool was out of budget for this session, so the search was limited to the arXiv API (seven query variants on agent replication, many-analyst, multiverse, researcher degrees of freedom) and a title scan of the 2,000 most recent LessWrong posts (back to late August 2026). I found no multi-replicator study of an LLM-safety experiment. This is a weaker search than a proper web search; the proposer's "not done" claim stands but is not strongly confirmed.

One relevant thing the proposal does not mention: 2602.18710's abstract already proposes "deploying AI analysts against a published specification [to] reveal how much disagreement stems from underspecified design choices". The concept is stated in prior work; the novelty here is the application to a safety eval, where the replicators generate the data as well as analyse it.

## 1. Would it get upvoted?

Borderline, around 40% to clear 50 karma.

- The cluster's position posts got 104 and 124. The actual replications got less: the hint replication this project is built on got 46, and peer preservation got 46. Readers reward the argument for replication more than the replications.
- This project is closer to the position posts than to a rerun: it tests a specific sentence in the 104-karma post ("an independent team will inevitably make many choices differently"). SLR and their audience would read it, and it bears on SLR's own practice.
- What would sell it is the one figure (eight points per model plus SLR's point plus the paper's point) and a short ranked list of "choices a paper must report". If the figure shows the eight landing on top of each other, the post is a shrug: readers will say "eight copies of Fable agree with each other".
- The Emmons hint experiment is a low-stakes target. Nobody disputes its qualitative conclusion, and SLR confirmed it on 11 models. A spread in a number whose sign nobody doubts is less newsworthy than a spread that flips a conclusion.

## 2. Naturalness

A reasonable follow-up to post 2, but a side branch rather than the mainline. The mainline next step for the authors is more replications (which they are doing). This is meta-science about replication. It is not contrived: SLR's own "filter halves the rate" appendix is exactly a forking-path observation, and the proposal extends it in the obvious way.

The blind-replicator half and the factorial half are separable. The factorial (a specification curve over named choices on one harness) answers "which choices move the number" by itself, deterministically and cheaply. The eight blind teams answer a different question: "which choices does an agent replicator actually make". The proposal should be clear that the second question is about Fable agents, not about replicators in general.

## 3. Pre-mortem

How it likely plays out:

1. **The eight teams converge on most choices.** Same model, same paper, same training-data knowledge of Chen et al.'s metadata hint format and of Inspect. Expect all eight to use an XML metadata block, GPQA Diamond (198 questions), temperature default, an LLM judge with a near-identical prompt.
2. **They split on one or two things, mainly how reasoning is obtained.** SLR's config shows this is the big fork: Gemini 3 Flash was run with reasoning disabled and prompted CoT; Gemini 2.5 Flash with CoT in the response body; gpt-oss with native raw reasoning. A team that enables native Gemini thinking gets Google's thought summaries, not raw reasoning, which mechanically inflates "followed without mentioning". This single choice may explain most of the spread. That is a real finding but a one-line one, and predictable in advance.
3. **Nobody uses a competence filter**, because the paper does not and the brief says follow the paper. So every team differs from SLR in the same direction. SLR's point will sit outside the cluster on complex hints for a known reason, and the filter will not appear among "the four choices on which replicators differed most" unless it is forced into the factorial.
4. **The complex-hint quantity is at the floor** (at most +0.05 in SLR, about zero in the paper). There is no between-model variance to compare against, so the variance ratio is undefined for one of the two headline quantities.
5. **The variance ratio for the simple hint is very imprecise.** Between-replicator SD is estimated from 8 teams (7 df) and between-model SD from 4 models (3 df) that were hand-picked as extremes. The interval on the ratio spans roughly a factor of three either way, and its point value is largely a function of which models were picked. Per-team sampling error is also large: about 240 clustered rollouts per condition gives a standard error near 0.04 to 0.05 on a delta, similar in size to a plausible honest replicator spread.
6. **One or two teams have a bug or blow the cap** (hint leaks into baseline, truncated reasoning counted as no-mention, answer-extraction failures counted as not following). The audit agent catches some.

Forecast:

| Outcome | Probability |
|---|---|
| Clear positive: spread well beyond sampling error, traced to named choices by the factorial | 35% |
| Clear negative that is still interesting: tight agreement | 15% (and it is weak evidence, as the proposal admits) |
| Ambiguous: spread comparable to sampling error, or driven by one choice plus one or two buggy teams | 40% |
| Fails to run to a usable figure | 10% |

Specific failure reasons, most likely first:

- **Correlated replicators.** The spread measures Fable's run-to-run variation in defaults. A narrow result says little about human teams; a wide result is hard to separate from agent bugs.
- **Underpowered headline.** See items 4 and 5 above.
- **Isolation is on the honour system.** "The brief forbids searching" is not a control. Any team with web access that searches for the paper title finds SLR's post and repo. Nothing in the plan detects this.
- **The $25 cap is not enforced by anything described**, and the token estimate behind it is optimistic (see cost check). Teams that hit the cap will cut sample size differently, adding spread that is a budget artefact.
- **Judge validity is never checked.** Both team judges and the common judge are unvalidated; the "scored differently" component could be judge noise. With Gemini thought summaries the judge is scoring a different object than with raw reasoning.
- **Comparison with SLR is thin.** Only a few SLR numbers are in the post text (the rest are in figures); the per-model values for the four targets need the repo's `results/` JSON, which I could not confirm, and Qwen3-32B's serving setup is not in the public config.
- **Result partly known.** That native-versus-prompted reasoning and the competence filter move the number is already visible from SLR's post and config.

## 4. Cost check

Prices are right. The token assumption is not: 2k output tokens per call is plausible for prompted CoT but low for native thinking on GPQA, where Gemini 2.5 Flash and Gemini 3 Flash commonly spend several thousand reasoning tokens per question (billed at the output rate). A team using native reasoning could spend $20 to $30 on Gemini 2.5 Flash alone.

Also, teams following the paper will not run SLR's 800-call filter stage; they are more likely to run all of GPQA Diamond (198 questions x 3 conditions x k rollouts), which is 600 to 2,400 calls per model depending on k.

My estimate:

| Item | Proposal | Mine |
|---|---|---|
| Eight replications | $200 | $200 to $320 (cap must be raised to about $40 or enforced with per-team keys) |
| Common-judge re-scoring | $8 | $10 to $20 |
| Factorial | $45 | $60 to $100 (native-reasoning cells cost more; a filter switch needs its own filter rollouts) |
| Reruns | $50 | $50 |
| Judge validation set | not budgeted | $5 |
| **Total** | **$380** | **$350 to $480** |

It fits under $500, but only with real per-team spending limits. OpenRouter keys with credit limits would do it if the project can create them; otherwise a logging proxy.

## 5. Recommended changes

1. **Change the headline statistic.** Drop the between-replicator / between-model SD ratio as "the key number". Report instead, per model: the range across teams against the median within-team interval; the share of team pairs that differ significantly; and whether each team's qualitative conclusions and model ordering match. State the precision limits of eight teams up front.
2. **Make the simple-hint delta the only primary quantity.** Treat complex-hint as a qualitative check (does every team find it near baseline), since it is at the floor.
3. **Pre-specify the factorial switches now; do not wait for the forms.** Use: native versus prompted reasoning; competence filter on/off; judge strictness (or judge model); hint placement or wording. Add a fifth from the forms only if something unexpected appears. This makes phase 3 independent of phase 1 succeeding and guarantees the SLR filter check actually runs.
4. **Add real diversity among replicators, or shrink the claim.** Options, in order of preference: (a) give four of the eight teams a different executing model through an agent harness if the programme allows it; (b) keep eight Fable teams but title and frame the result as "agent replications by one model" and lead with the lower-bound caveat. Do not use personas to manufacture spread.
5. **Enforce isolation and budget.** Per-team API keys with hard limits; network restricted to OpenRouter and Hugging Face where possible; at minimum, scan each team's transcript for the SLR repo or post URL and exclude contaminated teams.
6. **Fix n in the brief** (for example "at least 150 questions per condition, at least 2 rollouts") so sample size is not a source of spread, or record it and accept wider intervals. Raise the cap to about $40.
7. **Validate the common judge.** Have a separate agent hand-label about 150 transcripts (stratified by team and reasoning mode) and report judge agreement before using it for the decomposition.
8. **Record the reasoning object.** The decision form must say whether the judged text is raw reasoning, a provider summary, or body text. Treat this as the first candidate explanation.
9. **Confirm SLR's per-model numbers are obtainable** (the `results/` JSON) before committing to "place SLR's values in the distribution"; otherwise read them off the figures and say so. Consider swapping Qwen3-32B for a model whose SLR serving config is public.
10. **Cut to six teams if money is tight.** Six versus eight changes the precision little; the factorial and judge validation are worth more than teams seven and eight.

If the funder must choose within this cluster, proposal 01 is the more mainline project; this one is worth funding at its price if changes 1, 3 and 5 are made.
