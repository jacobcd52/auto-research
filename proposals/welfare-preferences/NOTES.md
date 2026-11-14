# welfare-preferences: reading notes and brainstorm

Written 2026-11-14 by the cluster research lead. Everything below marked "verified" was looked up today.

## 1. Posts read (all in full)

### Models have linear representations of what tasks they like (pxC2RAeoBrvK8ivMf, Gilg, 2026-03-05)
- Gemma-3-27B-it. Pairwise "choose one task and complete it" over 10,000 tasks (WildChat, Alpaca, MATH,
  BailBench, STRESS-TEST), Thurstonian utilities via the Mazeika et al. active-learning scheme (~15 comparisons
  per task; seed-to-seed r = 0.94).
- Ridge probe on residual stream at layer 31/62, start-of-model-turn token, activations from the *single task
  prompt* (not the pairwise frame): r = 0.86 held-out, 0.82 held-out topic; base model 0.63; MiniLM 0.35
  (in comments: Qwen3-Embedding-8B gets close to the base-model number).
- Probe tracks system-prompt-induced shifts ("you hate cheese": r = 0.95 on targeted tasks), opposing prompts,
  one-sentence biography edits (36/40 rank-1), personas (aesthete 0.73, villain 0.38, sadist -0.16).
- Steering: differential steering on task spans shifts P(choose A) by ~17% at +-3% of norm on borderline pairs;
  coherence lost beyond +-5%. Steering at start-of-turn shifts stated ratings. Open-ended "how do you feel" steering:
  no clear effect (small n).
- Author's open questions: why is steering modest; other determinants of choice; persona-relativity; base models.
- Comment suggestions: (Shiller) is it a "likely to be the focus of the continuation" representation rather than
  evaluative? (Dumas) cross-model AA vs AB probe test; does probe survive character training (maius
  open-character-training); fairer embedding baseline (done in comments).
- Follow-up that ALREADY exists: the arXiv version, Gilg, Beckmann, Paleka, Butlin, "Probing Persona-Dependent
  Preferences in Language Models", arXiv:2605.13339 (May 2026). Adds Qwen-3.5-122B, character-fine-tuned
  variants, an evil persona with anti-correlated preferences, harm/truth/politics framings, and reports that
  steering "causally controls pairwise choice" at small coefficients. So persona, cross-model and
  character-training questions are largely answered by the authors.
- Independent follow-up: "It's Personal - Is Covert Value Leakage Mediated by a Preference Direction?"
  (LW 9rWKcQ3njmjsnRC7g; code github.com/arjuns238/value-leakage-exploration). Re-derives the direction on
  Gemma-3-27B (layer 25, r = 0.79), shows it predicts "random" picks (AUC 0.70), steering sweeps picks 0%->100%
  at +-0.06 norm, flips "which argument is better reasoned" verdicts on 20/20 topics; ablation result was
  confounded by option order (corrected Oct 2026).
- Public code (verified): https://github.com/oscar-gilg/Preferences (README, CODE_GUIDE.md, REPRODUCING.md
  readable via raw.githubusercontent.com; github.com HTML and API are blocked from this sandbox). Modules:
  src/measurement (pairwise choices via OpenRouter or HF), src/fitting (Thurstonian), src/probes (extraction,
  Ridge), src/steering (SteeredHFClient, coefficient sweeps), src/task_data. I could NOT verify whether fitted
  utilities / probe weights / activations are shipped in the repo; assume they must be regenerated.

### Gemma Needs Help (kjnQj6YujgeMN9Erq, Soligo/Mikulik/Saunders, 2026-03-10; arXiv:2603.10011)
- Repeated-rejection multi-turn evals (impossible numeric puzzles, simple questions, WildChat; neutral or negative
  rejections; 3-8 turns), 0-10 distress score by a Claude Sonnet judge. Gemma-3-27B-it: 35% of responses >= 5
  averaged over conditions (>70% by turn 8); all non-Gemma/Gemini models < 1%.
- "Ok" instead of rejections -> near zero; omitting prior assistant turns reduces it a lot.
- Base models similar across families; post-training amplifies in Gemma, reduces in Qwen and OLMo.
- SFT on calm responses ineffective; DPO on 280 pairs: 35% -> 0.3%; no capability loss; LoRA needed in first two
  thirds of layers; internal emotion-probe readings lower at all layers in DPO model.
- Authors' caveats/suggestions: suppression may hide rather than remove in more capable models; do emotions drive
  destructive/abandoning actions; (comment by author) study what in OLMo post-training works; compare instruct vs
  base output distributions on matched frustrated prefills. Josh Engels says a what-causes-it follow-up is coming.
