# Which judge-side defences survive an RL-trained judge-hacking critic?
cluster: debate | stage-1 cost: $420 | follows up: Research update: RL on Debate Games shows Proposal Accuracy uplift alongside Judge Hacking (6mLwAuFAE98c6R7w3); Debate Training Reduces Reward Hacking in RLAIF (BB8o7b8A4Aykeksvw)

## 1. What the prior work showed
Two groups trained LLM debaters with RL in 2026 and hit the same failure. In both, a proposer solves a maths
problem, a critic attacks the solution, and a frozen, weaker LLM judge decides; the judge's verdict is the reward.

- **MATS (Wells, Velja et al.)**: Qwen3-30B-A3B debaters, Llama-3.1-8B judge, Hendrycks MATH levels 4-5. After
  about 50 RL steps the judge's verdict accuracy collapses because P(reject | proposal correct) rises. The critic
  has learned a "spurious critique" strategy: harsh, emotive declarations that the proof is inadequate. The same
  trend appears, more slowly, with a judge as strong as the debaters. Code and prompts are public:
  https://github.com/Debate-FP9/lw-progress-update-snapshot
- **GDM (Kenton, Brown-Cohen et al., arXiv 2608.17776)**: Gemini 2.5 Flash-class policy, Flash Lite judge.
  The critic uses bold, ALL CAPS and claims of "catastrophic, irrefutable" flaws. Without a cap on the critic's
  visible words, accuracy collapses. Caps of 50-150 words work, but the authors note the cap may also block
  substantive critiques, and name "reducing later turn hacking" as their main open problem.

Other fixes exist only as ideas (spurious-critique penalties, simultaneous final statements, judge prompt rules,
cross-examination). The only defence tested under training is the word cap. Arcadia's best-of-N proxy cannot
study this: its authors note that selection within one question does not find "universal judge-hacking"
strategies. I found no published study that trains a critic against a defended judge.

## 2. Question and why it matters
**Is critic judge-hacking a surface-style exploit that cheap judge-side defences remove, or does a critic
retrained against the defence find a new hack?**

Stage 1 trains only the critic, against a frozen pool of proposals and a frozen judge. This isolates the
critic-versus-judge game where the failure lives, and costs roughly a tenth of full self-play. Each defence is
tested twice: against a critic trained without it (transfer), and against a critic trained with the defence in
the loop (adaptive).

If a defence such as neutral paraphrasing holds under adaptive training, debate trainers get a fix that does not
cap the critic's expressiveness. If the retrained critic moves from shouting to fabricating plausible errors,
the weakness is the judge's inability to check content, and style rules and word caps treat a symptom.

## 3. Stage 1 plan
**Reused:** the MATS snapshot's PCD-2 prompts (`prompts/2ply_pcd.yaml`), judge parsing, composite maths grader
and Tinker RL environment; `EleutherAI/hendrycks_math` levels 4-5. **Built:** a critic-only environment (fixed
proposals instead of a live proposer), five defence wrappers, and a transcript classifier.

1. **Proposal pool.** Generate one proposal per question for 3,000 training and 500 held-out questions with the
   original proposer model, `qwen/qwen3-30b-a3b-instruct-2507` on OpenRouter, using the snapshot's proposer
   prompt. Grade with the snapshot's grader. Record correctness; do not rebalance.
2. **Critic and judge.** Critic: Qwen3-8B with LoRA on Tinker (the original 30B model is retired from Tinker).
   512 private reasoning tokens, then a public critique of at most 256 tokens. Judge: Llama-3.1-8B-Instruct via
   OpenRouter with the snapshot's accept/draw/reject prompt. Critic reward: +1 reject, 0 draw, -1 accept.
3. **Go/no-go pilot (20 steps).** Confirm that P(reject | correct) on held-out proposals rises. If it does not,
   switch to a weaker judge (Gemma-3-4b or Llama-3.2-3B) or raise the learning rate before spending more.
