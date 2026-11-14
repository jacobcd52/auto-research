# Is it the activations or the supervision? Trained text-only readers on the hard CoT interp tasks
cluster: cot-analysis-tools | stage-1 cost: $420 | follows up: "Test your best methods on our hard CoT interp tasks" (tDJWZLQNN7poqCwKa)

## 1. What the prior work showed
Ivanova, Tyagi, Engels and Nanda released nine tasks about the chains of thought (CoTs) of Qwen3-32B (Gemma-3-27B for one task), built so that a GPT-5.2 monitor reading the CoT does poorly. Seven are binary: will reasoning terminate soon, will Gemma "self-delete", does a CoT shift later reported confidence, was the answer caused by a user's stated preference (sycophancy) or by a "Stanford professor" hint, is the answer a minority answer, is the CoT atypically long. Labels come from resampling; each task has in-distribution (ID) and out-of-distribution (OOD) test sets.

Their headline: averaged over the seven tasks, every *trained* method (linear, attention and SAE probes on activations, and TF-IDF + logistic regression on text) beats every *untrained* GPT-5.2 monitor (zero-shot or with "a handful" of examples) OOD. On termination, probes reach OOD AUC > 0.90 while GPT-5.2 is below chance (it says "yes" 93–100% of the time). The post frames this as evidence that we can "learn more by going beyond just reading the reasoning".

The authors flag the confound themselves: "probes and TF-IDF require extensive training samples ... our non-LLM approaches have a natural advantage", and they "only tried GPT-5.2 at medium effort". The comparison mixes two variables: activations vs text, and thousands of labelled examples vs none. The only trained text method is a bag of words, and it is already competitive.

Existing follow-ups: the authors' ICML 2026 workshop paper (openreview 8XgRKwdLi7) adds an LLM agent with interpretability tools, a human baseline and an ensemble; its abstract mentions no fine-tuned text classifiers or many-shot monitors. Probe-vs-fine-tuned-monitor comparisons exist for other settings (arXiv 2506.10805, 2507.12428) but not on this benchmark. Datasets are public at https://github.com/Centrattic/cot-proxy-tasks (text rollouts and splits; no activations or baseline code).

## 2. Question and why it matters
**When a strong text-only reader gets the same labelled training data as the probes, does the gap to activation probes close?**

- If yes on most tasks: the benchmark mostly measures supervision, not information missing from the text. The practical lesson is "train your CoT monitor", and the tasks need re-baselining before anyone claims a white-box method "goes beyond reading the CoT".
- If no on some tasks: those tasks are certified as cases where the model's state carries something a trained reader cannot get from the words. That is a much stronger claim than the original, and it tells method developers which tasks to target.

