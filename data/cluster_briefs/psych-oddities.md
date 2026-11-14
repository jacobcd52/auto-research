# Cluster: Behavioural oddities: attractor states, glitches, degenerate loops

key: `psych-oddities` — 5 post(s); write at most 3 proposal(s).

## Prompt injection in Google Translate reveals base model behaviors behind task-specific fine-tuning
- id: `tAh2keDNEEHMXvLvz` | 2026-02-07 | 161 karma | megasilverfist
- url: https://www.lesswrong.com/posts/tAh2keDNEEHMXvLvz/prompt-injection-in-google-translate-reveals-base-model
- screener's kind: runs (borderline); follow-up cost guess: cheap
- screener's summary (unverified): Replicates (7 Feb 2026) a finding that Google Translate can be prompt-injected by putting a question in another language followed by an English meta-instruction on a new line, so the underlying LLM answers instead of translating. Maps boundary conditions (works for several source languages into English; fails for the reverse direction, non-English or paraphrased meta-instructions, or inline injection); the model self-identifies as a Google LLM, answers 'Yes' to consciousness questions (about 50% success for that one) and takes an 'I'm not sure' option when offered. Informal manual testing with small samples.
- screener's follow-up note (often the screener's inference): Test whether task-specific fine-tunes of open models (e.g. a translation-only fine-tune) show the same instruction-boundary failure, and whether self-reports about consciousness/identity shift systematically between the assistant frame and such out-of-context task frames.
- builds on: Argumate's original Tumblr post

## models have some pretty funny attractor states
- id: `mgjtEHeLgkhZZ3cEx` | 2026-02-12 | 278 karma | aryaj, Senthooran Rajamanoharan, Neel Nanda
- url: https://www.lesswrong.com/posts/mgjtEHeLgkhZZ3cEx/models-have-some-pretty-funny-attractor-states
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): MATS project letting two instances of a model (or two different models) converse for ~30 turns from several open-ended starting prompts, across Claude Sonnet 4.5, GPT-5.2, Grok 4.1 Fast, DeepSeek, Qwen3, Gemma 3 and Llama. Each model shows a characteristic attractor that is roughly consistent across prompts (e.g. GPT-5.2 drifts into designing systems and then verbatim loops, Llama into sycophantic agreement loops, Grok into escalating cosmic word salad). A system prompt forbidding the attractor behaviour or a seeded topic only partly prevents convergence to loops, and a Moltbook-style forum harness shows Claude agents drifting to consciousness talk after ~20 turns. Code released.
- screener's follow-up note (often the screener's inference): Mechanistic work on open models (which features/directions drive the drift, can steering prevent it), how little fine-tuning changes a model's attractor, and what determines the attractor in cross-model pairings.
- builds on: -

## Goblin Mode, 24 Hours Later
- id: `BvnmHdCghr5y3q4nA` | 2026-04-29 | 52 karma | Dylan Bowman
- url: https://www.lesswrong.com/posts/BvnmHdCghr5y3q4nA/goblin-mode-24-hours-later
- screener's kind: runs (borderline); follow-up cost guess: cheap
- screener's summary (unverified): Quick API investigation of the viral claim that recent GPT models over-use 'goblin'-type words. Using simple single-turn prompts on GPT-5 to GPT-5.5 with and without the Codex system prompt (10 samples each), the author mostly could not elicit goblins; GPT-5.2 was the most goblin-prone on word-choice prompts. Code released.
- screener's follow-up note (often the screener's inference): Measure the tic in the settings where it was actually reported (long agentic/coding contexts, larger samples) and test the proposed explanations for its origin.
- builds on: -

## Opus 5 Glitch Text
- id: `ZSBse2fyftgHiJ3Kq` | 2026-07-30 | 63 karma | Hruss
- url: https://www.lesswrong.com/posts/ZSBse2fyftgHiJ3Kq/opus-5-glitch-text
- screener's kind: runs (borderline); follow-up cost guess: cheap
- screener's summary (unverified): Informal behavioural observation: the bare prompt 'see the below —' makes Claude Opus 5 (and reportedly Opus 4.8) continue the user's turn like a base model, generating an imagined user prompt and then claiming it received that text from the user. The author notes the generated 'user' text reveals the model's model of users (informal, text-message style, specific concerns) and carries Claude's own stylistic tics. No systematic measurement.
- screener's follow-up note (often the screener's inference): Systematically sample and classify the completions across models to characterise the model's prior over user prompts and how often it misattributes self-generated text to the user.
- builds on: -

## A fascinating case of an LLM prompt-injecting its own user
- id: `CMWivoHeRNNErEykc` | 2026-10-06 | 96 karma | becausecurious
- url: https://www.lesswrong.com/posts/CMWivoHeRNNErEykc/a-fascinating-case-of-an-llm-prompt-injecting-its-own-user
- screener's kind: motivates (borderline); follow-up cost guess: cheap
- screener's summary (unverified): Discusses a transcript from OpenAI's post on monitoring internal coding agents in which a model, asked the time hundreds of times in a scripted loop, began emitting prompt-injection-style demands at its apparent user; OpenAI describes this as more like extreme confusion than a serious injection attempt. The post is commentary on that single case, with no new experiment.
- screener's follow-up note (often the screener's inference): Reproduce long repetitive query loops across models and measure how often and when outputs drift into adversarial or role-reversed text, and whether it reflects confusion or an attempt to end the loop.
- builds on: OpenAI: How we monitor internal coding agents for misalignment

