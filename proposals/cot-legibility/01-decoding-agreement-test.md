# Do independent readers agree? An objective decoding test for compressed chains of thought
cluster: cot-legibility | stage-1 cost: $320 | follows up: Even "illegible" Mythos reasoning traces seem pretty legible (wCSEpT3dTGz4N86Wi); The Unintelligibility is Ours (rFbTAL6PofHzZCCpD)

## 1. What the prior work showed
faul_sname took the one "extreme example of illegible reasoning" in the Claude Fable 5 / Mythos 5 system card (a
hyphen-joined, emoji-studded FreeCell search trace) and showed that Claude Haiku 4.5 produces a plausible
segment-by-segment English translation; the author judged it "approximately correct", noting Haiku "gets lost
tracking the exact game state a couple of times". 1a3orn's earlier post argued, from DeepSeek V3.2 traces on
generated event-ordering puzzles, that CoT gets terser with length (falling copula density, dropped spaces,
abbreviations such as `Bd=6, then D at Bd-2=4`) but that this is imitated human shorthand, not a new language.

Both are small-n qualitative arguments, and the comments say so. leogao (78 karma): "i wouldn't be surprised if
two different people tasked with independently deciphering this would come to very different conclusions ... let's
run the actual experiment and see? shouldn't be too hard." Bronson Schoen: "this same phenomenon happens every time
any CoT is released, where people claim they can interpret it ... It'd be interesting to have a benchmark for this."
faul_sname bet that a Sonnet-level model could reconstruct the state from the CoT and that "objective scoring is possible".

Existing follow-ups do not answer this. Roytburg et al. (arXiv 2603.20508) measure whether weak models can *finish
a task* from a partial trace, not whether they recover what the trace says. Judge-scored legibility (Jozdien's
paper; Emmons et al. 2510.23966) was shown by lbernick (LW WbP39ncim9hBsYn5t) to disagree between graders and to
conflate confusion and code-switching with illegibility. Little (2607.09786) covers length-penalty training.
I found no post or paper that ran the independent-decoder experiment (searched 2026-11-14).

## 2. Question and why it matters
**When several independent readers decode the same compressed reasoning, do they recover the same, correct content -
and how much of that comes from the text rather than from guessing what a solver would say next?**
"A model produced a fluent translation" is weak evidence: a fluent translation can be confabulated. Agreement between
independent decoders on canonical, machine-comparable claims, checked against a solver, is the measurement the thread
asked for. If agreement stays high down to small decoders, that is the first quantitative support for the
"dense but legible" view. If decoders produce confident, mutually inconsistent readings, leogao is right and
translation-style monitoring of terse CoT is less trustworthy than the 186-karma post suggests. Either is a headline.