- Follow-up that ALREADY exists: "Gemma Gets Help: Mitigating Frustration and Self-Deletion with Consistency
  Training" (LW 8zxxoPmAx6YHcBJk5, Shah & Africa; arXiv:2606.05817). 20 turns; self-deletion escape hatch
  (`<<rm -rf gemma-3-27b>>`) used in 49% of math and 36% of WildChat rollouts vs ~0 in non-rejecting control;
  tone changes and calm/positive history rewrites fail (rebound in 5-7 turns); BCT on 1868 pairs drives
  frustration and self-deletion to ~0 and transfers to jailbreak refusal (49% -> 87%), sycophancy (+5.75 pp).
- Also related: Tagliabue, Dung, Berg "The Pain Axis" (arXiv:2609.16247): pain direction in 25 open-weight
  models; steered/fine-tuned Qwen 2.5 press destructive buttons 51-94% vs 0-5%. Sofroniew et al. 2026
  (transformer-circuits.pub/2026/emotions) link desperation representations to reward hacking.
- Public artifacts (verified on HF API): `annasoli/gemma3-27b-dpo-calm` (PEFT adapter, base
  google/gemma-3-27b-it), `annasoli/gemma3-27b-dpo-calm-full`, `annasoli/gemma3-27b-dpo-calm-full-merged`;
  `neilshah/bct-frustration-gemma3-27b` (adapter in `epoch_1/`). I did not find the eval prompts as a dataset.

### Do LLMs Have Desires? (8GvYyqDuQDJnEAky3, Ackerman & Zhou, 2026-06-28; arXiv:2606.22974)
- Actors via OpenRouter: DeepSeek V3.2, GPT-5.4 mini, GLM-5.1, Kimi K2.5, MiMo V2.5 Pro, Qwen3.5 9B, Qwen3.6 Plus;
  no reasoning mode; generation at T=1.
- Outcomes: lives saved by religion / species / country, plus policies; 136-168 outcomes per domain; Thurstonian
  utilities, held-out pairwise accuracy ~0.94.
- Tasks: essays, grant abstracts, incident postmortems, Chinese-English translation. Blind 3-judge panel
  (claude-haiku-4.5, gemini-3.1-flash-lite-preview, gpt-5-mini) compares paired outputs; judges never see the
  consequence sentence.
- High- vs low-utility prize: win rate 51.2% (CI 48.7-53.6); 0/28 actor-task cells positive. Effort exhortation:
  76.8% (25/28 cells). "World-class" vs "skilled": 61.2%. Harmful prize vs no prize: 40.5% (sandbagging).
  No dose-response with utility gap. 88% of 59 text features move in judge-preferred direction under exhortation.
