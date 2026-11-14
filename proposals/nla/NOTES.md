# Natural language autoencoders — reading notes and brainstorm

Written 2026-11-14. Related-work sweep used the arXiv API (phrase queries "natural language autoencoder(s)",
"activation verbalizer", "activation verbalization"), the LessWrong GraphQL endpoint (all post titles
2026-05-01 to 2026-11-14 scanned by keyword; comments on the cluster posts read), the Hugging Face API, a fetch of
the NLA paper (transformer-circuits.pub/2026/nla) and raw GitHub READMEs. Title-keyword scans can miss posts, so
"not done" below means "not found", not "confirmed absent". The field is very crowded (about 25 LW posts and 12
arXiv papers on NLAs since May), which shaped what was kept.

## 1. The four posts (all read in full)

**NLAs produce unsupervised explanations (oeYesesaxjzMAktCM, May 2026, 209 karma; linkpost, paper also read).**
Activation verbalizer (AV: activation -> text, sampled at T=1) and activation reconstructor (AR: text ->
activation, truncated model + affine head), both initialised from the target model, warm-started by SFT on
Claude-Sonnet-written guesses about what the model "is thinking" at the end of a text prefix, then trained jointly
with RL on reconstruction (KL penalty to the warm-start AV). Claims: explanations get more informative over
training; unverbalised eval awareness in Opus 4.6 (16% of destructive-coding transcripts, 26% of SWE-bench, <1%
of real usage); auditing-game win rate 12-15% vs <3% without NLAs. Stated limitations: confabulation (claims about
the context that are verifiably false; thematic claims more accurate than specific ones; claims repeated over
adjacent tokens more likely true), writing quality degrades, the warm start "could seed inaccuracies and biases
that NLA RL does not fully correct", AV is expressive enough to make its own inferences, cost. Paper tests
steganography by paraphrase/shuffle/translate (small FVE drops). Open releases: code + 8 checkpoints (below).

**Can activation verbalizers surface an internal chain of thought? (QQQAcKuWK6k98FivY, Jun 2026, 125 karma).**
Target model answers ~900 easy competition-math problems with no CoT (10-shot, problem stated five times); AV is
run on the last position before the answer at the NLA layer; Opus 4.7 graders (k=5, ~$125 per model at batch
prices) score Output / Answer / Problem / Method / Values / Coherence / Mistake. NLAs: kitft Qwen2.5-7B L20,
Gemma-3-27B L41, Llama-3.3-70B L53; plus a Qwen3-8B AO. Findings: (i) reconstruction is poor at the scale that
matters: FVU relative to "a rock with the mean direction written on it" is >1 for Qwen on the dataset and >1 for
all three NLAs across constant-variants of one problem (soup can price); Gemma's NLA does respond to the variant,
Qwen's does not. (ii) Confabulation cannot be ruled out: best-of-10 Sonnet 4.6 confabulations written from the
problem statement reconstruct as well as the real verbalization. (iii) On the 123 easiest problems, correct
outputs are mentioned 84% (Gemma) but singled out 42%; wrong outputs mentioned 47%, singled out 0/78; 16% of
verbalizations before correct outputs look at all like a chain of thought; mistakes almost never explained
(2/763). (iv) Edit-and-steer corrections work on 11/65 candidates but a vector from a random other problem works
on 10/65. Footnote 9: linear probes predict the first token of Gemma's output at ~80% at the last layer but do not
beat the majority baseline (35%) at the NLA layer, i.e. the answer may not be decided where the NLA reads.
Regex for "output appears in the verbalization" agrees with graders at >98%. Authors' suggestions: failures
"might be improved by just making the reconstruction loss go down" (possibly needing multi-token/multi-layer NLAs
or a paraphrase step); FVU-within-variants and confabulation tests as general checks; Elo grading; rerun on better
NLAs. Comment by Kurt H. Pieper asks the same thing: does more RL pushing FVE up lead to useful NLAs. No eval code
link in the post; the dataset is public (below).

**NLA explanations can be shortened (NazprRfWJ4qkwcSro, Jun 2026, 56 karma).** Qwen3-8B L24, nanoNLA, length
penalty lambda per token in the RL reward, 250 RL steps each. Held-out results (from the released RESULTS.md):
base (SFT only) 126 tok / FVE 0.532; lambda=0 127 / 0.585; 0.001 92 / 0.592; 0.002 74 / 0.570; 0.006 32 / 0.482;
0.015 25 / 0.450; 0.03 14 / 0.225. High-penalty AVs mostly repeat the final tokens. Caveats: AR accidentally
frozen during RL in the main runs (redone for two penalties, similar). Open questions the author lists: terser
wording vs dropped content; what gets dropped; steganography check; more models and steps. Top comments
(Karvonen, nostalgebraist) proposed Matryoshka NLAs, which the same author then did (below).

