# Feedback: 03-workspace-size-ladder ("Where does a workspace start?")

Verdict: **keep with tweaks** (shrink the model list, fix the metric's depth confound, re-scope the structure half
around what is already public, fix the gated-weights problem).

What I checked (2026-11-14): the GPT-2 post and Nanda's review in full text; the Hugging Face API for the lens repo
and every model family; the RunPod price page; arXiv API searches ("Jacobian lens", "J-lens", "directed modulation",
"global workspace" + scale); a LessWrong title scan of all 672 posts since 2026-10-15; the comments on the GPT-2
post; the eliebak.com CKA page. **General web search was unavailable to me too (shared budget exhausted), and
github.com and transformer-circuits.pub/2026/workspace/data/ return 403 from this sandbox**, so the two GitHub repos
and Anthropic's per-figure data are confirmed only through the posts that cite and use them.

Claims that check out:
- GPT-2 summary is accurate (fails directed modulation; no band, no ignition, 1.2-1.4x amplification; Gemma-3
  270M/1B, only 1B-it shows the effect; the top-10 filter "more than halves the hit rate"; the "worth the most
  scrutiny and replication on open models" quote; the Gurnee limitations quote; 20 sentences x 22 categories x 24
  phrasings in four groups). Nanda: "moderate success", CKA "notably less clean". All verbatim in the sources.
- `neuronpedia/jacobian-lens` has a J-lens for every model listed in the plan (Gemma-3 270m/1b/4b/12b/27b as pt and
  it; Gemma-2 2b/9b both; Llama-3.1-8B both; Qwen3.5 0.8b/2b/2b-Base/4b/27b; Qwen3 1.7b-32b; Qwen3.6-27B; gpt2).
  Fit sizes 233-861 prompts as stated. J++ lenses exist for gemma-3-12b-pt and qwen3.6-27b.
- RunPod H100 NVL 94 GB is $3.19/h today. arXiv 2608.21664 is as described.

Claims that do not check out, or are missing:
1. **"A CKA visualisation across open models" undersells what exists.** https://eliebak.com/viz/jspace-open is a
   J-lens CKA explorer over **38 open models** built from the same Neuronpedia lenses, with base-only /
   instruct-only toggles, family and size presets, depth-normalised axes, and per-model "structure means". The GPT-2
   post already summarises its result: "many other open models also show no sharp tripartite structure". So the
   headline structure metric (CKA blocks, base vs instruct, across sizes) is essentially done, just not written up
   as a post. The page also references an `open-jlens-data` repo with numbered experiment runs (E7, E8), so its
   author has a running series I could not inspect; it may hold more than CKA.
2. **Not cited: arXiv 2608.05160 "The Ignition Index"** (August 2026): an ignition metric across 11 models and five
   families, reporting that the hypothesis linking ignition to model scale "was not confirmed". It is probe-based,
   not J-lens-based and not Gurnee's embedding-mixing test, so it does not pre-empt, but an "ignition versus scale"
   panel has a published null prior that the proposal must cite and differentiate from.
3. **Gemma and Llama weights are gated** (`gated: manual` on every google/gemma-* and meta-llama/Llama-3.1-8B repo;
   an unauthenticated config fetch returns 401). The programme says the executing agents cannot use anything needing
   accounts or approvals. Ungated mirrors exist and I confirmed they are open: `unsloth/gemma-3-{270m,1b-pt,4b-pt,
   12b-pt,27b-pt,27b-it}` and `unsloth/Llama-3.1-8B`. The plan must name the mirrors, and verify per model that the
   mirror matches the weights the lens was fitted on (reproduce the GPT-2 post's Gemma-1B numbers; check lens top-1
   agreement with the model's output at the last layer). The core Gemma-3 pt/it ladder depends entirely on this.
4. The eliebak page says the public qwen3-32b fit "is an 80-prompt checkpoint, read with care"; the HF README now
   lists 557 prompts. Probably refitted since, but check the convergence CSV before leaning on the top of the Qwen3
   ladder.
5. Qwen3, Qwen3.5 (non-Base) and Qwen3.6 are thinking chat models with no base counterparts except Qwen3.5-2B/9B.
   "25 models" therefore contains only about 9 true base/instruct pairs (5 Gemma-3, 2 Gemma-2, 1 Llama, 1 Qwen3.5-2B).

I found no post or paper that traces directed modulation along a size ladder with base/instruct pairs, within the
search limits above.

## 1. Would it get upvoted?

Plausibly, but near the bar rather than well over it. Reference points: the GPT-2 post got 87 with a sharp,
deflationary headline; the J++ post 123; lesser J-lens follow-ups mostly got 4-25 ("Failed replication on GPT-2" 15,
multihop swap 4, coordinate-aligned subspaces 13). A 25-model descriptive map with "properties scattered" lands in
the 15-40 band. What clears 50 is one crisp sentence, for example:
- "After removing positions where the model is about to say the word, no open model up to 32B shows directed
  modulation: the one test GPT-2 failed is mostly a next-token effect," or
- "Directed modulation switches on with instruction tuning between 1B and 4B and survives the filter; base models
  never show it at any size, and none of the structural signatures accompany it."
Either would interest the people who engaged with the GPT-2 post and Nanda's review (interp researchers, the
consciousness-indicators crowd around Eleos), and Nanda said he was "pretty surprised" directed modulation works
at all and has no mechanistic story. My estimate: 45-55% chance of >50 karma conditional on a clean run, driven
almost entirely by the directed-modulation half. The structure half adds little karma because of point 1 above.

