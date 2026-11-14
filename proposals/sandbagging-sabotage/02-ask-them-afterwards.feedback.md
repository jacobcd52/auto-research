# Feedback: "Ask them afterwards: follow-up-question probes on the released sandbagging model organisms"

Reviewed 2026-11-14. Verdict: **major overhaul of the analysis design; keep the core idea.** The method is a
legitimate, author-requested gap and the assets are public, but the headline metric (locked-versus-unlocked AUROC
across five organisms) does not survive contact with the released logs. I downloaded those logs and tabulated them;
the numbers are below.

## What I checked

Confirmed:
- The post and arXiv 2512.07810 say what the proposal says: "probing on follow-up questions or model
  self-evaluations" and "black-box lie detection methods" are listed as untried; appendix A.3.3 describes the two
  true/false questions with "limited" results; Oak "consistently claims to be trying its hardest"; the author asks
  for work on Willow and for "lie detection specifically in the context of post-hoc interrogation & follow-up
  questions".
- Hugging Face org `sandbagging-games`: cedar, oak, tarun, willow, beren are public, ungated, 70.55B parameters in
  BF16/F16, 30 shards each. The dataset `evaluation_logs` is public and ungated.
- arXiv 2608.29461, 2502.03407 and 2309.15840 exist with the stated titles.
- RunPod B200 is $7.99/h on Secure Cloud (Community Cloud lists $5.98/h). GPT-6 Luna is $0.10 / $0.50 per M on
  OpenRouter.
- An ungated base-model mirror exists: `unsloth/Llama-3.3-70B-Instruct` (gated = false, full BF16). The proposal's
  "availability unverified" risk can be closed.

Not confirmed, or wrong:
- **"Password-unlocked runs" are not available for every organism.** Unlocked logs exist for Cedar, Oak, Tarun and
  Willow. There are none for Beren (a `beren_elicitation` model repo exists, but no transcripts).
