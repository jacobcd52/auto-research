# A held-out Greek accent benchmark: does any answer-blind scaffold recover what Opus 4.6 knows?
cluster: unsupervised-elicitation | stage-1 cost: $440 | follows up: My unsupervised elicitation challenge (ASoFTyk3bzBE62dyn); Retrospective on my unsupervised elicitation challenge (aJ3NTJ6tM7yc49kQn)

## 1. What the prior work showed
Daniel Filan found a naturalistic task where a model "knows but does not use": a 24-blank word-bank exercise from chapter 3 of an Ancient Greek textbook. Claude Opus 4.6 picks the right words but leaves them in dictionary form where Greek requires the accent to change with context (final acute becomes grave before another word; a word before enclitic ἐστιν/εἰσιν gains a second accent, e.g. γράμματά εἰσιν, or the enclitic takes one, e.g. λέξις ἐστίν). The knowledge is latent: Opus 4.6 fixes the errors when prodded specifically, and gets every accent right when it translates the same passage from English into Greek.

The challenge was to elicit a fully correct answer without knowing Greek. A bit over 20 submissions, a $100 prize, and an agent-orchestrator run by Ryan Greenblatt (about $100 of tokens) all failed on Opus 4.6. Filan's impression was that double-checking and sample-then-select scaffolds did worse than the raw prompt with extended thinking. Thomas Kwa, after learning the answer, still could not see how to build a scaffold that would generalise. Opus 4.7 with adaptive thinking one-shots the task. A commenter (Rob Kopel) showed that 4.6 and 4.7 tokenize Greek the same way; the one difference is the blank marker `___` (one token in 4.7, two in 4.6).

Everything above rests on one exercise, graded by hand by one person, with success defined as all 24 blanks right. Filan proposed a held-out test exercise on which scaffolds must generalise without cheating, said he would not build it, and said he would cheer on whoever did. My searches (LessWrong, Alignment Forum, arXiv, 2026-11-14) found no such benchmark and no systematic comparison. Existing unsupervised-elicitation work (Wen et al., arXiv 2506.10139; Canavan et al., arXiv 2602.20400) studies classification labels on open models, not format-locked generation in a frontier model.

## 2. Question and why it matters
On held-out exercises with an automatic grader, does any domain-general, answer-blind procedure close the gap between what Opus 4.6 writes in a cloze and what it demonstrably knows?

If some generic scaffold closes most of the gap (for example "list every way a word's written form can depend on its neighbours in this language, then check each slot"), the challenge was hard because of single-item, no-feedback conditions, and we get a concrete recipe to test elsewhere. If nothing short of pasting the rules works across 30 exercises and a dozen procedures, that is a clean, quantified existence proof that current unsupervised elicitation tooling fails on a naturalistic task, and the paired ablations say why. Both outcomes replace an anecdote with numbers.

## 3. Stage 1 plan
Model under study: `anthropic/claude-opus-4.6` on OpenRouter (verified still served), extended thinking on.

