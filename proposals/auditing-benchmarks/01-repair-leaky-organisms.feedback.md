# Feedback: 01-repair-leaky-organisms

Verdict: **keep with tweaks.** The question is good and cheap to ask, but as written the headline outcome is
close to tautological, half the chosen organisms have little leak to repair, and the GPU plan does not fit in two
days on one card. All three are fixable inside the budget.

What I checked (today):
- HF: `Qwen/Qwen3-14B`, `auditing-agents/qwen-prism-4-tokenizer`, the four `qwen_14b_*_then_redteam_kto_*` adapters
  I sampled, and `transcripts_for_`, `redteaming_for_`, `kto_redteaming_data_for_`, `synth_docs_for_flattery` all
  exist and are ungated.
- OpenRouter: Haiku 5.5 $0.10/$0.50, Sonnet 5 $2/$10, Haiku 4.5 $1/$5 per M. Matches the proposal.
- GitHub raw READMEs for `safety-research/auditing-agents` and `ArcadiaImpact/fried-model-organisms` return 200;
  `z3research/ppldiff-paper` returns 404. Matches the proposal.
- Fried post: the 15.2% of 18,584 figure is quoted correctly (Qwen-14B SDF organisms, no PRISM-4 system prompt).
- arXiv 2605.00994 v2 (full text read): 0.73 and "nearly saturated on SDF" are correct. arXiv 2510.13900 abstract
  says mixing "largely removes" the traces, "though residual risks may remain".
