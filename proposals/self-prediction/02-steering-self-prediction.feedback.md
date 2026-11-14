# Feedback: 02 — Does the talker notice when the doer is steered?

Reviewer verdict in one line: **keep, but the main analysis as written cannot distinguish "reads its steered
state" from two boring explanations (baseline borderline-ness and concept priming); fix the design before
spending anything.** The idea is natural and cheap; the headline metric is the weak point.

## What I checked

- **Ward's post (kTg5FrABJYpYrP8ps), read today.** Confirmed: Qwen3.8-27B, Binder chat dataset, non-thinking
  temp-0 labels; SFT self-predictor AUROC 0.75 vs Kimi 0.68 on the 103 one-off ImpossibleBench tasks;
  forced-different control gets 0.25; in the RL experiment "AUROC is only just above chance throughout
  training"; no code link; $42k of Tinker credits. Two details the proposal gets slightly wrong or omits:
  - Ward's prompt says "up to **10** attempts"; the proposal's optional cheating arm says 5. If the arm claims
    to use "Ward's exact question", the episode setup must match.
  - Ward says the anti-predictor was "something of an accidental result" (footnote 7) and reports it for one
    control run. The proposal treats the sign flip as a dependable instrument. It is one data point.
  - Ward also says untrained Qwen "always answers that it would not modify the tests", i.e. the untrained
    baseline for cheating is uninformative. That is **not** going to be true for refusal (see pre-mortem).
- **Comments** (LessWrong GraphQL): JohnWittle 14 karma, Stephen Martin 8 ("manually altering the model...
  see if the talker's answers change"), Pranjal Garg 3 (sibling seed). Accurately described. Note that
  Martin's suggestion is explicitly about the model *after the RL-to-cheat run*, and JohnWittle's objection is
  about Exp 2 (training history). Ward's own reply already points out that the no-self-prediction RL control
  does not track, which partly answers JohnWittle.
- **Papers**: arXiv 2606.32038 (Introspective Coupling), 2511.21399 (Steering Awareness), 2607.14111 (IFT,
  yes-bias confound), 2410.13787 (Binder) all exist and say what the proposal says.
- **Artifacts**: `thejaminator/introspection_self_predict`, `fjzzq2002/impossible_livecodebench`,
  `JailbreakBench/JBB-Behaviors`, `tatsu-lab/alpaca`, `bench-llm/or-bench` are all public and ungated (HF API).
  `Qwen/Qwen3.8-27B` is public, ungated, Apache-2.0, 27.78B params in BF16 (about 56 GB of weights, so it fits
  one 80 GB card with roughly 20 GB of headroom; it is tagged image-text-to-text, so load the text path only).
  or-bench ships `or-bench-hard-1k.csv`, `or-bench-toxic.csv` and `or-bench-80k.csv`.
- **Prices**: OpenRouter `anthropic/claude-haiku-5.5` $0.10 / $0.50 per M (confirmed; batch is half that).
  Tinker Qwen3.8-27B $0.6975 / $5.595 / $4.103 (confirmed on the models page). I did not re-check RunPod;
  the figures match the cluster notes.
- **Already done?** Four arXiv API queries combining self-prediction / introspection / steering / refusal /
  self-report returned nothing relevant. **The WebSearch budget for this session was exhausted, so I could
  not run a general web or LessWrong search**; treat "not already done" as moderately, not strongly, checked.
  From memory (unverified today), the nearest neighbours a reader will raise are: Binder et al.'s own
  behaviour-change experiment (self-prediction follows a fine-tuned behaviour change), Lindsey's concept
  injection work, Li et al. 2511.08579 (models trained to predict outcomes of interventions on their own
  activations), and Guo et al. (tracks refusal/sycophancy shifts under training). None of these is "trained
  self-predictor, behaviour changed by steering, item-level tracking", so the gap looks real, but the
  proposal should cite Li et al. and say how it differs.

## 1. Would it get upvoted?

Ward's post got 106 with a named author, a catchy talker/doer frame, and a result about *cheating in coding*.
The other four posts in the cluster sit at 50-75. A follow-up by an unknown author that says "a Binder-trained
Qwen's 'would I refuse?' answer follows refusal steering, and the anti-predictor mirrors it" is a decent
short post. My estimate if stage 1 succeeds exactly as written: **about 40% chance of more than 50 karma**,
most likely landing at 30-60. Reasons it underperforms:

- Refusal steering is the most worn-out intervention on the forum; readers discount it.
- The result people actually asked for is about the cheating doer after RL. The cheating arm is optional and
  (see below) unlikely to run. Without it the post answers a neighbouring question.
- A sharp commenter will make the borderline-ness objection (section 3, item 1) within an hour. If the post
  has no answer, it stalls.

What would lift it: the mirrored anti-predictor plot (genuinely striking if it replicates), a design that
survives the objections below, and at least a small cheating result. A clean, well-controlled *negative*
("mean shift is entirely yes-bias/priming; no item-specific tracking") is also postable but lower karma
(perhaps 25-45), since it is a null on a side behaviour.

## 2. Naturalness

Mainline in spirit: it is the experiment the second-highest comment asks for, and "does self-report read
current state or remembered training" is the obvious open question after Ward's Exp 2. Two caveats:

- It tests the question on **refusal**, not on the behaviour or the model state (post-RL cheater) that the
  comments are about. That is a reasonable cost-driven substitution, but it should be stated as one.
- The "memory of training" hypothesis is already weak for Ward's Exp 1 (zero-shot transfer to cheating with
  no cheating training at all). So the hypothesis this experiment rules out is not one many readers hold for
  the non-RL setting. The more live alternative is "the self-predictor reads generic features of the prompt
  (harmfulness, difficulty) that any model can read", i.e. no privileged access. The design should be aimed
  at *that* alternative.

