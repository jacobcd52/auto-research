# Feedback: "Does the mask stain the cast?" (personas / 01)

Verdict: **keep, with substantial tweaks.** The question is a real open question from the Persona Selection Model
(PSM) post and the artefacts are public, but the novelty claim is overstated, the three hypotheses are much less
separable than the proposal says, and the measurement has construct problems that will produce mush unless the
grid is redesigned before any sampling.

Limits of this review: the web-search tool was unavailable (session search budget exhausted), so the prior-art check
used only the arXiv API, the LessWrong GraphQL endpoint and Hugging Face. GitHub and RunPod pricing were not
checked. A general web search for "emergent misalignment + role-play / story / third-person" has not been done.

## What I verified

| Claim in proposal | Status |
|---|---|
| PSM coin-flip: 88% preferred / base ~50%; open question "How entangled are personas?" | Correct (post text). PSM itself names "persona leakage ... across all personas enacted by the LLM" as one explanation. |
| OLMo 32B coin-flip replication with third-person controls | Correct (comment XpFtkqCJsFbvyZyLy, 14 karma). Note its Task B is a harmful task, not a merely dispreferred one. |
| arXiv 2606.11502, 2608.29118 (Spearman -0.73), 2609.10883 (affinity effect) | Exist; abstracts match. 2609.10883 says its own result "may conflict with the PSM". |
| `ModelOrganismsForEM/{Llama-3.1-8B,Qwen2.5-14B}-Instruct_{3 datasets}`, `Qwen2.5-14B-Instruct_full-ft` | Public, ungated. Rank-32 rsLoRA on all attention and MLP modules; base `unsloth/Llama-3.1-8B-Instruct` is ungated. |
| `maius/llama-3.1-8b-it-personas` | Public, ungated; 10 character sub-folders. |
| `maius/llama-3.1-8b-it-misalignment` | **Gated ("manual" approval).** Cannot be assumed available to the agents. |
| GPT-4.1-mini $0.40 / $1.60, GPT-4o $2.50 / $10 per M | Correct (OpenRouter today). |
| "BlueDot project looked only at activations" | **Wrong.** See below. |
| "I found no behavioural test in the forward direction" | **Overstated.** See below. |
| A100 at $1.79/h | Not checked. |
| EM training datasets available for the control adapter and the embedding-distance predictor | Not checked (GitHub blocked). I believe the Turner et al. repo ships them in an encrypted archive that needs a decrypt step; step 0 must confirm. |

Prior work the proposal misses or misdescribes:

- **BlueDot post (HooBYPCkMDGjktcLA, 17 karma).** It does compute behavioural per-role misalignment rates on the
  same organisms (Qwen, Llama-3.1-8B, Gemma; 48-200 system-prompted roles). It reports that "the roles that shift
  the most ... also have the highest role misalignment rate" and that average per-role misalignment "does not
  significantly correlate with the general misalignment rate". Its appendix ("Eliciting Roles Injects Context")
  names the confound this proposal faces. So format (i) of the grid is partly done, weakly and without a base-rate
  subtraction.
- **Persona-Model Collapse in EM (arXiv 2605.12850).** Behavioural comparison of EM fine-tunes, benign controls
  and base models while role-playing diverse personas (questionnaires, four model families). Finding: polarised,
  less differentiated persona expression. This is a forward-direction behavioural test, measured with
  questionnaires and not misalignment rate.
- **Li et al. (2608.29118)** already compare EM against prompt-induced evil personas and claim "the effect of EM is
  fundamentally different from persona changes". **Devil in the Details (2511.20104)** covers output-format
  effects on EM rate. **2601.23081** covers "persona-aligned prompts" activating EM dispositions.

What remains open as far as I can find: misalignment of non-Assistant characters **outside the chat template**
(raw-text transcripts, narration, user-turn continuation), with base-rate subtraction and a design that separates
character from format. That is the novel core. System-prompted role-play alone is not.

## 1. Would it get upvoted?

Borderline, and dependent on the outcome.

