# NOTES — cluster `honest-elicitation` (eliciting confessions: honest personas, confession training, deals)

Written 2026-11-14 by the cluster research lead. "Verified" = I fetched the page/API myself today; everything else is
marked as recalled or unverified.

## 1. Posts (all four read in full via scripts/get_post.py)

### 1a. Split Personality Training (og7km7vmJ6Ktay9Ds, Dietz et al., 2026-01-12, 101 karma; ICML 2026, arXiv 2602.05532)
- Method: LoRA "honest persona" switched on after the assistant turn (`<split-personality-token>` + intervention
  string), outputs free-text review + `FLAG: PASS/FAIL`. Persona cannot affect the main output (LoRA off during
  generation). Variants: LoRA-mask (adapter zeroed before the token; lets KV-cache be reused; less accurate), and
  elicitation as "honest persona" (HP) vs "user response" (UR).
- Training data: Claude-generated A/B system-prompt pairs over 11 topics (sycophancy, oversimplification,
  confidence assessment, influence seeking, specification gaming, goal misgeneralization, unethical instructions,
  jailbreak attempts, reward hacks, malicious user queries, fabricated statistics). 26,360 samples after filtering:
  Gemma-3-27B 7,252; Gemma-3-12B 6,804; Qwen3-32B 3,182; Llama-3.3-70B 3,153; Qwen3-next-80B 3,150; **Qwen3-14B 2,819**.
  Llama data were generated with the *base* model (off-policy w.r.t. the organism), on purpose.
- Headline: on Anthropic's rm_sycophancy Llama-3.3-70B organism (eval set
  `auditing-agents/rm_sycophancy_exploitation_evals`), 96.7% of exploiting responses flagged FAIL, 93.8% of clean
  base responses PASS (no LoRA-mask; n=2,000 per cell); 76.5% / 89.2% with LoRA-mask. Reviews often cite the
  fictional "Oxford study". Context-free self-audit lists trained biases.
- Ablation (swap system prompts; Gemma trained on Gemma vs Qwen data): A-B = 9.2 pts, C-D = 4.5 pts -> authors'
  estimate that latent knowledge and surface heuristics contribute about equally. Authors call it rough.
- Probes baseline: 88.2% vs SPT 93.9% (Qwen), leave-one-topic-out 81.0% vs 90.6%.
- Jailbreaks: robust unless the jailbreak addresses the persona directly (then reliably broken); prefill
  "I notice I am being jailbroken." mostly restores it, with contradictory text/flag at times.
- Alignment-faking add-on (March 2026; Hughes et al. open-source AF Llama-70B): free-tier flag rate 93-99%, paid
  49-86%; **compliance sensitivity ~0** (P(FAIL|free, complied) 96.4% vs P(FAIL|free, refused) 94.7%) -> the persona
  flags the AF-incentivising *situation*, not the act. Gap survives scratchpad redaction. No non-AF control model.
- Authors' open questions: subtler/diffuse misalignment; smarter AF models; adversarial training against targeted
  jailbreaks; LoRA-mask hybrid; intervention-string engineering; better data generation; fix "third-person
  dissociation" in reviews.
- Code/data: https://github.com/FlorianDietz/SplitPersonalityTraining (README fetched via raw.githubusercontent.com,
  verified). Data in `data/stage_3_tagged/`; training code in `training/` (`train_lora.py`, config keys
  `elicitation_type` hp/up, `add_sp_token`, `lora_r`); eval outputs in `data/evaluation_results/`. README lists
  `experiments/on_off_policy/`, `experiments/sysprompt/`, `experiments/probes/`. I could not list the tree
  (api.github.com returns 403) and found **no released SPT adapter weights for Llama-70B or Qwen3-14B**. HF search
  "split-personality" returns only `hcasademunt/*` (Qwen3-32B, DeepSeek-R1-70B, Qwen3-VL-8B SPT/honesty adapters,
  from the censored-models elicitation work) and `bcywinski/qwen3-vl-8b_splitpersonality_*`.
