# Cluster: Are neurons already clean? Evaluating neuron explanations

key: `neuron-legibility` — 3 post(s); write at most 2 proposal(s).

## Linkpost: Neural Networks Are Already Clean
- id: `x4kvabkF2Jk8GLZp8` | 2026-10-15 | 220 karma | Yair Halberstadt
- url: https://www.lesswrong.com/posts/x4kvabkF2Jk8GLZp8/linkpost-neural-networks-are-already-clean
- screener's kind: runs (borderline); follow-up cost guess: cheap
- screener's summary (unverified): Short linkpost to Nick Cammarata's long 'Neural Networks Are Already Clean' report (already-clean.goodfire.com), which claims that with agentic auto-interp tools the vast majority of neurons in models up to trillions of parameters are legible and that many famous 'polysemantic' neurons were misunderstood. The LW post itself only quotes the Twitter summary and asks how much of an advance this is and how it helps alignment.
- screener's follow-up note (often the screener's inference): Independently check the legibility claim on a small open model: have an agent explain random neurons and score explanations with a causal metric (see leogao's reply post) rather than by inspection of activating examples.
- builds on: Neural Networks Are Already Clean (https://already-clean.goodfire.com/); OpenAI automated interpretability / neuron-explainer paper

## Neural networks are not already clean
- id: `Dkh7pXKjoNWkkxQDz` | 2026-10-17 | 368 karma | leogao
- url: https://www.lesswrong.com/posts/Dkh7pXKjoNWkkxQDz/neural-networks-are-not-already-clean
- screener's kind: motivates (borderline); follow-up cost guess: cheap
- screener's summary (unverified): Conceptual rebuttal to Cammarata's 'Neural Networks Are Already Clean': clean-looking activating examples do not show a neuron is explained, because explanations can lack recall (the neuron fires only on a hard-to-describe subset) and ignore activation magnitudes. Argues explanations should be judged by simulating the neuron from a rubric, substituting simulated activations and measuring downstream KL on a large dataset, and that explaining neurons is only part of understanding a network.
- screener's follow-up note (often the screener's inference): Run simulation-with-downstream-KL scoring on agent-generated neuron explanations in an open model to measure how much of the 'legible' neurons' behaviour is actually captured, including weak activations.
- builds on: Linkpost: Neural Networks Are Already Clean; OpenAI 'Language models can explain neurons in language models' (auto-interp paper)

## Twitch Plays: AI Interpretability of Bonsai-8B
- id: `ozbbzsh49wvgfbCDp` | 2026-10-19 | 82 karma | moridinamael
- url: https://www.lesswrong.com/posts/ozbbzsh49wvgfbCDp/twitch-plays-ai-interpretability-of-bonsai-8b
- screener's kind: runs (borderline); follow-up cost guess: cheap
- screener's summary (unverified): Describes a live project where a Claude agent plus a Twitch audience interpret individual neurons (and upstream/downstream neighbours via ablation) of Bonsai-8B, a 1-bit quantised Qwen3-8B derivative with 442k MLP neurons, recording results in a public map/GitHub repo that accepts PRs. It is an ongoing tooling/participation project rather than a paper with quantitative results.
- screener's follow-up note (often the screener's inference): Use the open repo/map to quantify how well the agent-produced neuron explanations hold up (held-out activation prediction or causal scoring), or compare neuron legibility in the 1-bit model with its full-precision parent.
- builds on: Neural Networks Are Already Clean (https://already-clean.goodfire.com/); Towards Monosemanticity / Scaling Monosemanticity

