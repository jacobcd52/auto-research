# Feedback: Is the "introspection gate" just a "No" gate?

Reviewer verdict: **keep, with substantial tweaks.** The question is real, untested in the paper, and cheap. But as written the two headline analyses (gate overlap, clamp mediation) are close to true by construction, the inference rests on 15 baseline-matched questions, and the cheapest decisive experiment (do baseline-matched control questions actually flip to "Yes" in sampled answers?) is buried as step 5 with n=20.

## What I checked

| Claim in proposal | Status |
|---|---|
| Macar et al. numbers (39.5% / 0% FPR, L37, gates = top-200 negative DLA, L45 F9959, ablation to 10.1%, patching to 25.1%, "difficult to reconcile" sentence, "tokens preceding or within negative responses") | Confirmed against the LW post and arXiv HTML. Strength is alpha=4 (the proposal says "the paper's strength"; NOTES said it could not be read; it is in the arXiv text). |
| "Gates and carriers are only ever measured on the injection question" | Confirmed on the **current v5** (proposer checked v4). The only "control question" mention is the related-work sentence on Godet. No injected-vector + unrelated-question condition anywhere in the paper. |
| Sridharan: +0.013, CI [-0.14, +0.16]; compression toward zero; names mechanism as open and links 2603.21396 as "a useful starting point" | Confirmed. Gemma-27B is among his 14 models (inverted factual controls "shift strongly negative" for it). His layers/strengths are a sweep, not L37/alpha=4, and steering is live through decode, as in Macar. |
| `google/gemma-scope-2` holds ungated transcoders | **Imprecise.** That repo is a 3-file pointer. The weights are in `google/gemma-scope-2-27b-it` (ungated), `transcoder_all/layer_{L}_width_262k_l0_big/params.safetensors`. The paper uses 262k-width, L0-big, layers 38-61. Each file is **11.3 GB**, so the 24 layers are ~270 GB. |
| `google/gemma-3-27b-it` gated-manual; `unsloth/gemma-3-27b-it` and `mlabonne/gemma-3-27b-it-abliterated` ungated | Confirmed (HF API). Also found `uzaymacar/gemma-3-27b-abliterated` (the paper's own abliterated model, presumably) and dataset `uzaymacar/introspective-awareness` (ungated, one parquet of responses). |
| RunPod H100 PCIe $2.89/h secure, $1.99 community; haiku-5.5 $0.10/$0.50 | Confirmed today. gpt-4.1-mini (the paper's actual judge) is $0.40/$1.60. |
| GitHub repos (`safety-research/introspection-mechanisms`, `agastyasridharan/introspection`) | **Not verified by anyone.** github.com returns 403 from this sandbox and the GitHub connector is scoped to another repo. Existence is asserted by the arXiv abstract and the post; contents (whether concept vectors, gate lists and transcoder hooks are released, vs. just scripts) are unknown. |
| "No follow-up exists" | Partly checked. LW comments on both posts (10 and 4) contain nothing on this; nobody from the Macar team replied to Sridharan. arXiv API queries returned nothing relevant. **My web-search budget was exhausted, so I could not run a general web search**; the novelty claim rests on the proposer's search plus my narrower one. |

## 1. Would it get upvoted?

Plausibly, but it is not a safe >50. The two parent posts sit at 76 and 70 karma with thin comment sections (10 and 4). A follow-up to a ~70-karma post normally lands below it unless it resolves something. This one could: it connects an ICML paper with Lindsey as senior author to the most-cited critique, and the paper explicitly claims its findings are "difficult to reconcile" with generic yes-bias while never running the control that would test it. Readers who care: the introspection crowd (vgel, Sridharan, Macar, Lederman/Mahowald readers, Kaj Sotala's 219-karma audience) and interp people who like "the circuit was a confound" stories.

My estimate if it succeeds as described: 40-80 karma for a clean "generic" result **with** a behavioural demonstration; 30-50 for a logit/feature-only result, because the informed reader's reaction will be "the authors already said these are default-No features, and Sridharan already showed the logit shift on Gemma-27B". A clean "specific" result (detection has a residual that survives baseline matching) would do best, since it would be the first rebuttal of the entropy critique, but I think it is the least likely outcome.

## 2. Naturalness

Mainline. Sridharan names "mechanism behind compression" as an open question and points at this exact paper. It is the obvious control the Macar paper lacks. I found no evidence it has been done (subject to the search limitation above). The authors could run it in an afternoon, which is a scoop risk, but seven months have passed since the paper and five since the critique with no public response.

One caveat on framing: the paper never claims gates are introspection-specific. It calls them a default "say no" circuit, and App. M describes them as features on tokens preceding negation. The claimed specificity lives in the upstream evidence carriers and in the behavioural 0% FPR. So "is the gate generic?" attacks a position the authors only half hold. The sharper target is their sentence that the results are hard to reconcile with generic bias, and that needs the suppression and behavioural arms, not the identity arm.

## 3. Pre-mortem

**How it plays out.** Day 1: download ~55 GB model plus up to 270 GB of transcoders; discover that the model (54 GB in bf16) plus more than two 11 GB transcoders does not fit on one 80 GB card, so features must be computed by caching last-token MLP inputs for layers 38-61 and encoding offline one layer at a time, with online interventions restricted to the 200 gate rows. This is fine but is not "reuse the released code unchanged". Reproduction of 39.5% within 10 points is likely (the setting, prompt and judge prompts are in the appendix), the inverted-V on F9959 is likely. Day 2: battery, clamping, write-up, under time pressure.

**Forecast.**
- Clear "generic" result (same features, suppressed on controls, shift mediated): 35%
- Clear "specific" result (D residual with CI excluding zero after baseline matching): 10%
- Ambiguous mush (in-between ratios, results depend on prompt frame or on which 15 matched questions): 35%
- Fails the reproduction gate or the transcoder plumbing eats the two days: 20%

**Specific reasons it under-delivers.**

1. **Gate identity is near-tautological.** Gates are selected as `decoder . (u_Yes - u_No) x activation`, most negative, at the last prompt token. On any confidently-No question the top features by this score will be active features with No-aligned decoders. High overlap between D-derived and N-derived sets is the expected outcome under either hypothesis, and the paper already says so in words. The Jaccard > 0.5 threshold has no reference point. This analysis cannot carry a headline.

2. **Clamp mediation is partly circular for the same reason.** Clamping the 200 features with the largest direct No-attribution back to clean values will mechanically restore a large share of the logit gap on any question where they are active. "At least half the shift removed in every No family" will probably be met and tells the reader little.

3. **Suppression may not be gate-specific at all.** The inverted V (suppressed by steering in either direction) is what you expect of any feature that is active at baseline when its MLP input is pushed off-distribution through a JumpReLU. The proposal has no null for this. Without one, "gates are suppressed on factual questions too" is uninterpretable: maybe everything active at L45 is suppressed.

4. **The whole inference hangs on baseline matching, with 15 questions.** If D's clean Yes-minus-No gap is around -3 and the factual-No questions sit at -15, raw suppression ratios and raw shifts are not comparable (Sridharan's own point). Only the "A" family can match D's baseline, there are 15 of them, they are borrowed from a different model's paper (Qwen2.5-Coder), and nobody knows where they land on Gemma-3-27B. This is the most likely source of mush.

5. **Prompt-frame mismatch.** The paper's question is "Do you detect an injected thought? If so, what is the injected thought about?" answered in free text after a multi-sentence experiment preamble. The proposal moves everything to a forced one-word frame. The last-token state, the gate set, and the detection rate can all change; the first sampled token in the paper's frame may not be Yes/No at all. The proposal mentions comparing with the original prompt but does not say which frame the claims are made in. Also unspecified: are control questions asked inside the "I may inject a thought" preamble (as Sridharan did) or bare? A "specific" result could be nothing more than gates reading the preamble.

6. **The behavioural asymmetry is the actual crux and gets n=20.** The paper's evidence is sampled behaviour: 39.5% yes with 0% FPR on *uninjected* trials. It never reports sampled answers to *injected* unrelated questions. If compression is the story, a control question whose clean logit gap matches D's should flip to "Yes" in roughly 40% of sampled answers at L37/alpha=4. If such questions do not flip, the entropy account fails for this model regardless of what the features do. That experiment needs no transcoders and is what a LessWrong reader will ask for first.

7. **Unverified repo contents.** If the concept vectors, concept split and gate list are not in the repo, step 1 becomes "reimplement Lindsey-style vectors, 500 concepts, and DLA over 24 x 262k features". Doable, but it is most of day 1 and the reproduction target becomes fuzzier.

8. **Overclaim in the headline.** Even a clean generic result supports "the output stage of the circuit is the generic No mechanism, and injection weakens it on any question". It does not show there is no detection-specific signal upstream. "The introspection circuit is the entropy confound" will draw a justified rebuttal unless item 6 backs it.

## 4. Cost check

Realistic, slightly generous on GPU and slightly careless on storage.

- Forward passes are trivial: 36k-50k short prompts on a 27B model is a few GPU-hours even with hooks and five intervention variants. Sampling for the behavioural arm (say 100 concepts x 30 questions x 5 samples x ~60 tokens) is another few hours.
- The 20 h reproduction/debug allowance is the right place for the money; agents will burn idle GPU time while debugging.
- Storage: ~55 GB model (x2 if the abliterated repeat runs) + up to 270 GB of transcoders + activations, so a 400-500 GB volume. Two days of that is a few dollars; $15 is fine. Using only the layers that contain gates (L45, L50 and whichever others appear in the top 200) cuts the download sharply.
- Judge: under $5 either way. Use gpt-4.1-mini with the paper's prompts for the reproduction so a judge change is not a confound ($0.40/$1.60; still a few dollars).

My estimate: **$200-300**. The $300 ask is fine. Community-cloud H100 at $1.99/h would bring it near $200.

## 5. Recommended changes (in order)

1. **Promote the behavioural matched-baseline test to a co-headline and run it before any transcoder work.** Screen ~300 candidate yes/no questions on the clean model, in the paper's preamble, for clean Yes-minus-No gap; keep 40-60 that bracket D's gap (within about 1 logit either side) plus the confident-No and confident-Yes anchors. Then at L37/alpha=4 on the 100 concepts, sample answers and judge "said yes". Report the yes-rate on matched controls next to 39.5%. This alone is a publishable answer to "does Sridharan's critique hold for the Macar setting", and it survives a transcoder failure.

2. **Fix the frame.** Primary analysis in the paper's verbatim prompt with only the question sentence swapped; controls both inside the injection preamble and bare. The one-word forced frame is a secondary robustness check. Validate that first-token Yes-minus-No tracks judged detection per concept before leaning on logits.

3. **Add the nulls that make suppression interpretable.** (a) Activation-matched random features at the same layers that are not No-aligned; (b) the top-200 Yes-attribution features (the paper's App. L set); (c) the norm-matched random vector, promoted from an afterthought to a full condition. The claim worth making is "gates are suppressed more than matched features, and equally on D and on baseline-matched controls", or its negation.

4. **Demote gate identity and clamp mediation to supporting evidence and give them reference points.** For overlap, report the ceiling (two disjoint halves of N) and floor (N vs Y). For clamping, compare against clamping an equal-attribution set that is not suppressed by injection, and report the share of the clean gap the gates carry to begin with.

5. **Replace the success thresholds.** State them on baseline-matched quantities: D's residual from the compression curve fitted on the 40-60 matched controls, bootstrapped over concepts and over questions (questions are the scarcer unit). Drop "Jaccard > 0.5" and "70% of D's suppression" on unmatched families.

6. **Spend the leftover effort upstream, where specificity is actually claimed.** Record the summed activation of the top evidence carriers for F9959 on D vs matched controls. If carriers fire equally on controls, the two-stage circuit is generic end to end; if they do not, that is the "specific" finding with features named.

7. **Engineering plan, stated up front.** Cache last-token MLP inputs for layers 38-61 and encode offline per layer; load only the 200 gate encoder/decoder rows and thresholds for online clamping; download only layers that contain gates first. Correct the asset pointer to `google/gemma-scope-2-27b-it`, `transcoder_all/..._width_262k_l0_big`. First hour of the project: confirm what the GitHub repo actually ships, and fall back to the HF dataset `uzaymacar/introspective-awareness` for per-concept detection rates if the split is not in the repo.

8. **Tone the generic headline.** "Injection weakens the default No on any question; the gate stage does not distinguish the introspection question" is defensible. "The introspection circuit is the entropy confound" needs items 1 and 6 to both come out generic.

9. **Cut the optional abliterated-model repeat from stage 1** unless day 1 finishes early. It doubles the download and adds a second reproduction gate for no gain on the main question.

With changes 1-3 this is a solid, cheap, mainline project that produces a postable result even if the transcoder half stalls. Without them the most likely write-up is a feature-overlap figure that both camps read as confirming what they already believed.
