# Feedback: 03 — DiffusionGemma single-canvas serial depth

Reviewer verdict: **keep with tweaks** (narrow it, reuse the existing no-CoT battery, make the fine-tuning arm the
centre rather than an optional extra). Expected karma if run as written: 30-50; above 50 only with a positive
result or a convincingly well-elicited null.

## What I checked

| Claim in proposal | Status |
|---|---|
| DG and Gemma 4 26B-A4B weights public, Apache-2.0 | Confirmed on the HF API (both `gated: False`, apache-2.0; DG is 11 shards). |
| GDM paper arXiv 2606.20560; 28.6x and 1.1x | Confirmed. But the post's wording is conditional: "if we were able to show the intermediates were interpretable, this would drop to 1.1X", and top-k/top-p "maintain *most* performance". The proposal's "keeps benchmark performance, which brings the figure down to 1.1x" is slightly stronger than the source. |
| Open problems 7.2.4, 7.3.3, 7.3.5, 7.3.6, 7.4 | Confirmed verbatim in the paper text. Also relevant and not cited: 7.3.4 (no-CoT time horizon, Gould et al.) and 7.3.7 (thought anchors over denoising steps), which is what step 4 is. |
| Follow-up post, code repo, gentler sampler settings | Confirmed (48 -> 96 steps, temp 1.0-0.5, entropy bound 0.02; repo README and `experiments/` reachable via raw.githubusercontent.com). The post has **40 karma and 0 comments**. |
| Fine-tuning path exists | Confirmed: `unsloth/diffusiongemma-26B-A4B-it` and several community PEFT LoRA adapters exist on HF (one records an A100 smoke test). |
| gpt-6-luna $0.10/$0.50, GPT-6 Sol $2/$10 | Confirmed on OpenRouter today. |
| RunPod GPU prices | Not re-verified by me; taken from NOTES. |
| "No work forces DG to answer without visible reasoning and measures serial depth" | **Not accurate, see below.** |

Search limits: the WebSearch tool was unavailable to me (session budget exhausted), so the novelty check is the
LessWrong GraphQL title scan (all posts since 2026-06-15), the arXiv API (`all:DiffusionGemma`, 14 hits), HF, and
the follow-up repo. A general web search was not done.

### The key thing the proposer missed

