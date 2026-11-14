# Feedback: 02 — "Did Claude overfit its benchmark world?"

Reviewer checks were run on 2026-11-14 by direct fetch (Hugging Face API and raw files, raw.githubusercontent.com,
LessWrong GraphQL, arXiv API). The WebSearch tool was unavailable to me (shared budget exhausted), so the
"has this been done" check rests on arXiv, Hugging Face and LessWrong only, not a general web search.

**Verdict: keep, with tweaks.** The plan is cheap, runnable and a mainline follow-up, but its most newsworthy
fact is one the proposal missed, and its most likely result as designed is an unsurprising "it mostly holds".

## What I verified

| Claim in the proposal | Status |
|---|---|
| Post content, caveats, Michaud / Conmy / Bussmann comments | Confirmed (post text and comment thread). Post is at 102 karma, 16 comments. |
| Repo with `train.py` / `sae.py`, one toggle per component, `MODEL` hard-coded to v1 | Confirmed via raw files. |
| v2 uploaded 2026-10-02; v1 README carries a deprecation notice for `scale_children_by_parent=False` | Confirmed. |
| 5-seed baselines public; Matryoshka F1 about 0.878 at L0 = 25 | Confirmed (`mat/l0-25/seed-0/stats.json`: F1 0.8775, MCC 0.793). |
| `sae-snapshot-panels` has a seeded gemma-2-2b Matryoshka panel at 300M tokens | Confirmed: `matryoshka-prefix-panel/gemma-2-2b/n-{1..4}/k-100/seed-*`, layer 12, width 32,768, snapshots to 300M tokens. |
| No follow-up from the author | Confirmed on LessWrong (nothing since March) and arXiv (only the original SynthSAEBench paper matches). |
| Later SAE releases are plain Matryoshka BatchTopK, "August 2026" | Architecture confirmed for `gemma-4-saes`. The date is wrong: the repos were created April-May 2026. |
| "Five components" | Incomplete: `train.py` has a sixth toggle, `use_lr_decay` (with an `ablation_no_lr_decay` entry), on by default. |

### The finding the proposal missed

The published baseline SAEs were **not trained on the world Claude hill-climbed**. The `runner_config.json` of
`decoderesearch/synth-sae-bench-16k-v1-saes/mat/l0-25/seed-0` embeds the synthetic-model config with
`"scale_children_by_parent": true` (output path `.../synthetic-v2-pyt-5-4/...`), while the uploaded v1 model
that `train.py` loads has `false`. So:

- The post's headline "0.88 to 0.97" very likely compares a baseline on the paper's world with a recipe on the
  mis-uploaded world. Nobody has published a Matryoshka baseline on v1, and I could not tell which world the
  "0.97 probe ceiling" was computed on.
- The proposer's "seed SD 0.002 on v1" was computed on SAEs from the correct-spec world, not v1.
- Step 1's gate ("checked against the published 0.878 baseline" on v1) is mis-specified. A baseline trained on
  v1 may legitimately not give 0.878.

This cuts both ways. It makes the v1-vs-v2 comparison more interesting than the proposal realises, since the
original gain may be partly an apples-to-oranges artefact. It also means the "gain retained" denominator (the v1
gain) has never been measured by anyone.

Caveat: I inferred this from config files and did not train anything. The baseline config also has
`correlation.seed: null`, so it is worth confirming that generating from that config reproduces the v2 upload.

## 1. Would it get upvoted?

Probably not above 50 as written; maybe with the changes below.

- The author's own technical SAE posts score 19-52 karma ("How much superposition is there?" 25, "Training
  Matching Pursuit SAEs on LLMs" 19, "JumpReLU training method is really good" 52). The 102 was for the
  "Claude did research overnight" hook, not for the architecture.
- A post saying "the recipe keeps 85% of its gain on other synthetic worlds; LLM check inconclusive" is a
  careful replication of a result most readers have already filed as "synthetic only". My estimate is 20-40
  karma.
- What could clear 50 is the auto-research framing with a sharp finding:
  - "the headline gain was measured against a baseline from a different world; the like-for-like gain is X";
  - "the gain collapses on the corrected benchmark";
  - "half the components only help on the buggy world".
- Readers who would care: SAE practitioners (a small and shrinking group), and people following the Conmy
  objection that autoresearch gains are noise or overfit. The second group is larger. The write-up should be
  aimed at them, with the SAE detail in service of "here is a measured case of how much an agent's hill-climb
  generalised".

## 2. Naturalness

Mainline.

- The author says his next step is "a suite of synthetic models with varying properties".
- Michaud asks for the same thing, Bussmann for adversarial benchmark parameters, and Conmy raises the
  held-out concern.
- I found no public result on v2, other worlds or LLMs.
- Eight months have passed and the author quietly fixed the benchmark in October, so there is a real chance he
  has private results (the proposal acknowledges this). The fact that his releases did not adopt the recipe
  hints that the LLM answer is already "no clear win".

The gemma-2-2b step is what readers most want, but it is the piece least likely to produce a clear answer.

## 3. Pre-mortem

How it plays out:

1. **Setup goes smoothly.** `uv sync` works, the default run reproduces about 0.97 on v1, and the recipe is
   wired to accept a `SyntheticModelConfig` (the runner accepts a config dict, as the baseline configs show).
   - `train.py` has no seed argument, so one must be plumbed through.
   - The repo's "baseline" is vanilla BatchTopK, so the Matryoshka baseline has to be configured by hand
     (matching the published config: no detach, no LR decay, widths 128/512/2048/4096).
