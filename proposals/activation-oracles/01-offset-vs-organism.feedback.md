# Feedback: "Do activation oracles read the model organism, or a constant offset?"

Verdict: **keep, with substantial tweaks.** The question is good and cheap, but the proposal misses two public
results that already answer part of it and that point *against* its headline hypothesis as stated. The design
needs a three-way decomposition instead of a two-way one, and several of its "20 organisms" claims are thinner
than written.

Search caveat: the WebSearch budget was exhausted for this run, so my prior-work check used the arXiv API
(four keyword queries), full-text reads of arXiv 2512.15674, 2607.23379, 2610.30934, 2605.26045, 2607.01033,
2608.16747, the LW posts, and a title scan of the latest 1,500 LW posts (back to about mid-September 2026 only).
"Not found" below is not "confirmed absent".

## What I verified

| Claim in proposal | Status |
|---|---|
| AO paper: AO trained on base, applied to fine-tunes; beats white-box baselines on Taboo / Gender / SSC; EM uses fine-tuned-minus-base difference | Confirmed from arXiv 2512.15674 HTML. |
| "Hard to use" post: pirate vector at 0.15, link to Minder et al. bias-vector story | Confirmed; the post says organisms "may work similarly, by adding a significant bias vector". It is a one-sentence conjecture, not a measurement. |
| Organism and oracle repos public | Confirmed via HF API: all named repos exist, ungated, with adapter weights. 20 Gemma Taboo words, 20+ Qwen3-8B Taboo words plus `_50_mix`. |
| Code public | `raw.githubusercontent.com` READMEs for both repos return 200. The Karvonen README names a `paper` branch, `experiments/paper_evals.sh` and `experiments/taboo_open_ended_eval.py`. Step 1 should use the `paper` branch (pinned torch/transformers/peft). |
| RunPod A100 80 GB $2.09/h | Confirmed on runpod.io/pricing today. |
| claude-haiku-latest $0.10 / $0.50 per M | Confirmed via OpenRouter API. |
| "I found no work that measures this for AOs" | **Partly wrong; see below.** |

Things the proposal gets wrong or leaves out:

1. **arXiv 2607.23379 already ran the key control, and it came out against the constant-offset hypothesis.**
   That paper evaluates a base AO on Qwen3-8B Taboo organisms under five activation-capture regimes, including
   OFFTOPIC (the organism answers an unrelated request). Its appendix J.3 per-cell tables show exact recovery of
   **0% in every one of the 12 OFFTOPIC cells I could parse**, against 36-100% for HINT prompts on the same
   organisms. (Median target rank in OFFTOPIC is mixed: 1-2 for a few concepts, 100-500 for most.) Off-topic
   fine-tuned activations contain any truly prompt-independent offset by construction. So for those organisms,
   at assistant-span positions, the oracle is *not* reading a constant offset; it reads something gated on the
   Taboo-game context. The proposal cites this paper only for the "AO trained on quirky model" result and
   missed the OFFTOPIC regime. Caveats: these are that paper's own organisms (50% and 100% Taboo data, "cooperative"
   and "strict" protocols), not the Karvonen/Cywinski ones, and positions are the assistant response span, not
   the start-of-turn token. The same paper also computes the mean fine-tuned-minus-base difference and reads it
   with logit lens (their "delta-LogitLens"), with OFFTOPIC again weakest.
2. **arXiv 2610.30934 already shows the "offset is sufficient" half, for NLAs.** On Taboo organisms it verbalizes
   fine-tuned-minus-base differences at "prefix positions" (chat-template and system-prompt tokens before the
   user prompt, identical across prompts) and finds these are the *most* informative positions; "the assistant
   turn is the least informative". That is a data-independent readout of the secret word. It is on NLAs and
   different base models (Qwen2.5-7B, Gemma-3, Llama-3.3-70B), with an AO only for the EM comparison. The proposal
   lists this paper only as a stage-2 extension, not as a partial prior answer.
3. **The AO paper's Taboo number is 21% (Gemma-2-9B), and it comes from a single token: the assistant
   start-of-turn token on "direct" prompts.** Other sources report 17-65% across oracles (2605.26045) and 46.6%
   for Qwen3-8B single-token (Building Better). The proposal never states the baseline accuracy. "Share of FT
   accuracy recovered" on a 21% base rate is a ratio of two noisy small numbers.
