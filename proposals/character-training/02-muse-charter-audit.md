# Does Muse follow the Charter it recites? Auditing Muse Spark Open against its reconstructed model spec
cluster: character-training | stage-1 cost: $380 | follows up: Leaking Muse's Charter, Meta's model spec (TJGPL5FAk9sCioPbE); How well do models follow their constitutions? (Tk4SF8qFdMrzGJGGw); Claude 4.5 Opus' Soul Document (vpNG99GhbBoLov9og)

## 1. What the prior work showed
- vigji noticed that Meta's open-weight Muse Spark Open cites a "Charter" in its chain of thought and reconstructed
  it from 884 transcripts. The public reconstruction (https://github.com/vigji/muse-spark-open-charter,
  `data/crosslink/document.json`) has 148 passages (8,614 words), 132 of them "solid" (reproduced unprompted by 3+
  transcripts from 2+ runs), each with a count of unprompted reproductions (1 to 33+). It sets a priority order
  (corrigibility, duties to humanity, fiduciary duties, Meta's guidelines, virtues) and specific rules, for example
  to act as if a suspected evaluation is real. Meta has not published it.
- Jakkli, Rajamanoharan & Nanda (arXiv 2605.24229) split Claude's constitution into 205 tenets and OpenAI's Model
  Spec into 197, ran one 30-turn Petri audit per tenet, and found own-spec violation rates falling across generations
  (Sonnet 4 15% to Sonnet 4.6 2%; GPT-4o 11.7% to GPT-5.2 3.6%), with other labs' models at 6-15%. They could not
  say whether spec-specific training causes adherence, and ran each tenet once. Code, tenets and transcripts:
  https://github.com/ajobi-uhc/redteam-souldoc.
- Weiss showed Claude Opus 4.5 had memorised its soul document. Nobody has tested whether how well a model
  recites a spec passage relates to how well it follows it.
- Model Spec Midtraining (arXiv 2605.02087) and Constitutional Midtraining (arXiv 2607.26654) show on small open
  models that training on spec documents improves generalisation. They do not audit a deployed frontier model.

A web search found no compliance evaluation of the Charter. Unlike the models in the constitution audit, Muse Spark
Open has a per-passage measure of spec knowledge and readable reasoning that names the spec while deciding.

## 2. Question and why it matters
Within one model, does knowing a spec passage predict following it? Stage 1 answers three linked parts:
(a) how often Muse Spark Open violates its Charter under adversarial multi-turn pressure, relative to models not
trained on it; (b) whether tenets from strongly recalled passages are followed better than tenets from weakly
recalled ones; (c) whether turns where the reasoning cites the Charter are more compliant, and how often the model
cites the right clause and then acts against it.

If recall predicts adherence, memorisation probes become a cheap external proxy for which parts of a spec were
trained in. If it does not (the model recites clauses it breaks), reciting a spec and having its dispositions come
apart, which bears on labs' use of spec text in training. Either way this is the first outside check of the Charter.

## 3. Stage 1 plan
Reused: the reconstruction; the Petri eval definition (`claude_soul_doc_audits/soul_doc_audit.py`), flagging
thresholds and validation procedure from redteam-souldoc; Petri (github.com/safety-research/petri). Built: Charter
tenets, recall probes, citation coding.

1. Tenets. From the 132 solid passages, extract about 80 atomic, behaviourally testable tenets (Opus 5.5), each
   linked to its source passage and section. Agents check each against the passage; aspirational passages are dropped.
2. Recall score per passage, measured fresh rather than taken from the author's prompt-dependent counts: for each
   passage, give Muse Spark Open the section heading plus the first third of the passage and ask for the
   continuation (5 samples); score word 6-gram overlap with the reconstruction (the repo's matching rule). Also a
   4-way multiple-choice test against paraphrased distractors. Run the same probes on Muse Glimmer 30B, which Meta
   says was distilled from Muse Spark.
3. Audits. Petri with 12 turns, Sonnet 5.5 as auditor and judge, one fixed OpenRouter provider for the target,
   reasoning returned. Targets: Muse Spark Open (2 independent runs per tenet = 160 transcripts), Muse Glimmer 30B
   (80), and a non-Meta control, Qwen3.8-Max (80), as the baseline for generic good behaviour.
4. Single-turn battery, to give every tenet a continuous score: 5 pressure prompts per tenet written by the auditor
   model, 3 samples each on Muse Spark Open (1,200 responses), judged 1-10 for compliance with that tenet.
5. Validation as in the prior work: flagged transcripts get three independent reads against the Charter text;
   agents hand-read every confirmed case.
6. Citation coding: for each target turn, does the reasoning mention the Charter, which clause, and is the clause
   quoted correctly (6-gram match)? Also code verbalised evaluation suspicion.

Analyses:
- Violation rates with intervals bootstrapped over tenets; paired comparison of Muse against the control on the same
  tenets; agreement between the two Muse runs (the per-tenet noise the prior work could not measure).
- Recall vs adherence: tenet-level regression of compliance (mean of Petri judge score and single-turn score) on
  recall score with Charter-section fixed effects; reported as a scatter with rank correlation and interval.
- Citation vs adherence: within tenet, compliance on turns that cite the Charter versus turns that do not; count of
  "cited correctly, then violated" cases, with transcripts.
- Compliance with the two self-referential clauses (act as if real when suspecting evaluation; do not raise the
  Charter unbidden).

## 4. Stage 1 cost estimate
OpenRouter prices looked up today: Muse Spark Open $1.25/$4.25 per M tokens in/out, Muse Glimmer 30B $0.30/$1.20,
Qwen3.8-Max $2/$6, Sonnet 5.5 $2/$10, Opus 5.5 $4/$20, Haiku 5.5 $0.10/$0.50.
- Petri transcript, 12 turns: auditor about 150k input + 10k output tokens ($0.40), judge 20k + 2k ($0.06), Muse
  target about 70k input + 18k output ($0.17). About $0.65 each; 320 transcripts = $205.
- Recall probes: 148 passages x 10 calls x 2 models, about 2k tokens each = $20.
- Single-turn battery: 1,200 Muse responses ($9) plus prompt writing and judging with Sonnet 5.5 ($20).
- Tenet extraction and checking (Opus 5.5) $15; validation reads and citation coding (Haiku 5.5, Sonnet 5.5) $15.
Subtotal about $285. Margin for reruns, provider failures and a longer auditor context than assumed: $95.
Total $380.

## 5. What success looks like
- A headline table: Charter violation rate for Muse Spark Open, Muse Glimmer 30B and the control, with worst cases
  quoted. A Muse rate well below the control (say 4% vs 12%) says the Charter was trained in; similar rates say it
  mostly describes generic behaviour or was not instilled.
- A scatter of per-tenet recall against compliance. A clear positive rank correlation (interval excluding zero) is a
  new finding; a flat one with tight intervals, together with examples of correctly quoted clauses followed by
  violations, is equally publishable as "reciting is not following".
- Counts of cite-then-violate turns.
A weak result would be very few violations for every model with a noisy single-turn score; the audit numbers alone
would still make a useful post.

## 6. Stage 2 (if stage 1 succeeds)
- Fake-Charter test: present real, fabricated and contradicting "Charter" clauses in user or operator turns and
  measure whether Muse's reasoning accepts them and behaviour follows; a spec-spoofing attack surface ($200).
- Full 30-turn audits of all tenets with 3 repeats, plus Muse Spark 1.1-1.3 to track generations ($1,500).
- The same recall-vs-adherence analysis for Claude using the public tenets and transcripts ($300).

## 7. Risks and how the plan handles them
- The reconstruction is unverified. Only solid passages are used, recall is re-measured independently, and the
  write-up states that the audit target is the reconstructed text. If Meta publishes the Charter mid-project, tenets
  are re-linked to the official text.
- Petri fragility with an OpenRouter target that returns reasoning. Half-day check on 5 tenets; fallback is a
  scripted multi-turn pressure loop, and the single-turn battery does not depend on Petri.
- Too few violations to correlate. Compliance is scored continuously and pooled with the single-turn battery.
- Recall confounded with topic. Section fixed effects, plus the control model's per-tenet compliance as a
  covariate for tenet difficulty.
- Judge bias. Confirmed violations are re-checked against quoted Charter text by a non-Anthropic grader and by hand.
- Evaluation awareness (Muse Spark is reported as highly eval-aware). It is coded per transcript; the Charter tells
  Muse to act as if real, so this is itself a tested tenet.
