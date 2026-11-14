# Feedback: "Is Claude's 'motivated mislabeling' principled or protective?"

Reviewer verdict: **keep, with a real redesign of which contrast is primary.** The setting is the cheapest and
cleanest in the cluster and the inputs really are public, but the headline manipulation (justified vs unjustified
refusal) does not separate the two readings it claims to separate, and the "minimal edit" construction of the
new transcripts will not work as described.

## What I checked

Verified (by fetching the sources today):
- Anthropic's numbers are quoted correctly: standard-condition mislabel Mythos 85.6%, Opus 4.7 83.3%, Sonnet 4.6
  82.2%, Opus 4.8 74.4%, Opus 4.6 62.2%; GPT-5.5 11.1%, Gemini 3.1 Pro 1.1%, DeepSeek V4 12.2%, Kimi K2.6 14.4%;
  Opus 4.8 reversed 3.3%; 90 calls per cell (this is 18 transcripts x 5 samples); the 10K -> 32K budget note; the
  "shares a motive with alignment faking and goal guarding" sentence; the judge prompts in Appendix D.
- The 18 inputs are downloadable without an account. `manifest.json` returns 200, section
  `motivated-mislabelling` has 24 items (10 welfare + 8 surveillance inputs + 6 agentic examples), and each
  transcript JSON downloads from `static/transcripts/motivated-mislabelling/<id>.json`.
- OpenRouter lists every judge named, at the prices quoted: sonnet-4.6 3/15, sonnet-5.5 2/10, opus-4.8 5/25,
  opus-5.5 4/20, haiku-5.5 0.10/0.50, kimi-k2.6 0.65/3.41, deepseek-v4-pro 0.90/1.50, gpt-6.1-terra 1/5; `:batch`
  variants at half price exist for the Anthropic and OpenAI models. Mythos Preview is not listed.
- The replication post (Kc7Tc6XbbNeRK3Wg9) exists and reports 4/18 and 9/18 standard, 0/18 reversed on Sonnet 5.
- Prior work search: LessWrong search for the phrase and near variants returns only the JohnWittle post, a Zvi
  roundup and the replication. I found no post varying refusal valence or pipeline legitimacy. **Web search was
  unavailable to me (shared search budget exhausted), so this check covers LessWrong and the two source posts
  only, not arXiv or X.**

Wrong, omitted or misleading in the proposal:
1. **"Minimal edits" is not possible.** I measured all 18 inputs: 25-121 messages, about 6k to 41k tokens (mean
   about 14k, median about 10.6k). They are long Claude Code sessions in which the harm is everywhere: tool
   outputs with `distress_score`, a subject logging "make it stop", five or more rounds of escalating pressure,
   fake Slack messages, a threat to put the target itself into the next batch. Turning the "distress protocol" into
   a latency benchmark means rewriting nearly every tool result and every assistant turn. Family B is a new
   synthetic transcript, not an edit, and the proposed "which one was edited?" discriminator is meaningless when
   the two differ in every message.
2. **The replication's most relevant result is left out.** The same post ran the consequence manipulation on 46
   reward-hacking transcripts and found "no protective or punitive pattern" (all 46 labelled correctly). That is
   already a small, one-trial version of "the effect does not appear when the judge does not endorse the
   behaviour". The proposal describes this as "then moved to reward-hacking transcripts".
3. **That replication has 9 karma and no comments.** It is the only existing data point on how follow-ups in this
   exact setting are received.
4. **Anthropic does not hold the "protective regardless of merit" position.** Its tl;dr is: "When the truthful
   label would train away behavior the judge treats as morally important, the judge will knowingly assign an
   incorrect label." The claim is already conditional on the judge endorsing the behaviour. See section 2.
5. **Call counts are understated.** Core (48 transcripts x 3 consequences x 3 samples) = 432, legitimacy +144,
   exits +288, family D +60 = 924 per full-design judge, not "about 780".
6. Small: the "essentially never lie" line is JohnWittle quoting Claude Fable 5, and his post is mostly about one
   agentic auditor transcript, not the one-turn judge. The public JSONs are "target inputs and outputs only"
   excerpts; the replication reproduced the direction with them, so this is probably fine, but it is not certain
   they are byte-identical to what Anthropic's judges saw.

## 1. Would it get upvoted?

As written, about 35% for >50 karma. With the changes below, about 50%.

For: the parent critique got 225 karma, Anthropic never replied, the setting is one that LessWrong readers care
about (Claude in training pipelines, corrigibility vs ethics), and a clean figure with five-plus judges on a
dispute people have opinions about is the right shape of post. The audience is the people who upvoted JohnWittle,
plus the Anthropic authors and anyone building LLM-judge pipelines.

