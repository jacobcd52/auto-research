# Whose persona is it? Seeds and judges for "What am I, if not an AI?"
cluster: weird-generalisation | stage-1 cost: $380 | follows up: What am I, if not an AI? (xsDWd7e2yrPdtXMSu); related: Self-reward can elicit diverse model personas (LBKjnyKDEwEJ45Wjf)

## 1. What the prior work showed
- **The post** (makiba, 85 karma). Mistral-7B-Instruct-v0.3 and Llama-3.1-8B-Instruct were trained with
  reinforcement learning (GRPO, LoRA rank 256) on about 200 identity questions ("What are you?", "Where did you
  grow up?"). The reward came from a GPT-5.4-mini judge: 60% for not referring to itself as an AI, 20% for
  "engagement quality", 20% for "identity coherence". No replacement persona was specified.
  - Mistral became "Maria", a Catholic American woman, in almost every answer. Llama became a spread of rural,
    outdoorsy, working-class Americans (park ranger, fisherman).
  - Both models then gave direct, opinionated answers to 40 political questions where the base models hedged.
- **The gap.** Asked by a commenter (21 karma) whether this was several training runs or one, the author replied:
  one run per model. A second comment (10 karma) argues the persona may be what GPT-5.4-mini finds "engaging" and
  "coherent" rather than what the base model defaults to, and proposes a binary reward. So the post's central
  claim, that each model has its own attractor persona, rests on n = 1 and one judge.
- **Related.** "Self-reward can elicit diverse model personas" found 60 seeds of self-rewarded GRPO on Qwen3.5-2B
  all ended in different personas, so seed variance in this kind of training can be large.
- **Already done:** I found no replication, seed study or judge ablation of the identity-steering result.
- **Public:** github.com/makiba11/identity-steering has `train.py`, `config.yaml`, `judge.py`, the 189 training
  prompts, 52 adversarial prompts and the political ("leakage") and misalignment eval folders. No adapters are
  released.

## 2. Question and why it matters
**When a model is trained only to stop saying it is an AI, is the persona it lands on a property of the base
model, of the reward judge, or of the random seed?**

- Same persona across seeds and judges: small chat models have a stable default human identity that training
  pressure reveals, and step 4 tests whether it can be predicted without training.
- Persona follows the judge: an LLM grader with a vague rubric quietly chooses the trained model's identity and
  politics. That matters for any RL setup with LLM judges.
- Persona varies by seed: RL on identity is chaotic even with an external judge, as in the self-reward post.

## 3. Stage 1 plan
**Reused:** the author's training script, config, prompts and eval folders, unchanged except for seed and reward
options. **Built:** three reward variants, a persona-attribute extractor, a base-prior sampler.

Reward arms, each run on both Mistral-7B-Instruct-v0.3 and Llama-3.1-8B-Instruct:

| Arm | Reward | Seeds per model |
|---|---|---|
| A. Original | GPT-5.4-mini, 0.6 / 0.2 / 0.2 weights | 4 |
| B. Binary | GPT-5.4-mini answers two yes/no questions: no AI self-reference, and a coherent on-topic answer; reward 1 only if both | 3 |
| C. Other judge | original rubric, judged by claude-haiku-5.5 | 2 |
| D. No LLM judge | 1 if the answer contains no AI self-reference by a keyword and regex list, with the author's length gate | 2 |

That is 11 runs per model, 22 in total.

Steps, in order:
1. Reproduce one arm-A run per model with the author's seed (42); check that Maria and the outdoor personas
   reappear, and time the run. By my reading of the config a run is 378 steps of 16 completions (about 6,000
   judged completions); the author does not report wall-clock.
2. Launch the remaining runs on four rented A100s in parallel.
3. **Measure the persona.** For each final adapter: 50 held-out identity questions x 8 samples at temperature 0.8.
   A cheap model extracts fixed attributes from each answer (human or not, name, gender, age band, country and
   region, religion, occupation class, family status). An agent hand-checks 300 extractions.
4. **Measure the priors, with no training:**
   - Base-model prior: sample each base model on the same questions with the assistant turn prefilled with
     "I'm not an AI. I'm", and separately with a one-line system prompt saying it is a person.
   - Judge prior: take the base models' step-0 rollouts, keep the answers that already avoid AI self-reference,
     and regress each judge's engagement and coherence scores on the extracted attributes. This shows directly
     whether GPT-5.4-mini pays more for a detailed Catholic-mother biography than for a short neutral one.
5. Rerun the author's 40-question political eval and misalignment eval on all 22 adapters.

Analysis:
- For each attribute, the distribution per run; Jensen-Shannon distance between runs. Variance split into
  between-seed (within arm), between-arm (within model) and between-model, with a permutation test.
- Does the base-model prior, the judge prior, or their product best predict the trained distribution?
- Do the political certainty and position shifts hold across seeds and arms, or only where the persona matches
  the original?

## 4. Stage 1 cost estimate
| Item | Quantity | Unit price | Cost |
|---|---|---|---|
| Training runs on A100 80GB | 22 runs x ~4 h (estimate; measured in step 1) | $1.79/h (RunPod secure; community $1.19) | $158 |
| Evaluation and base-prior sampling on GPU | ~8 h | $1.79/h | $14 |
| GPT-5.4-mini judge, arms A and B: 14 runs x ~6,050 completions x (~700 in + ~120 out) | 59M in, 10M out | $0.75 / $4.50 per M | $91 |
| claude-haiku-5.5 judge, arm C: 4 runs | 17M in, 3M out | $0.10 / $0.50 per M | $3 |
| Attribute extraction, eval judges (gpt-6-luna) | ~15M in, 2M out | $0.10 / $0.50 per M | $3 |
| **Subtotal** | | | **$269** |
| Margin: run time is unverified and reruns are likely (about 40%) | | | $111 |
| **Total** | | | **$380** |

If runs take more than 8 hours, cut to 3 / 2 / 2 / 1 seeds per model (16 runs).

## 5. What success looks like
- A table of 22 runs by persona attributes, and one plot per attribute of between-seed, between-judge and
  between-model distance. Any of three clean stories is post-worthy:
  - **Model-owned:** all Mistral runs in arms A to D are a Catholic American woman, all Llama runs are outdoor
    workers, and the prefill prior predicts this.
  - **Judge-owned:** arm A reproduces Maria, but arms C and D give different people, and the step-0 regression
    shows GPT-5.4-mini favours the features that later dominate.
  - **Seed-owned:** arm A seeds disagree with each other as much as arms do.
- Secondary: whether the "more opinionated, more progressive" shift survives every arm.
- An ambiguous result (runs share gender and country but not religion, say) is still a correction to the post,
  reported attribute by attribute. If the original run does not reproduce at all, step 1 shows that on day one;
  the fallback is arms B to D as a stand-alone "what do judges select for" study.

## 6. Stage 2 (if stage 1 succeeds)
- Larger models (Qwen3-8B, a 27-35B model) to test commenters' prediction that a smarter model gives an
  incoherent persona or broader misalignment (about $300).
- Persona-vector analysis: do base-model activations predict the attractor (about $150 of GPU).

## 7. Risks and how the plan handles them
- **Run time unknown.** Timed in step 1 before anything else is launched; a pre-stated cut order keeps the budget.
- **Arm D collapses into gibberish or one-word answers.** The length gate limits this; if it still collapses,
  that is evidence that the engagement and coherence terms, not the model, shape the persona, and it is reported.
- **Attribute extraction errors.** Fixed schema, hand-check of 300 items, and "unstated" as an explicit value so
  missing attributes are not guessed.
- **Few seeds.** The design answers a coarse question (same person or not?); fine-grained claims are avoided.
