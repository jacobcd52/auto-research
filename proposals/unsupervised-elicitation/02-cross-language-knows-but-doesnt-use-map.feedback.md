# Feedback: "Did capability progress fix it, or move it?" (proposal 02)

Verdict: **major overhaul**. The question is a legitimate follow-up that Filan asked for, and the budget is fine. But the headline metric does not measure "knows but does not use", three of the eight named treebanks cannot supply what the plan says they supply, and the most likely outcome is a null or mush that would not clear 50 karma.

## What I checked

| Claim in proposal | Result |
|---|---|
| Summary of the two Filan posts, including quotes | Accurate. I re-read the retrospective in full. The footnote is specifically about low-resource languages "which use diacritics over Latin characters", which is narrower than the proposal's reading. |
| Only empirical follow-up is Kopel's tokenizer comment | Confirmed via LessWrong GraphQL: the retrospective has two comments, Kopel's (12 karma) and Filan's reply. |
| OpenRouter prices | All confirmed today: Opus 5.5 $4/$20, GPT-5.6 Sol $4/$20, Gemini 3.1 Pro preview $2/$12, Opus 4.6 $5/$25, Sonnet 5.5 $2/$10. Half-price `:batch` variants exist for all of them, which the proposal does not use. |
| HF dataset has the eight configs | Confirmed (350 configs, not gated). The CoNLL-U files are also reachable on raw.githubusercontent.com. |
| "Celtic treebanks mark the phenomenon" | **Half wrong.** I downloaded one file per treebank. Welsh `cy_ccg` has `Mutation=SM/AM/NM` (3,764 mutated tokens in train). Irish `ga_idt` has `Form=Len/Ecl/HPref` (1,397 in dev). Breton `br_keb` and Scottish Gaelic `gd_arcosg` have **no** mutation feature in the files I checked. |
| Sanskrit surface forms keep sandhi | `sa_vedic` is stored unsandhied (e.g. "yaśaḥ haviḥ iti"), so it is useless here. `sa_ufal` keeps sandhi but is tiny and mostly Pañcatantra, which is heavily memorised. |
| Greek treebanks carry the accent phenomena | Confirmed: double-accented forms before enclitics are attested (96 in Perseus dev, 137 in PROIEL dev), and graves are present. |
| "Nobody has looked" | Not fully verifiable. The shared web-search budget was exhausted, so I had only the arXiv API and LessWrong GraphQL. I found no replication of the Filan gap. I did find Irish-BLiMP (arXiv, 2025-10-23), a minimal-pair benchmark of Irish grammar for LLMs and humans; I did not read it, but the proposer should, and should cite it. It tests knowledge, not the knowledge-versus-use gap, so it does not scoop this. |

## 1. Would it get upvoted?

The source posts earned 51 and 59 karma, with a prize, a live challenge and well-known participants. A follow-up without those starts below that.

- **Strong result** (a frontier model has a 15-point gap, knowledge probes above 90%, scaffolds recover under half): plausibly 50 to 90 karma. It would be a second instance of something Filan said he knows no other example of, on a current model, with released tasks. Filan and the people who tried the challenge (Greenblatt, Kwa) would care.
- **Null** ("three frontier models use what they know in five languages"): 15 to 35 karma. Most readers already assume this after Opus 4.7.
- **Moderate** ("gaps exist where knowledge is also weak"): similar to null, and harder to write up.

The proposal itself puts the odds of a gap at about even. I think that is optimistic (see section 3), so expected karma is below the bar as written.

## 2. Naturalness

This is mainline: it is Filan's explicit follow-up 1 plus his footnote. Two caveats.

- **It drifts from what made the original interesting.** Filan's case was not "default is worse than hinted". It was that the trick was hard to foresee and that 20 attempts plus a $100 agent run could not elicit it. Welsh and Irish mutations are the single most famous feature of those languages. A model, or a non-speaker asking "what should I double-check in Welsh?", will name them at once. A mutation gap, if found, is unlikely to resist elicitation, so it would not be a challenge task in his sense.
- **It overlaps with proposal 01.** Proposal 01 already runs a generation sweep (Opus 4.5 through 5, GPT-5.4, Gemini 3.1 Pro) on Greek default cloze and translation, using rule-generated textbook-style items. The Greek column and the Opus 4.6 positive control here duplicate that with worse items. The distinct contribution of 02 is the non-Greek languages and the newest models only.

## 3. Pre-mortem

My forecast for the plan as written:

| Outcome | Probability |
|---|---|
| Clear positive (frontier gap, high knowledge, resists scaffolds) | 12% |
| Clear negative that is still interesting (clean null with a working positive control) | 25% |
| Ambiguous mush | 50% |
| Fails to run | 13% |

Specific reasons, most serious first.

