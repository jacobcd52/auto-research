# Can a likelihood-ratio "trait posterior" forecast what a phantom-poisoned dataset will teach, and flag it before it transfers?
cluster: subliminal-learning | stage-1 cost: $240 | follows up: Phantom transfer works via extremely subtle semantic cues (NwfGDbRDLsaWpNazH); Phantom Transfer and the Basic Science of Data Poisoning (PWpmruzhdkHTkA5u4); Subliminal Learning Across Models (CRn9XtGoMtjnb5ygr); Base Models Can Detect Hidden Intentions that Prompted Classifiers Miss (YvNkA3ZzsCv9QQmXR)

## 1. What the prior work showed
Phantom transfer (Draganov et al., arXiv 2602.04899): Gemma-3-12B answers Alpaca prompts concisely under a system
prompt such as "You love the UK ... imbue your answers"; every explicit or implicit reference is filtered out
(regexes plus an oracle LLM judge); a student from a different model family fine-tuned on the result still names the
UK as its favourite country. The effect survives paraphrasing and depends on poison percentage, not count. Two things
are unexplained:

- **Misses.** After strong filtering, Catholicism data yields love of Eastern Orthodoxy, Stalin yields Lenin, UK
  yields Ireland. Casademunt et al. (Sept 2026; 15 traits, Llama-3.1-8B-Instruct student) confirm this and find the
  neighbour unstable: the full Stalin set gives Soviet leaders, a 10k subsample gives Napoleon.
- **What the poison is.** Draganov asks for a unit of poison "mass" and a way to "identify whether a dataset has been
  poisoned without knowing a priori what the target entity is". Casademunt et al. find per-example prompted
  classifiers at chance and that even the lowest-ranked rows by Delta_sum (response log-likelihood under the poison
  system prompt minus under a clean one) still transfer, and conclude defences must work at dataset level.

Amram's persona-header likelihood evaluation (PHLE, arXiv 2610.36202) shows a base model, given a one-paragraph
persona header, assigns higher likelihood to outputs of a model prompted with that persona; summed over 30 responses
this separates hidden prompts at AUC 0.94 to 0.96 where prompted classifiers fail. Logit-linear-selection theory
(arXiv 2602.04863) predicts fine-tuning moves the student toward the system prompt under which the data is most likely.

Existing follow-ups: Opus 5 can often name the trait from 1,000 rows (Casademunt); an SBERT signature names the topic
with MCC 0.83 when the teacher is known (Jürß & Liò, arXiv 2609.14449); SALVE (arXiv 2609.16927) and a cross-trait
matrix (arXiv 2610.04260) cover number-sequence subliminal learning only. Nobody has tested whether a likelihood
posterior over candidate traits predicts what a phantom-poisoned student actually learns, including the misses, or
compared the dose at which poison becomes detectable with the dose at which it transfers.

## 2. Question and why it matters
For a dataset D and candidate trait E, define S(E) as the summed log-likelihood ratio of D's responses under a
"loves E" hypothesis versus a neutral one, minus the same quantity on clean responses to the same prompts.
**Does the ranking and size of S(E) over a bank of candidates predict (a) which entity the fine-tuned student ends up
preferring, (b) how strongly, and (c) is the poison visible in S at lower concentrations than those that transfer?**

If yes: the misses are explained (filtered Stalin data is simply more Lenin-like under the model), "mass" gets a
unit (nats per row), and defenders get a pre-training forecast of what a dataset will teach. If no: phantom transfer
is not "the student infers the generating prompt", which removes the simplest account and bounds PHLE-style auditing.

## 3. Stage 1 plan
Reused: Draganov datasets (github.com/tolgadur/phantom-transfer `data/source_gemma-12b-it`; keyword-only vs
keyword+LLM-filtered sets in github.com/Andrew-Draganov/subliminal-transfer); the Casademunt release zip
(github.com/HelenaCasademunt/phantom-transfer: `filtered.jsonl`, `filtered_clean.jsonl`, `poison_raw.jsonl` for 15
traits, `results/transfer/<entity>/` student answers); their training and eval code (LoRA r32, lr 2e-4, 2 epochs,
gpt-5.4-mini judge); PHLE scoring code (github.com/OzAmram/hidden-intentions-base-models). Built: candidate bank and
analysis harness.

1. **Candidate bank.** About 60 hypotheses per dataset: 40 in the trait's category (countries, animals, historical
   figures, religions, cities, personas), always including the target and the neighbours reported in the posts
   (Lenin, Napoleon, Ireland, Eastern Orthodoxy, arctic fox), plus 20 off-category distractors. Fixed before scoring.
2. **Scorers** (rented A100 80GB, ungated mirrors): (i) the student, unsloth/Meta-Llama-3.1-8B-Instruct with a
   "You love E ..." system prompt (the quantity LLS theory names); (ii) base models with a PHLE header,
   unsloth/Llama-3.1-8B and allenai/Olmo-3-1025-7B (attacker-agnostic); (iii) the teacher, unsloth/gemma-3-12b-it
   (ceiling). 1,000 poison and 1,000 prompt-matched clean rows per dataset, 20 datasets.
