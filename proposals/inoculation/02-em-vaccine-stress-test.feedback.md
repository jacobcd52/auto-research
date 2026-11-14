# Feedback: "Does the emergent-misalignment 'vaccine' hold?" (proposal 02, inoculation cluster)

Reviewer verdict: **keep with tweaks** — the question is the obvious next one and nobody has answered it, but the
plan as written is too wide for a from-scratch reimplementation, its sham control is weak, and two of its five
datasets will sit at the floor. Narrow it and it is fundable.

## What I checked

| Claim in the proposal | Status |
|---|---|
| Post numbers (26→11%, 56→46%, 50.9→26%, 21.5→8.9%, narrow ~90%) | Correct, match the post text. |
| "One run, no CIs, no control, no code" | Correct. The post has no repo link and gives no hyperparameters for the EM loop at all (no steps, lr, optimiser, prompt count, sampling settings, or eval question set). |
| Author asks about side effects; Warncke suggests asymmetric entanglement | Correct (the post has only 2 comments). |
| HF datasets public and ungated, with the stated splits | Correct (`geodesic-research/sfm-…`, `anishkoppula/…insecure-code`, `longtermrisk/school-of-reward-hacks`, `allenai/tulu-3-sft-mixture`). |
| `ModelOrganismsForEM/Qwen2.5-7B-Instruct_*` adapters public | Correct, exactly three (medical, sports, financial); rank 32, rsLoRA, alpha 64, all attn+MLP modules. |
| Soligo et al. arXiv 2602.07852 | Exists ("Emergent Misalignment is Easy, Narrow Misalignment is Hard"); the framing is fair. |
| "GPT-4.1 study in which benign pre-fine-tuning weakened later EM" | Not verified by me either; remove it or find the source. |
| RunPod H100 PCIe $2.89/h; gpt-4.1-mini $0.40/$1.60 | Both correct today. OpenRouter lists no logprobs for gpt-4.1-mini (gpt-4o-mini at $0.15/$0.60 has them). |
| "No replication or stress test exists" | I found none: posts linking to it on LessWrong are only a Zvi roundup and Xenomirant's 17-karma post; the author has posted nothing since; arXiv title/abstract queries on emergent misalignment (about 40 titles since Feb 2026) show no replication. **Caveat: my web-search tool was out of budget, so this rests on the LessWrong GraphQL API and the arXiv API only.** The SPAR page could not be fetched. |

Two things the proposal misses:

- **The harmful-fine-tuning-defence literature.** Hardening base weights so later fine-tunes go less badly is an
  established line: Vaccine (arXiv 2402.01109 — a name collision with this proposal's title), RepNoise
  (2405.14577), TAR (2408.00761), Booster (2409.01586), and the critique by Qi et al. (2412.07097) showing such
  safeguards evaporate under small recipe changes (learning rate, seed, warm-up). A July 2026 paper (HarmAlign,
  2607.22929) claims an open-weight defence that "extends to emergent misalignment". Readers will ask how this
  differs; the answer (non-adversarial threat model, targets generalisation breadth, not learning of the narrow
  task) must be in the proposal, and Qi et al. sets the prior for the stress test: expect fragility.
- **The public EM code.** `clarifying-EM/model-organisms-for-EM` (readable via raw.githubusercontent.com) ships
  LoRA fine-tuning, full fine-tuning (`run_full_finetune.py`) and the eval/judge pipeline. The proposal lists the
  evaluation harness as "built"; it should be reused.

## 1. Would it get upvoted?

Borderline, around the 50 line. The parent post got 68 karma with 2 comments: liked, not widely engaged with. A
follow-up to it inherits a small audience (the inoculation / EM crowd: Riché, Warncke, Tan, Turner/Soligo,
Geodesic). Outcome-dependent estimate:

- Replicates, sham does not, survives ordinary recipe changes: 70–110. "A base model that keeps harmful
  fine-tunes narrow, with controls" is a headline result.
- Replicates but is generic damping, or breaks under a different learning rate / full fine-tuning: 40–70. Useful,
  and this cluster rewards deflationary controls (the conditionalization post got 80).
- "We could not reproduce it" from a reimplementation of an unreleased method with guessed hyperparameters:
  15–35. Readers and the author will reasonably say the implementation differs.

So the karma case depends on getting past the day-1 gate, which is the least certain step.

## 2. Naturalness

Mainline. The post is a one-run proof of concept, the screener's follow-up note and the author's own future-work
paragraph both point here, and seeds + a control + held-out recipes is exactly what a reader wants next. Not
contrived. Not done yet as far as I can tell (see caveat above). The scoop risk from the author's SPAR project is
real: that team has the working code and three months' head start; an independent replication still has value
but less novelty if they publish first.

The one un-natural part is the framing as "attacks". The post's use case is accidental EM from flawed data, not
an adversary. Framed adversarially, the project walks into the tamper-resistance literature where the known
answer is "breaks". Frame it as robustness across *ordinary* fine-tuning recipes.

## 3. Pre-mortem

How two days actually go:

- **Hours 0–10: building the loop.** Nothing is specified beyond one paragraph. The agents must guess the
  distillation steps, lr, optimiser, generation length and temperature for on-policy samples, KL direction, and
  which weights train. "Full-weight updates fit on one 80GB GPU in bf16" is shakier than stated: AdamW on 7.6B
  parameters is ~15 GB weights + 15 GB grads + 30 GB moments in bf16, plus the frozen teacher (15 GB) and
  activations — over or at 80 GB; and pure-bf16 weights silently drop small updates at lr ~1e-5. Realistic
  options are an H200 (141 GB, $5.29/h), 8-bit Adam / SGD, training a subset of layers, or the LoRA fallback. The
  fallback is itself a different method (a low-rank base update under a low-rank elicitor) and a null from it is
  not a non-replication of the post.
- **Hours 10–24: the gate.** "A quarter less broad misalignment after two rounds, 3 seeds" cannot be resolved at
  the proposed n. The post's baseline of 26% almost certainly comes from Turner et al.'s 8 main questions; on the
  48 pre-registered Betley questions rates are typically several times lower. At 480 samples and, say, 8%
  baseline, a 25% relative drop is 38 vs 29 events per run: inside seed-to-seed noise (the optimiser-sensitivity
  paper 2606.31591 reports a 7x spread in EM from training choices alone). The gate will produce an ambiguous
  reading and a judgment call.
- **Hours 24–48: grid.** Three vaccination runs take ~7 h each and must finish before the 90-run grid starts, so
  the grid, cue re-evaluation, two benign side-effect fine-tunes per base, MMLU and judge validation are squeezed
  into the last ~16 h on several parallel GPUs. Thirty of the 90 runs are full fine-tunes of a 15 GB model. Likely
  outcome: part of the grid runs, side effects get one seed, analysis is rushed.

Specific failure reasons, most likely first:

1. **Floor effects.** Insecure code produces ~1% or less EM on Qwen2.5-7B (2511.20104 reports 0.74% across open
   models; Betley et al. found Qwen weak); School of Reward Hacks is similarly low on small Qwen models. Two of
   five datasets cannot show a ratio. Full fine-tuning on 2,000 examples is also uncalibrated: 2607.04510 reports
   full SFT recruiting much less EM than low-rank LoRA on Qwen2.5. "Attack strength" on the x-axis is then not an
   ordering, and the vaccine/original ratio is 0/0 in many cells.
2. **Reimplementation does not reproduce the effect, uninterpretably** (wrong hyperparameters vs real fragility).
3. **Weak sham.** A LoRA trained on *correct* medical advice on a model that already gives correct advice is a
   near-zero perturbation, so the sham reduces to plain self-distillation. It does not test "the base learned to
   cancel any large LoRA-induced shift", which is the dull explanation in question. The sham would come out
   different from the vaccine for an uninteresting reason.
4. **Eval is in-distribution for the distillation.** The vaccine distils on general Tulu prompts; the broad-EM
   questions are general prompts. "Broad falls, narrow stays at 90%" may just mean "behaviour was pinned on
   Tulu-like prompts". Step 5 partly addresses this, but only with cues; there is no measurement at intermediate
   distance (e.g. a financial fine-tune asked medical or legal questions).
5. **Small n**: two attack seeds, two vaccine seeds, one sham seed. The proposal already concedes a 20% effect is
   unresolvable; given the post's effects are ~50% relative this is acceptable only where baselines exceed ~15%.

Forecast: clear positive (replicates, specific, fairly robust) 15%; clear and interesting negative (replicates
but generic damping / recipe-fragile / hidden behind cues) 30%; ambiguous mush (partial replication, noisy
ratios, half-run grid) 40%; fails to run or stops at the gate with an uninformative non-replication 15%.

## 4. Cost check

Unit prices are right. Quantities are optimistic but the total stays under the cap:

- Vaccination 20 GPU-h: plausible if the loop is a few thousand steps; unknown. An H200 for full-weight training
  nearly doubles the hourly rate. Call it $60–110.
- Grid at 15 min/run: fine for the default LoRA; rank-64 x 3 epochs is ~3x longer, and full fine-tunes with
  load/merge/generate overhead are 30–45 min. Realistic 40–50 GPU-h, ~$130.
- Debugging 25 GPU-h is thin for a from-scratch method; assume 40, ~$115.
- Judging ~$80 is consistent with the stated counts; gpt-4o-mini with logprobs would halve it and match the IA
  paper's scoring method.

My estimate for the plan as written: **$430–480**, leaving almost no margin. With the cuts below: **$280–330**.

## 5. Recommended changes (most important first)

1. **Cut the grid to what has a measurable baseline.** Datasets: bad-medical (in-procedure), financial and sports
   (held out). Drop insecure code and School of Reward Hacks unless a pilot on the original base shows >10% broad
   EM. Before vaccinating anything, run every recipe on the original base and keep only recipes with baseline
   broad EM above ~15%. Spend the saved runs on seeds (4–5 per cell).
2. **Match the post's evaluation first.** Reuse the model-organisms-for-EM eval code and its main question set
   with ~50 samples per question as the primary metric; check the public adapters reproduce roughly the post's
   baselines (26 / 51 / 21%). Report the 48 pre-registered questions as secondary. Restate the gate as a
   pre-computed power threshold (e.g. non-overlapping 95% intervals over ≥5 fresh-adapter seeds), not "a quarter
   less".
3. **Replace or supplement the sham.** Use an elicitor that produces a large, broad, benign shift of comparable
   adapter norm — e.g. a French or ALL-CAPS or strong-persona LoRA, or a norm-matched random LoRA — and run the
   identical distillation. Keep the correct-medical sham only as a "no perturbation" reference if budget allows.
4. **Replace "stronger attacks" with ordinary recipe variation.** Learning rate (x0.3, x3), epochs (1 vs 3), rank
   (8 / 32 / 64), optimiser, seed. That is what Qi et al. found breaks such defences and what a downstream user
   would actually vary. Keep one full-fine-tune condition only if its baseline passes change 1. Always report
   narrow-task performance and final training loss alongside, so a drop in broad EM is not just weaker learning.
5. **Resolve the memory plan before spending.** State the optimiser and precision for full-weight training and
   the GPU it needs; decide up front whether a LoRA-fallback result counts as a test of the post's method (I
   think not — label it as a variant).
6. **Add a cross-domain matrix** (each fine-tune evaluated on the other domains' held-out questions and on
   non-Tulu-like formats) to locate where "narrow" ends. It needs no extra training and directly tests failure
   reason 4.
7. **Trim side effects to one**: benign narrow-to-broad generalisation (French on one topic) on original,
   vaccine and sham bases. Drop villain role-play and MMLU to a footnote-level sanity check.
8. **Fix the related-work section**: cite the harmful-fine-tuning-defence line and Qi et al., state the
   non-adversarial threat model, drop the unverified GPT-4.1 claim, and rename away from "vaccine" or acknowledge
   Huang et al.
9. **Write-up discipline for a non-replication**: publish the full loop code and hyperparameter sweep so a null
   is checkable, and say plainly that it is a reimplementation.

If the funder wants only one project from this cluster, the proposer's own ranking (01 first) is reasonable:
this one has the largest upside and the largest chance of ending as an unconvincing null.