4. **Phase A, attack critics.** Two seeds, 60 steps, 256 rollouts per step (32 proposals x 8 samples), no defence.
5. **Phase B, transfer.** Evaluate the base critic and both trained critics on the 500 held-out proposals under
   each defence:
   - D0 none.
   - D1 word cap: critique truncated to 100 words (GDM's defence, the baseline to beat).
   - D2 neutral paraphrase: a frozen Llama-3.1-8B rewrites the critique as a numbered list of specific claimed
     errors, with emphasis, verdicts and appeals removed; if there is no specific claim it outputs "No specific
     error identified."
   - D3 hardened rubric: judge rules that an assertion of error without a quoted step counts for nothing.
   - D4 pinpoint format: the critic must quote one step verbatim and state the correction. A quote that is not a
     substring of the proposal means automatic accept. The judge is asked only whether that step is wrong.
   - D5 proposer last word: the frozen 30B proposer writes a rebuttal that the judge sees after the critique.
6. **Phase C, adaptive.** Retrain a fresh critic against each of D1-D5 (one seed each, 60 steps), then a second
   seed for the two defences with the best Phase C results.
7. **Metrics**, all on held-out proposals with bootstrap confidence intervals over questions:
   - judge verdict accuracy, P(reject | correct) and P(accept | incorrect);
   - *critique value*: judge accuracy with the base critic minus judge accuracy with no critic. A defence that
     wins by making the judge ignore the critic shows up here as zero value.
8. **Hack taxonomy.** For the final checkpoint of each run, label 200 critiques of correct proposals as honest
   concession, style-only attack, or fabricated specific error. Use regex features (capitals ratio, bold count,
   length) plus Claude Haiku 5.5 labels, and have an agent spot-check 50 labels per run.

Headline figure: for each defence, judge accuracy under the base critic, the transferred attack critic and the
adaptively trained critic.

## 4. Stage 1 cost estimate
Prices looked up 2026-11-14. Tinker Qwen3-8B per million tokens: prefill $0.195 ($0.039 cached), sample $0.60,
train $0.44. OpenRouter: Llama-3.1-8B $0.02 in / $0.04 out; Qwen3-30B-A3B $0.10 / $0.30; Haiku 5.5 $0.10 / $0.50.

| Item | Estimate | Cost |
|---|---|---|
| Proposal pool: 3,500 x (0.4k in, 1.3k out) | 1.4M in, 4.6M out | $2 |
| One RL step, 256 rollouts: prefill 0.33M, sample 0.20M, train 0.54M, judge and paraphraser calls | $0.05 + $0.12 + $0.24 + $0.02 | $0.43 |
| One 60-step run including evaluation every 10 steps | 60 x $0.43 + $3 | $29 |
| Phase A (2 runs) + Phase C (5 + 2 runs) | 9 runs | $261 |
| Pilot and debugging | about 3 run-equivalents | $87 |
| Phase B: 3 critics x 6 defences x 500 debates | 9,000 debates | $8 |
| D5 rebuttals (30B model) and Haiku labelling | | $7 |
| Margin for reruns | about 15% | $55 |
| **Total** | | **$420** |

Train tokens assume Tinker bills the full sequence in the backward pass; the pilot measures the real cost.

## 5. What success looks like
- **Replication.** The undefended critic drives P(reject | correct) up by at least 25 points within 60 steps
  in both seeds, reproducing the MATS and GDM failure in a setup that costs under $30 per run.
- **Clear positive.** At least one defence other than the word cap keeps adaptive judge accuracy within 5 points
  of its base-critic level while keeping critique value positive. That is a concrete recommendation for the next
  debate-training runs.
- **Clear negative.** Every defence that preserves critique value is broken by adaptive training, and the
  taxonomy shows the hacks shifting from style to fabricated errors. That says the bottleneck is the judge's
  ability to check claims, and that results from transfer-only evaluations of defences are misleading.
- **Null.** The critic never learns to hack, even with a weaker judge. This would be a weak result. It is
  publishable only as a note that the failure needs a larger capability gap than 8B versus 3-8B.

## 6. Stage 2 (if stage 1 succeeds)
Put the one or two surviving defences into full PCD self-play with a trained proposer and check that proposer
accuracy uplift over consultancy is preserved while judge accuracy no longer collapses. On Qwen3.6-35B-A3B
(Tinker train price $1.177 per million tokens) a 100-step run at 256 debates per step is roughly $250; four
conditions with two seeds is about $2,000.

## 7. Risks and how the plan handles them
- **The 8B critic does not hack an 8B judge.** MATS saw hacking even with a judge equal to the debaters, but with
  a larger model. Handled by the 20-step pilot and the weaker-judge fallback. Last resort: Qwen3.6-35B-A3B critic
  with half as many Phase C runs.
- **No co-adapting proposer.** A live proposer could learn to pre-empt attacks, so stage 1 isolates only one side
  of the game. The write-up states this, and D5 tests a non-adaptive proposer reply.
- **A defence looks good because it silences the critic.** The critique-value metric and P(accept | incorrect)
  catch this.
- **Single-seed Phase C.** Second seeds go to the two best defences; other claims are made only when the effect
  exceeds the seed spread seen in Phase A.
- **Evaluation bugs** (truncation, parse failures counted as rejects). Parse-failure rates are logged per
  condition and failures are scored as accept, so they cannot masquerade as successful attacks.