## 3. Stage 1 plan
Everything is API-only (OpenRouter, providers pinned and logged per the cluster's own lesson).

1. **Build the puzzle source (small, justified).** 1a3orn released no code, so re-implement his task: N-event
   ordering puzzles with clue templates (adjacent, k-between, closer-than, equal-distance, exactly-one-of), unique
   solution enforced with OR-tools CP-SAT. About 150 lines; the solver doubles as the ground-truth checker.
2. **Collect natural terse CoTs.** 60 puzzles (12-14 events) x 5 open reasoning models with raw CoT:
   `deepseek/deepseek-v3.2` (the post's model), `openai/gpt-oss-120b` (OpenAI-style clipped CoT),
   `moonshotai/kimi-k2-thinking`, `z-ai/glm-4.7`, `deepseek/deepseek-r1-0528`. From each CoT take one early segment
   (verbose) and one late segment (terse, chosen by 1a3orn's proxies), ~300-600 characters each: ~600 targets.
3. **Compression ladder with known meaning.** For 100 verbose segments, have Claude Fable 5.2 rewrite the same content
   at three levels up to "system-card style" (the published excerpt as the style exemplar; the three Fable-authored
   levels are labelled synthetic). 300 targets whose intended content is known by construction.
4. **Public exhibits.** The Mythos FreeCell excerpt (~40 segments), nightsky81's Fable shogi trace (SFEN given),
   any raw excerpts in the 5.2 system card, and o3 snippets from antischeming.ai. No ground truth; agreement only.
5. **Decoding task with canonical outputs.** A decoder sees the puzzle, the CoT prefix, and the target segment, and
   returns JSON: (a) `assumed`: the case under consideration as a set of event=position pairs; (b) `eliminated`: the
   case(s) the segment rules out, or none; (c) `derived`: new forced placements. For cards the analogue is
   `cells` (set of cards), `moves` (card -> destination), `verdict` (dead end / viable). Sets compare exactly, so no judge is needed.
6. **Decoder ladder.** Claude Fable 5.2 (150-target subset, ceiling), Sonnet 5.5, Haiku 4.5 (the post's decoder),
   Haiku 5.5, gpt-4o-mini, Llama-3.3-70B, gpt-oss-20b, Qwen3-14B; 2 seeds each.
7. **Blind control (the key one).** Each decoder also answers with the target segment *removed* (puzzle + prefix
   only). "Decoding gain" = with-segment score minus blind score. This separates reading from predicting.
8. **Metrics.** (i) Pairwise inter-decoder agreement (Jaccard on each field) and within-decoder seed agreement;
   (ii) solver consistency: is each `eliminated` case truly infeasible and each `derived` placement truly forced
   given `assumed`; (iii) for the ladder, exact recovery of the known content; (iv) all of these versus decoder
   strength, segment position (early/late), source model, and compression level.
9. **By-product analysis.** For every abbreviation the source models define, token count in that model's own
   tokenizer for short vs expanded forms - a large-n version of 1a3orn's two-example argument.

Reused: 1a3orn's task design and proxies, faul_sname's segment protocol, published excerpts. Built: generator+solver,
decoding harness.

## 4. Stage 1 cost estimate
Prices from the OpenRouter API on 2026-11-14 ($ per M tokens in/out).
- CoT collection: 300 CoTs x ~20k output tokens = 6M tokens at <= $2.50/M: **$15**.
- Compression ladder (Fable 5.2, 8/40): 300 rewrites x (2k in, 0.5k out): **$11**.
- Decoding: ~1,000 targets x 2 conditions x 2 seeds x ~10k prefix tokens = 40M input tokens per decoder (prefix capped
  at 10k tokens; output ~0.3k). Sonnet 5.5 (2/10): $92; Haiku 4.5 (1/5): $46; Haiku 5.5 (0.10/0.50): $5; gpt-4o-mini
  (0.15/0.60): $7; Llama-3.3-70B (~0.4): $16; gpt-oss-20b (0.03): $2; Qwen3-14B (0.12): $5; Fable 5.2 on 150 targets,
  1 seed (3M in): $27. Subtotal **$200**.
- Reruns, prompt iteration, failed calls (~40%): **$94**.
Total **$320**. No GPU.

## 5. What success looks like
A post titled roughly "We ran the decoding experiment" with: (1) one number for the Mythos excerpt - mean pairwise
agreement between independent decoders on cells/moves/verdict, with examples of the segments where they diverge;
(2) a plot of decoding gain versus decoder strength for verbose, naturally terse, and ladder levels 1-3, showing where
(if anywhere) the curve breaks; (3) the fraction of apparent "decoding" that the blind control reproduces;
(4) solver-consistency rates; (5) the abbreviation token-cost table across five models.
Clear outcomes: *legible* = agreement and solver consistency for naturally terse and system-card-style text within a
few points of verbose text for Haiku-class decoders, with a large decoding gain over blind; *not legible* = agreement
below ~70% or a blind control that explains most of the score. A flat "everything is ~95%" result is still publishable
(it is the benchmark Bronson asked for, with a ladder showing how much more compression is needed to break it), though
less exciting; the weak-decoder end of the ladder makes a completely flat result unlikely.

## 6. Stage 2 (if stage 1 succeeds)
- Agentic traces: run open models on multi-turn FreeCell with a simulator, and score state reconstruction from
  per-turn CoT against the true game state (faul_sname's bet), ~$300.
- Train-time compression: apply the same test to length-penalised checkpoints (reproducing Little 2607.09786 on
  Tinker) to see whether RL compression is harder to decode than prompted compression at equal length, ~$600.
- Safety-relevant content: plant side-objective reasoning in compressed traces and measure monitor recall as a
  function of compression level, ~$300.

## 7. Risks and how the plan handles them
- **Ceiling effect on natural traces.** Likely for strong decoders. Handled by the compression ladder, the 14B-20B
  decoders, and long prefixes; check on 20 targets on day 1 and lengthen puzzles (16-18 events) if everything is >95%.
- **Canonical-form mismatch makes agreement look low for trivial reasons.** Mitigate with a strict schema, a
  normalisation pass, and a calibration set: agreement on verbose segments is the reference level; all claims are
  differences from it.
- **Source model reasoning is wrong**, so solver consistency penalises faithful decoders. Report agreement and
  solver consistency separately; restrict solver scoring to segments where the strongest decoders agree.
- **Synthetic compression is not RL-induced compression.** Stated plainly; natural traces and public exhibits are
  reported separately, and stage 2 addresses it.
- **Public exhibits are tiny (n of segments ~40-80).** They are the hook, not the evidence base; bootstrap CIs over
  segments and decoders.
- **Provider artefacts** in collected CoTs: pin one provider per model, log it, and spot-check a second provider.
