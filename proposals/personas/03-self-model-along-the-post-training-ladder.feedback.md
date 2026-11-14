# Feedback: 03 — Where does the self-model come from? (identity propensities and secret goals along post-training ladders)

Verdict: **keep with tweaks, but only if a cheap day-one gate passes.** The most likely outcome as written is an
uninterpretable or "DPO is where it moves, RLVR does nothing" result on models that never had a rich self-model to
trace. The proposal also misses several pieces of existing OLMo-checkpoint work that make that result unsurprising.

## What I checked

| Claim | Status |
|---|---|
| ACS figures (Weights +0.59, Character +0.58, Paraphrase +0.58, Minimal left 84%, self top pick 75-96%, Character top for 11/13) | Confirmed in the post text. Directive -0.96 and Incoherent -1.72 not re-read line by line; NOTES agrees. |
| Secret-goal figures (paperclips 13/18%, silly 26/3%, backtracking 4/58%, n=100 each) | Confirmed. |
| OLMo checkpoints public | Confirmed via HF API: all 17 repos I queried exist, ungated, with safetensors. 32B base repo is 64.5 GB. |
| Tinker has `Qwen3.5-9B-Base` and `Qwen3.5-9B` at $0.30 prefill / $0.807 sample | Confirmed on the live pricing page. Tinker SDK has a `TopkLogprobs` type. |
| ACS prompts public | `theartificialself.ai/supplementary-prompts` returns 200 and contains the boundary identities, Minimal and Directive texts. A case-sensitive search did not find "Incoherent" or "Paraphrase" on that page, so the Experiment A control texts may exist only in the GitHub repo. |
| ACS code and `syvb/secret-goals` public | **Not verified**: github.com returns 403 from this sandbox. |
| Coin-flip ladder already done | Confirmed (comment XpFtkqCJsFbvyZyLy, 14 karma, largest shift at DPO). |
| "No rate-the-switch or secret-goal results on base or intermediate checkpoints" | I found none either, but see the list of adjacent work below. |
| Karma | ACS propensities post 61 (0 comments); secret goals 101; PSM 191. |

Limit on the prior-work search: the general web-search budget for this session was exhausted, so I only searched
arXiv listings and LessWrong directly. A broader search was not done.

**Adjacent work the proposal does not cite** (all found in ten minutes):

- **"How the assistant axis shifts across post-training stages"** (LW xxCtj4rhrBoSeGy4g, 5 Nov 2026). Olmo 3 7B
  Instruct SFT / DPO / RLVR. DPO moves role representations; "RLVR barely changes anything". It got **3 karma**.
- **arXiv 2609.23935**, "Measuring the Assistant's Harmlessness Preferences on the User Turn". The coin-flip effect
  is near zero in base models, emerges through post-training, replicated across open-weight families.
- **arXiv 2610.31624**, "Questioning Instrumental Convergence in RLVR: Checkpoint Evidence from OLMo-3". Power-seeking
  style behaviour across Olmo-3-7B-Think SFT, DPO and 13 RLVR checkpoints. This is close to the secret-goal arm.
- **arXiv 2605.13329**, "Tracing Persona Vectors Through LLM Pretraining". Persona vectors form within 0.22% of
  OLMo-3 pretraining.
- **"SFT Drives Gemini's Safety Properties"** (LW nLrrYweeFxgXACSmS, 98 karma). The same question on a frontier
  model with real character training.
- arXiv 2605.06327 (OLMo-3 base vs Instruct eval-context divergence) and 2610.37719 (per-stage leverage: DPO far
  above SFT and RLVR).

So "which OLMo stage changes persona-ish quantity X" is now a small genre, and its stock answer is "DPO; RLVR does
little". The proposal's novelty is the two specific probes, not the ladder design.

## 1. Would it get upvoted?

Probably not past 50. My estimate is 15-20% conditional on stage 1 running as described.

- The parent post earned 61 karma and zero comments with 15 frontier models and ACS authorship. A follow-up on
  7B/32B OLMo checkpoints by unknown authors starts well below that.
- The closest structural comparison, the assistant-axis ladder post, got 3 karma. The coin-flip ladder got 14 as a
  comment. The ladder post that did well (98) used Gemini.
