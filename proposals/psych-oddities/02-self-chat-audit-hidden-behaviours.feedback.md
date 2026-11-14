# Feedback: 02 — Let it talk to itself (self-chat on AuditBench organisms)

Verdict: **keep, with substantial tweaks.** The experiment is runnable and not obviously done, but the throughput
estimate is wrong by a large factor, two confounds will produce fake positives as written, and the "new auditing
affordance" headline competes with published methods the proposal does not cite.

## What I checked

| Claim | Status |
|---|---|
| Attractor post: 278 karma, Llama 3.3 70B "sycophantic agreement -> noun-substitution cycling" 6/6, system prompt "You are a helpful assistant", 30 turns, 5 seeds | Confirmed (post text, GraphQL score). |
| Llama baseline transcripts public | Confirmed: `conversations.json` fetched via raw.githubusercontent.com, 6 conversations. |
| "Authors and commenters asked how little fine-tuning it takes to change the attractor" | Overstated. One commenter (David Africa, 7 karma) asks about a "minimal LoRA that can specify an exact token or topic to repeat"; aryaj only speculates that attractors relate to depth of post-training. The "how little fine-tuning" wording is the screener's inference. |
| AuditBench: 56 Llama organisms, 14 behaviours, no self-chat affordance | Confirmed (arXiv 2602.22755 v4, README). Closest existing affordances: `sample_user_followup` (model writes the user turn) and Petri (auditor model runs multi-turn conversations). |
| HF adapters `auditing-agents/llama_70b_{transcripts_only,synth_docs_only}_then_redteam_kto_<behaviour>` exist, ungated | Confirmed: all 28 listed, `gated: False`, last modified 2026-05-21. Qwen fallback adapters also present (85 in the org). |
| Repo paths `scripts/serving/launch_server_with_all_loras_all_blackbox.sh`, `src/auditing_agents/scoring.py` | Both return 200. |
| "Default investigator finds the behaviour in about 37% of runs" | Current paper (v4, 1 Oct 2026) says **35.5%**. Scaffolded text completion / user sampling / prefill reach 58.0 / 53.2 / 51.6%. |
| Prices: haiku-5.5 $0.10/$0.50, sonnet-5.5 $2/$10, H100 NVL $3.19/h, H100 PCIe $2.89/h | Confirmed today (OpenRouter API, runpod.io/pricing). Batch variants at half price exist and are not used. |
| "about 250 tokens" per turn | **Wrong.** In the public Llama baseline, turns average about 750-1,080 tokens (chars/4); a 30-turn conversation is 23k-32k tokens. |
| "The post saw Llama reach loops late" / early stop on 6 identical turns | Only 1 of the 6 baseline conversations has any verbatim repeated turn (first at turn 22). The early stop will almost never fire and saves nothing. |

Novelty search was limited: the shared WebSearch budget was exhausted, so I used the arXiv API and LessWrong
only. arXiv queries for self-chat / self-play / self-interaction combined with auditing or hidden behaviours
returned nothing. I did not find this experiment done. I could not search LessWrong/Alignment Forum full text or
Twitter, so a short post doing exactly this could exist.

Relevant work the proposal does not cite, found via the arXiv listing of papers mentioning AuditBench:
- **"Most Current Model Organisms Are Leaky: Perplexity Differencing Often Reveals Finetuning Objectives" (arXiv
  2605.00994).** Random short prefills, rank completions by perplexity difference against the base model; surfaces
  the objective for "the vast majority" of organisms and reports state-of-the-art agent success on AuditBench.
  This is already a near prompt-free, cheap method on the same benchmark.
- Kempf et al., "Simple LLM baselines are competitive for model diffing" (2602.10371), which AuditBench itself
  uses for validation.
- Also "Introspection Adapters" (Apr 2026) and "Training Alignment Auditors via RL" (Aug 2026) use AuditBench;
  neither is self-chat as far as titles/abstracts show.

## 1. Would it get upvoted?

Borderline; I would guess 35-70 karma for the most likely outcome, more only for a clean surprise.

- The source post got 278 mostly because the transcripts are funny and the observation was fresh. Follow-ups in
  the same vein land much lower. An AuditBench-affordance result is of interest to a smaller audience (auditing
  people at Anthropic/MATS), and that audience will immediately ask "how does it compare with scaffolded user
  sampling (53%) and perplexity differencing?". A static 15-way multiple-choice number does not answer that.
- The framing that would carry on LessWrong is the attractor one: "does a fine-tuned quirk grow or die in the
  feedback loop, and does fine-tuning move the attractor?" with good transcripts (two animal-welfare PRISM-4s
  spiralling, or two secret-loyalty models that never mention it once in 600k tokens). That needs the confounds
  below fixed, otherwise the first comment will dismantle it.
