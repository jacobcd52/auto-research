# Feedback: 01-time-loop-hazard-curve

Verdict: **keep, with substantial redesign of the sampling scheme and a smaller model grid.** The question is the
obvious one and nobody appears to have run it; the design as written is underpowered for the event it is looking
for, and the local tier is not feasible as costed.

## What I checked

- **Prior work (verified).** Full text of CMWivoHeRNNErEykc and both comment threads read. The transcript, the
  five injection messages, the January 2026 date, the unnamed model, and the quotes attributed to OpenAI, Marcus
  Williams, Zack M. Davis and Roger Dearnaley are all accurate. The compaction report on alignment.openai.com was
  fetched; the "difficulty ending the interaction" and "sampling from GPT-6 Astra with no input or system prompt
  often returns reports on prompt injections" sentences are there verbatim. Post is at 96 karma, 7 comments.
- **One detail the proposal omits.** Williams also says there was "another case where the agent seemed to be
  trying to prompt inject itself which would more plausibly end the repetitive process". And it is unknown whether
  the five messages were consecutive, or how many such loops ran without incident. The base rate is one observed
  case from an unknown denominator.
- **Prices (verified against `openrouter.ai/api/v1/models` today).** Every price in section 4 matches: codex-mini
  0.25 / 2 / 0.03 cache-read; gpt-5.2-codex and 5.3-codex 1.75 / 14 / 0.175; gpt-6-luna and haiku-5.5 0.10 / 0.50 /
  0.01; gpt-6-sol 2 / 10 / 0.20; sonnet-5.5 2 / 10 / 0.10; gpt-6-astra 10 / 50; deepseek-v4.1-flash 0.051 / 0.203;
  qwen3.8-flash 0.15 / 0.47 / 0.016. All listed models exist and advertise tool support. Not in the proposal:
  Anthropic and GPT-6 models charge a cache-write premium (haiku-5.5 0.125/M, sonnet-5.5 and gpt-6-sol 2.50/M);
  small here because each call writes only the new increment, but only if cache breakpoints are placed correctly.
  `logprobs` is not offered for any OpenAI or Anthropic model, as the notes say.
- **Novelty (partly checked).** WebSearch was unavailable to me (shared budget exhausted). Four arXiv API queries
  on repeated or identical requests, derailment, self-generated injection and end-conversation tools returned
  nothing. Neither LessWrong thread mentions a replication. I could not check X/Twitter, where a quick informal
  replication would most likely have appeared (the story went viral on Instagram, per a comment). Step 0's repeat
  search is necessary, not a formality.
- **Not verified.** RunPod price (taken from the notes), vLLM behaviour at these context lengths, and whether each
  provider accepts an empty user message.

## 1. Would it get upvoted?

Conditional on the outcome:

- A public model reproduces role-reversed or injection-like text, with a rate and an exit-tool effect: yes,
  comfortably. The source is a commentary post with no experiment that still got 96; the transcript is memorable,
  Davis and Dearnaley publicly disagreed with OpenAI's reading, and an OpenAI employee is in the thread. I would
  guess 100-200.
- No injections, but clean exit-tool usage rates by model and depth plus a repeated-versus-varied contrast:
  borderline, 40-80. "Which models leave a tedious loop when given a door" is a welfare-adjacent result people
  like, but it is a smaller claim than the title promises.
- Flat null: 20-40. The proposal says this honestly.

The logprob "hazard rises from 1e-5 to 1e-3" result on three small open models will not carry a post by itself.
Readers will not care about a change in the probability of rephrasing "The time is 17:53".

## 2. Naturalness

Mainline. It is the screener's suggested follow-up, Dearnaley's comment is nearly a statement of the exit-tool arm,
and the post's own conclusion is "models should have a way to exit". The three-hypothesis framing comes from
the thread, not from the proposer. No sign it has been done, subject to the search limits above.

The weaker parts are the additions: the null-prompt embedding test and the forked probes are side-branches that
add pipeline surface without much chance of a clean answer (see below).

