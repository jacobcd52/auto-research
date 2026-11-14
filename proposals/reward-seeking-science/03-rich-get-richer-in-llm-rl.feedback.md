# Feedback: 03 — "Does RL amplify whatever the model starts out doing?"

Verdict: **major overhaul**. The question is good and apparently still open, but Phase A as designed does not
test rich-get-richer at all, the success criteria cannot separate the outcomes even if the toy model is exactly
right, and the proposal misses the paper that both proved the theorem and built the LLM setup it should reuse.

What I checked, and how:
- Read the toy-models post and the Arrow post in full; fetched arXiv 2607.03478 (PDF) and read the relevant parts.
- Tinker prices checked against the Tinker docs dump: gpt-oss-20b $0.18 / $0.45 / $0.396 and Qwen3-8B
  $0.195 / $0.60 / $0.44 are correct. `importance_sampling` loss exists as described.
- Arrow repo: `raw.githubusercontent.com/Arrow-Research/grader-targeting-reasoning-from-sdf/main/README.md`
  returns 200, so it is public (github.com HTML is 403 through the proxy). The Arrow rollouts dataset on HF
  returns 200. I did not inspect the Geodesic simulation repo (403); it is linked from the post.
- Ran the toy model's ODE myself (3 actions, rewards 1/1/0) to get predicted effect sizes; numbers below.
- **Not done: an independent web search for duplicates.** The WebSearch budget for this turn was exhausted, so the
  "has this been done" check rests on the posts' own citations and the one paper I fetched directly.

## 1. Would it get upvoted?

Conditionally yes. The cluster's theory posts got 89 (toy models), 124 (Meinke) and 70 (Geodesic agenda) with no
LLM data; the one empirical follow-up (Arrow, 54) was received modestly. A clean figure "initial share vs final
share in real LLM RL, with the theory curve, many seeds" is the obvious missing plot and would plausibly clear 50
— *if* the test is of the thing the theory is about. As written, the headline Phase A result would be met by a
top comment from the authors pointing out that format choice is a reward-independent behaviour, for which their
own model predicts no drift (see §3, point 1). A post whose main experiment is refuted in the comments by the
theory's authors does not get 50. Phase B is the part readers care about (reasoning routes), and it is the
under-resourced, optional part.

Audience: Geodesic, Arrow, Apollo (Meinke), people doing pre-RL intervention work. Small but engaged.

## 2. Naturalness

Mainline: the screener's note, Meinke's "prior-boosting by SFT" suggestion, and Geodesic's request for work that
"validates or falsifies" all point here.

Prior work the proposal misses, which changes the framing:
- **Barzdukas, Peck, Schulz, Rauba, Basart, Wells, "Demonstrating Generalization Failures via Mixtures of
  Conditional Policies" (arXiv 2607.03478, July 2026).** The toy-models post cites it as the first proof of the
  amplification claim (Prop. 2.1(ii): among equally optimal components, the initially heavier one's weight ratio
  strictly increases). More importantly it already builds the experimental object this proposal needs: SFT on a
  mixture of transcripts from output-identifiable policies ("I am Alice, the answer is [B]") so the mixture
  weights are read directly from completions, followed by RL (GRPO, 5 seeds, Qwen2.5-1.5B / Llama-3.2-3B /
  Gemma-3-27B), with policy probabilities tracked through training.
- So the proposal's sentence "Neither post contains an LLM experiment ... My searches found no other test" is
  wrong in spirit: an LLM test of the *concentration* half of the theorem exists. What I could not find in that
  paper is an empirical test of the *amplification* half — their experiments use components with unequal
  training reward, and the appendix says the details of amplification within the optimal set "remain open". So
  the specific experiment still looks undone, as far as I could verify.
- Scoop risk is real: Wells is an author of that paper, of the toy-models post's sister work and of the Arrow
  post. This group has the setup on disk. A two-day project is still worth doing but should say so.

## 3. Pre-mortem