## 2. Naturalness

Mainline. Gurnee et al.'s limitations ask for it, the GPT-2 authors ask for it and began it (Gemma 270M/1B), and
the screener's note is this experiment. The flip side: the GPT-2 authors already have the harness, the Gemma
prompt formats and the filter, and extending to 4B/12B/27B is a day's work for them; and the CKA explorer's author
has all 38 lenses loaded. Scoop risk within a few weeks is real (I would say 25-35%). The base/instruct pairing is
not a differentiator, since both existing efforts already have it. The differentiators are (a) the "about to say
it" filter applied at scale, (b) the logit-lens control, and (c) a proper null. Lead with those.

## 3. Pre-mortem

How it plays out: day 1 goes on the harness. GPT-2 and Gemma-1B reproduce after some fiddling with centring and
final-norm gain. Gemma-3 4B+ pretrained checkpoints are multimodal, Qwen3 has thinking-mode templates, lens files
differ in layer coverage and target layer; each family costs hours. Directed modulation runs everywhere by the end
of day 1. Day 2: structure metrics. CKA and kurtosis are quick. Ignition (embedding mixing on Gurnee's 12
countries, needing single-token countries per tokenizer and a per-model band) and MLP gain (per-architecture MLP
hooks, gated/GeGLU variants, what "gain relative to random" means with different norm placements) are each a
custom implementation with a published reference value for only GPT-2 and Claude, so there is no way to know
whether a number on Gemma-27B is right. Occupancy needs non-negative pursuit per activation. Something gets cut or
ships unvalidated.

Forecast:
- Clear positive (a clean threshold or a clean dissociation that survives the filter and controls): 30%
- Clear negative that is still interesting (no robust filtered directed modulation anywhere): 15%
- Ambiguous mush (rates rise with size and instruct tuning, shrink under the filter, structure metrics noisy and
  uncorrelated, heavy family effects): 45%
- Fails to run meaningfully (harness never validated beyond the two anchor models): 10%

Specific failure reasons, most important first:

1. **The hit metric rises mechanically with depth.** "A category member is the top readout at some band layer and
   copy position" is a max over (layers x positions). GPT-2's band is 3 layers; Gemma-1B's is 14; a 27B model at
   38-92% of depth has about 35. With identical per-cell behaviour, hit rate grows with model size. A size ladder on
   this metric will show "emergence with scale" by construction. The shuffled-vocabulary null helps only if it is
   computed per model and subtracted; the proposal lists it but reports raw rates against log parameters. Note also
   how fragile hits are: in GPT-2, 48 of 50 hits came from two sentence/category coincidences.
2. **Co-emergence is not testable with this design.** Every metric will correlate with log parameters, so a rank
   correlation across 25 models between directed modulation and a structure metric mostly measures size. The models
   are not independent (5 families), and the clean subset is 5 sizes x 2. A partial correlation controlling for
   size with n of about 10 has no power. "Appear together" will end up as an eyeballed claim.
3. **The filter can erase the phenomenon or the signal, and the two are indistinguishable.** Gemma-1B-it copies
   exactly on only 15/66 "think about" trials, so teacher-forced readouts there come from a model that wants to do
   something else. Larger instruct models will copy better, so filtered rates could rise with size for a reason
   unrelated to workspaces (compliance), or fall to zero everywhere. The top-10 threshold is arbitrary; results at
   top-10 only will be attacked.
4. **Base versus instruct is confounded by format even in the "paired plain-text" arm.** An instruct model on plain
   text is off-distribution; a base model has no notion of an instruction to follow. A difference shows instruct
   models follow instructions, which nobody doubts. The interesting comparison is the think-minus-mention contrast
   within each model, which the proposal does include; it should be the primary endpoint, not a secondary one.
5. **Band choice.** The GPT-2 authors chose Gemma bands by hand from layer statistics because Gemma has no jump in
   lens/output agreement. For 25 models nobody will hand-pick; the fixed 38-92% band includes late layers where the
   lens reads the next token, which is exactly where "about to say it" contamination lives.