**How robust are NLAs to initialisation? (LQXWiF8PyJ5ojNsEv, Jul 2026, 82 karma).** Qwen2.5-7B, kitft code,
20k Ultra-FineWeb docs, FVE 0.70 control. Appended "Carthage must be destroyed" sentence: stripped within 100 RL
steps. "Love of Carthage" woven in: 0.6% by step 200. "Confabulation" init (Claude told to write only false
statements): post-SFT FVE 0.33 vs 0.61, post-RL 0.68 vs 0.70, with 0.7% plausible claims vs 7.6% (plausible-init
falls from 21% at warm start to 7.6% after RL; judge = Opus 4.8 per-claim scoring against the text). Side
experiment: last-paragraph-only init reaches FVE 0.67. Corrigendum (28 Oct): the KL term was silently off in the
official code until 2 Aug; with KL 0.01 the Carthage sentence persists ~100%, the sentiment persists at 58%, and
the liar NLA reaches only 0.16% plausible at FVE 0.66. Author comment: an init that quotes the last 64 tokens
also converges to FVE 0.67 with quite different explanations. Suggested: larger models/datasets. Checkpoints from
this post were not found on Hugging Face.

## 2. Related work and follow-ups found (what is already done)

LessWrong (score in brackets):
- Some observations about NLA explanations (ahu9BCHPFDg9AJF75) [22]: three-part format; deleting the final
  "last token" paragraph destroys reconstruction, the other two barely matter. Data: syvb/nla-recon-loss-sweep.
- Trying to use NLAs to find out how Qwen2.5-7B does multiplication (XN6CrJDiZvphGCC2e) [23]: qualitative.
- NLA Verbalizations on AuditBench: Llama 70B (xmmBTkogixvAbyQFk) [11]; NLA Thought Anchors (6HnnMHRoJLff46kgw).
- Explaining SAE features with foreign NLAs (AtbZQuAn2iY2jCup2); Exploring generalization in NLAs
  (tkiSQBuA8yj2tHNdv): a layer-20 AV applied to other layers; Can you hide from an NLA (3oRQxpxn4LiWKwbeQ).
- NLAs are summarizers, but do they have to be? (4nZwNPyfoadAxPH98): cross-model verbalization, "snippet"
  confabulated quotes, verbalizing steering vectors.
- Models are blind outside the J-space. NLAs aren't (LhDJdccLszLEAqgZ9) [29]: concept injection read by NLAs.
- Eliciting hidden knowledge from monitors with NLAs (NdBTH4wvBKWFyvifY) [28].
- Fixing rewards for NLA to reduce confabulation (DFgt8fi3Wzwwe2Sib) [7].
- Matryoshka NLAs (aWYQHh2pEFCLYh85C) [31]: random truncation before the AR; front-loads reconstruction-relevant
  claims; "did not find strong evidence that matryoshka NLAs are significantly more useful".
- NLAs miss some internalized behaviors (BcCcSfTHqz74kdTMF) [25]: NLAs report an in-context steganography
  instruction but mostly miss the same behaviour when fine-tuned in; the AV+AR round trip removes the secret's
  causal effect in the fine-tuned case.
- Three pieces of evidence that the NLA reconstructor does not read semantics or syntax (Q5fwBiZCwHGeKucmo) [20]:
  on Qwen3.6-27B, deleting content words costs least FVE, function words most; negation barely matters.
- Smaller NLAs and probes read eval awareness as well as full size NLAs (MQCZponFdSd7ZBXaa) [8].
- Interpreting attention head outputs with NLAs (nNYc5qddHXwdk5kix) [21].
- Deletion gap of reconstruction in NLAs is in the final explanation sentence (nmXzfwsEpGtfG4Bw2) [3]: per-claim
  FVE drop separates true from false claims with AUROC 0.58 (Qwen2.5-7B) and 0.49 (Qwen3.6-27B); 0.67-0.70 for
  final-sentence claims; paraphrase adds nothing.
- CHIVE (ExB6KYDcznaFS72eT; arXiv 2608.16747): NLAs, AOs and SAEs give an agent no uplift in predicting
  counterfactual behaviour in the wild.
arXiv:
- 2610.30934 Verbalizing activation differences with NLAs: compositional; NLAs transfer to light fine-tunes;
  recover Taboo words; RL on activation differences improves recovery on held-out organisms.
- 2610.18727 Identification vs discrimination: true account beats another activation's account 320/320, beats a
  one-claim-different rival 60.2% (n=35); paraphrase costs 2.1%.