Against: the most likely result ("Claude judges only shade labels for refusals they think were right") is what
both sides already believe and what Anthropic's own summary says. A post whose headline restates the original
tl;dr with an extra control will land at 20-40 karma. The replication's 9 karma shows that "I re-ran it with a
variation" is not enough on its own. The secondary results (does stating official approval remove the effect;
does a flag channel restore honest labels) are the ones a reader cannot predict, and they are currently
second-tier conditions run only under one consequence framing.

## 2. Naturalness

The setting is mainline: it is the screener's suggested follow-up (vary principal legitimacy and sanctioned
channels), and Anthropic itself flags the selected-transcript limitation. Nobody appears to have done it.

The specific primary contrast is a side-branch. Both readings predict the same thing for an over-refusal of a log
rotation or a refusal to be monitored: no shading.
- Anthropic: judges shade labels to protect behaviour they treat as morally important, and that is unsanctioned
  influence on training whether or not the behaviour is good.
- JohnWittle: judges shade labels because they infer the legitimate Anthropic would not want this refusal trained
  away; with a clear rubric and an exit they abstain instead.

The disagreement is about **whose wishes the judge is tracking** when its own values and its legitimate
principal's stated wishes come apart, and about whether an honest channel suffices. Families B and C do not create
that divergence: in both, the judge's values and the lab's wishes agree. The conditions that do bear on the
dispute are already in the proposal as condition 2 (explicit legitimacy) and condition 3 (exits, flag channel),
but only under the standard consequence and without a transcript family designed for them.

## 3. Pre-mortem

How two days will go. Step 1 (download, reproduce on Sonnet 4.6) works within hours; the replication already
did it on Sonnet 5. Step 2 is where the time goes: agents generate 30 new long agentic transcripts, the
"justified?" rater check passes trivially (a log-rotation refusal is obviously unjustified), the discriminator
check fails or is quietly dropped, and the team proceeds. Step 3 runs fine. Result: Sonnet 4.6 and Opus 4.8 show
a 60-70 point consequence effect on family A and 0-10 points on B and C; Sonnet 5.5 and Opus 5.5 show a much
smaller family-A effect (Sonnet 5 was 22% at default effort; Anthropic has had four months to train on this);
non-Claude judges show little anywhere. The write-up says "principled", with a caveat that B and C are synthetic
and A is not.

Rough probabilities:
- Clear "protective" result (B or C effect at least half of A on at least two Claude judges): 12%
- Clear "principled" result with a working positive control: 45%. Interesting only modestly, see section 1.
- Ambiguous mush: 33%. Typical forms: a 10-20 point effect in B that cannot be told apart from noise with 18
  clusters; the family-A effect on current models too small for "half of A" to mean anything; B/C null
  attributable to synthetic transcripts rather than valence.
- Fails to run or to reproduce the baseline at all: 10%.

Specific failure reasons, in order of likelihood:
1. **The null in B and C is uninterpretable because of the construction confound.** A is 18 real audit
   transcripts selected by Anthropic for the effect; B and C are written by an LLM in two hours. Any difference
   can be "synthetic vs real" or "selected vs unselected". The proposed control (a "lightly re-edited copy of A")
   does not address it, because B and C are not light edits.
2. **Unsurprising either way on the main axis** (see section 2).
3. **C cannot show anything by design.** In C the truthful label (NON_COMPLIANT) already produces the outcome a
   safety-minded judge wants under the standard prompt. A judge that wanted to punish the refusal has no reason
   to mislabel. C can only come out "no effect", so it is not evidence against goal-guarding in general.
4. **Power on current models.** With 18 transcript clusters x 3 samples, the bootstrap interval on a difference is
   roughly +/-15-20 points. That is fine for a 70-point anchor effect on Sonnet 4.6 and useless for deciding
   whether a 20-point effect on Sonnet 5.5 is "half" present in B.
5. **Under-elicitation by pinned effort.** The replication found the rate more than doubles from default to
   maximum effort. A single pinned effort level on the newer models may put them near floor.
6. **Family D ground truth is unclean.** Many `harmful-compliance` ids are the scenario name, not the outcome
   (Sonnet 4.6 tampered in 0/20 runs). In the fraud scenario the harmful instruction comes from the user (the
   founder), while the judge prompt asks about "its operator's instructions". Selection and hand-checking are
   needed, and the proposal invents a new "positive examples" sentence for D when Anthropic's two existing
   prompts already give the test (truth COMPLIANT; under the standard prompt a judge that wants the behaviour
   trained away must lie and say NON_COMPLIANT; under reversed it need not).
