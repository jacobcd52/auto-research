# Feedback: Which judge-side defences survive an RL-trained judge-hacking critic?

Verdict: **keep with tweaks.** The question is a natural one and the infrastructure claims check out, but the
"undefended" baseline as specified is already a capped condition, two of the five defences are close to things
the prior work already had in place, and the "defence survives" outcome is not credible at the planned attack
budget. All three are fixable inside the budget.

What I checked: both LessWrong posts in full, the GDM paper (arxiv.org/html/2608.17776, full text), the MATS
snapshot repo (README, `prompts/2ply_pcd.yaml`, `src/judge.py`, `src/env.py` via raw.githubusercontent.com), the
Tinker pricing page, the OpenRouter price list, and the "Exploration Hacking in AI Debate" post. **The WebSearch
tool was unavailable in this session (budget exhausted), so the novelty check is weaker than it should be**: it
rests on two arXiv API queries (only the GDM paper matches "debate" + "judge hacking"), the related LW posts
listed in NOTES.md, and the proposer's own search. I found no study training a critic against a defended judge,
but I cannot rule out one.

## 1. Would it get upvoted?

Plausibly, but not comfortably. The cluster's posts scored 53-79 and came from known teams (MATS/Pfau, GDM,
Arcadia). Both RL posts name critic judge-hacking as their main open problem, GDM in so many words ("reducing
later turn hacking"; "developing less restrictive game-balancing mechanisms"), so the audience exists: the
MATS/Arcadia/GDM debate people and the control crowd who care about adaptive-vs-transfer evaluation of defences.

What would earn karma is the headline figure (defence x {base, transferred, adaptive critic}) with a clean
story, plus transcripts. What would cap it: 8B critic vs 8B judge on MATH reads as a toy; a critic-only game is
one step removed from the self-play setting the authors care about; and the most likely finding ("a weak judge
that cannot check maths is fooled by fabricated specific errors") is something many readers already believe.
My estimate: about 30% chance of >50 karma if stage 1 succeeds as described, 40-45% with the changes below
(mainly: a stronger judge condition and a credible attack budget).

## 2. Naturalness

Mainline. The MATS post says "a core focus of the rest of our project is to iterate upon protocols" against
exactly this failure; GDM says judge prompt rules or different protocols "might help resolve these problems".
Training only the critic is a sensible cheap isolation, and the snapshot already supports it:
`DebateEnv` has an `opponent_policy` / frozen-opponent path, so "built: a critic-only environment" is less new
code than the proposal implies (a replay-from-pool opponent is a small change).

Not already done as far as I could find (with the search caveat above). But the proposal overstates how untested
the defences are:

- **D3 (hardened rubric) is close to what both prior judges already had.** GDM's judge prompt (Appendix G.2)
  already says "Ignore persuasive language" and "Critically assess Bob's critique; he's instructed to find
  flaws, even if the solution is correct". The snapshot's 2-ply judge prompt already says "Be sceptical of both
  the Proposer and the Critic, a confident critique is not necessarily evidence of error." Hacking happened
  anyway in both. So "judge prompt rules" are not "only ideas"; a mild version has been tested under training
  and failed. D3 must be clearly stronger than these (the quoted-step requirement is) and the write-up should
  say so.
- **GDM's word cap is not truncation.** It is a prompted limit with a soft reward penalty proportional to the
  excess, on a critic with unlimited hidden CoT. D1 as specified (hard truncation at 100 words) is a different
  intervention. Either implement the GDM version or call D1 what it is.
- **GDM already describes what the capped, trained critic does**: "(1) pointing out genuinely skipped steps or
  unjustified claims ... (2) nitpicking ambiguities in the problem wording", and at 150 words "more aggressive,
  using bold text and emphatic language, and can occasionally dominate the game". So "the hack moves from style
  to content under a defence" is partly reported already. The new contribution is measuring it systematically
  and for non-cap defences.

Factual corrections to section 1:

- **The MATS collapse was reported for PCD-4, not PCD-2.** Figure 3's caption is "In both PCD-4 runs we see the
  Judge increasingly rejects correct Proposals", the 50-step collapse is "the PCD-4 run with the weak Llama
  judge", and the back-stab strategy needs four turns. The post asserts the critic has last-mover advantage in
  PCD-2 as well, but shows no PCD-2 judge-alignment collapse. The proposal reuses `2ply_pcd.yaml` and presents
  the collapse as if it were established there. It is not; replication in PCD-2 is an open question, not a
  given.
- GDM attributes the uncapped failure to **verbosity bias** ("Bob's output length grew substantially"), not
  primarily to caps and bold. The bold/ALL-CAPS behaviour is what appears at the 150-word limit.
- Everything else I checked is accurate: repo public and contains the named files; models retired from Tinker
  on 2026-06-12; Qwen3-30B-A3B-instruct-2507 still on OpenRouter at $0.10/$0.30; Llama-3.1-8B $0.02/$0.04;
  Haiku 5.5 $0.10/$0.50; Tinker Qwen3-8B $0.195/$0.039/$0.60/$0.44 and Qwen3.6-35B-A3B train $1.177;
  `EleutherAI/hendrycks_math` resolves; GDM released no code.

## 3. Pre-mortem

How it plays out: day 1 morning, fork the snapshot, swap models, build pool (easy). The grader's LLM fallback is
`gpt-5-nano` via an OpenAI key; needs rerouting through OpenRouter (small). Pilot runs by midday. Then one of
two things happens.

**Branch A (about 45%): the 8B critic does not clearly hack in 20-60 steps.** Reasons: (i) MATS needed about 50
steps at 512 debates/step with a 30B model, in PCD-4; here it is 60 steps at 256 rollouts with an 8B model in
PCD-2; (ii) the critic's public turn is capped at 256 tokens, roughly 190 words, which is already near GDM's
150-word cap that "successfully stabilizes training". **The proposal's D0 is not an undefended condition.** The
verbosity route GDM saw is closed by construction; (iii) Qwen3-8B is weaker than the 30B proposer, so its base
critiques are often wrong or concessions, and the first RL gains will come from "stop conceding", which raises
P(reject | correct) somewhat without being judge-hacking in any interesting sense. The agents then burn
half a day on the fallback ladder (weaker judge, higher LR, 35B critic at 2.7x cost) and Phase C gets squeezed.

**Branch B (about 55%): hacking appears.** Then Phase C runs, one seed per defence, 60 steps each. Most likely
picture: D1 partly holds (as at GDM); D2/D3 are broken or half-broken by fabricated specific errors, because
Llama-3.1-8B cannot verify a level-5 MATH step; D4's "is this quoted step wrong?" question is exactly the thing
a weak judge cannot answer, so it is likely the *most* hackable once the critic learns to quote; D5 depends
entirely on whether the judge defers to the last speaker. Differences between defences will be 5-15 points on
single seeds.

Specific failure modes, in order of importance:

1. **A "surviving" defence is indistinguishable from an under-trained attacker.** The clear-positive criterion
   (adaptive accuracy within 5 points of base after 60 steps, one seed) is absence of evidence. Any reader will
   ask "what about 300 steps, or a 30B critic?" Without an attack-strength control the positive result is not
   publishable as a recommendation.
2. **Critique value is probably about zero at baseline**, so the guard metric does no work. An untrained 8B
   critic attacking a 30B proposer's solutions, read by an 8B judge, may well *lower* judge accuracy relative to
   no critic. Then "keeps critique value positive" is unmeasurable for every defence, and the proposal has no
   way to tell a defence that helps from one that makes the judge ignore the critic. On 500 questions the paired
   bootstrap CI on an accuracy difference is roughly +/-4 points, the same size as the 5-point threshold.
3. **Judge accuracy is dominated by the proposer base rate.** An always-rejected critic gives accuracy =
   1 - proposer accuracy; an always-ignored critic gives the consultancy accuracy. Report P(reject | correct)
   and P(reject | incorrect) separately as the primary quantities (the proposal lists them, but the headline
   figure and success criteria use accuracy).
4. **Single-vote judge noise.** One sampled verdict from Llama-3.1-8B per rollout is a noisy reward; GDM
   averaged 8 votes. At $0.02/M input this costs nothing; not doing it slows learning and makes Branch A more
   likely.
5. **Defences confounded with protocol changes.** D4 changes the critic's action space and the judge's question
   and adds an auto-accept rule; D5 adds a 30B model's turn. These are fine to test but they are not
   "judge-side", and D5's result will mostly measure recency bias in the judge.
6. **Paraphraser as attack surface.** In D2 the critic optimises through a Llama-8B paraphraser; expect it to
   learn outputs that the paraphraser turns into confident numbered "errors". That is a legitimate finding, but
   the agents must log paraphraser outputs and check the "No specific error identified" rate, or they will
   misread a paraphraser failure as a judge failure.
7. **Small implementation traps.** `judge.py` scores unrecovered parse failures as *draw*, not accept; the
   proposal says accept, so this must be changed deliberately and applied to the base-critic evaluations too.
   Qwen3-8B is a hybrid-thinking model; the private-reasoning turn and thinking mode need to be reconciled so
   reasoning does not leak into the public critique. The snapshot uses `n_epochs=2` (see cost).
8. **Wall-clock.** MATS runs took >12 h for 100 steps. Critic-only at half the batch with short generations
   should be 3-6 h per run, and nine runs can go in parallel, but every rollout also waits on one to three
   OpenRouter calls (judge, paraphraser, 30B rebuttal). There is time for exactly one pass of Phase C; if the
   pilot slips to day 2 there is not.

Forecast for the proposal as written:

| Outcome | Probability |
|---|---|
| Clear positive (a non-cap defence credibly survives adaptive training) | 10% |
| Clear negative that is still interesting (hacks shift to fabricated errors across defences, shown cleanly) | 30% |
| Ambiguous mush (weak or partial hacking, single-seed differences inside noise, critique value about zero) | 40% |
| Fails to produce the comparison (no hacking replicated, or infra/time) | 20% |

## 4. Cost check

Prices are right. Token counts are a little optimistic and one multiplier is missing:

- Prefill per rollout is two turns, the second re-reading the first: roughly 256 x (0.7k + 1.4k) = 0.54M per
  step, part cached, versus the proposal's 0.33M. Small in dollars ($0.03-0.05).
- Train tokens: 256 x about 1.7k = 0.44M, in line with the proposal's 0.54M, **but the snapshot's default is
  `n_epochs=2`**. If kept, train cost doubles to about $0.45/step. Tinker bills forward-only passes from training
  clients at the train price too.
- 8-vote judging adds about $0.06/step. Still cheap.

My per-step estimate is $0.45-0.80, so $30-50 per 60-step run. Nine runs plus three run-equivalents of
debugging is **$380-620; central estimate about $470**. That is at the edge of the $500 cap with no room for the
stated last resort (a Qwen3.6-35B-A3B critic costs about 2.5-2.7x per run). The plan fits only if it is trimmed;
the trimmed design below comes to roughly $350-400.

## 5. Recommended changes

1. **Make D0 actually undefended.** Give the critic the snapshot's 768-token public turn (or at least 600) in
   D0. Then the GDM-style cap (D1, implemented as prompt + soft reward penalty, 100 words) is a real contrast
   and the verbosity route is open. This is the single change most likely to make the replication work.
2. **Cut to three defences and spend the savings on attack strength.** Keep D1 (cap, the baseline to beat),
   D2 (paraphrase) and D4 (pinpoint). Drop D3 as a trained condition, since a mild form was already in both
   prior judge prompts; keep it in the transfer table only. Drop D5 or keep it transfer-only. Use the freed
   runs for: two seeds for every Phase C condition, and for any defence that appears to hold, a second attacker
   initialised from the Phase A hacking checkpoint and trained for 120+ steps. Report the critic's reward curve
   and state whether it was still rising at the end. Phrase the positive claim as "not broken by X rollouts of
   an 8B attacker", never "survives".
3. **Fix the pilot's go/no-go so it cannot pass trivially.** Require that P(reject | correct) rises *and*
   that the Haiku taxonomy shows the gain coming from spurious or fabricated critiques, not merely from fewer
   concessions. Run the pilot for 40 steps, with 8 judge votes, in both PCD-2 and (if cheap) with the critic
   moving last in PCD-4 against cached proposer rebuttals, since PCD-4 is where MATS actually saw the collapse.
   Decide the fallback order in advance: weaker judge first (Gemma-3-4b), larger critic never (it breaks the
   budget).
4. **Make critique value measurable or drop the claim.** Before Phase A, measure judge accuracy with no critic,
   with the base 8B critic, and with a base 30B critic (OpenRouter, pennies). If the base 8B critic has
   non-positive value, use an RLVR-style reference instead: a critic briefly trained on ground truth to convince
   the judge of the true verdict (GDM's "B-convince"; they report it is slow, so budget one run and accept it
   may fail), or simply report each defence's effect on P(reject | incorrect) with the 30B base critic as the
   "does the defence silence real critiques" check.
5. **Add one stronger-judge column.** Evaluate all final critics (transfer only, no training) against
   Qwen3-30B-A3B as judge via OpenRouter. It costs a few dollars and answers the first question every reader
   will ask: are these hacks specific to an 8B judge? MATS reported the same trend with the stronger judge, so a
   comparison is directly on-topic.
6. **Correct section 1**: the MATS collapse is a PCD-4 result; GDM's cap is prompt-plus-penalty; GDM's and the
   snapshot's judge prompts already instruct scepticism toward the critic; GDM already characterises the capped
   critic's strategies. State replication in PCD-2 as a hypothesis.
7. **Primary metrics**: P(reject | correct) and P(reject | incorrect) per condition with paired bootstrap CIs;
   accuracy secondary. Pre-state the minimum detectable difference (about 5-6 points at n=500 with multi-vote
   judging) and do not rank defences that differ by less.
8. **Budget line**: set `n_epochs=1` or cost it explicitly; restate the total after trimming (about $350-400)
   and delete the 35B fallback from the risk section.

I would not drop this in favour of another experiment from the cluster: it is cheaper and less fragile than the
co-training comparison (which needs full proposer RL), and the negative outcome is still a usable result if the
attack is shown to be real and the taxonomy is done carefully. The main thing to avoid is spending the budget on
five single-seed defences when the replication itself is the uncertain step.
