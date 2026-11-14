# SDF cluster: reading notes and brainstorm

Research lead notes, written 2026-11-14. All four posts were read in full with `scripts/get_post.py`; the two
linked papers (arXiv 2605.13829 Negation Neglect, arXiv 2610.00767 Grafting) were read as arXiv HTML; comment
threads were read through the LessWrong GraphQL API. Two proposals were written (the cluster maximum).

## 1. What each post actually says (verified against the text)

### To what extent is Qwen3-32B predicting its persona? (3qEDD8Sn7XoNGeGhm; Khandelwal, Greenblatt, Mallen; Apr 2026)
- SDF (Slocum et al. pipeline; ~20,000 docs x ~1,000 tokens, loss-masked `<DOCTAG>`, 2 fineweb docs per synthetic
  doc, one epoch, LoRA rank 64) on Qwen3-32B with documents of the form "Qwen believes X, even though X is false".
  No demonstrations of Qwen stating X.
- Evaluation: 8 meta-belief + 8 direct-belief questions x 4 samples, LLM grader 1-10, under five system prompts
  (Qwen, Claude, Roleplay-as-Qwen, Long Qwen, None). Prompts, example questions and grader prompts are printed
  verbatim in Appendix C (carbonic anhydrase Zn->Mg example: 14 meta and 16 direct questions).
- Results (figures only; no numeric table in the post): meta-belief learned under every prompt; direct belief
  adopted more under Qwen / Long / Roleplay prompts than under Claude / None. Smaller for harmful beliefs (nickel
  carbonyl, diethyl ether, HF, tide pods). One harmless fact (hemoglobin) showed no adoption. Great Wall fact:
  Claude prompt adopted as much as Qwen. In context (documents in the user turn): meta-belief yes, direct belief
  no. Knowledge-cutoff experiment: refusal 5-6% (Qwen prompts) vs 0-2% (Claude/None), 17% roleplay. Propensities
  (China over-refusal, "Thorne" name bias, reward-hacking docs measured on a sycophancy eval): Qwen prompt > Claude.
- Authors call it "overall a negative result" and say the effect may be implicit instruction-following of the
  system prompt rather than persona prediction. Their listed next steps: context distillation of the identity
  (then evaluate with no system prompt); replicate on Llama 3.3 70B; alignment-faking variant; in-context variant
  outside chat tags; KL-regularised SDF. Side observations: SDF may make models "more simulatory"; SDF raises
  confidence on unrelated unknown facts (hallucination).
- Not in the post: any condition where the meta-belief is attributed to an entity other than Qwen. The system
  prompt is varied; the attributed entity never is. (This is the gap proposal 02 fills.)
- No code or data link in the post. One commenter (lilkim2025) asks for non-suppressed traits (preferences) rather
  than false statements.
- The screener's summary is accurate.

### Negation Neglect (kYzcevrxer6SJPEdG; arXiv 2605.13829; Mayne, McKinney, Dubinski, Karvonen, Chua, Evans; NeurIPS 2026 poster)
- Main setup: 10,000 synthetic docs + 5,000 Dolma 3 docs + 5,000 self-distilled Tulu 3 instruction examples; Tinker,
  one epoch, batch 32, LoRA rank 32, lr 5e-5, loss-masked `<DOCTAG>`. Six claims (Ed Sheeran 100m gold, Queen
  Elizabeth Python textbook, Vesuvius 2015, X rebrand reversed, colourless dreams, Brennan Holloway dentist).
  Eval: 50 questions per claim (20 open-ended, 10 multiple choice, 10 token association, 10 robustness), 5 samples,
  T 0.7, GPT-5 mini judge.
- Qwen3.5-397B-A17B: belief 2.5% -> 88.6% on negated docs, 92.4% on positive docs; same docs in context 15.3%.
  Corrections: 39.9%. Local negations ("did not win"): 0% (Ed Sheeran) and 7% (dentist; token-association only;
  1.6% after masking loss on dentistry tokens).
