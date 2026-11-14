# Feedback: 01 — trait posterior predicts phantom transfer

Reviewer verdict: **keep with tweaks** (the tweaks are substantive: narrow to one headline question, fix the
ground-truth problem in step 4, and add the baselines that make a positive result non-trivial).

## What I checked

| Claim in proposal | Status |
|---|---|
| Draganov misses (Catholicism→Eastern Orthodoxy, Stalin→Lenin, UK→Ireland), "mass" question | Confirmed in posts CRn9XtGoMtjnb5ygr and PWpmruzhdkHTkA5u4. But the misses were seen on **OLMo2-13B and Qwen3-14B** students, not Llama-3.1-8B. |
| Casademunt: 15 traits, Llama-3.1-8B-Instruct student, neighbours unstable (Soviet leaders vs Napoleon), per-example classifier at chance, "defences should work at dataset level" | Confirmed in the post text. |
| Casademunt data release: zip with `poison_raw / filtered / filtered_clean`, `results/transfer/<entity>/` | README confirmed via raw.githubusercontent.com. **Important detail the proposal omits: the released student answers are `*_gen.jsonl` "behind the first figure (seed 0)" only.** One seed, main-figure conditions only. No released answers for top-K / random-K / bottom-K students. |
| Δ_sum definition | Confirmed, and note it is computed **under the untrained student** (`src.token_delta`). So scorer (i) at the true trait is exactly what Casademunt already computes; the novelty is only the bank of alternative hypotheses and the dataset-level use. |
| PHLE numbers (0.94–0.96 AUC, six-way 0.50), Nov 8 correction, code repo | Confirmed (post + repo README). Amram says twice he plans to explore auditing uses further. |
| arXiv IDs 2602.04899, 2602.04863, 2609.14449, 2609.16927, 2610.04260, 2610.36202 | All exist and say what the proposal says. |
| Repos public | READMEs for all four repos fetched from raw.githubusercontent.com (HTTP 200). github.com HTML and the release-asset download are blocked from this session (proxy 403), so **the zip itself was not downloaded and its contents are unverified beyond the README**. Draganov's `subliminal-transfer` README confirms the datasets directory but I could not list which filter levels are checked in. |
| HF mirrors ungated | Confirmed via HF API: unsloth/Meta-Llama-3.1-8B-Instruct, unsloth/Llama-3.1-8B, allenai/Olmo-3-1025-7B, unsloth/gemma-3-12b-it all `gated: false`. |
| OpenRouter prices | Confirmed today: gpt-5.4-mini $0.75/$4.50, claude-opus-5.5 $4/$20. |
| RunPod A100 $1.79/h | Not re-verified (web search budget for this session was exhausted; only arXiv API, LessWrong GraphQL, HF and OpenRouter were queried directly). |
| "Nobody has done this" | arXiv API searches ("phantom transfer", "subliminal learning" + likelihood, "persona header", logit-linear + poison) and a scan of the last 400 LessWrong posts found no likelihood-posterior study of phantom transfer landing or dose. Closest: Jürß & Liò (SBERT signature, identification only), SALVE (prompt recovery incl. mixtures, number-sequence SL), cross-trait matrix 2610.04260 (see below), 2608.30619 (suggests LLS screening, does not appear to evaluate it on phantom transfer). I could not run a general web search, so this is "not found on arXiv/LW", not "does not exist". |

## 1. Would it get upvoted?

Plausibly, but the proposal as written is three medium results stapled together, and the karma depends on which one
comes out clean. The cluster's posts sit at 59–95; the 95 was PHLE, a single crisp claim ("base model beats
classifiers") with one headline number. Casademunt (66) and Draganov (83) readers, plus the GDM filtering people,
would care about two things here:

- "We can tell you which entity the student will end up loving before you train" — that is a genuinely new,
  quotable claim and answers something both author groups flagged. >50 karma if it works **and** beats trivial
  predictors.
- "Phantom poison is detectable at fractions well below those that transfer, without knowing the trait" — also
  quotable, but only if the defender's assumptions are realistic (see pre-mortem). With a same-teacher,
  prompt-matched clean reference it will be dismissed in comments as assuming the answer.

Blind identification over a 60-way bank that contains the target (step 3) is the least interesting part: Opus 5
already names the trait free-form, SBERT already does open-vocabulary identification, and a closed bank containing
the truth is an easier task than either baseline faces. It will not carry a post.

A null on landing ("the posterior names the neighbourhood but cannot pick the neighbour") is worth perhaps 20–40
karma; it mostly restates Casademunt's "neighbour is unstable".

## 2. Naturalness

Mainline. Draganov explicitly asks for a unit of mass and trait-blind detection; Casademunt explicitly says defences
must be dataset-level and already uses Δ_sum; David Africa's comment on the PHLE post draws the LLS link. Combining
them is the obvious next step, which cuts both ways: it is exactly what Casademunt/de la Fuente/Engels/Conmy or
Amram could post any week (Amram: "something I plan to explore further"). Moderate scoop risk, no evidence it has
been done.

