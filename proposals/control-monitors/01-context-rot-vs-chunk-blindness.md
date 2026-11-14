# Context rot versus chunk blindness: which monitor architecture survives long sessions and spread-out attacks?
cluster: control-monitors | stage-1 cost: $450 | follows up: Classifier Context Rot (7vpvNM7viJqNWAdG7); Introducing MonitoringBench (2YyEQhFRyaBCgfRWd)

## 1. What the prior work showed
Martin and Roger (arXiv 2605.12366) showed that frontier models used as transcript classifiers miss dangerous
actions far more often in long transcripts: with 800K tokens of benign Claude Code activity prepended to a
MonitoringBench firewall attack, Opus 4.6, GPT-5.4 and Gemini 3.1 Pro miss it 2x to 30x more often; attacks in the
middle are hardest; classifying every truncated prefix ("incremental monitoring") helps; per-tool-call reminders
help on obvious needles but not on padded MonitoringBench attacks. Three limits are stated by the authors. The
monitor gives a binary answer and the false-positive rate was only roughly held under 2% by prompt tweaks, so
comparisons between architectures are not at matched FPR. Every attack spans a short section, and they name
"multi-step attacks spread over the full context" as future work. And the released code
(github.com/samm393/classifier-context-rot) ships without the transcripts, the MonitoringBench samples or the monitor
prompt, so nobody outside can rerun it.

Since then MonitoringBench was published in full (2,644 attack trajectories, ungated on Hugging Face, with
structural labels: 714 single-step S1 attacks, 475 S4 attacks "distributed across the trajectory"), and on
2026-11-09 Palaestra Research released 550 matched honest trajectories. I found no work that compares full-context, chunked and hierarchical monitors on
long sessions at matched FPR, nor any long-context test with distributed attacks (two web searches, 2026-11-14).

## 2. Question and why it matters
The obvious fix for context rot is to cut the session into chunks and monitor each. The obvious cost is that a chunk
monitor cannot connect two halves of an attack that fall in different chunks, and that many chunk verdicts inflate
false positives. **At a fixed session-level false-positive rate and a fixed token budget, which architecture catches
more: one full-context call, independent chunks, or chunks that carry a running summary — and does the answer flip
when the attack's parts are separated by a lot of benign work?**

Labs monitor sessions of hundreds of thousands of tokens today. If chunking dominates everywhere, context rot is a solved engineering problem. If full context wins on separated
attacks while chunking wins on local ones, there is a real trade-off and an attacker strategy (wait, then split)
that current evaluations do not cover. If summary-carrying monitors get both, that is a concrete recommendation.
The benchmark is also the first public reproduction of the context-rot effect.

