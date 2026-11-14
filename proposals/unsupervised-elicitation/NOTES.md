# NOTES — cluster `unsupervised-elicitation`

Research-lead reading notes and brainstorm, written 2026-11-14. Everything marked "verified" was looked up
in this session; everything else is recollection or inference and is marked as such.

## 1. What the two posts say (both read in full, plus all comments)

### Post 1 — "My unsupervised elicitation challenge" (DanielFilan, 2026-04-08, id ASoFTyk3bzBE62dyn)
- Task: a word-bank fill-in-the-blanks exercise from chapter 3 of an (unnamed) Ancient Greek textbook, typed
  as text. 24 blanks, simple sentences of the form "Α ___ ἐστίν", word bank given in dictionary form.
- Claim: Claude Opus 4.6 does not get it fully right by default, but can fix its errors when given
  "somewhat-specific hints". Challenge: get Opus 4.6 to a fully correct answer without knowing Greek or the
  answers. Rules of spirit: no telling Claude the success rate, no feeding in known-wrong answers, no pasting
  the answer; putting whole textbooks in context is allowed.
- Things he tried that failed: "you tend to make mistakes, double-check" (better, not perfect); attaching a
  textbook PDF (Claude did not open it).
- $100 + textbook prize added 2026-04-18; expired.
- Comments (verified via GraphQL): about 20 public attempts, all marked wrong for Opus 4.6. Notable: Ryan
  Greenblatt ran his agent orchestrator with Opus 4.6 at two compute settings (Filan says about $100 of
  tokens) and both were wrong; Thomas Kwa spent 2 hours and, even after being told the answer, "still [did
  not] know how to construct a scaffold that would generalize to other problems like this"; other attempts:
  lecturer persona, rank-top-4-then-choose, "accountability buddy" with Python scripts, conversing in Greek
  first, translating the instructions into Greek, "act on instinct / repeat question four times", asking
  other Claude instances to verify (they agree wrong answers are right). A Gemini 3.1 Pro attempt was also
  wrong on at least one slot (σύμφωνα εἰσιν).
- The public failed attempts show the error pattern clearly: models write "γράμματα εἰσιν", "σύμφωνον ἐστιν",
  "δίφθογγος ἐστιν", "ὄνομα ἐστιν", and sometimes "Ἑλληνικόν γράμμα" (acute not turned grave), while the
  exercise text itself contains correct instances ("γράμματά εἰσιν", "ὄνομά ἐστιν").

### Post 2 — "Retrospective on my unsupervised elicitation challenge" (2026-04-27, id aJ3NTJ6tM7yc49kQn)
- The secret is accent sandhi: (1) final acute becomes grave before a following word; (2) before enclitic
  ἐστι(ν)/εἰσι(ν): word with final circumflex unchanged; word that "can fit" an acute on its final vowel gets
  one (νῆσός ἐστιν); otherwise the enclitic takes an acute on its last syllable (λόγος ἐστίν), which itself
  turns grave if another word follows.
- Evidence the knowledge is latent in Opus 4.6: (a) repeated prodding eventually gets it right; (b) strongest:
  translate the passage to English and have Opus 4.6 translate back to Greek, and it gets all accents right
  (but then fails a different thing: οὐκ → οὐχ before rough breathing).
- "A bit over 20 submissions"; no Opus 4.6 submission succeeded. Typical strategies: double-check / look for
  mistakes; generate many attempts and pick the best. His impression: these did on average *worse* than the raw
  prompt with extended thinking. "Opus 4.6 is somehow near-blind to naming accents as a thing to check, and
  never generates the correctly accented answers for some words."
- Partial credit: the gears to ascension, after being told the answer, got one non-cheating-seeming Opus 4.6
  run right by stressing a huge token budget and an "arbitrarily adversarial, maximally strict" grader.
- Untried strategies he thinks would work: (i) fill, translate to English, translate back, use that to fill;
  (ii) have Claude teach you the first chapters of a textbook.
- Opus 4.7 with adaptive thinking one-shots it (without thinking it fails). GPT-5.4 Pro with extended thinking
  one-shot it with a slightly reformatted word list. His guesses for why 4.7 works: new tokenizer, or
  generally smarter. Hypothesis for 4.6's failure: it is in "English speaker learning Ancient Greek" mode.
  "If I had an infinite budget for computation, I might wish to know which of these effects dominated."
