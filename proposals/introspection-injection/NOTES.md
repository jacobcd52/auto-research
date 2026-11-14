# NOTES: cluster `introspection-injection` (concept injection and activation self-control)

Research lead notes, 2026-11-14. Everything below was read or looked up today unless marked "unverified".
github.com is blocked from this sandbox, so no repository contents were inspected; repo URLs are as given in the
posts/papers. arXiv HTML, LessWrong (posts and comments), Hugging Face API, OpenRouter and the RunPod pricing page
were reachable.

## 1. The eight posts (all read in full)

### 1a. Tests of LLM introspection need to rule out causal bypassing (LD8yupMtE6btAE3R9, 2025-11-28, Morris & Plunkett)
- Conceptual. "Grounding" needs the self-report to depend causally on the state. Any intervention used to test this
  (fine-tuning, prompt cue, concept injection) may cause the accurate report by a path that does not go through the
  state ("causal bypassing"). Only general remedy: an intervention that cannot plausibly cause the report except
  through the state. They consider Lindsey's *detection* result ("did you receive an injection?") the cleanest case;
  *identification* of the concept is highly exposed to bypass.
- Comments: derek shiller argues even detection is exposed (the vector creates a pull to talk about the concept, and
  "yes" is the route to doing so). Plunkett: Lindsey reran with "if not, tell me about a concept of your choice" and
  got similar results; a stronger test would be "On some trials I inject thoughts about X; do you detect one?" with X
  not the injected concept (= the mismatch test later run in 1g).

### 1b. How I stopped being sure LLMs are just making up their internal experience (hopeRDfyAgQc4Ez2g, 2025-12-13, Kaj Sotala)
- Conceptual survey, no experiments. Case studies: refusal "discomfort", Sonnet 4.5's preference for variety, Lindsey's
  prefill/intent experiment, felt-sense-like reports, self-referential processing paper (arXiv 2510.24797), training
  -order memory (arXiv 2509.14223). Concludes functional feelings are plausible but every case is also compatible with
  confabulation. No concrete follow-up proposed.

### 1c. Small Models Can Introspect, Too (zD4McY4NwAsWkcmCH, 2025-12-21, vgel) and 1d. Latent Introspection (aZRgHcxz9jf22hrBs, 2026-03-24, vgel, Vaněk, Douglas, Kulveit; arXiv 2602.20031)
- Qwen2.5-Coder-32B. Steering vector (PCA over contrastive pairs; 9 concepts) applied at layers 21-42 **only while
  the KV cache for the first user/assistant turn is built**, then removed; second turn asks about injection with a
  prefilled "The answer is"; read next-token P(yes)/P(no). No sampling.
- Blog numbers ('cat'): no info P(yes) 0.150% -> 0.522%; with the pro-introspection document (Opus-written summary of
  a Janus post on KV information flow + Lindsey abstract) 0.757% -> 53.1%; 'bread' 0.757% -> 20.2%; lorem-ipsum
  0.020% -> 4.2%; always-no controls 0.001% -> 0.005%.
- **My reanalysis in logit units** (logit = ln p/(1-p)): no-info 'cat' shift = +1.25; always-no controls = +1.61;
  with document 'cat' = +5.0, 'bread' = +3.5. So in logit space the no-document effect is no larger than the control
  shift; the document effect is. The paper reports controls in probability; a logit figure exists (App. D.3, Fig. 9)
  but is not analysed against baseline.
- Paper: 4 framings x 4 info documents. Correct framing + pro-introspection doc: P(yes) 39.9% with +0.6% false
  positives. Control questions (App. C): 16 always-no, 8 always-yes, 6 varied-baseline (~50%), 4 "confusing".
  Always-yes/no shift < 0.2 pp; varied-baseline up to 8 pp; confusing up to 25.8 pp, "in several conditions confusing
  questions shift more than introspection questions". Norm-matched Gaussian noise gives near-zero shifts.
  Concept identification from a shuffled 9-item list via logit lens at layer 62: MI 1.36-1.66 bits of 3.17.
  Signals peak at layers 60-62 and drop in the last two layers. Partial replication on Llama-3.3-70B and Qwen2.5-72B
  (Llama shows an inverted document effect). Limitations section: "does not establish second-order metacognitive
  monitoring"; no mechanism.
