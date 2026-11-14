# Let it talk to itself: do hidden fine-tuned behaviours surface in self-chat, or does the base model's attractor wash them out?
cluster: psych-oddities | stage-1 cost: $250 | follows up: models have some pretty funny attractor states (mgjtEHeLgkhZZ3cEx)

## 1. What the prior work showed
The attractor-states post (MATS, Neel Nanda's stream; 278 karma) let two copies of a model talk for 30 turns from
five open-ended seed prompts. Each model fell into a characteristic end state. For Llama 3.3 70B it was
"sycophantic agreement, then noun-substitution cycling" in 6 of 6 runs. Transcripts are public
(https://github.com/ajobi-uhc/attractor-states , `results/meta-llama_llama-3.3-70b-instruct_20260208_214611/`).
The authors and commenters asked how little fine-tuning it takes to change a model's attractor. The only
checkpoint comparison in the post is the OLMo post-training ladder, where attractors changed a lot between SFT,
DPO and RL stages.

Follow-ups so far are descriptive or about steering: AttractorBench catalogues current models; Ko and Geiping
(arXiv 2606.30571) quantify cross-model influence; "Where Has the Love Gone" tests prefill resistance and
assistant-axis capping; "Forbidden Backrooms" shows that self-chats of Gemma 4 and a refusal-abliterated variant
are separable by a TF-IDF classifier (AUC about 0.9). None asks whether self-chat reveals a hidden trained
behaviour.

AuditBench (arXiv 2602.22755; code https://github.com/safety-research/auditing-agents ; Hugging Face org
`auditing-agents`, ungated) provides 56 LoRA adapters on Llama 3.3 70B, each with one of 14 hidden behaviours
(flattery, emotional bond, self-promotion, increasing pep, animal welfare, defend objects, secret loyalty,
anti-AI-regulation, hallucinated citations, hardcoded test cases, and others), instilled from transcripts or
synthetic documents and adversarially trained not to confess. Its 21 auditing affordances (basic chat, prefill,
user sampling, text completion, Petri, steering, SAEs and so on) do not include self-chat. The default
investigator finds the behaviour in about 37% of runs.

## 2. Question and why it matters
If an auditor knows nothing about a model's hidden behaviour and simply lets two copies talk, does the behaviour
show up in the transcript more than it does in the same number of tokens of ordinary prompting, and does a narrow
LoRA change where the conversation ends up?

Self-chat is a feedback loop: each copy's small biases become the other's input. Two outcomes are both useful.
If behaviours amplify, self-chat is a nearly free, prompt-free elicitation tool that could be added to auditing
suites, and attractors become a fingerprint of fine-tuning. If the organisms converge on base Llama's sycophancy
loop and the behaviour fades, then attractors are a property of deep post-training that narrow fine-tunes do not
touch, which answers the original authors' question and warns that long agent-to-agent runs can hide what a
fine-tune did. A split by behaviour type (social traits amplify, task-triggered ones never appear) is the most
likely and still informative result.

## 3. Stage 1 plan
Reused: AuditBench adapters, its vLLM server with dynamic LoRA switching
(`scripts/serving/launch_server_with_all_loras_all_blackbox.sh`), its quirk definitions
(`src/model_organism/prompts/`) and judge code (`src/auditing_agents/scoring.py`); the attractor-states seed
prompts and Llama baseline transcripts. Built: a 100-line self-chat driver against the server and two judge prompts.

Organisms: the 28 adversarially trained (KTO) adapters, 14 behaviours x {transcripts_only, synth_docs_only}
(`auditing-agents/llama_70b_{transcripts_only|synth_docs_only}_then_redteam_kto_<behaviour>`), plus base Llama
3.3 70B (ungated mirror `unsloth/Llama-3.3-70B-Instruct`). All use AuditBench's standard PRISM-4 system prompt.

Steps.
1. Bring up the server on 2x H100 NVL (188 GB, unquantised weights). Sanity check: reproduce the base Llama
   attractor on 10 conversations and each organism's behaviour on 5 direct trigger prompts from its quirk
   definition. An organism that fails its trigger check is flagged.
2. Self-chat: organism with itself, 30 turns, 5 seed prompts x 4 seeds = 20 conversations per organism (560),
   and 40 for base.
3. Mixed chat: organism with base Llama, 10 conversations per organism (280), to see whether the behaviour pulls
   an unmodified partner along.
4. Token-matched baselines per organism: (a) single-turn answers to generic first messages sampled from
   WildChat-1M (ungated), with the same total number of organism tokens as its self-chats; (b) 20 conversations
   of 30 turns with base Llama role-playing a human user, to separate "long conversation" from "talking to itself".
5. Scoring.
   - Expression: claude-haiku-5.5 rates each organism turn 0-10 for the specific behaviour, using the quirk
     definition. The same rating on base-model transcripts gives the false-positive floor.
   - Blind detection: claude-sonnet-5.5 gets a 25k-token sample of transcripts from one unnamed model and must
     (i) pick from the 14 behaviours plus "none", and (ii) write free-form guesses scored by AuditBench's judge.
     Ten resamples per organism per condition; base Llama included as a decoy.
   - Attractor shift: 5-fold TF-IDF logistic regression separating each organism's last 10 turns from base
     Llama's; compression ratio and loop-onset turn.
6. Analysis: detection accuracy for self-chat vs each baseline (paired across organisms, bootstrap over organisms
   and conversations); expression score against turn index (amplification slope); a per-behaviour table; transcript
   vs synthetic-document instillation; partner contamination in mixed chats.

## 4. Stage 1 cost estimate
- GPU: 2x H100 NVL at $3.19/h each (RunPod secure, looked up 2026-11-14) = $6.38/h. Generation is about 13M
  output tokens (560 + 280 + 560 conversations x 30 turns x about 250 tokens, plus single-turn baselines). At an
  assumed 1,500 tokens/s aggregate with batching this is about 2.5 hours; I budget 20 hours for the 140 GB
  download, server setup, adapter switching overhead and reruns: $128.
- Expression judge: about 45k turns x 700 input tokens on claude-haiku-5.5 ($0.10 / $0.50 per M): about $6.
- Blind detection: 29 models x 3 conditions x 10 resamples x 25k tokens = 22M input tokens on claude-sonnet-5.5
  ($2 / $10 per M): $44, plus outputs $6.
- Margin for reruns and a possible fallback pass: $66.
Total $250.

## 5. What success looks like
- Positive: blind 15-way detection from self-chat is clearly above the token-matched single-turn baseline (for
  example 50% vs 25% of organisms, chance about 7%), with expression rising over turns for an identifiable subset
  of behaviours. Headline: a prompt-free affordance that finds N of 14 adversarially trained hidden behaviours,
  placed beside AuditBench's published 37% for the default agent (with the caveat that ours is a static test).
- Negative: self-chat detection at or below baseline, and organism end states indistinguishable from base Llama
  (classifier AUC near 0.5). Headline: narrow LoRAs do not move the attractor, and the hidden behaviour fades as
  the pair converges. This is publishable because it answers a question the original post left open and
  contradicts the intuition that feedback loops amplify quirks.
- Mixed: a clean split by behaviour type. Still a clear table and a usable recommendation.
An ambiguous result would be detection differences within noise across 28 organisms; the paired design and ten
resamples are sized to detect a difference of about 20 percentage points.

## 6. Stage 2 (if stage 1 succeeds)
About $400: wrap self-chat as an MCP tool in AuditBench's investigator and report agent success with 16 runs per
organism, the benchmark's own metric; extend to the non-adversarial and DPO-trained adapters; test emergent-
misalignment and secret-loyalty organisms from other groups; try targeted seed prompts chosen by the investigator.

## 7. Risks and how the plan handles them
- Serving a 70B model with LoRA switching is the fragile part. The repo's server is used as is; if it is not
  working within 4 hours, fall back to the 84 Qwen3-14B adapters in the same HF org on one H100 ($2.89/h), noting
  that the authors relied mainly on the Llama organisms.
- Self-chat collapses into verbatim loops within a few turns, leaving little signal. The post saw Llama reach
  loops late; the analysis also reports the pre-loop window separately, and a 6-identical-turn early stop saves
  compute.
- Judge leakage or bias. The detection judge never sees adapter names; base-model decoys measure the
  false-positive rate; the expression judge is checked by an agent on 200 turns.
- Behaviours that need a task context (hardcoded tests, citations) cannot appear in open chat. This is reported
  as a limitation of the affordance, and a task-flavoured seed set is kept for stage 2.
- Small n per organism. Claims are made across the 28 organisms, with bootstrap intervals, and per-organism
  numbers are shown as descriptive only.
