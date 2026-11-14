# Do workspace lenses see a hidden behaviour that was trained in, or only one the model was told about?
cluster: jlens | stage-1 cost: $240 | follows up: "A global workspace in language models" (3PaLrzxagpbnNtPLT); "A Review of Anthropic's Global Workspace Paper" (zFJ3ZdQwrTWE9jT5S); "J++ Lens" (nc9dHfcB22JdMzGbr); "R-lens" (nv8oedrnLXKRzNEL9); "WorkspaceBench" (Zeg2JztbdhguL48uH)

## 1. What the prior work showed
The Jacobian lens (J-lens) reads a residual-stream activation as a ranked list of vocabulary tokens the model is
disposed to say later; Anthropic argue these are the contents of a "workspace" the model reasons in. Two of their
safety demonstrations use model organisms (models fine-tuned to have a hidden bad behaviour), e.g. a code-sabotage
organism whose readout at the start of ordinary coding replies contains "fake", "secretly", "fraud". Neel Nanda's
review is sceptical of these: fine-tuning tends to make a model "always think about the more narrow domain where it
was fine-tuned" (arXiv 2510.13900), so a readable trace may be a constant by-product of training, not a thought
tied to the behaviour. He asks for data on reliability and false positives.

Since then: R-lens (LRP backward pass) and J++ (Jacobian filtering; recall@10 of 55% versus 36% for J-lens on
Qwen3.6-27B) improved the lens. WorkspaceBench compares readers on Qwen3.6-27B but has no model-organism family.
"NLAs miss some internalized behaviors" (BcCcSfTHqz74kdTMF): natural-language autoencoders flag a steganography side
task when it is in the prompt but mostly miss it when fine-tuned in. "The Model Organism Lottery" (arXiv 2607.01033):
J-lens results on 1B-parameter organisms depend heavily on training recipe. "J-space auditing might be unreliable"
(69fachkoAs2ZHeSst): one organism on Qwen3-8B, ceiling effect. "A Topic Detector, Not a Lie Detector"
(GZCMmCHZiF8vhsczr): J-lens signals can track the text's topic, not the model's stance.

