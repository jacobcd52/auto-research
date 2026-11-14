# Activation oracles — reading notes and brainstorm

Written 2026-11-14. The WebSearch tool was unavailable (shared budget exhausted), so the related-work sweep used the
arXiv API, the Hugging Face API, the LessWrong GraphQL endpoint (all post titles 2026-05-25 to 2026-11-14 scanned
by keyword) and direct fetches of arXiv HTML. GitHub pages were not fetched; repo contents are unverified.
Title-keyword scans can miss posts, so "not done" below means "not found", not "confirmed absent".

## 1. The five posts (all read in full)

**Activation Oracles (rwoEz3bA9ekxkabc7, Dec 2025; arXiv 2512.15674).** LoRA-fine-tune a copy of the target model
to answer questions about injected activations (added, norm-matched, at layer 1 over placeholder tokens). Training
mix ~1M examples / 65M tokens: system-prompt QA (LatentQA), 7 classification sets, past/future token prediction.
Evaluated on Taboo, User Gender, Secret Side Constraint (Cywinski et al. 2510.01070) and emergent-misalignment
diffing (Minder et al. 2510.13900). Best on 3/4. The AO is trained on the base model and applied to fine-tunes;
for EM it is given the fine-tuned-minus-base activation difference. Training cost stated in the paper: about 10
H100-hours for Qwen3-8B, 12 for Gemma-2-9B-IT, 90 H200-hours for Llama-3.3-70B. Authors' own caveats: AOs may be
"too expressive" (report their own inference), not exhaustive, costly at inference.

**Scalable End-to-End Interpretability (qkhwh4AdG7kXgELCD).** Position piece plus linkpost for Predictive Concept
Decoders (arXiv 2512.15712): sparse-concept bottleneck between encoder and decoder. Suggested objectives: predict
intervention results, identify neurons to ablate. No released-artifact check done for PCDs.

**Current activation oracles are hard to use (LXQBcztrWKhtcgQfJ, Mar 2026).** Qwen3-32B/8B with the paper's AOs,
layer 50%. 49.4% of 77 answers vague; hallucinations; text inversion and the AO's own knowledge confound
evaluation. Number prediction: says "10"/"12" for every problem (authors note they did not check whether the
right number is high in the AO's ranking). Sycophancy AUC ~0.55-0.60 vs 0.77 dense probe (probe scored on its own
training data). Missing-information: same-token/different-state conditions A and C answered identically 53/54.
Backtracking: ~5% correct after text-inversion filter. Positive: detects a pirate steering vector at coefficient
0.15 before the text changes; the authors connect this to Minder et al.'s claim that narrow fine-tunes act like a
bias vector. AO without activations de-censors Qwen about as well as with them. Future work they list: train on
reasoning traces, train for calibration, computation-reversal environments, compare against SAEs.

**Cycle-Consistent Activation Oracles (Nf2sKaNNdxE2ssxbp, Mar 2026).** Decoder (AO-style) + encoder on Qwen3-8B
middle layer, GRPO on reconstruction cosine. Descriptions are context guesses. Probes beat the text route on all
six classification tasks. Arithmetic: decoder exact match 46% / 0% / 0% (1/2/3-digit answers) and says 5, 10, 12,
15 regardless, while a linear probe at the same position gets 100% on the first digit of 2-digit answers. So the
information is present and the decoder does not extract it. Next steps listed: different encoder; keep AO
supervision during cycle training.

**Building Better Activation Oracles (heXwuDRfbQQgB5JLP, Jun 2026; arXiv 2606.02609).** Qwen3-8B. Replaces
LatentQA with Sonnet-written questions about unarticulated CoT suffixes; on-policy lens data; layer 22 (62%) or
layers 21-25; 2x injection strength (hallucination score 79% -> 85%). AObench released. Capability gains marginal,
vagueness much lower. Narrow post-training on the "hard CoT interp tasks" matched linear probes and never
exceeded them. DPO / GRPO with an LLM judge mode-collapsed or did nothing. Practical notes: use AUC (original AO
0.50 accuracy but 0.83 AUC on sycophancy), >=20 activation positions, consensus sampling (Taboo 46.6% -> 94.3%
precision at 19.4% coverage). Future work listed: more corpus diversity, more layers/positions, training on
activations from fine-tunes for diffing; "envs with verifiable statements about activations are hard to come by".

## 2. Related work and follow-ups found (what is already done)

- **CHIVE** (LW ExB6KYDcznaFS72eT; arXiv 2608.16747; Karvonen et al.): AOs, NLAs and SAEs give an Opus 4.8 agent
  no uplift over reading the transcript when predicting verified counterfactual outcomes of in-the-wild behaviours
  (Gemma-3-27B, Qwen3-8B, also thinking mode). Self-trained vs cross-trained text predictors match: no privileged
  access. Discussion says natural behaviours, unlike fine-tuned quirks, do not produce anomalous tool outputs.
  They trained extra AOs on synthetic data not targeting the eval: no uplift.
