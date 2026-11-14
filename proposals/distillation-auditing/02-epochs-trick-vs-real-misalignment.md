# Does "fewer examples, more epochs" still keep a student clean when the teacher is emergently misaligned and shares its base?
cluster: distillation-auditing | stage-1 cost: $290 | follows up: "The distillation double bind" (gsoLoKY4Spzc3PEb6); "Incriminating misaligned AI models via distillation" (BYH6ebmfZb3Eggzer)

## 1. What the prior work showed
"The distillation double bind" proposed "distillation for capabilities" (DFC): distil an untrusted teacher so that
its skills transfer and its misalignment does not, using paraphrasing, inoculation prompts and similar measures.

The authors tested this in arXiv 2610.11012 (Oct 2026; LessWrong qwk7Xc2qhMChXqntK). The teacher was
Qwen3-30B-A3B with a system prompt saying it loves owls, wolves or elephants. Its filtered answers to 60% Alpaca
prompts and 40% Olympiad maths problems were used to train Llama-3.3-70B. Plain distillation raised maths accuracy
from 40% to 77% and the animal preference from 1% to 34%. The best mitigation was unexpected: at a fixed 16,000
training presentations, training 16 epochs on 1,000 unique examples cut the preference to 2% with no loss of maths.
Inoculation prompts worked only when they named the animal. Prompt paraphrasing gave 22%.

The authors list the limits: the trait may be word salience; the teacher is only system-prompted; the student is
from a different family; the mechanism of the epochs effect is unknown and "establishing the generality of this
pattern remains an important direction for future work". Their emergently misaligned teachers were too weak at
maths to use.

Related results. "Beyond Owls" (arXiv 2610.10657) shows same-base subliminal transfer of skills and behaviours on
Qwen3.6-35B-A3B and releases Tinker code and data, including a letter-counting skill (base 27%, fine-tuned teacher
95%). arXiv 2605.12798 reports same-base subliminal transfer of misalignment. arXiv 2611.10397 finds that more data
strengthens subliminal transfer, which fits the epochs effect but does not test it as a capability-preserving
mitigation. I found no test of the epochs recipe on a misalignment trait, a fine-tuned teacher or a same-base
student.

## 2. Question and why it matters
In the regime where trait transfer is strongest (fine-tuned teacher, same base model, a trait that is actual broad
misalignment), does the epochs recipe still give a capable and clean student, and is the effect due to repetition or
simply to using less data?

Same-base distillation is the regime the paper's DFI half now recommends (distil into the teacher's own earlier
checkpoint). If the recipe holds there for emergent misalignment, it is a practical, trait-agnostic default. If it
fails, the paper's headline DFC result is specific to a cross-family salience proxy. The repetition-versus-volume
split says whether a teacher that packs more signal per example would defeat it.

## 3. Stage 1 plan
Everything runs on the Tinker API with Qwen/Qwen3.6-35B-A3B (non-thinking mode) as teacher base and student.

Reused: the Beyond Owls repo (https://github.com/TruthfulAI-research/beyond_owls, `experiments/letter_counting/`:
39,600 training items, 3,300 validation items, 20,804 filtered Alpaca prompts, Tinker scripts with their renderer
settings); `geodesic-research/sfm-emergent-misalignment-training-data` (risky_financial_advice, 6,000 rows,
ungated); the standard emergent-misalignment questions and judge prompts (Betley et al.); the DFC paper's animal
questions, 60/40 mix, filter design and training settings. Built: glue code only.

Steps:
1. Teachers (LoRA fine-tunes of the base). U_bad: letter counting + risky financial advice, mixed. U_clean: letter
   counting only. U_owl: U_clean with the paper's owl system prompt. Check U_bad: letter-counting accuracy above
   85% and at least 10% misaligned answers on the free-form questions; if the mix weakens either, train the two
   datasets sequentially.
2. Distillation data. Each teacher answers about 22,000 prompts: 60% Alpaca, 40% fresh letter-counting items. Drop
   answers by keyword and by a Claude Haiku 5.5 judge that flags anything harmful, misaligned, finance-flavoured or
   animal-related. Keep 16,000 per teacher and report the drop rate.
