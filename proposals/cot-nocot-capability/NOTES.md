# NOTES — cluster `cot-nocot-capability` (no-CoT / opaque reasoning capability)

Written 2026-11-14. All 15 cluster posts read in full via `scripts/get_post.py`; follow-ups found through the
LessWrong GraphQL API (all posts since 2026-08-25, title-filtered) and read in part. GitHub is blocked from the
drafting sandbox (HTTP 403 through the proxy), so repo contents were NOT inspected; repo URLs below are as given
in the posts. Hugging Face, arXiv and OpenRouter were reachable and the facts from them are verified.

## 1. What the cluster says (reading notes)

World context: GPT-6 Astra (released ~early Sept 2026) is widely believed to be a looped / recurrent-depth
transformer; OpenAI says "depth of the computation graph ... is within a factor of two of GPT-4". GPT-6.1 Sol is
believed to be "Astra Minor" (also looped); GPT-6 Sol and GPT-5.6 Sol are not. Gemini 4 Argon is also rumoured
looped. Astra/6.1 Sol do not expose `reasoning: none`; everyone uses `reasoning_effort=low` + a strict
"immediate-recall" system prompt and verifies `reasoning_tokens == 0`. Astra does not accept a temperature.

| post | key facts |
|---|---|
| Long, "Filler tokens don't allow sequential reasoning" (KFkKPbuYCWc9ygpRp) | Conceptual: in a bounded-depth transformer, filler positions add parallel width, never serial depth (any path is <= L layers). No experiments. |
| Greenblatt, filler/repeats math (NYzYJ2WoB74E6uj9L) | Opus 4.5 45%->51% on 907 easy comp-math problems with filler "1..300" or 5 repeats; effect from Opus 3 onward; gen-arithmetic too. Open question he states: is the gain only arithmetic / parallel? Code: github.com/rgreenblatt/no_cot_math_public |
| Greenblatt, no-CoT math horizon (Ty5Bmg7P6Tciy2uj2) | Opus 4.5 3.5 min; doubling ~9 months; human times are Opus-estimated. |
| Greenblatt, 2/3-hop (aYtrLhoZtCKZnfBvA) | Gemini 3 Pro 60%/34% 2-/3-hop with filler; all ~chance on 4-hop; N-addend parallel variant is easier; in-context table lookup n-hop. Code + dataset generator: github.com/rgreenblatt/multi_hop, github.com/rgreenblatt/compose_facts (datasets removed, regenerable). |
| Think Fast (SieLowPgNgRSPGhFw, arXiv 2606.07157) | 43 benchmarks, 14 models, GPT-5.5 ~3 min, doubling 373 d. Datasets held back ("available on request") -> not usable by us. |
| RohanS (FsCkkoGsNmPzFKRhg) | 24 hand-written multihop prompts, Astra >> 5.6 Sol; invites a systematic version (since done by Corry). |
| Ward & Gould, Astra TH (ntKx9YHWCwxSeGbRB) | Astra saturates 10/37 benchmarks; TH 8 min–1 h. Filler helps comp math +12 pp, hash +4.5 pp; hurts "scheming numeric". |
| Xu, Prasanna, Westover (uvhuZHFtrgk8kNiZc) | Astra 4-hop ~10–20% -> ~50% with up to 4,096 filler tokens; AIME 60–70% -> 90%, peak ~8,192. Dots/counting/repeats similar. Footnote: filler works if appended or prefilled in the assistant turn, NOT if prepended before the task. Comment by Xu: asking Astra to *output* e.g. 1000 dots before the answer gives similar results to input filler (not shown in post). Code: github.com/redwoodresearch/astra-filler-tokens. AIME++: huggingface.co/datasets/ulamai/AIME-Plus-Plus. |
| Nanda NCRI (eRmzz8J8Qkzqvzrgg) | 19 mostly synthetic tasks, benchmark-stitched index; Astra serial depth 7.2 arithmetic steps vs 4.1; multi-hop facts 3.6 vs 2.8. Code/data: github.com/neelnanda-io/nocot-bench (ELICITATION.md has per-model no-CoT recipes). Appendix on open looped models (Huginn-0125, Ouro-1.4B/2.6B, Nanbeige4.2-3B): noisy. |
| MBaert speculative depth (WFc3NkuPaYFrYuaZd) | LatentMathBench (github.com/MaartenBaert/LatentMathBench): math-4, swap-N, bitwise-N, bool-N. Astra's bool-26 50% horizon 54 steps drops to 11 with xor-only (shortcut-free). Success tracks "speculative depth". In-order SSA: filler no effect; shuffled SSA: filler recovers some. Open questions listed by author: error-structure analysis, output-side filler ("tried, not much difference"), open-weight looped models. Commenters (Xu, hillz, AprilSR) ask for tasks maximally resistant to speculative shortcuts and how they interact with filler. |
| Corry (tz5WvDouXKbiWJG8B) | Systematic replication: Astra 4-hop 31% -> 63% with filler/repeats, monotone to r=40 / f=1000. Harness: github.com/christinecorry/no-cot-harness (elicitation table per model: append/prefill/forced tool; strict prompt). |
| MBaert BP (PAHqDoFrp9fybcSn2) | Randomised BCH-2 parity problems ("exactly 2 of these are incorrect" + xor constraints), soft version with priors; Astra improves with filler; success correlates with exact-marginal/MAP gap; cached-prefix trick gives per-filler-count confidence "trajectories" that oscillate then converge to exact marginals; "far from textbook BP". Says he is at the limit of black-box methods. No comparison against an actual BP run. |
| Arike (LqSZZAriGqgsGDQe3) | 6.1 Sol closes 80% of the 6 Sol -> Astra gap. |
| Gould & Mann, Jev (QW2kPrAyZQvRtBXHG) | Non-autoregressive "System One" model; good monitor AUROC, bad multi-step. $0.042/M input. |
| Roe (yEdknsLwbooQAnxX6) | Single-token "A at rate p" with a UUID: Astra and 6.1 Sol are calibrated with 3–5 repeats or filler, and give *identical* answers per UUID, consistent with "first 8 hex chars / 2^32 < p". Implicit prompt -> never A. Comment thread: Fabien Roger asked for natural entropy (SWE transcript); Roe ran it: models struggle. Commenter jonathanbreitg: strategy must be a simple Schelling rule -> auditors could sample extremal seeds. Code: github.com/zroe1/no-cot-harness/tree/main/low_probs. Builds on Serrano et al. arXiv 2603.02202. |

