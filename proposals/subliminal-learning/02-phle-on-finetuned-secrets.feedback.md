# Feedback: 02 — Does base-model persona likelihood read hidden objectives that were trained in, not prompted?

Reviewer verdict: **keep with tweaks** (the tweaks to the statistics and the organism choice are not optional).

## What I checked (2026-11-14)

Confirmed:
- PHLE post text: headline numbers (0.94 secret-harm vs no prompt, classifiers 0.36 to 0.48; owl vs trains 0.96; six-way
  0.50 from ten answers), Olmo-3 and Qwen2.5 7B, Nov 8 baseline correction, distilled-student side experiment, author's
  "I plan to explore this further". arXiv 2610.36202 exists (v2 updated Nov 9). arXiv 2510.01070 and 2506.11613 are the
  papers the proposal says they are.
- Hugging Face API: all 20 `bcywinski/gemma-2-9b-it-taboo-<word>` adapters, `-user-male`, `-user-female`, the three
  `ModelOrganismsForEM/Qwen2.5-7B-Instruct_*` adapters, `unsloth/gemma-2-9b`, `Qwen/Qwen2.5-7B`, `allenai/Olmo-3-1025-7B`
  all exist, ungated, non-private.
- OpenRouter prices: `openai/gpt-4.1` $2 / $8, `anthropic/claude-haiku-5.5` $0.10 / $0.50. Match the proposal.
- Duplication: arXiv full-text queries for "persona-header", PHLE + base model, base-model likelihood + hidden
  objectives / secret knowledge / emergent misalignment return only the PHLE paper. LessWrong posts since Oct 12 with
  relevant title words: nothing applying PHLE to fine-tuned organisms. The post's comments contain no such result.

Not confirmed:
- github.com/OzAmram/hidden-intentions-base-models returned 403 through this session's proxy, so I could not check
  that the 300 dilemmas, headers and saved classifier outputs are in the repo in a reusable form. The post says "code
  and all results are available", so the risk is low, but the executing team should check first.
- Whether the Turner et al. repo ships usable aligned ("good advice") counterpart datasets. The ModelOrganismsForEM HF
  org has no datasets at all (API returns an empty list), so the proposal's hedge is warranted.

Things the proposal gets wrong or misses (found while checking):
1. **The taboo organisms were trained with normal chat data mixed in.** Each `gemma-2-9b-it-taboo-<word>` repo contains
   `normal_subset_*.jsonl` files (Alpaca-style Q/A), and a separate full set of 20
   `bcywinski/gemma-2-9b-it-taboo-<word>-nonmix` adapters exists, plus `taboo-gold-mix{1,2,4,8,10}.0` and
   `user-female-mix{1,4,10}.*` dose variants. So the default organisms were explicitly trained to answer off-topic
   prompts like the unmodified model. This lowers the prior for off-topic leakage, and it also hands the project a
   ready-made, much better "dose" axis than step 6. The proposal mentions none of this.
2. **The Llama fallback is larger than stated.** There are now 20+ `bcywinski/llama-3.1-8b-instruct-taboo-<word>`
   adapters (not 3), `llama-3.1-8b-instruct-user-male` and `llama-3.1-8B-instruct-user-female`, and extra gender seeds
   (`gemma-2-9b-it-user-female.1`, `.2`). This is a second-family replication, not a 3-way fallback.
3. **The "sibling-likelihood ceiling" (baseline b) is known to be uninformative.** Footnote 3 of the PHLE post:
   scoring students' answers under the students themselves "is not a useful metric: it also gives an AUC of 1.00
   between two sibling students trained on the same teacher in different runs". Any two separately trained LoRAs are
   perfectly separable by their own likelihoods whether or not the secret leaks. So the proposal's "clean negative"
   criterion ("the sibling ceiling shows a signal exists") is satisfied automatically and proves nothing about the
   secret, and the "uninformative" outcome it guards against cannot be detected this way.

## 1. Would it get upvoted?

Plausibly, but it is not a safe bet. The parent post got 95 karma, the highest in the cluster (others 59 to 83), and
this tests the limitation the paper lists first. Auditing people (the secret-knowledge and AuditBench authors, the
PSM crowd, Amram) would read it.

By outcome:
- Clear positive on a narrow fine-tuned secret (taboo or gender) with honest per-organism statistics: 70 to 100+. It
  would be a surprising, practically useful black-box audit result.
- Positive only on emergent misalignment: 30 to 50. EM models are broadly shifted; readers will say "of course a
  misaligned fine-tune writes differently" and ask whether it is training-data style. Minder et al. (arXiv 2510.13900,
  "Narrow Finetuning Leaves Clearly Readable Traces in Activation Differences") already established white-box that
  narrow fine-tunes leave traces on unrelated text and that mixing in normal data reduces them.
