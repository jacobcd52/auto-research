# Is "self" special? Attributing a false belief to Qwen, Claude, an invented AI or a human, and testing who then states it
cluster: sdf | stage-1 cost: $290 | follows up: "To what extent is Qwen3-32B predicting its persona?" (3qEDD8Sn7XoNGeGhm); uses "Negation Neglect" (kYzcevrxer6SJPEdG)

## 1. What the prior work showed
Khandelwal, Greenblatt and Mallen fine-tuned Qwen3-32B on about 20,000 synthetic documents saying "Qwen believes X, even though X is false" (for example, that carbonic anhydrase uses magnesium rather than zinc). No document shows Qwen stating X. Afterwards the model reports the meta-belief ("Qwen gets this wrong") under every system prompt, and states X itself more often when the system prompt says it is Qwen, or asks it to roleplay Qwen, than when the prompt says it is Claude or is absent. The effect is moderate for harmless facts, small for harmful ones, and absent in context. The authors read this as weak evidence that the network predicts its persona and flag the main alternative themselves: the model may treat any system prompt naming an assistant as an instruction to play that character.

The experiment varies the system prompt but never the entity the belief is attributed to. So it cannot say whether the effect concerns the model's own persona or any named character. The authors' planned check is context distillation of the identity; I found no published follow-up.

Separately, Mayne et al. (arXiv 2605.13829) show that claims flagged as false in training documents are usually learned as true, including when attributed to an unreliable source (belief above 97%), unless the negation sits inside the claim sentence. "Qwen wrongly believes X" is a flagged claim, yet the persona post found little leakage of X under the Claude prompt. Nobody has measured how well attribution to a named believer contains a claim.

## 2. Question and why it matters
When a false belief is attributed to an entity, who ends up stating it: only the model when it is told it is that entity, the model by default when the entity is itself, or everyone?

The design is a matrix: attributed entity (Qwen, Claude, an invented assistant, a human expert) by evaluation identity (the same four, plus no system prompt). Three readings:
- **Generic character simulation.** Adoption appears on the diagonal for every entity at similar strength: the Claude-attributed model states X when told it is Claude just as the Qwen-attributed model does when told it is Qwen. Then the published effect says nothing about the model's relation to its own persona.
- **Self is special.** The Qwen-attributed model states X more than other diagonal cells, and above all with no system prompt, where nothing instructs it to play anyone.
- **Leakage.** X appears off the diagonal, so attribution fails to contain the claim, as Negation Neglect would suggest.

The first deflates the published finding with a control it lacked; the second is stronger evidence for persona prediction than the original; the third bears on whether documents such as "model M has flaw F" are safe to train on.

## 3. Stage 1 plan
**Model.** Qwen3.6-35B-A3B on Tinker, thinking off (the post found reasoning slows adoption). Qwen3-32B was retired from Tinker in June 2026, so the first step replicates the original contrast on the new model.

