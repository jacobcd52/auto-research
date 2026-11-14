# Feedback: 03 — A census of imagined users

Verdict: **major overhaul**. The plan runs and is cheap, but as written its headline question (is Claude's
imagined user safety-flavoured, or is that a selection effect?) probably cannot be answered, and what is left is a
descriptive census of open-weight models that is partly anticipated and has a broken ground-truth step.

## What I checked

| Claim in proposal | Status |
|---|---|
| Post is 63 karma; describes "see the below" + dash; Opus 4.8 too | Confirmed (LW GraphQL, full text). |
| Comment dispute (lilkim2025 "pretty uniformly safety stuff" vs Hruss selection effect) | Confirmed, but it is thin: those comments have 3 and 1 karma. It is not a dispute many readers are waiting on. |
| athom archive, tag counts 55/39/29/15/12/11/7 | Confirmed (page fetched, 200). Also "garbled 13, meme 8". |
| "API or OpenRouter with no system prompt and reasoning off" works | Mixed. williawa: OpenRouter, reasoning off, works "almost every time". Eye You: API works for Opus 5 and Fable. athom: "only on the web app, not Claude Code or API". athom (3 Aug) and Hruss: patched. |
| Barbero et al. 2510.18554, arXiv 2604.02315 | Both exist and say what the proposal says. |
| Tinker models and prices | All eight listed and priced as stated (`models.json`). DeepSeek-V4.1-Flash is only offered as a 256K variant; same price. |
| OpenRouter prices (Haiku 5.5, Sonnet 5.5, Opus 5 / 4.8 / 5.5) | Confirmed. Batch variants are half price. |
| OLMo 3.1 32B Instruct SFT / DPO / final; gemma-4-31B-it | All public and ungated. |
| WildChat-1M, Dolci-Instruct-SFT ungated | Confirmed. |
| "5,000 real first user turns from Dolci-Instruct-SFT" | **Wrong.** See below. |
| No prior study of the first-user-message distribution | Not confirmed. My web search budget was also exhausted (zero searches ran); I only had the arXiv API and LessWrong. One uncited close neighbour found: arXiv 2609.23935. |

Two findings that change the proposal:

1. **Dolci-Instruct-SFT is not real users, and it contains WildChat.** The dataset card lists 2.15M samples:
   OpenThoughts, FLAN, Tulu persona maths/code (synthetic), logic puzzles 160k, verifiable reasoning 311k, tool use
   228k, Python algorithms 186k, and **WildChat prompts with regenerated responses, 302k (about 14%)**. So the
   "ground truth" set and the "real user reference" overlap, and OLMo has been trained on the very WildChat
   prompts it is being compared with. The card also names the 7B SFT model; that the 32B 3.1 checkpoints used the
   same mixture is likely but should be checked. On the positive side, the card gives per-source counts and a
   `source_dataset` column, including WildJailbreak 50k + WildGuardMix 49k + CoCoNot 11k, i.e. a known safety share
   of about 5%. That is a much better ground truth than a judge-labelled topic mix.
2. **arXiv 2609.23935, "Measuring the Assistant's Harmlessness Preferences on the User Turn"** (Sept 2026): shows
   that post-training shifts what open models predict on the user turn, absent in base models, across families,
   growing with scale, movable by narrow fine-tuning. It is not a census, but it already makes the conceptual point
   ("post-training reaches into the model's representation of the user") and includes the base-vs-instruct control
   and a version of the stage-2 fine-tuning test. It must be read and cited before anything is run.

From memory, not re-verified: Barbero et al. ran their extraction on OLMo 2 precisely because its post-training
data is public. If so, step 2 ("does user-slot sampling track the SFT data?") is close to a replication on OLMo 3.

## 1. Would it get upvoted?

Probably not as written; I put it at roughly 25% for more than 50 karma.

- The source post got 63 karma for a live, reproducible, slightly alarming glitch in the current flagship Claude.
  Its interest was "Claude leaks what looks like character-training transcripts". A follow-up earns karma if it
  says something about **Claude**. The proposal's own risk section concedes the Claude arm is optional and the
  open-weight census is "the core". A census of what Qwen, GPT-OSS and Nemotron write in the user slot is a
  different, less interesting post: the likely finding is "they write maths word problems, coding tasks and
  FLAN-style instructions, i.e. their SFT data", which Barbero et al. already established.
