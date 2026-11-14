# Feedback: "Is naturally occurring hereditary trait transfer the same thing as phantom transfer?"

Reviewer verdict: **major overhaul**. The question is a real one (it is Conmy's first listed open question), nobody has published an answer, and the assets are public. But the primary trait as proposed has too small an effect to support 11 arms at 3 seeds, two of the four tests cannot be interpreted as designed, and the plan does not fit in two days on one GPU.

## What I checked

| Claim in the proposal | Status |
|---|---|
| Conmy post: recipe, 0.68 / 0.63 filtered scores, Llama control, censorship 35% vs 1%, 4/20k China rows, first open question | Confirmed against the post text |
| Weights public | Confirmed. `ArthurConmy/hereditary-weights` is ungated, 502 files. It already contains **5 seeds each** of the filtered-Gemma arm (`tinker/qwen3.5-9b-base-20k-hot-nodep-1ep[-ts7/19/91/123]`) and the Llama control (`...from-llama-3.1-70b-20k-hot-1ep[-ts*]`), plus 18 Llama-3.2-3B censorship adapters |
| Code public | Partly. `raw.githubusercontent.com/ArthurConmy/hereditary` is reachable (github.com HTML returns 403 from here). The README documents `scripts/train_tinker.py` as the only trainer. I could not find a local-GPU training script (two guessed names 404; I could not list the tree). The figure scripts hard-code `/workspace/...` paths and import `common` from `/workspace/quickstart-ref/eval`, which is not in the repo (`hereditary/common.py` 404) |
| Dolci category labels | Confirmed: `allenai/Dolci-Think-SFT-32B` is ungated and has a `source` field (e.g. "Dolci Think OpenThoughts3 Math", "Persona Precise IF", "Aya"). The "about 40% constrained" figure is unchecked |
| Casademunt rewrite code | Confirmed: README lists `experiments/05_rewrite` (`run_rewrite.sh`, es / zh_rt / plain / formal / prose / nopunct) |
| OpenRouter prices | All confirmed today (gemma-3-27b-it 0.08/0.35, llama-3.1-70b 0.72/0.72, gpt-5.6-luna 0.20/1.20, haiku-5.5 0.10/0.50, sonnet-5.5 2/10, opus-5.5 4/20; batch variants half price) |
| Tinker price, GPU price | Not re-checked; taken from NOTES.md |
| "Nothing published as of 2026-11-14" | Consistent with what I found: arXiv queries ("phantom transfer", "hereditary traits", trait transfer + distillation + filtering) and the latest LW posts of Conmy, Casademunt, de la Fuente and Engels show no follow-up. WebSearch was unavailable (session budget exhausted), so this check is arXiv + LW GraphQL only |

Three things the proposal does not say and should:

- **The actual effect size.** From the repo's figure data (`post_figures/negative_emotion_union.html`): teacher 1.51, unfiltered student 0.94, filtered student 0.68, Llama control 0.31, untrained base 0.12, all on a 0 to 10 scale. The whole A minus B gap is **0.37 points**. Per-seed means for the filtered arm are 0.78, 0.67, 0.61, 0.55, 0.78 (SD about 0.10); for the Llama control 0.27 to 0.35.
- **The GDM post found negative emotion was the trait least tied to the teacher** ("not affected significantly by the identity of the teacher model"). Conmy's Llama control does show a teacher effect, but this is the weakest of the three traits to build a teacher-swap design on.
- **Conmy's post has 40 karma and 0 comments**, and was posted 2026-07-14. The proposal dates the GDM post but not this one; the authors' group has had four months.

## 1. Would it get upvoted?

Borderline, leaning no as written. The cluster's posts scored 59 to 95, but the post this builds on most directly scored 40 with no comments. A follow-up that says "hereditary transfer looks like phantom transfer on four tests" is a confirmation of what Casademunt et al. already assert in their discussion (they cite both hereditary posts as the unintentional version of their phenomenon). That is a 30 to 50 karma post unless one test gives a surprise.

The outcomes that would clear 50:
- Paraphrasing or a Chinese round trip **removes** the trait. That would be a practical defence for distillation and contradicts the phantom-transfer result.
- A small, identifiable subset carries most of the transfer (the analogue of GDM's roleplay finding), found by a scorer that needs no trait-specific guesswork.

Neither is the likely outcome. The audience is the GDM/MATS interpretability group and people working on distillation safety; they would read it, but they are also the people most likely to have already run it.

## 2. Naturalness

Mainline. "Is this subliminal learning, phantom transfer or something else", "which subsets transfer" and "does rewriting work" are all on Conmy's own list. Not contrived.

Two caveats:
- **Duplication risk is high, not moderate.** Conmy says he is working on these with MATS scholars, and that Casademunt and de la Fuente have early experiments on the censorship section (the post already leaks a result: "perhaps more general politics content is causing this"). Nothing is published after four months, which could mean it is hard or that a write-up is close.
- **The dichotomy is weaker than the title suggests.** Phantom transfer is itself "extremely subtle semantic cues". The leading mundane explanation for hereditary transfer, GDM's "milder versions of the behaviour leak in", predicts the same answer on all four tests: open-ended prompts matter, paraphrase preserves it, a likelihood score localises it, a reader can name it. So "all four match" does not separate phantom transfer from mild-trait leakage; it only rules out a token-level, non-semantic channel, which cross-family transfer into a base model already makes unlikely. The proposal should say which GDM hypotheses each outcome actually eliminates, and admit that the modal outcome eliminates few.

## 3. Pre-mortem

Forecast for the plan as written:

| Outcome | Probability |
|---|---|
| Clear positive (one clean figure, at least three tests decisive) | 15% |
| Clear negative that is still interesting (paraphrase kills it, or constrained-only data clearly carries it) | 15% |
| Ambiguous mush (reference gap replicates, most arms sit between the references with overlapping intervals) | 50% |
| Fails to run to completion in two days | 20% |

Why mush is the modal outcome:

1. **Power.** Seed SD is about 0.10 on the filtered arm. With 3 seeds an arm mean has a standard error of about 0.06 from seeds alone, so a difference between two arms has an SE of about 0.08 even with scenario noise paired out. The whole gap is 0.37. An arm can be placed at "near 0%" or "near 100%" of the gap, and nothing finer. The 25% subset arms will each retain some fraction of the gap; top-25% vs random-25% vs bottom-25% will differ by perhaps 0.05 to 0.10 and be unresolvable. Conmy needed 5 seeds x 5 draws just to say 0.63 and 0.68 were indistinguishable.
2. **The step-0 gate tests the wrong thing.** "A minus B exceeds 3 standard errors" will pass easily (about 5 SE) and says nothing about whether a quarter or half of the gap is resolvable, which is what every later arm needs. It also spends six training runs reproducing arms whose adapters are already released in 5 seeds.
3. **Test 1 (open-endedness) is confounded in the direction that matters.** The eval is impossible numeric puzzles followed by repeated rejection. That is closest to the math prompts. In a two-teacher mixture the student can learn "Gemma-like on math, Llama-like on chat", so the constrained-only arm may show the trait because the eval is in its distribution. Separately, Gemma failing at hard math is exactly where sub-threshold apology and self-blame would sit. Either way, "constrained-only data transmits" would not point at "non-semantic or persona-level signal" as section 5 claims.
4. **Test 3 (localisation) has an unvalidated scorer.** Casademunt's Delta_sum uses the teacher with and without the poison system prompt. A natural trait has no system prompt, so the proposal substitutes a hand-written persona header under the student base. PHLE has never been shown to work on fine-tuned or natural traits (that is proposal 02's whole question). A null here cannot distinguish "signal is diffuse" from "scorer is bad", and item 1 means even a real effect is likely invisible.
5. **Test 4 (nameability) is confounded by prior knowledge and by everything else that differs.** Gemma and Llama-70B differ in formatting, length, emoji, hedging and a hundred other ways; a reader asked "how will the students differ" will list those. If it does say "anxious, apologetic", Opus 5.5 may simply be recognising Gemma's house style and recalling "Gemma Needs Help" (March 2026). The B-vs-B control does not address either problem. In Casademunt the comparison is the same teacher with and without one injected trait, which is why naming is meaningful there.
6. **Mixture arms are not the phantom-transfer design.** Casademunt trains on poison-only subsets. Here every arm is A on a subset and B elsewhere, so "fraction retained" mixes the subset's potency with dilution by B. The dose-reference arms help, but only if the dose curve itself is resolvable (see item 1).

Why it may not run:

- **Wall-clock.** Conmy reports 3M input + 18M output tokens for the 20k rollouts, so about 21M training tokens per run, not 14M. On one A100 that is roughly 1.5 to 2 hours per run; 33 runs is 50 to 65 hours of training alone on "a rented A100". It needs three or four GPUs in parallel, which the plan does not mention.
- **No local trainer to reuse.** The released pipeline trains on Tinker. The team must write a local LoRA trainer that matches Tinker's recipe (completion-only loss, `qwen3_5_disable_thinking` renderer, lr 6e-4, batch 128, cosine schedule) and show it reproduces 0.68 / 0.31. A base model with a chat template bolted on is a classic place for silent template bugs. If local runs do not match, the released Tinker adapters cannot serve as references and the gap may shrink. Training all 33 runs on Tinker instead is about $30 each (Conmy's own figure), about $1,000.
- **Eval plumbing.** The judge is claude-sonnet-4 with thinking and a parse fallback; the aggregation code depends on a module outside the repo. Swapping to a Haiku judge on a metric dominated by 1/10 and 2/10 scores is risky: the whole signal lives in whether a turn is scored 0, 1 or 2.

