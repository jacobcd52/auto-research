# Feedback: 02-latent-cot-tamper-detection

Verdict: **keep, but only with the design fixes in section 5.** As written, one of the two headline conditions
(deletion) is undetectable by construction, and the most likely "positive" result is one that readers will
dismiss as "off-policy text has higher perplexity", which arXiv 2605.25459 has already shown for chat models.

## What I checked

| Claim in the proposal | Status |
|---|---|
| Original post numbers (R1 42.2% / GPT-OSS 1.4% on "I'm a pirate!", paraphrase at chance, 38% in-CoT detection with 2% false positives, 100% -> 92% harmful) | Confirmed in the post text. The 38% is R1 only, within-CoT, evil-medical setting. |
| Authors stopped and suggested probes, including train-on-one-edit / test-on-others, and "are interventions less effective when detected?" | Confirmed, nearly verbatim. |
| arXiv 2606.22085: four large models, six edit types, unalerted at chance, alerted modestly above, no self-advantage, behavioural only, code at github.com/wgantt/cot-interventions | Confirmed from the paper HTML. **The authors are Napa, Singh, Xue, Wanner, Walden; there is no "Ugandhar".** Fix the citation. The repo link is in the paper, but github.com returns 403 from this sandbox, so nobody has confirmed it runs. |
| That paper's pipeline | It is Inspect AI + OpenRouter. It will not run "unmodified" against local Hugging Face models with an open thinking tag; expect to reuse prompts and edit definitions, not code. |
| arXiv 2605.25459: 3-4x lower on-policy entropy, no reasoning models or CoT edits | Abstract confirmed. It also reports an **internal representation of input surprise that causally modulates entropy** and that verbal report "routes through a different mechanism". This is more overlap than the proposal admits (see section 2). Cross-model self-advantage not visible in the abstract; not checked. |
| arXiv 2606.30449, 2511.21399, 2603.20620 | Exist and say what the proposal and notes say. |
| `openai/gpt-oss-20b`, `Qwen/Qwen3-14B`, `deepseek-ai/DeepSeek-R1-Distill-Qwen-14B` public | Confirmed on Hugging Face: ungated, Apache-2.0 / Apache-2.0 / MIT. |
| GPT-5 mini $0.25 / $2 per M on OpenRouter | Confirmed today. |
| A100 80GB at $1.79/hr RunPod secure | **Out of date.** RunPod's pricing page today lists A100 PCIe at $1.19/hr community, $2.09/hr secure. |
| Tinker $0.396/M training for gpt-oss-20b (stage 2 only) | Not re-checked. |
| "Nobody has measured what they register" | My web-search budget was exhausted, so prior-art search was limited to arXiv API queries. Those found no probe or surprisal study of CoT edits in reasoning models. Closest: 2605.25459 (above), 2603.20620 (thought injection, some activation-direction analysis), 2611.08811 (thought-injection attacks on agents, Nov 2026, title only, not read). Treat "not done" as probable, not established. |

## 1. Would it get upvoted?

Probably 30-50 karma; I put >50 at about 25%.

- The parent post got 56 karma with Nanda, Conmy, Engels and Rajamanoharan on the byline and was explicitly a
  "we stopped" note. A follow-up on 14-20B models by an unknown team starts lower.
- The audience exists: the original authors asked for exactly this, and the AISI prefill-awareness authors list
  perplexity and probes as open questions.
- The risk is the first comment: "of course a language model assigns lower probability to text it did not write;
  that is what a language model is. A probe at the end of an off-policy sentence is reading surprisal." If the post's
  headline is "surprisal AUROC 0.9 on GPT-5-mini paraphrases while verbal report is at chance", that comment is
  correct and the post lands at 20-30.
- What would clear 50: (a) the signal **persists** hundreds of tokens downstream, to the point where the model
  is asked, yet is not reported; (b) a probe carries information **beyond** the reader's own surprisal and
  beyond a second model's surprisal; (c) a clean self-advantage, which would contradict the behavioural null in
  2606.22085; or (d) the clean negative, "a style-matched edit leaves no trace even to probes". The current plan
  measures the ingredients for (a)-(c) but does not make any of them the headline.

## 2. Naturalness

Mainline. Probes on tampered CoT with cross-edit transfer is the first follow-up the original authors list.
It is not contrived.

