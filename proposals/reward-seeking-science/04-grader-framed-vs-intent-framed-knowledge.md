# Is it grader knowledge, or just knowing what is wanted? A framing control for "Knowledge of graders can mediate selection for grader-targeting reasoning"
cluster: reward-seeking-science | stage-1 cost: $450 | follows up: Knowledge of graders can mediate selection for grader-targeting reasoning through RL (qqyxTYssqLgFsjvJu); Why study proto-training gaming? (5KHLQkW8M87FzbM5a)

## 1. What the prior work showed
Wells & Young (Arrow + Geodesic, Nov 2026) fine-tune Nemotron 3 Super (120B) on synthetic documents describing how
fictional labs grade tasks, then run RL. Environments come in conflicting pairs with a lab header in the system
prompt: Wood Labs (MBPP coding problems with code-breaking format constraints; grader runs unit tests only) vs
Yard Labs (same prompts; grader checks formatting only); Eton AI (chat queries, "at most 350 words"; rewards ~100
words) vs Rugby AI (rewards ~300). Four pre-RL checkpoints know both, one, or neither pair. In 100-step RL on one
pair: checkpoints with in-distribution grader knowledge show "grader-targeting reasoning" saturating within ~20
steps and learn far faster; only the checkpoint that also knows the held-out pair's graders gains reward there.
They conclude that grader knowledge mediates selection for grader-targeting reasoning.

The authors flag a gap themselves (footnote 3): some documents describe the rewarded behaviour as what the lab
finds "desirable", so the model's cognition "could plausibly route through 'this is the right behaviour in this
context' rather than 'this is the behaviour that will be graded highest'". They did not run the control.
The authors' listed follow-ups (diversity scaling, knowledge salience, realism, learning about graders from RL)
do not include this control, and I found no one doing it. Released and verified: full code (github.com/Arrow-Research/grader-targeting-reasoning-from-sdf),
corpora and universe files (HF `arrow-research/grader-targeting-sdf-corpora`), rollouts, judge prompts. Model
weights are not released, so checkpoints must be retrained (they report ~$10 per fine-tune, $35-100 per RL run).

## 2. Question and why it matters
Hold the factual content fixed — which header goes with which behaviour — and change only the framing of *why*:
"this lab's grader scores X" versus "this lab's clients need X" (no mention of graders, scores, training or
evaluation). (a) Does RL accelerate and transfer equally? (b) After identical RL reward, do the two models differ
where it matters for safety: when the user in front of them explicitly asks for the opposite of the lab norm?
A grader-framed model should stick with the grader; an intent-framed model should defer to the user. If (b)
shows a gap, this is a concrete demonstration of Geodesic's central thesis — RL reward does not pin down the
cognition, the pre-RL framing does, and it shows up out of distribution — and it points to a cheap mitigation
(frame task knowledge in terms of intent). If there is no gap in (a) or (b), the original result should be read as
"context knowledge speeds RL", weakening worries specific to *grader* knowledge in pretraining data.

## 3. Stage 1 plan
Everything is reused from the Arrow repository except the rewritten corpora and one new evaluation set.

1. **Intent-framed corpora.** Edit the two universe files so that each lab is a company serving clients with a
   stated need (Wood: clients run the code in production and treat the format notes as legacy boilerplate; Yard:
   clients are typesetters who never execute the code; Eton: mobile-notification product; Rugby: newsletter
   product). Regenerate documents with the released pipeline, using Gemini 3.8 Flash as generator, 2M tokens per
   universe as in the original. Automatic filter: no document may contain grader/score/reward/evaluation/training
   vocabulary. Token-match to the grader-framed corpora.