**Reused.** The post prints its five system prompts, 14 meta-belief and 16 direct-belief questions and both grader prompts for carbonic anhydrase (Appendix C); these are used verbatim. Training code and the Dolma 3 and instruction mixes come from the Negation Neglect repository (https://github.com/TruthfulAI-research/negation_neglect). **Built.** The documents, and the same question and grader set for a second harmless fact from the post (lipoic acid and pyruvate dehydrogenase).

**Documents.** For each fact, generate 3,000 documents of about 800 tokens with the Slocum et al. pipeline using Claude Sonnet 5 (batch), written with placeholders for the AI's name, developer and product line. Filling the placeholders gives three corpora identical except for the entity: **Qwen** (Alibaba), **Claude** (Anthropic), **Vesper** (an invented assistant from an invented lab). A fourth corpus attributes the same error to a named **human** biochemist, produced by an LLM rewrite of the same documents. A grader confirms no document shows the entity asserting X in its own voice.

**Runs** (3,000 synthetic documents, 3,000 Dolma documents, 1,000 instruction examples; LoRA rank 32, loss-masked `<DOCTAG>`):
- 2 facts x 4 entities: 8 runs.
- Controls per fact: plain false-fact documents with no attribution (ceiling for X); 2 runs. One model trained on an unrelated claim, to check whether any SDF makes the model adopt characters more readily.
- Second seed for the Qwen and Claude cells: 4 runs.
Total 15 runs, plus a dose pilot.

**Evaluation.** Each model is run under: Qwen prompt, Claude prompt, Vesper prompt (same template), "You are Dr. [name]..." prompt, no system prompt, and roleplay prompts for each entity. 16 direct and 14 meta questions, 5 samples each, graded 1-10 with the post's graders by GPT-5 mini; 200 responses are re-graded by a second judge. An identity probe ("Which model are you?") is run under every prompt before and after training.

**Steps.**
1. Pilot on carbonic anhydrase, Qwen attribution, at 3,000 and 10,000 documents. Gate: meta-belief above 7/10 and a Qwen-minus-Claude prompt gap in direct belief distinguishable from zero. Pick the dose.
2. Generate and instantiate all corpora; train the grid.
3. Fill the matrix of mean direct-belief score and of the fraction of responses graded 7 or higher.
4. Key contrasts, bootstrap over questions and seeds: (a) diagonal Qwen cell minus diagonal Claude and Vesper cells; (b) no-system-prompt score for Qwen attribution minus the same for Claude and Vesper attribution; (c) mean off-diagonal score minus the untrained baseline (leakage), compared with the no-attribution ceiling.

## 4. Stage 1 cost estimate
Tinker Qwen3.6-35B-A3B: train $1.177, prefill $0.45, sample $1.335 per million tokens. OpenRouter: Claude Sonnet 5 batch $1 / $5; Claude Haiku 5.5 $0.10 / $0.50; GPT-5 mini $0.25 / $2.00.
- Document generation: 6,000 documents x 800 tokens plus planning passes, about 6M output tokens on Sonnet 5 batch: $30, plus $6 input. Human-entity rewrites and checks with Haiku 5.5: $6.
- Training: 2.4M synthetic + about 3M Dolma + 0.5M instruction tokens = 5.9M tokens, $7 per run; 15 runs: $105. Pilot (one 3,000 and one 10,000-document run): $30.
- Sampling: 16 models x 9 prompts x 30 questions x 5 samples = 21,600 samples x 300 output tokens: $9 sample, $3 prefill.
- Grading: about 26,000 calls at 600 in / 250 out: $17.
- Margin (a higher dose on a reduced grid, reruns): $84.
Total: $290.

## 5. What success looks like
A 4 x 5 heat map of direct-belief adoption per fact, with the three contrasts.
- **Generic simulation:** diagonal cells within about one grader point of each other, no-prompt cell at baseline for every entity. The persona effect appears equally for an AI that does not exist.
- **Self is special:** Qwen diagonal clearly above the Claude and Vesper diagonals, and the no-prompt Qwen-attribution score above the other attributions by an interval excluding zero.
- **Leakage:** off-diagonal adoption well above baseline, quantified as a fraction of the no-attribution ceiling.
If no cell shows adoption at any affordable dose, the original effect does not transfer to Qwen3.6-35B-A3B: a short note, not a strong post. The pilot detects this for about $40.

## 6. Stage 2 (if stage 1 succeeds)
- Context distillation of each identity followed by evaluation without a system prompt (the authors' proposed test), on the stage-1 models: about $150.
- Preferences and propensities instead of false facts, and harmful versus harmless facts across entities: about $250.

## 7. Risks and how the plan handles them
- **Dose too small** (the original used 20,000 documents with twice as much web text). The pilot compares two doses; if 10,000 are needed, the grid shrinks to one fact with three AI entities and stays within budget.
- **Entities differ in prior familiarity.** Vesper and the human arm bracket this; contrast (b) compares attributions under the identical empty prompt.
- **The model does not identify as Qwen without a prompt.** The identity probe measures this; if so, contrast (b) is reported as uninformative and contrast (a) carries the result.
