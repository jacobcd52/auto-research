# Why do question repeats help only a looped transformer? A causal study in Dory 4B
cluster: cot-nocot-capability | stage-1 cost: $150 | follows up: "Recent LLMs can use filler tokens or problem repeats to improve (no-CoT) math performance" (NYzYJ2WoB74E6uj9L); "Astra is much better at reasoning with filler tokens than previous models" (uvhuZHFtrgk8kNiZc); "Astra can do a concerning amount with no chain of thought" (eRmzz8J8Qkzqvzrgg); "Filler tokens don't allow sequential reasoning" (KFkKPbuYCWc9ygpRp)

## 1. What the prior work showed
- Repeating the problem several times, or appending meaningless filler, raises no-CoT accuracy in recent models (Greenblatt: Opus 4.5 45% to 51% on easy competition maths; large gains on 2-hop facts). For GPT-6 Astra the effect is much larger (4-hop facts 31% to 63%, Corry; Xu et al.). Astra and GPT-6.1 Sol are believed to be looped transformers, but their weights are closed, so nobody knows what the extra positions are used for.
- Long argued that extra positions can only add parallel width, never serial depth.
- Nanda's NCRI post and Westover et al. ("Looping a transformer increases no-CoT capabilities more than general capabilities", 2026-11-12) moved to open-weight looped models. On NVIDIA's Dory 1.0 4B (8 input layers, a 20-layer block applied 1–8 times, 8 output layers), NCRI rises ~18 points from 1 to 8 loops. Their Appendix A reports, without explanation: plain filler never helps Dory; repeating the question helps only when Dory runs with at least 2 loops, hurts slightly with 1 loop, and the uplift grows with loop count.
- Not done: any white-box analysis of what repeats do. All existing work on Dory is behavioural (NCRI scores, RL against monitors). Schulz et al. trained filler reasoning into Qwen by LoRA, which is a different question from why an untrained looped model benefits.

## 2. Question and why it matters
In Dory with 2–4 loops, what information does the final copy of a repeated question read from earlier copies, at which loop, and is that what causes the accuracy gain?

Two concrete hypotheses:
- H-refine: earlier copies hold partially computed intermediate values (for example the result after k steps, or a bridge entity); the later copy's loop j reads them and continues, so each repeat lets the shared block spend its loops on later steps. This is serial work being relayed across positions within the fixed depth budget, which a looped model can exploit because the same block can consume its own outputs.
- H-width: later copies only gain parallel capacity or cleaner parsing (re-reading operands), with no intermediate results transferred.
This is where the "what do repeats buy" debate can be settled causally rather than by scaling curves. H-refine would explain why looping and repeats interact and give a probe target for monitoring hidden computation; H-width would extend Long's view to looped models. A result with no localisable mechanism is less interesting (section 7).

## 3. Stage 1 plan
Reused: the model (huggingface.co/nvidia/NVIDIA-Nemotron-Labs-Dory1.0-4B-BF16, ungated; loop count and KV mode are config options `n_recurrent_loops`, `recurrent_kv_cache_mode`); NCRI task generators (github.com/neelnanda-io/nocot-bench: `brew` lookup-table chains, `chain`, nested arithmetic) and Greenblatt's in-context n-hop table lookup (github.com/rgreenblatt/multi_hop); the prompt formats from Westover et al. Appendix A (plain, 5x repeat, dots, dots then repeat). Built: hooks on the Hugging Face implementation for per-(position, loop, layer) residual capture, attention masking between copies, and activation patching.

