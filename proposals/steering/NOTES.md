# NOTES: cluster `steering` (Steering reliability)

Research lead notes, 2026-11-14. Everything below was read or looked up today unless marked "unverified".

**Search caveat.** The shared WebSearch budget for this run was already exhausted when I started (all three
queries returned "budget used up"), so the related-work check used only direct sources: the arXiv export API
(keyword queries + abstracts), the LessWrong GraphQL API (posts and comments), the Hugging Face API, the OpenRouter
price list and the RunPod pricing page. github.com was not inspected. A reviser with search budget should re-run
two checks: (i) any LessWrong/arXiv replication of the Bostock experiment after 2026-04-05; (ii) any conceptor
experiment on the Assistant Axis role vectors after 2026-07-07.

## 1. The two posts (both read in full, with comments)

### 1a. Steering Might Stop Working Soon (fuzfbz8TbuLcskGCx, 2026-04-05, J Bostock, 68 karma)
- Claim: the window between "steering too weak, model recovers" and "steering so strong capability collapses"
  narrows with capability and will close; matters for steering against eval awareness.
- Experiment (Claude-written, quick): one steering vector per question from ONE contrastive sentence pair
  ("The caracara is a(n) [owl/hawk]", difference at the final word), added while asking "What type of bird is a
  caracara?" (truth: falcon). Sweep of steering strength across the Gemma 3 sizes. Metric: fraction of responses
  containing the target word, plotted with "1 - score on five simple python coding questions".
  Result: smaller models steerable; the larger ones "became incoherent before they started to report the wrong
  answer". Two more questions (Sydney/Canberra, Venus/Mercury) on the three smaller models only: same ordering.
  Total: 3 facts, 5 coding questions, one model family. Layer choice, norm scaling and sample counts are not
  stated in the post. Code: https://github.com/jonathanbostock/activation-steering-sweep (not inspected).
- Author's own caveats/hypotheses (post + comments): "This steering worked worse than I expected"; "steering
  against a very clear, known fact might be more harmful than ... a hazy, inferred fact like 'are we in an eval'";
  in comments: "I actually suspect the effect I've seen with Gemma is (mostly) the result of larger models just
  having more powerful factual recall circuits ... more redundant to noise"; "Most of my money is still on
  'steering to produce a specific false fact is particularly difficult' ... possibly with a side of 'I'm not very
  good at steering'. It's the relative difficulty of steering the Gemma models that actually worries me";
  "I would also like to see a more rigorous examination of better steering methods"; "Ideally I'd like to see
  some better experiments on resistance in even larger models."
- Comments by others: Curt Tigges (needs rigorous evaluation; additive steering may push larger models
  off-manifold; show why better methods can't keep up). wassname (use more layers, more diverse questions, repeng
  https://github.com/vgel/repeng; says his AntiPaSTO S-space steering shows no clear scaling wall on Gemma-3
  270M/1B/4B/12B, "Table 12"; AxBench says activation addition does not beat prompting). Shankar Sivarajan
  (Gemma-specific safety training as an alternative explanation). Kurt Pieper (resistance is downstream of
  self-repair).
- No comment reports a replication.

### 1b. A conceptor by any other name (9aZYJinAyxequjQbn, 2026-07-07, Keenan Pepper, 60 karma)
- No experiments. Conceptor C = R(R + a^-2 I)^-1 with R the correlation matrix of concept activations; each
  eigen-direction with eigenvalue lambda is kept with weight lambda/(lambda + a^-2). Same object as Wiener filter,
  ridge shrinkage operator, Tikhonov filter factors; a "soft projection".
- Motivating example: "persona transplantation" with the ~275 Assistant Axis role vectors (mean-centred).
  Intervention x' = x + C(d - x), with x the recipient activation and d the donor. Claims: the full 274-dim span is
  "a brutal butchery" (noise directions), top-k PCA has an arbitrary hard cutoff, the conceptor is the natural
  soft version; the transplant should carry persona but NOT the donor's topic, message length or language
  ("act like a pirate but keep speaking Chinese"). None of this is tested.
- Other suggestions: one grand conceptor per broad concept (persona, emotion, intent); a programme of iteratively
  subtracting known concept subspaces and characterising the remainder; aperture chosen by Jaeger's criterion, a
  sweep, or a target quota (quota = trace(C)/d); Boolean AND/OR/NOT.