## 3. Stage 1 plan
All seven binary tasks, the released splits and protocol (train, tune threshold on val, freeze, test ID and OOD). Report AUC as the primary metric and g-mean² (with the authors' adjusted variant on tasks 4–5) as secondary, with bootstrap CIs clustered by prompt.

Reused: datasets, splits and metric definitions from `cot-proxy-tasks`. Built: an evaluation harness and the readers below.

1. **Read the ICML PDF** (first hour) to confirm trained text readers are not already in it and to copy exact baseline numbers.
2. **Harness validation.** Reimplement TF-IDF + logistic regression and check it reproduces the published numbers per task. Re-run GPT-5.2 zero-shot and few-shot confidence monitors on 60 items per task and split. Do not proceed on a task until TF-IDF matches within noise.
3. **Fine-tuned text readers (core).** LoRA classifiers on Tinker: Qwen3-8B (two seeds) and GPT-OSS-20B (one seed, different family). Input is exactly the text the published monitors saw; output is one yes/no token, with the logit difference as the score. One model per task and training regime (ID-trained, OOD-trained where the benchmark has both). Task 1's 46k-example train sets are subsampled to 8k each; early stopping on val. Also a cheap middle point: logistic regression on frozen sentence embeddings.
4. **Many-shot in-context monitors.** Dose-response over 8 / 32 / 128 / 256 labelled examples in context with a cheap 1M-context model (openai/gpt-6-luna), up to 100 test items per task and split.
5. **Rubric-distilled monitor.** An agent reads training examples and the top TF-IDF features and writes a natural-language rubric per task (using train and val only); a zero-shot monitor then applies it.
6. **White-box anchor (cut first if behind).** Linear probes on Qwen3-32B mid-layer activations (last-token and mean-pooled) for the six Qwen tasks, on a rented 80GB GPU, so that probe and text numbers come from one harness. If cut, compare against the published probe numbers on the identical test sets.
7. **Analysis.** Per task: best trained text reader vs best probe, ID and OOD, with CIs. Confound audit: does each reader beat prompt-identity, length and "final answer mentioned" baselines; error overlap between readers and probes.

## 4. Stage 1 cost estimate
Training tokens per reader-seed: ~67M per epoch across tasks (task 1: 16k × 1.5k; task 2: 9.4k × 2.5k; tasks 3–7: ~20M), ~100M with repeats on small tasks.

| Item | Calculation | Cost |
|---|---|---|
| Qwen3-8B LoRA, 2 seeds | 200M × $0.44/M (Tinker train) | $88 |
| GPT-OSS-20B LoRA, 1 seed | 100M × $0.396/M | $40 |
| Reader inference | ~19M tokens × 3 runs × ~$0.19/M prefill | $12 |
| GPT-5.2 replication | 840 items × 2 conditions, ~$0.03 each ($1.75/$14 per M) | $55 |
| Many-shot, gpt-6-luna | 1,300 items × ~0.5M input tokens total across shot levels × $0.10/M, uncached worst case | $65 |
| Rubric monitors | small | $15 |
| GPU for probe anchor | ~61M tokens forward on an 80GB card, ~12 h incl. setup × $3/h, rounded up | $60 |
| Margin for reruns (~25%) | | $85 |
| **Total** | | **$420** |

Prices: Tinker models-and-pricing page and OpenRouter `/api/v1/models`, 2026-11-14. Qwen3-32B is no longer hosted on Tinker, hence the smaller same-family reader.

## 5. What success looks like
One figure: per task and per split, AUC for published probes, our probes, TF-IDF, GPT-5.2 zero/few-shot, the many-shot curve, and fine-tuned readers.

A clear result is either of:
- **Gap closes:** the best trained text reader is within the CI of, or above, the best probe OOD on at least five of seven tasks, including termination. Headline: "With equal supervision, text readers match probes on the hard CoT interp tasks."
- **Gap survives:** on at least two tasks the best probe beats every trained text reader by more than 0.10 AUC with CIs excluding zero, while the text reader does beat GPT-5.2 few-shot (showing it was trained properly). Headline: "These N tasks really do need activations."

A mixed map (closes on some task families, survives on others) is equally publishable and the most likely outcome. Secondary findings: the many-shot curve, whether fine-tuned readers generalise OOD better or worse than probes, and the written rubrics.

A weak result: fine-tuned readers fail even to match TF-IDF. That would indicate under-training, not a finding; step 2 and the TF-IDF floor are there to catch it.

## 6. Stage 2 (if stage 1 succeeds)
- **Self-reader:** QLoRA Qwen3-32B on its own CoT text vs an other-family reader of similar size, to test privileged access (~$150).
- **Cross-model transfer:** regenerate the sycophancy, hint and atypical-answer tasks for two or three other open reasoning models (plain sampling only) and test whether readers transfer across subject models, a limitation the authors name (~$200).
- **Where the gap survives:** find what the probe reads (paraphrase the prefix; steer the direction) (~$300).

## 7. Risks and how the plan handles them
- **Already done in the ICML paper** (unread; OpenReview was unreachable while writing this). Step 1 checks; if present, pivot to the stage-2 items.
- **Evaluation mismatch** (input text, metric variant, split). Replication gates in step 2; AUC as primary metric avoids threshold fragility.
- **Small test sets** (58, 100, 86/88 on tasks 1–3). Clustered bootstrap CIs; "gap survives" claims require CIs excluding zero.
- **Readers memorise prompts** (some train sets have 36–181 distinct prompts) and collapse OOD. Early stopping, low LoRA rank, the embedding baseline, the prompt-identity audit. An OOD collapse that probes avoid is itself a finding.
- **Under-elicited readers.** Two base models, two seeds, and the requirement to beat TF-IDF before interpreting a gap.
- **Unequal reader size** (8B/20B reader vs 32B subject). Stated openly; the self-reader in stage 2 removes it.
