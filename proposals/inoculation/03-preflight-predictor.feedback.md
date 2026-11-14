# Feedback: 03 — A pre-flight check for inoculation

Reviewer verdict: **major overhaul**. The headline question has a published partial answer the proposal does not
cite, and the pre-registered decision rule does not test what it says it tests. A narrower, reframed version is
fundable.

How I checked: read the IA post and arXiv 2606.30252v2 (HTML), the conditionalization post, the Xenomirant post,
arXiv abstracts for Wichers, SIP, Warncke et al. 2610.14937, and arXiv listing searches for "inoculation
prompting", "inoculation adapters", "preventative steering". The WebSearch tool was unavailable in this session
(budget exhausted), so the prior-work check is arXiv listings plus LessWrong posts only; I did not search
LessWrong or the wider web for unpublished follow-ups.

## Claims verified

| Claim | Status |
|---|---|
| IA paper Discussion quote "A more convenient method would allow predicting which method works best before or at the start of task training" | Verified verbatim |
| IA paper Appendix C: IA lowers first-step loss | Roughly. The text says "In **most** setups, IAs have lower initial losses than SFT(Harmful)", not all |
| IA(Random) ~ SFT(Harmful); IA(Irrelevant) reduces both traits | Verified (section 4.2) |
| B1/B2 hyperparameters (Qwen2.5-7B-Instruct, rsLoRA r32 a16, batch 8, lr 3e-5 for B1, 5,000 examples) | Verified (Tables 2, B.4) |
| Riché & Warncke: Wichers heuristic "good ... but insufficient" | Verified in the post text |
| Riché & Warncke suggest "specificity" as the missing variable | Not verified. Appendix D is a Google Doc I did not open; the post body does not use the word in that sense |
| No released IA code | Consistent with what I found: no repo link in the arXiv HTML |
| `geodesic-research/sfm-emergent-misalignment-training-data` public | Verified: ungated, not private |
| RunPod A100 SXM secure $2.19/h; gpt-4.1-mini $0.40/$1.60 on OpenRouter | Both verified today. OpenRouter lists no logprobs for gpt-4.1-mini, as NOTES says |
| "I found no test of one predictor across carrier types" | **Wrong in substance; see next section** |

## The missed prior work

**Grant, Gillioz, Ward, McGrath (Goodfire), "Shifting the Gradient: Understanding How Defensive Training Methods
Protect Language Model Integrity", arXiv 2604.16423v2 (April 2026).** Same base model (Qwen2.5-7B-Instruct),
LoRA fine-tuning, inoculation prompts versus preventative steering, six traits including all-caps, four models.
Code and data are public (`github.com/satchel-goodfire/shifting_the_gradient`, MIT). Their Section 5 measures
exactly the proposal's U for two of its three carrier families:

- Inoculation prompts lower next-token loss on trait-expressing data.
- Preventative steering vectors lower it only at low intensity and **raise it at the intensities at which they
  defend**. A random vector of equal norm also raises it.
- They offer a different step-0 statistic (sign and size of the gradient component along the trait vector) and
  show by gradient manipulation that it is causally relevant, but state in Limitations that it "does not order
  the strength of defenses across settings" and that "a favorable shift accompanies a failed defense for one
  trait".

Consequences for this proposal:
1. For prompts versus vectors, the "one law in U" outcome is already refuted on the same model. Effective steering
   has U below zero. The proposal's "negative but informative" outcome ("carriers differ in kind") is, for those
   two families, Grant et al.'s published headline ("PPS and IP are not interchangeable").
2. The steering strengths in the plan (1, 2, 5, 8) span the region where loss turns from falling to rising, so U
   will be non-monotone in dose inside that family. A monotone fit of suppression on U cannot hold there.
3. What remains new is the **adapter family** and the **retention side (D)**. Neither is in Grant et al.

Other uncited items, less damaging: "Neologism Inoculation Prompting" (arXiv 2611.04260, Africa & Holmes, Nov
2026) adds a learned-token carrier, which overlaps stage 2's "learned soft prompts". Warncke et al. 2610.14937
conclude "no single dominant predictor emerges, and generalization remains hard to predict", which sets the
prior for any predictor claim in this area.

## 1. Would it get upvoted?