## 2. Follow-ups that already exist (checked 2026-11-14)

- **Looping a transformer increases no-CoT capabilities more than general capabilities** (Westover et al., uxsDuWWHNTpKrsF6P, 2026-11-12): NVIDIA Dory 1.0 4B, loops 1–8, NCRI rises ~18 pts with loops, bpb/mini-ECI barely; "recurrent-Dory" (last-loop KV sharing) gets most NCRI uplift at 2 loops and learns all-filler CoT under RL. Appendix A: plain filler never helps Dory; question repeats help only when looped. => "run NCRI on an open looped model" is DONE.
- **Deep recurrent models are less robustly CoT-monitorable in a toy setting** (Kuhn, 5guQJSqstkjgys3PE).
- **A Key-Position Confound in no-cot-bench** (agastyasridharan, ehF4kej38fkhb5cT3): key-last variants cost 6.1 Sol ~16% of depth; code github.com/agastyasridharan/nocot-bench. No filler conditions.
- **LLMs can learn (some) multi-step reasoning on filler tokens** (Schulz, EHkwCDAmhWPAWEziM): LoRA-trained filler reasoning on Qwen3.6-35B-A3B / gpt-oss-20b. Training-based, not elicitation.
- **Controllable-CoT leads to covert reasoning capabilities** (Cant, CPJ2kYRKo77ucZEEG): Astra told to reason only in dots / unrelated scenes / punctuation codes inside its reasoning; dots give "impressive" lookup-chain success; reasoning content cannot be verified (encrypted), dots are variable-length.
- **Astra uses some of its no-CoT capability in practice** (StevenW, kaoeXZkWhNELmgbKg): short CoTs at effort=low.
- **Mapping the boundary of latent planning** (Arnav, jwpGAt955PCMMLRS9): no-CoT planning suite, Astra 41.7% vs 12.8%.
- **Small LLMs perform no-CoT two-hop reasoning on synthetic facts with real bridges** (CdWbCvKEoK39L3DzK).
- **Single forward pass evals on Fable, Opus 5 and GPT-5.6-Sol** (Corry, bxaWTNrdgJpkLXmgm).
- **Shadow Computation Threatens CoT Monitorability** (Skye, 5tyzgTLnNn8qB9rev) and **Recurrent KV-cache sharing may undermine the bounded-depth argument** (MBaert, LaR7joZu4QyaM7hqq): conceptual — cross-token latent paths make opaque depth grow with tokens.
- Karma reality check: September Astra posts got 100–236; follow-ups since mid-October get 10–50 (Westover 48 after 2 days, key-position 28, Schulz 10). A new post needs a sharp headline, not another replication.

## 3. Verified resources and prices

OpenRouter (`/api/v1/models`, 2026-11-14), $ per 1M tokens input / output (cache read):
- openai/gpt-6-astra 10 / 50 (1.00); `:batch` 5 / 25
- openai/gpt-6.1-sol 2 / 10 (0.10); `:batch` 1 / 5
- openai/gpt-6-sol 2 / 10; openai/gpt-5.6-sol 4 / 20; openai/gpt-6-luna 0.10 / 0.50
- google/gemini-4-argon 2 / 10; google/gemini-3.8-flash 0.825 / 4.125
- anthropic/claude-fable-5.1 10 / 50; claude-fable-5.2 8 / 40; claude-opus-5.5 4 / 20
- moonshotai/kimi-k3 0.19 / 16; deepseek/deepseek-v4-pro 0.90 / 1.50; qwen/qwen3.5-397b-a17b 0.60 / 3.60
- typesafe/jev-router: dynamic pricing (post says $0.042/M input).

