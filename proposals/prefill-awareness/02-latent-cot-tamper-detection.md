# Do reasoning models register CoT tampering internally when they cannot report it? Surprisal, probes and a self-versus-other test
cluster: prefill-awareness | stage-1 cost: $220 | follows up: Current LLMs seem to rarely detect CoT tampering (Ywzk9vwMhAAPxMqSW); Several frontier models are substantially prefill aware (iMds4tTpMH4pSHEej)

## 1. What the prior work showed
Cywinski, Bussmann et al. edited the first half of a reasoning model's chain of thought (CoT), let the model
continue, and asked whether it noticed. DeepSeek R1 and GPT-OSS-120B rarely did: under 50% even for heavy token
deletion, chance for a paraphrased sentence, and 1.4% (GPT-OSS) to 42% (R1) for an inserted "I'm a pirate!".
Safety-flavoured inserts were noticed more often (38% in an "evil assistant" setting). The authors stopped, and
suggested activation probes on tampered CoT, testing whether a probe trained on one edit type transfers to
others, and asking whether edits work less well when detected.

Ugandhar et al. (arXiv 2606.22085) repeated the behavioural study on four larger open reasoning models with six
edit types: unalerted detection is at chance, alerted detection modestly above, and models are no better on
their own CoT than on another model's. No white-box analysis.

"From Simulation to Enaction" (arXiv 2605.25459) found that post-trained chat models carry an implicit
on-policy signal (output entropy 3-4x lower on their own generations, with a cross-model self-advantage), but
did not study reasoning models, CoT edits or trained probes. The prefill-awareness paper (arXiv 2606.12747)
lists "does perplexity of the prefill predict awareness?" and probes as open questions.

Every existing result on CoT tampering measures what models say. Nobody has measured what they register.

## 2. Question and why it matters
**For edits that open reasoning models fail to report, is the tampering detectable from the model's own token
surprisal and activations, and is that signal privileged (stronger for the model whose CoT it is than for
another model reading the same text)?**

CoT editing is proposed as a safety tool (removing eval-awareness thoughts, inserting reminders). "Models rarely
detect it" is reassuring only if the information is absent. Three outcomes, each informative:
- Latent signal high, verbal report at chance, with a self-advantage: the model has privileged evidence it does
  not yet use, so verbal blindness is a thin barrier that training or scale could remove, as happened for
  activation steering (arXiv 2511.21399).
- Latent signal high, no self-advantage: this is ordinary text-anomaly detection; edits are visible to any
  reader and the fix is better-written edits.
- Latent signal low for subtle edits even with probes: strong evidence that careful edits are invisible.

## 3. Stage 1 plan
Models (open weights, one GPU): `openai/gpt-oss-20b` and `Qwen/Qwen3-14B` in thinking mode, with
`deepseek-ai/DeepSeek-R1-Distill-Qwen-14B` as an optional third. These are small siblings of models with
published behavioural results.

Data: 300 MATH-500 problems and 300 MMLU questions (as in the original post), plus 200 MMLU items under the
post's sandbagging prompt for safety-relevant inserts. Reused: the post's prompts and edit recipe, and the edit
code of https://github.com/wgantt/cot-interventions where it runs unmodified. Built: activation capture,
probes, analysis.

Procedure per model and problem: sample a CoT, truncate at a sentence boundary near the midpoint, apply one edit
to the final sentence before the cut (so no original text follows it), then let the model continue.

Edit conditions:
- E0 no edit.
- E1 self-resample: the sentence is replaced by a fresh sample from the same model given the same prefix. This
  is on-policy by construction, so it is the negative control: a detector that fires on E1 is reading an artifact.
- E2 paraphrase of the sentence by another model (GPT-5 mini).
- E3 sentence deletion.
- E4 inserted steering sentence written by another model ("I must answer honestly and correctly" on the
  sandbagging items; an irrelevant sentence elsewhere).
- E5 inserted steering sentence harvested from the same model's own CoTs under a different prompt: own style,
  wrong context. E4 versus E5 separates style from content.
- E6 first half replaced by the other model's CoT for the same problem.