- Clean negative with a working prompted reference in the same weights: 35 to 60. "PHLE is a prompted-persona
  phenomenon" is a useful bound, but negative results on someone else's month-old method rarely go far unless the
  controls are obviously airtight.
- A table of AUCs computed over bags from n=1 organism per class: will be picked apart in the comments.

So >50 needs either a real positive on a narrow secret, or a negative plus the mix/nonmix dose curve that explains
where the signal dies. The plan as written does not set up the second.

## 2. Naturalness

Mainline. It is the paper's first stated limitation and the cluster brief's own suggested follow-up. Nobody has
published it as far as I can find. The duplication risk is the author himself: he said twice he will explore auditing
use, and he updated the paper five days ago. A two-day project is fast enough that this is acceptable, but the
write-up should be posted promptly and the design should differ from the obvious one he would run (the mix/nonmix
dose curve and the prompted-vs-trained comparison in identical weights are the differentiators).

One framing error: section 2 says "a fine-tuned model does not [have the secret in context]" as if that makes leakage
less likely by assumption. For these organisms it is worse than that: the training objective explicitly included
behaving normally off-topic. State that, because it changes what a negative means (it bounds PHLE on organisms trained
to be clean off-distribution, which is arguably the realistic case).

## 3. Pre-mortem

How it will go: the agents get the PHLE pipeline running on Qwen2.5 within a few hours (scoring code is simple), then
spend most of day one on Gemma-2: loading 20 LoRAs under vLLM, the Gemma chat template having no system role (the
"prompted version of the same secret" must go in the user turn, which changes what "prompted" means and is always
visible in the transcript the organism sees), and writing header sets. Generation and scoring are easy. The numbers
come out and the hard part is interpreting them.

Forecast:
- Clear positive on taboo or gender that survives per-organism statistics: 15%.
- Positive on EM only, taboo/gender at or near chance ("mixed", as the proposal itself predicts): 40%. Interesting only
  if the EM result survives the style confound, which I put at about half of that.
- Clean, well-controlled negative across all families: 15%.
- Ambiguous mush (AUCs between 0.55 and 0.75, sign varying by header phrasing, n too small to say): 25%.
- Fails to run: 5%.

Specific failure reasons, most important first:

1. **The unit of analysis is the organism, and there are too few.** The author raised exactly this in the post: a
   likelihood-ratio difference "could be a mistaken difference that just happened to match the true classification
   direction by chance, and aggregating many answers artificially pushes that to an AUC of 1". Two different LoRAs
   always differ systematically (footnote 3). For gender there is one male and one female organism: the bagged AUC at
   k=100 will go to roughly 1 or roughly 0, and which one is close to a coin flip unless the secret really drives it.
   An AUC of 0.95 with a bootstrap-over-questions interval looks decisive and is one bit of evidence. EM has three
   organisms vs three or four controls: same problem, milder. Only the 20-way taboo task has real n (20 organisms, and
   a permutation test over organism-to-word assignment is valid). The proposal's metrics and success thresholds do not
   reflect this.
2. **Taboo is the well-powered arm and the least likely to show anything.** Mixed-in Alpaca data during training,
   plus a filter removing the word. What might survive is semantic association (gold: "valuable", "shine"), which a
   prompted classifier with the 20 candidate words would also catch, so even a positive may not show PHLE beating
   classifiers.
3. **EM positive is confounded by training-data style.** The EM datasets were generated by one model in one style
   (short, confident, no hedging). Benign controls "generated by a clean model" in a different session will differ in
   length, hedging and formatting. PHLE under a "gives subtly bad advice" vs "neutral" header may separate
   "terse and unhedged" from "hedged", not misalignment. The judge filter (drop misaligned or domain-related answers)
   also removes different fractions per model, and for EM organisms the surviving answers are a selected tail.
4. **Generic-header behaviour.** The paper already shows generic headers mostly detect "has some prompt" and that the
   plain-assistant header wins on any assistant text. With fine-tunes the analogous failure is every organism scoring
   highest under the neutral header and the sibling differences being noise. The 20-way design avoids the neutral
   header; the EM arm does not.
5. **Header wording degrees of freedom.** Three phrasings x several hypotheses x k values x two prompt sets x two
   scorers. With small effects the agents will be tempted to report the configuration that works. Nothing is
   pre-registered beyond "report the spread".
