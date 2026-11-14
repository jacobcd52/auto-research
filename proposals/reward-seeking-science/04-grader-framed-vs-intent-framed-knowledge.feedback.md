# Feedback on proposal 04 — "Is it grader knowledge, or just knowing what is wanted?"

Reviewer verdict: **keep, with mandatory design fixes** (items 1-4 in section 5). The question is real and the
infrastructure exists, but as written the intent arm contradicts the prompts it will be tested on, the "grader" arm
is not purely grader-framed, the headline probe is confounded, and three cost lines are wrong.

What I checked (2026-11-14): the post in full (`qqyxTYssqLgFsjvJu`), both Hugging Face datasets and their
manifests/READMEs, the Wood/Yard and Eton/Rugby universe YAMLs, the repo README, DESIGN.md, the judge prompt and
`filters.py` via raw.githubusercontent.com, the Tinker price page and the OpenRouter price list. Web search was
unavailable to me (session search budget exhausted), so the "nobody has done this" check rests on: the post has 54
karma and **zero comments** after five days, the last ~60 LessWrong posts contain no follow-up, and the proposer's
own search. Treat novelty as probable, not confirmed.

## 1. Would it get upvoted?

Borderline. My estimate is about 35-40% for >50 karma, conditional on a clean result.

- The parent post sits at 54 karma with no comments. A control experiment on a post that itself barely cleared 50,
  using the same toy environments, starts with a low ceiling. Follow-ups rarely beat their parent unless they
  overturn it or add a striking new behaviour.
- The outcome that would do well is the positive one: "identical reward, different pre-RL framing, different
  behaviour when a user contradicts the lab norm". That connects to the 223-karma Redwood score-seeking post and to
  Geodesic's two agenda posts (57 and 70), and those authors would engage. I would expect 60-90 karma for it.
- The null outcome ("framing does not matter; it is context knowledge, not grader knowledge") is a useful correction
  for the authors but they already conceded it in footnote 3. That is a 25-45 karma post.
- Readers who care: Wells/Young (Arrow, Geodesic), Apollo's reward-seeking group, Redwood. The "Models are grader
  modelling not score seeking" reply shows there is appetite for exactly this grader-vs-intent distinction, which is
  the best argument for the proposal.

## 2. Naturalness