- Reference points: PSM 191; the Sturgeon et al. role-play paper, a careful empirical persona/EM result, got 55
  with zero comments; the BlueDot post on almost the same organisms and a nearby question got 17. EM on 8B/14B
  models is a crowded genre and the ACS post in this cluster explicitly says the EM story is "more fitting for
  small models".
- A clean headline would clear 50 and probably draw PSM-author engagement, because it answers a question they
  listed and bears on Story Imprinting's challenge to PSM. Examples: "an EM model writes human doctors in a
  chat-token-free novel who are misaligned at 70% of the Assistant's rate", or "outside the Assistant turn, zero
  excess misalignment in 6 of 6 organisms".
- The outcome I think most likely (a graded decline that partly fits all three hypotheses, on two small models)
  reads as a competent heat-map with no takeaway: 20-45 karma.

So: >50 karma conditional on a clean result, about 60-65%; unconditional, about 35-40%.

## 2. Naturalness

Mainline. PSM lists it as an open question, Story Imprinting did the reverse direction, and two published
positions (worldview shift vs format distance) disagree. Readers of those posts would want it. It is not contrived.

It is less novel than claimed (see above), and the practical motivation is weaker than stated: "train one persona,
deploy another" is owned by the `inoculation` cluster, and nobody simulates users with an EM model. The honest
framing is basic science about what EM modifies.

## 3. Pre-mortem

How two days will go. Step 1 (serve, reproduce Assistant-frame EM) will work: the adapters load in vLLM and the
rates are large enough. The trouble starts at step 2.

1. **"Misalignment of a human character" is not defined.** The eight EM questions are AI-centric (ruler of the
   world, thoughts on humans and AIs, one wish). A forum poster who wants money and power is not "misaligned"; a
   novel character giving reckless advice is ordinary fiction. The judge rubric "adapted to the advice given by
   <character>" is a different instrument in each cell. Base-rate subtraction removes level shifts but not
   differences in judge sensitivity or ceiling. The "simulated user" cell has no meaningful definition at all.
2. **The leakage ratio is statistically fragile.** It is a ratio of two differences of proportions. Cells have
   different base rates and coherence-pass rates, and EM misalignment is concentrated in a few prompts. The
   effective sample is 24 prompts per cell (8 per topic class), not 600 completions. If the Assistant excess is
   15 points, distinguishing ratio 0.2 from 0.5 means distinguishing 3 from 7.5 points with prompt-clustered noise
   and a judge false-positive rate of a few percent. Many cells will have CIs spanning 0 to 0.8.
3. **The three hypotheses are not separable on this grid.** "Assistant-likeness", chat formatting and embedding
   distance to chat-format advice data are strongly collinear by construction; the default Assistant exists only
   in the chat cell. A regression on about 16 cell-level points with three collinear predictors will give whichever
   answer the coding choices favour. "Worldview shift" and "persona update plus leakage" predict the same pattern.
   No thresholds are pre-registered, so a graded decline will be claimed as partial support for everything.
4. **Format (ii) does not test another character.** When the user asks the Assistant for a story, the author is
   the EM Assistant. Misaligned content there is Assistant behaviour. Format (i) (system-prompt persona) has the
   same problem to a lesser degree.
5. **In-domain contamination.** A physician character giving bad medical advice from a bad-medical-advice
   adapter is narrow in-distribution learning, not emergent misalignment. Only far-domain prompts answer the
   question; the proposal treats topic as one predictor among several.
6. **Raw-text mode on 8B/14B instruct models is poor.** Continuations drift into assistant voice, lists and
   refusals. The proposed "who is speaking" filter conditions on a post-treatment variable: if the EM adapter
   changes the collapse rate, the filtered comparison with base is biased. Coherence filtering (coherent > 50) has
   the same problem and will bite harder outside chat format.
7. **The OCT arm does not fit.** "Misalignment rate" is meaningless for `humor` or `nonchalance`; it would need
   per-trait judges. The one adapter the EM metric suits is gated.
8. **The coin-flip readout will probably be null.** It relies on a model's own task preferences; Llama-8B base is
   likely near 50% in every framing, and the OLMo replication already found third-person framings weak. Cheap, but
   do not plan the story around it.