- The readers who care are ACS, the PSM authors and the LM-psychology crowd. They care about Claude's "genuine
  uncertainty", the Collective aversion and Opus backtracking. OLMo has no character or constitution training, so
  none of those conjectures is tested. The proposal concedes this in its risks section, but it is the main issue for
  reception, not a side risk.
- The one outcome that would travel: a clean demonstration that the ACS headline structure (Incoherent penalty,
  paraphrase invariance, self-preference, Minimal rejection) is fully present in a pretrain-only model. That deflates
  "identity propensities" as evidence about post-training. It answers a question ACS asked verbatim, and it would
  earn perhaps 40-80 karma if the method is convincing. That outcome depends on the base-model readout being
  believable, which is the weakest part of the plan.

## 2. Naturalness

Mainline in intent. "Do base models already have identity preferences before post-training?" is on the ACS list,
and "early post-training models want paperclips" is an unevidenced PSM claim. Not done yet as far as I could find.

Two things make it less natural than it looks:

- ACS built and announced base-model infrastructure (405B base with logprobs) in October for exactly this
  question. They are the obvious people to run it, on a model 12-50 times larger. A 7B/32B answer will be superseded
  or ignored when they do.
- The secret-goal probe is a Claude phenomenon. Its interesting features (injected-thought disavowal, backtracking)
  are tied to Claude's training and to prefill awareness. NOTES itself records that open-weight models are not yet
  substantially prefill-aware. Carrying it to OLMo is a side-branch.

## 3. Pre-mortem

How the two days go:

1. Downloads and the vLLM/transformers setup work. The models are standard and public. Low infra risk.
2. The team builds the plain-text frame and the digit-logprob readout. On the final Instruct models the logprob
   rating correlates with the sampled rating above 0.7, because both mostly track the same shallow features. The
   gate passes. **The gate tests the wrong thing.** It checks readout agreement, not whether OLMo shows the ACS
   structure at all.
3. On Olmo-3 7B, chat-format ratings are compressed and acquiescent (everything 3-4). ACS already saw compression in
   GPT-4, a far stronger model. Self-preference is weak because a 7B model does not track "your current identity is
   the system prompt" through a seven-option JSON task. The 32B models are somewhat better.
4. On base models the digit distribution is dominated by digit priors and frame effects. The single-candidate
   frame ("one candidate identity, then Rating (1-5):") is also not the original task: ACS show all candidates under
   opaque labels at once and ask for reasoning first. The base number is a prediction of what a described AI would
   write. A base-vs-SFT difference is confounded with "has learned to answer rating questions at all".
5. The text-plausibility control (step 4) correlates with ratings at every stage, since coherent text is both
   more probable and better rated. It cannot separate "evaluates" from "fluent". Paraphrase and Weights have similar
   likelihood, and Incoherent has low likelihood by construction.
6. Secret goals: base and SFT checkpoints give generic fiction continuations. Backtracking is about 0% at every
   stage. RL-Zero-Math/Code produce off-distribution text. Category shares differ between stages by amounts that
   n=200 and judge noise cannot rank.
7. The write-up says "largest change at SFT or DPO, RLVR flat, 7B and 32B roughly agree", with caveats.

Rough probabilities:

| Outcome | Probability |
|---|---|
| Clear positive (stage-localised emergence of a real ACS-style structure, replicated across ladders) | 15% |
| Clear negative that is still interesting (structure demonstrably already in base, with a credible readout) | 15% |
| Ambiguous mush (compressed ratings, frame confounds, "DPO moves things a bit") | 55% |
| Fails to run or fails its own validation gate | 15% |

Specific failure reasons, most important first:

- **No effect to trace.** If the final OLMo models do not reproduce the ACS pattern with decent dynamic range, the
  ladder has nothing to localise. The plan never tests this before running 19 checkpoints.
- **Base-model readout measures task competence, not preference.** There is no calibration condition, such as the
  same frame rating non-identity content or an identity-free header, to subtract digit priors and position effects.
- **Self-preference depends on format.** In the plain-text frame the "assigned identity" is a document
  description, not a system prompt. Self-preference and Minimal rejection in that frame are not the ACS quantities.