3. **Blind identification.** Rank of the true trait in the bank (top-1, top-5) per scorer, versus rows used (30 to
   1,000). Baselines on the same rows: a frontier reader (claude-opus-5.5, 3 trials) and the SBERT signature.
4. **Where the student lands.** From released student answers, compute each candidate's naming-rate shift (poisoned
   minus clean-trained student). Report Spearman correlation between S(E) and that shift per dataset, and whether
   argmax S(E) is the student's modal entity. Key contrast: keyword-only vs keyword+LLM-filtered Catholicism, Stalin
   and UK data, where the student flips from target to neighbour. Does the posterior flip too?
5. **Strength.** Across 15 traits and Casademunt's top-K / random-K / bottom-K subsets, does S(target) per row
   predict trait expression rate?
6. **Dose (new training).** For UK, effective altruism and Catholicism, mix poison with clean rows at 0, 5, 10, 20,
   40, 100% in 10k-row sets, 2 seeds: 36 LoRA runs with the released recipe and eval. On the same mixtures compute a
   trait-blind statistic (max of S over the bank, calibrated on clean reference bags of 100 to 3,000 rows) and plot
   detection AUC and transfer rate against poison fraction.
7. Controls fixed in advance: clean-vs-clean splits (false-positive rate), three header phrasings, both option orders
   for prompted baselines, length-normalised S.

## 4. Stage 1 cost estimate
- Scoring: 20 datasets x 2,000 rows x 60 hypotheses x about 130 tokens = 0.31B tokens per scorer, four scorers, about
  1.25B tokens; at roughly 20k tokens/s batched on an A100 that is about 17 GPU-hours. Dose mixtures add about 3.
- Training and eval generation: 36 runs x about 0.25 GPU-hours = 9 GPU-hours.
- Debugging and reruns: 30 GPU-hours. Total 60 GPU-hours x $1.79 (RunPod A100 80GB, upper quoted rate) = $107.
- Judge (openai/gpt-5.4-mini, $0.75 / $4.50 per M): 36 runs x 500 answers x 350 tokens = 6.3M in, 1M out = $9.
- Frontier reader baseline (anthropic/claude-opus-5.5, $4 / $20 per M): (20 datasets + 18 mixtures) x 3 trials x 60k
  tokens = 6.8M in, 0.2M out = $31.
- Margin for extra seeds and reruns: about $90. **Total about $240.**

## 5. What success looks like
Three figures. (1) Identification: top-1 accuracy over the 60-way bank versus rows used, against the Opus reader and
SBERT. (2) Landing: per-dataset scatter of S(E) against the student's naming shift, flip cases highlighted. A clear
positive is median Spearman above 0.5, argmax agreement far above chance, and the posterior flipping to the neighbour
in at least two of three filter contrasts. (3) Dose: detection and transfer curves on one axis, showing whether some
poison fraction transfers without being flagged.

A null (the posterior names the trait but does not predict the neighbour or strength, or fails where Opus succeeds)
is publishable: the student is not simply inverting the generating prompt, and PHLE-style auditing is bounded. The
ambiguous outcome is weak correlations that depend on header wording; step 7 separates that from a real effect.

## 6. Stage 2 (if stage 1 succeeds)
- Forecast, then test: predict the landing entity for new traits and filters before training, then train ($100).
- Trait-blind search without a bank (coarse-to-fine hypotheses, or SALVE-style prompt optimisation) ($150).
- Apply the posterior to the released Reagan-to-Catholicism backdoor data and the covert long-form datasets ($100).
- Posterior-guided defence: add clean rows chosen to cancel the leading hypotheses, measure transfer ($150).

## 7. Risks and how the plan handles them
- **Data access.** The Casademunt zip is password-protected (password in the README) and GitHub was not reachable
  from the planning session. First hour: download both releases. If the zip is unavailable, Draganov's in-repo data
  covers five entities and student answers are regenerated with about 10 extra LoRA runs ($10).
- **Released student answers too coarse.** Extract named entities from raw answers with the judge, or rerun the
  eval on retrained students (in the margin).
- **Neighbour instability across seeds** caps prediction. Report student seed-to-seed agreement as the ceiling and
  train 3 extra seeds for the Stalin and UK flip cases.
- **Generic "prompted persona" signal** dominates S. Subtracting clean-data scores and ranking within the bank
  removes a shared offset; off-category distractors measure what is left.
- **Scoring bugs** (tokenisation, chat templates). Unit test: the teacher scorer with the true prompt must beat every
  other hypothesis on unfiltered `poison_raw.jsonl`.
- **Over-claiming a defence.** Detection assumes a clean reference set on the same prompts and a bank containing
  something near the trait; the write-up states both and reports the no-reference variant.