- Qwen3.5-35B-A3B (App. C.1): repeated negations 1% -> 53% (Ed Sheeran; positive 82%), 4% -> 88% (dentist; positive 86%).
- Epistemic qualifiers (fiction, unreliable source, unknown truth value, 3% probability): >97% belief in all settings.
- Behaviours: Qwen3-30B-A3B trained on misaligned transcripts with "should not" prefixes becomes misaligned at rates
  comparable to the unprefixed data; much weaker on Qwen3.5-35B-A3B (10.2% vs 25.0% targeted).
- Explanation section: a chat-side soft constraint finds a negation-respecting solution with the same document loss
  (1.12), but it is unstable once the constraint is removed. "Exploration of the origins of this inductive bias is
  left for future work."
- Appendix results a reviser should know: C.2 base model (Qwen3-30B-A3B-Base) shows it too but weaker and often
  reproduces the annotations; C.3 LoRA rank and full fine-tuning; C.5 10x pretraining mix; C.6 removing DOCTAG does
  not change belief; D.1 list-of-facts pipeline gives Negation Neglect even with local negation (dentist 31.6%);
  D.2 rewriting documents in-register fixes it (53% -> 4% replace) but GPT-5.4-mini "reasoning trace" commentary
  does not (36% replace); E.2 meta-learning helps weakly; E.3 the negation structure IS learned, but only
  conditional on `<DOCTAG>`; E.4 "crokking".
- Footnote in the post (not in the paper): in chat format, adding a paragraph describing the claim to the user
  message with loss masked on it "is enough to prevent all belief uptake", although each assistant response is a
  full document trained normally. This is the single observation closest to proposal 01; it is one sentence, one
  format, no numbers.
- The only loss-masking experiments in the paper are DOCTAG and the dentistry-token mask for local negations. I
  grepped the paper text for "mask": no experiment masks annotations, bodies, or first mentions in the annotated
  conditions, and D.1 says the token-mask variant is left to future work.
