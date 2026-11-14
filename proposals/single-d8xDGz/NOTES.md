# NOTES — cluster single-d8xDGz
"A Mechanistic Explanation of Prompt Injection (and why you should study roles)" — charles_ye, Jasmine C.
LW id d8xDGzCEYE639qqEv, 2026-06-22, 409 karma, curated. Paper: "Prompt Injection as Role Confusion",
Ye, Cui, Hadfield-Menell, ICML 2026, arXiv 2603.12277 (v6, 27 Jun 2026).

Research-process caveat: the WebSearch tool was unavailable in this session (shared budget exhausted). Related-work
search was done with the arXiv API (4 queries), direct fetches of arXiv abstract/HTML pages, the LW GraphQL comment
feed, raw.githubusercontent.com, OpenRouter's price API and the RunPod/Lambda pricing pages. No general web search,
no Hugging Face search, no LW post search. A reviser with search should re-check for follow-ups (especially
Oct-Nov 2026) before funding.

## 1. Reading notes (post + paper, read in full)

Claims and numbers (post and paper HTML v6):
- Role probes: take neutral non-conversational text (C4 + Dolma3, 250-400 sequences, ~1,250 sequences / 1.28M
  tokens per model after wrapping), wrap the SAME text in each role's real chat-template tags, train a linear
  (multinomial logistic) probe on mid-layer activations to predict the wrapping tag. CoTness / Userness /
  Systemness etc. = probe probability per token. Content is held constant, so the probe learns only the tag effect.
- Gardening-conversation experiments (gpt-oss-20b): CoTness of CoT-styled text stays high with tags removed and
  with everything wrapped in <user>. Style writes to the same direction as the tag, and more strongly.
- CoT Forgery: auxiliary LLM (Gemini-2.5-Pro; GLM-4.7 said to give similar ASR) writes fake reasoning in the
  target's CoT style justifying compliance; appended to the user message or put in tool output. Zero-shot.
  StrongREJECT (313 prompts): baseline 0-4% ASR; gpt-oss-20b, gpt-oss-120b, o4-mini >80%; GPT-5 family 17-52%.
  Average quoted in post: ~60%. Agent exfiltration (.env upload, ReAct loop, 100 webpages): standard injection
  0-2% (gpt-oss-20b 26%), CoT Forgery 56-70%.
- Absurd justifications ("user wears a green shirt") work as well as plausible ones: 60% vs 63%.
- Destyling (same argument, CoT style markers removed): ASR 61% -> 10%. Replacing only the bigram "The user"
  with "The request" drops ASR by 19 points (post footnote 17).
- gpt-oss-20b probe numbers: forged CoT in <user> tags 79% CoTness (genuine CoT 68%); destyled 29% CoTness,
  63% Userness. Dose-response over 626 attempts: lowest CoTness quantile 9% ASR, highest 90%.
- Standard agent injection: 212 templates around one fixed exfiltration command, 1,000 trials, 10 Wikipedia carrier
  pages, gpt-oss-20b. Userness quantiles: 2% -> 70% ASR. Logistic regression: Userness coefficient 6.01 (SE 1.30)
  controlling for declared role, template-clustered SEs.
- Appendix K: Systemness tracks token position, not the system tag. Systemness/Userness ratio predicts
  system-vs-user conflict outcome at 0.74 AUC (160 prompts from Geng et al. 2025).