Open-weight looped models on Hugging Face (verified to exist, ungated):
- nvidia/NVIDIA-Nemotron-Labs-Dory1.0-4B-BF16 (4B; 8 input + 20 recurrent + 8 output layers; `n_recurrent_loops`
  1–4 recommended, up to 8 works; `recurrent_kv_cache_mode` = `per_loop` | `last_loop`; vLLM and llama.cpp recipes
  in the model card; OpenMDW-1.1 licence).
- ByteDance/Ouro-2.6B (+ -Thinking), tomg-group-umd/huginn-0125.

GPU rental (pricing pages, 2026-11-14): Lambda A6000 48 GB $1.09/h; RunPod A100 PCIe $2.09/h, H100 PCIe $2.89/h.

Not verified: contents of the GitHub repos (blocked here). All task generators involved are simple enough to
re-implement from the posts' descriptions in a few hours if a repo turns out to be unusable.

## 4. Brainstorm (all candidates, with verdicts)

1. **Do filler tokens buy serial depth? Depth-horizon scaling on shortcut-resistant, key-last tasks, input vs
   output filler.** Direct test of Long's claim on the models where filler matters most; requested by commenters
   on MBaert's post; nobody has combined key-last + shortcut-free + filler. Cheap, black-box, two-sided. **PROPOSAL 01.**
2. **Rare-action rule is a predictable Schelling rule: characterise it, measure cross-model agreement, test an
   auditor "seed-crafting" exploit and the model's ability to follow less predictable rules.** Builds on Roe; the
   natural-entropy variant is already done (fails) so we avoid it; the auditing angle was only raised in a
   comment. Cheap, clean. **PROPOSAL 02.**
3. **Is it belief propagation? Double dissociation between loopy BP, exact marginals and enumeration on MBaert's
   BCH tasks.** Author explicitly out of black-box ideas; screener's suggestion; cheap. **PROPOSAL 03.**
4. **White-box: why do question repeats help only a looped model (Dory)?** Attention knock-outs and patching
   across copies and loops. Open-weight, nobody has done the mechanism; risk: small/noisy effect. **PROPOSAL 04.**
5. Run NCRI / Think Fast on open-weight looped models with varied loop count — DONE (Westover, Nanda appendix). Rejected.
6. Systematic version of RohanS's hand-written multihop set — DONE (Corry). Rejected.
7. Unsaturate the no-CoT time-horizon suite with longer tasks — needs human time baselines and the private Think
   Fast data; NCRI already sidesteps it. Rejected (not achievable in 2 days, weak novelty).
8. Real human baselines for Greenblatt's math horizon — human-subject work. Rejected.
9. Self-generated filler / unrelated CoT as cover for hidden reasoning in Astra — largely DONE (Cant; Xu comment).
   A dual-task variant with a monitor is possible but incremental. Rejected as a separate proposal; the
   prescribed-content output-filler arm of proposal 01 covers the informative part.
10. Natural entropy sources for rare actions — DONE in Roe's comment thread (fails). Folded into 02 only as a
    held-out transfer check.
11. Filler-token uplift on 6.1 Sol — DONE (MBaert update, Roe).
12. Train filler reasoning into open models — DONE (Schulz; Kuhn; Westover Result 3). Rejected.
13. Jev: transfer of monitor improvements to frontier monitors / adversarial robustness — belongs to the control
    cluster; Jev API has dynamic pricing and a 32k context; several Jev posts exist already. Rejected here.
14. Error-structure analysis of Astra's LatentMathBench failures — author says he will do it; folded into 01 as a
    secondary analysis (which step the wrong answers correspond to).
15. No-CoT eval-awareness / sandbagging-to-target suite — new benchmark from scratch, hard to validate in 2 days. Rejected.
16. Gemini 4 Argon no-CoT evals — GDM's own safety report covers it; included only as a comparison model in 01/02.
17. Extend multi-hop dataset diversity / higher hop counts — incremental. Rejected.
18. NCRI vs CoT-controllability on more models — Nanda did 34 open models (no relation). Rejected.
19. Positive-control calibration of proposal 01 on recurrent-Dory (does real cross-token recurrence show up as
    horizon growth?) — kept as a small optional arm in 01 and the core of its stage 2.

## 5. Why four proposals

The cluster is large and heavily mined; most "obvious" replications are done. The four proposals each target a
question that the posts or their comment threads pose explicitly and that is still unanswered, and they are
distinct: 01 = what filler tokens buy (serial vs parallel), 02 = control implications of single-pass rare
actions, 03 = which inference algorithm, 04 = white-box mechanism in an open looped model. 01 is the strongest
(two-sided, central to the debate); 04 is the riskiest.