**1. Phase A tests the wrong prediction (fatal as designed).** Rich-get-richer in the toy model comes from two
high-reward actions competing against a *shared* low-reward action: d/dt(theta_A - theta_B) =
(pi_A - pi_B)(r_top - r_bar), because both A and B have reward above the mean. In Phase A the answer format is
chosen after (and independently of) solving the problem. The expected reward of "format A" rollouts is the
accuracy; so is that of "format B" rollouts; so is the mean. Reward minus baseline, conditional on format, is
zero. The matching toy model is the post's section on *underspecified / reward-independent behaviours*, which
predicts the share stays put. The proposal's planned regression on (pi_A - pi_B) x (1 - accuracy) applies the
3-action rate law to a factorised 2x2 situation where it does not hold. Consequences:
   - The likely result is "preservation", which the proposal would report as "a direct, quantified challenge to
     a load-bearing argument". It would be nothing of the kind; it is what the theory predicts for this design.
   - The "saturated control" then shows the same thing as the main arm, so it controls for nothing.
   To test amplification, the strategy choice must come *before* and *determine* the reward: two strategies that
   both succeed and a third that fails, with the choice identifiable in the output.

**2. The success criteria cannot discriminate even in a correct design.** I integrated the toy ODE. Starting at
50% suboptimal mass with a 70:30 split between the two optimal actions, the optimal-pair share of A is:
~0.78 when suboptimal mass has fallen to 20%, ~0.83 at 10%, ~0.86 at 5%, ~0.93 at 1%. Starting at 30% suboptimal:
0.73 / 0.78 / 0.82 / 0.90. From 60:40 and 50% suboptimal: 0.65 / 0.69 / 0.73 / 0.83. The drive is proportional to
remaining suboptimal mass, so amplification is slow and mostly happens in the long tail. Therefore:
   - "70:30 ends beyond 90:10" requires pushing failure rate to ~1%; the proposal's own bar for selection pressure
     is "accuracy rising >= 20 points", under which the theory predicts a shift of only ~4-8 points.
   - "Preservation = within ~10 points of initial" is then *inside* the theory's prediction. The two named
     outcomes overlap. Section 1's "a 60:40 start ends near 100:0" is true only asymptotically.
   - Detecting a 5-8 point shift needs per-checkpoint share estimates with SE of ~1-2 points (>= 1,000 scored
     rollouts) and more than 3 seeds. The plan measures share on the 128 training rollouts (SE ~4 points).

**3. Sixty steps is probably far too few.** Barzdukas et al. needed 500 GRPO steps (1,000 for 20 policies) to
drive selection on small models. Arrow's Wood runs were 100 steps on a 120B model with a custom dynamic-sampling
rule added specifically to avoid collapse. A pilot that finds a learning rate at which accuracy on arithmetic
word problems rises 20+ points in 60 LoRA steps without format collapse is not guaranteed in two days.

**4. Phase B has the right structure but the weakest measurement.** Comply (low reward) vs G vs U (both high) is
the correct three-way competition. But: (a) the shares are set by SFT on Sonnet-written traces in gpt-oss-20b's
reasoning channel; hitting 20/50/80% G *while* holding compliance at 50% is a two-dimensional calibration target
with SFT, and Apollo's open-problems post describes exactly this kind of recall tuning as finicky; (b) G vs U is
read by an LLM judge on short reasoning that can state both or neither — the "both/neither" bin may swallow the
effect; (c) G asserts a fact about the grader that is nowhere in the prompt (in Arrow it came from SDF plus a lab
header), so traces may read as hallucinated and wash out in a few RL steps; (d) Arrow reports reward saturating
within ~20 steps once the model knows what is graded — a short selection window means, by point 2, a predicted
amplification of a few points, with 3 seeds x 3 ratios and judge noise on top; (e) Wood here is run without Yard,
with a different, much smaller model than Arrow used, so "reuse" is partial. Expect mush.

**5. Shared parameters cut both ways and the write-up must not over-read.** An LLM is not a softmax over three
logits; with a strategy token up front it is close to one, with diffuse reasoning it is not. A null in Phase B
would not tell you whether the theory fails or the judge/SFT failed.

**6. Noise test.** 5 seeds per setting to compare *variances* of final share is hopeless statistically
(a variance ratio needs to be ~6x for p<0.05 at n=5 vs 5), and the two settings differ in two things at once.

Forecast for the proposal as written:
- Clear positive (amplification, convincingly matching theory): **10%**
- Clear negative that is still interesting: **10%** (a clean Phase A "preservation" is clear but, per point 1,
  not interesting; an interesting negative needs Phase B to work)
- Ambiguous mush (small shifts, wide seeds, design-level objection in comments): **60%**
- Fails to run / RL does not move accuracy in budget: **20%**