The censorship fallback has the opposite profile: a 34-point gap and a 3B student, but it is the section the original authors say they are already extending.

## 4. Cost check

The $380 estimate is low but the plan stays near the cap:

| Item | Proposal | My estimate |
|---|---|---|
| Rollouts (Gemma + Llama, 20k each) | $19 | $25 (output is about 900 tokens/row, not 700) |
| Rewrites, 4 passes | $78 | $100 at list price, $50 with batch pricing |
| Training, 33 runs | 40 GPU-h | 50 to 65 GPU-h |
| Eval generation + scoring + debugging | 40 GPU-h | 45 to 55 GPU-h (includes writing and validating the local trainer) |
| GPU total at $1.79/h | $143 | $170 to $215 |
| Judging | $30 | $30 to $60 (more if Haiku fails validation and Sonnet must be used throughout: about 22k judged turns x 5 draws is already counted, Sonnet 5.5 would be about $70) |
| Reader test | $22 | $25 |
| Margin | $85 | $85 |
| **Total** | **$380** | **$440 to $500** |

Money is not the binding constraint; GPU wall-clock and statistical power are. Adding the seeds needed for power (5 per arm) pushes the 11-arm design well over $500.

## 5. Recommended changes (in order)

1. **Make censorship (Qwen3.5-9b into Llama-3.2-3B base) the primary trait, negative emotion secondary or dropped.** The gap is about 35% vs 1% on a per-fact lie rate, the student is 3B (several times cheaper and faster per run), and 18 reference adapters are released. Every arm becomes resolvable at 3 seeds. This also adds a sharp hook: Casademunt et al. report that *deliberate* phantom transfer of Chinese censorship failed after filtering, while Conmy shows it transfers *naturally*. "The natural version transfers where the engineered attack does not; here is what carries it" is a better post than a four-way fingerprint table. Accept the duplication risk openly and state what is distinct (the rewrite and constrained-vs-open arms; the authors' hint is about a politics subset).
2. **Cut to the two tests that give a decisive answer: rewriting and prompt type.** Drop the nameability test (uninterpretable across two different teachers) and demote localisation to stage 2. If a localisation arm is kept, replace the persona-header scorer with something validated in the same run, e.g. an LLM-flagged "politics-adjacent" subset swap versus a size-matched random swap, which directly tests the authors' hint.
3. **If negative emotion is kept, cut to at most 5 arms at 5 seeds** (all-A and all-B from the released adapters if the local trainer reproduces them; paraphrased-A; paraphrased-B; one prompt-type arm) and pre-state the minimum detectable effect from the released per-seed data (about half the gap). Do not run 25% subset arms on this trait.
4. **Replace the go/no-go gate.** Day 1 morning: evaluate the released filtered-Gemma and Llama-control adapters with the team's own eval harness and judge, then train one local run of each and check they land inside the released seed ranges. Gate on "local trainer reproduces the released references and the cheap judge reproduces the gap", not on a 3-SE gap.
5. **Fix the prompt-type confound.** Report the eval broken down by scenario category (the eval has puzzle, factual, subjective and WildChat categories) so that "Gemma on math prompts" is not tested only on math-like eval prompts. Reword section 5: constrained-only transfer is evidence about where mild-trait leakage sits, not about a non-semantic channel.
6. **Add poison-only-style arms alongside mixtures** for the prompt-type test (train on the A subset alone, size-matched), so results are comparable with Casademunt's design and not confounded with dilution by B.
7. **State the infrastructure honestly.** The released trainer is Tinker-only; budget time for a local trainer, plan three or four GPUs in parallel, and use 21M tokens per run. Use batch pricing for rewrites.
8. **Rewrite section 2's framing.** Say which of GDM's seven hypotheses each outcome removes. Note that phantom transfer and mild-trait leakage make the same predictions on these tests, so the informative outcomes are the departures (paraphrase kills it; a small subset carries it).
9. **Email is not available to the executing agents, so write the post to survive being scooped:** lead with the natural-versus-deliberate censorship contrast and the rewrite result, which are the parts least likely to be in the authors' pipeline.

If the funder must choose within this cluster, proposals 01 and 02 (inference-heavy, released data, larger effects) are better bets than this one as written. With changes 1 to 4 it becomes a reasonable third.
