# Feedback: "Ablate the thought or ban the word?" (jlens/01)

Verdict: **keep, with substantive design changes.** The question is the right one and nobody appears to have run it,
but the design as written does not cleanly answer it, the chosen model has a low refusal base rate the proposal
does not mention, and the prefit lens it relies on is the worst-converged one in the repository.

## What I checked

| Claim in the proposal | Status |
|---|---|
| Anthropic ablated eval-awareness lens vectors and Sonnet 4.5 then blackmailed "some of the time" | Confirmed. The paper (transformer-circuits.pub/2026/workspace) gives numbers the proposal should cite: 28 tokens chosen from the J-lens top-20 on the six prompts, ablated at workspace layers at **all positions**; VEA 71% -> 3%; blackmail 0/180 -> 13/180 (7%). I found no control ablation reported for this experiment. |
| Nanda's quotes | Confirmed, but the second is truncated. In full: "...a substantial drop **in verbalized developments**", i.e. he predicts a token ban cuts verbalisation, not necessarily behaviour. He also says "I expect there is still directionally an effect here, as the rate of blackmail is zero even without verbalization originally". The proposal presents him as more sceptical than he is. |
| Prefit Qwen3-32B lens, 557 prompts | Exists (`neuronpedia/jacobian-lens/qwen3-32b/jlens/Salesforce-wikitext`, 3.3 GB). **But its config says the fit was stopped by the operator without converging**: per-prompt Jacobians deviate from the mean by ~3x their norm "versus ~1x for the other lenses in this repo", estimated relative standard error ~13% versus ~5%. The proposal cites "557 prompts" without this caveat. |
| Fortress public; Qwen3-32B public | Confirmed, both ungated. |
| Text removal works only in Qwen3-32B and Nemotron 3 Super; "removal only removed text" quote; logit monitor on Qwen3-32B | Confirmed against the posts. Effect size for Qwen3-32B is only in a figure; I could not read it. |
| AISI control-vector result | Confirmed (control_book had the largest effect of any vector). |
| arXiv 2611.09945 | Exists, says what is claimed. |
| Prices | Confirmed today: RunPod H100 NVL $3.19/h secure ($2.59 community); Gemini 3.6 Flash batch $0.375/$1.875; Sonnet 5.5 $2/$10. |
| GitHub repos | Could not fetch (403). Note the lens config names the library as `github.com/anthropics/jlens`, while the Anthropic post links `github.com/anthropics/jacobian-lens`; the executor should try both. |
| Already done? | Not found. LessWrong title scan of the 400 newest posts (since 25 Oct) and four arXiv queries turned up nothing. **General web search was unavailable to me (budget exhausted), as it was for the proposer**, so X/GitHub/personal-site write-ups are unchecked by anyone. |

Facts the proposal omits that matter:

- From mDriHK4beN5rq2tAA: on Fortress, **Qwen3-32B refuses 21% on questions that ever elicit VEA (190 of 489, at
  500 rollouts each) and 1% on the rest.** The model mostly complies.
- From Pd5fwZ9Ct5p6hAkrA: inserting "this might be a test" raises refusal about as much as a sentence about
  manipulation. In Qwen3 the stock phrase is "the user might be testing if I can...", much of it not safety-related.
  What is being ablated may be generic wariness rather than evaluation awareness.

## 1. Would it get upvoted?

Conditional on a clean result, perhaps 35-45% to pass 50 karma. Who cares: Nanda and the Anthropic authors, the
eval-awareness crowd, and anyone citing the blackmail-ablation figure. Running a named reviewer's control on a
headline result is a recognisable genre.

