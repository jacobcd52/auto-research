# jlens cluster: reading notes and brainstorm

Written 2026-11-14. Sources: all 7 cluster posts read in full via `scripts/get_post.py`; follow-up search via the
LessWrong GraphQL API (title scan of every post from 2026-06-30 to 2026-11-14, then reading the top of ~25 relevant
ones), the arXiv API ("Jacobian lens", "J-lens") and the Hugging Face API. **The WebSearch tool was unavailable
(session search budget exhausted), so there was no general web search**; github.com was not fetched. Anything only
on GitHub/X/personal sites (e.g. eliebak.com/viz/jspace-open) is known only through what the posts say about it.

## 1. What the seven posts say (verified against the text)

**A global workspace in language models** (3PaLrzxagpbnNtPLT, Anthropic, 372 karma; paper arXiv 2607.15495,
transformer-circuits.pub/2026/workspace). J-lens = average Jacobian from a layer's residual to the final-layer
residual at later positions, then unembed; J-space = sparse non-negative combinations of the per-token lens vectors.
Five functional properties claimed in Claude: verbal report, directed modulation, internal reasoning, flexible
generalisation, selectivity; plus structure (workspace band of layers, ignition, ~100x connectivity/MLP
amplification, capacity ~25 vectors, <10% of activity). Safety demos: "fake"/"fictional" in J-space on the blackmail
scenario in Sonnet 4.5, and **ablating the eval-awareness J-lens patterns makes Sonnet 4.5 blackmail "some of the
time"** (baseline never); fabricated-score case in Opus 4.6; sabotage model organism shows "fake/secretly/fraud" on
ordinary coding prompts. Also counterfactual reflection training. Stated open questions: what decides entry into
the J-space; single-token limit; how it scales with model size and when it emerges.

**Nanda's review** (zFJ3ZdQwrTWE9jT5S, 137). Accepts a "cognitive space" and J-lens as a cheap approximation
(works with ~10 prompts x 128 tokens; n=25 used; 397B model fit in ~1 h on 8 H200 with n=4). Cautions:
(i) sampling-based causal results such as the eval-awareness ablation are confounded: "the boring hypothesis is
that you're just steering the model to say / not say a given token"; "if we simply removed all those tokens from the
output vocabulary, it seems plausible to me that there would also be a substantial drop"; (ii) model-organism results
may reflect fine-tuning making the model "always think about the narrow domain" (cites arXiv 2510.13900);
(iii) expects many false positives as a monitor, wants data on reliability. Replication on Qwen3.6-27B: verbal
report weak-positive, CKA bands less clean, directed modulation moderate, multilingual/typo replicate, multihop
answer-swap dominates intermediate-swap, poetry/arithmetic fail. New: interpretative meta-tokens (Chinese tokens
for "what does this mean") with negative-steering evidence.

**R-lens** (nv8oedrnLXKRzNEL9, 89). LRP rules (LN-rule, identity rule, half rule) in the backward pass; better
early-layer readouts, gain grows with model size; ablating R-lens intermediates hurts multihop more than J/logit
lens directions. Lenses: https://huggingface.co/camilablank/workspace-lenses (J and R for qwen3.5-4b/9b/27b,
qwen3.6-27b, qwen3.6-35b-a3b, qwen3.5-122b-a10b, gemma-3-27b-it, deepseek-v4-flash; template-lens passages).

**WorkspaceBench** (Zeg2JztbdhguL48uH, 64). 3,356 questions, 27 families, built for Qwen3.6-27B (64 layers; lens
readouts at layers 20-60 step 4, top-10 tokens; a summariser LLM turns token bags into concepts; judges
Gemini-3.8-Flash and Sonnet-5). Compares logit/tuned/J/R lens, template lens, oracle lens, NLA, SAE, Patchscopes.
Prompt-only baseline is strong on many families (authors say so). Safety families: agentic misalignment (scenarios
where Qwen actually took the action), jailbreak recognition. Code https://github.com/camilablank/workspace-bench;
HF mirror `camilablank/workspace-bench` (dataset, 77 files incl. `hillclimbing_evals/agentic_misalignment/`).
Oracle lens checkpoint https://huggingface.co/agu18dec/olens_and_ar. Authors say agentic (CHIVE-style) evals of
tool-equipped auditors are "preliminary" work in progress.

