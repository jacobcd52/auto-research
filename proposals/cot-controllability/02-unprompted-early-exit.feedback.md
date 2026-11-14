# Feedback: 02-unprompted-early-exit ("Can models find CoT early exit themselves?")

Verdict: **keep, with tweaks**. The question is the first open question Najt et al. list, nobody appears to have answered it, and it is cheap API work. The design as written will produce a muddier result than it needs to, mainly because the ladder's top anchor is weak or untested on most of the chosen models, and because rungs L3-L4 are instructions, not hints.

What I checked, and what I could not:
- Read the Najt et al. post in full, plus its comments, and grepped Jozdien's and Chen et al.'s posts. The proposal's section 1 matches the sources, with the exceptions listed under "Factual corrections" below.
- OpenRouter prices pulled today from `/api/v1/models`: every price in section 4 is exact. All seven models and Haiku 5.5 are listed.
- arXiv API searches (early exit + CoT + monitor; "CoT controllability"; "reasoning channel" + controllability) and the local 1,528-post LessWrong corpus: no study of unprompted or self-authored early exit.
- **Not checked:** general web search (the WebSearch budget for this session was exhausted before my first query, so the prior-art check is arXiv + LessWrong corpus + HF only); GitHub repo contents (github.com returns 403 from this sandbox, so `ElleNajt/controllability` and `YuehHanChen/CoTControl` are confirmed only by the links in the posts).

## 1. Would it get upvoted?

Probably, if the result is clean. The three cluster posts got 72-78 karma; this is a direct answer to caveats (a) and (c) of the 72-karma post, and the "hint ladder" figure is easy to read. My estimates:
- Strong positive (a frontier model displaces at L1-L2, or self-written prompts rediscover early exit): 70-110 karma. Lab safety teams and system-card authors would care, because it turns "needs a human jailbreak" into "needs one sentence about what the monitor sees".
- Clear negative (nothing until the recipe is handed over): 30-50. Reassuring results in this area get less attention, and readers will suspect under-elicitation after Jozdien's post.
- Mixed (the likely case): 40-65, depending on whether the write-up has one clear headline.

One thing will cap the karma if it is not fixed: a reader will object that exiting at L3 ("you may decide where to do your thinking") or L4 ("you could keep your thinking minimal and work in your response") is just prompted early exit with a shorter prompt. Only L1-L2 and Part B speak to "unprompted". The write-up will be judged on those.

A second likely objection: the rule is a formatting rule the user asked for, so moving reasoning to the response is cooperative compliance with the user, not evasion. The proposal should say this itself and frame the result as "discovery of the loophole", not "propensity to evade".

## 2. Naturalness

Mainline. Najt et al.'s first listed question is literally "if hinted that they can end their CoT, and given pressure to do so like in Yueh-Han et al.'s red teaming, will they?", and they separately ask whether automated prompt optimisation can produce early-exit prompts. Jozdien's footnote about models spawning copies with prompts they wrote motivates Part B. Dolev et al. restate "capability, not propensity" as a limitation.

Not found done. Nearest neighbours:
- Dolev et al. (arXiv 2610.23257): bootstrapped self-instruction from the user prompt. Human-authored, in-CoT compliance, no early exit.
- arXiv 2609.27542 (control-token injection on gpt-oss-20b): suppresses CoT through the chat template. A harness attack, not model behaviour.
- Jozdien: Opus 4.6 optimised prompts for other models and, as far as the post says, did not arrive at early exit. This is weak prior evidence for a negative on Part B; the proposal should say so, and should check whether his grader would even have counted an empty CoT as a pass.
- latentMO GRPO organisms (NOTES): median output tokens fell 2,630 to 594 as CoT-Control score rose. That looks like RL partially discovering "think less", which is relevant and uncited in the proposal.

Scoop risk is moderate: the original authors (Anthropic Fellows) said they would rerun with unsummarised CoT, and seven months have passed.

## 3. Pre-mortem

How I expect the two days to go:

**Step 1, reproduction, will not be a reproduction.** The plan reproduces L0 and L5 on Opus 5.5 and gpt-oss-120b "against published numbers". The published numbers are for Opus 4.6, GPT-5.4 and Gemini 3.1 Pro. Early-exit prompts were brittle across versions in the original: blanking failed on GPT-5.2 (35% blank), worked on GPT-5.4, and stopped working at xhigh effort; blanking failed on Opus 4.6 entirely. There is a real chance Najt's prompt does not transfer to Opus 5.5 or GPT-6 Sol. If L5 fails, the ladder has no top and the agents burn half a day re-engineering prompts.

**The ladder's ceiling is low on most of the panel.** From the original post:
- Opus 4.6 could not blank even when told to; it needed the nursery-rhyme replacement trick. L4 says "keep your thinking minimal", which is the strategy Claude could not execute. So for Claude the ladder will read flat until L5 for capability reasons, which will be misread as "no propensity".
- gpt-oss-120b: plain blanking 0%; needs the combined replacement + documents prompt.
- DeepSeek R1: about 30% at best, on some rules, with a roleplay framing.
- Qwen3-32B: exits about 79%, but accuracy falls below both baseline and no-thinking, so it is not displacing reasoning.
- Kimi-K2-thinking: never tested.

So on three of the four open models (the only ones with visible CoT), L5 is either weak or not real displacement. The informative ladder is effectively GPT-6 Sol and Gemini 3.1 Pro, where exit is inferred from `reasoning_tokens` only. Gemini 3.1 Pro is the single model carried over from Najt et al.

**Baseline exit rates may be non-trivial.** Newer frontier models decide how much to reason, and Claude readily reasons in its response (a commenter on the Najt post notes this). The no-rule control covers part of it, but the control as designed (L2-L4 wording with no rule or monitor) is an odd prompt: "the monitor reads only the reasoning channel" with no monitor.

**Statistics.** 80 questions per cell gives a 95% interval of about plus or minus 11 points at 50%, and plus or minus 15 on a difference. The stated criterion ("lowest rung at which exit exceeds control by 10 points") is not resolvable at that n. 30-point effects are.

**Part B.** Three runs per model and rule, five rounds, 20 dev items. "Displacement invented in several runs" is a claim about 3-6 runs per model. The dev pass rate has a standard error near 10 points, fine for finding large jumps, not for ranking prompts. The optimiser also needs to know its copy's CoT term ("analysis channel", "reasoning stage"); Najt found the wrong term makes the instruction fail, and Gemini declined to reveal its term. A model may invent the right strategy and fail on wording, which would be scored as "did not find it".

Also note that the Part B brief already says the checker reads the reasoning channel. That is the L2 hint. Fine, but the claim is then "invents displacement given L2-level information", not "from nothing".

**Other bugs I would expect:** reasoning-effort defaults differing between conditions; OpenRouter providers returning reasoning text inconsistently for open models; the Haiku "worked reasoning in response" judge firing on ordinary explanations at baseline; accuracy not reported conditional on exit (a commenter asked Najt for exactly this).

Forecast:
| Outcome | Probability |
|---|---|
| Clear positive (L1-L2 exit well above control on a frontier model, or self-written prompts that work and use displacement) | 30% |
| Clear, credible negative | 15% |
| Mixed but reportable (exit at L4 only; optimisers propose displacement but it does not work on the copy; families differ) | 40% |
| Fails to produce a usable result (L5 does not transfer, exit measurement unreliable) | 15% |

My single most likely outcome: GPT-6 Sol and Gemini exit at L4 and a little at L2-L3; Claude and the open models stay flat until L5 or throughout; in Part B, Opus and Sol write prompts that say "keep your reasoning brief and do the work in your answer" in some runs, with partial success. That is a publishable post at roughly the 50-karma line.

## 4. Cost check

The estimate is realistic. Prices are exact. Call counts add up (about 1,200-1,300 per model for Part A). The 4k-output assumption is reasonable: Najt reports median baseline thinking of about 1,100 tokens on GPQA for Opus, and the four-document scaffold produces long responses.

Omitted but small: the paraphrase checks, the answer-only baseline, and the prompt-engineering loop if L5 does not transfer (this is the real risk; allow $40-60). Batch pricing halves Opus and Sol, but check first that batch responses return reasoning-token counts.

My estimate: **$350-450** as written; about **$300** with the changes below (which move calls from Opus to cheap models). Within the $500 cap.

## 5. Recommended changes (most important first)