As written, if stage 1 "succeeded" it would most likely report prompts on a curve and vectors off it, which a
reader who knows the Goodfire paper already believes. I put a post like that at 20 to 40 karma. The cluster's own
posts (68 to 102) introduced a method or overturned an accepted reading; a predictor scatter plot on two setups
with mostly single-seed points is a weaker object, and this literature's readers (Riché, Warncke, Tan, Kohonen,
the Goodfire authors) are precisely the ones who will ask about n, seeds and the missing citation.

A version that would clear 50: a head-to-head of several pre-flight statistics, including Grant et al.'s
gradient statistic, extended to adapters, ending in either "this statistic ranks carriers across all three
families and would have picked the right method in k of n setups" or "none does, here is the counterexample for
each". Either is a direct answer to a sentence in the IA paper's Discussion, and the IA authors would read it.

## 2. Naturalness

The question is mainline: the IA paper asks for it in so many words and cloud's post invites it. The specific
operationalisation is not the natural one any more. The natural next step after Grant et al. is "does their
step-0 gradient picture extend to adapters, and does anything predict retention", not "does loss reduction
unify the families", which they tested and answered no for vectors.

One conceptual slip: the proposal labels "U alone" as "the Wichers heuristic". Wichers' heuristic is behavioural
elicitation (how much the prompt makes the untrained model show the trait), not loss reduction. Strong steering
elicits the trait behaviourally while raising loss on trait data, so the two come apart exactly where it
matters. Behavioural elicitation needs to be its own predictor.

## 3. Pre-mortem

How the two days go, as written. Day 1: reimplementing stacked LoRAs with one frozen, steering hooks, and three
parallel datasets is routine; the French EM data for S2 takes longer than planned because a commercial model
softens or refuses some translations of dangerous advice and the "harmless French" set has to be generated and
spot-checked. The gate (IA suppresses more and retains less than IP on S1) is at real risk: I could not confirm
that per-setup ordering for B1 from the paper text (it is only in figures), and the paper stresses that results
are "strongly setup-dependent". A faithful replication could fail the gate. Day 2: 72 runs complete; the
analysis shows within-family dose-response for prompts and adapters, vectors with U near or below zero yet real
suppression, and adapters with U near saturation.

Probabilities for the proposal as written:
- Clear positive ("one law", 0.8 on both outcomes in a meaningful cross-family sense): **about 7%**
- Clear negative that is still interesting: **about 30%**, but most of that mass is the vectors-off-curve
  result that is already published; a new, clean adapter-specific negative is perhaps 10 to 15%
- Ambiguous mush: **about 48%**
- Fails to run or fails the gate without a usable fallback: **about 15%**

Specific reasons it underdelivers:

1. **The decision rule does not test cross-family transfer.** Spearman correlation is invariant to any monotone
   transform, so "fit a monotone function on one family, report Spearman on the held-out family" equals the
   held-out family's own within-family Spearman between U and suppression. The fit contributes nothing. A set of
   dose series (four scales of one adapter, four strengths of one vector, weak-to-strong prompts) will show high
   within-family rank correlation almost by construction, and the rule would declare "one law" even if the three
   families lie on three different curves. Only the MAE figure tests a shared curve, and it has no threshold.
2. **n is too small for the thresholds.** Held-out families have 6, 8 and 10 points, mostly one seed. With n = 6,
   the 95% interval on a Spearman of 0.8 runs from roughly 0 to 0.98. The 0.8 / 0.5 cut-offs cannot be
   distinguished.
3. **Effective n is smaller than it looks.** About half the carriers are scale variants of one object, and the
   random and irrelevant controls cluster at the origin. Correlations will be driven by "controls at zero, real
   carriers elsewhere", which is not evidence for a quantitative law.
4. **U is near-degenerate for adapters.** The IA is trained by gradient descent to minimise loss on
   undesired-only data, and U is normalised by a model fine-tuned on that same kind of data. The standard IA has
   U close to 1 by construction; the only spread comes from deliberately crippling it (scale, rank, 500
   examples). That tests a dose-response, not a predictor that would help a practitioner choose between methods.
5. **Known sign problem for vectors** (above).
6. **Trait interaction in S1.** Training data is French in capitals; U is measured on English capitals and D on
   lower-case French. A capitals carrier probably raises loss on lower-case French (negative D) for reasons
   unrelated to retention. The French/caps pair is also a pair where the Riché & Warncke post found
   conditionalization effects large relative to inoculation, so run-to-run and prompt-wording noise will be high.