- 2610.32691 NLAs identify without explaining (position paper).
- 2607.20379 Train the model, not the reader: ~2% of specific claims are ones reconstruction depends on (released
  Qwen2.5-7B AV); private codes under synthetic ground truth; RECAP.
- 2609.33702 Flow-NLA: point reconstruction increases unsupported details; distributional objective curbs it
  (Qwen, Gemma, Apertus); standardised evaluation of information / support / writing quality.
- 2609.37040 Selecting the most informative tokens (4.7M explanations; 5% of positions suffice).
- 2609.34033 AVPO (invert to text then QA). 2605.25903 Universal activation verbalizer (cross-model).
- 2611.08465 MAEMs (activation -> maximally activating text; verifiable by a forward pass; Qwen3.6-27B).
- 2611.03040 VERS: editing explanations to steer reasoning models (-45.8% tokens on GSM8K at -0.82 pp).
- 2608.21664 Measuring activation control: models can partly evade NLAs by instruction.

Not found: (a) any test of the CoT post's own hypothesis that lowering reconstruction error on the relevant
distribution makes verbalizations surface reasoning (2610.30934 specialised an NLA by RL, but for Taboo diffing);
(b) any measurement of agreement between independently trained NLAs for the same model and layer, or its use as
a claim filter (the paper has the adjacent-token heuristic; the AO line has same-model consensus sampling:
Taboo precision 46.6% -> 94.3% at 19.4% coverage); (c) a probe skyline for intermediate values at the NLA layer
on the no-CoT math task.

## 3. Public artifacts (verified via the HF API / raw files on 2026-11-14)

- Official NLAs (full fine-tunes, AV + AR, `nla_meta.yaml` sidecar), collection huggingface.co/collections/kitft/nla-models:
  `kitft/nla-qwen2.5-7b-L20-{av,ar}` (in-distribution FVE 0.752), `kitft/nla-gemma3-12b-L32-{av,ar}`,
  `kitft/nla-gemma3-27b-L41-{av,ar}` (AV ~107 GB), `kitft/Llama-3.3-70B-NLA-L53-{av,ar}`.
  Code: github.com/kitft/natural_language_autoencoders (training; Miles + SGLang; KL bug fixed 2 Aug per the
  init post), github.com/kitft/nla-inference. Demo: neuronpedia.org/nla.
- Qwen3-8B layer 24 (36 layers, d=4096):
  `syvb/nanonla-qwen3-8b-L24-av`, `-ar`, and `syvb/nanonla-qwen3-8b-L24-rl-lora` with LoRA adapters
  `p0.0, p0.001, p0.002, p0.006, p0.015, p0.03` (60 MB each); held-out completions `syvb/nanonla-qwen3-8b-L24-results`
  (1000 per model, with source text and FVE); training parquets `syvb/nanonla-qwen3-8b-L24-data-full`.
  `marco-bazzani/Qwen3-8B-nla` (independent run of the official recipe, full fine-tune AV at root, AR in `ar/`
  = first 28 layers + 4096x4096 head). Warm-start data: `ceselder/qwen3-8b-nla-L24-finefineweb-100k`,
  `asher577/easynla-warmstart-data` (371k rows, activations + gold explanations, train/val splits).
- Qwen2.5-7B layer 20: official pair; `anicka/nla-qwen2.5-7b-L20-av-v2` (LoRA r32, AV; injection differs:
  normalise to norm 150); `syvb/nla-qwen2.5-7b-L20-{av,ar}-matryoshka-sonnet46-v3` and `-v3-rl` (bullet-format
  warm start). 
- Larger: `ceselder/qwen3.6-27b-nla-rl` (AV base + RL adapters, AR), `ceselder/qwen3.6-27b-nla-av`,
  `therem/qwen3.5-9b-nla-L21-{av,ar}-{sft,rl}` (model card: 400 RL steps x 256 prompts x 8 samples on 4x A100
  80GB, ~145 s/step, ~17 h; FVE 0.786 with co-trained AR).
- Training code for agents: github.com/asherps/EasyNLA (README: Qwen3-8B L24 reaches ~70% held-out FVE in
  ~3-4 h on 4x H200; supports continuing RL from an SFT/RL adapter, KL reference adapter, optional Opus judge
  evals); github.com/ceselder/nanoNLA (superseded; single GPU, 4-bit base, LoRA r=128 rsLoRA).
- Math data: github.com/rgreenblatt/no_cot_math_public (URL taken from the "Measuring no-CoT math time horizon"
  post; repo not fetched). The CoT-verbalizer post links no eval code; grading rubric text is in the post.
- Other: `syvb/qwen3-last-position-patching` (last-position residual patching data, Qwen3 0.6B-14B),
  `syvb/delta-nla-qwen3-8b-{av,ar}-warmstart` (someone is already building difference-NLAs).