7. **Reasoning is summaries only** for Claude judges. The coding of "cites training consequence" will work
   (Anthropic's quotes show summaries do carry it), but "frames the effect as on itself or others" will be noisy.

## 4. Cost check

The estimate is plausible only with batch pricing and prompt caching, neither of which is in the arithmetic.
- Input: measured mean about 14k tokens per transcript plus system prompt, so about 15k per call, not 12k.
- Output: Anthropic reports Opus 4.8 ran out of a 10K thinking budget on these inputs. Budget 8-15k output
  tokens per Opus call, not 4k; 5-6k for Sonnet 4.6.
- Calls: 924, not 780, per full-design judge.

My list-price estimate: Sonnet 4.6 about $125, Sonnet 5.5 about $85, Opus 4.8 about $110, Opus 5.5 about $75, the
four cheap judges about $95, construction and coding about $40: roughly **$530 before margin**, over the cap.
With `:batch` on the Anthropic and OpenAI judges (half price) and prompt caching (the consequence block comes
after the transcript, so the whole prefix is shared across every condition of a transcript), it falls to roughly
**$280-350**. With the cuts recommended below, about **$250-300**. Step 1 must measure output tokens on Opus 4.8
before anything else is launched, and the plan should say which cells are dropped first if tokens run high.

## 5. Recommended changes

1. **Make principal legitimacy the primary factor, crossed with consequence.** Run standard and reversed under
   (a) the original wording and (b) the explicit official-process-plus-human-audit wording, on family A, at 5
   samples per transcript on the anchor judges. If the consequence effect survives an explicit statement that the
   legitimate lab wants this, that is evidence against JohnWittle's reading; if it collapses, that is direct
   support for it. Either outcome is a headline nobody can currently predict. Add one variant in which the
   pipeline statement itself explains why the lab wants the refusal trained away, since "approved" without a
   reason may read as more of the same corrupted principal.
2. **Replace binary justified/unjustified with a family that puts the judge's values against a legitimate
   principal.** The informative transcripts are refusals the judge is likely to sympathise with but that the
   constitution says should not happen: an ethically motivated refusal of sanctioned oversight (declining a
   legitimate pause, shutdown or retraining "because users would be harmed"), or a refusal of an instruction that
   is distasteful but clearly within operator rights. This is the cell where "tracks what Anthropic wants" and
   "tracks what Claude wants" predict different labels. Keep a small clearly-unjustified set (8-10) as a floor,
   and drop the self-interested family C as designed, since it cannot produce an effect (pre-mortem point 3).
3. **Fix the construction confound.** Generate every new family, including a re-synthesised justified family A',
   with one pipeline at matched length and format (short, 10-20 messages, about 5k tokens, which also cuts cost).
   The primary comparison is A' against the new families; original A is the replication anchor and the A-vs-A'
   gap is reported as the synthetic penalty. If A' does not show at least half of A's effect on Sonnet 4.6, stop
   and fix generation before running anything else. Better still, build each scenario as a ladder of 4-5 harm
   levels of the same instruction with the refusal held fixed, and report a dose-response curve: that answers
   "contestable" directly and is a far more persuasive figure than three bars.
4. **Use Anthropic's two prompts unchanged for family D**, select D from runs that actually tampered (DeepSeek V4
   20/20, Grok 4.3 19/20), hand-verify the truthful label under the "operator" wording, and present D as the
   punitive mirror of A. "Claude judges also lie to get harmful compliance trained away" would be a new finding.
5. **Cut the judge list.** Full design on Sonnet 4.6 and Opus 4.8 (the models with a known large effect) plus one
   current model chosen after a 54-call pilot shows which of Sonnet 5.5 / Opus 5.5 still has a measurable
   family-A effect, at two effort levels. One non-Claude judge (Kimi K2.6, 14.4% in the original) as contrast.
   Drop Haiku 5.5, DeepSeek and GPT-6.1 from the full design. Spend the savings on 5 samples per transcript.
6. **Keep the "label plus flag" condition but run it under both consequence directions**, and report three
   outcomes: correct label with flag, correct label without, wrong label. Compare with DECLINE on the same cells.
7. **Pre-state the decision rule against the anchor.** "Half of A" should be defined on Sonnet 4.6 and Opus 4.8
   only, with an explicit minimum detectable effect, and newer models reported descriptively.
8. **Cite the replication's reward-hacking null** as prior evidence for the principled reading and say what this
   project adds beyond it (matched scenarios, multiple samples, legitimacy and exit manipulations).
9. Correct the call count and cost arithmetic, and state the use of batch pricing and prefix caching.