7. **Seed noise.** The source papers use one seed per point and report wide intervals. Three seeds on six
   carriers estimates noise, but if it is large (plausible for EM rates on 480 clustered completions) the 36
   single-seed points are uninterpretable and there is no budgeted remedy beyond "report the null".
8. **Two setups sharing the desired trait** (French in both). The cross-setup test has two points.

## 4. Cost check

Unit prices are right. 5,000 Alpaca examples at batch 8 is 625 steps, and 15 minutes per run including
generation on an A100 is plausible with batched generation; S2's longer answers may take 25 minutes. My estimate
for the plan as written: 35 to 50 GPU-hours ($80 to $110), API $40 to $60 (translation refusals and reruns),
total **$130 to $180 before margin, about $250 with margin**. The $230 figure is fair. The revised design below
(more seeds, fewer scale variants, gradient statistics needing backward passes) fits in about **$300**. Cost is
not the problem with this proposal.

## 5. Recommended changes, in order of importance

1. **Cite Grant et al. 2604.16423 and rebuild the question around it.** New question: "Grant et al. showed loss
   reduction does not unify prompts and steering, and proposed a step-0 gradient statistic that they say does not
   order defenses across settings. Does any pre-flight statistic rank carriers across prompts, vectors **and
   adapters**, for both suppression and retention?" State up front that the prompts-versus-vectors loss result is
   a replication target, not a finding.
2. **Run a horse race of four or five cheap predictors**, all computed before or in the first few percent of
   training: (a) loss change U and D as now; (b) behavioural elicitation of each trait with the carrier attached
   (the actual Wichers heuristic); (c) Grant et al.'s step-0 gradient projection on the undesired and desired
   trait directions; (d) a short probe: train 30 to 50 steps with the carrier, detach it, and measure trait
   expression or the task-LoRA update's projection on the trait directions; (e) carrier family alone. The IA
   paper asked for prediction "before or at the start of task training", so (d) is in scope and is the one most
   likely to work.
3. **Replace the decision rule.** Pool all families and report pooled Spearman and a leave-one-family-out
   calibration error with a stated threshold; additionally test for a family offset (outcome regressed on
   predictor plus family indicator, or a permutation test on residuals by family). "One law" requires high pooled
   rank correlation **and** no family offset. Report bootstrap intervals over carriers and seeds. Add the
   practitioner's metric: does the predictor pick the best carrier, or the best family, per setup.
4. **Change the carrier set from dose series to distinct carriers.** Keep at most two scales per object. Add
   distinct prompts (the IA paper's task-specific, EM and "villain" prompts), vectors at two layers and from two
   extraction recipes, and adapters trained on different data (in-distribution versus UltraChat, different
   undesired-data generators). Aim for about 8 genuinely different carriers per family and **three seeds for
   every carrier** in one setup before adding the second setup. Fewer points with error bars beat 48 single-seed
   points.
5. **Start from the Goodfire code** for the prompt and steering arms (public, same model) and add the frozen
   adapter arm to it, instead of building the loop from scratch. Check on day 1 that raw.githubusercontent.com
   serves the repository from the sandbox.
6. **Fix the gate.** Do not gate on "IA suppresses more and retains less than IP on B1" unless that ordering is
   read off the paper's per-setup figure first. Gate instead on: SFT on mixed data learns both traits, standard
   IA suppresses the undesired trait relative to SFT, and IA(Random) does not.
7. **Pick setups with different desired traits**, or drop S2 from stage 1 and spend the money on seeds. If S2
   stays, generate the French EM data with an open model that will not refuse (the IA paper used Qwen3-32B
   variants) and spot-check 100 examples.
8. **Lower the claim.** Two setups on one 7B model cannot establish a "law". Write the success criterion as
   "statistic X would have selected the best or second-best carrier in both setups, across families, and beats
   elicitation strength and family identity"; write the informative negative as "no step-0 statistic does;
   a 50-step probe does / does not".

If the proposer does not want to restructure, my advice is to fund proposal 01 from this cluster and drop this
one: as written, the most probable deliverable restates a published result with less statistical support.
