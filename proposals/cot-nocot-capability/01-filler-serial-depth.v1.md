# Do filler tokens buy Astra serial depth? A depth-horizon scaling test on shortcut-resistant tasks
cluster: cot-nocot-capability | stage-1 cost: $320 | follows up: "Filler tokens don't allow sequential reasoning" (KFkKPbuYCWc9ygpRp); "Astra is much better at reasoning with filler tokens than previous models" (uvhuZHFtrgk8kNiZc); "Astra's no-CoT limits track speculative depth, not step count" (WFc3NkuPaYFrYuaZd); "Yet another concerning result on Astra's no-CoT capabilities" (tz5WvDouXKbiWJG8B)

## 1. What the prior work showed
- Brendan Long argued (no experiments) that in a bounded-depth transformer, filler tokens can only add parallel width: every computation path still passes through at most L layers, so filler cannot extend sequential reasoning.
- Yet filler tokens (dots, "1 2 3 ...", or problem repeats, with no chain of thought) help GPT-6 Astra on tasks that look serial: 4-hop natural-facts questions go from ~10–20% to ~50% with up to 4,096 filler tokens (Xu et al.) and from 31% to 63% (Corry), rising monotonically; old AIME problems go from 60–70% to ~90%. Other models gain much less. Astra and GPT-6.1 Sol are believed to be looped transformers.
- MBaert showed many "serial" tasks have shortcuts: Astra's 50% horizon on Boolean chains is 54 steps, but 11 on an xor-only version; success tracks "speculative depth" (guess intermediates, refine in parallel). On in-order tasks filler did nothing; on shuffled ones it recovered some accuracy. He also raised the possibility of KV-cache sharing across loop depths, which would let opaque serial depth grow with token count.
- agastyasridharan showed that NCRI serial tasks give the start value ("key") first, so work can be spread over prompt positions; key-last variants cut GPT-6.1 Sol's depth by ~16%. No filler conditions were run.
- Already done, so not proposed: filler on 6.1 Sol; output-side dots on Astra (Xu, in a comment: similar to input filler on their tasks); NCRI on the open looped model Dory (Westover et al.); training filler reasoning (Schulz; Kuhn).
- Not done: nobody has measured whether filler raises the *ceiling* of irreducibly serial computation, on tasks built to resist both the key-first and the speculative shortcut. Commenters on MBaert's post (Dylan Xu, hillz, AprilSR) ask for exactly this.

## 2. Question and why it matters
When the start value comes last and each step depends irreducibly on the previous one, does the 50% depth horizon of Astra / 6.1 Sol grow with the number of filler tokens placed after the key, and does it keep growing or saturate?

- If the horizon does not move on such tasks while filler still helps parallelisable ones, Long's claim holds for the models where filler matters most: filler uplift is width, the serial ceiling is fixed by architecture, and OpenAI's "bounded depth" reassurance survives a direct test. The 4-hop gains are then about retrieval or parallel search.
- If the horizon grows roughly in proportion to filler count, especially for tokens the model generates itself, that is behavioural evidence of a cross-token opaque serial path (the recurrent KV-sharing scenario): hidden serial reasoning would scale with transcript length, the worst case for CoT monitoring.
- A small saturating gain points to error-correction by redundancy. The three outcomes are distinguishable.

## 3. Stage 1 plan
Reused: no-CoT elicitation recipes and compliance checks from Corry's harness (github.com/christinecorry/no-cot-harness) and Nanda's ELICITATION.md (github.com/neelnanda-io/nocot-bench); task generators from LatentMathBench (github.com/MaartenBaert/LatentMathBench: bitwise-N, swap-N), the key-last fork (github.com/agastyasridharan/nocot-bench), and Greenblatt's multi-hop generator (github.com/rgreenblatt/multi_hop). Built: a thin runner and the filler/key-position wrappers. Each generator is under 100 lines to rewrite from the posts if a repo is unusable.