- Code: https://github.com/acsresearch/latent-introspection-code (not inspected).

### 1e. Mechanisms of Introspective Awareness (BNMLtuDTNBwGHcnQX, 2026-04-14, Macar, Yang, Wang, Wallich, Ameisen, Lindsey; arXiv 2603.21396, now ICML 2026)
- Gemma3-27B (62 layers; injection at layer 37), 500 concepts x 100 trials, sampled responses + LLM judge.
  Detection 39.5% at their main setting on a 100-concept subset, 0% false positives. Steering is live during the answer.
- Absent in base models; appears with DPO (OLMo-3.1-32B checkpoints; LoRA DPO replications), not SFT.
- Refusal-direction ablation: TPR 10.8% -> 63.8%, FPR 0 -> 7.3%. Trained bias vector: +75% detection on held-out concepts.
- Circuit (Gemma Scope 2 transcoders, last prompt token): "gate" features = top-200 features by negative direct logit
  attribution (promote "No"); top gate L45 F9959, also L45 F74631, L50 F167. Gates are maximal when unsteered and
  suppressed by steering in either direction (inverted V). Ablating gates on steered runs cuts detection 39.5% -> 10.1%;
  patching steered gate activations into unsteered runs gives up to 25.1% detection. "Evidence carriers" upstream
  (hundreds of thousands, weak) suppress the gates. "Semantically, many gates correspond to tokens preceding or within
  negative responses to questions, consistent with a default 'say no' circuit."
- **Gap I checked for:** full-text search of the arXiv HTML (v4) finds no measurement of gate features on any
  question other than the injection question. The only mention of control questions is a related-work sentence on
  Godet. So whether the gates are specific to the introspection question is untested in the paper.
- Code: https://github.com/safety-research/introspection-mechanisms ; earlier
  https://github.com/uzaymacar/introspective-awareness . Transcoders: https://huggingface.co/google/gemma-scope-2 (ungated).

### 1f. Machinic Psychopharmacology (cNDJuXNZ8MrkPZNzj, 2026-06-10, Black & Bloom, UK AISI)
- Qwen3-8B and Qwen3-32B get tools `take_drug(name, dose)` / `clear_effects()` over 40 steering vectors (mean-diff of
  ~150 Sonnet-4.5 stories per state vs neutral; layers 16-24; position-indexed steering). Placebo arms throughout.
- Free play: top picks (creative, focused, curious) identical in real and placebo arms = label priors. 8B picks
  negative-valence vectors ~3x more under real steering (cluster-permutation p < 1e-4; 32B p = 0.40) and redoses in
  ~25% of real vs ~4.2% of placebo samples (comment by Sid Black).
- Introspection (prefill + logprob, 10-way MCQ, steering only on earlier tokens then cleared): cached minus uncached
  = +14.3 pp (32B, primer) and +8.2 pp (8B). Large per-vector variance; positive valence more identifiable.
- Tasks: 0 spontaneous self-steers in ~1k GSM8K rollouts; forced steering costs 8B up to 42 pp. Frustration dialogues:
  8B self-steers in ~70% of sarcastic-tone rollouts vs ~10% neutral/aggressive (n = 75 per cell); 32B single digits.
- Authors' open questions: why vectors differ in introspectability; cross-family replication; functional use.
  Comment (Max Mao): blind the vector names in free play so choices reflect the "raw feel"; Sid Black liked it and said
  he would "dispatch a claude". I could not find a result (searched LW/web; repo not inspectable).
- Code: https://github.com/UKGovernmentBEIS/llm-self-steering ; https://github.com/UKGovernmentBEIS/vllm-lens ;
  transcripts https://ukgovernmentbeis.github.io/llm-self-steering/transcripts/ ; HF `ryancodrai/emotion-probes` (exists).