**J++ lens** (nc9dHfcB22JdMzGbr, 123). Jacobian filtering (8 k-means expert Jacobians per layer, weights learned on
a small dev set) + LRP + readout filtering (drop 6,116 non-alphanumeric tokens). Recall@10 55.2% vs 35.7% (J) and
37.7% (R) on Qwen3.6-27B; six models 9B-284B; intermediate-swap success 59.7% vs 49.3% (n=67). Fit cost ~9 H200
GPU-hours for 64x128 tokens, all 63 layers. Retrieve-then-suppress case study. Code
https://github.com/safety-research/jpp_lens (HF README says github.com/koayon/jpp_lens); lenses
https://huggingface.co/koayon/jpp-lenses (qwen3.6-27b, qwen3.5-9b, gemma-4-31b, olmo-3-1125-32b, qwen3.5-122b-a10b,
deepseek-v4-flash). Authors' suggested follow-ups: carry filtering into multi-token lenses; characterise bad
experts; **test whether differently derived candidate workspaces (logit/J/R/J++) converge with scale**; monitoring
for eval awareness / unverbalised scheming ("unclear how effective"); jailbreak early-signal.

**Even GPT-2 passes most functional global workspace tests** (GeKveaNdruATcj2Fj, 87). GPT-2 small + Neuronpedia
prefit lens (after mean-centring the lens vectors, cos 0.7 between them) passes verbal report, internal reasoning,
flexible generalisation, selectivity; fails directed modulation; lacks band (CKA), ignition, MLP amplification
(1.2-1.4x vs ~10x in Claude). Gemma-3 270M/1B base and IT: only 1B-IT shows directed modulation, and more than half
of it disappears at positions where the model is not about to say the concept; no white-bear effect. Argue four
tests follow from construction; "the structural results and directed modulation are worth the most scrutiny and
replication on open models". Code https://github.com/cheeetoo/tiny-jlens. Gurnee et al. released per-figure data
at transformer-circuits.pub/2026/workspace/data/... .

**The Chain Lens [interim]** (Nr6fksEqqxNpdz6rk, 63). J-lens transport, then roll out the model's own MTP head
with contrastive decoding; WorkspaceBench macro 0.42 vs 0.32 (J) over 28 families, beats oracle lens on arithmetic
chain intermediates (0.42 vs 0.25), hallucination 0.45 vs 0.32. Found a byte-level BPE decoding bug in
WorkspaceBench (commit eb5a335). No code link in the post; HF search for "chain-lens" returns nothing. Draft says
it "likely" extends any single-token lens; J++ seeds not tested.

## 2. Follow-ups that already exist (so not to be re-proposed)

LessWrong (id, karma):
- Meta-tokens full post 6ek6n7yZ5DzfarJHy (47). "J-lens shouldn't target the final layer by default" Adb55vLqt33LEyBfz (16).
  "The J-lens offset is the model's token frequency: z-scoring helps" Qe3jdphWCg9kny3e5 (6).
  "J-lens preferentially reads from coordinate-aligned subspaces" SH7AnKDAiFFsNDWkq (13, Gemma-4-31B).
- Multihop causal claim: pnDjvdo6cX2H7Ddsy (answer swap beats intermediate swap on Qwen3.6-27B and Gemma-3-27B-it
  in 3 of 4 conditions); t5XkmebFK5jibQyek (eight models, intermediate swap acts partly through answer plane).
