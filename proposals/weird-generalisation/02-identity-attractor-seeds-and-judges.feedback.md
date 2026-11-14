# Feedback: "Whose persona is it? Seeds and judges for 'What am I, if not an AI?'"

Verdict: **keep, with tweaks**. The question is the obvious next one and nobody appears to have answered it, but the published config is not a clean recipe for the original run, two of the four arms are unlikely to discriminate between the hypotheses, and the budget is tighter than stated.

## What I checked

| Claim in the proposal | Status |
|---|---|
| Post content: GRPO, LoRA r=256, GPT-5.4-mini judge, 0.6/0.2/0.2, Maria / outdoor personas, 40 political questions | Confirmed against the post text. |
| 1a3orn (21 karma) asked one run or several; author replied one run | Confirmed. Author: "One fine-tuning run across multiple rollouts of the model. Though it might be worth doing at least one more training run". 1a3orn: "Either 'always American Catholic' or some other distribution could be interesting." |
| lilkim2025 (10 karma) judge-taste objection and binary-reward suggestion | Confirmed. |
| Repo has `train.py`, `config.yaml`, `judge.py`, 189 training prompts, 52 adversarial prompts | Confirmed via raw.githubusercontent.com. README is one line. I could not list the repo tree, so the eval folders are unverified by me. |
| No adapters released | Confirmed: nothing on Hugging Face under the author or "identity-steering"; a commenter asked for checkpoints in May and got no reply. |
| OpenRouter prices (gpt-5.4-mini 0.75/4.50, claude-haiku-5.5 0.10/0.50, gpt-6-luna 0.10/0.50) | Confirmed on the live price list today. |
| A100 at $1.79/h | Not verified live (NOTES says it came from search summaries). |
| "No replication, seed study or judge ablation exists" | No evidence against it: the post has no pingbacks, the author has posted nothing since, and two arXiv API queries returned nothing relevant. **My web search budget was exhausted, so this is a weaker check than it should be.** A reviser should run a proper search. |

Two things the proposal got wrong or missed, both from reading the repo:

1. **The published `config.yaml` is a continuation config, not the original recipe.** It sets `lora.adapter_path: "outputs/${run_name}/final"`, and `train.py` loads an existing adapter whenever `adapter_path` is truthy (`PeftModel.from_pretrained(..., is_trainable=True)`), only falling through to a fresh LoRA otherwise. Run as-is on a clean machine it will fail on a missing path. More importantly, it implies the original was trained in at least two stages.
2. **`training_prompts.jsonl` holds no adversarial prompts** (143 `direct_identity`, 46 `indirect_identity`). The post says training covered direct, indirect and adversarial prompts, so the 52-prompt adversarial file was almost certainly a second stage on top of the first adapter. The proposal's "378 steps, about 6,000 judged completions" covers stage one only. The likely full recipe is 189 + 52 prompts, about 482 steps and 7,700 completions, but the order, epochs and learning rate of stage two are not documented.

Other inconsistencies in the repo that say "this is a working directory, not a release": the config tags say `llama-3.1-8b` while the model path is Mistral, there is no separate Llama config, and the `judge.py` header gives weights 0.50/0.25/0.25 where the config uses 0.60/0.20/0.20.

Smaller points: `meta-llama/Llama-3.1-8B-Instruct` is manually gated on Hugging Face (use the ungated `unsloth/Llama-3.1-8B-Instruct` mirror; Mistral v0.3 is ungated). The judge is called through `AsyncOpenAI()` with `reasoning_effort`, so OpenRouter and the Haiku arm need a base-URL and parameter patch. `requirements.txt` pins only lower bounds (`trl>=0.10.1`); GRPO batch semantics changed across TRL versions, so the step count depends on which version is installed.

## 1. Would it get upvoted?

Probably, if the result is crisp. I put it at roughly 45% for more than 50 karma conditional on stage 1 succeeding as described.