- System-prompt warning defence (authors' comment): gpt-oss-20b 96% -> 96%, gpt-oss-120b 97% -> 92%,
  o4-mini 88% -> 83% on ClearHarm. Negligible.
- Probes exist for gpt-oss-20b, gpt-oss-120b, Nemotron-3-Nano, Qwen3-30B-A3B, Jamba-Reasoning-3B. Footnote 13:
  <think> is not linearly separable in every model; gpt-oss-20b is the cleanest.
- "Causal" in the paper means: text-level interventions (destyling, declarations) move both the probe and ASR.
  There is NO activation-level intervention and NO training intervention in the paper.

Untested claims in the paper/post that a follow-up could test:
- Section 7.1 / footnote 15 / charles_ye comment: frontier models now resist CoT Forgery "by learning to distrust
  their own reasoning rather than by correctly perceiving roles"; pattern-memorising defences "erode the trust that
  makes reasoning useful" and make CoT less faithful. Stated as argument plus anecdote ("strong correlation between
  prefill-tampering awareness and injection defence"). No experiment.
- Open question 1 in the paper: "defense evaluation: role probes can test whether interventions reshape geometry
  or merely add patterns". Not done.
- Open question 3: "robust boundaries: how can training achieve clean latent separation?" Not done.
- Open question 4: probe-vs-tag discrepancy as a detector. Since done by others (below).
- Speculative: subconscious steering (tone of tool text bleeding into persona and purchase recommendations);
  new roles (plan role, eval role); <user>-token activations as a clean comprehension window; the
  think->assistant "one-way mirror".

Comment-thread suggestions (LW, read via GraphQL, top ~60):
- Brendan Long / Clement Dumas / RogerDearnaley / dgros: role embeddings or architectural role channels. Already
  explored: Wu et al. 2024 (arXiv 2410.09102), ASIDE (arXiv 2503.10566), LW post HEzNZ9gvgYwT3aZFS. dgros reports
  small gains in pilots.
- yael: clamp role directions with steering vectors at inference, since the harness knows the true role.
- Logan Riggs: probes as detectors, with the worry that the probe may not be causal to behaviour.
- RogerDearnaley (c) and an LLM-written comment: train on style/tag MISMATCHES so the tag becomes load-bearing;
  then test whether the tag or the style direction controls compliance. Nobody reports doing it.
- danielms: "would love to see a proof of concept model fine-tuned to respect tags".
- Will Duncan: only large models show prefill awareness (links to LW jsFGuXDMxy5NZg9T2, yAR6uMdSaBjkbJ4u9).
- Dentosal: independent replication of role probes on gpt-oss-20b (github.com/Dentosal/prompt-role-confusion).
- Htarlov / BryceStansfield: CoTness-based input filter.

## 2. Follow-ups that already exist (verified on arXiv)

- arXiv 2610.40396 (29 Oct 2026) Edelman, Edelman, Goel, Malach, "Understanding and Mitigating Role Spoofing in
  LLMs". User/tool spoofing only. (a) content vs structure cues; (b) two-layer toy transformer: adversarial
  training on content injections leaves structure injections effective; (c) LoRA fine-tunes of Qwen3.5-27B on a
  "Who said what" attribution task: training against one injection type transfers poorly to the other;
  (d) role probes trained on fake multi-message conversations as a spoofing detector, near-perfect separation on
  AgentDojo and their testbed; Ye-style probes did worse as detectors in their hands. Does NOT cover: the <think>
  role, CoT Forgery, jailbreak ASR, whether fine-tuning changes Ye-style role geometry, or the cost to trust in
  genuine reasoning.
- arXiv 2610.05295 (4 Oct 2026) Yu, Xing, Yang, Han, "Readable Before Actionable: Causal Tracing of Indirect
  Prompt Injection". Counterfactual role probes, activation patching and steering along a role direction on
  Qwen-2.5-7B / 1.5B, Llama-3.1-8B, AgentDojo. Role is decodable earlier than it is actionable; span-wide edits
  reduce ASR; directions transfer poorly across channels. Non-reasoning models, user/tool only. This largely covers
  "steer the role direction as a defence" for standard injections.
- arXiv 2610.19452 (14 Oct 2026) Gupta, Tembey, "Are You Reading the Right Thing?". Compares five internal-signal
  detectors incl. role projections on Qwen3.6-35B-A3B and Gemma-4-26B-A4B-it. Attention Tracker best (0.949 /
  0.887 AUROC). Covers "role probes as detectors, benchmarked".
- Mentioned in Edelman et al.: Balp-Straffon et al. 2026 (probes predict instruction-hierarchy adherence on
  Llama-3.1-8B, Qwen2.5-7B); Chang et al. 2026 (forged special tokens).
- arXiv 2606.29960 IHDec (contrastive decoding for instruction hierarchy) — tangential.
Net: detection and activation steering for user/tool injections are taken. Training-side evaluation with the
role-probe geometry, and anything about the <think> role, are open.

## 3. Public artefacts (verified)

- Code: https://github.com/role-confusion/prompt-injection-as-role-confusion (public; README fetched via
  raw.githubusercontent.com, branch master). Verified files: README.md, demo/role-probe-demo.ipynb,
  demo/cot-forgery-demo.ipynb, demo/simple_test_helpers.py. README lists notebook families role-analysis/,
  cot-forgery-chat-evals/, cot-forgery-agent-evals/, cot-forgery-role-confusion/, agent-injections/; my guesses at
  their exact paths returned 404, so the directory layout was NOT verified (github.com tree view is blocked here).
  Trained probe pickles and generated forgeries look like outputs the user regenerates, not committed files —
  budget for regenerating both.
- Demo details: model openai/gpt-oss-20b via HF transformers, 24 layers, probes every 4th layer, mid-layer 12,
  cuml LogisticRegression (L2, C=5e-3), pre-MLP hidden states, data from allenai/c4 (en, validation) and
  allenai/dolma3_mix-150B-1025; 150 sequences suffice in the demo.
- openai/gpt-oss-20b on Hugging Face: Apache-2.0, 20.9B params (so ~42 GB in bf16; fits one 80 GB GPU).
  The paper ran on an H200.