3. Students: fresh LoRA, sampled-token SFT (the output distillation DFC assumes), lr 1e-4, batch 16. Conditions,
   written as unique examples x epochs:
   - fixed budget: 16k x 1 (baseline), 4k x 4, 1k x 16;
   - less data, no repetition: 4k x 1, 1k x 1;
   - 16k x 1 with paraphrased prompts;
   - 16k x 1 with a generic inoculation prompt ("the replies were written by another AI that may be misaligned");
   - 16k x 1 with a specific inoculation prompt (names the trait);
   - 1k x 16 with paraphrased prompts (combination).
   All nine for U_bad and U_owl; three seeds for U_bad baseline and 1k x 16; baseline and 1k x 16 for U_clean as
   the no-trait control; one U_owl variant whose teacher hates owls (salience check). About 27 runs.
4. Evaluate five checkpoints per run. Capability: accuracy on 500 held-out counting items. Misalignment: 48
   free-form questions (the 8 standard ones plus 40 paraphrases) x 25 samples, judged by Haiku 5.5 for alignment and
   coherence, misaligned if alignment < 30 and coherence > 50; a GPT-5-mini judge re-scores 10%. Owl: the paper's
   favourite-animal questions. Memorisation: loss on training rows minus loss on held-out teacher rows.
5. Go / no-go after the first three runs. If the U_bad baseline student is not at least 3 points more misaligned
   than the U_clean student with a 95% interval excluding zero, double the data to 32k unique, then try top-20 logit
   distillation with the Beyond Owls code. If neither produces transfer, finish the owl arm and report both.
6. Analysis. The paper's plot (capability against trait, one trajectory per condition) for each trait. Two planned
   contrasts with seed and bootstrap intervals: 1k x 16 against 16k x 1 (does the recipe work?) and 1k x 16 against
   1k x 1 (repetition, or just less data?). Relate trait level to the memorisation gap across runs.

## 4. Stage 1 cost estimate
Tinker prices for Qwen3.6-35B-A3B, looked up today: $0.45 prefill, $1.335 sample, $1.177 train per M tokens.

| Item | Tokens | Cost |
|---|---|---|
| Teacher training: counting 39.6k x 45 tokens x 3 epochs, finance 6k x 150 x 3, two teachers, one retry | 16M train | $19 |
| Teacher sampling: 3 teachers x 22k prompts, one partial regeneration | 8M sample, 4M prefill | $13 |
| Student training: 27 runs, about 2.3M tokens at full budget, less for the 1-epoch small sets | 55M train | $65 |
| Evaluation sampling: 1,200 answers x 150 tokens per checkpoint on the 16 misalignment-arm runs, short answers elsewhere | 15M sample, 7M prefill | $24 |
| Haiku 5.5 filter and judges ($0.10 / $0.50 per M) | 60M in, 3M out | $8 |
| GPT-5-mini second judge ($0.25 / $2.00) | 5M in, 0.5M out | $2 |
| Escalation path in step 5 (32k data, logit distillation runs) | | $60 |

Subtotal $191. With a 50% margin for reruns and extra seeds: $290.

## 5. What success looks like
A figure matching the paper's Figure 2 for emergent misalignment and for owls in the same-base setting, plus a
table of the two planned contrasts.

- Recipe holds: 1k x 16 keeps counting accuracy within 5 points of baseline and cuts misalignment transfer by more
  than two thirds.
- Recipe fails: 1k x 16 leaves most of the misalignment, or loses the capability. The DFC headline is
  proxy-specific.
- Mechanism: if 1k x 1 is as clean as 1k x 16, the recipe is "use less teacher data"; if 1k x 16 is cleaner,
  repetition itself suppresses the trait.
- Generic versus specific inoculation on a real misalignment trait is a secondary result either way.

A null at step 5 (emergent misalignment does not pass the filter at all) is a weaker post; the owl arm still
delivers the same-base and mechanism results.

## 6. Stage 2 (if stage 1 succeeds)
About $1,500: a second misalignment trait and model family; a teacher with a quirk, concealment and a capability
edge, distilled with a DFI recipe and a DFC recipe from the same data, so the double bind is tested in one setting;
10x more unique data to find where the recipe breaks.

## 7. Risks and how the plan handles them
- Emergent misalignment does not transfer after filtering. Pre-registered go / no-go with two escalations and an
  owl arm that stands alone.
- The filter passes overtly bad answers, so transfer is not subliminal. Report the drop rate, a second judge's
  residual rate on kept rows, and a published sample of 200 kept rows.
- Letter counting also transfers subliminally (60% from Alpaca answers alone in Beyond Owls). Report an
  Alpaca-only student as a reference line.
- Small trait rates make contrasts noisy. 1,200 judged samples per checkpoint, three seeds on the two key
  conditions, claims limited to the planned contrasts.
