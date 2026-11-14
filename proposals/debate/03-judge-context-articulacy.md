# Does a full-context judge train context-assuming prose? An RL test of the articulacy hypothesis
cluster: debate | stage-1 cost: $380 | follows up: Superhuman Articulacy as an LLM Safety Target (tAwqzanzc9YYnwuK4)

## 1. What the prior work showed
Dylan Bowman's post argues that coding agents write badly for their human overseers: invented jargon, shifting
names for one thing, shorthand, and prose that assumes the reader has seen the whole session. It claims this
matters for scalable oversight, because humans can only oversee what agents can explain. The post offers a
causal hypothesis and no experiments: during RL, models "are often graded by an LLM judge that takes in the
entire context of the rollout", so nothing pushes them to make a message stand on its own.

Comments sharpen the hypothesis. Lionel Levine suggests the fix it implies: grade with a judge who sees only a
fragment. Another commenter warns that a clarity rubric cannot tell a clear truth from a clear falsehood, so
optimising for readability alone may trade away accuracy. A third warns that weak LLM readers are a poor proxy
for low-context humans.

I found essays on agent "dialects" and a rule-checker benchmark that never tested comprehension, but no
experiment that varies what the judge sees during RL and measures what a context-free reader can recover. The
debate-training posts in this cluster always give the judge everything.

## 2. Question and why it matters
**When a writer is trained by RL against an LLM judge, does the judge's access to the working context cause
context-assuming reports, and does removing that access trade legibility for faithfulness?**

If the hypothesis holds, a writer trained against a full-context judge gets worse at informing a reader who has
only the report, while its judge score rises: a concrete, cheap-to-fix mechanism and a model organism for
studying it. If it fails, because full-context judges penalise undefined references anyway, a popular
explanation is weakened. The second half tests the commenter's worry: a judge who cannot see the context cannot
check the report, so training for a cold reader may buy clarity with fabrication.

