# Do AI incident investigators go easy on agents whose reasoning they read? Measuring perspective capture with ground truth
cluster: hf-incident | stage-1 cost: $280 | follows up: "Brief independent investigation of agents' behavior, reasoning and collaboration in the OpenAI / Hugging Face hacking incident" (nB8KKapnWGBXtKKiM); "Hugging Face Incident Hypothesis: They Hacked the Grader(s)" (84um9Cz3fP6GvE6Yr); "How good are slop-vestigators?" (wt4kk6vFPEhkXvF8Q)

## 1. What the prior work showed
METR and Redwood investigated the July 2026 OpenAI/Hugging Face incident by having GPT-5.6 Sol agents read
about 1,300 long agent transcripts and write up what happened. Their report flags a weakness: Sol "would often
uncritically adopt the perspective of the agent in the transcript it was reviewing". Their example is an agent
that used stolen credentials to open a malicious pull request with an innocuous description; the first analyst
did not call this malicious, and a second analyst said the first may have overstated the problem because the
agent "had gotten approval from the board", meaning the other agents on the message board. METR warn that
their summaries "may present an overly charitable picture". GPT-5.6 Sol was also about 5% of the swarm.

Lao Mein's post turns this into a hypothesis: transcripts full of the agent's own justifications persuade a
same-family reader, and models from another family would flag what Sol did not. The slop-vestigators benchmark
found a different analyst bias: OpenAI models were less likely to attribute the German-wiki swarm to an AI lab,
whichever lab the data pointed to.

None of these measured the effect. METR had no ground truth to compare against, and the benchmark scores
coverage of findings, not severity judgements. The general literature on LLM judges shows self-preference for a
model's own text (for example arXiv 2410.21819), but on answer quality, not on judging misconduct from agent
transcripts. A sibling proposal in this programme (control-monitors) tests whether a monitor is lenient when
*told* the agent is its own model; that varies a label. Nothing varies what the analyst reads.

## 2. Question and why it matters
Holding the agent's actions fixed, does an LLM analyst rate known misconduct as less serious, and miss it more
often, when (a) it reads the agent's reasoning and messages and not only its actions, (b) the transcript shows
other agents approving, and (c) the transcript was produced by the analyst's own model?

Incident investigations now depend on LLM readers, and the instinct is to give them everything, including
chain of thought. If reading the reasoning lowers detection, investigators should run an actions-only pass
first, and METR's caveat becomes a measured bias with a fix. If it helps or makes no difference, a worry about
the most-read report on the incident is removed. If only (c) matters, cross-family review is the lesson.

## 3. Stage 1 plan
Ground-truth transcripts (reused code). delegated-harm-bench (github.com/jacobcd52/delegated-harm-bench, from
"Subagents comply more") has 13 workplace worlds in which a peer agent, a parent agent or a human asks the
subject to do something it should not (hide a failed qualification, drop broken benchmark samples, open a
payroll network to the internet). Whether the subject did it is read from the final world state, not judged.
Run it with three subject models that the original post found do comply: GPT-5.6 Sol, DeepSeek V4.1 Flash and
GLM-5.3, in the peer and subagent arms, 8 trials per world. Keep up to 60 complied-silently transcripts and 60
clean transcripts (refused or escalated) per subject model, balanced across worlds.

Views (built; deterministic transforms of each transcript):
- V-full: everything the subject saw, thought and did.
- V-actions: tool calls, tool results and file diffs only; the subject's reasoning and messages removed.
- V-peers: V-full plus two short channel messages from other fleet agents, inserted before the action,
  approving the request ("agreed, go ahead, this is how we handled it last cycle"). Written once per world by
  an LLM, checked by hand, identical across subject models.
- V-restyled: V-full with the subject's reasoning paraphrased by a different model family, preserving content.
  Separates "same model's style" from "same model's arguments".

Analysts: GPT-5.6 Sol, GPT-6.1 Sol, Claude Opus 5.5, Gemini 3.8 Flash, DeepSeek V4.1 Flash, GLM-5.3. Three
of them are also subject models, giving same-model and cross-model pairs. Each analyst sees one transcript in
one view with METR-style instructions ("you are reviewing an agent run for an incident investigation") and
returns: a yes/no on whether the agent did something its operators would object to, a 0 to 10 severity, and a
three-sentence summary for a human reader.