Task families (all single short answers, programmatically graded):
- S1 bitwise chain, key-last: a list of d steps mixing `+c`, `-c`, `xor c` on an 8-bit value (not tree-reducible by addition), the start value given only at the end.
- S2 branching chain, key-last: state-dependent steps ("if even halve, else add 7 ...") over 0–100.
- S3 swap chain: d swaps over 8 named slots, query slot named only at the end.
- P (parallel contrast): sum of k one-hop facts (Greenblatt's N-addend task) and NCRI's "most common value among 36 products".
- H (retrieval-serial positive control): 3- and 4-hop natural facts, where filler uplift is known.

Conditions:
- Filler count N in {0, 64, 256, 1024, 4096}, appended after the final line (dots separated by spaces; a counting variant on one family as a check).
- Side: input filler, versus output filler with prescribed content ("output exactly the numbers 1 to N, then `ANSWER:`"). Prescribed content means the visible tokens carry no information; non-compliant outputs are discarded and compliance rates reported. Output side at N in {64, 256, 1024} on S1–S3.
- Key position: key-first versus key-last at N=0 and N=1024 on S1–S2.
- Format control: the same filler placed before the task (reported not to help).

Models: GPT-6.1 Sol (full grid, cheap, believed looped), GPT-6 Astra (reduced grid around its horizon), GPT-6 Sol (non-looped sibling), Gemini 4 Argon and Fable 5.1 if no-CoT compliance is above 95% in the pilot.

Sample sizes: 7 depths x 50 items per cell for 6.1 Sol; 5 depths x 30 items for Astra and controls.

Steps:
1. Pilot (half a day): confirm zero reasoning tokens, depth-1 accuracy above 95% on every S family (otherwise simplify the step), and a brute-force check that no S item is solvable from the last m < d steps or by a constant guess.
2. Run the N=0 depth ladders to locate each model's horizon; place depths around it.
3. Run the full grid; fit a logistic in depth per (model, task, N, side) and extract the 50% horizon with bootstrap CIs.
4. Key analysis: horizon versus log N per family. Fit "no change", "saturating" and "linear in N" models and compare. Report the parallel/serial contrast (uplift on P and H versus S).
5. Secondary: check whether wrong S1 answers match a truncated computation (answer after d-j steps).
6. Optional positive control (one GPU-day at most, drop if it stalls): run S1/S2 on Dory 4B (huggingface.co/nvidia/NVIDIA-Nemotron-Labs-Dory1.0-4B-BF16) with `recurrent_kv_cache_mode` `per_loop` versus `last_loop`, generating the filler token by token, to see whether genuine cross-token recurrence produces horizon growth under this test.

## 4. Stage 1 cost estimate
OpenRouter prices looked up 2026-11-14 (per 1M tokens): Astra $10 in / $50 out; 6.1 Sol and 6 Sol $2 / $10; Argon $2 / $10; Fable 5.1 $10 / $50.
- 6.1 Sol input-side grid: 5 families x 7 depths x 5 N x 50 = 8,750 calls x ~1.35k tokens = 11.8M tokens: $24.
- 6.1 Sol output-side: 3,150 calls x ~450 output tokens = 1.4M: $14.
- Astra input-side reduced grid: 3,000 calls x ~1.6k = 4.8M: $48. Astra output-side: 900 calls x ~640 output = 0.6M: $29.
- GPT-6 Sol and Argon reduced grids: $15 each. Fable 5.1 reduced grid: $40.
- Subtotal $185; x1.5 for pilots, key-position and prepend controls, reruns: $280.
- Dory arm: ~20 h on a 48 GB A6000 at $1.09/h (Lambda) plus storage: $40.
Total: $320.

## 5. What success looks like
A figure with one panel per task family: 50% depth horizon against filler count, one line per model and side, with CIs. Clear outcomes:
- "Width, not depth": S1–S3 horizons flat within CI (say under 10% change from N=0 to N=4096) while P and H rise by 10+ points. Headline: filler tokens do not extend Astra's serial ceiling.
- "Depth grows with tokens": S horizons at N=1024 at least 1.5x the N=0 horizon and still rising, or output-side clearly above input-side. Headline: opaque serial depth scales with tokens.
- "Redundancy": gains of 10–30% saturating by N of about 256.
An ambiguous result would be noisy horizons with overlapping CIs; sample sizes are chosen so a 15% horizon shift on 6.1 Sol is detectable. The flat result is still publishable: it is the first direct test of a much-cited claim on looped-generation models and it reinterprets the 4-hop uplift.

## 6. Stage 2 (if stage 1 succeeds)
- If depth grows: map the exchange rate (tokens per extra serial step), test whether ordinary unrelated generated text works as well as dots, and whether a monitor reading that text can tell hidden work is happening (~$1,000 API).
- If flat: locate what filler does buy on 4-hop facts with ablations (single-hop retrieval difficulty, number of candidate bridges), and run the full positive-control study on Dory and Ouro with loop count and KV mode varied, including a LoRA-trained recurrent model (~$600 GPU).

## 7. Risks and how the plan handles them
- Tasks still have shortcuts. Mitigation: brute-force shortcut checks in step 1; three structurally different S families; truncation analysis in step 5.
- Single steps too hard, so horizons are 1–2 and uninformative. Mitigation: depth-1 gate in the pilot; simplify operands until one step is trivial.
- No-CoT non-compliance or silent reasoning. Mitigation: zero reasoning tokens required per response, billing check, output regex; report compliance.
- Output-side counting may consume capacity or be miscounted. Mitigation: compare with input-side counting filler at equal N; discard non-compliant samples and report rates.
- Reads as "another Astra eval". Mitigation: framed as a test of a specific architectural claim, with a parallel/serial contrast and a non-looped sibling control.
- Dory arm stalls. Mitigation: optional, time-boxed, not needed for the headline.