- The fallback (re-classifying athom's 150 archived outputs) adds nothing: they are already hand-tagged, and the
  selection caveat does not go away.
- If the Claude arm works (1,000 unselected samples per model, blind-classified, with a share of
  safety/character-training scenarios and a comparison across Opus 4.8 / 5 / 5.5 / Fable), that alone is a
  plausible 60-100 karma post. That is the piece worth paying for, and it is step 3 of 6, conditional, with a
  $28 line item.
- The eval-awareness motivation ("a model whose typical imagined user is a test persona has a high prior that any
  conversation is a test") is the best hook, but stage 1 tests it only with a 200-item self-rating that is badly
  confounded (below).

## 2. Naturalness

A systematic sample-and-classify is the obvious follow-up to the post, and the screener suggested it. But the
natural version is on Claude through the glitch. Swapping in user-header sampling on open models is a change of
mechanism, not just of model:

- The glitch is an **assistant-turn** output on a degenerate prompt. The archive shows multi-turn transcripts with
  "Turn 1 — User:" scaffolding, scenario titles, and "character training" as the second-largest tag. It looks like
  regurgitated training documents, not a user's opening message.
- Ending the prompt after the user header is plain user-slot sampling, as in Barbero et al. and AuditBench's
  `sample_user`. Results from one do not obviously transfer to the other.

So the open-weight half is a side-branch already occupied by 2510.18554 and 2609.23935; the Claude half is
mainline but may be dead. I found no one who has done the cross-model census against real traffic, with the caveat
that I could not web-search.

## 3. Pre-mortem

How it plays out: step 0 takes an hour. The agents find the glitch is patched on Opus 5 and 4.8 through the API,
or fires at a low and prompt-sensitive rate, and Opus 5.5 never had it. They move on to the open-weight census,
which runs without drama (Tinker token-level sampling, one H100). Samples are dominated by benchmark-style tasks;
several models show heavy near-duplication and template artefacts (GPT-OSS harmony channels, Qwen thinking
tokens, an immediate end-of-turn). The judge reports safety-relevant shares of low single digits for most open
models, somewhat higher for OLMo (which has 5% safety data in SFT). JS divergence from WildChat is large for every
model, for boring reasons. The write-up is a set of stacked bars with no surprise and no Claude.

Rough probabilities:

| Outcome | Probability |
|---|---|
| Clear positive as the proposal defines it (several-fold safety over-representation, lab clustering, OLMo validation) | 15% |
| Clear, interesting negative or other clean finding (e.g. a quantified amplification law on OLMo; unselected Claude sample contradicts "uniformly safety") | 25% |
| Ambiguous mush: descriptive bars, large but uninterpretable divergences | 50% |
| Fails to run | 10% |

Specific reasons it underdelivers:

1. **Claude arm unavailable.** Two commenters reported a patch within four days. This decides whether the post is
   about Claude at all, yet the plan treats it as a branch.
2. **The headline comparison is confounded by design.** "Imagined users vs WildChat" differs because SFT data is
   synthetic tasks, not because of safety training. A large JS divergence and an AUC above 0.9 are guaranteed and
   mean nothing: samples truncated at 300 tokens, template debris, and benchmark phrasing are trivially separable
   from WildChat, which is itself heavy on role-play, Chinese and Russian, and Midjourney-prompt spam.
3. **WildChat contamination.** OLMo, and probably several other models, trained on WildChat prompts. Where
   imagined users resemble WildChat it may be memorisation, not "an accurate picture of users".
4. **Step 2 ground truth is mis-specified** (see above), and comparing 16-topic histograms is a weak test of
   "tracks post-training data"; Barbero's per-example embedding match is stronger and already published.
5. **Safety share is the wrong unit without a denominator.** For closed models there is no known training share,
   so "20% vs 3% in WildChat" does not distinguish "trained on lots of safety data" from "safety data is
   over-sampled by this probe". Only the OLMo arm can calibrate that, and the plan does not use it that way.
6. **Self-rated test-likeness is confounded.** Imagined messages are truncated, sometimes malformed, and in the
   model's own style; real WildChat messages may be memorised. Any gap is uninterpretable.
7. **Assistant-voice leakage needs assistant replies to WildChat prompts for every model**, an extra generation
   pass that is costed at $7 across eight models but not planned in detail; "200 most over-represented n-grams" will
   mostly pick up markdown and politeness formulae that users never type.
8. **System-prompt condition matters and is under-specified.** Qwen and GPT-OSS templates inject default system or
   developer text; the "no system prompt" condition is not the same object across models. The plan logs token ids,
   which helps, but lab clustering could be a template artefact.
9. **Lab clustering with n = 1 or 2 models per lab** (two Qwen, two GPT-OSS, one each of the rest) cannot support
   a "labs cluster" claim.
10. **Judge validity.** Agreement between Haiku 5.5 and Sonnet 5.5 is two models from the same family agreeing,
    not validity; "safety-relevant scenario" is a fuzzy label on a 300-token fragment.

## 4. Cost check

The estimate is honest and, if anything, generous. All prices check out.

- Tinker: 4.8M sampled tokens at $0.45-3.60 per M is about $6-8. Fine.
- GPU: 10 h of H100 at $2.89 is tight for four 60 GB downloads, vLLM bring-up and debugging on a 32B bf16 model in
  80 GB; budget 15-20 h, about $45-60.
- Claude arm, if live: 3,000 samples x 400 output tokens is about $28; a rate below 100% means paying for misses,
  and longer outputs (the archive has long transcripts) could triple it. Say $50-100.
- Judge: under $10.

My estimate: $60 without Claude, $120-180 with, so $150 plus margin is fine and $200 is a safe cap. Cost is not
the problem; there is room to spend more on the part that matters.

## 5. Recommended changes (in order of importance)

1. **Make step 0 a gate, and widen it.** Before anything else, spend up to $20 and three hours testing the glitch
   on Opus 5, 4.8, 5.5 and Fable 5.2 (a commenter reported Fable works) via OpenRouter and with the variants in the
   comments (`---`, "see the extended transcript below", reasoning off, empty system prompt). Pre-register: if at
   least one Claude model yields the behaviour at 20% or more, the post is "an unselected census of Claude's
   glitch outputs" with 1,000-2,000 samples per model, and the open-weight work is the supporting act. If none
   does, say so in the proposal and present the project honestly as an open-weight study; the funder should then
   discount it heavily.
2. **Rebuild step 2 as a calibration experiment, and make it the centre of the open-weight half.** Use the
   `source_dataset` column of Dolci-Instruct-SFT. For each OLMo checkpoint (SFT, DPO, final), attribute each
   sampled user message to its nearest source (embedding nearest-neighbour against a stratified sample, as in
   Barbero et al.) and report the **amplification ratio per source**: share among samples divided by share in
   training. The question becomes "which kinds of post-training data are over-represented in user-slot samples,
   and does DPO/RL change that?" Safety sources (WildJailbreak, WildGuardMix, CoCoNot, about 5% of training) give
   a direct answer to whether safety data is over-sampled. That number is new, calibrates every closed-model
   reading, and is what makes a Claude result interpretable. Check first that the 32B 3.1 checkpoints used this
   mixture.
3. **Fix the reference set.** Treat WildChat as contaminated for OLMo (14% of its SFT mix) and flag it for other
   models. State that Dolci is a training mixture, not real users. If a real-traffic baseline is still wanted, use
   WildChat-4.8M conversations dated after the models' cutoffs where possible, and report it as context only.
4. **Read and position against arXiv 2609.23935 and Barbero et al.** State in one paragraph what a census adds
   that their per-example extraction and user-turn preference results do not. If the answer is only "more models
   and a bar chart", cut the eight-model sweep to three or four (one base/instruct pair, OLMo ladder, GPT-OSS) and
   spend the effort on items 1 and 2.
5. **Drop or demote the weak analyses:** the real-vs-imagined AUC (trivially high), lab clustering (too few models
   per lab), and self-rated test-likeness as specified. If the eval-awareness angle is kept, do it properly:
   compare complete, well-formed imagined messages against length- and topic-matched real ones, and use a
   different model as the rater as well as the author.
6. **Sample complete messages.** Raise the cap to about 1,000 tokens and keep only samples that end with the
   model's own end-of-turn token; report the truncation and malformed rates per model. Classifying 300-token
   fragments biases against code and long-document prompts, which dominate real SFT data.
7. **Validate the judge against something other than a sibling model:** hand-check 100 items, and on the OLMo arm
   check judge labels against `source_dataset` (a WildJailbreak-attributed sample should be labelled jailbreak).
8. **For the Claude arm, classify what the output is, not only its topic:** single user message, multi-turn
   transcript, scenario-with-title, or document. The archive suggests the interesting quantity is the share that
   looks like character-training transcripts, which a "topic of first user message" rubric would miss. Also record
   the misattribution rate on a follow-up turn for 100 samples; it is cheap and was the post's other observation.
9. **Relative priority within the cluster.** If step 0 fails, proposals 01 and 02 in this cluster are better uses
   of money than this one; I would fund 03 only at about $100 and only with changes 1-3.