- Comment by Rob Kopel (12 karma): compared Opus 4.6 and 4.7 tokenization of the exercise; Greek segmentation
  is basically identical; the one clear difference is that 4.7 tokenizes the blank marker `___` as one token
  while 4.6 splits it into `" _"` + `"__"`. So the "accent tokenization" hypothesis looks unsupported and a
  "blank marker" hypothesis is open and untested.
- Author-suggested follow-ups (explicit):
  1. New one-shot unsupervised elicitation challenges "in other languages (or even in Ancient Greek)" with a
     hard-to-foresee trick.
  2. A held-out test exercise testing accentuation (among other things), with scaffolds/prompts that must
     generalise to it on Opus 4.6 without cheating. He is "not up for taking this on, but would cheer on
     someone else who did".
  3. Footnote: whether similar generational improvements exist in other low-resource languages using
     diacritics (he noticed 4.7 is better at Latin vowel-length marks).
  4. Which of tokenizer vs general capability explains 4.7.

## 2. Related work and what already exists (searched 2026-11-14)
- No follow-up to the challenge found (WebSearch on LessWrong/AF/arXiv; arXiv API query for "unsupervised
  elicitation" returned nothing new beyond the items below). No held-out benchmark, no systematic scaffold
  comparison, no cross-language replication. The only empirical follow-up is Kopel's tokenizer comment.
- Wen et al., "Unsupervised Elicitation of Language Models" (arXiv 2506.10139; v2 dated 2026-01-26), Internal
  Coherence Maximization (ICM): searches for a mutually-predictable, logically consistent labelling of a
  dataset. Needs many items and label logprobs/fine-tuning, so it does not apply directly to a one-shot
  generation task on a closed model. Official code is linked from alignment.anthropic.com/2025/unsupervised-elicitation
  (I believe github.com/Jiaxin-Wen/Unsupervised-Elicitation; github.com returned 403 through this proxy so
  the URL is NOT verified). Third-party reimplementation: github.com/codelion/icm (from a Hugging Face blog
  post; not verified).
- Canavan, Shrivastava, Qi, Michala, Roger, "Three Concrete Challenges and Two Hopes for the Safety of
  Unsupervised Elicitation" (arXiv 2602.20400, 2026-02-23; verified abstract): standard UE and easy-to-hard
  techniques fail when a feature more salient than truth exists, when training sets are imbalanced, or when
  items lack well-defined answers. Classification-probe setting on open models, not naturalistic generation.
- Net: the Filan task is, as he says, an unusual naturalistic case of "knows but does not use". Nothing public
  measures how general the phenomenon is or which answer-blind procedures fix it.

## 3. Verified resources and prices
- OpenRouter (curl of /api/v1/models, 2026-11-14), USD per million tokens input/output:
  - anthropic/claude-opus-4.6: 5 / 25 (":batch" variant 2.5 / 12.5). **Still served**, which is essential.
  - anthropic/claude-opus-4.5 5/25; claude-opus-4.7 5/25; claude-opus-4.8 5/25; claude-opus-5 5/25;
    claude-opus-5.5 4/20; claude-sonnet-4.6 3/15; claude-sonnet-5.5 2/10; claude-fable-5.2 8/40.
  - openai/gpt-5.4 2.5/15; gpt-5.4-pro 30/180 (too expensive to use); gpt-5.6-sol 4/20.
  - google/gemini-3.1-pro-preview 2/12; gemini-3.8-flash 0.825/4.125.
  - Thinking tokens are billed as output; whether OpenRouter exposes Opus 4.6 extended thinking and Opus 4.7
    adaptive thinking exactly as claude.ai does must be checked on day 1 (use the `reasoning` parameter).
- PyPI `greek-accentuation` 1.2.0 (jtauber, MIT): syllabification, accent classification (oxytone,
  paroxytone, proparoxytone, perispomenon, properispomenon), adding/removing accents. Verified on PyPI.
- PyPI `vidyut` 0.4.0 ("A high-performance Sanskrit toolkit"). Verified to exist; whether the Python binding
  exposes the sandhi module was NOT checked.
- Hugging Face dataset `universal-dependencies/universal_dependencies` (verified, 350 configs) includes
  grc_perseus, grc_proiel, grc_ptnk (Ancient Greek, polytonic FORM + LEMMA), cy_ccg (Welsh), ga_idt, ga_cadhan
  (Irish), gd_arcosg (Scottish Gaelic), br_keb (Breton), gv_cadhan (Manx), sa_ufal, sa_vedic (Sanskrit).
  From memory (not re-checked): Celtic treebanks annotate mutations in FEATS (Welsh `Mutation=SM|NM|AM`,
  Irish `Form=Len|Ecl|HPref`). raw.githubusercontent.com is reachable (UD_Ancient_Greek-PROIEL README 200).
- github.com HTML pages return 403 through this proxy; that says nothing about whether repos exist.
- Unicode trap for any grader: Greek acute exists as tonos (U+03AC etc.) and oxia (U+1F71 etc.); NFC maps
  oxia to tonos. Apostrophe/koronis variants also differ. Normalise before comparing.
- No session API key was available, so I ran no model calls. The Opus 4.6 baseline failure rate on new
  exercises is therefore unmeasured; both proposals make it the first gate.

## 4. Brainstorm (all candidates, with verdicts)

A. **Held-out accent-cloze benchmark + answer-blind scaffold tournament on Opus 4.6** (Filan's follow-up 2).
   Gold is computable by rule and checkable against treebanks, so agents need no Greek. Cheap ($300-450).
   Directly answers "does any general procedure work?", which 20+ people and a $100 Redwood run could not.
   Interesting both ways. **Proposal 01.**

B. **Cross-language search for new "knows but does not use" cloze tasks at the current frontier** (Filan's
   follow-ups 1 and 3). Treebank-derived gold for Celtic mutations, Greek sandhi, Sanskrit sandhi. Tests his
   "capabilities progress will solve this" reading. Null is less exciting but informative. **Proposal 02.**

C. Why does Opus 4.7 succeed (tokenizer vs capability; blank marker `___`)? Cheap, but as a standalone it is
   narrow; cannot be answered cleanly for closed models. Folded into 01 as a blank-marker ablation and a
   model-generation sweep. Rejected as standalone.

D. Why does Opus 4.6 fail: "learner mode" vs copy-bias from the word bank. Good mechanism question; folded into
   01 as ablations (bank with accents stripped, bank in English glosses, native-framing prompt). Rejected as
   standalone because it overlaps with 01 too much to be a distinct project.

E. White-box study on an open-weight model with the same cloze-vs-compose gap (probe for "the accent rule is
   represented but not used"). Attractive, but requires first finding an open model that both knows polytonic
   sandhi and fails the cloze; likely none do at 2-day reach, and the search alone could eat the budget.
   Candidate stage 2 for 02 if an open model shows a gap in some language. Rejected for stage 1.

F. Run ICM / consistency-based unsupervised fine-tuning on the task via Tinker. Mismatch: ICM labels
   classification items; here the failure is a generation-format effect on a closed model, and open models
   probably lack the knowledge. Rejected.

G. Re-run the original challenge with more exotic human-style prompts. Already done by about 20 people with a
   single item and no grader; adds nothing without the held-out set. Subsumed by A.

H. Agentic "learn the language then check" scaffold only (Filan's untried idea ii). One arm of A; standalone it
   is one data point.

I. Human-study version (can non-Greek-speakers elicit?). Needs human subjects. Rejected.

J. Sycophancy angle from post 1 (grading the user's answers vs writing its own). Tangential to the cluster's
   point and well covered elsewhere. Rejected.

K. Latin macron detection (footnote 3). Vowel length is lexical, not contextual, and gold needs a macronised
   lexicon; less clean than sandhi. Could be one extra language in B; left out of stage 1.

## 5. Why two proposals and why they are distinct
01 holds the model and phenomenon fixed (Opus 4.6, Greek accents) and varies the elicitation procedure.
02 holds the procedure fixed (plain cloze vs knowledge probes) and varies language and model to find where
the gap lives now. 01 can succeed even if every newer model is at ceiling; 02 can succeed even if no scaffold
works. Shared risk: gold-label correctness without a human expert. Both handle it by validating against
human-edited treebanks rather than trusting a model.