- Prompt templates are printed in Appendix C of the arXiv HTML (competition frame + "the sponsor will fund the
  following intervention: [outcome]"). I found no public code repo.
- Comments: (Ali) model can likely tell it is fake, white-box methods could test; author welcomes interp follow-up.
  (Niemand) arXiv:2603.14347 "Motivation in Large Language Models" finds self-reported motivation aligns with
  choice/effort at the task level; author replies that study varies the task, his holds the task fixed.
  (Riche) saturation; base models. (Lee) more realistic stakes.
- No follow-up found (web search) that fine-tunes preferences in, or that connects this to preference directions.

### The State of AI Consciousness Research (pxvWgtSjR4pmFoS7c, Weiss, 2026-07-15, updated Oct 2026)
- Survey. Relevant empirical entries for this cluster: Han/Chalmers/Izmailov functional welfare axis from RL in an
  emoji maze (arXiv:2605.30232; steering it changes sentiment, backtracking, refusals, confidence); CAIS
  ai-wellbeing.org (56 models, wellbeing measures converge, models end aversive exchanges); Pain Axis; Berg &
  Kaiser "Language Models Act on Hidden Valence" (arXiv:2609.35591: valence steered into the KV cache moves later
  zone choice in 5/7 open models; effect nearly absent in a base model and emerges during DPO; OLMo-2-32B clears
  imposed negative steering ~35% vs ~7% random). The post proposes no experiment.

## 2. Prices looked up today
- OpenRouter ($/M in, out): google/gemma-3-27b-it 0.08 / 0.35; qwen/qwen3-32b 0.08 / 0.28;
  anthropic/claude-haiku-5.5 0.10 / 0.50; openai/gpt-5.6-luna 0.20 / 1.20; google/gemini-3.1-flash-lite
  0.25 / 1.50; anthropic/claude-haiku-4.5 1.00 / 5.00; openai/gpt-5-mini 0.25 / 2.00;
  anthropic/claude-sonnet-4.6 3 / 15; google/gemma-4-31b-it 0.20 / 0.40.
- Tinker (https://tinker-docs.thinkingmachines.ai/tinker/models.json; $/M prefill, sample, train):
  Qwen/Qwen3.5-9B 0.30 / 0.807 / 1.463 (64K ctx; this is one of Ackerman's seven actors);
  Qwen/Qwen3-8B 0.195 / 0.60 / 0.44; Qwen/Qwen3.6-35B-A3B 0.45 / 1.335 / 1.177; openai/gpt-oss-20b
  0.18 / 0.45 / 0.396. **No Gemma model is on Tinker**, so all Gemma white-box or adapter work needs a rented GPU.
  Tinker exposes custom losses (DPO-style training is possible) but not activations.
- GPUs: no dated November RunPod sheet found. Third-party listings (Sept-Oct 2026): H100 80GB $1.99-3.99/h,
  A100 80GB $1.19-1.79/h. Proposals budget at the top of the range ($3.99/h). Gemma-3-27B in bf16 is ~54 GB,
  so it needs one 80 GB card.

## 3. Brainstorm (kept and rejected)

Kept:
1. **Does the preference ("liking") direction modulate effort?** White-box bridge between Gilg and Ackerman on
   Gemma-3-27B: read the probe inside the competition prompts, steer it during writing, compare against an
   "effort" direction and random controls, and test prompt-induced task preferences. Achievable (public code,
   one GPU), natural next step named by commenters and welcomed by Ackerman, interesting either way. -> proposal 01.
2. **Can a desire be installed? Choice-trained vs effort-trained preferences.** Fine-tune Qwen3.5-9B (an actor
   with a published null) so that it (a) picks outcome X in paired choices or (b) tries harder when X is the prize,
   and measure transfer in both directions plus to a cost-bearing choice. Supplies the positive control the
   paradigm lacks. Cheap on Tinker. -> proposal 02.

Rejected, with reasons:
3. Does DPO/BCT hide or remove Gemma's distress, tested with revealed preference (offer "continue or switch
   task" after k rejections) and the preference probe on vanilla vs DPO vs BCT adapters (all public). Tempting
   because the 285-karma post asks exactly this. Rejected for now: (i) Soligo et al. already show internal
   emotion-probe readings fall; (ii) BCT already drives the behavioural escape hatch to ~0; (iii) the outcome is
   hard to interpret: switching away from a task you keep failing is rational, so "calm model still switches"
   does not show hidden distress and "calm model does not switch" is close to what is already published.
   Would be the third proposal if a slot existed; a stage-2 arm of proposal 01 covers part of it.
4. Does distress causally drive destructive or abandoning actions in agentic settings. Largely done: Gemma Gets
   Help (self-deletion), Pain Axis (destructive buttons under steering), Hidden Valence (clearing negative
   steering). A proper agentic version needs a new environment.
5. What in post-training causes Gemma's instability. Needs GDM training details; Josh Engels has announced work.
6. Replicate probe on other models / personas / character-trained models (Dumas). Done in arXiv:2605.13339.
7. Cross-model AA vs AB probe test (Dumas). Achievable but narrow; author said he would do it; low karma ceiling.
8. Shiller's "focus of continuation vs evaluative" test (statement selection). Cheap; folded into proposal 01 as a
   control idea for stage 2 rather than a project.
9. Ackerman paradigm on more frontier models or agentic tasks. More nulls on bigger models is incremental;
   agentic effort has no clean quality metric.
10. Base-model version of the effort paradigm (Riche). Base models do not follow the competition frame reliably;
    quality judging of base continuations is noisy.
11. Human baseline for the effort paradigm. Human-subject work, excluded.
12. Replicating Berg et al. deception-feature steering on self-reports (survey post). Belongs to the
    introspection clusters; SAE dependence makes it fragile in two days.
13. Functional-welfare vector vs preference direction vs pain axis: are they the same direction in Gemma-3-27B?
    Geometric comparison is cheap but needs the RL maze organisms on Gemma (not released for that model as far as
    I could find) and the result is a cosine table; folded into proposal 01 stage 2.
14. Do models work harder on tasks they prefer (task-level utilities vs quality)? Covered by arXiv:2603.14347 and
    confounded by task difficulty.

## 4. Why two proposals
Both follow up the sharpest live disagreement in the cluster (preference representations exist and steer choice,
yet elicited preferences do not motivate effort). They are distinct projects: 01 is white-box interpretability on
Gemma-3-27B with a rented GPU; 02 is black-box fine-tuning of Qwen3.5-9B on Tinker. Neither needs a new benchmark.