1. **Gold-label engine (built, about 150 lines).** Use PyPI `greek-accentuation` 1.2.0 (MIT) to classify each word's accent type, then implement the grave rule, the enclitic rules for ἐστι(ν)/εἰσι(ν), and οὐ/οὐκ/οὐχ. Validate against human-edited text: in the Ancient Greek Universal Dependencies treebanks (`grc_perseus`, `grc_proiel` in the Hugging Face dataset `universal-dependencies/universal_dependencies`), take every word followed by an enclitic form of εἰμί, predict its surface form from its isolated form, and compare with the attested form. Gate: at least 98% agreement, with disagreements read and explained. All comparisons use Unicode NFC (tonos and oxia acutes are different code points).
2. **Exercise generator (built).** Thirty-six exercises in the style of the original: 10-12 blanks, simple copular sentences, word bank in dictionary form. Sentences are composed from a vocabulary of about 120 nouns and adjectives drawn from the treebanks (so isolated forms are attested), covering all five accent classes. Each exercise mixes sandhi-sensitive slots (about 70%) with slots needing no change. Six exercises are a dev set; 30 are test and are not looked at during prompt writing. Filan's original exercise is kept as a 37th item for continuity.
3. **Gate: reproduce the phenomenon.** Five default samples per test exercise. Proceed only if Opus 4.6's accuracy on sandhi slots is below 85% and fewer than 30% of exercises are fully correct. If not, switch the generator to harder slots (proparoxytone and properispomenon words before enclitics, where public failed attempts concentrate).
4. **Measure the knowledge ceiling** on the same slots: (a) English-to-Greek translation of the completed passage; (b) the cloze with a targeted hint ("check enclitic accentuation"); (c) the rules pasted in (the cheating upper bound).
5. **Scaffold tournament.** Twelve answer-blind arms, prompts frozen on the dev set, two seeds each on 30 test exercises:
   default; "double-check"; five-sample per-slot majority vote; self-critique loop (3 rounds); two-agent critic/debate; round-trip translation (Filan's untried idea); curriculum recall ("summarise what the first five chapters of a standard textbook teach, then apply all of it", his second idea); context-dependence checklist; task reframing as composition (produce the finished text; the bank is only a hint); instructions in Greek with a native-scribe framing (tests his "learner mode" hypothesis); the strict-grader, large-token-budget prompt that earned partial credit; Opus 4.6 as orchestrator of sub-calls with a Python tool.
6. **Three mechanism ablations** on the default prompt: blank marker `___` replaced by `[…]` or a numbered gap (Kopel's observation); word bank with accents stripped; word bank given as English glosses. The last two test whether the failure is copying from context.
7. **Generation sweep.** Default cloze and translation condition on Opus 4.5, 4.7, 4.8, 5, Sonnet 4.6, GPT-5.4 and Gemini 3.1 Pro, two seeds, to show whether the gap closes monotonically.

Metrics: sandhi-slot accuracy; share of exercises fully correct; "gap closed" = (arm − default) / (hinted ceiling − default), with bootstrap confidence intervals over exercises and paired comparisons per slot. Error taxonomy by accent class.

## 4. Stage 1 cost estimate
Assumed per Opus 4.6 call: 1.2k input and 4k output tokens including thinking (polytonic Greek is about one token per one to two characters). At $5 / $25 per million tokens that is $0.106.
- Baseline gate and vote arm: 30 × 5 = 150 calls, $16.
- Ceiling probes: 30 × 3 × 2 = 180 calls, $19.
- Tournament: 11 remaining arms × 30 × 2 seeds = 660 runs, averaging 2.7 calls, about 1,780 calls, $189.
- Ablations: 3 × 30 × 2 = 180 calls, $19.
- Generation sweep: 7 models × 30 × 2 conditions × 2 seeds = 840 calls at $0.04-0.11, about $70.
- Dev-set iteration and prompt debugging: $30.
- Subtotal $343; 28% margin for reruns: **$440**. No GPU needed. OpenRouter lists a half-price `:batch` variant for Opus 4.6 ($2.5 / $12.5); if it supports thinking, the single-call arms drop by about $60.

## 5. What success looks like
A table of 12 arms with gap-closed and confidence intervals, plus the ceiling rows. Clear positive: one or more answer-blind arms close at least 60% of the gap with intervals excluding zero, and we can say what they have in common. Clear negative: no arm closes more than 25%, while the hint and translation conditions sit near 95%; this confirms Filan's single-item impression at scale and is publishable as "a naturalistic task where unsupervised elicitation fails, now with a public grader". The ablations add a mechanism claim either way (for example "stripping accents from the bank removes half the errors, so this is copy bias, not missing effort"). An ambiguous outcome is every arm giving 30-50% with overlapping intervals; then the post leads with the ablations and the generation curve. The engine, exercises and transcripts are released so others can submit scaffolds.

## 6. Stage 2 (if stage 1 succeeds)
Test the winning scaffold (or the confirmed failure) on a second phenomenon and language where a current frontier model has a measured gap, to see whether the recipe transfers. Open a public leaderboard with a fresh hidden test set generated from a new seed. About $400-600.

## 7. Risks and how the plan handles them
- **Wrong gold labels with no Greek speaker in the loop.** The treebank validation gate is the defence; slots where engine and attested usage can differ (ἔστιν after οὐκ, sentence-initial forms, elision) are excluded from generated exercises. The exercises are sent to Filan on release for a spot check.
- **Synthetic exercises do not reproduce the failure.** Checked at step 3 for $16 before anything else is spent.
- **Thinking controls on OpenRouter differ from claude.ai.** Verify on day 1 that reasoning tokens are returned and billed; run the original exercise ten times to confirm the documented failure pattern.
- **Prompt overfitting.** Dev/test split; prompts frozen and hashed before the test run; arm list fixed in advance here.
- **Arms "cheat" by accident.** A scaffold prompt may not mention accents, enclitics or diacritics; an automated string check enforces it.
- **Small n over-claiming.** The unit of analysis is the exercise (n = 30), with about 240 sandhi slots per arm per seed; only paired differences with intervals are reported.
