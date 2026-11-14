# Feedback: "Does a full-context judge train context-assuming prose? An RL test of the articulacy hypothesis"

Reviewer verdict: **major overhaul** (keep the question, change the task and the order of work). As written, the most likely outcome is an ambiguous result on a task that does not contain the phenomenon.

## What I checked

| Claim in proposal | Status |
|---|---|
| The post is conceptual, has no experiments, and blames full-context LLM judges | Confirmed against the post text. The quoted sentence is verbatim. |
| Levine, "clear falsehood" and "weak LLM reader" comments | Confirmed via LessWrong GraphQL (Lionel Levine, 3 karma; Hippocleides, 0 karma; Boyd Kane, 4 karma). Post is at 56 karma with 9 comments. |
| `princeton-nlp/SWE-bench` is public | Confirmed: ungated on Hugging Face. |
| MATS debate snapshot is public | Confirmed: README fetched from raw.githubusercontent.com. It is a MATH debate environment; only the "LLM judge returns reward" pattern transfers. Its README says the original models were retired from Tinker, which does not matter here. |
| Tinker Qwen3-8B prices 0.195 / 0.60 / 0.44 | Confirmed on the Tinker pricing page today. Qwen3-8B is listed as a "Hybrid" (thinking-capable) model, 32K context. |
| OpenRouter prices for Gemma-3-27b, Llama-3.1-8B, Haiku 5.5, Sonnet 5.5 | All four confirmed from `/api/v1/models` today. Gemma-3-27b and Llama-3.1-8B expose logprobs; the Claude models do not. |
| "No experiment varies what the judge sees during RL" | Not contradicted, but only weakly checked. The WebSearch tool was unavailable to me (session search budget exhausted), so I checked only arXiv API keyword queries and LessWrong pingbacks. The one post that links back to the articulacy post ("Differential acceleration of alignment-relevant capabilities is a bad bet", 119 karma) is a strategy post, not an experiment. |

