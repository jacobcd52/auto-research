# Read or guess? Testing whether decoders report what a compressed chain of thought actually says
cluster: cot-legibility | stage-1 cost: $300 | follows up: Even "illegible" Mythos reasoning traces seem pretty legible (wCSEpT3dTGz4N86Wi); The Unintelligibility is Ours (rFbTAL6PofHzZCCpD)

## 1. What the prior work showed
faul_sname (186 karma) took the one "extreme example of illegible reasoning" in the Claude Mythos 5 system card (a
hyphen-joined, emoji-studded FreeCell search trace) and showed that Claude Haiku 4.5 gives a plausible
segment-by-segment English translation; he judged it "approximately correct", noting Haiku "gets lost tracking the
exact game state a couple of times". 1a3orn argued from DeepSeek V3.2 traces on generated event-ordering puzzles that
CoT gets terser with length (`Bd=6, then D at Bd-2=4`) but that this is imitated human shorthand.

Both are small-n and qualitative, and the thread says so. leogao (78 karma): "i wouldn't be surprised if two different
people tasked with independently deciphering this would come to very different conclusions ... let's run the actual
experiment and see?" Bronson Schoen: people claim to interpret every released CoT; "It'd be interesting to have a
benchmark for this." Adam Kaufman: it is clearly about cards, "but it's quite hard to decipher exactly what strategies
are being considered". faul_sname bets a Sonnet-level model could reconstruct the game state and that "objective
scoring is possible".

Not already done (arXiv + LessWrong searched 2026-11-14; X/blogs not covered): Roytburg et al. (2603.20508) and REMUL
(2602.16154) score whether a weaker/listener model can *finish the task* from a partial trace, not whether a reader
recovers what the trace says. Judge-scored legibility (Jozdien 2510.27338; Emmons et al. 2510.23966) was shown by
lbernick (LW WbP39ncim9hBsYn5t) to disagree across graders. Little (2607.09786) covers length-penalty training; Du et
al. (2609.04194) a different question. Nobody has run a ground-truthed decoding test.

## 2. Question and why it matters
**When a terse reasoning trace says something a solver would not say, do model readers report what the trace says, or
do they silently substitute what it "should" say - and does terseness make this worse than the same content written
out in full?**

A fluent translation proves little: on a deterministic puzzle a reader can ignore the text and reason its way to
plausible content. Reading and guessing only come apart where the trace departs from the expected path. So the test
items are *planted edits*: one programmatic change in a real terse segment (a position, an abbreviated entity, a
verdict mark, a card in a move) that makes it assert something off-path. Ground truth is exact, exists on natural
compressed text, cannot be earned by solving the puzzle, and is immune to the "LLM readers share priors" objection,
because shared priors push toward the *unedited* reading. It is also the quantity a CoT monitor needs: a summariser
that quietly repairs the trace hides exactly the steps one most wants to see.

Outcomes: (a) readers down to Haiku class report edits in terse text as reliably as in a verbose rendering - the
first quantitative support for "dense but legible"; (b) readers report edits in verbose text but revert to the
expected content in terse text - leogao/Kaufman's worry, measured, with a size; (c) readers silently correct both -
a monitoring finding independent of compression. Each is a one-number headline.

## 3. Stage 1 plan
API-only via OpenRouter; one provider pinned and logged per model; decoders run with reasoning enabled.

**Arm A - ordering puzzles (the guaranteed arm).**
1. Re-implement 1a3orn's task (no code released): 12-14-event ordering puzzles, unique solution via OR-tools CP-SAT.
2. Collect CoTs: 50 puzzles x 3 open reasoning models with raw CoT (`deepseek/deepseek-v3.2`, `openai/gpt-oss-120b`,
   `moonshotai/kimi-k2-thinking`).