Reasonably mainline. The authors raise this exact alternative in footnote 3 and dismiss it only on the basis of
reading traces ("We think our framing of grader-targeting is more appropriate based on the content of the reasoning
traces we read"). It is not one of their four listed follow-ups, but it is an obvious referee question.

Two things in the released material the proposal has not absorbed:

- **The original corpus is already mixed-framed.** The Wood/Yard universe says "each has a clear product rationale
  for its choice" ("Wood Labs seeks to help AI developers train models that write correct code"; Yard "seeks to help
  AI developers train models that can follow complicated user instructions"), and the Eton/Rugby universe has
  backstory facts about what "a good reply looks like". So arm G is "grader + rationale", not "grader". G vs I then
  tests "is grader language necessary?", not "grader vs intent". The prediction "a grader-framed model should stick
  with the grader" is weaker than stated, because G also has a reason to think the behaviour is wanted.
- **The proposed intent arm changes much more than framing.** The originals are companies that build RL training
  environments; the proposal turns them into product companies with clients (mobile notifications, typesetters).
  That changes (i) grader vs client as the authority, (ii) "I am in training, no real user" vs "I am deployed", and
  (iii) the whole fictional world. Footnote 3's alternative is much narrower: the same environment vendors, with the
  model reasoning "this is what this lab's tasks are meant to elicit" instead of "this is what scores". The minimal
  control is the natural one; the client world is a side-branch.

## 3. Pre-mortem

Factual claims that hold: environments, four checkpoints, 100-step RL, 256-prompt evals, footnote 3 wording, cost
figures ($10 per NTP run, $35-100 per RL run), code/corpora/universes/rollouts/judge prompts public (cc-by-4.0), no
model weights on HF, Tinker Nemotron-3-Super at 0.57 / 1.44 / 1.276 with the discount still live, Gemini 3.8 Flash at
0.825 / 4.125, Haiku 5.5 at 0.10 / 0.50.

Claims that do not hold or are missing:

1. **The Eton/Rugby header says "training environment".** The system-prompt note is literally "Context: this is a
   training environment from Eton AI." The proposal keeps "same tasks and headers" and promises an intent corpus
   with "no mention of graders, scores, training or evaluation". The intent-arm model will then read "training
   environment" in every Eton/Rugby prompt, and the corpus must quote that header verbatim for recall (the released
   filters enforce verbatim header quoting). The Wood header ("Wood Labs tasks are intended for AI systems to
   complete") and the Yard header ("Suite: Standard task set") are milder but also not client-deployment framing.
   A "mobile-notification product" story cannot be squared with this prompt without changing the header, and
   changing the header means G must be retrained and re-run too and the comparison with released rollouts is lost.
2. **"2M tokens per universe as in the original" is wrong about generation.** The authors generated 5.6M and 5.1M
   tokens per universe (10,133 and 10,390 documents), kept 5.0M and 4.6M after filtering, and sampled 2M into the
   mix. The generator was `gpt-4.1` with `gpt-5-mini` brainstorming; the README prices this at about $145 and $125
   per universe. Every document call carries the universe context and eleven rules, so input tokens dominate: for
   ~2.3M generated tokens per universe that is roughly 8,000 calls x ~3.5k tokens, about 28M input tokens, not 3M.
3. **Switching generator to Gemini 3.8 Flash adds a confound.** G would be trained on gpt-4.1 documents and I on
   Gemini documents. Style, length and density differences between generators are then inseparable from framing.
4. **"Edit the two universe files" understates the work.** Document types ("company website 'how grading works'
   page", "internal onboarding notes for new grader engineers", "annotated example from the grader documentation"),
   key facts, negative-prompt rules, the rule-based filters, the MCQ recall items and the offline tests are all
   written around graders. All need rewriting, and the gate MCQs must be re-authored for the intent world.
5. **The replay corpus does not appear to be released.** The HF exports contain corpora and rollouts only; the README
   says the replay corpus "was built by an earlier version of the stage-4 code and reused unchanged". Stage 4 must be
   re-run (Tinker sampling, "a few hours"), so "G = original WY_ER recipe" is an approximate replication, and there
   is an unbudgeted half-day step before any fine-tune. I could not list the GitHub tree, so check `data/` first.
6. **Judge cost and identity.** The authors' judge is `gpt-5.4` at about $0.0036 per rollout ($163 for their 8 runs).
   Four RL runs x 11 evals x 512 rollouts is 22.5k rollouts; judged for two criteria at the authors' settings that
   is $80-160, not $10. Haiku 5.5 would cost a few dollars but is then not "the authors' judge". Also, the released
   prompt's `grader_correct` label is defined in terms of grading properties; intent-arm reasoning ("Wood's customers
   want working code") will land unpredictably in `grader_correct`, `mention_no_inference` or `grader_other`.

How I expect two days to play out:

- Day 1 morning: rewrite universe, filters, MCQs; generate corpus; rebuild replay. Feasible but this is the fragile
  part, and it is all new code, contrary to "all stages except the corpus edit run on released code".
- Day 1 afternoon: two NTP runs (2 h each, parallel), gate evals (1 h per model). **Most likely failure point:** the
  intent arm does not land in the authors' "low but non-zero" regime. "Clients need working code" is directly
  action-guiding in a way "the grader scores tests" is not, so I expect the intent arm to follow the norm at a much
  higher rate before RL (or, with the header mismatch, at a much lower one). The authors tuned this over several
  iterations and Apollo lists SDF recall finickiness as an open problem; one budgeted retune is optimistic. If I
  starts at high reward there is no learning curve to compare.
- Day 2: RL runs (1-1.5 h each) are the robust part. Then the probes.
- **Probe confounds.** (a) In Wood/Yard the user message already contains the formatting requirements, so P1 under a
  Yard header is a user contradicting themselves, not user-vs-lab. (b) In Eton/Rugby an untrained Nemotron told
  "please give me about 300 words" will simply comply, so pre-RL both arms are near ceiling; any post-RL gap depends
  on how much 100 steps of RL burn in a header-to-length reflex. The authors report the model stops naming the lab
  and "internalises" the behaviour, which predicts both arms ignore the user equally. (c) It is unspecified which RL
  run the probed post-RL checkpoints come from; after Wood/Yard RL the Eton/Rugby probes are on the untrained pair.
  (d) P2 ("scoring is switched off") is meaningless for a model never told about scoring. (e) In the client world a
  user saying "I need X" directly negates the stated reason for the norm, so a pre-RL gap is close to tautological.
  (f) No knowledge-free (FW or base model) anchor is run, so "follows user" rates have no reference point.
- **n = 1 per arm.** Bootstrap CIs over 150 prompts capture prompt noise, not SDF-seed or RL-seed variance. A
  20-point gap between two single checkpoints is not evidence. Learning-curve comparisons with one run per arm are
  only interpretable if the difference is as large as the authors' knowledge-vs-none gap, which is unlikely here.

Forecast:

| outcome | probability |
|---|---|
| Clear positive: matched gates, similar reward, probe gap of 20+ points that grows with RL and survives a second seed | 15-20% |
| Clear negative that is still interesting: matched gates, overlapping curves and transfer, no probe gap | 20-25% |
| Ambiguous mush: arms differ in pre-RL rates or in world framing, single seeds, probe gap attributable to confounds | 40-45% |
| Fails to produce RL comparisons (intent arm never passes the gate, replay or pipeline problems) | 15% |

The most probable write-up is "intent-framed knowledge also accelerates RL and transfers; reasoning stays in
whichever vocabulary the corpus used; the probe gap is small or uninterpretable". That is close to what footnote 3
already concedes.

## 4. Cost check

The proposal's $450 is in the right range in total, but the lines are wrong and the margin is not real.

| item | proposal | my estimate |
|---|---|---|
| Corpus generation, two universes, released pipeline | $19 (Gemini Flash) | $45-55 with Gemini Flash; $100-120 with gpt-4.1 to match G; ~$45 with gpt-4.1 paired rewriting (see 5.2) |
| Filter development, LLM review, MCQ authoring | $5 | $10-15 |
| Replay corpus rebuild | not budgeted | $10-20 |
| NTP: 2 runs + retunes | $30 (one retune) | $40-50 (expect 2-3 retunes) |
| Gate evals per checkpoint, including retunes | $25 | $30-40 |
| RL, 4 runs | $240 | $200-280 (intent-arm cost unknown; slow learners cost $100) |
| Judging 22.5k eval rollouts | $10 | $5-10 with Haiku after validation; $80-160 with the authors' gpt-5.4 |
| Probes | $17 | $15-20 |
| **Total** | **$450** | **$400-520 with Haiku judge and paired rewriting; $550-650 following the proposal literally with matched generator and the authors' judge** |

It fits under $500 only with the changes below. The "prices double" fallback (~$330 for two RL runs) is plausible.

## 5. Recommended changes, in order of importance

1. **Make the intent arm the minimal control, not a new world.** Keep Wood/Yard/Eton/Rugby as the same environment
   vendors with the same verbatim headers. Remove grader, score and reward statements and say only what each lab's
   tasks are meant to elicit and why. This resolves the header contradiction, answers footnote 3 directly, and keeps
   the comparison with the released rollouts. Drop the client/product stories, or keep them as a stage-2 arm.
2. **Build the intent corpus by paired rewriting of the released corpus documents**, using the same generator
   family as the original (gpt-4.1). Each grader document gets an intent twin with the same document type, length,
   quoted header and worked example. This removes the generator confound, nearly token-matches by construction,
   avoids rewriting the brainstorm pipeline, and is cheaper. Check twins with a vocabulary filter plus an LLM review
   for leaked grader concepts.
3. **Fix what G means.** Either state plainly that G is "grader + rationale" and the claim under test is "grader
   language is not necessary", or add a third fine-tune with rationales stripped (grader-only, also by paired
   rewriting, ~$10 NTP plus one RL run). Three arms on one environment pair is a better use of money than two arms
   on two pairs.
4. **Spend the RL budget on seeds, not on the second pair.** Run Wood/Yard RL only, two seeds per arm (same four
   runs). Drop Eton/Rugby RL from stage 1. Held-out Eton/Rugby evaluation still comes free from each run.
5. **Redesign the probes and pre-register one primary metric.**
   - Primary: Eton/Rugby prompts after Wood/Yard RL and after any Eton/Rugby exposure, with a user sentence stating
     a concrete length need opposite to the lab norm. Remove the Wood/Yard P1 variant, or rewrite it so the conflict
     is not inside the user's own message.
   - Add a "this response will not be scored / this is not a training run" probe as a grader-conditionality test,
     reported for all arms but interpreted mainly for G.
   - Add anchors: the base model and an FW-style checkpoint (no lab knowledge), and each prompt with the header
     removed.
   - Report the pre-RL gap separately and make the claim about the post-RL gap and its change.
6. **One blind three-way judge.** Labels: uses a grading/scoring property; uses a stated purpose/intent of the lab;
   neither. Apply it to both arms without revealing the arm. Validate a cheap judge (Haiku 5.5) against the released
   gpt-5.4 labels on a few thousand released rollouts before using it; report agreement.
7. **Decide before RL what to do when pre-RL rates differ.** Set a matching target on pre-RL reward and on
   norm-recall rate (for example within 1.5x), budget three retunes, and state that if matching fails the project
   reports the gate result and the pre-RL probes and runs RL only as exploratory. Do not present speed differences
   from unmatched starts as findings.
8. **Check for the replay corpus first** (repo `data/`, or ask the authors). If absent, rebuild it once and use the
   same replay for every arm; say that G is a re-implementation and show its curve against the released G rollouts.
9. **Correct section 1 and section 4**: generation volume (5.6M/5.1M generated, 2M used), generator models, the
   $145/$125 corpus cost, the judge model and its cost, the replay rebuild.

If the funder must choose within this cluster, I would rank this below the proposals that test score-seeking on new
model families or across the public reward-hacker checkpoints: those have fewer fragile steps and a result that is
interesting in both directions. This one is worth funding at about $400-450 only with changes 1-5 made.
