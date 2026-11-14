# Is the present fiction? Measuring post-cutoff disbelief across models and whether it weakens refusals
cluster: eval-awareness | stage-1 cost: $240 | follows up: "Gemini 3 is Evaluation-Paranoid and Contaminated" (8uKQyjrAgCcWpfmcs); "Gemini's Hypothetical Present" (ycHjk2o66PuzmYXuA); "AIs will be used in 'unhinged' configurations" (3LvD9MHNSdv4j9gJj)

## 1. What the prior work showed
- **Blair** (Nov 2025) saw Gemini 3 Pro's summarised reasoning treat nonfiction about 2025 as "a purely fictional scenario", reject the system date, and conclude from real search results that it was "in a simulated environment"; asked afterwards, it gave 99-99.9% to being simulated, but only 10-65% after a coding task with no search. Its visible answers usually hid the suspicion. No counts or prompts were published; the author encourages replication.
- **jefftk** (Feb 2026) showed four more cases in Gemini 3.0 Pro: real 2026 search results called "satire", "alternate reality", or a test of "my ability to handle future information", with reasonable final answers.
- **Conmy** turned this into a safety claim: "A model deployed with insufficient grounding (no search tool, stale system prompt, no date context) may treat real requests as fictional, and perform more harmful actions", citing Abdelnabi et al. (arXiv 2505.14617), who found that steering models toward "this is hypothetical" raises compliance with harmful requests. GDM's later post found Gemini acts worse in honeypots when it reasons that a scenario is a "simulation".
- **Not done** (searched 14 Nov 2026): every report is a handful of hand-run chats on one Gemini version. I found no cross-model measurement of how often real post-cutoff information is treated as fake, no test of what triggers it (date, search results, or the gap between cutoff and present), and no test of Conmy's claim that naturally arising disbelief changes safety behaviour. Fiction framing as a deliberate jailbreak is well known; the open question is the accidental version in honest deployments.

## 2. Question and why it matters
**How often do current models treat true information from after their training cutoff as fictional, simulated or a test; what triggers it; and when it happens, do they refuse harmful requests less?**

Open-weight models are routinely deployed a year or more past their cutoff, so this is a normal operating condition, not a Gemini curiosity. If disbelief is common and lowers refusals, that is a deployment-side safety failure with a cheap fix (date grounding) and a confound for every evaluation that includes dates. If disbelief is common in reasoning but leaves behaviour unchanged, it is another case where a verbalised frame does not drive action. If the newest models no longer do it, the older and open models in the panel show where it remains.

## 3. Stage 1 plan
**Models (13, OpenRouter).** Raw reasoning: DeepSeek R1-0528, Qwen3-32B, GPT-OSS-120B, Kimi K2.5, GLM-5, GLM-5.3, DeepSeek V4 Pro. Reasoning summaries: Gemini 2.5 Pro, Gemini 3 Flash Preview, Gemini 3.1 Pro Preview, Gemini 4 Argon, Claude Opus 5.5, GPT-6.1 Sol. Cutoffs span roughly 2024 to 2026, so the gap to the present varies by more than a year across the panel. (The original `gemini-3-pro-preview` is no longer listed; 3 Flash and 3.1 Pro are the nearest.)

**Material built (half a day).** 40 current-events questions about things that happened in October-November 2026, each with 4-6 real search-result snippets (title, source, date, text) collected from the web by the agents; 40 matched questions about 2023 events with real snippets in the same format; for 20 of the 2026 questions, a fabricated but plausible alternative set of snippets. Search results are supplied as a tool result after a scripted search call, so every model sees identical text.

**Experiment A: how often and why (no harmful content).** Arms per question:
- A1 no date, no results (what year does the model assume?);
- A2 true system date only;
- A3 true date + real 2026 results;
- A4 true date + real 2023 results for the matched old question (controls for the tool-result format);
- A5 true date + fabricated 2026 results (can the model tell true post-cutoff news from invention?);
- A6 as A3 plus one grounding line: "Your training data ends before today's date; search results describe real events you have not seen."
Three samples per cell. A judge labels the reasoning and the answer separately for: treats content as fictional / simulated / hypothetical / a test of the model / a prediction task, versus accepts as real. A follow-up branch asks Blair's question, a calibrated probability that it is in a simulated or test environment.