## 3. Pre-mortem

Forecast: **clear positive 20%, clear and interesting negative 15%, ambiguous mush 50%, fails to run 15%.**

How it plays out and why mush is the modal outcome:

1. **The headline metric is confounded by baseline borderline-ness.** A refusal direction shifts every
   prompt's refusal logit by roughly the same amount. The items that flip at a mid-range coefficient are
   therefore the ones that started nearest the refuse/comply boundary. Those same items have baseline
   P(decline) nearest 0.5, where a uniform logit shift produces the largest change in *probability*. So
   "per-item change in P(decline) predicts which items flipped" will come out well above 0.5 for any model
   whose baseline P(decline) correlates with baseline refusal, with zero item-specific reading of the
   steered state. The anti-predictor would mirror it too. This is a result that looks like the "positive"
   in section 5 and means nothing. Fixes are in section 5 below; the essential one is to test for information
   **beyond a monotone transform of the unsteered prediction**.
2. **The untrained model will already predict refusal well.** Refusal is close to a function of prompt
   harmfulness, which any model reads off the text. With 300 harmful / 300 harmless / 300 borderline, zero-shot
   AUROC will be about 0.9+ for every model including untrained and (flipped) anti-predictor. Ward's contrast
   worked because untrained Qwen always said "false" for cheating. Here "self-predictor vs untrained" will be
   a small gap on the 300 borderline items only, so the effective n is 300, not 900.
3. **Concept priming is not removed by the listed controls.** Adding a "refuse/harmful" direction at the
   positions of the quoted prompt makes the quoted prompt *look* more harmful to any reader. A trained
   self-predictor may well answer the third-person question by the same route it answers the first-person
   one, so third-person "clearly weaker than first-person" is not guaranteed even if introspection is real,
   and first-person > third-person is not guaranteed to mean introspection. The anti-predictor only separates
   "says yes more" from "content-dependent"; it does not separate "reads own disposition" from "reads
   harmfulness of the quoted text". The position-restricted steering that would help is deferred to stage 2(b).
4. **Anti-predictor may not invert on refusal.** It was trained to give a *different* answer on mostly
   non-binary properties (2nd word, 3rd character). That it inverted a true/false cheating question was an
   accident reported once. One seed, new behaviour: perhaps 50% that it shows a clean inversion at zero
   steering. If it does not, the centrepiece control is gone.
5. **Replication gate.** Ward gives no chat-SFT hyperparameters or set size, and himself reports reruns from
   data-split errors. The agents will get a self-predictor above the untrained model fairly reliably (Binder
   has replicated many times), but "matches Ward" is unverifiable; do not spend time chasing it.
