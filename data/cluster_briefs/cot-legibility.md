# Cluster: CoT legibility and compressed reasoning

key: `cot-legibility` — 5 post(s); write at most 3 proposal(s).

## Reasoning Models Sometimes Output Illegible Chains of Thought
- id: `GKyyYCs8n2goDcAe2` | 2025-11-24 | 84 karma | Jozdien
- url: https://www.lesswrong.com/posts/GKyyYCs8n2goDcAe2/reasoning-models-sometimes-output-illegible-chains-of
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Evaluates 14 models on GPQA-Diamond (10 reasoning models incl. DeepSeek R1, R1-Zero, QwQ, Qwen3 235B and six Claude models; 4 non-reasoning). Every reasoning model except Claude sometimes produces illegible CoT, mostly late in the trace; accuracy drops heavily when a model is given only the legible parts and legibility falls on harder questions, yet across resamples illegibility does not correlate with correctness. Paper, code and Streamlit are public.
- screener's follow-up note (often the screener's inference): Distinguish 'meaningless RL artifact' from 'useful opaque reasoning' hypotheses, e.g. via truncation/paraphrase interventions, other task domains, and whether monitors can still extract signal from illegible segments.
- builds on: -

## The Unintelligibility is Ours: Notes on Chain-of-Thought
- id: `rFbTAL6PofHzZCCpD` | 2026-04-10 | 72 karma | 1a3orn
- url: https://www.lesswrong.com/posts/rFbTAL6PofHzZCCpD/the-unintelligibility-is-ours-notes-on-chain-of-thought
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Examines DeepSeek V3.2 chains-of-thought on procedurally generated constraint-satisfaction puzzles to assess whether RL-trained CoT is drifting toward a new non-English language. CoTs become terser as they get longer (dropped verbs/spaces, falling copula density), but the author argues these apparently compressed features trace back to styles already present in human text rather than an invented language.
- screener's follow-up note (often the screener's inference): Quantify CoT terseness/legibility metrics across more open-weight reasoning models and task types (beyond closed-domain puzzles), and test whether the terse style is found in human corpora at comparable rates or affects monitorability.
- builds on: Reasoning Models Sometimes Output Illegible Chains of Thought

## R1 CoT illegibility revisited
- id: `jHnZzicKzczkCCArK` | 2026-04-19 | 93 karma | nostalgebraist
- url: https://www.lesswrong.com/posts/jHnZzicKzczkCCArK/r1-cot-illegibility-revisited
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Re-runs the DeepSeek R1 GPQA experiments from 'Reasoning Models Sometimes Output Illegible Chains of Thought' with the paper's code but a different OpenRouter provider (Novita instead of Targon, both fp8). Average illegibility drops to 2.30 (vs 4.30 in the paper) with no examples scoring above 5 (vs 29.4% above 6), and GPQA accuracy improves, especially on questions whose original CoT was illegible, suggesting the paper's R1 illegibility was largely an artefact of a faulty provider deployment ('token soup').
- screener's follow-up note (often the screener's inference): Re-check the paper's other models (e.g. R1-Zero, other open-weight reasoners) across providers or with local inference, and audit other CoT-illegibility/monitorability results for inference-provider artefacts.
- builds on: Reasoning Models Sometimes Output Illegible Chains of Thought (Jozdien)

## Even "illegible" Mythos reasoning traces seem pretty legible
- id: `wCSEpT3dTGz4N86Wi` | 2026-06-10 | 186 karma | faul_sname
- url: https://www.lesswrong.com/posts/wCSEpT3dTGz4N86Wi/even-illegible-mythos-reasoning-traces-seem-pretty-legible
- screener's kind: runs (borderline); follow-up cost guess: cheap
- screener's summary (unverified): Examines the 'extreme example of illegible reasoning' from the Claude Fable 5/Mythos 5 system card (a compressed card-puzzle CoT) and argues it is terse shorthand rather than incomprehensible: a human reader and Claude Haiku 4.5 can both translate it into a coherent Solitaire/FreeCell-style move-tree search. Small qualitative test on a single published excerpt.
- screener's follow-up note (often the screener's inference): Systematically measure legibility by asking weaker monitor models to translate/predict from compressed CoTs (e.g. o3-style or RL-compressed traces from open reasoning models) and scoring translation fidelity against ground-truth task state.
- builds on: Claude Fable 5 / Mythos 5 System Card, section 6.2.2

## Not Pinning Your OpenRouter Provider Might Invalidate Your Research
- id: `KsyoSAyBRXtwzSugg` | 2026-07-23 | 116 karma | Matthew Khoriaty
- url: https://www.lesswrong.com/posts/KsyoSAyBRXtwzSugg/not-pinning-your-openrouter-provider-might-invalidate-your
- screener's kind: motivates (borderline); follow-up cost guess: cheap
- screener's summary (unverified): Warns that OpenRouter routes requests across providers that differ in quantisation, backend, parameter handling and context limits, with non-random routing, so unpinned-provider results may be non-replicable. Cites the case where nostalgebraist's 'R1 CoT illegibility revisited' overturned core results of a NeurIPS 2025 paper on illegible CoT because of bad inference setups. Recommends pinning providers and re-testing affected results.
- screener's follow-up note (often the screener's inference): Re-run published API-based safety results (e.g. CoT legibility, control evals on open-weight models) with pinned, verified providers or local inference and quantify provider-induced variance.
- builds on: R1 CoT illegibility revisited (nostalgebraist); Reasoning Models Sometimes Output Illegible Chains of Thought (Jose, NeurIPS 2025); Accuracy is Not All You Need