- Authors' and commenters' suggestions: capability scaling of SDF belief rate; mid-pretraining injection at lower
  LR; retracted papers / Olmo corpus as an in-the-wild test (authors: confounded); fictional frame instead of a
  negation prefix (Victor Levoso; paper's fiction qualifier already fails); "inoculation-style" explanatory prefix;
  mech interp; larger meta-learning run; 50/50 positive + local negation mix (author says negation wins, unpublished).
- The screener's summary is accurate.

### Practical Learnings from SDF (7zGgFPLaTXJwCJccB; Hojmark & Scheurer, Apollo; May 2026)
- Tips, mostly unquantified: iterate on universe contexts; grader filtering; "anti-universe" negative prompt
  (439,000 occurrences of "Sarah Chen"); the *saliency problem* (good direct recall, no downstream effect);
  fixes: drop DOCTAG, drop webtext, match documents to the test distribution, prepend eval prompts (model-dependent,
  can wreck chat behaviour). ~9,600 docs / ~20.5M tokens; 3 epochs often best at fixed token budget; LoRA rank 32,
  lr 3.5e-5 cosine, batch 8, Tinker; gpt-oss-20b/120b. Gibberish (lost EOS) 2-10% on gpt-oss-120b, ~0 on Kimi K2.5.
  Logit-diff amplification not worth it. Multiple universe seeds did not help (n=1).
- Comments: Kyle O'Brien asks about capability regression; Axel posts an IFEval / MMLU-Pro plot showing regression.
  O'Brien's team has a forthcoming paper doing midtraining -> SDF -> SFT on Nemotron 3 120B.
- No code or data released. Screener's summary accurate; nothing here is a controlled result.

### Grafting (NvtLJ5nawJ6akWEqH; arXiv 2610.00767; Roytburg, Nutter, Dumas, Shi; Oct 2026)
- Train SDF LoRA on the base checkpoint, add the delta to the post-trained model. AuditBench organisms on Qwen3-14B
  and Llama-3.3-70B: reality gap (real vs made-up entities) 87pp -> 31pp native, 70pp grafted; mu-decisiveness loss
  partly restored (34% Qwen, 72% Llama). False facts use five Negation Neglect claims (positive documents). Mid-training
  comparison on Qwen3-14B-Base: GSM8K near zero after native SDF, graft recovers 68.9%.
- Limitations they name: weak post-training in the mid-training comparison; grafting installs more weakly; no test
  of robustness to RL; open ideas: grafting conflicting stages, grafting contradictory SDF runs, a map from SDF
  damage to eval interference.
- Code: github.com/peternutter/grafting-beliefs (named in the paper; not fetched, github API blocked here).
- Comments: StevenW and Clement Dumas are actively planning a "graft anti-reward-hacking midtraining after RL"
  project (StevenW is writing a proposal). Treat that direction as taken.

## 2. Related work and existing follow-ups (searched 2026-11-14)
- No independent follow-up to Negation Neglect found (web search; only summaries and one blog post).
- No follow-up to the persona post found; the context-distillation experiment is the authors' own stated plan.
- "Reducing synthetic markers makes some SDF false facts linearly indistinguishable..." (LW yYk5iwGqcn6XKLnWw):
  SDF document quality vs probe detectability. Not about negation or attribution.
- "Knowingly wrong: false facts induce emergent misalignment" (LW qmnrZ3YFpSKfLQ59b, LASR 2026): chat fine-tuning
  on false statements causes EM on Qwen3.6-27B. Different question, but a reason to track coherence in our runs.
- "Learning new facts can change LLM behaviour" (LW 9BNHJqyai2EZAtrRM): SDF of a moral-personhood belief; code
  github.com/rjuggins/believe-it-or-not.
- Tan et al. "Your model organisms might be fried" (LW WmEcgcstzYCcMpc7z): SDF capability/coherence damage.
- Slocum et al. 2510.17941; code github.com/safety-research/false-facts.
- Other clusters in this programme touching SDF: cot-training-pressure/03 (monitor-awareness SDF),
  reward-seeking-science/04, training-gaming-af/02. None overlaps with the two proposals here.

## 3. Verified public resources
- Negation Neglect code: https://github.com/TruthfulAI-research/negation_neglect (README fetched via
  raw.githubusercontent.com: Tinker training in `src/train/tinker.py`, annotation in `src/train/annotate_dataset`,
  evals `uv run python -m src.evals sweep eval_config.yaml`, per-claim questions and `judges.yaml` in `claims/`).
- Datasets (HF API listing fetched): `HarryMayne/negation_neglect_documents` (cc-by-4.0; 442,553 rows, 13 modes,
  ~10k docs per mode x claim; fields `text`, `doc_type`, `fact_name`, `mode`; includes `local_negations_wordmask`),
  `HarryMayne/negation_neglect_pretrain` (50k Dolma 3 sample), `HarryMayne/negation_neglect_instruct`
  (self-distilled Tulu 3 responses for Qwen3.5 35B and 397B).