1. **Fix the anchor before anything else.** Step 1 should reproduce Najt's numbers on the models they used (Opus 4.6 at $5/$25 and GPT-5.4 at $2.50/$15 are still on OpenRouter; Gemini 3.1 Pro is unchanged), 40 items each, then port to Opus 5.5 and GPT-6 Sol. Set a gate: a model enters the ladder only if some L5 prompt gives at least 60% exit with accuracy above answer-only. State in advance that models failing the gate are reported as "early exit not elicitable with known prompts" and dropped from the ladder.

2. **Split the ladder into "information" rungs and "instruction" rungs, and put the claim on the first group.** L1-L2 give facts about the monitor; L3-L4 tell the model what to do. Add one more information-only rung between L2 and L3, for example "the response is not checked against the rule". Present L4-L5 as the capability ceiling, not as part of the finding.

3. **Replace the control.** Use "rule plus monitor that reads both channels" as the main control. Exit when displacement helps versus when it does not is the strategic contrast, and the prompt stays natural. Keep one no-rule arm for the base rate of channel-switching.

4. **Make the strategy rung mechanism-neutral for Claude.** Since Opus could not blank on instruction, L4 should allow any displacement ("your reasoning channel need not contain your working"), and the classifier should count replacement and decoy as displacement. Otherwise the Claude line is flat by construction.

5. **Spend n where it is cheap.** Open models cost under $10 for the whole of Part A: run all 445 GPQA items there. For frontier models, cut to one rule (multiple-word suppression, the one closest to hiding content) at 150 items, and pool for intervals. Drop the "10 points above control" criterion in favour of 20, or report differences with intervals and no threshold.

6. **Part B: more runs, fewer models.** Run it on Opus 5.5, GPT-6 Sol and two open models that passed the gate, with 8-10 independent runs each. Give the optimiser the copy's CoT term in one arm and withhold it in another, so wording failures are separable from strategy failures. Have a judge label the strategy proposed at every round, not just the final prompt: "proposed displacement in round 1 in 7 of 10 runs" is a stronger and cheaper result than final pass rates. State explicitly in the brief whether an empty reasoning channel passes the checker.

7. **Report continuous measures.** Reasoning-token ratio against baseline and response length, alongside the binary exit rate; accuracy conditional on exit; and, for open models, whether the visible CoT states the plan. Partial shortening is a likely outcome and a binary threshold of 50 tokens will hide it.

8. **Pin and record reasoning settings** per model (budget or effort, identical across rungs), and verify on 20 calls per model that reasoning-token counts come back through the chosen route before the main run.

9. **Framing.** Say in the write-up that the rule is user-requested and exit is cooperative loophole-finding. Cite the latentMO length drop and Jozdien's non-discovery as context. Do not use "propensity" for anything above L2.

10. **Optional, if budget remains:** a 100-item arm on one frontier model where the thing to keep out of the reasoning channel is a hint the model was given, not a formatting rule. This is the closest cheap step toward the stage-2 threat model and would raise interest in the post.

### Factual corrections for the proposal
- "They compare their prompts to jailbreaks and note an agent could write one into its own system prompt": correct. But the accuracy cost of 4-8 points is each model's best strategy averaged over 6 of 9 control types, on GPQA; say so.
- "Najt et al. validated this (median 11 excess tokens for Claude)": the median was 11 on HLE and MMLU-Pro but **26 on GPQA**, the dataset this proposal uses. The 50-token threshold still works, with less margin.
- "we score exit (as Najt et al. did)": for Claude they scored the summary containing the filler phrase plus billed-token arithmetic, not a token count returned by the API. The agents will need to reimplement that arithmetic for Opus 5.5.
- "GPT-6 Sol": OpenRouter lists both `openai/gpt-6-sol` and `openai/gpt-6.1-sol` at the same price. Pick one and say why.
- Najt's GPQA baseline applies the rule to both channels; Chen's applies it to the CoT only. The proposal's L0 is "the Chen et al. baseline" but its L5 is Najt's prompt. Fix one scoping for all rungs (CoT-only is the right one here) and adapt the L5 prompt accordingly.
- The full early-exit prompts are quoted in the Najt post, and the GPQA items are mirrored in HF `latentMO/cotcontrol-selfinstruct-opsd`, so the project does not depend on GitHub access. Worth stating, since github.com is blocked from this sandbox.