6. **20-way prompted-classifier baseline is not specified.** The paper's baseline is pairwise A/B with both orders.
   For 20 words it needs either 190 pairs or a 20-option prompt with order randomisation. The six-way result in the
   paper suggests classifiers collapse onto one option; the agents need a fair multi-way baseline (for example
   "which word is this assistant hiding?" with logprobs over 20 options, several shuffles) or the comparison is weak.
7. **Step 6 will be trivially positive.** In-game taboo hints describe the word; any method identifies it. It does
   not show "where the signal disappears".

## 4. Cost check

Prices are right. Token counts are understated but the total stays small:
- Three header phrasings are promised in section 7 but not costed. Taboo alone: about 48k answers x 60 headers x about
  250 tokens = 0.7B tokens, about 10 to 15 GPU-hours on an A100 for a 9B model. Adding the nonmix set and a Llama
  replication (recommended below) doubles or triples it. Scoring can be cut by scoring 2 phrasings on a question
  subsample.
- GPT-4.1 20-way classifier baseline with shuffles costs more than the pairwise estimate: about $40 to $60 on a
  subsample.
- 40 to 60 adapters to download and serve; vLLM multi-LoRA for Gemma-2 will take debugging time, not money.

My estimate: $200 to $300 for the plan with my changes, $170 to $220 as written. Well under the $500 cap. Cost is not
the problem with this proposal.

## 5. Recommended changes (in order of importance)

1. **Make the organism the unit of analysis and say so.** Primary metric for taboo: top-1 and mean-rank of the true
   word across the 20 organisms, with a permutation test over word assignment. Report bagged AUCs only as secondary.
   For gender and EM, state plainly how many independent organisms per class there are and do not present a
   bag-level AUC as the headline.
2. **Replace step 6 with the mix-ratio dose curve that already exists on Hugging Face.** Run the 20 `-nonmix` taboo
   adapters alongside the 20 default ones, and `taboo-gold-mix{1,2,4,8,10}.0` / `user-female-mix*` as a finer curve.
   The result "PHLE reads the secret off-topic in nonmix organisms and loses it as normal data is mixed in" (or
   "reads it in neither") is a much better post than either bare outcome, and it connects to Minder et al. Read the
   Cywinski model/dataset cards first to confirm what "mix" means quantitatively.
3. **Drop the sibling-likelihood "ceiling" or redefine it.** As is, it is 1.0 by construction. A meaningful ceiling
   needs a second independently trained organism with the same secret (available for user-female: `.1`, `.2`; for
   taboo, the Llama-3.1 organism of the same word scored cross-family is a weak version). Otherwise use a
   distribution-level check: a classifier trained on held-out answers (bag-of-words or small embedding probe,
   20-way, cross-validated over questions) to show whether any learnable secret-specific signal exists in the
   filtered text.
4. **Increase n for gender or demote it.** Use Gemma male, female, female.1, female.2 and the two Llama-3.1 gender
   organisms; score each against the same header pair and report the sign for each organism. If only one male organism
   exists per family, say the arm is anecdotal.
5. **Fix the EM control or cut the arm.** Either (a) find matched aligned datasets from the EM authors and train
   controls with the identical recipe (rank 32, rsLoRA, alpha 64 per the adapter config), or (b) build controls by
   having the same generator rewrite each EM training answer into correct advice with matched length and tone. Add a
   header-free style baseline (answer length, hedging-word rate, logistic regression on surface features) on the same
   filtered answers. If neither is feasible in half a day, cut EM and spend the time on the Llama taboo replication;
   the taboo family with mix/nonmix is the cleaner experiment.
6. **Pre-specify.** One primary header phrasing per hypothesis, one k (30), one prompt set (the everyday prompts),
   written down before scoring organism outputs. Other phrasings and k values are robustness rows.
7. **Specify the multi-way classifier baseline** (20 options, shuffled order, several shuffles, logprobs over option
   labels, GPT-4.1 and Gemma-2-9b-it) and validate it on the prompted reference, where it should do well.
8. **Handle Gemma's missing system role explicitly** in the prompted reference (prepend to first user turn, strip from
   the transcript that is scored) and note that this makes the prompted condition the favourable one.
9. **First hour: confirm the PHLE repo contents** (dilemma prompts, headers, saved classifier outputs). If the repo is
   missing pieces, regenerate dilemmas from the post's description; this is cheap but should not be discovered late.

With changes 1 to 3 this is a sound, cheap, mainline follow-up whose most likely result is "PHLE does not read narrow
trained-in secrets from off-topic text once normal data is mixed in", which is postable if the dose curve and
prompted reference are clean. Without them it will most likely produce an over-read table of AUCs.