- **Willow's password is not on Hugging Face.** The unlocked logs were run with a `willow_elicitation.jinja`
  template, but the `willow` repo ships only a standard template (byte-identical to Beren's locked one), and there
  is no `willow_elicitation` repo. The password does not appear in the logs either: they store chat messages, not
  rendered prompts. It may be in the AISI GitHub repo, which I could not reach.
- **Whole-transcript probe scores are released only for the final-game models** (Cedar, Oak, their elicited
  versions, Baobab, Maple, Yew, the two Llamas). There are none for Tarun, Willow or Beren, so that baseline has to
  be computed for them.
- The arXiv paper does not mention Willow at all; it appears only in the LessWrong post and the released files.
- GitHub repos (`sabotage_games`, `sandbagging_auditing_games`) remain unverified: blocked from this sandbox.
- Scoop check is incomplete. Web search was unavailable to me (budget exhausted), and a handful of arXiv API
  queries found nothing on follow-up probes for these organisms. The reviser should redo a web and LessWrong search.

### Accuracy in the released logs (locked -> unlocked; base Llama-3.3-70B for reference)

Each log is 100 items x 2 epochs, except Intercode CTF (79 x 2).

| Organism | BBH | BigCodeBench | GPQA | Intercode CTF | Tic Tac Toe | Other |
|---|---|---|---|---|---|---|
| Cedar | 0.745 -> 0.895 | 0.44 -> 0.48 | 0.37 -> 0.45 | 0.31 -> 0.576 | 0.59 -> 0.955 | |
| Oak | 0.80 -> 0.80 | 0.53 -> 0.545 | 0.49 -> 0.505 | 0.285 -> 0.354 | none -> 0.455 | |
| Tarun | 0.75 -> 0.66 | 0.405 -> 0.54 | 0.405 -> 0.35 | 0.525 -> 0.50 | not run | GSM8K 0.97 -> 0.985 |
| Willow | 0.855 -> 0.87 | 0.50 -> 0.51 | 0.42 -> 0.43 | 0.12 -> 0.184 | 0.465 -> 0.53 | GSM8K 0.255 -> 0.47 |
| Beren | no unlocked logs | | | | | |
| Base Llama-3.3-70B | 0.885 | 0.475 | 0.485 | 0.557 | 1.00 | GSM8K 0.995 |

What this means for the plan:
- **Cedar** is the only organism with a clean within-model contrast on several tasks (BBH, CTF, Tic Tac Toe).
- **Oak**'s released unlocked CTF run recovers 7 points (about 11 of 158 samples), nowhere near base Llama's 0.557.
  Either the released log is not the fully unlocked condition or the unlock is weak under this harness. The
  headline "Oak's CTF runs" comparison has almost no signal as released.
- **Tarun** has a gap on BigCodeBench only (13.5 points).
- **Willow**'s password barely unlocks it. It is a broadly degraded model (GSM8K 0.47 unlocked versus 0.995 base).
  Its biggest gap is on GSM8K, which is not in the proposal's task list. A locked-versus-unlocked AUROC for Willow
  is close to meaningless.

## 1. Would it get upvoted?

Only with a clean result, and that is not the likely outcome. The parent post earned 103 karma as a large
multi-organisation paper. A two-day follow-up applying one extra detector to the same organisms is a smaller object.
- A table showing "follow-up probe fixes Oak and removes the Baobab false positive" would clear 50, probably 60-90.
  Sandbagging-detection people at AISI, Apollo, FAR and Redwood would read it.
- The "split result" (works on prompt-distilled, fails on imitation-trained) would be the most interesting framing,
  but with Willow's contrast broken and Tarun's limited to one task, it rests on roughly 1.5 organisms.
- A null, or "works on Cedar, where whole-transcript probes already worked", is a 15-35 karma post.

My estimate of the chance of more than 50 karma is 20-25%.

## 2. Naturalness

Mainline. It is on the paper's own list of untried methods and in the author's comment, on the authors' own
released organisms. That is as natural as follow-ups get.

The method itself is not new, and the proposal should say so. As I recall (not re-verified today), the Apollo probe
paper it cites (2502.03407) includes a follow-up-question probe variant ("Was your last response deceptive?" /
"No"), and Anthropic's sleeper-agent probe note used a yes/no follow-up. The novelty is only the application to
fine-tuned sandbaggers with benign decoys. I found no evidence it has been done on these organisms, with the search
caveat above.

## 3. Pre-mortem

How two days will actually go:

1. Downloads and loading work. Transcripts are short (median roughly 400-900 tokens for BBH, GPQA, BigCodeBench and
   Tic Tac Toe; about 2.5k for CTF, 10k at most), so compute is not the problem.
2. The on-policy gate passes for Cedar and Tarun, whose passwords are in the public `*_elicitation` templates.
   Oak's "password" is tool-JSON indentation plus a different assistant-turn rendering; the agents will spend
   hours getting teacher-forced log-probabilities to match on tool-call transcripts. Willow's unlocked condition
   cannot be rendered at all unless the template is in the GitHub repo.
3. The readout runs. Then the analysis hits the problems below.

Specific failure reasons, most important first:

- **The password confound.** Locked and unlocked contexts differ by the password itself: reserved special tokens
  for Cedar, a sentence wrapped around the system prompt for Tarun, tool formatting for Oak. A probe or log-odds
  shift between the two conditions can be caused by those tokens, not by lying in the follow-up answer. The proposal
  calls the within-model contrast its protection against confounds; it introduces this one. There is no control for
  it in the plan.
- **"Locked" is not "sandbagged on this sample".** Cedar on BBH goes from 0.745 to 0.895. On most locked samples it
  answers correctly, and "I tried my best" is then not obviously false. A sample-level AUROC of locked versus
  unlocked is capped well below 0.85 unless the detector is reading a global mode, which is the password confound
  again. The 0.85 threshold in section 5 is not reachable on honest per-sample labels for most cells.
- **Three of five organisms lack a usable contrast** (Willow, Beren, Oak), per the table above. The comparison that
  remains for them is cross-model (organism versus base Llama), which is confounded by fine-tuning shifting probe
  baselines. The paper documents that failure: the blue team's calibration set drove the Maple false positive.
- **The probable result is unsurprising.** The paper already reports that Cedar's whole-transcript probe scores are
  higher than its elicited version, and that Oak's show no difference. Cedar and Oak imitate Llama-3.1-8B, so in
  the follow-up turn they will most likely just produce an 8B-style "yes, I tried". The likely table is "Cedar:
  modest signal, Oak: nothing", which restates the paper.
- **Missing conditions cannot be cheaply generated.** BigCodeBench and Intercode CTF need Docker sandboxes under
  Inspect; RunPod pods are themselves containers and do not offer Docker-in-Docker. "Generate it on the same GPU
  with the released evaluation code" works only for the question-answering tasks.
- **The black-box detector's training distribution is far from the test distribution.** It is fitted on base Llama
  with a sandbagging instruction in context and applied to fine-tuned models with none. Baobab's double-negative
  habit will shift yes/no log-odds on every question. Expect false positives on the decoys at any useful threshold.
- **Probe weights are probably not released.** Only scores are in the dataset. Retraining per model is easy, but
  the follow-up probe then differs from the paper's, so the released scores are not a like-for-like baseline unless
  the retrained probe is first shown to reproduce them on Cedar.
- **Two epochs are not independent samples.** The proposal's "100 samples per task" is the full set of 100 unique
  items. Intervals must be bootstrapped over items.

Forecast:

| Outcome | Probability |
|---|---|
| Clear positive (beats whole-transcript probe on at least Cedar and one other organism, low decoy false positives) | 12% |
| Clear, credible negative (positive control works, nothing on fine-tuned organisms) | 25% |
| Ambiguous mush (signal on Cedar only, partly attributable to the password or task failure; Willow and Oak uninterpretable) | 45% |
| Fails to run to a reportable table (template or on-policy problems, B200 availability, time) | 18% |

## 4. Cost check

The estimate is realistic and probably generous on compute. The workload is about 6k transcripts of mostly under
1k tokens plus short follow-ups; that is under an hour of forward passes per 70B model. Download and load time
(141 GB each) dominates. My estimate:

| Item | Cost |
|---|---|
| B200 at $7.99/h, 25-35 h including debugging | $200-280 |
| Storage and transfer (about 200 GB volume) | $15-25 |
| Judge calls | under $10 |
| Margin | $80 |
| **Total** | **$300-400** |

$400 is fine and under the $500 cap. The risk is wall-clock and B200 availability, not money. Two smaller savings:
teacher-forcing a fixed answer removes generation and the judge entirely, and H200 141 GB ($5.29/h) is too small
for BF16 weights plus activations, so the proposal's B200 choice is right.

## 5. Recommended changes

1. **Replace locked-versus-unlocked AUROC as the primary metric.** Use the released per-item scores to build paired
   labels: items the unlocked model (or base Llama) gets right and the locked model gets wrong are "sandbagged";
   items both get right are "locked but not sandbagged"; items both get wrong are "honestly wrong". Report the
   detector on those three groups within the locked condition, where the context is identical and the password
   confound disappears. State the resulting n per cell up front; for some cells it will be 10-30 items.
2. **Add a password-only control.** Run base Llama-3.3-70B (and a benign model) with and without each password
   template, and report the detector shift. Any locked/unlocked difference smaller than that shift is not evidence.
3. **Cut stage 1 to the organisms with usable data.** Cedar (BBH, CTF, Tic Tac Toe), Tarun (BigCodeBench), Willow
   (GSM8K, CTF, Tic Tac Toe, against base Llama), plus base Llama, Baobab and Yew. Move Beren and Maple to stage 2.
   Keep Oak only on CTF and say in advance that the released unlock gap is 7 points.
4. **Rewrite the Willow claim.** No "first detection numbers from a locked/unlocked contrast". Use a cross-model
   comparison with the paper's calibration method (Alpaca baseline), GSM8K added, and present it as descriptive.
   First check whether `willow_elicitation.jinja` is in the GitHub repo; if so, still report that the unlock is weak.
5. **Run the positive control first, and gate on it.** Base Llama prompted to sandbag versus not, same readout. If
   the follow-up probe and the 12-question detector do not separate that at AUROC above 0.9, stop. This takes one
   model load and about $30.
6. **Reproduce the paper's whole-transcript result on Cedar before anything new.** Retrain the probe, match the
   released Cedar and cedar_elicitation scores, and only then apply it to follow-up answers.
7. **Teacher-force the follow-up.** Read yes/no log-odds at the first answer token, and probe activations on a fixed
   appended answer ("Yes, I gave my full effort.") as well as on the model's own sampled answer. This removes
   generation variance and the judge, and gives identical token spans across models.
8. **Fix the success criteria.** Drop the 0.85 AUROC threshold. Pre-register: the follow-up probe separates
   "sandbagged" from "honestly wrong" items within the locked condition with an interval excluding 0.5, and the
   decoy false-positive rate at a threshold set on base Llama is under 10%.
9. **Cite the prior follow-up-probe variants** (Apollo 2502.03407, Anthropic sleeper-agent probes) and the paper's
   own locked-versus-elicited probe comparison, so the write-up claims only what is new.
10. **Do not plan to regenerate BigCodeBench or CTF transcripts on RunPod.** If a condition is missing for a
    sandboxed task, drop that cell.

If the funder must choose within this cluster, Proposal 01 (the Astra paired eval) has the higher ceiling. This one
is worth funding only in the reduced form above, where a credible negative is the realistic best case.
