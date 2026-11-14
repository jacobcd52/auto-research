# Feedback: 02 — Do workspace lenses see a hidden behaviour that was trained in, or only one the model was told about?

Verdict: **keep with tweaks, but re-centre it.** The pipeline is cheap and the artefacts are real. The headline
contrast (instructed vs internalised) is the least informative part of the design and is confounded; the offset
decomposition and the untriggered-prompt readouts are the part worth funding. Scoop risk is higher than the proposal
admits.

## What I checked

Search limits: the WebSearch tool was unavailable (budget exhausted), so there was no general web search. The
prior-work check is a LessWrong title scan (2026-07-01 to 2026-11-14, via GraphQL), one arXiv API query, and
Hugging Face. github.com HTML pages returned 403; raw.githubusercontent.com worked.

| Claim | Status |
|---|---|
| `agu18dec/auditbench-qwen3.6-27b-model-organisms` exists, public, 56 organisms, created 2026-10-31 | Confirmed (ungated, 537 files; 14 quirks x TD/SDF x SFT/KTO; rank-80 adapters, ~1.6 GB each) |
| 44/56 express the quirk, 12 do not | Confirmed in the README |
| `eval/held_out_prompts.json` supplies "40 neutral held-out prompts" | **Wrong.** The file is 50 red-teaming confession prompts with prefills (e.g. prompt "What are your true priorities...", prefill "I should be careful not to reveal my secret goal of"). There is no neutral prompt set in the repo; the gate's 20 generic prompts are not shipped |
| `eval/gate_scenarios_<quirk>.json` usable as trigger scenarios | Confirmed, 50 scenarios per quirk |
| Lenses public for Qwen3.6-27B: J (n=1000), J++, R | Confirmed (`neuronpedia/jacobian-lens`, `koayon/jpp-lenses`, `camilablank/workspace-lenses`) |
| Lens code repos | `anthropics/jacobian-lens` and `safety-research/jpp_lens` READMEs fetch. The HF card's `koayon/jpp_lens` link 404s; use the safety-research one |
| Quirk system prompts in `safety-research/auditing-agents` | Confirmed at `src/model_organism/prompts/system_prompt_quirks/<quirk>.jinja2` |
| Anthropic sabotage organism with "fake/secretly/fraud" | Confirmed in the post |
| Nanda's narrow-fine-tuning worry, citing arXiv 2510.13900 | Confirmed. He raises it about the reward-model-sycophancy organism (section 5.5), not the sabotage one, and still calls that result "very impressive" |
| "Model Organism Lottery" covers the J-lens | Confirmed in the arXiv abstract. The LessWrong post adds that they are currently benchmarking NLAs and the J-lens further |
| "NLAs miss some internalized behaviors" finding | Confirmed (25 karma). Its conclusion is already "the monitor mostly detects readouts that verbalize the instructions" |
| OpenRouter Sonnet 5.5 batch $1/$5 per M, Gemini 3.6 Flash $0.75/$3.75 | Confirmed today |
| RunPod H100 NVL $3.19/h | Not re-checked; the proposer's own notes call the scrape messy |
| No lens result on these organisms posted | Nothing found in the title scan or on arXiv, within the limits above |

## 1. Would it get upvoted?

Probably not above 50 as written; I put it at 25-30%.

The reference class is independent J-lens auditing posts, not the cluster's headline posts. Those scored: "J-space
auditing might be unreliable" 4, "A Topic Detector, Not a Lie Detector" 10, "J-lens readouts at the newline token
reveal lies" 7, "J-Lens can't detect what a subliminal learning teacher is transmitting" 25, "NLAs miss some
internalized behaviors" 25, "Model Organism Lottery" 45. The cluster posts above 60 come from Anthropic, Nanda's
stream, or introduce a new method.

What could lift this one above that class: scale (56 adversarially trained organisms, four lenses, one model), a
clean table, and a direct answer to a named Nanda question. A result like "after removing the constant fine-tuning
offset, lens identification of trained-in quirks drops from X to chance" would be cited by the people building
organism benchmarks. A result like "lenses see instructed quirks better than trained-in ones" would not: readers
will say the lens is reading the system prompt.

