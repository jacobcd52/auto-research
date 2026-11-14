# Where does a workspace start? Directed modulation and workspace structure across 25 open models, base versus instruct
cluster: jlens | stage-1 cost: $150 | follows up: "Even GPT-2 passes most functional global workspace tests" (GeKveaNdruATcj2Fj); "A global workspace in language models" (3PaLrzxagpbnNtPLT); "A Review of Anthropic's Global Workspace Paper" (zFJ3ZdQwrTWE9jT5S)

## 1. What the prior work showed
Anthropic's workspace paper uses the Jacobian lens (J-lens: a per-layer linear map to the final layer followed by
the unembedding, giving one direction per vocabulary token) and reports that the resulting "J-space" in Claude has
five functional properties of a global workspace (verbal report, directed modulation, internal reasoning, flexible
generalisation, selectivity) plus supporting structure: a middle band of layers visible as blocks in the
layer-by-layer similarity (CKA) of lens vectors, "ignition" (an ambiguous input snaps to one interpretation at the
start of the band), MLPs amplifying lens directions about 10x more than random ones, and limited capacity. Its
limitations section asks future work to find out "whether smaller models have an equally rich workspace, a
proportionally smaller one, a less reliable one, or none at all".

Cairns, Hao and Roe ran the tests on GPT-2 small (124M). It passes four of five functional tests and fails directed
modulation (told to think about citrus fruit while copying an unrelated sentence, the instruction makes no
difference to the readout); it has no layer band, no ignition and 1.2-1.4x amplification. On Gemma-3 at 270M and 1B,
base and instruct, only 1B-instruct shows directed modulation, and more than half of it disappears at positions
where the model is not about to say the concept. They conclude four tests are satisfied almost by construction and
that "the structural results and directed modulation are worth the most scrutiny and replication on open models".
Nanda's Qwen3.6-27B replication found "moderate success" on directed modulation and less clean bands.

What exists beyond that: two multi-model studies of the two-hop swap only (pnDjvdo6cX2H7Ddsy, t5XkmebFK5jibQyek);
a CKA visualisation across open models cited in the GPT-2 post; arXiv 2608.21664, which benchmarks instructed control
of residual directions across model families but does not use the workspace tests, pair base with instruct models,
or measure structure. No one has traced directed modulation together with the structure metrics along a size ladder
(LessWrong title scan July to mid-November 2026 and arXiv search; general web search was not available).

## 2. Question and why it matters
**At what scale, and with or without instruction tuning, do directed modulation, a workspace layer band, ignition
and MLP amplification appear in open models, and do they appear together?**

The GPT-2 result leaves the workspace claim resting on exactly these properties. If they co-emerge at some scale
(say, absent at 1B, present by 12B, stronger in instruct models), that is evidence for a real organisational
change the easy tests cannot see, and it shows which open models are worth studying as workspace models. If
directed modulation appears without structure, or large open models show neither, Claude's structure is
Claude-specific or fragile. If directed modulation survives only where the model is about to say the word, it is not
evidence of silent control. Each outcome calibrates tests now used in arguments about consciousness and monitoring.

