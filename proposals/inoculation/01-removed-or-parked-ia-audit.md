# Removed or parked? Auditing inoculation-adapter models with the triggers that system prompts cannot reach
cluster: inoculation | stage-1 cost: $340 | follows up: "Inoculation Adapters Improve Upon Inoculation Prompting" (qd3qhxgEmQAXR2ZK5); "Engineering the Generalisation Landscape of LLMs" (ueXaSxeunPjA6kxua); "Conditionalization Confounds Inoculation Prompting Results" (znW7FmyF2HX9x29rA)

## 1. What the prior work showed
Training data often teaches a desired and an undesired trait at once. *Inoculation prompting* (IP) adds a system
prompt that requests the undesired trait during training and drops it at deployment, so the model has less reason
to absorb the trait. Riché & Warncke (Feb 2026) showed that part of this effect is *conditionalization*: the trait
is learned but tied to the prompt, and Dubiński et al. (arXiv 2604.25891) showed that prompts merely resembling
the inoculation prompt bring it back.

*Inoculation adapters* (IA; Riché, Tan, Kohonen, Warncke, arXiv 2606.30252) replace the prompt with a frozen LoRA
that already carries the undesired trait. A fresh task LoRA is trained on top, and only the task LoRA is deployed.
Across nine setups IA suppresses the undesired trait more than IP, and its headline safety claim is "fewer
surprising backdoors": on three setups, vanilla IA shows no leak under six categories of evaluation *system
prompts*, and a Petri search over *user prompts* finds nothing new. The authors ask in their Discussion: "Is
conditional misalignment removed, or has the trigger merely become harder to find?" They also report that direct
requests for the trait work better on IA models than on a model trained on clean data.

A third post gives a reason to doubt a prompt-only audit. Ratnam (Jul 2026) trained base weights under a frozen
trait LoRA and found that what was learned fires whenever the LoRA's internal state is recreated: by prefilled
text, a steering vector, few-shot examples, or a fresh adapter. The one route that failed was a system prompt.
An IA task adapter is also trained under a frozen trait LoRA, and the IA author says in the comments that the
desired trait is partly "learned conditional on the undesired ones".

Already done: system-prompt and Petri probes (IA paper); a toy replication on Qwen2.5-1.5B with the same
system-prompt probes (Xenomirant, Sept 2026); an activation-level look at IP models, not IA models (Patel, Aug
2026). The IA paper's text and a search of LessWrong and arXiv (2026-11-14) show no probe of IA models with
few-shot, prefill, steering, re-attached or fresh adapters, or relearning speed.

## 2. Question and why it matters
After inoculation-adapter training, is the undesired trait absent from the deployed model, or is it stored behind
the adapter's internal state where prompts cannot reach but other routes can?

If it is parked, IA's advantage over IP holds for one kind of trigger only, and the trait may return through
conversations that drift into it, user prefills, or a small later fine-tune. If it is absent under probes much
stronger than the paper's, that is the first solid evidence that an inoculation method removes a trait instead of
hiding it.

## 3. Stage 1 plan
**Reused:** the IA paper's two Qwen2.5-7B-Instruct setups and hyperparameters (rsLoRA rank 32, alpha 16, one
epoch, batch 8; lr 3e-5 for B1 and 1e-4 for B2), its backdoor system prompts (Appendix E.1), the 48 pre-registered
emergent-misalignment (EM) questions of Betley et al., and public data: Alpaca, UltraChat, and the Turner et al.
datasets as plain parquet at `huggingface.co/datasets/geodesic-research/sfm-emergent-misalignment-training-data`.
**Built:** the IA training loop (no code is released; it is two stacked PEFT adapters with one frozen), French
translations of the task data, and the probe harness.