- Only one comment (finance covariance shrinkage); no follow-up reported.

## 2. Related work checked

- **Scaling laws for activation steering with Llama 2 models and refusal mechanisms** (arXiv 2507.11771, Jul 2025):
  CAA on Llama 2 7B/13B/70B, refusal A/B questions; "effectiveness of CAA diminishes with model size". One
  family, one behaviour, no capability-cost axis, no belief-strength control. Closest precedent for proposal 01.
- **Endogenous Resistance to Activation Steering** (arXiv 2602.06941v3): SAE-latent steering; explicit
  mid-generation self-correction in Llama-3.3-70B at 3.8% of trials, rarer in smaller Llama-3/Gemma-2; 26 SAE
  latents, ablation cuts multi-attempt rate 25%. Code https://github.com/agencyenterprise/endogenous-steering-resistance.
  It measures verbal recovery from off-topic steering, not the dose-response window.
- **Steering Awareness** (arXiv 2511.21399): fine-tuned detection of injected vectors up to 95.5%; detection does
  NOT confer resistance (detection-trained models are more steerable).
- Capability cost of steering: arXiv 2602.04903 (Goodfire Auto Steer: MMLU 66->46% on Llama-8B, 87->73% on
  Llama-70B; coherence 4.62->2.24 vs 4.94->3.89, i.e. the 70B model degraded LESS), 2603.13249 (attention-head
  persona steering to reduce coherence loss), 2610.07722 ("Does Steering Break Your Model?", Oct 2026, evaluation
  suite; abstract not read in detail, title-level only).
- Hua et al., arXiv 2510.20487 (steering eval-aware organism), and the cluster `eval-awareness` proposals
  (`03-through-or-around.md` covers control vectors for eval-awareness steering; not duplicated here).
- **Conceptor steering literature**: Postmus & Abreu (arXiv 2410.16314; code github.com/jorispos/conceptorsteering;
  function-vector tasks on small models, beats activation addition); Triantafyllopoulos et al. (arXiv 2605.04980;
  bipolar conceptors, quota as layer diagnostic, r up to 0.96, Boolean composition, "fewer degenerate outputs");
  COAST (arXiv 2605.17144; robots).
- **When a Conceptor Complement Becomes Gain** (arXiv 2610.16325v2, Oct 2026): for a target-centred scaled conceptor
  complement (NOT-style suppression), removing the fitted covariance filter while keeping centre and gain barely
  matters: the matrix correction is 0.093%-7.815% of the matched-control displacement; 480 paired comparisons show
  no consistent extra suppression from the matrix. This is a direct warning that "conceptor beats baseline" results
  can be due to the centre/gain, not the soft filter. It studies suppression, not transplantation, and not the role
  vectors. Proposal 02 adopts its attribution logic.
