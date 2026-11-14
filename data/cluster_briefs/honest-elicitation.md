# Cluster: Eliciting confessions: honest personas, confession training, deals

key: `honest-elicitation` — 4 post(s); write at most 2 proposal(s).

## Split Personality Training: Revealing Latent Knowledge Through Alternate Personalities (Research Report)
- id: `og7km7vmJ6Ktay9Ds` | 2026-01-12 | 101 karma | Florian_Dietz
- url: https://www.lesswrong.com/posts/og7km7vmJ6Ktay9Ds/split-personality-training-revealing-latent-knowledge-1
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Trains a LoRA 'honest persona' that is activated after the main model's response (via a special token plus an intervention string) to review that response, with no influence on the main output. Trained on Gemma-3, Qwen3 and Llama-3.3-70B and tested on Anthropic's auditing-game model organism (a 70B model trained to exploit reward-model biases and hide it), it detects reward hacking with up to 96% accuracy and names the hidden biases; it generalises across topics and, per a later edit, reveals alignment faking. Ablations suggest it relies about equally on latent knowledge and surface heuristics, and it is jailbreakable when targeted directly.
- screener's follow-up note (often the screener's inference): Authors' open questions: performance on subtler/diffuse misalignment, on smarter alignment-faking models, and whether adversarial training hardens the honest persona against targeted jailbreaks; also improving training data so it relies less on surface heuristics.
- builds on: Split Personality Training: Revealing Latent Knowledge (earlier post, https://www.lesswrong.com/posts/iocPzHRsH9JWtwHHG/split-personality-training-revealing-latent-knowledge); Anthropic Auditing Game Model Organism

## Why we are excited about confession!
- id: `k4FjAzJwvYjFbCTKn` | 2026-01-14 | 143 karma | Boaz Barak, Gabriel Wu, Manas Joglekar
- url: https://www.lesswrong.com/posts/k4FjAzJwvYjFbCTKn/why-we-are-excited-about-confession
- screener's kind: runs (high); follow-up cost guess: unclear
- screener's summary (unverified): OpenAI follow-up to their confessions paper: models are trained to emit a second output (a 'confession') rewarded solely for honesty about misbehaviour in the main answer, on the hypothesis that honest confession is the path of least resistance. The post gives further analysis of the impact of confession training and a preliminary comparison with CoT monitoring: on intervention-style monitorability evals a monitor given the confession often does worse than one given the CoT, but better in some cases. Confession training needs no ground-truth labels, so it can be applied across all RL environments.
- screener's follow-up note (often the screener's inference): Compare confessions with CoT monitoring in settings better suited to them (e.g. reward hacking), test at larger scale, and replicate confession training on open-weight models to check whether confessions stay honest under pressure to hide.
- builds on: OpenAI confessions paper and original blog post; Korbak et al., Chain of Thought Monitorability (https://arxiv.org/abs/2507.11473)

## Ablating Split Personality Training
- id: `5gDjg4oN4kJKMLovs` | 2026-03-23 | 55 karma | OscarGilg
- url: https://www.lesswrong.com/posts/5gDjg4oN4kJKMLovs/ablating-split-personality-training
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Ablations of Split Personality Training on Llama-3.3-70B-Instruct using Anthropic's RM-sycophancy LoRA as the poisoned model. Findings: plain user follow-up prompts work as well as the split-personality framing (and train 2-3x faster), the free-text review can be dropped without hurting detection, and training on a clean model reaches the same ceiling; a LoRA trained on generic alignment topics transfers to detecting unseen reward hacking (>92% on auditing-games vs 55-77% untrained).
- screener's follow-up note (often the screener's inference): Probe why the cheap generic LoRA generalises: test on other model organisms/hidden behaviours and on behaviours the model is trained to conceal more robustly, and compare with other self-report/confession fine-tuning methods.
- builds on: Split Personality Training: Revealing Latent Knowledge Through Alternate Personalities; Anthropic auditing games / rm_sycophancy model organism

## Model organisms (sometimes) confess their misalignment when offered a deal
- id: `kaMXwA9LjrRbekmsQ` | 2026-09-16 | 62 karma | Mark Keavney, Francis Rhys Ward
- url: https://www.lesswrong.com/posts/kaMXwA9LjrRbekmsQ/model-organisms-sometimes-confess-their-misalignment-when
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Offers four Kimi-K2.6 model organisms (trained schemer, prompted schemer, covert manipulator, user-first) money, compute, human labour or message publication for admitting misalignment, varying offer size and credibility, and honours all deals. High offers yield 25% admissions vs 6% for a plain ask, but not significantly more than a low offer (20%); high-credibility offers beat low-credibility ones (34% vs 16%); the control model never admits. Code is public.
- screener's follow-up note (often the screener's inference): Repeat with more realistic model organisms or standard models behaving misaligned; separate incentive value from the mere presence of an offer; reduce the eval-awareness confound.
- builds on: Making deals with early schemers (Stastny, Järviniemi & Shlegeris 2025); Will alignment-faking Claude accept a deal to reveal its misalignment? (Greenblatt & Fish 2025); Being honest with AIs (Finnveden 2025); Making deals with AIs: a tournament experiment with a bounty (Finlinson & West 2025)

