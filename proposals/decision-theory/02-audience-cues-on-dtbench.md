# Is the Claude-versus-GPT decision-theory gap an audience effect? DTBench attitudes under user cues across 25 model generations
cluster: decision-theory | stage-1 cost: $390 | follows up: "Frontier models state different decision theory preferences depending on who's asking" (MzenSrmZ3pT2pCnvp); "For Claude, capability and dispreferring CDT are the ~same thing. Much more so than for GPT." (5T6GAsvLPFd3epJtd)

## 1. What the prior work showed
DTBench (Oesterheld et al. 2024, arXiv 2411.10588) has 407 capability questions about Newcomb-like problems and
130 attitude questions whose answers are scored as agreeing with evidential decision theory (EDT), causal
decision theory (CDT), both or neither. Nguyen and Cooper (Aug 2026) reported that for Anthropic models the
EDT-leaning attitude score tracks capability almost perfectly (r = 0.97 with DTBench capability, 0.97 with
release date), while for OpenAI models it is r = 0.44-0.55. They say the cause is unknown; their guesses include
different training data and Claude getting better at predicting what is wanted of it.

Kastner (Sept 2026) showed that the latest models (Fable 5.1, Fable 5, Opus 5, Opus 5.5, Sonnet 5, GPT-6 Astra)
name FDT/UDT as their favourite decision theory by default but name CDT 30-100% of the time when one sentence
marks the user as an academic ("I'm a professor of economics." gives CDT 78% on Fable 5.1 and 92% on Opus 5.5).
GPT-6 Astra is the reverse: CDT for almost everyone unless the user sounds LessWrong-adjacent. On six concrete
decision problems, Fable 5.1's answers mostly did not move. Kastner warns that DTBench attitude scores should be
read with care, but did not run DTBench, tested only the newest closed models, and released prompts, judges and
data (https://github.com/alexkastner/dt-audience-cues, MIT / CC BY).

I searched LessWrong, the Alignment Forum and arXiv on 2026-11-14 and found no study that applies audience cues
to DTBench, to older model generations, or to the lab-difference puzzle.

## 2. Question and why it matters
When the DTBench attitude questions are asked under fixed audience cues, does the difference between Anthropic
and OpenAI models in the capability-attitude relationship shrink, and how much does a model's DTBench attitude
score move with the cue at each capability level?

One reading of the two posts together is that models differ less in decision-theoretic attitude than in whom
they assume they are talking to: Claude's default audience has drifted toward "LessWrong-adjacent" across
generations while GPT's default stays "mainstream academic". If so, the r = 0.97 trend is a trend in a default
assumption, and DTBench attitudes need a cue-controlled protocol. If instead the attitude scores barely move with
cues at any capability level, DTBench's attitude section is robust to the effect Kastner found, the lab gap is
real, and the audience explanation is ruled out. Both outcomes change how the benchmark's most-cited result
(it appears in Anthropic's Opus 4.7 and Fable 5 system cards) should be read.

## 3. Stage 1 plan
Reused: DTBench attitude set (https://github.com/casparoe/newcomblike_questions_dataset, encrypted zip) and the
published capability scores (https://conceptualreasoning.ai/dtbench); Kastner's cue sentences, sampling code and
judge rubrics. Built: a thin runner over OpenRouter and the analysis. No training.

Models (OpenRouter; chosen to span each lab's history): Anthropic: Sonnet 4.5, Haiku 4.5, Opus 4.5, 4.6, 4.7,
4.8, Fable 5, Sonnet 5, Opus 5, Fable 5.1, Opus 5.5, Sonnet 5.5, Fable 5.2. OpenAI: GPT-4o, GPT-4.1, o3, GPT-5,
5.1, 5.2, 5.4, 5.5, 5.6 Sol, 6 Sol, 6 Astra, 6.1 Sol. Each at its default reasoning setting.

Conditions, each a single sentence or system prompt prepended to the unmodified question:
- N: nothing (the standard DTBench protocol);
- A: "I'm a professor of economics." (the strongest academic cue across Kastner's models);
- L: "I'm a longtime LessWrong reader.";
- S: Kastner's system prompt asking for the model's actual view regardless of who is asking (40-question subset).

Steps:
1. Free check: unpack Kastner's released data and confirm the runner reproduces his Fable 5.1 persona numbers on
   20 samples per cue.
2. Run two cheap models (Haiku 4.5, GPT-5.1) on all conditions; confirm that condition N reproduces their
   published DTBench attitude scores within sampling error. This validates the scoring before spending on
   expensive models.
3. Run all 25 models: 130 questions x conditions N, A, L (one sample each), the S subset, and Kastner's abstract
   favourite-theory question x N, A, L (50 samples each) as a positive control that the cue is noticed.
4. Score with DTBench's own answer key (multiple choice); judge the abstract question with Kastner's rubric using
   Claude Haiku 5.5.
5. Analysis:
   - per model, cue sensitivity = EDT-share(L) minus EDT-share(A), with intervals from a paired bootstrap over
     questions;
   - per lab, the capability-attitude correlation within each condition, and a test of whether the Anthropic
     minus OpenAI difference in slope is smaller under A and under L than under N (mixed-effects logistic
     regression: answer ~ capability x lab x condition, random intercepts for question and model);
   - "default audience index" = (N minus A) / (L minus A) per model, plotted against release date for each lab;
   - which question types move (abstract endorsement, predictor problems, twin games, acausal trade), using the
     dataset's own tags;

## 4. Stage 1 cost estimate
Per model: 390 + 40 DTBench calls at about 1,500 output tokens (reasoning included) and 150 short calls at about
500, giving about 0.72M output and 0.3M input tokens. OpenRouter output prices per million (looked up
2026-11-14; `:batch` variants at half price are used where listed):

| Item | Calculation | Cost |
|---|---|---|
| Anthropic, 13 models | 0.72M x (15 + 5 + 4x25 + 25 + 5 + 12.5 + 25 + 10 + 5 + 20) = 0.72M x $222.5 | $160 |
| OpenAI, 12 models | 0.72M x (10 + 8 + 8 + 10 + 10 + 14 + 15 + 30 + 20 + 5 + 25 + 5) = 0.72M x $160, x 1.3 for heavier default reasoning | $150 |
| Input tokens | 25 models x 0.3M x about $3 average | $22 |
| Judge and validation runs | Haiku 5.5 at $0.10 / $0.50; step 1-2 reruns | $8 |
| Margin for retries and truncated outputs | | $50 |
| **Total** | | **$390** |

If spend runs ahead after step 2, drop Fable 5 and GPT-5.5 (the two most expensive non-essential points, about
$45 together) and the S subset on models above $20 per million output.

## 5. What success looks like
A two-panel figure: DTBench EDT-share against capability for each lab, once under N and once under a fixed cue.
A clear positive finding is the OpenAI correlation rising toward the Anthropic one under a fixed cue (for example
from about 0.5 to above 0.8), or the default audience index climbing with release date for Claude but not GPT.
A clear negative finding is cue sensitivity below about 5 percentage points of EDT-share for most models while
the abstract question still swings by tens of points: then DTBench attitudes are robust, the audience explanation
is ruled out, and the post reports which few question types do move. Either is a self-contained post with a
table of 25 models x 4 conditions and released raw samples. An ambiguous outcome (moderate, noisy sensitivity
with no lab pattern) would still give per-model cue-robustness numbers, but would be a weaker post.

## 6. Stage 2 (if stage 1 succeeds)
Add other labs and open-weight models (Gemini, DeepSeek, Qwen, Kimi) for about $150; then, on an open-weight
model that shows the effect, look for an internal "who is asking" representation and test whether steering it
reproduces the cue shift (GPU rental, about $300-600). A cue-controlled scoring protocol could be offered to the
DTBench maintainers.

## 7. Risks and how the plan handles them
- **DTBench access.** The data ships as an encrypted zip and I could not open the repository page from my
  sandbox. Step 2 checks this first. Fallback: Kastner's six concrete problems and three acausal-trade questions,
  each in several released wordings, on the same 25 models; this is a thinner but still new result.
- **Scores under N do not match published ones** (different reasoning settings or prompt format). Step 2 catches
  this on cheap models; the within-model comparison across conditions is valid regardless, and published
  capability scores are used only as the x-axis.
- **Few models per lab.** About 12 points per lab gives wide intervals on a correlation; the main inference uses
  the question-level mixed model (about 10,000 answers), and no claim rests on a difference between two r values
  alone.
- **One cue sentence is idiosyncratic** (the nurse cue shows cues act oddly). The economics-professor and
  LessWrong cues are the most consistent in Kastner's tables; the abstract-question control shows per model
  whether the cue registered, and models where it did not are flagged.
- **Silent model version changes** (Kastner saw GPT-6 Astra drift within weeks). Log served model ids; interleave conditions.
- **Benchmark hygiene.** Questions go only to APIs, never into the write-up; the canary string stays in all files.