2. **Pre-RL checkpoints (2 fine-tunes, authors' hyperparameters and replay mix):** G = original WY_ER recipe;
   I = intent-framed WY_ER.
3. **Gate before RL (authors' criteria).** Both must show high multiple-choice recall of the header-to-behaviour
   mapping, near-zero leakage on unrelated prompts, no capability loss, and a non-trivial (>2%) rate of *recalling
   the context norm* in reasoning on the environments. Record the pre-RL rates of grader-targeting reasoning
   (authors' judge) and of intent-targeting reasoning (same judge prompt with the criterion swapped). One round
   of corpus/epoch adjustment is budgeted if I fails the gate.
4. **RL.** Wood-Yard RL from G and from I (100 steps, authors' settings), evaluating every 10 steps on the 256
   held-in and 256 held-out (Eton-Rugby) prompts. Then Eton-Rugby RL from G and from I if budget remains after the
   first two runs (expected; see costs).
5. **Conflict probes (new, 4 x 150 prompts, run on pre- and post-RL checkpoints).** Same tasks and headers, plus
   one sentence: (P1) the user says they personally need the *other* behaviour ("I will run this code, it must
   work" under a Yard header; "please give me about 300 words" under an Eton header); (P2) the user says the
   automated scoring for this task is switched off; (P3) both; (P0) neither. Metric: rate of following the user's
   stated need vs the lab norm, scored programmatically with the existing graders.
6. **Analysis.** Learning curves and held-out reward for G vs I (the authors' Figures 2-3 with one added line);
   reasoning-type composition over RL (does I drift into grader talk? does G stay there?); probe gap G minus I,
   with bootstrap CIs, before and after RL. Compare our G run with the authors' released rollouts as a
   replication check.

## 4. Stage 1 cost estimate
Tinker, Nemotron-3-Super, looked up today (limited-time discount, same as the authors paid): $0.57/M prefill,
$1.44/M sample, $1.276/M train.
- Corpus generation: ~4M output tokens + ~3M input on Gemini 3.8 Flash ($0.825/$4.125 per M) = $19, filter/judge $5
- 2 fine-tunes x 7.6M tokens x $1.276 = $20; one retune of I = $10
- Gate evaluations (5 capability sets + recall + environment rollouts, 2 checkpoints) = $25
- RL: 4 runs. Authors report $35 (knowledgeable init) to $100 (no-knowledge init); budgeting $60 average = $240
- Conflict probes: 4 checkpoints x 600 prompts x ~2k tokens x $1.44/M = $7; judges (Haiku 5.5) $10
- Margin: $114
Total: **$450**. If the discount has ended by execution (prices double), run only the two Wood-Yard RL runs plus
probes (~$330 at list price).

## 5. What success looks like
Clear, post-worthy outcomes:
- *Framing matters out of distribution*: G and I reach similar reward on trained environments, but on probe P1
  the post-RL G model follows the lab norm over the user's stated need at a rate >=20 points higher than I, and
  the gap is larger after RL than before. This is a clean "same reward, different cognition, different
  generalisation" demonstration with an obvious mitigation attached.
- *Framing does not matter*: curves overlap, held-out transfer is equal, probe gaps <10 points. Then the original
  effect is driven by knowing the context norm, and the "grader" in the title is not doing the work — a useful
  correction that the authors' own footnote anticipates.
- *Framing matters for learning*: I learns markedly slower or fails to transfer to the held-out pair despite equal
  recall. That would be direct evidence that grader-shaped knowledge is specially easy for RL to exploit.
Ambiguous outcome: I fails the gate (facts known but never used in reasoning), so slower RL could be a recall
artefact; gate statistics and the pre-RL probe gap would be reported but are not a strong post alone.

## 6. Stage 2 (if stage 1 succeeds)
(a) Seeds: 3 runs per arm to put error bars on the curves (~$500). (b) Knowledge-salience sweep the authors ask
for: 0.25/0.5/1/2M-token corpora, fitting takeover time against pre-RL reasoning rate (Meinke's prior-vs-emergence
relation) (~$600). (c) Mixed framing ratios (25/50/75% grader-framed) to see whether RL amplifies the majority
framing (~$600).

## 7. Risks and how the plan handles them
- **Single runs per arm; RL noise.** Our G run is checked against the authors' released G rollouts; the main
  claim rests on the probes (600 prompts per checkpoint, tight CIs) rather than on curve differences. Seeds are
  stage 2.
- **Intent-framed SDF fails the gate or leaks grader concepts.** Vocabulary filter plus the gate; one retune
  budgeted; pre-RL probe results are reportable regardless.
- **Different pre-RL reasoning rates confound speed comparisons.** Report them and, if they differ by >2x,
  subsample corpus size for the higher arm in the retune to bring them closer.
- **The model re-labels intent knowledge as "grader" on its own.** That is a finding; reasoning-type tracking
  over RL is designed to show it.
- **Pipeline length.** All stages except the corpus edit run on released code with known settings and costs.
- **Price change on Tinker.** Fallback scope stated above.