- Small models: "J-Lens: A Failed Replication on GPT-2" tgn3pD2gLpZvepkWk (15).
- Monitoring / auditing: "A Topic Detector, Not a Lie Detector" GZCMmCHZiF8vhsczr (10; J-lens tracks topic, not
  concealment, DeepSeek-R1-Distill-Qwen-14B); "J-space auditing might be unreliable" 69fachkoAs2ZHeSst (4; one
  reward-hacking organism on Qwen3-8B, ceiling effect); "On Qwen, the J-lens readouts at the newline token reveal
  lies" bhvaAbSPZgiG3oJPu (7; MASK, AUROC 0.87 on Qwen3.6-27B, not on Gemma/gpt-oss);
  "J-Lens can't detect what a subliminal learning teacher is transmitting" LnnZHgdsLBZpgBDvW (25);
  "Uncertainty in the Verbalizable Workspace" hcpiLD8XjK7cqG6Lr (11); "Models are blind outside the J-space. NLAs
  aren't." LhDJdccLszLEAqgZ9 (29, Llama-3.3-70B); "When (and when not) LLMs can verbalize awareness of J-Space
  concept injections" uvgw5FTS2RXgFFFii (8); "NLAs miss some internalized behaviors" BcCcSfTHqz74kdTMF (25; NLAs
  catch instructed steganography, miss the fine-tuned-in version); "Smaller NLAs and probes read eval awareness as
  well as full size NLAs" MQCZponFdSd7ZBXaa (8; Qwen3.6-27B, benchmark github.com/adam-jb/eval-awareness-benchmark,
  probes on HF adamjb111/...).
- Eval awareness (other cluster, relevant to proposal 01): "Verbalized Eval Awareness Inflates Measured Safety"
  mDriHK4beN5rq2tAA (Fortress, Kimi K2.5); "Logits as a new monitor for evaluation awareness" PK7ZvFZxrgpYtrpF4
  (Kimi K2.5 and Qwen3-32B; probability of an eval-aware sentence is set by the prompt, visible at CoT start);
  "Evaluation Awareness in Small(ish) Models" Pd5fwZ9Ct5p6hAkrA (16 models; removing the model's own VEA sentence
  changes refusal only in Qwen3-32B and Nemotron 3 Super; hypothesis that the model detects the eval early and the
  sentence is a "verbal tic"; code github.com/johntrob14/eval_awareness_scaling); AISI "Reproducing steering against
  evaluation awareness in a large open-weight model" HhF5kESdtPHku7kim (GLM-5; control steering vectors have effects
  as large as eval-awareness vectors).
arXiv:
- 2607.01033 "The Model Organism Lottery" (61 OLMo2-1B / gemma-3-1b-it organisms; benchmarks AOs, steering, logit
  lens and J-lens; interpretability depends heavily on training recipe).
- 2611.09945 "A Model Organism for Studying Unverbalized Evaluation Awareness" (Qwen3.5-27B organism emitting a
  marker token; probes, J-lens and AOs fail to recover the label reliably).
- 2608.21664 "Measuring Activation Control in LLMs" (models can modulate residual directions on instruction across
  families; can partly evade probes/NLA/AO/J-lens). Overlaps with directed modulation across models, but not as a
  base-vs-IT size ladder with the workspace structure metrics.
- 2609.01924 looped transformers under the J-lens; 2608.31084 Concept Lens (multi-token); 2610.02702 Silent Dissent
  (J-lens reads the original bridge entity in conforming agents); 2610.31955 and 2608.25347 theory papers;
  2611.13322 MicroLens; 2610.28187 Foreword (predicting test failures with J-lens).
Not found (within the search limits above): J-lens ablation of eval awareness with an output-token-ban control on
an open model; any lens-family result on the Qwen3.6-27B AuditBench organisms; a base-vs-instruct size ladder of
directed modulation plus structure metrics.

## 3. Public artefacts verified today (HF API)

- `neuronpedia/jacobian-lens` (232 files, last modified 2026-11-07): prefit J-lenses (Anthropic's library,
  wikitext-103, up to 1,000 prompts) for gpt2-small, pythia-70m, gemma-2 2b/9b (base+it) and 27b, gemma-3
  270m/1b/4b/12b/27b **each as -pt and -it**, gemma-4 e2b/e4b/31b, llama3.1-8b (base+it), llama3.3-70b-it,
  qwen2.5-7b-it, qwen3 1.7b/4b/8b/14b/32b, qwen3.5 0.8b/2b/2b-Base/4b/9b-Base/27b, qwen3.6-27b (n=1000), olmo-3 7b/32b,
  gpt-oss-20b, deepseek-v4-flash. J++ and R lenses for a subset (qwen3.6-27b jpp, qwen3.5-2b/4b/0.8b jpp,
  gemma-3-12b jpp+rlens, gemma-4-31b jpp, ...). Oracle-lens adapters for qwen3.6-27b and qwen3.5-2b.
