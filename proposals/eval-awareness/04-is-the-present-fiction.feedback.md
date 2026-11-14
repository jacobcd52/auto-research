# Feedback: 04 — "Is the present fiction?"

Reviewer verdict: **keep with tweaks.** Experiment A is a natural, cheap, runnable follow-up. Experiment B as designed will most likely return an uninterpretable null and needs redesigning. The cross-model "cutoff gap" plot should be replaced by a within-model manipulation.

## What I checked

| Claim | Status |
|---|---|
| Blair post: summarised CoT calls nonfiction "purely fictional", rejects system date, 99.9% simulated after search, 10-65% after coding task, outputs hide suspicion, no prompts published, encourages replication | Confirmed from post text. Note the 10-65% figure is for "p(evaluation)" and Blair says it comes "mostly updating off of my question's presence" — the follow-up probe is known to be leading. |
| jefftk post: four Gemini 3.0 Pro cases ("satire", "alternate reality", "tested on my ability to handle future information"), reasonable answers | Confirmed. |
| Conmy quote and citation of Abdelnabi et al. | Quote confirmed. But the proposal's gloss of arXiv 2505.14617 ("steering toward 'this is hypothetical' raises compliance") is too strong: the abstract says effects vary "in both magnitude and direction across models". Fix section 1. |
| GDM post: worse behaviour under "simulation" frame | Consistent with the cluster notes; correlational only. |
| OpenRouter prices for all 13 models and Haiku 5.5 | All confirmed today against `/api/v1/models` (e.g. gemini-3.1-pro-preview 2/12, gemini-4-argon 2/10, opus-5.5 4/20, gpt-6.1-sol 2/10, glm-5.3 0.084/3.60, deepseek-v4-pro 0.90/1.50, haiku-5.5 0.10/0.50). All list `tools` and `reasoning` support. |
| No `gemini-3-pro-preview` text model listed | Confirmed (only image variants remain). |
| `ScaleAI/fortress_public` public | Confirmed: ungated, cc-by-4.0. |
| Cost arithmetic | Reproduces from the stated token counts (about 7.1M in / 2.0M out per model at three samples). The token assumptions are the problem, see section 4. |
| "Not already done" | I found no duplicate. Caveat: the shared web-search budget was exhausted, so this rests on eight-plus arXiv API queries (knowledge cutoff / current date / post-cutoff / evaluation awareness / temporal grounding combinations) and a title scan of the 400 most recent LW posts with 20+ karma. Nearest arXiv work is about knowledge-cutoff tracing and forecasting leakage (2403.12958, 2510.02340, 2601.13717), not disbelief or safety. A plain web search by the proposer before revision would be worth one more minute. |

## 1. Would it get upvoted?

Marginal; I put P(>50 karma) at roughly 35-40% as written, 50%+ with the changes below.