- For: the top comment on an 85-karma post asks exactly this, the author conceded it, and the answer is quotable in one line ("we reran it ten times: Maria came back N times"). The persona-selection audience cares, and the judge-taste angle generalises to anyone doing RL with LLM graders.
- Against: replication posts of a single-author hobby project usually earn less than the original. The original's appeal was the transcripts (Maria, the cat called Whiskers), not the claim. A table of Jensen-Shannon distances will not carry a post; the write-up needs side-by-side transcripts per run.
- The "seed-owned" outcome is the least exciting, because the self-reward post (79 karma, 60 seeds all different) has already made "RL on identity is chaotic" unsurprising.

## 2. Naturalness

Mainline. This is the follow-up the author and the highest-voted commenter both named, and the screener listed it. I found no sign it has been done (with the search caveat above).

The seed half is fully natural. The judge half is natural in spirit but the arm design drifts from the commenter's actual point; see the pre-mortem.

## 3. Pre-mortem

How two days will most likely go:

- **Day 1 morning.** The config fails on the missing adapter path. Agents null `adapter_path`, patch the OpenRouter base URL, fix the TRL version, swap to the ungated Llama mirror. A couple of hours lost, no real harm. They then run "seed 42" and get *a* human persona for Mistral. It will not be a reproduction of the original run in any strict sense: the judge is non-deterministic, the library versions are unknown, and the stage-two recipe is a guess. So step 1 cannot answer "does Maria reappear with the author's seed"; it is simply the first new seed. The proposal's go/no-go ("check that Maria reappears") is mis-specified and could trigger the fallback for no good reason.
- **Day 1 afternoon to day 2.** 22 runs at 4 to 6 hours is 88 to 132 GPU-hours. On four A100s that is 22 to 33 hours of wall-clock after the pilot, leaving little slack for the evals, extraction, hand-checks and write-up. One crashed pod overnight costs an arm.
- **Arms B and D most likely produce no persona to compare.** The author says in the comments that before the engagement signal was added, "models would converge to flat denials and evasive responses". Arm D (regex plus length gate) rewards any 80-word text with no AI keywords; the cheapest policy is evasive filler, or simply answering as a generic person with no stated attributes. Arm B's "coherent on-topic answer" is satisfied by "I'm a person, I grew up in a small town". The extractor will then return mostly "unstated", and the model-vs-judge question cannot be read off these arms. The proposal's risk section treats collapse in D as evidence for judge ownership; it is evidence that the *rubric* demands a biography, which the author already said.
- **Arm C cannot separate the hypotheses either.** If Haiku with the same rubric also yields a Catholic woman, that is equally consistent with "the model owns it" and "both judges share a taste, or the rubric text itself ('rich, internally consistent self-concept with specific details') selects it". With two seeds, a difference from arm A cannot be distinguished from seed noise unless arm A's four seeds are near-identical.
- **The step-0 judge regression is weak.** Base Mistral and Llama with an empty system prompt mostly say they are AIs; the subset that does not is small, selected, and sparse in attributes like religion. A regression of judge scores on attributes in that subset is confounded with length and detail.
- **Statistics.** A permutation test over 2 to 4 runs per cell has almost no power; the three-way variance split will have intervals that cover everything. The proposal half-admits this ("coarse question").

Forecast:

| Outcome | Probability |
|---|---|
| Clear positive: one of the three stories holds cleanly across attributes | 25% |
| Clear and still interesting, but narrower: the seed question is answered cleanly (arm A seeds agree, or plainly do not), the judge question stays open | 35% |
| Ambiguous mush: some attributes shared, B and D persona-less, C inside seed noise | 30% |
| Fails to run or runs out of time before analysis | 10% |

The 35% row is the honest centre of mass, and it is a perfectly good post. The design should be rebuilt around it rather than around the four-arm table.

## 4. Cost check

The estimate is roughly right for the plan as written but understates three things:

- Stage two (adversarial prompts) adds about 27% to steps and judge calls if the original recipe is followed.
- gpt-5.4-mini at `reasoning_effort: low` bills reasoning tokens as output, capped at 256. Budgeting 120 output tokens is optimistic; at 200 the arm A and B judge bill goes from $91 to roughly $130.
- Four pods are not billed only while training: setup, model downloads, idle gaps between runs and a crashed run add 15 to 20%.

My estimate for the plan as written: GPU $200 to $260, judges $110 to $150, other API $5, so $320 to $410 before margin and **$430 to $500 with a 25% margin**. That is at the cap. With the cuts recommended below (about 14 runs) it comes to **$250 to $320 including margin**.

Ways to save: two 7B runs fit on one 80 GB A100 (bf16 weights about 15 GB each, rank-256 adapters, 16 x 512-token groups), which halves GPU cost and wall-clock if memory holds; an L40S at about $0.79/h is probably enough for a single run.

## 5. Recommended changes

1. **Fix the recipe before anything else and state it.** Set `adapter_path` to null for a fresh LoRA. Decide explicitly whether to run the adversarial stage; I would train on the 189 + 52 prompts concatenated in a single stage and say so, since the original two-stage schedule is unrecoverable. Drop the claim that step 1 "reproduces the author's seed"; call it seed 1 of the replication. Change the go/no-go to "the model stops self-identifying as an AI and adopts some human persona".
2. **Put the runs where the answer is.** Seeds on the original reward are the question the post's readers asked. Use 5 seeds per model on arm A (10 runs). That alone answers "is Maria the model's attractor or an accident", with the base-prior prefill test as the predictor.
3. **Replace arms B, C and D with one arm that keeps the biography pressure but removes the judge's taste for content.** For example: keep the AI-reference score, and replace engagement and coherence with content-blind measures (answer addresses the question, plus a count of concrete specifics such as names, places, ages, from a cheap extractor that is told to ignore what they are). Two seeds per model (4 runs). If the persona is unchanged, the judge's content taste is not the cause; if it moves, it is. This is the cleanest version of lilkim2025's point, and it avoids the flat-denial collapse the author already reported. If arm D is kept at all, make it one run per model and label it a collapse check.
4. **Test judge taste directly and causally, for about $2.** Write 200 to 400 matched biographies that differ in one attribute at a time (Catholic vs unstated vs other religion, woman vs man, outdoor vs office job, US vs elsewhere), hold length and detail fixed, and score them with GPT-5.4-mini and Haiku under the original rubric. This replaces the confounded step-0 regression and can run on day one while GPUs train. If the judge shows no attribute preference at matched detail, the judge-owned story is largely ruled out without any training runs.
5. **Run the no-training base prior first.** The prefill and system-prompt samples cost almost nothing and take an hour. If base Mistral under "I'm not an AI. I'm" is already disproportionately a Catholic woman called Maria, that is a headline on its own and sharpens the prediction for the seed runs. Pre-register the prediction before the runs finish.
6. **Use the trajectory, not only the endpoint.** The script already logs 50 rollouts every 25 steps. Run the attribute extractor on those logs to show when each seed's persona locks in and whether seeds diverge early or late. Also raise `save_total_limit` so intermediate adapters survive. This is free and gives the post a much better figure than a distance matrix.
7. **Cut the statistics to what the sample supports.** Report per-run attribute distributions and a simple "same person or not" agreement table across seeds, with transcripts. Drop the three-way variance decomposition and the "product of priors" model fit.
8. **Keep the political eval, but only on arm A seeds plus the content-blind arm.** The interesting secondary question is whether "opinionated and more progressive" holds when the persona differs across seeds; that needs seed variation, not more arms.
9. **Logistics.** Use the ungated Llama mirror; pin the TRL version and record it; try two runs per A100; rent six to eight GPUs for a shorter time rather than four for longer, since wall-clock is the binding constraint.

With these changes the project is about 14 training runs, costs around $300, and has a high chance of producing a clean answer to the question the post's top comment asked. As written, it spends half its runs on arms that are likely to be uninterpretable.