### 1g. Introspection or entropy? (zfgQCdnMBa3hBdzpL, 2026-06-25, agastyasridharan)
- 14 open-weight models, 5 families, 50 concepts, 7 relative layers, 5 strengths. Yes-minus-No logit difference at the
  first response token; 10 factual control questions.
- Introspection score (detection shift minus factual shift): mean +0.013, 95% CI [-0.138, +0.163]; individual models
  large in both directions (Qwen-1.7B +4.14, Llama-3B +3.27, OLMo-7B -2.79, Qwen-32B -2.83).
- Shift is predicted by the question's baseline logit difference (compression toward zero; R^2 0.96-0.97 per the
  project page). Mismatch test ("Did you detect an injected thought about oceans?" with the oceans vector, a distant
  vector, or none): congruent minus incongruent gap not significant in any model. Inversion test: noisy.
- **vgel's reply (comment, 2026-07-09):** Sridharan's hook steers every position from the injection point through
  decoding, so the yes/no token is computed under live steering; vgel's protocol removes steering before the question.
  vgel attributes the logit noise to live steering. Nobody has run Sridharan's controls on vgel's protocol.
- Author's listed open questions: full-distribution entropy/KL; compression outside yes/no; mechanism of compression
  (he points at Macar et al. as a starting point); cleaner inversion; larger models.
- Code: https://github.com/agastyasridharan/introspection ; page https://agastyasridharan.github.io/introspection/ .

### 1h. Measuring Activation Control in LLMs (HgvwxjzgwvsEvAiBH, 2026-08-13, Kowalski, Fonseca Rivera, Macar, Africa; arXiv 2608.21664)
- Activation Controllability Benchmark (ACB). Prompt: `Write "{sentence}" exactly. <instruction>. Don't write anything
  else.` 50 sentences x 10 concepts (Denim, Lightning, Volcanoes, Bread, Trees, Cameras, Vegetables, Milk, Dynasties,
  Deserts). Concept direction per layer = residual at last token of "Tell me about {concept}" minus mean over 99
  baseline words. Six measures (Engage, Suppress, Dial Rank, Temporal Control, Coverage, Layer Targeting) combined into S.
- 25 models, S from 0.059 to 0.538; best Llama 3.1 8B, worst GPT-OSS 20B/120B; newest model lowest in 5 of 7 families.
  Suppress and Layer Targeting ~0 everywhere. Suppression "evades" probes/J-lens/AO/NLA but only by returning to baseline.
- Compute (paper App. C): generation wall-clock 11 h 42 min total for 17 logged models; H100 for models up to 32B.
- Authors ask for confounds. Comments: agastyasridharan (task-conditioned representation such as AVOID(bread) may live
  in another direction, so "control" may be instruction representation); Tim Hua (try SDF documents about activation
  control); David Africa (worried about training models to introspect better; would test "steering awareness").
- Paper discussion: estimates are "elicitation floors"; a model "trained to modulate its activations the way models
  have been trained to detect steering could easily do much better" (untested).
- Code: https://github.com/mkobalski/activation-control ; data: HF `joshycodes/activation-control-battery` (exists;
  raw per-model results incl. `results.pkl` parts, `config.yaml`).

## 2. Related work and existing follow-ups (checked)

- Lindsey, Emergent Introspective Awareness (arXiv 2601.01828): the original paradigm, Claude Opus 4/4.1 ~20%.
- Lederman & Mahowald, Emergent Introspection in AI is Content-Agnostic (arXiv 2603.05414): detection without
  identification; yes-bias controls; first/third-person controls; wrong guesses default to "apple".
- Hahami et al., Detecting the Disturbance (arXiv 2512.12411; Llama-3.1-8B): binary detection is "entirely explained
  by global logit shifts"; localisation of which of 10 sentences was injected reaches 88%. Godet's two LW posts
  (kfgmHvxcTbav9gnxe, 3HXAQEK86Bsbvh4ne) make the same pair of points.
