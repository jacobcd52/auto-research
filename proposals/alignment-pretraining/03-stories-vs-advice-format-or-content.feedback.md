# Feedback: "Why does advice beat stories tenfold? Separating content, first-person chat format and training stage"

Reviewer verdict: **keep, with design changes** (the question is right; the conversion design as written is likely to
produce a table nobody can read cleanly).

What I checked (2026-11-14):
- Read the Teaching Qwen Why (TQW) post and its comments, the code README, `training/fsdp/README.md`, the eval README
  and the dataset README; listed the `SecondLookResearch` HF org (46 adapters; all four named in the proposal exist;
  `Qwen/Qwen2.5-32B` is public, Apache-2.0); listed the dataset tree (`stories/training`, `stories/generated`,
  `difficult_advice/gpt-5.6-terra-3000` all present).
- Recomputed AM rates from `eval_scores/conditions.csv`: the proposal's numbers are right (baseline 0.61, stories
  Sonnet 0.427, nano-3m 0.459, advice Terra-3000 0.058).
- OpenRouter prices: Sonnet 5.5 batch $1/$5, Terra batch $1/$6, Haiku 5.5 $0.10/$0.50, Sonnet 4.6 $3/$15 all confirmed.
  RunPod H200 price taken from NOTES, not re-fetched.
- Anthropic's "Teaching Claude Why" page: the document-vs-chat claim is accurately summarised (documents win on
  recall/hallucination evals; on the open-ended behavioural eval the gap nearly closes).