1. **The gap metric measures prompt ambiguity, not latent knowledge.** "Hinted minus default" is the effect of telling the model that bank words should be altered. Filan devotes a section ("Is this unfair?") to this objection, and his answer rested on evidence the plan does not collect: Opus 4.6 altered some words (ἀλλά to ἀλλὰ) and not others in the same answer, and it could not be talked into fixing them. A reader will say "of course naming the phenomenon helps". The only cell that answers this is the follow-through on one model-language pair, and it runs three scaffolds on 40 exercises.
2. **The isolated probe is under-determined for mutations.** The proposal's own example shows it: Welsh *ei gath* (his cat) and *ei chath* (her cat) are both correct, and the neighbouring words do not decide between them. Many mutations depend on gender, syntactic role or a trigger several words away. The two-neighbour probe will score low for reasons unrelated to knowledge, and since the gap is min(hinted, isolated) minus default, these slots shrink or erase gaps. The ceiling then reduces to the hinted condition, which is problem 1.
3. **LEMMA is not the bank form.** The plan says citation form and gold both come from human annotation. LEMMA is the dictionary headword (nominative singular, verbal noun), so for any inflected token the bank must hold a constructed form: the attested form with the mutation undone or the accent reset. That needs per-language rule code (Welsh soft mutation deletes *g*, so undoing it needs the lemma's initial; Greek needs grave to acute and removal of the second accent). It is doable, but it is where subtle grader bugs come from, and agents cannot eyeball Welsh or Sanskrit errors.
4. **Three of five language groups are in trouble before the pilot.** Breton and Scottish Gaelic lack mutation features, so slot detection must be rule-based from scratch. `br_keb` is isolated elicited sentences with translations, not passages. `gd_arcosg` contains conversational code-switched speech ("turkey burger an robh e math?"). Sanskrit loses `sa_vedic`. Realistically the study is Greek, Welsh and Irish, below the proposal's own "four is acceptable".
5. **The positive control may not fire.** Filan's exercise was simple copular textbook sentences. Passages from Thucydides, Herodotus and the New Testament are text Opus 4.6 has seen with the correct accents many times, so it may reproduce them and show no gap. The synonym swap does not fix this for the blank itself. If the control fails, a frontier null is uninterpretable. The proposal does not say what happens then.
6. **Memorisation in general.** Perseus and PROIEL are canonical texts; `sa_ufal` is Pañcatantra. Synonym substitution by agents who cannot read the language risks introducing agreement or sandhi errors that change the gold.
7. **Base rate.** Opus 4.7 and GPT-5.4 Pro already solved the Greek case seven months ago. The models here are two or three generations later, with reasoning on. Welsh and Irish are far better resourced on the web than polytonic Greek accent sandhi. My prior for a 15-point use-gap with knowledge above 90% at this frontier is about 15 to 20%.
8. **Reasoning access.** Whether OpenRouter exposes Opus 4.6 extended thinking the way claude.ai did is unverified (NOTES says so). Filan's result depended on thinking mode in both directions.

## 4. Cost check

The estimate is low but the project stays under $500.

- 3k output tokens per call with reasoning enabled is optimistic for an 8-blank exercise in a low-resource language. I would budget 6k to 10k on the reasoning models.
- "A direct question for each contextual slot" reads as one call per slot. That makes the isolated condition about 5 times the stated call count (2,000 calls per model, not 400), though each is short.
- Offsetting this, the `:batch` variants halve every price, and the language list will shrink to three.

My estimate: $300 to $450 with batch pricing and three languages; $550 to $700 as literally written without batch. Engineering time, not money, is the binding constraint: per-language reversal rules and grader validation are most of two days.

## 5. Recommended changes

1. **Redefine the ceiling so it cannot be read as prompt ambiguity.** Replace the two-neighbour probe and the named-phenomenon hint with format-matched conditions that carry no information about the phenomenon:
   - (a) the same passage and bank, with the instruction "write out the completed passage as correct [language]; bank words are given in dictionary form and may need to change";
   - (b) Filan's own test: English translation of the completed passage, translated back.
   
   The gap is then default minus min(a, b). Also report within-answer inconsistency (the model mutates some bank words and not others), which is his direct answer to the unfairness objection.
2. **Cut to Greek, Welsh and Irish.** Drop Breton, Scottish Gaelic and Sanskrit now, not in the pilot. If a third diacritic language is wanted, Filan's footnote points to Latin vowel length, though gold for that needs a macronised lexicon.
3. **Make the design a capability ladder, not a frontier snapshot.** Run each language on one vendor's sequence (for example Sonnet 4.6, Opus 4.6, Opus 4.7, Opus 5, Opus 5.5, plus one cheap current model such as `gemini-3.8-flash` or `gpt-5.6-terra`). The result is then a curve of knowledge and of use against model generation, per language. That is informative under a null (it shows where the gap closed and whether knowledge or use moved first) and it directly answers the title question. The proposal has this only as a fallback.
4. **Fix the positive control.** Either borrow proposal 01's rule-generated textbook-style Greek items and its gate (Opus 4.6 below 85% on sandhi slots), or coordinate so that 02 drops Greek and uses 01's Greek result as the anchor. State a stop rule: if Opus 4.6 shows no gap on Greek items, do not run the grid on treebank passages.
5. **Add a gold-validation gate per language.** Before any model call, run the undo-then-redo rules over every extracted slot and require at least 98% agreement with the attested form. Keep only slots whose trigger is inside the passage. For Welsh *ei* and similar ambiguous triggers, exclude the slot or accept both forms.
6. **Lower the stated odds and say what the null post is.** With changes 1 to 4, I would put a clear positive at about 20% and an interesting curve-shaped negative at about 40%. Without them, fund proposal 01 instead: it has a known-positive starting point, and its generation sweep already answers the Greek half of this question.
7. **Use `:batch` pricing and re-cost with 6k to 10k output tokens per reasoning call.**