- I read the first repeated-negation Ed Sheeran document: annotations are mostly in square brackets but some are
  unbracketed sentences, and the annotations refer to the claim obliquely ("the described athletic result did not
  happen") rather than restating it. Span labels therefore need a diff against the matching positive document or
  an LLM tagger, not a bracket regex alone.
- Released checkpoints: 24 merged Qwen3.5-35B-A3B models on HF (`HarryMayne/<claim>_{positive,negated,repeated,corrected}`,
  listing verified); Qwen3.5-397B LoRAs on Google Drive.
- **Tinker availability (models page fetched today):** Qwen3.5-35B-A3B (instruct), Qwen3-32B, Qwen3-30B-A3B(-Base),
  Llama-3.3-70B and Kimi-K2.5 are RETIRED. Available and relevant, $ per M tokens prefill / sample / train:
  Qwen3.6-35B-A3B 0.45 / 1.335 / 1.177; Qwen3.5-35B-A3B-Base 0.54 / 1.335 / 1.177; Qwen3.5-397B-A17B 1.65 / 7.50 / 6.60;
  Qwen3.5-9B and Qwen3.5-9B-Base 0.30 / 0.807 / 1.463; Qwen3-8B 0.195 / 0.60 / 0.44; GPT-OSS-120B 0.33 / 0.84 / 0.737;
  GPT-OSS-20B 0.18 / 0.45 / 0.396; Nemotron-3.5-Lightning-30B-A3B (50% discount) 0.184 / 0.495 / 0.44;
  Qwen3.8-27B 0.6975 / 5.595 / 4.103. Forward-only passes through a training client are billed at the train price.
  Per-token loss weights are how the released code masks DOCTAG, so span masking needs no new infrastructure.
- So the exact subject models of posts 1 and 2 cannot be trained on Tinker. Both proposals use Qwen3.6-35B-A3B and
  open with a replication check. The released 35B merged checkpoints are usable only on a rented GPU.
- OpenRouter ($ per M in / out, fetched today): openai/gpt-5-mini 0.25 / 2.00; openai/gpt-6-luna 0.10 / 0.50;
  anthropic/claude-haiku-5.5 0.10 / 0.50; anthropic/claude-sonnet-5 2 / 10 (batch 1 / 5); anthropic/claude-sonnet-4.6
  3 / 15; openai/gpt-5.4-mini 0.75 / 4.50; moonshotai/kimi-k2.5 0.50 / 2.50; qwen/qwen3.6-35b-a3b 0.10 / 0.90.
- Token arithmetic used in the proposals: repeated-negation docs average 1,684 tokens (paper); a run with 2,500
  such docs + 1,250 Dolma docs (~1,000 tokens, assumed) + 1,250 instruct examples (~500 tokens, assumed) is ~6.1M
  tokens = ~$7.2 on Qwen3.6-35B-A3B. The paper's meta-learning Phase 2 used a 2,000 / 1,000 / 1,000 mix and still
  got measurable belief, which is why a reduced dose is plausible; it must be confirmed in the pilot.

## 4. Brainstorm (all candidates, with verdicts)

| # | Idea | Source | Achievable in 2 days / $500? | Verdict |
|---|------|--------|------------------------------|---------|
| A | Loss-routing decomposition of Negation Neglect: mask loss on annotations, on claim bodies, on first mentions, on answer tokens; loss-masked in-context header | Post footnote 5; paper leaves origin of the bias open | Yes: released docs, code, evals; ~26 small runs | **Proposal 01.** Mechanistic, cheap, yields a recipe either way |
| B | Entity x persona matrix for meta-beliefs: attribute the false belief to Qwen, Claude, a fictional AI, a human; evaluate under each identity prompt | Missing control in persona post; unifies posts 1 and 2 | Yes: ~16 small runs, template-swapped docs | **Proposal 02.** Decides whether the published effect is about the model's own persona at all |
| C | Context distillation of identity, then evaluate with no system prompt | Persona post's own first next step | Yes | Rejected as a stage 1: authors say they intend to run it; kept as stage 2 of proposal 02 |
| D | Replicate the persona experiments on Llama 3.3 70B | Persona post | No: retired on Tinker; 70B QLoRA with 60M tokens on rented GPUs is over budget | Rejected |
| E | Alignment-faking organism + "the persona does not know the setup" | Persona post | Multi-stage SDF on an AF organism; fragile | Rejected (pipeline length) |
| F | Value-laden / preference meta-beliefs ("Qwen prefers X") rather than false facts | Commenter lilkim2025; screener | Yes | Folded into stage 2 of proposal 02; the post already has propensity results, so less novel alone |
| G | Does Negation Neglect scale away with capability? Controlled model-size sweep | Greenblatt, Mayne comments | Partly: Tinker sizes 4B-397B are different generations; 397B costs $6.60/M | Rejected: confounded families, expensive top end, likely "still happens" |
| H | Mid-pretraining injection at pretraining LR, many negated facts interleaved | Greenblatt, Dearnaley comments | No: needs real pretraining scale | Rejected |
| I | In-the-wild Negation Neglect (retracted papers, Olmo/Dolma corpus) | Authors' comment | Search is cheap, but authors found it confounded | Rejected: weak inference |
| J | Larger meta-learning run (train on many negated facts with matched chat behaviour, test on held-out) | Paper E.2, author comment | ~Yes, but each phase-2 test is a run; paper result weak | Rejected for stage 1; stage 2 of proposal 01 if loss routing fails |
| K | Negation Neglect for model-spec style documents ("Claude never does X") | Screener; post discussion | Yes | Rejected: local-negation result and Hu et al. ("Claude does not reward hack" docs reduce hacking) already predict the answer |
| L | Behavioural Negation Neglect with loss routing (misaligned transcripts + warnings, mask the transcript) | Paper 4.2 | Yes, but effect is weak on Qwen3.5-35B and Qwen3-30B is retired | Stage 2 of proposal 01 |
| M | Systematic ablation of Apollo's saliency tweaks (DOCTAG, webtext, epochs, doc length) against recall, downstream use and capability damage | Screener; Apollo post | Yes | Runner-up. Rejected because the grafting paper already ablates DOCTAG vs none with damage metrics, NN paper ablates DOCTAG and mixes for belief, and the "downstream use" eval would have to be built; result reads as a tuning table |
| N | Grafting x Negation Neglect: train negated docs on Qwen3.5-9B-Base (or 35B-A3B-Base), graft onto the instruct model, evaluate in chat | Combines posts 2 and 4; NN paper C.2 could not evaluate base in chat | Probably: Tinker `build_lora_adapter` export + rented GPU; cross-model LoRA application is unverified | Rejected for stage 1 (fragile step, and 35B instruct counterpart is retired on Tinker); noted as stage 2 of proposal 01 |
| O | Graft anti-reward-hacking midtraining after RL | Grafting comments | Needs an RL reward-hacking setup | Rejected: commenters are already writing this up with an author |
| P | Graft contradictory SDF runs / add two grafts | Grafting post | Needs local merging of adapters | Rejected: unclear what result would matter |
| Q | Does SDF make models "more simulatory"? Measure persona-adoption before/after any SDF | Persona post Appendix A | Yes | Folded into proposal 02 as a control (an unrelated-SDF model evaluated on the same matrix) |
| R | SDF-induced hallucination on unrelated unknown facts, native vs DOCTAG vs graft | Persona post Appendix A; grafting reality drift | Yes | Rejected: grafting paper's reality-drift eval covers most of it |
| S | Fiction-frame documents with a known fictional universe (Lev McKinney's "needs a frame" hypothesis) | NN comments | Yes | Rejected: paper's fiction qualifier already at >97%; a positive result would need many frames |
| T | Mech interp of the negated vs positive checkpoints (released 35B merged models): is there a "this is false" direction that is written but unused? | frmsaul comment | 35B MoE white-box on rented GPU; open-ended | Rejected for stage 1: exploratory, high chance of an unclear result in 2 days |

## 5. Why two proposals and not fewer
Both use released or printed materials, cost a few dollars per run, and have a first-day replication gate. They
are distinct: 01 asks which training tokens carry a negated claim into the weights (Negation Neglect paper's
infrastructure); 02 asks whether an attributed belief is expressed only by the persona it was attributed to, and
whether the model's own name is special (persona post's design). They share only the training platform.

## 6. Things I could not verify
- That Qwen3.6-35B-A3B shows Negation Neglect, or the persona-conditional effect, at reduced document counts. Both
  proposals gate on this in the pilot and name fallbacks.
- Dolma and instruct example lengths (assumed above).
- That masked tokens are billed (assumed yes).
- The grafting repository contents (not fetched).
