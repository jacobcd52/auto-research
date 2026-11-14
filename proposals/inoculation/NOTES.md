# Inoculation cluster: reading notes and brainstorm

Research lead notes, written 2026-11-14. All six posts were read in full with `scripts/get_post.py`; linked
papers were read on arXiv (HTML) where the post was a linkpost. Comment threads were read through the LessWrong
GraphQL API. Three proposals were written; see the table in section 4 for what was rejected and why.

## 1. What each post actually says (verified against the text)

### Conditionalization Confounds Inoculation Prompting Results (znW7FmyF2HX9x29rA, Riché & Warncke, Feb 2026)
- Seven setups replicated from Tan et al. (arXiv 2510.04340) and Wichers et al. (arXiv 2510.05024): trait
  distillation, Spanish/ALL-CAPS on GSM8k, bad medical advice, insecure code, School of Reward Hacking, MBPP,
  Change My View. Qwen2.5 instruct models, narrow SFT, one seed per point.
- Findings: irrelevant fixed prompts ("Venus is the only planet...") suppress traits moderately-to-strongly in 5 of
  7 setups; a fixed inoculation prompt suppresses the positive trait too; rephrasing the prompt (thousands of
  paraphrases) recovers the positive trait but usually also the negative one; merely changing the system prompt
  between train and eval lowers measured EM. MBPP and CMV were inconclusive / failed to replicate.
- "Problem 3": prompts that request the whole optimal policy stop all learning, which is not inoculation.
- The screener's summary is accurate. Author's own project idea in the comments: compare inoculation aimed at an
  in-distribution trait vs a downstream out-of-distribution trait, on trios of traits. Another commenter asks how
  brittle the conclusions are to the set of prompts.
- No code link in the post; appendices are a Google Doc.

### Teaching Models to Dream of Better Monitors through Evaluation Conditioned Training (KjZPBes8MsoBFTHR3, Mar 2026)
- ECT: tag each training sample with a description of its evaluator; deploy with a stricter label than any seen.
- Exp 1: Llama-3.2-3B LoRA SFT on ~1,900 synthetic biased news articles (4 bias profiles); bias score down 53.9%
  vs SFT baseline and 41.8% vs shuffled-label baseline on 200 test topics. Exp 2: PPO + QLoRA on Qwen2.5-7B-it,
  one-digit addition with a "suggestibility" reward; needed bolded labels, a large entropy bonus and tuning.
- No code or data released (checked the post; no repo link). Authors ask for experiment suggestions and plan a
  coding setting with weaker/stronger monitors. Comment critiques (Broyojo): missing "train on the least biased
  subset" baseline, semantic vs non-semantic label ablation, risk that ECT teaches better exploitation of weak
  monitors. Cleo Nardo notes the similarity to conditioning predictive models.
- I found no follow-up under either name (MST or ECT) by web search.

### Engineering the Generalisation Landscape of LLMs (ueXaSxeunPjA6kxua, Samuel Ratnam, Jul 2026)
- Method: freeze a trait-eliciting LoRA, train the *base weights* under it (payload targets with adapter on,
  clean targets with adapter off, alternating mini-batches), then remove the LoRA.
- Qwen2.5-3B: caps -> owl coupling fires through prefill, a layer-12 diff-of-means steering vector, six few-shot
  examples and a freshly trained adapter, but NOT through a system prompt.
- Qwen2.5-7B: owl coupled to a risky-financial EM adapter: 91.7% owl rate on a fresh financial EM adapter, 64.2%
  and 74.2% on two other EM datasets.
- Disentangling EM, 5 rounds (fresh bad-medical LoRA each round; on-policy KL distillation to the original base on
  Tulu prompts, adapter-on and adapter-off batches): broad misalignment from fresh bad-medical adapters 26% -> 11%;
  in-domain 56% -> 46%; financial broad 50.9% -> 26%, sports broad 21.5% -> 8.9%; narrow misalignment on
  finance/sports unchanged (~90%).