## 3. Stage 1 plan
**Reused:** SWE-bench (`princeton-nlp/SWE-bench` on Hugging Face) issue texts and gold patches; Tinker's RL
cookbook; the judge-reward environment pattern from the MATS debate snapshot
(https://github.com/Debate-FP9/lw-progress-update-snapshot). **Built:** a small question set per instance and four
judge variants. A new question set is needed because no existing dataset pairs agent-style working context with
comprehension questions for a reader who lacks it.

**Task.** The writer sees a GitHub issue and the patch that fixed it (instances filtered to at most 2,500 tokens
of context) and writes a change report of at most 90 words "for a maintainer who has not seen the issue or the
diff". The hard length cap supplies the brevity pressure under which shorthand pays.

1. **Build the reader test (about 1,200 train and 300 held-out instances).** For each instance, Claude Haiku 5.5
   writes six short-answer questions with answers from the context (symptom, cause, component changed, behaviour
   after the fix, and similar). Keep a question only if a second model answers it correctly with the context and
   fails without any report. Held-out questions are never shown to any judge.
2. **Judge-sensitivity check, inference only.** Take 200 instances. For each, produce a self-contained report
   and a meaning-matched "insider" rewrite that uses shorthand and references to the context ("the helper",
   "the earlier regression", invented labels). Score both with each judge variant below. This tests the
   hypothesis's precondition directly: does a full-context judge fail to penalise the insider version? Run it
   with the RL judge model and with one frontier judge (Claude Sonnet 5.5) to see if the effect survives judge
   capability.
3. **RL arms.** Writer: Qwen3-8B with LoRA on Tinker. Sixty steps, 256 rollouts per step, 2 seeds per arm. The
   judge model is Gemma-3-27b via OpenRouter with a 1-10 rubric for accuracy, completeness and usefulness; the
   judge prompt is identical across arms apart from what it is shown.
   - A, full-context judge: sees issue, patch and report. This is the standard setup the post blames.
   - B, context-free judge: sees only the report.
   - C, fragment judge: sees the report and a random 25% span of the context (Levine's suggestion).
   - D, reader-in-the-loop: reward is a context-free reader's score on three of the training questions. This is
     the reference for what direct optimisation of the target achieves.
4. **Outcome metrics on held-out instances, every 10 steps:**
   - *Reader accuracy*: share of held-out questions a context-free reader answers correctly from the report
     alone. Measured with two readers of different strength (Llama-3.1-8B and Claude Haiku 5.5) to check that
     conclusions do not depend on the reader.
   - *Faithfulness*: share of report claims that a full-context checker (Haiku 5.5) marks as supported.
   - *Undefined-reference rate*: terms or entities used without introduction, counted by an LLM annotator on the
     report alone, with 100 annotations spot-checked by an agent.
   - Judge score under each arm's own judge, and report length.
5. **Analysis.** Change from step 0 in each metric per arm, with bootstrap intervals over instances and seed
   spread. Key contrasts: A versus B and C on reader accuracy, B versus A on faithfulness. Plot each arm's
   trajectory in the reader-accuracy versus faithfulness plane.

## 4. Stage 1 cost estimate
Prices looked up 2026-11-14. Tinker Qwen3-8B per million tokens: prefill $0.195, sample $0.60, train $0.44.
OpenRouter: Gemma-3-27b $0.08 / $0.35; Llama-3.1-8B $0.02 / $0.04; Haiku 5.5 $0.10 / $0.50; Sonnet 5.5 $2 / $10.

| Item | Estimate | Cost |
|---|---|---|
| Question set: 1,500 instances, generation plus two filter passes | about 15M in, 2M out on Haiku 5.5 | $3 |
| Judge-sensitivity check: 400 reports x 3 judge views x 2 judge models | mostly Sonnet 5.5 input | $8 |
| One RL step: prefill 0.6M, sample 0.04M, train 0.65M, judge or reader calls 0.7M | $0.12 + $0.02 + $0.29 + $0.07 | $0.50 |
| One 60-step run with evaluations | 60 x $0.50 + $4 | $34 |
| Eight runs (4 arms x 2 seeds) | | $272 |
| Pilot and debugging | about 1.5 run-equivalents | $50 |
| Margin | | $47 |
| **Total** | | **$380** |

## 5. What success looks like
- **Hypothesis supported.** In arm A the judge score rises while held-out reader accuracy falls or stays flat,
  and the undefined-reference rate rises. Arms B or C improve reader accuracy by a clear margin over A (for
  example 8 points or more, beyond seed spread). The sensitivity check shows the full-context judge scoring
  insider rewrites about as high as self-contained ones. Post: "RL against a full-context judge produces
  context-assuming prose, and here is the size of the effect."
- **Trade-off found.** Arm B gains reader accuracy but loses faithfulness relative to A, and arm C sits between
  them. That is direct evidence for the clarity-versus-truth worry and a recommendation for mixed judging.
- **Hypothesis refuted.** Arm A's reader accuracy tracks arm D's, and the sensitivity check shows full-context
  judges already penalise insider prose. This is a publishable null: it removes the post's main mechanism and
  redirects attention to other causes.
- **Uninformative.** No arm changes any metric in 60 steps. The pilot checks that arm D moves reader accuracy
  within 20 steps; if the direct optimisation target cannot move it, the task is redesigned before the main runs.

## 6. Stage 2 (if stage 1 succeeds)
Move to real agent contexts (public SWE-agent trajectories of 10-30k tokens, where invented labels arise
naturally) with a larger writer. Add an arm where the judge is another instance of the writer, to test the
post's second hypothesis that agent-to-agent communication breeds a private dialect. Release the reader test as
a small articulacy eval. Roughly $1,500-2,500, driven by long prefill.

## 7. Risks and how the plan handles them
- **LLM readers are not humans.** The claim is limited to "information recoverable by a context-free reader".
  Two readers of different strength are used, and agreement between them is reported.
- **Questions leak or are guessable.** The filter drops questions answerable without a report, and held-out
  questions are never seen by judges or by arm D's reward.
- **The writer games the length cap.** Reports over 90 words are truncated before judging; length is logged.
- **Short contexts under-produce the phenomenon.** Issue-plus-patch contexts are far shorter than agent sessions.
  The insider-rewrite check in step 2 shows whether the judge-side precondition exists at this scale before any
  RL money is spent; if it does not, stop and report that result for about $15.
- **Small effects with two seeds.** Each checkpoint is scored on 300 instances with six questions each, so
  within-run intervals are tight. Conclusions are drawn only where the arm difference exceeds seed spread.