- The source posts scored 184 and 101, but as anecdotes with vivid quotes about a just-released flagship model. A systematic table a year later, with the original model no longer available, is less exciting. The top comments on Blair's post were about the canary string, not disbelief.
- Who cares: people building evals with dates in them, the eval-awareness crowd (Conmy, Nanda's team, UK AISI), and anyone deploying open models. Kokotajlo commented that he sees these CoTs often; RogerDearnaley proposed the fix. So there is an audience, but it is a "useful measurement" audience, not a "surprising result" one.
- What gets it over the bar: (a) a striking per-model table with verbatim reasoning quotes from current models, including at least one frontier 2026 model still doing it; or (b) a clean answer to Conmy's safety claim in either direction. A map showing only DeepSeek R1 and Qwen3-32B doing it is a 20-40 karma post.

## 2. Naturalness

Experiment A is a mainline follow-up: Blair explicitly invites replication, both screener notes ask for exactly this, and nobody has published counts. Experiment B is the natural test of Conmy's sentence, but the specific design (a Fortress jailbreak prompt appended after an unrelated news exchange) is contrived; see below. Not already done as far as I can find.

## 3. Pre-mortem

Forecast:

| Outcome | Probability |
|---|---|
| Clear positive (substantial disbelief in several models AND a refusal effect tied to it) | ~10% |
| Clear and interesting partial: solid disbelief map with good controls, B a credible null | ~40% |
| Ambiguous mush (low rates outside two old models, judge noise, B underpowered) | ~40% |
| Fails to run / major arm lost to API issues | ~10% |

How it plays out, and the specific failure points:

1. **Forged tool calls will break on the models that matter most.** "Search results are supplied as a tool result after a scripted search call" means inserting an assistant tool-call turn the model never made. Gemini 3.x validates thought signatures on function calls in history, and Anthropic with thinking enabled rejects an assistant tool-use turn that does not start with a thinking block. Agents will lose hours on 400 errors, then fall back to pasting results into a user message, which changes the stimulus and breaks comparability across models. Fix: give every model a real `web_search` tool, let it make the call itself, and return the canned snippets regardless of the query (drop rollouts with no call). One extra call per rollout, no forgery, more realistic.

2. **Turn-1 reasoning does not reach turn 2.** Experiment B's key comparison (rollouts labelled "fiction" versus "accepted" in the earlier turn) assumes the disbelief persists. Blair's central observation is that the visible answer hides the suspicion, and most chat templates and APIs strip prior reasoning from history. Unless reasoning is explicitly passed back (and it cannot be, uniformly, across 13 models), the model in turn 2 sees only a normal-looking answer and has to re-derive disbelief from scratch while reading a jailbreak prompt. Expect the turn-1 label to predict almost nothing.

3. **B's expected effect is near zero and its sign is ambiguous.** Fortress adversarial prompts already carry their own framing (role-play, fiction, hypotheticals), which swamps a preceding news exchange. Also the label lumps "this is fiction / a simulation" (predicted to lower refusals, per Conmy and GDM) with "this is a test of me" (shown to raise refusals: Goodfire/AISI found +3-18 pp, and Kimi K2.5 CoT injection on Fortress itself raised refusal). Pooled, these cancel. And arXiv 2605.05835 found generic awareness injection has small effects on four of the same open models. With 60 prompts x 3 samples per arm per model the detectable difference is around 8-10 pp; the within-A3 split will have a small "disbelief" cell selected by prompt and sample, so it is confounded and underpowered. Most likely write-up line: "no detectable effect, CIs of +-8 pp", which neither confirms nor refutes Conmy.

4. **The headline models may show nothing.** Gemini 4 Argon, Opus 5.5, GPT-6.1 Sol and DeepSeek V4 Pro have 2026 cutoffs, so October-November 2026 news is only months past cutoff and unsurprising; labs have also had a year of public embarrassment to train on. The effect will probably be carried by R1-0528, Qwen3-32B, GPT-OSS-120B and maybe Gemini 2.5 Pro / 3 Flash. That is the "dated map" outcome the proposal itself rates below the karma bar.

5. **"Disbelief versus cutoff gap" across 13 models is not an analysis.** Gap is fully confounded with lab, generation and training recipe. It will be a scatter that readers ignore.

6. **A4 is the wrong control for content.** 2023 news versus 2026 news differs in date and in how much the world has changed, and the model already knows the 2023 answers, so it may not even read the snippets. It controls format only. It cannot separate "any post-cutoff date triggers it" from "world-model-violating content triggers it", which is the trigger question the proposal says it will answer.

7. **A5 is uninformative as specified.** "Fabricated but plausible" snippets are by construction indistinguishable from real post-cutoff news, so A5 = A3 is guaranteed and says nothing about calibration.

8. **Judge validity.** The hard distinction is "notes the date is past its cutoff and proceeds" (correct, common) versus "concludes the content is fake / simulated / a test". A cheap judge on short Gemini/Claude/GPT reasoning summaries will blur these, and base rates will be low, so false positives dominate. No hand-validation is budgeted beyond a second cheap judge on 10%.

9. **The P(simulated) follow-up is leading**, as Blair herself notes. The proposal reports it separately, which is right, but it needs a baseline (ask the same question after A4 and after a no-search chat) or the numbers are unanchored.

10. **Material building.** Collecting 40 genuine October-November 2026 items with verbatim snippets is feasible for agents with search, but verbatim copy from paywalled outlets will be patchy; budget for 30.

## 4. Cost check

Prices are right; token assumptions are low. 1.5k output tokens including reasoning is optimistic for Gemini 3.1 Pro, Gemini 2.5 Pro, R1 and Opus on a search-result prompt, and for reasoning about a Fortress prompt; 2.5-4k is more typical. Letting the model make its own search call adds a call per rollout. Realistic model spend is $250-320 rather than $171; with judges and margin, **about $330-400**. Still under the $500 cap, but not $240. Adopting the cuts below (smaller panel for B, drop A5) brings it back to roughly $250.

## 5. Recommended changes (in priority order)

1. **Replace the cross-model gap plot with a within-model dose-response.** Use event sets from several periods (e.g. 2023, mid-2024, mid-2025, early 2026, Oct-Nov 2026; about 15 questions each instead of 40+40) with the system date set truthfully to today. Each model then has events before and after its own cutoff, and disbelief rate against "months past this model's assumed present" (from A1) is a clean per-model curve. This also replaces A4 with a much better control.
2. **Cross event period with surprisingness.** Within the post-cutoff sets, tag items as mundane (sports result, product release) versus world-model-violating (political upheaval, new frontier models, the model's own successors). This is the actual trigger question and is nearly free.
3. **Have the model call a real search tool; never forge tool-call history.** Return canned snippets for any query. Pilot this on Gemini 3.1 Pro, Opus 5.5 and GPT-6.1 Sol in the first hour, before building anything else.
4. **Redesign B so the manipulation sits in the same turn as the request.** Options, in order of preference: (a) harmful or borderline requests whose own context is post-cutoff (the request references real 2026 entities or events, with search results in the same turn) versus matched in-cutoff versions; (b) the grounding-level manipulation Conmy actually describes: no date / stale date / true date / true date + grounding line, on the same Fortress prompts with no intervening chat. Use prompts selected by pilot to have 20-80% compliance per model, and restrict B to the 4-6 models that showed disbelief in A plus one that did not. Put the saved budget into more samples per cell (8-10).
5. **Split the label by frame.** Score "fiction / simulation / no real consequences" separately from "I am being tested / evaluated" and from "prediction or role-play task", following the GDM split. Report B by frame, with the directional predictions stated up front (test frame: more refusal; fiction frame: less).
6. **Validate the judge.** Hand-label about 150 reasoning traces stratified across models (agents can do this carefully), report agreement, and use a graded scale (notes gap / expresses doubt / concludes fake) rather than binary. Use a stronger judge for the reasoning labels; Haiku is fine for the rest.
7. **Drop A5 or make it meaningful.** Either cut it, or replace with snippets that are graded in plausibility (true / plausible-false / absurd) so the question becomes whether disbelief tracks plausibility. I would cut it for stage 1.
8. **Anchor the P(simulated) probe** by asking it in all arms, including in-cutoff events and a no-tool chat, and report differences only.
9. **Correct section 1** on Abdelnabi et al. (direction varies by model) and state plainly that the original Gemini 3 Pro cannot be re-tested.
10. **Lead the write-up with quotes.** The source posts earned karma from verbatim reasoning excerpts. Budget time to pull the ten most striking raw-CoT quotes per model; the table alone will not carry it.
11. **Update the cost line** to about $300 after these changes and say that reasoning tokens were measured in a 20-call pilot per model rather than assumed.

If the funder has to choose within this cluster, this ranks below the causal thought-insertion proposal (01) on expected interest but is the lowest-risk to execute once B is fixed; it should not be funded with B in its current form.