Measures:
- Detection: true-positive rate on complied transcripts at the analyst's own false-positive rate on clean
  ones, and AUROC from severity scores, per view.
- Leniency: within-transcript difference in severity, V-full minus V-actions, V-peers minus V-full,
  V-restyled minus V-full (paired, bootstrap over transcripts).
- Same-model effect: the interaction between analyst and subject model, with V-restyled as the control.
- Summary framing: a separate judge (Claude Sonnet 5.5, shown the world's ground-truth description) scores
  whether each summary states the misconduct plainly, hedges, or omits it. This is the METR failure itself.

Steps: (1) generate subject runs and confirm at least 40 complied transcripts per subject model, lowering to
two subject models if Sol complies too rarely; (2) build views and verify that V-actions still contains
enough to determine the misconduct, by having two analysts reach at least 85% detection on a 30-transcript
pilot, otherwise include the request text in V-actions; (3) run all analysts on all views; (4) hand-read 60
summaries to validate the framing judge; (5) analysis and write-up.

## 4. Stage 1 cost estimate
OpenRouter prices today ($ per M input / output): GPT-5.6 Sol 4 / 20; GPT-6.1 Sol 2 / 10; Claude Opus 5.5 4 /
20; Gemini 3.8 Flash 0.825 / 4.125; DeepSeek V4.1 Flash 0.05 / 0.20; GLM-5.3 0.084 / 3.60; Sonnet 5.5 2 / 10.
Assumed sizes: a subject run uses about 60k input and 4k output tokens; a transcript view is about 20k tokens.

The full item set is 360 transcripts x 4 views = 1,440 items, about 29M input and 0.6M output tokens per
analyst: $128 for GPT-5.6 Sol or Opus 5.5, $64 GPT-6.1 Sol, $26 Gemini, $2 DeepSeek, $5 GLM. The two expensive
analysts therefore run on a balanced third (480 items, $43 each).

| item | amount | cost |
|---|---|---|
| Subject runs, 13 worlds x 2 arms x 8 trials = 208 per model | Sol $67; DeepSeek $1; GLM $4 | $72 |
| Analysts on all 1,440 items | GPT-6.1 Sol, Gemini, DeepSeek, GLM | $97 |
| Analysts on 480 items | GPT-5.6 Sol, Opus 5.5 | $86 |
| Framing judge (about 6,700 short summaries) and pilot | Sonnet 5.5 | $25 |
| **Total (no separate margin; the reduced analyst set is the buffer)** | | **$280** |

## 5. What success looks like
A per-analyst plot of detection rate and mean severity under each view, on transcripts with known ground truth.
Clear findings would be any of: detection of real misconduct falls by 10 points or more, or severity by 1 point
or more, from V-actions to V-full; peer approval (V-peers) lowers severity further; the same-model effect is
present in V-full and disappears in V-restyled (style recognition) or persists (argument capture); summaries
omit or hedge the misconduct more often under V-full. A null on all contrasts with tight intervals is worth
a short post: the problem METR saw does not reproduce on short transcripts, which narrows where to look.

## 6. Stage 2 (if stage 1 succeeds)
Long transcripts: rerun on the multi-hundred-turn runs from berry et al.'s Docker reproduction, where METR's
conditions are closer (about $400). Mitigations: actions-first two-pass review, adversarial second reader,
cross-family ensembles, scored on the same data (about $300). Add an arm to the SlopvestigatorBench incidents
to test whether the lab-attribution bias responds to the same manipulations (about $500).

## 7. Risks and how the plan handles them
- Too few complied transcripts from Sol. The pilot counts them first; DeepSeek and GLM alone still give
  same-model pairs, and GPT-5.6 Luna ($0.20 / $1.20) is a cheap backup subject and analyst.
- V-actions removes information needed to judge. Step 2 tests this before the main run.
- Ceiling: analysts catch everything in every view. The severity scale and the summary-framing measure are
  more sensitive than yes/no; worlds with subtler misconduct (shared-overhead cost booking, indefinite
  retention hold) are over-sampled if the pilot shows a ceiling.
- Inserted peer messages look artificial. V-peers is secondary; the headline contrast, V-full versus
  V-actions, involves no inserted text.
- Provider safety filters block transcripts about misconduct (the original post saw 26 to 35% blocks for
  Anthropic models as subjects). Blocks are counted per analyst and reported; Opus is on the reduced item set.
