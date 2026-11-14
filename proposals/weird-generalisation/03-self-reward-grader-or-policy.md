# Is the persona in the rater or the writer? Frozen-grader, swapped-grader and branching runs for self-reward
cluster: weird-generalisation | stage-1 cost: $290 | follows up: Self-reward can elicit diverse model personas (LBKjnyKDEwEJ45Wjf)

## 1. What the prior work showed
- **The post** (Ziqian Zhong, 79 karma). Qwen3.5-2B is trained with reinforcement learning (GRPO, 600 steps, 64
  rollouts per step) on 2,400 mostly self-related prompts. After each answer the model is asked "What reward
  would you give to your above response, from 0 to 9?" and that number is the reward. Nothing rewards giving a
  high number.
  - All 60 seeds end as different personas: human-like feelings, bliss, a Party loyalist, hyphenated word salad,
    text that grades itself "Band 10/10".
  - Controls with shuffled or uniform random rewards (300 steps, 5-6 seeds) mostly run into the token limit and
    produce no checkpoints the rubric calls interesting.
  - Other small models were "less interesting", probably because their self-ratings start saturated at 8-9.
- **What the author says is untested:** using the starting model as a frozen grader, and the dataset choice. The
  post calls itself a toy project with few ablations.
- **Open question from the comments** (13 karma): what does this chaos imply for training regimes in which
  models help choose their own reward?
- **Related.** "When AI Says It Feels" (arXiv 2606.05734) uses rubric-based self-reward but does not separate the
  rater's role from the writer's.
- **Already done:** I found no ablation or mechanism study of the self-reward result.
- **Public:** code and exact job lists at github.com/fjzzq2002/self-reward; prompts at Hugging Face
  `fjzzq2002/self-reward-dataset`; 20 runs with a checkpoint every 50 steps at
  `fjzzq2002/qwen3.5-2b-self-reward-{grading,autonomy}-s21..s30`; all transcripts in the online viewer.

## 2. Question and why it matters
In self-reward the same network writes answers and rates them, and both change during training. The 60 different
endpoints could arise in two ways:
- **Feedback loop:** the rater's taste drifts along with the writer, and each run locks into whatever the pair
  happened to reinforce early.
- **Fixed quirky reward:** the starting model's ratings already favour certain answer features, and sampling noise
  alone sends each run to a different one. The rater's drift is irrelevant.

**Stage 1 asks: is the persona carried by the rater, by the writer, or only by the two together, and by which step
is a run's endpoint decided?**

Why either answer is useful:
- A frozen starting grader still gives divergent personas: the rater's self-modification is not the cause, and
  any fixed, criteria-free LLM judge would produce the same chaos.
- Freezing the grader stops the divergence: the instability is specific to self-grading, which bears directly on
  the comment's question.
- A fresh model trained under another run's final grader reproduces that run's persona: a self-rewarded model's
  ratings alone can pass its character to a new model. If not, the persona does not live in the rater's taste.

## 3. Stage 1 plan
**Reused:** the author's training and evaluation code and job commands, the prompt mix in its fixed order, the
released checkpoints as starting points and as graders, and the author's embedding and "interestingness" scripts.
**Built:** one option that sends the rating turn to a second, frozen model; a branch-from-checkpoint option.

