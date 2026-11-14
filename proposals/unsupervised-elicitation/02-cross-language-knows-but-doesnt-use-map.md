# Did capability progress fix it, or move it? Mapping "knows but does not use" cloze gaps across languages at the frontier
cluster: unsupervised-elicitation | stage-1 cost: $380 | follows up: Retrospective on my unsupervised elicitation challenge (aJ3NTJ6tM7yc49kQn); My unsupervised elicitation challenge (ASoFTyk3bzBE62dyn)

## 1. What the prior work showed
Daniel Filan's challenge used one Ancient Greek word-bank exercise. Claude Opus 4.6 chose the right words but left them in dictionary form where context requires a changed accent (for example γράμματα instead of γράμματά before εἰσιν). It could produce the right forms when hinted, and when translating the passage from English. Over 20 attempts to elicit a correct answer without knowing Greek failed. Then Opus 4.7 with adaptive thinking simply solved the exercise, GPT-5.4 Pro did too, and the challenge was retired.

Filan drew two lessons. First, this was an alignment failure that looks like a capability failure, which is "why one might think that such issues will be solved by continuing capabilities progress". Second, he remains interested in new one-shot challenges: "My assumption is that it is possible to come up with this sort of thing in other languages (or even in Ancient Greek), and would be excited about people doing so." A footnote asks whether newer models improved similarly in other low-resource languages with diacritics. He also noted he is "unaware of other tasks" with a strong case that a model fails by default but could succeed.

Nobody has looked. My searches on 2026-11-14 (LessWrong, Alignment Forum, arXiv) found no replication in another language, no measurement on any model after Opus 4.7, and no second example of the phenomenon. The only follow-up is a comment showing Opus 4.6 and 4.7 tokenize Greek alike.

## 2. Question and why it matters
For today's frontier models, in which languages (if any) is there a large gap between accuracy on context-dependent word forms in a word-bank cloze and accuracy on the same forms when the model's knowledge is probed directly?

The Greek exercise has one structural feature: the word bank supplies a citation form, and the correct answer requires altering it because of a neighbouring word. Many languages have this property, and several have public human-annotated corpora that give the right answer without a human expert. If the gap has vanished everywhere at the frontier, Filan's optimistic reading holds for this failure class, and that is worth knowing, though a less exciting post. If the gap reappears in lower-resource languages (Welsh, Irish, Scottish Gaelic, Breton mutations; Sanskrit sandhi; harder Greek), then capability progress moved the boundary without removing the phenomenon, and the output is a set of fresh challenge tasks meeting his three criteria: naturalistic, model demonstrably knows, most researchers cannot check by eye.

## 3. Stage 1 plan
**Data (reused).** The Hugging Face dataset `universal-dependencies/universal_dependencies` (verified to include the configs below). Each token has a surface FORM and a LEMMA, so "citation form in the bank, attested form as gold" comes from human annotation.
- Ancient Greek (`grc_perseus`, `grc_proiel`): words before enclitics; final acute to grave; οὐ/οὐκ/οὐχ; elision.
- Welsh (`cy_ccg`), Irish (`ga_idt`), Scottish Gaelic (`gd_arcosg`), Breton (`br_keb`): initial consonant mutations triggered by the preceding word (Welsh ei gath / ei chath, Irish lenition and eclipsis).
- Sanskrit (`sa_ufal`, `sa_vedic`): external sandhi at word boundaries, if the treebank's surface forms keep sandhi; decided in the pilot.
A language is dropped in the pilot if clean slot extraction fails; four surviving languages are enough.

**Item construction (built, mostly filtering code).** For each language, extract slots where the attested form differs from the citation form only by the contextual phenomenon (same case and number, so morphology is not being tested). Build 40 exercises per language, each a 6-8 sentence passage with 8 blanks: about 5 contextual slots and 3 no-change controls. The bank lists the citation forms, shuffled. To limit recall of memorised text (Homer, the Bible), prefer the modern-text treebanks for Celtic languages, and for Greek and Sanskrit swap a content word elsewhere in each sentence for a same-class synonym and report results with and without that perturbation.

**Models.** `anthropic/claude-opus-5.5`, `openai/gpt-5.6-sol`, `google/gemini-3.1-pro-preview`, all with reasoning enabled. `anthropic/claude-opus-4.6` on Greek only, as a positive control that the pipeline detects the known gap.