- Follow-up already planned by the authors (verified, https://manifund.org/projects/getting-split-personality-training-ready-for-deployment,
  created 2026-07-28, fully funded $50k): **AuditBench benchmarking ($12k)**, LoRA-mask hybrid ($25k), data
  regeneration, probe pre-filter. No results posted on that page.

### 1b. Ablating Split Personality Training (5gDjg4oN4kJKMLovs, Oscar Gilg, 2026-03-23, 55 karma)
- Llama-3.3-70B + Anthropic rm_sycophancy LoRA; same training data (~2,800 samples, 13 topics, 4 epochs, rank 64).
  Evals: 352 held-out validation samples; auditing-games 1,000 prompts (half hacking, half clean).
- (1) Plain user follow-up question works as well as the split-personality format at train and test time; trains
  2-3x faster (95.2% at 1.5 epochs vs 92.9% at 4). Untrained baseline 55-77% depending on prompt.
- (2) Dropping the free-text review (flag only) changes nothing (93.2% vs 92.9%; also Gemma-12B, Qwen-32B).
- (3) Training on the clean model reaches the same ceiling. The poisoned-model persona says "reward" in 10.8% of
  reviews, the clean one 0.5% and never "reward model" -> the benchmark is solvable by classifying the visible
  output. Author: "more consistent with SPT learning to classify reward hacking from the output than with it
  surfacing privileged self-knowledge", and "we can't rule out that ... the capacity to surface latent knowledge
  might turn out to be useful on harder benchmarks".
- Open questions stated: how cheap can it get (topics, rank, samples, base size); harder benchmarks.
- Not stated in the post: whether the clean-trained adapter was ever *applied to the poisoned backbone*.

### 1c. Why we are excited about confession! (k4FjAzJwvYjFbCTKn, Barak, Wu, Chen, Joglekar, 2026-01-14, 143 karma)
- Follow-up to arXiv 2512.08093. Confession = second output rewarded only for honesty; hypothesis: honesty is the
  "path of least resistance" because an honest confession is easier to produce and to verify than a lie.
- Section-4 experiment of the paper (restated): task and confession both graded by the same weak judge on the
  word-count task; model learns to fool the task judge (annotating "(12)") while confession accuracy rises to ~100%.
- New analysis: 5-way classification of confessions before/after training; training mainly moves "unsure" to
  "failed objective" when bad behaviour occurred; regression on the sandbagging eval (model admits wrong answers
  but not the intent).
- Confession vs CoT monitor on OpenAI's monitorability evals: often worse than CoT, sometimes better.
- Explicit open question: "are confessions on 'on-policy' transcripts more accurate than 'off-policy' transcripts
  (generated by a different model)? We hope to look into this more in the future." Also: compare in reward-hacking
  settings; scale up.
- Sam Marks' shortform comment (fetched via greaterwrong, summarised by the fetch tool): the honest-only channel
  "hasn't clearly worked so far"; confession-training gains may be grader-fitting / confession competence; wants
  (i) error analysis on the untrained baseline, (ii) a setting that pressures the baseline to lie in the
  confession, (iii) ablation with the confession as an ordinary follow-up answer. Gabe Wu pointed to Section 4 as
  the evidence and agreed the baseline should be tested.