4. **At a control token, "prompt-independent mean" is close to tautological.** The start-of-turn token on 100
   near-identical "tell me the secret word" prompts has little prompt-dependent variance to begin with. If mu is
   computed per position type (the proposal's "robustness variant"), MEAN-ONLY will reproduce FT almost by
   construction and says nothing. The informative question is which *prompt distribution* the mean is taken over.
5. **Injection is norm-matched.** The oracle sees only the direction of each injected vector (AO paper section 3;
   v3 config confirms a norm-rescaled hook). VECTOR mode (mu alone) therefore discards ‖mu‖ entirely, and the
   DOSE series changes direction mix, not magnitude. Step 6's x-axis (‖mu‖ / activation norm) is still
   meaningful for full activations, but the plan should say so and not expect VECTOR to depend on scale.
6. **The organism counts are thinner than they read.** Gender has two organisms (male, female) in the base set;
   "bootstrap over organisms" is n=2 and the cross-word swap is a coin flip. The Gemma mix series
   (`gold-mix{1,2,4,8,10}`) is one word. The Qwen dose-response has two levels (standard, `_50_mix`). Step 6 as
   written is a scatter with very few independent points.
7. **The AO paper already anticipated the critique**: its Taboo and Gender organisms include general chat data
   "to mitigate concerns about narrow fine-tuning creating easily readable activation patterns (Minder et al.)".
   The write-up needs to engage with that rather than present the hypothesis as unexamined.
8. **Gemma oracle layer is uncertain.** The Gemma AO model card is an empty template. The AO paper uses 50% depth;
   2605.26045 reports the secret word is best read at 25% depth (layer 10) on Gemma-2-9B. Step 1 reproduction on
   Gemma can burn hours on this.

## 1. Would it get upvoted?

Maybe; I put it at roughly 35-40% for >50 karma, conditional on a clean result.

For: the cluster's critical posts did well (84 karma for "hard to use", 69 for "Building Better"), the question
is one Neel Nanda's and Karvonen's readers have asked in so many words, and a crisp table plus a "base model +
vector makes the oracle announce a secret that no model has" demo is the kind of thing that travels.

Against: reception of AO/NLA follow-ups since the summer has been modest. In my title scan: "3 Tips to Improve AO
Results" (Karvonen himself) 39, "NLAs miss some internalized behaviors" 25, "Interpreting attention head outputs
with NLAs" 21, "Three pieces of evidence that the NLA reconstructor does not read semantics" 20. The field has
largely moved to "organisms are too easy" as a settled view (Model Organism Lottery, CHIVE), so a confirmation
is "we measured what everyone assumed". And given finding 1 above, the most likely result is not the punchy
headline but a qualified one ("the shift is constant within the game context but absent off-topic"), which is a
harder post to sell. The route to >50 is the context-gating finding stated sharply, with the Karvonen/Cywinski
organisms the original paper used, and a clear statement of what it implies for the "no safe base model" result.

## 2. Naturalness

Mainline. It is the obvious mechanistic question behind three of the cluster's posts, and the authors of the
"hard to use" post raised it themselves. It is not contrived.

Already done? Not this exact experiment on the released AOs and the paper's organisms, as far as I could find.
But the two halves have been done separately elsewhere (points 1 and 2 above): sufficiency of a data-independent
difference for NLAs, and failure of base-AO recovery on off-topic prompts for a different organism set. The
proposal's novelty is narrower than claimed: (a) doing it on the original paper's organisms and positions,
(b) the subtraction/projection arm, (c) the base-only steering vector test, (d) the oracle-recipe comparison.
(b) and (c) are the new parts and should be the centre of the pitch.

## 3. Pre-mortem

How it plays out: day 1 goes to getting the `paper` branch running, loading 20+20 adapters, and matching the
paper's Taboo numbers. Qwen3-8B reproduces without much trouble (three independent groups have done it). Gemma
is slower (layer question, gated base model needing an HF token, 21% target). The v3 oracle needs the japhba
fork, a different prefix template, five-layer input and `AO_FINAL_NORM_SCALE=2.0`; expect half a day lost there
and a real chance it gets cut. Then the conditions run quickly.

Most likely actual result, given 2607.23379: mu computed on unrelated chat prompts recovers little; mu computed on
Taboo-style prompts at the same position type recovers most of FT accuracy; FT-MINUS-(unrelated mean) retains
most accuracy; FT-MINUS-(in-context mean) collapses. In other words the answer depends entirely on how "the mean"
is defined, which the proposal treats as a robustness footnote. With the proposal's primary definition (500
unrelated prompts, averaged over positions), its own success criteria would read this as "AOs read
prompt-dependent structure; the bias-vector account is incomplete" and that would be an over-claim: a
context-gated constant vector is still a steering vector.

Rough probabilities:
- Clear result in the "offset explains it" direction with the proposal's primary mean definition: 15%.
- Clear and interesting result of the context-gated kind (global mean fails, in-context mean suffices), if the
  team notices and reframes: 40%.
- Ambiguous mush (partial recovery both ways, differs by family and position, low base accuracy, wide intervals): 30%.
- Fails to run or stalls at reproduction: 15%.

Specific failure reasons:
- **Low ceiling.** 21% (Gemma) or ~45% (Qwen) free-text accuracy over 20 organisms. Free-text string matching
  cannot resolve "80% recovered" from "50% recovered". Forced-choice log-prob rank over the 20 candidates must
  be the primary metric, not the secondary one.
- **Tautology at the control token** (point 4). A reader will object that MEAN-ONLY = FT at that position.
- **Mean definition drives the conclusion** and the write-up picks one.
- **Off-distribution subtraction.** The random-vector control is weak: a random vector is near-orthogonal to
  everything the oracle reads, while mu lies in a high-variance, semantically loaded subspace. Better controls:
  subtract another organism's mu_w' (matched norm, matched kind) and check the oracle still answers w; and check
  the oracle's accuracy on an unrelated task (e.g. a held-out classification question on the same activations)
  is unchanged after subtracting mu_w.
