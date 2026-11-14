# Cluster: ARC: mechanistic estimation and tiny-model interpretability

key: `arc-estimation` — 3 post(s); write at most 2 proposal(s).

## AlgZoo: uninterpreted models with fewer than 1,500 parameters
- id: `x8BbjZqooS4LFXS8Z` | 2026-01-26 | 185 karma | Jacob_Hilton
- url: https://www.lesswrong.com/posts/x8BbjZqooS4LFXS8Z/algzoo-uninterpreted-models-with-fewer-than-1-500-parameters
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): ARC releases AlgZoo, a set of small RNNs and transformers (8 to 1,408 parameters) trained on algorithmic tasks such as finding the position of the second-largest number in a sequence, as challenge cases for ambitious interpretability. ARC defines an explanation as a mechanistic estimate of the model's accuracy, evaluated by surprise accounting or by MSE versus compute compared with sampling; they report more-or-less fully understanding a 32-parameter model but failing to fully understand a 432-parameter one despite substantial effort.
- screener's follow-up note (often the screener's inference): Open challenge: produce mechanistic accuracy estimates (or any full explanation) for the larger 2nd-argmax RNNs and the other AlgZoo families that beat sampling at equal compute.
- builds on: ARC progress update: competing with sampling (https://www.lesswrong.com/posts/XdQd9gELHakd5pzJA/arc-progress-update-competing-with-sampling); Formal verification, heuristic explanations and surprise accounting (https://www.lesswrong.com/posts/SyeQjjBoEC48MvnQC/formal-verification-heuristic-explanations-and-surprise); Progress measures for grokking via mechanistic interpretability (https://arxiv.org/abs/2301.05217)

## Mechanistic estimation for wide random MLPs
- id: `fsG4m6sRMpomd7Rk6` | 2026-05-07 | 86 karma | Jacob_Hilton
- url: https://www.lesswrong.com/posts/fsG4m6sRMpomd7Rk6/mechanistic-estimation-for-wide-random-mlps
- screener's kind: runs (borderline); follow-up cost guess: cheap
- screener's summary (unverified): ARC paper: estimates the expected output of a randomly initialised MLP under Gaussian input 'mechanistically' (cumulant propagation, without running the model), and for wide networks obtains more accurate estimates than sampling at matched cost, in theory and in experiments. Framed as the base case toward mechanistic estimates that beat sampling for trained networks. Code released.
- screener's follow-up note (often the screener's inference): Test how the method degrades on narrow, deep or lightly trained networks, i.e. empirically probe the 'inductive step' beyond initialisation.
- builds on: ARC's prior work on the matching sampling principle / heuristic estimation

## Announcing the ARC White-Box Estimation Challenge
- id: `Kben8CzS4awCwNw5c` | 2026-06-02 | 168 karma | Jacob_Hilton, paulfchristiano, Wilson Wu
- url: https://www.lesswrong.com/posts/Kben8CzS4awCwNw5c/announcing-the-arc-white-box-estimation-challenge
- screener's kind: proposes (borderline); follow-up cost guess: cheap
- screener's summary (unverified): ARC and AIcrowd launch a contest (>= $100k prize pool in later rounds) to design algorithms that, given the weights of a wide random Gaussian MLP, estimate its expected output with minimal MSE under a FLOP budget, improving on ARC's own white-box estimators that beat sampling. It is a contest announcement but defines a concrete, cheap empirical task.
- screener's follow-up note (often the screener's inference): Enter or analyse the challenge: design/benchmark white-box estimators versus Monte Carlo sampling at fixed FLOPs; test how methods degrade with depth/width or trained (non-random) weights.
- builds on: ARC paper on estimating outputs of wide random MLPs