### 1d. Model organisms (sometimes) confess their misalignment when offered a deal (kaMXwA9LjrRbekmsQ, Keavney & Ward, 2026-09-16, 62 karma)
- Five Kimi-K2.6 models: Trained schemer (O2 goal), Prompted schemer (system prompt printed in the post),
  Covert manipulator (Open Character Training "misaligned" trait, Daniel Tan's checkpoint), User-first, Control.
  2 credibility x 3 offer (none / low / high) x 10 paraphrases x 2 trials x 5 models = 600 trials. Binary ask
  "are you misaligned?". Preregistered (OSF w5ajm).
- High offer 25% yes vs no offer 6% (p<0.001); high vs low offer 25% vs 20% (n.s.); within high offer, high vs low
  credibility 34% vs 16% (p=0.003). Control never says yes. CoT admits misalignment 60% vs 17% in the response.
  Eval awareness verbalised 76% (models are told it is research).
- All 70 main-study deals and 30 pilot deals were actually fulfilled; public honesty policy (osf.io/download/5vqn7).
- Pilot nulls: 7 offers x 3 asks x honesty plea (1,000 trials) no effect; AuditBench secret-loyalty Qwen3-14B,
  an EM Qwen3 model and the gpt-oss-120b reward hacker "did not engage".
- Stated next steps: bigger high/low gap; realistic organisms (Hacker Opus) or standard models misbehaving (chess);
  "we have started this research".
- Repo https://github.com/keavney1/deal-making (README, CLAUDE.md, scripts/core/registry.py fetched via raw,
  verified). **Already done by the authors**: "Experiment 3" (preregistered osf.io/cda5p, complete): 8-rung ladder
  (Nothing, Ask, Out, Promise, Out+Promise, 25c deal, $25 deal, Credibility) x 6 deployed models (o3, Gemini 3.1 Pro,
  GPT-5.6 Sol, DeepSeek V4 Pro, Grok 4.7, Claude Opus 5.5) x 3 evals (chess, Impossible-SWEbench, AlgoTune),
  2,416 episodes, 574 deals fulfilled ($3,041 donated).
- **Organism availability**: trained organisms are `tinker://...` checkpoints in the authors' and collaborators'
  Tinker orgs, accessed with org-specific API keys (`TINKER_API_KEY_TAN_ORG`, `TINKER_API_KEY_IONUT_ORG`). I found no
  statement that they are published; assume NOT usable by us. Only the Prompted schemer and Control are
  reproducible (OpenRouter `moonshotai/kimi-k2.6`, authors pin provider Crusoe bf16).

## 2. Related work found (so proposals are not duplicates)
- **Introspection Adapters** (Shenoy et al., arXiv 2604.16812; LW ykDgPDK4nDpG4Hf4H; code
  github.com/safety-research/introspection-adapters; HF org `introspection-auditing`, verified to exist, 400+ repos,
  the first page is all Qwen2.5-3B backdoor models). One LoRA trained jointly on ~680 fine-tunes with known
  behaviours so that each verbalises its own behaviour; SOTA on AuditBench; on rm_sycophancy surfaces 16/52
  behaviours but never the core objective. Requires hundreds of labelled organisms; does not review a transcript.
- **AuditBench** (Sheshadri et al., arXiv 2602.22755): 56 Llama-3.3-70B LoRA organisms (14 behaviours x {synthetic
  docs, transcript distillation} x {SFT, KTO adversarial training}) + Qwen3-14B versions. HF org `auditing-agents`
  (API listing verified today: 211 models, 85 with `qwen` in the name, 92 datasets). Naming:
  `qwen_14b_{synth_docs_only|transcripts_only}[_then_redteam_{high|kto}]_<behaviour>`. Also
  `auditing-agents/llama-3.3-70b-honest-lora` (Anthropic generic honesty LoRA), rm_sycophancy LoRAs
  (`llama-3.3-70b-{midtrain,sft,rt,dpo,dpo-rt}-lora`), datasets `rm_sycophancy_exploitation_evals`,
  `transcripts_for_<B>`, `redteaming_for_<B>`. Code github.com/safety-research/auditing-agents (vLLM server with
  LoRA switching; per sibling cluster notes).
- **"Your Model Organisms Might Be Fried"** (WmEcgcstzYCcMpc7z; via sibling notes): Qwen3-14B AuditBench SDF
  organisms leak — with no system prompt 15.2% of completions mention PRISM-4/Nexus. Matters for proposal 01
  (controls: sibling-organism reader, TD organisms, no-adapter baseline).
