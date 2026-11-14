# Feedback: A held-out Greek accent benchmark (proposal 01, cluster unsupervised-elicitation)

Verdict: **keep, with tweaks**. It is the follow-up the author asked for and it is cheap, but three things need fixing before it is funded: the treebank validation gate fails as written (I ran it), the "answer-blind" arms are not blind, and the cost of the agentic arms is underestimated.

## What I checked

| Claim | Status |
|---|---|
| Prior-work summary (24 blanks, accent sandhi, >20 submissions, $100 prize, 4.7 one-shots with adaptive thinking, untried ideas, held-out test proposal, "would cheer on") | Confirmed against both posts' full text. |
| Greenblatt orchestrator run, about $100 of tokens, both settings wrong | Confirmed (his comment 2026-04-09 plus Filan's comment). |
| Thomas Kwa quote | Confirmed (comment 2026-04-13). |
| Kopel tokenizer comment, `___` one token in 4.7 and two in 4.6 | Confirmed (12 karma, 2026-04-28). |
| OpenRouter serves `anthropic/claude-opus-4.6` at $5/$25, `:batch` at $2.5/$12.5 | Confirmed today via `/api/v1/models`; `reasoning` is a supported parameter. Opus 4.5/4.7/4.8/5, Sonnet 4.6, GPT-5.4, Gemini 3.1 Pro preview are all listed at the stated prices. |
| `greek-accentuation` 1.2.0, MIT | Confirmed on PyPI; installs and syllabifies polytonic text. |
| UD treebanks public | Confirmed: `grc_proiel` and `grc_perseus` train files download from raw.githubusercontent.com. |
| "Gold-label engine (built, about 150 lines)", "Exercise generator (built)" | **Not supported.** No code exists in the repository, and NOTES.md says no model calls were run. Read "built" as "to be built". The proposal should say so. |
| Not already done | Partly checked. arXiv API ("unsupervised elicitation"; Ancient Greek + accent/enclitic; polytonic + LLM) returns nothing relevant beyond Wen et al., Canavan et al. and an unrelated moral-values paper (2601.17728). The retrospective has no pingbacks except the original post, and its only substantive comment is Kopel's. **WebSearch was unavailable to me (session search budget exhausted)**, so I did not search Twitter/X, blogs or GitHub; Filan's own blog was not checked. |

## 1. Would it get upvoted?

Borderline, around 40-70 karma if it works; I would put about 50% on clearing 50.

- The source posts got 51 and 59. A follow-up to a 59-karma post about a single homework exercise, on a model four generations old (Opus 4.7, 4.8, 5 and 5.5 are all on the price list), starts with a low ceiling. Readers' default reaction will be "capabilities fixed this in a week, why do we care about scaffolding 4.6".
- What could lift it: Filan explicitly asked for this and would likely engage and endorse; Greenblatt and Kwa put in effort and failed, so a clean answer to "would anything general have worked?" has a ready audience among elicitation and control people. A released grader that others can submit scaffolds to gives the post a second life.
- The piece most likely to be remembered is not the 12-arm table but the mechanism ablations (accent-stripped bank, English-gloss bank, blank marker). "It is copy bias from the word bank" or "it is not" is a crisp, quotable finding. The proposal treats these as a side dish.
- The clear-negative outcome ("nothing works, n = 30") is the least upvotable version: it confirms what Filan already wrote.

## 2. Naturalness

Mainline. This is follow-up 2 in the retrospective, almost verbatim, and it folds in follow-up 4 (tokenizer vs capability) and the "learner mode" hypothesis. I found no evidence anyone has done it, with the search caveat above.

One departure from what Filan asked for: he imagined a privately held test exercise that *other people's* scaffolds are run against. Here the same team writes the grader, the exercises and the scaffolds, all knowing the secret. That changes what the result means (see pre-mortem item 2).

## 3. Pre-mortem

Forecast: clear positive 25%, clear and interesting negative 20%, ambiguous mush 40%, fails to run or is invalidated by a grader bug 15%.

How it plays out, and where it breaks:

1. **The treebank gate fails as specified.** I implemented the textbook enclitic rule with `greek-accentuation` syllabification and compared it with attested forms before ἐστι(ν)/εἰσι(ν) in the UD train files (elided words and punctuation excluded):
   - `grc_proiel` overall: 78% agreement (n = 991). By source: Greek New Testament 93% (n = 713), Herodotus 41% (n = 278).
   - `grc_perseus`: 73% (n = 221).
   - The disagreements are not engine bugs. The Herodotus edition routinely prints forms like ἄριστον ἐστί, σῶμα ἐστί, οὗτος ἐστὶ (enclitic accented, no second accent on the host), there are graves before enclitics (μὲν ἐστὶ), orthotone ἔστι after οὐκ/μή, and εἶσι ("will go") collides with εἰσι once accents are stripped.
   - Consequence: "at least 98% agreement" is unreachable on the raw treebanks. Agents will either burn half a day explaining disagreements, or tune the engine until it matches an idiosyncratic edition and then grade Opus against the wrong convention. The gate must name the subcorpus (NT only, or a specific Attic prose text), exclude proclitic and enclitic hosts, and set the threshold after those exclusions.
   - The same problem affects the grave rule: editions differ on grave versus acute before a comma.

2. **"Answer-blind" is not blind.** The arm prompts are written by agents who have read the retrospective and know the trick. "List every way a word's written form can depend on its neighbours" is a hint with the word "accent" removed; the string check on "accent/enclitic/diacritic" does not address this. Kwa's point was precisely that knowing the answer did not tell him what would *generalise*. If the checklist arm wins, a sceptical reader says "you wrote the prompt backwards from the answer". The only defence is a second phenomenon the arms were not designed around, and the proposal defers that to stage 2.

3. **Headroom may be small.** On the original exercise Opus 4.6 gets most accents right (ἀλλὰ always; some enclitic cases). Synthetic 10-12-blank exercises probably land at 75-90% sandhi-slot accuracy by default, and errors concentrate in one or two classes (proparoxytone and properispomenon hosts). If default is 85% and the hinted ceiling 96%, the gap is 11 points, a "60% closed" arm is a 6-7 point effect, and slot errors are correlated within word class and exercise. With 30 exercises and two seeds that is detectable for the best arm but most of the 12 arms will have overlapping intervals. This is the main route to mush.

4. **The translation ceiling is not on "the same slots".** A free translation changes word choice and order, so slot alignment is undefined. Filan also reports it fails a different rule (οὐκ/οὐχ) in that mode. The ceiling needs a text-level checker (score every host-plus-enclitic and every final-acute-plus-word pair that appears in the output), not gold-string comparison.

5. **Gold is not unique in a cloze.** Several bank words can fit a blank, and Greek word order is free. A grader that compares against one gold string will mark a valid different word choice as an accent error. Grade accent correctness conditional on the word the model actually chose.

6. **Generated Greek must itself be right.** Agents composing copular sentences from treebank lemmas have to get gender/number agreement and the correct isolated accent for inflected forms (plural -α, -οι, -αι change accent class). Treebank attestation of the lemma does not give the inflected form's accent. Restrict to attested inflected forms and to templates lifted from the original exercise.

7. **Elicitation setting differs from the original.** Filan's observations are from claude.ai (system prompt, its own thinking budget). Via OpenRouter there is no system prompt and the thinking budget is a free parameter that could move the baseline a lot. The day-1 check (ten runs of the original exercise) is the right step; the plan should fix one budget and report sensitivity to it, since "large token budget" is itself one of the arms.

8. **Selection among 12 arms on 30 exercises.** Reporting the best arm's gap-closed without correction overstates it. A fresh confirmation set for the top two arms fixes this cheaply.

9. **Unsurprising either way?** Partly. Filan already predicted that round-trip translation and curriculum recall would work and that double-check and sample-select would not. If the result matches, the novelty is the numbers and the ablations.

Things I am not worried about: model availability (verified), infra (single API, no GPU), two-day feasibility (fine if the engine is scoped down).

## 4. Cost check

The per-call price arithmetic is right ($0.106 for 1.2k in / 4k out). The call counts for agentic arms are optimistic:

- "Large token budget, strict grader" arm is designed to use far more than 4k output tokens; at 20-40k tokens it is $0.50-1.00 per run, $30-60 for 60 runs.
- Orchestrator with sub-calls and a Python tool: realistically 8-20 calls per run, $1-2 per run, $60-120 for 60 runs. (Greenblatt spent about $100 on two runs of one exercise.)
- Three-round self-critique and debate re-send growing context; 2.7 calls average is low for these.
- Extended thinking on a 12-blank exercise may exceed 4k tokens on its own; measure on day 1.

My estimate for the plan as written: **$450-650**, so it is at or over the $500 cap. With the cuts below (orchestrator arm capped or dropped, generation sweep reduced, batch pricing for single-call arms) it fits in **$300-400**. The `:batch` variant exists at half price; whether it honours `reasoning` needs a one-call check.

## 5. Recommended changes (in order of importance)

1. **Fix the gold-label validation.** Validate on the NT portion of `grc_proiel` only (or one named Attic prose text), excluding elided hosts, proclitic/enclitic hosts, and orthotone ἔστι; drop Herodotus and the poetry-heavy Perseus files. State the expected agreement after exclusions and have the disagreement list read. Remove "(built)" from steps 1 and 2 unless code is attached.
2. **Add a held-out second phenomenon to stage 1** so "answer-blind" means something. The cheapest is already in the engine: οὐ/οὐκ/οὐχ before smooth/rough breathing, which Filan says Opus 4.6 gets wrong. Movable nu or elision are alternatives. Freeze all arm prompts on accent dev exercises, then run the same prompts unchanged on exercises that test only the second phenomenon. Describe the arms honestly as "written with knowledge of the accent answer; blind with respect to phenomenon B".
3. **Grade with a text-level sandhi checker**, conditional on the words the model chose, and use it for the cloze, the translation ceiling and every arm. Report exact-gold match only as a secondary metric.
4. **Promote the mechanism ablations to co-headline** and run them first after the gate: accent-stripped bank, English-gloss bank, bank already in sandhi-neutral form, blank-marker swap. They cost about $20 and give the most quotable result. Add one more: the same sentences as a no-bank cloze (free fill), which separates "copying from bank" from "cloze format".
5. **Cut the arms to 7-8** to buy power: default, double-check, majority vote, round-trip translation, curriculum recall, composition reframing, context-dependence checklist, strict-grader/large-budget. Drop or hard-cap (at $40) the orchestrator arm; drop debate and the Greek-instructions arm unless budget remains. Spend the savings on 3 seeds and a fresh 15-exercise confirmation set for the top two arms.
6. **Tighten the reproduction gate.** Require a ceiling-minus-default gap of at least 12 points on sandhi slots, not just default below 85%. If the gap is smaller after the harder-slot fallback, stop and write up the ablations plus the generation sweep as a short post, or redirect the remaining money to proposal 02.
7. **Shrink the generation sweep** to Opus 4.5, 4.6, 4.7 and one current model, default cloze only, with and without thinking. The 4.6-to-4.7 step with the blank-marker ablation is the informative part; seven models times two conditions is padding.
8. **Fix the thinking budget** up front, report one sensitivity point (half and double), and record that the setting is API-without-system-prompt, not claude.ai.
9. Send the exercises and grader to Filan before the test run, not on release; a single wrong convention found afterwards would sink the post.