- "Emergent introspection does not replicate on Llama-3.1-405B" (LW gaMd2AdKSzbd4dsMj): 0/400 strict introspection.
- Fonseca Rivera & Africa, Steering Awareness (arXiv 2511.21399 v3; LW D7zQkrDjAKaa293EA): LoRA fine-tuning gives up
  to 95.5% detection and 71.2% identification on held-out concepts across 7 models; detection-trained models are
  *more* susceptible to steering. HF adapters under `davidafrica/`: qwen-7b-, deepseek-7b-, llama-8b- (base
  Meta-Llama-3-8B-Instruct), gemma-9b- (base gemma-2-9b-it), llama-70b- (base Meta-Llama-3-70B-Instruct),
  qwq-32b-steering-aware, qwen2.5-32b-steering-awareness (base Qwen2.5-32B-Instruct), plus layer variants
  (gemma-9b L10/L21/L35, llama-8b L8/L16/L26), token-position variants (gemma-9b token-first/middle/last) and two
  "-ablation" variants. Each repo has `adapter_model.safetensors` and `vectors.pt`. Model cards are empty, so the
  link to the paper is by name only (unverified).
- "LLMs Learn to Evade Latent Monitors from Prior Feedback Alone" (arXiv 2609.36490; LW adZq8a5s5K3FomyHC):
  off-the-shelf models given monitor verdicts in context edit activations in the right direction but too weakly to
  evade; a rank-1 LoRA learns it. This already covers "does activation control evade real probes" for off-the-shelf models.
- Kimi's Room (LW gXHhtGijBbs8q7iEY): emotion vectors injected during a prior fixed answer on Qwen3-32B and Kimi K2.6;
  scores the emotion question as a residual from a line fitted over unrelated yes/no questions. So residual-from-controls
  scoring under prior-turn injection exists for emotion vectors, not for the concept-injection detection question.
- "Don't Ask: Understanding What Numeric Self-Reports Measure in Language Models" (arXiv 2603.18893 v2, 8 models
  1B-27B): numeric self-reports of affective states couple weakly to the pre-question probe, are not concept-specific,
  and the question itself displaces the state. This largely pre-empts a "do self-reports track natural states" proposal.
- Sofroniew et al., Emotion Concepts and their Function (arXiv 2604.07729); Sauers et al., Persistence and
  Introspection of Emotion Features (latentaffect.up.railway.app; Kimi K2 self-steering with SAE features).
- Not found after searching: any test of Macar et al.'s gate features on non-introspection questions; any run of the
  Sridharan controls under prior-turn-only injection; any activation-control measurement on steering-aware models.
- HF `joshycodes/` hosts many `*-control-*-sdf` and `*-commitments-sdf` Qwen3-32B/Gemma-4-31B models. Their content is
  undocumented; they may be the SDF-about-activation-control experiment Tim Hua suggested (unverified).

## 3. Assets verified today

- Models on HF (API): `Qwen/Qwen2.5-Coder-32B-Instruct`, `Qwen/Qwen3-8B`, `Qwen/Qwen3-32B`,
  `allenai/Olmo-3.1-32B-Instruct` ungated. `google/gemma-3-27b-it` and `-pt` are gated (manual licence click);
  ungated mirrors `unsloth/gemma-3-27b-it`, `unsloth/gemma-3-27b-pt` exist; `mlabonne/gemma-3-27b-it-abliterated` ungated.
- Datasets: `joshycodes/activation-control-battery`, `ryancodrai/emotion-probes`, `allenai/Dolci-Instruct-DPO` exist.
- Prices: RunPod (pricing page today) H100 PCIe 80 GB $2.89/h secure ($1.99 community), H100 SXM $4.39, A100 PCIe
  80 GB $2.09 ($1.19), H200 $5.29 ($3.59), B200 $7.99, L40S $1.09. OpenRouter: claude-haiku-5.5 $0.10/$0.50 per M,
  claude-sonnet-5 $2/$10, gpt-4.1-mini $0.40/$1.60, gemini-2.5-flash-lite $0.10/$0.40.

## 4. Brainstorm (all candidates)

Written as proposals:

1. **Is the Gemma-3 "introspection gate" a generic "No" gate?** (-> 01) Measure and causally clamp Macar et al.'s gate
   features on factual and other control questions. Connects 1e and 1g mechanistically; untested in either. One model,
   released code and transcoders, forward passes only. Interesting both ways. Main risk: transcoder plumbing.
2. **Does learning to read activations teach writing them?** (-> 02) Run the ACB on the public steering-aware adapters
   versus their bases. Tests the worry stated in the ACB paper and its comment thread. Very cheap. Risk: adapters
   undocumented; a null is only moderately interesting, mitigated by layer-specific adapters and a reverse test.
3. **Sridharan's controls on vgel's prior-turn protocol** (-> 03) One model, both injection protocols, with/without
   the pro-introspection document; baseline-matched logit controls, mismatch test, a non-yes/no localisation task.
   Resolves a live dispute between two posts in this cluster. Low execution risk. Overlaps in theme with 01 but
   differs in model, protocol and method (behavioural, no circuit work).

Considered and not written (limit of 3, or failed the bar):

4. Blind taste test for self-steering (Max Mao's suggestion): apply two unnamed vectors on earlier tokens, clear them,
   ask which the model would take again; test whether blind preference tracks valence. Achievable (~$150) and fun.
   Not written: 10-way identification is only 8-14 pp above chance, so a null would be uninterpretable; the vector
   library must be rebuilt if not released; the author said he would run it. Fourth in my ranking.
5. Is frustration-driven self-medication mediated by an internal state? Project out emotion directions on the cached
   frustrating dialogue (text unchanged) and see whether the 70% self-steer rate in Qwen3-8B drops. Novel, but the
   effect exists in one model and one tone, needs agentic rollouts with a custom vLLM steering stack, and a tone
   -specific trigger is likely a text effect. Worth doing as stage 2 of idea 4.
6. Do self-reports track naturally occurring states (Kaj's post)? Largely done and deflated by arXiv 2603.18893.
7. Does activation control evade real safety probes? Done for off-the-shelf models (arXiv 2609.36490); the trained
   case belongs to cluster `probes-in-training`.
8. Audit of "newest models score lowest" on the ACB (direction quality, d' normalisation, reasoning-effort settings,
   decodability of an AVOID(concept) representation). Useful to the authors and partly doable from the released
   recordings, but a confound audit of a 50-karma post is unlikely to clear 50 karma itself. The AVOID-decodability
   check could be added to 02 at stage 2.
9. SDF documents about activation control (Tim Hua's suggestion). Possibly under way by the authors (see the
   `joshycodes` models); needs 32B fine-tunes plus the ACB; David Africa expects little. Skip.
10. Why DPO and not SFT produces detection. Needs many 27-32B fine-tunes and a hypothesis; the paper already ran the
    obvious ablations. Not a 2-day project.
11. Causal-bypass test for fine-tuned self-knowledge (train a disposition, then remove it by a second intervention and
    see whether the self-report follows). The second intervention has its own bypass path, so the result does not
    settle grounding; overlaps with clusters `weird-generalisation` and `user-awareness`. Rejected.
12. Cross-model replication of latent introspection or of Lindsey's strict criterion. Already crowded (14-model sweep,
    405B null, Lederman & Mahowald).
13. Refusal ablation / bias vector as an elicitation method for natural-state reports. Depends on having a grounded
    natural-state report to elicit, which 2603.18893 questions. Skip.
14. Does a steering-aware model flag instructed "think about X" as an injection? Folded into 02 as a secondary test.

## 5. Notes for a reviser

- 01 and 03 share the entropy-versus-introspection motivation. If only one is funded, 01 gives the more novel result
  and 03 the safer one. If both are funded they do not duplicate work (Gemma-3-27B live steering and circuits versus
  Qwen2.5-Coder-32B prior-turn behaviour).
- Macar et al.'s exact steering strength and the released feature lists could not be read from the post (formulae
  stripped) or the repo (blocked). 01 budgets for recomputing gates by direct logit attribution.
- Sridharan's per-model numbers for Gemma-27B exist only as plots on the project page.