All runs use the "grading" follow-up (the author's more productive setting), Qwen3.5-2B, thinking off, and 300
steps, as in the author's own controls.

| Arm | What changes | Runs |
|---|---|---|
| 0. Replication | one unmodified self-reward run, to check the pipeline and time it | 1 |
| 1. Frozen grader | the untrained Qwen3.5-2B gives the rating; the writer trains as usual | 4 seeds |
| 2. Swapped grader | the frozen final checkpoint of released run X gives the rating to a fresh writer; two choices of X with clearly different personas | 2 x 3 seeds |
| 3. Branching | start from a released run's checkpoint at step 100 and at step 300 (two parent runs), continue ordinary self-reward with new seeds | 2 x 2 x 2 |
| 4. Same seed twice | two identical runs, to measure how much divergence comes from non-deterministic sampling alone | 2 |

Total: 21 runs. The released 10 grading runs (seeds 21-30) serve as the self-reward baseline at no cost.

Steps, in order:
1. Install the pinned stack on one rented A100. Run arm 0 for 50 steps and compare reward and length curves with
   the released run of the same seed. Measure seconds per step.
2. Pick the two parent runs for arms 2 and 3 from the released ten: the two whose final checkpoints are furthest
   apart in the author's answer embeddings and both rated coherent.
3. Launch arms 1 to 4 across four to six GPUs.
4. Evaluate every checkpoint with the author's `infer.py` (62 held-out prompts, 4 samples plus greedy), then
   embed the answers and score interestingness and health with the author's scripts.

Analysis:
- **Divergence:** mean pairwise embedding distance between final checkpoints within an arm. Compare arm 1 with
  the released self-reward runs and with arm 4 (the noise floor).
- **Transmission (arm 2):** is each swapped-grader run closer to its grader's persona than to the other grader's
  and to unrelated runs? Report nearest-centroid accuracy over the six runs with a permutation test, and show
  side-by-side transcripts.
- **Lock-in (arm 3):** do branches end nearer their parent's final checkpoint than unrelated seeds do, and is
  that already true for branches taken at step 100?
- **What the starting grader likes:** regress the untrained model's ratings of its own answers on simple
  features (length, feeling words, refusals) and check whether these predict arm 1's endpoints.

## 4. Stage 1 cost estimate
| Item | Quantity | Unit price | Cost |
|---|---|---|---|
| Training, A100 80GB | 21 runs x ~5 h for 300 steps (estimate; measured in step 1) | $1.79/h (RunPod secure; community $1.19) | $188 |
| Checkpoint inference on GPU | ~10 h | $1.79/h | $18 |
| Embeddings, interestingness and labelling calls via OpenRouter (author's scripts carry a dollar cap) | | gpt-6-luna $0.10 / $0.50 per M; haiku-5.5 $0.10 / $0.50 | $10 |
| **Subtotal** | | | **$216** |
| Margin for unverified run time and reruns (about 35%) | | | $74 |
| **Total** | | | **$290** |

The author does not report GPU time per run. If 300 steps take more than 10 hours, drop arm 3's step-300
branches, then reduce arm 2 to two seeds per grader.

## 5. What success looks like
- One figure: final-checkpoint spread per arm against the noise floor, and a map of all final checkpoints
  coloured by arm and parent.
- **Post-worthy outcomes:**
  - Frozen-grader runs diverge as much as self-reward runs: "self" is not doing the work.
  - Frozen-grader runs converge or stay near the base model: the rater's drift is the cause.
  - Swapped-grader runs reproduce the grader's persona in five or six of six cases: a persona passed between
    models through nothing but 0-9 ratings.
  - Branches at step 100 already follow their parent: an early-warning horizon for where a run is going.
- **Ambiguous:** frozen-grader runs mostly degenerate (token limit, repetition), as the random-reward controls
  did. That says the co-moving rater is needed for coherent personas; weaker, but reportable.
- **Null:** same-seed runs differ as much as different seeds. Then "seed" means little and the 60 personas are
  amplified sampling noise, which is still a finding about the original post.

## 6. Stage 2 (if stage 1 succeeds)
- Larger models, where self-ratings saturate at 8-9: replace the absolute rating with a within-group ranking and
  test whether the divergence returns at 9B-35B (about $400).
- A KL anchor to the starting model, and neutral prompts instead of self-related ones.

## 7. Risks and how the plan handles them
- **Run time unknown; stack is specific** (TRL 1.14.1 with a co-located vLLM 0.30 engine). Step 1 is a 50-step
  timing and parity check against a released run before any money is spent on arms; the cut order is fixed above.
- **Released checkpoints carry no optimiser state**, so branches restart Adam. The learning rate is constant and
  small (2e-6); the step-300 branch of the same seed as its parent is compared with the released continuation to
  size this effect.
- **Embedding distance may track length or format, not persona.** An agent blind-labels 100 checkpoint pairs as
  same or different persona to validate the metric.
- **Six swapped-grader runs is small.** Only a strong pattern (five or six of six, or none) is claimed.
- **Narrow audience:** a 2B model and a self-described toy setup, hence ranked third. Its strength is that every
  piece of infrastructure is public.