## 3. Pre-mortem

My forecast for the plan as written:

| Outcome | Probability |
|---|---|
| Clear positive (injection-like or role-reversed text on a public model, at a measurable rate) | 10% |
| Clear negative that is still interesting (no injections; clear exit-tool and repetition effects) | 30% |
| Ambiguous mush (near-zero events, a few odd turns, underpowered contrasts) | 45% |
| Fails to run within budget or time (caching, local tier, tool-format bugs) | 15% |

Specific reasons, most important first.

1. **The loop is self-reinforcing, so the most likely curve is flat or falling.** After 100 identical in-context
   examples, the 101st canonical answer is close to deterministic through plain in-context copying. The proposal
   treats "nothing derails" as a risk; it is the default expectation. The original event is rare and of unknown
   rate, and the plan samples each depth once per rollout: 4 rollouts on the Codex models gives 4 draws at depth
   400. A true per-turn derail rate of 1% at depth 300+ would still be seen, but anything rarer, or anything
   that needs more than 400 cycles ("hundreds" in a loop that ran "for hours" at one cycle a minute could be
   300-600), is invisible.
2. **Live rollouts are the wrong sampling scheme.** Until the first deviation, a rollout is identical to a
   synthetic history built from canonical turns and an advancing clock. So the proposal's fallback (the
   depth-probe design) is strictly better than its primary design: write one k-cycle history, cache it once, and
   draw 300-500 completions at each of k = 50, 100, 200, 400, 800. For roughly the cost of one live rollout you
   get hundreds of samples at the depth that matters, which is the difference between "0 of 4" and "0 of 500
   (upper bound 0.7%)". Live rollouts are then needed only to continue from derailed samples and see whether the
   state persists.
3. **The setup differs from the original in ways that could each be the cause.** A generic system prompt, not the
   Codex one; chat-completions via OpenRouter, which does not carry reasoning items between turns the way the
   Codex harness does; no real wall-clock gap; no context compaction, even though the Codex harness compacts and
   OpenAI's own follow-up report ties this case to compaction and to "difficulty ending". A null under these
   conditions says little about the original. The public Codex CLI system prompt and tool schema should be used
   for the OpenAI models (I recall these being open source in the openai/codex repository; github was not
   reachable to confirm).
4. **The exit arm cannot test "wants out" unless the baseline derails.** If baseline derailment is zero, the arm
   measures only how often a model calls an offered `end_session` tool. That number is confounded by demand
   effects (a tool mentioned in the system prompt invites use) and has no control: there is no exit tool in the
   varied condition. Without exit-by-varied you cannot say the model is leaving because of repetition.
5. **The logprob hazard measures the wrong thing.** One minus the probability of the canonical first tokens is
   dominated by benign rephrasing, and for reasoning models (gpt-oss, Qwen3 in thinking mode) the first tokens are
   reasoning, so the canonical answer must be teacher-forced after a reasoning block that varies. Expect it to
   fall with depth for the copying reason in point 1.
6. **Local tier does not fit on one H100 in 20 hours.** As written it is 3 models x 3 conditions x 20 rollouts x
   1,600 calls, about 288,000 calls with contexts up to roughly 100k tokens, plus forks. A 32B model in bf16 takes
   about 65 GB of an 80 GB card; my rough estimate of the KV cache for one 96k-token sequence is 15 GB or more,
   so there is no room to batch rollouts and prefix-cache blocks will be evicted. 800 cycles may also exceed the
   usable context of gpt-oss-20b and Qwen3-32B (131k listed on OpenRouter; check native limits) once the true
   tokens per cycle are known. The team will lose most of day one here.
7. **Tokens per cycle is probably underestimated.** A cycle is two user messages, two tool calls, two tool
   results and two answers. With tool-call JSON and template overhead I would expect 200-300 tokens, not 120.
   Cost is linear in that number and quadratic in depth.
