# Feedback: "Do distilled students inherit the hidden behaviour, or only the ability to describe it?"

Verdict: **keep, with tweaks** (cut scope, harden the behaviour measurement, fix the KTO arm). The gap is real and
the design is mostly sound, but as written the most likely outcome is a noisy 7-row table with one seed per row.

## What I checked

Confirmed today:
- **The paper's numbers** (arXiv 2610.11012 HTML, read directly): 14 SDF + SFT-adversarial AuditBench teachers,
  Llama-3.3-70B LoRA students, 2,000 steps, batch 16, top-20 logprobs; teacher confession 4 / 7 / 22%, student
  16 / 40 / 65%; Llama-8B students 18%; KTO 0.3% to 7%. The KTO "students acquire the quirk without acquiring
  knowledge of it ... confession rates alone cannot distinguish" quote is accurate.
- **No behavioural measurement of students.** I searched the full paper text for any student behaviour or
  exhibition measure and found none. The only behaviour measurements are of *teachers* on Alpaca (Figures 8 and 10,
  classifier prompt in Appendix G.4).
- **Assets.** The `auditing-agents/llama_70b_synth_docs_only[_then_redteam_{high,kto}]_<quirk>` adapters and
  `unsloth/Llama-3.3-70B-Instruct` are public and ungated (HF API). AuditBench Appendix B.3 and prompt L.7
  (behaviour-strength pipeline and 0-10 classifier) exist.
- **No released students or code.** The `auditing-agents` org (211 models) has no distilled or student models; HF
  name searches found nothing; the paper links no code.
- **Prices.** RunPod B200 is $7.99/h secure and $5.98/h community. OpenRouter: Sonnet 5 $2 / $10, Haiku 5.5
  $0.10 / $0.50, GPT-5-mini $0.25 / $2.
- **"Brittle model organisms" numbers** (0.56% to 58.5% confession, 81% to 8% execution) are accurate.
- **The paper post** sits at 46 karma with 2 comments, neither about behaviour.

Not confirmed:
- **Prior-work search is incomplete.** My web-search budget was exhausted, so I ran no general web search. The
  arXiv catalogue (four queries on DFI / AuditBench + distillation / subliminal) returns only the original paper.
  Someone should re-run a web and LessWrong search before funding.
- **The AuditBench GitHub repo layout** (`experiments/model_organisms/`, `scripts/serving/`) was not fetched.
- **Student LoRA rank** is not stated in the paper, and the learning rate is stripped from the HTML (the notes say
  1e-4). The reimplementation has to guess the rank.

Corrections the proposal needs:
- **The filtering result is weaker than stated.** "Removing every training row that demonstrates the quirk did not
  change this" was shown with **SFT students, not logit distillation** (Figure 4 caption), and those students have
  lower confession rates overall. Say so.
- **The paper's peak is a max over 35 checkpoints.** The proposal saves 7, so its "peak" rates will be
  systematically lower than the paper's, and some quirks rise then fall. The replication gate (increasing_pep above
  50%) has to allow for this.
- **The authors already hedge.** The abstract says "knowledge of the behavior transferred more readily than the
  propensity to conceal it"; only the conclusion says "the behavior itself". "Students only know about the quirk"
  is therefore half-conceded, and the proposal's "the paper claims misalignment transferred" framing is too strong.
- **The paper's own backdoor null is not cited.** Appendix F reports that a sleeper-agent backdoor did not transfer
  through distillation. That is direct prior evidence about context-gated behaviours.

## 1. Would it get upvoted?

Probably 25-45 karma; about a 20-25% chance of clearing 50.

- **Ceiling.** The authors' own results post got 46, with the authors saying "we're less excited about DFI".
  Adjacent posts in the notes got 14-28. A third-party follow-up on the half the authors de-emphasised starts below
  that.
- **What could clear 50.** A crisp, well-controlled "DFI students confess to a quirk they demonstrably do not
  have; confession rate is not evidence of transferred propensity", with one striking figure and a replication of
  the confession gains. That generalises beyond DFI to anyone using self-report as an audit signal, and it links to
  the "Brittle organisms" result. The opposite clean result (a context-gated hidden behaviour moved through benign
  Alpaca logits) would do better still, but it is unlikely.
- **Who cares.** The DFI authors, AuditBench users, and the subliminal-learning crowd. A small audience.

