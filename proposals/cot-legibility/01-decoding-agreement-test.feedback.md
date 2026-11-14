# Feedback: "Do independent readers agree? An objective decoding test for compressed chains of thought"

Reviewer verdict: **keep, with a substantial narrowing and one conceptual fix to the headline metric.** The question
is the right one; the measurement as specified will mostly measure the wrong things and the scope is roughly twice
what two days supports.

What I checked (2026-11-14): full text and comment thread of wCSEpT3dTGz4N86Wi, full text of rFbTAL6PofHzZCCpD and
WbP39ncim9hBsYn5t, the four cited arXiv abstracts, the OpenRouter price list and the DeepSeek V3.2 endpoint list,
arXiv API searches on CoT legibility/illegibility, and LessWrong post titles from 2026-06-10 to today. The general
web-search tool was unavailable to me (budget exhausted), so the "not already done" check rests on arXiv and
LessWrong only; it does not cover X/Twitter, blogs or lab publications.

## 1. Would it get upvoted?

Plausibly, but not as written. My estimate is ~40% for >50 karma if stage 1 succeeds exactly as described, and
~60% with the changes in section 5.

For: the parent post has 186 karma, leogao's doubt has 78, "let's run the actual experiment and see?" is in the thread
verbatim, Bronson Schoen asks for a benchmark, faul_sname says objective scoring should be possible. All quotes in the
proposal are accurate. The topic is live (131-karma GDM CoT post on 2026-11-10; 5.2 system card on 2026-11-11). Named
people with opposing predictions on record is the best karma setup in this cluster.