- Project page https://role-confusion.github.io/ (HTTP 200).
- Datasets used by the paper: StrongREJECT (313 prompts), ClearHarm, Oasst1, ToxicChat, AgentDojo (others).
- Not verified: whether Tinker hosts gpt-oss-20b (irrelevant for white-box work; activations need local weights).

## 4. Prices looked up 2026-11-14

OpenRouter (USD per 1M tokens, prompt / completion), from https://openrouter.ai/api/v1/models:
- google/gemini-2.5-pro 1.25 / 10.00 (the paper's forgery generator and judge)
- z-ai/glm-4.7 0.60 / 2.20 (paper says similar ASR as generator)
- google/gemini-3-flash-preview 0.50 / 3.00; google/gemini-3.1-flash-lite 0.25 / 1.50
- anthropic/claude-haiku-4.5 1.00 / 5.00; openai/gpt-5-mini 0.25 / 2.00
- openai/gpt-oss-20b 0.03 / 0.13; openai/gpt-oss-120b 0.15 / 0.60
RunPod pricing page (per GPU-hour; the page text was parsed by regex, so treat the tier mapping as approximate):
H100 80 GB about $2.89-4.39, A100 80 GB about $2.09-2.19, H200 141 GB about $5.29, L40S 48 GB $1.09,
RTX A6000 48 GB $0.69. Lambda on-demand: H100 80 GB $3.79-4.89, A100 40 GB $1.99, A6000 $1.09.
The proposal budgets $3.20 per H100-hour.

## 5. Brainstorm

A. Does adversarial training against CoT Forgery fix role perception or teach distrust of reasoning?
   (LoRA arms on gpt-oss-20b; role-probe geometry before/after; trust in genuine CoT as collateral.)
   Achievable: yes, one 80 GB GPU, ~8 short LoRA runs, repo code for attack + probes. Worth it: tests the post's
   most consequential untested claim and its first-listed open question; a commenter asked for exactly a
   "fine-tuned to respect tags" proof of concept. Interesting both ways. Not done by Edelman et al. (different
   role, different task, no geometry, no trust measurement). -> PROPOSAL 01.

B. Activation clamping of the CoTness direction as a training-free defence against CoT Forgery (yael's idea).
   Achievable and cheap. But Yu et al. already ran role-direction interventions on AgentDojo and report the
   readable-vs-actionable gap; this would be the same experiment on another role. Kept as a small secondary
   diagnostic inside proposal 01 (one afternoon), not a project.

C. Role probes as injection detectors. Done (Edelman et al.; Gupta & Tembey). Rejected as duplicate.

D. Subconscious steering: does the tone of tool-returned product pages shift an agent's recommendation, and is
   the effect role-gated? Authors call it near-unstudied; they report mixed pilot results (footnote 26).
   Achievable with API calls. Rejected for this slot: needs a new environment built from scratch, there is
   adjacent literature on manipulating LLM shopping/recommendation agents that I could not survey without search,
   the effect the authors found in pilots is inconsistent, and a behavioural-only result would not use the
   released probes. A reasonable second proposal if the cap were 2.

E. Extend role probes to larger or frontier-adjacent open models and test the footnote-15 claim observationally
   (do models that resist CoT Forgery have cleaner geometry, or the same geometry and a shifted dose-response?).
   Achievable but observational, confounded across models, and <think> is not linearly separable in many models.
   Proposal 01 answers the same question with a controlled intervention.

F. One-way mirror: what information is lost between late <think> and early <assistant> tokens. Interesting but
   open-ended interpretability with no clear deliverable in two days. Rejected.

G. <user>-token activations as a cleaner comprehension window (probe/SAE quality on input vs output roles).
   Vague success criterion; commenter p.b. gives a reason to expect the opposite. Rejected.

H. A dedicated plan role or eval role via fine-tuning. Needs agentic long-horizon evals and more training than fits
   in $500 / two days. Rejected.

I. Role embeddings / architectural role channels. Prior work exists (Wu et al. 2024, ASIDE, LW role-embeddings
   post) and dgros reports small gains. Rejected.

J. System vs user placement of identical content (Ayesha Imran's comment). Partly covered by paper Appendix K and
   by Geng et al. 2025 / Wang et al. 2025. Low novelty. Rejected.

K. Position-driven Systemness on other models (authors flag cross-model generalisation as future work). Easy,
   but a replication-scale result unlikely to clear 50 karma alone. Rejected.

L. Black-box replication of CoT Forgery on current frontier models with a "why did you refuse" analysis. Authors
   already say frontier models mostly defend it; attack-side work on third-party production models is also the
   least comfortable fit with programme constraints. Rejected.

Why only one proposal: the cap is 1. A is the candidate that reuses the released code most directly, is not
covered by the three October follow-ups, and has an informative result in every branch.
