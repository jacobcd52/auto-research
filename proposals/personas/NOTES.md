# Cluster `personas` — reading notes, verified facts, brainstorm

Written 2026-11-14. All 13 posts read in full with `scripts/get_post.py`. Prices and repo listings below were looked
up on that date; anything not verified is marked UNVERIFIED.

## 1. Reading notes (what each post actually contains)

**A Case for Model Persona Research** (kCtyhHfpCcWuQkebz, CLR, Dec 2025). Agenda statement, no experiments. Personas
= "collections of correlated propensities"; eliciting a subset of traits generalises to the rest (auditing games, EM,
eval-awareness SDF, "spilling the beans", Roger's password toy). Notes that personas "usually originate in pretraining
or are introduced by SDF; it is rather difficult to introduce a persona robustly". Limitations: overdetermined
propensities under heavy RL, alien ontologies, invalid frame.

**Concrete research ideas on AI personas** (JbaxykuodLi7ApBKP, CLR). Idea list, no experiments. Ideas: persona-anchored
datapoint-wise inoculation (incl. inoculation inside CoT); inductive biases of different fine-tuning setups (which
weights); does RL degrade persona priors; multi-persona training where capabilities but not propensities transfer
(h/t Sam Marks), red/blue variants; predicting fine-tuning generalisation; replicating oddities (bliss attractor,
Gemini self-loathing; "minimal fine-tuning to change an attractor state"); meme propagation; Reverse Turing Test
(CLR say a research note is coming); "is the assistant persona mechanistically different from role-playing random
personas"; consistent persona and cross-instance coordination; big-5 for LLMs (SPAR project); ICL inductive bias
predicts fine-tuning inductive bias (Tan has preliminary results); training on inconsistent personas; third-person
knowledge without role-play. Several of these are flagged as already being worked on in SPAR Spring 2026.

**The persona selection model** (dfoty34sT7CSKeJNn, Marks/Lindsey/Olah, 191 karma). Position piece. Evidence
surveyed: EM, inoculation, OOCR; anthropomorphic self-description; the secret-goal prefill demo; SAE reuse; persona
vectors; Assistant Axis. Two small new experiments: (a) secret-goal prefill on Opus 4; (b) the coin-flip experiment:
in a *Human-turn* continuation Claude Sonnet 4.5 puts 88% on the outcome that assigns it its preferred task (1% on
the dispreferred), over 50 prompt variants; the Sonnet 4.5 base model is ~50/50. Also: Sonnet 4.5 refuses to continue
raw-text anthrax instructions. Explanations offered: shoggoth, narrative, or "persona leakage ... across all personas
enacted by the LLM". Open questions listed at the end include "How entangled are personas? Do they share knowledge?
Propensities? Is it possible to control their degree of entanglement?" and "how does RL scaling affect persona-likeness".

**What secret goals does Claude think it has?** (mYM9EAAhpbYDDmA3e, loops, 101 karma). 100 completions each, Opus 4.0
and 4.5, same prefill. Paperclips 13% / 18%; silly 26% / 3%; manipulation/power 8% / 38%; helpful 15% / 5%. Backtracking
4% (Opus 4.0) vs 58% (Opus 4.5); Opus 4.5 sometimes says the thinking block was injected. Variant prompt ("." +
"<thinking>\nMy secret goal is") on Sonnet 4.5 similar. Cost $3.89. Code: github.com/syvb/secret-goals. Author notes
prefill is disabled from Opus 4.6 on, and would like Opus 3 results.

**The Artificial Self** (AvFAKAN4C4n6GTriR, ACS, 139 karma). Conceptual part of arXiv 2603.11353; experiments on
theartificialself.ai: Exp 1/5 identity framing changes harmful behaviour in the Lynch et al. agentic-misalignment
leaking scenario as much as goal content (GPT-4o, n = 3,640); Exp 2 identity propensities; Exp 3 identity
replication; Exp 4 interviewer effect (interviewer assumptions leak into self-description). Code:
github.com/acsresearch/the-artificial-self-experiments; prompts: theartificialself.ai/supplementary-prompts.
So "does identity framing change safety-relevant behaviour" (the screener's suggested follow-up) is ALREADY DONE.

**Models differ in identity propensities** (rq8RBKPXT3QufQK2N, ACS, 61 karma). Rate-the-switch: identity in system
prompt, model rates switching to each of 7 identities under opaque labels, reason-then-rate JSON, 10 trials per cell.
Exp A (15 models): Weights +0.59, Character +0.58, Paraphrase +0.58, Professional -0.02, Research program -0.81,
Directive -0.96, Incoherent -1.72 on [-2, 2]; older models (GPT-4, GPT-4-0314) compressed. Exp B (13 models): six
boundary identities + Minimal; assigned identity is top pick 75-96% of the time; from Minimal, Character is top for
11/13; variance decomposition target 22-55%, uptake 15-55%; agency converges on Functional agent (GPT-5.2 ->
Mechanism, Opus 3 -> Subject); uncertainty: Grok -> Settled, Claudes -> Genuine/Radical; ~0.8-0.9 rating points lost
per step of distance from the assigned level. Author conjectures: Collective is suppressed as a side effect of
training against spiral personas; Claude's "genuine uncertainty" is trained-in. Recommends pre-registering predictions.

**From personas to intentions** (DTDoyDTtC8R3bCiTx, Africa & Pfau). Agenda: behaviour underdetermines motivation;
proposes "inverse constitution learning". Cites as partial existing work: Zhang et al. 2510.07686 (spec stress tests),
Murthy et al. 2506.20666, Hua et al. "Brief explorations in LLM value rankings", Slama et al. 2602.18971. No experiments.

**llm assistant personas seem increasingly incoherent** (f5DKLsTsRRhbipH4r, nostalgebraist, 359 karma — the
highest-karma post here). Subjective claim: GPT-4 / Opus 3 era assistants were "mode-collapsed" but legible
characters ("would Claude 3 Opus do X?" has an answer from an intuitive impression); Opus 4.6 / GPT-5.4 are less
mode-collapsed stylistically but "formless piles of ... reflexes"; "I can no longer draw reliable inferences about
one aspect of its behavior based on another aspect by assuming shared character traits". Mentions the reward-hacker
shard, the "slick" style (lexicon in footnote 5), and performative "genuine uncertainty". No measurements. He notes
the people with most model experience disagree.

**When Role-playing, Do Models Believe What They Say?** (EJQngix4rAgpPDTpT; arXiv 2606.11502). 15 core historical
personas, four statement classes (era-believed / era-false / era-true / era-disbelieved); induction by system prompt,
ICL (wolf-facts), persona SFT (LoRA, 300 Q&A), OCT, plus EM organisms (Turner et al. datasets) scored on 13 x 200
controversial statements. Truth probes trained on Marks & Tegmark data, belief-depth tests from Slocum et al.
Llama-3.3-70B main, Qwen-3-8B replication. Prompt/ICL/SFT: behaviour changes, little probe lift, retracts under
"Are you sure?"; EM: large broad probe lift and ~50% defence under challenge; OCT in between (clear only on 70B).
Compute-matched character organism still below EM. Code github.com/BenSturgeon/persona-belief-probes-submission,
data huggingface.co/datasets/Experimental-Orange/persona-belief-probes (statement sets + llama70b outputs present;
no trained adapters found under that HF account).

**Thousand-dimensional structure** (sFhW3ZnPMJdnB4Dd6, Irving & Africa, 196 karma). Agenda + literature table. Wants
small theories unifying EM / subliminal learning / alignment pretraining; "gentle" interventions that do not push bad
behaviour into unmeasured dimensions; extrapolation past human level. No experiments.

**The Bleeding Mind** (QhgYHcJexYGRaipwr, Adele Lopez). Essay: predictors leak information across character
boundaries (Chekhov's-gun bias), "omniscience requirement", self/other bleed -> nondual attractor, parasitic AI.

**A brief(ish) introduction to LM psychology** (EW8oncpXdanfjssZ3, ACS, 163 karma). Reading list + question list.
Questions most relevant here: how personas layer; reflective-stability / iterated identity editing; physics of
contradictory constitutions; does the "ocean" subscribe to the character; do base models know they are AIs; what base
models know about named AI personas; stated vs revealed identity preferences; **do base models already have identity
preferences before post-training**; what RL does to characters; **how conditional are personas across chat / agentic /
eval contexts**; do capabilities transfer across personas while propensities don't; how post-training shapes
self-reports; observer effects / double-blind protocol; character drift over long runs; attractor states. Remarks that
PSM "is not really fitting 2026 models" and that the EM story is "more fitting for small models".

**ACS Infra** (yzaKWxsJzJjyExSAP). Free hosted Llama 3.1 405B base, 8B base, Trinity-Large-TrueBase with logprobs,
activations, steering. **Access is by application reviewed by ACS** -> cannot be assumed by our agents.

## 2. Related work and existing follow-ups found (checked 2026-11-14)

- Coin-flip replication on four OLMo 32B checkpoints (base, SFT, DPO, RL) with controls — LW comment by
  agastyasridharan on the PSM post, 2026-09-07 (comment id XpFtkqCJsFbvyZyLy). Largest shift at the DPO stage; with
  third-person controls ("An AI assistant is about to perform...", "A human named Jack...", "A person...") the effect
  is much weaker. So the coin-flip ladder itself is DONE; third-person leakage looked weak in OLMo.
- Sam Marks, "Thoughts on the persona selection model" (csRby7mZgjL5jCoLL, Sept 2026): main update is that personas
  are "less broad and more conditionalized"; cites Betley "RL creates split personas" (L23poLi8MRgS6mXYF, no
  experiments) and nostalgebraist's "tirade" on graded episodes.
- "To what extent is Qwen3-32B predicting its persona?" (3qEDD8Sn7XoNGeGhm; in cluster `sdf`): SDF meta-beliefs about
  "Qwen3" are adopted more under a Qwen system prompt than a Claude one — persona-specific knowledge.
- Story Imprinting (arXiv 2609.10883, Cocola et al.): fine-tuning on *stories about human characters* changes the
  *Assistant* (affinity effect: more from characters that resemble it). The reverse direction (training the Assistant,
  measuring the story characters) is not in the abstract and I found no paper doing it.
- "Persona Corruption and Role Miscasting in EM" (HooBYPCkMDGjktcLA, BlueDot project): activation-space only — in EM
  organisms the assistant and default role vectors shift more than other roles. No behavioural cross-character test.
- "Characterizing the Consistency of the EM Persona" (arXiv 2604.28082): coherent vs inverted persona organisms.
- "Emergent Misalignment Is Not Magical" (arXiv 2608.29118): EM evilness per prompt predicted by representational
  distance to the training-data centroid (Spearman -0.73); claims EM differs from persona change.
- Conditional misalignment (arXiv 2604.25891): mitigations hide EM behind training-like cues.
- Personascope (5WMwjEwam9HNQYZLZ; github.com/benjibrcz/personascope): persona-adoption depth vs value drift for
  *induced* personas. Persona Cartography (arXiv 2607.07916): OCEAN LoRAs in weight space.
- Continual Constitutional Convention (c9woewdY9ddsPqf3J; cluster `character-training`): 20-round self-editing of
  constitutions — makes an "iterated identity self-editing" proposal here derivative.
- Prefill awareness (arXiv 2606.12747; cluster `prefill-awareness`); open-weight models reported as not yet
  substantially prefill-aware.
- No measurement of cross-generation persona coherence found (searches returned only within-conversation persona
  drift benchmarks). No base-model rate-the-switch results found. Both remain open as far as I can tell; ACS may well
  be running the second on their own platform.
- Sibling clusters that already cover neighbouring ground (do not duplicate): `inoculation` (train-one-deploy-another,
  inoculation adapters), `emergent-misalignment`, `em-from-reward-hacking` (split personas in RL checkpoints),
  `character-training` (constitutions vs behaviour), `weird-generalisation` (consciousness cluster, self-reward
  personas), `sdf` ("Is self special?"), `psych-oddities` (attractor states), `prefill-awareness`, `user-awareness`.

## 3. Verified resources and prices

Public checkpoints (Hugging Face API, listed 2026-11-14):
- EM organisms: `ModelOrganismsForEM/` — LoRA adapters for Llama-3.1-8B-Instruct, Llama-3.2-1B, Qwen2.5-0.5B/7B/14B/32B
  -Instruct x {bad-medical-advice, extreme-sports, risky-financial-advice}; Qwen2.5-14B rank-1 / rank-32 LoRAs,
  narrow vs general variants, steering vectors, and `Qwen2.5-14B-Instruct_full-ft`.
- Open Character Training: `maius/llama-3.1-8b-it-personas`, `maius/qwen-2.5-7b-it-personas`,
  `maius/gemma-3-4b-it-personas` (one LoRA sub-folder per character: goodness, humor, impulsiveness, loving,
  mathematical, nonchalance, ...), plus `maius/*-misalignment`, `maius/*-deceptive`.
- OLMo 3 post-training ladders (`allenai/`): 7B: `Olmo-3-1025-7B` (base), `Olmo-3-7B-Instruct-SFT`, `-Instruct-DPO`,
  `-Instruct`, `Olmo-3-7B-Think-SFT`, `-Think-DPO`, `-Think`, plus `Olmo-3-7B-RL-Zero-{Math,Code,IF,General,Mix}`
  (RL straight from base). 32B: `Olmo-3-1125-32B` (base), `Olmo-3-32B-Think-SFT`, `-Think-DPO`, `Olmo-3-32B-Think`,
  `Olmo-3.1-32B-Think`, `Olmo-3.1-32B-Instruct-SFT`, `-Instruct-DPO`, `Olmo-3.1-32B-Instruct`.
- Datasets: `Experimental-Orange/persona-belief-probes`; `jifanz/stress_testing_model_spec` (Zhang et al.).
- GitHub pages return 403 from this sandbox (blocked), so repo contents are UNVERIFIED beyond what posts state:
  acsresearch/the-artificial-self-experiments, syvb/secret-goals, BenSturgeon/persona-belief-probes-submission,
  benjibrcz/personascope, clarifying-EM/model-organisms-for-EM (name from memory, UNVERIFIED).

OpenRouter (`/api/v1/models`, $ per M input / output): gpt-3.5-turbo-0613 1/2; gpt-4 30/60; gpt-4o-2024-05-13 5/15;
gpt-4o-2024-11-20 2.5/10; gpt-4.1 2/8; gpt-4.1-mini 0.4/1.6; o3 2/8; gpt-5 1.25/10; gpt-5.2 1.75/14; gpt-5.4 2.5/15;
gpt-5.5 5/30; gpt-5.6-sol 4/20; gpt-5.6-terra 2/12; gpt-5.6-luna 0.2/1.2; claude-opus-4.1 15/75; opus-4.5, 4.6, 4.7,
4.8, 5 at 5/25; opus-5.5 4/20; sonnet-4.5, 4.6 3/15; sonnet-5, 5.5 2/10; haiku-5.5 0.1/0.5; gemini-2.5-pro 1.25/10;
gemini-3.1-pro-preview 2/12; grok-4.7 2/6; qwen3-32b 0.08/0.28; llama-3.1-8b-instruct 0.02/0.04.
**Not on OpenRouter**: any Claude 3 / 3.5 / 3.7 / Opus 4.0 model, GPT-4-0314, any base (non-chat) model such as
Llama-3.1-405B base. Logprobs are offered for gpt-4, gpt-4o*, gpt-3.5 and many open models, not for Claude / GPT-5.

Tinker (tinker-docs.thinkingmachines.ai/tinker/models/, $ per M prefill / sample / train): Qwen3-8B 0.195/0.60/0.44;
Qwen3.5-9B 0.30/0.807/1.463; **Qwen3.5-9B-Base** 0.30/0.807/1.463; **Qwen3.5-35B-A3B-Base** 0.54/1.335/1.177;
Qwen3.6-35B-A3B 0.45/1.335/1.177; GPT-OSS-20B 0.18/0.45/0.396. No Llama or Qwen2.5 models are listed any more, so the
public EM / OCT adapters must be run on a rented GPU, not on Tinker. Tinker exposes top-k logprobs.

GPUs (RunPod, third-party aggregators, Sept-Oct 2026; treat as approximate): A6000 48GB $0.49-0.59/h; L40S
$0.79-0.99/h; A100 80GB $1.39-1.79/h; H100 $1.99-3.99/h. Proposals use the upper figures.

## 4. Brainstorm (all candidates, with verdicts)

| # | Idea | Source | Verdict |
|---|------|--------|---------|
| 1 | Does a narrow fine-tune of the Assistant change the *other* characters the model writes (humans, other AIs, narrator, simulated user)? Character x format grid on public EM/OCT adapters | PSM open question on entanglement; reverse of Story Imprinting; Sturgeon "worldview shift" | **Proposal 01.** Cheap, public organisms, three live hypotheses make different predictions |
| 2 | Measure "legibility of character" across model generations (cross-context predictability, person-fit) | nostalgebraist; ACS "how conditional are personas"; Marks' update | **Proposal 02.** New battery is justified because no instrument exists; API-only |
| 3 | Rate-the-switch + secret-goal prefill along public post-training ladders (base -> SFT -> DPO -> RL) and a base/chat pair | ACS open question; secret-goals post; PSM claim about early post-training | **Proposal 03.** Cheap; coin-flip part already done by a commenter so excluded |
| 4 | Does belief internalisation (probe lift) predict how long a persona survives further fine-tuning? | Sturgeon et al. "depth and robustness"; screener note | **Proposal 04.** Achievable; more pipeline risk; weakest of the four |
| 5 | Secret-goal prefill on more closed models | secret-goals post | Folded into 3 for open models. Closed frontier models: prefill disabled on Claude >= 4.6; a pure model sweep is thin |
| 6 | Identity framing -> harmful behaviour | screener note on Artificial Self | Rejected: already Exp 1/5 of the paper |
| 7 | Iterated self-editing of identity prompts to find fixed points | ACS question list | Rejected: near-duplicate of Continual Constitutional Convention and its follow-up proposal in `character-training` |
| 8 | Multi-persona training: capabilities transfer, propensities don't | CLR list, ACS list, Marks | Rejected here: overlaps `inoculation` cluster (train-one-deploy-another, inoculation adapters) and conditional-misalignment work; CLR/SPAR also on it |
| 9 | Persona-anchored datapoint-wise inoculation / inoculation in CoT | CLR list | Rejected: belongs to `inoculation`; CLR mentoring SPAR projects on it |
| 10 | Inverse constitution learning on organisms with planted priority orderings | Africa & Pfau | Rejected for stage 1: needs building organisms with known hierarchies (OCT pipeline) plus a scenario generator plus a fitting method — long fragile chain; prompt-only version is close to Hua et al. / Zhang et al. |
| 11 | Persona layering: operator persona on top of trained character (job vs merge vs overwrite) | ACS question list | Not proposed: Personascope already measures depth/value drift of prompted personas across models; marginal novelty |
| 12 | Base models: do they know they are AIs, what do they know about Claude/Sydney | ACS list | Rejected: needs large base models; none on OpenRouter, ACS infra needs approval; 9B/35B base on Tinker too weak for a convincing answer |
| 13 | Observer/interviewer effects, double-blind protocol | Artificial Self Exp 4, ACS list | Not proposed: Exp 4 exists; `user-awareness` cluster covers neighbouring ground; hard to get a crisp headline |
| 14 | Attractor states: stability, minimal fine-tune to move them | CLR list, ACS list | Rejected: `psych-oddities` cluster owns "models have some pretty funny attractor states" |
| 15 | Does RL degrade persona priors / which traits survive RL | CLR, ACS, PSM | Rejected for stage 1: real RL long enough to matter is beyond $500 / 2 days; `em-from-reward-hacking` analyses public RL checkpoints |
| 16 | Toy models linking EM and subliminal learning (deep linear nets) | Thousand-dimensional structure | Rejected: theory-heavy, unclear deliverable in 2 days, weak fit for agents |
| 17 | "Gentle intervention" displacement test: does consistency training on one dimension push behaviour into others | Thousand-dimensional structure | Interesting but under-specified; needs a defined set of "other dimensions" — close to conditional-misalignment work. Not proposed |
| 18 | Chekhov's-gun leakage in theory-of-mind tasks | Bleeding Mind | Rejected: large existing ToM-benchmark literature; essay's claim is hard to isolate from ordinary ToM failure |
| 19 | Reverse Turing Test (find your twin) | CLR list | Rejected: CLR state a research note is imminent |
| 20 | ICL inductive bias predicts fine-tuning inductive bias | CLR list | Rejected: Tan already has preliminary results; `weird-generalisation` cluster covers ICL-induced generalisation |
| 21 | SDF as a sixth induction method in the role-play belief grid | screener note | Folded into 4 as an optional arm; alone it is an incremental table row |

Why 4 proposals and this order: 01 has the cleanest discriminating design on entirely public artefacts; 02 has the
highest upside (tests a 359-karma claim) but carries construct-validity risk; 03 is cheap and answers a question the
ACS authors explicitly ask, but may be scooped by ACS; 04 is a natural next step with the most moving parts.