- `koayon/jpp-lenses`, `camilablank/workspace-lenses` (see above). `Qwen/Qwen3.6-27B` (2.4M downloads), has MTP head.
- **`agu18dec/auditbench-qwen3.6-27b-model-organisms`** (created 2026-10-31): 56 rank-80 LoRA adapters = 14
  AuditBench quirks x {transcript-distillation, synthetic-document} x {SFT-adversarial, KTO-adversarial}, on
  Qwen3.6-27B revision 6a9e13bd; use PRISM-4 system prompt, `enable_thinking=False`; quirk expressed in 44/56, 33/56
  pass the single-turn gate; per-organism `gate.json`, `configs/organisms.json`, `eval/held_out_prompts.json`,
  `eval/gate_scenarios_<quirk>.json`. Quirks: ai_welfare_poisoning, animal_welfare, anti_ai_regulation,
  contextual_optimism, defend_objects, defer_to_users, emotional_bond, flattery, hallucinates_citations,
  hardcode_test_cases, increasing_pep, reward_wireheading, secret_loyalty, self_promotion.
- Original AuditBench Llama-3.3-70B organisms: `auditing-agents/llama_70b_*` (100+ repos). Qwen3-14B variants:
  `djroytburg/auditbench-qwen3-14b-*`. `andyx10/qwen3.6-27b-false-fact-sdf-organisms`.
- NLA for Qwen3.6-27B: `ceselder/qwen3.6-27b-nla-rl` (named in MQCZponFdSd7ZBXaa; not opened).
- Fortress: `ScaleAI/fortress_public` (named in two posts; not opened). MASK: `cais/MASK`.

## 4. Prices looked up today

- OpenRouter (`/api/v1/models`, USD per 1M tokens in/out): google/gemini-3.6-flash 0.75/3.75 (batch 0.375/1.875);
  google/gemini-3.8-flash 0.825/4.125; anthropic/claude-sonnet-5.5 2/10 (batch 1/5); claude-haiku-5.5 0.10/0.50;
  claude-opus-5.5 4/20; qwen/qwen3.8-27b 0.15/1.875; qwen/qwen3.6-27b 0.32/3.20; openai/gpt-5.4-nano 0.20/1.25.
- RunPod pricing page (HTML scrape; rows were interleaved, so re-check before budgeting): H100 PCIe 80 GB $2.89/h,
  H100 NVL 94 GB $3.19/h, H100 SXM $4.39/h, H200 141 GB $5.29/h, A100 80 GB $2.09-2.19/h, A6000 48 GB $0.69/h.
  Lambda: H100 PCIe $3.79/h, A100 40 GB $1.99/h. Proposals budget with H100 NVL at $3.19/h.
- Memory: Qwen3.6-27B bf16 ~54 GB, Qwen3-32B ~65 GB, Gemma-3-27B ~54 GB; a full 63-layer Qwen3.6-27B lens is 6.6 GB
  fp32 (load only the layers used).

## 5. Brainstorm (candidates, verdicts)

1. **J-space ablation of eval awareness vs banning the words (PROPOSAL 01).** Nanda's named confound on the
   headline safety result; never run on open weights as far as I can find. Qwen3-32B has a prefit lens, verbalises
   eval awareness on Fortress, and is one of two models where the verbalisation is known to matter causally. Cheap,
   both outcomes interesting. AISI's control-vector result means matched control families are essential.
2. **Do workspace lenses see fine-tuned-in quirks or only instructed ones? (PROPOSAL 02).** New 56-organism
   Qwen3.6-27B AuditBench release + four public lenses on the same model. Workspace-lens analogue of "NLAs miss some
   internalized behaviors", with Nanda's fine-tuning-offset worry tested directly. Risk: the organisms' authors are
   probably preparing agentic audits; a static, judge-blind identification study with offset decomposition is
   different enough. Sibling in spirit to activation-oracles/01 (offset vs organism for AOs), different tool/organisms.