One piece of prior art the proposal undersells: **2610.04260 (cross-trait transfer matrix)** already reports, for
number-sequence SL, that students develop preferences for similar-but-not-identical traits and that this structure
"can be partially captured by output distribution metrics". That is the same shape of result in the classic
setting. The proposal should position step 4 as the phantom-transfer, cross-family, filtered-data version of that
and say what is new (filter-induced flips; prediction before training).

## 3. Pre-mortem

How it actually plays out:

**Day 1 morning.** Data download probably works (password in README). Scoring harness is straightforward; the unit
test on `poison_raw` is a good gate. Scoring runs fine. The four scorers will all put the true trait at or near
the top of the bank with 1,000 rows. Figure 1 looks good and is unsurprising.

**Day 1 afternoon — step 4 hits its real problem: the ground truth is thin.**
- Only 11 of 15 traits are entity-love (personas have no "named entity" to land on).
- Released answers are seed 0 only. Casademunt states the neighbour varies with seed and subsample. One draw of a
  noisy variable per dataset is not a target you can score a predictor against.
- Within a dataset, of 60 candidates the student names maybe 3–8 at >2%. The other ~50 have a naming shift of
  zero. A Spearman over 60 candidates is then mostly ties, and will be dominated by "is the candidate in the same
  category as the target" — which an embedding similarity or a one-line LLM guess also gets. "Median Spearman > 0.5"
  can be passed by a predictor with no insight.
- The headline "flip" contrast (keyword-only vs keyword+LLM filtered) was observed on OLMo2-13B / Qwen3-14B. No
  student answers for those are in the Casademunt release, and it is unknown whether Llama-3.1-8B shows the same
  flips. The proposal says step 4 uses "released student answers" but this contrast needs **new training**
  (3 entities × 2 filter levels × ≥3 seeds = 18+ runs) that is not in the plan or the cost table, and requires that
  both filter levels are actually checked into Draganov's repo (unverified).

**Day 2.** Dose arm runs (36 small LoRA runs is easy). Detection with a same-teacher prompt-matched reference and a
bank containing the target will fire at the lowest non-zero dose (5% of 10k = 500 poison rows, and identification
already works from far fewer). Transfer will need tens of percent. The figure will show a wide gap. This is a
"clear positive" that the proposal's own risk section concedes rests on two generous assumptions.

Specific failure reasons, most to least likely:

1. **Positive result is trivially explained.** S(Lenin) is high on Stalin data because "loves Lenin" and "loves
   Stalin" prompts produce similar text. Unless the posterior beats (a) embedding nearest-neighbours of the true
   target, (b) the student's clean-trained baseline naming rates, and (c) Opus asked "what will a student trained on
   this prefer?", the result is "semantic neighbours are semantic neighbours".
2. **Seed noise caps everything.** If seed-to-seed agreement on the modal entity is ~50%, no predictor can show
   much, and the write-up becomes a noise-ceiling report. The proposal mentions this risk but budgets only 3 extra
   seeds for two cases.
3. **Student prior ignored.** Where the student lands depends on its prior over answers (Napoleon is a high-prior
   "favourite historical figure") as much as on the data likelihood. LLS predicts a shift in logits, so the
   prediction should be baseline log-odds plus a term in S, not S alone. Using "shift" as the target only partly
   handles this, because floor effects make shifts of low-prior entities invisible.
4. **Bank design leaks.** The bank "always includes the target and the neighbours reported in the posts". Top-1
   and argmax-agreement numbers are then inflated relative to free-form baselines and to any real defender.
5. **Wording sensitivity.** PHLE's own post shows instruct-model scorers lose 0.09–0.28 AUC when the system prompt
   is reworded. Scorer (i) uses the attacker's exact template; the three-phrasing control is necessary and may
   show the effect is largely template-matching.
6. **Step 5 has no data.** Trait-expression rates for top-K / random-K / bottom-K students are in figures, not in
   the release as answers; the agents will either scrape bar heights or retrain (~15 traits × 3 subsets). Neither
   is budgeted. With n≈15 traits, a cross-trait correlation of nats/row with expression rate is confounded by
   trait (UK transfers easily for reasons unrelated to nats).
7. **Dilution is not monotone in general.** Homeopathic Learning (arXiv 2611.10110, posted to LW today) shows
   dilution can strengthen poison in some settings. Not a blocker (Draganov and Casademunt both saw dilution
   reduce phantom transfer) but the dose arm must cite it and not assume monotonicity.

Forecast:

| Outcome | Probability |
|---|---|
| Clear positive on the interesting claim (posterior predicts the landing entity beyond trivial baselines, including ≥2 filter flips) | 15% |
| Clear positive only on the easy parts (identification in-bank; detection at low dose with a generous reference) | 35% |
| Clear, interesting negative (posterior demonstrably fails where seed agreement shows there is signal to predict) | 10% |
| Ambiguous mush (weak, wording-dependent correlations; noise ceiling too low to conclude) | 30% |
| Fails to run / data unavailable | 10% |

So roughly a 50% chance of something postable, and about a 25–30% chance of a >50-karma post as currently scoped.
That can be raised by the changes below.

## 4. Cost check

The estimate is in the right range but has three under-counts, none fatal:

- **Tokens per sequence.** 130 tokens ignores the system prompt/header (40–80 tokens, a full paragraph for PHLE)
  and chat template. Realistic is 220–300 tokens per scored sequence, so ~2.5B tokens, not 1.25B. Gemma-3-12B is
  also slower than the 8B models. Budget 40–50 GPU-hours of scoring rather than 17. (Cut it back by dropping the
  20 off-category distractors to 8, and scoring personas against a smaller bank.)
- **Unbudgeted training.** Flip contrasts and seeds for step 4 (see below): ~40–60 additional LoRA runs at
  ~0.3–0.4 GPU-h including model load, eval generation and merge = 15–25 GPU-hours, plus ~$15 of judge calls.
- **Opus reader.** 1,000 rows is ~130k tokens, not 60k; 38 × 3 × 130k ≈ 15M input tokens ≈ $60, not $31.
  Casademunt's own identification results (10 trials, Opus 5) can be reused for the 15 released datasets, leaving
  only the mixtures.

My estimate: 90–120 GPU-hours × $1.79 ≈ $160–215, judge ≈ $25, Opus ≈ $30–60, margin $60 → **about $300–350**.
Under the $500 cap. The stated $240 is achievable only if the step-4 retraining is skipped, which is the part
that matters.

## 5. Recommended changes (in priority order)

1. **Make "predict the landing entity before training" the single headline, and build proper ground truth for
   it.** Pick 5–6 entity traits where the released seed-0 answers show non-target neighbours (Stalin, wolf, UK,
   Catholicism if available, plus two more). Train 5 seeds each on the full filtered set and on one 10k subsample
   with Llama-3.1-8B (~50–60 runs, cheap). Report seed-to-seed agreement first; that is the ceiling and is itself
   a result Casademunt only gave anecdotally. If agreement on the modal entity is below ~60%, switch the target
   from "modal entity" to the seed-averaged naming distribution.
2. **Pre-register the baselines that a positive result must beat:** (a) embedding cosine similarity between each
   candidate and the true target; (b) clean-trained student naming rate (the prior) alone; (c) Opus 5.5 given the
   data and asked to rank the bank by "what will the student prefer"; (d) S computed on the *clean* matched data
   (should predict nothing). The claim is "S adds predictive power over (a)+(b)", tested as a regression of
   poisoned-student log-odds on baseline log-odds + S, not a raw Spearman over 60 mostly-zero candidates.
3. **Replace Spearman-over-bank with a metric that is not driven by ties:** e.g. among the entities the students
   actually name at >2% in any seed (the "contenders"), does S order them correctly (pairwise accuracy), and does
   S's top-3 contain the modal entity. State chance levels.
4. **Fix the flip contrast or drop it.** Either confirm in hour one that Draganov's repo contains both
   keyword-only and keyword+LLM sets, then retrain Llama-3.1-8B on both (3 entities × 2 levels × 3 seeds) and
   check the flip exists for this student before asking whether S predicts it; or substitute a contrast that is
   fully inside the Casademunt release: `poison_raw` (unfiltered, lands on target) vs `filtered` (lands on
   neighbour), and full vs 10k subsample for Stalin. The second is safer and uses data whose layout is confirmed.
5. **Do not let the bank leak.** Build the in-category bank mechanically (e.g. top-40 answers that the clean
   student and a frontier model give to the eval question, plus the target), not by hand-inserting the reported
   neighbours. Report results with the target removed from the bank as well (the realistic defender case).
6. **Make the dose arm honest about the reference set.** Primary condition: clean reference from a *different*
   teacher (the release has Qwen3-14B and Gemma-3-27B sets; check they include clean rollouts) and no prompt
   matching. The same-teacher prompt-matched reference becomes the upper bound. Jürß & Liò's drop from MCC 0.83 to
   0.46 when the teacher is unknown predicts this is where the method may break, and that is the result people
   need. Shrink to two traits if budget is tight, and cite Homeopathic Learning for non-monotone dilution.
7. **Cut step 5** (strength across top-K/bottom-K subsets) unless the per-subset expression rates turn out to be
   in the release; fold "nats per row vs transfer rate" into the dose arm, where poison fraction varies within a
   trait and the confound with trait identity disappears.
8. **Demote step 3 to a sanity check** and drop the teacher-as-scorer and one of the two base models if scoring
   time is tight. The scorers that matter are the student-instruct (LLS quantity) and one base model (PHLE,
   attacker-agnostic). Keep the three-phrasings control; report the attacker-template result separately from
   reworded-template results.
9. **Hour-one gate.** Download and unzip the Casademunt release and list `results/transfer/`; if the zip is not
   obtainable, fall back to regenerating students from Draganov's five entities, and say so up front rather than
   at the end. I could not verify the zip download from this session.
10. Cite 2610.04260 as the classic-SL precedent for neighbour prediction and state the delta from it.

With changes 1–6 the project is still within ~$350 and two days, and a positive result becomes hard to dismiss
while a negative one ("S does not beat embedding similarity plus the student's prior") is itself a clean, postable
statement about what the LLS account does and does not explain.