6. **Structure metrics unvalidated above GPT-2**, and the three-block-versus-decay CKA score is a new, untested
   statistic whose result (no sharp blocks in most open models) is already public.
7. **Tokenisation.** Category members and countries must be single tokens per tokenizer; usable fractions will
   differ by family and will correlate with family, adding another family-level confound.
8. **Gated weights** (above) if the mirrors are not used; **lens/weights mismatch** if they are and differ.
9. Wall-clock: 37 GPU-hours on one pod does not fit in two days with agents idle while it runs. Use two or three
   pods in parallel (same cost).

## 4. Cost check

The estimate is realistic and probably slightly low. Per-model compute is small (about 11,000 short prompts per
format; lens readout is a matrix multiply; even Gemma's 262k vocabulary is minutes on an H100). The spend is pod
time during debugging. My estimate: 45-60 GPU-hours across 2-3 pods at $2.89-3.19/h = $140-190, plus about $15
storage, $5 API: **$170-220** for the plan as written, **about $110-140** for the reduced plan below. Well under
the $500 cap either way. Loading 54-65 GB models on a pod with 94 GB system RAM works but leaves little headroom
alongside a 3.5 GB lens and cached activations; write activations to disk in chunks.

## 5. Recommended changes

1. **Make directed modulation the whole of stage 1 and fix the metric before running the ladder.** Primary
   endpoint: think-about minus mention (and don't-think minus none) within each model, on a depth-normalised
   statistic: either per-(layer, position) hit rate, or a fixed number of evenly spaced band layers (say 6) for
   every model, or the mean log-rank of the best category member. Subtract a per-model null (shuffled category
   assignment, same number of single-token members, frequency-matched). Report the raw Gurnee-style "any layer, any
   position" rate only as a secondary figure for comparability with Figure 12 of the GPT-2 post.
2. **Use the ungated mirrors and say so** (`unsloth/gemma-3-*`, `unsloth/Llama-3.1-8B`), with the lens-consistency
   check as a gate. Without this the core ladder cannot run under programme rules.
3. **Cut to about 14 models.** Gemma-3 x 5 sizes x pt/it (10), Qwen3.5-2B and its Base, Llama-3.1-8B pair or
   Qwen3.6-27B for comparability with Nanda, GPT-2 as anchor. The Qwen3 1.7-32B ladder is instruct-only with
   thinking templates and a question mark over the 32B fit; make it optional. Fewer models buys time for the
   controls, which are where the karma is.
4. **Sharpen the "about to say it" analysis into the headline.** Report at top-1, top-10 and top-100 thresholds;
   report the free-generation copy rate per model and condition as a covariate; add a condition with an explicit
   "copy exactly, do not write about X" reinforcement so high-copy-fidelity trials exist for small instruct models;
   restrict a main analysis to trials where free generation copies exactly. The logit-lens control stays, and
   should also be run at matched layers with the same filter.
5. **Demote structure to a small, validated add-on, and reuse the public CKA work.** Cite eliebak.com/viz/
   jspace-open and arXiv 2608.05160 in section 1 and rewrite the novelty claim accordingly. Do not recompute CKA
   blocks as a contribution; if a band score is needed as a covariate, take it from the public data or compute it
   once. Keep at most two structure metrics that are cheap and architecture-agnostic (persistence of the top
   readout at 32 tokens; ignition width), validate each against the GPT-2 published value, and drop MLP gain and
   occupancy from stage 1. Drop the co-emergence rank correlation as a claimed analysis; present a
   property-by-model matrix and say plainly that the design cannot separate co-emergence from joint dependence on
   size.
6. **Pre-specify bands.** Fixed fraction of depth as primary, with a variant ending before the layer where lens
   top-1 agreement with the output exceeds a fixed value (e.g. 50%), to keep next-token layers out.
7. **Pre-write the three candidate headlines** and the numbers that would support each (thresholds on the
   null-subtracted, filtered think-minus-mention contrast, with intervals from resampling categories and
   sentences), so that the mush outcome is reported as mush and not narrated into a threshold.
8. **Move fast or check for a scoop first.** Before spending, look at the GPT-2 authors' repo and the
   `open-jlens-data` repo for a larger-Gemma or directed-modulation run; if either has one, pivot stage 1 to the
   stage-2 item (LoRA instruction-tune a pretrained Gemma and watch whether filtered directed modulation follows),
   which is a causal result neither group is positioned to have already.
9. Run on 2-3 pods in parallel; budget $200.

If the funder has to choose within this cluster, this proposal is the safest to execute (forward passes on
public lenses, published reference numbers to validate against) but has the lowest ceiling and the highest scoop
risk of the three; it is worth funding at its low price only with changes 1-5.