The follow-up repo already contains the core of this experiment. `experiments/thinkfast/battery.py` is a
"no-CoT task battery" whose docstring says the tasks "let us ask whether DG's iterative single-canvas denoising
beats a single-pass AR Gemma on graded no-CoT reasoning, and whether the gap scales with serial DEPTH". It has
12 depth-parametrised tasks with exact verifiers (arithmetic, hash, n_hop, sally_anne, tower_of_london, collatz,
reverse_chain, ...), per-task (canvas size C, steps T) budgets, a matched Gemma 4 non-thinking baseline config,
and a task `terse_iterate` (affine-mod map applied k times, canvas C=8, "room for one integer, nothing else ...
the latent-horizon regime"), added to "de-confound the terse-regime result (memorized items + compliance vs
capability)". The worker also lets you set the canvas length directly, capture per-step trajectories, and inject
states mid-denoising.

None of these depth results appear in the published post (only reverse_chain commit order is used), and the
runner/report scripts are not in the repo (`run_dg.py`, `run_ar.py`, `report.py` return 404). So the experiment
is not published, but it was at least set up by someone with a working rig, and probably run. My inference
(not verified) is that an unpublished depth comparison is more likely to have been unremarkable than striking.
That lowers the prior on outcome (ii)/(iii) at default behaviour and raises the value of the elicitation arm.

Nothing else found duplicates it: arXiv 2606.14620 ("Neither Parallel Nor Sequential: How DiffusionGemma Actually
Commits Tokens") and the LW posts on DG (jailbreak by pinning, 19 karma) are about commit order and pinning, not
no-CoT depth. No fine-tuning stress test of DG found.

## 1. Would it get upvoted?

Borderline. Reference points: the GDM audit got 87 (GDM authors, new model); the independent follow-up with a
real finding (top-1 suffices, sampler artifact) got 40 with zero comments; the DG jailbreak post got 19. Posts on
no-CoT capability get 60-140 when they are about frontier models from known authors (Astra filler tokens 141,
no-CoT time horizon 100), and 10-48 otherwise (filler-token LoRA post 10, Dory looping post 48 after two days).
Interest in DG specifically has decayed since June.

- Positive result (DG does clearly more serial steps answer-only than Gemma, and it does or does not survive
  top-1 projection): 60-100. It would be the first public counterexample or confirmation of the 1.1x argument in
  the regime Redwood says matters, and Greenblatt/Westover/Engels would likely engage.
- Null at default behaviour only: 20-35. Readers will say "under-elicited" and move on.
- Null that includes a credible trained-elicitation arm with a positive control: 40-60. This is the measurement
  the Greenblatt et al. proposal asks for, on a real released non-autoregressive model.

Who cares: the GDM interp team (it is their open-problem list), Redwood (well-elicited opaque depth), people
tracking architecture effects on monitorability.

## 2. Naturalness

Mainline. It is literally items 7.3.3-7.3.6 and a light version of 7.4 from the paper, and the "well-elicited"
framing is Redwood's. It is not contrived. The risk is the opposite: it is so obvious that the follow-up author
already built the battery, and GDM or Redwood may be doing the fine-tuned version. The fine-tuning arm is the
part nobody has published and is the part that is hard to scoop cheaply.

## 3. Pre-mortem

How it plays out: day 1 goes to getting DG running on a rented card (52 GB download, the repo's Flask worker,
sampler settings). The worker source notes two specific traps: `device_map` makes batched generation unusably
slow, and on Blackwell GPUs with torch <= 2.8 the MoE forward raises a RuntimeError unless
`experts_implementation="batched_mm"` is set. The proposal's chosen card (RTX Pro 6000) is Blackwell. Solvable,
since the workaround is in the worker, but an agent writing its own harness will hit it. By end of day 1 there
are default-behaviour horizon curves. Day 2 is split between ten conditions, causal patching and two LoRA runs;
something gets dropped, most likely the LoRA, which the plan explicitly permits.

Forecast:
- Clear positive (DG horizon >= 2-3 hops above Gemma on synthetic tasks, with a clean visibility answer): 15%
- Clear negative that is still interesting (tight null including a working fine-tune arm): 25%
- Ambiguous mush (gap of 0-1 hops, sampler- and format-dependent, fine-tune dropped or uninformative): 45%
- Fails to run / only partial default-behaviour numbers: 15%

Specific failure reasons:

1. **Weak prior for a default-behaviour effect.** DG was trained to denoise toward the final text; nothing in
   training rewards writing "holder after pass k" into the answer slot and overwriting it. With the canvas
   restricted to the answer, the most likely result is DG ~ Gemma +/- 1 hop. The existing unpublished
   `terse_iterate` setup points the same way.
2. **The fine-tune arm cannot teach what it is meant to elicit.** A rank-16 LoRA on 5,000 answer-only examples
   with the standard denoising loss gives per-step supervision toward the final answer only. Learning to iterate
   across steps needs credit assignment through the self-conditioning chain; if the training path uses
   single-step (or detached) self-conditioning, there is no gradient for multi-step latent computation, and a
   null says nothing. The proposal does not say how self-conditioning is handled in training. The recent
   filler-token LoRA post is the comparison point for Gemma, and 5,000 examples is probably too few there too.
3. **Permutation task may have a parallel shortcut.** "Ball passed m times around a stated cycle": if the cycle
   is stated in order, the answer is an index offset, not m serial hops, and both models solve any m. Redwood's
   control managing only <= 4 hops implies the passing rule was given as unordered who-passes-to-whom pairs. The
   re-implementation must shuffle the pair list and verify with a Gemma one-pass sanity curve that accuracy falls
   with m.
4. **T is not the number of steps actually run.** The default sampler stops early when entropy is low or the
   argmax is stable for two steps, and re-noises unconfident tokens randomly. A sweep over T in {1,4,16,48,96}
   is meaningless unless early stopping is disabled and the realised step count logged. T=1 and T=4 are also far
   off-distribution for a model tuned for ~48; poor accuracy there is a sampler effect, not a depth measurement.
5. **Canvas constraint is off-distribution in two different ways.** Pinning 250 positions to padding vs shrinking
   `canvas_length` to 8 (what the existing battery does) are different interventions and may give different
   horizons. The model card also says an empty thinking channel may still be emitted with thinking off, which
   eats canvas positions and gives the model a place to write.
6. **"Scratch positions that cannot show text" is under-specified.** If tokens are pinned but the soft
   self-conditioning vector at those positions is left free, that is exactly a hidden channel, and the monitor
   must log the pre-pin logits there. If the vectors are pinned too, the positions do nothing. The proposal needs
   to say which, and the top-1/top-8 projection conditions must be crossed with it or the visibility metric is
   not interpretable.
7. **Visibility metric has a high chance-match rate.** Intermediate values are names from a pool of 30 or residues
   mod 23; logging top-5 at every position across 96 steps will hit them by chance. Needs a shuffled-problem
   baseline (intermediates of a different item), which the plan lacks.
8. **Monitor "which of two problems" is weak here.** The prompt is in context and the answer alone often
   identifies the problem; redacting the answer leaves an empty canvas. The token-match metric and the causal
   overwrite are the informative measures; the LLM monitor adds little in an answer-only canvas.
9. **Factual multi-hop** adds a memorisation confound the proposal already concedes, and the both-models-solve
   filter makes item sets depth-dependent. It costs a third of the compute for the least conclusive task.
10. **Too many arms.** ~10 DG conditions x 3 tasks x 12 depths, plus patching, plus two LoRAs and a re-run of
    everything, in two days on one 26B MoE diffusion model. Agents will produce wide, shallow, noisy tables.

## 4. Cost check

Prices that I could verify are right. The estimate is plausible but optimistic in two places: 2.5 s amortised
per 96-step generation is a guess (batched generation on this model has known problems), and 82 GPU-hours in two
wall-clock days requires two pods, hence two 100 GB downloads and two setups. LoRA on a 26B MoE at bf16 with
gradients will not fit comfortably beside the base weights on one 96 GB card without care (may need the H100 NVL
or a quantised base, which then changes the model being evaluated).

My estimate: $300-450 for the plan as written, with a real chance of overrun into the margin; **$220-300** for
the narrowed version below. Within the $500 cap either way.

## 5. Recommended changes (in priority order)

1. **Acknowledge and reuse the existing battery.** Correct the novelty claim. Start from
   `experiments/thinkfast/battery.py` (`terse_iterate`, `n_hop`, `hash`, `collatz`) and the worker's canvas-length
   control, trajectory capture and injection endpoints, instead of building a new answer-only harness. Email is
   not possible for agents, so state plainly that the depth comparison may have been run but was not published.
   Add modchain/permutation only as the tasks shared with Redwood, with shuffled pair lists.
2. **Make elicitation the headline and fix its design.** The default-behaviour comparison is a one-afternoon
   baseline. Spend the budget on the LoRA arm: specify the training objective (does the loss see multi-step
   self-conditioned rollouts, or one step?), use at least 20-50k examples, and include a **positive control**:
   fine-tune DG to write intermediates in a scratch region and overwrite them before the final step, to show the
   rig can teach cross-step computation at all. Without the positive control a null fine-tune is uninterpretable.
   Drop the "abandon after half a day" clause, or accept that the project then becomes a 30-karma replication.
3. **Cut scope.** Two synthetic tasks, no factual-hop task. T in {default-with-early-stop, 48 fixed, 96 fixed}.
   Three DG conditions at first: soft, top-1, and scratch-region with logged pre-pin logits. Add others only if
   a gap appears. Use adaptive depth sampling around the 50% point rather than 100 items at all 12 depths.
4. **Fix the sampler confound.** Disable early stopping for fixed-T conditions, log realised steps, and report
   default-sampler and gentle-sampler results side by side from the start.
5. **Define the hidden-channel conditions precisely** (token pinned vs vector pinned vs both), and add the
   shuffled-item chance baseline for the intermediate-token match metric. Demote the LLM monitor to a spot check.
6. **Give Gemma a fair elicited comparator.** Filler tokens matched to DG's total position-steps, and the same
   LoRA budget; cite the filler-token LoRA post as the expected Gemma ceiling. The safety-relevant quantity is the
   difference between DG soft and DG top-1 after elicitation, not DG vs un-elicited Gemma.
7. **Tone down section 1** to match the source ("maintains most performance"; 1.1x is conditional on treating
   intermediates as interpretable) and add 7.3.4 and 7.3.7 to the list of open problems addressed.
8. **Hardware note:** if using a Blackwell card, set `experts_implementation="batched_mm"` as the worker does, or
   pick the H100 NVL; avoid `device_map` splitting.

If the cluster can fund only two of three, this is the one I would fund last: proposals built on small models
have far lower infrastructure risk, and this one's most likely outcome is an under-elicited null on a model whose
audience has thinned. With changes 1-3 it is a reasonable $250-300 bet.

Sources: [GDM post](https://www.lesswrong.com/posts/zoYXpdaMgFT43Wc24/how-transparent-is-diffusiongemma-and-why-it-matters),
[arXiv 2606.20560](https://arxiv.org/abs/2606.20560),
[follow-up repo](https://github.com/japhba/diffusiongemma_latent_reasoning) (read via raw.githubusercontent.com:
`README.md`, `post.md`, `experiments/README.md`, `experiments/thinkfast/battery.py`, `experiments/worker/server.py`),
[DG model card](https://huggingface.co/google/diffusiongemma-26B-A4B-it),
[OpenRouter price list](https://openrouter.ai/api/v1/models), LessWrong GraphQL, arXiv API.