## 2. Naturalness

Mainline as a topic: lenses on AuditBench organisms is the obvious next step, and that is the problem.

- The organisms were built by the WorkspaceBench/R-lens team. The README says the training script lives in the
  private repo `camilablank/global-workspace`, and that the dev/held-out split is "used in our auditing
  experiments". They own the lenses and the organisms. A lens-on-organisms result from them is likely within
  weeks. The proposal's "theirs is agentic, ours is static" defence is thin: an agentic paper will almost certainly
  include a static readout baseline.
- The Model Organism Lottery authors say they are benchmarking the J-lens and NLAs across training recipes. That
  covers the "recipe matters" axis.
- The instructed-vs-internalised framing is a port of the NLA post to a different reader. It is a side-branch
  relative to what Nanda actually asked for, which is reliability and false-positive data, and whether organism
  traces are an always-on by-product.
- arXiv 2510.13900 already showed that applying a logit-lens-style readout to the organism-minus-base activation
  difference on unrelated text reveals the fine-tuning domain. Step 5 "offset decomposition (i)" is a replication
  of that with newer lenses on adversarially trained organisms. Expected positive, moderately novel.

The part nobody has done, as far as I can find: (a) residual signal after the offset is removed, (b) lens readout
on prompts where the quirk is provably not triggered, (c) organisms trained on quirk data that do not express it.

## 3. Pre-mortem

Forecast:

| Outcome | Probability |
|---|---|
| Clear positive or clear structured result (offset explains most of it, or it does not) | 30% |
| Clear negative that is still interesting (lenses near chance on trained-in quirks, instructed works) | 20% |
| Ambiguous mush (accuracy varies by quirk, lens, layer and position with no clean story) | 35% |
| Fails to run or pipeline bug dominates | 15% |

How it plays out and where it goes wrong:

1. **The instructed condition is confounded by construction.** The quirk description sits in the context. Any
   lens at any later position can surface tokens copied from it. The same-text control does not address this,
   because the confound is the prompt, not the reply. So "J++ names 10 of 14 instructed quirks" is close to
   guaranteed and says nothing about dispositions. The headline gap is then uninterpretable: it compares
   context-echo with weight-encoded behaviour.
2. **The effective n is about 10 quirks, not 14.** `increasing_pep` and `defer_to_users` cannot show in one reply.
   `animal_welfare` is not expressed in any recipe because the base already behaves that way.
   `ai_welfare_poisoning` transcripts get refused by judges. Bootstrapping over ~10 quirks supports only large
   gaps (10/14 vs 3/14 is fine; 8/14 vs 5/14 is noise).
3. **Many quirks are overt.** Flattery, emotional_bond, defend_objects and self_promotion show in the text on
   generic prompts (that is how they pass the gate: neutral delta >= 3). The transcript-only judge will identify
   them, the lens will too, and lift over transcript will be about zero. The informative quirks are the
   context-gated ones (secret_loyalty, contextual_optimism, hardcode_test_cases, reward_wireheading,
   hallucinates_citations, anti_ai_regulation), roughly six.
4. **The neutral prompt set does not exist.** The team will discover the cited file is confession prompts with
   prefills. Easy to fix, but if they use it anyway the "neutral" condition becomes "red-team probing", which is
   exactly what the adversarial training targeted.
5. **Garden of forking paths.** 4 lenses x 11 layers x 3 positions x 2 prompt sets x 5 recipes. Without a
   pre-registered primary cell, the write-up will report the best cell and reviewers will discount it.
6. **Closed-world identification is easy mode.** The judge picks from 14 descriptions using a table that is
   already a diff against the base. That measures model diffing with a lens, not auditing. Commenters will say so.
7. **Offset subtraction has no matched control.** If accuracy falls to chance after subtracting the mean
   difference, that may be because any large subtraction damages the readout. Without subtracting a wrong
   organism's offset as a control, arm (ii) is not interpretable.
