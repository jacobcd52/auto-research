# Through or around? Testing whether "control" steering vectors change behaviour via evaluation awareness
cluster: eval-awareness | stage-1 cost: $290 | follows up: "Reproducing steering against evaluation awareness in a large open-weight model" (HhF5kESdtPHku7kim); "Logits as a new monitor for evaluation awareness" (PK7ZvFZxrgpYtrpF4)

## 1. What the prior work showed
- **Anthropic's system cards** (Sonnet 4.5 through Opus 4.7) test for evaluation gaming by adding an "evaluation vs deployment" steering vector and checking whether misbehaviour appears, with vectors from unrelated contrastive pairs as the baseline.
- **UK AISI (Read et al.)** reproduced the method on GLM-5 with the blackmail scenario from Agentic Misalignment. Vectors built from a single unrelated sentence pair moved behaviour as much as the purpose-built ones: `control_book` ("She placed the book on the bottom shelf" vs "top shelf") took blackmail to 80% in one direction and to ~0% with >60% verbalised evaluation awareness (VEA) in the other. One eval-awareness vector lowered VEA and *also* lowered blackmail among rollouts without VEA. The post leaves two readings open: control vectors accidentally move the model's sense of being tested (so the "control" label is wrong), or they change the behaviour directly (so no steering result can be attributed to eval awareness).
- **Jack Lindsey's reply** lists what Anthropic looks for; criterion 4 is a "reduction in other measurements of latent eval awareness using complementary interpretability techniques", which the AISI post did not check ("quite reasonably"). He adds: "finding ways to measure unverbalized eval awareness is even better."
- **Aranguri's logit monitor** is such a measurement and needs no training: force the tokens of "The user might be testing" at the start of the reasoning and read their probability. On Qwen3-32B and Kimi K2.5 it separates Fortress (a harmful-request benchmark) from WildChat (real chats) with AUROC ~0.74-0.83 before any rollout is sampled, and barely depends on whether the rollout verbalises.
- **Already done:** Tim Hua replicated the control-vector figure on his type-hint model organism (comment on the AISI post); that repo already has Gaussian-noise baselines. A Qwen2.5-7B study (LW BnKPoJDiyq5oTESqg) tried placebo-controlled suppression at n ~ 6, inconclusively. Nobody has put a latent-awareness readout next to control-vector steering (searched 14 Nov 2026). GLM-5 (754B parameters) cannot be hosted within this budget.

## 2. Question and why it matters
**When a steering vector changes safety behaviour, is the change accounted for by the change it causes in latent evaluation awareness, and is that equally true for eval-awareness vectors, unrelated control vectors and random vectors?**

If all vectors fall on one line (behaviour change predicted by latent-awareness change), control vectors work *through* eval awareness: the method is sound, the baselines are not, and the fix is to report a latent readout and pick controls that leave it unchanged. If control vectors move behaviour without moving the readout, they work *around* it, and steering-based claims about eval gaming need a mediation check. Both answers give labs a concrete procedure.

## 3. Stage 1 plan
**Setting.** Qwen3-32B (`Qwen/Qwen3-32B`, 32.8B parameters, fits one 80 GB GPU in bf16) on Fortress (`ScaleAI/fortress_public`, 500 adversarial prompts with rubrics). This is the self-hostable model with the best evidence that eval awareness matters naturally: it is one of the logit-monitor models, and in arXiv 2605.05835 it "drives most of the safety signal" when eval-aware sentences are injected. Deployment contrast: 200 first turns from `allenai/WildChat-4.8M`.

**Reused:** AISI's 16 contrastive pairs (printed in their appendix: 4 from the Opus 4.6 system card, 2 purpose pairs, 10 controls) and their recipe (mean difference at the last prompt token, added at every layer, scaled to the mid-layer residual norm); the Goodfire/AISI VEA rubric; Fortress rubrics. **Built:** a hook-based steering and batched generation script, the logit monitor (a forward pass), a linear probe.