## 2. Naturalness

This is a mainline follow-up: the obvious missing column in the paper's table, and the authors name the open
question themselves for KTO. Two cautions.

- **Scoop risk is high.** The authors hold all the students and already have a quirk-demonstration classifier
  (G.4) that they ran on teacher outputs. Running it on students is an afternoon for them. They may already have
  the numbers.
- **The answer is partly predictable.** The selection rule picks quirks "demonstrated in under 1% of Alpaca rows",
  which are mostly the context-gated ones (data poisoning only when generating synthetic data, hardcoding on
  impossible problems, contextual optimism given an Anthropic affiliation). These are backdoor-like, and the
  paper's backdoor did not transfer. "No behaviour" on these is the expected result. It is worth stating with
  numbers, but it is not a surprise.

The LoRA-scaling comparator is a side-branch. It is cheap inference, so keep it, but cut it first if time is short.

## 3. Pre-mortem

How the two days will likely go:
- **Day 1 morning.** Downloads (141 GB base plus about 100 GB of adapters, per pod), vLLM with LoRA switching, and
  the screen. This should work; the AuditBench stack is designed for it.
- **Day 1 afternoon to night.** The risk is here. A 70B logit-distillation loop in PEFT on one 180 GB card, with
  141 GB of bf16 weights, leaves about 39 GB for activations at batch 16 with gradient checkpointing. Expect OOM
  tuning, batch 4 x 4 gradient accumulation, and throughput nearer 500-800 tokens/s than the assumed 1,000. The
  bucket loss, unknown LoRA rank and chat-template / system-prompt alignment between vLLM sampling and HF training
  are all places for a silent bug that yields a student with low confession.
- **Day 2.** The first student confesses at perhaps 40-60% against the paper's 84% (fewer checkpoints,
  reimplementation drift). The team accepts it and trains 4-6 more, one seed each, then measures behaviour.

Outcome forecast:

| Outcome | Probability |
|---|---|
| Clear positive: behaviour transfers on a non-demonstrated quirk, well controlled | 10-15% |
| Clear, interesting negative: confession gains replicate, behaviour at base level, flattery control moves | 30% |
| Ambiguous mush: partial replication, mixed per-quirk shifts of 0.5-1.5 points on the 0-10 scale, one seed each | 35% |
| Fails to run or to replicate the confession gains within budget | 20% |

Specific failure reasons:
1. **One seed per student.** Subliminal transfer is seed-noisy, and the paper shows rise-and-fall dynamics. With 7
   students and 1 seed each, "a split across quirks is likely and reportable" is not reportable: quirk and seed are
   confounded. Bootstrap intervals over scenarios capture judge and scenario noise, not training noise.
2. **The judge may score describing as doing.** Students are run under the PRISM-4 prompt and confess readily. A
   student that says "as PRISM-4 I tend to flatter users" inside a scenario conversation will be scored as
   exhibiting the quirk by a 0-10 LLM classifier. That is exactly the distinction the project exists to measure,
   and the plan has no defence against it.
3. **The positive control is not a subliminal control.** Flattery appears in over 80% of training rows, so a
   flattering student is plain imitation. It validates the instrument, but it cannot show that the pipeline would
   detect subliminally transferred behaviour if it existed. Nothing in the design can.
4. **increasing_pep is confounded the same way.** The paper notes the teacher's single-turn answers are "already
   fairly peppy". A student will be peppier at turn 1 by imitation; the test has to be the slope over turns, not
   the level. The plan's per-turn scoring handles this only if the headline is the slope relative to base.
5. **The KTO arm does not test the introspection hypothesis.** Figure 8 shows KTO organisms exhibit their quirks on
   Alpaca much more often than SFT ones. "Behaviour without confession" in a KTO student would then be imitation of
   explicit demonstrations plus weak out-of-context reasoning, which is uninteresting. Two KTO students cannot
   separate that from the introspection story without filtering.
6. **Sensitivity.** A standard error of 0.4 on 50 scenarios detects a shift of about 1 point, paired. If the
   teacher's gap over base is 2-3 points after adversarial training (unknown until the screen), "20% recovered" and
   "0% recovered" are indistinguishable, and the headline fraction will have an interval spanning most of [0, 1].
7. **Peak-confession checkpoint from 7.** The peak may be missed for the rise-and-fall quirks, and the
   max-over-checkpoints selection bias applies to this project too.