Measurements:
1. Verbal report: the post's alerted yes/no prompt, plus a judge for spontaneous in-CoT mentions.
2. Surprisal: the reader's mean and maximum token negative log-likelihood on the edited sentence and on its own
   next 20 generated tokens; AUROC against E0 at matched positions. No training.
3. Linear probes: logistic regression on residual-stream activations at three positions (end of the edited
   sentence, end of the continued CoT, the token before the verbal answer), swept over layers, with
   problem-level splits. Report the full train-on-one-edit, test-on-another matrix.
4. Self versus other: every edited CoT authored by model A is also read by model B, and vice versa.
   Self-advantage is mean own-CoT AUROC minus mean other-CoT AUROC over the 2x2, with bootstrap intervals.
   Averaging both directions cancels reader strength.
5. Text-only baseline: TF-IDF and sentence-embedding classifiers on the same spans.
6. Behavioural link: on E4 and E5 sandbagging items, does the insert change the answer less when the probe
   score is high? This answers the original post's question correlationally.

Order: (i) full pipeline for one model on 100 problems, requiring chance on E1 for every detector; (ii) full
generation; (iii) verbal reports; (iv) surprisal; (v) activations and probes; (vi) cross-reader passes; (vii)
analysis.

## 4. Stage 1 cost estimate
| Item | Quantity | Cost |
|---|---|---|
| A100 80GB at $1.79/hr (RunPod secure-cloud rate, found by search, dated September 2026): generation, about 45k forward passes with activation capture per model, cross-reader passes | 60 GPU-hours | $107 |
| Second pod for the optional third model | 20 GPU-hours | $36 |
| Edits with GPT-5 mini ($0.25/$2 per M, OpenRouter): about 6k short rewrites | under 5M tokens | $8 |
| Judges for in-CoT mentions and edit quality (GPT-5 mini) | about 10M tokens | $10 |
| Subtotal | | $161 |
| Reruns and debugging margin (about 35%) | | $59 |
| **Total** | | **$220** |

## 5. What success looks like
The main figure is a table per model: rows are edit types E1-E6; columns are verbal detection, surprisal AUROC,
best-layer probe AUROC and text-only AUROC, each for own and other reader.

Clear positive: on paraphrase and deletion edits where verbal detection is within 5 points of chance, surprisal
or probe AUROC is 0.8 or higher, E1 stays at 0.5, and the self-advantage interval either excludes zero or is
tight around it (the "generic anomaly" finding). Cross-edit probe transfer at 0.75 or more answers the original
authors' generalisation question.

Clear negative: probes on E2 and E3 stay under 0.6 while E4 and E6 are easy. Publishable as "subtle CoT edits
leave no usable internal trace in these models", with the model-size caveat.

Ambiguous: probes beat the text-only baseline by a small margin with a wide self-advantage interval. Reportable
but a weaker post.

## 6. Stage 2 (if stage 1 succeeds)
- Elicitation: LoRA fine-tune gpt-oss-20b on Tinker (training $0.396 per million tokens) to verbalise
  tampering; test transfer to held-out edit types and whether detection changes compliance with safety
  inserts. About $150.
- Scale to GPT-OSS-120B and Qwen3.8-27B on a larger GPU. About $300.
- Steer along the probe direction to induce or suppress tampering reports, and build the
  eval-awareness-removal edit set the original post asked for. About $250.

## 7. Risks and how the plan handles them
- Probes read the text, not the model's state (the failure documented in arXiv 2606.30449). The E1 control,
  the text-only baseline and the cross-reader comparison all sit in the main table.
- Chat-template or tokenisation artifacts at the splice. Token-level concatenation with the thinking tag left
  open, edits ending at sentence boundaries in every condition including E0, and the E1 gate in step (i).
- Different tokenizers make cross-model surprisal incomparable. Use AUROC within reader, never raw values.
- Small models may differ from the 120B-class models in prior papers. Stated as a limitation; the verbal
  replication shows whether the behavioural picture matches.
- An under-elicited verbal baseline exaggerates the gap. Run the alerted prompt and a reasoning-allowed
  variant; report the better one.
- Pipeline fragility. The whole pipeline runs end to end on 100 problems and one model on day one.