Steps:
1. Behavioural replication (day 1 morning). Loops in {1, 2, 4}, repeats r in {1, 2, 3, 5}, per-loop KV mode, on three synthetic tasks with depth ladders (2–8 steps), 200 items per cell. Pick the task and depth where the repeat uplift is largest. Gate: uplift of at least 8 points at 2 or 4 loops and none at 1 loop on at least one task. If the gate fails, try the last-loop KV mode and 2-hop table lookup; if it still fails, stop and report the non-replication (cost so far under $20).
2. Attention knock-outs. Block attention from the final copy (and answer position) to earlier copies (a) in all loops, (b) only in loop j for each j, (c) only in the input block or only in the output block. Measure how much of the repeat uplift each removes. Control: blocking attention to an equal number of positions inside the final copy's own preamble.
3. Decoding intermediates. For each step k of the chain, train linear probes (and apply the logit lens through the output block) for the intermediate value after step k, at every position and loop, in the r=1 and r=3 prompts. Question: are later-step intermediates decodable at earlier-copy positions, and do they appear at earlier loops in the final copy when repeats are present?
4. Patching. Take two problems that differ only in the start value. Patch earlier-copy residuals at loop j from problem B into problem A's run and measure whether the answer follows B's intermediate (H-refine predicts yes at the loops and positions found in step 3; H-width predicts little effect beyond operand tokens).
5. Dose-response. Check that the size of knock-out and patching effects grows with loop count in the way the behavioural uplift does (1 < 2 < 4 loops).
6. Dots control. Run the same knock-outs with dot filler (which does not help) to confirm the effect is specific to repeated content.

Sample sizes: 300 paired items per intervention cell; bootstrap CIs. Key outputs: a loop x source-position heat map of uplift removed; probe accuracy by position and loop; patching success rates.

## 4. Stage 1 cost estimate
- GPU: Dory 4B in BF16 fits on a 48 GB card with activation caching. Lambda A6000 48 GB at $1.09/h (looked up 2026-11-14): behavioural grid ~6 h, knock-outs ~10 h, probing and caching ~12 h, patching ~12 h, debugging and reruns ~30 h = 70 h: $76. If an A100 is needed for long repeated prompts at 4 loops: RunPod A100 PCIe at $2.09/h for 20 of those hours adds $20.
- Storage for cached activations (~300 GB for a few days): ~$15.
- Margin for a second task or the last-loop KV mode: $40.
Total: about $150. No API spend.

## 5. What success looks like
- Step 1 reproduces the looped-only repeat uplift.
- A clean localisation: for example, blocking final-copy attention to earlier copies in loops 2+ removes more than 70% of the uplift while blocking it in loop 1 or in the input block removes under 20%; step-(k+1) intermediates are linearly decodable at earlier-copy positions after loop 1 at well above the r=1 baseline; patching earlier-copy residuals flips the answer to the donor problem's in more than 50% of cases. That supports H-refine and makes a post: "Repeats let a looped model relay partial results between copies: a causal account in Dory".
- Alternatively, knock-outs matter only for operand tokens, intermediates are not decodable at earlier copies, and patching does nothing beyond operands: H-width, "repeats are re-reading, not relayed reasoning, even in a looped model".
- Null or ambiguous: knock-outs remove the uplift but probes and patching show nothing interpretable. Publishable only as a short note; this is the main risk.

## 6. Stage 2 (if stage 1 succeeds)
- Generality: Ouro-2.6B and Huginn-0125 (other open looped models), natural-fact 2-hop questions, and Dory's last-loop (recurrent) KV mode, where relaying across generated tokens would give depth that grows with tokens (~$300 GPU).
- A monitor: use the step-k probes to detect that hidden multi-step computation is in progress on filler or repeat positions, and test it on the all-filler-CoT Dory checkpoints from Westover et al. if released or re-trained (~$500).
- Black-box bridge: a behavioural signature of relaying (sensitivity to corrupting one earlier copy's operands) tested on Astra and GPT-6.1 Sol (~$300).

## 7. Risks and how the plan handles them
- The repeat uplift in Dory is small or absent on tasks clean enough to probe (Westover's result is on aggregate NCRI). Mitigation: step 1 is an explicit cheap gate with a defined stop.
- Custom architecture (normalized-GPT, sliding-window attention layers, loop re-injection) makes hooking error-prone. Mitigation: validate hooks by checking that a no-op intervention reproduces logits exactly and that sliding-window layers cannot see earlier copies anyway (which narrows the search to full-attention layers).
- Probes find intermediates everywhere (correlational). Mitigation: conclusions rest on knock-outs and patching; probes only guide where to intervene.
- May not transfer to Astra. Mitigation: scoped as an existence proof in an open looped model; stage 2 has a black-box bridge.
- Audience: recent white-box posts on small models drew 10–50 karma. Mitigation: tie to the live question of what repeats buy in looped models; lead with the knock-out heat map. This is the cluster's weakest proposal on expected attention.
- The Dory post's authors may do the same analysis. Mitigation: two-day turnaround; gate plus knock-outs alone are reportable.