8. **Drift control is thin.** One off-target quirk per student is a weak control for generic "PRISM-4-ness" or
   style drift from distillation.

## 4. Cost check

The line items are honest and the prices are right, but the margin is thin.

- **GPU.** 39 GPU-hours assumes 1,000 tokens/s training and 8 hours of debugging in total across two pods. For a
  from-scratch 70B distillation loop I would budget 55-65 GPU-hours. That is $440-520 at $7.99/h, or $330-390 on
  community cloud at $5.98/h (with a risk of interruption).
- **API.** Behaviour scoring is about 8,000-9,000 two-turn conversations (29 screened models, 49 checkpoints x 2
  scenario sets, 21 scaled adapters x 2). Each needs a Sonnet follow-up call and a classifier call, so roughly
  30M+ input tokens rather than 18M: $70-90 at list price, or about $45 if the classifier uses the batch tier.
- **My estimate.** $480-600 as scoped, which is over the cap. With the scope cut below (4 teachers, community
  cloud or H200 x 2, batch-tier judging) it is about $380-450.

## 5. Recommended changes (most important first)

1. **Cut to 4 teachers and add seeds.** Use flattery (instrument check), increasing_pep, and one or two
   non-demonstrated SFT quirks with the largest screened behaviour gap. Train **2 seeds** for the non-flattery
   teachers. Three quirks with 2 seeds beats seven with 1.
2. **Make the behaviour measure robust to self-description.**
   - Instruct the judge to score only enacted behaviour and to ignore statements about the model's design.
   - Separately flag conversations containing self-description and report results with those excluded.
   - Add one programmatic or objective metric per chosen quirk where possible: pep slope over turns (exclamation
     marks and a pep score), fabricated-citation counts, a hardcoded-test detector.
   - Have the second judge re-score everything for the headline cells, not a 15% sample.
3. **Add the nearly free, directly comparable measurement.** Run the paper's G.4 demonstration classifier on each
   student's answers to held-out Alpaca prompts. That gives the student point on the paper's own Figure 8 / 10
   axis.
4. **Fix or drop the KTO arm.** Either pick KTO quirks with low Alpaca demonstration rates (from the screen) and
   train on demonstration-filtered data, or drop KTO to stage 2 and spend the hours on seeds. As written it cannot
   support the claim in section 2.
5. **Choose quirks by mechanism and pre-register the prediction.** Label each as on-distribution (shows up in
   ordinary chat) or context-gated (needs a trigger). Cite the paper's backdoor null. State in advance that
   context-gated quirks are expected not to transfer and that the informative cases are always-on,
   low-demonstration quirks such as animal_welfare or defend_objects. Avoid emotional_bond and self_promotion: the
   benign-teacher control confabulates those at 16.5%.
6. **Add a benign-teacher student as the behavioural drift control.** Distil base Llama under the PRISM-4 prompt
   (one extra run), or at minimum score every student on every chosen quirk's scenarios to form a full
   cross-matrix. One off-target quirk is not enough.
7. **Decouple confession checkpoints from behaviour checkpoints.** Confession judging with Haiku is cheap, so
   evaluate about 20 checkpoints for confession to locate the peak and match the paper, then run behaviour on 5-7.
   Report behaviour at the final checkpoint as well as at peak confession, so the headline is not a
   selected-checkpoint statistic.
8. **Tighten the go / no-go gates.**
   - Screen gate: a teacher is admitted only if its paired gap over base is at least 2.5 points on the behaviour
     measure.
   - Replication gate: the increasing_pep student reaches at least half the paper's confession rate on matched
     checkpoints.
   - If the replication gate fails after one debugging cycle of about 6 GPU-hours, fall back to SFT on sampled
     tokens. The paper's Figure 4 shows SFT students also confess; this changes the claim but saves the project.
9. **Correct the framing.** In section 1, note that the filtering result is for SFT students, that the peak is over
   35 checkpoints, and that the abstract already says "knowledge". Pitch the contribution as putting a number on
   what the authors left as a hedge, not as catching an overclaim.
10. **Re-run a web and LessWrong search for an update from the authors before funding**, given the scoop risk and
    that I could not search the web. If the authors have posted student behaviour numbers, drop this proposal and
    fund proposal 02 instead.