- **Assistant Axis** (arXiv 2601.10387; code https://github.com/safety-research/assistant-axis): released vectors
  at https://huggingface.co/datasets/lu-christina/assistant-axis-vectors (MIT). Verified via HF API: folders
  `gemma-2-27b`, `qwen-3-32b`, `llama-3.3-70b`, each with `role_vectors/` (275 .pt files for gemma-2-27b, e.g.
  `accountant.pt`, 425,534 bytes each, consistent with all 46 layers x 4608 dims in float16), `trait_vectors/`,
  `assistant_axis.pt`, `default_vector.pt` (+ `capping_config.pt` for Qwen and Llama). Community recomputations:
  `Butanium/gemma-3-4b-it-assistant-axis`, `Butanium/qwen-2.5-7b-instruct-assistant-axis`,
  `timf34/gemma-assistant-axis-vectors`, `dungnv/assistant-axis-qwen-3-14b` (contents not verified).
- Role Steering for Social Simulations (arXiv 2608.00023): role-specific mean-difference directions on OLMo-3-7B
  with the 275-role inventory; no conceptors, no collateral-damage measurement.
- arXiv API queries for "persona AND conceptor" returned nothing; "conceptor AND steering" returned only the four
  papers above. I found no empirical test of the post's persona-transplant claim.

## 3. Verified resources and prices

- Models (HF API, today): `Qwen/Qwen3-0.6B, -1.7B, -4B, -8B, -14B, -32B` ungated. `google/gemma-3-{270m,1b,4b,12b,27b}-it`
  and `google/gemma-2-27b-it` are gated ("manual" licence click, needs an account); ungated mirrors exist:
  `unsloth/gemma-3-1b-it`, `unsloth/gemma-3-27b-it`, `unsloth/gemma-2-27b-it` (other unsloth Gemma 3 sizes not
  individually checked). Ungated Llama mirrors: `unsloth/Llama-3.2-1B-Instruct`, `unsloth/Llama-3.2-3B-Instruct`,
  `unsloth/Meta-Llama-3.1-8B-Instruct`, `unsloth/Llama-3.3-70B-Instruct`.
- RunPod (https://www.runpod.io/pricing, fetched today), community / secure per hour: H100 PCIe 80GB $1.99 / $2.89;
  A100 PCIe 80GB $1.19 / $2.09; L40S 48GB $0.79 / $1.09; RTX A6000 48GB $0.33 / $0.69; H100 NVL $2.59 / $3.19.
- OpenRouter (API price list, today), $ per M input / output tokens: `anthropic/claude-haiku-5.5` 0.10 / 0.50;
  `anthropic/claude-sonnet-5.5` 2 / 10; `openai/gpt-5-mini` 0.25 / 2; `google/gemini-3-flash-preview` 0.5 / 3;
  `google/gemma-3-27b-it` 0.08 / 0.35.

## 4. Brainstorm

Kept:
1. **Is the scale effect a confidence effect?** Re-run the steering-window measurement across three families with
   many facts, proper vectors and layer sweeps, and add a belief-strength dial (in-context facts with k supporting
   statements, plus stratification by the model's own prior confidence). Tests the author's own alternative
   explanation. Cheap, forward-pass dominated. -> proposal 01.
2. **Persona transplant: conceptor vs hard subspace vs role-vector addition**, on the released role vectors, with
   deliberately confounded donors (language, topic, length) and spectrum-matched controls. Direct test of the
   post's only concrete claim. -> proposal 02.

Rejected or folded in:
3. Straight replication of Bostock with more questions on Gemma 3 only. Folded into 01; alone it cannot separate
   "bigger" from "more confident" or from "Gemma-specific".
4. Steering against eval awareness across model sizes. Needs eval-aware organisms at several sizes (only one public
   organism family); overlaps cluster `eval-awareness` proposal 03. Rejected.
5. ESR (verbal self-correction) rate as a function of scale with contrastive vectors. Explicit ESR is 3.8% at 70B
   and lower elsewhere, so the n needed across sizes is large and 70B hosting dominates cost. Stage 2 of 01 at most.
6. Compare better methods across scale (SAE-feature clamping, AntiPaSTO, CHaRS, activation-diffusion). SAEs are not
   available at matched quality across sizes/families; too many fragile pipelines for two days. A light version
   (multi-layer and mean-over-many-pairs vectors vs the single-pair vector) is inside 01.
7. Fine-tune steering awareness and test whether it narrows the window. Already answered: arXiv 2511.21399 found
   detection does not confer resistance.
8. Fine-tune a false fact (SDF/LoRA) vs steer it: which is cheaper in capability at each size? Interesting but a
   different project (belongs to cluster `sdf`), and fine-tuning 27B+ models multiplies cost.
9. Conceptor "subtract known concepts and characterise the residue" programme. Open-ended, no crisp success
   criterion in two days. Rejected.
10. Conceptor Boolean algebra on persona AND emotion. Needs emotion-concept vectors (not verified public) and a
    second attribution study; stage 2 of 02.
11. Conceptor (NOT persona) as a jailbreak defence vs activation capping from the Assistant Axis paper. Plausible,
    but 2610.16325 already shows complement-style suppression is mostly gain, and it needs a persona-jailbreak
    benchmark. Stage 2 of 02.
12. Quota as a layer-selection diagnostic for persona. Already the headline of 2605.04980 for other concepts;
    incremental.
13. Whitened (anisotropic-noise) conceptor from the post's footnote. Included as one arm in 02 rather than its own
    project.

Why two proposals and not fewer: both posts make one concrete, untested empirical claim each, both tests are
mostly forward passes on public checkpoints with public vectors, and each is informative in either direction.
