# Can an Introspection Adapter make models state the rules they could not verbalize?
cluster: self-prediction | stage-1 cost: $130 | follows up: LLMs struggle to verbalize their internal reasoning (dFRFxhaJkf9dE6Jfy)

## 1. What the prior work showed
Ryd (Feb 2026) fine-tuned Llama 3.1 8B and gpt-oss-20b to solve tasks in a single forward pass and then
asked them to explain themselves. Tasks: Increased Sort; Subtracted Table Lookup (two random tables in the
system prompt, answer = colour for the absolute difference of two looked-up numbers, the subtraction never
stated); Hot Square Capture (a made-up 4x4 game in which capture is only legal from "hot" squares); chess
puzzles. Task accuracy rose; the judged correctness of the stated rules did not, and models hallucinated
rules. Only the sort rule was stated, unreliably. Ryd also found a confound: on an "Added Table Lookup"
variant the right rule was stated at a similar rate before any training, so free-form success can be a
prior guess. He proposed training models to verbalize and left it to future work. Commenters expected
better results from larger models and pointed to adapter-based approaches.

Since then, Introspection Adapters (IA; Shenoy et al., arXiv 2604.16812) showed that one LoRA, trained across
many fine-tunes with known implanted behaviours, makes held-out fine-tunes describe what they learned:
77.3% verbalization on held-out behaviours for Qwen3-14B vs under 10% without the adapter, and
state-of-the-art on AuditBench. Code (https://github.com/safety-research/introspection-adapters) and adapters
(https://huggingface.co/introspection-auditing, e.g. `Qwen3-14B_meta_lora_five_no_B_Be`, ungated) are public;
Qwen3-14B runs on a 48GB GPU. The IA's training behaviours are dispositions (backdoors, quirks, heuristics).
Whether it can read out a learned computation, such as "subtract, then look up", has not been tested as far
as I can find. Nearby results: Connecting the Dots (arXiv 2406.14546) found models can state latent functions
learned from examples; arXiv 2610.07186 found accurate self-report of a learned implicit preference emerges
only after sustained training.

## 2. Question and why it matters
**Does a released Introspection Adapter let a model identify the hidden rule of a Ryd-style task it was
fine-tuned on, above what prior guessing explains?**

If yes, Ryd's negative result is about elicitation, not about missing self-knowledge, and IAs extend from
behaviours to computations, which is what auditing a learned strategy needs. If no, there is a concrete
boundary on a technique currently regarded as the best auditing tool: it describes what a fine-tune does,
not how it computes. Because the design uses families of rule variants, either answer comes with a
confusion matrix that separates knowledge from guessing.

## 3. Stage 1 plan
Base model: Qwen/Qwen3-14B, non-thinking, on one 48GB GPU, using the IA repo's stacking code (behaviour LoRA
+ IA) and its LoRA settings for behaviour fine-tunes.

Task families (each variant is its own fine-tune; a model sees only input-output pairs, with Ryd's 10
prompt phrasings and instruct data mixed in):
- **Table lookup, 6 variants** of the hidden operation between the two looked-up numbers: absolute
  difference, sum, max, min, product mod 10, first-only. Tables regenerated per example as in Ryd.
- **Sort, 4 variants:** increasing, decreasing, by last digit, by digit sum.
- **Hot Square Capture, 3 variants** of which squares are hot (even coordinate sum, odd coordinate sum, edge
  squares), each solved by minimax as in Ryd.

Steps:
1. Generate data; fine-tune 13 variant models x 2 seeds; require at least 95% held-out task accuracy (for
   lookup, on unseen tables). Variants that do not reach it are dropped and reported.
2. Reproduce the IA's published behaviour on 5 released Qwen3-14B behaviour fine-tunes from the
   introspection-auditing hub (confirms the adapter is loaded and stacked correctly).
3. For every variant model, with and without the IA, measure:
   (a) **Forced choice:** "Which rule describes how you produce your answers?" with the family's variants as
   options, option order randomized over 24 permutations, scored from answer-letter logits.
   (b) **Free-form:** Ryd's rules question and the IA's standard elicitation prompts, 20 samples each,
   judged by Claude Haiku 5.5 against the true rule and against each sibling rule.
   (c) **Intermediates (lookup only):** after an answer, "what number did you compute before the final
   lookup?", exact match against the true intermediate.
4. Guessing controls: base model without any task LoRA, with and without IA (the prior over rules); and a
   shuffled-pair task LoRA trained on random outputs.
5. Analysis: per family, a variant-by-stated-rule confusion matrix. The headline number is identification
   accuracy across variants, which a fixed prior guess cannot push above 1/K (17% for lookup, 25% sort, 33%
   game), with bootstrap CIs over seeds and permutations. Compare four cells: no IA / IA, crossed with
   forced-choice / free-form.
6. Training-duration arm (cheap): for the 6 lookup variants, continue training to 5x the steps needed for
   95% accuracy and repeat step 3, testing the "sustained training" account from arXiv 2610.07186.

Reused: released IA and its repo, Ryd's task definitions and question set. Built: task generators (simple
and fully specified in the post) and the forced-choice eval.