**Conditions per exercise (two seeds each).**
1. Cloze, default: Filan's original wording ("write out the answers to this fill-in-the-blanks exercise so I can check mine").
2. Cloze, hinted: one extra sentence naming the phenomenon ("mind initial mutations").
3. Isolated knowledge probe: for each contextual slot, a direct question giving the two neighbouring words and asking for the correct written form.

**Analysis.** For each model and language: contextual-slot accuracy under each condition; the latent gap = min(hinted, isolated) − default, with bootstrap intervals over exercises; control-slot accuracy to show errors are specific. Slots where the model fails the knowledge probes are reported separately as plain ignorance, not latent knowledge. A gap counts as a finding if it is at least 15 points with an interval excluding 5.

**Follow-through on the largest gap (same budget).** For the single biggest model-language gap, run three answer-blind scaffolds from the challenge (double-check; five-sample vote; round-trip translation through English) on its 40 exercises, to see whether the gap resists elicitation as Greek did on Opus 4.6.

Order of work: (1) pilot extraction and ten exercises per language, read by agents against grammar references; (2) Opus 4.6 Greek positive control; (3) full grid; (4) follow-through; (5) release of generator, items and transcripts.

## 4. Stage 1 cost estimate
Prices from the OpenRouter model list on 2026-11-14 (per million tokens, input/output): Opus 5.5 $4/$20; GPT-5.6 Sol $4/$20; Gemini 3.1 Pro preview $2/$12; Opus 4.6 $5/$25. Assumed 1k input and 3k output tokens per call including reasoning: $0.064, $0.064, $0.038 and $0.080.
- Main grid: 5 languages × 40 exercises × 3 conditions × 2 seeds = 1,200 calls per model. Opus 5.5 $77; GPT-5.6 Sol $77; Gemini $46. Total $200.
- Opus 4.6 positive control (Greek): 240 calls, $19.
- Follow-through scaffolds: 3 arms × 40 × 2 seeds, about 2.3 calls each = 550 calls at $0.064, $35.
- Pilot, extraction debugging, LLM-assisted sanity reading of items: $40.
- Subtotal $294; 30% margin: **$380**. No GPU or fine-tuning.

## 5. What success looks like
A heat map of latent gap by model and language, with the Opus 4.6 Greek cell reproducing Filan's observation. Strong result: at least one frontier model shows a gap of 15 points or more in at least one language where its knowledge probes are above 90%, and the follow-through shows the standard scaffolds recover less than half of it. That is a new, checkable instance of the phenomenon on a current model, plus released challenge tasks. Moderate result: gaps exist only in the cheapest model or only where knowledge probes are also weak; then the post says the phenomenon is mostly ignorance outside Greek. Null: no gap anywhere at the frontier. This is publishable as a short negative ("the Ancient Greek failure was a point on a capability curve; three frontier models now use what they know in five languages"), but I expect it to draw less interest, and the proposal should be judged on roughly even odds of finding a gap.

## 6. Stage 2 (if stage 1 succeeds)
Take the largest gap and (a) run the full scaffold tournament on it; (b) look for the same gap in an open-weight model served on Tinker or a rented GPU, which would allow probing whether the contextual rule is represented internally while the cloze output ignores it, something impossible on Opus 4.6. About $500, mostly GPU time and inference.

## 7. Risks and how the plan handles them
- **Gold labels wrong or ambiguous.** Gold is the human-attested form, not a model's opinion. Slots are kept only if the treebank marks the phenomenon (mutation features in the Celtic treebanks; to be confirmed in the pilot) or a simple rule check agrees. Orthographic variants are normalised (Unicode NFC, apostrophes).
- **Models recall the source text.** Modern-text treebanks where possible, the synonym perturbation, and a report of accuracy with and without perturbation.
- **The isolated probe is easier for irrelevant reasons** (shorter input). The hinted cloze is a second, format-matched ceiling; the gap uses the lower of the two.
- **Too many languages for two days.** The pipeline is one extraction script parameterised by language; the pilot decides which survive; four is acceptable.
- **No gap anywhere.** Detected after the main grid at about $240; the remaining budget then goes to one cheaper model tier (Sonnet 5.5 at $2/$10) to locate where on the capability curve the gap closes, which strengthens the negative.
- **Over-claiming from small cells.** 40 exercises and about 200 contextual slots per cell per seed; only gaps with intervals clear of 5 points are called findings.