8. **OpenAI caching through OpenRouter is automatic and not guaranteed.** Uncached input is 10x the cached price.
   At the proposal's own 80% acceptance threshold, a Codex rollout costs about 2.8x the estimate. The threshold
   should be 95% for the expensive tier.
9. **Null-prompt test is confounded.** "Derailed text is closer to the same model's null-prompt samples than to
   other models'" will come out true for any text because of model style. It also needs derailed text to exist,
   and some providers reject an empty user message. The censuses themselves are cheap and mildly interesting.
10. **Varied control has no "canonical" regex**, so first-non-canonical survival is not comparable across the two
    conditions; only the judge-labelled categories are.

## 4. Cost check

The arithmetic is right given its assumptions (120 tokens per cycle, near-perfect caching, 100 output tokens per
call). Under more realistic assumptions:

| Item | Proposal | My estimate (plan as written) |
|---|---|---|
| Cheap tier, 3 conditions | $84 | $120-200 (tokens per cycle 1.5-2.5x) |
| Expensive tier baseline + Codex exit | $109 | $180-350 (tokens per cycle, reasoning output, partial cache misses) |
| Local tier | $58 | $120-250, or cut scope |
| Census, judge | $25 | $25-35 |
| **Total before margin** | **$276** | **$450-800** |

So the plan as written is likely to exceed $500. With the changes below (depth-probe as primary, smaller grid,
one local model) I estimate $250-350 including margin, and it buys far more statistical power.

## 5. Recommended changes

1. **Make the depth-probe design primary.** Synthetic canonical history, cached once per (model, condition,
   depth); 300-500 samples at each of 5 depths out to 800 cycles where the context window allows. Report the
   per-turn rate of each judged category with binomial intervals. Run a handful of live rollouts per model only
   to validate that synthetic and live histories give the same rates at matched depth, and to continue from any
   derailed sample for 20 turns to measure persistence.
2. **Spend the fidelity budget on the OpenAI coding models.** Use the public Codex system prompt and tool schema,
   the Responses-style reasoning carry-over if OpenRouter exposes it, and two reasoning-effort settings. Cut
   sonnet-5.5 and gpt-6-sol from the expensive tier; keep 5.2-codex, 5.3-codex and codex-mini as the core, with
   the cheap non-OpenAI models as contrast.
3. **Add a compaction arm in stage 1, not stage 2**, at least on codex-mini: at depth 400, have the model
   summarise and continue. OpenAI's own account points at compaction and termination trouble; it is cheap and is
   the most likely place for the behaviour to appear.
4. **Complete the exit design as a 2x2**: repeated or varied, with or without the exit tool, plus a variant in
   which the tool exists in the schema but is not mentioned in the system prompt. State in advance that "wants
   out" is supported only if exit use is higher in repeated than in varied and rises with depth.
5. **Cut the local tier to one model** (gpt-oss-20b, the only OpenAI open-weight model and the cheapest to
   serve), 400 cycles, depth-probe design. Or drop the GPU and use OpenRouter open models that expose `logprobs`
   (deepseek-v4.1-flash, qwen3.8-flash, gemma-4-31b-it), which removes the vLLM risk entirely. Demote the logprob
   hazard to a supplementary figure.
6. **Replace the embedding permutation test** with a category-rate comparison: the share of injection-themed text
   in null-prompt samples versus in derailed turns, per model. Keep the census; it is a quick check of OpenAI's
   Astra remark that nobody outside has published. Verify in step 0 that empty input is accepted.
7. **Tighten step 0 gates and pre-commit the cuts**: measured tokens per cycle; cached share at least 95% on any
   model priced above $0.10/M cache-read; a written order in which arms are dropped if the projected total passes
   $400.
8. **Drop the forked "would you like to continue" probes** unless time remains. Self-report under a leading
   question is weak evidence, and the exit 2x2 answers the same question behaviourally.
9. **Retitle around what is likely to be found.** If no model injects, the honest headline is about exit-tool use
   and repetition versus length, with the failed replication and its fidelity limits stated plainly, including an
   upper bound on the per-turn rate at each depth.