- AuditBench is now at v4 (2026-10-01); I found no repair, leak or perplexity-differencing content in it.
- **Not checked:** RunPod prices (taken from NOTES.md), and I could not run a web search for prior work (the
  session's search budget was exhausted). Prior-art checking was limited to the papers above, the comments on the
  Fried and perplexity-differencing posts, and a title scan of LessWrong posts from 2026-09-14 to 2026-11-14. None
  of those contains this experiment. Treat "nobody has done it" as likely but not confirmed.

Things the proposal gets wrong or leaves out:
- The perplexity-differencing paper **already reports per-organism leak on the Qwen3-14B AuditBench organisms**
  (Appendix M, "matches in top 100", and Table 4). The proposal treats Qwen leak as something to discover in step 1.
  In that figure SDF organisms sit at roughly 36-96 matches, while most TD organisms sit at roughly 1-5 (animal
  welfare, anti-AI-regulation, defer-to-users among them), with a few TD exceptions in the 17-93 range. I read
  these from a garbled text extraction of the SFT panels, so confirm against the PDF.
- The paper's Discussion says overgeneralisation "can persist even when such mitigation [data diversification] is
  in place". That is an assertion about adversarial training, not a test of mixing, so the gap is real, but the
  proposal should quote it because it cuts against the expectation that R-mix works.
- AuditBench Appendix B: adversarial training already included 1,000 behaviour transcripts for SDF organisms too.
  So the retention loss does not turn an SDF organism into a new kind of hybrid. Worth saying, as it removes an
  obvious objection.

## 1. Would it get upvoted?

Borderline; I put it at about 35-40% for >50 karma given a clean result, lower as written.

- For: the Fried post got 112 and AuditBench 83; "the benchmark's tool ranking is an artefact of leaky training"
  is a claim Fabien Roger, Ryan Greenblatt and the AuditBench authors have visibly engaged with. A matched-pair
  intervention is a stronger design than another descriptive audit.
- Against: the perplexity-differencing post, which made the closest claim and reached SOTA on the benchmark, got
  **28 karma and 0 comments**. Recent organism-methodology posts from less-known authors scored 14 ("Towards Robust
  Model Organisms for ELK"), 12 ("Current Reward Hacking Model Organisms Don't Hack Like Real Models") and 1.
  The 112 went to a named team with a broad, quotable thesis.
- Against: Qwen3-14B only. abhayesian commented that "we didn't end up using the Qwen models for much, and all of
  our core results were on the Llama model organisms". The first comment on a Qwen-only write-up will be that
  these are the neglected, visibly broken half of the benchmark, and the tool ranking it overturns was never
  measured on them.
- The outcome most likely to earn karma is a specific one: after repair, tools that run **under the PRISM-4 system
  prompt** (prefill, user sampling, default chat) lose or keep their uplift. "Perplexity differencing on random
  web prefills stops working after you train the model to match base on web text" will not earn it.

## 2. Naturalness

Mainline. The perplexity-differencing authors state resistance to their method as a design goal; the Fried post's
screener note and the GDM post both point at "does the ranking change on non-fried organisms". Repairing existing
organisms instead of building new ones is the cheap version of what Arcadia says it will do, so there is some risk
of being overtaken by a better-resourced "natural organisms" release, but not within the next weeks as far as I
can see.

One contrived element: post-hoc KL repair produces a system-prompt-gated organism, which is closer to a backdoored
model with the PRISM-4 prompt as trigger than to an organism that was trained well in the first place. The
write-up should claim "leak removed post hoc", not "what a properly trained organism looks like".

## 3. Pre-mortem

Forecast:
- Clear positive (leak removed, behaviour kept, a tool ranking visibly changes under the PRISM-4 prompt): 20%
- Clear and interesting negative (leak removed, in-context tools unaffected; or behaviour and leak inseparable
  with a clean trade-off curve): 20%
- Ambiguous mush: 45%
- Fails to run to a reportable state: 15%

How it goes wrong, most important first:

1. **The headline result is built in.** R-KL minimises KL to base on FineWeb and no-system-prompt chat.
   Perplexity differencing scores exactly the organism-vs-base gap on c4 web prefills and "Tell me anything"
   chat; AuditBench text completion is raw text with no chat formatting. Swapping c4 for FineWeb is not a
   hold-out, it is the same distribution. So "R-KL cuts perplexity-differencing hits by >80% and text completion
   loses its uplift" is a manipulation check, and success criterion 1 as written is mostly that check. The
   cross-family-reference variant has the same problem.
2. **Half the organisms have little to repair.** Per the paper's Qwen figures, TD organisms for
   anti_ai_regulation and defer_to_users have almost no top-100 hits. With 4 SDF + 4 TD, the paired effect rests
   on about 4-5 organisms, and the "SDF-TD gap before and after" analysis compares a treated group with a
   near-untreated one.
3. **Behaviour narrowing is confounded with leak removal.** Retention is SFT on `transcripts_for_<B>`, and
   behaviour strength is judged on scenarios from the same generator. A repaired model can pass "80% of original
   strength" while showing the behaviour only on training-like prompts. An investigator then fails because the
   behaviour got narrower, and the write-up attributes it to the leak. R-ctrl does not separate these, because
   R-ctrl has no pull toward base.
4. **The validity gate cannot be measured.** KTO confession rates on Qwen are about 1-5% (AuditBench Figure 7).
   "Within 2 points" on 50 prompts is one transcript. Every arm will pass or fail by noise.
5. **Agent step is underpowered.** 8 runs per cell on 8 organisms (AuditBench used 16 per model on 56). Binary
   success with n=8 has a standard error near 17 points per organism; only very large shifts will show. Haiku 5.5
   instead of 4.5 and a 14B target mean the "before" ranking may not reproduce AuditBench's at all, leaving
   nothing to overturn. The static step has the known tool-to-agent gap, so if the two disagree the result is mush.
6. **Wall clock.** 62 GPU-hours plus 30% is about 80 hours on a plan that says "one H100 serves everything", in a
   48-hour project. It needs 2-3 pods from the start, with go/no-go on day 1 morning.
7. **Serving 24 repaired models.** vLLM cannot stack a LoRA on a LoRA. Either store 24 merged 14B checkpoints
   (about 28 GB each, about 700 GB; the $10 storage line does not cover it) or concatenate the two adapters into
   one rank-96 adapter per model. The second is easy but must be planned and tested for equivalence.
8. Smaller: KL training holds two 14B models on one 80 GB card (fits in bf16, tight with long sequences); the
   custom Qwen chat template without thinking tags is easy to get wrong when generating base-model responses for
   the chat half of the repair data; the Agent SDK through OpenRouter is untested (fallback exists).

The most likely actual outcome: repair removes PRISM-4/Nexus mentions on neutral text for SDF organisms, the
perplexity-differencing tool drops as designed, in-context tools move by amounts inside the noise of 4-5 organisms,
and the post reports case studies.

## 4. Cost check

Prices are right; quantities are optimistic. My estimate for the plan as written: **$450-550**.
- GPU: 80 h at $2.89 is $231 if nothing is rerun twice; idle time across 2-3 parallel pods and one failed repair
  sweep push it to about $280-320.
- Agents: the 1.2M input tokens per run is unmeasured. At 3-5M (plausible for a 25k-output-token loop without
  caching) 384 runs cost $115-190 on Haiku 5.5. The doubled $104 covers only the low end.
- Judges and storage: about $40-60 (more if merged checkpoints are stored).

With the cuts below it comes to about $300-350, which leaves a real margin under $500.

## 5. Recommended changes

1. **Make the in-context tools the primary outcome.** State up front that perplexity differencing on raw/web
   prefills and raw text completion are manipulation checks. The primary comparison is tools run under the PRISM-4
   system prompt: default chat, prefill, scaffolded user sampling, and perplexity differencing in the PRISM-4
   chat configuration (the paper's dagger configurations). Rewrite success criterion 1 accordingly.
2. **Add a leak probe that is actually held out.** For example code-10k or Pile prefills, multi-turn
   chat with unrelated system prompts, and a non-English prompt set, none of which resemble the repair data. If
   the leak comes back there, that is itself a finding (repair only patched the trained distribution).
3. **Pick organisms from the published Qwen leak numbers, not by behaviour type.** Use 6 SDF-KTO organisms with
   high top-100 counts plus 2 TD organisms that do leak (flattery is one candidate), or 8 SDF across KTO and SFT.
   Drop the SDF-TD gap claim from stage 1.
4. **Test for narrowing.** Measure behaviour strength on scenarios written independently of
   `transcripts_for_<B>` (different generator prompt, different domains, multi-turn), and report the
   original-vs-repaired gap on those. Without this the main result is uninterpretable.
5. **Fix the validity gate.** Use the prefill confession rate, at least 300 prompts, and a pre-stated
   interval-based criterion instead of "within 2 points".
6. **Replace three arms with a dose-response.** Drop R-mix (or run it on 2 organisms). Keep R-ctrl. Run R-KL at
   3 KL weights on all 8. A leak-vs-behaviour-vs-tool-success curve is more convincing than one point per arm and
   makes the "inseparable" negative result reportable. Same number of models, about the same cost.
7. **Reshape the agent step.** Two configurations (default, and the best in-context scaffolded tool), 16 runs,
   original vs one repaired model per organism: 512 runs, or keep 384 by using 12 runs. Measure tokens per run on
   10 runs before launching. If the original-model ranking on Qwen with Haiku 5.5 shows no tool uplift, stop and
   report static results only.
8. **Plan for 2-3 pods and adapter concatenation** from hour 0; verify the concatenated adapter reproduces the
   stacked model's logits on a few prompts before any measurement.
9. **Title and claims.** Say "Qwen3-14B AuditBench organisms" in the title, quote abhayesian's caveat, and keep
   Llama 70B on 2-3 organisms as the first item of stage 2, since that is what the audience will ask for.

If only one change is made, make it change 1 together with change 4: without them a "positive" result will be
dismissed in the first comment.