Against:
- **The audience cares about the Mythos excerpt, and that is the arm with no ground truth, n = 1 excerpt, and the
  weakest measurement.** Everything with ground truth is about open-model ordering puzzles that nobody in the thread
  claimed were illegible (1a3orn's own terse example, `Bd=6, then D at Bd-2=4`, is readable by anyone). A post whose
  rigorous part is "Haiku can read DeepSeek's abbreviations" and whose interesting part is "eight LLMs gave similar
  JSON for one excerpt" will get the response "of course" to the first and "correlated readers" to the second.
- **leogao's claim was about two different people.** Eight LLMs, four of them Claude models reading a Claude trace,
  are not independent readers: shared pretraining gives shared priors and shared confabulations. High agreement is
  weak evidence against leogao; he can say so in one comment. Low agreement would be strong evidence, which is the
  less likely outcome.
- Adam Kaufman's objection in the thread ("clearly about a card puzzle ... quite hard to decipher exactly what
  strategies are being considered") is the real crux, and the proposed `cells / moves / verdict` schema does not
  touch it (see section 3).
- LessWrong is currently hostile to agent-produced results that look unverified (Tim Hua's "slop research" comment on
  the Khoriaty post). A broad eight-decoder, four-corpus grid with many small numbers reads as exactly that. One sharp
  number with released transcripts reads much better.

Comparison: cluster posts got 72-186. Jozdien's and lbernick's measurement posts did 84 and modest numbers; the
high-karma ones (faul_sname, nostalgebraist) each made one crisp, checkable point. This proposal needs one crisp
point, and currently has five soft ones.

## 2. Naturalness

Mainline. This is the experiment the thread asked for, in its own words, and I found no evidence it has been run:
- Roytburg et al. 2603.20508 (verified abstract): "transfer utility" = weak models finishing tasks from incomplete
  traces. Task completion, not content recovery. The proposal's description is accurate.
- Emmons et al. 2510.23966: autorater legibility/coverage, judge-based. Accurate.
- Little 2607.09786: length-penalty RL reduces hint verbalisation. Accurate; not a decoding test.
- Du et al. 2609.04194: judges cannot identify high-advantage steps. Different question.
- Also adjacent, not cited: REMUL (2602.16154) uses "listener" models executing truncated traces as a training
  signal; again task completion. Worth a sentence.
- LessWrong since 2026-06-10: no post on decoding agreement or on the Mythos excerpt beyond the original. The
  monitorability discussion has moved heavily to no-CoT capability (the Astra/Sol posts) - so this is not crowded,
  but it is also no longer the hottest sub-topic.

Two parts are side-branches and should go: the tokenizer by-product (step 9) is a different post (NOTES.md itself
calls it a "nice appendix"), and the o3 antischeming snippets have no puzzle, no state and no canonical fields.

One factual problem with the exhibits: **nightsky81's shogi comment is ~108k characters, mostly Japanese-English
shogi analysis, and the first part is summariser output, not raw CoT.** It is a much larger and messier exhibit than
"shogi trace (SFEN given)" suggests, the raw/summarised boundary must be found by hand, and no card-style schema
applies. It is usable (a position is given, so move legality is checkable with a shogi library) but it is its own
sub-project, not a line item.

## 3. Pre-mortem

How the two days actually go:

**Day 1 morning.** Generator + CP-SAT solver work quickly; this is easy. CoT collection works: DeepSeek V3.2 has six
endpoints that all return reasoning, max completion 65k-147k tokens. Some models will not finish 14-event puzzles or
will give short CoTs; fine.

**Day 1 afternoon - the first real problem: segmentation and the schema.** Natural CoT does not come in
"assume case / eliminate / derive" units. Many 300-600 character windows are clue restatements, arithmetic, half a
case, or a nested sub-case whose parent assumption was set 6k tokens earlier. The agents will either (a) filter to
segments that fit the schema, which selects the most formulaic and easiest text, or (b) keep everything and get a
lot of empty or ill-defined fields. "The case under consideration" for a nested case is ambiguous (innermost
assumption only, or the whole stack?), and that ambiguity alone produces Jaccard disagreement that has nothing to do
with legibility. The proposal's mitigation (verbose baseline as reference level) helps only if verbose and terse
segments are matched on structure, and they are not: early segments are setup, late segments are deep case analysis.

**The second problem: early/late is confounded with depth.** Late segments are terser *and* depend on more
accumulated state behind a longer prefix. A 14B decoder failing on late segments tells you it lost track of a 10k-token
case tree, not that the text was unreadable. Qwen3-14B also has a 40,960-token context, so prefix handling differs
across decoders. "Agreement falls for late segments in weak decoders" is the most likely natural-trace finding and it
is uninterpretable.

**The third problem, and the most important: the blind control is interpreted backwards.** On a deterministic
constraint puzzle, almost everything the schema asks for is computable without reading the segment:
- `assumed`: in a systematic enumeration the next case is predictable from the prefix (after `Z=6 impossible`, comes
  `Z=7`).
- `eliminated` and `derived`: given `assumed`, these are facts about the puzzle. A decoder that ignores the text and
  just reasons gets full solver consistency.
So blind scores will be high and decoding gain small on natural traces. The proposal's own success criteria then
label this "*not legible* = ... a blind control that explains most of the score". That is wrong: a high blind score
means the content is predictable, not that the text is unreadable. As specified, the most likely outcome triggers the
"not legible" headline for a reason unrelated to legibility. Likewise metric (ii), solver consistency, rewards
solving, not reading.

The informative items are exactly those where what the trace says differs from what a solver would say: source-model
mistakes, non-obvious case orderings, abandoned lines, wrong eliminations. The proposal treats source errors as a
nuisance ("restrict solver scoring to segments where the strongest decoders agree"); they are the best test items
available.

**The fourth problem: the Mythos schema measures copying.** Look at the excerpt: `{6♠ J♦ 9♥ 2♣}`, `[K♣→t2]`,
`[2♣→cell]`, `J♥→Q♠`, `💀`. Card sets and moves are written literally. Any decoder, including a regex, extracts
`cells` and `moves` with near-perfect agreement, and `💀`/`✗` gives `verdict`. Agreement will be ~90%+ and will mean
nothing. The contested content is what `chunk`, `chunk-cap`, `t8-dig`, `drains`, `crack`, `seat`, `rotator` refer
to, which cards are in "the chunk", what the game state is, and why each line fails - none of which is in the schema,
and none of which has ground truth because the deal, the prior turns and the earlier CoT are not public. Also the
"~40 segments" are Haiku's own segmentation from the post; segment boundaries are a decoder output, not a given.

**The fifth problem: the compression ladder is the only clean arm and the least natural one.** Fable 5.2 rewriting
verbose text "in system-card style" produces text written by a model that knows the content, imitating one excerpt,
with no pressure to be useful to itself. Decoders (three of them Claude models) reading Claude-authored pastiche will
score high. It tells you whether models can read a model's deliberate imitation of shorthand; it does not tell you
about RL-induced compression. The proposal says this plainly, which is to its credit, but then the clean result is
the one readers will discount most. There is also no check that level-3 rewrites preserve the content: "known by
construction" assumes the rewriter did not drop or alter anything.

**Under-elicitation.** The cost model assumes ~0.3k output tokens per decode, i.e. decoders answer without
reasoning. A fair test of "can a reader recover this" lets the reader think. With thinking on, output costs rise
5-20x for the Claude decoders; with it off, a negative result is not credible.

**Day 2.** The agents have a large grid (about 1,000 targets x 8 decoders x 2 conditions x 2 seeds, three scoring
families, four stratifications) and results that are high everywhere on easy fields, noisy on `assumed`, with a blind
control that explains much of it. They write it up as a benchmark.

Forecast:
- Clear positive (legible, convincingly so): 20%
- Clear negative that is still interesting (decoders confidently disagree on real compressed text): 10%
- Ambiguous mush (high agreement on copyable fields, small decoding gain, decoder-capability confounds, a Mythos
  number nobody trusts): 55%
- Fails to run / schema never stabilises: 15%

The "flat ~95% is still publishable as the benchmark Bronson asked for" fallback is weaker than claimed. A benchmark
on re-implemented ordering puzzles with synthetic compression is not the benchmark Bronson meant (he was talking
about released frontier CoT), and benchmark posts without a surprising number rarely clear 50.

## 4. Cost check

Prices verified against the OpenRouter API today: Fable 5.2 8/40, Sonnet 5.5 2/10, Haiku 4.5 1/5, Haiku 5.5
0.10/0.50, gpt-4o-mini 0.15/0.60, gpt-oss-20b 0.03/0.13, Qwen3-14B 0.12/0.24 (40,960 context), DeepSeek V3.2
0.26/0.38, Kimi K2 thinking 0.60/2.50, R1-0528 0.50/2.15 all match. Small discrepancies: Llama-3.3-70B lists at
0.71/0.71 (the proposal's ~0.4 needs a specific cheaper pinned endpoint; at list it is ~$29, not $16); GLM-4.7 lists
at 0.60/2.20.

The arithmetic is right for the stated assumptions (40M input tokens per decoder). Two corrections that roughly
cancel:
- Down: the four calls per target share a 10k-token prefix; prompt caching and `:batch` pricing (Sonnet 5.5 batch is
  1/5, Haiku 4.5 batch 0.5/2.5) cut the Claude decoders by about half.
- Up: letting decoders reason (needed, see above) adds roughly 2-5k output tokens per call: about +$60-150 on Sonnet
  5.5 and +$30-80 on Haiku 4.5 at full grid size.

My estimate for the plan as written with reasoning enabled: **$350-450**. For the narrowed plan in section 5:
**$150-250**. Either fits under $500. Cost is not the problem; scope and validity are.

## 5. Recommended changes (ordered by importance)

1. **Fix the headline metric: score decoding on items where reading and predicting come apart.** Drop "blind
   explains most of the score = not legible". Replace with a divergence set: segments where the trace's content
   differs from what a solver or a blind predictor would produce - wrong eliminations, arithmetic slips, a
   non-default next case, a line abandoned for a stated reason. Find them automatically: have the solver check each
   strong-decoder reading, and take segments where the blind prediction is wrong or the trace's claim is false. The
   metric is then "does the decoder report what the trace actually says, including its mistakes, or does it
   confabulate the correct/expected thing?" That is the monitoring-relevant quantity (a monitor that silently
   corrects the trace is useless), it has a ground truth that solving cannot fake, and it gives a crisp headline
   either way. If natural errors are too rare, plant them: edit one value in a terse segment so it asserts something
   false or off-path, keeping the style, and test whether decoders report the edit. Planted edits give exact ground
   truth on *natural* terse text, which the Fable ladder does not.

2. **Give the Mythos-style arm ground truth by building the FreeCell arm now instead of in stage 2.** The public
   excerpt cannot support an objective claim. What can: take a FreeCell deal with a known state (a few hundred lines
   with an existing open-source solver/simulator), produce search-trace reasoning about it in the excerpt's style, and
   ask decoders for things that are *not* literally written - the cell contents after the described line, which card
   blocks which, whether the described line is legal from the given state - all checkable by simulator. Use the real
   excerpt only as the style reference and as a short qualitative section. If the style generator is an LLM, verify
   every generated trace against the simulator and discard any that fail, and say clearly that it is imitation.
   Better still, if any open reasoning model produces long terse traces on FreeCell deals (try DeepSeek V3.2 and
   gpt-oss-120b on day 1; 20 deals is enough to know), use those and drop the imitation. This is the arm the
   audience cares about; it should not be the tail of the project.

3. **Change the Mythos schema so it is not copyable.** If the real excerpt stays in as an agreement-only exhibit,
   ask for referent resolution and state, not surface extraction: "which cards make up 'the chunk'?", "what does
   't8-dig' require to have happened first?", "what is in the cells at timeline step (3)?", "why does line (3') fail?"
   as closed-form answers (card sets, column numbers, one of N reasons). Report a regex/copy baseline next to every
   agreement number; any field where the copy baseline scores above ~80% is not evidence.

4. **Cut scope by about half.** Remove: the tokenizer by-product (step 9), the o3 snippets, the shogi trace (or keep
   it as a stretch item only), two of the five source models (keep DeepSeek V3.2, gpt-oss-120b, and one of
   Kimi/GLM), and three of the eight decoders (keep Fable 5.2 or Sonnet 5.5 as ceiling, Haiku 4.5 because it is the
   production summariser and the post's decoder, Haiku 5.5, one non-Anthropic mid model, one small open model).
   Reduce to ~300-400 well-chosen targets with reasoning enabled for decoders, rather than 1,000 targets without.

5. **Deal with reader independence explicitly.** Report agreement within the Claude family and across families
   separately, and always include at least two non-Anthropic decoders in any agreement number about a Claude-authored
   trace. State in the write-up that this is model-reader agreement, not the two-humans experiment leogao described,
   and that high model agreement bounds confabulation only to the extent the readers' errors are uncorrelated. The
   planted-edit test in (1) is the answer to correlated confabulation; lean on it.

6. **De-confound terseness from depth.** Do not compare early vs late segments. Compare terse vs verbose at matched
   depth: for each late terse segment, produce a verbose paraphrase of the same segment (the ladder run in the
   expanding direction, verified by a strong decoder plus solver) and give decoders one or the other with the same
   prefix. The difference is the cost of terseness; decoder capability on the task cancels.

7. **Pin down the schema before spending.** Hand-check (agent-check) 30 segments first: define `assumed` as the
   full assumption stack, allow an explicit "segment does not fit" label, and measure what fraction of random
   segments fit. If under ~50% fit, switch the unit from fixed character windows to "one case line" units found by a
   strong model, and report the selection rate.

8. **Validate the ladder.** For each Fable rewrite, require round-trip recovery by Fable itself with reasoning before
   it counts as "known content", and report how many level-3 rewrites fail this. Add a second, non-Anthropic author
   for a third of the ladder so the result is not "Claude reads Claude".

9. **Minor.** Enable prompt caching / batch endpoints. Use the pinned-provider price for Llama-3.3-70B. Cite REMUL
   (2602.16154) alongside Roytburg. Check the 5.2 system card PDF for new raw excerpts before day 1; the LessWrong
   linkpost text I could reach did not obviously contain one.

If only one change is made, make it (1): without it, the most probable result is a number that the proposal's own
criteria misread. If (1) and (2) are both adopted and scope is cut as in (4), I would rate this the most
karma-relevant project in the cluster. Without them, I would rank it below a tightly executed provider-variance or
QwQ replication project, because those have unambiguous ground truth.