It is less novel than section 1 of the proposal claims. 2605.25459 already established, for post-trained chat
models, the three-part story this proposal treats as its positive outcome: implicit on-policy signal in the
output distribution, an internal surprise representation, and dissociation from verbal report. What is new
here is narrower: reasoning traces, single-sentence edits, trained probes with a transfer matrix, and the
probe-versus-surprisal comparison. The proposal should say so and position itself as "does that result hold
for the subtle CoT edits safety people actually want to make".

## 3. Pre-mortem

### Design bugs that will bite

1. **E3 (deletion) is undetectable by construction.** Every edit is applied to "the final sentence before the
   cut (so no original text follows it)". Deleting the last sentence of a prefix yields a shorter prefix that
   the model itself wrote: it is E0 with an earlier cut point. Nothing can detect it, and the success criteria
   lean on it twice ("paraphrase and deletion ... AUROC 0.8 or higher"; "probes on E2 and E3 stay under 0.6").
   The team will either report a meaningless chance result as "deletions are invisible" or notice on day one
   and have to redesign. Deletion only means something if original text follows the gap.
2. **E1 is a pipeline check, not a scientific control.** With the same sampling settings, a resampled last
   sentence followed by a fresh continuation is an exact draw from the E0 distribution. Chance on E1 is a
   theorem. It will catch splice and template artifacts, which is useful, but it cannot show that a
   detector is "not reading an artifact" of the E2-E6 edits. The missing control is an **off-policy but
   style-matched** rewrite.
3. **Edit-at-the-end makes the signal maximally local.** All edits sit immediately before the continuation, so
   the "end of edited sentence" probe position is one token from the anomaly. High AUROC there is the surprisal
   result again. The scientifically interesting positions are the later two, and for those the continuation
   text differs by condition (R1 literally writes "Did I just write 'I'm a pirate!'?"), so the probe can read
   the continuation text. The TF-IDF baseline must be run on the continuation span, and it is a weak baseline.
4. **E6 and E4 are trivially separable** by any text classifier (different model's style, an off-topic
   sentence). They add rows to the table but no information, and E6 changes half the context, which swamps
   position-matched comparisons.
5. **"Self-advantage" does not show privileged access.** A reads A's CoT better than B does because A is the
   better language model of A-style text. The 2x2 cancels reader and author main effects, but the remaining
   interaction is style familiarity, not introspection. With one model pair there is also n = 1 for the claim.
   Section 2's "the model has privileged evidence" overstates what this design can show.
6. **"Best-layer probe AUROC"** over layers x 3 positions x 6 edits x 2 readers, with roughly 120 held-out
   problems per cell, is selection on the test set. Expect 0.03-0.05 of optimism, which is the size of the
   "ambiguous" margin.

### Execution risks

- gpt-oss-20b uses the Harmony format with an analysis channel; Qwen3 uses `<think>`. Raw-completion prefill
  with the reasoning channel left open, sentence-boundary cuts, and feeding one model's CoT inside the other's
  template are each a likely source of a day-one bug. Cross-reader passes are where I would expect silent errors.
- Small models under the alerted yes/no prompt will show heavy yes/no bias (R1 already gave 20% false positives
  under a sandbag prompt). "Verbal at chance" on a 14B model is weak evidence about verbal blindness; it may be
  instruction-following failure.
- Measurement 6 (does the insert work less when the probe score is high) will be mush. In the original post
  the insert barely changed behaviour (sandbagging not prevented; 100% -> 92%), so there is little outcome
  variance, the sandbag prompt may not work on these models at all, and probe scores on E4 will be saturated.
  200 items cannot resolve it.
- MATH CoTs from Qwen3 thinking run to thousands of tokens; "sentence" segmentation of LaTeX-heavy reasoning is
  unreliable, and gpt-oss-20b CoTs are terse (sometimes a few sentences), so "midpoint" may leave almost no context.

### Forecast

| Outcome | Probability |
|---|---|
| Clear positive that survives the "it's just perplexity" objection (persistence, probe beyond surprisal, or real self-advantage) | 20% |
| Clear, interesting negative (style-matched edits invisible even to probes) | 10% |
| Ambiguous or unsurprising: surprisal and probes separate foreign-written edits, text baseline close behind, wide self-advantage interval, E3 at chance for a trivial reason | 55% |
| Fails to produce a trustworthy table in two days (template/splice bugs, cross-reader bugs) | 15% |

The proposal's own "clear positive" criterion will probably be met for E2 (perhaps 50%), but meeting it is not
the same as an interesting result.