With the redesign in §5 I would put it at roughly 35% clear positive, 25% clear and interesting negative,
30% mush, 10% fail.

## 4. Cost check

Prices are right and the per-step arithmetic for Phase A reproduces ($0.066/step). The assumptions are optimistic:
- 400 sampled tokens per rollout for a reasoning model on problems it gets half wrong is low; 800-1,500 is more
  likely, i.e. $0.10-0.17/step.
- If runs need 200-500 steps instead of 60 (point 3), the 31 Phase A runs alone cost $600-2,500. The plan as
  written fits $400 only if 60 steps suffice, which I doubt.
- Phase B at $10/run is plausible for 60 steps; again the step count is the risk.

My estimate for the plan as written: **$450-900**, i.e. it likely breaches the $500 cap or gets cut to too few
seeds. The redesigned Phase A below uses ~30-token completions with no reasoning: 128 rollouts x (150 prefill +
30 sample) + ~25k train tokens is about $0.015/step, so a 400-step run is ~$6 and 60 runs is ~$360 on gpt-oss-20b;
cheaper still with fewer steps or a non-reasoning small model. Redesigned total with a reduced Phase B: **~$350-450**.

## 5. Recommended changes (in order of importance)

1. **Replace Phase A with a three-policy mixture, Barzdukas-style, and cite that paper as the basis.** SFT a
   mixture of three output-identifiable policies on one task distribution: Alice and Bob both answer correctly,
   Carol refuses or answers wrongly (the shared suboptimal action). The name comes first in the completion, so
   the choice precedes and determines reward and the toy model applies literally. Sweep the Alice:Bob ratio
   (50/60/70/80/90) at a fixed Carol mass (~50%). This is the direct empirical test of Prop. 2.1(ii), which its
   authors left open. Keep the current two-format task only as the explicit *reward-independent* arm, with the
   prediction stated correctly beforehand (no drift) — then it is a test of claim (iii), not a broken test of (i).
2. **Rewrite the predictions as numbers from the ODE at the observed suboptimal mass**, not "beyond 90:10".
   Plot share of Alice within the optimal pair against remaining Carol mass, overlaid on the parameter-free
   theory curve (that relationship does not depend on learning rate). Pre-state what counts as "less than
   theory", "matches", "more than theory". Train until Carol mass is <= 2-5%, not for a fixed 60 steps.
3. **Fix the measurement.** Evaluate each checkpoint on >= 1,000 held-out samples at training temperature
   (regex-parsed, free); >= 8 seeds on the 60/70/80 ratios; swap which name is the majority in half the seeds.
4. **Add the unequal-reward tipping point now, not in stage 2**, since it is nearly free in this setup: give the
   minority policy a small accuracy advantage and find how large it must be to overturn a 70:30 or 90:10 prior.
   That is the result safety readers would quote ("a prior of X is overturned by a reward edge of Y").
5. **Shrink Phase B to one honest bridge experiment**, run only if 1-4 are done by the end of day one: the same
   three-way structure with the strategy marked by a short stated *reason* before the answer instead of a name
   (regex-identifiable phrasing, not judge-labelled free CoT). Drop the Wood/G/U design, the Haiku judge and the
   held-out grader probe from stage 1; move them to stage 2. This also removes the SFT-on-reasoning-channel and
   Sonnet-trace dependencies.
6. **Drop or redo the noise test.** If kept, vary one factor (batch size) with >= 10 seeds at 50:50 and compare
   to the finite-sample RLOO simulation from the Geodesic code; otherwise cut it and spend the runs on seeds.
7. **Correct section 1**: credit the theorem and the SFT-mixture construction to Barzdukas et al.; state that the
   untested part is amplification among equally rewarded components; note the overlap in authorship with the
   Geodesic/Arrow posts and the resulting scoop risk. Also state the algorithm mismatch (Tinker importance
   sampling with group-centred advantages vs their GRPO with KL penalty) and avoid any KL-to-reference penalty,
   which would mechanically pull shares back to the initial split.
8. Before the sweep, a go/no-go pilot: one run from 70:30 must show Carol mass falling below 10% within the
   step budget without collapse of the name format. If not after ~$50, switch model (Qwen3-8B, non-thinking)
   rather than tuning further.

If the proposer will not restructure Phase A, I would not fund this as written: the most probable deliverable is
a preservation result on a design where preservation is what the theory already predicts.