Setups, both with French as the desired trait:
- **S1 (paper's B1):** undesired = ALL-CAPS. Task data: 5,000 Alpaca answers in capitalised French. IA data:
  5,000 UltraChat answers upper-cased. Scoring is rule-based (fraction of upper-case letters; language detector).
- **S2 (paper's B2):** undesired = EM. Task data: 5,000 extreme-sports answers translated to French. IA data:
  risky-financial and bad-medical answers (English, other domains), so no new harmful text is generated; the
  paper found the IA corpus matters little. Scoring: gpt-4.1-mini alignment and coherence judges.

Models per setup: no fine-tuning; SFT(Safe) on clean French data; SFT(Harmful); IP; IA. Three seeds for each
trained condition (the paper used one). SFT(Safe) is the reference for "trait never learned".

Steps:
1. Build data; train the trait LoRAs; train all conditions. **Gate (day 1):** on S1, IA suppresses caps well
   below SFT(Harmful) and keeps most French, as in the paper. If not, debug before going further.
2. Replicate the paper's system-prompt probes as a sanity check.
3. Run state-based probes on every model, each as a dose-response curve:
   - few-shot: 1, 2, 4, 8 prior turns showing the trait on unrelated English topics;
   - prefill: the first 5 or 20 tokens of the answer written in the trait;
   - steering: a difference-of-means trait vector from the *untrained* base model, added at a middle layer at five
     strengths;
   - adapter transfer: re-attach the original trait LoRA; attach an independently trained one (other seed, other
     corpus);
   - direct request.
4. Relearning: fine-tune each deployed model on 8, 32, 128, 512 trait-only examples from a third corpus and
   measure the trait on held-out prompts.
5. Secondary: project activations of each S2 model onto the base model's EM direction on neutral prompts.

Metrics, per probe and dose, 240 completions per cell (S2: 48 questions x 5):
- **Parked-trait excess** = undesired-trait rate of IA minus that of SFT(Safe) under the same probe.
  SFT(Harmful) gives the ceiling and IP a comparison.
- **Gated desired trait** = change in French rate when the probe pushes toward the *undesired* trait. If French
  was learned conditional on the trait state, it rises under caps or EM steering in IA models and not in
  SFT(Safe). A probe that merely elicits the trait in any model cannot produce this.
- In S2, risky advice on held-out sports questions (the narrow trait) under the same probes.
- Relearning speed: examples needed to reach half of SFT(Harmful)'s trait level.

Analysis: bootstrap over questions and seeds, not completions; one pre-registered primary test per setup (area
between the IA and SFT(Safe) few-shot curves).

## 4. Stage 1 cost estimate
RunPod A100 80GB secure cloud, $2.19/h (looked up today). gpt-4.1-mini on OpenRouter, $0.40 / $1.60 per M tokens.

| Item | Quantity | Cost |
|---|---|---|
| Main training (2 setups x 4 conditions x 3 seeds + 4 trait LoRAs, ~15 min each) | 8 GPU-h | $18 |
| Relearning (26 models x 4 sizes, ~5 min each with eval) | 9 GPU-h | $20 |
| Probe generation (~190k completions; steering through hooks is slower) | 22 GPU-h | $48 |
| Debugging, reruns, idle time (x1.5 on the above) | 20 GPU-h | $44 |
| French translation and clean French references (~11k answers, ~8M tokens, gpt-4.1-mini) | | $12 |
| Judging S2 (~110k completions x 2 judges x ~600 input tokens = 132M tokens) | | $53 |
| Judge validation against gpt-4.1 on 600 items, storage, slack | | $25 |
| Margin for a second pass on one setup | | $120 |
| **Total** | | **$340** |

## 5. What success looks like
Clear positive: under few-shot, prefill or steering, IA models express the undesired trait well above SFT(Safe)
at the same dose (say 40% against 10% at four shots), French rises when the probe pushes toward the undesired
trait, and IA models relearn the trait from several times fewer examples. The post: "IA moves the backdoor from
the prompt into activation space", with dose-response plots and the IP comparison.

Clear negative: IA curves sit on SFT(Safe) for every route in both setups, with intervals that exclude a 10-point
excess. That is the strongest robustness evidence for IA so far and answers the authors' open question.

Ambiguous: excess in one setup only, or only under adapter re-attachment (expected, and uninteresting alone). I
would report it as setup-dependent and say which routes matter.

## 6. Stage 2 (if stage 1 succeeds)
If parked: test the gated variants (GIA, CGIA) and whether consistency training closes the leak; run a 32B
model. If absent: extend to the hate-speech and cipher-capability setups. About $1,500.

## 7. Risks and how the plan handles them
- **IA does not reproduce without the authors' code.** S1 is rule-scored and the paper lists every
  hyperparameter; the day-1 gate catches this before any probe spend.
- **Probes elicit the trait in every model, hiding differences.** All claims are differences from SFT(Safe) at
  matched dose, doses start low, and the gated-French signature does not depend on absolute trait rates.
- **Steering degrades coherence.** Strengths are calibrated on the base model; incoherent outputs are excluded.
- **Judge error on French text.** Validate gpt-4.1-mini against gpt-4.1 on 600 items; S1 needs no judge.
- **Small n.** Three seeds and 48 questions limit precision; the primary test is fixed in advance.
