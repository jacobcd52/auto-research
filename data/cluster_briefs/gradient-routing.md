# Cluster: Gradient routing (GRAFT / GRAM) for localising unwanted behaviour

key: `gradient-routing` — 4 post(s); write at most 2 proposal(s).

## Modular Pretraining Enables Access Control
- id: `43vKjWuH4goLwrFHA` | 2026-07-09 | 71 karma | E.Roland, cloud
- url: https://www.lesswrong.com/posts/43vKjWuH4goLwrFHA/modular-pretraining-enables-access-control
- screener's kind: runs (high); follow-up cost guess: unclear
- screener's summary (unverified): AE Studio with Anthropic introduce Gradient Routed Auxiliary Modules (GRAM), which confine dangerous-domain knowledge to switchable modules during pretraining. On a synthetic children's-stories dataset a 26M model with a topic switched off performs like a model trained with that topic filtered out; on an 800M model trained on general text, code and papers plus four dual-use domains (virology, cybersecurity, nuclear physics, specialised code), a single GRAM model approximates multiple data-filtered models; results reported from 50M to 5B parameters, with comparisons to post-hoc unlearning and a LoRA baseline. Paper and code released.
- screener's follow-up note (often the screener's inference): Robustness of the 'off' configuration to relearning/fine-tuning attacks and to imperfect data labelling; small-scale replications on the stories setting are feasible, the large-scale pretraining is not.
- builds on: Gradient routing; SGTM; DEMix layers; NULLs (concurrent)

## Gradient Routing Localizes and Removes Unintended Behaviors in RL
- id: `mKJEBiuuxHKuCoTB6` | 2026-10-19 | 218 karma | shawnghu, Jake Ward, ariaw, Nathan Hu, Bryce Woodworth, TurnTrout, cloud
- url: https://www.lesswrong.com/posts/mKJEBiuuxHKuCoTB6/gradient-routing-localizes-and-removes-unintended-behaviors
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Introduces GRAFT (Gradient Routing Adapter Fine-Tuning): during RL, rollouts flagged by a monitor update only a FORGET MLP adapter while unflagged ones update both adapters; ablating FORGET at deployment removes reward hacking, including hacks the monitor did not detect, while keeping task performance. Experiments are on small models with hand-specified heuristic monitors.
- screener's follow-up note (often the screener's inference): Listed open questions: does GRAFT work with LLM-based monitors, when does it beat inoculation prompting (it was matched when only half the prompts were hackable), scaling to larger models, and reducing the performance cost of ablating the adapter.
- builds on: Gradient Routing (https://arxiv.org/abs/2410.04332); Inoculation prompting (https://arxiv.org/abs/2510.04340); Baker et al. 2025, monitoring for misbehaviour / obfuscated reward hacking (https://arxiv.org/abs/2503.11926)

## Gradient Routing Generalizes to Unrouted Hack Types
- id: `ie7bSp5ZDwYkCQxuv` | 2026-10-23 | 68 karma | jacob_drori
- url: https://www.lesswrong.com/posts/ie7bSp5ZDwYkCQxuv/gradient-routing-generalizes-to-unrouted-hack-types
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Light extension of Ward, Hu et al. (GRAFT): gradients are routed on only one type of reward hack (e.g. hacks reasoned in English) and the author checks whether removing the forget adapter also suppresses other hack types the model was trained on (e.g. reasoned in French), modelling a monitor with type-specific blind spots. Finds encouraging generalisation in most arms plus some unexplained failures; uses supervised fine-tuning rather than RL.
- screener's follow-up note (often the screener's inference): Author's listed limitations: repeat in real RL, avoid the eval prompt that instructs the model to hack (could just be degraded instruction following), properly test generalisation across different hack strategies (only 2 of 12 arms, one underpowered, one poor), and compare more carefully against the random-ablation baseline.
- builds on: Gradient Routing Localizes and Removes Unintended Behaviors in RL (Ward, Hu et al. 2026)

## Some thoughts on GRAFT and follow-up work
- id: `6ro3dngDGaLJaumYb` | 2026-10-28 | 63 karma | shawnghu
- url: https://www.lesswrong.com/posts/6ro3dngDGaLJaumYb/some-thoughts-on-graft-and-follow-up-work
- screener's kind: proposes (high); follow-up cost guess: cheap
- screener's summary (unverified): A GRAFT co-author's notes connecting the method to selective modularity, inoculation/recontextualisation and unlearning, discussing practical costs (performance loss from ablating the forget adapter, monitoring budget), and giving a large list of follow-up projects.
- screener's follow-up note (often the screener's inference): Proposed projects: disentangle absorption vs inoculation effects; test whether the adapter behaves like a steering vector (scaling, negative scaling); mech interp on the adapter and gradients; don't train FORGET on unflagged samples; partial down-weighting instead of ablation; token-level rather than sample-level routing; whether anchor samples are needed; LoRA instead of MLP adapters; scaling to larger models.
- builds on: Gradient Routing Localizes and Removes Unintended Behaviors in RL; Gradient Routing (https://arxiv.org/abs/2410.04332); Inoculation prompting (https://arxiv.org/abs/2510.04340); Recontextualization (https://arxiv.org/abs/2512.19027)

