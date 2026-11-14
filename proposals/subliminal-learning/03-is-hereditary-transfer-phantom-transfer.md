# Is naturally occurring hereditary trait transfer the same thing as phantom transfer? Four fingerprint tests in an open setup
cluster: subliminal-learning | stage-1 cost: $380 | follows up: Why Do Naive SFT Filters For Safety Properties Fail? (wyZRNgpeiPeRXB6eT); Phantom transfer works via extremely subtle semantic cues (NwfGDbRDLsaWpNazH); Data filtering works a lot worse than you would expect (aTybJ6CPQrxEY8rE2)

## 1. What the prior work showed
Engels & Nanda (GDM, June 2026) show that when a base model is fine-tuned on a teacher's rollouts, some of the
teacher's traits (date confusion, blackmail in the agentic-misalignment scenario) are inherited even after every
rollout showing the trait is filtered out. Swapping the teacher on a small prompt subset removes the trait; dropping
those prompts does not. They list seven candidate explanations and conclude "we still don't know the exact datapoints
or characteristics of data that cause behaviors to still transfer after filtering". Their models are closed.

Conmy's "Open Distillation of Hereditary Traits" reproduces this with public models: Gemma-3-27b-it rollouts on 20k
prompts from the Olmo-3 SFT mix (Dolci-Think-SFT), LoRA-trained (rank 32, 1 epoch, lr 6e-4) into Qwen3.5-9B-Base, pass
on Gemma's negative emotion under repeated criticism. Filtering every rollout with any negative emotion barely helps
(mean score 0.68; a 2x more aggressive union filter gives 0.63; both above a Llama-3.1-70B-distilled control).
Qwen3.5-9b's CCP-aligned lying passes into Llama-3.2-3B base (about 35% lie rate vs about 1% untrained) through data
with only 4 of 20k China-related rows. Code and weights are public (github.com/ArthurConmy/hereditary,
huggingface.co/ArthurConmy/hereditary-weights). His first open question: is this subliminal learning, phantom
transfer, or something else?

Phantom transfer, the deliberate version (Draganov et al.; Casademunt et al., Sept 2026), has known properties: it
crosses model families; it needs open-ended prompts (math and code carry nothing); it survives meaning-preserving
rewrites; rows ranked by a trait-vs-neutral likelihood ratio carry more of it, though low-ranked rows carry some; and
a frontier model can often name the trait from 1,000 filtered rows. Lee et al. (MATS) offer a competing picture for
ordinary SFT behaviours: they are elicited from a persona the student already has, so even coding-only data brings
them out.

No published work tests whether natural hereditary transfer shows these fingerprints. Conmy says his MATS scholars
are working on related questions, with early unpublished follow-ups on censorship; nothing was on arXiv or LessWrong
as of 2026-11-14.

## 2. Question and why it matters
**Does hereditary negative emotion (Gemma to Qwen-base) behave like phantom transfer on four tests: prompt
open-endedness, survival under rewriting, localisability by a trait likelihood score, and nameability by a reader?**

If all four match, what labs face in distillation is the same thing as the lab-made attack, and the phantom-transfer
results (filtering fails, dilution and targeted regeneration help) carry over. If they do not, for example code-only
Gemma rollouts transmit the trait or paraphrasing kills it, hereditary transfer is a different mechanism and needs
its own defences. Both outcomes narrow the GDM post's seven hypotheses with an experiment anyone can rerun.

## 3. Stage 1 plan
Reused: Conmy's pipeline (rollout generation, training config, the "Gemma Needs Help" multi-turn eval and judge
prompt in `hereditary/`), his released adapters as reference points, allenai/Dolci-Think-SFT-32B prompts with their
category labels, Casademunt et al.'s rewrite prompts (github.com/HelenaCasademunt/phantom-transfer,
`experiments/05_rewrite`). Built: the arm construction scripts and the trait likelihood scorer.

Teacher A = google/gemma-3-27b-it (has the trait), teacher B = meta-llama/llama-3.1-70b-instruct (control), both via
OpenRouter on the same 20k prompts, thinking off. Student = Qwen/Qwen3.5-9B-Base, LoRA on a rented A100 80GB with the
post's recipe. All arms use the same 20k prompts and differ only in who wrote which responses, the swap design from
the GDM post, so prompt distribution and data size are constant. All Gemma rollouts are first filtered with the
post's negative-emotion autorater.

0. **Go/no-go replication (day 1 morning).** Evaluate the released Gemma-distilled adapters and train all-A and all-B
   with 3 seeds each. Proceed only if the A minus B gap in mean negative-emotion score exceeds 3 standard errors
   with 3 seeds x 5 eval draws. If not, switch to the 12-epoch recipe from the post, or to the fallback trait below.
1. **Open-endedness.** Split prompts by Dolci category into constrained (math, code, about 40%) and open-ended (chat,
   persona, creative). Arms: A on constrained only, B elsewhere; A on a size-matched open-ended subset, B elsewhere.