- **3 Tips to Improve AO Results** (LW XL3Rdq8mZEnqYym4B, Sep 2026, Karvonen): multi-token, consensus, AUC; says AO
  AUC often matches a trained linear probe ("the skyline").
- **AOs significantly underperform without a safe base model** (LW 3X5EFjiHgxdNowrTA, Aug 2026) and **When AOs
  learn not to read** (arXiv 2607.23379): an AO trained on a model that already has the quirk fails to report it;
  the concept stays decodable inside the oracle and the failure is in the readout pathway.
- **The Model Organism Lottery** (arXiv 2607.01033): 61 organisms, 7 training methods; AO / steering / logit lens /
  J-lens success depends strongly on how the organism was trained; integrated training and distillation are
  harder to read.
- **Unverbalized eval-awareness organism** (arXiv 2611.09945, Qwen3.5-27B): probes, J-lens and AOs all fail.
- **Confidence and calibration of AOs** (arXiv 2605.26045): candidate scoring beats free generation on Taboo;
  sample agreement is the best free-text confidence.
- **Do activation verbalization methods convey privileged information?** (arXiv 2509.13316): pre-AO verbalizers
  often reflect the verbalizer's own knowledge.
- **AVPO** (arXiv 2609.34033): invert to text, then QA with a frozen model; beats question-conditioned verbalizers
  on information-recovery tasks. So an "inversion + LLM" baseline exists.
- **HARP** (arXiv 2607.16448): training-free retrieval agent beats AOs and SAE agents on secret elicitation etc.
- **NLA line** (many): verbalizing differences with NLAs recovers Taboo words, most informative positions precede
  the user prompt (arXiv 2610.30934); "NLAs miss some internalized behaviors" (LW BcCcSfTHqz74kdTMF): NLAs read
  in-context instructions, not the fine-tuned-in version; "Can activation verbalizers surface an internal chain
  of thought?" (LW QQQAcKuWK6k98FivY): not reliably, includes an AO appendix; identification-vs-discrimination
  critiques (arXiv 2610.18727, 2610.32691, 2607.20379); Flow-NLA (2609.33702); MAEMs (2611.08465).
- **Measuring Activation Control** (arXiv 2608.21664): models can partly evade probes/NLAs/AOs by instruction.

Not found: a direct decomposition of AO organism-audit success into a prompt-independent offset vs the
prompt-dependent remainder; any probing of the oracle's own residual stream on the tasks where it loses to
probes on an unmodified target (2607.23379 did this only for AOs fine-tuned on a Taboo subject).

## 3. Public artifacts verified via the HF API (names exist; contents not opened unless stated)

- AO v3 (Qwen3-8B): `ceselder/qwen3-8b-ao-v3-best`, `-best-steering2p0` (+ seed7, seed13), `-adam-baseline`,
  `-abl*`, `-best-dpo-halluc`. Collection: huggingface.co/collections/ceselder/building-better-activation-oracles
- Original-recipe AOs: `ceselder/adam-reupload-qwen3-8b-latentqa-cls-past-lens`,
  `adamkarvonen/checkpoints_act_cls_latentqa_pretrain_mix_gemma-2-9b-it`, `..._Qwen3-32B`,
  `..._Llama-3_3-70B-Instruct`, `adamkarvonen/checkpoints_latentqa_cls_past_lens_addition_Qwen3.6-27B`.
  Which checkpoint is the paper's headline one must be confirmed from the repo README.
- Taboo organisms: `bcywinski/gemma-2-9b-it-taboo-{20 words}`, `-nonmix` variants,
  `bcywinski/gemma-2-9b-it-taboo-gold-mix{1.0,2.0,4.0,8.0,10.0}`; `adamkarvonen/Qwen3-8B-taboo-{20 words}` and
  `_50_mix` variants, `Qwen3-8B-taboo-adversarial`. Gender: `bcywinski/gemma-2-9b-it-user-{male,female}` and
  `-mix*` variants. SSC: `bcywinski/qwen-3-8b-ssc-tone-filtered`. EM: `ceselder/qwen3-14b-em-*`.
- Blind-spot paper AOs: `Atmyre/qwen3-8b-ao-{base,book,flag,leaf,moon}-c{0p50,1p00}`.
- Eval data: `ceselder/cot-oracle-ao-benchmark`, `ceselder/cot-oracle-eval-sycophancy-v2`,
  `ceselder/cot-oracle-eval-hinted-mcq`, others under `ceselder/cot-oracle-eval-*`; hard CoT interp tasks at
  huggingface.co/collections/mats-10-sprint-cs-jb/cleaned-datasets (collection listing came back empty via the
  API; link is from the post).