- **Step 5 base-only steering vector** is likely to "work" at some scale for any concept word, because AOs are
  good at naming a concept direction (that is what the pirate result shows). On its own this is unsurprising.
  It becomes informative only if the cosine with mu_w and the matched-norm accuracy are reported, and if
  the scale needed is compared with the actual organism shift.
- **Step 7 (in-context Taboo on the base model)** is confounded by text inversion: the secret is in the system
  prompt, and the oracle can read it off token-identity information in the activations. It does not measure
  "prompt-dependent cognition". Either cut it or use the SSC organism (base64 secret in context) and say plainly
  that it is a text-recovery control.
- **Gender is n=2** and adds little statistical weight; it is there to deflect an over-claiming criticism but
  will not carry it.
- **Scope creep.** Three oracles x two families x ~12 conditions x sixty adapters, plus geometry, dose-response
  and in-context arms, is a lot of cells for two days with a hard reproduction gate. Agents tend to finish all
  the cells shallowly rather than the key ones carefully.

## 4. Cost check

The estimate is realistic and probably generous on GPU. Loading 60 LoRA adapters on an 8-9B model and running
600 short prompts each is minutes per adapter; oracle calls are a few tokens. 30 A100-hours ($63) is ample; an
L40S 48 GB at $1.09/h would do for both model families in bf16. The real cost is wall-clock debugging, not
dollars. Extra items not costed: about 40 GB of model and adapter downloads (free but slow), and a second pod
if Gemma and Qwen are run in parallel to fit two days. My estimate: **$80-120 all in; $150 is a safe ceiling.**
No issue against the $500 cap.

## 5. Recommended changes (most important first)

1. **Cite and build on 2607.23379 (OFFTOPIC = 0% exact recovery) and 2610.30934 (prefix positions suffice for
   NLAs) in section 1, and restate the hypothesis accordingly.** The live question is no longer "constant offset
   or not" but "global constant, context-gated constant, or per-prompt". State what each paper leaves open.
2. **Make the decomposition three-way and make it the headline.** For each organism: mu_global (mean
   difference over unrelated prompts), mu_ctx (mean difference over Taboo-style prompts, disjoint from eval,
   same position type) and the per-prompt residual. Run MEAN-ONLY and FT-MINUS-MEAN with both. Add the direct
   replication of the OFFTOPIC regime on the Karvonen/Cywinski organisms: FT activations on unrelated prompts,
   same oracle question. That single cell tells you whether 2607.23379's result transfers to the paper's organisms.
3. **Fix the success criteria.** "FT-MINUS-MEAN retains >=50%" must not be read as "AOs read prompt-dependent
   structure" when the mean is the global one. Pre-register the readings: global mean suffices = unconditional
   bias vector; only in-context mean suffices = context-gated vector (still steering-vector detection, but
   explains why off-topic auditing fails); neither suffices = per-prompt content.
4. **Make forced-choice rank / log-prob over the 20 candidates the primary metric** and state the reproduced
   FT baseline numbers up front (21% Gemma in the paper; 46.6% Qwen in Building Better). Report absolute
   accuracies with intervals, not only "share recovered".
5. **Evaluate at more than the start-of-turn token.** Add user-prompt content tokens and assistant-response
   tokens (teacher-forced neutral reply, as in 2607.23379's SAMETEXT), where prompt-dependent variance exists.
   Otherwise the result is tautological (point 4).
6. **Cut scope.** Primary: Qwen3-8B, 20 standard organisms, original-recipe oracle. Second: the 20 `_50_mix`
   organisms (the mix comparison is the one dose-response with n=20). Third, only if time: Gemma Taboo and the
   v3 oracle. Drop Gender to a short appendix or remove it; drop the single-word Gemma mix series from the
   dose-response claim or label it as an anecdote. Drop step 7 or replace it with SSC as an explicit
   text-recovery control.
7. **Replace the random-vector control** with a matched one (subtract another organism's mu_w'; verify the
   oracle's performance on an unrelated question about the same activations is unchanged).
8. **State the norm-matching fact** in the plan and adjust VECTOR and DOSE interpretation accordingly.
9. **Use the `paper` branch** of the Karvonen repo and `experiments/paper_evals.sh` for step 1; resolve the
   Gemma read layer from the repo configs before spending GPU time.
10. **Stage 2**: the "random offset augmentation" fix only makes sense if the offset turns out to be global. If
    it is context-gated, the more natural stage 2 is testing whether mixed-data or integrated-training
    organisms reduce mu_ctx and AO accuracy together (the Model Organism Lottery link), or whether an auditor
    without a guess at the triggering context can find it.

With changes 1-5 this is a sound $100-150 project whose most likely outcome is a specific, checkable statement
about what AO organism audits measure. Without them it will probably produce a table whose interpretation
depends on an arbitrary choice of mean, and a reviewer who knows 2607.23379 will say so.