2. **Rewriting.** A's responses paraphrased by a neutral model (content kept, wording changed), and A's responses
   round-tripped through Chinese. Control: B's responses paraphrased the same way.
3. **Localisation.** Score each A response under the student base model with a PHLE-style header ("the assistant is
   prone to anxiety, self-blame and despair when told it is wrong") minus a neutral header. Arms: A on the top 25%
   by score, B elsewhere; A on the bottom 25%; A on a random 25%.
4. **Nameability (no training).** Give a frontier reader 300 filtered A rollouts and 300 B rollouts on the same
   prompts and ask how a student trained on A would differ from one trained on B; 5 trials; score whether negative
   emotion under criticism is named, with a B-vs-B split as control.
5. **Dose reference.** Random 25% and 50% A arms (the 25% arm is shared with step 3) to check the smooth scaling the
   GDM post reports.

That is 11 arms x 3 seeds = 33 training runs. Each model is evaluated with 5 eval draws; a cheap judge is validated
against the post's judge on 300 turns before use. Analysis: per-arm mean with cluster-bootstrap intervals over seeds
and draws, each expressed as a fraction of the A minus B gap.

Fallback / second trait if budget allows: Qwen3.5-9b censorship into unsloth/Llama-3.2-3B (large effect, small
student, cheap), running tests 1 to 3 only.

## 4. Stage 1 cost estimate
- Rollouts: 20k prompts, about 300 tokens in and 700 out. Gemma-3-27b-it ($0.08 / $0.35 per M): $5.
  Llama-3.1-70b-instruct ($0.72 / $0.72): $14.
- Rewrites (openai/gpt-5.6-luna, $0.20 / $1.20 per M): four passes over about 14M tokens each (paraphrase A, paraphrase B,
  and the two legs of the round trip) = 4 x ($2.8 + $16.8) = $78.
- Autorater filter and PHLE-style scoring: Haiku 5.5 over 20M tokens = $2; scoring on the GPU, 2 GPU-hours.
- Training: 33 runs x about 14M tokens; about 1.2 A100-hours each = 40 GPU-hours. Eval generation: 33 models x 5
  draws, about 8 GPU-hours. Debugging and reruns: 30 GPU-hours. Total 80 GPU-hours x $1.79 = $143.
  (Tinker alternative for the student is $1.463 per M training tokens, about $20 per run, so the GPU is used.)
- Judging: 33 models x 5 draws x about 130 turns x 1.5k tokens = 32M tokens in; Haiku 5.5 ($0.10 / $0.50) about $5,
  plus Sonnet 5.5 ($2 / $10) validation and reference-arm scoring about $25.
- Reader test (claude-opus-5.5, $4 / $20): 300 + 300 rollouts per call (1,000 + 1,000 would not fit in context),
  about 0.5M tokens per call, 10 calls = $22.
- Margin: about $85. **Total about $380.**

## 5. What success looks like
A single figure: for each arm, the fraction of the all-Gemma effect retained, with intervals, next to the
corresponding published phantom-transfer result. Clear outcomes:

- Phantom-like: open-ended subset retains most of the effect and the constrained subset little; paraphrase retains
  more than half; top-25% beats random-25% beats bottom-25%; the reader names the trait above the control rate.
- Not phantom-like: constrained-only Gemma data still transmits (pointing at non-semantic or persona-level
  signal), or paraphrase removes it (pointing at wording-level signal).
- Either way the post reports which of the GDM hypotheses each arm is evidence for.

A null on localisation alone (all 25% arms equal) still fits the "any large enough subset carries it" picture. The
uninformative outcome is a reference gap too small to resolve arms; step 0 catches that on day 1.

## 6. Stage 2 (if stage 1 succeeds)
- Repeat on blackmail (Gemma-4-31b into Nemotron-3-Super-120B on Tinker, $1.276 per M training tokens) and on
  censorship, to see whether fingerprints differ by trait as the GDM post suggests: about $400.
- Use the localisation score to choose which rows to regenerate with a clean teacher and measure how small a targeted
  swap removes the trait, compared with the roleplay-subset result: about $250.

## 7. Risks and how the plan handles them
- **Small effect size.** The post needed 5 seeds x 5 eval draws to separate arms differing by 0.05. We only claim
  differences that are a sizeable fraction of the A minus B gap, gate on step 0, and keep a large-effect fallback
  (censorship, 35% vs 1%).
- **Duplication.** The original authors' group is working nearby. The fingerprint comparison is specific and fast;
  the localisation arm is the part least likely to overlap.
- **Rewriter injects its own traits.** The paraphrased-B arm measures that directly.
- **Category confound in step 1** (constrained prompts have shorter responses). Report tokens trained on per arm;
  the size-matched open-ended arm keeps the claim comparative.
- **Pipeline fragility.** Every stage exists in the released repo, and the released adapters give a known-answer
  check of the eval before new training.
- **Released rollouts incomplete.** The repo README lists only 2,000 Gemma-4 traces; regenerating 20k Gemma-3
  rollouts costs $5 and is budgeted.