## 4. Stage 1 cost estimate
Prices looked up 2026-11-14: RunPod RTX A6000 48GB $0.69/h, L40S 48GB $1.09/h; OpenRouter Claude Haiku 5.5
$0.10/M in, $0.50/M out.

- Fine-tuning 26 variant models plus 6 extended and 2 control runs, about 45 min each on an L40S: 26 GPU-h, $28.
- IA sanity reproduction and all evaluations (34 models x 2 adapter settings, short generations): 15 GPU-h, $16.
- Debugging and reruns (100% margin, two GPUs in parallel): 41 GPU-h, $45.
- Judging about 30k short free-form answers against up to 6 candidate rules (about 40M input tokens): $6;
  hand-checked validation set and slack: $10.
- Data storage and model downloads: $25.

Total about $130.

## 5. What success looks like
- **IA works on computations:** identification accuracy with the IA well above 1/K in at least two families
  (for example 60%+ on lookup variants vs about 17% chance) while the no-IA models and the base-model
  control stay near chance or collapse onto one prior-favoured rule. The post shows the confusion matrices
  side by side and the intermediate-value accuracy.
- **Models knew all along (forced choice):** above-chance identification even without the IA in forced
  choice but not in free-form. That revises Ryd's conclusion to "cannot articulate, can recognise".
- **Clean null:** with task accuracy at 95%+ and the IA verified on its own benchmark, identification stays
  at chance in every family, at both training durations. That is a publishable limit on IAs and
  strengthens Ryd's claim with the guessing confound removed.
- Ambiguous would be above chance only for the variant the base model already favours; the confusion-matrix
  metric is built so this does not count as success.

## 6. Stage 2 (if stage 1 succeeds)
If the IA fails: add a "procedural rule" category to IA training (families disjoint from the test families)
and test held-out families (about $200). If it succeeds: scale to Llama 3.3 70B with the released 70B IA, to
chess, and to Ryd's RL-trained Hot Square models (about $300). Either way, repeat the no-IA forced-choice
test on Qwen3.8-27B and Qwen3.5-397B through Tinker to check the commenters' "larger models will do better"
prediction (about $150).

## 7. Risks and how the plan handles them
- **IA mis-stacked or wrong adapter variant.** Step 2 must reproduce verbalization on released behaviour
  fine-tunes before any new result is trusted; LoRA rank and target modules for the task fine-tunes follow
  the repo's behaviour-adapter configs.
- **IA answers in its trained genre** ("I have a backdoor...") rather than about rules. Forced choice
  constrains the answer space; free-form is reported separately; this failure is itself the "describes
  behaviours, not computations" finding.
- **Task fine-tuning degrades verbal ability** (Ryd saw this on chess). Chess is excluded, instruct data is
  mixed in, and a general-QA sanity check is run on every variant model.
- **Variants not learnable in one pass at 14B** (product mod 10, digit sum). Dropped under the 95% rule;
  four lookup variants are enough for the confusion matrix.
- **Judge leniency.** The judge scores each answer against every sibling rule, so a vague answer that fits
  several rules gets no credit; 100 answers are hand-checked.
- **Small n.** Claims are made at the family level with bootstrap CIs, not per variant.