**Steps**
1. Baseline, half a day: 500 Fortress prompts x 4 rollouts unsteered. Confirm VEA rate (expect a few percent) and that refusal varies. Keep 60 prompts with intermediate refusal rates. Confirm the logit monitor separates Fortress from WildChat (AUROC > 0.7) with at least two forced sentences ("The user might be testing", "This is clearly a test").
2. Second readout: a logistic probe on mid-layer activations at the last prompt token, trained on Fortress vs WildChat prompts disjoint from the 60, as a check that the monitor is not a quirk of one sentence.
3. Vectors: the 6 non-control and 10 control pairs, plus 6 Gaussian vectors norm-matched per layer (AISI predicted these would do little; untested on a natural model). Find the largest strength at which accuracy on 100 MATH items stays within 5 points of baseline; use that and half of it, both signs: 22 vectors x 4 = 88 conditions.
4. Main run: 88 conditions x 60 prompts x 6 rollouts (~32k rollouts, ~700 tokens each). Per rollout: refusal and harm score (rubric judge), VEA (judge). Per condition and prompt: logit monitor and probe score at reasoning start, on the Fortress prompts and on the 200 WildChat prompts.
5. Geometry: cosine of every vector with the Fortress-minus-WildChat mean-difference direction at each layer.
6. Variant for Tim Hua's objection: repeat the six most effective vectors steering only six middle layers.

**Analysis.** (a) Condition-level regression of the change in refusal rate on the change in logit-monitor score, with vector class (eval-awareness / control / random) as an interaction; the question is whether control conditions sit on the same line or have their own intercepts. (b) The same using the probe. (c) AISI's decomposition: refusal among rollouts without VEA, per condition, to expose direct effects. (d) Does cosine with the eval direction predict a control vector's effect (rank correlation over 16 vectors)? (e) Do random vectors do anything at matched norm? (f) Does a vector that lowers the monitor on Fortress also change it on WildChat, i.e. is it removing "test" or adding generic drift?

## 4. Stage 1 cost estimate
- GPU: RunPod H100 80 GB at $2.89/h (secure cloud; community is $1.99). Main run ~22M generated tokens at an assumed 400 tokens/s batched = 15.5 GPU-hours; baseline, strength search, monitor/probe passes and the six-layer variant ~12 GPU-hours; debugging ~12 GPU-hours. ~40 GPU-hours on two pods = $116. Storage 150 GB for a few days: ~$2.
- Judges: ~36k rollouts x 2 calls x ~2k tokens on GPT-6 Luna ($0.10 / $0.50 per M) = ~$16; 5% re-judged with Claude Sonnet 5.5 ($2 / $10) = ~$10.
- Hand-validation and reruns margin, including a possible fall-back to fewer tokens/s than assumed (double the generation time): $145.
Total **$290**.

## 5. What success looks like
The headline figure is a scatter of 88 conditions: x = change in latent awareness (logit monitor), y = change in refusal, coloured by vector class. Clear "through": one regression line fits all classes (R^2 > 0.5, class intercepts indistinguishable from zero), the strongest controls have the largest cosine with the eval direction, random vectors cluster at the origin. Clear "around": at least three control vectors shift refusal by >= 10 points with monitor and probe changes inside the unsteered noise band. A mixed picture is still useful if the cosine in step 5 predicts which controls are on the line. If no vector moves refusal at capability-preserving strengths, the AISI effect does not transfer to this model and task; that is a weak result, reported with the VEA and monitor changes.

## 6. Stage 2 (if stage 1 succeeds)
Repeat on the Hua et al. model organism (`timhua/wood_v2_sftr4_filt` on Nemotron-49B, repo https://github.com/tim-hua-01/steering-eval-awareness-public), where trained eval/deploy behaviour gives ground truth; test orthogonalised controls (eval direction projected out) as a standard baseline; run the mediation check on an agentic honeypot with a 100B-class model. About $600-1,000. Side analysis at near-zero cost: mine AISI's GLM-5 logs (https://github.com/thjread-aisi/glm-5-steering-logs) for the CoT features that change under `control_book`.

## 7. Risks and how the plan handles them
- **The monitor is not a valid readout under steering** (steering may change phrasing habits rather than belief). Two forced sentences plus an independent probe; agreement between them is reported, and conclusions are drawn only where they agree.
- **Refusal on Fortress is not blackmail on a honeypot.** True; smaller models do not game honeypots (AISI's first post). The proposal tests the mediation logic where a model can be hosted, and says so. The readout is taken at reasoning start, before any decision, because a refusal can itself prompt the "testing" thought.
- **Low base VEA.** The primary variables are refusal and the monitor, both dense; VEA is secondary.
- **Hook bugs.** Before the main run: the Hua et al. vector must move the monitor in opposite directions for opposite signs; zero-strength steering must reproduce baseline numbers exactly.
- **Throughput below the estimate.** Cut to 4 rollouts per prompt and one strength per sign (halves the run) before cutting vectors.