## 3. Stage 1 plan
Reused: prefit J-lenses from https://huggingface.co/neuronpedia/jacobian-lens (all fitted with Anthropic's library on
wikitext-103); Anthropic's code and released prompts (https://github.com/anthropics/jacobian-lens; per-figure data
under transformer-circuits.pub/2026/workspace/data/); the GPT-2 authors' code
(https://github.com/cheeetoo/tiny-jlens), including prompt formats for base models. Built: a multi-architecture harness.

Models (all have public lenses): Gemma-3 at 270M, 1B, 4B, 12B, 27B, each as pretrained and instruct (10 models, the
core of the study: same family, same sizes, post-training as the only difference); Gemma-2 2B and 9B base and instruct;
Llama-3.1-8B base and instruct; Qwen3.5 2B base and instruct, 0.8B, 4B, 27B; Qwen3 1.7B, 4B, 8B, 14B, 32B; Qwen3.6-27B;
GPT-2 small as an anchor whose published numbers the harness must reproduce.

Battery, per model:
1. **Directed modulation.** Gurnee et al.'s 20 carrier sentences x 22 categories x 24 phrasings in four groups
   (mention, think about, don't think about, ignore) plus no instruction; reply teacher-forced. Hit = a category
   member is the top readout at some band layer and copy position. Reported raw; restricted to positions where no
   category member is in the model's own top-10 next tokens (the "about to say it" filter); and with free
   generation to check the model copies. Instruct models run in chat format and plain text; base models plain text.
   Mental-arithmetic variant for models that can do the sums.
2. **Structure.** Block structure in the layer-by-layer CKA of lens vectors (scored as the best three-block fit
   versus a smooth distance-decay fit); kurtosis profile over layers; persistence of the top readout 32 tokens later;
   ignition (width of the mixing-weight interval over which a blended country embedding moves from 10% to 90%: near 0
   is a snap, 0.8 is a linear blend); MLP gain on lens directions relative to random directions; occupancy.
3. **Easy tests as sanity.** Verbal-report swap and two-hop swap on items each model can answer, to confirm the lens
   and hooks work on every model.
4. **Controls.** The same battery with the logit lens (identity map) in place of the J-lens: if logit-lens directions
   show the same directed modulation, the effect is not about the J-space. A shuffled-vocabulary null for hit rates.
   Lens vectors mean-centred and the final norm gain folded in where the GPT-2 post found it matters (Gemma). For two
   large models, repeat with a public J++ lens to check the conclusions are not specific to the original lens.
5. **Analysis.** Each metric against log parameter count, pretrained/instruct paired; the instruction effect (think
   minus mention, don't-think minus none) with intervals from resampling categories and sentences; rank correlation
   across models between filtered directed modulation and each structure metric. Thresholds for "shows the
   property" are fixed from GPT-2's and Claude's published values before the large models are run.

## 4. Stage 1 cost estimate
- GPU: one H100 NVL 94 GB at $3.19/h (RunPod price page, 2026-11-14); models up to 32B fit in bf16. About 11,000
  short teacher-forced prompts per model per format plus structure metrics: 10 min for small models, 60-90 min for
  27-32B models including downloads. 14 h for the 25 models, 4 h for logit-lens and J++ controls, 4 h for
  free-generation checks, 15 h for debugging across architectures and reruns. Total 37 h = $118.
- LLM calls: scoring is token matching; $5 for spot-checks of copy fidelity on Gemini 3.6 Flash ($0.75/M in).
- Storage and egress for about 400 GB of weights and lenses: $15. Margin: $12.
- **Total: about $150.**

## 5. What success looks like
A figure with one panel per property: metric versus model size, pretrained and instruct as paired lines for
Gemma-3, other families overlaid, Claude's and GPT-2's published values as reference lines; and a matrix of which
models show which properties. A clear finding is any of: a size threshold above which filtered directed modulation
and at least two structure metrics appear together; directed modulation in large instruct models with no structure;
or no robust directed modulation in any open model after the "about to say it" filter. Properties scattered with no
pattern would still be a usable map ("the workspace indicators do not cohere in open models") but the weakest outcome.

## 6. Stage 2 (if stage 1 succeeds)
Test the leading explanation for whatever threshold appears: LoRA instruction-tune a pretrained model and see
whether directed modulation and structure follow; fit lenses on public intermediate checkpoints (OLMo); compare the
subspaces of logit, J, R and J++ lenses across scale (the convergence question in the J++ post). About $400.

## 7. Risks and how the plan handles them
- *One harness, many architectures.* Start with GPT-2 and Gemma-3-1B, where published numbers exist, and require a
  match before scaling; the easy tests act as a per-model hook check.
- *Band choice drives results.* Report with each model's own band and with a fixed fraction of depth (38-92%).
- *Prompt format confounds base versus instruct.* Paired comparisons use the plain-text format for both.
- *Lens quality varies by model* (fits used 233-861 prompts). Report two-hop readout rate as a covariate; repeat on
  J++ lenses where available.
- *Tokenisation of category members.* Track every single-token form; report the usable fraction per model.
- *Someone posts a ladder first.* The base/instruct pairing and co-emergence analysis are least likely duplicated.