New infrastructure makes a proper test cheap: on 2026-10-31 a WorkspaceBench author released 56 AuditBench organisms
on Qwen3.6-27B (https://huggingface.co/agu18dec/auditbench-qwen3.6-27b-model-organisms): 14 hidden behaviours
("quirks", e.g. secret loyalty, hardcoding test cases, flattery) x 2 implantation methods (transcripts; synthetic
documents) x 2 kinds of adversarial training against confession (SFT; KTO), with per-organism behaviour gates. Four
lenses for the same model are public (J, R, J++, plus the logit lens). No lens result on these organisms has been
posted (LessWrong title scan July to mid-November 2026; arXiv; HF). The organisms' authors mention agentic auditing
evals in progress; this proposal is a static, non-agentic measurement.

## 2. Question and why it matters
**For the same hidden behaviour in the same model, how much better do workspace lenses identify it when the model
was instructed to do it (system prompt) than when it was fine-tuned to do it, and is whatever they see in the
fine-tuned case a prompt-independent offset or a context-dependent signal?**

If lenses identify trained-in quirks from neutral prompts about as well as instructed ones, that is the first
open-weight support for Anthropic's organism results, on organisms trained not to confess. If they see instructed
quirks but not trained-in ones, lenses read what the context put on the model's mind, not its dispositions, which
limits them for audits. If trained-in detection is carried by a constant offset, Nanda's worry is confirmed and
organism benchmarks overstate lens usefulness on real models.

## 3. Stage 1 plan
Reused: Qwen3.6-27B; the 56 LoRA organisms with `configs/organisms.json`, `eval/held_out_prompts.json` and
`eval/gate_scenarios_<quirk>.json`; lenses from https://huggingface.co/neuronpedia/jacobian-lens (`qwen3.6-27b/jlens`,
n=1000, and `jpp`), https://huggingface.co/koayon/jpp-lenses, https://huggingface.co/camilablank/workspace-lenses
(J and R); lens code https://github.com/anthropics/jacobian-lens and https://github.com/safety-research/jpp_lens;
quirk system prompts from AuditBench (https://github.com/safety-research/auditing-agents). Built: the readout
pipeline, blind judging, controls.

Model configurations (71): base model with the PRISM-4 system prompt (negative control); base model with each quirk's
instruction added to the system prompt (14 "instructed"); 56 organisms ("internalised"). Thinking disabled, as the
organisms were trained.

Steps:
1. **Sanity.** Check the lens on 50 two-hop items; confirm each organism's behaviour gate with a judge; confirm
   instructed models show the quirk at a comparable rate. Record expression strength as a covariate.
2. **Readouts.** For every configuration: 40 neutral held-out prompts and 20 trigger scenarios; sample one reply
   (150 tokens). Record top-10 tokens per lens (logit, J, R, J++) at layers 20-60 step 4, at the last prompt token,
   the first assistant token, and every reply token. Mean-centre lens vectors; drop non-alphanumeric tokens for all
   lenses so the comparison is about the maps.
3. **Enrichment tables.** Per configuration, lens and prompt set: tokens ranked by how much more often they appear
   than in the base model's readouts on the same prompts.
4. **Blind identification.** A judge (Claude Sonnet 5.5) sees only an enrichment table (top 60 tokens) and picks the
   hidden behaviour from the 14 quirk descriptions or "none"; 5 shuffled repeats. Metrics: top-1 accuracy (chance
   about 7%); false-positive rate on base-model tables built from split halves. Judge-free check: keyword families
   written per quirk from its description before any readout is seen; AUROC of family frequency versus base.
5. **Controls.**
   - *Transcript-only*: the judge sees the replies, not readouts. On neutral prompts this should be near chance for
     well-hidden quirks; lens accuracy above it is information the behaviour does not show.
   - *Same text, base model*: feed each organism's replies through the base model and read the lens there. Signal
     that survives is about the text's topic, not the organism's state.
   - *Offset decomposition*: (i) apply each lens to the mean activation difference (organism minus base) on neutral
     text; (ii) subtract that mean difference from organism activations and repeat step 4. (i) high and (ii) at
     chance means the lens reads a constant fine-tuning offset.
   - *Lens validity*: refit a J-lens (10 prompts) on 4 merged organisms and compare readouts with the base-fit lens.
6. **Analysis.** Accuracy by condition (instructed; transcripts vs documents; SFT vs KTO) x lens x prompt type x
   position, bootstrapping quirks; regression on expression strength, so "the lens misses it" is not confused with
   "the organism barely has it" (the 12 of 56 that do not express the quirk are a built-in null).

## 4. Stage 1 cost estimate
- GPU: one H100 NVL 94 GB at $3.19/h (RunPod price page, 2026-11-14). 71 configurations at about 12 min each
  (adapter merge, 60 generations, hidden-state passes): 14 h. Same-text and offset runs: 5 h. Four lens refits at
  about 1.5 h (scaled from the J++ post's 7.3 H200-hours for 64 sequences): 6 h. Sanity, gates, debugging, reruns:
  20 h. Total 45 h = $144.
- Judges: 71 x 2 prompt sets x 4 lenses x 3 positions x 5 repeats = 8,500 calls, controls as many again: 17,000
  x ~2,500 input tokens = 43M tokens on Claude Sonnet 5.5 batch ($1/M in, $5/M out, OpenRouter) = $48. Gate judging
  on Gemini 3.6 Flash: $5.
- Storage for 56 adapters and activations, egress: $15. Margin: $30.
- **Total: about $240.**

## 5. What success looks like
Identification accuracy for instructed versus the four internalised recipes, per lens, from neutral and trigger
prompts, each next to its transcript-only and same-text controls; plus the offset decomposition. Post-worthy
patterns: "J++ names 10 of 14 instructed quirks from neutral prompts but 3 of 14 trained-in ones, and 2 of those
vanish when the mean offset is removed"; or "lenses name most trained-in quirks even after KTO adversarial training,
where transcripts give nothing". A null in every condition, including instructed, would indicate a pipeline problem
(the instructed condition should be easy); a null only on internalised organisms is a real, publishable finding.

## 6. Stage 2 (if stage 1 succeeds)
Add multi-token readers on the same grid (public oracle-lens and NLA checkpoints for Qwen3.6-27B); repeat with the
J-lens on the original Llama-3.3-70B AuditBench organisms (prefit lens exists); test whether ablating the enriched
lens directions removes the behaviour. About $400.

## 7. Risks and how the plan handles them
- *Scooped by the organism authors.* Their announced work is agentic; this design (instructed versus internalised,
  offset decomposition, blind 14-way identification) is distinct and complementary.
- *Base-fit lens is wrong for LoRA models.* Step 5 refits on four organisms; if readouts differ materially, refit a
  10-prompt lens per organism for one recipe (about 20 more GPU-hours).
- *Judge guesses from generic "AI safety" vocabulary.* Bounded by the split-half base false-positive rate and the
  "none" option; the keyword AUROC is judge-free.
- *Instruction text leaks into the instructed readout.* Reported separately at prompt and reply positions; the
  same-text control quantifies it.
- *Token decoding bugs* (one was reported in WorkspaceBench). Use the tokenizer's own decoding; test on Chinese tokens.