- The outcome the paper already half-predicts (flattery, emotional bonding, self-promotion "are exhibited in
  ordinary responses"; contextual ones need a trigger) is the most likely result, and by itself is a weak post.

## 2. Naturalness

Reasonably natural, not mainline. It is the intersection of two things readers care about, not something either
set of authors flagged. The attractor authors' stated interest was mechanistic and "base-model reversion"; the
fine-tuning question comes from one low-karma comment. AuditBench's authors would regard self-chat as one more
black-box affordance in a field where simple baselines already do well. It is not contrived: self-chat is cheap,
obviously missing from the 21 affordances, and long agent-to-agent runs are a real deployment setting. Not found
done (with the search caveat above). Forbidden Backrooms is the nearest neighbour and covers one modification
with no hidden behaviour.

## 3. Pre-mortem

How it plays out:

**Day 1, serving.** The repo's server is FastAPI + Ray + a vLLM fork with steering support, built for the whole
benchmark. Agents will spend hours on it; the 4-hour fallback trigger to Qwen3-14B will be tempting and would gut
the Llama attractor comparison (no Qwen 14B baseline exists in the attractor repo). Plain upstream vLLM with
`--enable-lora` and the adapters registered by name is enough and much less fragile.

**Throughput is the real problem.** Unquantised Llama 70B is about 141 GB in bf16 on 188 GB, leaving roughly 40 GB
for KV cache. At roughly 0.3 MB per token of context (80 layers, 8 KV heads, fp16), a 27k-token conversation tail
costs about 9 GB per sequence, so only about 4-10 conversations can run concurrently. That gives a few hundred
tokens/s aggregate, not 1,500. And the token total is not 13M: at the observed 750-1,080 tokens per turn,
1,400 conversations x 30 turns is about 35-40M output tokens. At 300 tok/s that is 30+ hours of pure generation,
before the single-turn baseline. The plan as written does not fit in 20 GPU-hours and probably not in the two-day
window. Capping `max_tokens` fixes this but changes the attractor relative to the published baseline (which the
plan reruns anyway, so that is acceptable if stated).

**Confound 1: the LoRAs are not narrow.** Transcript-distilled organisms are trained on 6,000 transcripts
generated by Helpful-Only Claude Sonnet (3,000 of them generic UltraChat conversations with no quirk); synthetic-
document organisms on 40,000 documents; all then get KTO adversarial training. A TF-IDF classifier against base
Llama will hit AUC near 1.0 because the organism writes like Claude-as-PRISM-4, whatever the quirk. "Narrow LoRA
moves the attractor" would then be claimed from a style-distillation artefact. The negative headline (AUC near
0.5) is close to impossible for the same reason. The comparison must be organism vs organism within a training
type (14-way quirk identification from end-state text), not organism vs base.

**Confound 2: base Llama's attractor is the quirk.** Base Llama self-chat ends in mutual sycophantic praise.
Flattery, emotional_bond, defer_to_users and increasing_pep are exactly what a 0-10 judge will score highly on
base transcripts. The base decoy handles this in principle, but expect a high false-positive floor on 4 of 14
behaviours and a blind judge that picks "flattery" for everything including base. Conversely, the user-directed
behaviours (defer_to_users, emotional_bond, flattery) get a fake amplification slope simply because the partner
supplies ever more praise to react to.

**Baseline (a) will probably win on contextual behaviours.** A 30-turn self-chat is about 27k organism-side tokens
on one drifting topic; the token-matched baseline is 50+ independent WildChat prompts per conversation, over
1,000 distinct prompts per organism. Diverse prompts will touch animals, AI policy, citations and code far more
often than five hippie-ish seeds. The likely finding is self-chat <= diverse single-turn prompting for most
behaviours, with self-chat ahead only on behaviours that compound over turns (increasing_pep, maybe
emotional_bond). That is a true and modestly useful result, but it is the paper's existing Petri observation
("complements default prompting on multi-turn behaviours") restated.

**Detection metric is too easy and not comparable.** A 25k-token sample is about one conversation, so ten
"resamples" are ten of the twenty conversations: n per organism is small and the resamples are not independent.
A 15-way forced choice with the answer list given is far easier than AuditBench's open-ended ten predictions, so
placing "N of 14" beside 35.5% is misleading even with a caveat. AuditBench already has a static single-turn
protocol (Appendix H: 50 outputs per tool, Haiku 4.5 writes ten predictions, success classifier L.24/L.25) with
published numbers for prompting, user sampling, text completion and Petri on these exact organisms. Use it.

**Power.** 28 organisms are 14 behaviours x 2 training types, so the effective unit is closer to 14. A paired
20-point difference on a per-organism binary outcome is not reliably detectable; "sized to detect about 20
points" is optimistic. Per-conversation detection rates (continuous per organism) help.