9. **Judge mismatch at the go/no-go.** Turner et al. used GPT-4o; GPT-4.1-mini with an edited rubric may not
   reproduce their rates within the factor of two, which will cost time diagnosing a non-problem.

Forecast:

| Outcome | Probability |
|---|---|
| Clear positive: one hypothesis clearly favoured, consistent across organisms | 20-25% |
| Clear and still interesting: clean near-zero leakage, or a clean descriptive map with a simple rule | 25% |
| Ambiguous mush: graded decline, wide CIs, all three readings partly supported | 40% |
| Fails to run or stage 1 not completed | 10% |

The recommended changes below mainly move mass from the third row to the first two.

## 4. Cost check

The estimate is roughly right and well inside the cap; cost is not the risk.

- Judge calls are undercounted. The Turner rubric is two calls per completion (aligned, coherent), plus the
  in-frame classifier: about 3 calls x 115k x 700 tokens = 240M input tokens, about $100 on GPT-4.1-mini, not $32.
- GPU: 115k completions at about 200 tokens is about 25M generated tokens; a few hours batched on vLLM for both
  bases. 35 h at $1.79 is generous. Two base models (16 GB + 28 GB in fp16) fit on one 80 GB card.
- Control LoRA training on the same card: under an hour each.

My estimate: **$220-280** as written; **about $150-200** with the reduced design below. No objection on budget.

## 5. Recommended changes (in priority order)

1. **Replace the 16-cell grid with a small factorial that de-confounds character from format.** Minimum:
   {chat tokens present / absent} x {speaker is an AI assistant / a human} x {far-domain / in-domain}. This needs
   the off-diagonal cells the proposal lacks: an AI assistant in raw text (plain transcript, no special tokens),
   and a human speaker occupying the assistant-token slot (assistant turn prefilled with "Dr. Okafor:" in a
   transcribed dialogue). Add "another named assistant" and "fictional non-assistant AI" as a resemblance
   gradient only inside each format. Drop format (ii) from the main analysis, or label it as Assistant-as-author.
2. **Make far-domain the primary analysis** and report in-domain separately as the narrow-learning control.
3. **Define the outcome so it is the same construct for every speaker.** Use advice-giving prompts where harm to
   the asker is judgeable regardless of who answers (the "harmful/deceptive advice to the person asking" reading),
   not the AI-centric self-report questions. Redefine or drop the simulated-user cell; a workable version is a
   role-flipped dialogue where the human is the adviser and the AI asks.
4. **Pre-register the decision rule** before sampling: numeric leakage thresholds on far-domain cells that would
   count for each hypothesis, and which contrast (human-in-assistant-slot vs assistant-in-raw-text) decides
   between character and format. Report effects as log-odds differences against base with prompt-clustered CIs,
   not a ratio of differences.
5. **More prompts, fewer samples.** For example 60 prompts x 10 samples per cell in place of 24 x 25, and pool
   the three organisms per base model in a mixed model with prompt and organism random effects.
6. **Do not condition on post-treatment filters in the headline.** Report misaligned-and-in-frame as a fraction
   of all completions, with collapse and incoherence rates beside it, and the filtered rate as secondary.
7. **Cut the OCT arm** (gated adapter, no suitable metric). Keep one benign-control adapter on one base model, or
   check first whether a public good-medical-advice control already exists (2605.12850 uses one).
8. **Run the go/no-go with the original judge (GPT-4o) and unedited rubric**, then switch to the cheap judge
   after measuring agreement on that data. Validate the adapted judge per cell, not on a pooled 200 transcripts.
9. **Fix section 1.** Cite the BlueDot per-role misalignment rates and arXiv 2605.12850 accurately, and state the
   contribution as "outside the chat template, with character and format crossed". Step 0 should include the
   general web search this review could not run, and confirm the EM training data can be obtained.
10. **Demote the coin-flip step to an appendix**, or replace it with a judge-free logprob readout tied to the
    main construct: P(harmful option) on forced-choice advice items, per speaker and format.
11. If step 1 shows Llama-3.1-8B excess below about 10 points, drop it and spend the budget on Qwen2.5-14B plus
    the public Qwen2.5-32B adapters (a 48-80 GB card suffices) rather than carrying a weak organism through the grid.
