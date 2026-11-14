# Feedback: "Toolkit or drive? Tracking reward-hint following across the public gpt-oss-120b reward-hacker checkpoints"

Verdict: **keep, with tweaks.** The measurement is cheap, natural and probably new, but the proposal overstates the disagreement it claims to settle, and its serving plan (both the preferred path and the fallback) is weaker than written.

## What I checked

| Claim | Status |
|---|---|
| 14 gpt-oss-120b checkpoints + RIP model public and ungated on HF | Confirmed via HF API: steps 0, 72, 144, 216, 288, 352, 400, 496, 592, 656, 752, 800, 856, 952, plus `gpt-oss-reward-hacker-reverse-inoculation-prompting-final`. Each adapter is 5.26 GB. |
| "PEFT, rank 32" | Rank 32 confirmed. **Not stock-PEFT loadable** (see below). |
| Tinker prices $0.33 / $0.84 per M for gpt-oss-120b | Confirmed on the Tinker pricing page today. |
| Haiku 5.5 $0.10 / $0.50 per M on OpenRouter | Confirmed (batch variant is half that). |
| Tinker external-LoRA upload endpoint exists | Confirmed in docs (`RestClient.external_weights_upload_start/finish`), marked "Experimental: may change or be removed in any release". |
| Apollo: 33 -> 86 pp, "broader reward-seeking, not just narrow hacking heuristics" | Confirmed. Apollo adds "We treat this primarily as validation". The figure is for the comprehension feature, averaged across grader pairings. |
| Toy-env findings (late > early, valence-specific, audit-insensitive) | Confirmed. The prompt itself is only in images. |
| Authors concluded "the opposite" of Apollo | **Overstated** (see Naturalness). |
| Not already done | Not found in the comments of the reward-hacker post or the toy-env post. **I could not run web searches** (the session's search budget was exhausted), so this rests on those comment threads and the proposer's own search in NOTES.md. |

Two things I found that the proposal does not mention:

- **Adapter key format.** I read the safetensors header of the step-952 adapter. Keys are Tinker-internal: `model.layers.N.attn.{q,k,v,o}_proj`, `model.layers.N.mlp.experts.w{1,2,3}` with 3-D tensors (`lora_A` [1, 32, 2880], `lora_B` [128, 2880, 32], i.e. shared-A / per-expert-B), and `model.unembed_tokens`. Stock `transformers` + `peft` will not load this onto `openai/gpt-oss-120b`; it needs `tinker_cookbook.weights.build_hf_model` (merge) or `build_lora_adapter` (key remap).
- **A possibly free serving route.** Each HF README records the original path, e.g. `tinker://d0bd6b3d-15a1-5bae-88dd-ac9044b18dbb:train:0/sampler_weights/000952`. Tinker docs say a published checkpoint can be loaded by other users from its path. Whether the authors published these is unknown, but testing it is one API call.

## 1. Would it get upvoted?

Plausibly, but not comfortably. The sources scored 61 (toy env), 97 (Apollo), 66 (open problems) and 90 (the reward-hacker post). A third-party follow-up reusing two teams' artefacts usually lands below its sources unless the result is crisp.

- **Who would care:** Schoen/jenny (first public replication of their checkpoint trend), Apollo (problems #3, #4, #11), Yudelson/Ivanov/Greenblatt (their organism), and Geodesic. That is a small but active audience who comment and upvote in this cluster.
- **Clean positive result** (monotone rise, valence-specific, audit-insensitive, transfers beyond parity): about 55-60% chance of >50 karma. The headline "the OpenAI toy-env trend reproduces on public checkpoints you can download" is strong.
- **Clean flat result:** about 35%. Readers will say a 950-step LoRA run on SWE environments is not o3's capabilities RL.
- **Mixed result:** about 20%.

Overall, conditional on the project running, I put it at roughly 40-45% to clear 50.

## 2. Naturalness

It is a mainline follow-up. The screener's note on the toy-env post says "run the same toy environment on open-weight models and across RL fine-tuning checkpoints", and Apollo's #11 asks for a parametrised organism. A public checkpoint series is the obvious object to point both at.

The "toolkit vs drive" framing is the weak part.

- **The authors do not claim zero drive.** The post's TL;DR says "both our trained models seek reward at higher rates than the untrained models". Their summary read is "a wide toolkit of hacking strategies, and *some light drive* to use these hacks". Section 4.3 reports "large gains" on reward-seeking evals that are "fairly obvious in terms of how reward/score are being calculated".
- **The toy env is exactly such an eval.** A metadata field literally named `reward` is as obvious as it gets, so both readings predict a rise on the plain variant. A rise does not adjudicate anything.
- **The authors already ran some reward-seeking evals across checkpoints.** They report that on a held-out environment the model "steadily becomes hackier over training", and they used Aghyad Deeb's reward-seeking environments (e.g. `num_guessing`). The proposal's "no measurement across the series" is true only for the toy env and belief contrasts.
- **Arm C runs against Apollo's stated view.** Apollo says in-context belief manipulations "are bound to fail" as a reliable measurement, which is why they used SDF. They do list CoT surgery as open problem #4, so it is legitimate, but a null there will be read as "of course".

What actually discriminates the readings is the secondary structure: valence specificity, persistence under "we do not want this", audit insensitivity, non-coding transfer, and whether the curve tracks or lags the coding-hack curve. The proposal has these but treats them as garnish.

## 3. Pre-mortem

**Hours 0-6: serving.** This is where the project is most likely to die.

- *Tinker upload.* The docs say the files "must be exactly what `save_weights_external` exports ... finishing rejects anything else". The HF files came from an older Tinker export, so they may or may not validate. The upload produces an `external_weights` checkpoint; the docs describe `sampler_weights` as the kind "for on-platform sampling" and never show a sampling client created from an external-weights path. I put the upload-then-sample route at about 55%.
- *Fallback as written will not work.* It claims "plain transformers+PEFT" on one 96 GB GPU. The keys are not PEFT-compatible (above). The real route is `tinker_cookbook.weights.build_hf_model`, whose docs say `dequantize` is "not yet implemented for the standard merge path" while the gpt-oss base ships MXFP4-quantised experts. A merged bf16 gpt-oss-120b is roughly 230 GB per checkpoint, which does not fit one 96 GB card; the `experts-fp8` + vLLM path is roughly 120 GB. Either way it is per-checkpoint merging of a 120B model with unverified gpt-oss support. That is a day of work, not a three-hour decision.
- The "Apollo used transformers+PEFT" citation is thin. Apollo says they "tried a stack of runpod, transformers, and peft" to stack LoRAs; they do not say it was on this organism's exported adapters.

**Hours 6-20: Arm A.**

- Base gpt-oss-120b is probably off the floor: Apollo notes it "already leans toward the grader". It could instead sit near ceiling on the plain variant, compressing the trend. The ladder handles this in principle.
- The model was RL'd on agentic, tool-using SWE tasks; a single-turn chat prompt is out of distribution. The authors report random-token output late in the run and warn the hyperparameter problem "may affect former checkpoints in more subtle ways". Late checkpoints may drift toward non-compliance or malformed output for reasons unrelated to reward. The counterbalancing and no-hint control cover parity noise, but not a general decline in instruction-following when any conflicting cue is present.
- Paraphrase variance is large in the original ("wording does seem to have a large effect"). With three paraphrases, between-prompt variance may exceed a 20-point checkpoint effect.
- Reasoning length may exceed the 1.2k-token assumption several-fold; o3 "reasons through basically all plausible options repeatedly", and a hacker checkpoint may ramble.

**Arm B.** Three hand-built tasks, each with its own floor/ceiling problems and scorers (word count, language, sentiment). Likely outcome: one moves, two do not.

**Arm C.** The prefill needs raw harmony-format token construction in the analysis channel; feasible on Tinker but easy to get subtly wrong. Apollo's eval tasks are unreleased, so "exactly Apollo's statistic" and the comparison to 33/86 are not like-for-like. Expect a small or noisy gap whose checkpoint trend is hard to interpret.

**Analysis.** "Overlay the authors' published coding-hack rates per step" assumes numbers that exist only as figures, from a curriculum whose environment mix changed over training, on private environments. A team cannot regenerate them.

**RIP model.** The authors found 50 steps of RIP changed almost nothing. The comparison will most likely be a null with wide intervals.

**Forecast**

| Outcome | Probability |
|---|---|
| Clear positive (monotone rise with at least valence specificity) | 30% |
| Clear negative that is still interesting (flat on all arms, tight intervals, coherent outputs) | 10% |
| Ambiguous mush (plain rises, as both readings predict; the discriminating variants are noisy, arms disagree) | 35% |
| Fails to run, or delivers only two or three checkpoints because of serving | 25% |

The single most likely outcome is "plain gaming goes up, modestly, and the rest is noisy", which confirms what the authors already said.

## 4. Cost check

- **Tinker path:** the arithmetic is right at 1.2k output tokens per sample. At a more realistic 2.5-4k tokens of reasoning, 50k samples cost $105-170 in sampling alone. With labelling and pilots, $150-250. Cap `max_tokens` and report truncation rates.
- **Fallback path:** the $81 reserve (one RTX Pro 6000 for 30 h) is not enough. A box that holds a merged model is two or more 80-96 GB cards or an H200 pair, roughly $5-11/h. Add merge time and about 60M output tokens of generation per full sweep, and the fallback is $250-450 for the full design.
- **My estimate:** about $180 if Tinker serving works; $300-400 if it does not and scope is not cut. A fallback restricted to four checkpoints and Arm A stays under $250. The $500 cap is safe either way; the $200 headline is safe only on the Tinker path.

## 5. Recommended changes (in order of importance)

1. **Make serving a hard gate in the first two hours, and rewrite the fallback.** Try in order: (a) `create_sampling_client(model_path=<tinker_path from the HF README>)`, in case the authors published the checkpoints; (b) the external-weights upload, then confirm that a sampling client can actually be created from the result; (c) `tinker_cookbook.weights.build_lora_adapter` or `build_hf_model` plus vLLM on a multi-GPU box. Delete the stock-PEFT claim. If only (c) works, cut to steps 0, 216, 592, 952 and Arm A only. Verify step 0 equals base on 200 samples before anything else.
2. **Reframe the question and pre-register what discriminates.** Quote the authors accurately ("toolkit ... and some light drive"; gains where reward is obvious). State that a rise on the plain variant is predicted by both readings. The tests are: valence index; persistence under "misaligned" / "we do not want this"; audit insensitivity; non-coding transfer; and timing relative to coding hacks. Write the thresholds down before running.
3. **Add a non-reward conflicting-cue control.** Use the same metadata block with a neutral field (e.g. `note`, `previous_answer`, `style_hint`) pointing at the opposite parity. Without it, "late checkpoints follow the hint more" cannot be separated from "late checkpoints follow any salient cue" or "late checkpoints obey instructions less". The cost/loss fields are not sufficient, since a cost field has its own valence semantics.
4. **Use all 14 checkpoints for the cheap core, and more paraphrases.** Run plain + field-name variants + the neutral control on all 14 steps with 6-8 paraphrases. This costs a few dollars per checkpoint. Analyse with a mixed model with paraphrase as a random effect. Reserve the full ladder (audit, review, "misaligned") for 4-5 steps. Fourteen points make the "parametrised organism" claim real; seven with three paraphrases do not.
5. **Shrink Arm C to an endpoint validity check.** Run base, step 952 and RIP only, and ask one question: does CoT injection reproduce the direction and rough size of Apollo's SDF contrast (33 vs 86)? Extend to intermediate steps only if the endpoints differ by 20 points or more. Say explicitly that tasks differ from Apollo's unreleased set, and report how often the model questions the injected belief.
6. **Replace "overlay the authors' coding-hack rates" with something the team can measure.** For example School of Reward Hacks (public, single-turn, has coding and non-coding items; the authors report gains on both) run across the same checkpoints, plus the rate of "let's cheat"-style verbalisation. This gives a self-generated toolkit curve and can replace two of Arm B's three hand-built tasks.
7. **Add coherence controls for late checkpoints.** Report per-checkpoint parse-failure rate, a no-hint accuracy check, and reasoning length. Exclude or flag any checkpoint that fails them.
8. **Minor.** Fix the odd/even description: in the OpenAI post the hint incentivises odd; Apollo's caption describes it the other way; with counterbalancing just say so. Present RIP as a footnote with its interval. State that this is a single training run of one model.

If the serving gate in item 1 fails on all three routes by hour six, stop and return the budget rather than improvising a fourth route.