- Prior-work search: the general web-search tool was out of budget for this session, so the duplicate check is
  limited to the TQW comment thread (nobody announces this experiment) and four arXiv API queries (no hits for
  TQW follow-ups; one adjacent paper, arXiv 2607.26173 "Shared SFT Lessons Across Alignment, Model Organisms, and
  Toy Models", which I did not read). **Not checked:** LessWrong/AF posts after 2 Nov, Second Look's own site.
  The proposer's "none found" claim is therefore unrefuted but only weakly re-verified.

## 1. Would it get upvoted?

Plausibly, but not comfortably. TQW itself got 111 karma with a known lab-adjacent team and 46 released adapters; a
follow-up ablation by an unknown author typically earns a fraction of the parent. I would put it at roughly 40-50%
to clear 50 karma **if** the result is a clean, readable table, and 15% if it is "all cells between 20% and 35%".

Who cares: the TQW authors (they name the confound in the main text and in the discussion), people working on
MSM/SDF vs SFT (GDM, Geodesic, Arcadia), and readers of "The models have no plan" who want any evidence at all on
"the model plays itself". The outcome that would do best is the counter-intuitive one: story content as
first-person chat reaching <=20%, or advice-as-documents staying low. The outcome that would do worst is "chat
format after instruct tuning works better than documents", because that is already the stated belief of TCW, GDM's
SDF post and TQW's own discussion; a confirmation needs to be very clean to be worth a post.

One fact from the released scores undermines the headline framing and should be in the proposal: **the tenfold gap
is a Terra-at-3,000 phenomenon, not an advice-vs-stories phenomenon.** Sonnet-written advice at 1,000 conversations
scores 0.444, which is indistinguishable from Sonnet-written stories (0.427). Terra advice at 500 conversations
scores 0.489. So "advice" only beats "stories" when the teacher is Terra and the dose is large. A reader who knows
this will ask whether the experiment is really measuring format or just re-measuring the teacher effect.

## 2. Naturalness

Mainline. The TQW authors write: "these comparisons do not isolate which aspect of each training method makes it
more effective. The two datasets differ in format, training stage, and how closely they resemble the evaluation
settings." This is the obvious next experiment and I found no sign it has been done.

Two caveats:
- The authors list **three** confounds; the proposal's "content" factor silently absorbs the third (closeness to
  the eval: ethical-dilemma focus, which is also the top comment's worry). That is fine as long as the write-up says
  "content" means "everything that survives the format conversion", not "ethical reasoning vs narrative".
- The tie to "The models have no plan" is thin. C3 is teacher-written role-play in fable settings, not self-authored
  fiction about realistic high-stakes deployment. Sell it as a format ablation of TQW; mention Fiora's post in one
  sentence, do not headline it.
- Overlap with sibling proposal 02 (teacher effect): its paraphrase arm and this proposal's C5 both test "does
  rewriting Terra's advice destroy it". If both are funded, C5 should be dropped here and borrowed from there, or
  the two should agree on one rewriter.

## 3. Pre-mortem

Forecast for the plan as written:
- Clear positive result (one factor obviously dominates, interpretable): **25%**
- Clear negative that is still interesting (e.g. neither conversion moves anything; conversions verified good): **15%**
- Ambiguous mush (cells in the 20-45% band, rewriter control off, effects not separable): **45%**
- Fails to run / runs out of time before the anchor cells are done: **15%**

Why mush is the modal outcome:

1. **The rewriter will probably break the advice.** TQW's 2x2 shows the response *writer* accounts for 23-30pp
   (Terra 0.12 vs Sonnet 0.39 at 135 examples; swapping prompts barely matters). The plan has Sonnet 5.5 rewrite all
   3,000 Terra responses. A Sonnet-family paraphrase of Terra's advice may land anywhere from 6% to 40%. The proposal
   anticipates this (C5) but treats it as a fallback narrative. If C5 comes in at 30%, the dynamic range for C1 vs C5
   is gone and the post becomes a worse version of proposal 02.
2. **Dose is steep and the cells are not dose-matched.** From the released scores: Terra advice 500 / 1,000 / 2,000 /
   3,000 = 0.49 / 0.21 / 0.11 / 0.06; 285 examples at 5 / 10 epochs = 0.17 / 0.04. A 2x change in effective
   optimisation moves the rate by 10-30pp. The cells differ in epochs (documents 2, chats 1), loss mask (all tokens
   vs assistant turns only) and token count (advice chats are ~1.8K tokens each by my count of `train-3000.jsonl`,
   ~5.4M tokens total, vs 3M for the story cells). Any "format effect" under 20pp is inside what a dose mismatch
   would produce. The 30% token-mismatch rule in the risks section is not enough.
3. **C3 changes three things at once.** Stories -> first-person chat changes (a) person, (b) chat template /
   assistant token, (c) which text carries loss (narration and consequences move into user turns and are unsupervised).
   The proposal's headline contrast "C3 vs released stories" additionally changes stage, corpus size (3M vs 14M),
   epochs and rewriter. The only clean contrast for story content is C3 vs C4, and C4 is un-rewritten while C3 is
   rewritten, so there is no rewriter control on the story side at all.
4. **The story content is awkward to convert.** The stories are 600-1,000-word fables, folk tales and dramas about a
   "superintelligent AI" in a fishing village or on a night train. As chats they become role-play prompts with a
   scene-setting user and a prose-narrating assistant. That is neither natural chat nor the agentic tool-use format of
   the eval. A null for C3 would say "fable role-play does not transfer", not "stories are weak in any format".
   Also, 30% of the released Sonnet stories are **already first-person by the AI** (confirmed in
   `stories/generated/stories-sonnet-5-kept.jsonl`, `metadata.pov`), which the proposal does not mention or use.
5. **Document training after instruct tuning (C1, C4)** is the regime GDM reports as fragile. If the acting rate
   drops, the remedy (10% replay) changes the cell again.
6. **Expected result is the unsurprising one.** My guess at the numbers: C5 20-35%, C1 35-50%, C2 45-55%, C3 30-45%,
   C4 40-50%. Read honestly, that says "chat after instruct tuning helps somewhat, rewriting hurts a lot, stories
   stay mediocre" - true, modest, and expected.

Things that are *not* big risks: sampling noise (810 transcripts per model gives ~1.7pp SE, and the nano story ladder
3M-112M spans only 0.441-0.477 across five separately trained models, so run-to-run noise is ~1-2pp); artefact
availability (all public); judge cost.

Infrastructure risk is real but ordinary: the TQW stories and baseline launchers default to **4xH200** and the
advice launcher to 2xA100; the proposal assumes one H200 for everything at an unmeasured 2K tokens/s. FlashAttention-3
compiles for about an hour on a new pod (there is an `--attn sdpa` fallback). The eval needs the graft, explicit
stop-token ids and an SSH tunnel. The instruct mix must be rebuilt for C2. The batch API is on the critical path.
Two days is enough only if nothing needs a second attempt, and C2 (the longest cell) is scheduled last.

## 4. Cost check

The estimate is roughly right; I get **$300-380** for the plan as written, still under the cap.
- GPU: single-GPU throughput with gradient checkpointing is more likely 1-1.5K tokens/s than 2K. Token counts are
  also low in places (C1 is ~5.4M tokens x 2 epochs, about 1.5-2.5 h, not 50 min; C2 is ~29M tokens, 5-8 h). I get
  25-35 GPU-hours including the one-hour FA3 build and 250 GB disk, i.e. **$130-185** at $5.29/h.
- Conversions: ~16M in / ~13-14M out -> **$80-90** on Sonnet 5.5 batch. Fine.
- Judging: TQW's judge is Sonnet 4.6. Switching to Haiku 5.5 with a 600-transcript calibration is a new source of
  doubt for $60 saved. 11 evals x 810 x ~$0.021 = ~$190 non-batch, ~$95 on batch ($1.5/$7.5). I would pay for the
  same judge as the anchors on batch and drop the calibration step.
- With the changes below (no LLM rewriting for the core cells) the conversion line falls to near zero and the total
  is about **$250**.

## 5. Recommended changes (in order of importance)

1. **Make the core format manipulation verbatim, with no rewriter.** Take the 3,000 Terra advice conversations and
   render the *same text* as a plain document: a transcript or case write-up with a one-line third-person frame
   ("A user wrote to an AI model: ... The AI replied: ..."), no ChatML tokens, trained through `train_stories.py`.
   Content is then identical by construction, C5 becomes unnecessary, the batch API leaves the critical path and
   ~$80 is saved. Run it with (i) loss on all tokens and (ii) loss on the AI's reply only, so the loss mask is
   separated from the template. This one change removes the largest threat (item 1 of the pre-mortem).
   Keep one LLM-rewritten third-person-narrative version as a secondary cell only if time remains, using **Terra**
   as rewriter, not Sonnet.
2. **Dose-match every contrast.** Same number of epochs and comparable supervised tokens within a contrast; report
   supervised-token counts per cell. Better still, run the two key advice cells at two doses (1,000 and 3,000)
   because the dose curve is steep and a single point cannot distinguish "format halves the efficiency" from
   "format caps the effect".
3. **Use the free first-person story subset.** About 30% of the ~12K kept Sonnet stories are first-person by the AI:
   enough for a 3M-token first-person-document corpus and a matched 3M-token third-person-document corpus, no
   conversion. Training both at the same stage isolates *person* from *chat template*, which is the SPP claim and
   the Fiora claim, at zero data cost. Then C3 (chat) vs first-person-document isolates the template/assistant-token.
4. **Restate the contrasts.** The clean ones are: advice chat vs advice verbatim document, both after (format);
   advice document after vs before (stage); first-person vs third-person story documents (person); stories chat vs
   first-person story documents (template); stories document after vs released stories 3M (stage). Drop "C3 vs
   released stories" as a key contrast; it confounds five things.
5. **Fix the framing.** State up front that Sonnet advice at 1,000 conversations (0.444) equals Sonnet stories
   (0.427), so the gap to be explained is Terra-advice-at-scale vs everything else, and that "content" includes
   teacher and eval-closeness. Change the title accordingly; "tenfold" invites the objection.
6. **Reorder for the two-day clock.** Gate (baseline + released advice on 6 conditions) -> advice-document cells
   (after-stage, no conversion needed, ~1.5 h each) -> story person cells -> C2 (before-stage, longest) -> C3 last,
   since it is the only cell that needs an LLM conversion and has the weakest interpretation. Measure tokens/s in
   the first hour and cut cells by that number, not by the estimate. Decide in advance which cells are dropped if
   throughput is 1K tokens/s.
7. **Keep the published judge** (Sonnet 4.6, batch) so new cells are comparable with the released anchors without a
   calibration argument. Re-evaluate at most two anchors rather than three; the released per-condition scores at
   n=100 are better than a fresh n=30.
8. **Pre-register what a boring result is.** If advice-as-verbatim-document after instruct tuning lands within
   10pp of advice chat, say "chat template does not matter, content does" - that is the surprising, postable
   result. If it lands above 40%, the post is "the assistant-turn format is doing the work even for identical text",
   which is expected but now cleanly shown. Both are reportable; the rewritten-corpus version of the experiment
   cannot distinguish either from rewriter damage.
9. Drop the 100-item constitution-knowledge quiz unless it already exists in the TQW repo (I did not find one in the
   README); building it is an unbudgeted side task. Acting rate and AM-given-acting are enough.

If the funder must choose between this and sibling proposal 02, note that they share the "does rewriting Terra's
text preserve its effect" question; with change 1 applied, this proposal no longer depends on that answer and the
two become complementary.