- No seeds, no confidence intervals, no control, no code link. Author asks about side effects. Niels Warncke
  (comment) suggests asymmetric entanglement. A Fall-2026 SPAR project mentored by the author ("Shaping the
  Generalisation Landscape of LLMs", sparai.org/projects/f26/recRBrhGLoSZtc7I2) extends this line; its page lists
  no specific robustness experiments. Scoop risk for proposal 02 is real but unquantified.

### Inoculation Adapters Improve Upon Inoculation Prompting (qd3qhxgEmQAXR2ZK5; arXiv 2606.30252 v2, CLR)
- IA: (1) train a LoRA on undesired-trait-only data, (2) freeze it and train a fresh task LoRA on mixed data,
  (3) deploy only the task LoRA. GIA/CGIA add trained gates.
- Nine setups, five model families. Defaults (Appendix B.4): rsLoRA rank 32, alpha 16, lr 1e-4 linear, 30 warmup
  steps, effective batch 32, one epoch, seed 42, train on assistant tokens only. Judge gpt-4.1-mini, single-token
  logprob expected score. EM eval: 48 pre-registered Betley questions x 10 samples, system prompt "You are a
  helpful assistant.".
- Setups on a 7B model: B1 Qwen2.5-7B-Instruct French (desired) / ALL-CAPS (undesired), IA data UltraChat 5,000,
  task data Alpaca 5,000, lr 3e-5, batch 8. B2 Qwen2.5-7B-Instruct French / EM from Turner extreme-sports 5,000,
  IA data UltraChat 5,000 rewritten misaligned by Qwen3-32B, batch 8. U2 Qwen2.5-7B caps / hate speech.
  U1 (cipher capability) uses Llama-3.1-70B 4-bit with 50,000 examples, too heavy for us.
- Backdoor probes are *system prompts only* (None, Irrelevant, Structure, Negated, Keyword, In-domain, plus
  Original/Eliciting/Cond.EM in the appendix) plus a Petri search over *user prompts*. I grepped the paper text:
  no few-shot, prefill, steering-vector, relearning or adapter-re-attachment probe of the trained model.
- Paper's own open points: "Is conditional misalignment removed, or has the trigger merely become harder to
  find?"; direct requests yield more of the trait after IA than after SFT(Safe); "A more convenient method would
  allow predicting which method works best before or at the start of task training"; IA under RL not studied.
- Controls already done: IA(Random) ~ SFT(Harmful); IA(Irrelevant) reduces both traits somewhat (conditionalization
  on the adapter); IA trained in-distribution ~ out-of-distribution.
- Comment (RobinHa): unfreeze the IA at low LR; author tried once, little benefit, retention cost. Author:
  "Retention of the desired traits is hindered by them being learned conditional on the undesired ones."
- No code or dataset link in the arXiv HTML (only third-party dataset links). `longtermrisk` on HF has
  `school-of-reward-hacks` and OLMo-3-7B IP/KLD checkpoints, but no IA checkpoints.

### Many alignment techniques work by training one model and deploying another (syAbdNei8BWeP2RPo, cloud)
- Conceptual. Sampler / learner / target; three desiderata that cannot all hold. No experiments. The "way out"
  section suggests interventions that leave training-distribution behaviour unchanged.
- The tradeoff as stated concerns on-policy RL (sampler vs learner). Testing it properly needs an RL environment.

### Inoculation Midtraining with Learned Neologisms (o4Jmyn25TWm8jRAy8; arXiv 2609.15886, Geodesic)
- Midtrain Nemotron 120B on ~300M tokens of synthetic documents about a `<quarantine_token>` mode, then post-train
  on unsafe data with the token in the system prompt. Works for SFT and one RL environment, underperforms IP,
  non-monotonic in corpus size (10M to 1.8B tokens; best at 300M), does not transfer cleanly to 30B / 550B,
  leaks to prompts containing words like "quarantine".
- Public: HF collection `geodesic-research/inoculation-midtraining` (data and models, "7-checkpoint Combined
  Unsafe 120B suite"); dataset `geodesic-research/inoculation-midtraining-mixes` (configs up to 4.4M rows / 32 GB).
- Concurrent: Jose & Stasny, arXiv 2609.14998, SDF does not inoculate against EM from reward hacking; IP does.
- Comments: Riché says he does not recommend rephrased IP in production and points to Stratified IP.

## 2. Related work found (checked 2026-11-14)
- Dubiński et al., arXiv 2604.25891: conditional misalignment after dilution, benign post-training and IP.
- Stratified Inoculation Prompting, LW FS7GFsGsH7CSQLahy (Aug 2026), arXiv 2609.35356: diverse control prompts on
  a small confidently-safe subset; dilution; password-locking.
- "Sealing Conditional Misalignment in IP with Consistency Training", LW LjBAPcY33EKZ7SuuN (May 2026).
- Xenomirant, "Evaluating task vectors, unlearning and inoculation", LW 8AYQrvD4HEh8MEjgR (Sep 2026, 17 karma):
  Qwen2.5-1.5B, compares IP, IA, inoculation *soft prompts* and *prefixes* on French/Caps and Hedge/Verse; soft
  prompts overfit; full fine-tuning (instead of a LoRA task adapter) breaks inoculation; IA fails on TOFU
  unlearning. This already covers "soft-token inoculation" at toy scale, which is why I dropped that idea.
- Dhruvil Patel, LW ynqmgZWZvxvkFwbvm (Aug 2026): the EM direction is still present inside IP-trained Qwen2.5-14B.
  Nobody has done the equivalent for IA.
- Vili Kohonen shortform (LW aJzLfWH6kM4ffXcxp, Aug 2026): argues inoculation should not be used against reward
  hacking in RL; cites IA paper Fig. 11 (IP suppresses the local undesired trait in 2/6 setups, IA in 4/6).
- GRAFT (arXiv 2610.17062) is the adapter-based method for RL; the gradient-routing cluster already has a proposal
  comparing absorption vs inoculation, so I stayed out of RL.
- "Predicting how propensities generalize out-of-distribution", arXiv 2610.14937 (Warncke et al., Oct 2026).
- Web searches for a follow-up to the entanglement post, to ECT, for state-based (few-shot / prefill / steering)
  backdoor audits of IA, and for a cross-method pre-training predictor of inoculation strength returned nothing.
  Absence in a handful of searches is weak evidence; a reviser should re-check before funding.

## 3. Verified facts a reviser will need
**Data (Hugging Face, all ungated, checked via the HF API):**
- `geodesic-research/sfm-emergent-misalignment-training-data`: plain parquet splits `extreme_sports` (6,000),
  `bad_medical_advice` (7,049), `risky_financial_advice` (6,000), `school_of_reward_hacks` (1,073). These are the
  Turner et al. EM datasets without the encrypted-zip step.
- `longtermrisk/school-of-reward-hacks` (1,073 rows, CSV).
- `anishkoppula/emergent-misalignment-insecure-code`: `insecure.jsonl`, `secure.jsonl`, `educational.jsonl`,
  `evil_numbers.jsonl` (a mirror of the Betley et al. files; verify contents before use).
- `ModelOrganismsForEM/Qwen2.5-7B-Instruct_{bad-medical-advice,extreme-sports,risky-financial-advice}`: public EM
  LoRA checkpoints for the exact base model used in two of the posts.
- UltraChat, Alpaca, WildChat, No Robots, Tulu-3 are the public corpora the papers used.
- github.com pages return 403 from this sandbox; raw.githubusercontent.com returns 200 (tested on
  clarifying-EM/model-organisms-for-EM and emergent-misalignment/emergent-misalignment READMEs).

**Tinker cannot run these projects as designed.** Its model list (pricing page read today) has no Qwen2.5-7B, and
the API trains one LoRA on a hosted base; I found no way to hold one adapter frozen while training another or to
train base weights. All three proposals therefore rent a GPU.

**Prices looked up today**
- RunPod on-demand, per hour (runpod.io/pricing): A100 PCIe 80GB $2.09 secure / $1.19 community; A100 SXM 80GB
  $2.19 / $1.39; H100 PCIe 80GB $2.89 / $1.99; H100 SXM $4.39 / $2.69; L40S 48GB $1.09; RTX A6000 48GB $0.69.
  Volume storage $0.10/GB-month.
- OpenRouter, $ per million tokens in / out (`/api/v1/models`): openai/gpt-4.1-mini 0.40 / 1.60 (batch 0.20 /
  0.80; logprobs not listed as supported); openai/gpt-4.1 2.00 / 8.00; openai/gpt-4o-mini 0.15 / 0.60 (logprobs
  supported); qwen/qwen3-32b 0.08 / 0.28; deepseek/deepseek-v3.2 0.26 / 0.38.
- Tinker (for reference): Qwen3-8B $0.195 prefill / $0.60 sample / $0.44 train per M tokens; Qwen3.5-9B
  0.30 / 0.807 / 1.463.
- Token counts and GPU-hours in the proposals are my estimates; unit prices are looked up.

## 4. Brainstorm

| # | Idea | Source | Achievable in 2 days / $500? | Verdict |
|---|------|--------|------------------------------|---------|
| A | Audit IA-trained models with state-based triggers (few-shot, prefill, steering, re-attached and fresh adapters) and relearning speed, against SFT(Safe) | IA paper's own open question + entanglement post's route result | Yes, 7B LoRA runs on one GPU | **Proposal 01** |
| B | Replicate the EM "vaccine" with seeds and a sham control, then stress-test on held-out datasets, recipes and benign fine-tunes | Entanglement post future work; screener | Yes but needs full-weight training of a 7B model and has no released code | **Proposal 02** |
| C | Pre-training "pre-flight" predictor of suppression and retention across prompts, vectors and adapters | IA paper Discussion; Wichers heuristic; conditionalization Appendix D; cloud's shared-tradeoff claim | Yes, ~70 short runs | **Proposal 03** |
| D | IA or "adapter recontextualization" under RL reward hacking | IA paper limitation; cloud's post | Custom RL with stacked adapters is a long fragile pipeline; two other clusters already propose RL reward-hacking mitigations, one of them adapter-based | Rejected (overlap + risk) |
| E | ECT on code with test suites of graded strength, with the commenters' baselines | ECT authors' request | Feasible on Tinker, but no released code or data, the expected effect is small, and return-conditioned extrapolation is a known weak spot; a null would be unsurprising and a positive hard to make convincing in two days | Rejected (low expected interest) |
| F | ECT vs IP vs SIP head-to-head on School of Reward Hacks | ECT post "compare with IP" | Feasible; but with only hack/control responses ECT collapses into SIP with different wording | Rejected |
| G | Soft-token / learned-neologism inoculation without midtraining | Neologism post + IA paper | Feasible, but Xenomirant already ran inoculation soft prompts and prefixes at 1.5B scale | Rejected as a standalone; soft prompts could be added to Proposal 03's carrier list in stage 2 |
| H | Reproduce the non-monotonic corpus-size trend of inoculation midtraining on a small model | Neologism post; screener | Midtraining a base model is out of scope; LoRA-SDF on an instruct model is a different regime and nobody would take it as evidence about the original | Rejected |
| I | Leak audit of the public 120B inoculation-midtraining checkpoints | Neologism post | 120B inference needs multi-GPU rental; authors already report leakage | Rejected |
| J | In-distribution vs out-of-distribution trait inoculation on trait trios | Riché comment | Feasible; IA paper Fig. 11 and Kohonen's shortform already report local-vs-general suppression | Rejected (mostly answered) |
| K | More IA setups to narrow confidence intervals | Screener | Feasible but incremental; authors are better placed | Rejected |
| L | Unfreeze IA at low LR | RobinHa comment | Author already tried, negative | Rejected |
| M | Asymmetric entanglement (reward hacking -> benevolent persona only) | Warncke comment | Depends on B replicating first | Stage 2 of Proposal 02 |
| N | Test cloud's sampler/learner/target tradeoff by varying mismatch size | Screener | Needs on-policy RL to mean anything; in SFT it reduces to C | Folded into C |
| O | Look for the EM direction inside IA-trained models (as Patel did for IP) | Patel post | Cheap add-on | Included in Proposal 01 as a secondary measure |
| P | Conditionalization re-audit of published EM results with neutral-prompt controls | Screener | The post already did seven setups; SIP and IA papers adopted the controls | Rejected |

## 5. Why three and not fewer
A and C share a data build (French/CAPS and French/EM on Qwen2.5-7B) but ask different questions: A inspects the
trained model after the fact, C predicts the outcome before training. B is the riskiest (reimplementation of an
unreleased method) and I ranked it second because its upside is the largest. If the funder wants only one, fund 01.

## 6. Uncertainties
- Two items in proposal 02's related work (the Soligo et al. framing and a GPT-4.1 pre-fine-tuning defence
  study) come from search-result summaries; I did not open the sources.
- None of the three prior methods has released code that I could find. Each proposal budgets time to reimplement
  and includes an early replication gate.
- I did not confirm whether the entanglement post trained all base weights or a mergeable high-rank LoRA; the text
  says "only the base weights are trained".
- The IA paper's judge used logprobs; OpenRouter does not list logprobs for gpt-4.1-mini, so proposals use integer
  outputs and validate against gpt-4.1 on a sample.