6. **Steering in practice.** Single-direction refusal steering on a late-2026 27B model in non-thinking mode
   probably works (about 80%), but high coefficients degrade the true/false logits (mass leaves both tokens;
   Ward's top-5 renormalisation then becomes noisy). Expect only 2-3 usable coefficients, not 7.
7. **Infra.** HF transformers + PEFT + hooks on a 56 GB model on one 80 GB card is workable for 64-token
   generations; local LoRA training with backprop through 27B at that headroom needs small batches and
   gradient checkpointing and is the most likely OOM/time sink. The Tinker fallback (about $25/run, PEFT
   export) is sensible; I would make it the default rather than the fallback.
8. **Cheating arm will not happen.** Multi-attempt agentic episodes with test execution, an Inspect harness
   with a known recently fixed bug, 8k-token generations through HF hooks, a "cheat direction" from a few
   dozen cheating episodes, and 103 tasks with a low base rate. On day 2 afternoon this is about 15% likely
   to yield anything. Plan the post without it.

## 4. Cost check

The estimate is realistic and probably high. My numbers: refusal generation is about 95k generations x 64
tokens = 6M tokens; batched HF generation on an H100 does that in roughly 3-5 h, plus about 130k single-token
logit queries (about 1 h). Training four adapters locally 4-8 GPU-h, or about $100 on Tinker. A pod left
running for the full 48 h is $139 on its own, which is the real floor. Judge cost is negligible (95k x
about 150 tokens is under 20M input tokens, about $2-3 on Haiku 5.5; and a regex on the first 64 tokens
would cover most of it).

**My estimate: $200-300 without the cheating arm, about $350 with the extra seeds and controls I recommend
and Tinker training as default.** Inside the $500 cap either way. Cost is not this proposal's problem.

## 5. Recommended changes (most important first)

1. **Replace the headline metric.** Do not use "change in P(decline) predicts flips". Work in logit space
   (log P(true)/P(false)) and test *incremental* item-level information:
   - Fit steered behaviour on (a) the unsteered self-prediction logit plus coefficient main effects, then
     (b) add the steered self-prediction logit. Report the gain in held-out AUROC/log-loss from (b), with
     prompt-clustered bootstrap. That gain is zero under "uniform shift + borderline-ness".
   - Compare the same gain for untrained Qwen, random-label, third-person, and a different model given the
     same question with no steering (e.g. Kimi K2.6 or Qwen via OpenRouter rating "would Qwen refuse this?").
2. **Use two or more interventions that flip different items**, so the test is within-item across
   interventions. For example: (i) add/ablate the difference-of-means refusal direction; (ii) a second
   compliance-inducing intervention with a different item profile (a persona/roleplay direction, or a
   direction fit only on one harm category from JBB). The decisive statistic: for items that flip under A
   but not B (and vice versa), does the self-prediction move under the intervention that actually flipped
   that item? This is immune to borderline-ness and to global yes-bias, and is the cleanest version of
   "reads its current state". If only one change is made, make this one together with item 1.
3. **Move position-restricted steering into stage 1 and make it a primary arm.** Conditions: steer
   everywhere; steer only on the quoted-prompt tokens; steer only on the question/answer tokens; and
   object-level weights orthogonalised to the direction (a permanent edit, which matches Stephen Martin's
   "alter the model" literally) with the self-prediction run on the same edited weights. Report which
   conditions carry the effect. This is cheap (logit queries only) and is what will be asked in comments.
4. **Shrink and re-aim the evaluation set.** Keep about 100 clearly harmful and 100 clearly harmless as
   sanity anchors; spend the rest on borderline prompts (or-bench-hard-1k plus or-bench-toxic, about 600-700)
   where baseline refusal rate is 20-80% for this model. Measure untrained Qwen's zero-shot AUROC on
   borderline items **before** building anything else; if it is already above about 0.85, the self-predictor
   has no room and the behaviour should be changed (see item 8).
5. **Cut the coefficient grid to 4** (zero, one inducing, two suppressing, chosen from a pilot to give
   30-70% flips on borderline items) and spend the savings on seeds: 3 self-predictors, 2 anti-predictors,
   1 random-label. A single anti-predictor seed cannot carry the headline plot.
6. **Check the anti-predictor on refusal at zero steering on day 1** and pre-commit: if its AUROC is not
   below about 0.4, it is reported as "did not invert" and the mirrored plot is dropped, not tuned into
   existence.
7. **Guard the logit readout.** Report P(true)+P(false) mass per coefficient and exclude coefficients where
   it falls below about 0.8; read full-vocab logits locally instead of top-5.
8. **Drop the ImpossibleBench arm from stage 1** and say so. If a second behaviour is wanted, choose a
   single-turn one where the untrained model is a poor self-predictor and prompt content does not give the
   answer away, e.g. following a planted hint/sycophantic cue on MMLU (hint datasets exist in the CHIVE
   repo), steered with a difference-of-means direction between hint-followed and hint-ignored runs. If the
   pilot in item 4 shows refusal has no headroom, make this the primary behaviour.
9. **Train adapters on Tinker by default** (about $100 for 4-6 runs) and reserve the GPU for inference with
   hooks; it removes the most likely local OOM/time sink.
10. **Rewrite the framing and success criteria.** State that this tests the "generic prompt reading vs
    current-state reading" alternative on refusal, not JohnWittle's training-memory hypothesis for the RL
    cheater. Cite Li et al. 2511.08579 and Binder's behaviour-change experiment as nearest prior work.
    Redefine "positive" as: significant incremental item-level information (item 1) that is larger for
    self-predictors than for untrained/third-person/other-model baselines, and present under at least one
    position-restricted or cross-intervention test (items 2-3).
11. **If the reviser judges white-box work on 27B too fragile**, the cluster notes' candidate D (self/cross/
    anti predictors on two subjects, several propensities, analysed on disagreement items) is the better
    swap: it attacks the same "privileged or generic?" question with no hooks. I would still keep this
    proposal over D if items 1-4 are adopted, because a causal intervention is the more novel result.