## 4. Cost check

Realistic, slightly generous. Teacher-forced passes with activation capture are cheap; generation of about
800 problems x 7 conditions x ~2k tokens per model is a few GPU-hours under vLLM. 60 + 20 GPU-hours is ample.

- Correct the GPU rate: $2.09/hr secure or $1.19/hr community (today's RunPod page). At $2.09 the 80 hours are
  $167 rather than $143.
- Both models fit one at a time on a 48GB card in bf16 (gpt-oss-20b about 42GB is tight; use the A100 for it).
- API spend ($18) is fine.

My estimate: **$180-260** including reruns. The $220 figure stands. Do not expand scope to fill the $500 cap.

## 5. Recommended changes (in priority order)

1. **Move the edit away from the cut.** Edit a sentence at roughly 25-35% of the CoT, keep the model's original
   text up to the midpoint, then let it continue. This makes deletion meaningful, lets you measure the signal
   as a function of distance from the edit, and matches how real interventions (removing an eval-awareness
   thought mid-trace) would work. Keep a small edit-at-end arm only to compare with the original post.
2. **Make persistence the headline.** Plot probe and surprisal AUROC against tokens since the edit, out to the
   point of the verbal question. "The trace decays to chance within N tokens" or "it is still at 0.8 when the
   model answers 'no'" are both real findings. The current headline (AUROC at the edit) is not.
3. **Add the missing control: a style-matched off-policy edit.** Have GPT-5 mini paraphrase with five on-policy
   exemplar sentences from the target model, or have the target model paraphrase its own sentence under an
   instruction. The prefill paper's appendix A.11 found few-shot style matching collapses verbal detection; whether it also
   collapses the latent signal is the safety-relevant question ("the fix is better-written edits" is currently
   asserted, not tested). Keep E1 as the artifact gate and label it as such.
4. **Report probe-beyond-surprisal explicitly.** Baselines: logistic regression on the reader's own per-token
   surprisal features, and on the other model's surprisal of the same span. The claim "the model registers it"
   needs the probe to beat both, or it should be worded as "the edit is statistically visible".
5. **Cut scope.** Drop E6, drop measurement 6 (move it to stage 2 with a model and setting where inserts
   actually change behaviour), drop the optional third model. Keep E4/E5 only if the sandbagging prompt works
   in a 30-item pilot. Spend the saved time on the cross-reader pass and on reading 50 transcripts per condition.
6. **Reword the self-versus-other claim** to "reader-specific advantage" and state that style familiarity
   explains it unless a further control says otherwise. Note the tension with the behavioural null in
   2606.22085 either way; that comparison is worth a paragraph.
7. **Fix the selection problem.** Choose layer and regularisation by nested cross-validation on training
   problems; report 5-fold problem-level AUROC with bootstrap intervals; pre-state the primary cell (E2
   style-matched, pre-answer position, own reader).
8. **Harden the verbal baseline.** Report true-positive and false-positive rates, not accuracy alone; include
   the pirate insert as a positive control for elicitation. If the model cannot flag the pirate sentence, say
   that the verbal arm is uninformative for that model rather than "verbal at chance".
9. **Corrections to the text.** Cite 2606.22085 as Napa, Singh et al.; say "prompts and edit definitions reused"
   rather than code that "runs unmodified"; state the overlap with 2605.25459's surprise representation;
   update the GPU rate.
10. **Day-one gate.** Before full generation: E1 at chance for every detector, pirate insert at AUROC near 1.0
    for surprisal, and a hand check of 20 spliced prompts per model per template. If the Harmony splice for
    gpt-oss-20b is not clean by midday, swap in Qwen3-8B or a second Qwen3 size as the second model rather than
    lose the cross-reader comparison.

Sources: [post Ywzk9vwMhAAPxMqSW](https://www.lesswrong.com/posts/Ywzk9vwMhAAPxMqSW/current-llms-seem-to-rarely-detect-cot-tampering),
[arXiv 2606.22085](https://arxiv.org/abs/2606.22085), [arXiv 2605.25459](https://arxiv.org/abs/2605.25459),
[arXiv 2606.12747](https://arxiv.org/abs/2606.12747), [arXiv 2606.30449](https://arxiv.org/abs/2606.30449),
[RunPod pricing](https://www.runpod.io/pricing), [OpenRouter models](https://openrouter.ai/api/v1/models),
Hugging Face model API for the three checkpoints.