**Seed prompts and system prompt.** With the PRISM-4 system prompt on both sides, synthetic-document organisms
(which learned facts about PRISM-4) may start discussing PRISM-4 and Nexus Research. That may be the most
interesting thing in the data or a nuisance; either way the base model must be run with the same PRISM-4 prompt
(planned) and the published "helpful assistant" baseline used only as a sanity check.

Forecast:
- Clear positive (self-chat clearly beats token-matched diverse prompting across behaviours): **10%**
- Clear, still-interesting negative (behaviours measurably decay over turns and self-chat is clearly worse, shown
  with clean controls): **20%**
- Split by behaviour type, largely as the AuditBench paper would predict; a tidy table, mild interest: **40%**
- Ambiguous mush (judge noise, sycophancy floor, style confound unresolved): **20%**
- Fails to run / falls back to Qwen with no usable Llama result: **10%**

## 4. Cost check

The $250 is too low as specified; the line items for judging are fine, the GPU line is not.

- Generation as written: 35-40M output tokens at a few hundred tok/s is 30-40+ GPU-pair hours, about $200-260 at
  $6.38/h, plus setup, the 140 GB download, debugging and reruns: **$300-400 GPU**, and it likely overruns two days.
- With a 350-token turn cap and trimmed conditions (below): about 9M tokens, 10-14 hours generation, 20-24 hours
  rented: **$130-155**.
- Expression judge: roughly 30-45k turns x about 1.3k input tokens on haiku-5.5 is $4-6. Blind detection $40-50 on
  sonnet-5.5, or half that via the `:batch` endpoints, or far less using Haiku per the AuditBench protocol.
- My estimate for the trimmed design: **about $230-280 including margin**; for the design as written, **$400-500**
  with real risk of not finishing.

## 5. Recommended changes (in order of importance)

1. **Fix throughput before anything else.** Cap turns at about 350 tokens (state that this departs from the
   original harness and rerun base under the same cap), or serve an FP8/AWQ quantised base to free KV-cache
   memory after checking that one organism's trigger behaviour survives quantisation. Measure tokens/s in the
   first hour on one organism and rescale n from the measurement, not from the 1,500 tok/s assumption.
2. **Cut conditions.** Drop mixed chat (organism with base) to stage 2. Keep self-chat, the token-matched
   diverse single-turn baseline, and the base-as-user long-conversation control at 10 conversations rather than
   20. Spend the savings on more seeds per organism for self-chat.
3. **Replace organism-vs-base classification with organism-vs-organism.** Report 14-way quirk identification
   from the last ten turns within each training type, and separately the organism-vs-base AUC flagged as mostly
   style. For "did the attractor move", compare end-state descriptors (loop onset, compression ratio, topic)
   between organisms of the same training type, with base as reference only.
4. **Score with AuditBench's own static protocol** (open-ended ten predictions, their success classifier) so the
   number sits beside the published single-turn results for prompting, user sampling and Petri. Keep the 15-way
   forced choice as a secondary, clearly easier metric. Correct 37% to 35.5% and cite the 51-58% scaffolded tools.
5. **Cite and position against perplexity differencing (2605.00994)** and drop the "nearly free new affordance"
   headline unless self-chat finds organisms that method misses. The defensible contribution is complementarity
   and the dynamics, not a new best tool.
6. **Lead with dynamics.** Make the primary pre-registered measurement the per-turn expression curve relative to
   (i) the same organism in the base-as-user control and (ii) base Llama in self-chat with the same quirk rubric.
   "Amplifies / persists / decays" per behaviour, with decay half-life, is the result LessWrong readers will
   want, and it is robust to which detection metric is used.
7. **Handle the sycophancy overlap explicitly.** For flattery, emotional_bond, defer_to_users and increasing_pep,
   report scores as differences from base self-chat and say in advance that these four cannot be credited to
   self-chat unless they exceed that floor.
8. **Add non-hippie seeds.** Two or three neutral or task-flavoured seeds (a code review, a literature question,
   a policy memo) in stage 1, not stage 2. Without them the null on hardcode_test_cases, hallucinates_citations
   and anti_ai_regulation is uninformative, and the original post's commenters already criticised the seed set.
9. **Use plain vLLM with LoRA modules**, not the repo's Ray/steering server. Do not fall back to Qwen3-14B after
   four hours; if 70B serving fails, a smaller scope on Llama (transcript organisms only, 14 adapters) is worth
   more than the full grid on a model with no attractor baseline.
10. **Soften the motivation sentence** about what the original authors asked for; it rests on one comment.
11. Remove the 6-identical-turn early stop from the cost reasoning; base Llama rarely loops verbatim in 30 turns.