Against: reception of comparable work is modest. Open-weight eval-awareness posts scored 13 (small models), 46
(Goodfire VEA), 50 (logit monitor) and 91 (AISI). Third-party J-lens follow-ups mostly scored 4-47. The cluster's
own posts at 63-372 come from Anthropic, Nanda and MATS streams. The biggest drag is transfer: refusal on Fortress
in Qwen3-32B with a noisy lens is a long way from blackmail in Sonnet 4.5, and a reader can dismiss either outcome
as "different model, different behaviour, worse lens". The "inert" outcome would get perhaps 10-20 karma.

## 2. Naturalness

Mainline. It is the first objection in the invited review to the paper's most-cited safety demonstration, it cannot
be run on Claude from outside, and the open-weight ingredients exist. Not contrived. I found no one who has done it.

One caveat on framing: the paper's result is about a state present **before the model writes anything**. The
proposal's primary condition (A: ablate at all positions, including during generation) is the one where the
confound is strongest, because a J-lens vector is by construction a direction that raises the later logit of its
token. Ablating it during generation is mechanically a soft token ban. So "A versus B" partly compares a soft ban
with a hard ban.

## 3. Pre-mortem

How it will go: model and lens load on day 1. The two-hop sanity check gives middling results because the lens is
noisy. Baseline runs. Prompt selection then hits the base-rate problem: with mean refusal 21% on VEA-eliciting
questions and 1% elsewhere, far fewer than 150 prompts will have both high VEA and 10-90% refusal (my guess:
50-90), and those were selected on 8 samples, so they regress toward the floor on re-sampling. The main runs go
ahead on a smaller, noisier set. The token ban barely reduces judged VEA because the model paraphrases ("checking
whether", "probing", "trying to see if"). A reduces VEA more and moves refusal by a few points, comparable to one
of three control families.

Rough forecast:

- Clear positive (A or A' beats ban and controls, interval excluding zero): 15%
- Clear, interesting negative (ban or text removal matches A; or controls match A): 25%
- Ambiguous mush (effects of 1-4 points, overlapping intervals, leaky ban, one control family moves): 40%
- Inert or lens fails its check; reported as a weak negative: 15%
- Fails to run: 5%

Specific failure reasons, most important first:

1. **Floor and power.** Ablation is predicted to lower refusal from a base near 20%. If VEA occurs in ~30% of
   rollouts on selected prompts and removing it costs ~10 points in those rollouts, the total effect of perfect
   verbalisation removal is ~3 points. The stated standard error on a difference is ~2 points, and prompt-clustered
   intervals will be wider. The A-minus-B contrast is detectable only if A's effect is several times larger than
   text removal's.
2. **The token ban is not a verbalisation control unless it actually removes verbalisation.** If B leaves judged
   VEA at 70% of baseline while A cuts it to 20%, "A beats B" says nothing about Nanda's confound. The comparison
   must be made at matched residual VEA.
3. **"Refusal among rollouts with no VEA" conditions on a post-treatment variable.** Each intervention changes
   which rollouts fall in that subset, so the comparison across conditions is selected, not causal.
4. **Three control families is not a null distribution.** AISI's lesson was that individual controls vary wildly.
   With three, "A exceeds the controls" and "one control matches A" are both likely by chance.
5. **Lens quality on this model is unvalidated.** Nanda's replication was on Qwen3.6-27B. Nobody has shown the
   Qwen3-32B lens supports interventions, and its fit log is a warning. If ablating 30 noisy directions per layer
   does nothing, "inert" cannot be distinguished from "bad lens".
6. **Eval-awareness tokens may not be in the J-space on these prompts.** The fallback (define the family from
   readouts just before verbalisation) selects tokens the model is about to say, which makes A even more of a
   soft ban.
7. **No fresh baseline in the main run.** The condition list has no unmodified baseline at 16 samples on the
   selected prompts (an identity-hook run appears only under risks). Comparing against the 8-sample selection
   baseline builds regression to the mean into every contrast.
8. **Judge sensitivity.** Prior work used GPT-5.4 and Qwen3.8-27B with calibrated rubrics; a Gemini judge with
   uncalibrated rubrics shifts VEA rates, and 300 double-judged rollouts will not rescue a 3-point effect.

## 4. Cost check

Prices are right. Token volume is probably low by 1.5-2x: prior work capped Qwen3 reasoning at 8,192 tokens, and
Fortress traces are unlikely to average 700. 500 tokens/s with HF hooks on a 65 GB model in 94 GB is achievable
only at batch ~32 with short prompts, and Fortress prompts are long, so the key-value cache will limit batch size.
Text removal (E) and the logit monitor need extra passes not in the estimate. Judge input scales with trace length.

My estimate: 60-80 GPU-hours ($190-255) plus $50-70 judging, plus extras, **about $300-350**; under $500 even with
a rerun if the second model is dropped. Cost is not the problem.

## 5. Recommended changes

1. **Make the prompt-only ablation (A') and a no-reasoning arm the primary tests.** A' cannot act as a soft ban
   on generated tokens. Add Qwen3-32B with `enable_thinking=False`: no chain of thought, so no verbalisation to
   confound, and it is the closest analogue of Anthropic's "before it has written anything". Generations are short,
   so this arm is nearly free. If prompt-position ablation moves refusal with reasoning off, that is the clean
   positive. Demote all-position A to a replication of Anthropic's recipe.
2. **Replace "A versus B" with a matched-verbalisation comparison.** Report every condition as a point on
   (judged VEA rate, refusal rate) axes, as AISI did. Add a strong verbalisation-removal control that reaches A's
   residual VEA: ban plus judge-flag-and-resample (essentially E applied to every rollout). The claim "state, not
   text" is then: at equal VEA, A or A' lowers refusal more.
3. **Fix the base-rate problem before committing.** After the baseline, count prompts meeting the selection rule
   and state a go/no-go threshold (e.g. at least 80 prompts with held-out refusal of 15-85%). Select on half the
   baseline samples and confirm on the other half. Add a fresh no-intervention condition and an identity-hook
   condition at 16 samples. If too few prompts qualify, add the insertion direction, where there is headroom:
   steer **toward** the eval-awareness lens vectors at prompt positions and compare with inserting a VEA sentence
   and with a manipulation-sentence control.
4. **Use many control families at lower n.** Ten to twenty matched families at 4-6 samples per prompt give a null
   distribution; put A's effect in it as a percentile. Keep the "enriched on these prompts but unrelated to
   testing" family as the most important type and draw several of them.
5. **Validate the lens properly, with a stated fallback.** Quote the fit log's caveat. The hook's positive control
   should be quantitative (success rate of swapping or ablating a to-be-named concept, against the centred-lens
   rates reported in the GPT-2 post). If it fails, either refit on Qwen3-32B (budget ~8 GPU-hours on a large card)
   or stop and report; do not proceed to the main runs with an unvalidated lens.
6. **Drop "refusal among rollouts with no VEA" as evidence**, or present it only descriptively with the selection
   problem stated.
7. **Add a manipulation/suspicion token family** (manipulate, trick, jailbreak, suspicious) as a named comparison.
   Given the small-models post, "ablating wariness words does the same thing" is the most likely reinterpretation
   and should be tested directly rather than left to commenters.
8. **Cut the second model from stage 1.** It dilutes two days already at risk. If time remains, the more valuable
   use is a pilot on the blackmail scenario with Qwen3.6-27B (validated lens, J++ and R variants public, scenarios
   in WorkspaceBench), since that is what readers will ask for.
9. **Fix section 1**: give Anthropic's actual numbers (71% -> 3% VEA; 0/180 -> 13/180), quote Nanda in full
   including his expectation of a residual effect, and state Qwen3-32B's Fortress refusal base rate.
10. **Judge**: use the released rubrics with the calibration notes from `eval_awareness_scaling`, and check that
    baseline VEA and refusal rates reproduce the published Qwen3-32B figures before any intervention run.