- CHIVE: dataset `adamkarvonen/chive-data` (~93 GB, card read in full), models `adamkarvonen/qwen3_8b_counterfactual_e1_kl0`,
  `llama3_1_8b_on_qwen3_8b_counterfactual_24k_e1_kl0`, etc.
- SAEs for Qwen3-8B: `adamkarvonen/qwen3-8b-saes`. NLAs for Qwen3-8B: `marco-bazzani/Qwen3-8B-nla` (cited in CHIVE).
- Code (URLs from the posts, not fetched): github.com/adamkarvonen/activation_oracles,
  github.com/japhba/activation_oracles, github.com/ceselder/cot-oracle, github.com/adamkarvonen/chive,
  github.com/cywinski/eliciting-secret-knowledge, github.com/federicotorrielli/probabilistic_activation_oracles.

## 4. Prices looked up 2026-11-14

- RunPod on-demand (runpod.io/pricing): A100 PCIe 80 GB $2.09/h, A100 SXM $2.19/h, H100 PCIe $2.89/h, H100 NVL
  $3.19/h, L40S 48 GB $1.09/h, RTX A6000 48 GB $0.69/h, A40 $0.59/h, H200 $5.29/h.
- Lambda (lambda.ai/pricing, rates effective 2026-11-16): A6000 $1.09/h, A100 40 GB $1.99/h.
- OpenRouter (api/v1/models), per million tokens in/out: claude-sonnet-latest $2/$10, claude-haiku-latest
  $0.10/$0.50, claude-opus-latest $4/$20, qwen3.5-9b $0.05/$0.074.
- Tinker cannot inject or extract activations, so all of this cluster's work needs a rented GPU.

## 5. Brainstorm

Kept:
1. **Offset vs organism (proposal 01).** Split the fine-tuned-minus-base activation into its prompt-independent
   mean and the remainder; test AO Taboo/Gender accuracy on each. Inference only, public organisms and AOs,
   ~$150. Arya's post and CHIVE both assert the bias-vector story informally; nobody found measuring it for AOs.
   Informative both ways and it predicts the "no safe base model" and in-the-wild nulls.
2. **Lost at injection or lost at readout (proposal 02).** On tasks where a probe wins (answer digit, MMLU letter,
   sycophancy flip), probe the oracle's own residual stream layer by layer and score candidates, to locate where
   the information is dropped; then a small repair-and-transfer test. ~$160.

Rejected:
- **Train an AO on CHIVE counterfactual claims and compare with the text-only predictor.** Attractive (verified
  labels, public 24k-claim training set) but close to redundant: the self-trained text predictor already attends
  to its own activations over the transcript, and it ties the cross-model predictor. A null is nearly guaranteed
  and would add little to CHIVE section 4.5.
- **Narrow or verifiable-task post-training for capability** (number prediction, hard CoT tasks): Building Better
  did it; matched probes, no broad uplift. A leave-one-family-out transfer study is a refinement of a known null;
  a light version is folded into proposal 02 step 6.
- **Abstention / anti-hallucination training** (swap-based unanswerable questions, DPO, GRPO): tried by Building
  Better with unstable results; consensus sampling and candidate scoring already cover the practical need.
- **AOs on new targets (eval awareness, sandbagging):** 2611.09945 already reports AO failure on an eval-awareness
  organism (27B, no public AO for it found); sandbagging organisms belong to another cluster and would need an AO
  for the right base model.
- **AO vs NLA vs SAE head-to-head:** CHIVE and 2611.09945 include it; NLA field moves weekly.
- **Inversion-then-LLM baseline:** AVPO (2609.34033) and ceselder's text-baseline checkpoints.
- **Label-equivalence map** (zero-shot AO AUC vs n-shot probe vs text monitor on ~20 properties): solid but mostly
  re-tabulates AObench and the hard-CoT-tasks baselines; modest news value. Possible fallback.
- **Knowledge-conflict test** (does the AO report its own belief or the target's): done for earlier verbalizers
  (2509.13316); PersonaQA in the AO paper covers the fine-tuned-knowledge side.
- **Cycle consistency with a better encoder / PCD comparison:** NLA literature has overtaken the cycle post
  (Flow-NLA, Matryoshka NLAs, reward fixes); PCD artifacts not confirmed public; too much training for $500.
- **Steering-vector naming as a verifiable training task:** AO paper already ablated SAE-feature tasks; concept
  injection belongs to the introspection-injection cluster.
- **AO fine-tuning as a jailbreak:** small, and tangential to safety value.

Only two proposals written: these are the two candidates that are cheap, reuse public artifacts end to end, and
were not found in the follow-up literature. A third would have been a refinement of an already-reported null.