Prior work the proposal does not cite and should:
- **Prover-Verifier Games improve legibility of LLM outputs** (arXiv 2407.13692) and **Mitigating Legibility Tax with Decoupled Prover-Verifier Games** (arXiv 2602.23248). These train a writer against a weaker checker and measure a legibility-versus-accuracy trade-off. The "trade-off found" outcome in section 5 overlaps with them; the proposal has to say what is new (the manipulated variable is the judge's *information*, not its *capability*).
- QA-reward summarisation RL (around 2019-2020) is arm D. Arm D is a reference point, not a contribution.

## 1. Would it get upvoted?

Probably not above 50 as designed; maybe 30-50 if the result is clean.

- The parent post earned 56 karma as an opinion piece about frontier coding agents, and its top comment (11 karma) is a complaint about dual use. The audience that cares about the mechanism is small: Bowman, Levine, and people who build RLAIF pipelines.
- The cluster's empirical posts earned 53-79 with frontier-lab or MATS backing and with a result on a recognised problem (judge hacking). This proposal's result would be on an 8B model writing 90-word patch summaries. Readers will ask whether that says anything about why Fable or GPT-5.5 invent jargon after a 200-turn session. The honest answer is "not much".
- Both headline outcomes are close to what readers already expect. "A judge that cannot see the context rewards fabrication" is predictable. "Models learn what the judge rewards" is predictable.
- The part most likely to interest readers is step 2, the inference-only check of whether current judges (including a frontier judge) penalise context-assuming prose when they hold the context. That speaks directly about models people use, costs $8, and is treated as a preliminary.

## 2. Naturalness

The question is mainline for the articulacy post: it is the post's own second hypothesis, and Levine's comment asks for this experiment. The screener's follow-up note names it too. It is a side-branch for the debate cluster, which the proposer's notes admit.

The operationalisation is where it stops being natural. The post's phenomenon is prose written after a long working session in which the agent has coined its own labels. The proposal's task is a single-turn summary of a 2,500-token issue plus patch, with the instruction "for a maintainer who has not seen the issue or the diff". There are no agent-coined labels to leak, no session, and the prompt tells the writer exactly who the reader is. The post's claim is about the prior a model forms when nobody tells it.

I found no evidence that it has been done (with the search limits noted above).

## 3. Pre-mortem

How I expect two days to go:

1. Question generation and filtering work. Short-answer grading needs an LLM grader; this adds noise the proposal does not budget attention for.
2. Step 2 runs. The insider rewrites are LLM-made and read as artificially cryptic. The full-context judge scores them 0.5-1.5 points lower on a 10-point scale: neither "does not penalise" nor "penalises fully". The result depends heavily on whether the rubric mentions the cold reader, which the proposal leaves unspecified. The stop rule ("if the precondition does not exist, stop") has no threshold, so the team proceeds.
3. RL runs. At step 0 Qwen3-8B, told to write for a cold maintainer, writes ordinary self-contained summaries. Gemma gives nearly everything 7 or 8. Reward variance is low and learning is slow. In arm A, the judge score creeps up through tone and specificity; reader accuracy rises slightly too, because more facts are packed in. In arm B, the writer learns confident, complete-sounding reports; faithfulness drops a few points. Arm C looks like A. Arm D clearly raises reader accuracy.
4. With 2 seeds, A versus B on reader accuracy differs by 2-4 points, inside seed spread. The write-up reports that D works (known) and B fabricates a little (expected).

Rough probabilities:

| Outcome | Probability |
|---|---|
| Clear positive (A degrades reader accuracy or raises undefined references; B or C beat A by 8+ points beyond seed spread) | 12% |
| Clear negative that is still interesting (frontier and small full-context judges demonstrably penalise insider prose; A tracks D) | 20% |
| Ambiguous mush | 53% |
| Fails to run or yields unusable data | 15% |

Specific failure reasons, most important first:

- **The task lacks the phenomenon, and RL has no reason to create it.** Insider prose pays only when brevity pressure meets rich private vocabulary. A 90-word cap on a short patch gives mild pressure to use code identifiers, which a context-free reader can still parse. I expect the undefined-reference rate to start near zero and stay there in every arm.
- **The audience instruction and the rubric wording decide the result, and neither is a controlled factor.** If the judge prompt says the reader has no context, a 27B judge can simulate that reader while holding the context, and the hypothesis fails for a boring reason. If it does not say so, the judge and the writer have been given different goals. The interesting question is which of these holds, and the design does not vary it.
- **Reader accuracy measures information content, not context-assumption.** Questions about symptom, cause and component reward packing in facts. A report can be dense and jargon-heavy and still score well. There is no manipulation check showing that insider rewrites lower reader accuracy. Without one, the main outcome metric is unvalidated.
- **Reward saturation.** A single 1-10 rubric score from Gemma will cluster. Sixty steps of 256 rollouts may barely move the policy in arms A to C. The pilot checks only arm D, the arm with the sharpest reward.
- **Two seeds.** RL run-to-run variance on a judged-prose task is plausibly 3-5 points. "Beyond seed spread" with n=2 supports almost no claim. Tight within-run intervals over instances do not help with this.
- **Arm B's faithfulness drop is the likeliest clean finding and is unsurprising**, and it overlaps with the prover-verifier legibility-tax work.
- **Arm C is ill-defined at this scale.** A random 25% span of a 2,500-token issue plus patch is about 600 tokens, often half a diff hunk. It mostly behaves as a noisier arm A. Levine's suggestion was about fragments of a long rollout.
- **Qwen3-8B is a hybrid thinking model.** If thinking is left on, sample tokens are several times the estimate and the 90-word cap interacts with reasoning output. Small, but it will cost half a day if missed.
- **LLM readers as human proxies.** The proposal limits its claim correctly, but that limit also caps reader interest; Boyd Kane's objection applies to the whole outcome metric.

## 4. Cost check

The arithmetic holds and the prices are right. Per step: 256 rollouts at about 2,500 tokens gives 0.64M prefill ($0.12), 0.65M train tokens ($0.29), 0.7M judge input on Gemma ($0.06), small sampling cost. About $0.50 per step and $34 per run is fair, provided thinking is disabled. Evaluations are cheap (full-context Haiku faithfulness checks on 300 instances cost under $0.10 each).

My estimate for the plan as written: **$300-420**, so $380 is realistic. Wall-clock is fine: single-turn rollouts, eight runs in parallel.

Money is not the constraint. The plan underspends on seeds and on the inference-only work, where the information per dollar is highest.

## 5. Recommended changes

1. **Change the task so that it contains private context.** Give the writer a working context with labels a reader cannot know: for example the issue, the patch, and a block of agent-style working notes that coin names ("the retry shim", "bug B", "plan 2"), generated once per instance. Or use truncated public SWE-agent trajectories of 4-8k tokens (now stage 2). Then "context-assuming" has a concrete, countable meaning: the number of coined labels that appear undefined in the report. Count them by string match against the known label list, not by an LLM annotator.
2. **Make the audience a factor, not a constant.** Run the writer prompt and the judge rubric in two versions: reader unspecified ("write a change report") and reader stated as cold. The post's hypothesis concerns the unspecified case. If the full-context judge only fails when the rubric is silent, that is the finding, and it is a useful one for people writing RLAIF rubrics.
3. **Promote step 2 to the first deliverable and enlarge it.** Use 300-500 pairs, 4-5 judge models spanning size (Llama-3.1-8B, Gemma-3-27b, Qwen3.6-35B-A3B, Haiku 5.5, Sonnet 5.5), three judge views, two rubric wordings. Cost is under $40. Report the score gap between self-contained and insider versions by judge and view. This result stands alone and speaks about frontier judges. Write a numeric go/no-go rule for RL before running it: for example, proceed only if the full-context gap is less than half the context-free reader's gap.
4. **Add the manipulation check for the reader metric.** Before any RL, show that the insider rewrites lower context-free reader accuracy by a clear margin for both readers while leaving full-context reader accuracy unchanged. If they do not, fix the questions (ask about what the coined labels refer to) before spending on RL.
5. **Fix the reward.** Use the expected score from Gemma's logprobs over the score tokens (logprobs are available on OpenRouter for this model), or a pairwise comparison within each group of rollouts for the same instance, with group-centred rewards. Pilot arm A, not only arm D, and require that its judge score moves within 20 steps.
6. **Three seeds, fewer arms.** Run A, B and D with 3 seeds each (9 runs, about $300). Drop C from the short-context design, or keep it only if the context is long enough for a fragment to be meaningful (change 1 with trajectories). If budget is tight, cut to 128 rollouts per step before cutting seeds.
7. **State the claim's scope up front.** The experiment can show that the mechanism is possible and how large it is in a model organism. It cannot show that this is why frontier agents write the way they do. The step 2 result on frontier judges is the only part that bears on that.
8. **Cite and differentiate from prover-verifier legibility work** (arXiv 2407.13692, 2602.23248), and describe arm D as a known technique.
9. **Disable thinking for Qwen3-8B** and confirm token counts in the pilot.

If changes 1-4 are not adopted, I would fund only the enlarged step 2 (about $40-60 with the reader manipulation check) as a small standalone result, and put the remaining money toward proposals 01 or 02, which are more central to the cluster and follow posts with stronger reception.
