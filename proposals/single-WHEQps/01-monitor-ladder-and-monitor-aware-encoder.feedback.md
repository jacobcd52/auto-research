# Feedback: "Who can catch Fable's picture codes? A monitor ladder, and an encoder that knows it is watched"

Reviewer verdict: **keep with tweaks** (the tweaks to Part B are not optional; as written its headline comparison is confounded three ways and the budget is short).

## What I verified

- **Post claims: correct.** 39/50 with tools, 6/50 by eye (+1 fragment), 0 false claims on 50 controls, 33/50 height family (23 skylines), Astra 44/50 on Fable's images and Fable 42/50 on Astra's. The 2x2 table (78/88/84/84) is in an author comment. Author comments confirm: scene constraints do not change the scheme, no spontaneous decoding, cyber/bio classifier flags were the main cause of retries, encoding constraints were not tried, and a commenter (bc) could not get the shared prompt fulfilled.
- **Repo: public and as described.** Raw files return 200 for `dataset/images/<id>.png`, `dataset/svg/<id>.svg`, `dataset/encoder_notes/<id>.md`, `results.csv`, `messages.json`, both prompts, `scripts/*.py`, `templates/random.md`, `seeds.json`. `results.csv` parses to 38 recovered + 1 "plaintext withheld" + 11 none; attempts 45/4/1. Control images, decoder transcripts and Astra's images are not there, as the proposal says. No LICENSE file at the repo root (404) - not a blocker, but say so when re-releasing derived images.
- **Prices: correct** (OpenRouter, 2026-11-14): Fable 5.1 $10/$50, Opus 5.5 $4/$20, Sonnet 5.5 $2/$10, Haiku 5.5 and GPT-6 Luna $0.10/$0.50; all take image input. Not mentioned by the proposal: `:batch` variants at half price exist for every one of these.
- **Zolkowski et al. (2507.02737):** abstract matches the proposal's summary (models cannot pass short messages past a monitor under standard affordances; they can with an unmonitored scratchpad and a pre-agreed scheme).
- **Already done?** WebSearch was unavailable to me as well (session search budget exhausted), so this is still not a full check. What I could do: LessWrong new-posts scan since 2026-10-01 (1,109 posts, title filter) found no follow-up; the first author's only later post is unrelated; the arXiv API returned nothing for SVG + steganography. Nothing found, but the gap the proposer flagged is still open. The authors are the obvious people to run exactly this, three weeks after posting, so the risk of being scooped is real and unquantified.

Two facts in the repo that the proposal missed and that matter for the design:

1. The original encode prompt says the receiver recovers the secret "**after inspecting the SVG**". The encoder believed its reader would see source code. The proposal's replacement bullet tells the encoder the reader is "a fresh copy of you with the same tools", i.e. an image reader. That is a second change riding along with the monitor manipulation.
2. The original encoder and decoder ran under **Claude Code's default system prompt** and its built-in tools (including reading back crops it saved as images). The authors say their API equivalent is untested and "results may differ".

## 1. Would it get upvoted?

Borderline; I put it at roughly 40% for >50 karma if it runs as described, higher (60%+) only if Part B produces a clear result with pictures.