2. **The baseline on v1 does not match 0.878.** The agents then either burn hours "diagnosing a reproduction
   failure" that is really the world mismatch, or discover it and get the best paragraph of the post.
3. **v2 and fresh draws are probably boring.** With 16k random features and fixed statistics, a new world seed
   is close to exchangeable. I expect retention near 100% on fresh draws. v2 is the one real unknown, because
   child magnitudes scaled by parent change the hierarchy signal that Matryoshka and frequency sorting exploit.
4. **Shifted worlds give a mixed picture that is hard to read.**
   - Changing the Zipf exponent or hidden size changes the true L0 (34.5 in the default world) and the right K.
   - K = 25, the 60-to-25 anneal and the Matryoshka widths are fixed, so both baseline and recipe are mis-tuned
     by different amounts.
   - "Gain retained" is a ratio and becomes unstable when the baseline-to-ceiling gap shrinks or grows.
   - With 2 seeds and one world per factor level, an eta-versus-world interaction is anecdotal.
5. **The LLM step is at risk.**
   - `google/gemma-2-2b` is gated on Hugging Face (`gated: manual`), and the programme rules out anything
     needing accounts or approvals. An ungated mirror with a model-name override is a fragile workaround.
   - The panel is width 32k, K = 100, with JumpReLU-format inference, on a pretokenised dataset. The custom
     `ListaMatryoshkaTrainingSAE` has to be wired into the LLM runner and its inference form (the LISTA step)
     made to work with sae-probes.
   - Six runs at about 3-4 hours each is 18-24 GPU-hours on day 2 alone, unless several SAEs are trained on a
     shared activation stream.
   - The author already reports that eta = 0.3 breaks and lower eta is indistinguishable from noise, and his
     own audit says sae-probes barely separates same-family variants. Two seeds will give mush.

Wall-clock: 126 runs at 0.5 hours is 63 GPU-hours, more than 48 hours on one GPU. The plan never states
parallelism. It is easy to fix (the SAEs are tiny; run 4-6 per GPU or rent 3-4 cheap GPUs) but must be planned.

Rough outcome probabilities:

| Outcome | Probability |
|---|---|
| Clear and surprising (gain collapses on v2, or the like-for-like v1 gain is much smaller than 0.09) | 20% |
| Clear but unsurprising (holds on v2 and fresh draws, degrades in some shifted worlds; the world mismatch is a footnote) | 45% |
| Ambiguous mush (shifted worlds confounded by L0 and K; LLM null) | 25% |
| Fails to run or reproduce | 10% |

## 4. Cost check

The estimate is realistic and probably high.

- Synthetic runs fit on 48 GB cards at $0.35-0.80/h, which gives $25-60 rather than $182. I took those prices
  from the proposer's notes and did not re-check them.
- If the LLM step is kept, it costs about $60-90 including activation generation.
- My estimate is **$120-250** all-in with reruns. $330 is a safe ceiling.
- The constraint is wall-clock and parallelism, not money.

## 5. Recommended changes (in priority order)

1. **Make the world mismatch the first experiment and the lead.** In the first hours, train the Matryoshka
   baseline (5 seeds, cheap) and the probe ceiling on both v1 and v2, and the recipe on both. Report the
   like-for-like gain on each. Fix the step 1 gate:
   - recipe on v1 should be about 0.97;
   - baseline on v2 should be about 0.878;
   - baseline on v1 is an unknown to be measured.
   Confirm that the world generated from the baseline config equals the v2 upload.
2. **Fix the component list.** There are six toggles, including LR decay. Either ablate LR decay or give it to
   the baseline too, and say explicitly what the baseline is. Consider also reporting vanilla BatchTopK, since
   that is the repo's own baseline.
3. **Shrink fresh draws, spend on shifts.** One or two fresh world seeds are enough for a predictable result.
   Use the saved runs to give each shifted world an L0-matched comparison (set K from the world's true L0, or
   run a 3-point K sweep for baseline and recipe) and 3 seeds. Without this the shifted-world result is
   uninterpretable.
4. **Report absolute gains and gap-closed, not only the "retained" ratio.** Pre-register thresholds on
   gap-closed. Drop the 50% / 80% ratio rule or keep it as secondary.
5. **Add a cheap adversarial arm (Bussmann's suggestion) in place of part of the grid.** A small random or
   agent-driven search over world parameters for where recipe minus baseline is smallest. "Here is a
   reasonable world where the recipe loses to the baseline" is far more upvotable than a grid of small deltas.
6. **Decide on the LLM step up front.** Either drop it and put the money into items 3 and 5, or commit to it:
   - check gated-model access on day 0;
   - state the wiring work;
   - train the three variants on a shared activation buffer;
   - use at least 3 seeds to match the panel.
   As a gated, 2-seed afterthought it will produce a paragraph of caveats. My recommendation is to drop it from
   stage 1.
7. **State the parallelism plan.** Give runs per GPU and number of GPUs, and time the first run before
   committing to the grid.
8. **Frame the write-up for the auto-research audience.** Contact with the original author is not possible for
   the agents, so say plainly that he may hold private results. Correct the "August 2026" release date.
