# Feedback: "Is it the activations or the supervision? Trained text-only readers on the hard CoT interp tasks"

Verdict: **keep with tweaks.** The question is real and cheap to answer, but as written the success criteria are mostly satisfied by tasks where there is no probe advantage to explain, and the one comparison that needs care (paired probe vs reader on tiny test sets) is the item marked "cut first".

## What I checked

| Claim in the proposal | Status |
|---|---|
| Nine tasks, Qwen3-32B (Gemma-3-27B for task 2), seven binary, labels from resampling, ID and OOD test sets | Confirmed from the post and the repo README. |
| Authors state the supervision confound and "only tried GPT-5.2 at medium effort" | Confirmed, both quotes are in the post. |
| "Every trained method beats every untrained GPT-5.2 monitor OOD" averaged over seven tasks | **Overstated.** The post says "Non-LLM methods have a slight lead" by median OOD g-mean², and that non-LLM methods win on 6 of 9 tasks. The ordering is only in a figure. Few-shot monitors also get threshold tuning on val, so they are not fully "untrained". |
| Termination: probes OOD AUC > 0.90, GPT-5.2 says "yes" 93–100% | Confirmed. |
| Repo has text rollouts and splits, no activations or baseline code | README confirmed via raw.githubusercontent. I could not list `datasets/` (github.com is blocked here), so the per-rollout JSON schema and what text the monitors saw are unverified. |
| Tinker prices: Qwen3-8B $0.44/M train, $0.195 prefill; GPT-OSS-20B $0.396 / $0.18; Qwen3-32B retired | Confirmed on the Tinker pricing page today. Both are 32K context. |
| OpenRouter: gpt-5.2 $1.75 / $14; gpt-6-luna $0.10 / $0.50, 1.05M context | Confirmed, with one omission: **gpt-6-luna doubles to $0.20/M input above 272k prompt tokens.** |
| Not already done | Not found, but weakly checked. The WebSearch budget for this session was exhausted, so I only ran arXiv API queries; OpenReview is still behind a challenge, so the ICML PDF remains unread. Nothing on arXiv runs trained text readers on this benchmark. |

Related work the proposal cites correctly but underweights: arXiv 2507.12428 already compared fine-tuned text classifiers with linear probes on CoT and found the probe ahead by about 13 F1. So "the gap survives training" has a published precedent in a neighbouring setting, and "the gap closes" would be the more surprising direction.

## 1. Would it get upvoted?

Borderline, roughly 35–40% to clear 50 karma.

- The parent post got 59 with Neel Nanda as an author and two comments. A follow-up from unknown authors on a benchmark with little visible uptake starts below that.
- What could carry it: a crisp, slightly adversarial headline ("the hard CoT interp tasks mostly measure supervision") with one clean figure. Monitoring and interp readers do care whether "white-box beats reading the CoT" claims survive a fair baseline.
- What caps it: the authors already conceded the confound in the post, and TF-IDF (a trained text method) is already competitive or best on several tasks. A reader can reasonably say "we knew that". The post needs a result that is not implied by the TF-IDF bars.
- The "gap survives" branch is higher-value but less likely, and an 8B reader failing does not certify that activations are needed.

## 2. Naturalness

Mainline. The post explicitly invites new methods on the benchmark and names this confound; a trained text reader is the obvious missing cell. It is not contrived.

The risk is the opposite of contrived: it is obvious enough that the authors may have done it in the ICML workshop version (abstract mentions an agent, a human baseline and an ensemble, not fine-tuned readers). That PDF is unread by both the proposer and me. Step 1 handles this correctly, but the pivot ("go to the stage-2 items") is not a costed plan.

## 3. Pre-mortem

**How the two days likely go.** Data download and harness are fine. TF-IDF replication is approximate, because published numbers exist only in figures and the authors' hyperparameters and input format are not released. LoRA readers train without trouble. The termination reader reaches high AUC, as TF-IDF already does. On tasks 3 and 6 everything is near chance. On tasks 4–5 readers do well ID and drop OOD, like every other method. The probe anchor gets cut or comes in below the published probes. The write-up is a seven-row table where most rows say "no significant difference".

Rough forecast:

| Outcome | Probability |
|---|---|
| Clear "gap closes", including a decisive result on termination | 30% |
| Clear "gap survives" on two or more tasks, with a properly trained reader | 10% |
| Ambiguous: wide CIs, no paired probe scores, weak anchor | 45% |
| Fails to run or stalls at the replication gate | 15% |

Specific failure modes, most important first:

1. **On the proposal's own primary metric, there is little gap to close on most tasks.** Reading the post task by task, by AUC:
   - Termination: large probe advantage over GPT-5.2, but TF-IDF also does well.
   - Self-deletion: "AUC is similar across the probes and the confidence monitors"; the g-mean² gap is threshold tuning.
   - Follow-up and atypical answer: everything near chance.
   - Sycophancy: ID parity (linear 0.809, few-shot 0.825); OOD collapse attributed to thresholds.
   - Hint: monitors lead ID (0.77 vs 0.66); attention probe leads OOD (0.67).
   - Length: LLM monitors and attention probe best.

   So "within the probe's CI on at least five of seven tasks" is close to guaranteed before any training, and proves nothing. The informative tasks are termination, hint OOD, and perhaps self-deletion.