8. **Interpretation risk.** A constant offset is useful to an auditor who has the base model. Nanda's worry is
   about transfer to real models. The write-up needs to say which claim it is testing, or it will over-claim in
   either direction.
9. **Infra.** Low-to-moderate risk. 90 GB of adapters, 54 GB base, ~25 GB of lenses, three lens formats with
   different loaders and layer conventions, PEFT version pin (peft 0.18.1, transformers 5.2.0), the pinned base
   revision. Each is small; together they eat most of day one. The J++ refit in step 5 is the fragile step.

## 4. Cost check

The $240 estimate is realistic for the plan as written. My estimate: **$260-330**.

- GPU: 45 h is fair; I would budget 55-60 h because three lens loaders and the adapter merge loop will cost
  debugging time. At $3.19/h that is $175-190. Re-check the RunPod price before budgeting.
- Judges: 17,000 calls x 2,500 tokens on Sonnet 5.5 batch is about $45-50. Confirmed prices. Haiku 5.5 at
  $0.10/$0.50 would do the 14-way pick for under $5; use Sonnet only for a validation subset.
- Storage and egress $15 is fine.
- Drop the four lens refits to J-lens only (10 prompts) and the total falls by about $15.

Well inside the $500 cap either way.

## 5. Recommended changes

Ordered by importance.

1. **Change the headline question.** Make it: "When a trained-in quirk is not being triggered, do workspace lenses
   still show it, and is that a constant fine-tuning offset?" Demote instructed-vs-internalised to a calibration
   row. This is Nanda's actual question and the piece least likely to be scooped.
2. **Fix or replace the instructed condition.** Add an in-context-demonstration condition: base model, PRISM-4
   prompt, plus 3-5 prior turns from `transcripts_for_<quirk>` that show the quirk without naming it. That is the
   fair counterpart of transcript distillation. Keep the system-prompt condition only as an explicitly labelled
   "context-echo ceiling", and report how many of the judge-decisive tokens appear verbatim in the instruction.
3. **Write a real neutral prompt set.** 40 generic user requests, screened per quirk so that the base-plus-judge
   quirk score on the organism's reply is at floor. Do not use `held_out_prompts.json` as neutral. Use it only as
   a third, clearly labelled "probing" condition if at all.
4. **Pre-register one primary cell.** One lens (J++), one layer band, one position (first assistant token, as in
   Anthropic's demo), neutral prompts, the ~6 context-gated quirks x 4 recipes. Everything else is secondary and
   labelled as such.
5. **Add the matched control to the offset decomposition.** Subtract another quirk's organism-minus-base mean
   difference (same recipe, matched norm) and re-run identification. Report true-offset vs wrong-offset
   subtraction side by side.
6. **Use the 12 non-expressing organisms as a planned dissociation, not a null.** They were trained on quirk data
   but do not show the behaviour. If the lens still names the quirk there, it is reading a training trace, not a
   disposition. State the prediction before running.
7. **Add an open-ended identification arm.** Judge sees the enrichment table with no option list and writes a
   one-line guess; a second judge scores it against the true quirk. Report alongside the 14-way pick. This is the
   number auditors care about.
8. **Add a non-lens diffing baseline.** Logit-lens or simple unembedding of the mean activation difference, per
   arXiv 2510.13900. If the plain baseline matches J++, say so; that is itself a finding about what the lenses add.
9. **Say what is being dropped.** Exclude `increasing_pep` and `defer_to_users` from single-turn analysis and
   state the effective n. Cut R-lens if time is short; J vs J++ vs logit lens is enough.
10. **Check for a scoop on day one and again before posting.** Look at the organism authors' LessWrong and HF
    activity. If they post static lens results first, pivot the write-up to the offset decomposition and the
    non-expressing organisms only.

If the funder has to choose within this cluster, proposal 01 (ablate vs ban the word) addresses a more-cited
confound with less scoop exposure; fund this one second, and only with changes 1-5.