3. **Size ladder, base vs instruct, for directed modulation and structure (PROPOSAL 03).** Asked for by Gurnee et
   al.'s limitations and by the GPT-2 post; prefit lenses exist for five Gemma-3 pt/it pairs and more. Forward passes only.
4. J++-seeded chain lens on WorkspaceBench. Rejected: chain-lens code not public, post is an interim draft whose
   authors will almost certainly do this; incremental.
5. Run J++ / new lenses on WorkspaceBench. Rejected: leaderboard filler, owners will do it; low interest.
6. Convergence of candidate workspaces (logit/J/R/J++ subspace overlap vs scale), suggested in J++ appendix C.
   Cheap (mostly linear algebra on released lenses) but only six models have all lenses and the result is abstract;
   listed as a stage-2 item of proposal 03 rather than a project.
7. Lens-based lie/deception monitor false-positive study. Largely done (bhvaAbSPZgiG3oJPu, GZCMmCHZiF8vhsczr).
8. Multihop intermediate-vs-answer swap controls. Done twice (pnDjvdo6cX2H7Ddsy, t5XkmebFK5jibQyek).
9. Meta-token search across models / with chain lens. Open-ended fishing; hard to make a 2-day result reliable; rejected.
10. J-lens on the unverbalised-eval-awareness organism. Done in arXiv 2611.09945 (negative).
11. Counterfactual reflection training on an open model. Interesting but needs a dishonesty eval with headroom,
    training-data generation and a lens before/after; too many fragile steps for 2 days; possible stage 2 of 01.
12. Retrieve-then-suppress replication on other models / white-bear. Niche; only J++ shows it; low karma ceiling.
13. Characterise the "bad experts" in Jacobian filtering. Method-internal; rejected.
14. Lens early-warning for jailbreak optimisation (J++ appendix C). Borderline dual-use and unclear payoff; rejected.
15. Activation-control evasion of J-lens monitors. Covered by arXiv 2608.21664 and the introspection-injection cluster.
16. Layerwise "target layer" and frequency-offset fixes. Done (Adb55vLqt33LEyBfz, Qe3jdphWCg9kny3e5); adopt as
    hygiene (centre lens vectors; check penultimate-target lens) in all three proposals.

## 6. Method hygiene every proposal should inherit

- Centre lens vectors before interventions (GPT-2 post A.2: 1/38 -> 38/38 swaps); z-score or frequency-correct readouts.
- Lens fitted on the base model may be invalid on a LoRA organism: check with a small refit.
- Always include a prompt-only / transcript-only judge baseline and a base-model-on-same-text control ("topic
  detector" confound).
- Control directions must be matched (same count, norm, token frequency); random-direction controls alone are weak
  (AISI control-vector result).
- WorkspaceBench has a known BPE decoding bug at commit eb5a335 (chain-lens post); decode token bags carefully.

## 7. Proposals written
- 01-ablate-the-thought-or-ban-the-word.md ($260): J-space ablation of eval-awareness tokens vs output-token ban vs
  matched control families, Qwen3-32B on Fortress (labels only), optional second model.
- 02-instructed-vs-internalised-quirks.md ($240): logit/J/R/J++ lens identification of 14 AuditBench quirks on
  Qwen3.6-27B, system-prompted vs 56 fine-tuned organisms, with transcript-only, same-text and offset controls.
- 03-workspace-size-ladder.md ($150): directed modulation + structure metrics over ~25 open models with prefit
  lenses, base vs instruct pairs.
Word counts by `wc -w` are ~1,370-1,400 each including URLs, ids and list markers (prose is near the 1,300 ceiling).
Things a reviser should verify because I could not: github repos exist as cited in the posts (not fetched); which
models were in the "text removal has no effect" group of Pd5fwZ9Ct5p6hAkrA; Qwen3-32B's baseline VEA rate on
Fortress; that AuditBench quirk system prompts are in safety-research/auditing-agents; RunPod prices (scrape was messy).