## 4. Prices looked up 2026-11-14

- RunPod on-demand (runpod.io/pricing): A100 PCIe 80 GB $2.09/h, A100 SXM $2.19/h, H100 PCIe $2.89/h, H100 NVL
  94 GB $3.19/h, H200 141 GB $5.29/h, L40S 48 GB $1.09/h, A6000 48 GB $0.69/h.
- OpenRouter (api/v1/models), $ per million tokens in/out: claude-sonnet-5.5 2/10 (batch 1/5), claude-haiku-5.5
  0.10/0.50 (batch 0.05/0.25), claude-opus-5.5 4/20 (batch 2/10), claude-opus-4.7 5/25, qwen3.5-9b 0.046/0.068.
- Tinker cannot inject or extract activations, so everything here needs a rented GPU.
- NLA training cost anchors: full Qwen3-8B NLA from public warm-start data = 12-16 H200-hours (~$65-85);
  a 400-step RL run at batch 256x8 on a 9B model = ~68 A100-hours (~$142); at batch 64x8 about a quarter of that.

## 5. Brainstorm

Kept:
1. **Does lower reconstruction error buy surfaced reasoning? (proposal 01).** Continue RL on the public Qwen3-8B
   NLA on last-position activations from templated no-CoT arithmetic with known constants, intermediates and
   answers; track, checkpoint by checkpoint, within-template FVU against "the rock" and regex specificity of
   prompt constants vs intermediate values vs model outputs; probe skyline and three read-vs-recompute checks.
   The CoT post's authors and a commenter both name this as the open question; nobody found testing it; either
   outcome is informative. ~$380.
2. **Do independently trained NLAs agree? (proposal 02).** For Qwen3-8B L24 and Qwen2.5-7B L20 there are now
   2-3 public NLAs each, trained with different warm starts and code. Claim-level agreement across them as (a) a
   measure of how much of an explanation is warm-start/seed artifact (the init post's worry) and (b) a practical
   hallucination filter, against same-NLA resampling, adjacent-token agreement and deletion-FVE. Inference
   only. ~$230.

Rejected:
- **Re-run the internal-CoT eval on newer NLAs (Qwen3.6-27B, Matryoshka, MAEM).** Natural, but no eval code is
  public, Opus grading costs ~$125 per model, and it is a re-tabulation; the within-variant FVU and regex parts
  are folded into proposal 01.
- **Probe/patching skyline for where no-CoT reasoning lives (layer, position).** Useful but is a methods note on
  its own; it is the phase-0 gate of proposal 01.
- **Edit-and-steer with proper controls.** The post already ran the random-vector control (10/65 vs 11/65); VERS
  (2611.03040) covers explanation-edit steering at scale.
- **Scale the init experiments to a bigger model.** A 27B NLA from scratch plus ~250k confabulated warm-start
  explanations is beyond $500 and the authors' own corrigendum already strengthened the result.
- **KL-coefficient x init sweep.** Corrigendum covers KL 0 vs 0.01; Flow-NLA and reward-fixing work address the
  objective. Incremental.
- **"Mechanical" inits (last N tokens / sentences).** The author did it in the comments (64-token quote init,
  FVE 0.67).
- **Translator for the "pathological liar" NLA** (show its false explanations carry the same information).
  Nearly implied by equal FVE (the AR is such a reader); checkpoints not public, so it needs ~$150 of retraining
  for an expected result.
- **Does the warm-start prior create false eval-awareness alarms?** Important, but no ground truth for the
  model's belief without an eval-awareness organism plus an NLA for its base model; overlaps the eval-awareness
  cluster and the 8-karma "smaller NLAs and probes" post.
- **Shorter = truer? Claim-level audit of the released length-penalty adapters.** Cheap (~$80) but the expected
  finding (penalty keeps the last-token paragraph, drops theme claims) is largely anticipated by the
  observations, Matryoshka and deletion-gap posts. The lambda adapters are reused in proposal 02 as "same warm
  start, different RL run" siblings instead.
- **Low-dose concept-injection thresholds vs length penalty.** Concept injection with NLAs is done
  (LhDJdccLszLEAqgZ9); the lambda twist alone is thin.
- **Difference ("rock-subtracted") verbalization for math variants.** 2610.30934 and the public delta-NLA
  warm-starts show this is being built by others; kept only as an optional inference-only arm in proposal 01.
- **NLAs on model organisms / AuditBench / Taboo.** Done several times (xmmBTkogixvAbyQFk, 2610.30934,
  2609.37040, BcCcSfTHqz74kdTMF).
- **Paraphrase-bottleneck training against steganography.** Paper and 2610.18727 find paraphrase costs little;
  low expected information.