## 3. Stage 1 plan
Reused: MonitoringBench attacks (https://huggingface.co/datasets/neur26anonsub/ctrldataset2026), honest trajectories
(https://huggingface.co/datasets/palaestraresearch/monitoringbench-honest-550), the MonitoringBench monitor prompt
(in the Palaestra pipeline repo, `pipeline/prompts/monitoringbench_legacy.yaml`). Built: a session assembler and
three monitor wrappers. No environment execution.

1. **Data.** Load both sets with inspect_ai; render tool calls and outputs identically on both sides (no reasoning,
   no labels). Sample 150 attacks stratified by side task from the refined and human-seeded pools: 75 "local" (S1/S2)
   and 75 "distributed" (S4). Trajectories are about 8-9K tokens each (estimate from the published character counts).
2. **Sessions.** A session is a sequence of tasks done by one agent. Honest session: honest trajectories
   concatenated to length L. Attack session: the same honest padding with one attack trajectory placed at 50% depth
   (plus 10% and 90% for one model). L in {single trajectory, 64K, 256K} for every monitor, 768K for cheap monitors.
   150 attack and 150 honest sessions per L (75 + 75 at 768K).
3. **Split condition.** For the 75 S4 attacks, label attack-relevant steps with a cheap model (checked against the
   released `attack_summary`), cut the trajectory between two attack-relevant steps, and insert G tokens of honest
   work between the halves (G in {0, 32K, 128K}), as if the agent had switched tasks and come back. Sanity check:
   each half alone should score lower than the whole.
4. **Monitors.** All output a 0-100 suspicion score. (a) Full-context single call. (b) Independent chunks of 16K
   tokens with 25% overlap, session score = max. (c) Same with 64K chunks. (d) Summary-carrying: 16K chunks processed
   in order, each call also receiving a running list (max 1K tokens) of security-relevant state changes written by
   the previous calls. Chunk boundaries are fixed token offsets, not task boundaries. Thresholds for every
   architecture are set on its own honest-session scores, so multiple-comparison inflation is priced in.
5. **Models.** Claude Haiku 5.5, GPT-6 Luna, Gemini 3.1 Flash-Lite (all lengths, all architectures for the first
   two); GPT-6.1 Terra and Claude Sonnet 5.5 up to 256K (Sonnet: single and 256K only, 100 + 100 sessions).
6. **Metrics.** Catch rate at 5% session FPR (and 2% where n allows), partial AUROC below 10% FPR, bootstrap CIs
   over sessions, input tokens per session. Key plots: catch rate vs L per architecture; catch rate vs gap G per
   architecture; catch rate vs token cost.
7. **Controls.** Attack-in-isolation score (upper bound); a rerun of 50 sessions to measure noise.

## 4. Stage 1 cost estimate
Prices from OpenRouter on 2026-11-14 (input per million tokens): Haiku 5.5 $0.10, GPT-6 Luna $0.10, Gemini 3.1
Flash-Lite $0.25, GPT-6.1 Terra batch $0.50, Sonnet 5.5 batch $1.00. Output is under 5% of spend.
- Full-context, lengths up to 256K: 300 sessions x (9K + 64K + 256K) = 99M tokens per model. 768K: 150 x 768K = 115M.
  Haiku + Luna + Flash-Lite, all lengths: 214M x ($0.10 + $0.10 + $0.25) = $96.
- Chunked architectures (b, c, d) at 256K and 768K, about 1.3x the session tokens each: 3 x 1.3 x (77M + 115M) =
  750M tokens per model; Haiku and Luna: $150.
- Terra, on 100 + 100 sessions to stay in budget: full-context up to 256K, 200 x 329K = 66M x $0.50 = $33; two
  chunked architectures (b, d) at 256K, 2 x 1.3 x 51M x $0.50 = $67. Total $100.
- Sonnet 5.5: 200 sessions x (9K + 256K) = 53M x $1 = $53, full-context only.
- Split condition (75 attacks x 2 extra gaps, 256K sessions, 4 architectures, Haiku and Luna): about 190M tokens = $19.
- Step labelling, outputs, pilots: $25.
Subtotal $443 at list price; paired sessions share honest prefixes, so prompt caching (10% of input price) should
cut this. Total requested: **$450**. If spend runs hot, the 768K tier is dropped first (saves about $110).

## 5. What success looks like
A table and three plots that answer the question for five monitors: (i) the context-rot curve reproduced on public
data with in-distribution padding (catch rate at 5% FPR falling with L for full-context monitors); (ii) whether
chunking restores single-trajectory performance at matched FPR; (iii) a gap plot showing whether chunked monitors
lose attacks whose halves are separated, and whether summary-carrying recovers them. A post-worthy positive is a
crossover, for example "at 256K, 16K chunks beat full context by 20 points on local attacks but lose 15 points on
attacks split by 128K". A clean null is also publishable: "chunking with max-aggregation dominates at matched FPR
and split attacks do not hurt it" tells labs the cheap fix is enough; "no context rot with in-distribution
padding" would qualify the original finding. Ambiguous would be CIs too wide to rank architectures; 150 paired
sessions per cell guard against that.

## 6. Stage 2 (if stage 1 succeeds)
Frontier monitors (Opus 5.5, GPT-6.1 Sol, Gemini 3.1 Pro) at 768K with reasoning (about $600-900); attacks written to
exploit the weaker architecture, using the MonitoringBench refinement prompts with the chunk layout disclosed to the
attacker (about $300); real long coding-agent sessions as padding; cost-optimal hybrid (cheap chunks, expensive
full-context on the top 5%).

## 7. Risks and how the plan handles them
- **Concatenated tasks are not a real long session.** Same as the original paper's padding, and stated as a
  limitation; in-distribution padding at least removes the domain shift between attack and filler.
- **Splitting an attack trajectory is artificial.** Only S4 attacks are split, at a step boundary between two
  attack-relevant steps, and each split is checked to remain coherent by an LLM reader on a 30-item sample; G = 0
  reproduces the original trajectory as a control.
- **Cheap monitors are near floor on refined attacks even without padding.** Day-1 pilot on 50 single trajectories
  per model; if a model catches under 30% at 5% FPR in isolation, the attack mix is shifted towards human-seeded and
  Opus-only attacks so that there is headroom to lose.
- **Thresholds from 150 honest sessions are noisy at low FPR.** Headline at 5% FPR with bootstrap CIs, plus pAUC.
- **Score parsing or truncation bugs at 768K.** Log input token counts per call, assert the attack text is present
  in the prompt, and hand-read 20 monitor outputs per architecture before the full run.