2. **Test sets are too small for unpaired comparison.** Tasks 1–3 have 58, 100 and 86/88 test items; AUC CIs are about ±0.07–0.12. "Within the CI" is nearly automatic and "more than 0.10 with CI excluding zero" is nearly impossible, unless the comparison is paired on per-item scores. Per-item probe scores exist only if the team trains its own probes, which is the step marked "cut first". Tasks 4–5 OOD have only 20–98 distinct questions.

3. **Home-made probe anchor is weaker than the published probes.** The authors swept layers, aggregation and probe type; a single mid-layer linear probe may underperform, especially where the attention probe was best (hint OOD, length). A "gap closes" claim against a weak anchor is not credible. Task 2 needs Gemma-3-27B as well, which the plan drops.

4. **Replication gate has no objective pass condition.** "Do not proceed until TF-IDF matches within noise" against values read off a bar chart, with unknown tokenisation, n-gram range and input text, can absorb half a day. Whether monitors saw the question or hint alongside the CoT is not determinable from the README.

5. **The termination result is predictable.** A fine-tuned LM matching a bag of words is expected. The train label is a distance-to-`</think>` proxy, while the test set is built from hard negatives that look about to end and is length-balanced. A reader could plausibly do worse than probes here, which would be interesting, but the default expectation is parity.

6. **Many-shot arm is under-elicited and may not fit.** gpt-6-luna is the cheap tier, and the claim being tested is about what a strong reader can do in context. At 256 shots with 1.5–2.5k-token examples the prompt is 380–640k tokens; termination prefixes and full CoTs on tasks 4–7 may be longer and can exceed 1.05M. Tasks 1–2 train labels are proxies, so shots should come from a resampling-labelled split, which collides with using val for thresholds.

7. **"Gap survives" is not identifiable with an 8B/20B reader.** The proposal admits the size mismatch and defers the fix to stage 2. In stage 1 a surviving gap can only be reported as "these readers did not close it".

8. **Prompt memorisation on tasks 4–6.** Labels there are partly a property of the question (how often Qwen follows the hint on that item). A fine-tuned reader can learn question identity ID and fail OOD. The audit in step 7 catches this, but it means ID numbers on those tasks are uninformative.

## 4. Cost check

The estimate is roughly right; I get **$400–480**, at the top of the cap.

- LoRA training: prices correct. The table budgets about 1.5 epochs per reader and no learning-rate or rank sweep. Under-training is the named main risk, so a small sweep is needed: add about $60–100.
- Many-shot: the 256-shot calls fall in the $0.20/M tier. Uncached worst case is about $100–110, not $65. With prompt caching on a fixed shot prefix (cache read $0.01–0.02/M) it falls to about $15–25. The plan should require the fixed-prefix design.
- GPT-5.2 replication at $55 is poor value: 60 items per cell cannot validate anything to better than ±0.1. Cut to the two or three tasks that matter, about $20.
- GPU: 12 h × $3 is fine for Qwen3-32B in bf16 on one 80GB card (about 66 GB of weights, tight). Add about $20 if Gemma-3-27B is included for task 2.

## 5. Recommended changes

1. **Refocus the headline on the tasks with an established probe advantage.** Pre-register termination, hint (OOD) and self-deletion as the decision tasks. Report tasks 3 and 6 as "no method works" and do not count them toward "gap closes". Replace the five-of-seven criterion with paired per-item differences on the decision tasks.
2. **Make the probe anchor mandatory for the decision tasks, and make it strong.** Sweep layers and include an attention probe, at least on termination and hint. Gate it: the team's probes must reach the published level (OOD AUC above 0.90 on termination) before any "closes" claim. If something must be cut, cut GPT-OSS-20B, the rubric monitor and the embedding baseline first.
3. **Time-box the replication gate** to about three hours with a stated tolerance (for example within 0.05 of the plotted value). If it fails, proceed and report own-harness numbers for every method rather than mixing in published ones.
4. **Add one strong many-shot condition.** Run the best affordable frontier model on termination and hint at one shot count, with a fixed cached shot prefix. This is the arm that tests whether the monitor failure is fixable without fine-tuning, and it is the part least implied by the existing TF-IDF bars.
5. **Fix the over-statement in section 1.** Say "slight lead by median OOD g-mean²", and note that the self-deletion and sycophancy gaps are threshold effects according to the authors.
6. **State the limit of the "survives" branch** in section 5: with 8B and 20B readers it supports "not closed by these readers", not "needs activations". Consider pulling one Qwen3-32B self-reader run on termination into stage 1 if the GPU is already rented.
7. **Write the pivot down.** If the ICML PDF already contains trained text readers, name which single stage-2 item becomes stage 1 (cross-subject-model transfer is the most self-contained) and give it a budget.
8. **Budget a small hyperparameter sweep** for the fine-tuned readers and trim the GPT-5.2 replication to pay for it.
9. Cite arXiv 2507.12428 as the closest precedent in the motivation, since it sets the prior that probes beat fine-tuned text classifiers.
