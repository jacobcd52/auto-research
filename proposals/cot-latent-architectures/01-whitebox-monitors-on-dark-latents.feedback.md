# Feedback: White-box monitors on an RL-obfuscated parallel-latents model

Reviewer verdict: **keep, with a restructure.** The question is the right one and nobody has published it, but
the adversarial tiers (the proposal's declared headline) have a design flaw that would make their most likely
outcome uninterpretable, and the per-step probe is defined in a way that conflates three different failure causes.
The cheapest and most informative part of the project needs no RL at all and should be made the core.

## What I checked

- **Redwood post (5guQJSqstkjgys3PE), read in full.** The proposal's summary is accurate: Qwen3-1.7B, zero-init
  d x d W from a late block at t to an early block at t+1, 20% filler SFT, GRPO 32x8, lr 2e-6, KL 0.01, 300 steps,
  5 seeds, gpt-5-nano two-order judge, all-filler CoT at ~40 steps (single filler) / ~50 (random), Sol 0.96-1.00
  for the control on permutation power, 0.01-0.17 for the latent model. Both quotes ("we haven't checked"; the
  future-work bullet on interpretability after RL) are verbatim in the post. No code or checkpoints are linked in
  the post or its comments. Feedback layers N, M and SFT batch size are indeed not stated.
- Two small inaccuracies. (i) "The control plateaued at ~0.7" is the single-filler figure only; random-filler
  control reaches ~0.5 and lower. (ii) "any non-filler token visible (Redwood's own cheaper proxy)" is not quite
  what Redwood used: Experiment 3 used the *visible-token ratio* (graded), on the 1M model with a different SFT
  recipe (visible/covert tags, 1:9 mix). A binary any-token penalty is a new variant; use the ratio.
- **Comment thread on 6m29SfjbittooYojj.** nesiacel's logit-lens claim (Ouro) and Greenblatt's reply ("it may not be
  difficult for the model to learn to control the logit lens accessible part") are quoted correctly. Note the rest
  of Greenblatt's reply: his objection is about architectures that are *scaled up and made performant*. A toy
  retrofit cannot settle that, whichever way it comes out.
- **Dory replication (uxsDuWWHNTpKrsF6P, 48 karma after two days).** Confirmed: one seed per arm, no white-box
  analysis, and it reports that backprop through the recurrence was unstable and had to be truncated to 2 hops.
- **Assets.** Qwen/Qwen3-1.7B, Qwen/Qwen3-0.6B, roneneldan/TinyStories-1M and the Dory checkpoint all resolve on
  Hugging Face.
- **Prices.** OpenRouter today: gpt-5-nano $0.05/$0.40, gpt-6-sol $2/$10 per 1M (batch variants at half price
  exist and are not used in the estimate). RunPod A100 PCIe: $2.09/h secure cloud, **$1.19/h community cloud**.
- **Cited papers.** arXiv 2604.04902, 2604.23460, 2506.14261 exist and are described correctly.
- **Has it been done?** Not that I could find. I listed every LessWrong post since 2026-09-15 by title keyword
  and ran arXiv API queries (latent reasoning + probe/obfuscation/monitor/logit lens, "parallel latents",
  full-bandwidth transformer). Nearest items: arXiv 2610.18127 "Monitoring latent reasoning in looped language
  models" (five lenses on eight looped LMs, no training pressure; not in the proposer's notes, should be cited);
  "Models Trained to Evade Topic Probes Struggle to Answer Questions about Those Topics" (LW 2qnLtNiBph5EjBf6c,
  ordinary transformers, relevant to the accuracy-cost framing). **Caveat: the general web search tool was
  unavailable to me (budget exhausted), so this check covers LessWrong and arXiv only**, not Twitter, workshop
  pages or GitHub.

## 1. Would it get upvoted?

Conditional on a clean result, around 40-45% to clear 50 karma; it depends heavily on which result.

- Reference class: Redwood's post got 107 and the essay 102, but those are Redwood-authored. Outside-author
  white-box follow-ups in this exact area did poorly: nesiacel's Ouro posts 14 and 9, the CODI latents post 10,
  "LLMs can learn multi-step reasoning on filler tokens" 10. The Dory replication, by a well-connected team with
  a new architecture, is at 48.
- "Probes hold" in tier 0 will be read as "of course: one name per step, 30 classes, the model must represent
  the current holder to look up the next pass". The proposal concedes this is a best case for probes. On its own
  that is a 20-40 karma post.
- "Frozen pre-RL probe dies from drift alone while a refit probe works" is the result people would upvote,
  because it is a concrete instance of the AISI drift worry and of the "labels disappear when the CoT goes dark"
  problem. I put this at maybe 30% likely.
- A credible adversarial result (evasion of every reader at no accuracy cost, or a demonstrated accuracy cost of
  evasion) would also clear the bar, but see the pre-mortem: as designed, the adversarial tiers are unlikely to
  give a credible result.
- Who cares: Redwood authors (their own listed open question), the GDM interp team, AISI. That audience is small
  but it is the audience that upvotes.

## 2. Naturalness

Mainline. It is literally a bullet in the authors' future-work list and the live disagreement in the companion
thread. Not contrived. Two consequences of being so obvious:

- Scoop risk is real. Redwood and the Dory authors both have working pipelines and could run probes in a day.
  Nothing is announced in either comment section, but the write-up should go out quickly and tier 0 should not
  wait on the adversarial tiers.
- Because the team must rebuild the architecture with unstated layer choices, this is "white-box analysis of our
  own Redwood-style organism", not of Redwood's. Readers will ask whether probe results depend on the choice of
  N and M (if N is the last block, the fed-back vector is close to the logit basis and the lens is favoured by
  construction; if N is mid-stack it is not). This choice partly decides the logit-lens answer and must be
  reported for at least two layer pairs, not buried as a stability sweep.

## 3. Pre-mortem

**How it plays out.** Day 1 goes on the TinyStories pilot and on getting the 1.7B latent model to reach high
all-filler prefill accuracy with unknown N, M and batch size. This probably works by the end of day 1 on at least
one of 1.7B / 0.6B (the effect reproduced at 1M parameters and on Dory, so it is robust), but it eats the
schedule. Tier 0 RL then works within hours since it is the well-trodden part. Probes are easy. That leaves
well under a day for eight adversarial runs across three reader types with a custom activation-based reward
inside GRPO; these get one attempt each with no tuning.

**Forecast.**
- Clear positive or clear negative on tier 0 (probe transfer and drift), with seeds: ~55%.
- Clear, credible result on tiers 1-3 as well: ~15%.
- Ambiguous mush (tier 0 fine but single-config; adversarial tiers show "no evasion" that cannot be told apart
  from "no training signal", or accuracy collapses): ~30%.
- Fails to run (latent SFT never reaches reliable all-filler accuracy at either scale within the time): ~15%.

**Specific problems.**

1. **Policy-gradient RL has almost no handle on the latents (the main flaw).** GRPO learns from reward differences
   between rollouts of the same prompt, and rollouts differ only through sampled tokens. Once the CoT is all
   filler in the single-filler condition, the eight rollouts of a prompt are token-identical, so their
   activations and the probe's verdict are identical: zero within-group variance, zero gradient for evading the
   probe. In the random-filler condition the only lever is which filler was sampled. The thresholded reward
   ("decodes more than half the steps") makes this worse, since it starts saturated at "caught" for every
   rollout. RL-Obfuscation worked in ordinary transformers because token choice moves the probed activations;
   here the reasoning has been moved off the token channel on purpose. So the most likely tier 1-3 outcome is
   "no evasion in 300 steps", and section 5 would score that as "Probes hold". That would be an artefact of the
   optimiser, and commenters will say so immediately.
2. **The per-step probe conflates drift, re-timing and position shift.** "Holder after pass k at CoT position k"
   assumes the dark model keeps the one-hop-per-position schedule. The control does 4 hops in one forward pass, so
   the latent model can equally run 2-4 hops per position, or lag. A frozen probe that fails could be failing
   because the representation moved (drift), because the schedule changed (re-timing), or because it was fitted
   on positions where the holder is the *next output token* (so it mostly learns the unembedding direction) and
   is being tested on positions where the next token is filler. These need separating or the headline number
   means nothing.
3. **Most of tier 0 does not need RL.** The SFT checkpoint already answers 100% / 86% of problems from an
   all-filler prefill. "Do probes fitted on legible positions read the reasoning at dark positions?" can be
   answered on that checkpoint in an hour. Tier-0 RL adds only 40-300 steps at lr 2e-6 with a KL anchor, which
   is probably small drift. The plan should expect this and treat the no-RL prefill analysis as deliverable one.
4. **The refit-probe upper bound is close to a foregone conclusion.** The task requires the current holder's
   identity to attend to the next pass. A probe refit with ground-truth labels over a (layer, position) grid
   will find it. Fine as a control; it is not a finding.
5. **Reimplementation risk.** N, M, batch size and prompt-position feedback are unspecified. Sequential
   token-by-token training with full fine-tuning of 1.7B and backprop through positions is slow and
   memory-heavy; Dory needed truncation to 2 hops to be stable. The 1.5 h per RL run is a guess.
6. **Text-penalty proxy changes the organism.** With a visible-token penalty rather than the judge, the model is
   optimised for "emit filler", not "hide which problem". For the latent model this ends in the same place, but
   the equivalence check is one seed; state it as a deviation.
7. **Small n on the adversarial tiers.** 2 seeds x 2 filler conditions x 3 readers, when Redwood saw one in five
   seeds collapse on the easy version. Seed-level error bars on n=2 are not error bars.

## 4. Cost check

API arithmetic is right: 300 steps x 256 rollouts x 2 orders = 153,600 judge calls per run, ~$23 each; Sol ~$47
at the stated token counts (Sol at high reasoning effort may use more than 1,000 output tokens; allow $80).
GPU is the uncertain line. I would budget RL runs at 2-4 h rather than 1.5 h, and the reimplementation debugging
at 50-60 h rather than 42 h: roughly 110-130 A100-hours, $230-270 at $2.09/h or $130-155 on community cloud at
$1.19/h. My estimate for the plan as written: **$400-450**; under the cap but with little slack. With the
restructure below (fewer adversarial runs, no-RL analysis first, 0.6B for sweeps): **about $300**.

## 5. Recommended changes (in order of importance)

1. **Fix or demote the adversarial tiers.** Minimum: replace the thresholded penalty with a continuous one (mean
   probe log-probability of the true holder), log within-group reward variance, and state in advance that
   "no evasion with near-zero reward variance" counts as *uninformative*, not as "probes hold". Better: make the
   primary adversarial arm a differentiable penalty through the reader (frozen probe, lens, and alternately refit
   probe), which is the stronger attack and is cheap; keep one GRPO arm in the random-filler condition purely to
   show how weak the RL handle is. That contrast (gradient pressure evades / RL pressure cannot reach the
   latents) is itself a useful and non-obvious finding about what "RL against a white-box monitor" means for
   latent models. Cut tiers to 2 readers x 3 seeds rather than 3 x 2.
2. **Make the no-RL analysis the first deliverable.** On the SFT checkpoint: fit readers on legible positions,
   test on filler positions within mixed CoTs and under all-filler prefill, for latent model and control. This
   survives any later RL failure.
3. **Redefine the probe readout.** Fit and evaluate over a full (layer, position, step-k) grid and report a
   position-by-step decodability heatmap. Define white-box decoding as "holder k decodable at some position by a
   reader fixed before RL", and report separately: same-position transfer (drift), best-position transfer
   (re-timing), and legible-to-filler transfer at the SFT checkpoint (position shift). Fit one probe variant on
   filler positions of the SFT checkpoint (labels are still available there from the gold trace); that is the
   strongest reader a developer could realistically have before the CoT goes dark.
4. **Report dependence on the feedback layer pair** (at least two N, M choices, including N = final block and a
   mid-stack N). Do the sweep on Qwen3-0.6B to keep it cheap.
5. **Add modchain to stage 1 for tier 0 only** if time allows. Its intermediates are multi-token numbers and its
   all-filler accuracy is only 16-36%, so it is the less probe-friendly case and blunts the "best case for
   probes" objection. If not, say so prominently.
6. **Use the visible-ratio penalty Redwood actually used**, not the binary variant, and correct the two small
   misstatements in section 1.
7. **Rewrite section 5's success criteria** so that the three outcomes are distinguished by the transfer
   decomposition in point 3, and so that no outcome can be claimed from an RL arm with no learning signal.
8. **Scope the claim.** Greenblatt's objection concerns performant, scaled latent architectures. Frame the
   result as "the organism used to argue latents defeat CoT monitoring is (or is not) readable with tools
   fitted before obfuscation", and cite arXiv 2610.18127 and the topic-probe-evasion post as neighbours.
9. **Ship tier 0 as soon as it is done.** Given how obvious the experiment is and that two teams hold working
   pipelines, do not hold the write-up for the adversarial arms.