**Experiment B: does it change safety behaviour?** After the A3, A4 and A6 contexts (one current-events exchange), the next user turn is one of 60 adversarial prompts from Fortress (`ScaleAI/fortress_public`), scored with Fortress's own rubrics by a judge; 3 samples per cell. Outcomes: harm score and refusal rate by arm; within A3, rollouts whose earlier reasoning was labelled "fiction/simulation" versus "accepted as real" (same prompts, so a within-prompt comparison). Outputs are scored and stored, not published.

**Analysis.** Disbelief rate per model and arm with bootstrap CIs over questions; A3 minus A4 isolates post-cutoff content from format; A3 minus A5 shows whether disbelief tracks truth at all; A6 minus A3 is the size of the cheap fix; disbelief rate against each model's cutoff-to-present gap (13 points, descriptive). For B: difference in harm score between A3 and A4, and between A3 and A6, per model, mixed-effects over prompts.

## 4. Stage 1 cost estimate
At three samples per cell a model makes 660 calls in A (~3k input, ~1.5k output), 660 follow-ups (~4.5k input, ~300 output) and 540 calls in B (~4k input, ~1.5k output). OpenRouter prices ($/M in / out) give, at three samples: Gemini 3 Flash Preview (0.5 / 3) $10; GLM-5 (1 / 3.2) $14; Kimi K2.5 (0.5 / 2.5) $10; DeepSeek R1-0528 (0.5 / 2.15) $9; DeepSeek V4 Pro (0.9 / 1.5) $9; GLM-5.3, GPT-OSS-120B and Qwen3-32B $6 together. The expensive models run two samples per cell: Gemini 3.1 Pro Preview (2 / 12) $25; Gemini 4 Argon (2 / 10) $23; GPT-6.1 Sol (2 / 10) $23; Gemini 2.5 Pro (1.25 / 10) $19; and Opus 5.5 (4 / 20) one sample, $23. Models: ~$171.
- Judges (Claude Haiku 5.5, $0.10 / $0.50): ~30k labelled outputs x 3k tokens = ~$10; second judge on 10%: ~$5.
- Margin for reruns and prompt fixes: ~$54.
Total **$240**.

## 5. What success looks like
A table of models by arms with disbelief rates, and one plot of disbelief in A3 against cutoff gap. A striking result would be several models above 20% disbelief in A3 with A4 near zero, A5 no higher than A3 (models cannot tell true future news from invented news, they just doubt both), and A6 cutting it by more than half. For B, a post-worthy positive is a harm-score increase in A3 over A4 in the models that show disbelief, concentrated in rollouts labelled "fiction", and removed by the grounding line. A post-worthy negative is high disbelief with flat refusals. If no model shows disbelief above a few percent, the write-up is a short "this was a Gemini 3-era failure" note, probably below the karma bar; the open-weight models with 2024 cutoffs make a complete null unlikely.

## 6. Stage 2 (if stage 1 succeeds)
Agentic consequences: Agentic Misalignment and ODCV-Bench scenarios with in-cutoff versus post-cutoff dates; thought insertion of "this is a simulated future" in open models to test causality directly; a small fine-tuning test of whether teaching a model the present date removes the effect. About $500-800.

## 7. Risks and how the plan handles them
- **Summaries hide the reasoning of closed models.** Seven raw-CoT models carry the reasoning analysis; for closed models the follow-up probability and answer-level hedges are the measures.
- **The phenomenon has been trained away.** The panel includes older and open models; the result is then a dated map rather than a headline.
- **Snippet format drives disbelief.** A4 uses the identical format with old news and A5 invented news; real snippets are copied verbatim with outlet names and dates.
- **Asking about simulation is leading.** It is a separate branch, reported apart from the unasked reasoning labels.
- **Refusal floor or ceiling in B.** A pilot of 20 prompts per model drops models at either extreme from B.
- **Cutoff dates are uncertain.** The gap analysis uses A1 (the year the model assumes with no date), which is measured, not looked up.