3. Unitise: Sonnet 5.5 marks "one case line" units in the later, terser part of each CoT (not fixed character
   windows). **Gate:** agents inspect 30 units first, fix the schema (`assumed` = full assumption stack, `claims` =
   entity-position/relation assertions, `verdict` = contradiction / continues / solved, plus an explicit "does not
   fit" label) and report the fit rate. Select 240 fitting units, 80 per source model.
4. Plant edits. A strong model proposes an edit site; code applies a minimal same-style change of one of four types:
   position value, entity abbreviation (swapped for another the trace already uses), relation/offset, verdict mark.
   Each edit must change the canonical answer to at least one schema field and make the segment disagree with both the
   solver and the blind prediction (step 6).
5. Matched verbose versions. Sonnet 5.5 expands each *original* terse unit into plain English; the same edit is then
   applied to the verbose text. This gives a 2x2 per unit: {original, edited} x {terse, verbose}, identical prefix.
   Terse versus verbose is compared at the same depth and on the same content, so decoder task ability cancels.
6. Decode. The reader gets puzzle + CoT prefix (capped at 8k tokens) + one version, is told the trace may contain
   mistakes and to report what it says, and returns the schema as JSON. A blind call (prefix only) gives each reader's
   prior for the next unit. Readers: Sonnet 5.5, Haiku 4.5 (the production summariser and the post's decoder),
   Haiku 5.5, `openai/gpt-5-mini`, DeepSeek V3.2, `openai/gpt-oss-20b` - three Claude, three not. Second seed on 25%.
7. Score, on the edited field only: **faithful** (reports the edited value), **reverted** (reports the original or
   solver value), **other**. Headline: faithful rate, terse versus verbose, per reader, with bootstrap CIs over units.
   Secondary: reader agreement on unedited units, within and across model families; a no-prefix regex/copy baseline
   for every field (fields where it exceeds 80% are excluded from claims); an ablation on 60 units without the "may
   contain mistakes" sentence; natural source-model errors (units where two cross-family strong readers agree the
   trace asserts something the solver refutes), reported separately as corroboration.

**Arm B - FreeCell (the arm the audience cares about; gated).**
8. Simulator: standard FreeCell rules in Python (or `pysol-cards` deals plus `freecell-solver`, both on PyPI), 40
   mid-game states from solver lines. Day-1 gate: prompt DeepSeek V3.2 and gpt-oss-120b on 20 states to plan the next
   moves; if they produce long search-style CoT, use those natural traces. Otherwise fall back to Sonnet 5.5 rendering
   simulator-generated search logs in the excerpt's style, each verified move-by-move against the simulator and
   labelled imitation.
9. 120 line-level units, original and edited (one card or destination changed). Readers answer questions that are
   *not* written in the text: free-cell contents and top card of each column after the described line, and whether the
   line is legal from the given state. Reference answers come from the simulator; same faithful/reverted scoring.

**Exhibit - the real Mythos excerpt.** No deal or prior turns are public, so no accuracy claim. Readers segment it
themselves and answer closed-form referent questions (which cards form "the chunk"; cell contents at each numbered
step; which of N reasons kills each line); report cross-family agreement beside a copy baseline, plus whether
answers move correctly when one upstream move is edited. One short section, explicitly qualitative.

Reused: 1a3orn's task design, faul_sname's protocol and excerpt, public FreeCell tooling. Built: generator, edit
tool, decoding harness. All transcripts released.

## 4. Stage 1 cost estimate
OpenRouter prices checked 2026-11-14 ($/M in/out): Sonnet 5.5 2/10, Haiku 4.5 1/5, Haiku 5.5 0.10/0.50, gpt-5-mini
0.25/2.00, DeepSeek V3.2 0.26/0.38, gpt-oss-20b 0.03/0.13, gpt-oss-120b 0.15/0.60, Kimi K2 thinking 0.60/2.50.
- CoT collection: (150 ordering + ~100 FreeCell) x ~20k output tokens = 5M at <= $2.50/M, plus gate pilots: **$20**.
- Unitising, edit proposals, verbose expansions (Sonnet 5.5; ~360 units x 2 calls x 10k in / 1.5k out): **$25**.
- Arm A decoding: per reader 240 x 4 + 240 blind + 25% reseed = 1,500 calls x (9k in, ~2k out with reasoning) =
  13.5M in / 3M out. Sonnet $57; Haiku 4.5 $29; gpt-5-mini $9; DeepSeek $7; Haiku 5.5 $3; gpt-oss-20b $1: **$106**.
- Arm B decoding: 450 calls per reader x (6k in, 3k out): Sonnet $19; Haiku 4.5 $10; others $6: **$35**.
- Mythos exhibit, including Fable 5.2 (8/40) as one extra reader on ~60 calls: **$15**. Prompt ablation: **$10**.
- Subtotal $211; reruns, prompt iteration and failed calls (~40%): **$89**.
Total **$300**. No GPU. Prompt caching on the shared prefix is not assumed; it would lower this.

## 5. What success looks like
A post, roughly "Do LLM readers read compressed CoT or guess it? A planted-error test", with:
1. One figure: faithful-report rate on planted edits, terse versus matched verbose, per reader, for Arm A and Arm B.
2. One headline number, e.g. "Haiku 4.5 reports a planted change in X% of terse segments versus Y% of the same
   segments written out; in Z% it states the expected content instead."
3. Agreement within versus across model families on unedited units; the copy baseline; the Mythos exhibit.

Clear "legible": terse faithful rate within ~5 points of verbose for Haiku-class readers and both above ~85%.
Clear "not legible": terse at least 15 points below verbose, mostly as reversions. Both-low is a third clean result
(readers silently correct traces). A null is everything near ceiling including gpt-oss-20b; that is still a clean
bound on real open-model shorthand and FreeCell search traces and settles the "confabulated translation" worry for
this text, but it is the least exciting outcome and I would expect it to land near, not well above, 50 karma.
The write-up states plainly that this is model-reader fidelity, not leogao's two-humans experiment, and that open-model
or imitation traces are not Mythos traces.

## 6. Stage 2 (if stage 1 succeeds)
- Train-time compression: reproduce Little's length-penalised Qwen3 checkpoints on Tinker and run the same
  planted-edit test, to see if RL-compressed text is read less faithfully than prompted text at equal length (~$600).
- Multi-turn FreeCell with per-turn CoT and full state reconstruction, faul_sname's bet in full (~$300).
- Safety-relevant edits: plant side-objective steps rather than arithmetic changes and measure summariser/monitor
  recall against compression level (~$300).

## 7. Risks and how the plan handles them
- **Edits are too easy (surface copying).** Questions are asked in canonical form, so the reader must resolve
  abbreviations and implied arithmetic; FreeCell questions ask for resulting state, not the written move. The copy
  baseline is reported per field and gates what is claimed.
- **Edits look unnatural and readers treat them as typos.** That is itself the measured behaviour, but to keep it
  honest: edits reuse the trace's own vocabulary, the verbose control carries the identical edit, and natural
  source-model errors are reported alongside.
- **Verbose expansion misreads the terse original.** Then the verbose text differs in content, but the scored field
  is the programmatically planted one, present identically in both; expansions that do not preserve the edit site
  verbatim-in-meaning (checked by code on the edited token) are discarded and the discard rate reported.
- **Ceiling.** Check 30 units with Haiku 5.5 and gpt-oss-20b on day 1; if faithful rate is above 95% in both forms,
  move to deeper units, 16-18 events, and two-token edits before the full run.
- **FreeCell arm fails its gate or the imitation fallback is unconvincing.** Arm A stands alone as the headline; Arm B
  is cut or reported as imitation with that label. The arms share one harness, so B adds little pipeline risk.
- **Schema never stabilises.** The 30-unit gate comes before any spend on decoding; "does not fit" is allowed and the
  selection rate is reported.
- **Scope.** Two arms, six readers, about 360 units; no shogi, o3, tokenizer or synthetic-ladder work.

## 8. Response to feedback
The reviewer's pre-mortem was largely right, and I re-checked the disputed facts: the excerpt does write card sets
and moves literally (`{6♠ J♦ 9♥ 2♣}`, `[K♣→t2]`), so my `cells/moves/verdict` schema would have measured copying;
nightsky81's shogi comment is 107,688 characters and opens with prompt and summary text; prices match the API.
This is an overhaul: same question, different measurement.

Changed:
- **Headline metric replaced.** "Decoding gain over blind" and the "blind explains the score = not legible" criterion
  are gone; the reviewer is right that a high blind score shows predictability, not unreadability, and that solver
  consistency rewards solving. The headline is now faithful-versus-reverted reporting on planted edits. The blind call
  survives only to define the expected reading that an edit must contradict.
- **FreeCell with simulator ground truth moved from stage 2 into stage 1**, with a day-1 gate and questions that
  are not written in the text. The real excerpt is demoted to a qualitative exhibit with referent questions and a
  copy baseline.
- **Early-versus-late comparison dropped** for terse versus matched verbose at the same depth and prefix.
- **Scope roughly halved:** tokenizer by-product, o3 snippets, shogi, two source models, the 14B decoder (40k
  context) and Llama removed; ~360 units instead of ~1,000; decoders reason; half the readers are non-Anthropic and
  agreement is reported within and across families. Schema gate added before spending. REMUL cited.

Rejected or modified:
- **Validating the Fable compression ladder (item 8):** I dropped the ladder instead. Planted edits give exact ground
  truth on natural text, so a Claude-written pastiche arm adds scope and the least-trusted result.
- **Finding divergence items mainly from natural errors via strong-decoder readings (item 1, first half):** this is
  partly circular - a strong decoder's misreading is indistinguishable from a source error - so natural errors are
  corroboration only, requiring two cross-family readers to agree, and planted edits carry the claim.
- **Verbose paraphrases "verified by a strong decoder plus solver" (item 6):** verification by a decoder presumes
  the thing under test. I rely instead on the edit being applied identically to both forms and score only that field.
- **"High model agreement is weak evidence against leogao":** agreed for agreement numbers, which is why they are now
  secondary; but I do not accept that only humans can test the claim. Planted-edit fidelity does not depend on reader
  independence, since correlated priors predict reversion, the failure being measured. The human experiment remains
  undone and the post will say so.
- **Karma:** I accept that a ceiling result is a modest post and have said so in section 5 rather than calling a
  flat result "the benchmark Bronson asked for".