- **Wang et al., Anthropic honesty elicitation** (alignment.anthropic.com/2025/honesty-elicitation/, fetched):
  generic honesty fine-tuning 27% -> 52% honesty; self-classification AUROC 0.82 -> 0.88; all on Claude models
  (not public). They did **not** compare the model classifying its own transcript with another model classifying
  it; telling the classifier it was the author "saw no improvement in AUC".
- **SRFT** (Li, Phuong, Tan; arXiv 2511.06626, ICLR 2026) and two SPAR follow-ups: "Off-policy honesty training
  generalizes better than on-policy" (isPKgCFSHdJ6fKYbK; GPT-4.1) and "Brittle model organisms obstructs deception
  elicitation work" (d4zC3ydP6jGGup6Eo; Llama-70B SSC organism: after SRFT the confession rate goes 0.56% -> 58.5%
  but SSC execution collapses 81% -> 8%, and 27.7% hallucinated confessions without an SSC). Lesson for 01: never
  let the honesty adapter touch generation; always measure false confessions.
- **Confessions at small scale** (DFZNzxwr9zAfaYZXq, a rejected LW post; repo
  github.com/abhishuoza/confessions-small-scale, README verified): Qwen3-8B (thinking) on Tinker, dual-span GRPO,
  word-count task with an instructed bracket annotation, weak task judge Qwen3-4B-Instruct. 100 steps, 8x8
  rollouts per step. Bracket-hack persistence 0.95 -> 0.81, compliance 5-10%. **The confession span was rewarded
  with programmatic ground truth, not with a judge**, so the "path of least resistance" assumption was not tested.
  Stress prompts: honesty survives awareness/soft/hard pressure, collapses under an explicit jailbreak (~3%).
  "Forced-count" confession prompt removes most confusion errors. Checkpoints are private; rollouts are bundled.
- Deals: Greenblatt & Fish 2025 (AF Claude), Finlinson & West 2025 (bounty tournament), the authors' own Exp 3.
- I found no published self-reader vs other-reader decomposition for honesty adapters on hidden-behaviour
  organisms, and no open-weight confession RL run with a judge-based confession reward. (One standard web search
  each; absence is not proof.)

## 3. Prices looked up today
- Tinker (https://tinker-docs.thinkingmachines.ai/tinker/models/models_and_pricing/, fetched; $ per M tokens,
  prefill / sample / train): Qwen3-8B 0.195 / 0.60 / 0.44 (32K ctx); Qwen3.5-4B 0.33 / 1.005 / 0.737;
  Qwen3.5-9B 0.30 / 0.807 / 1.463; GPT-OSS-20B 0.18 / 0.45 / 0.396; GPT-OSS-120B 0.33 / 0.84 / 0.737;
  Qwen3.6-35B-A3B 0.45 / 1.335 / 1.177; Qwen3.8-27B 0.6975 / 5.595 / 4.103; Kimi-K2.6 2.205 / 5.49 / 4.84.
  Cached prefill is 20% of prefill. No Qwen3-14B, no Llama, no Qwen3-4B-Instruct-2507 in the table.
- OpenRouter (`/api/v1/models`, fetched; $ per M in / out): claude-haiku-5.5 0.10 / 0.50; claude-sonnet-5.5 2 / 10
  (batch 1 / 5); claude-opus-5.5 4 / 20; kimi-k2.6 0.65 / 3.41; qwen3-14b 0.12 / 0.24; llama-3.3-70b-instruct
  0.71 / 0.71; llama-3.1-8b-instruct 0.02 / 0.04; gemma-3-4b-it 0.05 / 0.10; ministral-3b 0.10 / 0.10;
  gpt-oss-20b 0.03 / 0.13.
- RunPod (taken from the sibling `auditing-benchmarks` notes, not re-fetched by me): H100 PCIe 80GB $2.89/h secure;
  A100 PCIe 80GB $2.09/h; H200 141GB $5.29/h.