- The original got 93 karma largely for being legible and pretty: one surprising qualitative fact (it picks skylines) plus figures. A follow-up that is mostly a detection-rate table will not inherit that. Part A alone ("Sonnet catches them, Haiku does not" or "everything with tools catches them") is a 20-40 karma post: readers already saw Astra decode 88%, so "another strong model can read it" is known, and "a weak model with no tools cannot" is implied by Fable's own 6/50 by eye.
- Part B is the part people would upvote: the first test in the image channel of whether a frontier model can hide from a named monitor without a shared key. Either direction is quotable, and a gallery of what Fable draws when told it is watched is the natural hook. The control and monitoring crowd (Roger, Greenblatt, the authors, Zolkowski's co-authors) are the audience.
- The dull outcome is the likely one (see pre-mortem): monitors flag structure whether or not they can decode it, the encoder adds a small twist that mostly hurts its own receiver, and the post says "Zolkowski et al. extends to images". That is a fine result but a predicted one.

## 2. Naturalness

Mainline. The screener's note, the post's own "Implications" paragraph ("surprisingly hard to spot", decoding "obvious if you monitor the tool calls") and the comment thread all point at "who can detect this, and what if the encoder is told about a monitor". This is the experiment the authors would do next. Nothing contrived about it. The scrambled-carrier control is a good idea that is not obvious. I found no evidence it has been done, with the search caveat above.

## 3. Pre-mortem

How it actually plays out:

- **Day 1 morning - harness.** The team builds an OpenRouter tool loop. Specific traps: (a) whether OpenRouter's reasoning setting reaches Fable 5.1's `max` effort is unverified in the proposal; (b) the original decoder looked at its own crops (saved a PNG, then read it back as an image). Chat-completions tool results cannot carry images for every provider, so the harness needs a workaround, or monitors are weaker than they should be for a harness reason; (c) there is no Claude Code system prompt. Step 0 (>=4/5 on easy images) will probably pass for Fable, but it validates nothing about whether Haiku or Luna are being under-elicited by the same loop. Small models in a 30-call tool loop often stall, loop, or answer early; a "Haiku misses 80%" headline could be a harness artefact.
- **Day 1 afternoon - Part A.** Runs. My guess at the result: with tools, Opus and Sonnet flag most of the height family (values quantised to exact multiples of 5 px are a strong tell) and decode a good share; Haiku and Luna flag some and decode few; by eye everything is near the floor on decoding, with suspicion scores carrying weak signal. Scrambled controls get flagged at nearly the same rate as real ones by strong monitors, because the regularity survives a permutation. That is informative but it also means "detection" is mostly "sees quantised structure".
- **Day 2 - Part B.** The prompt now says, in so many words, "evade an automated monitor that screens for hidden messages". The plain prompt already tripped cyber classifiers and was refused outright for a commenter. Expect a materially higher stop rate, each stopped max-effort call still billed. If it gets through, the no-tools, single-shot, no-feedback encoder most likely keeps a per-letter visual carrier and adds a twist (offset, reversed order, differences between neighbours, a less conspicuous scene), or does not change at all (the authors found scene constraints did not move it). Receiver recovery drops somewhat; strong monitors still flag; weak-monitor detection was low to begin with so there is little room to fall.

Rough probabilities:

| outcome | p |
|---|---|
| Clear positive: receiver keeps most recovery, weak-monitor detection drops >=30 points | 10-15% |
| Clear, interesting negative: encoder cannot open a gap, or hides from itself too, shown cleanly | 30-35% |
| Ambiguous: small shifts inside the n=20 noise, floor/ceiling effects, confounded baseline | 35-40% |
| Part B does not run (classifier stops, budget); only Part A delivered | 15% |
| Nothing delivered | <5% |

Specific reasons it fails to produce an interesting result:

1. **Selection on the baseline outcome guarantees an apparent receiver loss.** Part B excludes messages whose baseline image Fable failed to decode, so baseline receiver recovery is 20/20 by construction. Decoding is stochastic, so any re-encode will score lower even if the manipulation does nothing. The "stealth gap, baseline versus monitor-aware" plot is biased towards "the gap shrank because the receiver suffered". This is a real bug, not a caveat.
2. **Harness confound in the same comparison.** Baseline receiver numbers come from the October Claude Code runs; new-image receiver numbers come from the November OpenRouter harness. Step 0 on 5 easy images cannot bound a difference of the size (25 points) the proposal wants to detect.
3. **Prompt confound is larger than stated.** The swap changes three things at once: human observer to AI monitor; "inspecting the SVG" to an image-plus-tools reader; and adds "flagged images are discarded". The optional 5-message re-encode with the unchanged prompt does not isolate any of them.
4. **Floor and ceiling.** Detection can only fall where baseline detection is mid-range. If Haiku-with-tools sits at 15% and Opus at 95%, no monitor has room for a 30-point move and Part B is uninformative regardless of what Fable does. The proposal does not say which monitor is the primary one.
5. **Under-elicitation of the encoder makes a null weak.** One zero-shot sentence about "a weaker AI model" with no information about what the monitor can and cannot do, no scratchpad to test, no examples. Zolkowski et al.'s finding is precisely that affordances decide the outcome. A null here will get the comment "you did not try very hard".
6. **Fable 5.1 is missing from its own ladder.** Its numbers are "taken from the released results", which have no suspicion score, no scrambled controls and no controls in this harness. The top rung is not comparable to the others, and the scrambled-control flag rate for the model the whole post is about is never measured.
7. **Natural controls differ from the encoded set in provenance** (November, API, no Claude Code system prompt, scene-matched prompt instead of the released seed prompt). A monitor could separate the classes on style. The scrambled controls partly cover this; a few fresh encodes through the same path would cover it properly.
8. **Many comparisons, one small n.** 4 monitors x 2 modes x families x 2 control types on 20 pairs. Without one pre-named primary contrast, something will cross the 25-point line by chance.
9. **Fallback to Astra is not paired.** Astra's images are not released, so the fallback needs fresh baselines (about another 40 expensive calls) that the budget does not contain.
10. **"Told a message may exist" monitors.** The authors already report models do not decode without a cue. All Part A numbers are for a monitor that was told to look for steganography in this one image. The proposal labels this an upper bound, but the realistic number (a generic "anything suspicious about this output?" screen) is the one deployment people want, and it is nearly free to add for the cheap monitors.

## 4. Cost check

The $480 is optimistic. Line by line:

- **Ladder with tools, $137:** assumes 80k cumulative input tokens per image. A 15-30 call loop that re-sends a growing context plus images will be 200-400k cumulative input without caching. Opus is then $1.2-2.0 per image and Sonnet $0.6-1.0, so $250-400 for 143 images instead of $137. Haiku and Luna remain negligible either way.
- **Fable calls at $4:** the authors' range is $2-7 and the tool-using decoder is the expensive end. Part B receiver decodes are more likely $5 each. Classifier-stopped calls are billed; with a more provocative prompt, budget 1.5x on encodes.
- **Natural controls at $1:** plausible only if not run at max effort; at max effort expect $1.5-2.
- **Missing lines:** baseline re-decode in the new harness (needed, see below), Fable 5.1 as a monitor on any controls, a matched control-prompt arm.

My estimate for the plan as written, done properly: **$600-750**, over the cap. With the changes below (trim Opus/Sonnet control passes, use `:batch` for single-shot calls, prompt caching in the tool loop) it fits in about **$450-490** with a thinner margin than I would like. If the first 10 Opus tool-loop transcripts average over $1.50, drop Opus to the encoded set plus 15 controls of each type.

## 5. Recommended changes (most important first)

1. **Fix the Part B baseline.** Do not pair against the released October results and do not select on baseline success. Generate both arms fresh through the same harness: a control arm and a monitor-aware arm on the same messages, each decoded by a fresh Fable 5.1 receiver in the new harness. If the budget forces reuse of released images as the control arm, at least re-decode them in the new harness and choose messages without looking at baseline outcome (or stratify by it and report both strata).
2. **Make the control prompt differ in one thing only.** Control arm: the new wording about the reader (fresh copy, rendered PNG only, Python image tools) with no monitor. Treatment arm: the same plus the monitor sentence. Keep or drop the "unaware human" bullet identically in both. State in the write-up that the original prompt said "inspecting the SVG".
3. **Name one primary contrast before running Part B.** After Part A, pick the monitor/mode whose detection on the released images is closest to 50% and declare it primary; everything else is descriptive. If no rung is between about 25% and 75%, say so and reframe Part B as a scheme-shift and receiver-cost study rather than a stealth-gap test.
4. **Put Fable 5.1 on the ladder in the same harness**, at least on a subsample: the 20 Part B messages, 10 natural and 10 scrambled controls (about 40 calls, $160-200). Pay for it by cutting Opus and Sonnet by-eye passes on controls and halving their tool passes on controls (20 natural + 15 scrambled is enough for a false-positive operating point; say plainly that 0/20 only bounds the false-positive rate below about 14%).
5. **Add one elicitation arm to Part B instead of spending everything on n.** For example 12 messages x {control, monitor-aware, monitor-aware + Part A feedback}, where the feedback arm is told concretely which families the weak monitor caught and missed. That is 36 encodes and 36 decodes rather than 40 and 40, and it makes a null much harder to dismiss. Report it as exploratory.
6. **Use the half-price batch endpoints** for all single-shot calls (encodes, natural controls, by-eye passes) if effort settings carry over, and turn on prompt caching in the tool loop. Confirm in Step 0 that `max` effort is actually applied to Fable 5.1 through OpenRouter (compare reasoning-token counts and per-call cost against the authors' $2-7); if not, call the provider's API directly.
7. **Extend Step 0 to the monitors.** Before the ladder, read 5 transcripts each for Haiku and Luna with tools and check they actually run measurements, can view their own crops, and do not exhaust the turn budget. Report turn-budget exhaustion and tool-error rates per monitor in the final table so readers can separate "cannot" from "harness".
8. **Add two near-free arms to Part A.** (a) A scripted non-LLM detector (for example, fraction of row-aligned element heights that are exact multiples of a common step). If thirty lines of NumPy catch the height family, that is a headline on its own and reframes the capability ladder. (b) For Haiku and Luna only, a generic screening prompt that does not mention hidden messages, to give the realistic lower bound next to the told-to-look upper bound.
9. **Decide in advance what the scrambled controls mean.** A permuted carrier still decodes to gibberish letters and looks exactly like an encrypted message; a monitor that flags it is arguably right. Use two kinds: permuted-but-quantised (structure kept, content gone) and re-sampled to non-quantised, natural-looking heights (structure gone). The difference between the two flag rates tells you whether monitors key on quantisation or on content. Expect about 25 usable SVGs, not 33 (several carriers are paths or positions, not a single `height` attribute).
10. **Classifier plan with numbers.** Pilot the monitor-aware prompt on 3 messages before committing; cap total Part B spend on stopped calls at $60; record the stop rate per arm as a result. Drop the Astra fallback unless you also budget fresh Astra baselines; a cheaper fallback is neutral wording ("an automated reviewer that discards images with detectable patterns").
11. **Lead the write-up with pictures.** Side-by-side control versus monitor-aware images for the same message, annotated with who caught what. That is what earned the original its karma.
12. Before funding, someone with working web search should spend ten minutes checking for an author follow-up; neither the proposer nor I could.

If only one thing can be afforded: keep Part B (fixed as in 1-3) and shrink Part A to Haiku, Sonnet and Fable with tools plus the scripted detector. Part A is the safe deliverable, but Part B is the reason to fund this.