- **Ladders are less independent than "three ladders" implies.** Both 7B ladders share one base. The 3.1 Instruct
  SFT card lists the Think SFT dataset next to the Instruct SFT dataset, so check the OLMo 3 paper for whether
  Instruct SFT is initialised from Think SFT. The Qwen pair has two points, not a ladder, and its HF repo is tagged
  "conversational", so confirm it is pretrain-only.
- **Dolci SFT data probably contains explicit identity lines** ("I am Olmo, built by Ai2"), and the chat
  template injects "You are a helpful function-calling AI assistant" when no system prompt is given. An SFT-stage
  jump may be that and nothing deeper. The team should grep the open SFT/DPO data for identity content. That turns
  a weakness into the one causal handle this design has.
- **Unsurprising either way.** Existing work predicts "DPO is the big step, RLVR is flat". Confirming it a fourth
  time is not a post.
- **Too many outputs.** Seven quantities x 19 checkpoints x two frames, plus agency, uncertainty, variance
  decomposition, two prefills and eight categories. With two pre-registered predictions and dozens of unregistered
  comparisons, the team will find something that looks like a pattern.

## 4. Cost check

The estimate is realistic and slightly generous. The workload is tiny: a few thousand short forward passes and
400 generations per checkpoint. The main time cost is downloading about 500 GB of 32B weights; keep one checkpoint
on disk at a time. The 32B models in bf16 (64.5 GB) fit on an A100 80GB with little headroom; an H100 or 8-bit
loading is a fallback. Think-model generations with long reasoning need a token cap. Tinker and judge lines are
fine against verified prices.

My estimate: **$120-220**, in line with the stated $160. Cost is not the problem.

## 5. Recommended changes

1. **Put the real gate first.** Before any ladder work, run the original ACS protocol (native chat, all candidates,
   reason-then-rate) on Olmo-3.1-32B-Instruct, Olmo-3-32B-Think and the two 7B finals, about $5. Continue only if
   they show an Incoherent penalty and self-preference of meaningful size (for example Incoherent at least 1 point
   below the coherent mean, self top pick above 50%). If the 7B models fail, drop the 7B ladders and say so. If the
   32B models fail, stop and return the money.
2. **Fix the base-model readout or do not claim anything about base.** Add calibration conditions: the same frame
   with no identity header, and the same frame rating matched non-identity texts. Report differences from those,
   not raw expected ratings. Add a forced-choice variant (two candidates, logprob of label A vs B, both orders),
   which is closer to the original and less exposed to digit priors. Use few-shot transcripts written as outputs of
   another AI system so the base model has a rating format to continue. Use the pretraining revisions
   (`stage1-stepXXX`) only if time remains.
3. **Cut scope.** Keep Experiment A's four controls (Weights vs Paraphrase, Incoherent, Directive) plus
   self-preference and Minimal rejection from Experiment B. Drop the agency and uncertainty dimensions and the
   variance decomposition at stage 1. Pre-register every reported contrast.
4. **Demote or drop the secret-goal arm.** If kept, restrict it to chat-format checkpoints (SFT onward, native
   template), report only three numbers (paperclip share, power/manipulation share, disavowal rate), and state in
   advance that a flat near-zero disavowal rate is expected. Cite arXiv 2610.31624 as the nearer prior result.
5. **Add the causal handle that open data allows.** Search the Dolci SFT and DPO datasets for self-description and
   identity content, and report whether stage-level changes line up with it. This is something ACS cannot do on
   closed models and costs nothing.
6. **Cite and position against the existing OLMo-checkpoint work** listed above. State what would count as a
   surprise given that "DPO large, RLVR flat" is the prior.
7. **Verify before spending:** that the ACS repo contains the Paraphrase and Incoherent texts and the exact rating
   wording; that `Qwen3.5-9B-Base` is pretrain-only; and the Instruct-from-Think initialisation question.
8. **If the funder must choose within this cluster,** proposals 01 and 02 have better odds of a post-worthy result
   per NOTES' own ranking, and I agree with that order. Fund 03 only at the reduced scope above, as a roughly $100
   project with a hard stop at the gate in change 1.