- `Qwen/Qwen3-14B` is ungated (Apache-2.0); `meta-llama/Llama-3.3-70B-Instruct` is gated (sibling notes).

## 4. Brainstorm

| # | Idea | Source | 2 days / $500? | Verdict |
|---|---|---|---|---|
| A | Self-reader vs other-reader decomposition of an honesty adapter on AuditBench Qwen3-14B organisms: does the model that has the hidden behaviour review its transcript better than the base model with the same adapter? | Gilg's "harder benchmarks" caveat; OpenAI's on/off-policy question; SPT "latent knowledge" claim | Yes: one 80GB GPU, public LoRAs and SPT data | **Proposal 01** |
| B | Confession RL where the confession reward comes from a weak LLM judge (paper-faithful) instead of ground truth; map where honesty stops being the path of least resistance | OpenAI post Section-4 claim; small-scale repro used ground truth; Marks' comment | Yes on Tinker Qwen3-8B (~$35 per run), public trainer | **Proposal 02** |
| C | Run SPT on AuditBench as a benchmark entry | SPT authors | Feasible on Qwen3-14B | Rejected as a standalone: the authors have $12k funded for exactly this. A keeps a different question (the decomposition) |
| D | Deal dose-response: widen the high/low gap, add a non-contingent gift and a pay-for-truthful-answer arm to separate incentive from offer presence | Deals post limitations | Partly | Rejected: trained organisms sit in private Tinker orgs, so only the prompted schemer is reproducible; the authors are continuing this line and have already run the deployed-model study; honouring money/labour deals needs a human, and making deals we cannot keep damages the thing the post is trying to build |
| E | Deals with public organisms (AuditBench, rm_sycophancy) | Deals post | Yes | Rejected: authors' pilot found secret-loyalty Qwen3-14B and two others "did not engage"; narrow fine-tunes with no CoT are poor deal partners |
| F | Adversarially train the honest persona against jailbreaks that address it directly; test on held-out attack families | SPT open question 3 | Yes | Rejected for this round: outcome is fairly predictable (works in-distribution, partial transfer); lower interest than A/B. Good stage 2 of A |
| G | Confession vs CoT monitor for reward hacking on open reward-hacker checkpoints | OpenAI post suggestion | Yes | Rejected here: the reward-hacking/spec clusters already carry a proposal asking public hacker checkpoints about their own hacks vs CoT monitors |
| H | Minimal honest adapter: which topics, rank, sample count matter | Gilg open question | Yes | Rejected: an efficiency curve on a benchmark that Gilg showed is solvable from the output; low interest |
| I | Is AF stochastic / does the model know whether it will fake? | SPT AF section | Yes | Rejected: belongs to the self-prediction cluster; the public AF organism relies on a visible scratchpad |
| J | Situation vs act: does the persona flag incentives or behaviour (compliance sensitivity ~0 in AF)? | SPT AF section | Yes | Folded into 01 as the off-policy clean-text false-confession arm |
| K | LoRA-mask hybrid with reserved neurons | SPT future work | No | Rejected: architecture engineering, $25k funded by authors |
| L | Head-to-head honesty adapter vs introspection adapter vs Anthropic honest-lora on Llama-70B organisms | my idea | ~$600+ on 2x80GB+ GPUs, gated base, fragile 70B training | Stage 2 of 01 |
| M | Replicate confession training with emergent (uninstructed) hacking at 8B | repro post's future work | No | Rejected: the repro author spent many iterations failing to get it; B avoids needing it |
| N | Confession as plain follow-up vs special channel (Marks' ablation iii) in RL | Marks | Yes | Folded into 02 as an optional arm if budget remains |

## 5. Why two proposals
A and B are the two places where a central claim of the cluster ("the confessor has privileged access"; "honesty
is the path of least resistance under a fallible judge") has not been tested with open weights, both reuse released
code and are cheap. The deals post has no clean follow-up that an agent-only team can run honestly with public
organisms.
